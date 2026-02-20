#!/usr/bin/env python3
"""
Fixes incorrect percentage calculations in existing comparison HTML files.
The bug: used (A/B - 1)*100 instead of abs(A-B)/max(A,B)*100.
This affects COLI % and rent % in body text, meta descriptions, and FAQ schema.
"""

import os, re, glob, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPARE_DIR = os.path.join(BASE_DIR, 'compare')


def fix_city_comparison(filepath):
    """Fix percentages in a city-vs-city comparison page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract city names from h1
    h1_match = re.search(r'<h1>(.*?)<span class="vs-badge">VS</span>(.*?)</h1>', content)
    if not h1_match:
        return False, "no h1"
    city_a = h1_match.group(1).strip()
    city_b = h1_match.group(2).strip()

    # Extract COLI values
    coli_matches = re.findall(r'<div class="value">([\d.]+)</div>\s*<div class="label">COLI Index</div>', content)
    if len(coli_matches) < 2:
        return False, "no COLI"
    coli_a = float(coli_matches[0])
    coli_b = float(coli_matches[1])

    # Calculate correct COLI percentage
    if max(coli_a, coli_b) == 0:
        return False, "zero COLI"
    correct_coli_pct = round(abs(coli_a - coli_b) / max(coli_a, coli_b) * 100)

    # Determine cheaper city
    if coli_a < coli_b:
        cheaper = city_a
        pricier = city_b
    elif coli_b < coli_a:
        cheaper = city_b
        pricier = city_a
    else:
        cheaper = city_a  # same cost
        pricier = city_b

    # Extract rent values from the metric rows
    # Pattern: <div class="metric-value ...">$X,XXX</div> near "1BR Rent"
    rent_match = re.findall(r'<div class="metric-label">1BR Rent.*?</div>\s*<div class="metric-value[^"]*">\$([\d,]+)</div>\s*<div class="metric-value[^"]*">\$([\d,]+)</div>', content, re.DOTALL)
    if rent_match:
        rent_a = int(rent_match[0][0].replace(',', ''))
        rent_b = int(rent_match[0][1].replace(',', ''))
        correct_rent_pct = round(abs(rent_a - rent_b) / max(rent_a, rent_b) * 100) if max(rent_a, rent_b) > 0 else 0
    else:
        # Try alternate pattern from body text
        rent_body = re.findall(r'rent in .*? averages <strong>\$([\d,]+)/month</strong> compared to <strong>\$([\d,]+)/month</strong>', content)
        if rent_body:
            rent_a = int(rent_body[0][0].replace(',', ''))
            rent_b = int(rent_body[0][1].replace(',', ''))
            correct_rent_pct = round(abs(rent_a - rent_b) / max(rent_a, rent_b) * 100) if max(rent_a, rent_b) > 0 else 0
        else:
            rent_a = rent_b = 0
            correct_rent_pct = 0

    # Now replace the wrong percentages
    changes = 0

    # 1. Fix meta description: "{cheaper} is XX% cheaper"
    def fix_meta_pct(match):
        nonlocal changes
        changes += 1
        return match.group(0).replace(match.group(1), str(correct_coli_pct))

    content = re.sub(
        rf'{re.escape(cheaper)} is (\d+)% cheaper',
        lambda m: m.group(0).replace(m.group(1), str(correct_coli_pct)),
        content
    )

    # 2. Fix "approximately XX% cheaper" in Key Takeaways (COLI)
    # This appears as: "approximately <strong>XX% cheaper</strong>"
    old_pattern = re.search(r'approximately <strong>(\d+)% cheaper</strong> than .* based on our cost of living index', content)
    if old_pattern:
        old_pct = old_pattern.group(1)
        if old_pct != str(correct_coli_pct):
            content = content.replace(
                f'approximately <strong>{old_pct}% cheaper</strong> than {pricier} based on our cost of living index',
                f'approximately <strong>{correct_coli_pct}% cheaper</strong> than {pricier} based on our cost of living index'
            )
            changes += 1

    # 3. Fix rent percentage: "approximately <strong>XX% cheaper</strong> for rent alone"
    rent_pct_match = re.search(r'approximately <strong>(\d+)% cheaper</strong> for rent alone', content)
    if rent_pct_match and correct_rent_pct > 0:
        old_rent_pct = rent_pct_match.group(1)
        if old_rent_pct != str(correct_rent_pct):
            content = content.replace(
                f'approximately <strong>{old_rent_pct}% cheaper</strong> for rent alone',
                f'approximately <strong>{correct_rent_pct}% cheaper</strong> for rent alone'
            )
            changes += 1

    # 4. Fix FAQ schema — the original entries (not our answer box entries)
    # Fix "making {cheaper} approximately XX% cheaper" in FAQ
    content = re.sub(
        rf'making {re.escape(cheaper)} approximately (\d+)% cheaper',
        f'making {cheaper} approximately {correct_coli_pct}% cheaper',
        content
    )

    # Fix "lower rent by approximately XX%" in FAQ
    if correct_rent_pct > 0:
        content = re.sub(
            r'lower rent by approximately (\d+)%',
            f'lower rent by approximately {correct_rent_pct}%',
            content
        )

    # 5. Fix salary diff text: "That is <strong>XX%</strong> more/less"
    content = re.sub(
        r'That is <strong>(\d+)%</strong> (more|less)',
        lambda m: f'That is <strong>{correct_coli_pct}%</strong> {m.group(2)}',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True, f"COLI: {correct_coli_pct}%, rent: {correct_rent_pct}%"


def fix_neighborhood_comparison(filepath):
    """Fix percentages in neighborhood-vs-neighborhood comparison pages."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract multipliers from the comparison section
    # Pattern: <div class="val">1.45x</div>
    mult_matches = re.findall(r'<div class="val">([\d.]+)x</div>', content)
    if len(mult_matches) < 2:
        return False, "no multipliers"

    m1 = float(mult_matches[0])
    m2 = float(mult_matches[1])

    correct_pct = round(abs(m1 - m2) / max(m1, m2) * 100)

    # Extract neighborhood names from title
    title_match = re.search(r'<title>(.*?) vs (.*?),', content)
    if not title_match:
        return False, "no title"
    n1 = title_match.group(1).strip()
    n2 = title_match.group(2).strip()

    more_expensive = n1 if m1 > m2 else n2

    # Fix "XX% more expensive" in body text
    content = re.sub(
        rf'{re.escape(more_expensive)} is <strong>(\d+)% more expensive</strong>',
        f'{more_expensive} is <strong>{correct_pct}% more expensive</strong>',
        content
    )

    # Fix meta description "XX% more affordable"
    more_affordable = n2 if m1 > m2 else n1
    content = re.sub(
        rf'{re.escape(more_affordable)} is (\d+)% more affordable',
        f'{more_affordable} is {correct_pct}% more affordable',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True, f"pct: {correct_pct}%"


# ============ MAIN ============

# Fix city comparison pages
city_files = glob.glob(os.path.join(COMPARE_DIR, '*-vs-*.html'))
print(f"Fixing {len(city_files)} city comparison pages...")

success = 0
errors = 0
for f in sorted(city_files):
    try:
        ok, msg = fix_city_comparison(f)
        if ok:
            success += 1
        else:
            errors += 1
            if errors <= 5:
                print(f"  Skip {os.path.basename(f)}: {msg}")
    except Exception as e:
        errors += 1
        if errors <= 5:
            print(f"  Error {os.path.basename(f)}: {e}")

print(f"  City comparisons: {success} fixed, {errors} errors/skips")

# Fix neighborhood comparison pages
nhood_success = 0
nhood_errors = 0
nhood_dirs = [d for d in glob.glob(os.path.join(COMPARE_DIR, '*/')) if os.path.isdir(d)]
for nhood_dir in sorted(nhood_dirs):
    nhood_files = glob.glob(os.path.join(nhood_dir, '*-vs-*.html'))
    for f in nhood_files:
        try:
            ok, msg = fix_neighborhood_comparison(f)
            if ok:
                nhood_success += 1
            else:
                nhood_errors += 1
        except Exception as e:
            nhood_errors += 1
            if nhood_errors <= 5:
                print(f"  Error {os.path.basename(f)}: {e}")

print(f"  Neighborhood comparisons: {nhood_success} fixed, {nhood_errors} errors/skips")
print(f"\nTotal: {success + nhood_success} files fixed")
