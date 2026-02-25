#!/usr/bin/env python3
"""One-time script to inject in-article ad unit into blog articles, before the 3rd <h2>."""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, 'blog', 'articles')

AD_UNIT = '''
            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4472082543745200"
                 crossorigin="anonymous"></script>
            <ins class="adsbygoogle"
                 style="display:block; text-align:center;"
                 data-ad-layout="in-article"
                 data-ad-format="fluid"
                 data-ad-client="ca-pub-4472082543745200"
                 data-ad-slot="7732130560"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({});
            </script>

'''

updated = 0
skipped = 0

for fname in sorted(os.listdir(BLOG_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BLOG_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Idempotency: skip if already has in-article ad
    if 'data-ad-slot="7732130560"' in content:
        skipped += 1
        print(f'  SKIP (already has ad): {fname}')
        continue

    # Find all <h2 positions in the article-content
    h2_positions = [m.start() for m in re.finditer(r'<h2[\s>]', content)]

    if len(h2_positions) >= 3:
        # Insert before the 3rd <h2>
        insert_pos = h2_positions[2]
    elif len(h2_positions) >= 2:
        # Fallback: insert before the 2nd <h2>
        insert_pos = h2_positions[1]
    else:
        print(f'  SKIP (only {len(h2_positions)} h2 tags): {fname}')
        skipped += 1
        continue

    new_content = content[:insert_pos] + AD_UNIT + content[insert_pos:]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    updated += 1
    print(f'  UPDATED: {fname} (inserted before h2 #{3 if len(h2_positions) >= 3 else 2})')

print(f'\nDone: {updated} articles updated, {skipped} skipped')
