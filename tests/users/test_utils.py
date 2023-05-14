from django.test import TestCase

from users.utils import validate_email


class ValidateEmailTests(TestCase):
    def test_email_empty(self):
        """Test when even is empty."""
        is_valid, message = validate_email('')
        self.assertFalse(is_valid)
        self.assertEqual(message, 'Enter a valid email address.')
