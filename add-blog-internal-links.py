#!/usr/bin/env python3
"""
Add "Explore the Data" internal link sections to blog articles.
Inserts a styled section with relevant internal links just before the <footer> tag.
Idempotent: skips files that already contain the section.
"""

import os
import re

BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog', 'articles')

# Map of article slug -> list of (href, label)
ARTICLE_LINKS = {
    'london-vs-new-york-true-cost-comparison': [
        ('/compare/london-vs-new-york', 'London vs New York'),
        ('/city/london', 'London Cost of Living'),
        ('/city/new-york', 'New York Cost of Living'),
    ],
    'most-expensive-cities-in-the-world-2026': [
        ('/city/zurich', 'Zurich Cost of Living'),
        ('/city/new-york', 'New York Cost of Living'),
        ('/city/singapore', 'Singapore Cost of Living'),
        ('/city/hong-kong', 'Hong Kong Cost of Living'),
        ('/city/london', 'London Cost of Living'),
        ('/rankings/most-expensive-cities', 'Most Expensive Cities Rankings'),
    ],
    'average-salary-by-city-2026-global-comparison': [
        ('/city/san-francisco', 'San Francisco Cost of Living'),
        ('/city/zurich', 'Zurich Cost of Living'),
        ('/city/new-york', 'New York Cost of Living'),
        ('/rankings/highest-salaries', 'Highest Salaries Rankings'),
    ],
    'dubai-vs-singapore-expat-comparison': [
        ('/compare/dubai-vs-singapore', 'Dubai vs Singapore'),
        ('/city/dubai', 'Dubai Cost of Living'),
        ('/city/singapore', 'Singapore Cost of Living'),
    ],
    'affordable-cities-in-europe-for-americans-2026': [
        ('/city/lisbon', 'Lisbon Cost of Living'),
        ('/city/barcelona', 'Barcelona Cost of Living'),
        ('/city/berlin', 'Berlin Cost of Living'),
        ('/city/budapest', 'Budapest Cost of Living'),
        ('/city/bucharest', 'Bucharest Cost of Living'),
        ('/rankings/cheapest-cities', 'Cheapest Cities Rankings'),
    ],
    'cost-of-living-southeast-asia-digital-nomads-2026': [
        ('/city/bangkok', 'Bangkok Cost of Living'),
        ('/city/bali', 'Bali Cost of Living'),
        ('/city/ho-chi-minh-city', 'Ho Chi Minh City Cost of Living'),
        ('/city/kuala-lumpur', 'Kuala Lumpur Cost of Living'),
    ],
    'tech-salary-comparison-by-city-2026': [
        ('/city/san-francisco', 'San Francisco Cost of Living'),
        ('/city/seattle', 'Seattle Cost of Living'),
        ('/city/london', 'London Cost of Living'),
        ('/city/berlin', 'Berlin Cost of Living'),
        ('/city/bangalore', 'Bangalore Cost of Living'),
    ],
    'top-10-cities-for-remote-workers-2026': [
        ('/city/lisbon', 'Lisbon Cost of Living'),
        ('/city/bangkok', 'Bangkok Cost of Living'),
        ('/city/bali', 'Bali Cost of Living'),
        ('/city/buenos-aires', 'Buenos Aires Cost of Living'),
        ('/city/mexico-city', 'Mexico City Cost of Living'),
    ],
    'how-cost-of-living-affects-your-salary': [
        ('/compare/london-vs-new-york', 'London vs New York'),
        ('/compare/san-francisco-vs-austin', 'San Francisco vs Austin'),
    ],
    'what-is-a-good-salary-by-city-2026': [
        ('/city/new-york', 'New York Cost of Living'),
        ('/city/london', 'London Cost of Living'),
        ('/city/tokyo', 'Tokyo Cost of Living'),
        ('/city/dubai', 'Dubai Cost of Living'),
    ],
    'cost-of-living-adjustment-cola-guide-2026': [
        ('/city/san-francisco', 'San Francisco Cost of Living'),
        ('/city/new-york', 'New York Cost of Living'),
        ('/city/seattle', 'Seattle Cost of Living'),
    ],
    'geographic-pay-differentials-remote-workers-2026': [
        ('/compare/san-francisco-vs-austin', 'San Francisco vs Austin'),
        ('/compare/new-york-vs-miami', 'New York vs Miami'),
        ('/city/denver', 'Denver Cost of Living'),
    ],
    'salary-negotiation-when-relocating-abroad': [
        ('/compare/london-vs-dubai', 'London vs Dubai'),
        ('/compare/new-york-vs-singapore', 'New York vs Singapore'),
        ('/salary-needed/london', 'Salary Needed in London'),
    ],
    'purchasing-power-parity-explained': [
        ('/compare/london-vs-new-york', 'London vs New York'),
        ('/compare/tokyo-vs-bangkok', 'Tokyo vs Bangkok'),
        ('/city/zurich', 'Zurich Cost of Living'),
    ],
    'currency-exchange-rates-impact-take-home-pay-abroad': [
        ('/city/london', 'London Cost of Living'),
        ('/city/tokyo', 'Tokyo Cost of Living'),
        ('/city/zurich', 'Zurich Cost of Living'),
    ],
    '50-most-undervalued-neighborhoods-in-the-world': [
        ('/city/london', 'London Cost of Living'),
        ('/city/new-york', 'New York Cost of Living'),
        ('/city/paris', 'Paris Cost of Living'),
        ('/rankings/cheapest-rent', 'Cheapest Rent Rankings'),
    ],
    'real-cost-of-living-major-cities-neighborhood-breakdown': [
        ('/city/london', 'London Cost of Living'),
        ('/city/new-york', 'New York Cost of Living'),
        ('/city/paris', 'Paris Cost of Living'),
        ('/city/tokyo', 'Tokyo Cost of Living'),
    ],
    'where-your-salary-goes-furthest-neighborhood-edition': [
        ('/city/london', 'London Cost of Living'),
        ('/city/new-york', 'New York Cost of Living'),
        ('/rankings/best-value-cities', 'Best Value Cities Rankings'),
    ],
    # Retire blog posts
    'how-to-retire-abroad-cost-of-living-guide': [
        ('/retire/', 'Retire Abroad Tool'),
        ('/retire/city/lisbon', 'Retire in Lisbon'),
        ('/retire/city/bangkok', 'Retire in Bangkok'),
        ('/retire/city/medellin', 'Retire in Medell\u00edn'),
    ],
    'retire-on-2000-a-month-abroad-best-cities': [
        ('/retire/', 'Retire Abroad Tool'),
        ('/retire/city/chiang-mai', 'Retire in Chiang Mai'),
        ('/retire/city/medellin', 'Retire in Medell\u00edn'),
        ('/retire/city/da-nang', 'Retire in Da Nang'),
    ],
    'easiest-retirement-visas-2026': [
        ('/retire/', 'Retire Abroad Tool'),
        ('/retire/visa/', 'Retirement Visa Guide'),
        ('/retire/city/lisbon', 'Retire in Lisbon'),
        ('/retire/city/panama-city', 'Retire in Panama City'),
    ],
    'retire-abroad-social-security-only': [
        ('/retire/', 'Retire Abroad Tool'),
        ('/retire/city/bangkok', 'Retire in Bangkok'),
        ('/retire/city/medellin', 'Retire in Medell\u00edn'),
    ],
    'best-retirement-healthcare-countries-2026': [
        ('/retire/', 'Retire Abroad Tool'),
        ('/retire/city/lisbon', 'Retire in Lisbon'),
        ('/retire/city/bangkok', 'Retire in Bangkok'),
    ],
    'inheritance-tax-expats-retire-abroad': [
        ('/retire/', 'Retire Abroad Tool'),
        ('/retire/city/dubai', 'Retire in Dubai'),
        ('/retire/city/panama-city', 'Retire in Panama City'),
    ],
}


def build_section(links):
    """Build the HTML section with link buttons."""
    link_html_parts = []
    for href, label in links:
        link_html_parts.append(
            f'        <a href="{href}" style="display: inline-block; padding: 8px 16px; '
            f'background: var(--accent, #2563eb); color: #fff; border-radius: 8px; '
            f'text-decoration: none; font-size: 0.9rem;">{label}</a>'
        )
    links_joined = '\n'.join(link_html_parts)
    return f'''<section class="related-tools" style="max-width:800px;margin: 48px auto 0; padding: 32px; background: var(--stat-card-bg, #f5f5f7); border-radius: 16px;">
    <h3 style="margin: 0 0 16px; font-size: 1.2rem; color: var(--text-primary, #1d1d1f);">Explore the Data</h3>
    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
{links_joined}
    </div>
</section>
'''


def process_file(filepath, slug):
    """Add related-tools section to a blog article. Returns True if modified."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Idempotency check
    if 'related-tools' in content:
        return False

    links = ARTICLE_LINKS.get(slug)
    if not links:
        return False

    section_html = build_section(links)

    # Insert before the <footer tag
    footer_match = re.search(r'^(\s*<footer[\s>])', content, re.MULTILINE)
    if not footer_match:
        print(f"  WARNING: No <footer> tag found in {slug}")
        return False

    insert_pos = footer_match.start()
    content = content[:insert_pos] + section_html + content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    updated = 0
    skipped = 0
    not_found = 0

    for slug in sorted(ARTICLE_LINKS.keys()):
        filename = slug + '.html'
        filepath = os.path.join(BLOG_DIR, filename)

        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {filename}")
            not_found += 1
            continue

        if process_file(filepath, slug):
            print(f"  UPDATED: {filename}")
            updated += 1
        else:
            print(f"  SKIPPED (already has section): {filename}")
            skipped += 1

    print(f"\nDone. Updated: {updated}, Skipped: {skipped}, Not found: {not_found}")


if __name__ == '__main__':
    main()
