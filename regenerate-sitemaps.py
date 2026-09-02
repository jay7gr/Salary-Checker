#!/usr/bin/env python3
"""
Regenerate sitemaps for salary-converter.com.

Includes live money URLs: city pages, neighborhood pages (/city/{city}/{hood}),
city-vs-city compare pages, /salary-needed/{city} and hood-level salary-needed
when those HTML files exist.

Excludes: /404, /admin/*, nested compare/{city}/* (nhood-vs-nhood, gitignored,
Cloudflare Pages 20k cap), encoding-duplicate slugs, embed/widget one-offs.

lastmod is the HTML file's mtime (UTC date), not a fake global stamp.
"""
import os
import glob
import re
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
CHUNK_SIZE = 500
BASE_URL = 'https://salary-converter.com'

PRIORITY = {
    '': 0,
    'blog': 1,
    'rankings': 2,
    'city': 3,
    'retire': 4,
    'compare': 5,
    'salary': 6,
    'salary-needed': 7,
    'methodology': 8,
    'widget': 9,
    'privacy': 10,
}

EXCLUDE_PREFIXES = ('admin/',)
EXCLUDE_FILES = {'404.html', 'embed.html', 'retire-embed.html', 'widget.html'}


def load_redirect_sources():
    """Paths that _redirects already 301s away — do not list the dupe in sitemap."""
    sources = set()
    path = os.path.join(ROOT, '_redirects')
    if not os.path.isfile(path):
        return sources
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2 and parts[0].startswith('/'):
                sources.add(parts[0].rstrip('/'))
    return sources


REDIRECT_SOURCES = load_redirect_sources()


def is_encoding_dupe(rel_path):
    if '%' in rel_path:
        return True
    if any(ord(c) > 127 for c in rel_path):
        return True
    return False


def should_include(rel_path):
    rel_path = rel_path.replace('\\', '/')
    if rel_path in EXCLUDE_FILES or rel_path.startswith(EXCLUDE_PREFIXES):
        return False
    if is_encoding_dupe(rel_path):
        return False

    parts = rel_path.strip('/').split('/')

    if rel_path == 'index.html':
        return True

    if len(parts) == 1:
        return True

    section = parts[0]

    if section in ('blog', 'rankings', 'salary', 'retire', 'methodology'):
        return True

    # City: hub, city page, and neighborhood pages
    if section == 'city':
        return len(parts) in (2, 3)

    # City-vs-city only. Nested compare/{city}/* is banned (Pages cap).
    if section == 'compare':
        if len(parts) != 2:
            return False
        filename = parts[1].replace('.html', '')
        if filename == 'index':
            return True
        return '-vs-' in filename

    # Hub, /salary-needed/{city}, and hood-level if the HTML exists
    if section == 'salary-needed':
        return True

    return True


def html_to_path(filepath):
    rel = os.path.relpath(filepath, ROOT).replace('\\', '/')
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        rel = rel[:-len('index.html')]
        return '/' + rel
    if rel.endswith('.html'):
        rel = rel[:-len('.html')]
    if rel in ('embed', '404', 'admin/embeds', 'admin/feedback'):
        return None
    return '/' + rel


def html_to_url(filepath):
    path = html_to_path(filepath)
    if path is None:
        return None
    if path in REDIRECT_SOURCES:
        return None
    if path == '/':
        return f'{BASE_URL}/'
    return f'{BASE_URL}{path}'


def lastmod_for(filepath):
    ts = os.path.getmtime(filepath)
    return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()


def sort_key(item):
    url = item[0]
    path = url.replace(BASE_URL, '').strip('/')
    parts = path.split('/')
    section = parts[0] if parts[0] else ''
    priority = PRIORITY.get(section, 99)
    return (priority, path)


entries = {}  # url -> lastmod
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
    if not url:
        skipped += 1
        continue
    lm = lastmod_for(filepath)
    if url not in entries or lm > entries[url]:
        entries[url] = lm

entries[f'{BASE_URL}/'] = entries.get(f'{BASE_URL}/', lastmod_for(os.path.join(ROOT, 'index.html')))

items = sorted(entries.items(), key=sort_key)

print(f'Total HTML files on disk: {total_on_disk}')
print(f'Included in sitemap: {len(items)}')
print(f'Excluded: {skipped}')
print()

sections = {}
for url, _lm in items:
    path = url.replace(BASE_URL, '').strip('/')
    section = path.split('/')[0] if '/' in path else (path or 'homepage')
    sections[section] = sections.get(section, 0) + 1

for section, count in sorted(sections.items(), key=lambda x: -x[1]):
    print(f'  {section}: {count} URLs')

for pattern in ['sitemap-*.xml', 'sitemap-s*.xml']:
    for old in glob.glob(os.path.join(ROOT, pattern)):
        os.remove(old)
        print(f'  Removed old: {os.path.basename(old)}')

num_chunks = (len(items) + CHUNK_SIZE - 1) // CHUNK_SIZE
sitemap_files = []

for i in range(num_chunks):
    chunk = items[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
    filename = f'sitemap-s{i + 1}.xml'
    filepath = os.path.join(ROOT, filename)
    xml_entries = ''
    for url, lm in chunk:
        xml_entries += f'  <url><loc>{url}</loc><lastmod>{lm}</lastmod></url>\n'
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{xml_entries}</urlset>\n'
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    size_kb = os.path.getsize(filepath) / 1024
    print(f'  {filename}: {len(chunk)} URLs ({size_kb:.0f} KB)')
    sitemap_files.append((filename, max(lm for _u, lm in chunk)))

index_entries = ''
for filename, lm in sitemap_files:
    index_entries += (
        f'  <sitemap>\n'
        f'    <loc>{BASE_URL}/{filename}</loc>\n'
        f'    <lastmod>{lm}</lastmod>\n'
        f'  </sitemap>\n'
    )

index_content = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'{index_entries}</sitemapindex>\n'
)

with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f'\nDone: sitemap.xml index + {num_chunks} sitemaps ({len(items)} total URLs)')
