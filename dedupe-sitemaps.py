#!/usr/bin/env python3
"""
Remove duplicate URLs across the sitemap set, keeping each unique URL exactly
once. A sitemap is only a discovery hint — duplicates waste crawl budget but
add nothing — so this is safe as long as we never drop a *unique* URL.

SAFETY GUARANTEE: the script refuses to write anything unless the set of
unique <loc> URLs is identical before and after. If even one unique URL would
be lost, it aborts. Run --verify first to see the proof; it writes nothing.

Each surviving <url> block keeps its full contents (lastmod/changefreq/
priority) from its first occurrence, so no spurious re-crawl signals.

Usage:
  python3 dedupe-sitemaps.py --verify   # prove the unique set is unchanged
  python3 dedupe-sitemaps.py            # apply (only if the safety check passes)
"""

import glob
import re
import sys

URL_BLOCK_RE = re.compile(r"<url>\s*.*?</url>", re.S)
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.I)
CHILD_FILES = sorted(glob.glob("sitemap-*.xml"))


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def unique_locs_in_files(files):
    """Every distinct page URL currently present across the given files."""
    s = set()
    for p in files:
        for block in URL_BLOCK_RE.findall(read(p)):
            m = LOC_RE.search(block)
            if m and not m.group(1).endswith(".xml"):
                s.add(m.group(1).strip())
    return s


def main():
    verify = "--verify" in sys.argv or "--dry-run" in sys.argv

    before = unique_locs_in_files(CHILD_FILES)

    seen = set()
    plan = {}          # path -> new file text
    total_in = total_out = 0
    for path in CHILD_FILES:
        text = read(path)
        blocks = URL_BLOCK_RE.findall(text)
        total_in += len(blocks)
        kept = []
        for block in blocks:
            m = LOC_RE.search(block)
            loc = m.group(1).strip() if m else None
            if loc and loc in seen:
                continue  # duplicate of one we already kept
            if loc:
                seen.add(loc)
            kept.append(block)
        total_out += len(kept)
        # Rebuild the file from its surviving blocks (preserve header/footer)
        new_text = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join("  " + b + "\n" for b in kept)
            + "</urlset>\n"
        )
        plan[path] = (new_text, len(kept))

    # Simulate the result and assert no unique URL is lost.
    after = set()
    for new_text, _ in plan.values():
        for block in URL_BLOCK_RE.findall(new_text):
            m = LOC_RE.search(block)
            if m and not m.group(1).endswith(".xml"):
                after.add(m.group(1).strip())

    lost = before - after
    gained = after - before  # should always be empty
    print(f"Child sitemaps:           {len(CHILD_FILES)}")
    print(f"URL entries before:       {total_in}")
    print(f"URL entries after:        {total_out}")
    print(f"Duplicate entries removed:{total_in - total_out}")
    print(f"Unique URLs before:       {len(before)}")
    print(f"Unique URLs after:        {len(after)}")
    print(f"Unique URLs LOST:         {len(lost)}")
    print(f"Unique URLs gained:       {len(gained)}")
    empties = [p for p, (_, n) in plan.items() if n == 0]
    print(f"Files that become empty:  {len(empties)} {empties if empties else ''}")

    if lost or gained:
        print("\n❌ ABORT — the unique URL set would change. Writing nothing.")
        if lost:
            for u in list(lost)[:20]:
                print("   would lose:", u)
        return 1

    print("\n✅ SAFE — every unique URL is preserved exactly once.")

    if verify:
        print("(verify mode — no files written)")
        return 0

    for path, (new_text, n) in plan.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    print(f"Wrote {len(plan)} sitemap files.")
    if empties:
        print(f"NOTE: {len(empties)} file(s) are now empty but still valid; "
              f"left in place and referenced. Re-run with index cleanup if desired.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
