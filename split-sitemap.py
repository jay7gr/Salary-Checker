#!/usr/bin/env python3
"""
Splits the single sitemap.xml (10,421 URLs, 1.1MB) into multiple smaller
sitemaps + a sitemap index file.

The hosting provider truncates the single large sitemap, resulting in
malformed XML that Google rejects — explaining zero indexing after a week.

Split into chunks of ~2,000 URLs each to stay well under any size limits.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITEMAP_PATH = os.path.join(BASE_DIR, 'sitemap.xml')
CHUNK_SIZE = 2000

# Read all URLs from current sitemap
with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

urls = re.findall(r'<url>.*?</url>', content, re.DOTALL)
print(f"Found {len(urls)} URLs in sitemap.xml")

# Split into chunks and write individual sitemaps
num_chunks = (len(urls) + CHUNK_SIZE - 1) // CHUNK_SIZE
sitemap_files = []

for i in range(num_chunks):
    chunk = urls[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
    filename = f'sitemap-{i + 1}.xml'
    filepath = os.path.join(BASE_DIR, filename)

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url_entry in chunk:
        sitemap_content += f'  {url_entry}\n'
    sitemap_content += '</urlset>\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)

    size_kb = os.path.getsize(filepath) / 1024
    print(f"  {filename}: {len(chunk)} URLs ({size_kb:.0f} KB)")
    sitemap_files.append(filename)

# Write sitemap index
index_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
index_content += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for filename in sitemap_files:
    index_content += f'  <sitemap>\n'
    index_content += f'    <loc>https://salary-converter.com/{filename}</loc>\n'
    index_content += f'    <lastmod>2026-02-20</lastmod>\n'
    index_content += f'  </sitemap>\n'
index_content += '</sitemapindex>\n'

with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"\nRewrote sitemap.xml as sitemap index pointing to {num_chunks} sitemaps")
print("Done! Deploy all sitemap-*.xml files + the new sitemap.xml")
