#!/usr/bin/env python3
"""
Inject neighborhood data from neighborhood-data-compiled.js into index.html.

Extracts the salaryNeighborhoodsNew entries and adds them to the
cityNeighborhoods object in index.html.

Usage:
    python3 inject_neighborhoods.py           # dry run (default)
    python3 inject_neighborhoods.py --apply   # actually write changes
"""

import re
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'neighborhood-data-compiled.js')
TARGET_FILE = os.path.join(SCRIPT_DIR, 'index.html')

IDEMPOTENCY_KEY = "'Faro'"  # First city in salaryNeighborhoodsNew


def extract_salary_neighborhoods(data_content):
    """Extract the inner entries from salaryNeighborhoodsNew = { ... };"""
    # Find the start of salaryNeighborhoodsNew
    marker = 'const salaryNeighborhoodsNew = {'
    start_idx = data_content.find(marker)
    if start_idx == -1:
        print("ERROR: Could not find 'const salaryNeighborhoodsNew = {' in data file.")
        sys.exit(1)

    # Move past the opening brace
    brace_start = start_idx + len(marker) - 1  # position of '{'

    # Use brace counting to find the matching closing brace
    depth = 1
    pos = brace_start + 1
    while pos < len(data_content) and depth > 0:
        ch = data_content[pos]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        elif ch == "'" or ch == '"':
            # Skip string literals to avoid counting braces inside strings
            quote = ch
            pos += 1
            while pos < len(data_content) and data_content[pos] != quote:
                if data_content[pos] == '\\':
                    pos += 1  # skip escaped char
                pos += 1
        pos += 1

    if depth != 0:
        print("ERROR: Unbalanced braces in salaryNeighborhoodsNew.")
        sys.exit(1)

    # Extract inner content (between the outer braces)
    inner = data_content[brace_start + 1 : pos - 1]

    # Strip leading/trailing whitespace but preserve internal structure
    inner = inner.strip()

    return inner


def find_city_neighborhoods_block(html_content):
    """Find the cityNeighborhoods = { ... } block using brace counting.
    Returns (start_of_opening_brace, end_of_closing_brace) positions.
    """
    marker = 'const cityNeighborhoods = {'
    start_idx = html_content.find(marker)
    if start_idx == -1:
        print("ERROR: Could not find 'const cityNeighborhoods = {' in index.html.")
        sys.exit(1)

    brace_start = start_idx + len(marker) - 1  # position of '{'

    # Brace counting to find closing '}'
    depth = 1
    pos = brace_start + 1
    while pos < len(html_content) and depth > 0:
        ch = html_content[pos]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        elif ch == "'" or ch == '"':
            quote = ch
            pos += 1
            while pos < len(html_content) and html_content[pos] != quote:
                if html_content[pos] == '\\':
                    pos += 1
                pos += 1
        pos += 1

    if depth != 0:
        print("ERROR: Unbalanced braces in cityNeighborhoods.")
        sys.exit(1)

    closing_brace_pos = pos - 1  # position of the closing '}'
    return brace_start, closing_brace_pos


def reindent_entries(entries_text, target_indent):
    """Re-indent extracted entries to match the target indentation level.
    The cityNeighborhoods entries use 12-space indent for city keys.
    """
    lines = entries_text.split('\n')
    result = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append('')
            continue

        # Comment lines get the base indent
        if stripped.startswith('//'):
            result.append(target_indent + stripped)
        else:
            # Determine relative indent from the source
            # Source uses 4-space base indent for city keys
            leading = len(line) - len(line.lstrip())
            if leading <= 4:
                # Top-level city key line
                result.append(target_indent + stripped)
            else:
                # Nested content (neighborhood entries inside a city)
                extra = ' ' * (leading - 4)
                result.append(target_indent + extra + stripped)

    return '\n'.join(result)


def main():
    apply_mode = '--apply' in sys.argv

    # Read source data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data_content = f.read()

    # Read target HTML
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find the cityNeighborhoods block
    brace_start, closing_brace_pos = find_city_neighborhoods_block(html_content)

    # Idempotency check: is 'Faro' already in the cityNeighborhoods block?
    block_content = html_content[brace_start:closing_brace_pos + 1]
    if IDEMPOTENCY_KEY in block_content:
        print("SKIP: 'Faro' already found in cityNeighborhoods. Data was already injected.")
        sys.exit(0)

    # Extract salary neighborhood entries
    raw_entries = extract_salary_neighborhoods(data_content)

    # Re-indent to match cityNeighborhoods style (12 spaces for city keys)
    target_indent = '            '  # 12 spaces
    reindented = reindent_entries(raw_entries, target_indent)

    # Find the content just before the closing brace to add a trailing comma
    # Look backwards from closing_brace_pos for the last non-whitespace char
    before_close = html_content[brace_start + 1:closing_brace_pos]
    before_close_stripped = before_close.rstrip()

    # Ensure trailing comma on the last existing entry
    if before_close_stripped and not before_close_stripped.endswith(','):
        # Find position of the last non-whitespace char in the original
        last_content_end = brace_start + 1 + len(before_close_stripped)
        # Insert a comma after the last content char
        html_content = (
            html_content[:last_content_end] +
            ',' +
            html_content[last_content_end:]
        )
        # Recalculate closing brace position (shifted by 1)
        closing_brace_pos += 1
        print("Added trailing comma to last existing entry.")

    # Build the new content to inject
    # We need to insert before the line that contains the closing '};'
    # The closing brace line looks like: '\n        };'
    # Find the last newline before closing_brace_pos to locate the start of that line
    last_newline = html_content.rfind('\n', 0, closing_brace_pos)

    # The injection goes between the last entry and the closing '};' line
    # injection content: blank line + comment + re-indented entries
    injection = '\n\n            // ===== NEW CITIES (injected) =====\n' + reindented

    # Insert after the last entry content but before the '\n        };' line
    new_html = (
        html_content[:last_newline] +
        injection +
        html_content[last_newline:]
    )

    # Count new cities
    city_count = len(re.findall(r"^\s+'[^']+'\s*:\s*\{", reindented, re.MULTILINE))

    # Count lines changed
    original_lines = html_content.count('\n')
    new_lines = new_html.count('\n')
    lines_added = new_lines - original_lines

    print(f"Found {city_count} new city entries to inject.")
    print(f"Lines added: {lines_added}")
    print(f"Original file size: {len(html_content):,} bytes")
    print(f"New file size: {len(new_html):,} bytes")

    if apply_mode:
        with open(TARGET_FILE, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"\nSUCCESS: Wrote updated {TARGET_FILE}")
    else:
        print(f"\nDRY RUN: No changes written. Use --apply to write changes.")
        # Show a preview of what gets injected (first 20 lines)
        preview_lines = injection.strip().split('\n')[:20]
        print("\n--- Preview of injected content (first 20 lines) ---")
        for line in preview_lines:
            print(line)
        print("...")


if __name__ == '__main__':
    main()
