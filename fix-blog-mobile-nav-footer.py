#!/usr/bin/env python3
"""
Fix script for blog mobile nav, footer, and dark mode issues across ALL 27 blog posts.

Fixes applied:
1. Nav links: Add nav-link-text class to <a> tags inside .nav-links (not the theme toggle button)
2. Nav links mobile CSS: Add .nav-links a.nav-link-text { display: none; } to @media 768px
3. Theme toggle: Remove fixed positioning on mobile (the position:fixed block in @media 768px)
4. Footer: Upgrade bare <footer> to proper .footer with footer-inner, footer-links
5. Footer CSS: Add .footer CSS styles if missing
6. Footer links mobile: Add .footer-links gap rule to mobile @media
7. Related-tools mobile: Add .related-tools mobile CSS for padding/margin
"""

import os
import re
import glob

BLOG_DIR = '/Users/jason.i/Salary Converter Project/blog/articles'

FOOTER_HTML = '''<footer class="footer">
    <div class="footer-inner">
        <div class="footer-logo">salary<span>:</span>converter</div>
        <p class="footer-text">Compare salaries across cities and countries with real cost-of-living data.</p>
        <div class="footer-links">
            <a href="https://salary-converter.com">Tool</a>
            <a href="/salary/">Salaries</a>
            <a href="/retire/">Retire Abroad</a>
            <a href="/blog/">Blog</a>
            <a href="/privacy/">Privacy</a>
            <a href="/about/">About</a>
            <a href="/terms/">Terms</a>
        </div>
    </div>
</footer>'''

FOOTER_CSS = '''/* Footer */
.footer {
    border-top: 1px solid var(--border);
    padding: 40px 24px;
    text-align: center;
}
.footer-inner {
    max-width: 980px;
    margin: 0 auto;
}
.footer-logo {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.footer-logo span {
    color: #2563eb;
}
.footer-text {
    font-size: 0.8rem;
    color: var(--text-secondary);
}
.footer-links {
    margin-top: 16px;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 24px;
}
.footer-links a {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.2s;
}
.footer-links a:hover {
    color: var(--text-primary);
}'''


def fix_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixes = []

    # =========================================================================
    # Fix 1: Add nav-link-text class to nav <a> tags (skip if already present)
    # =========================================================================
    if 'nav-link-text' not in content:
        # Find <a href="...">Text</a> (without existing class) inside the nav-links div
        # and add class="nav-link-text". We look for the nav-links div in the HTML body.
        # Also handle files where some links already have a different class (e.g. tool-link-text):
        #   <a href="..." class="tool-link-text">Tool</a> -> leave as-is
        #   <a href="...">Salaries</a> -> add class="nav-link-text"

        def add_nav_link_class_to_block(m):
            block = m.group(0)
            # Only add class to <a> tags that don't already have a class attribute
            block = re.sub(
                r'<a href="([^"]*)">(.*?)</a>',
                r'<a href="\1" class="nav-link-text">\2</a>',
                block
            )
            return block

        # Match the nav-links div section containing <a> tags (with or without classes)
        # The pattern captures from <div class="nav-links"> through all <a> tags until
        # we hit a <button (theme toggle) or </div>
        new_content = re.sub(
            r'(<div class="nav-links">\s*(?:<a\s[^>]*>[^<]*</a>\s*)+)',
            add_nav_link_class_to_block,
            content
        )
        if new_content != content:
            content = new_content
            fixes.append('Added nav-link-text class to nav links')

    # =========================================================================
    # Fix 1b: Add .nav-links a.nav-link-text { display: none; } to mobile CSS
    # =========================================================================
    if 'nav-link-text' in content and '.nav-links a.nav-link-text' not in content:
        # We need to add this rule inside a @media (max-width: 768px) block
        # Find the first @media (max-width: 768px) block and add the rule at the start
        def add_nav_hide_rule(m):
            return m.group(0) + '\n            .nav-links a.nav-link-text {\n                display: none;\n            }\n'

        new_content = re.sub(
            r'@media\s*\(max-width:\s*768px\)\s*\{',
            add_nav_hide_rule,
            content,
            count=1
        )
        if new_content != content:
            content = new_content
            fixes.append('Added .nav-links a.nav-link-text display:none to mobile CSS')

    # =========================================================================
    # Fix 2: Remove theme-toggle fixed positioning on mobile
    # =========================================================================
    # Pattern varies but always has these 4 lines inside a @media 768px block
    # Some files have this as a standalone @media block, some have it inside a larger one

    # Case A: Standalone @media block with just the theme-toggle fix
    standalone_pattern = re.compile(
        r'\n\s*@media\s*\(max-width:\s*768px\)\s*\{\s*\n'
        r'\s*\.theme-toggle\s*\{\s*\n'
        r'\s*position:\s*fixed\s*!important;\s*\n'
        r'\s*top:\s*16px\s*!important;\s*\n'
        r'\s*right:\s*16px\s*!important;\s*\n'
        r'\s*z-index:\s*10001\s*!important;\s*\n'
        r'\s*\}\s*\n'
        r'\s*\}',
        re.MULTILINE
    )
    new_content = standalone_pattern.sub('', content)
    if new_content != content:
        content = new_content
        fixes.append('Removed theme-toggle fixed positioning (standalone @media block)')
    else:
        # Case B: Inside a larger @media block - remove just the .theme-toggle block
        inline_pattern = re.compile(
            r'\n\s*\.theme-toggle\s*\{\s*\n'
            r'\s*position:\s*fixed\s*!important;\s*\n'
            r'\s*top:\s*16px\s*!important;\s*\n'
            r'\s*right:\s*16px\s*!important;\s*\n'
            r'\s*z-index:\s*10001\s*!important;\s*\n'
            r'\s*\}',
            re.MULTILINE
        )
        new_content = inline_pattern.sub('', content)
        if new_content != content:
            content = new_content
            fixes.append('Removed theme-toggle fixed positioning (inside @media block)')

    # =========================================================================
    # Fix 3: Upgrade bare <footer> to proper .footer with footer-inner
    # =========================================================================
    # Only for files with bare <footer> (not <footer class="footer"> or <footer class="page-footer"> etc.)
    # Check: has <footer> but NOT <footer class=
    has_bare_footer = bool(re.search(r'<footer>\s*\n\s*<p>', content))
    has_classed_footer = bool(re.search(r'<footer\s+class=', content))

    if has_bare_footer and not has_classed_footer:
        # Replace the bare footer HTML
        bare_footer_pattern = re.compile(
            r'<footer>\s*\n\s*<p>&copy;.*?</footer>',
            re.DOTALL
        )
        new_content = bare_footer_pattern.sub(FOOTER_HTML, content)
        if new_content != content:
            content = new_content
            fixes.append('Upgraded bare <footer> to proper .footer with footer-inner')

    # =========================================================================
    # Fix 4: Add .footer CSS if not present (for files that now have .footer class)
    # =========================================================================
    if 'class="footer"' in content and '.footer-inner' not in content:
        # Add footer CSS before </style> (but before share-bar styles if present)
        # Find the right insertion point
        if '.share-bar {' in content or '.share-bar{' in content:
            # Insert before share-bar styles
            share_pattern = re.compile(r'(\n\s*\.share-bar\s*\{)')
            new_content = share_pattern.sub('\n\n        ' + FOOTER_CSS.replace('\n', '\n        ') + r'\1', content, count=1)
        else:
            # Insert before </style>
            new_content = content.replace('</style>', '        ' + FOOTER_CSS.replace('\n', '\n        ') + '\n    </style>', 1)

        if new_content != content:
            content = new_content
            fixes.append('Added .footer CSS styles')

    # =========================================================================
    # Fix 5: Ensure footer-links has flex-wrap: wrap
    # =========================================================================
    if '.footer-links' in content:
        # Check if flex-wrap is already in ANY .footer-links CSS block
        # Find all .footer-links { ... } blocks and check if any has flex-wrap
        all_footer_links = re.findall(r'\.footer-links\s*\{([^}]*)\}', content)
        has_flex_wrap = any('flex-wrap' in block for block in all_footer_links)
        if not has_flex_wrap and all_footer_links:
            # Find the main (non-media-query) .footer-links block with display: flex
            for block_match in re.finditer(r'\.footer-links\s*\{([^}]*)\}', content):
                if 'display: flex' in block_match.group(1):
                    old = block_match.group(0)
                    new = old.replace('display: flex;', 'display: flex;\n    flex-wrap: wrap;')
                    if new == old:
                        new = old.replace('display: flex;', 'display: flex; flex-wrap: wrap;')
                    content = content.replace(old, new, 1)
                    fixes.append('Added flex-wrap: wrap to .footer-links')
                    break

    # =========================================================================
    # Fix 6: Add .footer-links mobile gap to @media (max-width: 768px)
    # =========================================================================
    if '.footer-links' in content:
        # Simple string check: if we already have .footer-links with gap: 16px 20px anywhere, skip
        has_mobile_footer_links = 'gap: 16px 20px' in content
        if not has_mobile_footer_links:
            # Find the first @media (max-width: 768px) block and add the rule
            def add_footer_links_mobile(m):
                return m.group(0) + '\n            .footer-links {\n                gap: 16px 20px;\n            }\n'

            new_content = re.sub(
                r'@media\s*\(max-width:\s*768px\)\s*\{',
                add_footer_links_mobile,
                content,
                count=1
            )
            if new_content != content:
                content = new_content
                fixes.append('Added .footer-links mobile gap rule')

    # =========================================================================
    # Fix 7: Add .related-tools mobile CSS
    # =========================================================================
    if 'related-tools' in content:
        # Simple string check for the CSS rule we inject
        has_related_tools_mobile = '.related-tools {' in content or '.related-tools{' in content
        if not has_related_tools_mobile:
            # Find the first @media (max-width: 768px) block and add the rule
            def add_related_tools_mobile(m):
                return m.group(0) + '\n            .related-tools {\n                margin-left: 16px !important;\n                margin-right: 16px !important;\n                padding: 24px !important;\n            }\n'

            new_content = re.sub(
                r'@media\s*\(max-width:\s*768px\)\s*\{',
                add_related_tools_mobile,
                content,
                count=1
            )
            if new_content != content:
                content = new_content
                fixes.append('Added .related-tools mobile CSS')

    # =========================================================================
    # Write back if changed
    # =========================================================================
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  FIXED {filename}:")
        for fix in fixes:
            print(f"    - {fix}")
        return True
    else:
        print(f"  SKIP  {filename}: no changes needed")
        return False


def main():
    html_files = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))
    print(f"Processing {len(html_files)} blog files...\n")

    fixed_count = 0
    skipped_count = 0

    for filepath in html_files:
        if fix_file(filepath):
            fixed_count += 1
        else:
            skipped_count += 1

    print(f"\nDone! Fixed: {fixed_count}, Skipped: {skipped_count}, Total: {len(html_files)}")


if __name__ == '__main__':
    main()
