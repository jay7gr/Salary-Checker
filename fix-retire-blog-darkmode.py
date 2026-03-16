#!/usr/bin/env python3
"""
Fix dark mode on retire abroad blog posts.
These posts use hardcoded hex colors instead of CSS variables,
causing them to remain white/light when dark mode is active.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

# The 5 retire abroad blog posts
RETIRE_BLOGS = [
    'blog/articles/how-to-retire-abroad-cost-of-living-guide.html',
    'blog/articles/retire-on-2000-a-month-abroad-best-cities.html',
    'blog/articles/easiest-retirement-visas-2026.html',
    'blog/articles/retire-abroad-social-security-only.html',
    'blog/articles/best-retirement-healthcare-countries-2026.html',
]

# Also check for inheritance tax blog
if os.path.exists(os.path.join(ROOT, 'blog/articles/inheritance-tax-expats-retire-abroad.html')):
    RETIRE_BLOGS.append('blog/articles/inheritance-tax-expats-retire-abroad.html')

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # === NAV FIXES ===
    # Fix nav background (hardcoded light background -> CSS variable with fallback)
    content = content.replace(
        'background: rgba(245, 245, 247, 0.72);',
        'background: var(--nav-bg, rgba(245, 245, 247, 0.72));'
    )
    # Fix nav border in dark mode
    content = content.replace(
        'border-bottom: 1px solid rgba(0, 0, 0, 0.1);',
        'border-bottom: 1px solid var(--border);'
    )

    # Fix nav-links a color (hardcoded -> variable)
    # Match:  .nav-links a {\n ... color: #1d1d1f;
    content = re.sub(
        r'(\.nav-links a\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )

    # === ARTICLE CARD FIXES ===
    # Fix article-card background
    content = re.sub(
        r'(\.article-card\s*\{[^}]*?)background:\s*#ffffff;',
        r'\1background: var(--card-bg);',
        content
    )
    # Fix article-card box-shadow
    content = re.sub(
        r'(\.article-card\s*\{[^}]*?)box-shadow:\s*0 2px 20px rgba\(0,\s*0,\s*0,\s*0\.06\);',
        r'\1box-shadow: var(--shadow);',
        content
    )

    # === ARTICLE TITLE FIX ===
    content = re.sub(
        r'(\.article-title\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )

    # === ARTICLE BODY FIXES ===
    # Fix h2 color
    content = re.sub(
        r'(\.article-body h2\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )
    # Fix h3 color
    content = re.sub(
        r'(\.article-body h3\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )
    # Fix p color
    content = re.sub(
        r'(\.article-body p\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )
    # Fix ul, ol color
    content = re.sub(
        r'(\.article-body (?:ul|ol)\s*(?:,\s*\.article-body (?:ul|ol)\s*)?\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )
    # Fix strong color
    content = re.sub(
        r'(\.article-body strong\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )
    # Fix blockquote color
    content = re.sub(
        r'(\.article-body blockquote\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )
    # Fix blockquote background to use CSS variable
    content = re.sub(
        r'(\.article-body blockquote\s*\{[^}]*?)background:\s*rgba\(37,\s*99,\s*235,\s*0\.04\);',
        r'\1background: var(--tag-bg);',
        content
    )

    # === DESTINATION CARD FIXES ===
    content = re.sub(
        r'(\.destination-card\s*\{[^}]*?)background:\s*#f5f5f7;',
        r'\1background: var(--stat-card-bg);',
        content
    )
    content = re.sub(
        r'(\.destination-card\s*\{[^}]*?)border:\s*1px solid rgba\(0,\s*0,\s*0,\s*0\.04\);',
        r'\1border: 1px solid var(--border-light);',
        content
    )

    # Fix destination-card label color
    content = re.sub(
        r'(\.destination-card\s+\.detail-grid\s+\.label\s*\{[^}]*?)color:\s*#86868b;',
        r'\1color: var(--text-secondary);',
        content
    )
    # Fix destination-card value color
    content = re.sub(
        r'(\.destination-card\s+\.detail-grid\s+\.value\s*\{[^}]*?)color:\s*#1d1d1f;',
        r'\1color: var(--text-primary);',
        content
    )

    # === META FIXES ===
    # Fix article-date, article-read-time color
    content = re.sub(
        r'(\.article-date\s*,\s*\n?\s*\.article-read-time\s*\{[^}]*?)color:\s*#86868b;',
        r'\1color: var(--text-secondary);',
        content
    )
    # Fix meta-dot background
    content = re.sub(
        r'(\.meta-dot\s*\{[^}]*?)background:\s*#86868b;',
        r'\1background: var(--text-secondary);',
        content
    )

    # === FOOTER FIX ===
    content = re.sub(
        r'(footer\s*\{[^}]*?)color:\s*#86868b;',
        r'\1color: var(--text-secondary);',
        content
    )

    # === KEY TAKEAWAY / HIGHLIGHT BOX FIXES ===
    # Fix any highlight/key-takeaway boxes with hardcoded backgrounds
    content = re.sub(
        r'(\.key-takeaway\s*\{[^}]*?)background:\s*#f5f5f7;',
        r'\1background: var(--stat-card-bg);',
        content
    )
    content = re.sub(
        r'(\.highlight-box\s*\{[^}]*?)background:\s*#f5f5f7;',
        r'\1background: var(--stat-card-bg);',
        content
    )

    # === COMPARISON/SUMMARY BOX FIXES ===
    content = re.sub(
        r'(\.summary-box\s*\{[^}]*?)background:\s*#f5f5f7;',
        r'\1background: var(--stat-card-bg);',
        content
    )

    # === ADD DARK MODE NAV BACKGROUND (if not already present) ===
    # Check if there's already a [data-theme="dark"] nav rule
    if '[data-theme="dark"] nav' not in content:
        # Add dark mode nav background right after the existing [data-theme="dark"] CSS variables block
        dark_theme_insertion = '''        [data-theme="dark"] nav {
            background: var(--nav-bg, rgba(0, 0, 0, 0.85));
            border-bottom-color: var(--border);
        }
'''
        # Insert after the closing brace of [data-theme="dark"] { ... }
        content = re.sub(
            r'(\[data-theme="dark"\]\s*\{[^}]+\})\n',
            r'\1\n' + dark_theme_insertion + '\n',
            content,
            count=1
        )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


count = 0
for rel_path in RETIRE_BLOGS:
    filepath = os.path.join(ROOT, rel_path)
    if not os.path.exists(filepath):
        print(f'  SKIP (not found): {rel_path}')
        continue

    changed = fix_file(filepath)
    if changed:
        count += 1
        print(f'  FIXED: {rel_path}')
    else:
        print(f'  NO CHANGE: {rel_path}')

print(f'\nDone: fixed {count} files')
