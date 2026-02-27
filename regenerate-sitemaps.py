#!/usr/bin/env python3
"""
Regenerate all sitemaps from actual HTML files on disk.
More robust than relying on data structures — captures every page that exists.

Produces sitemap-1.xml through sitemap-N.xml (2,000 URLs each) + sitemap.xml index.
Cleans up any stale sitemap-N.xml files from previous runs.
"""
import os
import glob
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
CHUNK_SIZE = 2000
TODAY = date.today().isoformat()
BASE_URL = 'https://salary-converter.com'

# Priority order for URL sorting (homepage first, then hubs, then pages)
PRIORITY = {
    '': 0,           # homepage
    'widget': 1,
    'city': 2,
    'compare': 3,
    'salary-needed': 4,
    'blog': 5,
    'privacy': 6,
}

def html_to_url(filepath):
    """Convert a file path to its canonical URL."""
    rel = os.path.relpath(filepath, ROOT)
    # Remove .html extension
    if rel.endswith('/index.html'):
        rel = rel[:-len('/index.html')]
    elif rel.endswith('.html'):
        rel = rel[:-len('.html')]
    # Skip non-page files
    if rel in ('widget', 'embed'):
        if rel == 'embed':
            return None  # embed.html is not a public page
        return f'{BASE_URL}/{rel}'
    return f'{BASE_URL}/{rel}' if rel else f'{BASE_URL}/'

def sort_key(url):
    """Sort URLs by directory priority, then alphabetically."""
    path = url.replace(BASE_URL, '').strip('/')
    parts = path.split('/')
    section = parts[0] if parts[0] else ''
    priority = PRIORITY.get(section, 99)
    return (priority, path)

# Collect all URLs from HTML files on disk
urls = set()

for filepath in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    # Skip hidden dirs
    if '/.' in filepath:
        continue
    url = html_to_url(filepath)
    if url:
        urls.add(url)

# Also add the homepage explicitly (index.html -> /)
urls.add(f'{BASE_URL}/')

# Sort for consistent output
urls = sorted(urls, key=sort_key)
print(f'Found {len(urls)} URLs from HTML files on disk')

# Verify key pages are present
checks = ['/salary-needed/', '/privacy/', '/city/', '/compare/', '/blog/']
for check in checks:
    matching = [u for u in urls if check in u]
    print(f'  {check}: {len(matching)} URLs')

# Remove old sitemap files
for old in glob.glob(os.path.join(ROOT, 'sitemap-*.xml')):
    os.remove(old)
    print(f'  Removed old: {os.path.basename(old)}')

# Split into chunks and write individual sitemaps
num_chunks = (len(urls) + CHUNK_SIZE - 1) // CHUNK_SIZE
sitemap_files = []

for i in range(num_chunks):
    chunk = urls[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
    filename = f'sitemap-{i + 1}.xml'
    filepath = os.path.join(ROOT, filename)

    xml_entries = ''
    for url in chunk:
        xml_entries += f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>\n'

    content = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{xml_entries}</urlset>\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    size_kb = os.path.getsize(filepath) / 1024
    print(f'  {filename}: {len(chunk)} URLs ({size_kb:.0f} KB)')
    sitemap_files.append(filename)

# Write sitemap index
index_entries = ''
for filename in sitemap_files:
    index_entries += f'  <sitemap>\n    <loc>{BASE_URL}/{filename}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </sitemap>\n'

index_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{index_entries}</sitemapindex>\n'

with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f'\nDone: sitemap.xml index + {num_chunks} sitemaps ({len(urls)} total URLs)')
