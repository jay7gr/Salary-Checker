#!/usr/bin/env python3
"""
One-time script: Rewrite city page meta descriptions to include
top neighborhood names for better CTR on neighborhood-specific queries.

Before: 1BR rent: $2,500/mo. Ranked #6/182 globally. You need ~£98,496/yr to live comfortably. 35 neighborhoods ranked. Compare salaries, tax rates & neighborhoods.
After:  1BR rent: $2,500/mo. Ranked #6/182 globally. £98,496/yr salary needed. 35 neighborhoods incl. Chelsea, Hampstead & Brixton. Taxes, groceries & salary data.
"""
import os, glob, re, sys

# Import cityNeighborhoods from generate-pages.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import util as imp_util

def load_city_neighborhoods():
    """Load cityNeighborhoods dict from generate-pages.py without running the whole script."""
    spec = imp_util.spec_from_file_location("gen", os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate-pages.py"))
    # We can't just import it (it would run main). Instead, parse the dict manually.
    # Safer approach: read the file and exec just the cityNeighborhoods assignment.
    gen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate-pages.py")
    with open(gen_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # Extract the cityNeighborhoods dict (starts at "cityNeighborhoods = {" and ends at matching "}")
    start = source.index('cityNeighborhoods = {')
    # Find the matching closing brace by counting braces
    depth = 0
    i = start + len('cityNeighborhoods = ')
    while i < len(source):
        if source[i] == '{':
            depth += 1
        elif source[i] == '}':
            depth -= 1
            if depth == 0:
                break
        i += 1

    dict_source = source[start:i+1]
    local_vars = {}
    exec(dict_source, {}, local_vars)
    return local_vars['cityNeighborhoods']

def slugify(name):
    """Match the slugify function from generate-pages.py."""
    slug = name.lower()
    slug = slug.replace(' (denpasar)', '')
    slug = slug.replace(' (cr)', '')
    slug = slug.replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('ü', 'u')
    slug = slug.replace('ú', 'u').replace('í', 'i').replace('ó', 'o')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def get_top_neighborhoods(neighborhoods_dict, n=3):
    """Pick the top N most recognizable neighborhoods.
    Strategy: pick a mix — 1 expensive, 1 mid-range, 1 affordable.
    This ensures diverse neighborhood names that match different search queries.
    """
    if not neighborhoods_dict or len(neighborhoods_dict) < 3:
        return list(neighborhoods_dict.keys())[:n] if neighborhoods_dict else []

    sorted_hoods = sorted(neighborhoods_dict.items(), key=lambda x: x[1], reverse=True)

    # Pick: most expensive, median, cheapest (but still recognizable)
    top = sorted_hoods[0][0]  # Most expensive / premium
    mid_idx = len(sorted_hoods) // 2
    mid = sorted_hoods[mid_idx][0]  # Median
    # For the third, pick something affordable but recognizable (around 25th percentile)
    affordable_idx = int(len(sorted_hoods) * 0.75)
    affordable = sorted_hoods[affordable_idx][0]

    # Clean up neighborhood names — remove parenthetical suffixes for brevity
    def clean_name(name):
        # "Manhattan (Midtown)" -> "Midtown Manhattan" is too long
        # "Brooklyn (Williamsburg)" -> "Williamsburg"
        # "Cambridge (Harvard Sq)" -> "Harvard Square"
        # Just use the name as-is but shorten parentheticals
        name = re.sub(r'\s*\([^)]*\)\s*$', '', name)
        return name.strip()

    result = [clean_name(top), clean_name(mid), clean_name(affordable)]
    # Remove duplicates (can happen after cleaning)
    seen = set()
    deduped = []
    for r in result:
        if r not in seen:
            seen.add(r)
            deduped.append(r)

    # If we lost some to dedup, fill from sorted list
    idx = 0
    while len(deduped) < n and idx < len(sorted_hoods):
        name = clean_name(sorted_hoods[idx][0])
        if name not in seen:
            deduped.append(name)
            seen.add(name)
        idx += 1

    return deduped[:n]

def fix_meta_description(filepath, city_name, neighborhoods):
    """Rewrite the meta description to include neighborhood names."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Match the current meta description pattern
    # Pattern: content="1BR rent: $X/mo. Ranked #Y/182 globally. You need ~CURRENCY/yr to live comfortably. Z neighborhoods ranked. Compare salaries, tax rates & neighborhoods."
    pattern = r'(<meta name="description" content=")([^"]*)(">)'
    match = re.search(pattern, content)
    if not match:
        return False, "no meta description found"

    current_desc = match.group(2)

    # Check if already modified (idempotency)
    if 'incl.' in current_desc:
        return False, "already modified"

    # Parse components from current description
    # "1BR rent: $2,500/mo. Ranked #6/182 globally. You need ~£98,496/yr to live comfortably. 35 neighborhoods ranked. Compare salaries, tax rates & neighborhoods."

    rent_match = re.search(r'(1BR rent: [^.]+\.)', current_desc)
    rank_match = re.search(r'(Ranked #\d+/182 globally\.)', current_desc)
    salary_match = re.search(r'You need ~([^/]+/yr)', current_desc)
    hood_count_match = re.search(r'(\d+) neighborhoods ranked', current_desc)

    if not all([rent_match, rank_match]):
        return False, "description doesn't match expected pattern"

    rent_part = rent_match.group(1)
    rank_part = rank_match.group(1)
    salary_part = salary_match.group(1) if salary_match else None
    hood_count = hood_count_match.group(1) if hood_count_match else None

    # Build neighborhood string
    if neighborhoods and len(neighborhoods) >= 2:
        hood_names = f"{neighborhoods[0]}, {neighborhoods[1]} & {neighborhoods[2]}" if len(neighborhoods) >= 3 else f"{neighborhoods[0]} & {neighborhoods[1]}"
        if hood_count:
            hood_part = f"{hood_count} neighborhoods incl. {hood_names}."
        else:
            hood_part = f"Neighborhoods incl. {hood_names}."
    elif hood_count:
        hood_part = f"{hood_count} neighborhoods ranked."
    else:
        hood_part = ""

    # Build new description
    if salary_part:
        new_desc = f"{rent_part} {rank_part} {salary_part} salary needed. {hood_part} Taxes, groceries & salary data."
    else:
        new_desc = f"{rent_part} {rank_part} {hood_part} Taxes, groceries & salary data."

    # Replace
    new_content = content[:match.start(2)] + new_desc + content[match.end(2):]

    if new_content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, new_desc

    return False, "no change"


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    city_files = glob.glob(os.path.join(base, 'city', '*.html'))

    print(f"Found {len(city_files)} city files")

    # Load neighborhoods data
    print("Loading neighborhood data from generate-pages.py...")
    city_neighborhoods = load_city_neighborhoods()
    print(f"Loaded neighborhoods for {len(city_neighborhoods)} cities")

    # Build slug -> city name mapping
    slug_to_city = {}
    for city_name in city_neighborhoods:
        slug = slugify(city_name)
        slug_to_city[slug] = city_name

    fixed = 0
    skipped = 0
    errors = 0

    for filepath in sorted(city_files):
        filename = os.path.basename(filepath)
        slug = filename.replace('.html', '')

        city_name = slug_to_city.get(slug)
        if not city_name:
            # Try to find by partial match
            skipped += 1
            continue

        neighborhoods = get_top_neighborhoods(city_neighborhoods.get(city_name, {}))

        success, detail = fix_meta_description(filepath, city_name, neighborhoods)
        if success:
            fixed += 1
            print(f"  FIXED: {filename} -> {detail[:80]}...")
        else:
            if detail == "already modified":
                skipped += 1
            elif detail == "no meta description found" or detail == "description doesn't match expected pattern":
                errors += 1
                print(f"  ERROR: {filename} - {detail}")
            else:
                skipped += 1

    print(f"\nResults: {fixed} fixed, {skipped} skipped, {errors} errors")
    print(f"Total: {fixed + skipped + errors} / {len(city_files)} files processed")


if __name__ == '__main__':
    main()
