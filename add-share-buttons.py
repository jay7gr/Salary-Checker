#!/usr/bin/env python3
"""
Adds share buttons (Twitter/X, LinkedIn, WhatsApp, Copy Link, Email)
to all page types across the salary-converter site.
"""

import os, re, glob, html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── CSS ──────────────────────────────────────────────────────────────────
SHARE_CSS = """
        .share-bar {
            display: flex; align-items: center; gap: 8px;
            margin: 16px 0 20px; padding: 12px 16px;
            background: var(--stat-card-bg, #f5f5f7); border-radius: 12px;
        }
        .share-bar-label {
            font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);
            text-transform: uppercase; letter-spacing: 0.5px; margin-right: 4px;
        }
        .share-btn {
            display: flex; align-items: center; justify-content: center;
            width: 34px; height: 34px; border-radius: 50%;
            border: 1px solid var(--border, #e5e5ea); background: var(--card-bg, #fff);
            color: var(--text-secondary, #86868b); cursor: pointer; transition: all 0.2s;
            padding: 0;
        }
        .share-btn:hover { color: var(--accent); border-color: var(--accent); transform: scale(1.08); }
        .share-btn.copied { color: #22c55e; border-color: #22c55e; }
"""

# ── SVG Icons ────────────────────────────────────────────────────────────
ICON_X = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" fill="currentColor"/></svg>'
ICON_LI = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/></svg>'
ICON_WA = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" fill="currentColor"/></svg>'
ICON_COPY = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_EMAIL = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="22,6 12,13 2,6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def share_bar_html(share_text, share_url):
    """Build the share bar HTML with data attributes."""
    t = html.escape(share_text, quote=True)
    u = html.escape(share_url, quote=True)
    return f'''<div class="share-bar" data-share-text="{t}" data-share-url="{u}">
            <span class="share-bar-label">Share</span>
            <button class="share-btn" data-platform="twitter" aria-label="Share on X" type="button">{ICON_X}</button>
            <button class="share-btn" data-platform="linkedin" aria-label="Share on LinkedIn" type="button">{ICON_LI}</button>
            <button class="share-btn" data-platform="whatsapp" aria-label="Share on WhatsApp" type="button">{ICON_WA}</button>
            <button class="share-btn" data-platform="copy" aria-label="Copy link" type="button">{ICON_COPY}</button>
            <button class="share-btn" data-platform="email" aria-label="Share via email" type="button">{ICON_EMAIL}</button>
        </div>'''


# ── JS ───────────────────────────────────────────────────────────────────
SHARE_JS = """
    <script>
    (function(){
        document.querySelectorAll('.share-bar').forEach(function(bar){
            var text=bar.getAttribute('data-share-text'),url=bar.getAttribute('data-share-url');
            bar.querySelectorAll('.share-btn').forEach(function(btn){
                btn.addEventListener('click',function(){
                    var p=btn.getAttribute('data-platform'),enc=encodeURIComponent(text+'\\n'+url);
                    if(p==='twitter')window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(text)+'&url='+encodeURIComponent(url),'_blank','width=550,height=420');
                    else if(p==='linkedin')window.open('https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent(url),'_blank','width=550,height=420');
                    else if(p==='whatsapp')window.open('https://wa.me/?text='+enc,'_blank');
                    else if(p==='email')window.location.href='mailto:?subject='+encodeURIComponent(text)+'&body='+enc;
                    else if(p==='copy'){navigator.clipboard.writeText(url).then(function(){btn.classList.add('copied');setTimeout(function(){btn.classList.remove('copied')},2000)})}
                });
            });
        });
    })();
    </script>"""


def get_canonical(content):
    """Extract canonical URL from page."""
    m = re.search(r'<link rel="canonical" href="(.*?)"', content)
    return m.group(1) if m else ''


def inject(content, css, html_block, js):
    """Inject CSS before </style>, HTML at landmark, JS before </body>."""
    # CSS
    content = content.replace('</style>', css + '\n    </style>', 1)
    # JS
    content = content.replace('</body>', js + '\n</body>', 1)
    # HTML is handled by caller (different per page type)
    return content


# ── COMPARISON PAGES ─────────────────────────────────────────────────────
def process_comparison(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'share-bar' in content:
        return False

    url = get_canonical(content)
    if not url:
        return False

    # Extract share text from answer box
    m = re.search(r'<p class="answer-box-answer"><strong>(.*?)</strong>', content)
    if m:
        share_text = html.unescape(m.group(1)) + ' — See the full comparison on salary:converter'
        # Inject after answer-box closing </div>
        bar = share_bar_html(share_text, url)
        content = content.replace('</div>\n<section class="content-card">', '</div>\n' + bar + '\n<section class="content-card">', 1)
    else:
        # Neighborhood comparison (no answer box) — extract from meta description
        m2 = re.search(r'<meta name="description" content="(.*?)"', content)
        share_text = html.unescape(m2.group(1)) if m2 else 'Compare on salary:converter'
        share_text += ' — salary:converter'
        bar = share_bar_html(share_text, url)
        # Inject after hero </section>
        content = content.replace('</section>\n\n        <div class="card">', '</section>\n' + bar + '\n        <div class="card">', 1)
        if bar not in content:
            # Fallback: try right after first </section>
            content = content.replace('</section>', '</section>\n' + bar, 1)

    content = inject(content, SHARE_CSS, bar, SHARE_JS)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


# ── SALARY-NEEDED PAGES ──────────────────────────────────────────────────
def process_salary_needed(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'share-bar' in content:
        return False

    url = get_canonical(content)
    if not url:
        return False

    # Index page (no salary cards)
    if '/salary-needed/index.html' in filepath or filepath.endswith('salary-needed/index.html'):
        share_text = 'What salary do you need to live comfortably? Find out for 100+ cities on salary:converter'
        bar = share_bar_html(share_text, url)
        # Inject after subtitle paragraph
        content = content.replace('<div class="city-grid">', bar + '\n        <div class="city-grid">', 1)
        content = inject(content, SHARE_CSS, bar, SHARE_JS)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    # City name
    m_city = re.search(r'<h1>What Salary Do You Need to Live in (.*?)\?</h1>', content)
    city_name = html.unescape(m_city.group(1)) if m_city else 'this city'

    # Comfortable tier amount
    m_amount = re.search(r'class="salary-card highlight">.*?<div class="salary-card-amount">(.*?)</div>', content, re.DOTALL)
    amount = html.unescape(m_amount.group(1)) if m_amount else ''

    if amount:
        share_text = f'You need {amount} to live comfortably in {city_name}. Full salary breakdown on salary:converter'
    else:
        share_text = f'What salary do you need in {city_name}? Find out on salary:converter'

    bar = share_bar_html(share_text, url)

    # Inject after salary-cards div
    if '</div>\n\n        <section class="content-card">' in content:
        content = content.replace('</div>\n\n        <section class="content-card">', '</div>\n\n        ' + bar + '\n\n        <section class="content-card">', 1)
    else:
        # Fallback: after first content-card heading
        content = content.replace('<section class="content-card">', bar + '\n        <section class="content-card">', 1)

    content = inject(content, SHARE_CSS, bar, SHARE_JS)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


# ── CITY PAGES ───────────────────────────────────────────────────────────
def process_city(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'share-bar' in content:
        return False

    url = get_canonical(content)
    if not url:
        return False

    # Extract city name, COLI, rank
    m_city = re.search(r'<h1>Cost of Living in (.*?)</h1>', content)
    city = html.unescape(m_city.group(1)) if m_city else ''

    m_coli = re.search(r'<div class="stat-value">([\d.]+)</div>\s*<div class="stat-label">COLI Index</div>', content)
    coli = m_coli.group(1) if m_coli else ''

    m_rank = re.search(r'<div class="stat-value">#(\d+)</div>\s*<div class="stat-label">', content)
    rank = m_rank.group(1) if m_rank else ''

    if city and coli:
        share_text = f'{city} cost of living index: {coli}'
        if rank:
            share_text += f' (ranked #{rank} of 101)'
        share_text += '. Compare salaries & neighborhoods on salary:converter'
    else:
        # Fallback: use meta description
        m_desc = re.search(r'<meta name="description" content="(.*?)"', content)
        share_text = html.unescape(m_desc.group(1)) if m_desc else f'Cost of living in {city} — salary:converter'

    bar = share_bar_html(share_text, url)

    # Inject after hero </section> (line ~344)
    hero_close = content.find('</section>')
    if hero_close != -1:
        insert_pos = hero_close + len('</section>')
        content = content[:insert_pos] + '\n        ' + bar + content[insert_pos:]

    content = inject(content, SHARE_CSS, bar, SHARE_JS)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


# ── BLOG ARTICLES ────────────────────────────────────────────────────────
def process_blog(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'share-bar' in content:
        return False

    url = get_canonical(content)
    if not url:
        return False

    # Extract title
    m = re.search(r'<h1>(.*?)</h1>', content)
    title = html.unescape(m.group(1)) if m else 'Article'
    share_text = f'{title} — salary:converter'

    bar = share_bar_html(share_text, url)

    # Inject between </header> and <div class="article-content">
    content = content.replace('</header>\n\n        <div class="article-content">', '</header>\n\n        ' + bar + '\n\n        <div class="article-content">', 1)

    content = inject(content, SHARE_CSS, bar, SHARE_JS)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


# ── MAIN ─────────────────────────────────────────────────────────────────
def main():
    totals = {'comparison': 0, 'salary_needed': 0, 'city': 0, 'blog': 0}
    errors = []

    # 1. Comparison pages
    files = glob.glob(os.path.join(BASE_DIR, 'compare', '*.html'))
    files += glob.glob(os.path.join(BASE_DIR, 'compare', '*', '*.html'))
    # Exclude index pages
    files = [f for f in files if not f.endswith('/index.html')]
    print(f"Processing {len(files)} comparison pages...")
    for f in sorted(files):
        try:
            if process_comparison(f):
                totals['comparison'] += 1
        except Exception as e:
            errors.append(f"  compare: {os.path.basename(f)}: {e}")

    # 2. Salary-needed pages
    files = glob.glob(os.path.join(BASE_DIR, 'salary-needed', '*.html'))
    files += glob.glob(os.path.join(BASE_DIR, 'salary-needed', '*', '*.html'))
    print(f"Processing {len(files)} salary-needed pages...")
    for f in sorted(files):
        try:
            if process_salary_needed(f):
                totals['salary_needed'] += 1
        except Exception as e:
            errors.append(f"  salary-needed: {os.path.basename(f)}: {e}")

    # 3. City pages
    files = glob.glob(os.path.join(BASE_DIR, 'city', '*.html'))
    files += glob.glob(os.path.join(BASE_DIR, 'city', '*', '*.html'))
    files = [f for f in files if not f.endswith('/index.html')]
    print(f"Processing {len(files)} city pages...")
    for f in sorted(files):
        try:
            if process_city(f):
                totals['city'] += 1
        except Exception as e:
            errors.append(f"  city: {os.path.basename(f)}: {e}")

    # 4. Blog articles
    files = glob.glob(os.path.join(BASE_DIR, 'blog', 'articles', '*.html'))
    print(f"Processing {len(files)} blog articles...")
    for f in sorted(files):
        try:
            if process_blog(f):
                totals['blog'] += 1
        except Exception as e:
            errors.append(f"  blog: {os.path.basename(f)}: {e}")

    print(f"\nDone!")
    print(f"  Comparison: {totals['comparison']}")
    print(f"  Salary-needed: {totals['salary_needed']}")
    print(f"  City: {totals['city']}")
    print(f"  Blog: {totals['blog']}")
    print(f"  Total: {sum(totals.values())}")
    if errors:
        print(f"\n{len(errors)} errors:")
        for e in errors[:20]:
            print(e)


if __name__ == '__main__':
    main()
