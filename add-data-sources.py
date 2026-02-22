#!/usr/bin/env python3
"""
One-time script: Add authoritative data sources section to neighborhood pages.

Adds external links to government statistics agencies and OECD for E-E-A-T
signals. Placed before the page footer.
"""

import os
import sys
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import importlib.util
spec = importlib.util.spec_from_file_location("generate_pages", os.path.join(BASE_DIR, "generate-pages.py"))
gp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gp)

cityNeighborhoods = gp.cityNeighborhoods
cityCountry = gp.cityCountry
slugify = gp.slugify

CURRENT_YEAR = date.today().year

COUNTRY_SOURCES = {
    'United States': [
        ('U.S. Bureau of Labor Statistics', 'https://www.bls.gov/cpi/'),
        ('U.S. Census Bureau', 'https://www.census.gov/topics/income-poverty.html'),
    ],
    'United Kingdom': [
        ('UK Office for National Statistics', 'https://www.ons.gov.uk/economy/inflationandpriceindices'),
        ('HM Revenue &amp; Customs', 'https://www.gov.uk/government/organisations/hm-revenue-customs'),
    ],
    'Germany': [
        ('Statistisches Bundesamt (Destatis)', 'https://www.destatis.de/EN/Themes/Prices/_node.html'),
        ('Bundesagentur für Arbeit', 'https://www.arbeitsagentur.de/'),
    ],
    'Japan': [
        ('Statistics Bureau of Japan', 'https://www.stat.go.jp/english/data/cpi/index.html'),
        ('Ministry of Health, Labour and Welfare', 'https://www.mhlw.go.jp/english/'),
    ],
    'France': [
        ('INSEE (Institut national de la statistique)', 'https://www.insee.fr/en/accueil'),
        ("Ministère de l'Économie", 'https://www.economie.gouv.fr/'),
    ],
    'Australia': [
        ('Australian Bureau of Statistics', 'https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation'),
        ('Australian Taxation Office', 'https://www.ato.gov.au/'),
    ],
    'Canada': [
        ('Statistics Canada', 'https://www.statcan.gc.ca/en/subjects-start/prices_and_price_indexes'),
        ('Canada Revenue Agency', 'https://www.canada.ca/en/revenue-agency.html'),
    ],
    'Singapore': [
        ('Singapore Department of Statistics', 'https://www.singstat.gov.sg/'),
        ('Inland Revenue Authority of Singapore', 'https://www.iras.gov.sg/'),
    ],
    'UAE': [
        ('Federal Competitiveness and Statistics Centre', 'https://fcsc.gov.ae/en-us'),
    ],
    'South Korea': [
        ('Statistics Korea (KOSTAT)', 'https://kostat.go.kr/portal/eng/index.action'),
    ],
    'Spain': [
        ('Instituto Nacional de Estadística (INE)', 'https://www.ine.es/en/index.htm'),
    ],
    'Italy': [
        ('Istituto Nazionale di Statistica (ISTAT)', 'https://www.istat.it/en/'),
    ],
    'Switzerland': [
        ('Swiss Federal Statistical Office', 'https://www.bfs.admin.ch/bfs/en/home.html'),
    ],
    'Netherlands': [
        ('Statistics Netherlands (CBS)', 'https://www.cbs.nl/en-gb'),
    ],
}


def build_sources_html(country):
    c_sources = COUNTRY_SOURCES.get(country, [])
    all_sources = c_sources + [('OECD Better Life Index', 'https://www.oecdbetterlifeindex.org/')]
    source_links = ' · '.join([
        f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">{name}</a>'
        for name, url in all_sources
    ])
    return f'''<div style="margin-top: 24px; padding: 16px; background: var(--stat-card-bg, #f5f5f7); border-radius: 12px; font-size: 0.78rem; color: var(--text-secondary, #86868b); line-height: 1.7;">
            <strong>Data Sources:</strong> Cost of living indices based on crowd-sourced price data and official statistics. Tax calculations follow {CURRENT_YEAR} rates. Sources include {source_links}. Figures are estimates and may vary based on individual circumstances.
        </div>'''


def main():
    city_dir = os.path.join(BASE_DIR, 'city')
    added_count = 0
    skipped_count = 0

    for city, neighborhoods in cityNeighborhoods.items():
        city_slug = slugify(city)
        country = cityCountry.get(city, '')
        city_path = os.path.join(city_dir, city_slug)
        if not os.path.isdir(city_path):
            continue

        sources_html = build_sources_html(country)

        for neighborhood in neighborhoods:
            nhood_slug = slugify(neighborhood)
            fpath = os.path.join(city_path, f'{nhood_slug}.html')
            if not os.path.exists(fpath):
                continue

            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Idempotency check
            if 'Data Sources:' in content:
                skipped_count += 1
                continue

            # Insert before the page footer
            footer_marker = '<footer class="page-footer">'
            pos = content.rfind(footer_marker)
            if pos == -1:
                print(f'  SKIP (no footer): {city_slug}/{nhood_slug}.html')
                skipped_count += 1
                continue

            content = content[:pos] + sources_html + '\n\n        ' + content[pos:]

            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

            added_count += 1
            if added_count <= 10 or added_count % 200 == 0:
                print(f'  Added sources: {city_slug}/{nhood_slug}.html')

    print(f'\nDone: Added data sources to {added_count} pages.')
    if skipped_count:
        print(f'  Skipped {skipped_count} (already had sources or no footer).')


if __name__ == '__main__':
    main()
