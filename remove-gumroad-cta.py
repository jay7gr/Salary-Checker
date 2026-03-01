#!/usr/bin/env python3
"""
One-time script: Remove Gumroad PDF report CTA boxes from existing pages.

Removes the <section class="content-card gumroad-cta-v1"> block that was
added by add-gumroad-cta.py.

Targets:
  - City pages (city/*.html, top-level only) — ~113 files
  - Rankings pages (rankings/*.html) — ~8 files
  - Salary pages (salary/*.html) — ~38 files
  - Blog articles (blog/articles/*.html) — ~19 files

Idempotency: Skips files that don't contain 'gumroad-cta-v1'.
"""
import os
import glob
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# Regex: match the entire <section class="content-card gumroad-cta-v1" ...>...</section>
# block plus any surrounding blank lines / whitespace.
CTA_PATTERN = re.compile(
    r'\n*\s*<section class="content-card gumroad-cta-v1"[^>]*>.*?</section>\s*',
    re.DOTALL
)


def process_directory(label, pattern):
    """Remove Gumroad CTA from all HTML files matching the glob pattern."""
    files = sorted(glob.glob(pattern))
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency: skip files without the CTA
        if 'gumroad-cta-v1' not in content:
            skipped += 1
            continue

        new_content = CTA_PATTERN.sub('\n', content)

        if new_content == content:
            # Regex didn't match even though the class was present
            errors += 1
            print(f"  WARN: Regex did not match in {label}/{filename}")
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated += 1
        print(f"  Removed: {label}/{filename}")

    return updated, skipped, errors


if __name__ == '__main__':
    print("Removing Gumroad PDF report CTAs from existing pages...")
    print()

    dirs = [
        ("city",           os.path.join(BASE, 'city', '*.html')),
        ("rankings",       os.path.join(BASE, 'rankings', '*.html')),
        ("salary",         os.path.join(BASE, 'salary', '*.html')),
        ("blog/articles",  os.path.join(BASE, 'blog', 'articles', '*.html')),
    ]

    grand_updated = 0
    grand_skipped = 0
    grand_errors = 0

    for i, (label, pat) in enumerate(dirs, 1):
        print(f"{i}. {label.capitalize()} pages ({label}/*.html)...")
        u, s, e = process_directory(label, pat)
        print(f"   Updated: {u}, Skipped: {s}, Errors: {e}")
        print()
        grand_updated += u
        grand_skipped += s
        grand_errors += e

    print("=" * 50)
    print(f"TOTAL: {grand_updated} updated, {grand_skipped} skipped, {grand_errors} errors")
