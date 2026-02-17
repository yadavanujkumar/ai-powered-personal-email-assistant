from flask import Flask, request, jsonify, render_template
from email_handler import EmailHandler
from ai_engine import AIAssistant
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
email_handler = EmailHandler()
ai_assistant = AIAssistant()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/emails', methods=['GET'])
def get_emails():
    try:
        emails = email_handler.fetch_emails()
        return jsonify(emails)
    except Exception as e:
        logging.error(f"Error fetching emails: {e}")
        return jsonify({"error": "Failed to fetch emails."}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize_email():
    try:
        data = request.json
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        summary = ai_assistant.summarize_email(email_content)
        return jsonify({"summary": summary})
    except Exception as e:
        logging.error(f"Error summarizing email: {e}")
        return jsonify({"error": "Failed to summarize email."}), 500

@app.route('/api/reply', methods=['POST'])
def generate_reply():
    try:
        data = request.json
        email_content = data.get('content', '')
        if not email_content:
            return jsonify({"error": "Email content is required."}), 400
        reply = ai_assistant.generate_reply(email_content)
        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"Error generating reply: {e}")
        return jsonify({"error": "Failed to generate reply."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)