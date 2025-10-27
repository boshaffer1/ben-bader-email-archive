#!/usr/bin/env python3
"""
Gmail Email Collector
Fetches all emails from a specific sender and exports to JSON
"""

import os
import json
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailCollector:
    def __init__(self):
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

    def get_emails_from_sender(self, sender_email, max_results=None):
        """Fetch all emails from specific sender"""
        emails = []
        page_token = None

        print(f"Fetching emails from: {sender_email}")

        try:
            while True:
                query = f'from:{sender_email}'
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=page_token,
                    maxResults=100
                ).execute()

                messages = results.get('messages', [])

                if not messages:
                    print("No more messages found.")
                    break

                print(f"Processing {len(messages)} messages...")

                for msg in messages:
                    email_data = self.get_email_details(msg['id'])
                    if email_data:
                        emails.append(email_data)
                        print(f"Collected: {email_data['subject'][:50]}...")

                    if max_results and len(emails) >= max_results:
                        break

                page_token = results.get('nextPageToken')

                if not page_token or (max_results and len(emails) >= max_results):
                    break

            print(f"\nTotal emails collected: {len(emails)}")
            return emails

        except HttpError as error:
            print(f'An error occurred: {error}')
            return emails

    def get_email_details(self, msg_id):
        """Get full details of a single email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

            body = self.get_email_body(message['payload'])

            return {
                'id': msg_id,
                'subject': subject,
                'from': sender,
                'date': date,
                'timestamp': message['internalDate'],
                'body': body,
                'snippet': message.get('snippet', '')
            }

        except HttpError as error:
            print(f'Error fetching message {msg_id}: {error}')
            return None

    def get_email_body(self, payload):
        """Extract email body from payload"""
        body = ""

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        return body

    def export_to_json(self, emails, filename='../data/raw_emails.json'):
        """Export emails to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(emails, indent=2, fp=f, ensure_ascii=False)
        print(f"Exported {len(emails)} emails to {filename}")

    def export_to_csv(self, emails, filename='../data/emails.csv'):
        """Export emails to CSV file"""
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if not emails:
                return

            fieldnames = ['id', 'subject', 'from', 'date', 'timestamp', 'snippet', 'body']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for email in emails:
                writer.writerow(email)

        print(f"Exported {len(emails)} emails to {filename}")


def main():
    sender_email = input("Enter sender email address: ").strip()

    if not sender_email:
        print("No sender email provided. Exiting.")
        return

    collector = GmailCollector()
    emails = collector.get_emails_from_sender(sender_email)

    if emails:
        collector.export_to_json(emails)
        collector.export_to_csv(emails)
        print(f"\n✓ Successfully collected {len(emails)} emails")
    else:
        print("No emails found or error occurred.")


if __name__ == '__main__':
    main()
