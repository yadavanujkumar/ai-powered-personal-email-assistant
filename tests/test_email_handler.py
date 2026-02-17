"""Tests for Email Handler module."""
import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock the Google modules before importing email_handler
sys.modules['google'] = Mock()
sys.modules['google.oauth2'] = Mock()
sys.modules['google.oauth2.credentials'] = Mock()
sys.modules['googleapiclient'] = Mock()
sys.modules['googleapiclient.discovery'] = Mock()

from email_handler import EmailHandler

class TestEmailHandler(unittest.TestCase):
    """Test cases for EmailHandler class."""
    
    @patch('email_handler.build')
    @patch('email_handler.Credentials')
    @patch('builtins.open', create=True)
    @patch('email_handler.json.load')
    def test_fetch_emails(self, mock_json_load, mock_open, mock_credentials, mock_build):
        """Test fetching emails."""
        # Mock credentials loading
        mock_json_load.return_value = {'token': 'test_token'}
        mock_credentials.from_authorized_user_info.return_value = MagicMock()
        
        # Mock Gmail API service
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
        emails = handler.fetch_emails()

        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0]['snippet'], 'Email 1')
        self.assertEqual(emails[1]['snippet'], 'Email 2')
    
    @patch('email_handler.build')
    @patch('email_handler.Credentials')
    @patch('builtins.open', create=True)
    @patch('email_handler.json.load')
    def test_fetch_emails_empty(self, mock_json_load, mock_open, mock_credentials, mock_build):
        """Test fetching emails when no emails are found."""
        # Mock credentials loading
        mock_json_load.return_value = {'token': 'test_token'}
        mock_credentials.from_authorized_user_info.return_value = MagicMock()
        
        # Mock Gmail API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.users().messages().list().execute.return_value = {
            'messages': []
        }

        handler = EmailHandler()
        emails = handler.fetch_emails()

        self.assertEqual(len(emails), 0)


if __name__ == '__main__':
    unittest.main()
