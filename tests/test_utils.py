import unittest
from utils import validate_email_content

class TestUtils(unittest.TestCase):
    def test_validate_email_content_valid(self):
        try:
            validate_email_content("This is a valid email content.")
        except ValueError:
            self.fail("validate_email_content raised ValueError unexpectedly!")

    def test_validate_email_content_invalid(self):
        with self.assertRaises(ValueError):
            validate_email_content("")

        with self.assertRaises(ValueError):
            validate_email_content(None)

        with self.assertRaises(ValueError):
            validate_email_content(12345)