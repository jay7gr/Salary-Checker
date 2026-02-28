#!/usr/bin/env python3
"""
One-time script to rewrite <title> and <meta description> tags across all page
types to improve Google Search Console CTR.

Strategy: Front-load specific numbers (rent, salary, percentages) in titles
and descriptions so SERP snippets compel clicks.

Updates all 6 meta tags per page:
  <title>, <meta description>, og:title, og:description, twitter:title, twitter:description

Safe to re-run (idempotent): skips files already matching new patterns.
"""

import os
import re
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
YEAR = '2026'


def decode_unicode_escapes(s):
    """Decode \\uXXXX sequences in a string to actual Unicode characters."""
    if '\\u' not in s:
        return s
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)


def section_stats():
    return {'updated': 0, 'skipped': 0, 'errors': 0, 'warnings': []}


def replace_meta_tags(content, title_text, desc_text, og_title_text=None, tw_title_text=None):
    """Replace all 6 meta tags. Uses lambda to avoid backreference issues."""
    if og_title_text is None:
        og_title_text = title_text
    if tw_title_text is None:
        tw_title_text = title_text

    # Title
    content = re.sub(
        r'<title>[^<]+</title>',
        lambda _: f'<title>{title_text}</title>',
        content, count=1)

    # Meta description
    content = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        lambda m: m.group(1) + desc_text + m.group(2),
        content, count=1)

    # OG title
    content = re.sub(
        r'(<meta property="og:title" content=")[^"]*(")',
        lambda m: m.group(1) + og_title_text + m.group(2),
        content, count=1)

    # OG description
    content = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        lambda m: m.group(1) + desc_text + m.group(2),
        content, count=1)

    # Twitter title (only if present)
    content = re.sub(
        r'(<meta name="twitter:title" content=")[^"]*(")',
        lambda m: m.group(1) + tw_title_text + m.group(2),
        content, count=1)

    # Twitter description (only if present)
    content = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        lambda m: m.group(1) + desc_text + m.group(2),
        content, count=1)

    return content


# =============================================================================
# 1. COMPARE PAGES  (compare/{city1}-vs-{city2}.html)
# =============================================================================
def fix_compare_pages():
    """
    Old: {City1} vs {City2}: Which Is Cheaper? Cost of Living Comparison 2026
    New: {City1} vs {City2}: {pct}% Cost Difference (2026)
    """
    stats = section_stats()
    files = glob.glob(os.path.join(BASE, 'compare', '*.html'))

    for filepath in files:
        if os.path.basename(filepath) == 'index.html':
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Idempotency check — only skip if description already has rent figures
            if re.search(r'content="Rent: \$[\d,]+/mo vs \$[\d,]+/mo', content):
                stats['skipped'] += 1
                continue

            # Extract city names from title (handles both old and new formats)
            m = re.search(r'<title>([^<]+?) vs ([^<:]+?):', content)
            if not m:
                stats['skipped'] += 1
                continue

            city1 = m.group(1).strip()
            city2 = m.group(2).strip()
            # Clean city2 in case it picked up extra from new title format
            city2 = city2.strip()

            # Extract cheaper city and percentage from description/body
            desc_m = re.search(r'([\w][\w\s\-\'\.]+?) is (\d+)% cheaper than ([\w][\w\s\-\'\.]+?)\.', content)
            if not desc_m:
                stats['skipped'] += 1
                continue

            cheaper_city = desc_m.group(1).strip()
            pct = desc_m.group(2)
            expensive_city = desc_m.group(3).strip()

            # Extract rent figures from page body
            rent_m = re.search(
                r'rent in .+ averages <strong>\$([\d,]+)/month</strong> compared to <strong>\$([\d,]+)/month</strong>',
                content, re.IGNORECASE)

            if rent_m:
                rent_a = rent_m.group(1)  # first city's rent
                rent_b = rent_m.group(2)  # second city's rent
            else:
                rent_a = None
                rent_b = None

            # Build new title
            title_text = f'{city1} vs {city2}: {pct}% Cost Difference ({YEAR})'

            if len(title_text) > 60:
                title_text = f'{city1} vs {city2}: {pct}% Gap ({YEAR})'

            if len(title_text) > 60:
                stats['warnings'].append(f'Title too long ({len(title_text)}): {title_text}')

            # Build new description
            if rent_a and rent_b:
                desc_text = f'Rent: ${rent_a}/mo vs ${rent_b}/mo. {cheaper_city} is {pct}% cheaper overall. Salary equivalents, taxes & 2,000+ neighborhoods compared.'
            else:
                desc_text = f'{cheaper_city} is {pct}% cheaper than {expensive_city}. Compare rent, salary equivalents & taxes. 2,000+ neighborhoods compared.'

            if len(desc_text) > 155:
                # Shorter fallback
                if rent_a and rent_b:
                    desc_text = f'Rent: ${rent_a}/mo vs ${rent_b}/mo. {cheaper_city} is {pct}% cheaper. Salary equivalents, taxes & neighborhoods compared.'
                else:
                    desc_text = f'{cheaper_city} is {pct}% cheaper than {expensive_city}. Rent, salary equivalents & taxes compared.'

            if len(desc_text) > 155:
                stats['warnings'].append(f'Desc too long ({len(desc_text)}): {os.path.basename(filepath)}')

            content = replace_meta_tags(content, title_text, desc_text)

            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            stats['updated'] += 1

        except Exception as e:
            print(f'  ERROR {filepath}: {e}')
            stats['errors'] += 1

    return stats


# =============================================================================
# 1B. NEIGHBORHOOD COMPARISON PAGES (compare/{city}/{n1}-vs-{n2}.html)
# =============================================================================
def fix_neighborhood_compare_pages():
    """
    Old: {N1} vs {N2}, {City}: Which Is Cheaper? Neighborhood Comparison 2026
    New: {N1} vs {N2}, {City}: {pct}% Cost Difference (2026)
    """
    stats = section_stats()

    for city_dir in glob.glob(os.path.join(BASE, 'compare', '*')):
        if not os.path.isdir(city_dir):
            continue

        for filepath in glob.glob(os.path.join(city_dir, '*.html')):
            if os.path.basename(filepath) == 'index.html':
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    content = fh.read()

                # Idempotency check
                if '% Cost Difference (' in content:
                    title_m = re.search(r'<title>[^<]*% Cost Difference \([^<]*</title>', content)
                    if title_m:
                        stats['skipped'] += 1
                        continue

                # Extract neighborhoods and city from title
                m = re.search(r'<title>(.+?) vs (.+?),\s*(.+?):', content)
                if not m:
                    stats['skipped'] += 1
                    continue

                n1 = m.group(1).strip()
                n2 = m.group(2).strip()
                city = m.group(3).strip()

                # Extract cheaper neighborhood and percentage
                desc_m = re.search(r'([\w][\w\s\(\)\-\.\']+?) is (\d+)% cheaper than', content)
                if not desc_m:
                    # Try "more affordable" pattern
                    desc_m = re.search(r'([\w][\w\s\(\)\-\.\']+?) is (\d+)% more affordable', content)

                if desc_m:
                    cheaper = desc_m.group(1).strip()
                    pct = desc_m.group(2)
                    expensive = n2 if cheaper == n1 else n1
                else:
                    stats['skipped'] += 1
                    continue

                title_text = f'{n1} vs {n2}, {city}: {pct}% Cost Difference ({YEAR})'
                if len(title_text) > 60:
                    title_text = f'{n1} vs {n2}: {pct}% Cost Difference ({YEAR})'

                desc_text = f'{cheaper} is {pct}% cheaper than {expensive} in {city}. Compare rent, groceries & salary equivalents neighborhood by neighborhood.'
                if len(desc_text) > 155:
                    desc_text = f'{cheaper} is {pct}% cheaper than {expensive} in {city}. Rent, groceries & salary equivalents compared.'

                content = replace_meta_tags(content, title_text, desc_text)

                with open(filepath, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                stats['updated'] += 1

            except Exception as e:
                print(f'  ERROR {filepath}: {e}')
                stats['errors'] += 1

    return stats


# =============================================================================
# 2. CITY PAGES  (city/{slug}.html)
# =============================================================================
def fix_city_pages():
    """
    Old: Is {City} Expensive? Cost of Living & Salary Guide (2026)
    New: {City} Cost of Living: ${rent}/mo Rent (2026)
    """
    stats = section_stats()

    files = glob.glob(os.path.join(BASE, 'city', '*.html'))

    for filepath in files:
        if os.path.basename(filepath) == 'index.html':
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Idempotency check
            if re.search(r'<title>[^<]*/mo Rent \(\d{4}\)</title>', content):
                stats['skipped'] += 1
                continue

            # Extract city name from current title (handles multiple formats)
            m = re.search(r'<title>Is ([^?]+?) Expensive\?', content)
            if not m:
                # Try older format
                m = re.search(r'<title>Cost of Living in ([^—–]+?)\s*[—–\d]', content)
            if not m:
                # Try new format without rent (from first broken run)
                m = re.search(r'<title>([^<]+?) Cost of Living \(\d{4}\)</title>', content)
            if not m:
                stats['skipped'] += 1
                continue

            city = m.group(1).strip()

            # Extract rank and total from description
            rank_m = re.search(r'Ranked #(\d+) of (\d+)', content)
            if not rank_m:
                rank_m = re.search(r'Ranked #(\d+)/(\d+)', content)
            rank = rank_m.group(1) if rank_m else None
            total = rank_m.group(2) if rank_m else None

            # Extract n_hoods from description
            nhood_m = re.search(r'(\d+) neighborhoods', content)
            n_hoods = nhood_m.group(1) if nhood_m else None

            # Extract rent from page body (USD rent figure)
            rent_m = re.search(r'average one-bedroom rent.*?\$([\d,]+)/month', content, re.IGNORECASE)
            if not rent_m:
                rent_m = re.search(r'one-bedroom rent of <strong>\$([\d,]+)/month</strong>', content)
            if not rent_m:
                rent_m = re.search(r'rent.*?averages.*?\$([\d,]+)/month', content, re.IGNORECASE)

            rent_usd = rent_m.group(1) if rent_m else None

            # Try to get comfortable salary from corresponding salary-needed page
            city_slug = os.path.basename(filepath).replace('.html', '')
            sn_path = os.path.join(BASE, 'salary-needed', f'{city_slug}.html')
            comf_salary = None
            if os.path.exists(sn_path):
                with open(sn_path, 'r', encoding='utf-8') as sfh:
                    sn_content = sfh.read()
                comf_m = re.search(r'or ([^/]+)/yr to be comfortable', sn_content)
                if comf_m:
                    comf_salary = comf_m.group(1).strip()

            # Build title
            if rent_usd:
                title_text = f'{city} Cost of Living: ${rent_usd}/mo Rent ({YEAR})'
            else:
                title_text = f'{city} Cost of Living ({YEAR})'

            if len(title_text) > 60:
                title_text = f'{city}: ${rent_usd}/mo Rent ({YEAR})' if rent_usd else f'{city} Cost of Living ({YEAR})'

            if len(title_text) > 60:
                stats['warnings'].append(f'Title too long ({len(title_text)}): {title_text}')

            # Build description
            parts = []
            if rent_usd:
                parts.append(f'1BR rent: ${rent_usd}/mo.')
            if rank and total:
                parts.append(f'Ranked #{rank}/{total} globally.')
            if comf_salary:
                parts.append(f'You need ~{comf_salary}/yr to live comfortably.')
            if n_hoods:
                parts.append(f'{n_hoods} neighborhoods ranked.')

            desc_text = ' '.join(parts)

            if len(desc_text) > 155:
                # Shorter: drop "globally" and shorten
                parts_short = []
                if rent_usd:
                    parts_short.append(f'1BR: ${rent_usd}/mo.')
                if rank and total:
                    parts_short.append(f'#{rank}/{total} cities.')
                if comf_salary:
                    parts_short.append(f'Need ~{comf_salary}/yr to live well.')
                if n_hoods:
                    parts_short.append(f'{n_hoods} neighborhoods.')
                desc_text = ' '.join(parts_short)

            if len(desc_text) > 155:
                stats['warnings'].append(f'Desc too long ({len(desc_text)}): {os.path.basename(filepath)}')

            content = replace_meta_tags(content, title_text, desc_text)

            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            stats['updated'] += 1

        except Exception as e:
            print(f'  ERROR {filepath}: {e}')
            stats['errors'] += 1

    return stats


# =============================================================================
# 3. NEIGHBORHOOD PAGES  (city/{city}/{neighborhood}.html)
# =============================================================================
def fix_neighborhood_pages():
    """
    Old: Is {Neighborhood} Expensive? {City} Cost of Living (2026)
    New: {Neighborhood}, {City}: {rent}/mo Rent (2026)
    """
    stats = section_stats()

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
                if re.search(r'<title>[^<]*/mo Rent \(\d{4}\)</title>', content):
                    stats['skipped'] += 1
                    continue

                # Extract neighborhood and city from current title
                m = re.search(r'<title>Is ([^?]+?) Expensive\?\s*(.+?)\s*Cost of Living', content)
                if not m:
                    stats['skipped'] += 1
                    continue

                neighborhood = m.group(1).strip()
                city = m.group(2).strip()

                # Extract rent from description (local currency)
                rent_m = re.search(r'1BR rent: ~([^/]+)/mo', content)
                fmt_rent = rent_m.group(1).strip() if rent_m else None

                # Extract rank and total
                rank_m = re.search(r'Ranked #(\d+) of (\d+)', content)
                rank = rank_m.group(1) if rank_m else None
                total_hoods = rank_m.group(2) if rank_m else None

                # Extract pct difference and direction
                pct_m = re.search(r"It's (\d+)% (more expensive|cheaper) than the", content)
                if pct_m:
                    pct = pct_m.group(1)
                    direction = pct_m.group(2)
                    above_below = 'above' if direction == 'more expensive' else 'below'
                else:
                    pct = None
                    above_below = None

                # Build title
                if fmt_rent:
                    title_text = f'{neighborhood}, {city}: {fmt_rent}/mo Rent ({YEAR})'
                else:
                    title_text = f'{neighborhood}, {city} Cost of Living ({YEAR})'

                if len(title_text) > 60:
                    # Drop city if too long
                    if fmt_rent:
                        title_text = f'{neighborhood}: {fmt_rent}/mo Rent ({YEAR})'
                    else:
                        title_text = f'{neighborhood} Cost of Living ({YEAR})'

                if len(title_text) > 60:
                    stats['warnings'].append(f'Title too long ({len(title_text)}): {title_text}')

                # Build description
                parts = []
                if pct and above_below:
                    parts.append(f'{pct}% {above_below} {city} avg.')
                if fmt_rent:
                    parts.append(f'1BR: ~{fmt_rent}/mo.')
                if rank and total_hoods:
                    parts.append(f'#{rank} of {total_hoods} neighborhoods.')
                parts.append('Salary needed & full cost breakdown inside.')
                desc_text = ' '.join(parts)

                if len(desc_text) > 155:
                    # Shorter
                    parts_short = []
                    if pct and above_below:
                        parts_short.append(f'{pct}% {above_below} {city} avg.')
                    if fmt_rent:
                        parts_short.append(f'1BR: ~{fmt_rent}/mo.')
                    if rank and total_hoods:
                        parts_short.append(f'#{rank}/{total_hoods}.')
                    parts_short.append('Full breakdown inside.')
                    desc_text = ' '.join(parts_short)

                if len(desc_text) > 155:
                    stats['warnings'].append(f'Desc too long ({len(desc_text)}): {os.path.basename(filepath)}')

                content = replace_meta_tags(content, title_text, desc_text)

                with open(filepath, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                stats['updated'] += 1

            except Exception as e:
                print(f'  ERROR {filepath}: {e}')
                stats['errors'] += 1

    return stats


# =============================================================================
# 4. SALARY-NEEDED PAGES  (salary-needed/**/*.html)
# =============================================================================
def fix_salary_needed_pages():
    """
    Old: What Salary Do You Need in {Name}? 2026 Cost Breakdown — salary:converter
    New: Salary Needed in {Name}: {comf_salary}/yr (2026)
    """
    stats = section_stats()

    files = glob.glob(os.path.join(BASE, 'salary-needed', '*.html'))
    for d in glob.glob(os.path.join(BASE, 'salary-needed', '*')):
        if os.path.isdir(d):
            files.extend(glob.glob(os.path.join(d, '*.html')))

    for filepath in files:
        if os.path.basename(filepath) == 'index.html':
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                content = fh.read()

            # Idempotency check — only skip if title and description look correct
            head_section = '\n'.join(content.split('\n')[:30])
            title_ok = bool(re.search(r'<title>(?:Salary Needed in |.+?:).+?/yr (?:Needed )?\(\d{4}\)</title>', head_section))
            desc_ok = bool(re.search(r'content="(?:Minimum|Min): [^"\\]+Full single', head_section))
            if title_ok and desc_ok:
                stats['skipped'] += 1
                continue

            # Extract display name from title (handles old and new formats)
            m = re.search(r'<title>What Salary Do You Need in ([^?]+)\?', content)
            if not m:
                m = re.search(r'<title>Salary Needed in ([^:]+):', content)
            if not m:
                m = re.search(r'<title>([^:]+):[^<]*/yr Needed', content)
            if not m:
                stats['skipped'] += 1
                continue

            display_name = m.group(1).strip()

            # Clean up any garbled meta tags from previous runs (broken quotes)
            # Use whole-line replacement: match from tag start to closing >
            content = re.sub(
                r'    <meta name="description" content="[^>]*>',
                '    <meta name="description" content="PLACEHOLDER">',
                content, count=1)
            content = re.sub(
                r'    <meta property="og:description" content="[^>]*>',
                '    <meta property="og:description" content="PLACEHOLDER">',
                content, count=1)
            content = re.sub(
                r'    <meta name="twitter:description" content="[^>]*>',
                '    <meta name="twitter:description" content="PLACEHOLDER">',
                content, count=1)

            # Extract min and comfortable salary from full page content (FAQ schema is reliable)
            comf_m = re.search(r'you need a gross annual salary of approximately ([^.]+)\.', content, re.IGNORECASE)
            if not comf_m:
                comf_m = re.search(r'Comfortable: ([^/]+)/yr', content)
            if not comf_m:
                comf_m = re.search(r'or ([^/]+)/yr to be comfortable', content)

            min_m = re.search(r'minimum to get by is ([^.]+)\.', content, re.IGNORECASE)
            if not min_m:
                min_m = re.search(r'Minimum: ([^/]+)/yr', content)
            if not min_m:
                min_m = re.search(r'costs ([^/]+)/yr minimum', content)

            min_salary = decode_unicode_escapes(min_m.group(1).strip()) if min_m else None
            comf_salary = decode_unicode_escapes(comf_m.group(1).strip()) if comf_m else None

            if not comf_salary:
                stats['skipped'] += 1
                continue

            # Try to extract rent from FAQ schema or page body
            rent_m = re.search(r'Monthly rent for a 1-bedroom apartment in .+? is approximately ([^.]+)\.', content)
            if not rent_m:
                rent_m = re.search(r'rent.*?approximately ([A-Z$€£¥₹₩R][^\s.<,"]+)', content)
            monthly_rent = decode_unicode_escapes(rent_m.group(1).strip()) if rent_m else None

            tax_m = re.search(r'effective tax rate[^:]*?is[^:]*?(\d+\.?\d*)%', content, re.IGNORECASE)
            if not tax_m:
                tax_m = re.search(r'total deductions of approximately <strong>(\d+\.?\d*)%</strong>', content)
            tax_rate = tax_m.group(1) if tax_m else None

            # Build title
            title_text = f'Salary Needed in {display_name}: {comf_salary}/yr ({YEAR})'

            if len(title_text) > 60:
                # Try shorter
                title_text = f'{display_name}: {comf_salary}/yr Needed ({YEAR})'

            if len(title_text) > 60:
                stats['warnings'].append(f'Title too long ({len(title_text)}): {title_text}')

            # Build description
            parts = []
            if min_salary:
                parts.append(f'Minimum: {min_salary}/yr.')
            parts.append(f'Comfortable: {comf_salary}/yr.')
            if monthly_rent:
                parts.append(f'Rent: {monthly_rent}/mo.')
            if tax_rate:
                parts.append(f'Tax rate: {tax_rate}%.')
            parts.append('Full single & family breakdown.')
            desc_text = ' '.join(parts)

            if len(desc_text) > 155:
                # Shorter
                parts_short = [f'Min: {min_salary}/yr.' if min_salary else '']
                parts_short.append(f'Comfortable: {comf_salary}/yr.')
                parts_short.append('Full single & family breakdown.')
                desc_text = ' '.join(p for p in parts_short if p)

            if len(desc_text) > 155:
                stats['warnings'].append(f'Desc too long ({len(desc_text)}): {os.path.basename(filepath)}')

            content = replace_meta_tags(content, title_text, desc_text)

            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            stats['updated'] += 1

        except Exception as e:
            print(f'  ERROR {filepath}: {e}')
            stats['errors'] += 1

    return stats


# =============================================================================
# 5. HOMEPAGE
# =============================================================================
def fix_homepage():
    """Update index.html title and description."""
    stats = section_stats()
    filepath = os.path.join(BASE, 'index.html')

    try:
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()

        if '2,000+ Neighborhoods Compared' in content:
            stats['skipped'] += 1
            return stats

        title_text = f'Salary Converter {YEAR} — 2,000+ Neighborhoods Compared'
        desc_text = f'Compare salaries across 2,000+ neighborhoods in 101 cities. Single &amp; family mode with rent, taxes &amp; childcare. Free. Updated {YEAR}.'

        content = replace_meta_tags(content, title_text, desc_text)

        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        stats['updated'] += 1

    except Exception as e:
        print(f'  ERROR {filepath}: {e}')
        stats['errors'] += 1

    return stats


# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    print('=== CTR Improvement: Rewriting titles & descriptions ===\n')

    total = section_stats()

    sections = [
        ('1. Compare pages', fix_compare_pages),
        ('1b. Neighborhood comparison pages', fix_neighborhood_compare_pages),
        ('2. City pages', fix_city_pages),
        ('3. Neighborhood pages', fix_neighborhood_pages),
        ('4. Salary-needed pages', fix_salary_needed_pages),
        ('5. Homepage', fix_homepage),
    ]

    for label, func in sections:
        print(f'{label}...')
        s = func()
        print(f'   Updated: {s["updated"]}, Skipped: {s["skipped"]}, Errors: {s["errors"]}')
        if s['warnings']:
            for w in s['warnings'][:5]:
                print(f'   ⚠ {w}')
            if len(s['warnings']) > 5:
                print(f'   ... and {len(s["warnings"]) - 5} more warnings')
        total['updated'] += s['updated']
        total['skipped'] += s['skipped']
        total['errors'] += s['errors']
        total['warnings'].extend(s['warnings'])
        print()

    print(f'=== TOTAL: {total["updated"]} updated, {total["skipped"]} skipped, {total["errors"]} errors, {len(total["warnings"])} warnings ===')
