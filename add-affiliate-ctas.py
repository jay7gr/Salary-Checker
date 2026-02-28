#!/usr/bin/env python3
"""
One-time script: Add Wise affiliate CTA boxes to existing pages.

Targets:
  - Compare pages (compare/*.html) — ~5,959 files
  - City pages (city/*.html, top-level only) — ~101 files
  - Salary-needed pages (salary-needed/**/*.html) — ~2,214 files

Idempotency: Skips files that already contain 'wise-cta'.
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# Affiliate link — replace with real Wise invite link when approved
WISE_LINK = 'https://wise.com/invite/u/placeholder'

# City → currency code lookup (for city page messaging)
CITY_CURRENCY = {
    'New York': 'USD', 'San Francisco': 'USD', 'Los Angeles': 'USD', 'Chicago': 'USD',
    'Miami': 'USD', 'Austin': 'USD', 'Seattle': 'USD', 'Denver': 'USD', 'Boston': 'USD',
    'Washington DC': 'USD', 'Houston': 'USD', 'Charlotte': 'USD', 'Las Vegas': 'USD',
    'Tampa': 'USD', 'Raleigh': 'USD', 'Dallas': 'USD', 'Atlanta': 'USD',
    'Philadelphia': 'USD', 'Phoenix': 'USD', 'San Diego': 'USD', 'Nashville': 'USD',
    'Minneapolis': 'USD', 'Portland': 'USD',
    'Toronto': 'CAD', 'Vancouver': 'CAD', 'Montreal': 'CAD',
    'Mexico City': 'MXN', 'Cancun': 'MXN', 'Playa del Carmen': 'MXN',
    'Panama City': 'USD',
    'London': 'GBP', 'Edinburgh': 'GBP',
    'Paris': 'EUR', 'Nice': 'EUR', 'Amsterdam': 'EUR', 'Berlin': 'EUR', 'Munich': 'EUR',
    'Dublin': 'EUR', 'Brussels': 'EUR', 'Luxembourg City': 'EUR',
    'Madrid': 'EUR', 'Barcelona': 'EUR', 'Valencia': 'EUR', 'Malaga': 'EUR',
    'Lisbon': 'EUR', 'Porto': 'EUR', 'Rome': 'EUR', 'Milan': 'EUR', 'Athens': 'EUR',
    'Split': 'EUR', 'Vienna': 'EUR', 'Helsinki': 'EUR', 'Tallinn': 'EUR',
    'Riga': 'EUR', 'Bucharest': 'RON',
    'Zurich': 'CHF', 'Geneva': 'CHF',
    'Stockholm': 'SEK', 'Copenhagen': 'DKK', 'Oslo': 'NOK',
    'Prague': 'CZK', 'Budapest': 'HUF', 'Warsaw': 'PLN', 'Krakow': 'PLN',
    'Istanbul': 'TRY',
    'Tokyo': 'JPY', 'Osaka': 'JPY', 'Fukuoka': 'JPY',
    'Seoul': 'KRW', 'Hong Kong': 'HKD', 'Taipei': 'TWD',
    'Shanghai': 'CNY', 'Beijing': 'CNY', 'Shenzhen': 'CNY', 'Guangzhou': 'CNY',
    'Singapore': 'SGD', 'Bangkok': 'THB', 'Chiang Mai': 'THB', 'Phuket': 'THB',
    'Kuala Lumpur': 'MYR', 'Ho Chi Minh City': 'VND', 'Hanoi': 'VND',
    'Manila': 'PHP', 'Jakarta': 'IDR', 'Bali': 'IDR', 'Phnom Penh': 'USD',
    'Mumbai': 'INR', 'Bangalore': 'INR', 'Delhi': 'INR', 'Chennai': 'INR',
    'Sydney': 'AUD', 'Melbourne': 'AUD', 'Perth': 'AUD', 'Auckland': 'NZD',
    'Dubai': 'AED', 'Abu Dhabi': 'AED', 'Doha': 'QAR', 'Riyadh': 'SAR',
    'Tel Aviv': 'ILS',
    'Cape Town': 'ZAR', 'Nairobi': 'KES', 'Lagos': 'NGN', 'Cairo': 'EGP',
    'Marrakech': 'MAD', 'Casablanca': 'MAD',
    'Sao Paulo': 'BRL', 'Buenos Aires': 'ARS', 'Bogota': 'COP', 'Medellin': 'COP',
    'Lima': 'PEN', 'Santiago': 'CLP', 'Montevideo': 'UYU', 'San Jose': 'CRC',
}


def build_wise_cta(headline, body_text, button_text):
    """Build the Wise affiliate CTA HTML block."""
    return f'''
        <section class="content-card wise-cta" style="border: 1px solid #9fe870; border-left: 4px solid #9fe870; background: var(--card-bg);">
            <div style="display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap;">
                <div style="flex:1; min-width:200px;">
                    <p style="font-size:0.65rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin:0 0 6px;">Sponsored</p>
                    <h3 style="font-size:1rem; font-weight:600; margin:0 0 6px; color:var(--text-primary);">{headline}</h3>
                    <p style="font-size:0.85rem; color:var(--text-body); line-height:1.5; margin:0 0 12px;">{body_text}</p>
                    <a href="{WISE_LINK}" rel="noopener noreferrer sponsored" target="_blank"
                       style="display:inline-block; padding:10px 24px; background:#9fe870; color:#1a1a1a; border-radius:100px; font-weight:600; font-size:0.85rem; text-decoration:none; transition:transform 0.2s;">
                        {button_text} &rarr;
                    </a>
                </div>
            </div>
        </section>
'''


def extract_city_from_title(content, pattern):
    """Extract city name(s) from <title> tag using a regex pattern."""
    m = re.search(pattern, content)
    return m.groups() if m else None


def process_compare_pages():
    """Add Wise CTA to compare pages (city vs city)."""
    pattern = os.path.join(ROOT, 'compare', '*.html')
    files = glob.glob(pattern)
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        if filename == 'index.html':
            skipped += 1
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency check
        if 'wise-cta' in content:
            skipped += 1
            continue

        # Extract city names from title: "{City1} vs {City2}: ..."
        m = re.search(r'<title>([^<]+?) vs ([^<:]+?):', content)
        if not m:
            # Try alternate title format
            m = re.search(r'<title>([^<]+?) vs ([^<]+?) ', content)
        if not m:
            errors += 1
            print(f"  WARN: Could not extract cities from {filename}")
            continue

        city1 = m.group(1).strip()
        city2 = m.group(2).strip()

        headline = f"Moving between {city1} and {city2}?"
        body = "Save up to 6x on international transfers. Send money at the real exchange rate with no hidden fees."
        button = "Compare Transfer Fees"
        cta_html = build_wise_cta(headline, body, button)

        # Insert before existing CTA section
        anchor = '        <section class="cta-section">'
        if anchor in content:
            content = content.replace(anchor, cta_html + '\n' + anchor, 1)
        else:
            # Fallback: insert before FAQ section
            faq_anchor = '        <section class="content-card">\n            <h2>Frequently Asked Questions</h2>'
            if faq_anchor in content:
                content = content.replace(faq_anchor, cta_html + '\n' + faq_anchor, 1)
            else:
                errors += 1
                print(f"  WARN: No anchor found in {filename}")
                continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1

    return updated, skipped, errors


def process_city_pages():
    """Add Wise CTA to city pages (top-level only, not neighborhood pages)."""
    pattern = os.path.join(ROOT, 'city', '*.html')
    files = glob.glob(pattern)
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        if filename == 'index.html':
            skipped += 1
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency check
        if 'wise-cta' in content:
            skipped += 1
            continue

        # Extract city name from title: "{City} Cost of Living: ..." or "{City} Cost of Living (2026)"
        m = re.search(r'<title>([^<]+?) Cost of Living', content)
        if not m:
            errors += 1
            print(f"  WARN: Could not extract city from {filename}")
            continue

        city = m.group(1).strip()

        # Look up currency code
        currency = CITY_CURRENCY.get(city, 'USD')

        headline = f"Moving to {city}?"
        body = f"Open a multi-currency account to manage {currency} and your home currency. No hidden fees, real exchange rate."
        button = "Open a Wise Account"
        cta_html = build_wise_cta(headline, body, button)

        # Insert before "Salary Comparison" section
        anchor = '        <section class="content-card">\n            <h2>Salary Comparison:'
        if anchor in content:
            content = content.replace(anchor, cta_html + '\n' + anchor, 1)
        else:
            # Fallback: insert before footer
            footer_anchor = '        <footer class="page-footer">'
            if footer_anchor in content:
                content = content.replace(footer_anchor, cta_html + '\n' + footer_anchor, 1)
            else:
                errors += 1
                print(f"  WARN: No anchor found in {filename}")
                continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1

    return updated, skipped, errors


def process_salary_needed_pages():
    """Add Wise CTA to salary-needed pages (city + neighborhood)."""
    updated = 0
    skipped = 0
    errors = 0

    # City-level pages
    city_pattern = os.path.join(ROOT, 'salary-needed', '*.html')
    # Neighborhood-level pages
    nhood_pattern = os.path.join(ROOT, 'salary-needed', '*', '*.html')
    files = glob.glob(city_pattern) + glob.glob(nhood_pattern)

    for filepath in files:
        filename = os.path.relpath(filepath, ROOT)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency check
        if 'wise-cta' in content:
            skipped += 1
            continue

        headline = "Earning abroad?"
        body = "Send money internationally at the real exchange rate. Save up to 6x vs traditional banks."
        button = "Try Wise for Free"
        cta_html = build_wise_cta(headline, body, button)

        # Insert before "How We Calculate This" section
        anchor = '        <section class="content-card">\n            <h2>How We Calculate This</h2>'
        if anchor in content:
            content = content.replace(anchor, cta_html + '\n' + anchor, 1)
        else:
            # Fallback: insert before FAQ section
            faq_anchor = '        <section class="content-card">\n            <h2>Frequently Asked Questions</h2>'
            if faq_anchor in content:
                content = content.replace(faq_anchor, cta_html + '\n' + faq_anchor, 1)
            else:
                # Last fallback: insert before footer
                footer_anchor = '        <footer class="page-footer">'
                if footer_anchor in content:
                    content = content.replace(footer_anchor, cta_html + '\n' + footer_anchor, 1)
                else:
                    errors += 1
                    print(f"  WARN: No anchor found in {filename}")
                    continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1

    return updated, skipped, errors


if __name__ == '__main__':
    print("Adding Wise affiliate CTAs to existing pages...")
    print()

    print("1. Compare pages...")
    u, s, e = process_compare_pages()
    print(f"   Updated: {u}, Skipped: {s}, Errors: {e}")

    print("2. City pages...")
    u2, s2, e2 = process_city_pages()
    print(f"   Updated: {u2}, Skipped: {s2}, Errors: {e2}")

    print("3. Salary-needed pages...")
    u3, s3, e3 = process_salary_needed_pages()
    print(f"   Updated: {u3}, Skipped: {s3}, Errors: {e3}")

    total_updated = u + u2 + u3
    total_skipped = s + s2 + s3
    total_errors = e + e2 + e3
    print()
    print(f"Total: {total_updated} updated, {total_skipped} skipped, {total_errors} errors")
