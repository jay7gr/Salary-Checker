#!/usr/bin/env python3
"""
Strip .html extensions from all internal URLs across the entire site.

The hosting provider (Cloudflare Pages) serves pages at clean URLs (no .html)
and 308-redirects .html requests. Having .html in sitemaps, canonical tags,
OG URLs, internal links, and schema markup wastes crawl budget and confuses
Google indexing.

This script:
1. Processes all HTML files in city/, compare/, salary-needed/, blog/
2. Strips .html from internal URLs (href, canonical, og:url, schema, share bars)
3. Updates all 6 sitemap files
4. Does NOT touch the homepage (index.html) URL — that stays as /
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def strip_html_ext(content):
    """Remove .html from internal salary-converter.com URLs and relative paths."""
    # Absolute URLs: https://salary-converter.com/anything.html → drop .html
    # But NOT index.html (homepage) or widget.html
    content = re.sub(
        r'(https://salary-converter\.com/(?:city|compare|salary-needed|blog/articles)/[^"\'>\s]+?)\.html',
        r'\1',
        content
    )
    # Also handle blog index: /blog/index.html → /blog/ (but blog/ alone is fine)
    # And the directory index pages
    content = re.sub(
        r'(https://salary-converter\.com/(?:city|compare|salary-needed|blog))/index\.html',
        r'\1/',
        content
    )

    # Relative URLs: href="/city/london.html" → href="/city/london"
    content = re.sub(
        r'(href|src|content|item)="(/(?:city|compare|salary-needed|blog/articles)/[^"]+?)\.html"',
        r'\1="\2"',
        content
    )
    # Relative directory index: href="/blog/index.html" → href="/blog/"
    content = re.sub(
        r'(href|src|content|item)="(/(?:city|compare|salary-needed|blog))/index\.html"',
        r'\1="\2/"',
        content
    )

    return content


def process_html_files():
    """Process all HTML files across all directories."""
    patterns = [
        os.path.join(BASE_DIR, 'city', '**', '*.html'),
        os.path.join(BASE_DIR, 'compare', '**', '*.html'),
        os.path.join(BASE_DIR, 'salary-needed', '**', '*.html'),
        os.path.join(BASE_DIR, 'blog', '**', '*.html'),
        os.path.join(BASE_DIR, 'index.html'),
    ]

    total = 0
    modified = 0

    for pattern in patterns:
        for filepath in glob.glob(pattern, recursive=True):
            total += 1
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = strip_html_ext(content)

            if new_content != content:
                modified += 1
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

    print(f"Processed {total} HTML files, modified {modified}")


def process_sitemaps():
    """Strip .html from all sitemap URLs."""
    modified = 0
    for i in range(1, 7):
        filepath = os.path.join(BASE_DIR, f'sitemap-{i}.xml')
        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Strip .html from all <loc> URLs (except index.html and widget.html)
        new_content = re.sub(
            r'(<loc>https://salary-converter\.com/(?:city|compare|salary-needed|blog/articles)/[^<]+?)\.html(</loc>)',
            r'\1\2',
            content
        )
        # Handle directory index pages
        new_content = re.sub(
            r'(<loc>https://salary-converter\.com/(?:city|compare|salary-needed|blog))/index\.html(</loc>)',
            r'\1/\2',
            new_content
        )

        if new_content != content:
            modified += 1
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

    print(f"Updated {modified} sitemap files")


if __name__ == '__main__':
    print("Stripping .html extensions from all internal URLs...")
    print()
    process_html_files()
    process_sitemaps()
    print()
    print("Done! Deploy and resubmit sitemap to Google Search Console.")
