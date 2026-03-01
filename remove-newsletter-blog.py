#!/usr/bin/env python3
"""
One-time script: Remove newsletter signup sections from blog articles.
Removes <section class="newsletter-blog-v1"> blocks added by add-blog-enhancements.py.
Idempotency: Skips files without 'newsletter-blog-v1'.
"""
import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))
PATTERN = re.compile(
    r'\n*\s*<section class="newsletter-blog-v1"[^>]*>.*?</section>\s*',
    re.DOTALL
)

files = sorted(glob.glob(os.path.join(BASE, 'blog', 'articles', '*.html')))
updated = skipped = errors = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'newsletter-blog-v1' not in content:
        skipped += 1
        continue
    new = PATTERN.sub('\n', content)
    if new == content:
        errors += 1
        print(f"  WARN: Regex no match in {os.path.basename(f)}")
        continue
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(new)
    updated += 1

print(f"TOTAL: {updated} updated, {skipped} skipped, {errors} errors")
