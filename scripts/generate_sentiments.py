#!/usr/bin/env python3
"""
Generate sentiment tags for all emails using AI
"""

import json
import os
from openai import OpenAI

class SentimentGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.emails = []

    def load_emails(self, filepath='../data/raw_emails.json'):
        """Load emails from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.emails = json.load(f)
        print(f"Loaded {len(self.emails)} emails")

    def analyze_sentiment(self, email):
        """Use AI to analyze email sentiment/vibe"""
        text = f"Subject: {email['subject']}\n\n{email['body'][:1500]}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": """Analyze this email and assign 1-3 sentiment tags from this list:
- Funny (humorous, witty, makes you laugh)
- Thoughtful (deep, philosophical, introspective)
- Motivational (inspiring, uplifting, encouraging)
- Personal (intimate, vulnerable, heartfelt)
- Casual (conversational, relaxed, everyday)
- Provocative (challenging, controversial, edgy)
- Storytelling (narrative, descriptive, anecdotal)
- Advice (tips, guidance, teaching)

Return ONLY the tags as a comma-separated list. Pick 1-3 tags that best fit."""
                }, {
                    "role": "user",
                    "content": text
                }],
                max_tokens=50,
                temperature=0.3
            )

            tags_text = response.choices[0].message.content.strip()
            tags = [tag.strip() for tag in tags_text.split(',')]

            return tags

        except Exception as e:
            print(f"Error analyzing email {email['id']}: {e}")
            return ["Casual"]

    def generate_all_sentiments(self):
        """Generate sentiments for all emails"""
        print("\n🔄 Analyzing email sentiments...\n")

        for i, email in enumerate(self.emails):
            sentiments = self.analyze_sentiment(email)
            email['sentiments'] = sentiments

            print(f"✓ {i + 1}/{len(self.emails)}: {email['subject'][:50]}... → {', '.join(sentiments)}")

            # Save after every 50 emails as backup
            if (i + 1) % 50 == 0:
                self.save_emails()
                print(f"\n💾 Backup saved at {i + 1} emails\n")

        print(f"\n✅ Completed sentiment analysis for {len(self.emails)} emails")

    def save_emails(self, filepath='../data/raw_emails.json'):
        """Save emails with sentiments back to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.emails, indent=2, fp=f, ensure_ascii=False)
        print(f"💾 Saved emails with sentiments to {filepath}")

    def generate_summary(self):
        """Generate summary statistics"""
        print("\n" + "=" * 60)
        print("SENTIMENT SUMMARY")
        print("=" * 60)

        sentiment_counts = {}
        for email in self.emails:
            for sentiment in email.get('sentiments', []):
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

        print("\nSentiment Distribution:")
        for sentiment, count in sorted(sentiment_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {sentiment}: {count} emails")

        print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("EMAIL SENTIMENT ANALYSIS")
    print("=" * 60)

    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("\n⚠️  OPENAI_API_KEY not found")
        api_key = input("Enter OpenAI API key: ").strip()

        if not api_key:
            print("❌ API key required")
            return

    generator = SentimentGenerator(api_key)

    generator.load_emails()

    confirm = input(f"\n⚠️  This will analyze {len(generator.emails)} emails (~$2-5 cost). Continue? (y/n): ")

    if confirm.lower() != 'y':
        print("❌ Cancelled")
        return

    generator.generate_all_sentiments()
    generator.save_emails()
    generator.generate_summary()

    print("\n📋 Next steps:")
    print("1. Run: python prepare_website_data.py")
    print("2. Sentiment tags are now in each email's data")
    print("3. UI update needed to display sentiment filters")


if __name__ == '__main__':
    main()
