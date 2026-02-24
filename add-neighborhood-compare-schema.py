#!/usr/bin/env python3
"""
Add Article + FAQPage structured data (JSON-LD) to neighborhood comparison pages.

These pages (compare/{city}/{n1}-vs-{n2}.html) currently only have BreadcrumbList schema.
City-level comparison pages have Article + BreadcrumbList + FAQPage, giving them
rich snippet eligibility. This script closes the gap for ~909 neighborhood pages.

Data is extracted from existing page content (title, description, rents, multipliers, etc.)
to generate contextual FAQ questions and answers.

Idempotent: skips pages that already have FAQPage schema.
"""

import os
import re
import json
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

stats = {'updated': 0, 'skipped': 0, 'errors': 0}


def extract_page_data(content):
    """Extract data points from the neighborhood comparison page HTML."""
    data = {}

    # Title: "Mayfair vs Kensington, London: Which Is Cheaper? Neighborhood Comparison 2026"
    # or old format: "Mayfair vs Kensington, London — Cost of Living Comparison"
    m = re.search(r'<title>(.+?) vs (.+?),\s*(.+?)[\s:—–]', content)
    if not m:
        return None
    data['n1'] = m.group(1).strip()
    data['n2'] = m.group(2).strip()
    data['city'] = m.group(3).strip()

    # Meta description — extract cheaper neighborhood and percentage
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', content)
    data['description'] = desc_m.group(1) if desc_m else ''

    # Percentage cheaper: "7% cheaper" or "7% more expensive" or "7% more affordable"
    pct_m = re.search(r'(\d+)% (?:cheaper|more affordable)', data['description'])
    if pct_m:
        data['pct'] = pct_m.group(1)
    else:
        # Try from body content: "7% more expensive"
        exp_m = re.search(r'(\d+)% more expensive', content)
        data['pct'] = exp_m.group(1) if exp_m else None

    # Figure out which is cheaper from description
    # "Kensington is 7% cheaper than Mayfair"
    cheaper_m = re.search(r'([\w][\w\s\(\)\-\.\']+?) is \d+% cheaper', data['description'])
    if cheaper_m:
        data['cheaper'] = cheaper_m.group(1).strip()
        data['expensive'] = data['n1'] if data['cheaper'] == data['n2'] else data['n2']
    else:
        # Try "X is Y% more expensive than Z"
        exp_m2 = re.search(r'([\w][\w\s\(\)\-\.\']+?) is <strong>\d+% more expensive</strong> than ([\w][\w\s\(\)\-\.\']+)', content)
        if exp_m2:
            data['expensive'] = exp_m2.group(1).strip()
            data['cheaper'] = exp_m2.group(2).strip()
        else:
            data['cheaper'] = None
            data['expensive'] = None

    # Rents: look for "Est. 1BR Rent" values
    rent_matches = re.findall(r'<div class="val">([^<]*)</div>\s*<div class="lbl">Est\. 1BR Rent</div>', content)
    if len(rent_matches) >= 2:
        data['rent1'] = rent_matches[0].strip()
        data['rent2'] = rent_matches[1].strip()
    else:
        data['rent1'] = None
        data['rent2'] = None

    # Multipliers: "1.45x"
    mult_matches = re.findall(r'<div class="val">([\d.]+)x</div>\s*<div class="lbl">.*?Multiplier</div>', content)
    if len(mult_matches) >= 2:
        data['mult1'] = mult_matches[0]
        data['mult2'] = mult_matches[1]
    else:
        data['mult1'] = None
        data['mult2'] = None

    # Salary equivalents: "$75K Equivalent"
    equiv_matches = re.findall(r'<div class="val">([^<]*)</div>\s*<div class="lbl">\$75K Equivalent</div>', content)
    if len(equiv_matches) >= 2:
        data['equiv1'] = equiv_matches[0].strip()
        data['equiv2'] = equiv_matches[1].strip()
    else:
        data['equiv1'] = None
        data['equiv2'] = None

    # Canonical URL
    canon_m = re.search(r'<link rel="canonical" href="([^"]*)"', content)
    data['url'] = canon_m.group(1) if canon_m else ''

    return data


def build_article_schema(data):
    """Build Article JSON-LD schema."""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{data['n1']} vs {data['n2']}, {data['city']}: Neighborhood Cost of Living Comparison 2026",
        "description": data['description'],
        "url": data['url'],
        "datePublished": "2026-02-18",
        "dateModified": "2026-02-23",
        "publisher": {
            "@type": "Organization",
            "name": "salary:converter",
            "url": "https://salary-converter.com"
        }
    }


def build_faq_schema(data):
    """Build FAQPage JSON-LD schema with 4-6 contextual questions."""
    questions = []
    n1, n2, city = data['n1'], data['n2'], data['city']

    # Q1: Which is cheaper?
    if data.get('cheaper') and data.get('pct'):
        questions.append({
            "@type": "Question",
            "name": f"Is {n1} or {n2} cheaper in {city}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"{data['cheaper']} is approximately {data['pct']}% cheaper than {data['expensive']} in {city}, based on rent and local cost-of-living multipliers."
            }
        })
    else:
        questions.append({
            "@type": "Question",
            "name": f"Is {n1} or {n2} cheaper in {city}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Compare {n1} and {n2} side by side on salary-converter.com to see which {city} neighborhood is more affordable based on rent, expenses, and salary equivalents."
            }
        })

    # Q2: Rent comparison
    if data.get('rent1') and data.get('rent2'):
        questions.append({
            "@type": "Question",
            "name": f"What is the rent difference between {n1} and {n2} in {city}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Estimated 1-bedroom rent in {n1} is {data['rent1']}/month, compared to {data['rent2']}/month in {n2}."
            }
        })

    # Q3: Cost multiplier
    if data.get('mult1') and data.get('mult2'):
        questions.append({
            "@type": "Question",
            "name": f"What are the cost-of-living multipliers for {n1} and {n2}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"{n1} has a cost multiplier of {data['mult1']}x and {n2} has {data['mult2']}x relative to the {city} average. Higher multipliers mean higher living costs in that neighborhood."
            }
        })

    # Q4: Salary equivalent
    if data.get('equiv1') and data.get('equiv2'):
        questions.append({
            "@type": "Question",
            "name": f"What salary do I need in {n1} vs {n2}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"A $75,000 USD salary is equivalent to approximately {data['equiv1']} in {n1} and {data['equiv2']} in {n2}, after adjusting for neighborhood-level cost of living in {city}."
            }
        })

    # Q5: General comparison question
    questions.append({
        "@type": "Question",
        "name": f"How do I compare the cost of living between {n1} and {n2}?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": f"Use the salary converter at salary-converter.com to compare {n1} and {n2} in {city}. The tool accounts for rent, groceries, transport, utilities, healthcare, and tax differences at the neighborhood level."
        }
    })

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": questions
    }


def process_file(filepath):
    """Add Article + FAQPage schemas to a single neighborhood comparison page."""
    try:
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # Idempotency: skip if FAQPage already present
        if '"FAQPage"' in content:
            stats['skipped'] += 1
            return

        # Extract data from page
        data = extract_page_data(content)
        if not data:
            stats['skipped'] += 1
            return

        # Build schemas
        article = build_article_schema(data)
        faq = build_faq_schema(data)

        # Format as JSON-LD script blocks
        article_block = f'''    <script type="application/ld+json">
    {json.dumps(article, indent=8, ensure_ascii=False)}
    </script>'''

        faq_block = f'''    <script type="application/ld+json">
    {json.dumps(faq, indent=8, ensure_ascii=False)}
    </script>'''

        # Insert after the existing BreadcrumbList </script> block, before <style>
        # Pattern: find the closing </script> of the BreadcrumbList, then insert before <style>
        insertion = f'\n{article_block}\n{faq_block}\n'

        # Find the BreadcrumbList script block end and insert after it
        pattern = r'(</script>\s*\n)(\s*<style>)'
        match = re.search(pattern, content)
        if match:
            insert_pos = match.start(2)
            content = content[:insert_pos] + insertion + content[insert_pos:]
        else:
            # Fallback: insert before </head>
            content = content.replace('</head>', insertion + '</head>')

        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(content)
        stats['updated'] += 1

    except Exception as e:
        print(f'  ERROR {filepath}: {e}')
        stats['errors'] += 1


def main():
    print('Adding Article + FAQPage schema to neighborhood comparison pages...\n')

    for city_dir in sorted(glob.glob(os.path.join(BASE, 'compare', '*'))):
        if not os.path.isdir(city_dir):
            continue

        city_slug = os.path.basename(city_dir)
        city_files = sorted(glob.glob(os.path.join(city_dir, '*.html')))
        # Skip index.html (city-level comparison page)
        neigh_files = [f for f in city_files if os.path.basename(f) != 'index.html']

        if not neigh_files:
            continue

        prev_updated = stats['updated']
        for filepath in neigh_files:
            process_file(filepath)

        city_updated = stats['updated'] - prev_updated
        if city_updated > 0:
            print(f'  {city_slug}: {city_updated} pages updated')

    print(f'\n=== TOTAL: {stats["updated"]} updated, {stats["skipped"]} skipped, {stats["errors"]} errors ===')


if __name__ == '__main__':
    main()
