#!/usr/bin/env python3
"""
One-time script to:
1. Add 'Salaries' nav link across all page types
2. Make job-title names clickable in compare page salary tables

Idempotency: Checks for 'salary-nav-v1' marker.
"""

import glob, os, re

MARKER = 'salary-nav-v1'
BASE = os.path.dirname(os.path.abspath(__file__))

# Job titles and their slugs (must match /salary/ page filenames)
JOB_SLUGS = {
    'Doctor (General)': 'doctor-general',
    'Surgeon': 'surgeon',
    'Dentist': 'dentist',
    'Pharmacist': 'pharmacist',
    'Nurse': 'nurse',
    'Psychologist': 'psychologist',
    'Software Engineer': 'software-engineer',
    'DevOps Engineer': 'devops-engineer',
    'Data Scientist': 'data-scientist',
    'Mechanical Engineer': 'mechanical-engineer',
    'Civil Engineer': 'civil-engineer',
    'Electrical Engineer': 'electrical-engineer',
    'Architect': 'architect',
    'UX Designer': 'ux-designer',
    'Product Manager': 'product-manager',
    'Project Manager': 'project-manager',
    'Financial Analyst': 'financial-analyst',
    'Accountant': 'accountant',
    'Business Analyst': 'business-analyst',
    'Consultant': 'consultant',
    'Investment Banker': 'investment-banker',
    'Actuary': 'actuary',
    'Lawyer': 'lawyer',
    'Paralegal': 'paralegal',
    'Marketing Manager': 'marketing-manager',
    'Sales Manager': 'sales-manager',
    'Graphic Designer': 'graphic-designer',
    'Content Writer': 'content-writer',
    'HR Manager': 'hr-manager',
    'Operations Manager': 'operations-manager',
    'CEO / Executive': 'ceo-executive',
    'Teacher': 'teacher',
    'Professor': 'professor',
    'Research Scientist': 'research-scientist',
    'Pilot': 'pilot',
    'Chef': 'chef',
    'Journalist': 'journalist',
}

SALARY_NAV_LINK = '<a href="/salary/">Salaries</a>'


def add_nav_link(content, relpath):
    """Add Salaries nav link. Returns modified content or None if no match/change."""

    # ---------------------------------------------------------------
    # Pattern 1: Rankings pages (inline-style nav div)
    #   <a href="/compare/">Compare</a>  <a href="/blog/">Blog</a>
    # Also matches their footer:
    #   <a href="/compare/">Compare</a>  <a href="/blog/">Blog</a>
    # We insert Salaries between Compare and Blog.
    # Use replace_all=False (count=1 per call), but call for each occurrence.
    # ---------------------------------------------------------------
    pat_compare_blog = re.compile(
        r'(<a href="/compare/">Compare</a>)'
        r'(\s+)'
        r'(<a href="/blog/">Blog</a>)'
    )
    if pat_compare_blog.search(content):
        content = pat_compare_blog.sub(
            r'\1\2' + SALARY_NAV_LINK + r'\2\3',
            content
        )
        return content

    # ---------------------------------------------------------------
    # Pattern 2: City, compare, neighborhood pages (nav-links div)
    #   <a href="/compare/">City Comparisons</a>  <a href="/blog/">Blog</a>
    # Also matches footers with same pattern.
    # Insert Salaries between City Comparisons and Blog.
    # Additionally handle footer variants for neighborhood pages:
    #   <a href="/city/">All Cities</a>  <a href="/blog/">Blog</a>
    #   <a href="/compare/">All Comparisons</a>  <a href="/blog/">Blog</a>
    # ---------------------------------------------------------------
    pat_citycomp_blog = re.compile(
        r'(<a href="/compare/">City Comparisons</a>)'
        r'(\s+)'
        r'(<a href="/blog/">Blog</a>)'
    )
    if pat_citycomp_blog.search(content):
        content = pat_citycomp_blog.sub(
            r'\1\2' + SALARY_NAV_LINK + r'\2\3',
            content
        )
        # Also handle neighborhood footer variants
        pat_footer_allcities = re.compile(
            r'(<a href="/city/">All Cities</a>)'
            r'(\s+)'
            r'(<a href="/blog/">Blog</a>)'
        )
        if pat_footer_allcities.search(content):
            content = pat_footer_allcities.sub(
                r'\1\2' + SALARY_NAV_LINK + r'\2\3',
                content
            )
        pat_footer_allcomp = re.compile(
            r'(<a href="/compare/">All Comparisons</a>)'
            r'(\s+)'
            r'(<a href="/blog/">Blog</a>)'
        )
        if pat_footer_allcomp.search(content):
            content = pat_footer_allcomp.sub(
                r'\1\2' + SALARY_NAV_LINK + r'\2\3',
                content
            )
        return content

    # ---------------------------------------------------------------
    # Pattern 3: Homepage — two separate insertions needed
    #   3a: Desktop header links (blog-link class with left positions)
    #   3b: Mobile nav-dropdown (emoji-prefixed links)
    # ---------------------------------------------------------------
    pat3a = re.compile(
        r'(<a href="/compare/" class="blog-link" style="left: 150px;">City Comparisons</a>)'
        r'(\s+)'
        r'(<a href="/blog/" class="blog-link" style="left: 235px;">Blog</a>)'
    )
    matched_homepage = False
    if pat3a.search(content):
        content = pat3a.sub(
            r'\1\2'
            '<a href="/salary/" class="blog-link" style="left: 250px;">Salaries</a>'
            r'\2'
            '<a href="/blog/" class="blog-link" style="left: 330px;">Blog</a>',
            content, count=1
        )
        matched_homepage = True

    pat3b = re.compile(
        r'(<a href="/salary-needed/"><span>\U0001f4b0</span>Salary Needed</a>)'
        r'(\s+)'
        r'(<a href="/blog/">)'
    )
    if pat3b.search(content):
        content = pat3b.sub(
            r'\1\2'
            '<a href="/salary/"><span>\U0001f4bc</span>Salaries by Job</a>'
            r'\2\3',
            content, count=1
        )
        matched_homepage = True

    if matched_homepage:
        return content

    # ---------------------------------------------------------------
    # Pattern 4: Blog article pages
    #   <a href="https://salary-converter.com">Tool</a>
    #   <a href="/blog/">Blog</a>
    # Insert Salaries between Tool and Blog.
    # ---------------------------------------------------------------
    pat4 = re.compile(
        r'(<a href="https://salary-converter\.com">Tool</a>)'
        r'(\s+)'
        r'(<a href="/blog/">Blog</a>)'
    )
    if pat4.search(content):
        return pat4.sub(
            r'\1\2' + SALARY_NAV_LINK + r'\2\3',
            content, count=1
        )

    # ---------------------------------------------------------------
    # Pattern 5: Blog index page
    #   <a href="https://salary-converter.com" class="nav-link-text">Tool</a>
    #   <a href="/blog/" class="active nav-link-text">Blog</a>
    # ---------------------------------------------------------------
    pat5 = re.compile(
        r'(<a href="https://salary-converter\.com" class="nav-link-text">Tool</a>)'
        r'(\s+)'
        r'(<a href="/blog/" class="active nav-link-text">Blog</a>)'
    )
    if pat5.search(content):
        return pat5.sub(
            r'\1\2'
            '<a href="/salary/" class="nav-link-text">Salaries</a>'
            r'\2\3',
            content, count=1
        )

    # ---------------------------------------------------------------
    # Pattern 6: Salary-needed pages (no nav bar at all)
    #   <body>\n    <button class="theme-toggle"
    # Add a minimal inline nav bar before the theme toggle.
    # ---------------------------------------------------------------
    pat6 = re.compile(
        r'(<body>)'
        r'(\s+)'
        r'(<button class="theme-toggle")'
    )
    if pat6.search(content):
        nav_html = (
            '\n    <div style="max-width:900px; margin:0 auto; padding:12px 24px 0; '
            'display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">'
            '\n        <a href="/" style="color:var(--text-primary); text-decoration:none; '
            'font-weight:600; font-size:0.85rem;">salary<span style="color:var(--accent);">:</span>converter</a>'
            '\n        <div style="display:flex; align-items:center; gap:14px;">'
            '\n            <a href="/city/" style="color:var(--text-secondary); text-decoration:none; '
            'font-size:0.8rem; font-weight:500;">Cities</a>'
            '\n            <a href="/compare/" style="color:var(--text-secondary); text-decoration:none; '
            'font-size:0.8rem; font-weight:500;">Compare</a>'
            '\n            <a href="/salary/" style="color:var(--text-secondary); text-decoration:none; '
            'font-size:0.8rem; font-weight:500;">Salaries</a>'
            '\n            <a href="/blog/" style="color:var(--text-secondary); text-decoration:none; '
            'font-size:0.8rem; font-weight:500;">Blog</a>'
            '\n        </div>'
            '\n    </div>'
        )
        return pat6.sub(
            r'\1' + nav_html + r'\2\3',
            content, count=1
        )

    # ---------------------------------------------------------------
    # Pattern 7: 404 page
    #   <a href="/compare/">Compare Cities</a>
    #   <a href="/blog/">Read Blog</a>
    # ---------------------------------------------------------------
    pat7 = re.compile(
        r'(<a href="/compare/">Compare Cities</a>)'
        r'(\s+)'
        r'(<a href="/blog/">Read Blog</a>)'
    )
    if pat7.search(content):
        return pat7.sub(
            r'\1\2'
            '<a href="/salary/">Salaries</a>'
            r'\2\3',
            content, count=1
        )

    # ---------------------------------------------------------------
    # Pattern 8: compare/index.html — nav has Cities then Blog (no Compare link)
    #   <a href="/city/">Cities</a>  <a href="/blog/">Blog</a>
    # Insert Salaries between Cities and Blog.
    # Also handle footer: <a href="/city/">All Cities</a> <a href="/blog/">Blog</a>
    # ---------------------------------------------------------------
    pat8_nav = re.compile(
        r'(<a href="/city/">Cities</a>)'
        r'(\s+)'
        r'(<a href="/blog/">Blog</a>)'
    )
    pat8_footer = re.compile(
        r'(<a href="/city/">All Cities</a>)'
        r'(\s+)'
        r'(<a href="/blog/">Blog</a>)'
    )
    matched_8 = False
    if pat8_nav.search(content):
        content = pat8_nav.sub(
            r'\1\2' + SALARY_NAV_LINK + r'\2\3',
            content
        )
        matched_8 = True
    if pat8_footer.search(content):
        content = pat8_footer.sub(
            r'\1\2' + SALARY_NAV_LINK + r'\2\3',
            content
        )
        matched_8 = True
    if matched_8:
        return content

    # ---------------------------------------------------------------
    # Pattern 9: Privacy page — footer only
    #   <a href="/">Tool</a>  <a href="/blog/">Blog</a>
    # ---------------------------------------------------------------
    pat9 = re.compile(
        r'(<a href="/">Tool</a>)'
        r'(\s+)'
        r'(<a href="/blog/">Blog</a>)'
    )
    if pat9.search(content):
        return pat9.sub(
            r'\1\2' + SALARY_NAV_LINK + r'\2\3',
            content, count=1
        )

    return None


def linkify_job_titles(content):
    """Make job titles clickable in salary comparison tables on compare pages.
    Returns modified content or None if no changes."""
    changed = False
    for title, slug in JOB_SLUGS.items():
        escaped_title = re.escape(title)
        pattern = re.compile(
            r'(<td style="font-weight: 500;">)'
            + escaped_title
            + r'(</td>)'
        )
        if pattern.search(content):
            link = (
                f'<a href="/salary/{slug}" '
                f'style="color: var(--text-primary); text-decoration: underline dotted; '
                f'text-underline-offset: 3px;">{title}</a>'
            )
            content = pattern.sub(r'\1' + link + r'\2', content)
            changed = True
    return content if changed else None


def process_all_pages():
    """Process all HTML files."""
    html_files = glob.glob(os.path.join(BASE, '**', '*.html'), recursive=True)
    html_files.sort()

    # Skip files that don't have meaningful navigation
    SKIP_FILES = {'embed.html', 'widget.html'}

    stats = {
        'nav_updated': 0,
        'nav_skipped': 0,
        'nav_no_match': 0,
        'jobs_linked': 0,
        'errors': 0,
    }

    for filepath in html_files:
        relpath = os.path.relpath(filepath, BASE)
        basename = os.path.basename(filepath)

        if basename in SKIP_FILES:
            stats['nav_skipped'] += 1
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if MARKER in content:
                stats['nav_skipped'] += 1
                continue

            modified = False
            new_content = content

            # --- Part 1: Add nav link ---
            # Skip salary pages (they already have the Salaries nav link)
            is_salary_page = (
                relpath.startswith('salary' + os.sep)
                and not relpath.startswith('salary-needed')
            )
            if is_salary_page:
                stats['nav_skipped'] += 1
            else:
                nav_result = add_nav_link(new_content, relpath)
                if nav_result is not None:
                    new_content = nav_result
                    modified = True
                    stats['nav_updated'] += 1
                else:
                    stats['nav_no_match'] += 1
                    print(f'  No nav match: {relpath}')

            # --- Part 2: Linkify job titles in compare pages ---
            # Only top-level compare pages (city-vs-city), not neighborhood comparisons
            is_compare_page = (
                relpath.startswith('compare' + os.sep)
                and relpath.count(os.sep) == 1
                and os.path.basename(relpath) != 'index.html'
            )
            if is_compare_page:
                jobs_result = linkify_job_titles(new_content)
                if jobs_result is not None:
                    new_content = jobs_result
                    modified = True
                    stats['jobs_linked'] += 1

            # Write back if anything changed
            if modified:
                # Insert idempotency marker as an HTML comment near the top
                new_content = new_content.replace(
                    '<!DOCTYPE html>',
                    f'<!-- {MARKER} --><!DOCTYPE html>',
                    1
                )
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'  Updated: {relpath}')

        except Exception as e:
            print(f'  ERROR: {relpath} — {e}')
            stats['errors'] += 1

    print()
    print('=== Summary ===')
    print(f"  Nav updated:    {stats['nav_updated']}")
    print(f"  Nav skipped:    {stats['nav_skipped']} (already done or salary/skip pages)")
    print(f"  Nav no match:   {stats['nav_no_match']} (no recognized nav pattern)")
    print(f"  Jobs linked:    {stats['jobs_linked']} compare pages")
    print(f"  Errors:         {stats['errors']}")
    print(f"  Total files:    {len(html_files)}")


def main():
    print(f'add-salary-links.py — processing all HTML files in {BASE}')
    print(f'Idempotency marker: {MARKER}')
    print()
    process_all_pages()


if __name__ == '__main__':
    main()
