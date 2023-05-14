from unittest.mock import patch

from django.test import TestCase
from django.test.utils import override_settings

from tests.users.test_models import UserFactory
from users.tasks import send_email_message


class SendMessageTests(TestCase):
    @override_settings(DEFAULT_FROM_EMAIL='admin@example.com')
    @patch('users.tasks.send_mail')
    def test_success(self, send_mail):
        user = UserFactory.create(email='john@example.com')

        send_email_message(
            subject='Some subject',
            template_name='test.html',
            user_id=user.id,
            ctx={'a': 'b'},
        )
        send_mail.assert_called_with(
            subject='Some subject',
            message='',
            from_email='admin@example.com',
            recipient_list=[user.email],
            fail_silently=False,
            html_message='',
        )
