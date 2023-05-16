import uuid
from typing import Any

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):  # type:ignore
    """UserManager class."""

    def create_user(self, email: str, password: str, **extra_fields: dict[str, Any]) -> AbstractUser:
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: dict[str, Any]) -> AbstractUser:
        """Create and return a `User` with superuser (admin) permissions."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # type:ignore
    email = models.EmailField(db_index=True, unique=True)
    thumbnail = models.ImageField(upload_to='users/', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()  # type:ignore

    def __str__(self) -> str:
        """Return a string representation of this User."""
        string = self.email if self.email != '' else self.get_full_name()
        return f'{self.id} {string}'


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True)
    github_link = models.CharField(max_length=20000, null=True)
    birth_date = models.DateField(null=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self) -> str:
        """Return a string representation of this UserProfile."""
        string = self.user.email if self.user.email != '' else self.user.get_full_name()
        return f'<UserProfile {self.id} {string}>'


@receiver(post_save, sender=User)
def update_user_profile_signal(sender: Any, instance: User, created: bool, **kwargs: dict[str, Any]) -> None:
    """Create or update UserProfile model after each user gets created or updated."""
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class Series(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20000)
    image = models.ImageField(upload_to='series/')

    class Meta:
        verbose_name_plural = 'Series'

    def __str__(self) -> str:
        """Return a string representation of this model."""
        return self.name


class Articles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20000)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'Articles'

    def __str__(self) -> str:
        """Return a string representation of this model."""
        return self.title
