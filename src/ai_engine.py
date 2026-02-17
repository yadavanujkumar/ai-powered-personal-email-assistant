"""AI Engine for email processing and analysis."""
from transformers import pipeline
from utils import validate_email_content
from config import Config
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AIAssistant:
    """AI Assistant for email processing, summarization, and analysis."""
    
    def __init__(self):
        """Initialize AI models."""
        try:
            logger.info("Initializing AI models...")
            self.summarizer = pipeline('summarization', model=Config.SUMMARIZATION_MODEL)
            self.generator = pipeline('text-generation', model=Config.TEXT_GENERATION_MODEL)
            self.sentiment_analyzer = pipeline('sentiment-analysis', model=Config.SENTIMENT_MODEL)
            logger.info("AI models initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AI models: {e}")
            raise

    def summarize_email(self, content: str) -> str:
        """
        Summarize email content.
        
        Args:
            content: Email content to summarize
            
        Returns:
            Summarized text
        """
        validate_email_content(content)
        try:
            # Truncate content if too long (models have token limits)
            max_input_length = 1024
            if len(content) > max_input_length:
                content = content[:max_input_length]
            
            summary = self.summarizer(
                content, 
                max_length=Config.SUMMARY_MAX_LENGTH, 
                min_length=Config.SUMMARY_MIN_LENGTH, 
                do_sample=False
            )
            return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Error summarizing email: {e}")
            return f"Unable to summarize: {str(e)}"

    def generate_reply(self, content: str) -> str:
        """
        Generate a reply suggestion for an email.
        
        Args:
            content: Email content to reply to
            
        Returns:
            Generated reply text
        """
        validate_email_content(content)
        try:
            # Create a more natural prompt
            prompt = f"Email: {content[:200]}\n\nReply:"
            reply = self.generator(
                prompt, 
                max_length=Config.REPLY_MAX_LENGTH, 
                num_return_sequences=1,
                temperature=0.7
            )
            generated_text = reply[0]['generated_text']
            # Extract only the reply part
            if "Reply:" in generated_text:
                return generated_text.split("Reply:")[-1].strip()
            return generated_text
        except Exception as e:
            logger.error(f"Error generating reply: {e}")
            return f"Unable to generate reply: {str(e)}"
    
    def analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of an email.
        
        Args:
            content: Email content to analyze
            
        Returns:
            Dictionary with sentiment label and score
        """
        validate_email_content(content)
        try:
            # Truncate content if too long
            max_input_length = 512
            if len(content) > max_input_length:
                content = content[:max_input_length]
            
            result = self.sentiment_analyzer(content)[0]
            return {
                'sentiment': result['label'],
                'confidence': round(result['score'], 3)
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'sentiment': 'UNKNOWN',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def prioritize_email(self, content: str, subject: str = '') -> Dict[str, Any]:
        """
        Determine the priority level of an email.
        
        Args:
            content: Email content
            subject: Email subject (optional)
            
        Returns:
            Dictionary with priority level and reasoning
        """
        validate_email_content(content)
        
        try:
            # Combine subject and content
            full_text = f"{subject} {content}".lower()
            
            # Check for high-priority keywords
            priority_score = 0
            matched_keywords = []
            
            for keyword in Config.HIGH_PRIORITY_KEYWORDS:
                if keyword in full_text:
                    priority_score += 1
                    matched_keywords.append(keyword)
            
            # Analyze sentiment - negative emails might need quick attention
            sentiment = self.analyze_sentiment(content)
            if sentiment.get('sentiment') == 'NEGATIVE' and sentiment.get('confidence', 0) > 0.7:
                priority_score += 1
                matched_keywords.append('negative sentiment')
            
            # Determine priority level
            if priority_score >= 2:
                priority = 'high'
            elif priority_score == 1:
                priority = 'medium'
            else:
                priority = 'low'
            
            return {
                'priority': priority,
                'score': priority_score,
                'keywords': matched_keywords,
                'sentiment': sentiment
            }
        except Exception as e:
            logger.error(f"Error prioritizing email: {e}")
            return {
                'priority': 'medium',
                'score': 0,
                'keywords': [],
                'error': str(e)
            }
    
    def categorize_email(self, content: str, subject: str = '') -> Dict[str, Any]:
        """
        Categorize an email into predefined categories.
        
        Args:
            content: Email content
            subject: Email subject (optional)
            
        Returns:
            Dictionary with category and confidence
        """
        validate_email_content(content)
        
        try:
            # Combine subject and content
            full_text = f"{subject} {content}".lower()
            
            # Count keyword matches for each category
            category_scores = {}
            for category, keywords in Config.CATEGORY_KEYWORDS.items():
                score = sum(1 for keyword in keywords if keyword in full_text)
                if score > 0:
                    category_scores[category] = score
            
            # Determine the best category
            if category_scores:
                best_category = max(category_scores, key=category_scores.get)
                total_keywords = sum(category_scores.values())
                confidence = round(category_scores[best_category] / total_keywords, 2)
                
                return {
                    'category': best_category,
                    'confidence': confidence,
                    'all_scores': category_scores
                }
            else:
                return {
                    'category': 'general',
                    'confidence': 1.0,
                    'all_scores': {}
                }
        except Exception as e:
            logger.error(f"Error categorizing email: {e}")
            return {
                'category': 'general',
                'confidence': 0.0,
                'error': str(e)
            }