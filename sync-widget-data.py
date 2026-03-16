#!/usr/bin/env python3
"""
Sync JavaScript data blocks from index.html to embed.html.

Copies these const declarations from index.html -> embed.html:
  - coliData
  - exchangeRates
  - cityToCurrency
  - cityToCountry
  - cityNeighborhoods

Also adds missing exchange rates to both files.
"""

import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, 'index.html')
EMBED_PATH = os.path.join(BASE_DIR, 'embed.html')

VARIABLES = ['coliData', 'exchangeRates', 'cityToCurrency', 'cityToCountry', 'cityNeighborhoods']

# Missing exchange rates to add (currencies referenced in cityToCurrency but missing from exchangeRates)
MISSING_RATES = {
    'DOP': 76.8,
    'TZS': 3420,
    'GTQ': 10.28,
    'NPR': 176.8,
    'LAK': 28800,
    'LKR': 398,
    'GHS': 20.5,
    'TND': 4.12,
    'JOD': 0.942,
    'LBP': 119000,
    'OMR': 0.512,
    'GEL': 3.62,
    'AMD': 515,
    'MMK': 2790,
    'UGX': 4920,
    'ETB': 76.5,
    'XOF': 738,
    'BGN': 2.2,
    'RSD': 139,
    'BAM': 2.32,
    'ALL': 121,
    'BOB': 9.18,
}


def extract_block(content, var_name):
    """
    Extract a full `const VARNAME = { ... };` block from the content.

    Matches the opening `const VARNAME = {` and finds the closing `};`
    at the same indentation level (8 spaces).

    Returns (full_match_string, start_index, end_index) or None.
    """
    # Match: 8 spaces, optional comment line before, then const declaration
    # The pattern finds `const VARNAME = {` with 8-space indentation
    pattern = re.compile(
        r'^(        const ' + re.escape(var_name) + r' = \{)',
        re.MULTILINE
    )

    match = pattern.search(content)
    if not match:
        print(f"  ERROR: Could not find 'const {var_name}' in content")
        return None

    start = match.start()

    # Now find the closing `};` at 8-space indentation level
    # We need to track brace depth starting from the opening `{`
    brace_depth = 0
    i = match.start()

    while i < len(content):
        ch = content[i]
        if ch == '{':
            brace_depth += 1
        elif ch == '}':
            brace_depth -= 1
            if brace_depth == 0:
                # Found the matching closing brace
                # Include the semicolon after it
                end = i + 1
                if end < len(content) and content[end] == ';':
                    end += 1
                return content[start:end], start, end
        i += 1

    print(f"  ERROR: Could not find closing braces for 'const {var_name}'")
    return None


def add_missing_rates_to_block(block_text):
    """
    Add missing exchange rates before the closing `};` of the exchangeRates block.
    """
    # Find the last entry line before closing `};`
    # Pattern: find the last data line, remove its trailing newline, add comma if needed, then add new lines

    # Split into lines
    lines = block_text.split('\n')

    # Find the closing line (should be `        };`)
    closing_idx = None
    for idx in range(len(lines) - 1, -1, -1):
        if lines[idx].strip() == '};':
            closing_idx = idx
            break

    if closing_idx is None:
        print("  ERROR: Could not find closing }; in exchangeRates block")
        return block_text

    # Check if the last data line needs a trailing comma
    last_data_idx = closing_idx - 1
    last_data_line = lines[last_data_idx].rstrip()
    if last_data_line and not last_data_line.endswith(','):
        lines[last_data_idx] = last_data_line + ','

    # Build new rate lines
    new_lines = []
    rate_items = list(MISSING_RATES.items())
    for i, (currency, rate) in enumerate(rate_items):
        # Format: integer rates without decimal, others with decimal
        if isinstance(rate, float) and rate == int(rate) and rate >= 10:
            rate_str = str(int(rate))
        else:
            rate_str = str(rate)

        comma = ',' if i < len(rate_items) - 1 else ''
        new_lines.append(f"            '{currency}': {rate_str}{comma}")

    # Insert new lines before the closing line
    result_lines = lines[:closing_idx] + new_lines + lines[closing_idx:]
    return '\n'.join(result_lines)


def main():
    print("=" * 60)
    print("Syncing JavaScript data from index.html -> embed.html")
    print("=" * 60)

    # Read both files
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_content = f.read()
    print(f"Read index.html: {len(index_content):,} chars")

    with open(EMBED_PATH, 'r', encoding='utf-8') as f:
        embed_content = f.read()
    print(f"Read embed.html: {len(embed_content):,} chars")

    # --- Step 1: Add missing exchange rates to index.html ---
    print("\n--- Adding missing exchange rates to index.html ---")
    result = extract_block(index_content, 'exchangeRates')
    if result:
        old_block, start, end = result
        print(f"  Found exchangeRates in index.html ({end - start:,} chars)")
        new_block = add_missing_rates_to_block(old_block)
        index_content = index_content[:start] + new_block + index_content[end:]
        print(f"  Added {len(MISSING_RATES)} missing exchange rates to index.html")

    # Write updated index.html
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("  Wrote updated index.html")

    # --- Step 2: Extract blocks from (updated) index.html and replace in embed.html ---
    print("\n--- Syncing data blocks to embed.html ---")

    for var_name in VARIABLES:
        print(f"\nProcessing: {var_name}")

        # Extract from index.html
        index_result = extract_block(index_content, var_name)
        if not index_result:
            print(f"  SKIPPED: Could not extract from index.html")
            continue
        index_block, _, _ = index_result
        print(f"  Extracted from index.html: {len(index_block):,} chars")

        # Extract from embed.html (to find location to replace)
        embed_result = extract_block(embed_content, var_name)
        if not embed_result:
            print(f"  SKIPPED: Could not find in embed.html")
            continue
        embed_block, embed_start, embed_end = embed_result
        print(f"  Found in embed.html: {len(embed_block):,} chars (positions {embed_start}-{embed_end})")

        # Replace
        embed_content = embed_content[:embed_start] + index_block + embed_content[embed_end:]
        print(f"  Replaced! New block: {len(index_block):,} chars")

    # Write updated embed.html
    with open(EMBED_PATH, 'w', encoding='utf-8') as f:
        f.write(embed_content)
    print(f"\nWrote updated embed.html: {len(embed_content):,} chars")

    # --- Step 3: Verification ---
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    # Re-read and count cities in coliData for both files
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_final = f.read()
    with open(EMBED_PATH, 'r', encoding='utf-8') as f:
        embed_final = f.read()

    for filename, content in [('index.html', index_final), ('embed.html', embed_final)]:
        result = extract_block(content, 'coliData')
        if result:
            block = result[0]
            # Count entries: lines matching 'CityName': number pattern
            entries = re.findall(r"'[^']+'\s*:\s*[\d.]+", block)
            print(f"  {filename} coliData: {len(entries)} cities")

        result = extract_block(content, 'exchangeRates')
        if result:
            block = result[0]
            entries = re.findall(r"'[^']+'\s*:\s*[\d.]+", block)
            print(f"  {filename} exchangeRates: {len(entries)} currencies")

        result = extract_block(content, 'cityToCurrency')
        if result:
            block = result[0]
            entries = re.findall(r"'[^']+'\s*:\s*'[^']+'", block)
            print(f"  {filename} cityToCurrency: {len(entries)} mappings")

        result = extract_block(content, 'cityToCountry')
        if result:
            block = result[0]
            entries = re.findall(r"'[^']+'\s*:\s*'[^']+'", block)
            print(f"  {filename} cityToCountry: {len(entries)} mappings")

        result = extract_block(content, 'cityNeighborhoods')
        if result:
            block = result[0]
            # Count top-level city entries
            cities = re.findall(r"'[^']+'\s*:\s*\{", block)
            # Subtract 1 for the outer object opening
            print(f"  {filename} cityNeighborhoods: {len(cities) - 1} cities with neighborhoods")

    print("\nDone!")


if __name__ == '__main__':
    main()
