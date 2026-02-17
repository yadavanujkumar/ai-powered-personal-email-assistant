# AI-Powered Personal Email Assistant

## Overview
This project is an advanced AI-powered personal email assistant that helps users manage their emails efficiently. It uses cutting-edge natural language processing (NLP) to analyze email content, prioritize messages, categorize emails, analyze sentiment, and draft intelligent responses based on user input.

## Features

### 🎯 Core AI Features
- **Email Prioritization**: Automatically categorize emails into high, medium, and low priority based on content analysis and keywords
- **Smart Categorization**: Classify emails into categories (work, personal, finance, promotions, social)
- **Sentiment Analysis**: Detect the emotional tone of emails (positive, negative) with confidence scores
- **Email Summarization**: Transform lengthy emails into concise, actionable summaries
- **Smart Reply Suggestions**: Generate context-aware AI-powered reply suggestions
- **Complete Email Analysis**: Get comprehensive insights including priority, category, and sentiment in one request

### 🎨 User Interface
- **Modern UI**: Beautiful, responsive design with gradient backgrounds and card-based layout
- **Interactive Actions**: Click-to-analyze buttons for each email
- **Real-time Feedback**: Loading states and error messages for better user experience
- **Mobile Responsive**: Optimized for all screen sizes

### 🔧 Technical Features
- **Configurable AI Models**: Environment-based configuration for different AI models
- **Comprehensive Error Handling**: Proper error messages and status codes
- **Input Validation**: Robust validation for all API inputs
- **RESTful API**: Well-structured API endpoints with clear responses
- **Secure Authentication**: OAuth2-based authentication for Gmail

## Tech Stack
- **Backend**: Python 3.8+ with Flask
- **AI/ML**: Transformers library with multiple pre-trained models
  - Summarization: facebook/bart-large-cnn
  - Text Generation: GPT-2
  - Sentiment Analysis: DistilBERT
  - PyTorch: 2.6.0+ (patched for security vulnerabilities)
- **Frontend**: Modern JavaScript (Vanilla JS) with CSS3
- **Containerization**: Docker
- **Testing**: pytest

## Security

This project follows security best practices:
- ✅ **XSS Protection**: Secure DOM manipulation without innerHTML vulnerabilities
- ✅ **Updated Dependencies**: All dependencies updated to patched versions
  - PyTorch upgraded to 2.6.0+ to address heap buffer overflow, use-after-free, and RCE vulnerabilities
- ✅ **Input Validation**: Comprehensive validation for all user inputs
- ✅ **CodeQL Verified**: No security alerts in static analysis

## Setup Instructions

### Prerequisites
- Python 3.8+
- Docker (optional)
- Gmail API credentials (OAuth2)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-powered-personal-email-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Gmail API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the Gmail API.
   - Download the `credentials.json` file and place it in the `src/` directory.

4. (Optional) Configure environment variables:
   ```bash
   export FLASK_HOST=0.0.0.0
   export FLASK_PORT=5000
   export DEBUG=True
   export MAX_EMAILS=10
   export SUMMARY_MAX_LENGTH=130
   export SUMMARY_MIN_LENGTH=30
   ```

5. Run the application locally:
   ```bash
   python src/main.py
   ```

6. Build and run the Docker container:
   ```bash
   docker build -t ai-email-assistant .
   docker run -p 5000:5000 ai-email-assistant
   ```

7. Access the application:
   Open your browser and navigate to `http://localhost:5000`.

## API Endpoints

### GET `/api/config`
Get application configuration.

### GET `/api/emails`
Fetch emails from Gmail.

**Response:**
```json
{
  "emails": [{"id": "...", "snippet": "..."}],
  "count": 10
}
```

### POST `/api/summarize`
Summarize an email.

**Request:**
```json
{
  "content": "Email content to summarize..."
}
```

**Response:**
```json
{
  "summary": "Summarized content...",
  "success": true
}
```

### POST `/api/reply`
Generate a reply suggestion.

**Request:**
```json
{
  "content": "Email content to reply to..."
}
```

**Response:**
```json
{
  "reply": "Suggested reply...",
  "success": true
}
```

### POST `/api/sentiment`
Analyze email sentiment.

**Request:**
```json
{
  "content": "Email content to analyze..."
}
```

**Response:**
```json
{
  "sentiment": {
    "sentiment": "POSITIVE",
    "confidence": 0.95
  },
  "success": true
}
```

### POST `/api/prioritize`
Determine email priority.

**Request:**
```json
{
  "content": "Email content...",
  "subject": "Email subject (optional)"
}
```

**Response:**
```json
{
  "priority": {
    "priority": "high",
    "score": 2,
    "keywords": ["urgent", "important"],
    "sentiment": {...}
  },
  "success": true
}
```

### POST `/api/categorize`
Categorize an email.

**Request:**
```json
{
  "content": "Email content...",
  "subject": "Email subject (optional)"
}
```

**Response:**
```json
{
  "category": {
    "category": "work",
    "confidence": 0.75,
    "all_scores": {...}
  },
  "success": true
}
```

### POST `/api/analyze`
Complete email analysis (sentiment + priority + category).

**Request:**
```json
{
  "content": "Email content...",
  "subject": "Email subject (optional)"
}
```

**Response:**
```json
{
  "sentiment": {...},
  "priority": {...},
  "category": {...},
  "success": true
}
```

## Testing
Run the test suite using:
```bash
pytest tests/
```

Run specific test files:
```bash
pytest tests/test_ai_engine.py
pytest tests/test_utils.py
pytest tests/test_config.py
pytest tests/test_email_handler.py
```

## Configuration

The application supports environment-based configuration. Available options:

- `FLASK_HOST`: Flask server host (default: 0.0.0.0)
- `FLASK_PORT`: Flask server port (default: 5000)
- `DEBUG`: Enable debug mode (default: True)
- `MAX_EMAILS`: Maximum number of emails to fetch (default: 10)
- `SUMMARIZATION_MODEL`: Model for summarization (default: facebook/bart-large-cnn)
- `TEXT_GENERATION_MODEL`: Model for text generation (default: gpt2)
- `SENTIMENT_MODEL`: Model for sentiment analysis (default: distilbert-base-uncased-finetuned-sst-2-english)
- `SUMMARY_MAX_LENGTH`: Maximum summary length (default: 130)
- `SUMMARY_MIN_LENGTH`: Minimum summary length (default: 30)
- `REPLY_MAX_LENGTH`: Maximum reply length (default: 100)

## File Structure
```
.
├── README.md
├── Dockerfile
├── requirements.txt
├── src
│   ├── main.py              # Flask application
│   ├── config.py            # Configuration management
│   ├── utils.py             # Utility functions
│   ├── email_handler.py     # Gmail API integration
│   ├── ai_engine.py         # AI/ML processing
│   ├── templates
│   │   └── index.html       # Frontend UI
│   └── static
│       └── app.js           # Frontend JavaScript
└── tests
    ├── test_email_handler.py
    ├── test_ai_engine.py
    ├── test_config.py
    └── test_utils.py
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.
