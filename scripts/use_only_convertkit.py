#!/usr/bin/env python3
"""
Use ONLY ConvertKit broadcasts, discard Gmail exports
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
    print("USING ONLY CONVERTKIT BROADCASTS")
    print("=" * 60)

    # Load ConvertKit broadcasts
    with open('../data/convertkit-broadcasts-full.json', 'r', encoding='utf-8') as f:
        convertkit_data = json.load(f)

    print(f"\n✓ Loaded {len(convertkit_data)} ConvertKit broadcasts")

    # Convert ConvertKit emails
    emails = []

    for broadcast in convertkit_data:
        email_id = f"convertkit_{broadcast['id']}"

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

        emails.append(email)

    # Sort by timestamp
    emails.sort(key=lambda x: int(x.get('timestamp', '0')))

    # Get date range
    if emails:
        earliest = datetime.fromtimestamp(int(emails[0]['timestamp']) / 1000)
        latest = datetime.fromtimestamp(int(emails[-1]['timestamp']) / 1000)
        print(f"\n📅 Date range: {earliest.strftime('%B %d, %Y')} - {latest.strftime('%B %d, %Y')}")

    # Save emails
    with open('../data/raw_emails.json', 'w', encoding='utf-8') as f:
        json.dump(emails, indent=2, fp=f, ensure_ascii=False)

    print(f"\n✅ SUCCESS!")
    print(f"   Total emails: {len(emails)}")
    print(f"   Source: ConvertKit broadcasts only")

    print("\n📋 Next steps:")
    print("1. python check_duplicates.py (verify no duplicates)")
    print("2. python process_embeddings.py (regenerate topics)")
    print("3. python prepare_website_data.py (copy to website)")

if __name__ == '__main__':
    main()
