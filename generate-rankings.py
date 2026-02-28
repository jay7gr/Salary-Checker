#!/usr/bin/env python3
"""
Generate ranking pages for salary-converter.com
Loads data from generate-pages.py and creates 8 ranking pages + 1 index page
in the /rankings/ directory.
"""

import os
import json
import html as html_mod
from datetime import date

# ============================================================
# LOAD DATA FROM generate-pages.py via exec()
# ============================================================

ROOT = os.path.dirname(os.path.abspath(__file__))

_source = open(os.path.join(ROOT, 'generate-pages.py'), encoding='utf-8').read()
_data_portion = _source.split("if __name__ == '__main__':")[0]

_namespace = {}
exec(_data_portion, _namespace)

# Pull everything we need into module scope
coliData = _namespace['coliData']
exchangeRates = _namespace['exchangeRates']
cityToCurrency = _namespace['cityToCurrency']
cityCountry = _namespace['cityCountry']
cityRent1BR = _namespace['cityRent1BR']
taxBrackets = _namespace['taxBrackets']
countryDeductions = _namespace['countryDeductions']
calculate_tax = _namespace['calculate_tax']
calculate_all_deductions = _namespace['calculate_all_deductions']
slugify = _namespace['slugify']
format_currency_amount = _namespace['format_currency_amount']
build_share_bar = _namespace['build_share_bar']

THEME_CSS_VARS = _namespace['THEME_CSS_VARS']
THEME_TOGGLE_CSS = _namespace['THEME_TOGGLE_CSS']
THEME_JS = _namespace['THEME_JS']
SHARE_JS = _namespace['SHARE_JS']
GA4_SNIPPET = _namespace['GA4_SNIPPET']
WISE_LINK = _namespace['WISE_LINK']

CURRENT_YEAR = date.today().year

# ============================================================
# ESTIMATED MONTHLY LIVING COSTS (USD) PER CITY
# Keys: groceries, utilities, transport, healthcare, childcare
# ============================================================

def _estimate_living_costs(city):
    """Estimate monthly living costs in USD based on COLI index.
    Returns dict with groceries, utilities, transport, healthcare, childcare."""
    coli = coliData.get(city, 50)
    factor = coli / 100.0  # NY = 1.0
    return {
        'groceries': round(550 * factor),
        'utilities': round(180 * factor),
        'transport': round(130 * factor),
        'healthcare': round(200 * factor),
        'childcare': round(1200 * factor),
    }

cityLivingCosts = {city: _estimate_living_costs(city) for city in coliData}


# ============================================================
# COUNTRY FLAG EMOJI MAPPING
# ============================================================

COUNTRY_FLAGS = {
    'United States': '\U0001F1FA\U0001F1F8',
    'Canada': '\U0001F1E8\U0001F1E6',
    'Mexico': '\U0001F1F2\U0001F1FD',
    'Panama': '\U0001F1F5\U0001F1E6',
    'United Kingdom': '\U0001F1EC\U0001F1E7',
    'France': '\U0001F1EB\U0001F1F7',
    'Netherlands': '\U0001F1F3\U0001F1F1',
    'Germany': '\U0001F1E9\U0001F1EA',
    'Ireland': '\U0001F1EE\U0001F1EA',
    'Belgium': '\U0001F1E7\U0001F1EA',
    'Luxembourg': '\U0001F1F1\U0001F1FA',
    'Switzerland': '\U0001F1E8\U0001F1ED',
    'Spain': '\U0001F1EA\U0001F1F8',
    'Portugal': '\U0001F1F5\U0001F1F9',
    'Italy': '\U0001F1EE\U0001F1F9',
    'Greece': '\U0001F1EC\U0001F1F7',
    'Croatia': '\U0001F1ED\U0001F1F7',
    'Sweden': '\U0001F1F8\U0001F1EA',
    'Denmark': '\U0001F1E9\U0001F1F0',
    'Finland': '\U0001F1EB\U0001F1EE',
    'Norway': '\U0001F1F3\U0001F1F4',
    'Austria': '\U0001F1E6\U0001F1F9',
    'Czech Republic': '\U0001F1E8\U0001F1FF',
    'Hungary': '\U0001F1ED\U0001F1FA',
    'Poland': '\U0001F1F5\U0001F1F1',
    'Romania': '\U0001F1F7\U0001F1F4',
    'Estonia': '\U0001F1EA\U0001F1EA',
    'Latvia': '\U0001F1F1\U0001F1FB',
    'Turkey': '\U0001F1F9\U0001F1F7',
    'Japan': '\U0001F1EF\U0001F1F5',
    'South Korea': '\U0001F1F0\U0001F1F7',
    'China (SAR)': '\U0001F1ED\U0001F1F0',
    'Taiwan': '\U0001F1F9\U0001F1FC',
    'China': '\U0001F1E8\U0001F1F3',
    'Singapore': '\U0001F1F8\U0001F1EC',
    'Thailand': '\U0001F1F9\U0001F1ED',
    'Malaysia': '\U0001F1F2\U0001F1FE',
    'Vietnam': '\U0001F1FB\U0001F1F3',
    'Philippines': '\U0001F1F5\U0001F1ED',
    'Indonesia': '\U0001F1EE\U0001F1E9',
    'Cambodia': '\U0001F1F0\U0001F1ED',
    'India': '\U0001F1EE\U0001F1F3',
    'Australia': '\U0001F1E6\U0001F1FA',
    'New Zealand': '\U0001F1F3\U0001F1FF',
    'UAE': '\U0001F1E6\U0001F1EA',
    'Qatar': '\U0001F1F6\U0001F1E6',
    'Saudi Arabia': '\U0001F1F8\U0001F1E6',
    'Israel': '\U0001F1EE\U0001F1F1',
    'South Africa': '\U0001F1FF\U0001F1E6',
    'Kenya': '\U0001F1F0\U0001F1EA',
    'Nigeria': '\U0001F1F3\U0001F1EC',
    'Egypt': '\U0001F1EA\U0001F1EC',
    'Morocco': '\U0001F1F2\U0001F1E6',
    'Brazil': '\U0001F1E7\U0001F1F7',
    'Argentina': '\U0001F1E6\U0001F1F7',
    'Colombia': '\U0001F1E8\U0001F1F4',
    'Peru': '\U0001F1F5\U0001F1EA',
    'Chile': '\U0001F1E8\U0001F1F1',
    'Uruguay': '\U0001F1FA\U0001F1FE',
    'Costa Rica': '\U0001F1E8\U0001F1F7',
}


# ============================================================
# CALCULATION HELPERS
# ============================================================

def get_monthly_essentials(city):
    """Return total monthly essentials in USD: rent + groceries + utilities + transport + healthcare."""
    rent = cityRent1BR.get(city, 0)
    lc = cityLivingCosts.get(city, {})
    return rent + lc.get('groceries', 0) + lc.get('utilities', 0) + lc.get('transport', 0) + lc.get('healthcare', 0)


def get_comfortable_salary_usd(city):
    """Calculate comfortable gross salary in USD using the 50/30/20 rule.
    Essentials should be 50% of take-home, then gross up for taxes."""
    essentials = get_monthly_essentials(city)
    if essentials <= 0:
        return 0
    # Take-home needed: essentials / 0.5  (essentials = 50% of take-home)
    annual_take_home_needed = (essentials / 0.5) * 12

    # Gross up: convert take-home to gross via taxes
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    rate_to_local = exchangeRates.get(currency, 1) / exchangeRates.get('USD', 1)

    # Iterative gross-up: find gross such that gross - deductions = take_home_needed
    take_home_local = annual_take_home_needed * rate_to_local
    # Start with a guess
    gross_local = take_home_local * 1.35
    for _ in range(20):
        ded = calculate_all_deductions(gross_local, country, city)
        net = ded['net']
        if net <= 0:
            gross_local *= 2
            continue
        # Adjust proportionally
        gross_local = gross_local * (take_home_local / net)

    # Convert back to USD
    return gross_local / rate_to_local


def get_effective_tax_rate(city):
    """Calculate effective total deduction rate for a reference salary in local currency."""
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    coli = coliData.get(city, 50)
    rate_to_local = exchangeRates.get(currency, 1) / exchangeRates.get('USD', 1)
    ref_salary_local = 75000 * (coli / 100) * rate_to_local
    if ref_salary_local <= 0:
        return 0
    ded = calculate_all_deductions(ref_salary_local, country, city)
    return ded['total_rate']


def get_value_ratio(city):
    """Salary-to-cost ratio: comfortable_salary / annual_cost.
    Lower = better value (less salary needed per dollar of cost)."""
    essentials = get_monthly_essentials(city)
    annual_cost = essentials * 12
    if annual_cost <= 0:
        return float('inf')
    salary = get_comfortable_salary_usd(city)
    return salary / annual_cost


def get_family_cost(city):
    """Family monthly cost: rent * 1.5 (2BR) + childcare + groceries * 1.5."""
    rent = cityRent1BR.get(city, 0)
    lc = cityLivingCosts.get(city, {})
    return rent * 1.5 + lc.get('childcare', 0) + lc.get('groceries', 0) * 1.5


# ============================================================
# WISE CTA HTML
# ============================================================

WISE_CTA = f'''
        <section class="content-card wise-cta" style="border: 1px solid #9fe870; border-left: 4px solid #9fe870; background: var(--card-bg);">
            <div style="display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap;">
                <div style="flex:1; min-width:200px;">
                    <p style="font-size:0.65rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin:0 0 6px;">Sponsored</p>
                    <h3 style="font-size:1rem; font-weight:600; margin:0 0 6px; color:var(--text-primary);">Planning a move abroad?</h3>
                    <p style="font-size:0.85rem; color:var(--text-body); line-height:1.5; margin:0 0 12px;">Send money internationally at the real exchange rate. Save up to 6x vs traditional banks.</p>
                    <a href="{WISE_LINK}" rel="noopener noreferrer sponsored" target="_blank"
                       style="display:inline-block; padding:10px 24px; background:#9fe870; color:#1a1a1a; border-radius:100px; font-weight:600; font-size:0.85rem; text-decoration:none; transition:transform 0.2s;">
                        Try Wise for Free &rarr;
                    </a>
                </div>
            </div>
        </section>'''


# ============================================================
# RANKING PAGE DEFINITIONS
# ============================================================

def _build_rankings():
    """Pre-compute all ranking data for each page."""
    all_cities = sorted(coliData.keys())

    # Cache expensive calculations
    comfortable_salaries = {}
    tax_rates = {}
    value_ratios = {}
    family_costs = {}

    for city in all_cities:
        comfortable_salaries[city] = get_comfortable_salary_usd(city)
        tax_rates[city] = get_effective_tax_rate(city)
        value_ratios[city] = get_value_ratio(city)
        family_costs[city] = get_family_cost(city)

    rankings = [
        {
            'slug': 'cheapest-cities',
            'title': f'Cheapest Cities to Live In ({CURRENT_YEAR})',
            'meta_desc': f'Ranked: the {len(all_cities)} cheapest cities to live in worldwide. Compare cost of living, rent & salaries. Updated {CURRENT_YEAR}.',
            'h1': f'Cheapest Cities to Live In ({CURRENT_YEAR})',
            'description': f'All {len(all_cities)} cities in our database ranked from cheapest to most expensive by Cost of Living Index (New York = 100).',
            'short_desc': 'Cities ranked from lowest to highest cost of living index.',
            'data': sorted(all_cities, key=lambda c: coliData[c]),
            'primary_col': 'COLI',
            'secondary_col': '1BR Rent',
            'get_primary': lambda c: f'{coliData[c]:.1f}',
            'get_secondary': lambda c: f'${cityRent1BR.get(c, 0):,}/mo',
            'stat1_label': '#1 Cheapest',
            'stat1_value': lambda data: data[0],
            'stat2_label': 'Median City',
            'stat2_value': lambda data: data[len(data)//2],
            'stat3_label': '#1 Most Expensive',
            'stat3_value': lambda data: data[-1],
            'faqs': [
                (f'What is the cheapest city to live in {CURRENT_YEAR}?', None),
                ('How are cities ranked?', 'Cities are ranked by Cost of Living Index (COLI), where New York = 100. A COLI of 50 means living costs are roughly half of New York.'),
                ('How often is this data updated?', f'Our cost-of-living data is reviewed and updated quarterly. This page reflects {CURRENT_YEAR} data.'),
            ],
        },
        {
            'slug': 'most-expensive-cities',
            'title': f'Most Expensive Cities in the World ({CURRENT_YEAR})',
            'meta_desc': f'The {len(all_cities)} most expensive cities ranked by cost of living. Compare rent, taxes & salaries. Updated {CURRENT_YEAR}.',
            'h1': f'Most Expensive Cities in the World ({CURRENT_YEAR})',
            'description': f'All {len(all_cities)} cities ranked from most expensive to cheapest by Cost of Living Index.',
            'short_desc': 'Cities ranked from highest to lowest cost of living index.',
            'data': sorted(all_cities, key=lambda c: coliData[c], reverse=True),
            'primary_col': 'COLI',
            'secondary_col': '1BR Rent',
            'get_primary': lambda c: f'{coliData[c]:.1f}',
            'get_secondary': lambda c: f'${cityRent1BR.get(c, 0):,}/mo',
            'stat1_label': '#1 Most Expensive',
            'stat1_value': lambda data: data[0],
            'stat2_label': 'Median City',
            'stat2_value': lambda data: data[len(data)//2],
            'stat3_label': '#1 Cheapest',
            'stat3_value': lambda data: data[-1],
            'faqs': [
                (f'What is the most expensive city to live in {CURRENT_YEAR}?', None),
                ('How are cities ranked?', 'Cities are ranked by Cost of Living Index (COLI), where New York = 100. A COLI above 100 means the city is more expensive than New York.'),
                ('How often is this data updated?', f'Our cost-of-living data is reviewed and updated quarterly. This page reflects {CURRENT_YEAR} data.'),
            ],
        },
        {
            'slug': 'cheapest-rent',
            'title': f'Cities with the Cheapest Rent ({CURRENT_YEAR})',
            'meta_desc': f'Find the cheapest rent worldwide. {len(all_cities)} cities ranked by 1-bedroom apartment rent. Updated {CURRENT_YEAR}.',
            'h1': f'Cities with the Cheapest Rent ({CURRENT_YEAR})',
            'description': f'All {len(all_cities)} cities ranked by average 1-bedroom apartment rent in the city center, from cheapest to most expensive.',
            'short_desc': 'Cities ranked by average 1-bedroom rent, lowest first.',
            'data': sorted(all_cities, key=lambda c: cityRent1BR.get(c, 0)),
            'primary_col': '1BR Rent',
            'secondary_col': 'COLI',
            'get_primary': lambda c: f'${cityRent1BR.get(c, 0):,}/mo',
            'get_secondary': lambda c: f'{coliData[c]:.1f}',
            'stat1_label': 'Cheapest Rent',
            'stat1_value': lambda data: data[0],
            'stat2_label': 'Median Rent',
            'stat2_value': lambda data: data[len(data)//2],
            'stat3_label': 'Highest Rent',
            'stat3_value': lambda data: data[-1],
            'faqs': [
                (f'Which city has the cheapest rent in {CURRENT_YEAR}?', None),
                ('How are cities ranked?', 'Cities are ranked by average monthly rent for a 1-bedroom apartment in the city center, converted to USD for comparison.'),
                ('How often is this data updated?', f'Rent data is reviewed and updated quarterly. This page reflects {CURRENT_YEAR} data.'),
            ],
        },
        {
            'slug': 'highest-salaries',
            'title': f'Cities with the Highest Salaries ({CURRENT_YEAR})',
            'meta_desc': f'Which cities offer the highest salaries? {len(all_cities)} cities ranked by comfortable salary. Updated {CURRENT_YEAR}.',
            'h1': f'Cities with the Highest Salaries ({CURRENT_YEAR})',
            'description': f'All {len(all_cities)} cities ranked by the gross salary needed to live comfortably (50/30/20 rule: essentials = 50% of take-home pay).',
            'short_desc': 'Cities ranked by the salary needed to live comfortably.',
            'data': sorted(all_cities, key=lambda c: comfortable_salaries.get(c, 0), reverse=True),
            'primary_col': 'Comfortable Salary',
            'secondary_col': '1BR Rent',
            'get_primary': lambda c: f'${comfortable_salaries.get(c, 0):,.0f}/yr',
            'get_secondary': lambda c: f'${cityRent1BR.get(c, 0):,}/mo',
            'stat1_label': 'Highest Salary',
            'stat1_value': lambda data: data[0],
            'stat2_label': 'Median',
            'stat2_value': lambda data: data[len(data)//2],
            'stat3_label': 'Lowest Salary',
            'stat3_value': lambda data: data[-1],
            'faqs': [
                (f'Which city requires the highest salary in {CURRENT_YEAR}?', None),
                ('How are cities ranked?', 'Cities are ranked by the gross annual salary needed to live comfortably, calculated using the 50/30/20 budgeting rule. Essentials (rent, groceries, utilities, transport, healthcare) should equal 50% of take-home pay, then grossed up for local taxes.'),
                ('How often is this data updated?', f'Salary and cost data are reviewed and updated quarterly. This page reflects {CURRENT_YEAR} data.'),
            ],
        },
        {
            'slug': 'lowest-taxes',
            'title': f'Cities with the Lowest Taxes ({CURRENT_YEAR})',
            'meta_desc': f'Find cities with the lowest tax rates. {len(all_cities)} cities ranked by effective tax rate. Updated {CURRENT_YEAR}.',
            'h1': f'Cities with the Lowest Taxes ({CURRENT_YEAR})',
            'description': f'All {len(all_cities)} cities ranked by effective total deduction rate (income tax + social security + levies) on a reference salary, from lowest to highest.',
            'short_desc': 'Cities ranked by total effective tax & deduction rate, lowest first.',
            'data': sorted(all_cities, key=lambda c: tax_rates.get(c, 0)),
            'primary_col': 'Eff. Tax Rate',
            'secondary_col': 'COLI',
            'get_primary': lambda c: f'{tax_rates.get(c, 0):.1f}%',
            'get_secondary': lambda c: f'{coliData[c]:.1f}',
            'stat1_label': 'Lowest Tax',
            'stat1_value': lambda data: data[0],
            'stat2_label': 'Median',
            'stat2_value': lambda data: data[len(data)//2],
            'stat3_label': 'Highest Tax',
            'stat3_value': lambda data: data[-1],
            'faqs': [
                (f'Which city has the lowest taxes in {CURRENT_YEAR}?', None),
                ('How are cities ranked?', 'Cities are ranked by total effective deduction rate, which includes income tax, social security contributions, and any local levies. The rate is calculated on a reference salary scaled to local cost of living.'),
                ('How often is this data updated?', f'Tax bracket data is reviewed annually and updated for the current fiscal year. This page reflects {CURRENT_YEAR} data.'),
            ],
        },
        {
            'slug': 'best-value-cities',
            'title': f'Best Value Cities to Live In ({CURRENT_YEAR})',
            'meta_desc': f'Best value cities worldwide: lowest salary-to-cost ratio. {len(all_cities)} cities ranked. Updated {CURRENT_YEAR}.',
            'h1': f'Best Value Cities to Live In ({CURRENT_YEAR})',
            'description': f'All {len(all_cities)} cities ranked by salary-to-cost ratio. A lower ratio means you need less gross salary for every dollar of living cost — better value.',
            'short_desc': 'Cities ranked by salary-to-cost ratio. Lower = better value.',
            'data': sorted(all_cities, key=lambda c: value_ratios.get(c, float('inf'))),
            'primary_col': 'Value Ratio',
            'secondary_col': 'COLI',
            'get_primary': lambda c: f'{value_ratios.get(c, 0):.2f}x',
            'get_secondary': lambda c: f'{coliData[c]:.1f}',
            'stat1_label': 'Best Value',
            'stat1_value': lambda data: data[0],
            'stat2_label': 'Median',
            'stat2_value': lambda data: data[len(data)//2],
            'stat3_label': 'Worst Value',
            'stat3_value': lambda data: data[-1],
            'faqs': [
                (f'Which city offers the best value in {CURRENT_YEAR}?', None),
                ('How are cities ranked?', 'Cities are ranked by salary-to-cost ratio: the gross comfortable salary divided by annual living costs. A lower ratio means better value — you need less income per dollar of expenses, typically because taxes are low.'),
                ('How often is this data updated?', f'Our cost-of-living and tax data are reviewed and updated quarterly. This page reflects {CURRENT_YEAR} data.'),
            ],
        },
        {
            'slug': 'cheapest-for-families',
            'title': f'Cheapest Cities for Families ({CURRENT_YEAR})',
            'meta_desc': f'Find the cheapest cities for families. {len(all_cities)} cities ranked by family living costs. Updated {CURRENT_YEAR}.',
            'h1': f'Cheapest Cities for Families ({CURRENT_YEAR})',
            'description': f'All {len(all_cities)} cities ranked by estimated monthly family cost: 2-bedroom rent (1.5x of 1BR) + childcare + groceries for a family (1.5x single).',
            'short_desc': 'Cities ranked by monthly family cost (2BR rent + childcare + groceries).',
            'data': sorted(all_cities, key=lambda c: family_costs.get(c, 0)),
            'primary_col': 'Family Cost',
            'secondary_col': '1BR Rent',
            'get_primary': lambda c: f'${family_costs.get(c, 0):,.0f}/mo',
            'get_secondary': lambda c: f'${cityRent1BR.get(c, 0):,}/mo',
            'stat1_label': 'Cheapest',
            'stat1_value': lambda data: data[0],
            'stat2_label': 'Median',
            'stat2_value': lambda data: data[len(data)//2],
            'stat3_label': 'Most Expensive',
            'stat3_value': lambda data: data[-1],
            'faqs': [
                (f'Which city is cheapest for families in {CURRENT_YEAR}?', None),
                ('How are cities ranked?', 'Cities are ranked by estimated monthly family cost, which includes 2-bedroom rent (1.5x the 1-bedroom average), childcare, and groceries scaled for a family (1.5x single person).'),
                ('How often is this data updated?', f'Our family cost data is reviewed and updated quarterly. This page reflects {CURRENT_YEAR} data.'),
            ],
        },
    ]

    return rankings, comfortable_salaries, tax_rates, value_ratios, family_costs


# ============================================================
# HTML GENERATION
# ============================================================

def _share_bar_css():
    return '''
        .share-bar {
            display: flex; align-items: center; gap: 8px;
            margin: 16px 0 20px; padding: 12px 16px;
            background: var(--stat-card-bg, #f5f5f7); border-radius: 12px;
        }
        .share-bar-label {
            font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);
            text-transform: uppercase; letter-spacing: 0.5px; margin-right: 4px;
        }
        .share-btn {
            display: flex; align-items: center; justify-content: center;
            width: 34px; height: 34px; border-radius: 50%;
            border: 1px solid var(--border, #e5e5ea); background: var(--card-bg, #fff);
            color: var(--text-secondary, #86868b); cursor: pointer; transition: all 0.2s;
            padding: 0;
        }
        .share-btn:hover { color: var(--accent); border-color: var(--accent); transform: scale(1.08); }
        .share-btn.copied { color: #22c55e; border-color: #22c55e; }'''


def _base_css():
    return f'''{THEME_CSS_VARS}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text-primary); line-height: 1.5; -webkit-font-smoothing: antialiased; }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; padding: 32px 24px 60px; }}
        .nav-bar {{ display: flex; align-items: center; justify-content: space-between; padding: 16px 0 24px; border-bottom: 1px solid var(--border-light); margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }}
        .nav-bar a {{ color: var(--text-secondary); text-decoration: none; font-size: 0.8rem; font-weight: 500; }}
        .nav-bar a:hover {{ color: var(--accent); }}
        .logo {{ font-size: 1rem; font-weight: 700; color: var(--text-primary) !important; letter-spacing: -0.5px; }}
        .breadcrumb {{ font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        .hero {{ margin-bottom: 24px; }}
        .hero h1 {{ font-size: 1.6rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .hero p {{ font-size: 0.9rem; color: var(--text-body); }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }}
        .stat-card {{ background: var(--stat-card-bg); border-radius: 12px; padding: 16px; text-align: center; }}
        .stat-card .label {{ font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); margin-bottom: 4px; }}
        .stat-card .value {{ font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }}
        .stat-card .sub {{ font-size: 0.75rem; color: var(--text-secondary); margin-top: 2px; }}
        .content-card {{ background: var(--card-bg); border-radius: 16px; padding: 28px 24px; box-shadow: var(--shadow); margin-bottom: 20px; }}
        .content-card h2 {{ font-size: 1.15rem; font-weight: 700; margin-bottom: 16px; }}
        .content-card p {{ font-size: 0.9rem; color: var(--text-body); line-height: 1.6; margin-bottom: 12px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        th {{ text-align: left; padding: 10px 8px; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); border-bottom: 2px solid var(--border); }}
        td {{ padding: 10px 8px; border-bottom: 1px solid var(--border-light); }}
        tr:nth-child(even) {{ background: var(--table-stripe); }}
        .similar-cities {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .similar-city-link {{ display: inline-block; padding: 8px 16px; background: var(--stat-card-bg); border-radius: 8px; color: var(--accent); text-decoration: none; font-size: 0.82rem; font-weight: 500; transition: background 0.2s; }}
        .similar-city-link:hover {{ background: var(--border); }}
        .page-footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border-light); display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; }}
        .page-footer a {{ font-size: 0.78rem; color: var(--text-secondary); text-decoration: none; }}
        .page-footer a:hover {{ color: var(--accent); }}
        .faq-item {{ margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid var(--border-light); }}
        .faq-item:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .faq-item h3 {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 8px; color: var(--text-primary); }}
        .faq-item p {{ font-size: 0.9rem; color: var(--text-body); line-height: 1.7; margin: 0; }}
{THEME_TOGGLE_CSS}
{_share_bar_css()}
        @media (max-width: 600px) {{
            .page-wrapper {{ padding: 16px 16px 48px; }}
            .hero h1 {{ font-size: 1.3rem; }}
            .stat-grid {{ grid-template-columns: 1fr; }}
            table {{ font-size: 0.8rem; }}
            th, td {{ padding: 8px 6px; }}
        }}'''


def _nav_bar():
    return '''
        <nav class="nav-bar">
            <a href="/" class="logo">salary:converter</a>
            <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
                <a href="/city/">Cities</a>
                <a href="/compare/">Compare</a>
                <a href="/blog/">Blog</a>
                <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme" type="button">
                    <span class="toggle-thumb">
                        <svg class="toggle-icon icon-sun" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/></svg>
                        <svg class="toggle-icon icon-moon" viewBox="0 0 20 20" fill="currentColor"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/></svg>
                    </span>
                </button>
            </div>
        </nav>'''


def _footer():
    return '''
        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/rankings/">Rankings</a>
            <a href="/city/">Cities</a>
            <a href="/compare/">Compare</a>
            <a href="/blog/">Blog</a>
        </footer>'''


def generate_ranking_page(ranking, all_rankings):
    """Generate a single ranking page HTML."""
    page_slug = ranking['slug']
    page_title = ranking['title']
    meta_desc = ranking['meta_desc']
    h1 = ranking['h1']
    description = ranking['description']
    data = ranking['data']
    primary_col = ranking['primary_col']
    secondary_col = ranking['secondary_col']
    get_primary = ranking['get_primary']
    get_secondary = ranking['get_secondary']

    canonical_url = f'https://salary-converter.com/rankings/{page_slug}'
    share_text = f'{page_title} | salary:converter'
    share_bar = build_share_bar(share_text, canonical_url)

    # Stat cards
    stat1_city = ranking['stat1_value'](data)
    stat2_city = ranking['stat2_value'](data)
    stat3_city = ranking['stat3_value'](data)

    # Table rows
    table_rows = ''
    for i, city in enumerate(data):
        city_slug = slugify(city)
        country = cityCountry.get(city, '')
        flag = COUNTRY_FLAGS.get(country, '')
        primary_val = get_primary(city)
        secondary_val = get_secondary(city)
        table_rows += f'''
                        <tr>
                            <td style="text-align:center; color:var(--text-secondary);">{i+1}</td>
                            <td><a href="/city/{city_slug}" style="color: var(--accent); text-decoration: none; font-weight: 500;">{city}</a></td>
                            <td style="text-align:center; font-weight:600;">{primary_val}</td>
                            <td style="text-align:center;">{secondary_val}</td>
                            <td style="text-align:right;">{flag} {country}</td>
                        </tr>'''

    # FAQs
    faqs = ranking['faqs']
    faq1_q, faq1_a = faqs[0]
    if faq1_a is None:
        # Auto-generate: the #1 city
        top_city = data[0]
        faq1_a = f'According to our {CURRENT_YEAR} data, {top_city} ranks #1. See the full table above for all {len(data)} cities.'
    faq2_q, faq2_a = faqs[1]
    faq3_q, faq3_a = faqs[2]

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": faq1_q, "acceptedAnswer": {"@type": "Answer", "text": faq1_a}},
            {"@type": "Question", "name": faq2_q, "acceptedAnswer": {"@type": "Answer", "text": faq2_a}},
            {"@type": "Question", "name": faq3_q, "acceptedAnswer": {"@type": "Answer", "text": faq3_a}},
        ]
    })

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"},
            {"@type": "ListItem", "position": 2, "name": "Rankings", "item": "https://salary-converter.com/rankings/"},
            {"@type": "ListItem", "position": 3, "name": page_title},
        ]
    })

    # Cross-links to other ranking pages
    cross_links = ''
    for r in all_rankings:
        if r['slug'] == page_slug:
            continue
        cross_links += f'\n                <a href="/rankings/{r["slug"]}" class="similar-city-link">{r["title"]}</a>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{html_mod.escape(page_title)}</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta name="description" content="{html_mod.escape(meta_desc)}">
    <link rel="canonical" href="{canonical_url}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{html_mod.escape(page_title)}">
    <meta property="og:description" content="{html_mod.escape(meta_desc)}">
    <meta property="og:url" content="{canonical_url}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{html_mod.escape(page_title)}">
    <meta name="twitter:description" content="{html_mod.escape(meta_desc)}">
    <script type="application/ld+json">{breadcrumb_schema}</script>
    <script type="application/ld+json">{faq_schema}</script>
{GA4_SNIPPET}
    <style>
{_base_css()}
    </style>
</head>
<body>
    <div class="page-wrapper">
{_nav_bar()}

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/rankings/">Rankings</a> &rsaquo; {html_mod.escape(h1)}
        </div>

        <div class="hero">
            <h1>{html_mod.escape(h1)}</h1>
            <p>{html_mod.escape(description)}</p>
        </div>

        <div class="stat-grid">
            <div class="stat-card">
                <div class="label">{html_mod.escape(ranking['stat1_label'])}</div>
                <div class="value">{html_mod.escape(stat1_city)}</div>
                <div class="sub">{html_mod.escape(get_primary(stat1_city))}</div>
            </div>
            <div class="stat-card">
                <div class="label">{html_mod.escape(ranking['stat2_label'])}</div>
                <div class="value">{html_mod.escape(stat2_city)}</div>
                <div class="sub">{html_mod.escape(get_primary(stat2_city))}</div>
            </div>
            <div class="stat-card">
                <div class="label">{html_mod.escape(ranking['stat3_label'])}</div>
                <div class="value">{html_mod.escape(stat3_city)}</div>
                <div class="sub">{html_mod.escape(get_primary(stat3_city))}</div>
            </div>
        </div>

        {share_bar}

        <section class="content-card">
            <h2>Full Rankings &mdash; {html_mod.escape(h1)}</h2>
            <div style="overflow-x:auto;">
            <table>
                <thead>
                    <tr>
                        <th style="text-align:center; width:40px;">#</th>
                        <th>City</th>
                        <th style="text-align:center;">{html_mod.escape(primary_col)}</th>
                        <th style="text-align:center;">{html_mod.escape(secondary_col)}</th>
                        <th style="text-align:right;">Country</th>
                    </tr>
                </thead>
                <tbody>{table_rows}
                </tbody>
            </table>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 16px; margin-bottom: 0;">Data covers {len(data)} cities worldwide. COLI baseline: New York = 100. Updated {CURRENT_YEAR}.</p>
        </section>

{WISE_CTA}

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-item"><h3>{html_mod.escape(faq1_q)}</h3><p>{html_mod.escape(faq1_a)}</p></div>
            <div class="faq-item"><h3>{html_mod.escape(faq2_q)}</h3><p>{html_mod.escape(faq2_a)}</p></div>
            <div class="faq-item"><h3>{html_mod.escape(faq3_q)}</h3><p>{html_mod.escape(faq3_a)}</p></div>
        </section>

        <section class="content-card">
            <h2>Explore More Rankings</h2>
            <div class="similar-cities">{cross_links}
                <a href="/rankings/" class="similar-city-link">All Rankings</a>
                <a href="/city/" class="similar-city-link">All Cities</a>
            </div>
        </section>

{_footer()}
    </div>
{THEME_JS}
{SHARE_JS}
</body>
</html>'''
    return html


def generate_index_page(all_rankings):
    """Generate the rankings index page with cards linking to each ranking."""
    page_title = f'City Rankings ({CURRENT_YEAR}) | salary:converter'
    meta_desc = f'Explore {len(all_rankings)} city ranking lists: cheapest cities, highest salaries, lowest taxes, best value & more. Updated {CURRENT_YEAR}.'
    canonical_url = 'https://salary-converter.com/rankings/'

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"},
            {"@type": "ListItem", "position": 2, "name": "Rankings"},
        ]
    })

    # Build cards
    cards = ''
    for r in all_rankings:
        cards += f'''
                <a href="/rankings/{r['slug']}" class="ranking-card">
                    <h2>{html_mod.escape(r['title'])}</h2>
                    <p>{html_mod.escape(r['short_desc'])}</p>
                    <span class="card-link">View Rankings &rarr;</span>
                </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{html_mod.escape(page_title)}</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta name="description" content="{html_mod.escape(meta_desc)}">
    <link rel="canonical" href="{canonical_url}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{html_mod.escape(page_title)}">
    <meta property="og:description" content="{html_mod.escape(meta_desc)}">
    <meta property="og:url" content="{canonical_url}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{html_mod.escape(page_title)}">
    <meta name="twitter:description" content="{html_mod.escape(meta_desc)}">
    <script type="application/ld+json">{breadcrumb_schema}</script>
{GA4_SNIPPET}
    <style>
{_base_css()}
        .ranking-cards {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .ranking-card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 24px;
            box-shadow: var(--shadow);
            text-decoration: none;
            color: var(--text-primary);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
        }}
        .ranking-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 24px rgba(0,0,0,0.12);
        }}
        .ranking-card h2 {{
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-primary);
        }}
        .ranking-card p {{
            font-size: 0.85rem;
            color: var(--text-body);
            line-height: 1.5;
            margin: 0 0 12px;
            flex: 1;
        }}
        .card-link {{
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--accent);
        }}
        @media (max-width: 600px) {{
            .ranking-cards {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="page-wrapper">
{_nav_bar()}

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; Rankings
        </div>

        <div class="hero">
            <h1>City Rankings ({CURRENT_YEAR})</h1>
            <p>Explore {len(all_rankings)} ways to rank and compare {len(coliData)} cities worldwide by cost of living, rent, salaries, taxes, and more.</p>
        </div>

        <div class="ranking-cards">{cards}
        </div>

{WISE_CTA}

        <section class="content-card">
            <h2>Explore More</h2>
            <div class="similar-cities">
                <a href="/city/" class="similar-city-link">All Cities</a>
                <a href="/compare/" class="similar-city-link">Compare Cities</a>
                <a href="/blog/" class="similar-city-link">Blog</a>
            </div>
        </section>

{_footer()}
    </div>
{THEME_JS}
</body>
</html>'''
    return html


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    rankings_dir = os.path.join(ROOT, 'rankings')
    os.makedirs(rankings_dir, exist_ok=True)

    print(f'Building ranking data for {len(coliData)} cities...')
    all_rankings, comfortable_salaries, tax_rates, value_ratios, family_costs = _build_rankings()

    # Generate individual ranking pages
    for ranking in all_rankings:
        filepath = os.path.join(rankings_dir, f'{ranking["slug"]}.html')
        html = generate_ranking_page(ranking, all_rankings)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Created: rankings/{ranking["slug"]}.html')

    # Generate index page
    index_path = os.path.join(rankings_dir, 'index.html')
    html = generate_index_page(all_rankings)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Created: rankings/index.html')

    print(f'\nDone: {len(all_rankings)} ranking pages + 1 index page generated in /rankings/')
