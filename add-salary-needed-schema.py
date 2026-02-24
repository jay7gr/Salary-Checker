#!/usr/bin/env python3
"""
Add Article JSON-LD schema to all salary-needed pages (~2,214 pages).

These pages already have FAQPage + BreadcrumbList schemas. This script adds
an Article schema block between the BreadcrumbList </script> and <style> tags
to improve rich snippet eligibility in search results.

Data is extracted from existing page content (title, meta description, canonical URL).

Idempotent: skips pages that already contain '"Article"' in their content.
"""

import os
import re
import json
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

stats = {'updated': 0, 'skipped_already': 0, 'skipped_no_data': 0, 'errors': 0}


def extract_page_data(content):
    """Extract headline, description, and canonical URL from the page HTML."""
    data = {}

    # Title / headline
    title_m = re.search(r'<title>(.+?)</title>', content)
    if not title_m:
        return None
    data['headline'] = title_m.group(1).strip()

    # Meta description
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', content)
    data['description'] = desc_m.group(1) if desc_m else ''

    # Canonical URL
    canon_m = re.search(r'<link rel="canonical" href="([^"]*)"', content)
    data['url'] = canon_m.group(1) if canon_m else ''

    return data


def build_article_schema(data):
    """Build Article JSON-LD schema."""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": data['headline'],
        "description": data['description'],
        "url": data['url'],
        "datePublished": "2026-02-18",
        "dateModified": "2026-02-23",
        "publisher": {
            "@type": "Organization",
            "name": "salary:converter",
            "url": "https://salary-converter.com"
        }
    }


def process_file(filepath):
    """Add Article schema to a single salary-needed page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # Idempotency: skip if Article schema already present
        if '"Article"' in content:
            stats['skipped_already'] += 1
            return

        # Extract data from page
        data = extract_page_data(content)
        if not data:
            stats['skipped_no_data'] += 1
            return

        # Build schema
        article = build_article_schema(data)

        # Format as JSON-LD script block
        article_block = '    <script type="application/ld+json">\n    ' + json.dumps(article, indent=8, ensure_ascii=False) + '\n    </script>'

        # Insert after the BreadcrumbList </script> block, before <style>
        # The page structure is: FAQPage <script>...</script> then BreadcrumbList <script>...</script> then <style>
        # We want to insert after the BreadcrumbList closing </script> and before <style>
        # Find the pattern: </script>\n    <style>  (the last </script> before <style>)
        pattern = r'(</script>\n)(\s*<style>)'
        matches = list(re.finditer(pattern, content))
        if matches:
            # Use the last match (which is the BreadcrumbList </script> before <style>)
            match = matches[-1]
            insert_pos = match.end(1)
            content = content[:insert_pos] + article_block + '\n' + content[insert_pos:]
        else:
            # Fallback: insert before </head>
            content = content.replace('</head>', article_block + '\n</head>')

        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        stats['updated'] += 1

    except Exception as e:
        print(f'  ERROR {filepath}: {e}')
        stats['errors'] += 1


def main():
    print('Adding Article schema to salary-needed pages...\n')

    # Process city-level pages: salary-needed/{city}.html
    city_files = sorted(glob.glob(os.path.join(BASE, 'salary-needed', '*.html')))
    city_count_before = stats['updated']
    for filepath in city_files:
        process_file(filepath)
    city_updated = stats['updated'] - city_count_before
    print(f'  City-level pages: {city_updated} updated (of {len(city_files)} total)')

    # Process neighborhood-level pages: salary-needed/{city}/*.html
    neighborhood_total = 0
    neighborhood_updated_total = 0
    for city_dir in sorted(glob.glob(os.path.join(BASE, 'salary-needed', '*'))):
        if not os.path.isdir(city_dir):
            continue

        city_slug = os.path.basename(city_dir)
        neigh_files = sorted(glob.glob(os.path.join(city_dir, '*.html')))
        if not neigh_files:
            continue

        neighborhood_total += len(neigh_files)
        prev_updated = stats['updated']
        for filepath in neigh_files:
            process_file(filepath)

        city_updated = stats['updated'] - prev_updated
        neighborhood_updated_total += city_updated
        if city_updated > 0:
            print(f'  {city_slug}: {city_updated} neighborhood pages updated')

    print(f'\n  Neighborhood-level pages: {neighborhood_updated_total} updated (of {neighborhood_total} total)')
    print(f'\n=== TOTAL: {stats["updated"]} updated, {stats["skipped_already"]} already had Article, {stats["skipped_no_data"]} skipped (no data), {stats["errors"]} errors ===')


if __name__ == '__main__':
    main()
