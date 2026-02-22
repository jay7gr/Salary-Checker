#!/usr/bin/env python3
"""
One-time script: Fix broken comparison links in neighborhood pages.

The popular_pairs in generate-pages.py had city pairs in non-alphabetical order,
but comparison files are named alphabetically. This fixes the 6 wrong URL patterns
across ~109 neighborhood HTML files.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Wrong URL -> Correct URL (alphabetical order)
REPLACEMENTS = {
    '/compare/london-vs-dubai': '/compare/dubai-vs-london',
    '/compare/new-york-vs-los-angeles': '/compare/los-angeles-vs-new-york',
    '/compare/singapore-vs-hong-kong': '/compare/hong-kong-vs-singapore',
    '/compare/tokyo-vs-seoul': '/compare/seoul-vs-tokyo',
    '/compare/paris-vs-berlin': '/compare/berlin-vs-paris',
    '/compare/sydney-vs-melbourne': '/compare/melbourne-vs-sydney',
}

fixed_files = 0
total_replacements = 0

# Scan all neighborhood HTML files in city/*/
city_dir = os.path.join(BASE_DIR, 'city')
for city_folder in os.listdir(city_dir):
    city_path = os.path.join(city_dir, city_folder)
    if not os.path.isdir(city_path):
        continue
    for fname in os.listdir(city_path):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(city_path, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        file_replacements = 0
        for wrong, correct in REPLACEMENTS.items():
            if wrong in new_content:
                count = new_content.count(wrong)
                new_content = new_content.replace(wrong, correct)
                file_replacements += count

        if file_replacements > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed_files += 1
            total_replacements += file_replacements
            print(f'  Fixed {file_replacements} link(s) in {city_folder}/{fname}')

print(f'\nDone: Fixed {total_replacements} broken links across {fixed_files} files.')
