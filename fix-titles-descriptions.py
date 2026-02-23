#!/usr/bin/env python3
"""
One-time script to update <title> and <meta description> tags on all existing
generated pages to improve Google Search Console CTR.

Updates:
- City pages: question hook + rank-first description
- Compare pages: "Which Is Cheaper?" title + answer-first description
- Neighborhood pages: "How Much Do You Need to Earn?" title
- Salary-needed pages: "Cost Breakdown" title + number-first description

Also syncs og:title, og:description, twitter:title, twitter:description.

Safe to re-run (idempotent): skips files already matching new patterns.
"""

import os
import re
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

stats = {'updated': 0, 'skipped': 0, 'errors': 0}


def update_tag(content, tag_pattern, new_value):
    """Replace a meta tag value using regex. Returns (new_content, changed)."""
    new_content = re.sub(tag_pattern, new_value, content)
    return new_content, new_content != content


# =============================================================================
# 1. CITY PAGES  (city/{slug}.html and city/{slug}/index.html)
# =============================================================================
def fix_city_pages():
    """Update city page titles from 'Cost of Living in {city}, {country}...'
    to 'Cost of Living in {city} 2026 — Rent, Salary & Neighborhood Guide'"""

    patterns = [
        os.path.join(BASE, 'city', '*.html'),
    ]
    # Also handle city/{slug}/index.html (directory-style)
    for d in glob.glob(os.path.join(BASE, 'city', '*')):
        if os.path.isdir(d) and os.path.basename(d) != 'index.html':
            idx = os.path.join(d, 'index.html')
            if os.path.exists(idx):
                patterns.append(idx)

    files = []
    for p in patterns:
        files.extend(glob.glob(p))

    # Filter: only city-level pages (not neighborhood sub-pages, not the city index)
    city_files = []
    for f in files:
        rel = os.path.relpath(f, os.path.join(BASE, 'city'))
        # city/{slug}.html — no slashes
        # city/{slug}/index.html — one level deep
        parts = rel.replace('\\', '/').split('/')
        if len(parts) == 1 and parts[0] != 'index.html':
            city_files.append(f)
        elif len(parts) == 2 and parts[1] == 'index.html':
            city_files.append(f)

    for filepath in city_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Check if already updated (idempotency)
            if 'Rent, Salary &amp; Neighborhood Guide' in content or 'Rent, Salary & Neighborhood Guide' in content:
                stats['skipped'] += 1
                continue

            # Extract city name from existing title
            m = re.search(r'<title>Cost of Living in ([^,]+),\s*([^—–]+?)\s*[—–]', content)
            if not m:
                stats['skipped'] += 1
                continue

            city = m.group(1).strip()

            # Extract rank and total from existing description
            rank_m = re.search(r'rank #(\d+)/(\d+)', content)
            neigh_m = re.search(r'Explore (\d+) neighborhoods', content)

            if not rank_m:
                stats['skipped'] += 1
                continue

            rank = rank_m.group(1)
            total = rank_m.group(2)
            n_hoods = neigh_m.group(1) if neigh_m else '?'

            # New title
            old_title_pattern = r'<title>Cost of Living in [^<]+</title>'
            new_title = f'<title>Cost of Living in {city} 2026 — Rent, Salary &amp; Neighborhood Guide</title>'
            content = re.sub(old_title_pattern, new_title, content)

            # New meta description
            old_desc_pattern = r'(<meta name="description" content=")[^"]*(")'
            new_desc = f'\\1How expensive is {city}? Ranked #{rank} of {total} cities. See rent by neighborhood, salary needed to live comfortably, and tax rates. {n_hoods} neighborhoods compared.\\2'
            content = re.sub(old_desc_pattern, new_desc, content)

            # OG title
            old_og_title = r'(<meta property="og:title" content=")[^"]*(")'
            new_og_title = f'\\1Cost of Living in {city} 2026 — Rent, Salary &amp; Neighborhood Guide\\2'
            content = re.sub(old_og_title, new_og_title, content)

            # OG description
            old_og_desc = r'(<meta property="og:description" content=")[^"]*(")'
            new_og_desc = f'\\1How expensive is {city}? Ranked #{rank} of {total}. See rent, salary needed, and {n_hoods} neighborhoods compared.\\2'
            content = re.sub(old_og_desc, new_og_desc, content)

            # Twitter title
            old_tw_title = r'(<meta name="twitter:title" content=")[^"]*(")'
            new_tw_title = f'\\1Cost of Living in {city} 2026 — Rent, Salary &amp; Neighborhood Guide\\2'
            content = re.sub(old_tw_title, new_tw_title, content)

            # Twitter description
            old_tw_desc = r'(<meta name="twitter:description" content=")[^"]*(")'
            new_tw_desc = f'\\1How expensive is {city}? Ranked #{rank} of {total}. See rent, salary needed, and neighborhoods compared.\\2'
            content = re.sub(old_tw_desc, new_tw_desc, content)

            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            stats['updated'] += 1

        except Exception as e:
            print(f'  ERROR {filepath}: {e}')
            stats['errors'] += 1


# =============================================================================
# 2. COMPARE PAGES  (compare/{city1}-vs-{city2}.html)
# =============================================================================
def fix_compare_pages():
    """Update compare page titles to 'Which Is Cheaper?' format."""

    files = glob.glob(os.path.join(BASE, 'compare', '*.html'))

    for filepath in files:
        if os.path.basename(filepath) == 'index.html':
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Idempotency check
            if 'Which Is Cheaper?' in content:
                stats['skipped'] += 1
                continue

            # Extract city names from title
            m = re.search(r'<title>([^<]+?) vs ([^<:]+?):\s*Cost of Living', content)
            if not m:
                stats['skipped'] += 1
                continue

            city1 = m.group(1).strip()
            city2 = m.group(2).strip()

            # Extract cheaper city and percentage from description
            desc_m = re.search(r'(\w[\w\s]+?) is (\d+)% cheaper', content)
            if not desc_m:
                stats['skipped'] += 1
                continue

            cheaper_city = desc_m.group(1).strip()
            pct = desc_m.group(2)

            # Determine expensive city
            expensive_city = city2 if cheaper_city == city1 else city1

            # New title
            old_title = r'<title>[^<]+</title>'
            new_title = f'<title>{city1} vs {city2}: Which Is Cheaper? Cost of Living Comparison 2026</title>'
            content = re.sub(old_title, new_title, content, count=1)

            # New description
            old_desc = r'(<meta name="description" content=")[^"]*(")'
            new_desc = f'\\1{cheaper_city} is {pct}% cheaper than {expensive_city}. Compare rent, groceries, taxes, and what salary you\'d need in each city. Neighborhood-level data included.\\2'
            content = re.sub(old_desc, new_desc, content, count=1)

            # OG title
            old_og_title = r'(<meta property="og:title" content=")[^"]*(")'
            new_og_title = f'\\1{city1} vs {city2}: Which Is Cheaper? Cost of Living 2026\\2'
            content = re.sub(old_og_title, new_og_title, content, count=1)

            # OG description
            old_og_desc = r'(<meta property="og:description" content=")[^"]*(")'
            new_og_desc = f'\\1{cheaper_city} is {pct}% cheaper than {expensive_city}. Compare rent, groceries, taxes, and salary equivalents.\\2'
            content = re.sub(old_og_desc, new_og_desc, content, count=1)

            # Twitter title
            old_tw_title = r'(<meta name="twitter:title" content=")[^"]*(")'
            new_tw_title = f'\\1{city1} vs {city2}: Which Is Cheaper? 2026\\2'
            content = re.sub(old_tw_title, new_tw_title, content, count=1)

            # Twitter description
            old_tw_desc = r'(<meta name="twitter:description" content=")[^"]*(")'
            new_tw_desc = f'\\1{cheaper_city} is {pct}% cheaper than {expensive_city}. Full comparison with neighborhood data.\\2'
            content = re.sub(old_tw_desc, new_tw_desc, content, count=1)

            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            stats['updated'] += 1

        except Exception as e:
            print(f'  ERROR {filepath}: {e}')
            stats['errors'] += 1


# =============================================================================
# 2B. NEIGHBORHOOD COMPARISON PAGES  (compare/{city}/{n1}-vs-{n2}.html)
# =============================================================================
def fix_neighborhood_compare_pages():
    """Update neighborhood comparison titles to 'Which Is Cheaper?' format."""

    for city_dir in glob.glob(os.path.join(BASE, 'compare', '*')):
        if not os.path.isdir(city_dir):
            continue

        city_slug = os.path.basename(city_dir)

        for filepath in glob.glob(os.path.join(city_dir, '*.html')):
            if os.path.basename(filepath) == 'index.html':
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    content = fh.read()

                # Idempotency check
                if 'Which Is Cheaper?' in content:
                    stats['skipped'] += 1
                    continue

                # Extract neighborhoods and city from existing title
                # Format: "{N1} vs {N2}, {City} — Cost of Living Comparison"
                m = re.search(r'<title>(.+?) vs (.+?),\s*(.+?)\s*[—–]\s*Cost of Living Comparison</title>', content)
                if not m:
                    stats['skipped'] += 1
                    continue

                n1 = m.group(1).strip()
                n2 = m.group(2).strip()
                city = m.group(3).strip()

                # Extract cheaper neighborhood and percentage from description
                # Format: "{N2} is X% more affordable"
                # Note: neighborhood names can have hyphens (Saint-Denis), parentheses, dots, etc.
                desc_m = re.search(r'([\w][\w\s\(\)\-\.\']+?) is (\d+)% more affordable', content)
                if desc_m:
                    cheaper = desc_m.group(1).strip()
                    pct = desc_m.group(2)
                    expensive = n1 if cheaper == n2 else n2
                else:
                    # Fallback: no percentage found
                    cheaper = None
                    pct = None
                    expensive = None

                # New title
                new_title_text = f'{n1} vs {n2}, {city}: Which Is Cheaper? Neighborhood Comparison 2026'
                old_title = r'<title>[^<]+</title>'
                content = re.sub(old_title, lambda _m: f'<title>{new_title_text}</title>', content, count=1)

                # New description
                if cheaper and pct:
                    new_desc_text = f'{cheaper} is {pct}% cheaper than {expensive} in {city}. Compare rent, groceries, and salary equivalents neighborhood by neighborhood.'
                else:
                    new_desc_text = f'{n1} vs {n2} in {city}: which neighborhood is cheaper? Compare rent, cost of living, and salary equivalents side by side.'

                old_desc = r'(<meta name="description" content=")[^"]*(")'
                content = re.sub(old_desc, lambda _m: _m.group(1) + new_desc_text + _m.group(2), content, count=1)

                # OG title
                old_og_title = r'(<meta property="og:title" content=")[^"]*(")'
                content = re.sub(old_og_title, lambda _m: _m.group(1) + new_title_text + _m.group(2), content, count=1)

                # OG description
                old_og_desc = r'(<meta property="og:description" content=")[^"]*(")'
                content = re.sub(old_og_desc, lambda _m: _m.group(1) + new_desc_text + _m.group(2), content, count=1)

                with open(filepath, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                stats['updated'] += 1

            except Exception as e:
                print(f'  ERROR {filepath}: {e}')
                stats['errors'] += 1


# =============================================================================
# 3. NEIGHBORHOOD PAGES  (city/{city}/{neighborhood}.html)
# =============================================================================
def fix_neighborhood_pages():
    """Update neighborhood titles to 'How Much Do You Need to Earn?' format."""

    for city_dir in glob.glob(os.path.join(BASE, 'city', '*')):
        if not os.path.isdir(city_dir):
            continue

        for filepath in glob.glob(os.path.join(city_dir, '*.html')):
            if os.path.basename(filepath) == 'index.html':
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    content = fh.read()

                # Idempotency check
                if 'How Much Do You Need to Earn?' in content:
                    stats['skipped'] += 1
                    continue

                # Extract neighborhood and city from existing title
                m = re.search(r'<title>([^,]+),\s*([^:]+):\s*Salary Needed', content)
                if not m:
                    stats['skipped'] += 1
                    continue

                neighborhood = m.group(1).strip()
                city = m.group(2).strip()

                # Extract salary and rent data from existing description for new desc
                salary_m = re.search(r'You need ~([^/]+)/yr', content)
                rent_m = re.search(r'1BR rent[:\s~]*([^/]+)/mo', content)
                pct_m = re.search(r'\(([+-]?\d+)% vs', content)

                salary = salary_m.group(1).strip() if salary_m else None
                rent = rent_m.group(1).strip() if rent_m else None
                pct_info = pct_m.group(1) if pct_m else None

                # New title (use lambda to avoid backreference issues with names containing digits)
                new_title_text = f'{neighborhood}, {city}: How Much Do You Need to Earn? (2026)'
                old_title = r'<title>[^<]+</title>'
                content = re.sub(old_title, lambda _m: f'<title>{new_title_text}</title>', content, count=1)

                # New description
                if salary and rent and pct_info:
                    sign = '+' if not pct_info.startswith('-') and not pct_info.startswith('+') else ''
                    new_desc_text = f'Living in {neighborhood}, {city}? You need ~{salary}/yr to be comfortable. 1BR rent: ~{rent}/mo ({sign}{pct_info}% vs city avg). Full expense breakdown inside.'
                    old_desc = r'(<meta name="description" content=")[^"]*(")'
                    content = re.sub(old_desc, lambda _m: _m.group(1) + new_desc_text + _m.group(2), content, count=1)

                    old_og_desc = r'(<meta property="og:description" content=")[^"]*(")'
                    content = re.sub(old_og_desc, lambda _m: _m.group(1) + new_desc_text + _m.group(2), content, count=1)

                # OG title
                old_og_title = r'(<meta property="og:title" content=")[^"]*(")'
                content = re.sub(old_og_title, lambda _m: _m.group(1) + new_title_text + _m.group(2), content, count=1)

                with open(filepath, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                stats['updated'] += 1

            except Exception as e:
                print(f'  ERROR {filepath}: {e}')
                stats['errors'] += 1


# =============================================================================
# 4. SALARY-NEEDED PAGES  (salary-needed/{city}.html)
# =============================================================================
def fix_salary_needed_pages():
    """Update salary-needed titles to 'Cost Breakdown' format."""

    files = glob.glob(os.path.join(BASE, 'salary-needed', '*.html'))
    # Also check subdirectories (salary-needed/{city}/{neighborhood}.html)
    for d in glob.glob(os.path.join(BASE, 'salary-needed', '*')):
        if os.path.isdir(d):
            files.extend(glob.glob(os.path.join(d, '*.html')))

    for filepath in files:
        if os.path.basename(filepath) == 'index.html':
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Idempotency check — look specifically in the title tag
            if re.search(r'<title>[^<]*Cost Breakdown[^<]*</title>', content):
                stats['skipped'] += 1
                continue

            # Extract display name from existing title
            m = re.search(r'<title>What Salary Do You Need in ([^?]+)\?', content)
            if not m:
                stats['skipped'] += 1
                continue

            display_name = m.group(1).strip()

            # Extract salary data from existing description
            min_m = re.search(r'From ([^\s]+) to get by', content)
            comf_m = re.search(r'to ([^\s]+) to live comfortably', content)

            min_salary = min_m.group(1).strip() if min_m else None
            comf_salary = comf_m.group(1).strip() if comf_m else None

            # New title
            old_title = r'<title>[^<]+</title>'
            new_title = f'<title>What Salary Do You Need in {display_name}? 2026 Cost Breakdown</title>'
            content = re.sub(old_title, new_title, content, count=1)

            # New description
            if min_salary and comf_salary:
                new_desc_text = f'Living in {display_name} costs {min_salary}/yr minimum, or {comf_salary}/yr to be comfortable. See after-tax take-home, rent, and full expense breakdown for 2026.'
                old_desc = r'(<meta name="description" content=")[^"]*(")'
                content = re.sub(old_desc, f'\\1{new_desc_text}\\2', content, count=1)

                old_og_desc = r'(<meta property="og:description" content=")[^"]*(")'
                content = re.sub(old_og_desc, f'\\1{new_desc_text}\\2', content, count=1)

                old_tw_desc = r'(<meta name="twitter:description" content=")[^"]*(")'
                content = re.sub(old_tw_desc, f'\\1{new_desc_text}\\2', content, count=1)

            # OG title
            old_og_title = r'(<meta property="og:title" content=")[^"]*(")'
            content = re.sub(old_og_title, f'\\1What Salary Do You Need in {display_name}? 2026 Cost Breakdown\\2', content, count=1)

            # Twitter title
            old_tw_title = r'(<meta name="twitter:title" content=")[^"]*(")'
            content = re.sub(old_tw_title, f'\\1What Salary Do You Need in {display_name}? 2026 Cost Breakdown\\2', content, count=1)

            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            stats['updated'] += 1

        except Exception as e:
            print(f'  ERROR {filepath}: {e}')
            stats['errors'] += 1


# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    print('=== Fixing titles and descriptions for CTR improvement ===\n')

    print('1. City pages...')
    fix_city_pages()
    print(f'   Updated: {stats["updated"]}, Skipped: {stats["skipped"]}, Errors: {stats["errors"]}')

    prev = stats.copy()
    print('\n2. Compare pages...')
    fix_compare_pages()
    print(f'   Updated: {stats["updated"] - prev["updated"]}, Skipped: {stats["skipped"] - prev["skipped"]}, Errors: {stats["errors"] - prev["errors"]}')

    prev = stats.copy()
    print('\n2b. Neighborhood comparison pages...')
    fix_neighborhood_compare_pages()
    print(f'   Updated: {stats["updated"] - prev["updated"]}, Skipped: {stats["skipped"] - prev["skipped"]}, Errors: {stats["errors"] - prev["errors"]}')

    prev = stats.copy()
    print('\n3. Neighborhood pages...')
    fix_neighborhood_pages()
    print(f'   Updated: {stats["updated"] - prev["updated"]}, Skipped: {stats["skipped"] - prev["skipped"]}, Errors: {stats["errors"] - prev["errors"]}')

    prev = stats.copy()
    print('\n4. Salary-needed pages...')
    fix_salary_needed_pages()
    print(f'   Updated: {stats["updated"] - prev["updated"]}, Skipped: {stats["skipped"] - prev["skipped"]}, Errors: {stats["errors"] - prev["errors"]}')

    print(f'\n=== TOTAL: {stats["updated"]} updated, {stats["skipped"]} skipped, {stats["errors"]} errors ===')
