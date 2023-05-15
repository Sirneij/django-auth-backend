from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from django_auth.test_settings import common_settings
from tests.users.test_models import UserFactory


@common_settings
class RegenerateTokenView(TestCase):
    def setUp(self) -> None:
        self.url = reverse('users:regenerate')
        self.client = Client()

    def test_regenerate_token_empty_email(self):
        """Test when data (email) is empty."""
        data_empty_email = {}
        response = self.client.post(path=self.url, data=data_empty_email, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Email field is empty')

    def test_regenerate_token_invalid_email(self):
        """Test when data (email) is invalid."""
        data_invalid_email = {'email': 'john@example'}
        response = self.client.post(path=self.url, data=data_invalid_email, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Enter a valid email address.')

    def test_regenerate_token_user_does_not_exist(self):
        """Test when the user does not exist (active)."""
        user = UserFactory.create(email='john@example.com')

        data_correct = {'email': user.email}

        response = self.client.post(path=self.url, data=data_correct, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()['error'],
            "A user with this e-mail address does not exist. "
            "If you registered with this email, ensure you haven't activated it yet. "
            "You can check by logging in",
        )

    def test_request_change_password_success(self):
        """Test regenerate token success."""
        user = UserFactory.create(email='john@example.com')
        user.is_active = False
        user.save()

        data_correct = {'email': user.email}

        with patch('users.views.regenerate.send_email_message.delay') as send_email_message:
            response = self.client.post(path=self.url, data=data_correct, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['message'],
            'Account activation link has been sent to your email address. ' 'Kindly take action before its expiration',
        )

        send_email_message.assert_called_once()
