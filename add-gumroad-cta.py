#!/usr/bin/env python3
"""
One-time script: Add Gumroad PDF report CTA boxes to existing pages.

Product: "2026 Global Salary & Cost of Living Report" — sold on Gumroad.

Targets:
  - City pages (city/*.html, top-level only) — ~113 files
  - Rankings pages (rankings/*.html) — ~9 files
  - Salary pages (salary/*.html) — ~38 files
  - Blog articles (blog/articles/*.html) — ~19 files

Idempotency: Skips files that already contain 'gumroad-cta-v1'.
"""
import os
import glob
import re

BASE = os.path.dirname(os.path.abspath(__file__))

GUMROAD_URL = 'https://gumroad.com/l/placeholder'

CTA_HTML = f'''
        <section class="content-card gumroad-cta-v1" style="border: 1px solid #3b82f6; border-left: 4px solid #3b82f6; background: var(--card-bg); margin-top: 24px;">
            <div style="display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap;">
                <div style="flex:1; min-width:200px;">
                    <p style="font-size:0.65rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin:0 0 6px;">\U0001f4ca Premium Report</p>
                    <h3 style="font-size:1rem; font-weight:600; margin:0 0 6px; color:var(--text-primary);">2026 Global Salary & Cost of Living Report</h3>
                    <p style="font-size:0.85rem; color:var(--text-body); line-height:1.5; margin:0 0 12px;">113 cities, 37 job titles, tax breakdowns, neighborhood data & more &mdash; all in one downloadable PDF.</p>
                    <a href="{GUMROAD_URL}" rel="noopener noreferrer" target="_blank"
                       style="display:inline-block; padding:10px 24px; background:#3b82f6; color:#ffffff; border-radius:100px; font-weight:600; font-size:0.85rem; text-decoration:none; transition:transform 0.2s;">
                        Download the Report &mdash; $9 &rarr;
                    </a>
                </div>
                <div style="flex-shrink:0; display:flex; align-items:center;">
                    <div style="width:80px; height:80px; background:linear-gradient(135deg, #1e3a5f, #3b82f6); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:2rem;">\U0001f4c4</div>
                </div>
            </div>
        </section>
'''


def process_city_pages():
    """Add Gumroad CTA to city pages (top-level only, not neighborhood subdirectories)."""
    pattern = os.path.join(BASE, 'city', '*.html')
    files = sorted(glob.glob(pattern))
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        if filename == 'index.html':
            skipped += 1
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency check
        if 'gumroad-cta-v1' in content:
            skipped += 1
            continue

        # Insert before <footer class="page-footer">
        anchor = re.search(r'(\s*<footer class="page-footer">)', content)
        if anchor:
            insert_pos = anchor.start()
            content = content[:insert_pos] + '\n' + CTA_HTML + content[insert_pos:]
        else:
            errors += 1
            print(f"  WARN: No anchor found in city/{filename}")
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f"  Updated: city/{filename}")

    return updated, skipped, errors


def process_rankings_pages():
    """Add Gumroad CTA to rankings pages."""
    pattern = os.path.join(BASE, 'rankings', '*.html')
    files = sorted(glob.glob(pattern))
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency check
        if 'gumroad-cta-v1' in content:
            skipped += 1
            continue

        # Insert before <footer class="page-footer">
        anchor = re.search(r'(\s*<footer class="page-footer">)', content)
        if anchor:
            insert_pos = anchor.start()
            content = content[:insert_pos] + '\n' + CTA_HTML + content[insert_pos:]
        else:
            errors += 1
            print(f"  WARN: No anchor found in rankings/{filename}")
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f"  Updated: rankings/{filename}")

    return updated, skipped, errors


def process_salary_pages():
    """Add Gumroad CTA to salary pages."""
    pattern = os.path.join(BASE, 'salary', '*.html')
    files = sorted(glob.glob(pattern))
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency check
        if 'gumroad-cta-v1' in content:
            skipped += 1
            continue

        # Insert before <footer class="page-footer">
        anchor = re.search(r'(\s*<footer class="page-footer">)', content)
        if anchor:
            insert_pos = anchor.start()
            content = content[:insert_pos] + '\n' + CTA_HTML + content[insert_pos:]
        else:
            errors += 1
            print(f"  WARN: No anchor found in salary/{filename}")
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f"  Updated: salary/{filename}")

    return updated, skipped, errors


def process_blog_articles():
    """Add Gumroad CTA to blog articles. Blog uses <footer class="footer"> not page-footer."""
    pattern = os.path.join(BASE, 'blog', 'articles', '*.html')
    files = sorted(glob.glob(pattern))
    updated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        filename = os.path.basename(filepath)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Idempotency check
        if 'gumroad-cta-v1' in content:
            skipped += 1
            continue

        # Blog articles use <footer class="footer"> or possibly <footer class="page-footer">
        anchor = re.search(r'(\s*<footer[\s>])', content)
        if anchor:
            insert_pos = anchor.start()
            content = content[:insert_pos] + '\n' + CTA_HTML + content[insert_pos:]
        else:
            errors += 1
            print(f"  WARN: No anchor found in blog/articles/{filename}")
            continue

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
        print(f"  Updated: blog/articles/{filename}")

    return updated, skipped, errors


if __name__ == '__main__':
    print("Adding Gumroad PDF report CTAs to existing pages...")
    print()

    print("1. City pages (city/*.html)...")
    u1, s1, e1 = process_city_pages()
    print(f"   Updated: {u1}, Skipped: {s1}, Errors: {e1}")
    print()

    print("2. Rankings pages (rankings/*.html)...")
    u2, s2, e2 = process_rankings_pages()
    print(f"   Updated: {u2}, Skipped: {s2}, Errors: {e2}")
    print()

    print("3. Salary pages (salary/*.html)...")
    u3, s3, e3 = process_salary_pages()
    print(f"   Updated: {u3}, Skipped: {s3}, Errors: {e3}")
    print()

    print("4. Blog articles (blog/articles/*.html)...")
    u4, s4, e4 = process_blog_articles()
    print(f"   Updated: {u4}, Skipped: {s4}, Errors: {e4}")
    print()

    total_updated = u1 + u2 + u3 + u4
    total_skipped = s1 + s2 + s3 + s4
    total_errors = e1 + e2 + e3 + e4
    print("=" * 50)
    print(f"TOTAL: {total_updated} updated, {total_skipped} skipped, {total_errors} errors")
