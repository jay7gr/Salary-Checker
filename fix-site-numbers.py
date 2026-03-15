#!/usr/bin/env python3
"""
Fix inconsistent neighborhood and city counts across the entire site.

Actual data: 3,418 neighborhoods across 182 cities (88 countries, 67 currencies)
Found variants: "2,000+", "2,100+", "2,400+", "2,483", "113 cities", "101 cities", "100+ cities", "180+ cities"
Target: All should say "3,400+" neighborhoods and "182 cities"
"""

import os
import re
import glob

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Patterns to fix (order matters — most specific first)
REPLACEMENTS = [
    # Neighborhood counts — all variants → "3,400+"
    # Must handle both with and without "+" suffix
    ('2,483 neighborhoods', '3,400+ neighborhoods'),
    ('2,400+ neighborhoods', '3,400+ neighborhoods'),
    ('2,400 neighborhoods', '3,400+ neighborhoods'),
    ('2,100+ neighborhoods', '3,400+ neighborhoods'),
    ('2,000+ neighborhoods', '3,400+ neighborhoods'),

    # "over 2,400 neighborhoods" pattern (embed.html)
    ('over 2,400 neighborhoods', '3,400+ neighborhoods'),

    # "2,400+ neighborhood adjustments" pattern (city/compare pages)
    ('2,400+ neighborhood adjustments', '3,400+ neighborhood adjustments'),
    ('2,400+ neighborhood-level adjustments', '3,400+ neighborhood-level adjustments'),

    # "2,000+ neighborhood-level" pattern (index.html JSON-LD)
    ('2,000+ neighborhood-level', '3,400+ neighborhood-level'),

    # "2,000+ locations" pattern (salary-needed)
    ('2,000+ locations', '3,400+ locations'),

    # "Browse all 2,100+ neighborhoods" (index.html link)
    ('Browse all 2,100+ neighborhoods', 'Browse all 3,400+ neighborhoods'),

    # "2,483 neighborhoods across 101 cities" (blog article about neighborhoods)
    ('2,483 neighborhoods across 101 cities', '3,400+ neighborhoods across 182 cities'),

    # City counts — all variants → "182 cities"
    # Be careful not to replace "113 cities" inside article content that specifically references 113 as a data point
    # The rankings pages legitimately show 113 cities in their ranking tables
    # But meta tags, CTAs, footers, and hero text should say 182

    # Specific patterns that should definitely be updated:
    ('Compare 113 cities and', 'Compare 182 cities and'),
    ('across 113 cities and', 'across 182 cities and'),
    ('across 113 cities worldwide', 'across 182 cities worldwide'),
    ('for 113 cities worldwide', 'for 182 cities worldwide'),
    ('across 101 cities and', 'across 182 cities and'),
    ('across 101 cities with', 'across 182 cities with'),
    ('across 100+ cities with', 'across 182 cities with'),
    ('across 100+ cities', 'across 182 cities'),
    ('in 180+ cities', 'in 182 cities'),
    ('covering 180+ cities', 'covering 182 cities'),
    ('Compare 100+ cities', 'Compare 182 cities'),
    ('Browse all 100+ cities', 'Browse all 182 cities'),

    # "for 113 cities" in salary page descriptions
    ('for 113 cities', 'for 182 cities'),

    # "in 113 cities worldwide" pattern
    ('in 113 cities worldwide', 'in 182 cities worldwide'),

    # "in 113 cities" general (salary pages hero, FAQs, data notes)
    ('in 113 cities after', 'in 182 cities after'),
    ('in 113 cities.', 'in 182 cities.'),

    # "all 113 cities" pattern (FAQ answers)
    ('all 113 cities', 'all 182 cities'),

    # "113 cities ranked" pattern
    ('113 cities ranked', '182 cities ranked'),

    # "113 cities" in salary page meta descriptions: "earn in 113 cities worldwide"
    ('earn in 113 cities', 'earn in 182 cities'),

    # Blog footer: "101 cities and 2,100+ neighborhoods"
    ('101 cities and 2,100+ neighborhoods', '182 cities and 3,400+ neighborhoods'),

    # About page body text
    ('113 cities and 2,400+ neighborhoods worldwide', '182 cities and 3,400+ neighborhoods worldwide'),
    ('113 cities and 2,400+ neighborhoods', '182 cities and 3,400+ neighborhoods'),

    # Widget page: "Covers 113 cities"
    ('Covers 113 cities', 'Covers 182 cities'),

    # "Data covers 113 cities"
    ('Data covers 113 cities', 'Data covers 182 cities'),

    # "Compare 37 professions across 113 cities" (salary index page)
    ('across 113 cities', 'across 182 cities'),
]

# Count changes
total_files_changed = 0
total_replacements = 0
changes_by_file = {}

# Process all HTML files recursively
for root, dirs, files in os.walk(PROJECT_DIR):
    # Skip hidden dirs, node_modules, .git
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']

    for filename in files:
        if not filename.endswith('.html'):
            continue

        filepath = os.path.join(root, filename)
        rel_path = os.path.relpath(filepath, PROJECT_DIR)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        file_changes = []

        for old, new in REPLACEMENTS:
            count = content.count(old)
            if count > 0:
                content = content.replace(old, new)
                file_changes.append(f"  {old!r} → {new!r} ({count}x)")
                total_replacements += count

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            total_files_changed += 1
            changes_by_file[rel_path] = file_changes

            if len(file_changes) <= 5:
                print(f"📝 {rel_path}")
                for c in file_changes:
                    print(f"   {c}")
            else:
                print(f"📝 {rel_path} ({len(file_changes)} patterns fixed)")

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Files modified: {total_files_changed}")
print(f"Total replacements: {total_replacements}")

# Verify no old patterns remain
print(f"\n{'='*60}")
print("VERIFICATION — checking for remaining old patterns...")
print(f"{'='*60}")

check_patterns = [
    '2,000+ neighborhoods',
    '2,100+ neighborhoods',
    '2,400+ neighborhoods',
    '2,400 neighborhoods',
    'over 2,400 neighborhoods',
    '2,483 neighborhoods',
    '2,400+ neighborhood adjustments',
    '2,400+ neighborhood-level',
    '2,000+ neighborhood-level',
    '2,100+ neighborhood',
    'in 180+ cities',
    '101 cities and',
    'Browse all 100+',
    'Browse all 2,100+',
]

remaining_issues = 0
for root, dirs, files in os.walk(PROJECT_DIR):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
    for filename in files:
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(root, filename)
        rel_path = os.path.relpath(filepath, PROJECT_DIR)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        for pattern in check_patterns:
            if pattern in content:
                print(f"  ⚠️  {rel_path}: still contains '{pattern}'")
                remaining_issues += 1

if remaining_issues == 0:
    print("  ✅ All clean — no old patterns found!")
else:
    print(f"\n  ⚠️  {remaining_issues} remaining issues found")
