#!/usr/bin/env python3
"""
Merge ConvertKit broadcasts with existing emails
"""

import json
import re
from html.parser import HTMLParser
from datetime import datetime

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ' '.join(self.text)

def html_to_text(html):
    """Convert HTML to plain text"""
    if not html:
        return ""

    # Remove style tags and their content
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)

    # Remove script tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)

    # Convert <p> to newlines
    html = html.replace('</p>', '\n\n')
    html = html.replace('<br>', '\n')
    html = html.replace('<br/>', '\n')
    html = html.replace('<br />', '\n')

    # Extract text
    parser = HTMLTextExtractor()
    try:
        parser.feed(html)
        text = parser.get_text()
    except:
        text = html

    # Clean up
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove extra blank lines
    text = re.sub(r' +', ' ', text)  # Remove extra spaces
    text = text.strip()

    return text

def parse_convertkit_date(date_str):
    """Convert ConvertKit date to timestamp"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return str(int(dt.timestamp() * 1000))
    except:
        return "0"

def main():
    print("=" * 60)
    print("MERGING CONVERTKIT EMAILS")
    print("=" * 60)

    # Load existing emails
    with open('../data/raw_emails.json', 'r', encoding='utf-8') as f:
        existing_emails = json.load(f)

    print(f"\n✓ Loaded {len(existing_emails)} existing emails")

    # Load ConvertKit broadcasts
    with open('../data/convertkit-broadcasts-full.json', 'r', encoding='utf-8') as f:
        convertkit_data = json.load(f)

    print(f"✓ Loaded {len(convertkit_data)} ConvertKit broadcasts")

    # Track existing IDs to avoid duplicates
    existing_ids = {email['id'] for email in existing_emails}

    # Convert ConvertKit emails
    new_emails = []
    skipped = 0

    for broadcast in convertkit_data:
        email_id = f"convertkit_{broadcast['id']}"

        # Skip if already exists
        if email_id in existing_ids:
            skipped += 1
            continue

        # Convert HTML to text
        body_text = html_to_text(broadcast.get('content', ''))

        # Create email object
        email = {
            'id': email_id,
            'subject': broadcast.get('subject', 'Untitled'),
            'from': f"Ben Bader <{broadcast.get('email_address', 'benbader0@gmail.com')}>",
            'date': broadcast.get('published_at', broadcast.get('send_at', '')),
            'timestamp': parse_convertkit_date(broadcast.get('published_at', broadcast.get('send_at', ''))),
            'body': body_text,
            'snippet': body_text[:200] if body_text else ''
        }

        new_emails.append(email)

    print(f"\n✓ Converted {len(new_emails)} new emails")
    print(f"⊘ Skipped {skipped} duplicates")

    # Merge and sort
    all_emails = existing_emails + new_emails
    all_emails.sort(key=lambda x: int(x.get('timestamp', '0')))

    # Get date range
    if all_emails:
        earliest = datetime.fromtimestamp(int(all_emails[0]['timestamp']) / 1000)
        latest = datetime.fromtimestamp(int(all_emails[-1]['timestamp']) / 1000)
        print(f"\n📅 Date range: {earliest.strftime('%B %d, %Y')} - {latest.strftime('%B %d, %Y')}")

    # Save merged emails
    with open('../data/raw_emails.json', 'w', encoding='utf-8') as f:
        json.dump(all_emails, indent=2, fp=f, ensure_ascii=False)

    print(f"\n✅ SUCCESS!")
    print(f"   Total emails: {len(all_emails)}")
    print(f"   ({len(existing_emails)} existing + {len(new_emails)} new)")

    print("\n📋 Next steps:")
    print("1. python prepare_website_data.py (copy to website)")
    print("2. python process_embeddings.py (regenerate topics)")
    print("3. Refresh website to see all emails!")

if __name__ == '__main__':
    main()
