#!/usr/bin/env python3
"""One-time script to add touch-action: manipulation to disable zoom on Safari iOS.

Safari ignores user-scalable=no since iOS 10+. The CSS touch-action property
is the reliable cross-browser way to prevent pinch-to-zoom.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DIRS_TO_WALK = ['city', 'compare', 'salary-needed', 'blog', 'blog/articles', 'privacy']
ROOT_FILES = ['index.html']

updated = 0
skipped = 0
total = 0


def process_file(fpath):
    global updated, skipped, total
    total += 1

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Idempotency: skip if already has touch-action
    if 'touch-action' in content:
        skipped += 1
        return

    original = content

    # Pattern A: html, body { overflow-x: hidden; }
    pattern_a = r'(html, body \{ overflow-x: hidden; \})'
    replacement_a = r'\1\n        html { touch-action: manipulation; -ms-touch-action: manipulation; }'
    new_content = re.sub(pattern_a, replacement_a, content, count=1)

    if new_content == content:
        # Pattern B: html,body{overflow-x:hidden} (minified)
        pattern_b = r'(html,body\{overflow-x:hidden\})'
        replacement_b = r'\1\n        html{touch-action:manipulation;-ms-touch-action:manipulation}'
        new_content = re.sub(pattern_b, replacement_b, content, count=1)

    if new_content == content:
        # Pattern C: multiline html, body { \n overflow-x: hidden; \n }
        pattern_c = r'(html, body \{\s*overflow-x: hidden;\s*\})'
        replacement_c = r'\1\n        html {\n            touch-action: manipulation;\n            -ms-touch-action: manipulation;\n        }'
        new_content = re.sub(pattern_c, replacement_c, content, count=1, flags=re.DOTALL)

    if new_content == content:
        # Pattern D: blog files with * { box-sizing } but no overflow-x line
        # Matches both * { } and *, *::before, *::after { } variants
        pattern_d = r'(\*(?:, \*::before, \*::after)? \{\s*margin: 0;\s*padding: 0;\s*box-sizing: border-box;\s*\})'
        replacement_d = r'''\1
        html, body {
            overflow-x: hidden;
        }
        html {
            touch-action: manipulation;
            -ms-touch-action: manipulation;
        }'''
        new_content = re.sub(pattern_d, replacement_d, content, count=1, flags=re.DOTALL)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fname = os.path.relpath(fpath, BASE_DIR)
        print(f'  UPDATED: {fname}')
        updated += 1
    else:
        skipped += 1
        fname = os.path.relpath(fpath, BASE_DIR)
        print(f'  SKIP (no matching pattern): {fname}')


# Process root files
for fname in ROOT_FILES:
    fpath = os.path.join(BASE_DIR, fname)
    if os.path.isfile(fpath):
        process_file(fpath)

# Process directories
for d in DIRS_TO_WALK:
    dirpath = os.path.join(BASE_DIR, d)
    if not os.path.isdir(dirpath):
        continue
    for fname in sorted(os.listdir(dirpath)):
        if not fname.endswith('.html'):
            continue
        process_file(os.path.join(dirpath, fname))

print(f'\nDone: {total} files processed, {updated} updated, {skipped} skipped')
