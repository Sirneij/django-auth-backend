from typing import Any

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'django-auth/static'
    default_acl = 'public-read'

    def get_accessed_time(self, name: str) -> Any:
        """Override method."""

    def get_created_time(self, name: str) -> Any:
        """Override method."""

    def path(self, name: str) -> Any:
        """Override method."""


class PublicMediaStorage(S3Boto3Storage):
    location = 'media/users/django-auth'
    default_acl = 'public-read'
    file_overwrite = False

    def get_accessed_time(self, name: str) -> Any:
        """Override method."""

    def get_created_time(self, name: str) -> Any:
        """Override method."""

    def path(self, name: str) -> Any:
        """Override method."""
