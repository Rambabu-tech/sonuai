# mailbot/gmail_confirm.py

import os
import base64
import re
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

TOKEN_PATH = "mailbot/token.json"
CREDENTIALS_PATH = "credentials.json"


def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH, SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def list_recent_emails(max_results=10):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
    ).execute()

    messages = results.get("messages", [])
    subjects = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["Subject"],
        ).execute()

        headers = msg_data.get("payload", {}).get("headers", [])

        for header in headers:
            if header["name"] == "Subject":
                subjects.append(header["value"])

    return subjects


def extract_company_from_subject(subject):
    # Example:
    # "Thank you for applying to Stripe"
    match = re.search(r"applying to (.+)", subject, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return None


def find_application_confirmations():
    subjects = list_recent_emails(15)

    confirmations = []

    for subject in subjects:
        if "thank you for applying" in subject.lower():
            company = extract_company_from_subject(subject)
            if company:
                confirmations.append(company)

    return confirmations
