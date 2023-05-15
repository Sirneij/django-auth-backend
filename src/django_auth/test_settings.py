from django.test import override_settings

common_settings = override_settings(
    STORAGES={
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
    },
    DEFAULT_FROM_EMAIL='admin@example.com',
    PASSWORD_HASHERS=('django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',),
)