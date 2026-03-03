#!/usr/bin/env python3
"""
Regenerate sitemaps with SMART FILTERING for SEO crawl budget optimization.

Instead of submitting all 13,000+ URLs (most of which Google ignores),
we focus on high-value pages that are most likely to get indexed and rank.

Strategy:
- Homepage, blog, rankings, salary hub pages: ALWAYS include
- City pages: main city pages only (no neighborhoods)
- Compare pages: only major city pairs (top 30 cities × top 30 cities)
- Retire pages: all (they're high-value, unique content)
- Salary-needed: hub page only (noindex on individual pages)
- Neighborhoods: EXCLUDE (too thin, dilutes crawl budget)

Produces sitemap-s1.xml through sitemap-sN.xml + sitemap.xml index.
"""
import os
import glob
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
CHUNK_SIZE = 500
TODAY = date.today().isoformat()
BASE_URL = 'https://salary-converter.com'

# Top 30 cities by search volume / importance — these get compare pages in sitemap
TOP_CITIES = {
    'london', 'new-york', 'paris', 'tokyo', 'dubai', 'singapore',
    'hong-kong', 'san-francisco', 'los-angeles', 'sydney',
    'toronto', 'berlin', 'amsterdam', 'barcelona', 'miami',
    'chicago', 'seattle', 'boston', 'melbourne', 'munich',
    'zurich', 'geneva', 'copenhagen', 'stockholm', 'dublin',
    'lisbon', 'bangkok', 'shanghai', 'austin', 'denver',
}

# Priority order for URL sorting
PRIORITY = {
    '': 0,           # homepage
    'blog': 1,       # blog posts rank best — put first
    'rankings': 2,
    'city': 3,
    'retire': 4,
    'compare': 5,
    'salary': 6,
    'salary-needed': 7,
    'widget': 8,
    'privacy': 9,
}


def should_include(rel_path):
    """Decide if a page should be included in the sitemap."""
    parts = rel_path.strip('/').split('/')

    # Always include root pages
    if len(parts) == 1:
        return True

    section = parts[0]

    # Blog: include everything
    if section == 'blog':
        return True

    # Rankings: include everything
    if section == 'rankings':
        return True

    # Salary pages: include everything (only ~38 pages)
    if section == 'salary':
        return True

    # Retire: include everything (439 pages, all high-value unique content)
    if section == 'retire':
        return True

    # City pages: only main city pages (city/london), not neighborhoods (city/london/mayfair)
    if section == 'city':
        # city/index.html or city/london.html → include
        # city/london/mayfair.html → exclude
        return len(parts) == 2

    # Compare pages: only top city × top city comparisons (no neighborhoods)
    if section == 'compare':
        # compare/index.html → include
        if len(parts) == 2:
            filename = parts[1].replace('.html', '')
            # Must be city1-vs-city2 format
            if '-vs-' in filename:
                city1, city2 = filename.split('-vs-', 1)
                return city1 in TOP_CITIES and city2 in TOP_CITIES
            # Hub page
            return filename == 'index'
        return False

    # Salary-needed: only the hub page
    if section == 'salary-needed':
        return len(parts) == 1 or (len(parts) == 2 and parts[1] in ('index.html', ''))

    # Privacy, widget etc
    return True


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
            return None
        return f'{BASE_URL}/{rel}'
    return f'{BASE_URL}/{rel}' if rel else f'{BASE_URL}/'


def sort_key(url):
    """Sort URLs by directory priority, then alphabetically."""
    path = url.replace(BASE_URL, '').strip('/')
    parts = path.split('/')
    section = parts[0] if parts[0] else ''
    priority = PRIORITY.get(section, 99)
    return (priority, path)


# Collect URLs with filtering
urls = set()
skipped = 0
total_on_disk = 0

for filepath in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    if '/.' in filepath:
        continue
    total_on_disk += 1

    rel = os.path.relpath(filepath, ROOT)

    if not should_include(rel):
        skipped += 1
        continue

    url = html_to_url(filepath)
    if url:
        urls.add(url)

# Ensure homepage
urls.add(f'{BASE_URL}/')

# Sort
urls = sorted(urls, key=sort_key)

print(f'Total HTML files on disk: {total_on_disk}')
print(f'Included in sitemap: {len(urls)}')
print(f'Excluded (thin/neighborhood): {skipped}')
print(f'Reduction: {100 - len(urls) / total_on_disk * 100:.0f}%')
print()

# Breakdown by section
sections = {}
for url in urls:
    path = url.replace(BASE_URL, '').strip('/')
    section = path.split('/')[0] if '/' in path else (path or 'homepage')
    sections[section] = sections.get(section, 0) + 1

for section, count in sorted(sections.items(), key=lambda x: -x[1]):
    print(f'  {section}: {count} URLs')

# Remove old sitemap files
for pattern in ['sitemap-*.xml', 'sitemap-s*.xml']:
    for old in glob.glob(os.path.join(ROOT, pattern)):
        os.remove(old)
        print(f'  Removed old: {os.path.basename(old)}')

# Split into chunks and write sitemaps
num_chunks = (len(urls) + CHUNK_SIZE - 1) // CHUNK_SIZE
sitemap_files = []

for i in range(num_chunks):
    chunk = urls[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
    filename = f'sitemap-s{i + 1}.xml'
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
