from shutil import rmtree
from tempfile import NamedTemporaryFile, mkdtemp

from django.test import Client, TestCase
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone

from django_auth.test_settings import common_settings
from tests.users.test_models import UserFactory


@common_settings
class UserUpdateViewTests(TestCase):
    def setUp(self) -> None:
        """Set up."""
        self.url = reverse('users:profile_update')
        self.client = Client()
        self.media_folder = mkdtemp()

    def tearDown(self):
        rmtree(self.media_folder)

    def test_update_user_not_authenticated(self):
        """Test when user is not authenticated."""
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()['error'],
            'You are not logged in. Kindly ensure you are logged in and try again',
        )

    def test_update_user_success_first_name(self):
        """Test update user success with first_name."""
        # First login
        user = UserFactory.create(email='john@example.com')
        user.set_password('12345SomeData')
        user.save()
        url_login = reverse('users:login')
        login_data = {'email': user.email, 'password': '12345SomeData'}
        response = self.client.post(
            path=url_login, data=login_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], user.email)

        # User update
        data = {'first_name': 'Owolabi'}
        encoded_data = encode_multipart(BOUNDARY, data)
        response = self.client.patch(
            self.url, encoded_data, content_type=MULTIPART_CONTENT
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertEqual(user.first_name, data['first_name'])

    def test_update_user_success_last_name(self):
        """Test update user success with last_name."""
        # First login
        user = UserFactory.create(email='john@example.com')
        user.set_password('12345SomeData')
        user.save()
        url_login = reverse('users:login')
        login_data = {'email': user.email, 'password': '12345SomeData'}
        response = self.client.post(
            path=url_login, data=login_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], user.email)

        # User update
        data = {'last_name': 'Idogun'}
        encoded_data = encode_multipart(BOUNDARY, data)
        response = self.client.patch(
            self.url, encoded_data, content_type=MULTIPART_CONTENT
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()

        self.assertEqual(user.last_name, data['last_name'])

    def test_update_user_success_thumbnail(self):
        """Test update user success with thumbnail."""
        # First login
        user = UserFactory.create(email='john@example.com')
        user.set_password('12345SomeData')
        user.save()
        url_login = reverse('users:login')
        login_data = {'email': user.email, 'password': '12345SomeData'}
        response = self.client.post(
            path=url_login, data=login_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], user.email)

        # Update user
        with override_settings(MEDIA_ROOT=self.media_folder):
            with NamedTemporaryFile() as f:
                f.write(b'some file data')
                f.seek(0)
                data = {'thumbnail': f}
                encoded_data = encode_multipart(BOUNDARY, data)
                response = self.client.patch(
                    self.url, encoded_data, content_type=MULTIPART_CONTENT
                )
                self.assertEqual(response.status_code, 200)

        user.refresh_from_db()

        self.assertIsNotNone(user.thumbnail)

    def test_update_user_success_phone_number(self):
        """Test update user success with phone_number."""
        # First login
        user = UserFactory.create(email='john@example.com')
        user.set_password('12345SomeData')
        user.save()
        url_login = reverse('users:login')
        login_data = {'email': user.email, 'password': '12345SomeData'}
        response = self.client.post(
            path=url_login, data=login_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], user.email)

        # User update
        data = {'phone_number': '+2348145359073'}
        encoded_data = encode_multipart(BOUNDARY, data)
        response = self.client.patch(
            self.url, encoded_data, content_type=MULTIPART_CONTENT
        )
        self.assertEqual(response.status_code, 200)

        user.userprofile.refresh_from_db()

        self.assertEqual(user.userprofile.phone_number, data['phone_number'])

    def test_update_user_success_birth_date(self):
        """Test update user success with birth_date."""
        # First login
        user = UserFactory.create(email='john@example.com')
        user.set_password('12345SomeData')
        user.save()
        url_login = reverse('users:login')
        login_data = {'email': user.email, 'password': '12345SomeData'}
        response = self.client.post(
            path=url_login, data=login_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], user.email)

        # User update
        data = {'birth_date': timezone.localdate()}
        encoded_data = encode_multipart(BOUNDARY, data)
        response = self.client.patch(
            self.url, encoded_data, content_type=MULTIPART_CONTENT
        )
        self.assertEqual(response.status_code, 200)

        user.userprofile.refresh_from_db()

        self.assertEqual(user.userprofile.birth_date, data['birth_date'])

    def test_update_user_success_github_link(self):
        """Test update user success with github_link."""
        # First login
        user = UserFactory.create(email='john@example.com')
        user.set_password('12345SomeData')
        user.save()
        url_login = reverse('users:login')
        login_data = {'email': user.email, 'password': '12345SomeData'}
        response = self.client.post(
            path=url_login, data=login_data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], user.email)

        # User update
        data = {'github_link': 'https://github.com/Sirneij'}
        encoded_data = encode_multipart(BOUNDARY, data)
        response = self.client.patch(
            self.url, encoded_data, content_type=MULTIPART_CONTENT
        )
        self.assertEqual(response.status_code, 200)

        user.userprofile.refresh_from_db()

        self.assertEqual(user.userprofile.github_link, data['github_link'])
