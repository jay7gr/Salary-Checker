#!/usr/bin/env python3
"""
One-time script: Replace boilerplate ending in compare page meta descriptions.

Before: Rent: $1,800/mo vs $1,900/mo. Austin is 1% cheaper overall. Salary equivalents, taxes & 3,400+ neighborhoods compared. See the full comparison.
After:  Rent: $1,800/mo vs $1,900/mo. Austin is 1% cheaper overall. Side-by-side taxes, groceries, rent & salary equivalents for singles & families.
"""
import os, glob

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    compare_dir = os.path.join(base, 'compare')
    files = sorted(glob.glob(os.path.join(compare_dir, '*.html')))

    print(f"Found {len(files)} compare files")

    old_ending = 'Salary equivalents, taxes &amp; 3,400+ neighborhoods compared. See the full comparison.'
    new_ending = 'Side-by-side taxes, groceries, rent &amp; salary equivalents for singles &amp; families.'

    # Also handle the non-escaped version (in case some files use & instead of &amp;)
    old_ending_unescaped = 'Salary equivalents, taxes & 3,400+ neighborhoods compared. See the full comparison.'
    new_ending_unescaped = 'Side-by-side taxes, groceries, rent & salary equivalents for singles & families.'

    fixed = 0
    skipped = 0

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Try escaped version first (most common in HTML attributes)
        if old_ending in content:
            content = content.replace(old_ending, new_ending)
        elif old_ending_unescaped in content:
            content = content.replace(old_ending_unescaped, new_ending_unescaped)
        else:
            skipped += 1
            continue

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
        else:
            skipped += 1

    print(f"\nResults: {fixed} fixed, {skipped} skipped")
    print(f"Total: {fixed + skipped} / {len(files)} files")


if __name__ == '__main__':
    main()
