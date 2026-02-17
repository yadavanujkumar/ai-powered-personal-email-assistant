# AI-Powered Personal Email Assistant

## Overview
This project is an AI-powered personal email assistant that helps users manage their emails efficiently. It uses natural language processing (NLP) to analyze email content, prioritize messages, and even draft responses based on user input.

## Features
- **Email Prioritization**: Automatically categorize emails into high, medium, and low priority.
- **Smart Reply Suggestions**: Generate AI-powered reply suggestions for emails.
- **Email Summarization**: Summarize lengthy emails into concise points.
- **Secure Authentication**: OAuth2-based authentication for Gmail.

## Tech Stack
- **Backend**: Python (Flask)
- **Frontend**: JavaScript (Vanilla JS)
- **Containerization**: Docker

## Setup Instructions

### Prerequisites
- Python 3.8+
- Docker
- Gmail API credentials (OAuth2)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-email-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Gmail API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the Gmail API.
   - Download the `credentials.json` file and place it in the `src/` directory.

4. Run the application locally:
   ```bash
   python src/main.py
   ```

5. Build and run the Docker container:
   ```bash
   docker build -t ai-email-assistant .
   docker run -p 5000:5000 ai-email-assistant
   ```

6. Access the application:
   Open your browser and navigate to `http://localhost:5000`.

## Testing
Run the test suite using:
```bash
pytest tests/
```

## File Structure
```
.
├── README.md
├── Dockerfile
├── requirements.txt
├── src
│   ├── main.py
│   ├── utils.py
│   ├── email_handler.py
│   ├── ai_engine.py
│   ├── templates
│   │   └── index.html
│   └── static
│       └── app.js
└── tests
    ├── test_email_handler.py
    ├── test_ai_engine.py
    └── test_utils.py
```

## License
This project is licensed under the MIT License.