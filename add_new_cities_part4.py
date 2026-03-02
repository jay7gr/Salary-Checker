# New country data for retireCountryData (27 new countries)
# Format: {capitalGainsTax: decimal, dividendTax: percentage, wealthTax: null or dict,
#          healthInsurance60Plus: monthly USD, continent: str, inheritanceTax: null or dict, region: str}
NEW_COUNTRY_DATA = {
    'Ecuador': {'capitalGainsTax': 0, 'dividendTax': 0, 'wealthTax': None, 'healthInsurance60Plus': 80, 'continent': 'South America', 'inheritanceTax': {'rate': 35, 'spouseExempt': True, 'notes': 'Progressive rates up to 35% on inheritances over $866K'}, 'region': 'South America'},
    'Guatemala': {'capitalGainsTax': 0.10, 'dividendTax': 5, 'wealthTax': None, 'healthInsurance60Plus': 60, 'continent': 'Central America', 'inheritanceTax': None, 'region': 'Central America'},
    'Nepal': {'capitalGainsTax': 0.10, 'dividendTax': 5, 'wealthTax': None, 'healthInsurance60Plus': 40, 'continent': 'Asia', 'inheritanceTax': None, 'region': 'South Asia'},
    'Sri Lanka': {'capitalGainsTax': 0.10, 'dividendTax': 14, 'wealthTax': None, 'healthInsurance60Plus': 50, 'continent': 'Asia', 'inheritanceTax': None, 'region': 'South Asia'},
    'Ghana': {'capitalGainsTax': 0.15, 'dividendTax': 8, 'wealthTax': None, 'healthInsurance60Plus': 60, 'continent': 'Africa', 'inheritanceTax': None, 'region': 'West Africa'},
    'Tunisia': {'capitalGainsTax': 0.10, 'dividendTax': 10, 'wealthTax': None, 'healthInsurance60Plus': 50, 'continent': 'Africa', 'inheritanceTax': {'rate': 25, 'spouseExempt': True, 'notes': 'Progressive rates, direct heirs pay lower rates'}, 'region': 'North Africa'},
    'Jordan': {'capitalGainsTax': 0, 'dividendTax': 0, 'wealthTax': None, 'healthInsurance60Plus': 80, 'continent': 'Middle East', 'inheritanceTax': None, 'region': 'Middle East'},
    'Lebanon': {'capitalGainsTax': 0.10, 'dividendTax': 10, 'wealthTax': None, 'healthInsurance60Plus': 120, 'continent': 'Middle East', 'inheritanceTax': {'rate': 12, 'spouseExempt': False, 'notes': 'Progressive rates 3-12% depending on relationship'}, 'region': 'Middle East'},
    'Oman': {'capitalGainsTax': 0, 'dividendTax': 0, 'wealthTax': None, 'healthInsurance60Plus': 130, 'continent': 'Middle East', 'inheritanceTax': None, 'region': 'Middle East'},
    'Armenia': {'capitalGainsTax': 0.10, 'dividendTax': 5, 'wealthTax': None, 'healthInsurance60Plus': 50, 'continent': 'Asia', 'inheritanceTax': None, 'region': 'Caucasus'},
    'Laos': {'capitalGainsTax': 0.10, 'dividendTax': 10, 'wealthTax': None, 'healthInsurance60Plus': 40, 'continent': 'Asia', 'inheritanceTax': None, 'region': 'Southeast Asia'},
    'Myanmar': {'capitalGainsTax': 0.10, 'dividendTax': 0, 'wealthTax': None, 'healthInsurance60Plus': 35, 'continent': 'Asia', 'inheritanceTax': None, 'region': 'Southeast Asia'},
    'Tanzania': {'capitalGainsTax': 0.10, 'dividendTax': 5, 'wealthTax': None, 'healthInsurance60Plus': 40, 'continent': 'Africa', 'inheritanceTax': None, 'region': 'East Africa'},
    'Uganda': {'capitalGainsTax': 0.30, 'dividendTax': 15, 'wealthTax': None, 'healthInsurance60Plus': 45, 'continent': 'Africa', 'inheritanceTax': None, 'region': 'East Africa'},
    'Ethiopia': {'capitalGainsTax': 0.15, 'dividendTax': 10, 'wealthTax': None, 'healthInsurance60Plus': 35, 'continent': 'Africa', 'inheritanceTax': None, 'region': 'East Africa'},
    'Senegal': {'capitalGainsTax': 0.10, 'dividendTax': 10, 'wealthTax': None, 'healthInsurance60Plus': 50, 'continent': 'Africa', 'inheritanceTax': None, 'region': 'West Africa'},
    'Slovakia': {'capitalGainsTax': 0.19, 'dividendTax': 7, 'wealthTax': None, 'healthInsurance60Plus': 120, 'continent': 'Europe', 'inheritanceTax': None, 'region': 'Central Europe'},
    'Slovenia': {'capitalGainsTax': 0.25, 'dividendTax': 25, 'wealthTax': None, 'healthInsurance60Plus': 130, 'continent': 'Europe', 'inheritanceTax': {'rate': 39, 'spouseExempt': True, 'notes': 'Spouse and direct descendants exempt, others 5-39%'}, 'region': 'Central Europe'},
    'Lithuania': {'capitalGainsTax': 0.15, 'dividendTax': 15, 'wealthTax': None, 'healthInsurance60Plus': 100, 'continent': 'Europe', 'inheritanceTax': {'rate': 10, 'spouseExempt': True, 'notes': 'Close relatives exempt, others 5-10%'}, 'region': 'Baltic States'},
    'Bulgaria': {'capitalGainsTax': 0.10, 'dividendTax': 5, 'wealthTax': None, 'healthInsurance60Plus': 60, 'continent': 'Europe', 'inheritanceTax': {'rate': 6.6, 'spouseExempt': True, 'notes': 'Spouse and direct line exempt, others 0.4-6.6%'}, 'region': 'Eastern Europe'},
    'Serbia': {'capitalGainsTax': 0.15, 'dividendTax': 15, 'wealthTax': None, 'healthInsurance60Plus': 70, 'continent': 'Europe', 'inheritanceTax': {'rate': 2.5, 'spouseExempt': True, 'notes': 'First-order heirs exempt, others 1.5-2.5%'}, 'region': 'Eastern Europe'},
    'Bosnia and Herzegovina': {'capitalGainsTax': 0.10, 'dividendTax': 10, 'wealthTax': None, 'healthInsurance60Plus': 60, 'continent': 'Europe', 'inheritanceTax': None, 'region': 'Eastern Europe'},
    'Montenegro': {'capitalGainsTax': 0.09, 'dividendTax': 9, 'wealthTax': None, 'healthInsurance60Plus': 80, 'continent': 'Europe', 'inheritanceTax': {'rate': 3, 'spouseExempt': True, 'notes': 'Close relatives exempt, others 3%'}, 'region': 'Eastern Europe'},
    'Albania': {'capitalGainsTax': 0.15, 'dividendTax': 8, 'wealthTax': None, 'healthInsurance60Plus': 50, 'continent': 'Europe', 'inheritanceTax': None, 'region': 'Eastern Europe'},
    'Cyprus': {'capitalGainsTax': 0.20, 'dividendTax': 0, 'wealthTax': None, 'healthInsurance60Plus': 100, 'continent': 'Europe', 'inheritanceTax': None, 'region': 'Mediterranean'},
    'Dominican Republic': {'capitalGainsTax': 0.27, 'dividendTax': 10, 'wealthTax': None, 'healthInsurance60Plus': 70, 'continent': 'Central America', 'inheritanceTax': {'rate': 3, 'spouseExempt': False, 'notes': 'Flat 3% on inherited assets'}, 'region': 'Caribbean'},
    'Bolivia': {'capitalGainsTax': 0.125, 'dividendTax': 12.5, 'wealthTax': None, 'healthInsurance60Plus': 40, 'continent': 'South America', 'inheritanceTax': {'rate': 20, 'spouseExempt': False, 'notes': 'Progressive rates 1-20% on estates'}, 'region': 'South America'},
}

# Country name to ISO code additions
NEW_COUNTRY_ISO = {
    'Ecuador': 'EC', 'Guatemala': 'GT', 'Nepal': 'NP', 'Sri Lanka': 'LK',
    'Ghana': 'GH', 'Tunisia': 'TN', 'Jordan': 'JO', 'Lebanon': 'LB',
    'Oman': 'OM', 'Armenia': 'AM', 'Laos': 'LA', 'Myanmar': 'MM',
    'Tanzania': 'TZ', 'Uganda': 'UG', 'Ethiopia': 'ET', 'Senegal': 'SN',
    'Slovakia': 'SK', 'Slovenia': 'SI', 'Lithuania': 'LT', 'Bulgaria': 'BG',
    'Serbia': 'RS', 'Bosnia and Herzegovina': 'BA', 'Montenegro': 'ME',
    'Albania': 'AL', 'Cyprus': 'CY', 'Dominican Republic': 'DO', 'Bolivia': 'BO',
}

# Country flags (ISO to emoji)
NEW_COUNTRY_FLAGS = {
    'EC': '\U0001f1ea\U0001f1e8', 'GT': '\U0001f1ec\U0001f1f9', 'NP': '\U0001f1f3\U0001f1f5', 'LK': '\U0001f1f1\U0001f1f0',
    'GH': '\U0001f1ec\U0001f1ed', 'TN': '\U0001f1f9\U0001f1f3', 'JO': '\U0001f1ef\U0001f1f4', 'LB': '\U0001f1f1\U0001f1e7',
    'OM': '\U0001f1f4\U0001f1f2', 'AM': '\U0001f1e6\U0001f1f2', 'LA': '\U0001f1f1\U0001f1e6', 'MM': '\U0001f1f2\U0001f1f2',
    'TZ': '\U0001f1f9\U0001f1ff', 'UG': '\U0001f1fa\U0001f1ec', 'ET': '\U0001f1ea\U0001f1f9', 'SN': '\U0001f1f8\U0001f1f3',
    'SK': '\U0001f1f8\U0001f1f0', 'SI': '\U0001f1f8\U0001f1ee', 'LT': '\U0001f1f1\U0001f1f9', 'BG': '\U0001f1e7\U0001f1ec',
    'RS': '\U0001f1f7\U0001f1f8', 'BA': '\U0001f1e7\U0001f1e6', 'ME': '\U0001f1f2\U0001f1ea',
    'AL': '\U0001f1e6\U0001f1f1', 'CY': '\U0001f1e8\U0001f1fe', 'DO': '\U0001f1e9\U0001f1f4', 'BO': '\U0001f1e7\U0001f1f4',
}

# City region map assignments (for filtering)
# Existing regions: north_america, central_america, south_america, europe,
#   southeast_asia, east_asia, south_asia, oceania, middle_east, africa
NEW_CITY_REGIONS = {
    # Beach/Coastal
    'Faro': 'europe', 'Canggu': 'southeast_asia', 'Koh Samui': 'southeast_asia',
    'Da Nang': 'southeast_asia', 'Hoi An': 'southeast_asia', 'Hua Hin': 'southeast_asia',
    'Puerto Vallarta': 'central_america', 'Tulum': 'central_america', 'Mazatl\u00e1n': 'central_america',
    'C\u00e1diz': 'europe', 'Taormina': 'europe', 'Kotor': 'europe',
    'Cascais': 'europe', 'Las Palmas': 'europe', 'Santa Cruz de Tenerife': 'europe',
    'Paphos': 'europe', 'Limassol': 'europe', 'Nha Trang': 'southeast_asia',
    'Siargao': 'southeast_asia', 'El Nido': 'southeast_asia',
    'Essaouira': 'africa', 'Punta Cana': 'central_america', 'Zanzibar': 'africa',
    # Mountain
    'Cuenca': 'south_america', 'Da Lat': 'southeast_asia', 'Ubud': 'southeast_asia',
    'Innsbruck': 'europe', 'Interlaken': 'europe',
    'San Crist\u00f3bal de las Casas': 'central_america', 'Oaxaca': 'central_america',
    'Antigua Guatemala': 'central_america', 'Pokhara': 'south_asia',
    'Luang Prabang': 'southeast_asia',
    # Major cities
    'Colombo': 'south_asia', 'Accra': 'africa', 'Tunis': 'africa',
    'Tangier': 'africa', 'Amman': 'middle_east', 'Beirut': 'middle_east',
    'Muscat': 'middle_east', 'Batumi': 'europe', 'Yerevan': 'europe',
    'Vientiane': 'southeast_asia', 'Yangon': 'southeast_asia',
    'Kampala': 'africa', 'Addis Ababa': 'africa', 'Dakar': 'africa',
    'Kathmandu': 'south_asia',
    # European
    'Bratislava': 'europe', 'Ljubljana': 'europe', 'Vilnius': 'europe',
    'Plovdiv': 'europe', 'Sofia': 'europe', 'Belgrade': 'europe',
    'Sarajevo': 'europe', 'Tirana': 'europe', 'Funchal': 'europe',
    'Palma de Mallorca': 'europe',
    # Latin American
    'M\u00e9rida': 'central_america', 'Quito': 'south_america', 'La Paz': 'south_america',
    'Santo Domingo': 'central_america', 'San Juan': 'north_america',
    # Asia-Pacific
    'Chiang Rai': 'southeast_asia', 'Ipoh': 'southeast_asia',
    'Dumaguete': 'southeast_asia', 'Jeju': 'east_asia',
    'Taichung': 'east_asia', 'Vung Tau': 'southeast_asia',
}

# Attractiveness/Tourism score (0-100)
NEW_ATTRACTIVENESS = {
    'Faro': 68, 'Canggu': 72, 'Koh Samui': 75, 'Da Nang': 65, 'Hoi An': 82,
    'Hua Hin': 55, 'Puerto Vallarta': 70, 'Tulum': 78, 'Mazatl\u00e1n': 55,
    'C\u00e1diz': 72, 'Taormina': 88, 'Kotor': 82, 'Cascais': 75, 'Las Palmas': 68,
    'Santa Cruz de Tenerife': 62, 'Paphos': 70, 'Limassol': 58, 'Nha Trang': 62,
    'Siargao': 72, 'El Nido': 85, 'Essaouira': 72, 'Punta Cana': 68, 'Zanzibar': 78,
    'Cuenca': 62, 'Da Lat': 58, 'Ubud': 80, 'Innsbruck': 82, 'Interlaken': 88,
    'San Crist\u00f3bal de las Casas': 68, 'Oaxaca': 75, 'Antigua Guatemala': 78,
    'Pokhara': 82, 'Luang Prabang': 85,
    'Colombo': 52, 'Accra': 38, 'Tunis': 55, 'Tangier': 62, 'Amman': 65,
    'Beirut': 58, 'Muscat': 62, 'Batumi': 60, 'Yerevan': 55, 'Vientiane': 45,
    'Yangon': 58, 'Kampala': 35, 'Addis Ababa': 42, 'Dakar': 48, 'Kathmandu': 68,
    'Bratislava': 62, 'Ljubljana': 72, 'Vilnius': 65, 'Plovdiv': 58,
    'Sofia': 52, 'Belgrade': 55, 'Sarajevo': 62, 'Tirana': 48,
    'Funchal': 78, 'Palma de Mallorca': 72,
    'M\u00e9rida': 62, 'Quito': 65, 'La Paz': 60, 'Santo Domingo': 55,
    'San Juan': 72,
    'Chiang Rai': 62, 'Ipoh': 48, 'Dumaguete': 45, 'Jeju': 72,
    'Taichung': 52, 'Vung Tau': 48,
}

# Visa programs for new countries (only countries with notable programs)
NEW_VISA_PROGRAMS = [
    {'country': 'EC', 'name': 'Ecuador Retirement Visa', 'type': 'retirement', 'minIncome': 1375, 'minWealth': 0},
    {'country': 'GT', 'name': 'Guatemala Pensionado Visa', 'type': 'retirement', 'minIncome': 1000, 'minWealth': 0},
    {'country': 'NP', 'name': 'Nepal Tourist Visa Extension', 'type': 'passive_income', 'minIncome': 0, 'minWealth': 0},
    {'country': 'LK', 'name': 'Sri Lanka My Dream Home Visa', 'type': 'retirement', 'minIncome': 1500, 'minWealth': 15000},
    {'country': 'AM', 'name': 'Armenia Residence Permit', 'type': 'passive_income', 'minIncome': 0, 'minWealth': 0},
    {'country': 'ME', 'name': 'Montenegro Temporary Residence', 'type': 'passive_income', 'minIncome': 0, 'minWealth': 0},
    {'country': 'CY', 'name': 'Cyprus Category F Permit', 'type': 'retirement', 'minIncome': 0, 'minWealth': 30000},
    {'country': 'DO', 'name': 'Dominican Republic Pensionado Visa', 'type': 'retirement', 'minIncome': 1500, 'minWealth': 0},
    {'country': 'BO', 'name': 'Bolivia Specific Purpose Visa', 'type': 'retirement', 'minIncome': 1000, 'minWealth': 0},
    {'country': 'BG', 'name': 'Bulgaria Type D Long-Stay Visa', 'type': 'passive_income', 'minIncome': 0, 'minWealth': 0},
    {'country': 'RS', 'name': 'Serbia Temporary Residence', 'type': 'passive_income', 'minIncome': 0, 'minWealth': 0},
    {'country': 'AL', 'name': 'Albania Residence Permit', 'type': 'passive_income', 'minIncome': 0, 'minWealth': 0},
    {'country': 'SI', 'name': 'Slovenia Residence Permit', 'type': 'passive_income', 'minIncome': 1000, 'minWealth': 0},
]

# New exchange rates for new currencies
NEW_EXCHANGE_RATES = {
    'GTQ': 10.28, 'NPR': 176.5, 'LKR': 410, 'GHS': 16.8,
    'TND': 4.12, 'JOD': 0.94, 'LBP': 119000, 'OMR': 0.512,
    'AMD': 513, 'LAK': 27800, 'MMK': 2795, 'TZS': 3350,
    'UGX': 4885, 'ETB': 76.5, 'XOF': 805, 'BGN': 2.41,
    'RSD': 144, 'BAM': 2.41, 'ALL': 125, 'DOP': 78.5, 'BOB': 9.2,
}
