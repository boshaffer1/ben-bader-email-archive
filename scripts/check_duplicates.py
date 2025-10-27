#!/usr/bin/env python3
"""
Check for duplicate emails
"""

import json
from collections import defaultdict
from datetime import datetime

def main():
    print("=" * 60)
    print("CHECKING FOR DUPLICATES")
    print("=" * 60)

    # Load emails
    with open('../data/raw_emails.json', 'r', encoding='utf-8') as f:
        emails = json.load(f)

    print(f"\n✓ Loaded {len(emails)} emails")

    # Check for duplicate IDs
    ids = [email['id'] for email in emails]
    duplicate_ids = {id: count for id, count in
                     defaultdict(int, ((id, ids.count(id)) for id in set(ids))).items()
                     if count > 1}

    if duplicate_ids:
        print(f"\n⚠️  Found {len(duplicate_ids)} duplicate IDs:")
        for id, count in duplicate_ids.items():
            print(f"   {id}: {count} occurrences")
    else:
        print("\n✅ No duplicate IDs found")

    # Check for duplicate subjects + dates (likely duplicates)
    subject_date_map = defaultdict(list)

    for email in emails:
        date_str = email.get('date', '') or ''
        date_prefix = date_str[:10] if len(date_str) >= 10 else date_str
        key = (email['subject'].lower().strip(), date_prefix)
        subject_date_map[key].append(email)

    duplicates = {k: v for k, v in subject_date_map.items() if len(v) > 1}

    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} potential duplicates (same subject + date):")
        print()
        for (subject, date), email_list in list(duplicates.items())[:10]:
            print(f"Subject: {subject[:60]}...")
            print(f"Date: {date}")
            print(f"Count: {len(email_list)}")
            for email in email_list:
                print(f"  - ID: {email['id']}")
            print()
    else:
        print("\n✅ No duplicate subjects+dates found")

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total emails: {len(emails)}")
    print(f"Unique IDs: {len(set(ids))}")
    print(f"Duplicate IDs: {len(duplicate_ids)}")
    print(f"Duplicate subject+date combinations: {len(duplicates)}")

    if duplicates:
        total_duplicate_emails = sum(len(v) - 1 for v in duplicates.values())
        print(f"Emails that could be removed: {total_duplicate_emails}")
        print(f"After cleanup: {len(emails) - total_duplicate_emails} emails")

if __name__ == '__main__':
    main()
