#!/usr/bin/env python3
"""
One-time idempotent script: add "Data Sources & Methodology" citations to
ranking, salary, salary-needed, and neighborhood-compare pages.

Idempotency marker: data-citations-v1
"""

import os, glob, re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Load cityCountry from generate-pages.py via exec()
# ---------------------------------------------------------------------------
_source = open(os.path.join(ROOT, 'generate-pages.py'), encoding='utf-8').read()
_data_portion = _source.split("if __name__ == '__main__':")[0]
_namespace = {}
exec(_data_portion, _namespace)
cityCountry = _namespace['cityCountry']  # dict mapping city name -> country

# ---------------------------------------------------------------------------
# Country-specific government sources
# ---------------------------------------------------------------------------
COUNTRY_SOURCES = {
    'United States': [
        ('U.S. Bureau of Labor Statistics', 'https://www.bls.gov/'),
        ('U.S. Census Bureau', 'https://www.census.gov/topics/income-poverty.html'),
    ],
    'United Kingdom': [
        ('UK Office for National Statistics', 'https://www.ons.gov.uk/economy/inflationandpriceindices'),
        ('HM Revenue & Customs', 'https://www.gov.uk/government/organisations/hm-revenue-customs'),
    ],
    'Germany': [
        ('Destatis (Federal Statistical Office)', 'https://www.destatis.de/EN/Home/_node.html'),
        ('Bundesagentur f\u00fcr Arbeit', 'https://www.arbeitsagentur.de/'),
    ],
    'Japan': [
        ('Statistics Bureau of Japan', 'https://www.stat.go.jp/english/'),
        ('Ministry of Health, Labour and Welfare', 'https://www.mhlw.go.jp/english/'),
    ],
    'France': [
        ('INSEE', 'https://www.insee.fr/en/accueil'),
    ],
    'Australia': [
        ('Australian Bureau of Statistics', 'https://www.abs.gov.au/'),
        ('Australian Taxation Office', 'https://www.ato.gov.au/'),
    ],
    'Canada': [
        ('Statistics Canada', 'https://www.statcan.gc.ca/'),
        ('Canada Revenue Agency', 'https://www.canada.ca/en/revenue-agency.html'),
    ],
    'Singapore': [
        ('Singapore Department of Statistics', 'https://www.singstat.gov.sg/'),
    ],
    'UAE': [
        ('Federal Competitiveness and Statistics Centre', 'https://fcsc.gov.ae/en-us'),
    ],
    'South Korea': [
        ('Korean Statistical Information Service', 'https://kosis.kr/eng/'),
    ],
    'Spain': [
        ('INE (Instituto Nacional de Estad\u00edstica)', 'https://www.ine.es/en/index.htm'),
    ],
    'Italy': [
        ('ISTAT', 'https://www.istat.it/en/'),
    ],
    'Switzerland': [
        ('Swiss Federal Statistical Office', 'https://www.bfs.admin.ch/bfs/en/home.html'),
    ],
    'Netherlands': [
        ('Statistics Netherlands (CBS)', 'https://www.cbs.nl/en-gb'),
    ],
}

# ---------------------------------------------------------------------------
# Slug helpers
# ---------------------------------------------------------------------------
def slugify(name):
    return name.lower().replace(' ', '-').replace(',', '').replace("'", '').replace('(', '').replace(')', '').replace('\u00e3', 'a').replace('\u00e9', 'e').replace('\u00fc', 'u').replace('\u00f6', 'o').replace('\u00e4', 'a').replace('\u00f8', 'o').replace('\u00e5', 'a')

SLUG_TO_COUNTRY = {}
for city, country in cityCountry.items():
    SLUG_TO_COUNTRY[slugify(city)] = country

# ---------------------------------------------------------------------------
# Source URLs
# ---------------------------------------------------------------------------
NUMBEO_COL = 'https://www.numbeo.com/cost-of-living/'
EXPATISTAN = 'https://www.expatistan.com/cost-of-living'
NUMBEO_RENT = 'https://www.numbeo.com/property-investment/'
ECB = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
OECD_TAX = 'https://www.oecd.org/tax/tax-policy/taxing-wages-brochure.pdf'
BLS = 'https://www.bls.gov/oes/'
GLASSDOOR = 'https://www.glassdoor.com/Salaries/index.htm'
PAYSCALE = 'https://www.payscale.com/research/US/Country=United_States/Salary'
ROBERT_HALF = 'https://www.roberthalf.com/salary-guide'
MARKER = 'data-citations-v1'
TODAY = date.today().strftime('%Y-%m-%d')

# ---------------------------------------------------------------------------
# Template A -- Full section (ranking + salary pages)
# ---------------------------------------------------------------------------
TEMPLATE_A = f'''
        <section class="content-card data-citations-v1">
            <h2>Data Sources &amp; Methodology</h2>
            <p>Cost of living indices (COLI) are benchmarked to New York City = 100 and derived from <a href="{NUMBEO_COL}" target="_blank" rel="noopener noreferrer">Numbeo</a> and <a href="{EXPATISTAN}" target="_blank" rel="noopener noreferrer">Expatistan</a> crowd-sourced price surveys, cross-referenced with national statistics agencies.</p>
            <p>Salary ranges are compiled from the <a href="{BLS}" target="_blank" rel="noopener noreferrer">U.S. Bureau of Labor Statistics (OES)</a>, <a href="{GLASSDOOR}" target="_blank" rel="noopener noreferrer">Glassdoor</a>, <a href="{PAYSCALE}" target="_blank" rel="noopener noreferrer">PayScale</a>, and the <a href="{ROBERT_HALF}" target="_blank" rel="noopener noreferrer">Robert Half Salary Guide</a>. Tax rates use 2026 published brackets from <a href="{OECD_TAX}" target="_blank" rel="noopener noreferrer">OECD Taxing Wages</a> and national tax authorities. Exchange rates from the <a href="{ECB}" target="_blank" rel="noopener noreferrer">European Central Bank</a>. Rent data from <a href="{NUMBEO_RENT}" target="_blank" rel="noopener noreferrer">Numbeo Property Prices</a>.</p>
            <p style="font-size: 0.8rem; color: var(--text-secondary, #86868b); margin-bottom: 0;">Last updated: {TODAY}. Data is refreshed periodically. All figures are estimates for informational purposes only and should not be used as the sole basis for financial decisions.</p>
        </section>

'''

# ---------------------------------------------------------------------------
# Template B builder -- Compact div (salary-needed + neighborhood compare)
# ---------------------------------------------------------------------------
def build_template_b(country):
    sources = COUNTRY_SOURCES.get(country, [])
    if sources:
        country_links = ' &middot; '.join(
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">{name}</a>'
            for name, url in sources
        )
        country_part = f' &middot; {country_links}'
    else:
        country_part = ''

    return f'''
        <div class="data-citations-v1" style="margin: 24px 0; padding: 16px; background: var(--stat-card-bg, #f5f5f7); border-radius: 12px; font-size: 0.78rem; color: var(--text-secondary, #86868b); line-height: 1.7;">
            <strong>Data Sources:</strong> Cost of living data from <a href="{NUMBEO_COL}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">Numbeo</a> &middot; <a href="{EXPATISTAN}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">Expatistan</a>. Rent from <a href="{NUMBEO_RENT}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">Numbeo Property Prices</a>. Tax rates from <a href="{OECD_TAX}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">OECD Taxing Wages</a>{country_part}. Salary data from <a href="{BLS}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">BLS</a> &middot; <a href="{GLASSDOOR}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">Glassdoor</a>. Exchange rates from the <a href="{ECB}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">ECB</a>. Updated {TODAY}. All figures are estimates.
        </div>

'''

# ---------------------------------------------------------------------------
# Injection helper
# ---------------------------------------------------------------------------
FOOTER_TAG = '<footer class="page-footer">'

def inject(filepath, snippet):
    """Read file, inject snippet before the last <footer>, write back.
    Returns 'updated', 'skipped', or 'error'.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        return 'skipped'

    pos = content.rfind(FOOTER_TAG)
    if pos == -1:
        return 'error'

    new_content = content[:pos] + snippet + content[pos:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return 'updated'

# ---------------------------------------------------------------------------
# Processing functions
# ---------------------------------------------------------------------------
def process_ranking_pages():
    pattern = os.path.join(ROOT, 'rankings', '*.html')
    files = sorted(glob.glob(pattern))
    updated = skipped = errors = 0
    print(f'--- Ranking pages ({len(files)} files) ---')
    for fp in files:
        basename = os.path.basename(fp)
        if basename == 'index.html':
            print(f'  SKIP (index): {basename}')
            skipped += 1
            continue
        result = inject(fp, TEMPLATE_A)
        if result == 'updated':
            print(f'  UPDATED: {basename}')
            updated += 1
        elif result == 'skipped':
            print(f'  SKIPPED (already has marker): {basename}')
            skipped += 1
        else:
            print(f'  WARNING: footer not found in {basename}')
            errors += 1
    print(f'  Subtotal: {updated} updated, {skipped} skipped, {errors} errors\n')
    return (updated, skipped, errors)


def process_salary_pages():
    pattern = os.path.join(ROOT, 'salary', '*.html')
    files = sorted(glob.glob(pattern))
    updated = skipped = errors = 0
    print(f'--- Salary pages ({len(files)} files) ---')
    for fp in files:
        basename = os.path.basename(fp)
        if basename == 'index.html':
            print(f'  SKIP (index): {basename}')
            skipped += 1
            continue
        result = inject(fp, TEMPLATE_A)
        if result == 'updated':
            print(f'  UPDATED: {basename}')
            updated += 1
        elif result == 'skipped':
            print(f'  SKIPPED (already has marker): {basename}')
            skipped += 1
        else:
            print(f'  WARNING: footer not found in {basename}')
            errors += 1
    print(f'  Subtotal: {updated} updated, {skipped} skipped, {errors} errors\n')
    return (updated, skipped, errors)


def process_salary_needed_city_pages():
    pattern = os.path.join(ROOT, 'salary-needed', '*.html')
    files = sorted(glob.glob(pattern))
    updated = skipped = errors = 0
    print(f'--- Salary-needed city pages ({len(files)} files) ---')
    for fp in files:
        basename = os.path.basename(fp)
        slug = os.path.splitext(basename)[0]
        country = SLUG_TO_COUNTRY.get(slug, None)
        snippet = build_template_b(country)
        result = inject(fp, snippet)
        if result == 'updated':
            print(f'  UPDATED: {basename} (country={country})')
            updated += 1
        elif result == 'skipped':
            print(f'  SKIPPED (already has marker): {basename}')
            skipped += 1
        else:
            print(f'  WARNING: footer not found in {basename}')
            errors += 1
    print(f'  Subtotal: {updated} updated, {skipped} skipped, {errors} errors\n')
    return (updated, skipped, errors)


def process_salary_needed_neighborhood_pages():
    pattern = os.path.join(ROOT, 'salary-needed', '*', '*.html')
    files = sorted(glob.glob(pattern))
    updated = skipped = errors = 0
    print(f'--- Salary-needed neighborhood pages ({len(files)} files) ---')
    for fp in files:
        basename = os.path.basename(fp)
        slug = os.path.basename(os.path.dirname(fp))
        country = SLUG_TO_COUNTRY.get(slug, None)
        snippet = build_template_b(country)
        result = inject(fp, snippet)
        if result == 'updated':
            print(f'  UPDATED: {slug}/{basename} (country={country})')
            updated += 1
        elif result == 'skipped':
            print(f'  SKIPPED (already has marker): {slug}/{basename}')
            skipped += 1
        else:
            print(f'  WARNING: footer not found in {slug}/{basename}')
            errors += 1
    print(f'  Subtotal: {updated} updated, {skipped} skipped, {errors} errors\n')
    return (updated, skipped, errors)


def process_neighborhood_compare_pages():
    pattern = os.path.join(ROOT, 'compare', '*', '*.html')
    files = sorted(glob.glob(pattern))
    updated = skipped = errors = 0
    print(f'--- Neighborhood compare pages ({len(files)} files) ---')
    for fp in files:
        basename = os.path.basename(fp)
        slug = os.path.basename(os.path.dirname(fp))
        country = SLUG_TO_COUNTRY.get(slug, None)
        snippet = build_template_b(country)
        result = inject(fp, snippet)
        if result == 'updated':
            print(f'  UPDATED: {slug}/{basename} (country={country})')
            updated += 1
        elif result == 'skipped':
            print(f'  SKIPPED (already has marker): {slug}/{basename}')
            skipped += 1
        else:
            print(f'  WARNING: footer not found in {slug}/{basename}')
            errors += 1
    print(f'  Subtotal: {updated} updated, {skipped} skipped, {errors} errors\n')
    return (updated, skipped, errors)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f'add-citations-bulk.py -- adding citations to pages')
    print(f'Idempotency marker: {MARKER}')
    print()

    r = process_ranking_pages()
    s = process_salary_pages()
    sc = process_salary_needed_city_pages()
    sn = process_salary_needed_neighborhood_pages()
    nc = process_neighborhood_compare_pages()

    total_updated = r[0]+s[0]+sc[0]+sn[0]+nc[0]
    total_skipped = r[1]+s[1]+sc[1]+sn[1]+nc[1]
    total_errors = r[2]+s[2]+sc[2]+sn[2]+nc[2]

    print(f'\n{"="*50}')
    print(f'TOTAL: {total_updated} updated, {total_skipped} skipped, {total_errors} errors')


if __name__ == '__main__':
    main()
