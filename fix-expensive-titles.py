#!/usr/bin/env python3
"""
One-time script to optimize title tags, meta descriptions, H1 tags, and
social meta tags across neighborhood and city pages to target
"is [X] expensive?" search queries.

Updates:
- Neighborhood pages (~2,123): title, description, H1, OG/Twitter tags
- City pages (~101): title, description, H1, OG/Twitter tags

Safe to re-run (idempotent): skips files already matching new patterns.
"""

import os
import re
import sys
import glob

# Add project root to path so we can import from generate-pages
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Import data and utilities from generate-pages.py
import importlib.util
spec = importlib.util.spec_from_file_location("generate_pages", os.path.join(BASE_DIR, "generate-pages.py"))
gp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gp)

# Aliases
cityNeighborhoods = gp.cityNeighborhoods
slugify = gp.slugify

stats = {'updated': 0, 'skipped': 0, 'errors': 0}


def compute_title(name, city=None, max_len=60):
    """Build title with length-aware fallback."""
    if city:
        primary = f'Is {name} Expensive? {city} Cost of Living (2026)'
        if len(primary) <= max_len:
            return primary
    fallback = f'Is {name} Expensive? Cost of Living (2026)'
    if len(fallback) <= max_len:
        return fallback
    return f'Is {name} Expensive? Cost of Living'


def compute_city_title(city, max_len=60):
    """Build city page title with length-aware fallback."""
    # &amp; counts as 5 chars in source but Google renders as & (1 char)
    # Use & for length check, &amp; in actual HTML
    primary_display = f'Is {city} Expensive? Cost of Living & Salary Guide (2026)'
    if len(primary_display) <= max_len:
        return f'Is {city} Expensive? Cost of Living &amp; Salary Guide (2026)'
    fallback = f'Is {city} Expensive? Cost of Living Guide (2026)'
    if len(fallback) <= max_len:
        return fallback
    return f'Is {city} Expensive? Cost of Living Guide'


def build_neighborhood_desc(neighborhood, city, pct_diff, rent, rank, total):
    """Build meta description for neighborhood page."""
    if pct_diff > 5:
        price_phrase = f"{pct_diff:.0f}% more expensive than the {city} average"
    elif pct_diff < -5:
        price_phrase = f"{abs(pct_diff):.0f}% cheaper than the {city} average"
    else:
        sign = '+' if pct_diff >= 0 else ''
        price_phrase = f"near the {city} average ({sign}{pct_diff:.0f}%)"

    desc = (
        f"Is {neighborhood} expensive? It's {price_phrase}. "
        f"1BR rent: ~{rent}/mo. "
        f"Ranked #{rank} of {total} neighborhoods. "
        f"See salary needed & full breakdown."
    )
    return desc


# =====================================================
# 1. NEIGHBORHOOD PAGES
# =====================================================
def fix_neighborhood_pages():
    print('Processing neighborhood pages...')
    for city, neighborhoods in sorted(cityNeighborhoods.items()):
        city_slug = slugify(city)
        city_dir = os.path.join(BASE_DIR, 'city', city_slug)
        if not os.path.isdir(city_dir):
            continue

        # Compute rankings (most expensive first)
        sorted_nhoods = sorted(neighborhoods.items(), key=lambda x: x[1], reverse=True)
        total = len(sorted_nhoods)

        city_updated = 0
        for rank_idx, (neighborhood, multiplier) in enumerate(sorted_nhoods):
            rank = rank_idx + 1
            nhood_slug = slugify(neighborhood)
            fpath = os.path.join(city_dir, f'{nhood_slug}.html')
            if not os.path.exists(fpath):
                continue

            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Idempotency: skip if already updated
                if re.search(r'<title>Is .+ Expensive\?', content):
                    stats['skipped'] += 1
                    continue

                pct_diff = (multiplier - 1) * 100

                # Extract rent from existing description
                rent_m = re.search(r'1BR rent: ~([^/]+)/mo', content)
                rent = rent_m.group(1).strip() if rent_m else '?'

                # Build new tags
                new_title = compute_title(neighborhood, city)
                new_desc = build_neighborhood_desc(neighborhood, city, pct_diff, rent, rank, total)

                # 1. Title
                content = re.sub(
                    r'<title>[^<]+</title>',
                    f'<title>{new_title}</title>',
                    content, count=1)

                # 2. Meta description
                content = re.sub(
                    r'(<meta name="description" content=")[^"]*(")',
                    lambda m: m.group(1) + new_desc + m.group(2),
                    content, count=1)

                # 3. H1
                content = re.sub(
                    r'(<h1>)[^<]+(</h1>)',
                    lambda m: m.group(1) + f'Is {neighborhood} Expensive?' + m.group(2),
                    content, count=1)

                # 4. OG title
                content = re.sub(
                    r'(<meta property="og:title" content=")[^"]*(")',
                    lambda m: m.group(1) + new_title + m.group(2),
                    content, count=1)

                # 5. OG description
                content = re.sub(
                    r'(<meta property="og:description" content=")[^"]*(")',
                    lambda m: m.group(1) + new_desc + m.group(2),
                    content, count=1)

                # 6. Twitter title
                content = re.sub(
                    r'(<meta name="twitter:title" content=")[^"]*(")',
                    lambda m: m.group(1) + new_title + m.group(2),
                    content, count=1)

                # 7. Twitter description
                content = re.sub(
                    r'(<meta name="twitter:description" content=")[^"]*(")',
                    lambda m: m.group(1) + new_desc + m.group(2),
                    content, count=1)

                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                stats['updated'] += 1
                city_updated += 1

            except Exception as e:
                print(f'  ERROR {fpath}: {e}')
                stats['errors'] += 1

        if city_updated > 0:
            print(f'  {city_slug}: {city_updated} pages updated')


# =====================================================
# 2. CITY PAGES
# =====================================================
def fix_city_pages():
    print('\nProcessing city pages...')
    for fpath in sorted(glob.glob(os.path.join(BASE_DIR, 'city', '*.html'))):
        # Skip index.html if it exists at city level
        if os.path.basename(fpath) == 'index.html':
            continue

        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Idempotency
            if re.search(r'<title>Is .+ Expensive\?', content):
                stats['skipped'] += 1
                continue

            # Extract city name from current title
            # Pattern: "Cost of Living in {City} 2026 — Rent, Salary &amp; Neighborhood Guide"
            m = re.search(r'<title>Cost of Living in (.+?) 2026', content)
            if not m:
                stats['skipped'] += 1
                continue
            city = m.group(1).strip()

            # Extract rank and neighborhood count from existing description
            rank_m = re.search(r'Ranked #(\d+) of (\d+)', content)
            nhoods_m = re.search(r'(\d+) neighborhoods compared', content)
            rank = rank_m.group(1) if rank_m else '?'
            total_cities = rank_m.group(2) if rank_m else '101'
            n_hoods = nhoods_m.group(1) if nhoods_m else '?'

            new_title = compute_city_title(city)
            new_desc = (
                f"Is {city} expensive? Ranked #{rank} of {total_cities} "
                f"cities globally. Average 1BR rent, salary needed, "
                f"and tax rates. {n_hoods} neighborhoods compared."
            )

            # 1. Title
            content = re.sub(
                r'<title>[^<]+</title>',
                f'<title>{new_title}</title>',
                content, count=1)

            # 2. Meta description
            content = re.sub(
                r'(<meta name="description" content=")[^"]*(")',
                lambda m: m.group(1) + new_desc + m.group(2),
                content, count=1)

            # 3. H1 — city pages have "Cost of Living in {City}"
            content = re.sub(
                r'(<h1>)Cost of Living in [^<]+(</h1>)',
                lambda m: m.group(1) + f'Is {city} Expensive?' + m.group(2),
                content, count=1)

            # 4. OG title
            content = re.sub(
                r'(<meta property="og:title" content=")[^"]*(")',
                lambda m: m.group(1) + new_title + m.group(2),
                content, count=1)

            # 5. OG description
            content = re.sub(
                r'(<meta property="og:description" content=")[^"]*(")',
                lambda m: m.group(1) + new_desc + m.group(2),
                content, count=1)

            # 6. Twitter title
            content = re.sub(
                r'(<meta name="twitter:title" content=")[^"]*(")',
                lambda m: m.group(1) + new_title + m.group(2),
                content, count=1)

            # 7. Twitter description
            content = re.sub(
                r'(<meta name="twitter:description" content=")[^"]*(")',
                lambda m: m.group(1) + new_desc + m.group(2),
                content, count=1)

            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['updated'] += 1
            city_name = os.path.basename(fpath).replace('.html', '')
            print(f'  {city_name}: updated')

        except Exception as e:
            print(f'  ERROR {fpath}: {e}')
            stats['errors'] += 1


# =====================================================
# MAIN
# =====================================================
if __name__ == '__main__':
    print('=== Optimizing for "Is X Expensive?" queries ===\n')

    fix_neighborhood_pages()

    nhood_stats = stats.copy()
    print(f'\nNeighborhood totals: {nhood_stats["updated"]} updated, '
          f'{nhood_stats["skipped"]} skipped, '
          f'{nhood_stats["errors"]} errors')

    fix_city_pages()

    city_updated = stats['updated'] - nhood_stats['updated']
    city_skipped = stats['skipped'] - nhood_stats['skipped']
    city_errors = stats['errors'] - nhood_stats['errors']
    print(f'\nCity totals: {city_updated} updated, '
          f'{city_skipped} skipped, {city_errors} errors')

    print(f'\n=== GRAND TOTAL: {stats["updated"]} updated, '
          f'{stats["skipped"]} skipped, '
          f'{stats["errors"]} errors ===')
