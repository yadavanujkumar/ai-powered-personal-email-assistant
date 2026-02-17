"""Tests for AI Assistant module."""
import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock the transformers module before importing ai_engine
sys.modules['transformers'] = Mock()

from ai_engine import AIAssistant


class TestAIAssistant(unittest.TestCase):
    """Test cases for AIAssistant class."""
    
    @patch('ai_engine.pipeline')
    def setUp(self, mock_pipeline):
        """Set up test fixtures."""
        # Create mock pipelines
        self.mock_summarizer = MagicMock()
        self.mock_summarizer.return_value = [{'summary_text': 'Test summary'}]
        
        self.mock_generator = MagicMock()
        self.mock_generator.return_value = [{'generated_text': 'Reply: Test reply'}]
        
        self.mock_sentiment = MagicMock()
        self.mock_sentiment.return_value = [{'label': 'POSITIVE', 'score': 0.95}]
        
        mock_pipeline.side_effect = [self.mock_summarizer, self.mock_generator, self.mock_sentiment]
        
        self.ai_assistant = AIAssistant()

    def test_summarize_email(self):
        """Test email summarization."""
        content = "This is a long email content that needs to be summarized for testing purposes."
        summary = self.ai_assistant.summarize_email(content)
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)

    def test_summarize_email_with_empty_content(self):
        """Test summarization with empty content."""
        with self.assertRaises(ValueError):
            self.ai_assistant.summarize_email("")

    def test_generate_reply(self):
        """Test reply generation."""
        content = "This is an email that needs a reply for testing purposes."
        reply = self.ai_assistant.generate_reply(content)
        self.assertIsInstance(reply, str)
        self.assertTrue(len(reply) > 0)

    def test_generate_reply_with_empty_content(self):
        """Test reply generation with empty content."""
        with self.assertRaises(ValueError):
            self.ai_assistant.generate_reply("")

    def test_analyze_sentiment(self):
        """Test sentiment analysis."""
        content = "This is a positive email message."
        sentiment = self.ai_assistant.analyze_sentiment(content)
        self.assertIsInstance(sentiment, dict)
        self.assertIn('sentiment', sentiment)
        self.assertIn('confidence', sentiment)
        self.assertEqual(sentiment['sentiment'], 'POSITIVE')

    def test_analyze_sentiment_with_empty_content(self):
        """Test sentiment analysis with empty content."""
        with self.assertRaises(ValueError):
            self.ai_assistant.analyze_sentiment("")

    def test_prioritize_email_high_priority(self):
        """Test high priority email detection."""
        content = "This is an urgent message that requires immediate action."
        subject = "URGENT: Action Required"
        priority = self.ai_assistant.prioritize_email(content, subject)
        
        self.assertIsInstance(priority, dict)
        self.assertIn('priority', priority)
        self.assertIn('score', priority)
        self.assertEqual(priority['priority'], 'high')

    def test_prioritize_email_low_priority(self):
        """Test low priority email detection."""
        content = "This is a regular message."
        subject = "Regular Update"
        priority = self.ai_assistant.prioritize_email(content, subject)
        
        self.assertIsInstance(priority, dict)
        self.assertIn('priority', priority)

    def test_prioritize_email_with_empty_content(self):
        """Test prioritization with empty content."""
        with self.assertRaises(ValueError):
            self.ai_assistant.prioritize_email("")

    def test_categorize_email_work(self):
        """Test work email categorization."""
        content = "Let's schedule a meeting to discuss the project deadline."
        subject = "Project Meeting"
        category = self.ai_assistant.categorize_email(content, subject)
        
        self.assertIsInstance(category, dict)
        self.assertIn('category', category)
        self.assertIn('confidence', category)
        self.assertEqual(category['category'], 'work')

    def test_categorize_email_personal(self):
        """Test personal email categorization."""
        content = "Looking forward to dinner with the family this weekend!"
        subject = "Weekend Plans"
        category = self.ai_assistant.categorize_email(content, subject)
        
        self.assertIsInstance(category, dict)
        self.assertIn('category', category)
        self.assertEqual(category['category'], 'personal')

    def test_categorize_email_general(self):
        """Test general email categorization."""
        content = "This is a generic message with no specific keywords."
        subject = "Update"
        category = self.ai_assistant.categorize_email(content, subject)
        
        self.assertIsInstance(category, dict)
        self.assertEqual(category['category'], 'general')

    def test_categorize_email_with_empty_content(self):
        """Test categorization with empty content."""
        with self.assertRaises(ValueError):
            self.ai_assistant.categorize_email("")


if __name__ == '__main__':
    unittest.main()
