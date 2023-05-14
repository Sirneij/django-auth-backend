from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from tests.users.test_models import UserFactory


class RegisterViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.url = reverse('users:register')
        self.client = Client()

        self.data_correct = {
            'email': 'john@example.com',
            'password': 'SomeData12345',
            'first_name': 'John',
            'last_name': 'Idogun',
        }
        self.data_no_first_name = {
            'email': 'john@example.com',
            'password': 'SomeData12345',
            'last_name': 'Idogun',
        }
        self.data_invalid_email = {
            'email': 'john@example',
            'password': 'SomeData12345',
            'first_name': 'John',
            'last_name': 'Idogun',
        }

    def test_register_failure_no_first_name(self):
        """Test when first_name is not present."""
        response = self.client.post(path=self.url, data=self.data_no_first_name, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['error'],
            'All fields are required: email, first_name, last_name, password',
        )

    def test_register_failure_invalid_email(self):
        """Test when email is not valid."""
        response = self.client.post(path=self.url, data=self.data_invalid_email, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['error'],
            'Enter a valid email address.',
        )

    def test_register_failure_user_exists(self):
        """Test when user with such email already exists."""
        UserFactory.create(email='john@example.com')
        response = self.client.post(path=self.url, data=self.data_correct, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['error'],
            'A user with that email address already exists',
        )

    def test_register_success(self):
        """Test when user with such email already exists."""
        with patch('users.views.register.send_email_message.delay') as send_email_message_to_user:
            response = self.client.post(path=self.url, data=self.data_correct, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()['message'],
            'Your account was created successfully. '
            'Check your email address to activate your account as we '
            'just sent you an activation link. Ensure you activate your '
            'account before the link expires',
        )
        send_email_message_to_user.assert_called_once()
