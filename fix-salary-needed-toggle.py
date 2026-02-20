#!/usr/bin/env python3
"""
Replaces the simple dark/light toggle on salary-needed pages with the
site-wide toggle (sun/moon SVG icons, hover effects, glow in dark mode).
"""

import os, re, glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALARY_DIR = os.path.join(BASE_DIR, 'salary-needed')

# Old CSS to replace (the simple toggle)
OLD_CSS_PATTERN = re.compile(
    r'\.theme-toggle \{[^}]+\}\s*'
    r'\[data-theme="dark"\] \.theme-toggle \{[^}]+\}\s*'
    r'\.theme-toggle \.thumb \{[^}]+\}\s*'
    r'\[data-theme="dark"\] \.theme-toggle \.thumb \{[^}]+\}'
)

# New CSS (matches main site)
NEW_CSS = """.theme-toggle {
            position: fixed; top: 20px; right: 20px; z-index: 10001;
            display: inline-flex; align-items: center;
            width: 38px; height: 22px;
            background: var(--border); border: none; border-radius: 11px;
            cursor: pointer; padding: 0; transition: background 0.3s; flex-shrink: 0;
        }
        .theme-toggle:hover { background: var(--text-secondary); }
        .theme-toggle .toggle-thumb {
            position: absolute; left: 2px; width: 18px; height: 18px;
            background: var(--card-bg); border-radius: 50%;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
        }
        [data-theme="dark"] .theme-toggle { background: #3b82f6; }
        [data-theme="dark"] .theme-toggle:hover { background: #60a5fa; }
        [data-theme="dark"] .theme-toggle .toggle-thumb {
            transform: translateX(16px);
            box-shadow: 0 0 0 2px #93c5fd, 0 1px 3px rgba(0,0,0,0.2);
        }
        .theme-toggle .toggle-icon { width: 11px; height: 11px; }
        .theme-toggle .icon-sun { color: #f59e0b; }
        .theme-toggle .icon-moon { display: none; color: #3b82f6; }
        [data-theme="dark"] .theme-toggle .icon-sun { display: none; }
        [data-theme="dark"] .theme-toggle .icon-moon { display: block; color: #3b82f6; }"""

# Old HTML button pattern
OLD_BUTTON = '<button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"><span class="thumb"></span></button>'

# New HTML button with SVG icons
NEW_BUTTON = '''<button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" type="button">
        <span class="toggle-thumb">
            <svg class="toggle-icon icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
            <svg class="toggle-icon icon-moon" viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </span>
    </button>'''

# Old JS pattern (simple, no aria-label update, no system preference listener)
OLD_JS_PATTERN = re.compile(
    r"<script>\s*\(function\(\)\{\s*var t=document\.getElementById\('themeToggle'\);"
    r".*?</script>",
    re.DOTALL
)

# New JS (matches main site, with aria-label and system preference listener)
NEW_JS = """<script>
    (function(){
        var t=document.getElementById('themeToggle');
        function g(){var s=localStorage.getItem('theme');if(s)return s;return matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'}
        function a(m){document.documentElement.setAttribute('data-theme',m);localStorage.setItem('theme',m);t.setAttribute('aria-label',m==='dark'?'Switch to light mode':'Switch to dark mode')}
        a(g());
        t.addEventListener('click',function(){a(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')});
        matchMedia('(prefers-color-scheme:dark)').addEventListener('change',function(e){if(!localStorage.getItem('theme'))a(e.matches?'dark':'light')});
    })();
    </script>"""


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Replace CSS
    content = OLD_CSS_PATTERN.sub(NEW_CSS, content)

    # 2. Replace HTML button
    content = content.replace(OLD_BUTTON, NEW_BUTTON)

    # 3. Replace JS
    content = OLD_JS_PATTERN.sub(NEW_JS, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# Process all salary-needed pages
files = glob.glob(os.path.join(SALARY_DIR, '*.html'))
files += glob.glob(os.path.join(SALARY_DIR, '*', '*.html'))

print(f"Found {len(files)} salary-needed pages")

success = 0
skipped = 0
for filepath in sorted(files):
    try:
        if fix_file(filepath):
            success += 1
        else:
            skipped += 1
    except Exception as e:
        print(f"  Error: {os.path.basename(filepath)}: {e}")

print(f"Updated toggle on {success} pages, skipped {skipped}")
