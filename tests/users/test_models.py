import pytest
from django.test import TestCase
from factory.django import DjangoModelFactory

from users.models import User, UserProfile


class UserFactory(DjangoModelFactory):
    first_name = 'John'
    last_name = 'Doe'
    is_active = True

    class Meta:
        model = User
        django_get_or_create = ('email',)


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create = ('user',)


class UserModelTests(TestCase):
    def setUp(self):
        """Test Setup."""
        self.user = UserFactory.create(email='john@example.com')

    def test_str_representation(self):
        """Test __str__ of user."""
        self.assertEqual(str(self.user), f'{self.user.id} {self.user.email}')


class UserProfileModelTests(TestCase):
    def setUp(self):
        """Test Setup."""
        self.user = UserFactory.create(email='john@example.com')
        self.user_profile = UserProfileFactory.create(user=self.user)

    def test_str_representation(self):
        """Test __str__ of user."""
        self.assertEqual(
            str(self.user_profile),
            f'<UserProfile {self.user_profile.id} {self.user_profile.user.email}>',
        )

    def test_create_user_success(self):
        """Test create_user method."""
        user = User.objects.create_user(email='nelson@example.com', password='123456Data')
        self.assertEqual(user.email, 'nelson@example.com')

    def test_create_user_failure(self):
        """Test create_user method fails."""

        with pytest.raises(ValueError, match='The Email must be set'):
            User.objects.create_user(email='', password='123456Data')

    def test_create_super_user_success(self):
        """Test create_user method."""
        user = User.objects.create_superuser(email='nelson@example.com', password='123456Data')
        self.assertEqual(user.email, 'nelson@example.com')

    def test_create_super_user_failure(self):
        """Test create_user method fails."""

        with pytest.raises(TypeError, match='Superusers must have a password.'):
            User.objects.create_superuser(email='nelson@example.com', password=None)
