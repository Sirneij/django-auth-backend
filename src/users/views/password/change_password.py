import json
from typing import Any

from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from users.token import account_activation_token


@method_decorator(csrf_exempt, name='dispatch')
class ChangePasswordView(View):
    async def post(self, request: HttpRequest, **kwargs: dict[str, Any]) -> JsonResponse:
        """Change user password."""
        data = json.loads(request.body.decode("utf-8"))
        password = data.get('password')
        combined = data.get('token')

        try:
            uidb64, token = combined.split(':')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = await get_user_model().objects.aget(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.set_password(password)
            await user.asave(update_fields=['password'])

            return JsonResponse(
                {
                    'message': 'Your password has been changed successfully. Kindly login with the new password',
                }
            )
        return JsonResponse(
            {
                'error': 'It appears that your password request token has expired or previously used',
            }
        )
