from django.test import Client, TestCase
from django.urls import reverse

from django_auth.test_settings import common_settings
from tests.users.test_models import UserFactory


@common_settings
class LoginViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.url = reverse('users:login')
        self.client = Client()

        self.user = UserFactory.create(email='john@example.com')

        self.data_empty = {}
        self.data_password_not_match = {
            'email': self.user.email,
            'password': 'somedata',
        }
        self.data = {'email': self.user.email, 'password': '12345SomeData'}

    def test_user_login_failure_empty(self):
        """Test user login failure with empty data."""
        response = self.client.post(
            path=self.url, data=self.data_empty, content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Please provide email and password')

    def test_user_login_failure_wrong_password(self):
        """Test user login failure with wrong password"""
        self.user.set_password('12345SomeData')
        self.user.save()
        response = self.client.post(
            path=self.url,
            data=self.data_password_not_match,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Email and password do not match')

    def test_user_login_success(self):
        """Test user login success"""
        self.user.set_password('12345SomeData')
        self.user.save()
        response = self.client.post(
            path=self.url, data=self.data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], self.user.email)
