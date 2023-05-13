from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: get_user_model(), timestamp: int):
        return text_type(user.pk) + text_type(user.email) + text_type(timestamp) + text_type(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
