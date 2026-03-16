#!/usr/bin/env python3
"""
Improve title tags and meta descriptions on city and compare pages for better CTR.

Changes:
- City titles: "London Cost of Living: $2,500/mo Rent (2026)" →
  "Cost of Living in London 2026 — $2,500/mo Rent, Salary & Tax Data"
- City meta: Add "Compare neighborhoods, salary data & tax rates." CTA
- Compare titles: "London vs New York: 12% Cost Difference (2026)" →
  "London vs New York Cost of Living 2026: Which Is Cheaper?"
- Compare meta: Add "Find out which city..." CTA hook
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

city_count = 0
compare_count = 0


def fix_city_page(filepath):
    """Improve title and meta for a city page."""
    global city_count
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Extract current title parts
    # Pattern: "London Cost of Living: $2,500/mo Rent (2026)"
    title_match = re.search(r'<title>(.+?) Cost of Living: (\$[\d,]+)/mo Rent \((\d{4})\)</title>', content)
    if not title_match:
        return False

    city = title_match.group(1)
    rent = title_match.group(2)
    year = title_match.group(3)

    old_title = title_match.group(0)
    new_title = f'<title>Cost of Living in {city} {year} — {rent}/mo Rent, Salary & Tax Data</title>'

    # Check title length (Google truncates at ~60 chars)
    inner = new_title.replace('<title>', '').replace('</title>', '')
    if len(inner) > 65:
        new_title = f'<title>Cost of Living in {city} {year}: {rent}/mo Rent & More</title>'

    content = content.replace(old_title, new_title)

    # Also update og:title and twitter:title
    old_og = f'content="{city} Cost of Living: {rent}/mo Rent ({year})"'
    new_inner = new_title.replace('<title>', '').replace('</title>', '')
    new_og = f'content="{new_inner}"'
    content = content.replace(old_og, new_og)

    # Improve meta description — add CTA
    desc_match = re.search(r'<meta name="description" content="([^"]+)">', content)
    if desc_match:
        old_desc = desc_match.group(1)
        # Add CTA to existing description
        if 'Compare' not in old_desc and 'See' not in old_desc:
            new_desc = old_desc.rstrip('.')
            new_desc += '. Compare salaries, tax rates & neighborhoods.'
            # Keep under 155 chars
            if len(new_desc) > 155:
                new_desc = old_desc  # Don't change if too long
            content = content.replace(
                f'<meta name="description" content="{old_desc}">',
                f'<meta name="description" content="{new_desc}">'
            )
            # Update og:description too
            content = content.replace(
                f'og:description" content="{old_desc}"',
                f'og:description" content="{new_desc}"'
            )
            content = content.replace(
                f'twitter:description" content="{old_desc}"',
                f'twitter:description" content="{new_desc}"'
            )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        city_count += 1
        return True
    return False


def fix_compare_page(filepath):
    """Improve title and meta for a compare page."""
    global compare_count
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Pattern: "London vs New York: 12% Cost Difference (2026)"
    title_match = re.search(r'<title>(.+?) vs (.+?): (\d+)% Cost Difference \((\d{4})\)</title>', content)
    if not title_match:
        return False

    city1 = title_match.group(1)
    city2 = title_match.group(2)
    pct = title_match.group(3)
    year = title_match.group(4)

    old_title = title_match.group(0)
    new_title = f'<title>{city1} vs {city2} Cost of Living {year}: Which Is Cheaper?</title>'

    # Check length
    inner = new_title.replace('<title>', '').replace('</title>', '')
    if len(inner) > 65:
        new_title = f'<title>{city1} vs {city2}: Cost of Living Compared ({year})</title>'
        inner = new_title.replace('<title>', '').replace('</title>', '')
        if len(inner) > 65:
            new_title = f'<title>{city1} vs {city2} — Cost of Living {year}</title>'

    content = content.replace(old_title, new_title)

    # Update og:title and twitter:title
    old_og_title = f'{city1} vs {city2}: {pct}% Cost Difference ({year})'
    new_inner = new_title.replace('<title>', '').replace('</title>', '')
    content = content.replace(
        f'content="{old_og_title}"',
        f'content="{new_inner}"'
    )

    # Improve meta description
    desc_match = re.search(r'<meta name="description" content="([^"]+)">', content)
    if desc_match:
        old_desc = desc_match.group(1)
        if 'Find out' not in old_desc and 'Discover' not in old_desc:
            new_desc = old_desc.rstrip('.')
            new_desc += '. See the full comparison.'
            if len(new_desc) > 155:
                new_desc = old_desc
            content = content.replace(
                f'<meta name="description" content="{old_desc}">',
                f'<meta name="description" content="{new_desc}">'
            )
            content = content.replace(
                f'og:description" content="{old_desc}"',
                f'og:description" content="{new_desc}"'
            )
            content = content.replace(
                f'twitter:description" content="{old_desc}"',
                f'twitter:description" content="{new_desc}"'
            )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        compare_count += 1
        return True
    return False


# Fix all main city pages
for fp in sorted(glob.glob(os.path.join(ROOT, 'city', '*.html'))):
    if fp.endswith('/index.html'):
        continue
    fix_city_page(fp)

print(f'Updated {city_count} city page titles & descriptions')

# Fix all main compare pages (only top city pairs are indexed, but improve all for consistency)
for fp in sorted(glob.glob(os.path.join(ROOT, 'compare', '*.html'))):
    if fp.endswith('/index.html'):
        continue
    fix_compare_page(fp)

print(f'Updated {compare_count} compare page titles & descriptions')
print(f'Total: {city_count + compare_count} pages improved')
