import json
from datetime import timedelta
from typing import Any

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, JsonResponse
from django.urls.base import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.tasks import send_email_message
from users.token import account_activation_token
from users.utils import validate_email


@method_decorator(csrf_exempt, name='dispatch')
class RequestPasswordChangeView(View):
    async def post(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        """Request user password change."""
        data = json.loads(request.body.decode("utf-8"))
        email = data.get('email')

        if email is None:
            return JsonResponse({'error': 'Email field is empty'}, status=400)

        is_valid, error_text = validate_email(email)
        if not is_valid:
            return JsonResponse({'error': error_text}, status=400)

        try:
            user = await get_user_model().objects.filter(email=email, is_active=True).aget()
        except get_user_model().DoesNotExist:
            return JsonResponse(
                {
                    'error': 'An active user with this e-mail address does not exist. '
                    'If you registered with this email, ensure you have activated your account. '
                    'You can check by logging in. If you have not activated it, '
                    f'visit {settings.FRONTEND_URL}/auth/regenerate-token to '
                    'regenerate the token that will allow you activate your account.'
                },
                status=404,
            )

        token = await sync_to_async(account_activation_token.make_token)(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        confirmation_link = (
            f"{request.scheme}://{get_current_site(request)}"
            f"{reverse('users:confirm_password_change_request', kwargs={'uidb64': uid, 'token': token})}",
        )

        subject = 'Password reset instructions'
        ctx = {
            'title': "(Django) RustAuth - Password Reset Instructions",
            'domain': settings.FRONTEND_URL,
            'confirmation_link': confirmation_link,
            'expiration_time': (timezone.localtime() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)).minute,
            'exact_time': (timezone.localtime() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)).strftime(
                '%A %B %d, %Y at %r'
            ),
        }

        send_email_message.delay(
            subject=subject,
            template_name='password_reset_email.html',
            user_id=user.id,
            ctx=ctx,
        )

        return JsonResponse(
            {
                'message': 'Password reset instructions have been sent to your email address. '
                'Kindly take action before its expiration'
            },
            status=200,
        )
