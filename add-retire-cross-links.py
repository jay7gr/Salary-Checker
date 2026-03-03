#!/usr/bin/env python3
"""
Inject a "Retire in {City}" CTA into /city/ and /salary-needed/ pages
for every city that exists in the retire database (182 cities).

Reads retire/index.html to extract the coliData keys,
then finds matching city/*.html and salary-needed/*.html files
and injects a retire CTA section before the <footer tag.

Idempotent: skips files that already contain 'retire-cross-link-cta'.
"""

import os, re, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1. Read retire/index.html and extract coliData keys (182 cities)
# ---------------------------------------------------------------------------
retire_index_path = os.path.join(BASE_DIR, 'retire', 'index.html')
with open(retire_index_path, 'r', encoding='utf-8') as f:
    retire_html = f.read()


def js_to_json(raw):
    """Convert a JS object literal string to valid JSON."""
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
    raw = re.sub(r'\bnull\b', '0', raw)
    raw = re.sub(r',\s*}', '}', raw)
    raw = re.sub(r',\s*]', ']', raw)
    raw = re.sub(r'(?<=[{,\s])([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', raw)
    return raw


def extract_object(html, var_name):
    """Extract a simple JS object literal from HTML and parse it."""
    pattern = rf"const {var_name}\s*=\s*\{{([\s\S]*?)\}};"
    match = re.search(pattern, html)
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


print("Extracting coliData from retire/index.html...")
retire_coli = extract_object(retire_html, 'coliData')
print(f"Found {len(retire_coli)} cities in retire database")

if len(retire_coli) == 0:
    print("ERROR: No retire cities found. Exiting.")
    exit(1)

# ---------------------------------------------------------------------------
# 2. Slug functions
# ---------------------------------------------------------------------------

def to_slug(name):
    """to_slug from generate-salary-needed.py / generate-retire-pages.py.
    Used for salary-needed pages and retire city page URLs."""
    slug = re.sub(r'\s*\(.*?\)\s*', '', name)
    slug = re.sub(r'[^a-z0-9]+', '-', slug.lower())
    return slug.strip('-')


def slugify(name):
    """slugify from generate-pages.py.
    Used for /city/ pages — handles accented chars properly."""
    slug = name.lower()
    slug = slug.replace(' (denpasar)', '')
    slug = slug.replace(' (cr)', '')
    slug = slug.replace('\u00e3', 'a').replace('\u00e1', 'a').replace('\u00e9', 'e').replace('\u00fc', 'u')
    slug = slug.replace('\u00fa', 'u').replace('\u00ed', 'i').replace('\u00f3', 'o')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


# ---------------------------------------------------------------------------
# 3. CTA template
# ---------------------------------------------------------------------------

CTA_TEMPLATE = '''
<section class="retire-cross-link-cta" style="max-width:800px;margin:20px auto;padding:20px 24px;background:linear-gradient(135deg,#2563eb,#1d4ed8);border-radius:16px;text-align:center;color:#fff;">
    <p style="font-size:1rem;font-weight:600;margin:0 0 8px;">\U0001f334 Thinking about retiring in {CITY_NAME}?</p>
    <p style="font-size:0.85rem;margin:0 0 12px;color:rgba(255,255,255,0.85);">See how long your savings will last, visa options, healthcare scores, and more.</p>
    <a href="/retire/city/{CITY_SLUG}" style="display:inline-block;padding:10px 24px;background:#fff;color:#2563eb;border-radius:10px;text-decoration:none;font-weight:600;font-size:0.85rem;">Retire in {CITY_NAME} Guide \u2192</a>
</section>
'''


def make_cta(city_name, retire_slug):
    """Generate the CTA HTML for a given city."""
    return CTA_TEMPLATE.replace('{CITY_NAME}', city_name).replace('{CITY_SLUG}', retire_slug)


# ---------------------------------------------------------------------------
# 4. Injection logic
# ---------------------------------------------------------------------------

def inject_cta(filepath, city_name, retire_slug):
    """Inject the CTA into a page. Returns True if injected, False if skipped."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Idempotency check
    if 'retire-cross-link-cta' in content:
        return False

    cta_html = make_cta(city_name, retire_slug)

    # Try to inject before <footer tag
    footer_match = re.search(r'<footer\s', content)
    if footer_match:
        insert_pos = footer_match.start()
        new_content = content[:insert_pos] + cta_html + content[insert_pos:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    # Fallback: inject before the last </body>
    body_close = content.rfind('</body>')
    if body_close != -1:
        new_content = content[:body_close] + cta_html + content[body_close:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    print(f"  WARNING: Could not find injection point in {filepath}")
    return False


# ---------------------------------------------------------------------------
# 5. Process all retire cities
# ---------------------------------------------------------------------------

city_dir = os.path.join(BASE_DIR, 'city')
salary_dir = os.path.join(BASE_DIR, 'salary-needed')

city_updated = 0
city_skipped = 0
city_not_found = 0
salary_updated = 0
salary_skipped = 0
salary_not_found = 0

for city_name in sorted(retire_coli.keys()):
    retire_slug = to_slug(city_name)
    city_page_slug = slugify(city_name)
    salary_page_slug = to_slug(city_name)

    # --- /city/ pages ---
    city_path = os.path.join(city_dir, f"{city_page_slug}.html")
    if os.path.exists(city_path):
        if inject_cta(city_path, city_name, retire_slug):
            city_updated += 1
        else:
            city_skipped += 1
    else:
        city_not_found += 1

    # --- /salary-needed/ pages ---
    salary_path = os.path.join(salary_dir, f"{salary_page_slug}.html")
    if os.path.exists(salary_path):
        if inject_cta(salary_path, city_name, retire_slug):
            salary_updated += 1
        else:
            salary_skipped += 1
    else:
        salary_not_found += 1


# ---------------------------------------------------------------------------
# 6. Print stats
# ---------------------------------------------------------------------------
print()
print("=== Retire Cross-Link CTA Injection Stats ===")
print(f"City pages updated:          {city_updated}")
print(f"City pages skipped (exists): {city_skipped}")
print(f"City pages not found:        {city_not_found}")
print()
print(f"Salary-needed pages updated:          {salary_updated}")
print(f"Salary-needed pages skipped (exists): {salary_skipped}")
print(f"Salary-needed pages not found:        {salary_not_found}")
print()
print(f"Total pages modified: {city_updated + salary_updated}")
