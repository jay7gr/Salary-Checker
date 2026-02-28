#!/usr/bin/env python3
"""
Generate job-title salary landing pages for salary-converter.com
Loads data from generate-pages.py and creates 37 individual salary pages + 1 index page
in the /salary/ directory.
"""

import os
import json
import html as html_mod
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

_source = open(os.path.join(ROOT, 'generate-pages.py'), encoding='utf-8').read()
_data_portion = _source.split("if __name__ == '__main__':")[0]

_namespace = {}
exec(_data_portion, _namespace)

coliData = _namespace['coliData']
exchangeRates = _namespace['exchangeRates']
cityToCurrency = _namespace['cityToCurrency']
cityCountry = _namespace['cityCountry']
taxBrackets = _namespace['taxBrackets']
countryDeductions = _namespace['countryDeductions']
calculate_tax = _namespace['calculate_tax']
calculate_all_deductions = _namespace['calculate_all_deductions']
slugify = _namespace['slugify']
format_currency_amount = _namespace['format_currency_amount']
build_share_bar = _namespace['build_share_bar']
salaryRanges = _namespace['salaryRanges']

THEME_CSS_VARS = _namespace['THEME_CSS_VARS']
THEME_TOGGLE_CSS = _namespace['THEME_TOGGLE_CSS']
THEME_JS = _namespace['THEME_JS']
SHARE_JS = _namespace['SHARE_JS']
GA4_SNIPPET = _namespace['GA4_SNIPPET']
WISE_LINK = _namespace['WISE_LINK']

CURRENT_YEAR = date.today().year

JOB_CATEGORIES = {
    'Healthcare': ['Doctor (General)', 'Surgeon', 'Dentist', 'Pharmacist', 'Nurse', 'Psychologist'],
    'Engineering & Tech': ['Software Engineer', 'DevOps Engineer', 'Data Scientist', 'Mechanical Engineer', 'Civil Engineer', 'Electrical Engineer', 'Architect', 'UX Designer'],
    'Business & Finance': ['Product Manager', 'Project Manager', 'Financial Analyst', 'Accountant', 'Business Analyst', 'Consultant', 'Investment Banker', 'Actuary'],
    'Legal': ['Lawyer', 'Paralegal'],
    'Marketing & Sales': ['Marketing Manager', 'Sales Manager', 'Graphic Designer', 'Content Writer'],
    'Management & HR': ['HR Manager', 'Operations Manager', 'CEO / Executive'],
    'Education & Research': ['Teacher', 'Professor', 'Research Scientist'],
    'Skilled Trades & Other': ['Pilot', 'Chef', 'Journalist'],
}

JOB_TO_CATEGORY = {}
for cat, titles in JOB_CATEGORIES.items():
    for title in titles:
        JOB_TO_CATEGORY[title] = cat


def compute_city_salary_data(job_title, city):
    ranges = salaryRanges[job_title]
    mid_salary_usd = ranges['mid']
    coli = coliData.get(city, 50)
    adjusted_usd = mid_salary_usd * (coli / 100)
    currency = cityToCurrency.get(city, 'USD')
    rate_to_local = exchangeRates.get(currency, 1) / exchangeRates.get('USD', 1)
    local_salary = adjusted_usd * rate_to_local
    country = cityCountry.get(city, '')
    if local_salary > 0:
        ded = calculate_all_deductions(local_salary, country, city)
        take_home_pct = (1 - ded['total_rate']) * 100
    else:
        take_home_pct = 100.0
    local_formatted = format_currency_amount(local_salary, currency)
    return {
        'adjusted_usd': adjusted_usd, 'local_salary': local_salary,
        'local_formatted': local_formatted, 'currency': currency,
        'coli': coli, 'take_home_pct': take_home_pct,
    }


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
        .page-wrapper {{ max-width: 1100px; margin: 0 auto; padding: 32px 24px 60px; }}
        .nav-bar {{ display: flex; align-items: center; justify-content: space-between; padding: 16px 0 24px; border-bottom: 1px solid var(--border-light); margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }}
        .nav-bar a {{ color: var(--text-secondary); text-decoration: none; font-size: 0.8rem; font-weight: 500; }}
        .nav-bar a:hover {{ color: var(--accent); }}
        .logo {{ font-size: 1rem; font-weight: 700; color: var(--text-primary) !important; letter-spacing: -0.5px; }}
        .breadcrumb {{ font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        .hero {{ margin-bottom: 24px; }}
        .hero h1 {{ font-size: 1.6rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .hero-desc {{ font-size: 0.9rem; color: var(--text-body); line-height: 1.6; }}
        .hero p {{ font-size: 0.9rem; color: var(--text-body); }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }}
        .stat-card {{ background: var(--stat-card-bg); border-radius: 12px; padding: 16px; text-align: center; }}
        .stat-card .label {{ font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); margin-bottom: 4px; }}
        .stat-card .value {{ font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }}
        .stat-card .sub {{ font-size: 0.75rem; color: var(--text-secondary); margin-top: 2px; }}
        .content-card {{ background: var(--card-bg); border-radius: 16px; padding: 28px 24px; box-shadow: var(--shadow); margin-bottom: 20px; }}
        .content-card h2 {{ font-size: 1.15rem; font-weight: 700; margin-bottom: 16px; }}
        .content-card p {{ font-size: 0.9rem; color: var(--text-body); line-height: 1.6; margin-bottom: 12px; }}
        .table-wrapper {{ overflow-x: auto; }}
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
                <a href="/salary/">Salaries</a>
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
            <a href="/salary/">Salaries</a>
            <a href="/city/">Cities</a>
            <a href="/compare/">Compare</a>
            <a href="/blog/">Blog</a>
        </footer>'''


def generate_salary_page(job_title):
    ranges = salaryRanges[job_title]
    low, mid, high = ranges['low'], ranges['mid'], ranges['high']
    slug = slugify(job_title)
    jt_lower = job_title.lower()
    city_data = []
    for city in sorted(coliData.keys()):
        d = compute_city_salary_data(job_title, city)
        city_data.append({'city': city, 'city_slug': slugify(city), **d})
    city_data.sort(key=lambda x: x['adjusted_usd'], reverse=True)
    nc = len(city_data)
    fmt_mid = f'${mid:,}'
    h_city = city_data[0]['city']
    h_sal = f'${city_data[0]["adjusted_usd"]:,.0f}' 
    m_city = city_data[nc//2]['city']
    m_sal = f'${city_data[nc//2]["adjusted_usd"]:,.0f}' 
    bv = max(city_data, key=lambda x: x['adjusted_usd'] * x['take_home_pct'] / max(x['coli'], 1))
    bv_city = bv['city']
    bv_sal = f'${bv["adjusted_usd"]:,.0f}' 
    low_k, high_k = low // 1000, high // 1000
    canon = f'https://salary-converter.com/salary/{slug}'
    ptitle = f'{job_title} Salary by City ({CURRENT_YEAR}) | salary:converter'
    mdesc = f'What do {jt_lower}s earn in {nc} cities worldwide? ${low_k}K-${high_k}K base, adjusted for cost of living. Compare take-home pay across cities.'
    sbar = build_share_bar(f'{job_title} Salary by City ({CURRENT_YEAR}) | salary:converter', canon)
    rows = ''
    for i, r in enumerate(city_data):
        rows += f'<tr><td style="text-align:center; color:var(--text-secondary);">{i+1}</td><td><a href="/city/{r["city_slug"]}" style="color: var(--accent); text-decoration: none; font-weight: 500;">{html_mod.escape(r["city"])}</a></td><td style="text-align:right; font-weight:600;">{r["local_formatted"]}</td><td style="text-align:right;">${r["adjusted_usd"]:,.0f}</td><td style="text-align:center;">{r["coli"]:.1f}</td><td style="text-align:center;">{r["take_home_pct"]:.1f}%</td></tr>\n' 
    f1q = f'What is the average {jt_lower} salary in {CURRENT_YEAR}?'
    f1a = f'The mid-career {jt_lower} base salary is {fmt_mid} (New York baseline). Entry-level starts around ${low:,} and senior roles can reach ${high:,}. These figures are adjusted for each city using local cost of living.'
    f2q = f'Which city pays {jt_lower}s the most?'
    f2a = f'After adjusting for cost of living, {h_city} offers the highest {jt_lower} salary at {h_sal} (USD equivalent). See the full table above for all {nc} cities.'
    f3q = 'How is the salary adjusted for each city?'
    f3a = "We start with the New York baseline salary and scale it by each city's Cost of Living Index (COLI). For example, a city with COLI 50 means living costs are half of New York, so the adjusted salary is 50% of the baseline. Take-home percentage accounts for local income tax and social contributions."
    faq_s = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f1q, "acceptedAnswer": {"@type": "Answer", "text": f1a}}, {"@type": "Question", "name": f2q, "acceptedAnswer": {"@type": "Answer", "text": f2a}}, {"@type": "Question", "name": f3q, "acceptedAnswer": {"@type": "Answer", "text": f3a}}]})
    bc_s = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"}, {"@type": "ListItem", "position": 2, "name": "Salaries", "item": "https://salary-converter.com/salary/"}, {"@type": "ListItem", "position": 3, "name": f'{job_title} Salary'}]})
    cat = JOB_TO_CATEGORY.get(job_title, '')
    rel = ''.join(f'<a href="/salary/{slugify(t)}" class="similar-city-link">{html_mod.escape(t)}</a>' for t in JOB_CATEGORIES.get(cat, []) if t != job_title)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{html_mod.escape(ptitle)}</title><link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta name="description" content="{html_mod.escape(mdesc)}"><link rel="canonical" href="{canon}">
    <meta property="og:type" content="article"><meta property="og:title" content="{html_mod.escape(ptitle)}">
    <meta property="og:description" content="{html_mod.escape(mdesc)}"><meta property="og:url" content="{canon}">
    <meta name="twitter:card" content="summary"><meta name="twitter:title" content="{html_mod.escape(ptitle)}">
    <meta name="twitter:description" content="{html_mod.escape(mdesc)}">
    <script type="application/ld+json">{bc_s}</script>
    <script type="application/ld+json">{faq_s}</script>
{GA4_SNIPPET}
    <style>{_base_css()}</style>
</head>
<body>
    <div class="page-wrapper">
        {_nav_bar()}
        <div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/salary/">Salaries</a> &rsaquo; {html_mod.escape(job_title)} Salary</div>
        <div class="hero"><h1>{html_mod.escape(job_title)} Salary by City ({CURRENT_YEAR})</h1><p class="hero-desc">Mid-career base salary: {fmt_mid} in New York. See what it&rsquo;s worth in {nc} cities after adjusting for cost of living and taxes.</p></div>
        <div class="stat-grid">
            <div class="stat-card"><div class="stat-label">Highest Adjusted</div><div class="stat-value">{html_mod.escape(h_city)}</div><div class="stat-sub">{h_sal}</div></div>
            <div class="stat-card"><div class="stat-label">Median City</div><div class="stat-value">{html_mod.escape(m_city)}</div><div class="stat-sub">{m_sal}</div></div>
            <div class="stat-card"><div class="stat-label">Best Value</div><div class="stat-value">{html_mod.escape(bv_city)}</div><div class="stat-sub">{bv_sal}</div></div>
        </div>
        {sbar}
        <section class="content-card">
            <h2>{html_mod.escape(job_title)} Salary &mdash; All {nc} Cities</h2>
            <div class="table-wrapper"><table><thead><tr><th style="text-align:center; width:40px;">#</th><th>City</th><th style="text-align:right;">Salary (Local)</th><th style="text-align:right;">Salary (USD)</th><th style="text-align:center;">COLI</th><th style="text-align:center;">Take-Home %</th></tr></thead><tbody>{rows}</tbody></table></div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 16px; margin-bottom: 0;">Data covers {nc} cities worldwide. Salaries adjusted by Cost of Living Index (New York = 100). Updated {CURRENT_YEAR}.</p>
        </section>
{WISE_CTA}
        <section class="content-card"><h2>Salary Range</h2><p>Typical {html_mod.escape(jt_lower)} salary range (New York baseline, USD):</p>
            <div class="stat-grid"><div class="stat-card"><div class="stat-label">Entry Level</div><div class="stat-value">${low:,}</div></div><div class="stat-card"><div class="stat-label">Mid-Career</div><div class="stat-value">${mid:,}</div></div><div class="stat-card"><div class="stat-label">Senior</div><div class="stat-value">${high:,}</div></div></div>
        </section>
        <section class="content-card"><h2>Related Salaries</h2><div class="similar-cities">{rel}</div></section>
        <section class="content-card"><h2>Explore More</h2><div class="similar-cities"><a href="/rankings/highest-salaries" class="similar-city-link">Highest Salary Cities</a><a href="/rankings/best-value-cities" class="similar-city-link">Best Value Cities</a><a href="/rankings/lowest-taxes" class="similar-city-link">Lowest Tax Cities</a><a href="/salary/" class="similar-city-link">All Salaries</a></div></section>
        <section class="content-card"><h2>Frequently Asked Questions</h2>
            <div class="faq-item"><h3>{html_mod.escape(f1q)}</h3><p>{html_mod.escape(f1a)}</p></div>
            <div class="faq-item"><h3>{html_mod.escape(f2q)}</h3><p>{html_mod.escape(f2a)}</p></div>
            <div class="faq-item"><h3>{html_mod.escape(f3q)}</h3><p>{html_mod.escape(f3a)}</p></div>
        </section>
        {_footer()}
    </div>
{THEME_JS}
{SHARE_JS}
</body>
</html>'''
    return html


def generate_index_page():
    nc = len(coliData)
    ptitle = f'Salary by Job Title ({CURRENT_YEAR}) \u2014 37 Professions in {nc} Cities | salary:converter'
    mdesc = f'Compare salaries for 37 professions across {nc} cities worldwide. Each salary is adjusted for local cost of living and taxes. Updated {CURRENT_YEAR}.'
    canon = 'https://salary-converter.com/salary/'
    bc_s = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"}, {"@type": "ListItem", "position": 2, "name": "Salaries"}]})
    sections = ''
    for cat_name, titles in JOB_CATEGORIES.items():
        cards = ''
        for t in titles:
            r = salaryRanges[t]
            cards += f'<a href="/salary/{slugify(t)}" class="ranking-card"><h3>{html_mod.escape(t)}</h3><p>${r["low"]//1000}K &ndash; ${r["high"]//1000}K</p><span class="card-cta">Compare {nc} cities &rarr;</span></a>' 
        sections += f'<section class="content-card"><h2>{html_mod.escape(cat_name)}</h2><div class="ranking-grid">{cards}</div></section>' 
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{html_mod.escape(ptitle)}</title><link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta name="description" content="{html_mod.escape(mdesc)}"><link rel="canonical" href="{canon}">
    <meta property="og:type" content="website"><meta property="og:title" content="{html_mod.escape(ptitle)}">
    <meta property="og:description" content="{html_mod.escape(mdesc)}"><meta property="og:url" content="{canon}">
    <meta name="twitter:card" content="summary"><meta name="twitter:title" content="{html_mod.escape(ptitle)}">
    <meta name="twitter:description" content="{html_mod.escape(mdesc)}">
    <script type="application/ld+json">{bc_s}</script>
{GA4_SNIPPET}
    <style>{_base_css()}
        .ranking-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
        .ranking-card {{ background: var(--stat-card-bg); border-radius: 12px; padding: 20px; text-decoration: none; color: var(--text-primary); transition: transform 0.2s, box-shadow 0.2s; display: flex; flex-direction: column; }}
        .ranking-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 24px rgba(0,0,0,0.12); }}
        .ranking-card h3 {{ font-size: 1rem; font-weight: 700; margin-bottom: 6px; color: var(--text-primary); }}
        .ranking-card p {{ font-size: 0.85rem; color: var(--text-body); line-height: 1.5; margin: 0 0 10px; flex: 1; }}
        .card-cta {{ font-size: 0.82rem; font-weight: 600; color: var(--accent); }}
        @media (max-width: 600px) {{ .ranking-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        {_nav_bar()}
        <div class="breadcrumb"><a href="/">Home</a> &rsaquo; Salaries</div>
        <div class="hero"><h1>Salary by Job Title ({CURRENT_YEAR})</h1><p>Compare salaries for 37 professions across {nc} cities worldwide. Each salary is adjusted for local cost of living and taxes.</p></div>
        {sections}
{WISE_CTA}
        <section class="content-card"><h2>Explore More</h2><div class="similar-cities"><a href="/rankings/" class="similar-city-link">City Rankings</a><a href="/city/" class="similar-city-link">All Cities</a><a href="/compare/" class="similar-city-link">Compare Cities</a><a href="/blog/" class="similar-city-link">Blog</a></div></section>
        {_footer()}
    </div>
{THEME_JS}
</body>
</html>'''
    return html


if __name__ == '__main__':
    salary_dir = os.path.join(ROOT, 'salary')
    os.makedirs(salary_dir, exist_ok=True)
    all_job_titles = list(salaryRanges.keys())
    print(f'Generating salary pages for {len(all_job_titles)} job titles across {len(coliData)} cities...')
    for job_title in all_job_titles:
        slug = slugify(job_title)
        filepath = os.path.join(salary_dir, f'{slug}.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(generate_salary_page(job_title))
        print(f'  Created: salary/{slug}.html')
    index_path = os.path.join(salary_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(generate_index_page())
    print(f'  Created: salary/index.html')
    print(f'\nGenerated {len(all_job_titles)} salary pages in salary/')
