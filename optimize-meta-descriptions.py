#!/usr/bin/env python3
"""
Optimize meta descriptions for ranking pages.
Current descriptions are too short (90-110 chars). Optimal is 150-160 chars.
Also updates og:description to match.
"""

import os
import re

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Ranking page meta description improvements
# Current descriptions are ~90 chars, optimal is 150-160
updates = {
    'rankings/most-expensive-cities.html': {
        'old': 'The 113 most expensive cities ranked by cost of living. Compare rent, taxes &amp; salaries. Updated 2026.',
        'new': 'The 113 most expensive cities in the world, ranked by cost of living index. Compare rent, taxes, salaries &amp; neighborhoods side by side. Free, updated for 2026.',
    },
    'rankings/cheapest-cities.html': {
        'old': 'Ranked: the 113 cheapest cities to live in worldwide. Compare cost of living, rent &amp; salaries. Updated 2026.',
        'new': 'The 113 cheapest cities to live in worldwide, ranked by cost of living index. Compare rent, salaries &amp; quality of life. Find where your money goes furthest in 2026.',
    },
    'rankings/highest-salaries.html': {
        'old': 'Which cities offer the highest salaries? 113 cities ranked by comfortable salary. Updated 2026.',
        'new': 'Which cities pay the highest salaries in 2026? 113 cities ranked by comfortable salary, adjusted for cost of living. Compare take-home pay after taxes &amp; rent.',
    },
    'rankings/cheapest-rent.html': {
        'old': 'Find the cheapest rent worldwide. 113 cities ranked by 1-bedroom apartment rent. Updated 2026.',
        'new': 'Find the cheapest rent worldwide in 2026. 113 cities ranked by 1-bedroom apartment rent in USD. Compare rent costs across every major city, updated monthly.',
    },
    'rankings/lowest-taxes.html': {
        'old': 'Find cities with the lowest tax rates. 113 cities ranked by effective tax rate. Updated 2026.',
        'new': 'Find cities with the lowest tax rates in 2026. 113 cities ranked by effective income tax rate. Compare tax brackets, deductions &amp; take-home pay worldwide.',
    },
    'rankings/best-value-cities.html': {
        'old': 'Best value cities worldwide: lowest salary-to-cost ratio. 113 cities ranked. Updated 2026.',
        'new': 'Best value cities to live in 2026: where salaries go furthest relative to cost of living. 113 cities ranked by salary-to-cost ratio with rent &amp; tax data.',
    },
    'rankings/cheapest-for-families.html': {
        'old': 'Find the cheapest cities for families. 113 cities ranked by family living costs. Updated 2026.',
        'new': 'Find the cheapest cities for families in 2026. 113 cities ranked by family living costs including rent, childcare, groceries &amp; taxes. Compare family budgets.',
    },
    'rankings/index.html': {
        'old': 'Explore 7 city ranking lists: cheapest cities, highest salaries, lowest taxes, best value &amp; more. Updated 2026.',
        'new': 'Explore 7 city ranking lists for 2026: cheapest cities, highest salaries, lowest taxes, best value, cheapest rent &amp; more. 113 cities compared across every metric.',
    },
}

print("Optimizing ranking page meta descriptions...")
print("=" * 60)

changes = 0
for rel_path, desc in updates.items():
    filepath = os.path.join(PROJECT_DIR, rel_path)
    if not os.path.exists(filepath):
        print(f"  ⚠️  {rel_path} not found")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Update meta description
    old_meta = f'<meta name="description" content="{desc["old"]}">'
    new_meta = f'<meta name="description" content="{desc["new"]}">'
    if old_meta in content:
        content = content.replace(old_meta, new_meta)
        modified = True

    # Also update og:description if it matches the old description
    old_og = f'content="{desc["old"]}"'
    new_og = f'content="{desc["new"]}"'
    # Count occurrences — should be 2 (meta description + og:description)
    if content.count(old_og) > 0:
        content = content.replace(old_og, new_og)
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n  📝 {rel_path}")
        print(f"     OLD ({len(desc['old'])} chars): {desc['old'][:80]}...")
        print(f"     NEW ({len(desc['new'])} chars): {desc['new'][:80]}...")
        changes += 1
    else:
        print(f"  ⚠️  {rel_path} — old description not found")

print(f"\n{'=' * 60}")
print(f"Updated: {changes}/{len(updates)} ranking page descriptions")
