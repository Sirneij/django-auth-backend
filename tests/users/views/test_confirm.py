from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from tests.users.test_models import UserFactory
from users.token import account_activation_token


class ConfirmViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.client = Client()

    def test_user_failure_is_active(self):
        """Test when user is already active."""
        user = UserFactory.create(email='john@example.com')

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        url = reverse('users:confirm', kwargs={'uidb64': uid, 'token': token})

        response = self.client.get(url, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/auth/regenerate-token')

    def test_user_is_available(self):
        """Test when user is available."""
        user = UserFactory.create(email='john@example.com')
        user.is_active = False
        user.save()

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        url = reverse('users:confirm', kwargs={'uidb64': uid, 'token': token})

        response = self.client.get(url, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/auth/confirmed')

        user.refresh_from_db()
        self.assertTrue(user.is_active)
