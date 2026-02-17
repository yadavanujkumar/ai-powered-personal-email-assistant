"""Main Flask application for AI Email Assistant."""
from flask import Flask, request, jsonify, render_template
from email_handler import EmailHandler
from ai_engine import AIAssistant
from config import Config
from utils import setup_logging
import logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
email_handler = EmailHandler()
ai_assistant = AIAssistant()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get application configuration."""
    try:
        return jsonify(Config.to_dict())
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        return jsonify({"error": "Failed to get configuration."}), 500

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """Fetch emails from Gmail."""
    try:
        emails = email_handler.fetch_emails()
        return jsonify({"emails": emails, "count": len(emails)})
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        return jsonify({"error": "Failed to fetch emails.", "details": str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize_email():
    """Summarize an email."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required."}), 400
        
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        
        summary = ai_assistant.summarize_email(email_content)
        return jsonify({"summary": summary, "success": True})
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error summarizing email: {e}")
        return jsonify({"error": "Failed to summarize email.", "details": str(e)}), 500

@app.route('/api/reply', methods=['POST'])
def generate_reply():
    """Generate a reply suggestion for an email."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required."}), 400
        
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        
        reply = ai_assistant.generate_reply(email_content)
        return jsonify({"reply": reply, "success": True})
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating reply: {e}")
        return jsonify({"error": "Failed to generate reply.", "details": str(e)}), 500

@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze the sentiment of an email."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required."}), 400
        
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        
        sentiment = ai_assistant.analyze_sentiment(email_content)
        return jsonify({"sentiment": sentiment, "success": True})
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return jsonify({"error": "Failed to analyze sentiment.", "details": str(e)}), 500

@app.route('/api/prioritize', methods=['POST'])
def prioritize_email():
    """Determine the priority level of an email."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required."}), 400
        
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        
        subject = data.get('subject', '')
        priority = ai_assistant.prioritize_email(email_content, subject)
        return jsonify({"priority": priority, "success": True})
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error prioritizing email: {e}")
        return jsonify({"error": "Failed to prioritize email.", "details": str(e)}), 500

@app.route('/api/categorize', methods=['POST'])
def categorize_email():
    """Categorize an email."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required."}), 400
        
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        
        subject = data.get('subject', '')
        category = ai_assistant.categorize_email(email_content, subject)
        return jsonify({"category": category, "success": True})
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error categorizing email: {e}")
        return jsonify({"error": "Failed to categorize email.", "details": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_email():
    """Perform complete analysis on an email (sentiment, priority, category)."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required."}), 400
        
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        
        subject = data.get('subject', '')
        
        # Perform all analyses
        sentiment = ai_assistant.analyze_sentiment(email_content)
        priority = ai_assistant.prioritize_email(email_content, subject)
        category = ai_assistant.categorize_email(email_content, subject)
        
        return jsonify({
            "sentiment": sentiment,
            "priority": priority,
            "category": category,
            "success": True
        })
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error analyzing email: {e}")
        return jsonify({"error": "Failed to analyze email.", "details": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info(f"Starting AI Email Assistant on {Config.FLASK_HOST}:{Config.FLASK_PORT}")
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.DEBUG)
