from transformers import pipeline
from utils import validate_email_content

class AIAssistant:
    def __init__(self):
        self.summarizer = pipeline('summarization')
        self.generator = pipeline('text-generation', model='gpt2')

    def summarize_email(self, content):
        validate_email_content(content)
        summary = self.summarizer(content, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']

    def generate_reply(self, content):
        validate_email_content(content)
        reply = self.generator(f"Reply to: {content}", max_length=50, num_return_sequences=1)
        return reply[0]['generated_text']