#!/usr/bin/env python3
"""
Add inline CTAs to blog articles and clean up leftover Gumroad CTAs.

1. Remove any remaining gumroad-cta-v1 sections from all blog articles
2. Add an inline CTA mid-article (after ~3rd h2) if not already present
3. Add a bottom "Try the Converter" CTA if not already present

Idempotency: Skips files that already have the markers.
"""
import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE, 'blog', 'articles')

# ── Patterns ──────────────────────────────────────────────────────────

# Gumroad CTA removal pattern
GUMROAD_PATTERN = re.compile(
    r'\n*\s*<section class="content-card gumroad-cta-v1"[^>]*>.*?</section>\s*',
    re.DOTALL
)

# Inline CTA marker
INLINE_CTA_MARKER = 'blog-inline-cta-v1'

# Bottom CTA marker (existing ones use "Try the Converter" text)
BOTTOM_CTA_MARKER = 'Try the Converter'

# h2 tags in article content (to find injection point for inline CTA)
H2_PATTERN = re.compile(r'(<h2[^>]*>)', re.IGNORECASE)

# ── CTA HTML blocks ──────────────────────────────────────────────────

INLINE_CTA_HTML = '''
<div class="blog-inline-cta-v1" style="margin:36px 0;padding:20px 24px;background:linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);border-radius:16px;text-align:center;">
    <p style="color:#fff;font-size:1rem;font-weight:600;margin:0 0 6px;">What would your salary be worth in another city?</p>
    <p style="color:rgba(255,255,255,0.8);font-size:0.88rem;margin:0 0 14px;">Compare 113 cities and 2,400+ neighborhoods — free, instant results.</p>
    <a href="/" style="display:inline-block;padding:10px 24px;background:#fff;color:#1e3a5f;border-radius:10px;text-decoration:none;font-size:0.9rem;font-weight:600;transition:transform 0.2s;">Calculate Your Equivalent Salary &rarr;</a>
</div>
'''

BOTTOM_CTA_HTML = '''
    <section style="max-width:800px;margin:40px auto;padding:0 24px;">
        <div style="padding:24px;background:var(--accent,#2563eb);border-radius:16px;text-align:center;margin-bottom:32px;">
            <p style="color:#fff;font-size:1rem;font-weight:600;margin-bottom:12px;">Try the Converter</p>
            <p style="color:rgba(255,255,255,0.8);font-size:0.9rem;margin-bottom:16px;">See what your salary is really worth in another city</p>
            <a href="/" style="display:inline-block;padding:12px 28px;background:#fff;color:var(--accent,#2563eb);border-radius:12px;text-decoration:none;font-size:0.95rem;font-weight:600;">Compare Salaries &rarr;</a>
        </div>
    </section>
'''

# ── Process files ─────────────────────────────────────────────────────

files = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))
stats = {'gumroad_removed': 0, 'inline_added': 0, 'bottom_added': 0, 'files_modified': 0}

for f in files:
    fname = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    original = content
    changes = []

    # 1. Remove Gumroad CTAs
    if 'gumroad-cta-v1' in content:
        content = GUMROAD_PATTERN.sub('\n', content)
        changes.append('gumroad removed')
        stats['gumroad_removed'] += 1

    # 2. Add inline CTA mid-article (after ~3rd h2 inside article content)
    if INLINE_CTA_MARKER not in content:
        # Find all h2 tags in the file
        h2_matches = list(H2_PATTERN.finditer(content))

        # We want h2s inside the article body, skip the first one (usually the opener)
        # and inject after the 3rd h2's preceding paragraph block
        # Target: inject BEFORE the 3rd or 4th h2 (whichever gives us a mid-article position)
        target_h2_idx = min(3, len(h2_matches) - 1) if len(h2_matches) > 3 else max(1, len(h2_matches) - 2)

        if len(h2_matches) >= 3 and target_h2_idx < len(h2_matches):
            # Only inject within .article-content or <article> blocks (not in footer sections)
            target_h2 = h2_matches[target_h2_idx]
            # Make sure it's before any footer/cross-links section
            cross_links_pos = content.find('cross-links-v1')
            citations_pos = content.find('blog-citations-v1')
            footer_pos = content.find('<footer')
            boundary = min(p for p in [cross_links_pos, citations_pos, footer_pos] if p > 0) if any(p > 0 for p in [cross_links_pos, citations_pos, footer_pos]) else len(content)

            if target_h2.start() < boundary:
                insert_pos = target_h2.start()
                content = content[:insert_pos] + INLINE_CTA_HTML + '\n' + content[insert_pos:]
                changes.append('inline CTA added')
                stats['inline_added'] += 1

    # 3. Add bottom CTA if missing
    if BOTTOM_CTA_MARKER not in content:
        # Insert before cross-links or citations or footer — whichever comes first after </article>
        article_end = content.find('</article>')
        if article_end == -1:
            # Some articles may not have </article> tag, look for cross-links or citations
            article_end = content.find('cross-links-v1')
            if article_end == -1:
                article_end = content.find('blog-citations-v1')

        if article_end > 0:
            # Find the line start
            line_start = content.rfind('\n', 0, article_end) + 1
            content = content[:line_start] + BOTTOM_CTA_HTML + '\n' + content[line_start:]
            changes.append('bottom CTA added')
            stats['bottom_added'] += 1

    # Write if changed
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        stats['files_modified'] += 1
        print(f"  {fname}: {', '.join(changes)}")

print(f"\nTOTAL: {stats['files_modified']} files modified")
print(f"  Gumroad removed: {stats['gumroad_removed']}")
print(f"  Inline CTAs added: {stats['inline_added']}")
print(f"  Bottom CTAs added: {stats['bottom_added']}")
