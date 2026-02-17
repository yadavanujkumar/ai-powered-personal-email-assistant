"""Configuration management for the AI Email Assistant."""
import os
from typing import Dict, Any

class Config:
    """Application configuration."""
    
    # Flask configuration
    FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Email configuration
    MAX_EMAILS = int(os.environ.get('MAX_EMAILS', 10))
    
    # AI Model configuration
    SUMMARIZATION_MODEL = os.environ.get('SUMMARIZATION_MODEL', 'facebook/bart-large-cnn')
    TEXT_GENERATION_MODEL = os.environ.get('TEXT_GENERATION_MODEL', 'gpt2')
    SENTIMENT_MODEL = os.environ.get('SENTIMENT_MODEL', 'distilbert-base-uncased-finetuned-sst-2-english')
    
    # AI parameters
    SUMMARY_MAX_LENGTH = int(os.environ.get('SUMMARY_MAX_LENGTH', 130))
    SUMMARY_MIN_LENGTH = int(os.environ.get('SUMMARY_MIN_LENGTH', 30))
    REPLY_MAX_LENGTH = int(os.environ.get('REPLY_MAX_LENGTH', 100))
    
    # Priority thresholds
    HIGH_PRIORITY_KEYWORDS = [
        'urgent', 'asap', 'important', 'critical', 'immediately',
        'deadline', 'emergency', 'priority', 'action required'
    ]
    
    # Category keywords
    CATEGORY_KEYWORDS: Dict[str, list] = {
        'work': ['meeting', 'project', 'deadline', 'report', 'presentation', 'colleague'],
        'personal': ['family', 'friend', 'dinner', 'birthday', 'vacation', 'weekend'],
        'finance': ['invoice', 'payment', 'bank', 'transaction', 'receipt', 'bill'],
        'promotions': ['sale', 'discount', 'offer', 'deal', 'shopping', 'promo'],
        'social': ['facebook', 'twitter', 'linkedin', 'instagram', 'notification', 'like']
    }
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'flask_host': cls.FLASK_HOST,
            'flask_port': cls.FLASK_PORT,
            'debug': cls.DEBUG,
            'max_emails': cls.MAX_EMAILS,
            'summarization_model': cls.SUMMARIZATION_MODEL,
            'text_generation_model': cls.TEXT_GENERATION_MODEL,
            'sentiment_model': cls.SENTIMENT_MODEL
        }
