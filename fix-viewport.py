#!/usr/bin/env python3
"""
Remove 'maximum-scale=1.0, user-scalable=no' from viewport meta tags.

This restriction violates WCAG 2.0 and prevents users with visual
impairments from zooming on mobile devices.

Before: <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
After:  <meta name="viewport" content="width=device-width, initial-scale=1.0">
"""
import os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

OLD = ', maximum-scale=1.0, user-scalable=no'
NEW = ''

PATTERNS = [
    'city/**/*.html',
    'compare/**/*.html',
    'salary-needed/**/*.html',
    'salary/*.html',
    'rankings/*.html',
    'blog/**/*.html',
]

stats = {'updated': 0, 'skipped': 0}

for pattern in PATTERNS:
    files = sorted(glob.glob(os.path.join(BASE, pattern), recursive=True))
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()

        if OLD not in content:
            stats['skipped'] += 1
            continue

        content = content.replace(OLD, NEW)

        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        stats['updated'] += 1

print(f"Done: {stats['updated']} updated, {stats['skipped']} skipped")
