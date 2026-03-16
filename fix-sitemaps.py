#!/usr/bin/env python3
"""
Fix sitemap gap: Add missing pages to sitemaps.
Scans all HTML files, reads existing sitemap URLs, generates new sitemap files
for any missing pages.
"""

import os
import glob
import re
from datetime import date

BASE_URL = 'https://salary-converter.com'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_URLS_PER_SITEMAP = 2000
TODAY = date.today().isoformat()  # 2026-03-12

# Files to exclude from sitemaps
EXCLUDE_FILES = {
    '404.html',
    'embed.html',
    'retire-embed.html',
    'widget.html',
}


def get_all_page_urls():
    """Scan all HTML files and return their URLs."""
    urls = set()
    for filepath in glob.glob(os.path.join(PROJECT_DIR, '**', '*.html'), recursive=True):
        # Get relative path
        rel = os.path.relpath(filepath, PROJECT_DIR)

        # Skip excluded files
        if os.path.basename(rel) in EXCLUDE_FILES:
            continue

        # Skip scripts and non-page files
        if rel.startswith('.') or rel.startswith('node_modules'):
            continue

        # Convert file path to URL
        # Remove .html extension for clean URLs (except index.html which becomes /)
        if rel == 'index.html':
            url = BASE_URL + '/'
        elif rel.endswith('/index.html'):
            # e.g., blog/index.html -> /blog/
            url = BASE_URL + '/' + rel.replace('/index.html', '') + '/'
        elif rel == 'blog/index.html':
            url = BASE_URL + '/blog/'
        else:
            # e.g., city/new-york.html -> /city/new-york
            url = BASE_URL + '/' + rel.replace('.html', '')

        urls.add(url)

    return urls


def get_existing_sitemap_urls():
    """Read all existing sitemap files and return the set of URLs already included."""
    urls = set()
    for sitemap_file in sorted(glob.glob(os.path.join(PROJECT_DIR, 'sitemap-s*.xml'))):
        with open(sitemap_file, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in re.finditer(r'<loc>(.*?)</loc>', content):
            urls.add(match.group(1))
    return urls


def generate_sitemap_xml(urls, lastmod):
    """Generate sitemap XML content for a list of URLs."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in sorted(urls):
        lines.append(f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod></url>')
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def update_sitemap_index(new_sitemap_names):
    """Add new sitemap references to sitemap.xml index."""
    index_path = os.path.join(PROJECT_DIR, 'sitemap.xml')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Insert new sitemap entries before </sitemapindex>
    new_entries = ''
    for name in new_sitemap_names:
        new_entries += f'  <sitemap>\n    <loc>{BASE_URL}/{name}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </sitemap>\n'

    content = content.replace('</sitemapindex>', new_entries + '</sitemapindex>')

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    # Step 1: Get all page URLs from disk
    all_urls = get_all_page_urls()
    print(f'Total page URLs on disk: {len(all_urls)}')

    # Step 2: Get existing sitemap URLs
    existing_urls = get_existing_sitemap_urls()
    print(f'URLs already in sitemaps: {len(existing_urls)}')

    # Step 3: Find missing URLs
    missing_urls = all_urls - existing_urls
    print(f'Missing URLs to add: {len(missing_urls)}')

    if not missing_urls:
        print('No missing URLs. Sitemaps are complete!')
        return

    # Show breakdown
    categories = {}
    for url in missing_urls:
        path = url.replace(BASE_URL, '')
        if '/city/' in path and path.count('/') >= 3:
            cat = 'city neighborhoods'
        elif '/city/' in path:
            cat = 'city top-level'
        elif '/salary-needed/' in path and path.count('/') >= 3:
            cat = 'salary-needed neighborhoods'
        elif '/salary-needed/' in path:
            cat = 'salary-needed top-level'
        elif '/compare/' in path:
            cat = 'compare'
        elif '/retire/' in path:
            cat = 'retire'
        elif '/salary/' in path:
            cat = 'salary'
        elif '/blog/' in path:
            cat = 'blog'
        elif '/rankings/' in path:
            cat = 'rankings'
        else:
            cat = 'other'
        categories[cat] = categories.get(cat, 0) + 1

    print('\nMissing URL breakdown:')
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {count}')

    # Step 4: Split into sitemap files
    missing_list = sorted(missing_urls)
    chunks = [missing_list[i:i + MAX_URLS_PER_SITEMAP]
              for i in range(0, len(missing_list), MAX_URLS_PER_SITEMAP)]

    # Find the next available sitemap number
    existing_numbers = []
    for f in glob.glob(os.path.join(PROJECT_DIR, 'sitemap-s*.xml')):
        match = re.search(r'sitemap-s(\d+)\.xml', f)
        if match:
            existing_numbers.append(int(match.group(1)))
    next_num = max(existing_numbers) + 1 if existing_numbers else 1

    new_sitemap_names = []
    for i, chunk in enumerate(chunks):
        sitemap_name = f'sitemap-s{next_num + i}.xml'
        sitemap_path = os.path.join(PROJECT_DIR, sitemap_name)
        xml_content = generate_sitemap_xml(chunk, TODAY)

        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)

        size_kb = len(xml_content.encode('utf-8')) / 1024
        print(f'\nCreated {sitemap_name}: {len(chunk)} URLs ({size_kb:.1f} KB)')
        new_sitemap_names.append(sitemap_name)

    # Step 5: Update sitemap index
    update_sitemap_index(new_sitemap_names)
    print(f'\nUpdated sitemap.xml with {len(new_sitemap_names)} new sitemap references')

    # Final summary
    total_after = len(existing_urls) + len(missing_urls)
    print(f'\n=== Summary ===')
    print(f'Before: {len(existing_urls)} URLs in sitemaps')
    print(f'Added: {len(missing_urls)} URLs')
    print(f'After: {total_after} URLs total')
    print(f'New sitemaps created: {", ".join(new_sitemap_names)}')


if __name__ == '__main__':
    main()
