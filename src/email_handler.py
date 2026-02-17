import os
import base64
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from utils import validate_email_content

class EmailHandler:
    def __init__(self):
        self.credentials = self._load_credentials()
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def _load_credentials(self):
        try:
            creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
            return Credentials.from_authorized_user_info(creds_data)
        except Exception as e:
            raise RuntimeError(f"Failed to load credentials: {e}")

    def fetch_emails(self):
        try:
            results = self.service.users().messages().list(userId='me', maxResults=10).execute()
            messages = results.get('messages', [])
            emails = []
            for message in messages:
                msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
                snippet = msg.get('snippet', '')
                emails.append({"id": message['id'], "snippet": snippet})
            return emails
        except Exception as e:
            raise RuntimeError(f"Failed to fetch emails: {e}")