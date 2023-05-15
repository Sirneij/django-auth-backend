from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django_auth.test_settings import common_settings
from tests.users.test_models import UserFactory
from users.token import account_activation_token


@common_settings
class ChangePasswordViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.client = Client()

    def test_change_password_success(self):
        """Test when user is active."""
        user = UserFactory.create(email='john@example.com')

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        url = reverse('users:change_password')

        data = {'password': 'SomeOther123456', 'token': f'{uid}:{token}'}

        response = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_change_password_failure_is_not_active(self):
        """Test when user is not active."""
        user = UserFactory.create(email='john@example.com')
        user.is_active = False
        user.save()

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        url = reverse('users:change_password')

        data = {'password': 'SomeOther123456', 'token': f'{uid}:{token}'}

        response = self.client.post(url, data=data, content_type='application/json', follow=True)
        self.assertEqual(
            response.json()['error'],
            'It appears that your password request token has expired or previously used',
        )
