#!/usr/bin/env python3
"""
One-time script: Remove <script src="/consent.js" defer></script> from all HTML files.
Google's AdSense CMP now handles consent — the custom consent.js is no longer needed.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_LINE = '    <script src="/consent.js" defer></script>\n'

updated = 0
skipped = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    # Skip hidden dirs and node_modules
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        if TARGET_LINE not in content:
            skipped += 1
            continue
        new_content = content.replace(TARGET_LINE, '')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated += 1

print(f'Updated: {updated} files')
print(f'Skipped (no match): {skipped} files')
