"""Tests for utility functions."""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import validate_email_content, format_email_response, truncate_text

class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_email_content_valid(self):
        """Test validation with valid content."""
        try:
            validate_email_content("This is a valid email content.")
        except ValueError:
            self.fail("validate_email_content raised ValueError unexpectedly!")

    def test_validate_email_content_empty_string(self):
        """Test validation with empty string."""
        with self.assertRaises(ValueError):
            validate_email_content("")

    def test_validate_email_content_whitespace_only(self):
        """Test validation with whitespace only."""
        with self.assertRaises(ValueError):
            validate_email_content("   ")

    def test_validate_email_content_none(self):
        """Test validation with None."""
        with self.assertRaises(ValueError):
            validate_email_content(None)

    def test_validate_email_content_invalid_type(self):
        """Test validation with invalid type."""
        with self.assertRaises(ValueError):
            validate_email_content(12345)
        
        with self.assertRaises(ValueError):
            validate_email_content([])
        
        with self.assertRaises(ValueError):
            validate_email_content({})
    
    def test_format_email_response(self):
        """Test email response formatting."""
        raw_email = {
            'id': '12345',
            'snippet': 'Test email snippet',
            'subject': 'Test Subject',
            'from': 'test@example.com',
            'date': '2024-01-01',
            'priority': 'high',
            'category': 'work'
        }
        
        formatted = format_email_response(raw_email)
        
        self.assertEqual(formatted['id'], '12345')
        self.assertEqual(formatted['snippet'], 'Test email snippet')
        self.assertEqual(formatted['subject'], 'Test Subject')
        self.assertEqual(formatted['from'], 'test@example.com')
        self.assertEqual(formatted['priority'], 'high')
        self.assertEqual(formatted['category'], 'work')
    
    def test_format_email_response_missing_fields(self):
        """Test email response formatting with missing fields."""
        raw_email = {'id': '12345'}
        formatted = format_email_response(raw_email)
        
        self.assertEqual(formatted['id'], '12345')
        self.assertEqual(formatted['snippet'], '')
        self.assertEqual(formatted['priority'], 'medium')
        self.assertEqual(formatted['category'], 'general')
    
    def test_truncate_text_short(self):
        """Test text truncation with short text."""
        text = "This is a short text"
        truncated = truncate_text(text, 100)
        self.assertEqual(truncated, text)
    
    def test_truncate_text_long(self):
        """Test text truncation with long text."""
        text = "This is a very long text " * 50
        truncated = truncate_text(text, 50)
        self.assertEqual(len(truncated), 53)  # 50 + "..."
        self.assertTrue(truncated.endswith("..."))
    
    def test_truncate_text_exact_length(self):
        """Test text truncation with exact length."""
        text = "a" * 100
        truncated = truncate_text(text, 100)
        self.assertEqual(truncated, text)


if __name__ == '__main__':
    unittest.main()
