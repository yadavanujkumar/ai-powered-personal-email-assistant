import unittest
from ai_engine import AIAssistant

class TestAIAssistant(unittest.TestCase):
    def setUp(self):
        self.ai_assistant = AIAssistant()

    def test_summarize_email(self):
        content = "This is a long email content that needs to be summarized."
        summary = self.ai_assistant.summarize_email(content)
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)

    def test_generate_reply(self):
        content = "This is an email that needs a reply."
        reply = self.ai_assistant.generate_reply(content)
        self.assertIsInstance(reply, str)
        self.assertTrue(len(reply) > 0)