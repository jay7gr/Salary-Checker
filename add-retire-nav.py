#!/usr/bin/env python3
"""
Add 'Retire Abroad' link to navigation and footers across all generated pages.

Nav patterns to update:
1. nav-links: Add <a href="/retire/">Retire Abroad</a> before Blog link
2. page-footer: Add <a href="/retire/">Retire Abroad</a> before Blog link

Idempotency: Skips files that already have '/retire/' link.
"""
import os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Patterns to search across all page types
PATTERNS = [
    'city/**/*.html',
    'compare/**/*.html',
    'salary-needed/**/*.html',
    'salary/*.html',
    'rankings/*.html',
    'blog/**/*.html',
    'blog/index.html',
    'about/index.html',
    'privacy/index.html',
    'terms/index.html',
    'widget/index.html',
]

stats = {'updated': 0, 'skipped': 0, 'errors': 0}

for pattern in PATTERNS:
    files = sorted(glob.glob(os.path.join(BASE, pattern), recursive=True))
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Skip if already has /retire/ link
            if '/retire/' in content:
                stats['skipped'] += 1
                continue

            original = content

            # Pattern 1: nav-links with Blog link
            # Add before <a href="/blog/">Blog</a> in nav-links sections
            content = content.replace(
                '<a href="/blog/">Blog</a>',
                '<a href="/retire/">Retire Abroad</a>\n                <a href="/blog/">Blog</a>',
                1  # Only replace first occurrence (nav)
            )

            # Pattern 2: page-footer - add before Blog link in footer
            # The footer Blog link may have different indentation
            if '<footer class="page-footer">' in content:
                footer_start = content.rfind('<footer class="page-footer">')
                footer_end = content.find('</footer>', footer_start)
                if footer_start > 0 and footer_end > footer_start:
                    footer_section = content[footer_start:footer_end]
                    blog_pos = footer_section.find('<a href="/blog/">')
                    if blog_pos > 0:
                        new_footer = (footer_section[:blog_pos] +
                                     '<a href="/retire/">Retire Abroad</a>\n            ' +
                                     footer_section[blog_pos:])
                        content = content[:footer_start] + new_footer + content[footer_end:]

            if content != original:
                with open(f, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                stats['updated'] += 1
            else:
                stats['skipped'] += 1

        except Exception as e:
            print(f"  ERROR: {os.path.relpath(f, BASE)}: {e}")
            stats['errors'] += 1

print(f"\nDone: {stats['updated']} updated, {stats['skipped']} skipped, {stats['errors']} errors")
