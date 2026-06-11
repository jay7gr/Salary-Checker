#!/usr/bin/env python3
"""
Remove dead /compare/ internal links sitewide.

The /compare/ pages were retired (they 301 to /offer-evaluator/), but ~9,762
pages still link to them, so Google keeps discovering dead URLs. This removes:

  1. The whole "Compare {City} With Other Cities" section on city pages
     (a content-card full of /compare/{a}-vs-{b} links). City pages keep their
     separate, legitimate "Explore Similar Cities" /city/ link section.
  2. Bare nav/footer links to the /compare/ index (<a href="/compare/">...</a>).

It does NOT touch /city/ links or the "Explore Similar Cities" section, and it
leaves the retire/compare/ pages (a different, still-live set) alone.

Usage:
  python3 remove-compare-links.py --dry-run FILE   # preview one file
  python3 remove-compare-links.py                  # apply to whole site
"""

import os
import re
import sys
import glob

# 1) The big "Compare X With Other Cities" content-card section (multiline)
SECTION_RE = re.compile(
    r'\s*<section class="content-card"><h2>Compare [^<]*?With Other Cities</h2>.*?</section>',
    re.S,
)
# 1b) Neighborhood pages: <div class="card"><h2>{heading}</h2><div ...>[/compare/ pills]</div></div>
#     Covers both "Compare {Nhood}" and "{City} City Comparisons" headings. Anchored on the
#     FIRST inner link being a /compare/ link, so a legit card (e.g. /city/ links) is never removed.
NHOOD_CARD_RE = re.compile(
    r'\s*<div class="card">\s*<h2>[^<]*</h2>\s*<div [^>]*>\s*<a href="/compare/.*?</div>\s*</div>',
    re.S,
)
# 2) Bare nav/footer links to the /compare/ index — eat optional leading newline+indent
NAV_LINK_RE = re.compile(
    r'(?:\n[ \t]*)?<a [^>]*href="/compare/"[^>]*>[^<]*</a>'
)
# 3) Stray /compare/{slug} links that sit alone on their own line (footer "Tools" lists) -> drop the line
LIST_COMPARE_RE = re.compile(
    r'\n[ \t]*<a [^>]*href="/compare/[^"]*"[^>]*>[^<]*</a>(?=[ \t]*(?:\n|$))'
)
# 4) Any remaining inline /compare/ links (blog prose) -> unwrap, keep the visible text intact
INLINE_COMPARE_RE = re.compile(
    r'<a [^>]*href="/compare/[^"]*"[^>]*>([^<]*)</a>'
)

def clean(text):
    text, n_sec = SECTION_RE.subn('', text)
    text, n_card = NHOOD_CARD_RE.subn('', text)
    text, n_nav = NAV_LINK_RE.subn('', text)
    text, n_list = LIST_COMPARE_RE.subn('', text)
    text, n_inline = INLINE_COMPARE_RE.subn(r'\1', text)
    return text, n_sec + n_card, n_nav + n_list + n_inline

def main():
    dry = '--dry-run' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]

    if dry and args:
        files = args
    else:
        files = glob.glob('**/*.html', recursive=True)

    total_files = 0
    total_sec = 0
    total_nav = 0
    for path in files:
        # never touch the still-live retirement comparison pages
        if path.startswith('retire/compare/'):
            continue
        try:
            with open(path, encoding='utf-8') as f:
                src = f.read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        if '/compare/' not in src:
            continue
        out, n_sec, n_nav = clean(src)
        if out != src:
            total_files += 1
            total_sec += n_sec
            total_nav += n_nav
            if dry:
                print(f"{path}: would remove {n_sec} section(s), {n_nav} nav link(s)")
                # show remaining /compare/ refs (should be 0)
                left = out.count('href="/compare/')
                print(f"  remaining /compare/ links after clean: {left}")
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(out)

    print(f"\n{'DRY RUN — ' if dry else ''}files changed: {total_files}, "
          f"sections removed: {total_sec}, nav links removed: {total_nav}")

if __name__ == '__main__':
    main()
