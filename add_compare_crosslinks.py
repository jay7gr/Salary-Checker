#!/usr/bin/env python3
"""Add cross-links from compare pages to salary-needed pages."""
import os
import re

COMPARE_DIR = 'compare'
SALARY_DIR = 'salary-needed'

# Get all salary-needed city slugs
salary_cities = set()
for f in os.listdir(SALARY_DIR):
    if f.endswith('.html') and not f.startswith('.'):
        salary_cities.add(f.replace('.html', ''))

print(f"Found {len(salary_cities)} salary-needed city pages")

crosslink_html = '''
    <div style="margin:24px auto;max-width:800px;padding:0 16px;">
        <p style="font-size:0.95rem;color:var(--text-secondary,#888);margin:0 0 8px;">
            <strong>Related:</strong> How much salary do you need to live comfortably?
        </p>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
            {links}
        </div>
    </div>
'''

link_template = '<a href="/salary-needed/{slug}" style="color:var(--accent,#4a90d9);text-decoration:none;padding:4px 12px;border:1px solid var(--accent,#4a90d9);border-radius:16px;font-size:0.85rem;">Salary needed in {name}</a>'

count = 0
skipped = 0

for fname in sorted(os.listdir(COMPARE_DIR)):
    if not fname.endswith('.html') or not '-vs-' in fname:
        continue

    fpath = os.path.join(COMPARE_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Already has cross-links?
    if 'salary-needed/' in content:
        skipped += 1
        continue

    # Extract city slugs from filename: city1-vs-city2.html
    base = fname.replace('.html', '')
    parts = base.split('-vs-')
    if len(parts) != 2:
        continue

    city1_slug, city2_slug = parts

    # Build links for cities that have salary-needed pages
    links = []
    for slug in [city1_slug, city2_slug]:
        if slug in salary_cities:
            name = slug.replace('-', ' ').title()
            links.append(link_template.format(slug=slug, name=name))

    if not links:
        continue

    links_html = crosslink_html.format(links='\n            '.join(links))

    # Insert before </body>
    content = content.replace('</body>', links_html + '\n</body>')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    count += 1

print(f"Updated {count} compare pages with salary-needed cross-links")
print(f"Skipped {skipped} (already had links)")
