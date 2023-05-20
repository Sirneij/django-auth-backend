from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponseRedirect
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from users.token import account_activation_token


class ConfirmPasswordChangeRequestView(View):
    async def get(
        self, request: HttpRequest, uidb64: str, token: str
    ) -> HttpResponseRedirect:
        """Confirm password change requests."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = await get_user_model().objects.aget(pk=uid, is_active=True)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            # Generate a new token
            token = await sync_to_async(account_activation_token.make_token)(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            combined = f'{uid}:{token}'
            return HttpResponseRedirect(
                f'{settings.FRONTEND_URL}/auth/password/change-password?token={combined}'
            )

        return HttpResponseRedirect(
            f'{settings.FRONTEND_URL}/auth/regenerate-token?reason=It appears that '
            'your confirmation token has expired or previously used. Kindly generate a new token',
        )
