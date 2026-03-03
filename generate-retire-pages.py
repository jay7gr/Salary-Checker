#!/usr/bin/env python3
"""
Generates Retire Abroad SEO pages:
  /retire/city/{slug}.html        — 182 city retirement guides
  /retire/country/{slug}.html     — ~55 country guides
  /retire/visa/{slug}.html        — ~45 visa guides
  /retire/budget/{slug}.html      — 12 budget pages
  /retire/compare/{a}-vs-{b}.html — ~150 comparison pages
  /retire/destinations/index.html — browse all destinations

Reads data from retire/index.html via regex (same pattern as generate-salary-needed.py).
"""

import os, re, json, math, html as html_mod

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Google Analytics + AdSense ──────────────────────────────────────
GA4_SNIPPET = '''
    <!-- Google Consent Mode v2 -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('consent', 'default', {
            'ad_storage': 'denied',
            'ad_user_data': 'denied',
            'ad_personalization': 'denied',
            'analytics_storage': 'granted',
            'wait_for_update': 500,
            'regions': ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH','BR','CA']
        });
        gtag('consent', 'default', {
            'ad_storage': 'granted',
            'ad_user_data': 'granted',
            'ad_personalization': 'granted',
            'analytics_storage': 'granted'
        });
    </script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-MMZSM2Z96B"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-MMZSM2Z96B');
    </script>
    <!-- Google AdSense Auto Ads -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4472082543745200" crossorigin="anonymous"></script>'''

WISE_LINK = 'https://wise.com/invite/drhc/iason-georgiosi'

# ── Read retire/index.html ──────────────────────────────────────────
with open(os.path.join(BASE_DIR, 'retire', 'index.html'), 'r', encoding='utf-8') as f:
    index_html = f.read()

# ── JS → JSON parser (from generate-salary-needed.py) ──────────────
def js_to_json(raw):
    raw = re.sub(r'//[^\n]*', '', raw)
    tokens = []
    i = 0
    while i < len(raw):
        c = raw[i]
        if c == "'":
            j = i + 1
            content_chars = []
            while j < len(raw) and raw[j] != "'":
                if raw[j] == '\\' and j + 1 < len(raw):
                    next_c = raw[j + 1]
                    if next_c == "'":
                        content_chars.append("'")
                        j += 2
                    elif next_c == '"':
                        content_chars.append('\\"')
                        j += 2
                    elif next_c == '\\':
                        content_chars.append('\\\\')
                        j += 2
                    else:
                        content_chars.append(raw[j:j+2])
                        j += 2
                else:
                    if raw[j] == '"':
                        content_chars.append('\\"')
                    else:
                        content_chars.append(raw[j])
                    j += 1
            j += 1
            tokens.append('"' + ''.join(content_chars) + '"')
            i = j
        elif c == '"':
            j = i + 1
            while j < len(raw) and raw[j] != '"':
                if raw[j] == '\\':
                    j += 2
                else:
                    j += 1
            j += 1
            tokens.append(raw[i:j])
            i = j
        else:
            tokens.append(c)
            i += 1
    raw = ''.join(tokens)
    raw = raw.replace('Infinity', '999999999')
    raw = re.sub(r',\s*}', '}', raw)
    raw = re.sub(r',\s*]', ']', raw)

    # Quote unquoted keys — but ONLY outside of strings
    # Split by double-quoted strings, process non-string parts only
    parts = re.split(r'("(?:[^"\\]|\\.)*")', raw)
    for i in range(0, len(parts), 2):  # Even indices are outside strings
        parts[i] = re.sub(r'(?<=[{,\s\[])([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', parts[i])
    raw = ''.join(parts)

    return raw


def extract_object(var_name):
    pattern = rf"const {var_name}\s*=\s*\{{([\s\S]*?)\}};"
    match = re.search(pattern, index_html)
    if not match:
        print(f"  Could not find {var_name}")
        return {}
    raw = '{' + match.group(1) + '}'
    raw = js_to_json(raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  Failed to parse {var_name}: {e}")
        return {}


def extract_nested_object(var_name):
    pattern = rf"const {var_name}\s*=\s*\{{"
    match = re.search(pattern, index_html)
    if not match:
        print(f"  Could not find {var_name}")
        return {}
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
        print(f"  Failed to parse {var_name}: {e}")
        return {}


def extract_array(var_name):
    """Extract a JS array (like visaPrograms)."""
    pattern = rf"const {var_name}\s*=\s*\["
    match = re.search(pattern, index_html)
    if not match:
        print(f"  Could not find {var_name}")
        return []
    bracket_start = index_html.index('[', match.start())
    depth = 0
    i = bracket_start
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
            if c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    break
        i += 1
    raw = index_html[bracket_start:i+1]
    raw = js_to_json(raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  Failed to parse {var_name}: {e}")
        return []


# ── Extract all data ────────────────────────────────────────────────
print("Extracting data from retire/index.html...")
coli_data = extract_object('coliData')
city_rent = extract_object('cityRent1BR')
city_to_country = extract_object('cityToCountry')
city_to_currency = extract_object('cityToCurrency')
exchange_rates = extract_object('exchangeRates')
city_living_costs = extract_nested_object('cityLivingCosts')
safety_index = extract_object('retireSafetyIndex')
healthcare_index = extract_object('retireHealthcareIndex')
climate_score = extract_object('retireClimateScore')
english_score = extract_object('retireEnglishScore')
expat_community = extract_object('retireExpatCommunity')
charm_score = extract_object('retireCityCharmScore')
inheritance_tax = extract_nested_object('retireInheritanceTax')
country_data = extract_nested_object('retireCountryData')
lifestyle_map = extract_nested_object('cityLifestyleMap')
visa_programs = extract_array('visaPrograms')

print(f"Loaded: {len(coli_data)} cities, {len(visa_programs)} visa programs, {len(country_data)} countries")

if len(coli_data) == 0:
    print("ERROR: No data loaded. Exiting.")
    exit(1)

# ── Constants ───────────────────────────────────────────────────────
CURRENCY_SYMBOLS = {
    'USD':'$','GBP':'£','EUR':'€','JPY':'¥','CNY':'¥','CHF':'CHF ','AUD':'A$','CAD':'C$',
    'SGD':'S$','HKD':'HK$','NZD':'NZ$','SEK':'kr ','NOK':'kr ','DKK':'kr ','CZK':'Kč ',
    'HUF':'Ft ','PLN':'zł ','TRY':'₺','BRL':'R$','MXN':'MX$','ZAR':'R ','KRW':'₩',
    'TWD':'NT$','IDR':'Rp ','VND':'₫','PHP':'₱','ILS':'₪','EGP':'E£','KES':'KSh ',
    'NGN':'₦','MAD':'MAD ','ARS':'AR$','COP':'CO$','PEN':'S/','CLP':'CL$','UYU':'$U ',
    'CRC':'₡','QAR':'QR ','SAR':'SR ','PAB':'B/','RON':'lei ','AED':'AED ','INR':'₹',
    'MYR':'RM ','THB':'฿','LKR':'Rs ','KHR':'៛','GEL':'₾','ALL':'L ','BAM':'KM ',
    'RSD':'din ','BGN':'лв ','HRK':'kn ','MKD':'ден ','MDL':'L ','JOD':'JD ','OMR':'OMR ',
    'BHD':'BD ','KWD':'KD ','TND':'DT ','MUR':'₨','GHS':'₵','TZS':'TSh ','UGX':'USh '
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
    'BR':'Brazil','AR':'Argentina','CO':'Colombia','PE':'Peru','CL':'Chile','UY':'Uruguay',
    'CR':'Costa Rica','CY':'Cyprus','MT':'Malta','SI':'Slovenia','LT':'Lithuania','ME':'Montenegro',
    'RS':'Serbia','BA':'Bosnia and Herzegovina','AL':'Albania','MK':'North Macedonia','MD':'Moldova',
    'GE':'Georgia','JO':'Jordan','OM':'Oman','BH':'Bahrain','KW':'Kuwait','TN':'Tunisia',
    'MU':'Mauritius','GH':'Ghana','TZ':'Tanzania','UG':'Uganda','LK':'Sri Lanka','EC':'Ecuador',
    'BG':'Bulgaria'
}

# Share bar SVG icons
SHARE_ICON_X = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" fill="currentColor"/></svg>'
SHARE_ICON_LI = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/></svg>'
SHARE_ICON_WA = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" fill="currentColor"/></svg>'
SHARE_ICON_COPY = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SHARE_ICON_EMAIL = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="22,6 12,13 2,6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


# ── Helpers ─────────────────────────────────────────────────────────
def to_slug(name):
    slug = re.sub(r'\s*\(.*?\)\s*', '', name)
    slug = re.sub(r'[^a-z0-9]+', '-', slug.lower())
    return slug.strip('-')

def fmt_usd(amount):
    r = round(amount)
    if r >= 1000000:
        return f"${r/1000000:.1f}M"
    return f"${r:,}"

def fmt_currency(amount, currency):
    sym = CURRENCY_SYMBOLS.get(currency, currency + ' ')
    r = round(amount)
    if r >= 1000000:
        return f"{sym}{r/1000000:.1f}M"
    return f"{sym}{r:,}"

def get_country_name(country_code):
    return COUNTRY_NAMES.get(country_code, country_code)

def get_monthly_cost(city, household='single'):
    """Get monthly cost in USD for a city."""
    costs = city_living_costs.get(city, {})
    rent = city_rent.get(city, 800)
    groceries = costs.get('groceries', 350)
    utilities = costs.get('utilities', 200)
    transport = costs.get('transport', 100)
    healthcare = costs.get('healthcare', 300)
    if household == 'couple':
        rent = round(rent * 1.4)
        groceries = round(groceries * 1.5)
        utilities = round(utilities * 1.3)
        transport = round(transport * 2)
        healthcare = round(healthcare * 1.7)
    return {
        'rent': rent, 'groceries': groceries, 'utilities': utilities,
        'transport': transport, 'healthcare': healthcare,
        'total': rent + groceries + utilities + transport + healthcare
    }

def years_money_lasts(savings, city, household='single'):
    """How many years savings will last in a city."""
    monthly = get_monthly_cost(city, household)['total']
    if monthly <= 0:
        return 99
    return round(savings / (monthly * 12), 1)

def get_visa_programs_for_country(country_code):
    """Filter visa programs for a specific country."""
    return [v for v in visa_programs if v.get('country') == country_code]

def get_rank(city, data_dict, reverse=True):
    """Get ranking of a city in a score dictionary (1 = best)."""
    if city not in data_dict:
        return '-'
    sorted_cities = sorted(data_dict.keys(), key=lambda c: data_dict[c], reverse=reverse)
    try:
        return sorted_cities.index(city) + 1
    except ValueError:
        return '-'

def lifestyle_tags_html(city):
    """Get lifestyle tags as HTML badges."""
    tags = lifestyle_map.get(city, ['major_city'])
    if isinstance(tags, str):
        tags = [tags]
    icons = {'major_city': '🏙️ Big City', 'smaller_city': '🏘️ Small Town',
             'beach': '🏖️ Beach/Coastal', 'mountain': '🏔️ Mountain/Nature'}
    return ' '.join(f'<span class="lifestyle-tag">{icons.get(t, t)}</span>' for t in tags)

def expat_badge(city):
    size = expat_community.get(city, 'medium')
    if isinstance(size, (int, float)):
        if size >= 70: size = 'large'
        elif size >= 40: size = 'medium'
        else: size = 'small'
    icons = {'large': '🌍 Large Expat Community', 'medium': '🌐 Medium Expat Community', 'small': '👥 Small Expat Community'}
    return icons.get(size, '🌐 Expat Community')

def inheritance_tax_text(country_name):
    tax = inheritance_tax.get(country_name)
    if not tax or tax == 0:
        return 'None'
    if isinstance(tax, dict):
        rate = tax.get('rate', 0)
        if rate == 0:
            return 'None'
        threshold = tax.get('threshold', 0)
        currency = tax.get('currency', 'USD')
        note = tax.get('note', '')
        if threshold > 0:
            return f"{rate}% above {fmt_currency(threshold, currency)}"
        return f"{rate}%"
    return 'None'


# ── Shared HTML components ──────────────────────────────────────────
def build_share_bar(share_text, share_url):
    t = html_mod.escape(share_text, quote=True)
    u = html_mod.escape(share_url, quote=True)
    return f'''<div class="share-bar" data-share-text="{t}" data-share-url="{u}">
            <span class="share-bar-label">Share</span>
            <button class="share-btn" data-platform="twitter" aria-label="Share on X" type="button">{SHARE_ICON_X}</button>
            <button class="share-btn" data-platform="linkedin" aria-label="Share on LinkedIn" type="button">{SHARE_ICON_LI}</button>
            <button class="share-btn" data-platform="whatsapp" aria-label="Share on WhatsApp" type="button">{SHARE_ICON_WA}</button>
            <button class="share-btn" data-platform="copy" aria-label="Copy link" type="button">{SHARE_ICON_COPY}</button>
            <button class="share-btn" data-platform="email" aria-label="Share via email" type="button">{SHARE_ICON_EMAIL}</button>
        </div>'''

DATA_SOURCES_HTML = '''
        <section class="content-card">
            <h2>Data Sources &amp; Methodology</h2>
            <p>Our retirement data is compiled from multiple authoritative sources, cross-referenced for accuracy:</p>
            <ul class="sources-list">
                <li><strong>Cost of Living:</strong> <a href="https://www.numbeo.com/cost-of-living/" target="_blank" rel="noopener">Numbeo Cost of Living Index</a> — crowdsourced consumer prices, updated monthly</li>
                <li><strong>Healthcare:</strong> <a href="https://www.who.int/data" target="_blank" rel="noopener">WHO Global Health Observatory</a>, <a href="https://www.numbeo.com/health-care/" target="_blank" rel="noopener">Numbeo Healthcare Index</a></li>
                <li><strong>Safety:</strong> <a href="https://www.numbeo.com/crime/" target="_blank" rel="noopener">Numbeo Crime Index</a>, <a href="https://worldpopulationreview.com/country-rankings/safest-countries-in-the-world" target="_blank" rel="noopener">Global Peace Index</a></li>
                <li><strong>Climate:</strong> <a href="https://www.weatherbase.com" target="_blank" rel="noopener">Weatherbase</a>, <a href="https://www.climate-data.org" target="_blank" rel="noopener">Climate-Data.org</a></li>
                <li><strong>Visa Programs:</strong> Official government immigration websites for each country</li>
                <li><strong>Tax Data:</strong> <a href="https://www.oecd.org/tax/" target="_blank" rel="noopener">OECD Tax Database</a>, <a href="https://taxfoundation.org" target="_blank" rel="noopener">Tax Foundation</a>, national tax authority websites</li>
                <li><strong>Expat Community:</strong> <a href="https://www.internations.org" target="_blank" rel="noopener">InterNations Expat Insider Survey</a></li>
                <li><strong>English Proficiency:</strong> <a href="https://www.ef.com/epi/" target="_blank" rel="noopener">EF English Proficiency Index</a></li>
            </ul>
            <p style="font-size:0.8rem;color:var(--text-secondary);margin-top:12px;">All data is for informational purposes only and updated periodically. Individual circumstances may vary. Consult a qualified financial advisor for personal retirement planning. Last updated: March 2026.</p>
        </section>'''

WISE_CTA_HTML = f'''
        <section class="content-card wise-cta" style="border: 1px solid #9fe870; border-left: 4px solid #9fe870; background: var(--card-bg);">
            <div style="display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap;">
                <div style="flex:1; min-width:200px;">
                    <p style="font-size:0.65rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin:0 0 6px;">Sponsored</p>
                    <h3 style="font-size:1rem; font-weight:600; margin:0 0 6px; color:var(--text-primary);">Moving money abroad?</h3>
                    <p style="font-size:0.85rem; color:var(--text-body); line-height:1.5; margin:0 0 12px;">Send your pension or savings internationally at the real exchange rate. Save up to 6x vs traditional banks.</p>
                    <a href="{WISE_LINK}" rel="noopener noreferrer sponsored" target="_blank"
                       style="display:inline-block; padding:10px 24px; background:#9fe870; color:#1a1a1a; border-radius:100px; font-weight:600; font-size:0.85rem; text-decoration:none;">
                        Try Wise for Free &rarr;
                    </a>
                </div>
            </div>
        </section>'''

RETIRE_CTA_HTML = '''
        <section class="content-card" style="text-align:center;background:var(--accent);color:#fff;border:none;">
            <h2 style="color:#fff;">Plan Your Retirement</h2>
            <p style="color:rgba(255,255,255,0.85);">Enter your savings, income, and preferences to find your ideal retirement destination.</p>
            <a href="/retire/" style="display:inline-block;margin-top:8px;padding:12px 28px;background:#fff;color:var(--accent);border-radius:12px;text-decoration:none;font-weight:600;">Try the Retire Abroad Calculator &rarr;</a>
        </section>'''

SALARY_CTA_HTML = '''
        <section class="content-card" style="text-align:center;background:var(--stat-card-bg);border:1px solid var(--border);">
            <h2>What Salary Do You Need?</h2>
            <p style="color:var(--text-body);">Compare salaries across 100+ cities with neighborhood-level data.</p>
            <a href="/" style="display:inline-block;margin-top:8px;padding:12px 28px;background:var(--accent);color:#fff;border-radius:12px;text-decoration:none;font-weight:600;">Open Salary Converter &rarr;</a>
        </section>'''

def build_footer():
    return '''
        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/retire/">Retire Abroad</a>
            <a href="/retire/destinations/">All Destinations</a>
            <a href="/salary-needed/">Salary Needed</a>
            <a href="/blog/">Blog</a>
            <a href="/privacy/">Privacy</a>
            <a href="/about/">About</a>
            <a href="/terms/">Terms</a>
        </footer>'''


# ── CSS (shared across all pages) ──────────────────────────────────
PAGE_CSS = '''
        :root {
            --bg: #f5f5f7; --card-bg: #ffffff; --text-primary: #1d1d1f;
            --text-secondary: #86868b; --text-body: #4a4a4c; --accent: #2563eb;
            --accent-hover: #1d4ed8; --shadow: 0 2px 20px rgba(0,0,0,0.06);
            --border: #e5e5ea; --border-light: #f0f0f2; --stat-card-bg: #f5f5f7;
            --table-stripe: #f9f9fb;
        }
        [data-theme="dark"] {
            --bg: #000000; --card-bg: #1c1c1e; --text-primary: #f5f5f7;
            --text-secondary: #98989f; --text-body: #b0b0b5; --accent: #3b82f6;
            --accent-hover: #2563eb; --shadow: 0 2px 20px rgba(0,0,0,0.3);
            --border: #38383a; --border-light: #2c2c2e; --stat-card-bg: #2c2c2e;
            --table-stripe: #2c2c2e;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        html, body { overflow-x: hidden; }
        html { touch-action: manipulation; }
        body { font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif; background:var(--bg); color:var(--text-primary); min-height:100vh; }
        .page-container { max-width:800px; margin:0 auto; padding:24px 20px 60px; }
        .breadcrumb { font-size:0.8rem; color:var(--text-secondary); margin-bottom:24px; }
        .breadcrumb a { color:var(--accent); text-decoration:none; }
        h1 { font-size:2rem; font-weight:700; letter-spacing:-1px; line-height:1.2; margin-bottom:8px; }
        .subtitle { font-size:0.95rem; color:var(--text-body); margin-bottom:32px; line-height:1.5; }
        .stat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px; }
        .stat-box { background:var(--card-bg); border-radius:12px; padding:16px; text-align:center; box-shadow:var(--shadow); }
        .stat-box-value { font-size:1.3rem; font-weight:700; color:var(--text-primary); }
        .stat-box-label { font-size:0.7rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.3px; margin-top:4px; }
        .content-card { background:var(--card-bg); border-radius:16px; padding:28px 24px; box-shadow:var(--shadow); margin-bottom:20px; }
        .content-card h2 { font-size:1.15rem; font-weight:700; margin-bottom:16px; }
        .content-card h3 { font-size:1rem; font-weight:600; margin:16px 0 8px; }
        .content-card p { font-size:0.9rem; color:var(--text-body); line-height:1.6; margin-bottom:12px; }
        .content-card ul, .content-card ol { font-size:0.9rem; color:var(--text-body); line-height:1.6; margin:0 0 12px 20px; }
        .content-card li { margin-bottom:6px; }
        .content-card a { color:var(--accent); text-decoration:none; }
        .content-card a:hover { text-decoration:underline; }
        .sources-list { font-size:0.82rem; }
        .sources-list li { margin-bottom:8px; }
        table { width:100%; border-collapse:collapse; font-size:0.85rem; }
        th { text-align:left; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-secondary); padding:10px 12px; border-bottom:2px solid var(--border); }
        td { padding:10px 12px; border-bottom:1px solid var(--border-light); }
        tr:nth-child(even) td { background:var(--table-stripe); }
        .stat-row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border-light); font-size:0.9rem; }
        .stat-label { color:var(--text-secondary); }
        .stat-value { font-weight:600; }
        .faq-item { margin-bottom:20px; }
        .faq-item h3 { font-size:0.95rem; font-weight:600; margin-bottom:6px; }
        .faq-item p { font-size:0.85rem; color:var(--text-body); line-height:1.5; }
        .lifestyle-tag { display:inline-block; padding:4px 10px; background:var(--stat-card-bg); border-radius:8px; font-size:0.8rem; margin:2px 4px 2px 0; }
        .winner-badge { display:inline-block; background:#22c55e; color:#fff; font-size:0.65rem; font-weight:700; padding:2px 6px; border-radius:4px; margin-left:6px; }
        .page-footer { margin-top:40px; padding-top:24px; border-top:1px solid var(--border-light); text-align:center; display:flex; justify-content:center; gap:20px; flex-wrap:wrap; }
        .page-footer a { font-size:0.8rem; color:var(--text-secondary); text-decoration:none; font-weight:500; }
        .page-footer a:hover { color:var(--accent); }
        .theme-toggle {
            position: fixed; top: 20px; right: 20px; z-index: 10001;
            display: inline-flex; align-items: center;
            width: 38px; height: 22px;
            background: var(--border); border: none; border-radius: 11px;
            cursor: pointer; padding: 0; transition: background 0.3s; flex-shrink: 0;
        }
        .theme-toggle:hover { background: var(--text-secondary); }
        .theme-toggle .toggle-thumb {
            position: absolute; left: 2px; width: 18px; height: 18px;
            background: var(--card-bg); border-radius: 50%;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
        }
        [data-theme="dark"] .theme-toggle { background: #3b82f6; }
        [data-theme="dark"] .theme-toggle:hover { background: #60a5fa; }
        [data-theme="dark"] .theme-toggle .toggle-thumb {
            transform: translateX(16px);
            box-shadow: 0 0 0 2px #93c5fd, 0 1px 3px rgba(0,0,0,0.2);
        }
        .theme-toggle .toggle-icon { width: 11px; height: 11px; }
        .theme-toggle .icon-sun { color: #f59e0b; }
        .theme-toggle .icon-moon { display: none; color: #3b82f6; }
        [data-theme="dark"] .theme-toggle .icon-sun { display: none; }
        [data-theme="dark"] .theme-toggle .icon-moon { display: block; color: #3b82f6; }
        .visa-card { background:var(--stat-card-bg); border-radius:12px; padding:16px; margin-bottom:12px; }
        .visa-card-name { font-weight:600; font-size:0.95rem; margin-bottom:8px; }
        .visa-detail { display:flex; justify-content:space-between; font-size:0.82rem; padding:4px 0; }
        .visa-detail-label { color:var(--text-secondary); }
        .visa-detail-value { font-weight:500; }
        .city-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:12px; }
        .city-link { display:flex; justify-content:space-between; align-items:center; padding:14px 18px; background:var(--card-bg); border-radius:12px; box-shadow:var(--shadow); text-decoration:none; color:var(--text-primary); transition:all 0.2s; }
        .city-link:hover { border-color:var(--accent); transform:translateY(-1px); }
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
        .share-btn.copied { color: #22c55e; border-color: #22c55e; }
        @media (max-width:768px) {
            .stat-grid { grid-template-columns: repeat(2,1fr); }
            h1 { font-size: 1.5rem; }
            .content-card { padding: 20px 16px; }
            .city-grid { grid-template-columns: 1fr; }
        }'''

THEME_JS = '''
    <script>(function(){var t=localStorage.getItem("theme");if(t){document.documentElement.setAttribute("data-theme",t)}else if(window.matchMedia("(prefers-color-scheme:dark)").matches){document.documentElement.setAttribute("data-theme","dark")}})();</script>'''

FOOTER_JS = '''
    <script>
    (function(){
        var t=document.getElementById('themeToggle');
        function g(){var s=localStorage.getItem('theme');if(s)return s;return matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'}
        function a(m){document.documentElement.setAttribute('data-theme',m);localStorage.setItem('theme',m);t.setAttribute('aria-label',m==='dark'?'Switch to light mode':'Switch to dark mode')}
        a(g());
        t.addEventListener('click',function(){a(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')});
        matchMedia('(prefers-color-scheme:dark)').addEventListener('change',function(e){if(!localStorage.getItem('theme'))a(e.matches?'dark':'light')});
    })();
    </script>
    <script>
    (function(){
        document.querySelectorAll('.share-bar').forEach(function(bar){
            var text=bar.getAttribute('data-share-text'),url=bar.getAttribute('data-share-url');
            bar.querySelectorAll('.share-btn').forEach(function(btn){
                btn.addEventListener('click',function(){
                    var p=btn.getAttribute('data-platform'),enc=encodeURIComponent(text+'\\n'+url);
                    if(p==='twitter')window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(text)+'&url='+encodeURIComponent(url),'_blank','width=550,height=420');
                    else if(p==='linkedin')window.open('https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(url),'_blank','width=550,height=420');
                    else if(p==='whatsapp')window.open('https://wa.me/?text='+enc,'_blank');
                    else if(p==='email')window.location.href='mailto:?subject='+encodeURIComponent(text)+'&body='+enc;
                    else if(p==='copy'){navigator.clipboard.writeText(url).then(function(){btn.classList.add('copied');setTimeout(function(){btn.classList.remove('copied')},2000)})}
                });
            });
        });
    })();
    </script>
    <script src="/chat.js?v=2"></script>'''

THEME_TOGGLE_HTML = '''
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" type="button">
        <span class="toggle-thumb">
            <svg class="toggle-icon icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
            <svg class="toggle-icon icon-moon" viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </span>
    </button>'''


# ═══════════════════════════════════════════════════════════════════
#  PAGE TYPE A: /retire/city/{slug}.html
# ═══════════════════════════════════════════════════════════════════
def generate_city_page(city):
    cc = city_to_country.get(city, '')
    country_name = get_country_name(cc)
    slug = to_slug(city)
    canonical = f"https://salary-converter.com/retire/city/{slug}"
    cd = country_data.get(country_name, {})
    region = cd.get('region', '')

    # Costs
    single_cost = get_monthly_cost(city, 'single')
    couple_cost = get_monthly_cost(city, 'couple')

    # Scores
    safety = safety_index.get(city, 50)
    healthcare = healthcare_index.get(city, 50)
    climate = climate_score.get(city, 50)
    english = english_score.get(city, 50)
    charm = charm_score.get(city, 50)

    # Rankings
    safety_rank = get_rank(city, safety_index)
    healthcare_rank = get_rank(city, healthcare_index)
    climate_rank = get_rank(city, climate_score)
    total_cities = len(coli_data)

    # Savings scenarios
    savings_scenarios = [200000, 300000, 500000, 750000, 1000000]
    savings_rows = '\n'.join(
        f'<tr><td>{fmt_usd(s)}</td><td>{years_money_lasts(s, city, "single")} yrs</td><td>{years_money_lasts(s, city, "couple")} yrs</td></tr>'
        for s in savings_scenarios
    )

    # Visa programs
    visas = get_visa_programs_for_country(cc)
    visa_html = ''
    if visas:
        visa_cards = ''
        for v in visas:
            income_req = fmt_usd(v['minMonthlyIncome']) + '/mo' if v.get('minMonthlyIncome') else 'N/A'
            savings_req = fmt_usd(v['minSavings']) if v.get('minSavings') else 'N/A'
            pr_path = 'Yes' if v.get('pathToPR') else 'No'
            cit_years = f"{v['citizenshipYears']} years" if v.get('citizenshipYears') else 'N/A'
            visa_cards += f'''
                <div class="visa-card">
                    <div class="visa-card-name">{v.get('name', 'Visa Program')}</div>
                    <div class="visa-detail"><span class="visa-detail-label">Type</span><span class="visa-detail-value">{v.get('type', 'N/A').replace('_', ' ').title()}</span></div>
                    <div class="visa-detail"><span class="visa-detail-label">Min. Monthly Income</span><span class="visa-detail-value">{income_req}</span></div>
                    <div class="visa-detail"><span class="visa-detail-label">Min. Savings</span><span class="visa-detail-value">{savings_req}</span></div>
                    <div class="visa-detail"><span class="visa-detail-label">Path to PR</span><span class="visa-detail-value">{pr_path}</span></div>
                    <div class="visa-detail"><span class="visa-detail-label">Citizenship Timeline</span><span class="visa-detail-value">{cit_years}</span></div>
                    {"<div class='visa-detail'><span class='visa-detail-label'>Health Insurance</span><span class='visa-detail-value'>Required</span></div>" if v.get('healthInsuranceRequired') else ""}
                    <p style="font-size:0.78rem;color:var(--text-secondary);margin:8px 0 0;">{v.get('notes', '')}</p>
                </div>'''
        visa_html = f'''
        <section class="content-card">
            <h2>🛂 Visa &amp; Residency Options in {country_name}</h2>
            <p>Here are the visa programs available for retiring in {country_name}:</p>
            {visa_cards}
            <p style="font-size:0.8rem;color:var(--text-secondary);margin-top:8px;"><a href="/retire/visa/{to_slug(country_name)}">Full {country_name} visa guide &rarr;</a></p>
        </section>'''

    # Tax overview
    inh_tax = inheritance_tax_text(country_name)
    cap_gains = cd.get('capitalGainsTax', 'N/A')
    div_tax = cd.get('dividendTax', 'N/A')
    wealth_tax_data = cd.get('wealthTax')
    wealth_tax_str = 'None'
    if wealth_tax_data and isinstance(wealth_tax_data, dict) and wealth_tax_data.get('rate'):
        wealth_tax_str = f"{wealth_tax_data['rate']}%"
    health_ins = cd.get('healthInsurance60Plus', 'N/A')
    health_ins_str = fmt_usd(health_ins) + '/mo' if isinstance(health_ins, (int, float)) else str(health_ins)

    # Related cities in same country
    same_country_cities = [c for c in coli_data if city_to_country.get(c) == cc and c != city]
    related_links = ''
    if same_country_cities:
        related_links = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;">'
        for rc in same_country_cities[:8]:
            related_links += f'<a href="/retire/city/{to_slug(rc)}" style="display:inline-block;padding:6px 14px;background:var(--stat-card-bg);border-radius:8px;font-size:0.82rem;text-decoration:none;color:var(--text-primary);">{rc}</a>'
        related_links += '</div>'

    # FAQ
    faq_items = [
        {'q': f'How much does it cost to retire in {city}?',
         'a': f'A single retiree needs approximately {fmt_usd(single_cost["total"])}/month in {city}, covering rent ({fmt_usd(single_cost["rent"])}), groceries, utilities, transport, and healthcare. A couple needs about {fmt_usd(couple_cost["total"])}/month.'},
        {'q': f'Do I need a visa to retire in {city}?',
         'a': f'{country_name} {"offers " + str(len(visas)) + " visa programs" if visas else "has limited visa options"} for retirees. {"The most accessible is the " + visas[0]["name"] + "." if visas else "Check official immigration resources for the latest requirements."}'},
        {'q': f'Is {city} safe for retirees?',
         'a': f'{city} has a safety score of {safety}/100, ranking #{safety_rank} out of {total_cities} retirement destinations in our database.'},
        {'q': f'How good is healthcare in {city}?',
         'a': f'{city} scores {healthcare}/100 for healthcare quality, ranking #{healthcare_rank} out of {total_cities} cities. {"Private health insurance for retirees 60+ costs approximately " + health_ins_str + "." if isinstance(health_ins, (int, float)) else ""}'},
        {'q': f'How long will $500,000 last in {city}?',
         'a': f'With $500,000 in savings, a single retiree can expect their money to last approximately {years_money_lasts(500000, city, "single")} years in {city}. For a couple, approximately {years_money_lasts(500000, city, "couple")} years.'},
        {'q': f'What is the inheritance tax in {country_name}?',
         'a': f'Inheritance tax in {country_name}: {inh_tax}. Capital gains tax: {cap_gains}%. {"Wealth tax applies." if wealth_tax_str != "None" else "No wealth tax."}'}
    ]

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in faq_items]
    }, indent=8)

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com"},
            {"@type": "ListItem", "position": 2, "name": "Retire Abroad", "item": "https://salary-converter.com/retire/"},
            {"@type": "ListItem", "position": 3, "name": f"Retire in {city}", "item": canonical}
        ]
    }, indent=8)

    title = f"Retire in {city} 2026: Cost of Living, Visa, Healthcare & Safety"
    if len(title) > 60:
        title = f"Retire in {city}: Costs, Visa & Safety Guide (2026)"
    desc = f"Complete 2026 guide to retiring in {city}. Monthly budget: {fmt_usd(couple_cost['total'])} (couple). Safety: {safety}/100. Healthcare: {healthcare}/100. Visa options, tax info & more."
    if len(desc) > 155:
        desc = f"Retire in {city}: {fmt_usd(couple_cost['total'])}/mo (couple). Safety {safety}/100, healthcare {healthcare}/100. Visa, tax & lifestyle guide."

    share_bar = build_share_bar(f"Retire in {city}: {fmt_usd(couple_cost['total'])}/mo for a couple. Full guide on salary:converter", canonical)

    faq_html = '\n'.join(
        f'''            <div class="faq-item">
                <h3>{f['q']}</h3>
                <p>{f['a']}</p>
            </div>'''
        for f in faq_items
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="retire in {city}, retirement {city}, cost of living {city} retirees, {city} retirement visa, retire abroad {country_name}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="manifest" href="/manifest.json">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
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
{GA4_SNIPPET}
    <style>
{PAGE_CSS}
    </style>
{THEME_JS}
</head>
<body>
{THEME_TOGGLE_HTML}

    <div class="page-container">
        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/retire/">Retire Abroad</a> &rsaquo; <a href="/retire/country/{to_slug(country_name)}">{country_name}</a> &rsaquo; {city}
        </div>

        <h1>Retire in {city}</h1>
        <p class="subtitle">Your complete 2026 guide to retiring in {city}, {country_name}. Costs, visa options, healthcare, safety, and quality of life — all in one place.</p>

        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-box-value">{fmt_usd(couple_cost['total'])}</div>
                <div class="stat-box-label">Monthly (Couple)</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-value">{safety}/100</div>
                <div class="stat-box-label">Safety</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-value">{healthcare}/100</div>
                <div class="stat-box-label">Healthcare</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-value">{climate}/100</div>
                <div class="stat-box-label">Climate</div>
            </div>
        </div>

        {share_bar}

        <section class="content-card">
            <h2>💰 Monthly Cost Breakdown</h2>
            <div style="overflow-x:auto;">
            <table>
                <thead><tr><th>Category</th><th style="text-align:right">Single</th><th style="text-align:right">Couple</th></tr></thead>
                <tbody>
                    <tr><td>Rent (1BR / 2BR)</td><td style="text-align:right">{fmt_usd(single_cost['rent'])}</td><td style="text-align:right">{fmt_usd(couple_cost['rent'])}</td></tr>
                    <tr><td>Groceries</td><td style="text-align:right">{fmt_usd(single_cost['groceries'])}</td><td style="text-align:right">{fmt_usd(couple_cost['groceries'])}</td></tr>
                    <tr><td>Utilities</td><td style="text-align:right">{fmt_usd(single_cost['utilities'])}</td><td style="text-align:right">{fmt_usd(couple_cost['utilities'])}</td></tr>
                    <tr><td>Transport</td><td style="text-align:right">{fmt_usd(single_cost['transport'])}</td><td style="text-align:right">{fmt_usd(couple_cost['transport'])}</td></tr>
                    <tr><td>Healthcare</td><td style="text-align:right">{fmt_usd(single_cost['healthcare'])}</td><td style="text-align:right">{fmt_usd(couple_cost['healthcare'])}</td></tr>
                    <tr style="font-weight:700;"><td>Total</td><td style="text-align:right">{fmt_usd(single_cost['total'])}</td><td style="text-align:right">{fmt_usd(couple_cost['total'])}</td></tr>
                </tbody>
            </table>
            </div>
        </section>

        <section class="content-card">
            <h2>📊 How Long Will Your Savings Last?</h2>
            <p>Based on current cost of living in {city}, here's how long different savings amounts will sustain you:</p>
            <div style="overflow-x:auto;">
            <table>
                <thead><tr><th>Savings</th><th style="text-align:right">Single</th><th style="text-align:right">Couple</th></tr></thead>
                <tbody>{savings_rows}</tbody>
            </table>
            </div>
            <p style="font-size:0.78rem;color:var(--text-secondary);margin-top:8px;">Assumes current costs, no investment returns or inflation adjustment. <a href="/retire/">Calculate with your exact numbers &rarr;</a></p>
        </section>

        <section class="content-card">
            <h2>🏥 Healthcare &amp; Safety</h2>
            <div class="stat-row"><span class="stat-label">Healthcare Quality</span><span class="stat-value">{healthcare}/100 (#{healthcare_rank} of {total_cities})</span></div>
            <div class="stat-row"><span class="stat-label">Safety</span><span class="stat-value">{safety}/100 (#{safety_rank} of {total_cities})</span></div>
            <div class="stat-row"><span class="stat-label">Health Insurance (60+)</span><span class="stat-value">{health_ins_str}</span></div>
        </section>

        <section class="content-card">
            <h2>🌤️ Climate &amp; Lifestyle</h2>
            <div class="stat-row"><span class="stat-label">Climate Score</span><span class="stat-value">{climate}/100 (#{get_rank(city, climate_score)} of {total_cities})</span></div>
            <div class="stat-row"><span class="stat-label">English Friendliness</span><span class="stat-value">{english}/100</span></div>
            <div class="stat-row"><span class="stat-label">Expat Community</span><span class="stat-value">{expat_badge(city)}</span></div>
            <div class="stat-row"><span class="stat-label">City Charm</span><span class="stat-value">{charm}/100</span></div>
            <div class="stat-row" style="border-bottom:none;"><span class="stat-label">Lifestyle</span><span class="stat-value">{lifestyle_tags_html(city)}</span></div>
        </section>

        {visa_html}

        <section class="content-card">
            <h2>💼 Tax Overview — {country_name}</h2>
            <div class="stat-row"><span class="stat-label">Inheritance Tax</span><span class="stat-value">{inh_tax}</span></div>
            <div class="stat-row"><span class="stat-label">Capital Gains Tax</span><span class="stat-value">{cap_gains}%</span></div>
            <div class="stat-row"><span class="stat-label">Dividend Tax</span><span class="stat-value">{div_tax}%</span></div>
            <div class="stat-row"><span class="stat-label">Wealth Tax</span><span class="stat-value">{wealth_tax_str}</span></div>
            <p style="font-size:0.78rem;color:var(--text-secondary);margin-top:8px;">Tax rates are indicative. Your actual liability depends on residency status, tax treaties, and personal circumstances. Consult a tax advisor.</p>
        </section>

        <section class="content-card">
            <h2>More in {country_name}</h2>
            <p><a href="/retire/country/{to_slug(country_name)}">Complete {country_name} retirement guide &rarr;</a></p>
            {related_links}
        </section>

        <section class="content-card">
            <h2>Explore {city}</h2>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <a href="/city/{slug}" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg);border-radius:10px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:600;">{city} Cost of Living</a>
                <a href="/salary-needed/{slug}" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg);border-radius:10px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:600;">Salary Needed in {city}</a>
            </div>
        </section>

{RETIRE_CTA_HTML}

{SALARY_CTA_HTML}

{WISE_CTA_HTML}

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>

{DATA_SOURCES_HTML}

{build_footer()}
    </div>

{FOOTER_JS}
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  PAGE TYPE B: /retire/country/{slug}.html
# ═══════════════════════════════════════════════════════════════════
def generate_country_page(country_code, country_name, cities):
    slug = to_slug(country_name)
    canonical = f"https://salary-converter.com/retire/country/{slug}"
    cd = country_data.get(country_name, {})
    visas = get_visa_programs_for_country(country_code)

    # City comparison rows
    city_rows = ''
    for city in sorted(cities, key=lambda c: get_monthly_cost(c, 'couple')['total']):
        cost = get_monthly_cost(city, 'couple')
        s = safety_index.get(city, '-')
        h = healthcare_index.get(city, '-')
        cl = climate_score.get(city, '-')
        ch = charm_score.get(city, '-')
        city_rows += f'<tr><td><a href="/retire/city/{to_slug(city)}" style="color:var(--accent);text-decoration:none;font-weight:500;">{city}</a></td><td style="text-align:right">{fmt_usd(cost["total"])}</td><td style="text-align:right">{s}</td><td style="text-align:right">{h}</td><td style="text-align:right">{cl}</td><td style="text-align:right">{ch}</td></tr>\n'

    # Visa cards
    visa_html = ''
    if visas:
        visa_cards = ''
        for v in visas:
            income_req = fmt_usd(v['minMonthlyIncome']) + '/mo' if v.get('minMonthlyIncome') else 'N/A'
            savings_req = fmt_usd(v['minSavings']) if v.get('minSavings') else 'N/A'
            pr_path = 'Yes' if v.get('pathToPR') else 'No'
            cit_years = f"{v['citizenshipYears']} years" if v.get('citizenshipYears') else 'N/A'
            visa_cards += f'''
                <div class="visa-card">
                    <div class="visa-card-name">{v.get('name', 'Visa Program')}</div>
                    <div class="visa-detail"><span class="visa-detail-label">Min. Monthly Income</span><span class="visa-detail-value">{income_req}</span></div>
                    <div class="visa-detail"><span class="visa-detail-label">Min. Savings</span><span class="visa-detail-value">{savings_req}</span></div>
                    <div class="visa-detail"><span class="visa-detail-label">Path to PR</span><span class="visa-detail-value">{pr_path}</span></div>
                    <div class="visa-detail"><span class="visa-detail-label">Citizenship</span><span class="visa-detail-value">{cit_years}</span></div>
                </div>'''
        visa_html = f'''
        <section class="content-card">
            <h2>🛂 Visa &amp; Residency Programs</h2>
            {visa_cards}
            <p style="font-size:0.82rem;margin-top:8px;"><a href="/retire/visa/{slug}">Full {country_name} visa guide &rarr;</a></p>
        </section>'''

    # Tax
    inh_tax = inheritance_tax_text(country_name)
    cap_gains = cd.get('capitalGainsTax', 'N/A')
    div_tax = cd.get('dividendTax', 'N/A')
    wealth_tax_data = cd.get('wealthTax')
    wealth_tax_str = 'None'
    if wealth_tax_data and isinstance(wealth_tax_data, dict) and wealth_tax_data.get('rate'):
        wealth_tax_str = f"{wealth_tax_data['rate']}%"
    health_ins = cd.get('healthInsurance60Plus', 'N/A')
    health_ins_str = fmt_usd(health_ins) + '/mo' if isinstance(health_ins, (int, float)) else str(health_ins)

    # FAQ
    cheapest = min(cities, key=lambda c: get_monthly_cost(c, 'couple')['total'])
    cheapest_cost = get_monthly_cost(cheapest, 'couple')['total']
    faq_items = [
        {'q': f'What is the cheapest city to retire in {country_name}?',
         'a': f'The most affordable city for retirees in {country_name} is {cheapest}, with a monthly cost of approximately {fmt_usd(cheapest_cost)} for a couple.'},
        {'q': f'Do I need a visa to retire in {country_name}?',
         'a': f'{country_name} {"offers " + str(len(visas)) + " visa programs for retirees" if visas else "has limited retirement visa options"}. Check our detailed visa guide for requirements.'},
        {'q': f'Is there inheritance tax in {country_name}?',
         'a': f'Inheritance tax in {country_name}: {inh_tax}. Capital gains tax: {cap_gains}%.'}
    ]

    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in faq_items]
    }, indent=8)

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com"},
            {"@type": "ListItem", "position": 2, "name": "Retire Abroad", "item": "https://salary-converter.com/retire/"},
            {"@type": "ListItem", "position": 3, "name": country_name, "item": canonical}
        ]
    }, indent=8)

    title = f"Retire in {country_name} 2026: {len(cities)} Cities, Visas & Complete Guide"
    if len(title) > 60:
        title = f"Retire in {country_name}: Cities, Visas & Guide (2026)"
    desc = f"Complete guide to retiring in {country_name}. Compare {len(cities)} cities, visa options, tax rates, healthcare & cost of living. Updated 2026."

    faq_html = '\n'.join(f'<div class="faq-item"><h3>{f["q"]}</h3><p>{f["a"]}</p></div>' for f in faq_items)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="retire in {country_name}, retirement {country_name}, {country_name} retirement visa, cost of living {country_name} retirees">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <script type="application/ld+json">
    {faq_schema}
    </script>
    <script type="application/ld+json">
    {breadcrumb_schema}
    </script>
{GA4_SNIPPET}
    <style>
{PAGE_CSS}
    </style>
{THEME_JS}
</head>
<body>
{THEME_TOGGLE_HTML}
    <div class="page-container">
        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/retire/">Retire Abroad</a> &rsaquo; {country_name}
        </div>
        <h1>Retire in {country_name}</h1>
        <p class="subtitle">Compare {len(cities)} cities in {country_name} for retirement — costs, safety, healthcare, climate, and visa options.</p>

        <section class="content-card">
            <h2>🏙️ Cities Compared</h2>
            <div style="overflow-x:auto;">
            <table>
                <thead><tr><th>City</th><th style="text-align:right">Monthly (Couple)</th><th style="text-align:right">Safety</th><th style="text-align:right">Healthcare</th><th style="text-align:right">Climate</th><th style="text-align:right">Charm</th></tr></thead>
                <tbody>{city_rows}</tbody>
            </table>
            </div>
        </section>

        {visa_html}

        <section class="content-card">
            <h2>💼 Tax Overview</h2>
            <div class="stat-row"><span class="stat-label">Inheritance Tax</span><span class="stat-value">{inh_tax}</span></div>
            <div class="stat-row"><span class="stat-label">Capital Gains Tax</span><span class="stat-value">{cap_gains}%</span></div>
            <div class="stat-row"><span class="stat-label">Dividend Tax</span><span class="stat-value">{div_tax}%</span></div>
            <div class="stat-row"><span class="stat-label">Wealth Tax</span><span class="stat-value">{wealth_tax_str}</span></div>
            <div class="stat-row" style="border-bottom:none;"><span class="stat-label">Health Insurance (60+)</span><span class="stat-value">{health_ins_str}</span></div>
        </section>

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {faq_html}
        </section>

{RETIRE_CTA_HTML}
{SALARY_CTA_HTML}
{WISE_CTA_HTML}
{DATA_SOURCES_HTML}
{build_footer()}
    </div>
{FOOTER_JS}
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  PAGE TYPE C: /retire/visa/{slug}.html
# ═══════════════════════════════════════════════════════════════════
def generate_visa_page(country_code, country_name, visas):
    slug = to_slug(country_name)
    canonical = f"https://salary-converter.com/retire/visa/{slug}"

    visa_details = ''
    for v in visas:
        income_req = fmt_usd(v['minMonthlyIncome']) + '/mo' if v.get('minMonthlyIncome') else 'Not specified'
        savings_req = fmt_usd(v['minSavings']) if v.get('minSavings') else 'Not specified'
        pr_path = 'Yes' if v.get('pathToPR') else 'No'
        citizenship = f"Yes — after {v['citizenshipYears']} years" if v.get('pathToCitizenship') and v.get('citizenshipYears') else ('Yes' if v.get('pathToCitizenship') else 'No')
        max_stay = f"{v['maxStayYears']} years" if v.get('maxStayYears') else 'Unlimited'
        visa_details += f'''
        <section class="content-card">
            <h2>{v.get('name', 'Visa Program')}</h2>
            <div class="stat-row"><span class="stat-label">Type</span><span class="stat-value">{v.get('type', '').replace('_', ' ').title()}</span></div>
            <div class="stat-row"><span class="stat-label">Min. Monthly Income</span><span class="stat-value">{income_req}</span></div>
            <div class="stat-row"><span class="stat-label">Min. Savings / Investment</span><span class="stat-value">{savings_req}</span></div>
            <div class="stat-row"><span class="stat-label">Max Initial Stay</span><span class="stat-value">{max_stay}</span></div>
            <div class="stat-row"><span class="stat-label">Path to Permanent Residency</span><span class="stat-value">{pr_path}</span></div>
            <div class="stat-row"><span class="stat-label">Path to Citizenship</span><span class="stat-value">{citizenship}</span></div>
            <div class="stat-row" style="border-bottom:none;"><span class="stat-label">Health Insurance Required</span><span class="stat-value">{'Yes' if v.get('healthInsuranceRequired') else 'No'}</span></div>
            <p style="font-size:0.85rem;color:var(--text-body);margin-top:12px;">{v.get('notes', '')}</p>
        </section>'''

    faq_items = [
        {'q': f'What visa do I need to retire in {country_name}?',
         'a': f'{country_name} offers {len(visas)} visa program{"s" if len(visas) > 1 else ""} for retirees: {", ".join(v["name"] for v in visas)}.'},
        {'q': f'What is the minimum income to retire in {country_name}?',
         'a': f'The minimum income requirements vary by program. ' + (f'The most accessible option ({visas[0]["name"]}) requires {fmt_usd(visas[0]["minMonthlyIncome"])}/month.' if visas[0].get('minMonthlyIncome') else f'The {visas[0]["name"]} requires minimum savings of {fmt_usd(visas[0]["minSavings"])}.' if visas[0].get('minSavings') else 'See individual program details above.')},
        {'q': f'Can I get citizenship through retirement in {country_name}?',
         'a': f'{"Yes — " + ", ".join(v["name"] + " (after " + str(v["citizenshipYears"]) + " years)" for v in visas if v.get("pathToCitizenship") and v.get("citizenshipYears")) + "." if any(v.get("pathToCitizenship") for v in visas) else "Current programs do not offer a direct path to citizenship through retirement."}'}
    ]
    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in faq_items]
    }, indent=8)
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com"},
            {"@type": "ListItem", "position": 2, "name": "Retire Abroad", "item": "https://salary-converter.com/retire/"},
            {"@type": "ListItem", "position": 3, "name": f"{country_name} Visa", "item": canonical}
        ]
    }, indent=8)

    title = f"{country_name} Retirement Visa 2026: Requirements & How to Apply"
    if len(title) > 60:
        title = f"{country_name} Retirement Visa: Requirements (2026)"
    desc = f"{country_name} retirement visa guide. {len(visas)} programs compared — income requirements, PR path, citizenship timeline. Updated 2026."
    faq_html = '\n'.join(f'<div class="faq-item"><h3>{f["q"]}</h3><p>{f["a"]}</p></div>' for f in faq_items)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{country_name} retirement visa, retire in {country_name} visa, {country_name} residency permit, retirement visa requirements {country_name}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">
    {faq_schema}
    </script>
    <script type="application/ld+json">
    {breadcrumb_schema}
    </script>
{GA4_SNIPPET}
    <style>
{PAGE_CSS}
    </style>
{THEME_JS}
</head>
<body>
{THEME_TOGGLE_HTML}
    <div class="page-container">
        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/retire/">Retire Abroad</a> &rsaquo; <a href="/retire/country/{slug}">{country_name}</a> &rsaquo; Visa Guide
        </div>
        <h1>{country_name} Retirement Visa Guide</h1>
        <p class="subtitle">{len(visas)} visa program{"s" if len(visas) > 1 else ""} available for retirees in {country_name}. Income requirements, PR paths, and citizenship timelines.</p>

        {visa_details}

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {faq_html}
        </section>

        <section class="content-card">
            <h2>Explore {country_name}</h2>
            <p><a href="/retire/country/{slug}">Full {country_name} retirement guide &rarr;</a></p>
        </section>

{RETIRE_CTA_HTML}
{SALARY_CTA_HTML}
{WISE_CTA_HTML}
{DATA_SOURCES_HTML}
{build_footer()}
    </div>
{FOOTER_JS}
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  PAGE TYPE D: /retire/budget/{slug}.html
# ═══════════════════════════════════════════════════════════════════
def generate_budget_page(budget_type, amount, label):
    """budget_type: 'monthly' or 'savings'"""
    slug = label.lower().replace('$', '').replace(',', '').replace(' ', '-').replace('/', '-')
    canonical = f"https://salary-converter.com/retire/budget/{slug}"

    if budget_type == 'monthly':
        title = f"Where Can You Retire on {label}? Best Cities Ranked (2026)"
        desc = f"Discover cities where you can retire on {label}. Ranked by affordability, safety, and quality of life. Updated 2026."
        # Filter cities where couple cost <= amount
        qualifying = [(city, get_monthly_cost(city, 'couple')) for city in coli_data]
        qualifying = [(city, cost) for city, cost in qualifying if cost['total'] <= amount]
        qualifying.sort(key=lambda x: x[1]['total'])
    else:
        title = f"Retire on {label}: Where Your Savings Last Longest (2026)"
        desc = f"With {label} in savings, see where you can retire longest. {len(coli_data)} cities ranked. Updated 2026."
        qualifying = [(city, get_monthly_cost(city, 'couple')) for city in coli_data]
        qualifying.sort(key=lambda x: years_money_lasts(amount, x[0], 'couple'), reverse=True)

    city_rows = ''
    for i, (city, cost) in enumerate(qualifying[:50], 1):
        cc = city_to_country.get(city, '')
        cn = get_country_name(cc)
        s = safety_index.get(city, '-')
        h = healthcare_index.get(city, '-')
        yrs = years_money_lasts(amount if budget_type == 'savings' else amount * 12 * 20, city, 'couple')
        city_rows += f'<tr><td>{i}</td><td><a href="/retire/city/{to_slug(city)}" style="color:var(--accent);text-decoration:none;font-weight:500;">{city}</a></td><td>{cn}</td><td style="text-align:right">{fmt_usd(cost["total"])}/mo</td><td style="text-align:right">{s}</td><td style="text-align:right">{h}</td></tr>\n'

    count = len(qualifying) if budget_type == 'monthly' else len(coli_data)

    faq_items = [
        {'q': f'Can I retire on {label}?',
         'a': f'Yes — {"there are " + str(len(qualifying)) + " cities worldwide where a couple can live on " + label if budget_type == "monthly" else "with " + label + " in savings, your money can last over " + str(years_money_lasts(amount, qualifying[0][0], "couple")) + " years in " + qualifying[0][0] if qualifying else "many cities offer affordable retirement"}.'},
        {'q': f'What is the cheapest place to retire abroad?',
         'a': f'The cheapest city in our database is {qualifying[0][0]} at {fmt_usd(qualifying[0][1]["total"])}/month for a couple.' if qualifying else 'See our full list of affordable retirement cities.'}
    ]
    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in faq_items]
    }, indent=8)
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com"},
            {"@type": "ListItem", "position": 2, "name": "Retire Abroad", "item": "https://salary-converter.com/retire/"},
            {"@type": "ListItem", "position": 3, "name": label, "item": canonical}
        ]
    }, indent=8)
    faq_html = '\n'.join(f'<div class="faq-item"><h3>{f["q"]}</h3><p>{f["a"]}</p></div>' for f in faq_items)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">
    {faq_schema}
    </script>
    <script type="application/ld+json">
    {breadcrumb_schema}
    </script>
{GA4_SNIPPET}
    <style>
{PAGE_CSS}
    </style>
{THEME_JS}
</head>
<body>
{THEME_TOGGLE_HTML}
    <div class="page-container">
        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/retire/">Retire Abroad</a> &rsaquo; {label}
        </div>
        <h1>{'Where Can You Retire on ' + label + '?' if budget_type == 'monthly' else 'Retire on ' + label}</h1>
        <p class="subtitle">{'Cities where a couple can retire on ' + label + ', ranked by total monthly cost.' if budget_type == 'monthly' else 'Where your ' + label + ' savings will stretch the furthest, ranked by years of retirement.'} Based on 2026 cost of living data across {len(coli_data)} cities.</p>

        <section class="content-card">
            <h2>{'Top ' + str(min(50, len(qualifying))) + ' Most Affordable Cities' if budget_type == 'monthly' else 'Top 50 Cities by Savings Duration'}</h2>
            <div style="overflow-x:auto;">
            <table>
                <thead><tr><th>#</th><th>City</th><th>Country</th><th style="text-align:right">Monthly (Couple)</th><th style="text-align:right">Safety</th><th style="text-align:right">Healthcare</th></tr></thead>
                <tbody>{city_rows}</tbody>
            </table>
            </div>
        </section>

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {faq_html}
        </section>

{RETIRE_CTA_HTML}
{SALARY_CTA_HTML}
{WISE_CTA_HTML}
{DATA_SOURCES_HTML}
{build_footer()}
    </div>
{FOOTER_JS}
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  PAGE TYPE E: /retire/compare/{a}-vs-{b}.html
# ═══════════════════════════════════════════════════════════════════
def generate_compare_page(city_a, city_b):
    slug = f"{to_slug(city_a)}-vs-{to_slug(city_b)}"
    canonical = f"https://salary-converter.com/retire/compare/{slug}"

    cost_a_s = get_monthly_cost(city_a, 'single')
    cost_b_s = get_monthly_cost(city_b, 'single')
    cost_a_c = get_monthly_cost(city_a, 'couple')
    cost_b_c = get_monthly_cost(city_b, 'couple')

    def winner(a_val, b_val, higher_better=True):
        if a_val == b_val or a_val == '-' or b_val == '-':
            return '', ''
        if higher_better:
            return ('<span class="winner-badge">Winner</span>' if a_val > b_val else '',
                    '<span class="winner-badge">Winner</span>' if b_val > a_val else '')
        else:
            return ('<span class="winner-badge">Winner</span>' if a_val < b_val else '',
                    '<span class="winner-badge">Winner</span>' if b_val < a_val else '')

    sa_a, sa_b = safety_index.get(city_a, 50), safety_index.get(city_b, 50)
    hc_a, hc_b = healthcare_index.get(city_a, 50), healthcare_index.get(city_b, 50)
    cl_a, cl_b = climate_score.get(city_a, 50), climate_score.get(city_b, 50)
    en_a, en_b = english_score.get(city_a, 50), english_score.get(city_b, 50)
    ch_a, ch_b = charm_score.get(city_a, 50), charm_score.get(city_b, 50)

    w_cost = winner(cost_a_c['total'], cost_b_c['total'], higher_better=False)
    w_safety = winner(sa_a, sa_b)
    w_health = winner(hc_a, hc_b)
    w_climate = winner(cl_a, cl_b)
    w_english = winner(en_a, en_b)
    w_charm = winner(ch_a, ch_b)

    cc_a = city_to_country.get(city_a, '')
    cc_b = city_to_country.get(city_b, '')
    cn_a = get_country_name(cc_a)
    cn_b = get_country_name(cc_b)

    faq_items = [
        {'q': f'Is it cheaper to retire in {city_a} or {city_b}?',
         'a': f'{city_a if cost_a_c["total"] < cost_b_c["total"] else city_b} is cheaper for couples at {fmt_usd(min(cost_a_c["total"], cost_b_c["total"]))}/month vs {fmt_usd(max(cost_a_c["total"], cost_b_c["total"]))}/month.'},
        {'q': f'Which is safer, {city_a} or {city_b}?',
         'a': f'{city_a if sa_a > sa_b else city_b} scores higher for safety ({max(sa_a, sa_b)}/100 vs {min(sa_a, sa_b)}/100).'},
        {'q': f'Which has better healthcare, {city_a} or {city_b}?',
         'a': f'{city_a if hc_a > hc_b else city_b} scores higher for healthcare quality ({max(hc_a, hc_b)}/100 vs {min(hc_a, hc_b)}/100).'}
    ]
    faq_schema = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in faq_items]
    }, indent=8)
    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com"},
            {"@type": "ListItem", "position": 2, "name": "Retire Abroad", "item": "https://salary-converter.com/retire/"},
            {"@type": "ListItem", "position": 3, "name": f"{city_a} vs {city_b}", "item": canonical}
        ]
    }, indent=8)

    title = f"Retire in {city_a} vs {city_b}: Costs, Safety & Visa Compared (2026)"
    if len(title) > 60:
        title = f"{city_a} vs {city_b}: Retirement Comparison (2026)"
    desc = f"Compare {city_a} and {city_b} for retirement. Costs, safety, healthcare, climate, visa — side by side. 2026 data."
    faq_html = '\n'.join(f'<div class="faq-item"><h3>{f["q"]}</h3><p>{f["a"]}</p></div>' for f in faq_items)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{city_a} vs {city_b} retirement, retire {city_a} or {city_b}, retirement comparison">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">
    {faq_schema}
    </script>
    <script type="application/ld+json">
    {breadcrumb_schema}
    </script>
{GA4_SNIPPET}
    <style>
{PAGE_CSS}
    </style>
{THEME_JS}
</head>
<body>
{THEME_TOGGLE_HTML}
    <div class="page-container">
        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/retire/">Retire Abroad</a> &rsaquo; {city_a} vs {city_b}
        </div>
        <h1>Retire in {city_a} vs {city_b}</h1>
        <p class="subtitle">Side-by-side retirement comparison of {city_a} ({cn_a}) and {city_b} ({cn_b}). Costs, safety, healthcare, climate, and visa options compared.</p>

        <section class="content-card">
            <h2>📊 Key Metrics</h2>
            <div style="overflow-x:auto;">
            <table>
                <thead><tr><th>Metric</th><th style="text-align:right">{city_a}</th><th style="text-align:right">{city_b}</th></tr></thead>
                <tbody>
                    <tr><td>Monthly Cost (Couple)</td><td style="text-align:right">{fmt_usd(cost_a_c['total'])} {w_cost[0]}</td><td style="text-align:right">{fmt_usd(cost_b_c['total'])} {w_cost[1]}</td></tr>
                    <tr><td>Monthly Cost (Single)</td><td style="text-align:right">{fmt_usd(cost_a_s['total'])}</td><td style="text-align:right">{fmt_usd(cost_b_s['total'])}</td></tr>
                    <tr><td>Safety</td><td style="text-align:right">{sa_a}/100 {w_safety[0]}</td><td style="text-align:right">{sa_b}/100 {w_safety[1]}</td></tr>
                    <tr><td>Healthcare</td><td style="text-align:right">{hc_a}/100 {w_health[0]}</td><td style="text-align:right">{hc_b}/100 {w_health[1]}</td></tr>
                    <tr><td>Climate</td><td style="text-align:right">{cl_a}/100 {w_climate[0]}</td><td style="text-align:right">{cl_b}/100 {w_climate[1]}</td></tr>
                    <tr><td>English Friendliness</td><td style="text-align:right">{en_a}/100 {w_english[0]}</td><td style="text-align:right">{en_b}/100 {w_english[1]}</td></tr>
                    <tr><td>City Charm</td><td style="text-align:right">{ch_a}/100 {w_charm[0]}</td><td style="text-align:right">{ch_b}/100 {w_charm[1]}</td></tr>
                    <tr><td>$500K Lasts (Couple)</td><td style="text-align:right">{years_money_lasts(500000, city_a, 'couple')} yrs</td><td style="text-align:right">{years_money_lasts(500000, city_b, 'couple')} yrs</td></tr>
                </tbody>
            </table>
            </div>
        </section>

        <section class="content-card">
            <h2>Explore Each City</h2>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <a href="/retire/city/{to_slug(city_a)}" style="display:inline-block;padding:8px 16px;background:var(--accent);color:#fff;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:600;">Retire in {city_a} &rarr;</a>
                <a href="/retire/city/{to_slug(city_b)}" style="display:inline-block;padding:8px 16px;background:var(--accent);color:#fff;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:600;">Retire in {city_b} &rarr;</a>
            </div>
        </section>

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {faq_html}
        </section>

{RETIRE_CTA_HTML}
{SALARY_CTA_HTML}
{WISE_CTA_HTML}
{DATA_SOURCES_HTML}
{build_footer()}
    </div>
{FOOTER_JS}
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  PAGE TYPE F: /retire/destinations/index.html
# ═══════════════════════════════════════════════════════════════════
def generate_destinations_index():
    # Group cities by region
    regions = {}
    for city in sorted(coli_data.keys()):
        cc = city_to_country.get(city, '')
        cn = get_country_name(cc)
        cd_item = country_data.get(cn, {})
        region = cd_item.get('region', cd_item.get('continent', 'Other'))
        if region not in regions:
            regions[region] = []
        regions[region].append(city)

    region_sections = ''
    for region in sorted(regions.keys()):
        cities = regions[region]
        links = '\n'.join(
            f'<a href="/retire/city/{to_slug(c)}" class="city-link"><span class="city-name">{c}</span><span class="city-salary">{fmt_usd(get_monthly_cost(c, "couple")["total"])}/mo</span></a>'
            for c in sorted(cities)
        )
        region_sections += f'''
        <section class="content-card">
            <h2>{region} ({len(cities)} cities)</h2>
            <div class="city-grid">{links}</div>
        </section>'''

    canonical = "https://salary-converter.com/retire/destinations/"
    title = f"All Retirement Destinations: {len(coli_data)} Cities Worldwide (2026)"
    desc = f"Browse {len(coli_data)} retirement destinations worldwide. Monthly costs, safety, healthcare scores. Find your ideal retirement city."

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Retirement Destinations",
        "description": "{desc}",
        "url": "{canonical}"
    }}
    </script>
{GA4_SNIPPET}
    <style>
{PAGE_CSS}
    </style>
{THEME_JS}
</head>
<body>
{THEME_TOGGLE_HTML}
    <div class="page-container">
        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/retire/">Retire Abroad</a> &rsaquo; All Destinations
        </div>
        <h1>Retirement Destinations</h1>
        <p class="subtitle">Browse {len(coli_data)} cities across {len(regions)} regions. Monthly cost shown is for a couple (rent, groceries, utilities, transport, healthcare).</p>

        {region_sections}

{RETIRE_CTA_HTML}
{SALARY_CTA_HTML}
{DATA_SOURCES_HTML}
{build_footer()}
    </div>
{FOOTER_JS}
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  COMPARE PAIRS
# ═══════════════════════════════════════════════════════════════════
COMPARE_PAIRS = [
    # Same-region: Europe
    ('Lisbon', 'Barcelona'), ('Lisbon', 'Porto'), ('Barcelona', 'Valencia'),
    ('Madrid', 'Barcelona'), ('Rome', 'Milan'), ('Berlin', 'Munich'),
    ('Paris', 'Nice'), ('Prague', 'Budapest'),
    ('Tallinn', 'Riga'), ('Warsaw', 'Wrocław'),
    ('Vienna', 'Budapest'), ('Amsterdam', 'Berlin'), ('Dublin', 'Edinburgh'),
    ('Málaga', 'Valencia'), ('Lisbon', 'Athens'), ('Nice', 'Barcelona'),
    ('Prague', 'Vienna'), ('Split', 'Kotor'), ('Tirana', 'Sarajevo'),
    ('Plovdiv', 'Bucharest'), ('Funchal', 'Faro'),
    # Same-region: Southeast Asia
    ('Chiang Mai', 'Bali (Denpasar)'), ('Bangkok', 'Ho Chi Minh City'), ('Kuala Lumpur', 'Bangkok'),
    ('Da Nang', 'Chiang Mai'), ('Bali (Denpasar)', 'Ho Chi Minh City'),
    ('Phnom Penh', 'Chiang Mai'), ('Manila', 'Bangkok'), ('Hanoi', 'Da Nang'),
    ('Chiang Mai', 'Hoi An'), ('Da Nang', 'Bali (Denpasar)'),
    # Same-region: Latin America
    ('Mexico City', 'Medellín'), ('Medellín', 'Bogotá'), ('Buenos Aires', 'Montevideo'),
    ('Lima', 'Bogotá'), ('Cancún', 'Tulum'), ('Panama City', 'Medellín'),
    ('Santiago', 'Buenos Aires'), ('Cuenca', 'Medellín'), ('São Paulo', 'Buenos Aires'),
    # Cross-region popular
    ('Lisbon', 'Chiang Mai'), ('Lisbon', 'Medellín'), ('Barcelona', 'Bali (Denpasar)'),
    ('Bangkok', 'Lisbon'), ('Mexico City', 'Barcelona'), ('Berlin', 'Bangkok'),
    ('Kuala Lumpur', 'Lisbon'), ('Buenos Aires', 'Barcelona'), ('Athens', 'Bali (Denpasar)'),
    ('Prague', 'Chiang Mai'), ('Nice', 'Bali (Denpasar)'), ('Rome', 'Bangkok'),
    ('Málaga', 'Chiang Mai'), ('Valencia', 'Da Nang'), ('Porto', 'Medellín'),
    # Middle East / Africa
    ('Dubai', 'Lisbon'), ('Dubai', 'Bangkok'), ('Cape Town', 'Lisbon'),
    ('Marrakech', 'Lisbon'), ('Cairo', 'Istanbul'), ('Istanbul', 'Athens'),
    ('Tel Aviv', 'Barcelona'),
    # US vs abroad
    ('Miami', 'Lisbon'), ('San Diego', 'Málaga'), ('Austin', 'Mexico City'),
    ('New York', 'London'), ('San Francisco', 'Barcelona'), ('Los Angeles', 'Barcelona'),
    # Asia-Pacific
    ('Tokyo', 'Taipei'), ('Seoul', 'Taipei'), ('Singapore', 'Kuala Lumpur'),
    ('Melbourne', 'Auckland'), ('Sydney', 'Singapore'),
    # Popular retirement matchups
    ('Lisbon', 'Valencia'), ('Porto', 'Athens'), ('Panama City', 'Lisbon'),
    ('Cuenca', 'Chiang Mai'), ('Faro', 'Málaga'),
    ('Bali (Denpasar)', 'Medellín'), ('Hoi An', 'Bali (Denpasar)'),
    ('Chiang Mai', 'Da Nang'), ('Colombo', 'Chiang Mai'), ('Nairobi', 'Cape Town'),
]


# ═══════════════════════════════════════════════════════════════════
#  GENERATE ALL PAGES
# ═══════════════════════════════════════════════════════════════════
print("\n--- Generating Retire Abroad pages ---\n")

# Create directories
for d in ['retire/city', 'retire/country', 'retire/visa', 'retire/budget', 'retire/compare', 'retire/destinations']:
    os.makedirs(os.path.join(BASE_DIR, d), exist_ok=True)

# A. City pages
city_count = 0
for city in coli_data:
    html = generate_city_page(city)
    if html:
        path = os.path.join(BASE_DIR, 'retire', 'city', f'{to_slug(city)}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        city_count += 1
print(f"City pages: {city_count}")

# B. Country pages
countries = {}
for city in coli_data:
    cc = city_to_country.get(city, '')
    if cc:
        cn = get_country_name(cc)
        if cn not in countries:
            countries[cn] = {'code': cc, 'cities': []}
        countries[cn]['cities'].append(city)

country_count = 0
for cn, info in countries.items():
    html = generate_country_page(info['code'], cn, info['cities'])
    if html:
        path = os.path.join(BASE_DIR, 'retire', 'country', f'{to_slug(cn)}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        country_count += 1
print(f"Country pages: {country_count}")

# C. Visa pages
visa_count = 0
visa_countries = {}
for v in visa_programs:
    cc = v.get('country', '')
    if cc not in visa_countries:
        visa_countries[cc] = []
    visa_countries[cc].append(v)

for cc, visas in visa_countries.items():
    cn = get_country_name(cc)
    html = generate_visa_page(cc, cn, visas)
    if html:
        path = os.path.join(BASE_DIR, 'retire', 'visa', f'{to_slug(cn)}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        visa_count += 1
print(f"Visa pages: {visa_count}")

# D. Budget pages
budgets = [
    ('monthly', 1000, '$1,000/Month'), ('monthly', 1500, '$1,500/Month'),
    ('monthly', 2000, '$2,000/Month'), ('monthly', 2500, '$2,500/Month'),
    ('monthly', 3000, '$3,000/Month'), ('monthly', 3500, '$3,500/Month'),
    ('savings', 200000, '$200K Savings'), ('savings', 300000, '$300K Savings'),
    ('savings', 500000, '$500K Savings'), ('savings', 750000, '$750K Savings'),
    ('savings', 1000000, '$1M Savings'), ('savings', 2000000, '$2M Savings'),
]
budget_count = 0
for btype, amount, label in budgets:
    html = generate_budget_page(btype, amount, label)
    if html:
        slug = label.lower().replace('$', '').replace(',', '').replace(' ', '-').replace('/', '-')
        path = os.path.join(BASE_DIR, 'retire', 'budget', f'{slug}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        budget_count += 1
print(f"Budget pages: {budget_count}")

# E. Compare pages
compare_count = 0
for city_a, city_b in COMPARE_PAIRS:
    if city_a in coli_data and city_b in coli_data:
        html = generate_compare_page(city_a, city_b)
        if html:
            slug = f"{to_slug(city_a)}-vs-{to_slug(city_b)}"
            path = os.path.join(BASE_DIR, 'retire', 'compare', f'{slug}.html')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            compare_count += 1
    else:
        missing = city_a if city_a not in coli_data else city_b
        print(f"  Skipping compare {city_a} vs {city_b}: '{missing}' not found")
print(f"Compare pages: {compare_count}")

# F. Destinations index
dest_html = generate_destinations_index()
with open(os.path.join(BASE_DIR, 'retire', 'destinations', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(dest_html)
print(f"Destinations index: 1")

total = city_count + country_count + visa_count + budget_count + compare_count + 1
print(f"\n=== Total: {total} pages generated in /retire/ ===")
