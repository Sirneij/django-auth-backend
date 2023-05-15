from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django_auth.test_settings import common_settings
from tests.users.test_models import UserFactory
from users.token import account_activation_token


@common_settings
class ConfirmPasswordChangeRequestViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.client = Client()

    def test_confirm_password_change_request_success(self):
        """Test when user is active."""
        user = UserFactory.create(email='john@example.com')

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        url = reverse('users:confirm_password_change_request', kwargs={'uidb64': uid, 'token': token})

        response = self.client.get(url, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/auth/password/change-password')

    def test_confirm_password_change_request_failure(self):
        """Test when user is inactive."""
        user = UserFactory.create(email='john@example.com')
        user.is_active = False
        user.save()

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        url = reverse('users:confirm_password_change_request', kwargs={'uidb64': uid, 'token': token})

        response = self.client.get(url, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/auth/regenerate-token')
