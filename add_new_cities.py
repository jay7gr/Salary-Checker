#!/usr/bin/env python3
"""
add_new_cities.py — Inject 69 new cities into coliData, cityToCurrency, and cityToCountry
in both index.html and retire/index.html.

Part 1: Script framework + coliData, cityToCurrency, cityToCountry data.
Subsequent parts will add more data objects (exchangeRates, taxBrackets, etc.).

Usage:
    python add_new_cities.py          # dry-run (prints what it would do)
    python add_new_cities.py --apply  # actually modify the files
"""

import re
import sys
import os

from add_new_cities_part2 import NEW_SAFETY, NEW_HEALTHCARE, NEW_CLIMATE, NEW_INFRASTRUCTURE
from add_new_cities_part3 import NEW_ENGLISH, NEW_EXPAT, NEW_CULTURE, NEW_CITY_TO_COUNTRY_FULL, NEW_COORDS, NEW_LIFESTYLE
from add_new_cities_part4 import NEW_COUNTRY_DATA, NEW_COUNTRY_ISO, NEW_COUNTRY_FLAGS, NEW_CITY_REGIONS, NEW_ATTRACTIVENESS, NEW_VISA_PROGRAMS, NEW_EXCHANGE_RATES

# ─── Configuration ──────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = [
    os.path.join(BASE_DIR, 'index.html'),
    os.path.join(BASE_DIR, 'retire', 'index.html'),
]

# ─── New City Data ──────────────────────────────────────────────────────────────

# Cost of Living Index (New York = 100)
NEW_COLI = {
    # Smaller Beach/Coastal
    'Faro': 35,
    'Canggu': 28,
    'Koh Samui': 32,
    'Da Nang': 25,
    'Hoi An': 23,
    'Hua Hin': 30,
    'Puerto Vallarta': 30,
    'Tulum': 38,
    'Mazatlán': 26,
    'Cádiz': 42,
    'Taormina': 52,
    'Kotor': 35,
    'Cascais': 45,
    'Las Palmas': 40,
    'Santa Cruz de Tenerife': 38,
    'Paphos': 38,
    'Limassol': 45,
    'Nha Trang': 22,
    'Siargao': 22,
    'El Nido': 25,
    'Essaouira': 22,
    'Punta Cana': 35,
    'Zanzibar': 25,
    # Smaller Mountain/Nature
    'Cuenca': 28,
    'Da Lat': 20,
    'Ubud': 26,
    'Innsbruck': 62,
    'Interlaken': 82,
    'San Cristóbal de las Casas': 20,
    'Oaxaca': 24,
    'Antigua Guatemala': 28,
    'Pokhara': 18,
    'Luang Prabang': 22,
    # Major Cities (underrepresented regions)
    'Colombo': 28,
    'Accra': 32,
    'Tunis': 25,
    'Tangier': 28,
    'Amman': 38,
    'Beirut': 35,
    'Muscat': 45,
    'Batumi': 25,
    'Yerevan': 28,
    'Vientiane': 25,
    'Yangon': 22,
    'Kampala': 28,
    'Addis Ababa': 28,
    'Dakar': 35,
    'Kathmandu': 22,
    # More European
    'Bratislava': 42,
    'Ljubljana': 45,
    'Vilnius': 38,
    'Plovdiv': 28,
    'Sofia': 32,
    'Belgrade': 30,
    'Sarajevo': 28,
    'Tirana': 28,
    'Funchal': 35,
    'Palma de Mallorca': 48,
    # More Latin American
    'Mérida': 25,
    'Quito': 30,
    'La Paz': 22,
    'Santo Domingo': 32,
    'San Juan': 55,
    # More Asia-Pacific
    'Chiang Rai': 25,
    'Ipoh': 24,
    'Dumaguete': 20,
    'Jeju': 48,
    'Taichung': 38,
    'Vung Tau': 24,
}

# City -> Currency code
NEW_CURRENCY = {
    'Faro': 'EUR',
    'Canggu': 'IDR',
    'Koh Samui': 'THB',
    'Da Nang': 'VND',
    'Hoi An': 'VND',
    'Hua Hin': 'THB',
    'Puerto Vallarta': 'MXN',
    'Tulum': 'MXN',
    'Mazatlán': 'MXN',
    'Cádiz': 'EUR',
    'Taormina': 'EUR',
    'Kotor': 'EUR',
    'Cascais': 'EUR',
    'Las Palmas': 'EUR',
    'Santa Cruz de Tenerife': 'EUR',
    'Paphos': 'EUR',
    'Limassol': 'EUR',
    'Nha Trang': 'VND',
    'Siargao': 'PHP',
    'El Nido': 'PHP',
    'Essaouira': 'MAD',
    'Punta Cana': 'DOP',
    'Zanzibar': 'TZS',
    'Cuenca': 'USD',
    'Da Lat': 'VND',
    'Ubud': 'IDR',
    'Innsbruck': 'EUR',
    'Interlaken': 'CHF',
    'San Cristóbal de las Casas': 'MXN',
    'Oaxaca': 'MXN',
    'Antigua Guatemala': 'GTQ',
    'Pokhara': 'NPR',
    'Luang Prabang': 'LAK',
    'Colombo': 'LKR',
    'Accra': 'GHS',
    'Tunis': 'TND',
    'Tangier': 'MAD',
    'Amman': 'JOD',
    'Beirut': 'LBP',
    'Muscat': 'OMR',
    'Batumi': 'GEL',
    'Yerevan': 'AMD',
    'Vientiane': 'LAK',
    'Yangon': 'MMK',
    'Kampala': 'UGX',
    'Addis Ababa': 'ETB',
    'Dakar': 'XOF',
    'Kathmandu': 'NPR',
    'Bratislava': 'EUR',
    'Ljubljana': 'EUR',
    'Vilnius': 'EUR',
    'Plovdiv': 'BGN',
    'Sofia': 'BGN',
    'Belgrade': 'RSD',
    'Sarajevo': 'BAM',
    'Tirana': 'ALL',
    'Funchal': 'EUR',
    'Palma de Mallorca': 'EUR',
    'Mérida': 'MXN',
    'Quito': 'USD',
    'La Paz': 'BOB',
    'Santo Domingo': 'DOP',
    'San Juan': 'USD',
    'Chiang Rai': 'THB',
    'Ipoh': 'MYR',
    'Dumaguete': 'PHP',
    'Jeju': 'KRW',
    'Taichung': 'TWD',
    'Vung Tau': 'VND',
}

# City -> 2-letter ISO country code
NEW_COUNTRY = {
    'Faro': 'PT',
    'Canggu': 'ID',
    'Koh Samui': 'TH',
    'Da Nang': 'VN',
    'Hoi An': 'VN',
    'Hua Hin': 'TH',
    'Puerto Vallarta': 'MX',
    'Tulum': 'MX',
    'Mazatlán': 'MX',
    'Cádiz': 'ES',
    'Taormina': 'IT',
    'Kotor': 'ME',
    'Cascais': 'PT',
    'Las Palmas': 'ES',
    'Santa Cruz de Tenerife': 'ES',
    'Paphos': 'CY',
    'Limassol': 'CY',
    'Nha Trang': 'VN',
    'Siargao': 'PH',
    'El Nido': 'PH',
    'Essaouira': 'MA',
    'Punta Cana': 'DO',
    'Zanzibar': 'TZ',
    'Cuenca': 'EC',
    'Da Lat': 'VN',
    'Ubud': 'ID',
    'Innsbruck': 'AT',
    'Interlaken': 'CH',
    'San Cristóbal de las Casas': 'MX',
    'Oaxaca': 'MX',
    'Antigua Guatemala': 'GT',
    'Pokhara': 'NP',
    'Luang Prabang': 'LA',
    'Colombo': 'LK',
    'Accra': 'GH',
    'Tunis': 'TN',
    'Tangier': 'MA',
    'Amman': 'JO',
    'Beirut': 'LB',
    'Muscat': 'OM',
    'Batumi': 'GE',
    'Yerevan': 'AM',
    'Vientiane': 'LA',
    'Yangon': 'MM',
    'Kampala': 'UG',
    'Addis Ababa': 'ET',
    'Dakar': 'SN',
    'Kathmandu': 'NP',
    'Bratislava': 'SK',
    'Ljubljana': 'SI',
    'Vilnius': 'LT',
    'Plovdiv': 'BG',
    'Sofia': 'BG',
    'Belgrade': 'RS',
    'Sarajevo': 'BA',
    'Tirana': 'AL',
    'Funchal': 'PT',
    'Palma de Mallorca': 'ES',
    'Mérida': 'MX',
    'Quito': 'EC',
    'La Paz': 'BO',
    'Santo Domingo': 'DO',
    'San Juan': 'US',
    'Chiang Rai': 'TH',
    'Ipoh': 'MY',
    'Dumaguete': 'PH',
    'Jeju': 'KR',
    'Taichung': 'TW',
    'Vung Tau': 'VN',
}

# Monthly rent for 1-bedroom apartment (USD)
NEW_RENT_1BR = {
    'Faro': 650, 'Canggu': 350, 'Koh Samui': 400, 'Da Nang': 300, 'Hoi An': 250,
    'Hua Hin': 350, 'Puerto Vallarta': 500, 'Tulum': 650, 'Mazatlán': 350,
    'Cádiz': 600, 'Taormina': 750, 'Kotor': 450, 'Cascais': 800,
    'Las Palmas': 650, 'Santa Cruz de Tenerife': 600, 'Paphos': 550, 'Limassol': 700,
    'Nha Trang': 250, 'Siargao': 300, 'El Nido': 350, 'Essaouira': 250,
    'Punta Cana': 500, 'Zanzibar': 350,
    'Cuenca': 350, 'Da Lat': 200, 'Ubud': 300, 'Innsbruck': 900, 'Interlaken': 1400,
    'San Cristóbal de las Casas': 250, 'Oaxaca': 350, 'Antigua Guatemala': 400,
    'Pokhara': 150, 'Luang Prabang': 250,
    'Colombo': 350, 'Accra': 450, 'Tunis': 250, 'Tangier': 300, 'Amman': 450,
    'Beirut': 400, 'Muscat': 700, 'Batumi': 300, 'Yerevan': 350, 'Vientiane': 250,
    'Yangon': 300, 'Kampala': 350, 'Addis Ababa': 400, 'Dakar': 450, 'Kathmandu': 200,
    'Bratislava': 650, 'Ljubljana': 700, 'Vilnius': 550, 'Plovdiv': 300,
    'Sofia': 450, 'Belgrade': 400, 'Sarajevo': 350, 'Tirana': 350,
    'Funchal': 550, 'Palma de Mallorca': 850,
    'Mérida': 350, 'Quito': 400, 'La Paz': 250, 'Santo Domingo': 450,
    'San Juan': 900,
    'Chiang Rai': 250, 'Ipoh': 250, 'Dumaguete': 200, 'Jeju': 600,
    'Taichung': 450, 'Vung Tau': 250,
}

# Monthly living costs breakdown (USD)
NEW_LIVING_COSTS = {
    'Faro': {'groceries': 250, 'utilities': 100, 'transport': 40, 'healthcare': 60, 'childcare': 400},
    'Canggu': {'groceries': 200, 'utilities': 60, 'transport': 15, 'healthcare': 35, 'childcare': 180},
    'Koh Samui': {'groceries': 220, 'utilities': 80, 'transport': 30, 'healthcare': 45, 'childcare': 350},
    'Da Nang': {'groceries': 150, 'utilities': 50, 'transport': 15, 'healthcare': 30, 'childcare': 200},
    'Hoi An': {'groceries': 130, 'utilities': 45, 'transport': 10, 'healthcare': 25, 'childcare': 150},
    'Hua Hin': {'groceries': 200, 'utilities': 70, 'transport': 25, 'healthcare': 40, 'childcare': 300},
    'Puerto Vallarta': {'groceries': 220, 'utilities': 60, 'transport': 25, 'healthcare': 55, 'childcare': 350},
    'Tulum': {'groceries': 280, 'utilities': 70, 'transport': 30, 'healthcare': 60, 'childcare': 400},
    'Mazatlán': {'groceries': 180, 'utilities': 50, 'transport': 20, 'healthcare': 40, 'childcare': 250},
    'Cádiz': {'groceries': 270, 'utilities': 110, 'transport': 45, 'healthcare': 70, 'childcare': 450},
    'Taormina': {'groceries': 320, 'utilities': 130, 'transport': 45, 'healthcare': 80, 'childcare': 500},
    'Kotor': {'groceries': 220, 'utilities': 80, 'transport': 30, 'healthcare': 45, 'childcare': 300},
    'Cascais': {'groceries': 280, 'utilities': 110, 'transport': 45, 'healthcare': 65, 'childcare': 450},
    'Las Palmas': {'groceries': 260, 'utilities': 90, 'transport': 40, 'healthcare': 60, 'childcare': 400},
    'Santa Cruz de Tenerife': {'groceries': 250, 'utilities': 85, 'transport': 35, 'healthcare': 60, 'childcare': 380},
    'Paphos': {'groceries': 250, 'utilities': 100, 'transport': 35, 'healthcare': 55, 'childcare': 350},
    'Limassol': {'groceries': 280, 'utilities': 110, 'transport': 40, 'healthcare': 65, 'childcare': 400},
    'Nha Trang': {'groceries': 120, 'utilities': 40, 'transport': 10, 'healthcare': 25, 'childcare': 130},
    'Siargao': {'groceries': 150, 'utilities': 50, 'transport': 10, 'healthcare': 20, 'childcare': 120},
    'El Nido': {'groceries': 170, 'utilities': 55, 'transport': 12, 'healthcare': 22, 'childcare': 130},
    'Essaouira': {'groceries': 130, 'utilities': 40, 'transport': 10, 'healthcare': 25, 'childcare': 150},
    'Punta Cana': {'groceries': 250, 'utilities': 80, 'transport': 30, 'healthcare': 50, 'childcare': 300},
    'Zanzibar': {'groceries': 150, 'utilities': 45, 'transport': 15, 'healthcare': 30, 'childcare': 150},
    'Cuenca': {'groceries': 180, 'utilities': 50, 'transport': 15, 'healthcare': 40, 'childcare': 250},
    'Da Lat': {'groceries': 110, 'utilities': 35, 'transport': 8, 'healthcare': 20, 'childcare': 100},
    'Ubud': {'groceries': 180, 'utilities': 55, 'transport': 12, 'healthcare': 30, 'childcare': 160},
    'Innsbruck': {'groceries': 350, 'utilities': 160, 'transport': 55, 'healthcare': 90, 'childcare': 600},
    'Interlaken': {'groceries': 450, 'utilities': 200, 'transport': 80, 'healthcare': 120, 'childcare': 800},
    'San Cristóbal de las Casas': {'groceries': 120, 'utilities': 35, 'transport': 10, 'healthcare': 30, 'childcare': 150},
    'Oaxaca': {'groceries': 150, 'utilities': 40, 'transport': 12, 'healthcare': 35, 'childcare': 200},
    'Antigua Guatemala': {'groceries': 170, 'utilities': 45, 'transport': 15, 'healthcare': 35, 'childcare': 200},
    'Pokhara': {'groceries': 80, 'utilities': 25, 'transport': 8, 'healthcare': 15, 'childcare': 80},
    'Luang Prabang': {'groceries': 120, 'utilities': 40, 'transport': 10, 'healthcare': 20, 'childcare': 100},
    'Colombo': {'groceries': 160, 'utilities': 45, 'transport': 15, 'healthcare': 35, 'childcare': 200},
    'Accra': {'groceries': 200, 'utilities': 70, 'transport': 25, 'healthcare': 50, 'childcare': 300},
    'Tunis': {'groceries': 140, 'utilities': 40, 'transport': 12, 'healthcare': 30, 'childcare': 200},
    'Tangier': {'groceries': 160, 'utilities': 50, 'transport': 15, 'healthcare': 35, 'childcare': 200},
    'Amman': {'groceries': 240, 'utilities': 80, 'transport': 30, 'healthcare': 55, 'childcare': 350},
    'Beirut': {'groceries': 220, 'utilities': 60, 'transport': 25, 'healthcare': 50, 'childcare': 350},
    'Muscat': {'groceries': 280, 'utilities': 100, 'transport': 40, 'healthcare': 70, 'childcare': 500},
    'Batumi': {'groceries': 150, 'utilities': 45, 'transport': 12, 'healthcare': 30, 'childcare': 200},
    'Yerevan': {'groceries': 170, 'utilities': 50, 'transport': 12, 'healthcare': 35, 'childcare': 200},
    'Vientiane': {'groceries': 130, 'utilities': 40, 'transport': 10, 'healthcare': 25, 'childcare': 120},
    'Yangon': {'groceries': 130, 'utilities': 35, 'transport': 10, 'healthcare': 25, 'childcare': 150},
    'Kampala': {'groceries': 150, 'utilities': 45, 'transport': 15, 'healthcare': 35, 'childcare': 180},
    'Addis Ababa': {'groceries': 160, 'utilities': 40, 'transport': 12, 'healthcare': 35, 'childcare': 200},
    'Dakar': {'groceries': 220, 'utilities': 60, 'transport': 20, 'healthcare': 50, 'childcare': 300},
    'Kathmandu': {'groceries': 100, 'utilities': 30, 'transport': 8, 'healthcare': 20, 'childcare': 100},
    'Bratislava': {'groceries': 270, 'utilities': 130, 'transport': 40, 'healthcare': 65, 'childcare': 450},
    'Ljubljana': {'groceries': 280, 'utilities': 130, 'transport': 45, 'healthcare': 70, 'childcare': 500},
    'Vilnius': {'groceries': 240, 'utilities': 110, 'transport': 35, 'healthcare': 55, 'childcare': 400},
    'Plovdiv': {'groceries': 170, 'utilities': 70, 'transport': 20, 'healthcare': 35, 'childcare': 250},
    'Sofia': {'groceries': 200, 'utilities': 80, 'transport': 30, 'healthcare': 45, 'childcare': 300},
    'Belgrade': {'groceries': 190, 'utilities': 80, 'transport': 25, 'healthcare': 40, 'childcare': 280},
    'Sarajevo': {'groceries': 170, 'utilities': 70, 'transport': 20, 'healthcare': 35, 'childcare': 250},
    'Tirana': {'groceries': 170, 'utilities': 65, 'transport': 18, 'healthcare': 35, 'childcare': 250},
    'Funchal': {'groceries': 230, 'utilities': 90, 'transport': 35, 'healthcare': 55, 'childcare': 350},
    'Palma de Mallorca': {'groceries': 300, 'utilities': 120, 'transport': 45, 'healthcare': 75, 'childcare': 500},
    'Mérida': {'groceries': 160, 'utilities': 45, 'transport': 12, 'healthcare': 35, 'childcare': 220},
    'Quito': {'groceries': 190, 'utilities': 50, 'transport': 15, 'healthcare': 45, 'childcare': 280},
    'La Paz': {'groceries': 120, 'utilities': 35, 'transport': 10, 'healthcare': 25, 'childcare': 150},
    'Santo Domingo': {'groceries': 200, 'utilities': 65, 'transport': 25, 'healthcare': 45, 'childcare': 280},
    'San Juan': {'groceries': 320, 'utilities': 140, 'transport': 45, 'healthcare': 85, 'childcare': 550},
    'Chiang Rai': {'groceries': 150, 'utilities': 50, 'transport': 12, 'healthcare': 30, 'childcare': 200},
    'Ipoh': {'groceries': 140, 'utilities': 45, 'transport': 12, 'healthcare': 25, 'childcare': 180},
    'Dumaguete': {'groceries': 120, 'utilities': 40, 'transport': 8, 'healthcare': 20, 'childcare': 100},
    'Jeju': {'groceries': 300, 'utilities': 120, 'transport': 40, 'healthcare': 65, 'childcare': 500},
    'Taichung': {'groceries': 230, 'utilities': 80, 'transport': 25, 'healthcare': 45, 'childcare': 350},
    'Vung Tau': {'groceries': 130, 'utilities': 40, 'transport': 10, 'healthcare': 25, 'childcare': 140},
}

# ─── Injection Logic ────────────────────────────────────────────────────────────

def inject_before_closing(content, obj_name, new_entries_str):
    """
    Find 'const OBJ_NAME = {' block and inject new_entries_str before its
    closing '};'.

    Uses brace-counting to find the correct closing brace, handles nested
    objects, and ensures the last existing entry gets a trailing comma if
    it doesn't already have one.
    """
    pattern = rf'(const\s+{re.escape(obj_name)}\s*=\s*\{{)'
    match = re.search(pattern, content)
    if not match:
        print(f"  WARNING: Could not find 'const {obj_name}' — skipping")
        return content

    start = match.end() - 1  # position of the opening {
    depth = 0
    i = start
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                close_pos = i  # position of the closing }
                break
        i += 1
    else:
        print(f"  WARNING: Could not find closing brace for {obj_name}")
        return content

    # Find the newline before the closing } to know the indent of the closing line
    nl_before_close = content.rfind('\n', start, close_pos)
    if nl_before_close != -1:
        closing_indent = content[nl_before_close + 1:close_pos]
    else:
        closing_indent = ''

    # Everything between opening { and the closing } line
    # We want the content up to the last real code line (not trailing whitespace)
    inner = content[start + 1:nl_before_close] if nl_before_close != -1 else content[start + 1:close_pos]
    inner_stripped = inner.rstrip()
    # Position in content of the last non-whitespace char of the inner block
    last_code_pos = start + 1 + len(inner_stripped)

    # Ensure the last non-whitespace character has a trailing comma
    needs_comma = inner_stripped and not inner_stripped.endswith(',')
    comma_str = ',' if needs_comma else ''

    # Build the replacement: everything from last code char to closing }
    # Original: <last_entry_char><whitespace>\n<indent>}
    # New:      <last_entry_char>,\n<new_entries>\n<indent>}
    replacement = comma_str + '\n' + new_entries_str + '\n' + closing_indent
    content = content[:last_code_pos] + replacement + content[close_pos:]

    print(f"  Injected {len(new_entries_str.splitlines())} lines into {obj_name}")
    return content


def inject_before_array_closing(content, arr_name, new_entries_str):
    """For const arrName = [...], inject before closing ];"""
    pattern = rf'(const\s+{re.escape(arr_name)}\s*=\s*\[)'
    match = re.search(pattern, content)
    if not match:
        print(f"  WARNING: Could not find 'const {arr_name}' — skipping")
        return content

    start = match.end() - 1
    depth = 0
    i = start
    while i < len(content):
        if content[i] == '[':
            depth += 1
        elif content[i] == ']':
            depth -= 1
            if depth == 0:
                close_pos = i
                break
        i += 1
    else:
        print(f"  WARNING: Could not find closing bracket for {arr_name}")
        return content

    nl_before_close = content.rfind('\n', start, close_pos)
    if nl_before_close != -1:
        closing_indent = content[nl_before_close + 1:close_pos]
    else:
        closing_indent = ''

    inner = content[start + 1:nl_before_close] if nl_before_close != -1 else content[start + 1:close_pos]
    inner_stripped = inner.rstrip()
    last_code_pos = start + 1 + len(inner_stripped)

    needs_comma = inner_stripped and not inner_stripped.endswith(',')
    comma_str = ',' if needs_comma else ''

    replacement = comma_str + '\n' + new_entries_str + '\n' + closing_indent
    content = content[:last_code_pos] + replacement + content[close_pos:]

    print(f"  Injected {len(new_entries_str.splitlines())} lines into {arr_name}")
    return content


def format_coli_entries(data, indent=12):
    """Format coliData entries: 'City Name': 42.0"""
    prefix = ' ' * indent
    lines = []
    items = list(data.items())
    for i, (city, value) in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''
        # Use integer if whole number, else one decimal
        if isinstance(value, float) and not value.is_integer():
            lines.append(f"{prefix}'{city}': {value}{comma}")
        else:
            lines.append(f"{prefix}'{city}': {int(value)}{comma}")
    return '\n'.join(lines)


def format_string_entries(data, indent=12):
    """Format string-value entries: 'City Name': 'VALUE'"""
    prefix = ' ' * indent
    lines = []
    items = list(data.items())
    for i, (city, value) in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''
        lines.append(f"{prefix}'{city}': '{value}'{comma}")
    return '\n'.join(lines)


def format_multiline_string_entries(data, indent=12, per_line=4):
    """
    Format string-value entries packed multiple per line (matching the
    existing style of cityToCurrency and cityToCountry).
    """
    prefix = ' ' * indent
    lines = []
    items = list(data.items())
    line_parts = []
    for i, (city, value) in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''
        line_parts.append(f"'{city}': '{value}'{comma}")
        if len(line_parts) == per_line or i == len(items) - 1:
            lines.append(prefix + ' '.join(line_parts))
            line_parts = []
    return '\n'.join(lines)


def format_living_costs_entries(data, indent=12):
    """Format cityLivingCosts entries with nested objects"""
    prefix = ' ' * indent
    lines = []
    items = list(data.items())
    for i, (city, costs) in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''
        lines.append(f"{prefix}'{city}': {{groceries: {costs['groceries']}, utilities: {costs['utilities']}, transport: {costs['transport']}, healthcare: {costs['healthcare']}, childcare: {costs['childcare']}}}{comma}")
    return '\n'.join(lines)


def format_coords_entries(data, indent=12):
    """Format retireCityCoords entries: 'City': [lat, lng]"""
    prefix = ' ' * indent
    lines = []
    items = list(data.items())
    for i, (city, coords) in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''
        lines.append(f"{prefix}'{city}': [{coords[0]}, {coords[1]}]{comma}")
    return '\n'.join(lines)


def format_lifestyle_entries(data, indent=12):
    """Format cityLifestyleMap entries: 'City': ['tag1', 'tag2']"""
    prefix = ' ' * indent
    lines = []
    items = list(data.items())
    for i, (city, tags) in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''
        tags_str = ', '.join(f"'{t}'" for t in tags)
        lines.append(f"{prefix}'{city}': [{tags_str}]{comma}")
    return '\n'.join(lines)


def format_country_data_entries(data, indent=2):
    """Format retireCountryData entries with multiline nested objects matching existing style"""
    prefix = ' ' * indent
    inner_prefix = ' ' * (indent + 2)
    lines = []
    items = list(data.items())
    for i, (country, info) in enumerate(items):
        comma = ',' if i < len(items) - 1 else ''
        cgt = info['capitalGainsTax']
        dt = info['dividendTax']
        wt = 'null' if info['wealthTax'] is None else str(info['wealthTax'])
        hi = info['healthInsurance60Plus']
        cont = info['continent']
        region = info['region']

        lines.append(f"{prefix}'{country}': {{")
        lines.append(f"{inner_prefix}capitalGainsTax: {cgt},")
        lines.append(f"{inner_prefix}dividendTax: {dt},")
        lines.append(f"{inner_prefix}wealthTax: {wt},")
        lines.append(f"{inner_prefix}healthInsurance60Plus: {hi},")
        lines.append(f"{inner_prefix}continent: '{cont}',")
        lines.append(f"{inner_prefix}region: '{region}'")
        lines.append(f"{prefix}}}{comma}")
    return '\n'.join(lines)


def format_visa_entries(data, indent=8):
    """Format visaPrograms array entries"""
    prefix = ' ' * indent
    lines = []
    for i, prog in enumerate(data):
        comma = ',' if i < len(data) - 1 else ''
        lines.append(f"{prefix}{{country: '{prog['country']}', name: '{prog['name']}', type: '{prog['type']}', minIncome: {prog['minIncome']}, minWealth: {prog['minWealth']}}}{comma}")
    return '\n'.join(lines)


def inject_into_region_sets(content, city_regions_dict):
    """
    Append new cities into the existing regionSets arrays.
    For each region, find the array line like 'southeast_asia': [...]
    and append the new cities before the closing ].
    """
    # Group cities by region
    region_to_cities = {}
    for city, region in city_regions_dict.items():
        region_to_cities.setdefault(region, []).append(city)

    for region, cities in region_to_cities.items():
        # Match the region line within regionSets, e.g. 'southeast_asia': ['Singapore',...,'Phnom Penh']
        # The line ends with ],
        pattern = rf"('{re.escape(region)}':\s*\[)(.*?)(\])"
        match = re.search(pattern, content)
        if not match:
            print(f"  WARNING: Could not find region '{region}' in regionSets — skipping")
            continue

        existing_array = match.group(2).rstrip()
        # Build the new city entries
        new_city_strs = ','.join(f"'{c}'" for c in cities)
        # Ensure trailing comma on existing content if needed
        if existing_array and not existing_array.rstrip().endswith(','):
            new_array = existing_array + ',' + new_city_strs
        else:
            new_array = existing_array + new_city_strs

        replacement = match.group(1) + new_array + match.group(3)
        content = content[:match.start()] + replacement + content[match.end():]
        print(f"  Added {len(cities)} cities to regionSets['{region}']")

    return content


def build_const_block(var_name, data, formatter):
    """
    Build a complete 'const varName = { ... };' block from data using the
    given formatter function.
    """
    formatted = formatter(data)
    return f"const {var_name} = {{\n{formatted}\n}};\n"


# ─── Injection Specifications ───────────────────────────────────────────────────
# Each tuple: (object_name, data_dict, formatter_function)

# Injections for BOTH files (salary converter + retirement)
COMMON_INJECTIONS = [
    ('coliData',       NEW_COLI,     format_coli_entries),
    ('cityToCurrency', NEW_CURRENCY, format_multiline_string_entries),
    ('cityToCountry',  NEW_COUNTRY,  format_multiline_string_entries),
]

# Injections for RETIREMENT tool ONLY
RETIRE_INJECTIONS = [
    ('cityRent1BR',              NEW_RENT_1BR,              format_coli_entries),
    ('cityLivingCosts',          NEW_LIVING_COSTS,           format_living_costs_entries),
    ('retireSafetyIndex',        NEW_SAFETY,                format_coli_entries),
    ('retireHealthcareIndex',    NEW_HEALTHCARE,            format_coli_entries),
    ('retireClimateScore',       NEW_CLIMATE,               format_coli_entries),
    ('retireInfrastructureScore', NEW_INFRASTRUCTURE,       format_coli_entries),
    ('retireEnglishScore',       NEW_ENGLISH,               format_coli_entries),
    ('retireExpatCommunity',     NEW_EXPAT,                 format_string_entries),
    ('retireCultureScore',       NEW_CULTURE,               format_coli_entries),
    ('retireCountryData',        NEW_COUNTRY_DATA,          format_country_data_entries),
    ('retireCityToCountry',      NEW_CITY_TO_COUNTRY_FULL,  format_string_entries),
    ('retireCityCoords',         NEW_COORDS,                format_coords_entries),
    ('countryNameToISO',         NEW_COUNTRY_ISO,           format_multiline_string_entries),
    ('countryFlags',             NEW_COUNTRY_FLAGS,         format_multiline_string_entries),
    ('exchangeRates',            NEW_EXCHANGE_RATES,        format_coli_entries),
]

# ─── Main ────────────────────────────────────────────────────────────────────────

def main():
    dry_run = '--apply' not in sys.argv

    if dry_run:
        print("DRY RUN — pass --apply to write changes.\n")
    else:
        print("APPLYING changes.\n")

    print(f"Total new cities: {len(NEW_COLI)}\n")

    for filepath in FILES:
        print(f"Processing {filepath}")
        if not os.path.exists(filepath):
            print(f"  ERROR: File not found — skipping")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        is_retire = 'retire' in filepath

        injections = COMMON_INJECTIONS + (RETIRE_INJECTIONS if is_retire else [])

        for obj_name, data, formatter in injections:
            sample_key = list(data.keys())[0] if isinstance(data, dict) else None
            if sample_key:
                # Check if the sample key exists within THIS specific data block, not the whole file
                obj_match = re.search(rf'(const\s+{re.escape(obj_name)}\s*=\s*\{{)', original)
                if obj_match:
                    obj_start = obj_match.end() - 1
                    depth_check, j = 0, obj_start
                    while j < len(original):
                        if original[j] == '{': depth_check += 1
                        elif original[j] == '}':
                            depth_check -= 1
                            if depth_check == 0: break
                        j += 1
                    obj_block = original[obj_start:j+1]
                    if f"'{sample_key}'" in obj_block:
                        print(f"  SKIP {obj_name}: '{sample_key}' already in this block")
                        continue

            formatted = formatter(data) if not isinstance(data, list) else formatter(data)
            content = inject_before_closing(content, obj_name, formatted)

        # Handle visa programs (array, not object)
        if is_retire and NEW_VISA_PROGRAMS:
            visa_formatted = format_visa_entries(NEW_VISA_PROGRAMS)
            content = inject_before_array_closing(content, 'visaPrograms', visa_formatted)

        # Create new const declarations for cityLifestyleMap and cityAttractivenessScore
        if is_retire:
            # Check if already present
            if 'const cityLifestyleMap' not in original:
                lifestyle_block = build_const_block('cityLifestyleMap', NEW_LIFESTYLE,
                                                    lambda d: format_lifestyle_entries(d, indent=4))
                attractiveness_block = build_const_block('cityAttractivenessScore', NEW_ATTRACTIVENESS,
                                                         lambda d: format_coli_entries(d, indent=4))
                # Insert before 'const cityRegionMap = {};'
                marker = 'const cityRegionMap = {};'
                marker_pos = content.find(marker)
                if marker_pos != -1:
                    insert_str = lifestyle_block + '\n' + attractiveness_block + '\n'
                    content = content[:marker_pos] + insert_str + content[marker_pos:]
                    print(f"  Created const cityLifestyleMap ({len(NEW_LIFESTYLE)} entries)")
                    print(f"  Created const cityAttractivenessScore ({len(NEW_ATTRACTIVENESS)} entries)")
                else:
                    print("  WARNING: Could not find 'const cityRegionMap = {};' — skipping lifestyle/attractiveness blocks")
            else:
                print("  SKIP cityLifestyleMap/cityAttractivenessScore: already present")

            # Inject cities into regionSets arrays
            # Check against the original file's regionSets block (not 'content'
            # which already has the city names injected into other objects)
            first_new_city = list(NEW_CITY_REGIONS.keys())[0]
            region_sets_match = re.search(r'const regionSets\s*=\s*\{.*?\};', original, re.DOTALL)
            region_sets_text = region_sets_match.group(0) if region_sets_match else ''
            if f"'{first_new_city}'" not in region_sets_text:
                content = inject_into_region_sets(content, NEW_CITY_REGIONS)
            else:
                print("  SKIP regionSets injection: cities already present")

        if content == original:
            print("  No changes needed.\n")
            continue

        if dry_run:
            print("  (dry run — file not modified)\n")
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  File updated.\n")

    print("Done.")


if __name__ == '__main__':
    main()
