#!/usr/bin/env python3
"""
Fix remaining "113 cities" and "100+ cities" references across city, compare, salary, blog pages.
Also fixes "of 113" ranking references and "#X/113" patterns.
Run AFTER fix-site-numbers.py which handled the neighborhood counts.
"""

import os
import re

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Simple string replacements
SIMPLE_REPLACEMENTS = [
    # City pages: stat label
    ('of 113 Cities', 'of 182 Cities'),
    # Compare/city body text: "out of 113 cities"
    ('out of 113 cities', 'out of 182 cities'),
    ('out of 113</strong> cities', 'out of 182</strong> cities'),
    # Compare body text: "ranked #X of 113 cities"
    ('of 113 cities)', 'of 182 cities)'),
    ('of 113 cities,', 'of 182 cities,'),
    ('of 113 cities.', 'of 182 cities.'),
    # Salary pages: "all 113 cities" should already be caught, but double check
    ('all 113 cities', 'all 182 cities'),
    # Salary-needed "100+ cities" remaining
    ('100+ cities', '182 cities'),
    # "Compare 37 professions across 113 cities"
    ('across 113 cities', 'across 182 cities'),
    # "113 cities ranked"
    ('113 cities ranked', '182 cities ranked'),
    # Blog index footer: remaining 101 references
    ('101 cities', '182 cities'),
    # "100 cities" without the +
    ('across 100 cities', 'across 182 cities'),
    ('Compare 100 cities', 'Compare 182 cities'),
]

# Regex replacements for patterns like "#6/113" and "Ranked #21/113"
REGEX_REPLACEMENTS = [
    # "#6/113" → "#6/182" in meta descriptions and share data
    (r'#(\d+)/113', r'#\1/182'),
    # "ranked #6 of 113" in body text
    (r'ranked #(\d+) of 113', r'ranked #\1 of 182'),
]

total_files_changed = 0
total_replacements = 0

for root, dirs, files in os.walk(PROJECT_DIR):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']

    for filename in files:
        if not filename.endswith('.html'):
            continue

        filepath = os.path.join(root, filename)
        rel_path = os.path.relpath(filepath, PROJECT_DIR)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        file_changes = 0

        # Simple replacements
        for old, new in SIMPLE_REPLACEMENTS:
            count = content.count(old)
            if count > 0:
                content = content.replace(old, new)
                file_changes += count

        # Regex replacements
        for pattern, replacement in REGEX_REPLACEMENTS:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                file_changes += len(matches)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            total_files_changed += 1
            total_replacements += file_changes

            if file_changes <= 3:
                print(f"📝 {rel_path} ({file_changes} fixes)")
            else:
                print(f"📝 {rel_path} ({file_changes} fixes)")

print(f"\n{'='*60}")
print(f"Files modified: {total_files_changed}")
print(f"Total replacements: {total_replacements}")

# Final verification
print(f"\n{'='*60}")
print("VERIFICATION — checking for remaining '113' references in key areas...")
print(f"{'='*60}")

remaining = 0
for root, dirs, files in os.walk(PROJECT_DIR):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
    for filename in files:
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(root, filename)
        rel_path = os.path.relpath(filepath, PROJECT_DIR)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for remaining problematic patterns
        for pattern in ['of 113 cities', 'of 113 Cities', '/113', 'out of 113',
                        '100+ cities', '101 cities',
                        '2,000+ neighborhoods', '2,100+ neighborhoods', '2,400+ neighborhoods']:
            if pattern in content:
                print(f"  ⚠️  {rel_path}: still contains '{pattern}'")
                remaining += 1

if remaining == 0:
    print("  ✅ All clean!")
else:
    print(f"\n  ⚠️  {remaining} remaining issues")
