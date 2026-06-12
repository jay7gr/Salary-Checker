#!/usr/bin/env python3
"""
Submit site URLs to IndexNow (Bing, Yandex, Seznam, DuckDuckGo, Ecosia).

IndexNow pings search engines the moment content changes so they re-crawl
quickly — instead of waiting for them to discover updates on their own.
Google does NOT participate, but Bing + its syndication partners (DuckDuckGo,
Yahoo, Ecosia) do — and that is exactly where our live traffic comes from.

The verification key file (KEY.txt) is already hosted at the site root.

Usage:
  python3 submit-indexnow.py                  # submit every URL in the sitemaps
  python3 submit-indexnow.py --dry-run        # print what would be sent, no POST
  python3 submit-indexnow.py URL [URL ...]    # submit specific URLs only
  python3 submit-indexnow.py --files a.html…  # submit URLs for changed files
"""

import glob
import json
import re
import sys
import urllib.request
import urllib.error

HOST = "salary-converter.com"
KEY = "7449d578a1364cf59a8a76dfaab8a0e7"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10000  # IndexNow accepts up to 10,000 URLs per request

LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.I)


def urls_from_sitemaps():
    """Collect every page <loc> from the local sitemap-*.xml url-set files.

    The sitemap index (sitemap.xml) only lists child sitemaps, so we read the
    children directly and skip any <loc> that itself points at a .xml sitemap.
    """
    found = set()
    for path in sorted(glob.glob("sitemap-*.xml")):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        for loc in LOC_RE.findall(text):
            if loc.endswith(".xml"):
                continue  # a nested sitemap reference, not a page
            found.add(loc.strip())
    return sorted(found)


def files_to_urls(paths):
    """Map changed repo file paths to their canonical live URLs.

    Mirrors Cloudflare Pages clean-URL serving:
      index.html        -> /
      foo/index.html    -> /foo/
      foo.html          -> /foo
      foo/bar.html      -> /foo/bar
    Skips non-HTML, noindexed areas (admin/**), and 404.
    """
    urls = []
    for p in paths:
        p = p.strip().lstrip("./")
        if not p.endswith(".html"):
            continue
        if p == "404.html" or p.startswith("admin/"):
            continue
        if p == "index.html":
            path = "/"
        elif p.endswith("/index.html"):
            path = "/" + p[: -len("index.html")]  # keeps trailing slash
        else:
            path = "/" + p[: -len(".html")]
        urls.append(f"https://{HOST}{path}")
    return sorted(set(urls))


def submit(urls, dry_run=False):
    if not urls:
        print("No URLs to submit.")
        return 0
    total = 0
    for i in range(0, len(urls), BATCH):
        chunk = urls[i:i + BATCH]
        payload = {
            "host": HOST,
            "key": KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": chunk,
        }
        if dry_run:
            print(f"[dry-run] would submit {len(chunk)} URLs (first: {chunk[0]})")
            total += len(chunk)
            continue
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"Submitted {len(chunk)} URLs -> HTTP {resp.status}")
                total += len(chunk)
        except urllib.error.HTTPError as e:
            # 200/202 = OK; 400 bad request; 403 key not valid; 422 url/host mismatch; 429 too many
            body = e.read().decode("utf-8", "replace")[:300]
            print(f"HTTP {e.code} for batch starting {chunk[0]}: {body}")
            if e.code in (400, 403, 422):
                return total  # config problem — stop, retrying won't help
        except urllib.error.URLError as e:
            print(f"Network error: {e.reason}")
            return total
    return total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if "--files" in sys.argv:
        urls = files_to_urls(args)
    elif args:
        urls = args
    else:
        urls = urls_from_sitemaps()
    print(f"{'DRY RUN — ' if dry else ''}submitting {len(urls)} URL(s) to IndexNow...")
    n = submit(urls, dry_run=dry)
    print(f"Done. {n} URL(s) {'previewed' if dry else 'submitted'}.")


if __name__ == "__main__":
    main()
