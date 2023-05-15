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
class RegisterView(View):
    async def post(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        """Register users."""
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        # Some validations
        if email is None or password is None or first_name is None or last_name is None:
            return JsonResponse(
                {'error': 'All fields are required: email, first_name, last_name, password'}, status=400
            )

        is_valid, error_text = validate_email(email)
        if not is_valid:
            return JsonResponse({'error': error_text}, status=400)

        user_exists = await get_user_model().objects.filter(email=email).aexists()
        if user_exists:
            return JsonResponse({'error': 'A user with that email address already exists'}, status=400)

        user = await sync_to_async(get_user_model().objects.create_user)(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active = False
        await user.asave(update_fields=['is_active'])

        token = await sync_to_async(account_activation_token.make_token)(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        confirmation_link = (
            f"{request.scheme}://{get_current_site(request)}"
            f"{reverse('users:confirm', kwargs={'uidb64': uid, 'token': token})}",
        )

        subject = 'Please, verify your account'
        ctx = {
            'title': "(Django) RustAuth - Let's get you verified",
            'domain': settings.FRONTEND_URL,
            'confirmation_link': confirmation_link,
            'expiration_time': (timezone.localtime() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)).minute,
            'exact_time': (timezone.localtime() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)).strftime(
                '%A %B %d, %Y at %r'
            ),
        }

        send_email_message.delay(
            subject=subject,
            template_name='verification_email.html',
            user_id=user.id,
            ctx=ctx,
        )

        return JsonResponse(
            {
                'message': 'Your account was created successfully. '
                'Check your email address to activate your account as we '
                'just sent you an activation link. Ensure you activate your '
                'account before the link expires'
            },
            status=201,
        )
