from django.test import Client, TestCase
from django.urls import reverse

from tests.users.test_models import UserFactory


class CurrentUserViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.client = Client()
        self.url_login = reverse('users:login')
        self.url = reverse('users:current_user')

    def test_get_current_user_failure_unauthenticated(self):
        """Test get current user failure."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['error'],
            'You are not logged in. Kindly ensure you are logged in and try again',
        )

    def test_get_current_user_success(self):
        """Test get current user success."""
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

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
