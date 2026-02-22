#!/usr/bin/env python3
"""Strip .html from internal URL references in generator scripts.

Handles both literal paths and f-string template patterns like:
  /city/{slug}.html  →  /city/{slug}
  /compare/{slug1}-vs-{slug2}.html  →  /compare/{slug1}-vs-{slug2}
"""
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for fname in ['generate-pages.py', 'generate-salary-needed.py']:
    filepath = os.path.join(BASE_DIR, fname)
    with open(filepath, 'r') as f:
        content = f.read()

    old_count = content.count('.html')

    # Pattern 1: Literal paths like /city/london.html
    new_content = re.sub(
        r"(/(?:city|compare|salary-needed|blog/articles)/[^'\"\s}<>]+?)\.html",
        r'\1',
        content
    )

    # Pattern 2: f-string templates like /city/{slug}.html or /compare/{slug1}-vs-{slug2}.html
    # These have curly braces in the path
    new_content = re.sub(
        r'(/(?:city|compare|salary-needed|blog/articles)/[^\'"\s<>]*?\}[^\'"\s<>]*?)\.html',
        r'\1',
        new_content
    )

    # Pattern 3: JS template like slugify(cities[0]) + '-vs-' + slugify(cities[1]) + '.html'
    new_content = new_content.replace(
        "slugify(cities[1]) + '.html'",
        "slugify(cities[1])"
    )

    new_count = new_content.count('.html')

    if new_content != content:
        print(f'{fname}: removed {old_count - new_count} .html references ({new_count} remaining)')
        with open(filepath, 'w') as f:
            f.write(new_content)
    else:
        print(f'{fname}: no changes needed')
