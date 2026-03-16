#!/usr/bin/env python3
"""
SEO Title Optimization Script
1A: Remove "| salary:converter blog/Blog" and "— salary:converter" suffixes from blog post <title> tags
1B: Strengthen ranking page titles with "Full Ranking" and remove parentheses from year
"""

import os
import re
import glob

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DRY_RUN = False  # Set to True to preview changes without writing

# ============================================================
# PART 1A: Blog title cleanup
# ============================================================

blog_dir = os.path.join(PROJECT_DIR, 'blog', 'articles')
blog_files = glob.glob(os.path.join(blog_dir, '*.html'))

print("=" * 60)
print("PART 1A: Blog Title Cleanup")
print("=" * 60)

blog_changes = 0
for filepath in sorted(blog_files):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match the <title> tag
    title_match = re.search(r'<title>(.*?)</title>', content)
    if not title_match:
        print(f"  ⚠️  No <title> found in {filename}")
        continue

    old_title = title_match.group(1)

    # Remove suffix patterns:
    # " | salary:converter blog" (lowercase b)
    # " | salary:converter Blog" (uppercase B)
    # " — salary:converter"
    new_title = old_title
    new_title = re.sub(r'\s*\|\s*salary:converter\s*[Bb]log\s*$', '', new_title)
    new_title = re.sub(r'\s*[—–-]\s*salary:converter\s*$', '', new_title)

    if new_title != old_title:
        print(f"\n  📝 {filename}")
        print(f"     OLD: {old_title}")
        print(f"     NEW: {new_title}")
        print(f"     LEN: {len(old_title)} → {len(new_title)} chars")

        if not DRY_RUN:
            content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        blog_changes += 1
    else:
        print(f"  ✅ {filename} — no suffix found, skipping")

print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}Blog titles updated: {blog_changes}/{len(blog_files)}")

# ============================================================
# PART 1B: Ranking page title improvements
# ============================================================

print("\n" + "=" * 60)
print("PART 1B: Ranking Page Title Improvements")
print("=" * 60)

rankings_dir = os.path.join(PROJECT_DIR, 'rankings')

# Define specific title improvements for each ranking page
ranking_title_map = {
    'most-expensive-cities.html': {
        'old_title': 'Most Expensive Cities in the World (2026)',
        'new_title': 'Most Expensive Cities in the World 2026 — Full Ranking',
        'old_og': 'Most Expensive Cities in the World (2026)',
        'new_og': 'Most Expensive Cities in the World 2026 — Full Ranking',
    },
    'cheapest-cities.html': {
        'old_title': 'Cheapest Cities to Live In (2026)',
        'new_title': 'Cheapest Cities to Live In 2026 — Full Ranking',
        'old_og': 'Cheapest Cities to Live In (2026)',
        'new_og': 'Cheapest Cities to Live In 2026 — Full Ranking',
    },
    'highest-salaries.html': {
        'old_title': 'Cities with the Highest Salaries (2026)',
        'new_title': 'Cities with the Highest Salaries 2026 — Full Ranking',
        'old_og': 'Cities with the Highest Salaries (2026)',
        'new_og': 'Cities with the Highest Salaries 2026 — Full Ranking',
    },
    'cheapest-rent.html': {
        'old_title': 'Cities with the Cheapest Rent (2026)',
        'new_title': 'Cities with the Cheapest Rent 2026 — Full Ranking',
        'old_og': 'Cities with the Cheapest Rent (2026)',
        'new_og': 'Cities with the Cheapest Rent 2026 — Full Ranking',
    },
    'lowest-taxes.html': {
        'old_title': 'Cities with the Lowest Taxes (2026)',
        'new_title': 'Cities with the Lowest Taxes 2026 — Full Ranking',
        'old_og': 'Cities with the Lowest Taxes (2026)',
        'new_og': 'Cities with the Lowest Taxes 2026 — Full Ranking',
    },
    'best-value-cities.html': {
        'old_title': 'Best Value Cities to Live In (2026)',
        'new_title': 'Best Value Cities to Live In 2026 — Full Ranking',
        'old_og': 'Best Value Cities to Live In (2026)',
        'new_og': 'Best Value Cities to Live In 2026 — Full Ranking',
    },
    'cheapest-for-families.html': {
        'old_title': 'Cheapest Cities for Families (2026)',
        'new_title': 'Cheapest Cities for Families 2026 — Full Ranking',
        'old_og': 'Cheapest Cities for Families (2026)',
        'new_og': 'Cheapest Cities for Families 2026 — Full Ranking',
    },
    'index.html': {
        'old_title': 'City Rankings (2026) | salary:converter',
        'new_title': 'City Rankings 2026 — Compare 113 Cities',
        'old_og': 'City Rankings (2026) | salary:converter',
        'new_og': 'City Rankings 2026 — Compare 113 Cities',
    },
}

ranking_changes = 0
for filename, changes in ranking_title_map.items():
    filepath = os.path.join(rankings_dir, filename)
    if not os.path.exists(filepath):
        print(f"  ⚠️  {filename} not found, skipping")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    modified = False

    # Update <title>
    if changes['old_title'] in content:
        content = content.replace(
            f"<title>{changes['old_title']}</title>",
            f"<title>{changes['new_title']}</title>"
        )
        modified = True

    # Update og:title
    if changes['old_og'] in content:
        content = content.replace(
            f'content="{changes["old_og"]}"',
            f'content="{changes["new_og"]}"'
        )
        modified = True

    # Also update twitter:title if present
    if f'content="{changes["old_og"]}"' in original_content:
        # Already handled above since og and twitter usually match
        pass

    if modified:
        print(f"\n  📝 {filename}")
        print(f"     TITLE: {changes['old_title']}")
        print(f"         → {changes['new_title']} ({len(changes['new_title'])} chars)")

        if not DRY_RUN:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        ranking_changes += 1
    else:
        print(f"  ⚠️  {filename} — old title not found in content")

print(f"\n{'[DRY RUN] ' if DRY_RUN else ''}Ranking titles updated: {ranking_changes}/{len(ranking_title_map)}")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Blog titles cleaned: {blog_changes}")
print(f"  Ranking titles improved: {ranking_changes}")
print(f"  Total files modified: {blog_changes + ranking_changes}")
if DRY_RUN:
    print("\n  ⚠️  DRY RUN — no files were actually modified")
    print("  Set DRY_RUN = False to apply changes")
