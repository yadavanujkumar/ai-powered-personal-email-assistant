import unittest
from unittest.mock import patch, MagicMock
from email_handler import EmailHandler

class TestEmailHandler(unittest.TestCase):
    @patch('email_handler.build')
    def test_fetch_emails(self, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.users().messages().list().execute.return_value = {
            'messages': [{'id': '1'}, {'id': '2'}]
        }
        mock_service.users().messages().get().execute.side_effect = [
            {'snippet': 'Email 1'},
            {'snippet': 'Email 2'}
        ]

        handler = EmailHandler()
        handler.service = mock_service
        emails = handler.fetch_emails()

        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0]['snippet'], 'Email 1')
        self.assertEqual(emails[1]['snippet'], 'Email 2')