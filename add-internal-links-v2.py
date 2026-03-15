#!/usr/bin/env python3
"""
Comprehensive internal linking script v2.
Handles 6 improvements across all page types:
  1. Compare pages: "Similar Comparisons" section (~5,900 pages)
  2. Salary-needed pages: "Similar Cost Cities" section (~230 pages)
  3. Compare index: Regional category sections (1 page)
  4. City pages: "Salary by Job Title" links (~113 pages)
  5. Salary-needed & compare pages: Blog cross-links (~230 + ~5,900 pages)
  6. Retire city pages: "Also Consider" section (~84 pages)

Idempotent: Each improvement uses its own marker class.
"""
import os
import re
import glob
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# ─── Import data from generate-pages.py ───────────────────────────
# Read the data portion (before if __name__) and exec it
_gp_path = os.path.join(ROOT, 'generate-pages.py')
with open(_gp_path, 'r', encoding='utf-8') as _f:
    _source = _f.read()
_data_end = _source.find("\nif __name__")
if _data_end == -1:
    _data_end = len(_source)
_namespace = {}
try:
    exec(compile(_source[:_data_end], _gp_path, 'exec'), _namespace)
except Exception:
    # Some functions may fail without full context; we only need data dicts
    pass

coliData = _namespace.get('coliData', {})
cityRegions = _namespace.get('cityRegions', {})

# Build reverse lookup: city -> region
city_to_region = {}
for region, cities in cityRegions.items():
    for city in cities:
        city_to_region[city] = region

# ─── Slug functions ───────────────────────────────────────────────
def slugify(name):
    slug = name.lower()
    slug = slug.replace(' (denpasar)', '').replace(' (cr)', '')
    slug = slug.replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('ü', 'u')
    slug = slug.replace('ú', 'u').replace('í', 'i').replace('ó', 'o')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')

def to_slug(name):
    slug = re.sub(r'\s*\(.*?\)\s*', '', name)
    slug = re.sub(r'[^a-z0-9]+', '-', slug.lower())
    return slug.strip('-')

# ─── Helpers ──────────────────────────────────────────────────────
def compare_url(city1, city2):
    s1, s2 = slugify(city1), slugify(city2)
    if s1 > s2:
        s1, s2 = s2, s1
    return f'/compare/{s1}-vs-{s2}'

def inject_before_footer(content, html):
    m = re.search(r'<footer\s', content)
    if m:
        return content[:m.start()] + html + '\n    ' + content[m.start():]
    return None

# Pre-compute sorted COLI list and existing compare filenames
coli_sorted = sorted(coliData.items(), key=lambda x: x[1])
all_cities = sorted(coliData.keys())

existing_compare = set()
for f in glob.glob(os.path.join(ROOT, 'compare', '*.html')):
    bn = os.path.basename(f)
    if bn != 'index.html':
        existing_compare.add(bn)

# Blog article data for cross-linking
BLOG_CITY_MAP = {
    'london-vs-new-york-true-cost-comparison': (['London', 'New York'], 'London vs New York: The True Cost Comparison'),
    'most-expensive-cities-in-the-world-2026': (['Zurich', 'New York', 'Singapore', 'Hong Kong', 'London', 'San Francisco', 'Geneva', 'Copenhagen', 'Tel Aviv', 'Sydney'], 'Most Expensive Cities in the World 2026'),
    'affordable-cities-in-europe-for-americans-2026': (['Lisbon', 'Barcelona', 'Berlin', 'Budapest', 'Bucharest', 'Prague', 'Warsaw', 'Athens', 'Porto', 'Valencia'], 'Affordable Cities in Europe for Americans 2026'),
    'tech-salary-comparison-by-city-2026': (['San Francisco', 'Seattle', 'London', 'Berlin', 'Bangalore', 'Tokyo', 'New York', 'Austin'], 'Tech Salary by City 2026'),
    'dubai-vs-singapore-expat-comparison': (['Dubai', 'Singapore'], 'Dubai vs Singapore: The Complete Expat Comparison'),
    'cost-of-living-southeast-asia-digital-nomads-2026': (['Bangkok', 'Bali (Denpasar)', 'Ho Chi Minh City', 'Kuala Lumpur', 'Chiang Mai', 'Manila', 'Jakarta', 'Phnom Penh', 'Hanoi'], 'Cost of Living in Southeast Asia for Digital Nomads'),
    'top-10-cities-for-remote-workers-2026': (['Lisbon', 'Bangkok', 'Buenos Aires', 'Mexico City', 'Berlin', 'Chiang Mai'], 'Top 10 Cities for Remote Workers 2026'),
    'what-is-a-good-salary-by-city-2026': (['New York', 'London', 'Tokyo', 'Dubai', 'San Francisco', 'Sydney', 'Paris'], 'What Is a Good Salary? 2026 Guide for 50 Cities'),
    'average-salary-by-city-2026-global-comparison': (['San Francisco', 'Zurich', 'New York', 'London', 'Tokyo', 'Singapore'], 'Average Salary by City 2026'),
    'how-cost-of-living-affects-your-salary': (['London', 'New York', 'San Francisco', 'Austin', 'Bangkok'], 'How Cost of Living Affects Your Salary'),
    'new-york-vs-los-angeles-cost-of-living-2026': (['New York', 'Los Angeles'], 'New York vs Los Angeles Cost of Living 2026'),
    'best-cities-for-expats-2026': (['Lisbon', 'Dubai', 'Singapore', 'Bangkok', 'Berlin', 'Amsterdam', 'Toronto', 'Melbourne'], 'Best Cities for Expats 2026'),
    'cheapest-countries-to-live-in-2026': (['Budapest', 'Bucharest', 'Bangkok', 'Chiang Mai', 'Lima', 'Buenos Aires', 'Ho Chi Minh City', 'Mumbai', 'Bangalore'], 'Cheapest Countries to Live In 2026'),
    'geo-arbitrage-guide-2026': (['San Francisco', 'Lisbon', 'Bangkok', 'Mexico City', 'Buenos Aires', 'Medellín'], 'Geo-Arbitrage Guide 2026'),
    'how-far-does-100k-go-in-every-city-2026': (['New York', 'London', 'Bangkok', 'Zurich', 'San Francisco', 'Tokyo'], 'How Far Does $100K Go in Every City?'),
    'cost-of-living-for-couples-by-city-2026': (['New York', 'London', 'Bangkok', 'Lisbon', 'Tokyo', 'Dubai'], 'Cost of Living for Couples by City 2026'),
    'cost-of-living-single-person-by-city-2026': (['New York', 'London', 'Bangkok', 'Tokyo', 'Berlin', 'Lisbon'], 'Cost of Living for a Single Person 2026'),
    'what-5000-a-month-gets-you-in-30-cities': (['New York', 'London', 'Bangkok', 'Tokyo', 'Lisbon', 'Mexico City', 'Dubai'], 'What $5,000/Month Gets You in 30 Cities'),
    'monthly-budget-breakdown-by-city-2026': (['New York', 'London', 'Bangkok', 'Tokyo', 'Berlin', 'Sydney'], 'Monthly Budget Breakdown by City 2026'),
    'remote-work-relocation-pay-cut-worth-it-2026': (['San Francisco', 'Austin', 'Lisbon', 'Bangkok', 'Mexico City', 'Denver'], 'Remote Work Relocation: Is a Pay Cut Worth It?'),
    'us-vs-canada-vs-uk-vs-australia-cost-of-living-2026': (['New York', 'Toronto', 'London', 'Sydney', 'Vancouver', 'Melbourne'], 'US vs Canada vs UK vs Australia Cost of Living'),
    'retire-on-2000-a-month-abroad-best-cities': (['Bangkok', 'Chiang Mai', 'Lisbon', 'Medellín', 'Buenos Aires', 'Lima'], 'Retire on $2,000/Month Abroad: Best Cities'),
    'how-to-retire-abroad-cost-of-living-guide': (['Lisbon', 'Bangkok', 'Mexico City', 'Buenos Aires', 'Dubai'], 'How to Retire Abroad: Cost of Living Guide'),
    'minimum-wage-vs-cost-of-living-by-city-2026': (['New York', 'London', 'San Francisco', 'Austin', 'Bangkok', 'Berlin'], 'Minimum Wage vs Cost of Living by City'),
    'gen-z-salary-vs-cost-of-living-2026': (['New York', 'Austin', 'Berlin', 'Lisbon', 'Bangkok'], 'Gen Z Salary vs Cost of Living 2026'),
}

# Build reverse: city -> [(slug, title), ...]
city_to_blogs = {}
for slug, (cities, title) in BLOG_CITY_MAP.items():
    for city in cities:
        city_to_blogs.setdefault(city, []).append((slug, title))


# ══════════════════════════════════════════════════════════════════
# IMPROVEMENT 1: Compare pages — "Similar Comparisons" section
# ══════════════════════════════════════════════════════════════════
def improvement_1():
    MARKER = 'similar-comparisons-v1'
    print('\n[1/6] Compare pages: Similar Comparisons')
    updated = skipped = errors = 0

    files = glob.glob(os.path.join(ROOT, 'compare', '*.html'))
    for filepath in files:
        bn = os.path.basename(filepath)
        if bn == 'index.html':
            skipped += 1
            continue
        # Skip subdirectory files
        rel = os.path.relpath(filepath, os.path.join(ROOT, 'compare'))
        if os.sep in rel:
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            # Extract cities from filename: city1-vs-city2.html
            stem = bn.replace('.html', '')
            parts = stem.split('-vs-')
            if len(parts) != 2:
                skipped += 1
                continue

            slug_a, slug_b = parts
            # Find city names from slugs
            city_a = city_b = None
            for c in coliData:
                s = slugify(c)
                if s == slug_a:
                    city_a = c
                if s == slug_b:
                    city_b = c
            if not city_a or not city_b:
                skipped += 1
                continue

            # Find related comparisons
            links = []
            seen = {frozenset({city_a, city_b})}

            # Comparisons involving city_a (up to 3)
            for c in all_cities:
                if len(links) >= 3:
                    break
                if c == city_a or c == city_b:
                    continue
                pair = frozenset({city_a, c})
                if pair in seen:
                    continue
                s1, s2 = sorted([slugify(city_a), slugify(c)])
                if f'{s1}-vs-{s2}.html' in existing_compare:
                    links.append((city_a, c))
                    seen.add(pair)

            # Comparisons involving city_b (up to 3)
            for c in all_cities:
                if len(links) >= 6:
                    break
                if c == city_a or c == city_b:
                    continue
                pair = frozenset({city_b, c})
                if pair in seen:
                    continue
                s1, s2 = sorted([slugify(city_b), slugify(c)])
                if f'{s1}-vs-{s2}.html' in existing_compare:
                    links.append((city_b, c))
                    seen.add(pair)

            if not links:
                skipped += 1
                continue

            # Build HTML
            items = []
            for c1, c2 in links:
                url = compare_url(c1, c2)
                items.append(f'<a href="{url}" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--accent,#2563eb);font-size:0.82rem;font-weight:500;">{c1} vs {c2}</a>')

            section = f'''
    <section class="{MARKER}" style="margin-top:24px;">
        <h2 style="font-size:1rem;font-weight:700;color:var(--text-primary);margin-bottom:12px;">Similar Comparisons</h2>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            {chr(10).join(f"            {item}" for item in items)}
        </div>
    </section>
'''
            new_content = inject_before_footer(content, section)
            if new_content is None:
                errors += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f'  ERROR: {bn}: {e}')

    print(f'  Done: {updated} updated, {skipped} skipped, {errors} errors')
    return updated, skipped, errors


# ══════════════════════════════════════════════════════════════════
# IMPROVEMENT 2: Salary-needed pages — "Similar Cost Cities"
# ══════════════════════════════════════════════════════════════════
def improvement_2():
    MARKER = 'similar-cost-v1'
    print('\n[2/6] Salary-needed pages: Similar Cost Cities')
    updated = skipped = errors = 0

    files = glob.glob(os.path.join(ROOT, 'salary-needed', '*.html'))
    for filepath in files:
        bn = os.path.basename(filepath)
        if bn == 'index.html':
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            # Match city by filename slug
            file_slug = bn.replace('.html', '')
            city_name = None
            for c in coliData:
                if to_slug(c) == file_slug:
                    city_name = c
                    break
            if not city_name:
                skipped += 1
                continue

            target_coli = coliData[city_name]
            # Find 6 nearest COLI neighbors
            neighbors = sorted(
                [(c, abs(coli - target_coli)) for c, coli in coli_sorted if c != city_name],
                key=lambda x: x[1]
            )[:6]

            items = []
            for c, _ in neighbors:
                c_slug = to_slug(c)
                c_coli = coliData[c]
                items.append(f'<a href="/salary-needed/{c_slug}" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--accent,#2563eb);font-size:0.82rem;font-weight:500;">{c} <span style="font-size:0.75rem;color:var(--text-secondary);">COLI {c_coli}</span></a>')

            section = f'''
    <section class="{MARKER}" style="margin-top:24px;">
        <h2 style="font-size:1rem;font-weight:700;color:var(--text-primary);margin-bottom:12px;">Cities with Similar Cost of Living</h2>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            {chr(10).join(f"            {item}" for item in items)}
        </div>
    </section>
'''
            new_content = inject_before_footer(content, section)
            if new_content is None:
                errors += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f'  ERROR: {bn}: {e}')

    print(f'  Done: {updated} updated, {skipped} skipped, {errors} errors')
    return updated, skipped, errors


# ══════════════════════════════════════════════════════════════════
# IMPROVEMENT 3: Compare index — Regional categories
# ══════════════════════════════════════════════════════════════════
def improvement_3():
    MARKER = 'compare-categories-v1'
    print('\n[3/6] Compare index: Regional categories')

    filepath = os.path.join(ROOT, 'compare', 'index.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print('  Done: 0 updated, 1 skipped, 0 errors')
        return 0, 1, 0

    CONTINENTS = {
        'Europe': ['Western Europe', 'Southern Europe', 'Northern Europe', 'Eastern Europe'],
        'North America': ['North America'],
        'Asia & Oceania': ['East Asia', 'Southeast Asia', 'South Asia', 'Oceania', 'Middle East'],
        'South America & Africa': ['South America', 'Africa'],
    }
    city_to_continent = {}
    for cont, regions in CONTINENTS.items():
        for region in regions:
            for city in cityRegions.get(region, []):
                city_to_continent[city] = cont

    sections = []
    for cont_name in ['Europe', 'North America', 'Asia & Oceania', 'South America & Africa', 'Cross-Continental']:
        pairs = []
        for i, c1 in enumerate(all_cities):
            for c2 in all_cities[i+1:]:
                s1, s2 = slugify(c1), slugify(c2)
                if s1 > s2:
                    s1, s2 = s2, s1
                if f'{s1}-vs-{s2}.html' not in existing_compare:
                    continue
                cont1 = city_to_continent.get(c1)
                cont2 = city_to_continent.get(c2)
                if cont_name == 'Cross-Continental':
                    if cont1 and cont2 and cont1 != cont2:
                        diff = abs(coliData[c1] - coliData[c2])
                        pairs.append((c1, c2, diff))
                else:
                    if cont1 == cont_name and cont2 == cont_name:
                        diff = abs(coliData[c1] - coliData[c2])
                        pairs.append((c1, c2, diff))

        pairs.sort(key=lambda x: x[2], reverse=True)
        top = pairs[:15]

        cards = []
        for c1, c2, diff in top:
            url = compare_url(c1, c2)
            coli1 = coliData[c1]
            coli2 = coliData[c2]
            diff_pct = round(diff / max(coli1, coli2, 1) * 100)
            cards.append(
                f'                <a href="{url}" class="compare-card">\n'
                f'                    <div class="compare-card-cities">{c1} <span class="vs">vs</span> {c2}</div>\n'
                f'                    <div class="compare-card-stats">COLI: {coli1} vs {coli2} &middot; {diff_pct}% difference</div>\n'
                f'                </a>'
            )

        sections.append(f'''
        <h2 class="{MARKER}" style="font-size:1.2rem;font-weight:700;margin:32px 0 16px;color:var(--text-primary);">{cont_name} Comparisons</h2>
        <div class="compare-grid">
{chr(10).join(cards)}
        </div>''')

    all_sections = '\n'.join(sections)

    new_content = inject_before_footer(content, all_sections)
    if new_content is None:
        print('  Done: 0 updated, 0 skipped, 1 errors')
        return 0, 0, 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('  Done: 1 updated, 0 skipped, 0 errors')
    return 1, 0, 0


# ══════════════════════════════════════════════════════════════════
# IMPROVEMENT 4: City pages — "Salary by Job Title" links
# ══════════════════════════════════════════════════════════════════
def improvement_4():
    MARKER = 'salary-links-v2'
    print('\n[4/6] City pages: Salary by Job Title links')
    updated = skipped = errors = 0

    TOP_JOBS = [
        ('Software Engineer', 'software-engineer'),
        ('Doctor', 'doctor-general'),
        ('Nurse', 'nurse'),
        ('Teacher', 'teacher'),
    ]

    files = glob.glob(os.path.join(ROOT, 'city', '*.html'))
    for filepath in files:
        bn = os.path.basename(filepath)
        if bn == 'index.html':
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            items = []
            for title, slug in TOP_JOBS:
                items.append(f'<a href="/salary/{slug}" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--accent,#2563eb);font-size:0.82rem;font-weight:500;">{title} Salary</a>')

            section = f'''
    <section class="{MARKER}" style="margin-top:24px;">
        <h2 style="font-size:1rem;font-weight:700;color:var(--text-primary);margin-bottom:8px;">Salary by Job Title</h2>
        <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">See how salaries compare across cities for specific jobs:</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            {chr(10).join(f"            {item}" for item in items)}
        </div>
    </section>
'''
            new_content = inject_before_footer(content, section)
            if new_content is None:
                errors += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f'  ERROR: {bn}: {e}')

    print(f'  Done: {updated} updated, {skipped} skipped, {errors} errors')
    return updated, skipped, errors


# ══════════════════════════════════════════════════════════════════
# IMPROVEMENT 5: Blog cross-links on salary-needed & compare pages
# ══════════════════════════════════════════════════════════════════
def improvement_5():
    MARKER = 'blog-cross-v1'
    print('\n[5/6] Blog cross-links on salary-needed & compare pages')
    updated = skipped = errors = 0

    # 5a: Salary-needed pages
    files = glob.glob(os.path.join(ROOT, 'salary-needed', '*.html'))
    for filepath in files:
        bn = os.path.basename(filepath)
        if bn == 'index.html':
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            file_slug = bn.replace('.html', '')
            city_name = None
            for c in coliData:
                if to_slug(c) == file_slug:
                    city_name = c
                    break
            if not city_name or city_name not in city_to_blogs:
                skipped += 1
                continue

            blogs = city_to_blogs[city_name][:2]
            if not blogs:
                skipped += 1
                continue

            items = []
            for slug, title in blogs:
                items.append(f'<a href="/blog/articles/{slug}" style="display:block;padding:12px 16px;background:var(--card-bg,#fff);border:1px solid var(--border-light,#f0f0f2);border-radius:12px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:500;">{title}</a>')

            section = f'''
    <section class="{MARKER}" style="margin-top:24px;">
        <h2 style="font-size:1rem;font-weight:700;color:var(--text-primary);margin-bottom:12px;">Related Articles</h2>
        <div style="display:flex;flex-direction:column;gap:8px;">
            {chr(10).join(f"            {item}" for item in items)}
        </div>
    </section>
'''
            new_content = inject_before_footer(content, section)
            if new_content is None:
                errors += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

        except Exception as e:
            errors += 1

    # 5b: Compare pages — add blog links
    files = glob.glob(os.path.join(ROOT, 'compare', '*.html'))
    for filepath in files:
        bn = os.path.basename(filepath)
        if bn == 'index.html':
            skipped += 1
            continue
        rel = os.path.relpath(filepath, os.path.join(ROOT, 'compare'))
        if os.sep in rel:
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            stem = bn.replace('.html', '')
            parts = stem.split('-vs-')
            if len(parts) != 2:
                skipped += 1
                continue

            slug_a, slug_b = parts
            city_a = city_b = None
            for c in coliData:
                s = slugify(c)
                if s == slug_a:
                    city_a = c
                if s == slug_b:
                    city_b = c

            # Collect blog articles mentioning either city
            blogs = set()
            if city_a and city_a in city_to_blogs:
                for b in city_to_blogs[city_a][:2]:
                    blogs.add(b)
            if city_b and city_b in city_to_blogs:
                for b in city_to_blogs[city_b][:2]:
                    blogs.add(b)

            if not blogs:
                skipped += 1
                continue

            blog_list = list(blogs)[:2]
            items = []
            for slug, title in blog_list:
                items.append(f'<a href="/blog/articles/{slug}" style="display:block;padding:12px 16px;background:var(--card-bg,#fff);border:1px solid var(--border-light,#f0f0f2);border-radius:12px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:500;">{title}</a>')

            section = f'''
    <section class="{MARKER}" style="margin-top:24px;">
        <h2 style="font-size:1rem;font-weight:700;color:var(--text-primary);margin-bottom:12px;">Related Articles</h2>
        <div style="display:flex;flex-direction:column;gap:8px;">
            {chr(10).join(f"            {item}" for item in items)}
        </div>
    </section>
'''
            new_content = inject_before_footer(content, section)
            if new_content is None:
                errors += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

        except Exception as e:
            errors += 1

    print(f'  Done: {updated} updated, {skipped} skipped, {errors} errors')
    return updated, skipped, errors


# ══════════════════════════════════════════════════════════════════
# IMPROVEMENT 6: Retire city pages — "Also Consider" section
# ══════════════════════════════════════════════════════════════════
def improvement_6():
    MARKER = 'retire-similar-v1'
    print('\n[6/6] Retire city pages: Also Consider')
    updated = skipped = errors = 0

    files = glob.glob(os.path.join(ROOT, 'retire', 'city', '*.html'))
    for filepath in files:
        bn = os.path.basename(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            # Extract city from title: "Retire in {City}:"
            m = re.search(r'<title>Retire in (.+?)[:\s—\-]', content)
            if not m:
                skipped += 1
                continue
            city = m.group(1).strip()

            # Find the city in coliData
            if city not in coliData:
                # Try slug match
                file_slug = bn.replace('.html', '')
                city = None
                for c in coliData:
                    if to_slug(c) == file_slug:
                        city = c
                        break
                if not city:
                    skipped += 1
                    continue

            city_coli = coliData[city]
            city_region = city_to_region.get(city, '')

            # Find similar: 3 same region + 3 similar budget
            results = []
            seen = {city}

            # Same region
            region_peers = sorted(
                [(c, abs(coliData[c] - city_coli)) for c in coliData
                 if city_to_region.get(c) == city_region and c != city],
                key=lambda x: x[1]
            )
            for c, _ in region_peers[:3]:
                # Check retire page exists
                if os.path.exists(os.path.join(ROOT, 'retire', 'city', f'{to_slug(c)}.html')):
                    results.append(c)
                    seen.add(c)

            # Similar budget (any region)
            budget_peers = sorted(
                [(c, abs(coliData[c] - city_coli)) for c in coliData if c not in seen],
                key=lambda x: x[1]
            )
            for c, _ in budget_peers[:3]:
                if os.path.exists(os.path.join(ROOT, 'retire', 'city', f'{to_slug(c)}.html')):
                    results.append(c)
                    seen.add(c)

            if not results:
                skipped += 1
                continue

            items = []
            for dest in results[:6]:
                items.append(f'<a href="/retire/city/{to_slug(dest)}" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:500;">{dest}</a>')

            section = f'''
    <section class="{MARKER}" style="margin-top:24px;">
        <h2 style="font-size:1rem;font-weight:700;color:var(--text-primary);margin-bottom:8px;">Also Consider</h2>
        <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">Similar retirement destinations by region and budget:</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
            {chr(10).join(f"            {item}" for item in items)}
        </div>
    </section>
'''
            new_content = inject_before_footer(content, section)
            if new_content is None:
                errors += 1
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1

        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f'  ERROR: {bn}: {e}')

    print(f'  Done: {updated} updated, {skipped} skipped, {errors} errors')
    return updated, skipped, errors


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('=' * 60)
    print('Internal Linking Improvements v2')
    print('=' * 60)

    total_updated = total_skipped = total_errors = 0

    for fn in [improvement_1, improvement_2, improvement_3, improvement_4, improvement_5, improvement_6]:
        u, s, e = fn()
        total_updated += u
        total_skipped += s
        total_errors += e

    print('\n' + '=' * 60)
    print(f'TOTAL: {total_updated} updated, {total_skipped} skipped, {total_errors} errors')
    print('=' * 60)
