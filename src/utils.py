"""Utility functions for the email assistant."""
import logging
from typing import Any, Dict

def validate_email_content(content: Any) -> None:
    """
    Validate email content.
    
    Args:
        content: Content to validate
        
    Raises:
        ValueError: If content is invalid
    """
    if not content or not isinstance(content, str):
        raise ValueError("Invalid email content. Content must be a non-empty string.")
    
    if len(content.strip()) == 0:
        raise ValueError("Email content cannot be empty or whitespace only.")

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def format_email_response(email: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format email data for API response.
    
    Args:
        email: Raw email data
        
    Returns:
        Formatted email data
    """
    return {
        'id': email.get('id', ''),
        'snippet': email.get('snippet', ''),
        'subject': email.get('subject', ''),
        'from': email.get('from', ''),
        'date': email.get('date', ''),
        'priority': email.get('priority', 'medium'),
        'category': email.get('category', 'general')
    }

def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
