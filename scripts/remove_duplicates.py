#!/usr/bin/env python3
"""
Remove duplicate emails based on subject + date
"""

import json
from collections import defaultdict

def main():
    print("=" * 60)
    print("REMOVING DUPLICATES")
    print("=" * 60)

    # Load emails
    with open('../data/raw_emails.json', 'r', encoding='utf-8') as f:
        emails = json.load(f)

    print(f"\n✓ Loaded {len(emails)} emails")

    # Find duplicates by subject + date
    subject_date_map = defaultdict(list)

    for email in emails:
        date_str = email.get('date', '') or ''
        date_prefix = date_str[:10] if len(date_str) >= 10 else date_str
        key = (email['subject'].lower().strip(), date_prefix)
        subject_date_map[key].append(email)

    duplicates = {k: v for k, v in subject_date_map.items() if len(v) > 1}

    if not duplicates:
        print("\n✅ No duplicates found")
        return

    print(f"\n⚠️  Found {len(duplicates)} duplicate groups")

    # Keep first occurrence of each duplicate, remove others
    emails_to_remove = set()

    for (subject, date), email_list in duplicates.items():
        print(f"\nSubject: {subject[:60]}...")
        print(f"Date: {date}")
        print(f"Keeping: {email_list[0]['id']}")

        for email in email_list[1:]:
            print(f"Removing: {email['id']}")
            emails_to_remove.add(email['id'])

    # Filter out duplicates
    cleaned_emails = [e for e in emails if e['id'] not in emails_to_remove]

    print(f"\n📊 Summary:")
    print(f"   Before: {len(emails)} emails")
    print(f"   Removed: {len(emails_to_remove)} duplicates")
    print(f"   After: {len(cleaned_emails)} emails")

    # Save cleaned data
    with open('../data/raw_emails.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_emails, indent=2, fp=f, ensure_ascii=False)

    print(f"\n✅ SUCCESS! Duplicates removed")
    print("\n📋 Next steps:")
    print("1. python prepare_website_data.py (copy to website)")
    print("2. Refresh website to see cleaned data")

if __name__ == '__main__':
    main()
