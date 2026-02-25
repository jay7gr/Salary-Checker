#!/usr/bin/env python3
"""One-time script to fix mobile horizontal overflow on all HTML pages.

Adds:
1. html, body { overflow-x: hidden; } after the * { box-sizing } reset
2. flex-wrap: wrap on .page-footer to prevent footer link overflow
3. Removes margin: 0 12px from .page-footer a (replaced by gap on parent)
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DIRS_TO_WALK = ['city', 'compare', 'salary-needed', 'blog', 'blog/articles', 'privacy']
ROOT_FILES = ['index.html']

updated_overflow = 0
updated_footer = 0
skipped = 0
total = 0


def process_file(fpath):
    global updated_overflow, updated_footer, skipped, total
    total += 1

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # --- Fix 1: Add overflow-x: hidden after * { box-sizing } reset ---
    if 'overflow-x: hidden' not in content and 'overflow-x:hidden' not in content:
        # Pattern A: *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        pattern_a = r'(\*, \*::before, \*::after \{ box-sizing: border-box; margin: 0; padding: 0; \})'
        replacement_a = r'\1\n        html, body { overflow-x: hidden; }'
        new_content = re.sub(pattern_a, replacement_a, content, count=1)

        if new_content == content:
            # Pattern B: * { margin:0; padding:0; box-sizing:border-box; }
            pattern_b = r'(\* \{ margin:0; padding:0; box-sizing:border-box; \})'
            replacement_b = r'\1\n        html, body { overflow-x: hidden; }'
            new_content = re.sub(pattern_b, replacement_b, content, count=1)

        if new_content == content:
            # Pattern C: *{margin:0;padding:0;box-sizing:border-box} (minified)
            pattern_c = r'(\*\{margin:0;padding:0;box-sizing:border-box\})'
            replacement_c = r'\1\n        html,body{overflow-x:hidden}'
            new_content = re.sub(pattern_c, replacement_c, content, count=1)

        if new_content != content:
            content = new_content
            changes.append('overflow-x')
            updated_overflow += 1

    # --- Fix 2: Add flex-wrap to .page-footer ---
    # Only fix if page-footer exists and doesn't already have flex-wrap in .page-footer block
    footer_match = re.search(r'\.page-footer\s*\{[^}]*\}', content, flags=re.DOTALL)
    footer_has_flex = footer_match and 'flex-wrap' in footer_match.group(0) if footer_match else True
    if '.page-footer' in content and not footer_has_flex:
        # Match .page-footer { ... } block (may span multiple lines) and inject flex props before closing }
        pattern_footer = r'(\.page-footer\s*\{[^}]*border-top:\s*1px solid var\(--border\);)\s*(\})'
        def add_flex(m):
            # Check if it's a single-line or multi-line block
            if '\n' in m.group(1):
                return m.group(1) + '\n            display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px;\n        ' + m.group(2)
            else:
                return m.group(1) + ' display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px; ' + m.group(2)
        new_content = re.sub(pattern_footer, add_flex, content, count=1, flags=re.DOTALL)

        if new_content != content:
            content = new_content
            changes.append('footer-flex')
            updated_footer += 1

    # --- Fix 3: Remove margin: 0 12px from .page-footer a (gap on parent handles it) ---
    footer_a_match = re.search(r'\.page-footer a\s*\{[^}]*\}', content, flags=re.DOTALL)
    footer_a_has_margin = footer_a_match and 'margin: 0 12px' in footer_a_match.group(0) if footer_a_match else False
    if footer_a_has_margin:
        content = re.sub(
            r'(\.page-footer a\s*\{[^}]*?) ?margin: 0 12px;',
            r'\1',
            content,
            flags=re.DOTALL
        )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        fname = os.path.relpath(fpath, BASE_DIR)
        print(f'  UPDATED ({", ".join(changes)}): {fname}')
    else:
        skipped += 1


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

print(f'\nDone: {total} files processed')
print(f'  {updated_overflow} files got overflow-x: hidden')
print(f'  {updated_footer} files got footer flex-wrap')
print(f'  {skipped} files skipped (already had fixes)')
