#!/usr/bin/env python3
"""
Prepare data files for website deployment
Copies processed data to website's public folder
"""

import shutil
import os

def prepare_data():
    """Copy data files to website public folder"""

    data_dir = '../data'
    public_dir = '../website/public/data'

    os.makedirs(public_dir, exist_ok=True)

    files_to_copy = [
        ('raw_emails.json', True),   # Required
        ('topics.json', False),       # Optional
        ('embeddings.json', False)    # Optional
    ]

    for filename, required in files_to_copy:
        src = os.path.join(data_dir, filename)
        dst = os.path.join(public_dir, filename)

        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✓ Copied {filename} to website/public/data/")
        elif required:
            print(f"✗ ERROR: {filename} not found (required)")
            return False
        else:
            print(f"⚠ {filename} not found (optional, skipping)")

    print("\n✓ Website data preparation complete")

if __name__ == '__main__':
    prepare_data()
