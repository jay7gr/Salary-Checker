#!/usr/bin/env python3
"""
Adds "Is X Cheaper Than Y?" answer boxes to all comparison pages.
Also adds new FAQ schema entries for "is X cheaper than Y" queries.
"""

import os, re, json, glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPARE_DIR = os.path.join(BASE_DIR, 'compare')

# CSS for the answer box (will be injected once per file)
ANSWER_BOX_CSS = """
        .answer-box {
            background: var(--card-bg); border-radius: 20px; padding: 28px 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
            border-left: 4px solid #22c55e;
        }
        .answer-box.more-expensive { border-left-color: #ef4444; }
        .answer-box.similar { border-left-color: #f59e0b; }
        .answer-box-question {
            font-size: 1.1rem; font-weight: 700; color: var(--text-primary);
            margin-bottom: 8px;
        }
        .answer-box-answer {
            font-size: 1rem; color: var(--text-body); line-height: 1.6;
        }
        .answer-box-answer strong { color: var(--text-primary); }
        .answer-box-stat {
            display: inline-block; background: var(--stat-card-bg); border-radius: 8px;
            padding: 4px 10px; font-weight: 700; font-size: 0.9rem; margin-top: 8px;
        }
        .answer-box-stat.cheaper { color: #22c55e; }
        .answer-box-stat.pricier { color: #ef4444; }
"""

def extract_city_names(filename):
    """Extract city names from filename like 'london-vs-new-york.html'."""
    base = os.path.basename(filename).replace('.html', '')
    parts = base.split('-vs-')
    if len(parts) != 2:
        return None, None
    return parts[0], parts[1]

def slug_to_name(slug):
    """Convert a slug back to city name by reading the page's title."""
    return None  # We'll extract from the page content instead

def process_file(filepath):
    """Add answer box to a single comparison page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has answer box
    if 'answer-box' in content:
        return False

    # Extract city names from <h1> tag
    h1_match = re.search(r'<h1>(.*?)<span class="vs-badge">VS</span>(.*?)</h1>', content)
    if not h1_match:
        return False
    city_a = h1_match.group(1).strip()
    city_b = h1_match.group(2).strip()

    # Extract COLI values from the hero section
    # Pattern: <div class="value">87.5</div>\n<div class="label">COLI Index</div>
    coli_matches = re.findall(r'<div class="value">([\d.]+)</div>\s*<div class="label">COLI Index</div>', content)
    if len(coli_matches) < 2:
        return False
    coli_a = float(coli_matches[0])
    coli_b = float(coli_matches[1])

    # Calculate difference
    if coli_a < coli_b:
        cheaper = city_a
        pricier = city_b
        diff_pct = round((coli_b - coli_a) / coli_b * 100)
        box_class = ''
    elif coli_b < coli_a:
        cheaper = city_b
        pricier = city_a
        diff_pct = round((coli_a - coli_b) / coli_a * 100)
        box_class = ''
    else:
        cheaper = None
        pricier = None
        diff_pct = 0
        box_class = ' similar'

    # Build the answer box HTML
    if cheaper:
        answer_text = f'<strong>Yes, {cheaper} is {diff_pct}% cheaper than {pricier}</strong> based on our cost of living index. {cheaper} has a COLI of {min(coli_a, coli_b)}, while {pricier} has a COLI of {max(coli_a, coli_b)}.'
        stat_html = f'<span class="answer-box-stat cheaper">{diff_pct}% cheaper</span>'

        # "Is city_a cheaper than city_b?"
        if cheaper == city_a:
            question_text = f"Is {city_a} cheaper than {city_b}?"
            answer_full = f"Yes, {city_a} is {diff_pct}% cheaper than {city_b} based on cost of living data."
        else:
            question_text = f"Is {city_a} cheaper than {city_b}?"
            answer_full = f"No, {city_a} is actually {diff_pct}% more expensive than {city_b} based on cost of living data."
    else:
        answer_text = f'<strong>{city_a} and {city_b} have a similar cost of living.</strong> Both cities have a COLI of {coli_a}.'
        stat_html = '<span class="answer-box-stat">Similar cost</span>'
        question_text = f"Is {city_a} cheaper than {city_b}?"
        answer_full = f"{city_a} and {city_b} have similar costs of living (both COLI {coli_a})."

    answer_box_html = f'''
        <div class="answer-box{box_class}">
            <div class="answer-box-question">{question_text}</div>
            <p class="answer-box-answer">{answer_text} {stat_html}</p>
        </div>
'''

    # Also create reverse question FAQ entries
    faq_new_entries = []

    # "Is CityA cheaper than CityB?"
    faq_new_entries.append({
        "@type": "Question",
        "name": f"Is {city_a} cheaper than {city_b}?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": f"{'Yes' if cheaper == city_a else 'No'}, {city_a} is {'cheaper' if cheaper == city_a else 'more expensive'} than {city_b}. {city_a} has a COLI of {coli_a} while {city_b} has a COLI of {coli_b}, making {cheaper} approximately {diff_pct}% cheaper." if cheaper else f"{city_a} and {city_b} have a similar cost of living with COLI of {coli_a}."
        }
    })

    # "Is CityB cheaper than CityA?"
    faq_new_entries.append({
        "@type": "Question",
        "name": f"Is {city_b} cheaper than {city_a}?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": f"{'Yes' if cheaper == city_b else 'No'}, {city_b} is {'cheaper' if cheaper == city_b else 'more expensive'} than {city_a}. {city_b} has a COLI of {coli_b} while {city_a} has a COLI of {coli_a}, making {cheaper} approximately {diff_pct}% cheaper." if cheaper else f"{city_a} and {city_b} have a similar cost of living with COLI of {coli_a}."
        }
    })

    # "How much cheaper is CityA than CityB?"
    if cheaper:
        faq_new_entries.append({
            "@type": "Question",
            "name": f"How much cheaper is {cheaper} than {pricier}?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"{cheaper} is approximately {diff_pct}% cheaper than {pricier} overall. {cheaper} has a cost of living index of {min(coli_a, coli_b)} compared to {max(coli_a, coli_b)} for {pricier}."
            }
        })

    # "What salary do I need in CityA compared to CityB?"
    city_a_slug = re.sub(r'[^a-z0-9]+', '-', city_a.lower()).strip('-')
    city_b_slug = re.sub(r'[^a-z0-9]+', '-', city_b.lower()).strip('-')
    faq_new_entries.append({
        "@type": "Question",
        "name": f"What salary do I need in {city_a} compared to {city_b}?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": f"If you earn a given salary in {city_b}, you'd need {diff_pct}% {'less' if cheaper == city_a else 'more'} in {city_a} to maintain the same standard of living, due to cost of living differences. Use our salary converter at salary-converter.com for an exact calculation." if cheaper else f"Since {city_a} and {city_b} have similar costs of living, you'd need roughly the same salary in either city."
        }
    })

    # 1. Insert CSS before </style>
    if 'answer-box' not in content:
        content = content.replace('    </style>', ANSWER_BOX_CSS + '    </style>', 1)

    # 2. Insert answer box after hero </section> and before first <section class="content-card">
    # Find the hero section end
    hero_pattern = re.compile(r'(</section>)\s*(<section class="content-card">)', re.DOTALL)
    hero_match = hero_pattern.search(content)
    if hero_match:
        insert_pos = hero_match.start(2)
        content = content[:insert_pos] + answer_box_html + content[insert_pos:]

    # 3. Add new FAQ entries to existing FAQPage schema
    faq_pattern = re.compile(r'("@type":\s*"FAQPage",\s*"mainEntity":\s*\[)(.*?)(\]\s*\})', re.DOTALL)
    faq_match = faq_pattern.search(content)
    if faq_match:
        existing_entries = faq_match.group(2).strip()
        new_entries_json = ', '.join(json.dumps(entry) for entry in faq_new_entries)
        if existing_entries:
            new_main_entity = existing_entries + ', ' + new_entries_json
        else:
            new_main_entity = new_entries_json
        content = content[:faq_match.start(2)] + new_main_entity + content[faq_match.end(2):]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


# Process all comparison pages
files = glob.glob(os.path.join(COMPARE_DIR, '*-vs-*.html'))
print(f"Found {len(files)} comparison pages")

success = 0
skipped = 0
errors = 0

for filepath in sorted(files):
    try:
        if process_file(filepath):
            success += 1
        else:
            skipped += 1
    except Exception as e:
        errors += 1
        if errors <= 5:
            print(f"  Error processing {os.path.basename(filepath)}: {e}")

print(f"\nDone! Added answer boxes to {success} pages")
print(f"Skipped: {skipped}, Errors: {errors}")
print(f"Total processed: {success + skipped + errors}")
