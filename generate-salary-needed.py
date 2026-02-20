#!/usr/bin/env python3
"""
Generates "What Salary Do I Need in {City}?" pages
Reads data from index.html, generates static HTML for each city + neighborhood
"""

import os, re, json, math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Read index.html
with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
    index_html = f.read()

def js_to_json(raw):
    """Convert a JS object literal string to valid JSON.
    Properly handles single-quoted strings, double-quoted strings with apostrophes,
    comments, Infinity, trailing commas, unquoted keys, and null."""
    # Remove single-line comments (but not inside strings)
    raw = re.sub(r'//[^\n]*', '', raw)

    # Tokenize: extract strings first to protect them, then transform the rest
    tokens = []
    i = 0
    while i < len(raw):
        c = raw[i]
        if c == "'":
            # Single-quoted string — find the end, handling \' escapes
            j = i + 1
            content_chars = []
            while j < len(raw) and raw[j] != "'":
                if raw[j] == '\\' and j + 1 < len(raw):
                    next_c = raw[j + 1]
                    if next_c == "'":
                        # \' in JS single-quoted string = literal apostrophe
                        content_chars.append("'")
                        j += 2
                    elif next_c == '"':
                        content_chars.append('\\"')
                        j += 2
                    elif next_c == '\\':
                        content_chars.append('\\\\')
                        j += 2
                    else:
                        # Other escapes (\n, \t, etc.) — pass through
                        content_chars.append(raw[j:j+2])
                        j += 2
                else:
                    if raw[j] == '"':
                        content_chars.append('\\"')
                    else:
                        content_chars.append(raw[j])
                    j += 1
            j += 1  # skip closing quote
            tokens.append('"' + ''.join(content_chars) + '"')
            i = j
        elif c == '"':
            # Double-quoted string — keep as-is, just consume it
            j = i + 1
            while j < len(raw) and raw[j] != '"':
                if raw[j] == '\\':
                    j += 2
                else:
                    j += 1
            j += 1  # skip closing quote
            tokens.append(raw[i:j])
            i = j
        else:
            tokens.append(c)
            i += 1

    raw = ''.join(tokens)

    # Replace Infinity
    raw = raw.replace('Infinity', '999999999')

    # Replace null with 0
    raw = re.sub(r'\bnull\b', '0', raw)

    # Remove trailing commas before } or ]
    raw = re.sub(r',\s*}', '}', raw)
    raw = re.sub(r',\s*]', ']', raw)

    # Quote unquoted keys: word characters before a colon that aren't already quoted
    raw = re.sub(r'(?<=[{,\s])([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', raw)

    return raw


def extract_object(var_name):
    """Extract a simple JS object literal from index.html and parse it."""
    pattern = rf"const {var_name}\s*=\s*\{{([\s\S]*?)\}};"
    match = re.search(pattern, index_html)
    if not match:
        print(f"Could not find {var_name}")
        return {}
    raw = '{' + match.group(1) + '}'
    raw = js_to_json(raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Failed to parse {var_name}: {e}")
        return {}


def extract_nested_object(var_name):
    """Extract a deeply nested JS object (like cityNeighborhoods, taxBrackets, countryDeductions)."""
    pattern = rf"const {var_name}\s*=\s*\{{"
    match = re.search(pattern, index_html)
    if not match:
        print(f"Could not find {var_name}")
        return {}

    # Find the matching closing brace by counting braces
    brace_start = index_html.index('{', match.start() + len(f"const {var_name}"))
    depth = 0
    i = brace_start
    in_single = False
    in_double = False
    while i < len(index_html):
        c = index_html[i]
        if c == '\\' and (in_single or in_double):
            i += 2
            continue
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif not in_single and not in_double:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
        i += 1

    raw = index_html[brace_start:i+1]
    raw = js_to_json(raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Failed to parse {var_name}: {e}")
        lines = raw.split('\n')
        error_line = e.lineno - 1 if hasattr(e, 'lineno') else 0
        context_start = max(0, error_line - 2)
        context_end = min(len(lines), error_line + 3)
        for idx in range(context_start, context_end):
            marker = ">>>" if idx == error_line else "   "
            print(f"  {marker} {idx+1}: {lines[idx][:200]}")
        return {}

# Extract all data
print("Extracting data from index.html...")
coli_data = extract_object('coliData')
exchange_rates = extract_object('exchangeRates')
city_to_currency = extract_object('cityToCurrency')
city_to_country = extract_object('cityToCountry')
city_rent_1br = extract_object('cityRent1BR')
tax_brackets = extract_nested_object('taxBrackets')
city_living_costs = extract_nested_object('cityLivingCosts')
city_neighborhoods = extract_nested_object('cityNeighborhoods')
country_deductions = extract_nested_object('countryDeductions')
city_deduction_overrides = extract_nested_object('cityDeductionOverrides')

# Also try to get neighborhoodDeductions
neighborhood_deductions = extract_nested_object('neighborhoodDeductions')

print(f"Loaded: {len(coli_data)} cities, {len(exchange_rates)} currencies, {len(tax_brackets)} tax systems")
print(f"Neighborhoods: {sum(len(v) for v in city_neighborhoods.values())} across {len(city_neighborhoods)} cities")

if len(coli_data) == 0:
    print("ERROR: No data loaded. Exiting.")
    exit(1)

# Currency symbols
CURRENCY_SYMBOLS = {
    'USD':'$','GBP':'£','EUR':'€','JPY':'¥','CNY':'¥','CHF':'CHF ','AUD':'A$','CAD':'C$',
    'SGD':'S$','HKD':'HK$','NZD':'NZ$','SEK':'kr ','NOK':'kr ','DKK':'kr ','CZK':'Kč ',
    'HUF':'Ft ','PLN':'zł ','TRY':'₺','BRL':'R$','MXN':'MX$','ZAR':'R ','KRW':'₩',
    'TWD':'NT$','IDR':'Rp ','VND':'₫','PHP':'₱','ILS':'₪','EGP':'E£','KES':'KSh ',
    'NGN':'₦','MAD':'MAD ','ARS':'AR$','COP':'CO$','PEN':'S/','CLP':'CL$','UYU':'$U ',
    'CRC':'₡','QAR':'QR ','SAR':'SR ','PAB':'B/','RON':'lei ','AED':'AED ','INR':'₹','MYR':'RM ','THB':'฿'
}

COUNTRY_NAMES = {
    'US':'United States','CA':'Canada','MX':'Mexico','PA':'Panama','GB':'United Kingdom',
    'FR':'France','NL':'Netherlands','DE':'Germany','IE':'Ireland','BE':'Belgium','LU':'Luxembourg',
    'CH':'Switzerland','ES':'Spain','PT':'Portugal','IT':'Italy','GR':'Greece','HR':'Croatia',
    'SE':'Sweden','DK':'Denmark','FI':'Finland','NO':'Norway','AT':'Austria','CZ':'Czech Republic',
    'HU':'Hungary','PL':'Poland','RO':'Romania','EE':'Estonia','LV':'Latvia','TR':'Turkey',
    'JP':'Japan','KR':'South Korea','HK':'Hong Kong','TW':'Taiwan','CN':'China','SG':'Singapore',
    'TH':'Thailand','MY':'Malaysia','VN':'Vietnam','PH':'Philippines','ID':'Indonesia','KH':'Cambodia',
    'IN':'India','AU':'Australia','NZ':'New Zealand','AE':'UAE','QA':'Qatar','SA':'Saudi Arabia',
    'IL':'Israel','ZA':'South Africa','KE':'Kenya','NG':'Nigeria','EG':'Egypt','MA':'Morocco',
    'BR':'Brazil','AR':'Argentina','CO':'Colombia','PE':'Peru','CL':'Chile','UY':'Uruguay','CR':'Costa Rica'
}


def calc_tax(income, country_code):
    """Calculate progressive income tax."""
    brackets = tax_brackets.get(country_code, [])
    tax = 0
    prev = 0
    for bracket in brackets:
        upper, rate = bracket[0], bracket[1]
        if income <= prev:
            break
        taxable = min(income, upper) - prev
        tax += taxable * (rate / 100)
        prev = upper
    return tax


def calc_deductions(income, country_code, city_name):
    """Calculate social security and other mandatory deductions."""
    total = 0
    d = country_deductions.get(country_code, {})

    if 'social_security' in d:
        ss = d['social_security']
        rate = ss.get('local', 0) / 100
        cap = ss.get('cap', 999999999) or 999999999
        base = min(income, cap)
        total += base * rate
        # Reduced rate above cap (UK NI)
        if 'reduced_rate' in ss and income > cap:
            total += (income - cap) * (ss['reduced_rate'] / 100)

    # City/state overrides
    override = city_deduction_overrides.get(city_name, {})
    for key, val in override.items():
        if isinstance(val, dict):
            if 'rate' in val:
                total += income * (val['rate'] / 100)
            elif 'flat_annual' in val:
                total += val['flat_annual']

    # Solidarity surcharge (Germany)
    if 'solidarity' in d:
        income_tax = calc_tax(income, country_code)
        total += income_tax * (d['solidarity'].get('rate', 0) / 100)

    return total


def usd_to_local(usd, currency):
    """Convert USD to local currency."""
    return usd * exchange_rates.get(currency, 1) / exchange_rates.get('USD', 1)


def format_currency(amount, currency):
    """Format a number with currency symbol."""
    sym = CURRENCY_SYMBOLS.get(currency, currency + ' ')
    rounded = round(amount)
    if rounded >= 1000000:
        return f"{sym}{rounded/1000000:.1f}M"
    return f"{sym}{rounded:,}"


def to_slug(name):
    """Convert a name to URL-friendly slug."""
    slug = re.sub(r'\s*\(.*?\)\s*', '', name)  # remove parenthetical
    slug = re.sub(r'[^a-z0-9]+', '-', slug.lower())
    slug = slug.strip('-')
    return slug


def calc_salary_needed(city_name, nb_multiplier=1.0):
    """Calculate salary needed for three lifestyle tiers."""
    currency = city_to_currency.get(city_name)
    country = city_to_country.get(city_name)
    if not currency or not country:
        return None

    # Monthly costs in USD (base)
    rent = city_rent_1br.get(city_name, 1500) * nb_multiplier
    living = city_living_costs.get(city_name, {'groceries': 350, 'utilities': 200, 'transport': 100, 'healthcare': 300, 'childcare': 0})
    essentials = living.get('groceries', 350) + living.get('utilities', 200) + living.get('transport', 100) + living.get('healthcare', 300)

    # Three tiers (monthly in USD)
    monthly_get_by = rent + essentials
    monthly_comfortable = monthly_get_by / 0.5  # 50/30/20 rule
    monthly_live_well = monthly_get_by / 0.4    # essentials = 40%

    def gross_from_net(annual_net):
        """Binary search for gross salary given desired net."""
        lo, hi = annual_net, annual_net * 3
        for _ in range(50):
            mid = (lo + hi) / 2
            tax = calc_tax(mid, country)
            ded = calc_deductions(mid, country, city_name)
            net = mid - tax - ded
            if net < annual_net:
                lo = mid
            else:
                hi = mid
        return round((lo + hi) / 2)

    # Annual net needed in local currency
    annual_get_by_local = usd_to_local(monthly_get_by * 12, currency)
    annual_comfortable_local = usd_to_local(monthly_comfortable * 12, currency)
    annual_live_well_local = usd_to_local(monthly_live_well * 12, currency)

    gross_get_by = gross_from_net(annual_get_by_local)
    gross_comfortable = gross_from_net(annual_comfortable_local)
    gross_live_well = gross_from_net(annual_live_well_local)

    # Effective tax rate
    tax_comf = calc_tax(gross_comfortable, country)
    ded_comf = calc_deductions(gross_comfortable, country, city_name)
    effective_tax_rate = f"{(tax_comf + ded_comf) / gross_comfortable * 100:.1f}" if gross_comfortable > 0 else "0.0"

    monthly_rent_local = usd_to_local(rent, currency)
    monthly_essentials_local = usd_to_local(essentials, currency)

    return {
        'currency': currency,
        'gross_get_by': gross_get_by,
        'gross_comfortable': gross_comfortable,
        'gross_live_well': gross_live_well,
        'monthly_rent_local': monthly_rent_local,
        'monthly_essentials_local': monthly_essentials_local,
        'effective_tax_rate': effective_tax_rate,
        'rent_usd': rent,
        'essentials_usd': essentials
    }


def generate_page(city_name, neighborhood_name=None, nb_multiplier=1.0):
    """Generate a full HTML page."""
    data = calc_salary_needed(city_name, nb_multiplier)
    if not data:
        return None

    is_nb = neighborhood_name is not None
    display_name = f"{neighborhood_name}, {city_name}" if is_nb else city_name
    title = f"What Salary Do You Need in {display_name}? (2026)"

    if is_nb:
        desc = f"Find out the minimum salary to live in {neighborhood_name}, {city_name} in 2026. From {format_currency(data['gross_get_by'], data['currency'])} to get by, to {format_currency(data['gross_comfortable'], data['currency'])} to live comfortably."
    else:
        desc = f"Find out the minimum salary to live in {city_name} in 2026. From {format_currency(data['gross_get_by'], data['currency'])} to get by, to {format_currency(data['gross_comfortable'], data['currency'])} to live comfortably. After-tax breakdown included."

    city_slug = to_slug(city_name)
    country = city_to_country.get(city_name, '')
    country_name = COUNTRY_NAMES.get(country, country)

    if is_nb:
        canonical = f"https://salary-converter.com/salary-needed/{city_slug}/{to_slug(neighborhood_name)}.html"
    else:
        canonical = f"https://salary-converter.com/salary-needed/{city_slug}.html"

    # Neighborhood comparison table (city pages only)
    neighborhood_section = ''
    if not is_nb and city_name in city_neighborhoods:
        nbs = city_neighborhoods[city_name]
        nb_entries = []
        for name, mult in nbs.items():
            nb_data = calc_salary_needed(city_name, mult)
            if nb_data:
                nb_entries.append((name, mult, nb_data))
        nb_entries.sort(key=lambda x: x[2]['gross_comfortable'], reverse=True)

        rows = '\n'.join(
            f'''<tr>
                <td><a href="/salary-needed/{city_slug}/{to_slug(name)}.html" style="color:var(--accent);text-decoration:none;font-weight:500;">{name}</a></td>
                <td style="text-align:right">{format_currency(d['gross_get_by'], d['currency'])}</td>
                <td style="text-align:right;font-weight:600">{format_currency(d['gross_comfortable'], d['currency'])}</td>
                <td style="text-align:right">{format_currency(d['gross_live_well'], d['currency'])}</td>
            </tr>'''
            for name, mult, d in nb_entries
        )

        neighborhood_section = f'''
        <section class="content-card">
            <h2>Salary Needed by Neighborhood</h2>
            <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:16px;">How much you need varies dramatically within {city_name}. Here's the breakdown for {len(nb_entries)} neighborhoods:</p>
            <div style="overflow-x:auto;">
            <table>
                <thead><tr>
                    <th>Neighborhood</th>
                    <th style="text-align:right">Get By</th>
                    <th style="text-align:right">Comfortable</th>
                    <th style="text-align:right">Live Well</th>
                </tr></thead>
                <tbody>{rows}</tbody>
            </table>
            </div>
        </section>'''

    # Related section (neighborhood pages only)
    related_section = ''
    if is_nb:
        related_section = f'''
        <section class="content-card">
            <h2>More in {city_name}</h2>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <a href="/salary-needed/{city_slug}.html" style="display:inline-block;padding:8px 16px;background:var(--accent,#2563eb);color:#fff;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:600;">All {city_name} neighborhoods</a>
                <a href="/city/{city_slug}/{to_slug(neighborhood_name)}.html" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:600;">Cost of living in {neighborhood_name}</a>
                <a href="/" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:600;">Salary Converter →</a>
            </div>
        </section>'''

    # FAQ Schema
    faq_items = [
        {
            'q': f"What salary do you need to live in {display_name}?",
            'a': f"To live comfortably in {display_name} in 2026, you need a gross annual salary of approximately {format_currency(data['gross_comfortable'], data['currency'])}. This covers rent, groceries, utilities, transport, healthcare, and leaves 30% for wants and 20% for savings (50/30/20 rule). The minimum to get by is {format_currency(data['gross_get_by'], data['currency'])}."
        },
        {
            'q': f"What is the cost of living in {display_name}?",
            'a': f"Monthly rent for a 1-bedroom apartment in {display_name} is approximately {format_currency(data['monthly_rent_local'], data['currency'])}. Essential monthly expenses (groceries, utilities, transport, healthcare) add roughly {format_currency(data['monthly_essentials_local'], data['currency'])}. The effective tax rate is {data['effective_tax_rate']}%."
        },
        {
            'q': f"Is {format_currency(data['gross_get_by'], data['currency'])} enough to live in {display_name}?",
            'a': f"{format_currency(data['gross_get_by'], data['currency'])} is the bare minimum salary to get by in {display_name} — it covers rent and essential expenses with very little left over. For a comfortable lifestyle with savings, you'd want at least {format_currency(data['gross_comfortable'], data['currency'])}."
        }
    ]

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item['q'],
                "acceptedAnswer": {"@type": "Answer", "text": item['a']}
            }
            for item in faq_items
        ]
    }, indent=8)

    if is_nb:
        breadcrumb_items = [
            {"pos": 1, "name": "Home", "item": "https://salary-converter.com"},
            {"pos": 2, "name": "Salary Needed", "item": "https://salary-converter.com/salary-needed/"},
            {"pos": 3, "name": city_name, "item": f"https://salary-converter.com/salary-needed/{city_slug}.html"},
            {"pos": 4, "name": neighborhood_name, "item": canonical}
        ]
    else:
        breadcrumb_items = [
            {"pos": 1, "name": "Home", "item": "https://salary-converter.com"},
            {"pos": 2, "name": "Salary Needed", "item": "https://salary-converter.com/salary-needed/"},
            {"pos": 3, "name": city_name, "item": canonical}
        ]

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i["pos"], "name": i["name"], "item": i["item"]}
            for i in breadcrumb_items
        ]
    }, indent=8)

    city_deduction_note = f" (including local taxes for {city_name})" if city_name in city_deduction_overrides else ""

    breadcrumb_html = f'<a href="/">Home</a> › <a href="/salary-needed/">Salary Needed</a>'
    if is_nb:
        breadcrumb_html += f' › <a href="/salary-needed/{city_slug}.html">{city_name}</a> › {neighborhood_name}'
    else:
        breadcrumb_html += f' › {city_name}'

    faq_html = '\n'.join(
        f'''            <div class="faq-item">
                <h3>{item['q']}</h3>
                <p>{item['a']}</p>
            </div>'''
        for item in faq_items
    )

    total_essentials = format_currency(data['monthly_rent_local'] + data['monthly_essentials_local'], data['currency'])

    # Build the city page footer link
    footer_city_link = f'<a href="/city/{city_slug}.html">{city_name} Cost of Living</a>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — salary:converter</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="salary needed {display_name}, minimum salary {display_name}, cost of living {display_name}, {display_name} salary 2026, what salary {city_name}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="manifest" href="/manifest.json">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:image:alt" content="Salary Converter - Compare cost of living and salaries between cities">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    {faq_schema}
    </script>
    <script type="application/ld+json">
    {breadcrumb_schema}
    </script>
    <style>
        :root {{
            --bg: #f5f5f7; --card-bg: #ffffff; --text-primary: #1d1d1f;
            --text-secondary: #86868b; --text-body: #4a4a4c; --accent: #2563eb;
            --accent-hover: #1d4ed8; --shadow: 0 2px 20px rgba(0,0,0,0.06);
            --border: #e5e5ea; --border-light: #f0f0f2; --stat-card-bg: #f5f5f7;
            --table-stripe: #f9f9fb;
        }}
        [data-theme="dark"] {{
            --bg: #000000; --card-bg: #1c1c1e; --text-primary: #f5f5f7;
            --text-secondary: #98989f; --text-body: #b0b0b5; --accent: #3b82f6;
            --accent-hover: #2563eb; --shadow: 0 2px 20px rgba(0,0,0,0.3);
            --border: #38383a; --border-light: #2c2c2e; --stat-card-bg: #2c2c2e;
            --table-stripe: #2c2c2e;
        }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif; background:var(--bg); color:var(--text-primary); min-height:100vh; }}
        .page-container {{ max-width:800px; margin:0 auto; padding:24px 20px 60px; }}
        .breadcrumb {{ font-size:0.8rem; color:var(--text-secondary); margin-bottom:24px; }}
        .breadcrumb a {{ color:var(--accent); text-decoration:none; }}
        h1 {{ font-size:2rem; font-weight:700; letter-spacing:-1px; line-height:1.2; margin-bottom:8px; }}
        .subtitle {{ font-size:0.95rem; color:var(--text-body); margin-bottom:32px; line-height:1.5; }}
        .salary-cards {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:32px; }}
        .salary-card {{ background:var(--card-bg); border-radius:16px; padding:24px 20px; box-shadow:var(--shadow); text-align:center; }}
        .salary-card.highlight {{ border:2px solid var(--accent); }}
        .salary-card-label {{ font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-secondary); margin-bottom:8px; }}
        .salary-card-amount {{ font-size:1.5rem; font-weight:700; color:var(--text-primary); margin-bottom:6px; }}
        .salary-card-note {{ font-size:0.75rem; color:var(--text-secondary); line-height:1.4; }}
        .content-card {{ background:var(--card-bg); border-radius:16px; padding:28px 24px; box-shadow:var(--shadow); margin-bottom:20px; }}
        .content-card h2 {{ font-size:1.15rem; font-weight:700; margin-bottom:16px; }}
        .content-card p {{ font-size:0.9rem; color:var(--text-body); line-height:1.6; margin-bottom:12px; }}
        table {{ width:100%; border-collapse:collapse; font-size:0.85rem; }}
        th {{ text-align:left; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-secondary); padding:10px 12px; border-bottom:2px solid var(--border); }}
        td {{ padding:10px 12px; border-bottom:1px solid var(--border-light); }}
        tr:nth-child(even) td {{ background:var(--table-stripe); }}
        .stat-row {{ display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border-light); font-size:0.9rem; }}
        .stat-label {{ color:var(--text-secondary); }}
        .stat-value {{ font-weight:600; }}
        .faq-item {{ margin-bottom:20px; }}
        .faq-item h3 {{ font-size:0.95rem; font-weight:600; margin-bottom:6px; }}
        .faq-item p {{ font-size:0.85rem; color:var(--text-body); line-height:1.5; }}
        .page-footer {{ margin-top:40px; padding-top:24px; border-top:1px solid var(--border-light); text-align:center; display:flex; justify-content:center; gap:20px; flex-wrap:wrap; }}
        .page-footer a {{ font-size:0.8rem; color:var(--text-secondary); text-decoration:none; font-weight:500; }}
        .page-footer a:hover {{ color:var(--accent); }}
        .theme-toggle {{
            position: fixed; top: 20px; right: 20px; z-index: 10001;
            display: inline-flex; align-items: center;
            width: 38px; height: 22px;
            background: var(--border); border: none; border-radius: 11px;
            cursor: pointer; padding: 0; transition: background 0.3s; flex-shrink: 0;
        }}
        .theme-toggle:hover {{ background: var(--text-secondary); }}
        .theme-toggle .toggle-thumb {{
            position: absolute; left: 2px; width: 18px; height: 18px;
            background: var(--card-bg); border-radius: 50%;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
        }}
        [data-theme="dark"] .theme-toggle {{ background: #3b82f6; }}
        [data-theme="dark"] .theme-toggle:hover {{ background: #60a5fa; }}
        [data-theme="dark"] .theme-toggle .toggle-thumb {{
            transform: translateX(16px);
            box-shadow: 0 0 0 2px #93c5fd, 0 1px 3px rgba(0,0,0,0.2);
        }}
        .theme-toggle .toggle-icon {{ width: 11px; height: 11px; }}
        .theme-toggle .icon-sun {{ color: #f59e0b; }}
        .theme-toggle .icon-moon {{ display: none; color: #3b82f6; }}
        [data-theme="dark"] .theme-toggle .icon-sun {{ display: none; }}
        [data-theme="dark"] .theme-toggle .icon-moon {{ display: block; color: #3b82f6; }}
        @media (max-width:600px) {{
            .salary-cards {{ grid-template-columns:1fr; }}
            h1 {{ font-size:1.5rem; }}
            .salary-card-amount {{ font-size:1.3rem; }}
        }}
    </style>
    <script>/* early-theme-detect */(function(){{var t=localStorage.getItem("theme");if(t){{document.documentElement.setAttribute("data-theme",t)}}else if(window.matchMedia("(prefers-color-scheme:dark)").matches){{document.documentElement.setAttribute("data-theme","dark")}}}})();</script>
</head>
<body>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" type="button">
        <span class="toggle-thumb">
            <svg class="toggle-icon icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
            <svg class="toggle-icon icon-moon" viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </span>
    </button>

    <div class="page-container">
        <div class="breadcrumb">
            {breadcrumb_html}
        </div>

        <h1>What Salary Do You Need to Live in {display_name}?</h1>
        <p class="subtitle">Based on 2026 cost of living data, here's how much you need to earn (before tax) in {display_name}, {country_name} — from bare minimum to living well.</p>

        <div class="salary-cards">
            <div class="salary-card">
                <div class="salary-card-label">Get By</div>
                <div class="salary-card-amount">{format_currency(data['gross_get_by'], data['currency'])}</div>
                <div class="salary-card-note">Covers rent & essentials. No savings, tight budget.</div>
            </div>
            <div class="salary-card highlight">
                <div class="salary-card-label">Comfortable</div>
                <div class="salary-card-amount">{format_currency(data['gross_comfortable'], data['currency'])}</div>
                <div class="salary-card-note">50/30/20 rule. Savings, dining out, some travel.</div>
            </div>
            <div class="salary-card">
                <div class="salary-card-label">Live Well</div>
                <div class="salary-card-amount">{format_currency(data['gross_live_well'], data['currency'])}</div>
                <div class="salary-card-note">Premium lifestyle with strong savings & flexibility.</div>
            </div>
        </div>

        <section class="content-card">
            <h2>Monthly Cost Breakdown</h2>
            <div class="stat-row"><span class="stat-label">Rent (1BR)</span><span class="stat-value">{format_currency(data['monthly_rent_local'], data['currency'])}/mo</span></div>
            <div class="stat-row"><span class="stat-label">Groceries + Utilities + Transport + Healthcare</span><span class="stat-value">{format_currency(data['monthly_essentials_local'], data['currency'])}/mo</span></div>
            <div class="stat-row"><span class="stat-label">Total essentials</span><span class="stat-value">{total_essentials}/mo</span></div>
            <div class="stat-row" style="border-bottom:none;"><span class="stat-label">Effective tax + deductions rate</span><span class="stat-value">{data['effective_tax_rate']}%</span></div>
        </section>

        <section class="content-card">
            <h2>How We Calculate This</h2>
            <p>We start with actual monthly costs in {display_name}: rent for a 1-bedroom apartment, groceries, utilities, transport, and healthcare. For the <strong>"comfortable"</strong> tier, we apply the 50/30/20 rule — your essentials should be 50% of take-home pay, leaving 30% for wants and 20% for savings.</p>
            <p>We then reverse-calculate the gross (pre-tax) salary you'd need, using {country_name}'s progressive tax brackets and mandatory deductions{city_deduction_note}. All figures are in {data['currency']} for 2026.</p>
        </section>

        {neighborhood_section}

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>

        {related_section}

        <section class="content-card" style="text-align:center;background:var(--accent);color:#fff;border:none;">
            <h2 style="color:#fff;">Compare Your Salary</h2>
            <p style="color:rgba(255,255,255,0.85);">See what your current salary is worth in {city_name} — or any other city.</p>
            <a href="/" style="display:inline-block;margin-top:8px;padding:12px 28px;background:#fff;color:var(--accent);border-radius:12px;text-decoration:none;font-weight:600;">Open Salary Converter →</a>
        </section>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            {footer_city_link}
            <a href="/salary-needed/">All Cities</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>

    <script>
    (function(){{
        var t=document.getElementById('themeToggle');
        function g(){{var s=localStorage.getItem('theme');if(s)return s;return matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'}}
        function a(m){{document.documentElement.setAttribute('data-theme',m);localStorage.setItem('theme',m);t.setAttribute('aria-label',m==='dark'?'Switch to light mode':'Switch to dark mode')}}
        a(g());
        t.addEventListener('click',function(){{a(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')}});
        matchMedia('(prefers-color-scheme:dark)').addEventListener('change',function(e){{if(!localStorage.getItem('theme'))a(e.matches?'dark':'light')}});
    }})();
    </script>
    <script src="/chat.js?v=2"></script>
</body>
</html>'''


# ============ GENERATE ALL PAGES ============

out_dir = os.path.join(BASE_DIR, 'salary-needed')
os.makedirs(out_dir, exist_ok=True)

city_count = 0
nb_count = 0
all_cities_data = []

for city_name in coli_data:
    city_slug = to_slug(city_name)

    # Generate city page
    city_html = generate_page(city_name)
    if city_html:
        with open(os.path.join(out_dir, f'{city_slug}.html'), 'w', encoding='utf-8') as f:
            f.write(city_html)
        city_count += 1

        # Save for index page
        d = calc_salary_needed(city_name)
        if d:
            all_cities_data.append((city_name, d))

    # Generate neighborhood pages
    neighborhoods = city_neighborhoods.get(city_name, {})
    if neighborhoods:
        nb_dir = os.path.join(out_dir, city_slug)
        os.makedirs(nb_dir, exist_ok=True)

        for nb_name, mult in neighborhoods.items():
            nb_slug = to_slug(nb_name)
            nb_html = generate_page(city_name, nb_name, mult)
            if nb_html:
                with open(os.path.join(nb_dir, f'{nb_slug}.html'), 'w', encoding='utf-8') as f:
                    f.write(nb_html)
                nb_count += 1

# Generate index page
all_cities_data.sort(key=lambda x: x[0])
city_links = '\n'.join(
    f'            <a href="/salary-needed/{to_slug(city)}.html" class="city-link">'
    f'<span class="city-name">{city}</span>'
    f'<span class="city-salary">{format_currency(d["gross_comfortable"], d["currency"])}</span></a>'
    for city, d in all_cities_data
)

index_page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>What Salary Do You Need? 2026 — Compare {city_count} Cities — salary:converter</title>
    <meta name="description" content="Find out the minimum salary to live comfortably in {city_count} cities worldwide. Neighborhood-level data for 2,000+ locations. Updated for 2026.">
    <meta name="keywords" content="salary needed, minimum salary, cost of living, salary by city, comfortable salary 2026">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/salary-needed/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="manifest" href="/manifest.json">
    <meta property="og:type" content="website">
    <meta property="og:title" content="What Salary Do You Need? 2026 — {city_count} Cities Compared">
    <meta property="og:description" content="Find the minimum salary to live comfortably in {city_count} cities. Neighborhood-level breakdown.">
    <meta property="og:url" content="https://salary-converter.com/salary-needed/">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:image:alt" content="Salary Converter - Compare cost of living and salaries between cities">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="What Salary Do You Need? {city_count} Cities Compared 2026">
    <meta name="twitter:description" content="Minimum salary to live comfortably in {city_count} cities. With neighborhood-level data.">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Salary Needed by City 2026",
        "description": "Find out the salary you need in {city_count} cities worldwide",
        "url": "https://salary-converter.com/salary-needed/"
    }}
    </script>
    <style>
        :root {{ --bg:#f5f5f7;--card-bg:#fff;--text-primary:#1d1d1f;--text-secondary:#86868b;--text-body:#4a4a4c;--accent:#2563eb;--shadow:0 2px 20px rgba(0,0,0,0.06);--border:#e5e5ea;--border-light:#f0f0f2; }}
        [data-theme="dark"] {{ --bg:#000;--card-bg:#1c1c1e;--text-primary:#f5f5f7;--text-secondary:#98989f;--text-body:#b0b0b5;--accent:#3b82f6;--shadow:0 2px 20px rgba(0,0,0,0.3);--border:#38383a;--border-light:#2c2c2e; }}
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text-primary);min-height:100vh}}
        .page{{max-width:900px;margin:0 auto;padding:32px 20px 60px}}
        h1{{font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:8px}}
        .subtitle{{font-size:0.95rem;color:var(--text-body);margin-bottom:32px;line-height:1.5}}
        .city-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}}
        .city-link{{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:var(--card-bg);border-radius:12px;box-shadow:var(--shadow);text-decoration:none;color:var(--text-primary);transition:all 0.2s}}
        .city-link:hover{{border-color:var(--accent);transform:translateY(-1px)}}
        .city-name{{font-weight:600;font-size:0.9rem}}
        .city-salary{{font-size:0.85rem;color:var(--accent);font-weight:600}}
        .page-footer{{margin-top:40px;padding-top:24px;border-top:1px solid var(--border-light);text-align:center;display:flex;justify-content:center;gap:20px;flex-wrap:wrap}}
        .page-footer a{{font-size:0.8rem;color:var(--text-secondary);text-decoration:none;font-weight:500}}
        .page-footer a:hover{{color:var(--accent)}}
    </style>
    <script>/* early-theme-detect */(function(){{var t=localStorage.getItem("theme");if(t){{document.documentElement.setAttribute("data-theme",t)}}else if(window.matchMedia("(prefers-color-scheme:dark)").matches){{document.documentElement.setAttribute("data-theme","dark")}}}})();</script>
</head>
<body>
    <div class="page">
        <h1>What Salary Do You Need? (2026)</h1>
        <p class="subtitle">Find the minimum salary to live comfortably in {city_count} cities worldwide — with neighborhood-level breakdowns for 2,000+ locations.</p>
        <div class="city-grid">
{city_links}
        </div>
        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/">All Cities</a>
            <a href="/compare/">City Comparisons</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
    <script>
    (function(){{
        var t=localStorage.getItem('theme');
        if(!t)t=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
        document.documentElement.setAttribute('data-theme',t);
    }})();
    </script>
    <script src="/chat.js?v=2"></script>
</body>
</html>'''

with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_page)

print(f"\nGenerated: {city_count} city pages + {nb_count} neighborhood pages + 1 index page")
print(f"Total: {city_count + nb_count + 1} pages in /salary-needed/")
