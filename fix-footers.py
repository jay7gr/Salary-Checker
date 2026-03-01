#!/usr/bin/env python3
"""
Add About, Terms, and Privacy links to all page footers.

Two footer patterns:
1. Generated pages (city, compare, salary-needed, salary, rankings):
   <footer class="page-footer">
       <a href="...">...</a>
       ...
   </footer>

2. Blog pages (blog/index.html, blog/articles/*.html):
   <footer class="footer">
       <div class="footer-inner">
           ...
           <div class="footer-links">
               <a href="...">...</a>
           </div>
       </div>
   </footer>

Idempotency: Skips files that already have '/about/' in footer.
"""
import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))

# Links to add
TRUST_LINKS_PAGE_FOOTER = '''
            <a href="/about/">About</a>
            <a href="/privacy/">Privacy</a>
            <a href="/terms/">Terms</a>'''

TRUST_LINKS_BLOG_FOOTER = '''
                <a href="/about/">About</a>
                <a href="/terms/">Terms</a>'''

# File patterns to scan
PATTERNS = [
    'city/**/*.html',
    'compare/**/*.html',
    'salary-needed/**/*.html',
    'salary/*.html',
    'rankings/*.html',
    'blog/articles/*.html',
    'blog/index.html',
]

stats = {'updated': 0, 'skipped': 0, 'errors': 0}

for pattern in PATTERNS:
    files = sorted(glob.glob(os.path.join(BASE, pattern), recursive=True))
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Skip if already has /about/ link
            if '/about/' in content:
                stats['skipped'] += 1
                continue

            original = content

            # Pattern 1: page-footer (generated pages)
            if '<footer class="page-footer">' in content:
                # Insert links before </footer>
                # Find the last link before </footer>
                footer_close = content.find('</footer>')
                if footer_close > 0:
                    # Check if /privacy/ already exists (some pages have it, some don't)
                    has_privacy = '/privacy/' in content[content.rfind('<footer', 0, footer_close):footer_close]

                    if has_privacy:
                        # Only add About and Terms
                        links = '\n            <a href="/about/">About</a>\n            <a href="/terms/">Terms</a>'
                    else:
                        links = TRUST_LINKS_PAGE_FOOTER

                    content = content[:footer_close] + links + '\n        ' + content[footer_close:]

            # Pattern 2: blog footer with footer-links div
            elif '<footer class="footer">' in content:
                # Find </div> that closes footer-links
                footer_links_start = content.find('<div class="footer-links">')
                if footer_links_start > 0:
                    # Find the closing </div> for footer-links
                    # It's the first </div> after the footer-links opening
                    close_div = content.find('</div>', footer_links_start + 25)
                    if close_div > 0:
                        has_privacy = '/privacy/' in content[footer_links_start:close_div]

                        if has_privacy:
                            # Only add About and Terms (privacy already there)
                            links = TRUST_LINKS_BLOG_FOOTER
                        else:
                            links = '\n                <a href="/about/">About</a>\n                <a href="/privacy/">Privacy</a>\n                <a href="/terms/">Terms</a>'

                        content = content[:close_div] + links + '\n            ' + content[close_div:]

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
