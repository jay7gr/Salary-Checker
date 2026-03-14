#!/usr/bin/env python3
"""
Add AI disclaimer line to all page footers across the site.

Handles four footer patterns:
1. site-footer (homepage, retire/index.html)
2. page-footer (city, compare, salary-needed, retire subpages, salary, rankings, data)
3. footer with footer-inner (blog, about, privacy, terms, widget)
4. plain footer (retire blog articles)

Uses inline styles to avoid injecting CSS into varied <style> blocks.
Idempotency: Skips files that already contain 'ai-disclaimer'.
"""
import os
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Inline-styled disclaimer variants for each footer pattern
DISCLAIMER_SITE_FOOTER = '        <p class="ai-disclaimer" style="font-size:0.72rem;color:var(--text-secondary);margin-top:14px;letter-spacing:0.01em;">AI-powered salary insights &mdash; built with real cost-of-living data and <a href="/about/#how-we-use-ai" style="color:var(--text-secondary);text-decoration:underline;text-underline-offset:2px;">verified by our team</a>.</p>'

DISCLAIMER_PAGE_FOOTER = '            <p class="ai-disclaimer" style="width:100%;font-size:0.72rem;color:var(--text-secondary);margin-top:8px;text-align:center;">AI-powered salary insights &mdash; built with real cost-of-living data and <a href="/about/#how-we-use-ai" style="color:var(--text-secondary);text-decoration:underline;text-underline-offset:2px;">verified by our team</a>.</p>'

DISCLAIMER_BLOG_FOOTER = '            <p class="ai-disclaimer" style="font-size:0.72rem;color:var(--text-secondary);margin-top:12px;">AI-powered salary insights &mdash; built with real cost-of-living data and <a href="/about/#how-we-use-ai" style="color:var(--text-secondary);text-decoration:underline;text-underline-offset:2px;">verified by our team</a>.</p>'

DISCLAIMER_PLAIN_FOOTER = '        <p class="ai-disclaimer" style="font-size:0.72rem;color:var(--text-secondary);margin-top:8px;">AI-powered salary insights &mdash; built with real cost-of-living data and <a href="/about/#how-we-use-ai" style="color:var(--text-secondary);text-decoration:underline;text-underline-offset:2px;">verified by our team</a>.</p>'

# All HTML file patterns to process
PATTERNS = [
    'city/**/*.html',
    'compare/**/*.html',
    'salary-needed/**/*.html',
    'salary/*.html',
    'rankings/*.html',
    'data/*.html',
    'retire/**/*.html',
    'blog/**/*.html',
    'privacy/index.html',
    'terms/index.html',
    'widget/index.html',
]

# Skip these files (handled manually)
SKIP_FILES = {
    os.path.join(BASE, 'index.html'),
    os.path.join(BASE, 'about', 'index.html'),
}

stats = {'updated': 0, 'skipped': 0, 'errors': 0}

for pattern in PATTERNS:
    files = sorted(glob.glob(os.path.join(BASE, pattern), recursive=True))
    for f in files:
        if f in SKIP_FILES:
            stats['skipped'] += 1
            continue

        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Idempotency: skip if already has disclaimer
            if 'ai-disclaimer' in content:
                stats['skipped'] += 1
                continue

            # Must have a footer to modify
            if '</footer>' not in content:
                stats['skipped'] += 1
                continue

            original = content

            # Determine footer pattern and choose disclaimer variant
            if 'class="site-footer"' in content:
                disclaimer = DISCLAIMER_SITE_FOOTER
            elif 'class="page-footer"' in content:
                disclaimer = DISCLAIMER_PAGE_FOOTER
            elif 'class="footer"' in content:
                # Blog/static pages with footer-inner
                disclaimer = DISCLAIMER_BLOG_FOOTER
            else:
                # Plain footer (retire blogs, etc.)
                disclaimer = DISCLAIMER_PLAIN_FOOTER

            # Insert disclaimer before </footer>
            # Find the LAST </footer> tag (in case of multiple)
            footer_close_idx = content.rfind('</footer>')
            if footer_close_idx > 0:
                content = content[:footer_close_idx] + disclaimer + '\n    ' + content[footer_close_idx:]

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
