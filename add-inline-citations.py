#!/usr/bin/env python3
"""
add-inline-citations.py  v2
Adds inline superscript citation markers to blog article body text,
linked to the existing blog-citations-v1 section at the bottom.

Strategy:
- Each article's citations section gets id="citations-list"
- Citation CSS is injected into the <style> block
- Superscripts are added ONCE per source per article, on the FIRST matching claim
- Matching is done on the raw HTML text (not just inside > ... <) so it catches
  patterns like <span>COLI:</span> 38.5 and <td>$1,200/month</td>
- Skips <script>, <style>, JSON-LD blocks, and the citations section itself
- Idempotency: skips files already containing 'cite-ref'
"""

import os
import re

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "blog", "articles")

CITATION_CSS = """
        /* Inline citations */
        .cite-ref {
            font-size: 11px;
            vertical-align: super;
            line-height: 0;
            margin-left: 1px;
        }
        .cite-ref a {
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
        }
        .cite-ref a:hover {
            text-decoration: underline;
        }
        #citations-list {
            scroll-margin-top: 80px;
        }
"""

SOURCE_KEYWORDS = {
    'numbeo':       ['numbeo.com', 'Numbeo'],
    'expatistan':   ['expatistan.com', 'Expatistan'],
    'bls':          ['bls.gov', 'Bureau of Labor Statistics'],
    'oecd':         ['oecd.org', 'OECD'],
    'worldbank':    ['worldbank.org', 'World Bank'],
    'economist':    ['economist.com', 'Big Mac'],
    'mercer':       ['mercer.com', 'Mercer'],
    'internations': ['internations.org', 'InterNations', 'Expat Insider'],
    'ef':           ['ef.com', 'EF English'],
    'gpi':          ['visionofhumanity.org', 'Global Peace Index'],
    'ecb':          ['ecb.europa.eu', 'European Central Bank'],
    'eurostat':     ['eurostat', 'Eurostat'],
    'eiu':          ['eiu.com', 'Economist Intelligence'],
}

# (regex_pattern, source_key)
# Pattern matches the claim text that should get a superscript right after it.
CITE_PATTERNS = [
    # COLI / COL index value  e.g. "COLI:</span> 38.5" or "COL index 62.4" or "index of 69"
    (r'COLI(?::</span>)?\s+\d{2,3}(?:\.\d+)?',              'numbeo'),
    (r'COL(?:I)?(?: index| score| of)?\s+\d{2,3}(?:\.\d+)?','numbeo'),
    (r'cost[- ]of[- ]living index\s+(?:of\s+)?\d{2,3}',     'numbeo'),
    (r'index\s+(?:of\s+|score\s+)?\d{2,3}(?:\.\d+)?',       'numbeo'),

    # Explicit Numbeo mention
    (r"Numbeo(?:'s|&#39;s)?",                                'numbeo'),

    # Explicit Expatistan mention
    (r'Expatistan',                                          'expatistan'),

    # Rent / cost figures  e.g. "$1,200/month" "€850 per month" "£1,400/mo"
    (r'[$€£¥]\s*\d[\d,]+\s*(?:(?:per|a|\/)\s*month|\/mo\.?)', 'numbeo'),

    # Monthly budget  e.g. "$1,300 – $1,800" "€2,800–€3,800"
    (r'[$€£]\s*\d[\d,]+\s*[–\-—]+\s*[$€£]\s*\d[\d,]+',     'numbeo'),

    # Annual salary figures in salary context
    (r'(?:salary|income|earnings?|wage)\s+(?:of\s+)?[$€£]\s*\d[\d,]+', 'bls'),

    # Tax rate percentages
    (r'(?:tax rate|income tax|effective tax rate)\s+(?:of\s+)?\d{1,3}(?:\.\d+)?%', 'oecd'),
    (r'\d{1,3}(?:\.\d+)?%\s+(?:income\s+)?tax',             'oecd'),

    # Explicit OECD mention
    (r'OECD',                                                'oecd'),

    # BLS / Bureau of Labor Statistics
    (r'Bureau of Labor Statistics',                          'bls'),

    # PPP
    (r'purchasing[- ]power parity',                          'worldbank'),

    # Big Mac Index
    (r'Big Mac',                                             'economist'),

    # Survey names
    (r'Mercer',                                              'mercer'),
    (r'InterNations',                                        'internations'),
    (r'Expat Insider',                                       'internations'),
    (r'Global Peace Index',                                  'gpi'),
    (r'EF English Proficiency',                              'ef'),
    (r'Economist Intelligence',                              'eiu'),
]


def extract_sources(html):
    """
    Parse the blog-citations-v1 section. Returns list of (key, display, href).
    """
    section = re.search(r'class="blog-citations-v1".*?</section>', html, re.DOTALL)
    if not section:
        return []

    items = re.findall(r'<li>(.*?)</li>', section.group(0), re.DOTALL)
    sources = []
    seen_keys = set()

    for li in items:
        href_m = re.search(r'href="([^"]+)"', li)
        text_m = re.search(r'>([^<]{2,})<', li)
        if not href_m:
            continue
        href = href_m.group(1)
        text = text_m.group(1).strip() if text_m else href

        key = None
        for src_key, keywords in SOURCE_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in href.lower() or kw.lower() in li.lower():
                    key = src_key
                    break
            if key:
                break
        if key is None:
            key = f'other_{len(sources)}'

        if key not in seen_keys:
            seen_keys.add(key)
            sources.append((key, text, href))

    return sources


def build_cite_map(sources):
    return {src[0]: idx + 1 for idx, src in enumerate(sources)}


def sup(num):
    return f'<sup class="cite-ref"><a href="#citations-list">[{num}]</a></sup>'


def strip_skip_blocks(html):
    """
    Replace script/style/JSON-LD/citations blocks with placeholders.
    Returns (stripped_html, placeholders_dict).
    """
    placeholders = {}
    counter = [0]

    def replace(m):
        key = f'__PLACEHOLDER_{counter[0]}__'
        placeholders[key] = m.group(0)
        counter[0] += 1
        return key

    # JSON-LD script blocks
    result = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>',
                    replace, html, flags=re.DOTALL | re.IGNORECASE)
    # Other script blocks
    result = re.sub(r'<script[^>]*>.*?</script>',
                    replace, result, flags=re.DOTALL | re.IGNORECASE)
    # Style blocks
    result = re.sub(r'<style[^>]*>.*?</style>',
                    replace, result, flags=re.DOTALL | re.IGNORECASE)
    # Citations section
    result = re.sub(r'<section[^>]*blog-citations-v1[^>]*>.*?</section>',
                    replace, result, flags=re.DOTALL | re.IGNORECASE)
    # Head block
    result = re.sub(r'<head[^>]*>.*?</head>',
                    replace, result, flags=re.DOTALL | re.IGNORECASE)

    return result, placeholders


def restore_placeholders(html, placeholders):
    for key, val in placeholders.items():
        html = html.replace(key, val)
    return html


def add_citations(html, cite_map):
    working, placeholders = strip_skip_blocks(html)
    used = set()

    for pattern, src_key in CITE_PATTERNS:
        cite_num = cite_map.get(src_key)
        if cite_num is None:
            continue
        if src_key in used:
            continue

        def replacer(m, src_key=src_key, cite_num=cite_num, used=used):
            if src_key in used:
                return m.group(0)
            used.add(src_key)
            return m.group(0) + sup(cite_num)

        new_working = re.sub(pattern, replacer, working, count=1, flags=re.IGNORECASE)
        if new_working != working:
            working = new_working

    return restore_placeholders(working, placeholders)


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Idempotency
    if 'cite-ref' in html:
        print(f'  SKIP (already done): {os.path.basename(filepath)}')
        return False

    sources = extract_sources(html)
    if not sources:
        print(f'  SKIP (no citations): {os.path.basename(filepath)}')
        return False

    cite_map = build_cite_map(sources)

    # Add id to citations section
    html = re.sub(
        r'(<section\s+class="blog-citations-v1")',
        r'<section id="citations-list" class="blog-citations-v1"',
        html
    )

    # Inject CSS
    html = re.sub(r'(</style>)', CITATION_CSS + r'\1', html, count=1)

    # Add inline citations
    html = add_citations(html, cite_map)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    # Count how many superscripts landed
    count = html.count('cite-ref"><a href="#citations-list"')
    print(f'  OK [{count} inline cites, {len(sources)} sources]: {os.path.basename(filepath)}')
    return True


def main():
    files = sorted([
        os.path.join(ARTICLES_DIR, f)
        for f in os.listdir(ARTICLES_DIR)
        if f.endswith('.html')
    ])
    print(f'Processing {len(files)} blog articles...\n')
    updated = skipped = 0
    for fp in files:
        if process_file(fp):
            updated += 1
        else:
            skipped += 1
    print(f'\nDone. {updated} updated, {skipped} skipped.')


if __name__ == '__main__':
    main()
