#!/usr/bin/env python3
"""
Conversion pilot: embed a pre-configured, interactive salary calculator high
in the highest-traffic blog articles, so readers can run a comparison inline
instead of bouncing (these pages currently sit at ~1.0 views/user).

Uses the pre-fillable widget (embed.html?from=&to=). Idempotent: skips a file
that already has the funnel embed. Inserts right after the first paragraph
following the first <h2>, i.e. just under the opening hook.

Usage:
  python3 add-funnel-embeds.py --dry-run
  python3 add-funnel-embeds.py
"""

import re
import sys
from urllib.parse import quote

MARKER = "<!-- funnel-embed:"

# article file (in blog/articles/)  ->  (from city, to city, heading)
ARTICLES = {
    "cost-of-living-adjustment-cola-guide-2026.html":
        ("London", "New York", "Try it: your cost-of-living-adjusted salary"),
    "most-expensive-cities-in-the-world-2026.html":
        ("New York", "Zurich", "Try it: New York vs Zurich"),
    "average-salary-by-city-2026-global-comparison.html":
        ("Berlin", "London", "Try it: compare salaries between cities"),
    "london-vs-new-york-true-cost-comparison.html":
        ("London", "New York", "Try it: London vs New York"),
    "cheapest-countries-to-live-in-2026.html":
        ("London", "Bangkok", "Try it: London vs Bangkok"),
}


def embed_html(from_city, to_city, label):
    src = f"/embed.html?from={quote(from_city)}&amp;to={quote(to_city)}"
    return (
        f'\n{MARKER} interactive pre-set calculator (conversion pilot) -->\n'
        f'<div class="article-tool-embed" style="margin:32px 0;">\n'
        f'  <div style="font-weight:700;font-size:1.2rem;letter-spacing:-0.3px;margin:0 0 4px;">{label}</div>\n'
        f'  <p style="font-size:0.95rem;color:var(--text-secondary,#86868b);margin:0 0 14px;">'
        f'Enter your salary to see its real equivalent &mdash; adjusted for taxes, rent, and cost of living.</p>\n'
        f'  <iframe src="{src}" width="100%" height="780" loading="lazy" '
        f'style="border:1px solid var(--border,#e5e5ea);border-radius:16px;display:block;'
        f'background:var(--card-bg,#fff);" title="{label} salary calculator"></iframe>\n'
        f'</div>\n'
    )


def insert(text, block):
    """Insert block right after the first </p> that follows the first <h2>."""
    h2 = re.search(r"<h2[ >]", text)
    if not h2:
        return None
    p_end = text.find("</p>", h2.end())
    if p_end == -1:
        return None
    cut = p_end + len("</p>")
    return text[:cut] + "\n" + block + text[cut:]


def main():
    dry = "--dry-run" in sys.argv
    changed = 0
    for fname, (frm, to, label) in ARTICLES.items():
        path = f"blog/articles/{fname}"
        try:
            with open(path, encoding="utf-8") as f:
                src = f.read()
        except OSError as e:
            print(f"❌ {fname}: {e}")
            continue
        if MARKER in src:
            print(f"• {fname}: already has funnel embed — skipped")
            continue
        out = insert(src, embed_html(frm, to, label))
        if out is None:
            print(f"❌ {fname}: no <h2>…</p> anchor found — skipped")
            continue
        changed += 1
        if dry:
            print(f"✅ {fname}: would insert {frm} → {to} embed")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"✅ {fname}: inserted {frm} → {to} embed")
    print(f"\n{'DRY RUN — ' if dry else ''}{changed} file(s) {'would change' if dry else 'changed'}.")


if __name__ == "__main__":
    main()
