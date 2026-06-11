#!/usr/bin/env python3
"""
One-time SEO repair: remove all /compare/ URLs from the sitemaps.

Context: ~40,803 /compare/ city-vs-city pages were dropped during the move to a
git-based deploy and now 301-redirect to /offer-evaluator/. They were never
removed from the sitemaps, so Google kept crawling 40K redirect URLs and
deindexed the section (and burned crawl budget meant for real pages). The
compare pages earned ~zero organic traffic, so we retire them cleanly rather
than resurrect them.

This script:
  1. Strips every <url> line containing "/compare/" from each sitemap-*.xml
  2. Deletes any sitemap file that becomes empty (was 100% compare)
  3. Rebuilds sitemap.xml (the index) to reference only surviving files
  4. Refreshes lastmod on touched files to today
"""

import os
import re
import glob
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().isoformat()
DOMAIN = "https://salary-converter.com"

url_files = sorted(glob.glob(os.path.join(BASE, "sitemap-*.xml")))

surviving = []   # filenames (basename) that still have URLs
deleted = []     # filenames removed (emptied)
removed_total = 0

for path in url_files:
    name = os.path.basename(path)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    kept, removed = [], 0
    for line in lines:
        if "<loc>" in line and "/compare/" in line:
            removed += 1
            continue
        kept.append(line)

    remaining_urls = sum(1 for l in kept if "<loc>" in l)
    removed_total += removed

    if remaining_urls == 0:
        os.remove(path)
        deleted.append(name)
        print(f"  DELETED {name} (was {removed} compare URLs, 0 remain)")
        continue

    if removed > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(kept)
        print(f"  STRIPPED {name}: removed {removed} compare, {remaining_urls} remain")
    surviving.append(name)

# Rebuild the sitemap index to reference only surviving files
surviving.sort(key=lambda n: (len(n), n))  # natural-ish order
index_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for name in surviving:
    index_lines.append("  <sitemap>")
    index_lines.append(f"    <loc>{DOMAIN}/{name}</loc>")
    index_lines.append(f"    <lastmod>{TODAY}</lastmod>")
    index_lines.append("  </sitemap>")
index_lines.append("</sitemapindex>")
index_lines.append("")

with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(index_lines))

print(f"\nSummary:")
print(f"  Compare URLs removed:  {removed_total}")
print(f"  Sitemap files deleted: {len(deleted)} -> {deleted}")
print(f"  Sitemap files kept:    {len(surviving)}")
print(f"  Rebuilt sitemap.xml referencing {len(surviving)} files")
