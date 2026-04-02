#!/usr/bin/env python3
"""
fix-ctr-meta.py
Rewrites <title> and <meta name="description"> for the top-impression pages
to improve CTR. Each entry is (filepath, new_title, new_description).
Idempotent: skips files where the new title is already present.
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    # (relative_path, new_title, new_description)

    # 1. Homepage — 607 imp, 1.2% CTR, pos 7.1
    (
        "index.html",
        "Salary Converter 2026: Is Your Pay Worth the Same Elsewhere?",
        "Find out how far your salary really goes. Compare take-home pay, rent, and cost of living across 182 cities and 3,400+ neighborhoods. Free, instant results.",
    ),

    # 2. /city/ hub — 599 imp, 0% CTR, pos 7.4 (title wrongly said 113 cities)
    (
        "city/index.html",
        "Cost of Living by City 2026 — Compare 182 Cities Worldwide",
        "Explore cost of living data for 182 cities worldwide. Compare rent, salaries, taxes, and neighborhood breakdowns — find out where your money goes furthest.",
    ),

    # 3. Average salary by city blog — 577 imp, 0.2% CTR, pos 5.9
    (
        "blog/articles/average-salary-by-city-2026-global-comparison.html",
        "Average Salary by City 2026: Which Cities Pay the Most?",
        "See average salaries across 182 cities — ranked by pay, cost of living, and real purchasing power. Discover where $80K actually feels like $120K.",
    ),

    # 4. London vs New York blog — 397 imp, 0.8% CTR, pos 8.8
    (
        "blog/articles/london-vs-new-york-true-cost-comparison.html",
        "London vs New York 2026: Which City Is Really More Expensive?",
        "London or New York — the answer might surprise you. We break down rent, taxes, take-home pay, and hidden costs for singles and families in 2026.",
    ),

    # 5. What is a good salary — 273 imp, 0% CTR, pos 7.0
    (
        "blog/articles/what-is-a-good-salary-by-city-2026.html",
        "What Is a Good Salary in 2026? 50 Cities, Real Numbers",
        "$80K is comfortable in Bangkok but barely middle class in San Francisco. See what a genuinely good salary looks like in 50+ cities — with neighborhood breakdowns.",
    ),

    # 6. Most expensive cities — 255 imp, 0.8% CTR, pos 7.8
    (
        "blog/articles/most-expensive-cities-in-the-world-2026.html",
        "Most Expensive Cities in the World 2026 — The Full Ranking",
        "Zurich, Singapore, NYC — but which city is truly the priciest in 2026? Full top-25 ranking with rent, groceries, and the salary you'd need to live comfortably.",
    ),

    # 7. /compare/ hub — 232 imp, 0% CTR, pos 8.3
    (
        "compare/index.html",
        "Compare Cost of Living Between Any Two Cities — 6,000+ Pairs",
        "Pick any two cities and instantly compare rent, take-home pay, taxes, and purchasing power. Over 6,000 city pairs with neighborhood-level data.",
    ),

    # 8. Austin vs Denver — 199 imp, 0% CTR, pos 5.6 (excellent position!)
    (
        "compare/austin-vs-denver.html",
        "Austin vs Denver 2026: Which City Is Cheaper to Live In?",
        "Austin vs Denver — rent, taxes, and salaries compared side by side. Denver is 1% pricier overall, but the neighborhood-level gaps are much bigger. See the full breakdown.",
    ),

    # 9. Dubai vs Singapore blog — 142 imp, 0% CTR, pos 19.2
    (
        "blog/articles/dubai-vs-singapore-expat-comparison.html",
        "Dubai vs Singapore for Expats 2026: Tax, Salary & Lifestyle",
        "Zero tax in Dubai vs. world-class infrastructure in Singapore — which is the better expat move in 2026? Salary, cost of living, and quality of life compared.",
    ),

    # 10. Hong Kong vs Shenzhen — 133 imp, 0% CTR, pos 4.7 (top of page 1!)
    (
        "compare/hong-kong-vs-shenzhen.html",
        "Hong Kong vs Shenzhen 2026: How Big Is the Cost Difference?",
        "Shenzhen is 43% cheaper than Hong Kong — but what does that mean for your salary and lifestyle? Full rent, tax, and purchasing power comparison for 2026.",
    ),

    # 11. Shanghai vs Tokyo — 125 imp, 0% CTR, pos 9.3
    (
        "compare/shanghai-vs-tokyo.html",
        "Shanghai vs Tokyo Cost of Living 2026: Which Is Cheaper?",
        "Shanghai is 40% cheaper than Tokyo — but salaries differ too. See real rent, taxes, and take-home pay for expats and locals in both cities.",
    ),

    # 12. London vs New York compare page — 118 imp, 0% CTR, pos 9.0
    (
        "compare/london-vs-new-york.html",
        "London vs New York Cost of Living 2026: The Numbers Don't Lie",
        "NYC rent runs $3,500/mo vs £2,500 in London — but factor in taxes and the gap narrows fast. Full salary-equivalent breakdown for singles and families.",
    ),

    # 13. Dubai vs San Francisco — 117 imp, 0% CTR, pos 5.6 (page 1!)
    (
        "compare/dubai-vs-san-francisco.html",
        "Dubai vs San Francisco 2026: Is Dubai Really 26% Cheaper?",
        "Dubai's 0% income tax vs San Francisco's 13%+ — the real cost difference is massive. Full rent, salary, and lifestyle comparison for 2026.",
    ),

    # 14. Salary negotiation abroad blog — 113 imp, 0% CTR, pos 40.6
    (
        "blog/articles/salary-negotiation-when-relocating-abroad.html",
        "How to Negotiate Your Salary When Moving Abroad (2026 Guide)",
        "Don't accept the first offer when relocating internationally. Learn how to negotiate COLA adjustments, tax equalization, and currency protection — with real scripts and examples.",
    ),

    # 15. City: Hong Kong — 108 imp, 0% CTR, pos 7.6
    (
        "city/hong-kong.html",
        "Cost of Living in Hong Kong 2026: Rent, Salary & Neighborhoods",
        "1BR rent from $2,500/mo in Hong Kong. See what salary you'd need in 22 neighborhoods — from The Peak to Quarry Bay — with full tax and grocery breakdowns.",
    ),

    # 16. LA vs Toronto — 102 imp, 1% CTR, pos 7.3
    (
        "compare/los-angeles-vs-toronto.html",
        "Los Angeles vs Toronto 2026: Why Toronto Is 18% Cheaper",
        "Los Angeles vs Toronto — $2,400 vs $2,000/mo rent, but tax differences make the gap even larger. Full cost of living and salary comparison for 2026.",
    ),

    # 17. City: Santiago — 98 imp, 0% CTR, pos 12.6
    (
        "city/santiago.html",
        "Cost of Living in Santiago 2026: Cheap, But By How Much?",
        "1BR rent from just $550/mo in Santiago. See the salary you'd need across 19 neighborhoods — Vitacura to Bellavista — with taxes and grocery costs included.",
    ),

    # 18. Melbourne vs Sydney — 92 imp, 0% CTR, pos 16.1
    (
        "compare/melbourne-vs-sydney.html",
        "Melbourne vs Sydney 2026: Which Australian City Is Cheaper?",
        "Melbourne is 8% cheaper than Sydney — but the difference varies hugely by neighborhood. Full rent, salary, and tax comparison for 2026.",
    ),

    # 19. Copenhagen vs London — 88 imp, 0% CTR, pos 8.8
    (
        "compare/copenhagen-vs-london.html",
        "Copenhagen vs London 2026: High Tax vs High Rent — Who Wins?",
        "Copenhagen rents are lower, but Denmark's taxes are higher. Which city leaves more in your pocket? Full cost of living and salary comparison for 2026.",
    ),

    # 20. Miami vs Montreal — 82 imp, 0% CTR, pos 4.6 (top of page 1!)
    (
        "compare/miami-vs-montreal.html",
        "Miami vs Montreal 2026: Montreal Is 35% Cheaper — Here's Why",
        "Miami vs Montreal — $2,500 vs $1,400/mo rent, zero state tax vs Canadian rates. Find out which city wins for your budget and lifestyle in 2026.",
    ),

    # 21. London vs LA — 75 imp, 1.3% CTR, pos 6.7
    (
        "compare/london-vs-los-angeles.html",
        "London vs Los Angeles 2026: Which City Is Actually Cheaper?",
        "LA is 13% cheaper than London overall — but UK taxes vs California taxes tell a different story. Full salary-equivalent and neighborhood breakdown for 2026.",
    ),

    # 22. City: Toronto — 69 imp, 1.4% CTR, pos 11.9
    (
        "city/toronto.html",
        "Cost of Living in Toronto 2026: What Salary Do You Actually Need?",
        "You need C$131,512/yr to live comfortably in Toronto. See rent and salary data for 24 neighborhoods — from Yorkville to North York — with taxes included.",
    ),

    # 23. City: Munich — 66 imp, 0% CTR, pos 45.2 (too deep — skip for now)
    # Skipping Munich as position 45 means it's page 5 — title/meta won't help much
]


def fix_file(rel_path, new_title, new_desc):
    filepath = os.path.join(BASE, rel_path)
    if not os.path.exists(filepath):
        print(f"  NOT FOUND: {rel_path}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Idempotency check
    if new_title in html:
        print(f"  SKIP (already done): {rel_path}")
        return False

    # Replace <title>...</title>
    new_html = re.sub(
        r"<title>[^<]*</title>",
        f"<title>{new_title}</title>",
        html,
        count=1,
    )

    # Replace meta description content
    new_html = re.sub(
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        rf'\g<1>{new_desc}\g<2>',
        new_html,
        count=1,
    )
    # Also handle reversed attribute order
    new_html = re.sub(
        r'(<meta\s+content=")[^"]*("\s+name="description")',
        rf'\g<1>{new_desc}\g<2>',
        new_html,
        count=1,
    )

    # Update og:title
    new_html = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf'\g<1>{new_title}\g<2>',
        new_html,
        count=1,
    )

    # Update og:description
    new_html = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        rf'\g<1>{new_desc}\g<2>',
        new_html,
        count=1,
    )

    # Update twitter:title
    new_html = re.sub(
        r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")',
        rf'\g<1>{new_title}\g<2>',
        new_html,
        count=1,
    )

    # Update twitter:description
    new_html = re.sub(
        r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")',
        rf'\g<1>{new_desc}\g<2>',
        new_html,
        count=1,
    )

    if new_html == html:
        print(f"  NO CHANGE (pattern not matched): {rel_path}")
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"  OK: {rel_path}")
    return True


def main():
    print(f"Fixing CTR meta for {len(PAGES)} pages...\n")
    updated = skipped = 0
    for rel_path, title, desc in PAGES:
        if fix_file(rel_path, title, desc):
            updated += 1
        else:
            skipped += 1
    print(f"\nDone. {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    main()
