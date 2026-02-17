import logging

def validate_email_content(content):
    if not content or not isinstance(content, str):
        raise ValueError("Invalid email content.")

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')