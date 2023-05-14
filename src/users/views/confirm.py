from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponseRedirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from users.token import account_activation_token


class ConfirmEmailView(View):
    async def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponseRedirect:
        """Confirm and activate user emails and accounts."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = await get_user_model().objects.aget(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            await user.asave(update_fields=['is_active'])
            return HttpResponseRedirect(f'{settings.FRONTEND_URL}/auth/confirmed')

        return HttpResponseRedirect(
            f'{settings.FRONTEND_URL}/auth/regenerate-token?reason=It appears that'
            'your confirmation token has expired or previously used. Kindly generate a new token',
        )
