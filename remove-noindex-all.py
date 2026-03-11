#!/usr/bin/env python3
"""
One-time script to remove noindex meta tags from all HTML files
in city/, salary-needed/, and compare/ directories.

Replaces: <meta name="robots" content="noindex, follow">
With:     <meta name="robots" content="index, follow">

This reverses the March 3, 2026 SEO overhaul that caused a traffic decline.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORIES = ['city', 'salary-needed', 'compare']

# Pattern to match noindex meta tags (flexible whitespace)
NOINDEX_PATTERN = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\']noindex,\s*follow["\']',
    re.IGNORECASE
)
REPLACEMENT = '<meta name="robots" content="index, follow"'

total_files = 0
modified_files = 0
skipped_files = 0
errors = 0

for directory in DIRECTORIES:
    dir_path = os.path.join(BASE_DIR, directory)
    dir_modified = 0
    dir_total = 0

    if not os.path.exists(dir_path):
        print(f"WARNING: Directory not found: {dir_path}")
        continue

    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            if not filename.endswith('.html'):
                continue

            filepath = os.path.join(root, filename)
            dir_total += 1
            total_files += 1

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                if NOINDEX_PATTERN.search(content):
                    new_content = NOINDEX_PATTERN.sub(REPLACEMENT, content)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    modified_files += 1
                    dir_modified += 1
                else:
                    skipped_files += 1

            except Exception as e:
                print(f"ERROR processing {filepath}: {e}")
                errors += 1

    print(f"{directory}/: {dir_modified} modified out of {dir_total} HTML files")

print(f"\n{'='*50}")
print(f"TOTAL HTML files scanned: {total_files}")
print(f"Files modified (noindex → index): {modified_files}")
print(f"Files already OK (skipped): {skipped_files}")
print(f"Errors: {errors}")
print(f"{'='*50}")
