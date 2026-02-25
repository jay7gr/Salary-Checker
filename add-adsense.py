#!/usr/bin/env python3
"""One-time script to inject Google AdSense Auto Ads tag into all existing HTML pages."""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ADSENSE_TAG = (
    '\n    <!-- Google AdSense Auto Ads -->'
    '\n    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4472082543745200" crossorigin="anonymous"></script>'
)

# Match the end of the GA4 config block
GA4_END = re.compile(
    r"(gtag\('config',\s*'G-MMZSM2Z96B'\);\s*</script>)"
)

DIRS = ['city', 'compare', 'salary-needed', 'blog', 'privacy']

updated = 0
skipped = 0
no_match = 0

for d in DIRS:
    dir_path = os.path.join(BASE_DIR, d)
    if not os.path.isdir(dir_path):
        continue
    for root, dirs, files in os.walk(dir_path):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Idempotency: skip if already has AdSense
            if 'pagead2.googlesyndication.com' in content:
                skipped += 1
                continue

            new_content, count = GA4_END.subn(lambda m: m.group(1) + ADSENSE_TAG, content, count=1)
            if count > 0:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1
            else:
                no_match += 1
                rel = os.path.relpath(fpath, BASE_DIR)
                print(f'  NO MATCH: {rel}')

print(f'\nDone: {updated} files updated, {skipped} already had AdSense, {no_match} had no GA4 block')
