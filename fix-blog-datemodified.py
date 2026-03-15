#!/usr/bin/env python3
"""
Add dateModified to blog articles' JSON-LD structured data.
Inserts dateModified after datePublished for articles that don't already have it.
Uses datePublished as the default value (content hasn't changed since publish).
"""

import os
import re
import glob

BLOG_DIR = os.path.join(os.path.dirname(__file__), 'blog', 'articles')

def fix_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has dateModified
    if '"dateModified"' in content:
        return False

    # Match the datePublished line and insert dateModified after it
    # Pattern: "datePublished": "YYYY-MM-DD",
    pattern = r'("datePublished":\s*"(\d{4}-\d{2}-\d{2})")(,?\s*\n)'

    def replacer(match):
        date_published_part = match.group(1)
        date_value = match.group(2)
        trailing = match.group(3)
        # Ensure there's a comma after datePublished
        if not trailing.strip().startswith(','):
            date_published_part += ','
            indent = '        '
            return f'{date_published_part}\n{indent}"dateModified": "{date_value}"{trailing}'
        else:
            indent = '        '
            return f'{date_published_part}{trailing}{indent}"dateModified": "{date_value}",\n'

    new_content = re.sub(pattern, replacer, content, count=1)

    if new_content == content:
        print(f'  WARNING: No datePublished found in {os.path.basename(filepath)}')
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    articles = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))
    print(f'Found {len(articles)} blog articles')

    modified = 0
    skipped = 0

    for filepath in articles:
        name = os.path.basename(filepath)
        if fix_article(filepath):
            print(f'  + Added dateModified: {name}')
            modified += 1
        else:
            if '"dateModified"' in open(filepath).read():
                print(f'  ~ Already has dateModified: {name}')
            skipped += 1

    print(f'\nDone: {modified} modified, {skipped} skipped')


if __name__ == '__main__':
    main()
