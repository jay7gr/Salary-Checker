#!/usr/bin/env python3
"""
One-time script: Add Data Sources citations to blog articles.
Idempotency: Checks for 'blog-citations-v1' marker.
"""
import os, glob
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
MARKER = 'blog-citations-v1'
TODAY = date.today().strftime('%Y-%m-%d')

# Source URLs
NUMBEO_COL = 'https://www.numbeo.com/cost-of-living/'
EXPATISTAN = 'https://www.expatistan.com/cost-of-living'
NUMBEO_RENT = 'https://www.numbeo.com/property-investment/'
ECB = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
OECD_TAX = 'https://www.oecd.org/tax/tax-policy/taxing-wages-brochure.pdf'
BLS = 'https://www.bls.gov/oes/'
GLASSDOOR = 'https://www.glassdoor.com/Salaries/index.htm'
PAYSCALE = 'https://www.payscale.com/research/US/Country=United_States/Salary'
ROBERT_HALF = 'https://www.roberthalf.com/salary-guide'

ARTICLE_EXTRA_SOURCES = {
    'london-vs-new-york-true-cost-comparison': [
        ('UK Office for National Statistics', 'https://www.ons.gov.uk/economy/inflationandpriceindices'),
        ('HM Revenue & Customs', 'https://www.gov.uk/government/organisations/hm-revenue-customs'),
        ('U.S. Census Bureau', 'https://www.census.gov/topics/income-poverty.html'),
    ],
    'dubai-vs-singapore-expat-comparison': [
        ('Federal Competitiveness and Statistics Centre (UAE)', 'https://fcsc.gov.ae/en-us'),
        ('Singapore Department of Statistics', 'https://www.singstat.gov.sg/'),
        ('Inland Revenue Authority of Singapore', 'https://www.iras.gov.sg/'),
    ],
    'tech-salary-comparison-by-city-2026': [
        ('Glassdoor Salary Explorer', GLASSDOOR),
        ('PayScale', PAYSCALE),
        ('Robert Half Salary Guide', ROBERT_HALF),
    ],
    'average-salary-by-city-2026-global-comparison': [
        ('Glassdoor Salary Explorer', GLASSDOOR),
        ('PayScale', PAYSCALE),
    ],
    'purchasing-power-parity-explained': [
        ('World Bank International Comparison Program', 'https://www.worldbank.org/en/programs/icp'),
        ('OECD Purchasing Power Parities', 'https://data.oecd.org/conversion/purchasing-power-parities-ppp.htm'),
    ],
    'cost-of-living-adjustment-cola-guide-2026': [
        ('U.S. Social Security Administration COLA', 'https://www.ssa.gov/cola/'),
        ('U.S. Bureau of Labor Statistics CPI', 'https://www.bls.gov/cpi/'),
    ],
    'affordable-cities-in-europe-for-americans-2026': [
        ('Eurostat', 'https://ec.europa.eu/eurostat'),
    ],
    'cost-of-living-southeast-asia-digital-nomads-2026': [
        ('Singapore Department of Statistics', 'https://www.singstat.gov.sg/'),
    ],
    'what-is-a-good-salary-by-city-2026': [
        ('Glassdoor Salary Explorer', GLASSDOOR),
        ('PayScale', PAYSCALE),
    ],
    'geographic-pay-differentials-remote-workers-2026': [
        ('Glassdoor Salary Explorer', GLASSDOOR),
        ('PayScale', PAYSCALE),
        ('Robert Half Salary Guide', ROBERT_HALF),
    ],
    'how-to-retire-abroad-cost-of-living-guide': [
        ('OECD Better Life Index', 'https://www.oecdbetterlifeindex.org/'),
    ],
    'salary-negotiation-when-relocating-abroad': [
        ('Glassdoor Salary Explorer', GLASSDOOR),
        ('Robert Half Salary Guide', ROBERT_HALF),
    ],
    'currency-exchange-rates-impact-take-home-pay-abroad': [
        ('European Central Bank Exchange Rates', ECB),
    ],
    'most-expensive-cities-in-the-world-2026': [
        ('Mercer Cost of Living Survey', 'https://www.mercer.com/en-us/insights/total-rewards/talent-mobility-insights/cost-of-living/'),
    ],
    'top-10-cities-for-remote-workers-2026': [
        ('Glassdoor Salary Explorer', GLASSDOOR),
    ],
}


def build_blog_citations(article_slug):
    extras = ARTICLE_EXTRA_SOURCES.get(article_slug, [])

    extra_html = ''
    for name, url in extras:
        extra_html += f'            <li><a href="{url}" target="_blank" rel="noopener noreferrer" style="color:var(--accent,#2563eb);">{name}</a></li>\n'

    return f'''
    <section class="blog-citations-v1" style="max-width:800px;margin:32px auto 0;padding:24px 28px;background:var(--card-bg,#fff);border-radius:16px;border:1px solid var(--border-light,#f0f0f2);">
        <h2 style="font-size:1.1rem;font-weight:700;color:var(--text-primary,#1d1d1f);margin:0 0 12px;">Data Sources</h2>
        <p style="font-size:0.85rem;color:var(--text-body,#4a4a4c);line-height:1.7;margin:0 0 8px;">The data in this article is sourced from:</p>
        <ul style="font-size:0.85rem;color:var(--text-body,#4a4a4c);line-height:1.8;padding-left:20px;margin:0 0 12px;">
            <li><a href="{NUMBEO_COL}" target="_blank" rel="noopener noreferrer" style="color:var(--accent,#2563eb);">Numbeo</a> and <a href="{EXPATISTAN}" target="_blank" rel="noopener noreferrer" style="color:var(--accent,#2563eb);">Expatistan</a> — crowd-sourced cost of living surveys</li>
            <li><a href="{BLS}" target="_blank" rel="noopener noreferrer" style="color:var(--accent,#2563eb);">U.S. Bureau of Labor Statistics</a> — occupational employment and wage statistics</li>
            <li><a href="{OECD_TAX}" target="_blank" rel="noopener noreferrer" style="color:var(--accent,#2563eb);">OECD Taxing Wages</a> — effective tax rates by country</li>
            <li><a href="{ECB}" target="_blank" rel="noopener noreferrer" style="color:var(--accent,#2563eb);">European Central Bank</a> — daily reference exchange rates</li>
{extra_html}        </ul>
        <p style="font-size:0.78rem;color:var(--text-secondary,#86868b);margin:0;">All cost of living indices use New York City as the baseline (COLI = 100). Salary ranges are global baselines adjusted by local cost of living. Data as of {TODAY}. Figures are estimates for informational purposes only.</p>
    </section>

'''


def process_blog_articles():
    files = sorted(glob.glob(os.path.join(BASE, 'blog', 'articles', '*.html')))
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        relpath = os.path.relpath(filepath, BASE)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if MARKER in content:
                skipped += 1
                continue

            slug = os.path.basename(filepath).replace('.html', '')
            citations = build_blog_citations(slug)

            # Find footer insertion point (try multiple patterns)
            footer_patterns = [
                '<footer class="footer">',
                '<footer class="page-footer">',
                '<footer>',
            ]
            insert_pos = -1
            for pattern in footer_patterns:
                pos = content.rfind(pattern)
                if pos != -1:
                    insert_pos = pos
                    break

            if insert_pos == -1:
                print(f'  WARNING: No footer found in {relpath}')
                errors += 1
                continue

            content = content[:insert_pos] + citations + content[insert_pos:]

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  Updated: {relpath}')
            updated += 1

        except Exception as e:
            print(f'  ERROR: {relpath} — {e}')
            errors += 1

    return updated, skipped, errors


def main():
    print(f'add-blog-citations.py — adding citations to blog articles')
    print(f'Idempotency marker: {MARKER}')
    print()

    updated, skipped, errors = process_blog_articles()

    print(f'\n{"="*50}')
    print(f'TOTAL: {updated} updated, {skipped} skipped, {errors} errors')


if __name__ == '__main__':
    main()
