#!/usr/bin/env python3
"""
One-time script to standardize consent code across all blog HTML files.
Handles 3 patterns:
  1. Standard pattern (analytics_storage denied + granted, 75 regions)
  2. Variant pattern (functionality_storage, personalization_storage, wait_for_update)
  3. GA4_SNIPPET pattern with "End Consent Mode" comment
Replaces all with the new simplified consent block + consent.js reference.
"""

import os, re, glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NEW_CONSENT_BLOCK = '''    <!-- Google Consent Mode v2 — ad signals denied in strict consent regions only -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('consent', 'default', {
            'ad_storage': 'denied',
            'ad_user_data': 'denied',
            'ad_personalization': 'denied',
            'analytics_storage': 'granted',
            'wait_for_update': 500,
            'regions': ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH','BR','CA']
        });
        gtag('consent', 'default', {
            'ad_storage': 'granted',
            'ad_user_data': 'granted',
            'ad_personalization': 'granted',
            'analytics_storage': 'granted'
        });
    </script>
    <script src="/consent.js" defer></script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-MMZSM2Z96B"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-MMZSM2Z96B');
    </script>'''

# Regex to match entire consent + GA4 block
# Covers: "<!-- Google Consent Mode" through the gtag config closing </script>
CONSENT_REGEX = re.compile(
    r'[ \t]*<!-- Google Consent Mode v2[^>]*-->.*?'          # Opening comment
    r'gtag\(\'config\',\s*\'G-MMZSM2Z96B\'\);'              # Config line
    r'\s*</script>',                                          # Closing script tag
    re.DOTALL
)

files = glob.glob(os.path.join(BASE_DIR, 'blog', '**', '*.html'), recursive=True)
updated = 0
skipped = 0
errors = 0

for fpath in sorted(files):
    rel = os.path.relpath(fpath, BASE_DIR)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if 'consent.js' in content:
        print(f'  {rel}: already updated, skipping')
        skipped += 1
        continue

    match = CONSENT_REGEX.search(content)
    if not match:
        print(f'  {rel}: no consent block found, skipping')
        skipped += 1
        continue

    # Also remove any "End Consent Mode" comment that may follow
    new_content = content[:match.start()] + NEW_CONSENT_BLOCK + content[match.end():]
    # Clean up any leftover "End Consent Mode" comment
    new_content = re.sub(r'\s*<!-- End Consent Mode[^>]*-->\s*', '\n', new_content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  {rel}: UPDATED')
    updated += 1

print(f'\n=== Done: {updated} updated, {skipped} skipped, {errors} errors ===')
