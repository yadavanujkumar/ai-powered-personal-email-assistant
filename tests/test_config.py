"""Tests for configuration module."""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config

class TestConfig(unittest.TestCase):
    """Test cases for Config class."""
    
    def test_config_defaults(self):
        """Test default configuration values."""
        self.assertEqual(Config.FLASK_HOST, '0.0.0.0')
        self.assertEqual(Config.FLASK_PORT, 5000)
        self.assertTrue(Config.DEBUG)
        self.assertEqual(Config.MAX_EMAILS, 10)
    
    def test_config_models(self):
        """Test AI model configuration."""
        self.assertIsInstance(Config.SUMMARIZATION_MODEL, str)
        self.assertIsInstance(Config.TEXT_GENERATION_MODEL, str)
        self.assertIsInstance(Config.SENTIMENT_MODEL, str)
    
    def test_config_ai_parameters(self):
        """Test AI parameters."""
        self.assertIsInstance(Config.SUMMARY_MAX_LENGTH, int)
        self.assertIsInstance(Config.SUMMARY_MIN_LENGTH, int)
        self.assertIsInstance(Config.REPLY_MAX_LENGTH, int)
        self.assertGreater(Config.SUMMARY_MAX_LENGTH, Config.SUMMARY_MIN_LENGTH)
    
    def test_config_priority_keywords(self):
        """Test priority keywords configuration."""
        self.assertIsInstance(Config.HIGH_PRIORITY_KEYWORDS, list)
        self.assertTrue(len(Config.HIGH_PRIORITY_KEYWORDS) > 0)
        self.assertIn('urgent', Config.HIGH_PRIORITY_KEYWORDS)
        self.assertIn('important', Config.HIGH_PRIORITY_KEYWORDS)
    
    def test_config_category_keywords(self):
        """Test category keywords configuration."""
        self.assertIsInstance(Config.CATEGORY_KEYWORDS, dict)
        self.assertTrue(len(Config.CATEGORY_KEYWORDS) > 0)
        self.assertIn('work', Config.CATEGORY_KEYWORDS)
        self.assertIn('personal', Config.CATEGORY_KEYWORDS)
        self.assertIn('finance', Config.CATEGORY_KEYWORDS)
        
        # Test that each category has keywords
        for category, keywords in Config.CATEGORY_KEYWORDS.items():
            self.assertIsInstance(keywords, list)
            self.assertTrue(len(keywords) > 0)
    
    def test_config_to_dict(self):
        """Test configuration dictionary conversion."""
        config_dict = Config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertIn('flask_host', config_dict)
        self.assertIn('flask_port', config_dict)
        self.assertIn('debug', config_dict)
        self.assertIn('max_emails', config_dict)
        self.assertIn('summarization_model', config_dict)


if __name__ == '__main__':
    unittest.main()
