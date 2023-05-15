from unittest.mock import patch

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from django_auth.test_settings import common_settings
from tests.users.test_models import UserFactory


@common_settings
class RequestPasswordChangeViewTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse('users:request_password_change')
        self.client = Client()

    def test_request_change_password_empty_email(self):
        """Test when data (email) is empty."""
        data_empty_email = {}
        response = self.client.post(path=self.url, data=data_empty_email, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Email field is empty')

    def test_request_change_password_invalid_email(self):
        """Test when data (email) is invalid."""
        data_invalid_email = {'email': 'john@example'}
        response = self.client.post(path=self.url, data=data_invalid_email, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Enter a valid email address.')

    def test_request_change_password_user_does_not_exist(self):
        """Test when the user does not exist (not active)."""
        user = UserFactory.create(email='john@example.com')
        user.is_active = False
        user.save()

        data_correct = {'email': user.email}

        response = self.client.post(path=self.url, data=data_correct, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()['error'],
            'An active user with this e-mail address does not exist. '
            'If you registered with this email, ensure you have activated your account. '
            'You can check by logging in. If you have not activated it, '
            f'visit {settings.FRONTEND_URL}/auth/regenerate-token to '
            'regenerate the token that will allow you activate your account.',
        )

    def test_request_change_password_success(self):
        """Test request change password success."""
        user = UserFactory.create(email='john@example.com')
        data_correct = {'email': user.email}

        with patch('users.views.password.request_change.send_email_message.delay') as send_email_message:
            response = self.client.post(path=self.url, data=data_correct, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['message'],
            'Password reset instructions have been sent to your email address. '
            'Kindly take action before its expiration',
        )

        send_email_message.assert_called_once()
