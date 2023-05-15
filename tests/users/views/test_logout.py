from django.test import Client, TestCase
from django.urls import reverse

from django_auth.test_settings import common_settings
from tests.users.test_models import UserFactory


@common_settings
class LogoutViewTests(TestCase):
    def test_logout_success(self):
        """Test logout success."""
        self.client = Client()
        self.url_login = reverse('users:login')
        self.user = UserFactory.create(email='john@example.com')
        self.user.set_password('12345SomeData')
        self.user.save()

        self.data = {'email': self.user.email, 'password': '12345SomeData'}

        response = self.client.post(
            path=self.url_login,
            data=self.data,
            content_type='application/json',
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.url = reverse('users:logout')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'You have successfully logged out')
