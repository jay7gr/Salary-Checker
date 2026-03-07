#!/usr/bin/env python3
"""
Fix FAQ dark mode readability on city and compare pages.

Problem: FAQ sections have hardcoded inline colors that don't respond to dark mode:
  - h3: color: #1d1d1f (near-black, invisible on dark bg)
  - p:  color: #4a4a4c (dark grey, barely visible on dark bg)
  - div: border-bottom: 1px solid #f0f0f2 (invisible border on dark bg)

Fix: Replace hardcoded colors with CSS variables that respond to [data-theme="dark"]:
  - #1d1d1f → var(--text-primary)
  - #4a4a4c → var(--text-body)
  - #f0f0f2 → var(--border-light)
"""

import os
import glob
import re

def fix_faq_darkmode(filepath):
    """Fix hardcoded FAQ inline colors in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix h3 color: #1d1d1f → var(--text-primary)
    # Pattern: inside style attribute on h3 tags in FAQ section
    content = content.replace(
        'color: #1d1d1f;',
        'color: var(--text-primary);'
    )

    # Fix p color: #4a4a4c → var(--text-body)
    content = content.replace(
        'color: #4a4a4c;',
        'color: var(--text-body);'
    )

    # Fix div border: 1px solid #f0f0f2 → var(--border-light)
    content = content.replace(
        'border-bottom: 1px solid #f0f0f2;',
        'border-bottom: 1px solid var(--border-light);'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    base = os.path.dirname(os.path.abspath(__file__))

    city_dir = os.path.join(base, 'city')
    compare_dir = os.path.join(base, 'compare')

    city_files = glob.glob(os.path.join(city_dir, '*.html'))
    compare_files = glob.glob(os.path.join(compare_dir, '*.html'))

    print(f"Found {len(city_files)} city files")
    print(f"Found {len(compare_files)} compare files")

    city_fixed = 0
    compare_fixed = 0

    for f in city_files:
        if fix_faq_darkmode(f):
            city_fixed += 1

    for f in compare_files:
        if fix_faq_darkmode(f):
            compare_fixed += 1

    print(f"\nFixed {city_fixed}/{len(city_files)} city files")
    print(f"Fixed {compare_fixed}/{len(compare_files)} compare files")
    print(f"Total: {city_fixed + compare_fixed} files updated")


if __name__ == '__main__':
    main()
