#!/usr/bin/env python3
"""
One-time script to add internal cross-links across all page types.
Closes 5 linking gaps between page types:
  1. Ranking pages -> neighborhood hubs + salary-needed
  2. Compare pages -> "See all neighborhoods" links
  3. Neighborhood hub pages -> ranking page links
  4. City pages -> quick-links card (neighborhoods, salary-needed, rankings)
  5. Blog articles -> related ranking links

Idempotency: Checks for 'cross-links-v1' class before modifying.
"""

import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
MARKER = 'cross-links-v1'

# Cities that have neighborhood data (and therefore hub pages)
NEIGHBORHOOD_CITIES = [
    'New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Miami', 'Austin',
    'Seattle', 'Denver', 'Boston', 'Washington DC', 'Houston', 'Charlotte',
    'Las Vegas', 'Tampa', 'Raleigh', 'Dallas', 'Atlanta', 'Philadelphia',
    'Phoenix', 'San Diego', 'Nashville', 'Minneapolis', 'Portland',
    'Toronto', 'Vancouver', 'Montreal', 'Mexico City', 'Cancun', 'Panama City',
    'London', 'Paris', 'Amsterdam', 'Berlin', 'Munich', 'Dublin', 'Brussels',
    'Luxembourg City', 'Zurich', 'Geneva', 'Edinburgh', 'Nice',
    'Madrid', 'Barcelona', 'Valencia', 'Malaga', 'Lisbon', 'Porto', 'Rome',
    'Milan', 'Athens', 'Split',
    'Stockholm', 'Copenhagen', 'Helsinki', 'Oslo', 'Vienna',
    'Prague', 'Budapest', 'Warsaw', 'Krakow', 'Bucharest', 'Tallinn', 'Riga', 'Istanbul',
    'Tokyo', 'Osaka', 'Fukuoka', 'Seoul', 'Hong Kong', 'Taipei',
    'Shanghai', 'Beijing', 'Shenzhen', 'Guangzhou',
    'Singapore', 'Bangkok', 'Chiang Mai', 'Phuket', 'Kuala Lumpur',
    'Ho Chi Minh City', 'Hanoi', 'Manila', 'Jakarta', 'Bali',
    'Phnom Penh',
    'Mumbai', 'Bangalore', 'Delhi', 'Chennai',
    'Sydney', 'Melbourne', 'Perth', 'Auckland',
    'Dubai', 'Abu Dhabi', 'Doha', 'Riyadh', 'Tel Aviv',
    'Cape Town', 'Nairobi', 'Lagos', 'Cairo', 'Marrakech', 'Casablanca',
    'Sao Paulo', 'Buenos Aires', 'Bogota', 'Lima', 'Santiago', 'Medellin',
    'Montevideo', 'San Jose', 'Playa del Carmen',
]

RANKING_PAGES = {
    'cheapest-cities': 'Cheapest Cities to Live In',
    'most-expensive-cities': 'Most Expensive Cities in the World',
    'cheapest-rent': 'Cities with the Cheapest Rent',
    'highest-salaries': 'Cities with the Highest Salaries',
    'lowest-taxes': 'Cities with the Lowest Taxes',
    'best-value-cities': 'Best Value Cities to Live In',
    'cheapest-for-families': 'Cheapest Cities for Families',
}

BLOG_RANKING_MAP = {
    'affordable-cities': ['cheapest-cities', 'best-value-cities'],
    'most-expensive': ['most-expensive-cities'],
    'tech-salary': ['highest-salaries', 'best-value-cities'],
    'salary-negotiation': ['highest-salaries'],
    'cost-of-living': ['cheapest-cities', 'most-expensive-cities'],
    'remote-workers': ['best-value-cities', 'cheapest-rent'],
    'retire-abroad': ['cheapest-cities', 'cheapest-for-families'],
    'dubai-vs-singapore': ['most-expensive-cities', 'highest-salaries'],
    'london-vs-new-york': ['most-expensive-cities'],
    'neighborhood': ['cheapest-cities', 'cheapest-rent'],
    'average-salary': ['highest-salaries'],
    'currency-exchange': ['best-value-cities'],
    'purchasing-power': ['best-value-cities', 'cheapest-cities'],
    'geographic-pay': ['highest-salaries', 'best-value-cities'],
    'cola': ['cheapest-cities', 'most-expensive-cities'],
    'southeast-asia': ['cheapest-cities', 'cheapest-rent'],
    'good-salary': ['highest-salaries', 'cheapest-cities'],
    '_default': ['cheapest-cities', 'most-expensive-cities', 'best-value-cities'],
}

TOP_NEIGHBORHOOD_CITIES = [
    'New York', 'London', 'San Francisco', 'Los Angeles', 'Tokyo',
    'Paris', 'Sydney', 'Dubai', 'Singapore', 'Berlin',
]

TOP_SALARY_CITIES = [
    'New York', 'London', 'San Francisco', 'Tokyo', 'Dubai',
    'Paris', 'Sydney', 'Singapore', 'Berlin', 'Toronto',
]


def slugify(name):
    """Convert city name to URL-safe slug. Same as generate-pages.py."""
    slug = name.lower()
    slug = slug.replace(' (denpasar)', '')
    slug = slug.replace(' (cr)', '')
    slug = slug.replace('\xe3', 'a').replace('\xe1', 'a').replace('\xe9', 'e').replace('\xfc', 'u')
    slug = slug.replace('\xfa', 'u').replace('\xed', 'i').replace('\xf3', 'o')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


def process_ranking_pages():
    """Add neighborhood hub links + salary-needed links to ranking pages."""
    pattern = os.path.join(ROOT, 'rankings', '*.html')
    files = glob.glob(pattern)
    updated = skipped = errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        if filename == 'index.html':
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            nhood_links = []
            for city in TOP_NEIGHBORHOOD_CITIES:
                slug = slugify(city)
                nhood_links.append(
                    '<a href="/city/' + slug + '/cheapest-neighborhoods" '
                    'class="similar-city-link cross-links-v1" '
                    'style="border-left: 3px solid #9fe870;">'
                    'Cheapest Neighborhoods in ' + city + '</a>'
                )
            salary_links = []
            for city in TOP_SALARY_CITIES:
                slug = slugify(city)
                salary_links.append(
                    '<a href="/salary-needed/' + slug + '" '
                    'class="similar-city-link cross-links-v1" '
                    'style="border-left: 3px solid #3b82f6;">'
                    'Salary Needed in ' + city + '</a>'
                )

            new_links_html = '\n                '.join(nhood_links + salary_links)

            anchor = '<a href="/city/" class="similar-city-link">All Cities</a>'
            if anchor in content:
                content = content.replace(anchor, new_links_html + '\n                ' + anchor, 1)
            else:
                anchor2 = '<a href="/rankings/" class="similar-city-link">All Rankings</a>'
                if anchor2 in content:
                    content = content.replace(anchor2, new_links_html + '\n                ' + anchor2, 1)
                else:
                    errors += 1
                    print('  WARN: No anchor found in ' + filename)
                    continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
        except Exception as e:
            errors += 1
            print('  ERROR: ' + filename + ': ' + str(e))

    return updated, skipped, errors


def process_compare_pages():
    """Add 'See all neighborhoods' links after Top 5 tables in compare pages."""
    pattern = os.path.join(ROOT, 'compare', '*.html')
    files = glob.glob(pattern)
    updated = skipped = errors = 0
    nhood_slugs = {slugify(c): c for c in NEIGHBORHOOD_CITIES}

    for filepath in files:
        filename = os.path.basename(filepath)
        if filename == 'index.html':
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue
            if '<h2>Neighborhoods</h2>' not in content:
                skipped += 1
                continue

            top5_pat = re.compile(
                r'(<h3 style="font-size:0\.95rem; margin-bottom:12px;">)(.*?) \(Top 5\)(</h3>)'
            )
            matches = list(top5_pat.finditer(content))
            if not matches:
                skipped += 1
                continue

            modified = False
            for match in reversed(matches):
                city_name = match.group(2)
                city_slug = slugify(city_name)
                if city_slug not in nhood_slugs:
                    continue

                close_pat = '</tbody></table></div>'
                close_pos = content.find(close_pat, match.end())
                if close_pos == -1:
                    continue
                insert_pos = close_pos + len(close_pat)

                link_html = (
                    '<div class="cross-links-v1" style="margin-top:8px;">'
                    '<a href="/city/' + city_slug + '/cheapest-neighborhoods" '
                    'style="font-size:0.8rem; color:#9fe870; text-decoration:none; font-weight:500;">'
                    'See all neighborhoods in ' + city_name + ' &rarr;</a></div>'
                )
                content = content[:insert_pos] + link_html + content[insert_pos:]
                modified = True

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print('  ERROR: ' + filename + ': ' + str(e))

    return updated, skipped, errors


def process_neighborhood_hub_pages():
    """Add ranking page links to neighborhood hub pages."""
    updated = skipped = errors = 0
    hub_pattern = os.path.join(ROOT, 'city', '*', '*-neighborhoods.html')
    files = glob.glob(hub_pattern)

    ranking_links = []
    for slug, title in RANKING_PAGES.items():
        ranking_links.append(
            '<a href="/rankings/' + slug + '" class="similar-city-link cross-links-v1">' + title + '</a>'
        )
    ranking_links_html = '\n                '.join(ranking_links)

    for filepath in files:
        relpath = os.path.relpath(filepath, ROOT)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            anchor = '<a href="/city/" class="similar-city-link">All Cities</a>'
            if anchor in content:
                content = content.replace(anchor, ranking_links_html + '\n                ' + anchor, 1)
            else:
                errors += 1
                print('  WARN: No anchor found in ' + relpath)
                continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
        except Exception as e:
            errors += 1
            print('  ERROR: ' + relpath + ': ' + str(e))

    return updated, skipped, errors


def process_city_pages():
    """Add quick-links card to city pages (top-level *.html only)."""
    pattern = os.path.join(ROOT, 'city', '*.html')
    files = glob.glob(pattern)
    updated = skipped = errors = 0
    nhood_slug_set = {slugify(c) for c in NEIGHBORHOOD_CITIES}

    for filepath in files:
        filename = os.path.basename(filepath)
        if filename == 'index.html':
            skipped += 1
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            m = re.search(r'<title>([^<]+?) Cost of Living', content)
            if not m:
                errors += 1
                print('  WARN: Could not extract city from ' + filename)
                continue

            city = m.group(1).strip()
            city_slug = slugify(city)
            links = []

            if city_slug in nhood_slug_set:
                links.append(
                    '<a href="/city/' + city_slug + '/cheapest-neighborhoods" '
                    'class="similar-city-link" style="border-left: 3px solid #9fe870;">'
                    'Cheapest Neighborhoods in ' + city + '</a>'
                )
                links.append(
                    '<a href="/city/' + city_slug + '/most-expensive-neighborhoods" '
                    'class="similar-city-link" style="border-left: 3px solid #9fe870;">'
                    'Most Expensive Neighborhoods in ' + city + '</a>'
                )

            links.append(
                '<a href="/salary-needed/' + city_slug + '" '
                'class="similar-city-link" style="border-left: 3px solid #3b82f6;">'
                'Salary Needed to Live in ' + city + '</a>'
            )
            for rslug, rtitle in [
                ('cheapest-cities', 'Cheapest Cities to Live In'),
                ('most-expensive-cities', 'Most Expensive Cities'),
                ('highest-salaries', 'Highest Salaries by City'),
                ('best-value-cities', 'Best Value Cities'),
            ]:
                links.append('<a href="/rankings/' + rslug + '" class="similar-city-link">' + rtitle + '</a>')

            links_html = '\n                '.join(links)
            card_html = (
                '        <section class="content-card cross-links-v1">\n'
                '            <h2>Quick Links</h2>\n'
                '            <div class="similar-cities">\n'
                '                ' + links_html + '\n'
                '            </div>\n'
                '        </section>\n\n'
            )

            anchor = '        <section class="content-card">\n            <h2>Explore Similar Cities</h2>'
            if anchor in content:
                content = content.replace(anchor, card_html + anchor, 1)
            else:
                footer_anchor = '        <footer class="page-footer">'
                if footer_anchor in content:
                    content = content.replace(footer_anchor, card_html + footer_anchor, 1)
                else:
                    errors += 1
                    print('  WARN: No anchor found in ' + filename)
                    continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
        except Exception as e:
            errors += 1
            print('  ERROR: ' + filename + ': ' + str(e))

    return updated, skipped, errors


def process_blog_articles():
    """Add Related Rankings links to blog articles."""
    pattern = os.path.join(ROOT, 'blog', 'articles', '*.html')
    files = glob.glob(pattern)
    updated = skipped = errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if MARKER in content:
                skipped += 1
                continue

            matched_rankings = []
            for keyword, rankings in BLOG_RANKING_MAP.items():
                if keyword == '_default':
                    continue
                if keyword in filename:
                    matched_rankings = rankings
                    break
            if not matched_rankings:
                matched_rankings = BLOG_RANKING_MAP['_default']

            ranking_links = []
            for rslug in matched_rankings:
                if rslug in RANKING_PAGES:
                    rtitle = RANKING_PAGES[rslug]
                    ranking_links.append(
                        '<a href="/rankings/' + rslug + '" '
                        'style="display:block;padding:12px 16px;background:var(--card-bg,#fff);'
                        'border:1px solid var(--border-light,#f0f0f2);border-left:3px solid #3b82f6;'
                        'border-radius:12px;text-decoration:none;color:var(--text-primary,#1d1d1f);'
                        'font-size:0.9rem;font-weight:500;transition:all 0.2s;">'
                        + rtitle + ' (2026)</a>'
                    )
            if not ranking_links:
                skipped += 1
                continue

            ranking_links_html = '\n            '.join(ranking_links)
            rankings_section = (
                '\n    <section class="cross-links-v1" style="margin-top:24px;">\n'
                '        <h2 style="font-size:1.1rem;font-weight:700;'
                'color:var(--text-primary,#1d1d1f);margin-bottom:16px;">Related Rankings</h2>\n'
                '        <div style="display:flex;flex-direction:column;gap:10px;">\n'
                '            ' + ranking_links_html + '\n'
                '        </div>\n'
                '    </section>'
            )

            ra_marker = '>Related Articles</h2>'
            ra_pos = content.find(ra_marker)
            if ra_pos != -1:
                close_pos = content.find('</section>', ra_pos)
                if close_pos != -1:
                    insert_pos = close_pos + len('</section>')
                    content = content[:insert_pos] + rankings_section + content[insert_pos:]
                else:
                    errors += 1
                    print('  WARN: No closing section after Related Articles in ' + filename)
                    continue
            else:
                footer_anchor = '<!-- Footer -->'
                if footer_anchor in content:
                    content = content.replace(footer_anchor, rankings_section + '\n\n    ' + footer_anchor, 1)
                else:
                    footer2 = '<footer>'
                    footer3 = '<footer class="page-footer">'
                    if footer2 in content:
                        content = content.replace(footer2, rankings_section + '\n\n    ' + footer2, 1)
                    elif footer3 in content:
                        content = content.replace(footer3, rankings_section + '\n\n        ' + footer3, 1)
                    else:
                        errors += 1
                        print('  WARN: No anchor found in ' + filename)
                        continue

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
        except Exception as e:
            errors += 1
            print('  ERROR: ' + filename + ': ' + str(e))

    return updated, skipped, errors


if __name__ == '__main__':
    print("Adding cross-links across all page types...")
    print()

    print("1. Ranking pages (adding neighborhood hub + salary-needed links)...")
    u1, s1, e1 = process_ranking_pages()
    print("   Updated: %d, Skipped: %d, Errors: %d" % (u1, s1, e1))

    print("2. Compare pages (adding 'See all neighborhoods' links)...")
    u2, s2, e2 = process_compare_pages()
    print("   Updated: %d, Skipped: %d, Errors: %d" % (u2, s2, e2))

    print("3. Neighborhood hub pages (adding ranking links)...")
    u3, s3, e3 = process_neighborhood_hub_pages()
    print("   Updated: %d, Skipped: %d, Errors: %d" % (u3, s3, e3))

    print("4. City pages (adding quick-links card)...")
    u4, s4, e4 = process_city_pages()
    print("   Updated: %d, Skipped: %d, Errors: %d" % (u4, s4, e4))

    print("5. Blog articles (adding related rankings)...")
    u5, s5, e5 = process_blog_articles()
    print("   Updated: %d, Skipped: %d, Errors: %d" % (u5, s5, e5))

    total_updated = u1 + u2 + u3 + u4 + u5
    total_skipped = s1 + s2 + s3 + s4 + s5
    total_errors = e1 + e2 + e3 + e4 + e5
    print()
    print("Total: %d updated, %d skipped, %d errors" % (total_updated, total_skipped, total_errors))
