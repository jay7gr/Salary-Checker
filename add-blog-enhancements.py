#!/usr/bin/env python3
"""
Add author bio and newsletter signup to all 19 blog articles.

Author bio: inserted after share-bar, before article-content div.
Newsletter signup: inserted before the last <footer tag.

Idempotency:
  - author-bio class in content -> skip author bio
  - newsletter-blog-v1 class in content -> skip newsletter
"""

import os
import re
import glob

BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog', 'articles')

AUTHOR_BIO_HTML = '''
<div class="author-bio" style="display:flex;align-items:center;gap:16px;padding:16px 20px;background:var(--stat-card-bg,#f5f5f7);border-radius:12px;margin-bottom:24px;">
    <div style="width:48px;height:48px;background:linear-gradient(135deg,#2563eb,#1d4ed8);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:1.2rem;color:#fff;font-weight:700;">s:c</div>
    <div>
        <p style="font-size:0.85rem;font-weight:600;color:var(--text-primary,#1d1d1f);margin:0 0 2px;">salary:converter Research Team</p>
        <p style="font-size:0.78rem;color:var(--text-secondary,#86868b);margin:0;line-height:1.4;">Data-driven insights on salaries, cost of living, and relocation decisions for 113 cities worldwide.</p>
    </div>
</div>'''

NEWSLETTER_HTML = '''<section class="newsletter-blog-v1" style="max-width:800px;margin:32px auto 0;padding:28px;background:linear-gradient(135deg,var(--card-bg,#fff) 0%,var(--stat-card-bg,#f5f5f7) 100%);border-radius:16px;border:1px solid var(--accent,#2563eb);text-align:center;">
    <h3 style="font-size:1.05rem;font-weight:700;color:var(--text-primary,#1d1d1f);margin:0 0 8px;">&#x1F4EC; Get Weekly Salary Insights</h3>
    <p style="font-size:0.85rem;color:var(--text-body,#4a4a4c);margin:0 0 16px;line-height:1.5;">City spotlights, salary trends, and cost of living updates &#x2014; delivered every week.</p>
    <form class="newsletter-blog-form" style="display:flex;gap:8px;max-width:400px;margin:0 auto;" onsubmit="event.preventDefault();this.style.display='none';this.nextElementSibling.style.display='';if(typeof gtag==='function')gtag('event','newsletter_signup',{event_category:'conversion',source:'blog'});">
        <input type="email" placeholder="your@email.com" required style="flex:1;padding:10px 14px;border:1px solid var(--border,#e5e5ea);border-radius:10px;font-size:0.85rem;background:var(--card-bg,#fff);color:var(--text-primary,#1d1d1f);outline:none;">
        <button type="submit" style="padding:10px 20px;background:var(--accent,#2563eb);color:#fff;border:none;border-radius:10px;font-size:0.85rem;font-weight:600;cursor:pointer;white-space:nowrap;">Subscribe</button>
    </form>
    <div style="display:none;padding:8px 0;">
        <p style="font-size:0.9rem;font-weight:600;color:var(--accent,#2563eb);margin:0;">You're in! &#x1F389;</p>
        <p style="font-size:0.78rem;color:var(--text-secondary,#86868b);margin:4px 0 0;">Check your inbox to confirm.</p>
    </div>
    <p style="font-size:0.7rem;color:var(--text-secondary,#86868b);margin:8px 0 0;">No spam. Unsubscribe anytime.</p>
</section>

'''


def add_author_bio(content, filename):
    """Insert author bio into the article, handling three structure variants:
    1. share-bar + article-content: insert between share-bar </div> and <div class="article-content">
    2. h1 + article-body: insert between </h1> line and <div class="article-body">
    3. h1 + direct <p>: insert between </h1> line and the first <p> or next element
    """
    if 'author-bio' in content:
        return content, False

    # --- Strategy 1: share-bar present, article-content follows ---
    share_bar_match = re.search(r'<div class="share-bar"', content)
    if share_bar_match:
        pattern = r'(</div>\s*\n)(\s*<div class="article-content">)'
        search_start = share_bar_match.start()
        match = re.search(pattern, content[search_start:])
        if match:
            abs_start = search_start + match.start()
            abs_end = search_start + match.end()
            replacement = match.group(1) + AUTHOR_BIO_HTML + '\n\n' + match.group(2).lstrip('\n')
            return content[:abs_start] + replacement + content[abs_end:], True

    # --- Strategy 2: no share-bar, article-content div exists (e.g. purchasing-power-parity) ---
    ac_match = re.search(r'(\n)([ \t]*<div class="article-content">)', content)
    if ac_match:
        insert_pos = ac_match.start() + 1  # after the newline
        indent = ac_match.group(2)[:len(ac_match.group(2)) - len(ac_match.group(2).lstrip())]
        bio_indented = '\n'.join(indent + line if line.strip() else line for line in AUTHOR_BIO_HTML.strip().split('\n'))
        new_content = content[:insert_pos] + bio_indented + '\n\n' + content[insert_pos:]
        return new_content, True

    # --- Strategy 3: no share-bar, article-body div follows h1 ---
    ab_match = re.search(r'(</h1>\s*\n)(\s*<div class="article-body">)', content)
    if ab_match:
        insert_pos = ab_match.start() + len(ab_match.group(1))
        indent = ab_match.group(2)[:len(ab_match.group(2)) - len(ab_match.group(2).lstrip())]
        bio_indented = '\n'.join(indent + line if line.strip() else line for line in AUTHOR_BIO_HTML.strip().split('\n'))
        new_content = content[:insert_pos] + '\n' + bio_indented + '\n\n' + content[insert_pos:]
        return new_content, True

    # --- Strategy 4: no share-bar, no article-content/body wrapper, direct <p> after h1 ---
    # Pattern: </h1>\n\n  <p>  OR  </h1>\n  <div class="meta">...\n\n  <p>
    h1_match = re.search(r'</h1>\s*\n', content)
    if h1_match:
        # Find the position right after the h1 closing tag line
        after_h1 = h1_match.end()
        # Check if there's a meta div right after
        meta_match = re.match(r'([ \t]*<div class="meta">.*?</div>\s*\n)', content[after_h1:], re.DOTALL)
        if meta_match:
            insert_pos = after_h1 + meta_match.end()
        else:
            insert_pos = after_h1

        # Detect indentation from surrounding content
        next_line_match = re.match(r'([ \t]*)', content[insert_pos:])
        indent = next_line_match.group(1) if next_line_match else '            '
        bio_indented = '\n'.join(indent + line if line.strip() else line for line in AUTHOR_BIO_HTML.strip().split('\n'))
        new_content = content[:insert_pos] + '\n' + bio_indented + '\n\n' + content[insert_pos:]
        return new_content, True

    print(f"  WARNING: Could not find insertion point for author bio in {filename}")
    return content, False


def add_newsletter(content, filename):
    """Insert newsletter signup before the last <footer tag."""
    if 'newsletter-blog-v1' in content:
        return content, False

    # Find the LAST <footer tag (with or without class)
    footer_matches = list(re.finditer(r'\n<footer[\s>]', content))
    if not footer_matches:
        # Try without leading newline
        footer_matches = list(re.finditer(r'<footer[\s>]', content))

    if not footer_matches:
        print(f"  WARNING: No <footer tag found in {filename}")
        return content, False

    last_footer = footer_matches[-1]
    insert_pos = last_footer.start()

    # Insert newsletter HTML before the footer
    new_content = content[:insert_pos] + '\n' + NEWSLETTER_HTML + content[insert_pos:]
    return new_content, True


def main():
    files = sorted(glob.glob(os.path.join(BLOG_DIR, '*.html')))
    print(f"Found {len(files)} blog articles in {BLOG_DIR}\n")

    bio_added = 0
    bio_skipped = 0
    bio_failed = 0
    newsletter_added = 0
    newsletter_skipped = 0
    newsletter_failed = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"Processing: {filename}")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Author bio
        if 'author-bio' in content:
            print(f"  Author bio: SKIPPED (already present)")
            bio_skipped += 1
            bio_ok = False
        else:
            content, bio_ok = add_author_bio(content, filename)
            if bio_ok:
                print(f"  Author bio: ADDED")
                bio_added += 1
            else:
                bio_failed += 1

        # Newsletter
        if 'newsletter-blog-v1' in content:
            print(f"  Newsletter: SKIPPED (already present)")
            newsletter_skipped += 1
            nl_ok = False
        else:
            content, nl_ok = add_newsletter(content, filename)
            if nl_ok:
                print(f"  Newsletter: ADDED")
                newsletter_added += 1
            else:
                newsletter_failed += 1

        # Write if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    print(f"\n{'='*50}")
    print(f"RESULTS")
    print(f"{'='*50}")
    print(f"Files processed:      {len(files)}")
    print(f"Author bio added:     {bio_added}")
    print(f"Author bio skipped:   {bio_skipped}")
    print(f"Author bio failed:    {bio_failed}")
    print(f"Newsletter added:     {newsletter_added}")
    print(f"Newsletter skipped:   {newsletter_skipped}")
    print(f"Newsletter failed:    {newsletter_failed}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
