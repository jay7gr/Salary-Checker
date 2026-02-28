#!/usr/bin/env python3
"""
One-time script: Upgrade existing compare page Data Sources sections
to include salary sources (BLS, Glassdoor, PayScale) and rent source (Numbeo Property Prices).

Idempotency: Checks for 'bls.gov' in content (not present in old template).
Target: compare/*.html (top-level city-vs-city pages, ~6,300 files)
"""
import os, glob, re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().strftime('%Y-%m-%d')

# The OLD content pattern to find (regex to match the Data Sources section)
OLD_PATTERN = re.compile(
    r'(<section class="content-card">\s*'
    r'<h2>Data Sources</h2>\s*'
    r'<p>Cost of living indices are derived from.*?</p>\s*'
    r'<p style="font-size: 0\.8rem;[^"]*">Last updated:.*?</p>\s*'
    r'</section>)',
    re.DOTALL
)

# The NEW replacement content
NEW_SECTION = f'''<section class="content-card">
            <h2>Data Sources &amp; Methodology</h2>
            <p>Cost of living indices (COLI) are benchmarked to New York City = 100 and derived from <a href="https://www.numbeo.com/cost-of-living/" target="_blank" rel="noopener noreferrer">Numbeo</a> and <a href="https://www.expatistan.com/cost-of-living" target="_blank" rel="noopener noreferrer">Expatistan</a> crowd-sourced price surveys, cross-referenced with national statistics agencies. Rent data from <a href="https://www.numbeo.com/property-investment/" target="_blank" rel="noopener noreferrer">Numbeo Property Prices</a>.</p>
            <p>Salary ranges are compiled from the <a href="https://www.bls.gov/oes/" target="_blank" rel="noopener noreferrer">U.S. Bureau of Labor Statistics (OES)</a>, <a href="https://www.glassdoor.com/Salaries/index.htm" target="_blank" rel="noopener noreferrer">Glassdoor</a>, and <a href="https://www.payscale.com/research/US/Country=United_States/Salary" target="_blank" rel="noopener noreferrer">PayScale</a>. Tax rates are approximate effective rates for mid-range earners based on <a href="https://www.oecd.org/tax/tax-policy/taxing-wages-brochure.pdf" target="_blank" rel="noopener noreferrer">OECD Taxing Wages</a> and national tax authorities. Exchange rates from the <a href="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html" target="_blank" rel="noopener noreferrer">European Central Bank</a>. Neighborhood multipliers are estimated from local rental indices and property data.</p>
            <p style="font-size: 0.8rem; color: #86868b; margin-bottom: 0;">Last updated: {TODAY}. Data is refreshed periodically. All figures are estimates for informational purposes only.</p>
        </section>'''


def main():
    print(f'upgrade-compare-citations.py — upgrading Data Sources on compare pages')
    print()

    # Top-level compare pages only (compare/*.html, not compare/*/*.html)
    files = sorted(glob.glob(os.path.join(ROOT, 'compare', '*.html')))

    updated = 0
    skipped = 0
    no_match = 0
    errors = 0

    for filepath in files:
        relpath = os.path.relpath(filepath, ROOT)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Idempotency: skip if already upgraded (has bls.gov)
            if 'bls.gov' in content:
                skipped += 1
                continue

            # Try to find and replace the old Data Sources section
            new_content, count = OLD_PATTERN.subn(NEW_SECTION, content, count=1)
            if count == 0:
                no_match += 1
                print(f'  No match: {relpath}')
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

        except Exception as e:
            print(f'  ERROR: {relpath} — {e}')
            errors += 1

    print(f'\n{"="*50}')
    print(f'Updated:  {updated}')
    print(f'Skipped:  {skipped} (already upgraded)')
    print(f'No match: {no_match}')
    print(f'Errors:   {errors}')
    print(f'Total:    {len(files)} files')


if __name__ == '__main__':
    main()
