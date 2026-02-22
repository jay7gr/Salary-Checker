#!/usr/bin/env python3
"""
One-time script: Enrich neighborhood pages with unique prose content.

Adds ~250-400 words of data-driven text to each neighborhood page to address
Google's thin content concerns. The content includes:
- Cost positioning narrative (most expensive, affordable, etc.)
- Monthly budget breakdown (housing, food, transport percentages)
- Typical salary figures for 3 representative jobs
- Salary needed to live comfortably (50/30/20 rule)
- Tax/take-home context

Also updates title tags and meta descriptions to differentiate from city pages.

This script imports data from generate-pages.py and processes all existing
neighborhood HTML files in-place.
"""

import os
import re
import sys
from datetime import date

# Add project root to path so we can import from generate-pages
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Import data and utilities from generate-pages.py
# We need to import the module's data structures
import importlib.util
spec = importlib.util.spec_from_file_location("generate_pages", os.path.join(BASE_DIR, "generate-pages.py"))
gp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gp)

# Aliases for readability
coliData = gp.coliData
cityNeighborhoods = gp.cityNeighborhoods
cityCountry = gp.cityCountry
cityToCurrency = gp.cityToCurrency
cityRent1BR = gp.cityRent1BR
exchangeRates = gp.exchangeRates
salaryRanges = gp.salaryRanges
format_currency_amount = gp.format_currency_amount
get_expense_breakdown = gp.get_expense_breakdown
slugify = gp.slugify
calculate_all_deductions = gp.calculate_all_deductions

CURRENT_YEAR = date.today().year


def generate_prose_html(city, neighborhood, multiplier):
    """Generate the enriched prose section HTML for a neighborhood."""
    city_coli = coliData[city]
    nhood_coli = round(city_coli * multiplier, 1)
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    rate_to_local = exchangeRates[currency] / exchangeRates['USD']

    # Multiplier description
    pct_diff = (multiplier - 1) * 100
    sign = '+' if pct_diff >= 0 else ''

    # Rank within city
    all_nhoods = cityNeighborhoods.get(city, {})
    sorted_nhoods = sorted(all_nhoods.items(), key=lambda x: x[1], reverse=True)
    rank_in_city = 1
    total_in_city = len(sorted_nhoods)
    for i, (n, m) in enumerate(sorted_nhoods):
        if n == neighborhood:
            rank_in_city = i + 1
            break

    # Estimated rent
    city_rent = cityRent1BR.get(city, 0)
    nhood_rent = city_rent * multiplier
    nhood_rent_local = nhood_rent * rate_to_local
    fmt_rent = format_currency_amount(nhood_rent_local, currency)

    # Expense breakdown
    expenses = get_expense_breakdown(city)
    nhood_housing_pct = min(55, max(18, round(expenses['housing'] * multiplier)))
    nhood_food_pct = expenses['food']
    nhood_transport_pct = expenses['transport']

    # Salary needed to live comfortably (rent = 30% of gross)
    comfortable_annual = (nhood_rent_local * 12) / 0.30
    fmt_comfortable = format_currency_amount(comfortable_annual, currency)

    # Deductions
    nhood_ref_salary_local = 75000 * (nhood_coli / 100) * rate_to_local
    nhood_ded_result = calculate_all_deductions(nhood_ref_salary_local, country, city, is_expat=False, neighborhood=neighborhood)
    nhood_total_ded_rate = nhood_ded_result['total_rate']

    # Job salaries
    representative_jobs = ['Software Engineer', 'Teacher', 'Nurse']
    job_salary_lines = ''
    for job_title in representative_jobs:
        ranges = salaryRanges.get(job_title, {})
        if not ranges:
            continue
        local_mid = ranges['mid'] * (nhood_coli / 100) * rate_to_local
        fmt_job_salary = format_currency_amount(local_mid, currency)
        job_salary_lines += f'<li>A <strong>{job_title}</strong> earns approximately <strong>{fmt_job_salary}</strong> per year.</li>\n'

    # Cost tier description
    tier_pct = rank_in_city / total_in_city
    if tier_pct <= 0.1:
        tier_desc = f'the most expensive area in {city}'
        tier_context = f'Only the top {rank_in_city} of {total_in_city} neighborhoods cost more.'
    elif tier_pct <= 0.25:
        tier_desc = f'one of the pricier neighborhoods in {city}'
        tier_context = f'It ranks #{rank_in_city} out of {total_in_city} areas by cost.'
    elif tier_pct <= 0.5:
        tier_desc = f'a moderately-priced area within {city}'
        tier_context = f'It sits around the middle of the pack at #{rank_in_city} out of {total_in_city} neighborhoods.'
    elif tier_pct <= 0.75:
        tier_desc = f'a relatively affordable area in {city}'
        tier_context = f'At #{rank_in_city} of {total_in_city}, it is below the city average in cost.'
    else:
        tier_desc = f'one of the most affordable neighborhoods in {city}'
        tier_context = f'Ranked #{rank_in_city} of {total_in_city}, it offers some of the lowest costs in the city.'

    # Most affordable and most expensive for context
    cheapest_name = sorted_nhoods[-1][0] if sorted_nhoods else ''
    cheapest_mult = sorted_nhoods[-1][1] if sorted_nhoods else 1.0
    priciest_name = sorted_nhoods[0][0] if sorted_nhoods else ''
    priciest_mult = sorted_nhoods[0][1] if sorted_nhoods else 1.0
    cheapest_rent = city_rent * cheapest_mult * rate_to_local
    priciest_rent = city_rent * priciest_mult * rate_to_local
    fmt_cheapest_rent = format_currency_amount(cheapest_rent, currency)
    fmt_priciest_rent = format_currency_amount(priciest_rent, currency)

    # Take-home on comfortable salary
    takehome = format_currency_amount(comfortable_annual * (1 - nhood_total_ded_rate / 100), currency)

    prose = f'''<div class="card neighborhood-guide">
            <h2>Living in {neighborhood}, {city}</h2>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75; margin-bottom: 14px;">
                {neighborhood} is {tier_desc}, with a cost of living index of <strong>{nhood_coli}</strong> — that is <strong>{sign}{pct_diff:.0f}%</strong> compared to the {city} average. {tier_context} Estimated rent for a one-bedroom apartment here is around <strong>{fmt_rent}/month</strong>, compared to a range of {fmt_cheapest_rent} in {cheapest_name} to {fmt_priciest_rent} in {priciest_name}.
            </p>
            <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 10px;">Monthly Budget Breakdown</h3>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75; margin-bottom: 14px;">
                For a typical resident of {neighborhood}, housing takes up roughly <strong>{nhood_housing_pct}%</strong> of monthly expenses. Food and groceries account for about <strong>{nhood_food_pct}%</strong>, while transportation costs around <strong>{nhood_transport_pct}%</strong>. To live comfortably here — meaning rent stays at or below 30% of gross income — you would need an annual salary of approximately <strong>{fmt_comfortable}</strong> before tax.
            </p>
            <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 10px;">Typical Salaries in {neighborhood}</h3>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75; margin-bottom: 8px;">
                Salaries in {neighborhood} reflect the local cost of living. Based on the neighborhood COLI of {nhood_coli}:
            </p>
            <ul style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.85; margin-bottom: 14px; padding-left: 20px;">
                {job_salary_lines}
            </ul>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75;">
                After tax and deductions of <strong>{nhood_total_ded_rate}%</strong> in {country}, take-home pay for someone earning {fmt_comfortable} would be roughly <strong>{takehome}/year</strong>. Use the <a href="/" style="color: var(--accent, #2563eb);">salary converter</a> to calculate an exact figure for your situation, including expat-specific tax adjustments.
            </p>
        </div>'''

    new_meta_desc = f'{neighborhood}, {city} cost of living: COLI {nhood_coli} ({sign}{pct_diff:.0f}% vs avg). 1BR rent ~{fmt_rent}/mo. You need ~{fmt_comfortable}/yr to live comfortably. Compare salaries and expenses.'
    new_title = f'{neighborhood}, {city}: Salary Needed &amp; Cost of Living {CURRENT_YEAR} — salary:converter'
    new_og_title = f'{neighborhood}, {city}: Salary Needed &amp; Cost of Living {CURRENT_YEAR}'

    return prose, new_meta_desc, new_title, new_og_title


def process_file(fpath, city, neighborhood, multiplier):
    """Process a single neighborhood HTML file."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Idempotency check
    if 'neighborhood-guide' in content:
        return False

    prose_html, new_meta_desc, new_title, new_og_title = generate_prose_html(city, neighborhood, multiplier)

    # 1. Inject prose section after share bar, before Key Stats card
    # The share bar ends with </div> and then the Key Stats card starts
    # We look for the end of the share-bar div followed by the Key Stats card
    injection_pattern = re.compile(
        r'(</div>\s*\n\s*\n\s*<div class="card">\s*\n\s*<h2>Key Stats</h2>)',
        re.DOTALL
    )

    # More specific: find the share bar closing, then Key Stats
    # The share bar has class="share-bar" and ends with buttons then </div>
    # After it comes the Key Stats card
    share_bar_end = content.find('data-platform="email"')
    if share_bar_end == -1:
        # Try without share bar
        share_bar_end = content.find('<div class="card">\n            <h2>Key Stats</h2>')
        if share_bar_end == -1:
            print(f'  SKIP (no injection point): {fpath}')
            return False
        content = content[:share_bar_end] + prose_html + '\n\n        ' + content[share_bar_end:]
    else:
        # Find the closing </div> of the share bar after the email button
        close_div_pos = content.find('</div>', share_bar_end)
        if close_div_pos == -1:
            print(f'  SKIP (no share bar close): {fpath}')
            return False
        # Move past the </div>
        insert_pos = close_div_pos + len('</div>')
        # Find the next newline(s) and the Key Stats card
        content = content[:insert_pos] + '\n\n        ' + prose_html + content[insert_pos:]

    # 2. Update title tag
    content = re.sub(
        r'<title>Cost of Living in [^<]+</title>',
        f'<title>{new_title}</title>',
        content,
        count=1
    )

    # 3. Update meta description
    content = re.sub(
        r'<meta name="description" content="Cost of living in [^"]+">',
        f'<meta name="description" content="{new_meta_desc}">',
        content,
        count=1
    )

    # 4. Update og:title
    content = re.sub(
        r'<meta property="og:title" content="Cost of Living in [^"]+">',
        f'<meta property="og:title" content="{new_og_title}">',
        content,
        count=1
    )

    # 5. Update og:description
    content = re.sub(
        r'<meta property="og:description" content="Cost of living in [^"]+">',
        f'<meta property="og:description" content="{new_meta_desc}">',
        content,
        count=1
    )

    # 6. Update twitter:title if present
    content = re.sub(
        r'<meta name="twitter:title" content="Cost of Living in [^"]+">',
        f'<meta name="twitter:title" content="{new_og_title}">',
        content,
        count=1
    )

    # 7. Update twitter:description if present
    content = re.sub(
        r'<meta name="twitter:description" content="Cost of living in [^"]+">',
        f'<meta name="twitter:description" content="{new_meta_desc}">',
        content,
        count=1
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    city_dir = os.path.join(BASE_DIR, 'city')
    enriched_count = 0
    skipped_count = 0
    error_count = 0

    for city, neighborhoods in cityNeighborhoods.items():
        city_slug = slugify(city)
        city_path = os.path.join(city_dir, city_slug)
        if not os.path.isdir(city_path):
            continue

        for neighborhood, multiplier in neighborhoods.items():
            nhood_slug = slugify(neighborhood)
            fpath = os.path.join(city_path, f'{nhood_slug}.html')
            if not os.path.exists(fpath):
                continue

            try:
                if process_file(fpath, city, neighborhood, multiplier):
                    enriched_count += 1
                    if enriched_count <= 10 or enriched_count % 100 == 0:
                        print(f'  Enriched: {city_slug}/{nhood_slug}.html')
                else:
                    skipped_count += 1
            except Exception as e:
                error_count += 1
                print(f'  ERROR: {city_slug}/{nhood_slug}.html — {e}')

    print(f'\nDone: Enriched {enriched_count} neighborhood pages.')
    if skipped_count:
        print(f'  Skipped {skipped_count} (already enriched or no injection point).')
    if error_count:
        print(f'  Errors: {error_count}.')


if __name__ == '__main__':
    main()
