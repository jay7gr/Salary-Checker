#!/usr/bin/env python3
"""Inject City Charm scores and Inheritance Tax data into retire/index.html"""

import re

HTML_PATH = '/Users/jason.i/Salary Converter Project/retire/index.html'

# ── City Charm Scores (from background task output) ──
CHARM_JS = """
// ------------------------------------------------------------------
// 8b. CITY CHARM & ARCHITECTURE SCORES (0-100)
//     Reflects historic architecture, urban aesthetics, natural beauty,
//     cultural character, and overall visual appeal
// ------------------------------------------------------------------
const retireCityCharmScore = {
    'New York': 72, 'Los Angeles': 45, 'San Francisco': 74, 'Miami': 52,
    'Chicago': 73, 'Austin': 48, 'Denver': 50, 'Seattle': 58, 'Honolulu': 62,
    'London': 82, 'Paris': 95, 'Berlin': 65, 'Amsterdam': 85, 'Barcelona': 90,
    'Madrid': 75, 'Lisbon': 88, 'Rome': 94, 'Milan': 78, 'Vienna': 93,
    'Prague': 94, 'Dublin': 70, 'Copenhagen': 76, 'Zürich': 77, 'Geneva': 75,
    'Stockholm': 74, 'Helsinki': 62, 'Munich': 80, 'Brussels': 72,
    'Luxembourg City': 68, 'Edinburgh': 88, 'Athens': 72, 'Budapest': 90,
    'Kraków': 85, 'Warsaw': 55, 'Porto': 88, 'Bucharest': 38, 'Istanbul': 86,
    'Dubai': 55, 'Abu Dhabi': 50, 'Bangkok': 60, 'Chiang Mai': 65,
    'Kuala Lumpur': 52, 'Singapore': 62, 'Ho Chi Minh City': 42, 'Hanoi': 64,
    'Jakarta': 30, 'Bali (Ubud)': 78, 'Manila': 28, 'Taipei': 50,
    'Hong Kong': 58, 'Seoul': 55, 'Tokyo': 68, 'Osaka': 65, 'Shanghai': 62,
    'Beijing': 70, 'Sydney': 72, 'Melbourne': 68, 'Brisbane': 48, 'Perth': 50,
    'Auckland': 52, 'Queenstown': 75, 'Cape Town': 72, 'Johannesburg': 35,
    'Nairobi': 32, 'Mexico City': 70, 'Cancún': 45, 'Playa del Carmen': 42,
    'Guadalajara': 65, 'San Miguel de Allende': 92, 'Medellín': 55,
    'Bogotá': 48, 'Cartagena': 85, 'Lima': 58, 'Santiago': 50,
    'Buenos Aires': 76, 'Montevideo': 58, 'São Paulo': 42, 'Rio de Janeiro': 78,
    'Panama City': 40, 'San José (Costa Rica)': 35, 'Tel Aviv': 55, 'Doha': 48,
    'Kuching': 50, 'George Town (Penang)': 75, 'Phuket': 55, 'Koh Phangan': 50,
    'Da Nang': 48, 'Tbilisi': 78, 'Marrakech': 82, 'Cairo': 68, 'Tulum': 55,
    'Puerto Vallarta': 60, 'Dubrovnik': 93, 'Split': 82, 'Florence': 96,
    'Tallinn': 84, 'Riga': 80, 'Vilnius': 75, 'Bratislava': 68, 'Ljubljana': 76,
    'Plovdiv': 72, 'Sofia': 55, 'Belgrade': 52, 'Sarajevo': 70, 'Tirana': 38,
    'Cusco': 90, 'Kyoto': 95, 'Chiang Rai': 60,
    'Faro': 65, 'Canggu': 52, 'Koh Samui': 55, 'Hoi An': 88, 'Hua Hin': 45,
    'Mazatlán': 58, 'Cádiz': 80, 'Taormina': 90, 'Kotor': 92, 'Cascais': 78,
    'Las Palmas': 65, 'Santa Cruz de Tenerife': 60, 'Paphos': 62, 'Limassol': 55,
    'Nha Trang': 48, 'Siargao': 45, 'El Nido': 55, 'Essaouira': 78,
    'Punta Cana': 40, 'Zanzibar': 65, 'Cuenca': 75, 'Da Lat': 52, 'Ubud': 78,
    'Innsbruck': 85, 'Interlaken': 82, 'San Cristóbal de las Casas': 78,
    'Oaxaca': 82, 'Antigua Guatemala': 90, 'Pokhara': 62, 'Kathmandu': 58,
    'Luang Prabang': 85, 'Colombo': 42, 'Accra': 28, 'Tunis': 60,
    'Tangier': 65, 'Amman': 50, 'Beirut': 58, 'Muscat': 55, 'Batumi': 60,
    'Yerevan': 55, 'Vientiane': 48, 'Yangon': 62, 'Kampala': 25,
    'Addis Ababa': 30, 'Dakar': 38, 'Funchal': 80, 'Palma de Mallorca': 82,
    'Mérida': 72, 'Quito': 75, 'La Paz': 55, 'Santo Domingo': 50,
    'San Juan': 72, 'Ipoh': 55, 'Dumaguete': 38, 'Jeju': 58,
    'Taichung': 45, 'Vung Tau': 40
};
"""

# ── Inheritance Tax Data (converted to JS) ──
INHERITANCE_TAX_JS = """
// ------------------------------------------------------------------
// 8c. INHERITANCE TAX DATA BY COUNTRY
//     rate: top marginal rate for direct heirs (%)
//     threshold: exemption amount in local currency
//     currency: ISO currency code
//     null = no inheritance tax
// ------------------------------------------------------------------
const retireInheritanceTax = {
    'United States': {rate: 40, threshold: 13610000, currency: 'USD', note: 'Federal estate tax above $13.61M exemption'},
    'Canada': null,
    'Mexico': null,
    'Panama': null,
    'Costa Rica': null,
    'Guatemala': null,
    'Dominican Republic': {rate: 3, threshold: 0, currency: 'DOP', note: '3% flat tax on net estate'},
    'Brazil': {rate: 8, threshold: 0, currency: 'BRL', note: 'ITCMD state tax 2-8%; varies by state'},
    'Argentina': {rate: 6.5, threshold: 0, currency: 'ARS', note: 'Buenos Aires province only; 2.2-6.5% progressive'},
    'Colombia': {rate: 10, threshold: 0, currency: 'COP', note: '10% flat on inherited amounts'},
    'Peru': null,
    'Chile': {rate: 25, threshold: 0, currency: 'CLP', note: '1-25% progressive; direct heirs get deductions'},
    'Uruguay': null,
    'Ecuador': {rate: 35, threshold: 71870, currency: 'USD', note: '0-35% progressive above ~$72k'},
    'Bolivia': {rate: 1, threshold: 0, currency: 'BOB', note: '1% transaction tax on property transfers'},
    'United Kingdom': {rate: 40, threshold: 325000, currency: 'GBP', note: 'IHT above nil-rate band; +175k for family home'},
    'France': {rate: 45, threshold: 100000, currency: 'EUR', note: '100k allowance per child; 5-45% progressive'},
    'Netherlands': {rate: 20, threshold: 25187, currency: 'EUR', note: '10-20% for children; threshold indexed'},
    'Germany': {rate: 30, threshold: 400000, currency: 'EUR', note: '400k exemption per child; 7-30% progressive'},
    'Ireland': {rate: 33, threshold: 335000, currency: 'EUR', note: 'Capital Acquisitions Tax; Group A threshold'},
    'Belgium': {rate: 30, threshold: 0, currency: 'EUR', note: '3-30% for direct heirs; varies by region'},
    'Luxembourg': {rate: 5, threshold: 0, currency: 'EUR', note: '0% for spouses; 2-5% for children'},
    'Switzerland': null,
    'Austria': null,
    'Spain': {rate: 34, threshold: 0, currency: 'EUR', note: 'Varies by region; many offer 95-99% reduction'},
    'Portugal': null,
    'Italy': {rate: 8, threshold: 1000000, currency: 'EUR', note: '4% above 1M for children/spouse; 6-8% others'},
    'Greece': {rate: 10, threshold: 150000, currency: 'EUR', note: '1-10% for children/spouse; 150k exemption'},
    'Croatia': {rate: 4, threshold: 0, currency: 'EUR', note: '4% on property; direct heirs exempt'},
    'Cyprus': null,
    'Sweden': null,
    'Denmark': {rate: 15, threshold: 321700, currency: 'DKK', note: '15% for close family; 25% additional for others'},
    'Finland': {rate: 19, threshold: 20000, currency: 'EUR', note: '7-19% progressive; 20k exemption'},
    'Norway': null,
    'Czech Republic': null,
    'Hungary': {rate: 18, threshold: 0, currency: 'HUF', note: '18% general; direct heirs fully exempt'},
    'Poland': {rate: 7, threshold: 36120, currency: 'PLN', note: '3-7% for close family; full exemption if reported in 6mo'},
    'Romania': null,
    'Estonia': null,
    'Latvia': null,
    'Turkey': {rate: 10, threshold: 1371632, currency: 'TRY', note: '1-10% progressive; exemption indexed'},
    'Slovakia': null,
    'Slovenia': {rate: 14, threshold: 0, currency: 'EUR', note: '5-14% for 2nd class; children/spouse exempt'},
    'Lithuania': {rate: 10, threshold: 150000, currency: 'EUR', note: '5% up to 150k, 10% above; family can be exempt'},
    'Bulgaria': {rate: 6.6, threshold: 0, currency: 'BGN', note: '0.4-6.6%; direct heirs exempt'},
    'Serbia': {rate: 2.5, threshold: 0, currency: 'RSD', note: '1.5-2.5% for 2nd/3rd order; 1st order exempt'},
    'Bosnia and Herzegovina': {rate: 5, threshold: 0, currency: 'BAM', note: 'Direct heirs generally exempt; 5% for others'},
    'Montenegro': {rate: 3, threshold: 0, currency: 'EUR', note: '3% for 2nd order; 1st order exempt'},
    'Albania': null,
    'Japan': {rate: 55, threshold: 30000000, currency: 'JPY', note: '10-55% progressive; 30M JPY + 6M per heir exemption'},
    'South Korea': {rate: 50, threshold: 500000000, currency: 'KRW', note: '10-50% progressive; 500M KRW exemption'},
    'Hong Kong': null,
    'Taiwan': {rate: 20, threshold: 13330000, currency: 'TWD', note: '10-20% progressive; 13.33M TWD exemption'},
    'China': null,
    'Singapore': null,
    'Thailand': {rate: 10, threshold: 100000000, currency: 'THB', note: '5% for 100M-300M; 10% above 300M'},
    'Malaysia': null,
    'Vietnam': {rate: 10, threshold: 10000000, currency: 'VND', note: '10% income tax on inherited assets above 10M VND'},
    'Philippines': {rate: 6, threshold: 5000000, currency: 'PHP', note: '6% flat above 5M PHP standard deduction'},
    'Indonesia': null,
    'Cambodia': null,
    'Laos': null,
    'Myanmar': null,
    'India': null,
    'Nepal': null,
    'Sri Lanka': null,
    'Australia': null,
    'New Zealand': null,
    'UAE': null,
    'Qatar': null,
    'Saudi Arabia': null,
    'Israel': null,
    'Jordan': null,
    'Lebanon': {rate: 12, threshold: 0, currency: 'LBP', note: '3-12% for direct heirs; varies by kinship'},
    'Oman': null,
    'Georgia': null,
    'Armenia': null,
    'South Africa': {rate: 25, threshold: 3500000, currency: 'ZAR', note: '20% on first 30M above 3.5M; 25% above 30M'},
    'Kenya': null,
    'Nigeria': null,
    'Egypt': null,
    'Morocco': null,
    'Ghana': null,
    'Tunisia': {rate: 25, threshold: 0, currency: 'TND', note: '2.5% for direct heirs; up to 25% for unrelated'},
    'Tanzania': null,
    'Uganda': null,
    'Ethiopia': null,
    'Senegal': {rate: 10, threshold: 0, currency: 'XOF', note: '1-10% for direct heirs'}
};
"""

def main():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already injected
    if 'const retireCityCharmScore' in content:
        print('retireCityCharmScore already exists, skipping charm injection')
    else:
        # Insert after retireCultureScore closing }; (before country tax data)
        marker = '// ------------------------------------------------------------------\n// 8. COUNTRY TAX DATA'
        if marker in content:
            content = content.replace(marker, CHARM_JS.strip() + '\n\n' + marker)
            print('✅ Injected retireCityCharmScore (182 cities)')
        else:
            print('❌ Could not find marker for charm score injection')

    if 'retireInheritanceTax' in content:
        print('retireInheritanceTax already exists, skipping inheritance tax injection')
    else:
        # Insert after charm scores, before country tax data
        marker2 = '// ------------------------------------------------------------------\n// 8. COUNTRY TAX DATA'
        if marker2 in content:
            content = content.replace(marker2, INHERITANCE_TAX_JS.strip() + '\n\n' + marker2)
            print('✅ Injected retireInheritanceTax (89 countries)')
        else:
            print('❌ Could not find marker for inheritance tax injection')

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Done!')

if __name__ == '__main__':
    main()
