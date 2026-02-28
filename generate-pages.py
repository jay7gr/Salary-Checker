#!/usr/bin/env python3
"""
Generate static city pages and comparison pages for salary-converter.com
Uses the same data embedded in index.html to create SEO-friendly individual pages.
"""

import os
import json
import re
from datetime import date

# ============================================================
# DATA (mirrors index.html exactly)
# ============================================================

coliData = {
    'New York': 100, 'San Francisco': 97.6, 'Los Angeles': 76.3, 'Chicago': 73.2,
    'Miami': 80.1, 'Austin': 64.8, 'Seattle': 79.5, 'Denver': 65.7, 'Boston': 82.4,
    'Washington DC': 79.8, 'Houston': 60.2,
    'Charlotte': 59.8, 'Las Vegas': 58.2, 'Tampa': 64.5, 'Raleigh': 58.6,
    'Dallas': 62.5, 'Atlanta': 63.2, 'Philadelphia': 68.8, 'Phoenix': 58.9,
    'San Diego': 77.5, 'Nashville': 62.8, 'Minneapolis': 61.4, 'Portland': 67.2,
    'Toronto': 62.3, 'Vancouver': 65.4,
    'Montreal': 52.1, 'Mexico City': 32.5, 'Cancún': 35.8, 'Panama City': 42.3,
    'London': 87.5, 'Paris': 46.9, 'Amsterdam': 82.6, 'Berlin': 51.2, 'Munich': 61.5,
    'Dublin': 72.8, 'Brussels': 50.3, 'Luxembourg City': 68.4, 'Zurich': 122.4,
    'Geneva': 118.6, 'Edinburgh': 62.1, 'Nice': 52.7,
    'Madrid': 38.0, 'Barcelona': 42.1, 'Valencia': 33.5, 'Málaga': 31.2,
    'Lisbon': 34.7, 'Porto': 30.1, 'Rome': 49.3, 'Milan': 57.8, 'Athens': 30.6, 'Split': 31.8,
    'Stockholm': 64.3, 'Copenhagen': 85.7, 'Helsinki': 58.2, 'Oslo': 78.5, 'Vienna': 48.2,
    'Prague': 30.6, 'Budapest': 26.1, 'Warsaw': 28.4, 'Krakow': 23.8, 'Bucharest': 22.5,
    'Tallinn': 28.9, 'Riga': 25.3, 'Istanbul': 23.1,
    'Tokyo': 77.3, 'Osaka': 62.8, 'Fukuoka': 51.4, 'Seoul': 68.9, 'Hong Kong': 73.6,
    'Taipei': 44.8, 'Shanghai': 46.2, 'Beijing': 43.5, 'Shenzhen': 41.9, 'Guangzhou': 38.7,
    'Singapore': 87.7, 'Bangkok': 37.2, 'Chiang Mai': 22.6, 'Phuket': 30.5,
    'Kuala Lumpur': 32.8, 'Ho Chi Minh City': 26.4, 'Hanoi': 24.1, 'Manila': 26.8,
    'Jakarta': 24.5, 'Bali (Denpasar)': 25.3, 'Phnom Penh': 24.8,
    'Mumbai': 22.3, 'Bangalore': 20.8, 'Delhi': 19.5, 'Chennai': 18.9,
    'Sydney': 74.5, 'Melbourne': 68.2, 'Perth': 63.5, 'Auckland': 60.8,
    'Dubai': 72.4, 'Abu Dhabi': 67.8, 'Doha': 69.5, 'Riyadh': 42.6, 'Tel Aviv': 81.3,
    'Cape Town': 28.4, 'Nairobi': 24.7, 'Lagos': 27.3, 'Cairo': 16.8,
    'Marrakech': 19.2, 'Casablanca': 22.1,
    'São Paulo': 41.8, 'Buenos Aires': 25.6, 'Bogotá': 22.9, 'Lima': 25.8,
    'Santiago': 33.2, 'Medellín': 20.4, 'Montevideo': 32.5,
    'San José (CR)': 31.2, 'Playa del Carmen': 30.8
}

exchangeRates = {
    'GBP': 1.0, 'USD': 1.328, 'EUR': 1.126, 'SGD': 1.73, 'JPY': 205.72,
    'AED': 4.811, 'THB': 41.157, 'AUD': 1.887, 'CAD': 1.798, 'CHF': 1.076,
    'CNY': 8.94, 'HKD': 10.4, 'INR': 110.5, 'MYR': 5.4, 'NZD': 2.14,
    'SEK': 12.09, 'NOK': 13.34, 'DKK': 8.43, 'CZK': 30.6, 'HUF': 477,
    'PLN': 5.2, 'TRY': 42.5, 'BRL': 6.7, 'MXN': 22.5, 'ZAR': 24.2,
    'KRW': 1686, 'TWD': 42.0, 'IDR': 20500, 'VND': 33200, 'PHP': 74.5,
    'ILS': 4.78, 'EGP': 64.8, 'KES': 171.5, 'NGN': 2100, 'MAD': 12.9,
    'ARS': 1480, 'COP': 5520, 'PEN': 4.92, 'CLP': 1245, 'UYU': 55.8,
    'CRC': 672, 'QAR': 4.84, 'SAR': 4.98, 'PAB': 1.328, 'RON': 5.62
}

cityToCurrency = {
    'New York': 'USD', 'San Francisco': 'USD', 'Los Angeles': 'USD',
    'Chicago': 'USD', 'Miami': 'USD', 'Austin': 'USD', 'Seattle': 'USD',
    'Denver': 'USD', 'Boston': 'USD', 'Washington DC': 'USD', 'Houston': 'USD',
    'Charlotte': 'USD', 'Las Vegas': 'USD', 'Tampa': 'USD', 'Raleigh': 'USD',
    'Dallas': 'USD', 'Atlanta': 'USD', 'Philadelphia': 'USD', 'Phoenix': 'USD',
    'San Diego': 'USD', 'Nashville': 'USD', 'Minneapolis': 'USD', 'Portland': 'USD',
    'Toronto': 'CAD', 'Vancouver': 'CAD', 'Montreal': 'CAD',
    'Mexico City': 'MXN', 'Cancún': 'MXN', 'Panama City': 'USD',
    'London': 'GBP', 'Edinburgh': 'GBP',
    'Paris': 'EUR', 'Amsterdam': 'EUR', 'Berlin': 'EUR', 'Munich': 'EUR',
    'Dublin': 'EUR', 'Brussels': 'EUR', 'Luxembourg City': 'EUR', 'Nice': 'EUR',
    'Zurich': 'CHF', 'Geneva': 'CHF',
    'Madrid': 'EUR', 'Barcelona': 'EUR', 'Valencia': 'EUR', 'Málaga': 'EUR',
    'Lisbon': 'EUR', 'Porto': 'EUR', 'Rome': 'EUR', 'Milan': 'EUR',
    'Athens': 'EUR', 'Split': 'EUR',
    'Stockholm': 'SEK', 'Copenhagen': 'DKK', 'Helsinki': 'EUR',
    'Oslo': 'NOK', 'Vienna': 'EUR',
    'Prague': 'CZK', 'Budapest': 'HUF', 'Warsaw': 'PLN', 'Krakow': 'PLN',
    'Bucharest': 'RON', 'Tallinn': 'EUR', 'Riga': 'EUR', 'Istanbul': 'TRY',
    'Tokyo': 'JPY', 'Osaka': 'JPY', 'Fukuoka': 'JPY',
    'Seoul': 'KRW', 'Hong Kong': 'HKD', 'Taipei': 'TWD',
    'Shanghai': 'CNY', 'Beijing': 'CNY', 'Shenzhen': 'CNY', 'Guangzhou': 'CNY',
    'Singapore': 'SGD',
    'Bangkok': 'THB', 'Chiang Mai': 'THB', 'Phuket': 'THB',
    'Kuala Lumpur': 'MYR',
    'Ho Chi Minh City': 'VND', 'Hanoi': 'VND',
    'Manila': 'PHP', 'Jakarta': 'IDR', 'Bali (Denpasar)': 'IDR',
    'Phnom Penh': 'USD',
    'Mumbai': 'INR', 'Bangalore': 'INR', 'Delhi': 'INR', 'Chennai': 'INR',
    'Sydney': 'AUD', 'Melbourne': 'AUD', 'Perth': 'AUD', 'Auckland': 'NZD',
    'Dubai': 'AED', 'Abu Dhabi': 'AED', 'Doha': 'QAR',
    'Riyadh': 'SAR', 'Tel Aviv': 'ILS',
    'Cape Town': 'ZAR', 'Nairobi': 'KES', 'Lagos': 'NGN',
    'Cairo': 'EGP', 'Marrakech': 'MAD', 'Casablanca': 'MAD',
    'São Paulo': 'BRL', 'Buenos Aires': 'ARS',
    'Bogotá': 'COP', 'Medellín': 'COP',
    'Lima': 'PEN', 'Santiago': 'CLP', 'Montevideo': 'UYU',
    'San José (CR)': 'CRC', 'Playa del Carmen': 'MXN'
}

cityNeighborhoods = {
            # ===== NORTH AMERICA =====
            'New York': {
                'Manhattan (Midtown)': 1.25, 'Manhattan (Upper East Side)': 1.30, 'Manhattan (Lower East Side)': 1.10,
                'Brooklyn (Williamsburg)': 1.05, 'Brooklyn (Park Slope)': 1.08, 'Brooklyn (Bushwick)': 0.88,
                'Queens (Astoria)': 0.90, 'Queens (Long Island City)': 0.95, 'Harlem': 0.82,
                'The Bronx': 0.72, 'Staten Island': 0.75, 'SoHo / Tribeca': 1.35,
                'Chelsea': 1.18, 'West Village': 1.28, 'Greenwich Village': 1.25, 'Upper West Side': 1.22, 'Financial District': 1.2, 'DUMBO': 1.15, 'Fort Greene': 1.02, 'Prospect Heights': 1.05, 'Crown Heights': 0.85, 'Red Hook': 0.88, 'Greenpoint': 1.0, 'Jackson Heights': 0.78, 'Flushing': 0.8, 'Bay Ridge': 0.82, 'Forest Hills': 0.88, 'Hoboken (NJ)': 1.08, 'Murray Hill': 1.12, "Hell's Kitchen": 1.1
            },
            'San Francisco': {
                'Financial District': 1.20, 'SoMa': 1.15, 'Mission District': 1.05,
                'Castro': 1.08, 'Sunset District': 0.92, 'Richmond District': 0.90,
                'Nob Hill': 1.18, 'Pacific Heights': 1.25, 'Tenderloin': 0.78,
                'Oakland (Downtown)': 0.80, 'Oakland (Rockridge)': 0.88, 'Berkeley': 0.90,
                'Marina District': 1.22, 'Hayes Valley': 1.15, 'Potrero Hill': 1.1, 'Dogpatch': 1.05, 'Russian Hill': 1.2, 'North Beach': 1.12, 'Haight-Ashbury': 1.08, 'Excelsior': 0.82, 'Bayview': 0.75, 'Daly City': 0.78, 'San Mateo': 0.92, 'Palo Alto': 1.28
            },
            'Los Angeles': {
                'Santa Monica': 1.25, 'Beverly Hills': 1.40, 'Hollywood': 1.10,
                'Downtown LA': 1.05, 'Silver Lake': 1.08, 'Venice': 1.20,
                'Koreatown': 0.85, 'Echo Park': 0.90, 'Pasadena': 0.92,
                'Long Beach': 0.80, 'Culver City': 1.02, 'Burbank': 0.88,
                'West Hollywood': 1.22, 'Westwood': 1.18, 'Glendale': 0.9, 'Studio City': 1.05, 'Sherman Oaks': 1.02, 'Encino': 1.08, 'Bel Air': 1.45, 'Mar Vista': 0.95, 'Los Feliz': 1.12, 'Highland Park': 0.88, 'Eagle Rock': 0.85, 'Inglewood': 0.72, 'Torrance': 0.82, 'Malibu': 1.42, 'Manhattan Beach': 1.3, 'Playa del Rey': 1.1, 'Arts District': 1.05, 'Atwater Village': 0.95
            },
            'Chicago': {
                'The Loop': 1.20, 'Lincoln Park': 1.15, 'Wicker Park': 1.08,
                'River North': 1.22, 'Gold Coast': 1.25, 'Lakeview': 1.05,
                'Logan Square': 0.92, 'Pilsen': 0.82, 'Hyde Park': 0.85,
                'Bridgeport': 0.78, 'Evanston': 0.95, 'Oak Park': 0.90,
                'Bucktown': 1.1, 'Uptown': 0.88, 'Edgewater': 0.9, 'West Loop': 1.18, 'South Loop': 1.08, 'Humboldt Park': 0.82, 'Ravenswood': 0.95, 'Irving Park': 0.8, 'Avondale': 0.85, 'Old Town': 1.15, 'Ukrainian Village': 1.05, 'Chinatown': 0.78, 'Beverly': 0.82, 'Portage Park': 0.75, 'Rogers Park': 0.78
            },
            'Miami': {
                'South Beach': 1.30, 'Brickell': 1.25, 'Wynwood': 1.10,
                'Coconut Grove': 1.15, 'Coral Gables': 1.20, 'Downtown Miami': 1.08,
                'Little Havana': 0.78, 'North Miami': 0.82, 'Hialeah': 0.72,
                'Miami Beach': 1.22, 'Doral': 0.88, 'Kendall': 0.80,
                'Edgewater': 1.1, 'Midtown': 1.12, 'Design District': 1.18, 'Key Biscayne': 1.35, 'Aventura': 1.08, 'Sunny Isles': 1.15, 'Pinecrest': 1.12, 'Westchester': 0.78, 'Surfside': 1.18, 'Bal Harbour': 1.32, 'Homestead': 0.68, 'Overtown': 0.7
            },
            'Austin': {
                'Downtown': 1.25, 'South Congress (SoCo)': 1.18, 'East Austin': 1.05,
                'West Lake Hills': 1.30, 'Hyde Park': 1.08, 'Mueller': 1.02,
                'North Loop': 0.95, 'Round Rock': 0.80, 'Cedar Park': 0.78,
                'Pflugerville': 0.75, 'South Lamar': 1.10,
                'Zilker': 1.22, 'Barton Hills': 1.18, 'Clarksville': 1.25, 'Bouldin Creek': 1.15, 'Travis Heights': 1.12, 'Crestview': 0.95, 'Holly': 1.08, 'Allandale': 0.98, 'Windsor Park': 0.82, 'Riverside': 0.88, 'Govalle': 0.78, 'St. Elmo': 0.85
            },
            'Seattle': {
                'Capitol Hill': 1.12, 'Downtown': 1.18, 'Queen Anne': 1.10,
                'Ballard': 1.05, 'Fremont': 1.08, 'University District': 0.88,
                'Beacon Hill': 0.85, 'West Seattle': 0.92, 'Columbia City': 0.90,
                'Bellevue': 1.15, 'Redmond': 1.05, 'Kirkland': 1.02,
                'South Lake Union': 1.15, 'Georgetown': 0.82, 'Madrona': 1.1, 'Wallingford': 1.05, 'Ravenna': 0.98, 'Magnolia': 1.08, 'Central District': 0.92, 'Rainier Valley': 0.78, 'Green Lake': 1.05, 'Northgate': 0.82, 'Pioneer Square': 0.95, 'Mercer Island': 1.25
            },
            'Denver': {
                'LoDo (Lower Downtown)': 1.22, 'Cherry Creek': 1.28, 'Capitol Hill': 1.10,
                'RiNo (River North)': 1.15, 'Highlands': 1.12, 'Washington Park': 1.08,
                'Baker': 1.02, 'Park Hill': 0.90, 'Montbello': 0.72,
                'Aurora': 0.78, 'Lakewood': 0.85, 'Englewood': 0.82,
                'Five Points': 0.95, 'Sloan Lake': 1.08, 'Congress Park': 1.05, 'Platt Park': 1.02, 'Hilltop': 1.15, 'City Park': 1.0, 'Globeville': 0.72, 'Stapleton (Central Park)': 0.92, 'Green Valley Ranch': 0.75, 'Federal Heights': 0.7, 'Wheat Ridge': 0.8, 'Arvada': 0.82
            },
            'Boston': {
                'Back Bay': 1.30, 'Beacon Hill': 1.28, 'South End': 1.18,
                'North End': 1.12, 'Seaport': 1.25, 'Cambridge (Harvard Sq)': 1.15,
                'Cambridge (Kendall Sq)': 1.20, 'Somerville': 0.95, 'Jamaica Plain': 0.90,
                'Dorchester': 0.78, 'Allston/Brighton': 0.85, 'Brookline': 1.10,
                'Fenway-Kenmore': 1.12, 'Charlestown': 1.05, 'South Boston (Southie)': 1.08, 'East Boston': 0.82, 'Roxbury': 0.72, 'Medford': 0.85, 'Newton': 1.1, 'Watertown': 0.88, 'Waltham': 0.82, 'Malden': 0.78, 'Quincy': 0.8, 'Revere': 0.75
            },
            'Washington DC': {
                'Georgetown': 1.30, 'Dupont Circle': 1.20, 'Capitol Hill': 1.15,
                'Adams Morgan': 1.05, 'Logan Circle': 1.18, 'Navy Yard': 1.10,
                'Columbia Heights': 0.92, 'Foggy Bottom': 1.22, 'U Street': 1.08,
                'Anacostia': 0.72, 'Arlington (VA)': 1.05, 'Bethesda (MD)': 1.12,
                'Shaw': 1.08, 'Woodley Park': 1.15, 'Cleveland Park': 1.12, 'Tenleytown': 1.05, 'Petworth': 0.9, 'Brookland': 0.88, 'Chevy Chase (DC)': 1.18, 'Takoma Park (MD)': 0.85, 'Silver Spring (MD)': 0.88, 'Pentagon City (VA)': 1.02, 'Rosslyn (VA)': 1.08, 'Alexandria (VA)': 1.05
            },
            'Houston': {
                'River Oaks': 1.35, 'The Heights': 1.15, 'Montrose': 1.12,
                'Downtown': 1.18, 'Midtown': 1.10, 'Museum District': 1.08,
                'Upper Kirby': 1.05, 'EaDo': 0.95, 'Katy': 0.82,
                'Sugar Land': 0.85, 'Spring': 0.78, 'Pearland': 0.80,
                'West University Place': 1.22, 'Bellaire': 1.08, 'Memorial': 1.18, 'Tanglewood': 1.25, 'Rice Village': 1.1, 'Galleria': 1.15, 'Clear Lake': 0.85, 'Cypress': 0.78, 'Kingwood': 0.82, 'The Woodlands': 0.92, 'Pasadena (TX)': 0.72, 'Friendswood': 0.82
            },
            'Charlotte': {
                'South End': 1.22, 'Uptown': 1.25, 'NoDa': 1.12, 'Plaza Midwood': 1.08,
                'Dilworth': 1.15, 'Myers Park': 1.35, 'Ballantyne': 0.92, 'SouthPark': 1.18,
                'Huntersville': 0.78, 'Cornelius': 0.80, 'Davidson': 0.82, 'Matthews': 0.75,
                'Mint Hill': 0.72, 'Indian Trail': 0.70, 'Mooresville': 0.75, 'Concord': 0.72,
                'Pineville': 0.73, 'Fort Mill (SC)': 0.76, 'Rock Hill (SC)': 0.68,
                'Lake Norman': 0.88, 'Elizabeth': 1.12, 'Cherry': 1.10, 'Sedgefield': 1.02,
                'Montford': 0.95, 'Cotswold': 1.05, 'Eastover': 1.30, 'Steele Creek': 0.78,
                'University City': 0.80, 'Highland Creek': 0.76, 'Wesley Heights': 1.08
            },
            'Las Vegas': {
                'The Strip Area': 1.25, 'Downtown / Fremont': 0.92, 'Summerlin': 1.28,
                'Henderson': 1.10, 'Green Valley': 1.08, 'Anthem (Henderson)': 1.15,
                'Centennial Hills': 1.02, 'North Las Vegas': 0.72, 'Spring Valley': 0.88,
                'Enterprise': 0.90, 'Southern Highlands': 1.12, 'Mountains Edge': 0.95,
                'Aliante': 0.78, 'Providence': 0.82, 'Boulder City': 0.85,
                'Inspirada': 1.05, 'Rhodes Ranch': 0.92, 'Skye Canyon': 1.00,
                'Lake Las Vegas': 1.32, 'Chinatown': 0.82, 'Arts District': 0.95,
                'Paradise': 0.88, 'Sunrise Manor': 0.70, 'Whitney Ranch': 0.98,
                'Southwest': 0.90, 'Lone Mountain': 1.05, 'Silverado Ranch': 0.92,
                'MacDonald Highlands': 1.38, 'Queensridge': 1.35, 'Tule Springs': 0.80
            },
            'Tampa': {
                'Downtown Tampa': 1.22, 'Channelside': 1.20, 'Harbour Island': 1.30,
                'Hyde Park': 1.35, 'SoHo (South Howard)': 1.25, 'Bayshore': 1.28,
                'Davis Islands': 1.32, 'Westshore': 1.05, 'Seminole Heights': 1.02,
                'Ybor City': 0.90, 'Brandon': 0.78, 'Riverview': 0.75,
                'Wesley Chapel': 0.80, 'New Tampa': 0.88, 'Temple Terrace': 0.82,
                'Plant City': 0.68, 'Clearwater': 0.92, 'St. Petersburg': 0.98,
                'Dunedin': 0.88, 'Safety Harbor': 0.85, 'Carrollwood': 0.90,
                'Westchase': 0.95, 'Lutz': 0.82, 'Valrico': 0.75,
                "Town 'n' Country": 0.80, 'Palma Ceia': 1.38, 'Beach Park': 1.15,
                'Fishhawk': 0.85, 'South Tampa': 1.18, 'Waterfront (St. Pete)': 1.10
            },
            'Raleigh': {
                'Downtown Raleigh': 1.20, 'North Hills': 1.18, 'Glenwood South': 1.22,
                'Cameron Village': 1.15, 'Five Points': 1.12, 'Cary': 1.05,
                'Apex': 0.92, 'Holly Springs': 0.85, 'Fuquay-Varina': 0.78,
                'Wake Forest': 0.82, 'Knightdale': 0.75, 'Garner': 0.72,
                'Clayton': 0.70, 'Morrisville': 0.98, 'Durham': 0.95,
                'Chapel Hill': 1.25, 'Carrboro': 1.10, 'Brier Creek': 1.02,
                'Midtown': 1.12, 'Oakwood': 1.15, 'Boylan Heights': 1.10,
                'ITB (Inside the Beltline)': 1.18, 'North Raleigh': 0.90,
                'West Raleigh': 0.92, 'Falls of Neuse': 0.88, 'Wendell': 0.72,
                'Zebulon': 0.68, 'RTP Area': 1.00, 'Hillsborough': 0.80, 'Wakefield': 0.95
            },
            'Dallas': {
                'Highland Park': 1.40, 'University Park': 1.35, 'Turtle Creek': 1.32, 'Uptown': 1.28,
                'Preston Hollow': 1.25, 'Downtown': 1.20, 'Knox-Henderson': 1.18, 'Victory Park': 1.18,
                'Design District': 1.15, 'Oak Lawn': 1.12, 'Lakewood': 1.10, 'Lower Greenville': 1.08,
                'Southlake': 1.08, 'Deep Ellum': 1.05, 'Bishop Arts': 1.02, 'Addison': 0.95,
                'Frisco': 0.92, 'Prosper': 0.90, 'Plano': 0.88, 'Coppell': 0.88,
                'Richardson': 0.85, 'Flower Mound': 0.85, 'McKinney': 0.82, 'Carrollton': 0.82,
                'Rockwall': 0.80, 'Allen': 0.80, 'Irving': 0.78, 'Lewisville': 0.78,
                'Arlington': 0.75, 'Denton': 0.75
            },
            'Atlanta': {
                'Buckhead': 1.35, 'Midtown': 1.25, 'Ansley Park': 1.22, 'Virginia-Highland': 1.18,
                'Inman Park': 1.15, 'Poncey-Highland': 1.12, 'West Midtown': 1.12, 'Old Fourth Ward': 1.08,
                'Druid Hills': 1.08, 'Brookhaven': 1.05, 'Downtown': 1.05, 'Grant Park': 1.02,
                'Vinings': 1.00, 'Reynoldstown': 1.00, 'Decatur': 0.95, 'East Atlanta Village': 0.92,
                'Sandy Springs': 0.92, 'Avondale Estates': 0.92, 'Kirkwood': 0.90, 'Johns Creek': 0.90,
                'Dunwoody': 0.88, 'Alpharetta': 0.88, 'Roswell': 0.85, 'Smyrna': 0.82,
                'Chamblee': 0.82, 'Peachtree City': 0.80, 'Marietta': 0.78, 'Tucker': 0.78,
                'Duluth': 0.75, 'Kennesaw': 0.72
            },
            'Philadelphia': {
                'Rittenhouse Square': 1.35, 'Society Hill': 1.28, 'Center City': 1.25,
                'Fitler Square': 1.22, 'Bryn Mawr (Main Line)': 1.22, 'Old City': 1.20,
                'Wayne (Main Line)': 1.18, 'Ardmore (Main Line)': 1.15, 'Fishtown': 1.12,
                'Queen Village': 1.12, 'University City': 1.10, 'Northern Liberties': 1.08,
                'Bella Vista': 1.08, 'Spring Garden': 1.08, 'Graduate Hospital': 1.05,
                'East Passyunk': 1.05, 'Chestnut Hill': 1.02, 'Conshohocken': 1.02,
                'Fairmount': 1.00, 'King of Prussia': 0.92, 'South Philadelphia': 0.88,
                'Haddonfield (NJ)': 0.88, 'West Chester': 0.88, 'Brewerytown': 0.88,
                'Manayunk': 0.85, 'Media': 0.85, 'Mount Airy': 0.82, 'Roxborough': 0.80,
                'Cherry Hill (NJ)': 0.80, 'Norristown': 0.68
            },
            'Phoenix': {
                'Paradise Valley': 1.40, 'Scottsdale (Old Town)': 1.30, 'Biltmore': 1.28,
                'Arcadia': 1.25, 'Scottsdale (North)': 1.22, 'North Scottsdale': 1.18,
                'Camelback East': 1.15, 'Downtown Phoenix': 1.12, 'Roosevelt Row': 1.08,
                'Cave Creek': 1.05, 'Tempe (Downtown)': 1.05, 'Encanto': 1.02,
                'Central Phoenix': 0.95, 'Fountain Hills': 0.95, 'Ahwatukee': 0.88,
                'Tempe (South)': 0.88, 'Chandler': 0.85, 'Gilbert': 0.82,
                'North Phoenix': 0.82, 'Goodyear': 0.80, 'Mesa (Central)': 0.78,
                'Peoria': 0.78, 'Anthem': 0.78, 'Glendale': 0.75, 'Queen Creek': 0.75,
                'South Mountain': 0.72, 'Mesa (East)': 0.72, 'Surprise': 0.72,
                'Sun City': 0.70, 'Avondale': 0.70
            },
            'San Diego': {
                'Coronado': 1.40, 'Rancho Santa Fe': 1.40, 'Del Mar': 1.38, 'La Jolla': 1.35,
                'Gaslamp Quarter': 1.22, 'Downtown': 1.20, 'Solana Beach': 1.18, 'Little Italy': 1.18,
                'Point Loma': 1.15, 'Carmel Valley': 1.15, 'Encinitas': 1.12, 'Pacific Beach': 1.12,
                'Mission Beach': 1.10, 'Hillcrest': 1.08, 'Carlsbad': 1.08, 'North Park': 1.05,
                'Ocean Beach': 1.02, 'Normal Heights': 0.98, 'University City': 0.95,
                'Poway': 0.92, 'Mission Valley': 0.92, 'Clairemont': 0.88,
                'Kearny Mesa': 0.85, 'Oceanside': 0.82, 'San Marcos': 0.78, 'City Heights': 0.78,
                'Chula Vista': 0.75, 'Escondido': 0.75, 'El Cajon': 0.72, 'National City': 0.68
            },
            'Nashville': {
                'Belle Meade': 1.38, 'Oak Hill': 1.30, 'The Gulch': 1.30, 'Downtown / SoBro': 1.28,
                '12South': 1.25, 'Germantown': 1.22, 'Green Hills': 1.20, 'Hillsboro Village': 1.18,
                'Midtown': 1.15, 'Belmont-Hillsboro': 1.15, 'Brentwood': 1.15,
                'East Nashville': 1.12, 'West End': 1.10, 'Wedgewood-Houston': 1.10,
                'Music Row': 1.08, 'The Nations': 1.05, 'Franklin': 1.05,
                'Sylvan Park': 1.02, 'Berry Hill': 0.95, 'Mt. Juliet': 0.82,
                'Hendersonville': 0.80, 'Donelson': 0.78, 'Murfreesboro': 0.75,
                'Goodlettsville': 0.75, 'Gallatin': 0.72, 'Hermitage': 0.72,
                'Madison': 0.70, 'Lebanon': 0.70, 'Antioch': 0.68, 'Whites Creek': 0.65
            },
            'Minneapolis': {
                'Kenwood': 1.30, 'Edina': 1.28, 'North Loop': 1.25, 'Linden Hills': 1.22,
                'Lowry Hill': 1.20, 'Downtown Minneapolis': 1.18, 'Lake Harriet': 1.18,
                'Uptown': 1.12, 'Northeast (NE)': 1.08, 'St. Paul (Summit Hill)': 1.08,
                'Southwest Minneapolis': 1.05, 'St. Paul (Highland Park)': 1.02,
                'St. Paul (Cathedral Hill)': 1.00, 'Whittier': 0.95, 'Minnetonka': 0.95,
                'St. Paul (Mac-Groveland)': 0.95, 'Prospect Park': 0.92, 'Longfellow': 0.92,
                'Plymouth': 0.92, 'Eden Prairie': 0.92, 'St. Paul (Downtown)': 0.90,
                'Nokomis': 0.90, 'Seward': 0.88, 'Bloomington': 0.88, 'Dinkytown': 0.85,
                'Maple Grove': 0.85, 'Powderhorn': 0.82, 'Eagan': 0.82,
                'Phillips': 0.75, 'Brooklyn Park': 0.72
            },
            'Portland': {
                'Pearl District': 1.30, 'Lake Oswego': 1.28, 'Nob Hill / NW 23rd': 1.22,
                'South Waterfront': 1.18, 'Downtown Portland': 1.15, 'West Linn': 1.15,
                'Laurelhurst': 1.12, 'Alberta Arts District': 1.10, 'Irvington': 1.08,
                'Hawthorne': 1.08, 'Mississippi District': 1.05, 'Division': 1.05,
                'Goose Hollow': 1.05, 'Sellwood-Moreland': 1.02, 'Buckman': 1.00,
                'Sunnyside': 0.98, 'Woodstock': 0.92, 'Brooklyn': 0.90,
                'Kenton': 0.88, 'Foster-Powell': 0.88, 'St. Johns': 0.85,
                'Montavilla': 0.85, 'Beaverton': 0.82, 'Milwaukie': 0.82,
                'Hillsboro': 0.80, 'Tigard': 0.78, 'Cully': 0.78,
                'Lents': 0.75, 'Oregon City': 0.72, 'Gresham': 0.70
            },
            'Toronto': {
                'Yorkville': 1.30, 'King West': 1.22, 'Liberty Village': 1.10,
                'Queen West': 1.08, 'The Annex': 1.12, 'Leslieville': 0.95,
                'Kensington Market': 0.92, 'Etobicoke': 0.80, 'Scarborough': 0.75,
                'North York': 0.85, 'Downtown Core': 1.18, 'Danforth': 0.90,
                'Distillery District': 1.15, 'Cabbagetown': 1.05, 'Roncesvalles': 1.02, 'High Park': 1.08, 'Midtown': 1.12, 'Bloor West Village': 0.95, 'Riverdale': 0.98, 'Parkdale': 0.82, 'Mimico': 0.78, 'Don Mills': 0.85, 'Forest Hill': 1.28, 'Yorkdale': 0.88
            },
            'Vancouver': {
                'Yaletown': 1.25, 'Kitsilano': 1.15, 'Gastown': 1.12,
                'West End': 1.10, 'Commercial Drive': 0.95, 'Mount Pleasant': 1.05,
                'East Van': 0.88, 'Burnaby': 0.82, 'Richmond': 0.85,
                'North Vancouver': 0.92, 'West Vancouver': 1.30, 'Surrey': 0.72,
                'Coal Harbour': 1.22, 'False Creek': 1.12, 'Kerrisdale': 1.08, 'Dunbar': 1.05, 'Marpole': 0.85, 'Hastings-Sunrise': 0.8, 'Main Street': 0.98, 'Point Grey': 1.15, 'Collingwood': 0.78, 'New Westminster': 0.75, 'Coquitlam': 0.78, 'Port Moody': 0.8
            },
            'Montreal': {
                'Plateau Mont-Royal': 1.18, 'Old Montreal': 1.22, 'Griffintown': 1.15,
                'Mile End': 1.08, 'Outremont': 1.20, 'Westmount': 1.30,
                'Villeray': 0.92, 'Rosemont': 0.95, 'Verdun': 0.88,
                'NDG (Notre-Dame-de-Grâce)': 0.90, 'Hochelaga': 0.78, 'Laval': 0.75,
                'Saint-Henri': 0.92, 'Ahuntsic': 0.85, 'Côte-des-Neiges': 0.82, 'Pointe-Saint-Charles': 0.88, 'Petite-Italie': 1.05, 'Mercier': 0.78, 'Lachine': 0.75, 'Saint-Laurent': 0.8, 'Dorval': 0.82, 'Brossard': 0.78, 'Longueuil': 0.72, 'Anjou': 0.75
            },
            'Mexico City': {
                'Polanco': 1.35, 'Condesa': 1.22, 'Roma Norte': 1.18,
                'Santa Fe': 1.15, 'Coyoacán': 1.02, 'Del Valle': 0.95,
                'Narvarte': 0.88, 'Tlalpan': 0.78, 'Iztapalapa': 0.65,
                'Centro Histórico': 0.90, 'San Ángel': 1.10,
                'Lomas de Chapultepec': 1.3, 'Juárez': 1.12, 'Anzures': 1.08, 'Pedregal': 1.22, 'Xochimilco': 0.72, 'Reforma': 1.15, 'Escandón': 0.95, 'Doctores': 0.78, 'Portales': 0.82, 'Cuauhtémoc': 0.9, 'Mixcoac': 0.85, 'Lindavista': 0.82, 'Insurgentes Sur': 1.05, 'Satélite': 0.8
            },
            'Cancún': {
                'Zona Hotelera': 1.35, 'Puerto Cancún': 1.28, 'Centro': 0.85,
                'SM 17 (Downtown)': 0.82, 'Alfredo V. Bonfil': 0.72, 'Playa Mujeres': 1.22,
                'Puerto Juárez': 0.90, 'Isla Mujeres': 1.15,
                'Punta Sam': 1.08, 'El Table': 0.78, 'Residencial Campestre': 0.82, 'Supermanzana 500': 0.7, 'Lagos del Sol': 0.88, 'Jardines del Sur': 0.75, 'Malecón Américas': 0.92
            },
            'Panama City': {
                'Punta Pacífica': 1.30, 'Costa del Este': 1.25, 'Casco Viejo': 1.12,
                'Obarrio': 1.10, 'El Cangrejo': 1.02, 'San Francisco': 1.08,
                'Calidonia': 0.78, 'Juan Díaz': 0.72, 'Clayton': 1.05,
                'Balboa': 0.92,
                'Marbella': 1.15, 'Bella Vista': 1.08, 'Condado del Rey': 0.85, 'Albrook': 0.88, 'Betania': 0.75, 'Transistmica': 0.72, 'San Miguelito': 0.68, 'Coco del Mar': 1.1, 'Vista Hermosa': 0.92
            },

            # ===== EUROPE - WESTERN =====
            'London': {
                'Mayfair': 1.45, 'Chelsea': 1.38, 'Kensington': 1.35,
                'Notting Hill': 1.28, 'Soho': 1.22, 'Shoreditch': 1.10,
                'Camden': 1.05, 'Islington': 1.12, 'Brixton': 0.88,
                'Hackney': 0.92, 'Peckham': 0.82, 'Canary Wharf': 1.15,
                'Greenwich': 0.90, 'Clapham': 0.95, 'Stratford': 0.78,
                'Marylebone': 1.32, 'Hampstead': 1.30,
                'Battersea': 1.05, 'Fulham': 1.1, 'Wimbledon': 1.02, 'Ealing': 0.85, 'Dalston': 0.95, 'Tooting': 0.82, 'Walthamstow': 0.8, 'Richmond': 1.18, 'Putney': 1.05, 'Chiswick': 1.1, 'Balham': 0.98, 'Lewisham': 0.78, 'Croydon': 0.72, 'Barking': 0.68, 'Angel (Islington)': 1.12, 'Vauxhall': 1.05, 'Bermondsey': 1.0, 'Kentish Town': 0.95
            },
            'Paris': {
                'Le Marais (3rd/4th)': 1.30, 'Saint-Germain (6th)': 1.35, 'Champs-Élysées (8th)': 1.40,
                'Montmartre (18th)': 0.92, 'Bastille (11th)': 1.05, 'Oberkampf (11th)': 1.02,
                'Belleville (20th)': 0.82, 'La Défense': 1.10, 'Pigalle (9th)': 0.95,
                'Nation (12th)': 0.88, 'Batignolles (17th)': 0.98, 'Boulogne-Billancourt': 1.08,
                'Latin Quarter (5th)': 1.25, 'Tour Eiffel (7th)': 1.38, 'Opéra (9th)': 1.15, 'République (10th)': 1.0, 'Bercy (12th)': 0.95, 'Alésia (14th)': 0.92, 'Vaugirard (15th)': 0.9, 'Passy (16th)': 1.3, 'Buttes-Chaumont (19th)': 0.85, 'Neuilly-sur-Seine': 1.25, 'Saint-Denis': 0.7, 'Vincennes': 0.95, 'Levallois-Perret': 1.1, 'Issy-les-Moulineaux': 1.02
            },
            'Amsterdam': {
                'Canal Ring (Centrum)': 1.30, 'Jordaan': 1.25, 'De Pijp': 1.10,
                'Oud-West': 1.15, 'Oud-Zuid': 1.28, 'Oost': 0.95,
                'Noord': 0.82, 'Nieuw-West': 0.75, 'Amstelveen': 0.88,
                'Zuidas': 1.20, 'Westerpark': 1.05,
                'Rivierenbuurt': 1.05, 'Buitenveldert': 0.92, 'Java-eiland': 1.08, 'IJburg': 0.88, 'Diemen': 0.78, 'Haarlem': 0.82, 'Watergraafsmeer': 0.98, 'Slotervaart': 0.72, 'Geuzenveld': 0.7
            },
            'Berlin': {
                'Mitte': 1.22, 'Prenzlauer Berg': 1.12, 'Kreuzberg': 1.08,
                'Friedrichshain': 1.02, 'Charlottenburg': 1.15, 'Neukölln': 0.85,
                'Schöneberg': 1.05, 'Wedding': 0.78, 'Tempelhof': 0.82,
                'Spandau': 0.72, 'Steglitz': 0.88, 'Grunewald': 1.30,
                'Lichtenberg': 0.75, 'Pankow': 0.85, 'Treptow': 0.82, 'Reinickendorf': 0.72, 'Moabit': 0.92, 'Köpenick': 0.78, 'Wilmersdorf': 1.1, 'Dahlem': 1.22, 'Zehlendorf': 1.05, 'Britz': 0.72, 'Rudow': 0.7, 'Friedenau': 0.98
            },
            'Munich': {
                'Altstadt-Lehel': 1.35, 'Maxvorstadt': 1.18, 'Schwabing': 1.22,
                'Bogenhausen': 1.15, 'Haidhausen': 1.10, 'Glockenbachviertel': 1.20,
                'Sendling': 0.92, 'Moosach': 0.82, 'Pasing': 0.85,
                'Neuhausen': 1.05, 'Berg am Laim': 0.88,
                'Schwabing-West': 1.18, 'Au': 1.08, 'Solln': 1.02, 'Trudering': 0.88, 'Milbertshofen': 0.82, 'Laim': 0.9, 'Riem': 0.85, 'Unterföhring': 0.95, 'Thalkirchen': 1.0
            },
            'Dublin': {
                'Dublin 2 (City Centre)': 1.25, 'Dublin 4 (Ballsbridge)': 1.30,
                'Dublin 6 (Ranelagh)': 1.15, 'Dublin 8 (Portobello)': 1.08,
                'Dún Laoghaire': 1.10, 'Rathmines': 1.05, 'Drumcondra': 0.92,
                'Tallaght': 0.75, 'Clontarf': 1.02, 'Howth': 1.12,
                'Dublin 1 (North City)': 1.08, 'Dublin 7 (Phibsborough)': 0.98, 'Dublin 3 (Clontarf)': 1.05, 'Dublin 9 (Griffith Avenue)': 0.95, 'Blackrock': 1.15, 'Stillorgan': 1.02, 'Sandyford': 0.9, 'Swords': 0.78, 'Lucan': 0.75
            },
            'Brussels': {
                'Ixelles': 1.18, 'Saint-Gilles': 1.05, 'Uccle': 1.22,
                'Sablon': 1.28, 'Etterbeek': 1.02, 'Schaerbeek': 0.85,
                'Molenbeek': 0.72, 'Woluwe-Saint-Pierre': 1.12, 'Forest': 0.88,
                'EU Quarter': 1.15, 'Auderghem': 0.95,
                'Avenue Louise': 1.2, 'Montgomery': 1.02, 'Flagey': 1.08, 'Place du Châtelain': 1.12, 'Jette': 0.8, 'Anderlecht': 0.72, 'Stockel': 1.05, 'Watermael-Boitsfort': 0.98, 'Evere': 0.82
            },
            'Luxembourg City': {
                'Ville Haute': 1.30, 'Kirchberg': 1.22, 'Belair': 1.18,
                'Limpertsberg': 1.15, 'Grund': 1.08, 'Bonnevoie': 0.88,
                'Gasperich': 1.05, 'Eich': 0.92, 'Hollerich': 0.85,
                'Cessange': 0.90,
                'Clausen': 1.02, 'Merl': 0.95, 'Pfaffenthal': 0.98, 'Neudorf': 0.88, 'Hamm': 0.82, 'Bertrange': 0.92, 'Strassen': 0.9
            },
            'Zurich': {
                'Bahnhofstrasse': 1.35, 'Seefeld': 1.25, 'Enge': 1.18,
                'Niederdorf': 1.15, 'Wiedikon': 1.02, 'Oerlikon': 0.88,
                'Altstetten': 0.82, 'Hottingen': 1.12, 'Wipkingen': 0.95,
                'Schwamendingen': 0.78,
                'Seebach': 0.8, 'Witikon': 1.05, 'Höngg': 0.92, 'Fluntern': 1.1, 'Leimbach': 0.82, 'Affoltern': 0.75, 'Wollishofen': 1.0, 'Unterstrass': 0.98
            },
            'Geneva': {
                'Eaux-Vives': 1.20, 'Champel': 1.25, 'Carouge': 1.05,
                'Plainpalais': 1.10, 'Pâquis': 0.92, 'Nations': 1.15,
                'Servette': 0.88, 'Meyrin': 0.78, 'Vernier': 0.75,
                'Cologny': 1.35,
                'Florissant': 1.18, 'Grand-Saconnex': 0.95, 'Lancy': 0.82, 'Onex': 0.72, 'Thônex': 0.85, 'Chêne-Bourg': 0.8, 'Bernex': 0.78, 'Plan-les-Ouates': 0.88
            },
            'Edinburgh': {
                'New Town': 1.25, 'Old Town': 1.18, 'Stockbridge': 1.15,
                'Morningside': 1.10, 'Marchmont': 1.02, 'Leith': 0.90,
                'Portobello': 0.88, 'Bruntsfield': 1.08, 'Gorgie': 0.78,
                'Corstorphine': 0.82,
                'Haymarket': 1.05, 'Dean Village': 1.15, 'Comely Bank': 1.02, 'Cramond': 0.92, 'Dalry': 0.85, 'Tollcross': 0.95, 'Murrayfield': 1.08, 'Newington': 0.9
            },
            'Nice': {
                'Promenade des Anglais': 1.30, 'Old Nice (Vieux Nice)': 1.18, 'Cimiez': 1.15,
                'Port': 1.05, 'Libération': 0.90, 'Riquier': 0.85,
                'Saint-Roch': 0.82, "L'Ariane": 0.70, 'Fabron': 0.95,
                'Mont Boron': 1.22,
                'Magnan': 0.88, 'Musiciens': 1.1, 'Carabacel': 0.82, 'Pasteur': 0.78, 'Gambetta': 0.85, 'Las Planas': 0.72, 'Saint-Isidore': 0.75, 'Caucade': 0.8
            },

            # ===== EUROPE - SOUTHERN =====
            'Madrid': {
                'Salamanca': 1.30, 'Chamberí': 1.18, 'Malasaña': 1.10,
                'Chueca': 1.12, 'La Latina': 1.05, 'Lavapiés': 0.90,
                'Retiro': 1.15, 'Chamartín': 1.08, 'Vallecas': 0.72,
                'Tetuán': 0.82, 'Moncloa': 1.02,
                'Barrio de las Letras': 1.15, 'Arganzuela': 0.95, 'Hortaleza': 0.85, 'Usera': 0.72, 'Carabanchel': 0.7, 'Moncloa-Aravaca': 1.08, 'Barajas': 0.8, 'Fuencarral': 0.88, 'Atocha': 1.0, 'Prosperidad': 0.92, 'Conde de Casal': 0.88, 'Arturo Soria': 0.95
            },
            'Barcelona': {
                'Eixample': 1.15, 'Gràcia': 1.08, 'Born / El Born': 1.20,
                'Gothic Quarter': 1.18, 'Barceloneta': 1.10, 'Poblenou': 1.02,
                'Raval': 0.88, 'Sants': 0.85, 'Sant Andreu': 0.78,
                'Sarrià-Sant Gervasi': 1.25, 'Horta-Guinardó': 0.80,
                'Pedralbes': 1.3, 'Les Corts': 1.05, 'Sant Martí': 0.82, 'El Clot': 0.8, 'Diagonal Mar': 1.08, 'Vila de Gràcia': 1.1, 'La Sagrada Família': 1.05, 'Sant Antoni': 1.02, 'Poble Sec': 0.92, 'Camp Nou': 0.9, 'Nou Barris': 0.72, 'Vallcarca': 0.85
            },
            'Valencia': {
                'El Carmen': 1.18, 'Ruzafa': 1.15, 'Eixample': 1.10,
                'Ciutat Vella': 1.12, 'El Cabanyal': 0.92, 'Benimaclet': 0.88,
                'Patraix': 0.82, 'Poblats Marítims': 0.85, 'Campanar': 0.90,
                'Quatre Carreres': 0.78,
                'La Seu': 1.08, 'Pla del Real': 1.05, 'Mestalla': 0.95, 'Algirós': 0.88, 'Jesús': 0.78, 'La Saïdia': 0.82, 'Olivereta': 0.75, 'Malvarrosa': 0.9
            },
            'Málaga': {
                'Centro Histórico': 1.22, 'Soho': 1.15, 'Pedregalejo': 1.10,
                'El Palo': 0.92, 'Huelin': 0.88, 'Teatinos': 0.85,
                'La Malagueta': 1.18, 'Puerto de la Torre': 0.75,
                'Churriana': 0.78, 'El Limonar': 1.12,
                'La Merced': 1.08, 'Carretera de Cádiz': 0.8, 'Ciudad Jardín': 0.92, 'Bailén-Miraflores': 0.78, 'Cruz de Humilladero': 0.82, 'Campanillas': 0.7, 'Rosaleda': 0.88, 'Victoria': 1.05
            },
            'Lisbon': {
                'Chiado': 1.28, 'Príncipe Real': 1.25, 'Alfama': 1.10,
                'Bairro Alto': 1.15, 'Estrela / Lapa': 1.12, 'Avenidas Novas': 1.05,
                'Alcântara': 0.95, 'Benfica': 0.82, 'Amadora': 0.72,
                'Parque das Nações': 1.08, 'Campo de Ourique': 1.02,
                'Santos': 1.08, 'Graça': 1.05, 'Anjos': 0.92, 'Penha de França': 0.85, 'Belém': 1.1, 'Lumiar': 0.88, 'Telheiras': 0.9, 'Marvila': 0.78, 'Olivais': 0.8
            },
            'Porto': {
                'Ribeira': 1.22, 'Foz do Douro': 1.25, 'Cedofeita': 1.10,
                'Boavista': 1.15, 'Bonfim': 0.95, 'Campanhã': 0.78,
                'Paranhos': 0.85, 'Ramalde': 0.82, 'Matosinhos': 0.90,
                'Vila Nova de Gaia': 0.88,
                'Clérigos': 1.15, 'Miragaia': 1.05, 'Lordelo do Ouro': 0.92, 'Aldoar': 0.82, 'Massarelos': 1.02, 'São Bento': 1.1, 'Bonfim Sul': 0.88, 'Gondomar': 0.75
            },
            'Rome': {
                'Centro Storico': 1.30, 'Trastevere': 1.15, 'Prati': 1.18,
                'Testaccio': 1.05, 'Monti': 1.20, 'San Giovanni': 0.92,
                'EUR': 0.88, 'Pigneto': 0.85, 'Ostiense': 0.90,
                'Garbatella': 0.82, 'Flaminio': 1.08,
                'Aventino': 1.12, 'Coppedè': 1.15, 'Nomentano': 1.02, 'Balduina': 0.92, 'Trastevere Nord': 1.08, 'San Lorenzo': 0.85, 'Monteverde': 0.88, 'Tor Vergata': 0.72, 'Parioli': 1.22, 'Trieste': 1.05, 'Appio-Latino': 0.82
            },
            'Milan': {
                'Brera': 1.30, 'Navigli': 1.15, 'Porta Nuova': 1.25,
                'City Centre': 1.35, 'Isola': 1.10, 'Città Studi': 0.90,
                'Lambrate': 0.85, 'Bovisa': 0.78, 'San Siro': 0.88,
                'Porta Venezia': 1.12,
                'Tortona': 1.08, 'Loreto': 0.95, 'Garibaldi': 1.18, 'Porta Romana': 1.1, 'Cenisio': 0.92, 'Bicocca': 0.82, 'Corsica': 0.88, 'Porta Ticinese': 1.05, 'Sarpi': 0.95, 'Nolo': 0.85, 'QT8': 0.8
            },
            'Athens': {
                'Kolonaki': 1.30, 'Plaka': 1.18, 'Kifissia': 1.22,
                'Glyfada': 1.15, 'Pangrati': 1.02, 'Exarchia': 0.85,
                'Koukaki': 1.05, 'Nea Smyrni': 0.90, 'Piraeus': 0.78,
                'Marousi': 0.95, 'Psyrri': 1.08,
                'Vouliagmeni': 1.25, 'Monastiraki': 1.1, 'Thisio': 1.08, 'Ampelokipoi': 0.88, 'Patisia': 0.72, 'Zografou': 0.82, 'Halandri': 0.92, 'Filothei': 1.18, 'Peristeri': 0.75
            },
            'Split': {
                'Diocletian\'s Palace': 1.25, 'Bačvice': 1.15, 'Manuš': 1.05,
                'Žnjan': 1.10, 'Firule': 1.02, 'Spinut': 0.90,
                'Sućidar': 0.82, 'Trstenik': 0.88, 'Mertojak': 0.92,
                'Varoš': 1.0, 'Bol': 0.95, 'Gripe': 0.85, 'Lokve': 0.78, 'Kman': 0.8, 'Pazdigrad': 0.88, 'Brda': 0.82
            },

            # ===== EUROPE - NORTHERN =====
            'Stockholm': {
                'Östermalm': 1.32, 'Södermalm': 1.15, 'Kungsholmen': 1.10,
                'Vasastan': 1.12, 'Gamla Stan': 1.20, 'Djurgården': 1.18,
                'Hammarby Sjöstad': 1.05, 'Hägersten': 0.88, 'Farsta': 0.75,
                'Solna': 0.90, 'Nacka': 0.92, 'Lidingö': 1.08,
                'Norrmalm': 1.22, 'Bromma': 0.95, 'Enskede': 0.82, 'Skärholmen': 0.72, 'Bandhagen': 0.78, 'Liljeholmen': 1.02, 'Kista': 0.8, 'Sundbyberg': 0.88, 'Täby': 0.95, 'Danderyd': 1.15, 'Vallentuna': 0.72, 'Huddinge': 0.78
            },
            'Copenhagen': {
                'Indre By (City Centre)': 1.28, 'Frederiksberg': 1.18, 'Nørrebro': 1.02,
                'Vesterbro': 1.10, 'Østerbro': 1.15, 'Christianshavn': 1.12,
                'Amager': 0.90, 'Valby': 0.85, 'Brønshøj': 0.80,
                'Hellerup': 1.22, 'Nordvest': 0.78,
                'Sydhavnen': 0.92, 'Vanløse': 0.82, 'Gentofte': 1.18, 'Hvidovre': 0.78, 'Rødovre': 0.75, 'Islands Brygge': 1.08, 'Nørreport': 1.15, 'Carlsberg Byen': 1.05, 'Nordhavn': 1.12
            },
            'Helsinki': {
                'Kruununhaka': 1.25, 'Eira': 1.22, 'Punavuori': 1.15,
                'Kallio': 1.05, 'Töölö': 1.12, 'Ullanlinna': 1.18,
                'Vallila': 0.95, 'Sörnäinen': 0.88, 'Vuosaari': 0.75,
                'Espoo (Tapiola)': 0.92, 'Kontula': 0.72,
                'Lauttasaari': 1.08, 'Herttoniemi': 0.85, 'Munkkiniemi': 1.02, 'Pasila': 0.9, 'Malmi': 0.72, 'Kulosaari': 1.12, 'Arabianranta': 0.92, 'Jätkäsaari': 1.05, 'Katajanokka': 1.18
            },
            'Oslo': {
                'Frogner': 1.30, 'Majorstuen': 1.18, 'Grünerløkka': 1.12,
                'Aker Brygge': 1.25, 'Sentrum': 1.15, 'St. Hanshaugen': 1.08,
                'Tøyen': 0.88, 'Sagene': 1.02, 'Grønland': 0.82,
                'Stovner': 0.72, 'Bærum': 1.10,
                'Bygdøy': 1.22, 'Holmenkollen': 1.18, 'Nydalen': 1.02, 'Torshov': 1.05, 'Alna': 0.78, 'Nordstrand': 0.92, 'Lambertseter': 0.85, 'Ullern': 1.12, 'Manglerud': 0.8
            },
            'Vienna': {
                'Innere Stadt (1st)': 1.35, 'Josefstadt (8th)': 1.15, 'Neubau (7th)': 1.12,
                'Wieden (4th)': 1.18, 'Mariahilf (6th)': 1.08, 'Landstraße (3rd)': 1.05,
                'Leopoldstadt (2nd)': 0.95, 'Favoriten (10th)': 0.75, 'Ottakring (16th)': 0.82,
                'Döbling (19th)': 1.20, 'Hietzing (13th)': 1.10,
                'Alsergrund (9th)': 1.08, 'Margareten (5th)': 0.95, 'Brigittenau (20th)': 0.78, 'Floridsdorf (21st)': 0.72, 'Donaustadt (22nd)': 0.8, 'Liesing (23rd)': 0.82, 'Meidling (12th)': 0.85, 'Penzing (14th)': 0.88, 'Hernals (17th)': 0.82
            },

            # ===== EUROPE - EASTERN =====
            'Prague': {
                'Prague 1 (Old Town)': 1.30, 'Prague 2 (Vinohrady)': 1.18, 'Prague 3 (Žižkov)': 0.95,
                'Prague 5 (Smíchov)': 1.05, 'Prague 6 (Dejvice)': 1.12, 'Prague 7 (Holešovice)': 1.08,
                'Prague 4 (Nusle)': 0.88, 'Prague 8 (Karlín)': 1.02, 'Prague 9': 0.78,
                'Prague 10': 0.82,
                'Prague 11 (Chodov)': 0.78, 'Prague 12 (Modřany)': 0.75, 'Prague 13 (Stodůlky)': 0.72, 'Letná': 1.1, 'Anděl': 1.08, 'Vršovice': 0.9, 'Bubeneč': 1.12, 'Troja': 0.85
            },
            'Budapest': {
                'District V (Belváros)': 1.30, 'District VI (Terézváros)': 1.15, 'District VII (Jewish Quarter)': 1.12,
                'District I (Buda Castle)': 1.22, 'District II (Buda Hills)': 1.18, 'District IX (Ferencváros)': 1.02,
                'District XIII': 1.05, 'District XI (Újbuda)': 0.92, 'District VIII (Józsefváros)': 0.82,
                'District XIV (Zugló)': 0.85, 'District III (Óbuda)': 0.88,
                'District IV (Újpest)': 0.78, 'District X (Kőbánya)': 0.75, 'District XV (Rákospalota)': 0.72, 'District XII (Hegyvidék)': 1.15, 'District XVI (Árpádföld)': 0.8, 'Margaret Island': 1.1, 'Csepel': 0.68, 'Kelenföld': 0.85
            },
            'Warsaw': {
                'Śródmieście (Centre)': 1.25, 'Mokotów': 1.12, 'Żoliborz': 1.15,
                'Wilanów': 1.18, 'Wola': 1.05, 'Praga Północ': 0.88,
                'Ursynów': 0.85, 'Ochota': 0.95, 'Bielany': 0.82,
                'Bemowo': 0.78, 'Targówek': 0.72,
                'Kabaty': 0.88, 'Saska Kępa': 1.08, 'Stary Mokotów': 1.15, 'Muranów': 0.95, 'Natolin': 0.82, 'Służewiec': 0.92, 'Powsin': 0.78, 'Grochów': 0.75
            },
            'Krakow': {
                'Old Town (Stare Miasto)': 1.28, 'Kazimierz': 1.18, 'Podgórze': 1.05,
                'Krowodrza': 0.95, 'Dębniki': 0.90, 'Zabłocie': 1.08,
                'Nowa Huta': 0.72, 'Prądnik Biały': 0.82, 'Bronowice': 0.85,
                'Ruczaj': 0.88,
                'Salwator': 1.05, 'Zwierzyniec': 1.1, 'Łagiewniki': 0.82, 'Prądnik Czerwony': 0.8, 'Mistrzejowice': 0.72, 'Kurdwanów': 0.75, 'Bieżanów': 0.7, 'Czyżyny': 0.85
            },
            'Bucharest': {
                'Dorobanți': 1.28, 'Primăverii': 1.25, 'Floreasca': 1.18,
                'Herăstrău': 1.22, 'Cotroceni': 1.10, 'Aviatorilor': 1.15,
                'Pipera': 1.02, 'Militari': 0.75, 'Rahova': 0.70,
                'Tineretului': 0.88, 'Berceni': 0.78,
                'Unirii': 1.05, 'Titan': 0.82, 'Drumul Taberei': 0.78, 'Băneasa': 1.12, 'Colentina': 0.72, 'Pantelimon': 0.68, 'Victoriei': 1.08, 'Giurgiului': 0.65
            },
            'Tallinn': {
                'Old Town (Vanalinn)': 1.28, 'Kalamaja': 1.15, 'Kadriorg': 1.18,
                'Pirita': 1.10, 'Telliskivi': 1.12, 'Rotermanni': 1.08,
                'Kristiine': 0.92, 'Mustamäe': 0.82, 'Lasnamäe': 0.72,
                'Nõmme': 0.88,
                'Pelgulinn': 0.85, 'Kopli': 0.78, 'Tondi': 0.82, 'Viimsi': 0.92, 'Haabersti': 0.8, 'Õismäe': 0.75, 'Ülemiste': 0.88
            },
            'Riga': {
                'Old Riga (Vecrīga)': 1.25, 'Quiet Centre': 1.18, 'Āgenskalns': 1.05,
                'Mežaparks': 1.10, 'Grīziņkalns': 0.92, 'Teika': 0.95,
                'Purvciems': 0.78, 'Imanta': 0.75, 'Ziepniekkalns': 0.72,
                'Torņakalns': 0.88,
                'Sarkandaugava': 0.8, 'Jugla': 0.72, 'Ķengarags': 0.7, 'Dreiliņi': 0.68, 'Čiekurkalns': 0.82, 'Berģi': 0.75, 'Iļguciems': 0.78
            },
            'Istanbul': {
                'Beşiktaş': 1.28, 'Nişantaşı': 1.35, 'Kadıköy': 1.15,
                'Bebek': 1.30, 'Cihangir': 1.18, 'Karaköy': 1.12,
                'Şişli': 1.05, 'Üsküdar': 0.92, 'Bakırköy': 0.88,
                'Fatih': 0.82, 'Beyoğlu': 1.08, 'Esenyurt': 0.65,
                'Sarıyer': 1.12, 'Ataşehir': 1.05, 'Maltepe': 0.88, 'Pendik': 0.75, 'Levent': 1.22, 'Etiler': 1.25, 'Bağcılar': 0.68, 'Beykoz': 0.92, 'Çekmeköy': 0.78, 'Zeytinburnu': 0.8, 'Küçükçekmece': 0.72, 'Kartal': 0.82
            },

            # ===== ASIA - EAST =====
            'Tokyo': {
                'Minato (Roppongi)': 1.30, 'Shibuya': 1.25, 'Shinjuku': 1.18,
                'Chiyoda (Marunouchi)': 1.35, 'Meguro': 1.15, 'Setagaya': 1.08,
                'Nakano': 0.92, 'Suginami': 0.88, 'Koto (Toyosu)': 1.05,
                'Adachi': 0.75, 'Edogawa': 0.78, 'Bunkyo': 1.10,
                'Daikanyama': 1.28, 'Ebisu': 1.22, 'Ikebukuro': 1.08, 'Asakusa': 0.92, 'Akihabara': 1.0, 'Nerima': 0.82, 'Katsushika': 0.72, 'Toshima': 0.95, 'Shinagawa': 1.12, 'Kichijoji (Musashino)': 0.98, 'Chofu': 0.85, 'Machida': 0.78, 'Ota': 0.88, 'Arakawa': 0.82, 'Sumida': 0.9, 'Taito': 0.95, 'Itabashi': 0.8, 'Azabu': 1.35
            },
            'Osaka': {
                'Kita (Umeda)': 1.22, 'Chuo (Namba)': 1.18, 'Tennoji': 1.08,
                'Fukushima': 1.10, 'Nishi': 1.05, 'Shinmachi': 1.02,
                'Sumiyoshi': 0.88, 'Higashiyodogawa': 0.82, 'Ikuno': 0.78,
                'Sakai': 0.75,
                'Shinsaibashi': 1.15, 'Tsurumi': 0.8, 'Abeno': 1.02, 'Minoh': 0.85, 'Toyonaka': 0.9, 'Ibaraki': 0.82, 'Nishinari': 0.68, 'Yodogawa': 0.85, 'Joto': 0.78, 'Miyakojima': 0.92
            },
            'Fukuoka': {
                'Tenjin': 1.20, 'Hakata': 1.15, 'Daimyo': 1.12,
                'Yakuin': 1.08, 'Ohori': 1.10, 'Nishijin': 0.92,
                'Hakozaki': 0.85, 'Kashii': 0.80, 'Noke': 0.78,
                'Momochi': 1.05,
                'Imaizumi': 1.1, 'Ropponmatsu': 1.05, 'Meinohama': 0.82, 'Chihaya': 0.78, 'Nishijin Area': 0.88, 'Muromi': 0.85, 'Zasshonokuma': 0.75, 'Takamiya': 0.82
            },
            'Seoul': {
                'Gangnam': 1.30, 'Itaewon': 1.15, 'Myeongdong': 1.20,
                'Hongdae': 1.08, 'Bukchon': 1.18, 'Yeouido': 1.12,
                'Sinchon': 0.92, 'Gwangjin': 0.88, 'Nowon': 0.75,
                'Mapo': 1.02,
                'Seocho': 1.25, 'Jongno': 1.15, 'Jung-gu': 1.12, 'Songpa': 1.1, 'Yongsan': 1.08, 'Seodaemun': 0.92, 'Dongjak': 0.95, 'Eunpyeong': 0.8, 'Geumcheon': 0.72, 'Dobong': 0.75, 'Gangdong': 0.88, 'Yangcheon': 0.85
            },
            'Hong Kong': {
                'Central': 1.40, 'The Peak': 1.50, 'Mid-Levels': 1.30,
                'Causeway Bay': 1.25, 'Tsim Sha Tsui': 1.15, 'Wan Chai': 1.18,
                'Mong Kok': 0.92, 'Sham Shui Po': 0.78, 'Tai Po': 0.72,
                'Sai Kung': 0.85, 'Discovery Bay': 1.10,
                'Repulse Bay': 1.3, 'Aberdeen': 0.92, 'Happy Valley': 1.22, 'Tseung Kwan O': 0.8, 'Sha Tin': 0.78, 'Tuen Mun': 0.68, 'Yuen Long': 0.65, 'Kennedy Town': 1.05, 'North Point': 1.0, 'Quarry Bay': 0.98, 'Hung Hom': 0.88
            },
            'Taipei': {
                'Da\'an': 1.25, 'Xinyi': 1.30, 'Zhongshan': 1.12,
                'Songshan': 1.08, 'Zhongzheng': 1.10, 'Shilin': 0.92,
                'Beitou': 0.88, 'Neihu': 1.02, 'Wanhua': 0.82,
                'Banqiao (New Taipei)': 0.78,
                'Wenshan': 0.85, 'Nangang': 0.9, 'Datong': 0.8, 'Tamsui': 0.72, 'Xindian (New Taipei)': 0.78, 'Yonghe (New Taipei)': 0.82, 'Zhonghe (New Taipei)': 0.78, 'Linkou (New Taipei)': 0.72, 'Tianmu': 1.05, 'Donghu': 0.95
            },
            'Shanghai': {
                'Jing\'an': 1.30, 'Xuhui (French Concession)': 1.28, 'Lujiazui (Pudong)': 1.25,
                'Huangpu (The Bund)': 1.22, 'Changning': 1.10, 'Hongkou': 0.92,
                'Yangpu': 0.88, 'Minhang': 0.82, 'Baoshan': 0.75,
                'Putuo': 0.90,
                'Xintiandi': 1.25, 'Pudong (Century Park)': 1.15, 'Gubei': 1.12, 'Qingpu': 0.72, 'Songjiang': 0.7, 'Jiading': 0.68, 'Zhabei': 0.88, 'Pudong (Jinqiao)': 1.05, 'Luwan': 1.18, 'Fengxian': 0.65, 'Chuansha': 0.72, 'Zhangjiang': 1.02
            },
            'Beijing': {
                'Chaoyang (CBD)': 1.28, 'Dongcheng': 1.22, 'Xicheng': 1.18,
                'Haidian (Zhongguancun)': 1.15, 'Shunyi': 1.08, 'Chaoyang (Sanlitun)': 1.25,
                'Fengtai': 0.82, 'Tongzhou': 0.75, 'Daxing': 0.72,
                'Changping': 0.78,
                'Wangjing': 1.08, 'Yizhuang': 0.82, 'Shijingshan': 0.85, 'Dongzhimen': 1.15, 'Guomao': 1.22, 'Wudaokou': 1.05, 'Xidan': 1.12, 'Wangfujing': 1.18, 'Lido': 1.05, 'Yansha': 1.1, 'Zhongguancun South': 1.08, 'Mentougou': 0.68
            },
            'Shenzhen': {
                'Nanshan (Shekou)': 1.25, 'Futian (CBD)': 1.22, 'Luohu': 1.05,
                'Nanshan (Tech Park)': 1.18, 'Bao\'an': 0.82, 'Longhua': 0.78,
                'Longgang': 0.72, 'Yantian': 0.85, 'Guangming': 0.75,
                'Qianhai': 1.12,
                'Houhai': 1.2, 'Chegongmiao': 1.08, 'Shuiwei': 1.02, 'Sungang': 0.9, 'Buji': 0.75, 'Xili': 0.88, 'Shahe': 0.82, 'Dalang': 0.7, 'Pingshan': 0.68
            },
            'Guangzhou': {
                'Tianhe': 1.22, 'Yuexiu': 1.10, 'Haizhu': 1.02,
                'Liwan': 0.92, 'Panyu': 0.82, 'Baiyun': 0.78,
                'Huangpu': 1.05, 'Nansha': 0.75, 'Zhujiang New Town': 1.18,
                'Huadu': 0.72,
                'Dongshan': 1.08, 'Jiangnan Xi': 0.95, 'Wuyang': 1.02, 'Zhujiang New Town East': 1.12, 'Dongpu': 0.8, 'Fangcun': 0.78, 'Luogang': 0.72, 'Conghua': 0.65, 'Zengcheng': 0.68
            },

            # ===== ASIA - SOUTHEAST =====
            'Singapore': {
                'Orchard Road': 1.30, 'Marina Bay': 1.35, 'Raffles Place': 1.25,
                'Holland Village': 1.12, 'Tiong Bahru': 1.10, 'Tanjong Pagar': 1.15,
                'Bukit Timah': 1.18, 'Clementi': 0.88, 'Woodlands': 0.75,
                'Tampines': 0.78, 'Jurong East': 0.80, 'Sentosa': 1.40,
                'Toa Payoh': 0.82, 'Ang Mo Kio': 0.78, 'Bishan': 0.85, 'Queenstown': 0.88, 'Novena': 1.05, 'Bedok': 0.78, 'Punggol': 0.72, 'Sengkang': 0.72, 'Pasir Ris': 0.75, 'Serangoon': 0.85, 'Katong': 1.02, 'Dempsey Hill': 1.22
            },
            'Bangkok': {
                'Sukhumvit (Asoke)': 1.25, 'Silom / Sathorn': 1.22, 'Siam': 1.18,
                'Thonglor': 1.28, 'Ekkamai': 1.15, 'Ari': 1.10,
                'Khao San': 0.85, 'On Nut': 0.88, 'Phra Khanong': 0.92,
                'Bang Na': 0.78, 'Chatuchak': 0.90, 'Ladprao': 0.82,
                'Ratchadaphisek': 1.02, 'Phrom Phong': 1.18, 'Sathorn': 1.15, 'Pratunam': 0.95, 'Saphan Kwai': 0.88, 'Rama 9': 1.02, 'Bangrak': 0.92, 'Thong Lo Soi': 1.22, 'Udom Suk': 0.8, 'Bearing': 0.75, 'Pinklao': 0.82, 'Bangsue': 0.85
            },
            'Chiang Mai': {
                'Old City': 1.15, 'Nimmanhaemin': 1.22, 'Santitham': 1.05,
                'Chang Khlan (Night Bazaar)': 1.08, 'Hang Dong': 0.82, 'San Sai': 0.78,
                'Mae Rim': 0.85, 'Suthep': 1.02, 'Wualai': 0.92,
                'San Kamphaeng': 0.75,
                'Tha Phae': 1.1, 'Night Bazaar East': 1.02, 'Wat Ket': 0.88, 'Chang Phueak': 0.95, 'Ban Waen': 0.72, 'Mae Hia': 0.75, 'Pa Tan': 0.82, 'Don Kaeo': 0.78
            },
            'Phuket': {
                'Patong': 1.22, 'Kata': 1.12, 'Karon': 1.08,
                'Kamala': 1.15, 'Surin': 1.20, 'Bang Tao': 1.18,
                'Phuket Town': 0.85, 'Rawai': 0.92, 'Chalong': 0.88,
                'Cherng Talay': 1.05,
                'Mai Khao': 1.1, 'Nai Harn': 1.05, 'Kata Noi': 1.15, 'Ao Po': 0.85, 'Thalang': 0.78, 'Kathu': 0.82, 'Wichit': 0.8, 'Koh Kaew': 0.88
            },
            'Kuala Lumpur': {
                'KLCC': 1.30, 'Bukit Bintang': 1.22, 'Bangsar': 1.18,
                'Mont Kiara': 1.15, 'Damansara Heights': 1.20, 'Sri Hartamas': 1.08,
                'Petaling Jaya': 0.90, 'Cheras': 0.78, 'Sentul': 0.82,
                'Kepong': 0.75, 'Desa ParkCity': 1.10,
                'Bukit Jalil': 0.92, 'Taman Tun Dr Ismail': 1.08, 'Ampang': 0.85, 'Setapak': 0.72, 'Wangsa Maju': 0.78, 'Brickfields': 0.88, 'Mid Valley': 1.05, 'Kuchai Lama': 0.8, 'Old Klang Road': 0.82
            },
            'Ho Chi Minh City': {
                'District 1': 1.30, 'District 2 (Thao Dien)': 1.22, 'District 3': 1.15,
                'District 7 (Phu My Hung)': 1.12, 'Binh Thanh': 1.02, 'District 4': 0.90,
                'Go Vap': 0.82, 'Tan Binh': 0.85, 'Thu Duc': 0.88,
                'Binh Tan': 0.72,
                'District 5 (Chinatown)': 0.85, 'District 6': 0.78, 'District 8': 0.72, 'District 10': 0.88, 'District 11': 0.82, 'Phu Nhuan': 0.95, 'Tan Phu': 0.78, 'District 9': 0.8, 'Nha Be': 0.72
            },
            'Hanoi': {
                'Hoan Kiem (Old Quarter)': 1.25, 'Ba Dinh': 1.18, 'Tay Ho (West Lake)': 1.22,
                'Hai Ba Trung': 1.08, 'Dong Da': 1.02, 'Cau Giay': 1.05,
                'Thanh Xuan': 0.88, 'Ha Dong': 0.78, 'Long Bien': 0.82,
                'Hoang Mai': 0.85,
                'Nam Tu Liem': 0.88, 'Bac Tu Liem': 0.82, 'Tay Ho Tay': 1.15, 'My Dinh': 0.92, 'Gia Lam': 0.75, 'Thanh Tri': 0.72, 'Truc Bach': 1.08, 'Kim Ma': 1.05, 'Van Quan': 0.8
            },
            'Manila': {
                'Makati (CBD)': 1.28, 'BGC (Taguig)': 1.25, 'Rockwell': 1.22,
                'Alabang': 1.10, 'Ortigas': 1.08, 'Eastwood (Quezon City)': 1.02,
                'Pasig': 0.92, 'Mandaluyong': 0.95, 'Quezon City (Cubao)': 0.82,
                'Manila (Ermita)': 0.78, 'Las Piñas': 0.75,
                'Greenhills': 1.05, 'San Juan': 0.98, 'Marikina': 0.82, 'Antipolo': 0.72, 'Paranaque': 0.85, 'Muntinlupa': 0.88, 'Valenzuela': 0.72, 'Cainta': 0.75, 'Quezon City (Diliman)': 0.88
            },
            'Jakarta': {
                'Menteng': 1.30, 'Sudirman (SCBD)': 1.25, 'Kemang': 1.18,
                'Kuningan': 1.15, 'Senopati': 1.20, 'Pondok Indah': 1.12,
                'Kelapa Gading': 1.02, 'Pluit': 0.90, 'Cempaka Putih': 0.82,
                'Bekasi': 0.72, 'Tangerang': 0.75,
                'Cikini': 1.1, 'Thamrin': 1.22, 'Pantai Indah Kapuk': 1.08, 'Sunter': 0.88, 'Ancol': 0.85, 'Tebet': 0.95, 'Cipete': 1.02, 'Cilandak': 1.05, 'Depok': 0.68, 'Bintaro': 0.82
            },
            'Bali (Denpasar)': {
                'Seminyak': 1.28, 'Canggu': 1.22, 'Ubud': 1.10,
                'Sanur': 1.05, 'Kuta': 0.92, 'Nusa Dua': 1.18,
                'Jimbaran': 1.12, 'Denpasar Centre': 0.82, 'Uluwatu': 1.15,
                'Legian': 0.88,
                'Kedonganan': 1.08, 'Pererenan': 1.15, 'Tabanan': 0.75, 'Gianyar': 0.8, 'Amed': 0.85, 'Lovina': 0.78, 'Pecatu': 1.1, 'Keramas': 0.82
            },
            'Phnom Penh': {
                'BKK1': 1.30, 'BKK2': 1.10, 'Tonle Bassac': 1.22,
                'Daun Penh (Riverside)': 1.15, 'Toul Tom Poung (Russian Market)': 1.05,
                'Chroy Changvar': 0.90, 'Toul Kork': 0.95, 'Sen Sok': 0.78,
                'Meanchey': 0.72, 'Chamkarmon': 1.02,
                'BKK3': 1.0, 'Tuol Sleng': 0.85, 'Chbar Ampov': 0.68, 'Prek Pnov': 0.62, 'Russey Keo': 0.72, 'Boeung Kak': 0.88, 'Olympic': 0.92
            },

            # ===== ASIA - SOUTH =====
            'Mumbai': {
                'South Mumbai (Colaba)': 1.35, 'Bandra West': 1.28, 'Juhu': 1.22,
                'Worli': 1.25, 'Lower Parel': 1.18, 'Andheri West': 1.05,
                'Powai': 1.08, 'Dadar': 0.95, 'Andheri East': 0.88,
                'Borivali': 0.78, 'Thane': 0.72, 'Navi Mumbai': 0.75,
                'Kandivali West': 0.82, 'Malad West': 0.8, 'Goregaon West': 0.85, 'Chembur': 0.88, 'Wadala': 0.92, 'BKC': 1.2, 'Versova': 1.02, 'Santacruz West': 1.05, 'Vikhroli': 0.82, 'Mulund': 0.75, 'Ghatkopar West': 0.82, 'Khar West': 1.12, 'Matunga': 0.95, 'Sion': 0.85
            },
            'Bangalore': {
                'Indiranagar': 1.25, 'Koramangala': 1.22, 'Whitefield': 1.08,
                'MG Road': 1.18, 'HSR Layout': 1.05, 'Jayanagar': 1.02,
                'Electronic City': 0.85, 'Marathahalli': 0.92, 'Yelahanka': 0.78,
                'Bannerghatta Road': 0.88, 'Hebbal': 0.95,
                'Sadashivanagar': 1.15, 'Rajajinagar': 0.95, 'Malleswaram': 1.02, 'Basavanagudi': 0.98, 'JP Nagar': 0.88, 'BTM Layout': 0.85, 'Bellandur': 0.92, 'Sarjapur Road': 0.85, 'Ulsoor': 1.08, 'Shivajinagar': 0.9, 'Vijayanagar': 0.78, 'Kengeri': 0.72
            },
            'Delhi': {
                'South Delhi (GK)': 1.30, 'Lutyens Delhi': 1.40, 'Hauz Khas': 1.18,
                'Defence Colony': 1.22, 'Vasant Kunj': 1.08, 'Dwarka': 0.85,
                'Rohini': 0.78, 'Gurugram (DLF)': 1.12, 'Noida (Sector 18)': 0.82,
                'Saket': 1.05, 'Karol Bagh': 0.88,
                'Lajpat Nagar': 1.05, 'Greater Kailash': 1.25, 'Rajouri Garden': 0.88, 'Connaught Place': 1.22, 'Janakpuri': 0.8, 'Patel Nagar': 0.82, 'Mayur Vihar': 0.85, 'Pitampura': 0.82, 'Vasant Vihar': 1.18, 'Chanakyapuri': 1.3, 'Green Park': 1.1, 'Lodhi Colony': 1.15, 'Nehru Place': 0.92
            },
            'Chennai': {
                'Adyar': 1.18, 'Nungambakkam': 1.22, 'T. Nagar': 1.10,
                'Anna Nagar': 1.05, 'Mylapore': 1.08, 'OMR (Sholinganallur)': 0.92,
                'Velachery': 0.88, 'Tambaram': 0.75, 'Porur': 0.82,
                'Besant Nagar': 1.15,
                'Boat Club': 1.2, 'Alwarpet': 1.15, 'Kilpauk': 1.02, 'Thiruvanmiyur': 1.05, 'Perungudi': 0.85, 'Chromepet': 0.72, 'Medavakkam': 0.78, 'Kodambakkam': 0.92, 'Royapettah': 1.0, 'Egmore': 0.95
            },

            # ===== OCEANIA =====
            'Sydney': {
                'CBD': 1.25, 'Bondi': 1.22, 'Surry Hills': 1.15,
                'Darlinghurst': 1.12, 'Newtown': 1.05, 'Manly': 1.10,
                'Parramatta': 0.82, 'Bankstown': 0.72, 'Chatswood': 0.95,
                'Pyrmont': 1.18, 'Mosman': 1.28, 'Marrickville': 0.90,
                'Glebe': 1.08, 'Redfern': 1.02, 'Balmain': 1.1, 'Coogee': 1.12, 'Paddington': 1.15, 'Double Bay': 1.3, 'Neutral Bay': 1.05, 'Kirribilli': 1.12, 'Lane Cove': 0.92, 'Hornsby': 0.78, 'Cronulla': 0.9, 'Ryde': 0.82
            },
            'Melbourne': {
                'CBD': 1.20, 'South Yarra': 1.22, 'Fitzroy': 1.10,
                'Carlton': 1.05, 'St Kilda': 1.08, 'Collingwood': 1.02,
                'Richmond': 0.98, 'Brunswick': 0.92, 'Footscray': 0.78,
                'Docklands': 1.12, 'Toorak': 1.30, 'Prahran': 1.08,
                'Albert Park': 1.15, 'Northcote': 1.02, 'Thornbury': 0.95, 'Preston': 0.82, 'Caulfield': 1.0, 'Malvern': 1.15, 'Box Hill': 0.82, 'Camberwell': 1.05, 'Brighton': 1.22, 'Hawthorn': 1.08, 'Kew': 1.12, 'Sunshine': 0.72
            },
            'Perth': {
                'CBD': 1.18, 'Subiaco': 1.15, 'Cottesloe': 1.22,
                'Claremont': 1.12, 'Fremantle': 1.05, 'Leederville': 1.08,
                'Mount Lawley': 1.02, 'Northbridge': 0.95, 'Scarborough': 0.90,
                'Rockingham': 0.78, 'Joondalup': 0.82, 'Nedlands': 1.10,
                'Victoria Park': 1.0, 'South Perth': 1.1, 'Applecross': 1.15, 'Dalkeith': 1.25, 'Morley': 0.85, 'Cannington': 0.8, 'Armadale': 0.72, 'Innaloo': 0.85, 'Midland': 0.72, 'Karrinyup': 0.92
            },
            'Auckland': {
                'Ponsonby': 1.25, 'Parnell': 1.22, 'Herne Bay': 1.30,
                'Grey Lynn': 1.15, 'CBD': 1.12, 'Newmarket': 1.08,
                'Mt Eden': 1.05, 'Kingsland': 1.02, 'Devonport': 1.10,
                'Henderson': 0.78, 'Manukau': 0.72, 'Takapuna': 0.95,
                'Remuera': 1.18, 'Mission Bay': 1.15, 'Onehunga': 0.85, 'Mt Albert': 0.92, 'Epsom': 1.05, 'Botany': 0.8, 'Albany': 0.82, 'Howick': 0.85, 'Titirangi': 0.88, 'St Heliers': 1.08
            },

            # ===== MIDDLE EAST =====
            'Dubai': {
                'Downtown Dubai': 1.35, 'Dubai Marina': 1.28, 'Palm Jumeirah': 1.40,
                'JBR': 1.22, 'Business Bay': 1.18, 'DIFC': 1.30,
                'JLT': 1.05, 'Deira': 0.78, 'Al Barsha': 0.88,
                'Jumeirah': 1.15, 'Silicon Oasis': 0.72, 'Sports City': 0.80,
                'Arabian Ranches': 1.08, 'The Greens': 0.95, 'Discovery Gardens': 0.72, 'International City': 0.65, 'Mirdif': 0.85, 'Al Nahda': 0.78, 'Jumeirah Village Circle': 0.82, 'Damac Hills': 0.9, 'City Walk': 1.22, 'Dubai Hills': 1.1, 'Al Quoz': 0.75, 'Motor City': 0.78
            },
            'Abu Dhabi': {
                'Al Reem Island': 1.22, 'Saadiyat Island': 1.30, 'Corniche': 1.25,
                'Al Raha Beach': 1.15, 'Yas Island': 1.12, 'Khalifa City': 0.88,
                'Mussafah': 0.72, 'Al Khalidiya': 1.08, 'Tourist Club Area': 0.92,
                'Al Ain': 0.78,
                'Al Maryah Island': 1.22, 'Al Bateen': 1.15, 'Al Mushrif': 0.95, 'Al Shamkha': 0.72, 'Mohamed Bin Zayed City': 0.78, 'Al Reef': 0.82, 'Al Ghadeer': 0.8, 'Masdar City': 0.92, 'Al Ruwais': 0.68
            },
            'Doha': {
                'The Pearl': 1.35, 'West Bay': 1.28, 'Katara': 1.22,
                'Al Sadd': 1.05, 'Souq Waqif': 1.10, 'Lusail': 1.18,
                'Al Rayyan': 0.85, 'Al Wakrah': 0.78, 'Al Gharrafa': 0.82,
                'Industrial Area': 0.65,
                'Musheireb': 1.12, 'Al Dafna': 1.22, 'Ain Khaled': 0.88, 'Al Thumama': 0.82, 'Umm Salal': 0.75, 'Al Kheesa': 0.78, 'Duhail': 0.85, 'Education City': 1.05
            },
            'Riyadh': {
                'Al Olaya': 1.28, 'King Abdullah Financial District': 1.30, 'Al Nakheel': 1.18,
                'Diplomatic Quarter': 1.22, 'Al Malqa': 1.12, 'Al Yasmin': 1.05,
                'Al Sulimaniyah': 0.95, 'Al Batha': 0.72, 'Al Khaleej': 0.82,
                'Al Thumama': 0.88,
                'Al Muhammadiyah': 1.05, 'Al Rawdah': 1.08, 'Hittin': 1.15, 'Al Narjis': 0.92, 'Al Izdihar': 0.88, 'Al Aqiq': 1.0, 'Al Wadi': 0.82, 'King Fahad Road': 1.12, 'Al Shifa': 0.75
            },
            'Tel Aviv': {
                'Rothschild Blvd': 1.35, 'Neve Tzedek': 1.30, 'Florentin': 1.10,
                'Old North': 1.20, 'Sarona': 1.18, 'Jaffa': 0.95,
                'Ramat Aviv': 1.12, 'Bat Yam': 0.78, 'Holon': 0.75,
                'Givatayim': 0.92,
                "Lev Ha'ir (City Centre)": 1.25, 'Kerem HaTeimanim': 1.15, 'Shapira': 0.82, 'Yad Eliyahu': 0.88, 'Ramat HaHayal': 1.08, 'Bavli': 1.12, 'Kiryat Shalom': 0.78, 'Herzliya Pituach': 1.28, 'Bnei Brak': 0.72
            },

            # ===== AFRICA =====
            'Cape Town': {
                'Camps Bay': 1.35, 'Clifton': 1.40, 'Sea Point': 1.18,
                'City Bowl': 1.15, 'Green Point': 1.12, 'Woodstock': 0.92,
                'Observatory': 0.88, 'Rondebosch': 0.95, 'Claremont': 1.02,
                'Khayelitsha': 0.55, 'Mitchell\'s Plain': 0.60,
                'Constantia': 1.22, 'Newlands': 1.1, 'Hout Bay': 1.05, 'Muizenberg': 0.82, 'Fish Hoek': 0.78, 'Bloubergstrand': 0.85, 'Table View': 0.8, 'Stellenbosch': 0.92, 'Gardens': 1.12, 'Tamboerskloof': 1.08
            },
            'Nairobi': {
                'Westlands': 1.25, 'Karen': 1.22, 'Kilimani': 1.18,
                'Lavington': 1.15, 'Runda': 1.28, 'Kileleshwa': 1.10,
                'Upper Hill': 1.08, 'South B': 0.88, 'Eastleigh': 0.72,
                'Kibera': 0.55, 'Lang\'ata': 0.95,
                'Muthaiga': 1.2, 'Spring Valley': 1.12, 'Hurlingham': 1.08, 'Parklands': 0.92, 'Gigiri': 1.15, 'Kayole': 0.62, 'Donholm': 0.75, 'Kasarani': 0.72, 'Kitisuru': 1.1
            },
            'Lagos': {
                'Victoria Island': 1.35, 'Ikoyi': 1.30, 'Lekki Phase 1': 1.22,
                'Banana Island': 1.45, 'Yaba': 0.88, 'Surulere': 0.82,
                'Ikeja': 0.90, 'Ajah': 0.78, 'Oshodi': 0.68,
                'Maryland': 0.85, 'Gbagada': 0.92,
                'Lekki Phase 2': 1.08, 'Magodo': 0.95, 'Festac Town': 0.72, 'Ilupeju': 0.82, 'Agege': 0.65, 'Amuwo-Odofin': 0.78, 'Ogudu': 0.82, 'Sangotedo': 0.75, 'Chevron Drive': 1.12
            },
            'Cairo': {
                'Zamalek': 1.35, 'Garden City': 1.28, 'Maadi': 1.18,
                'Heliopolis': 1.08, 'New Cairo (5th Settlement)': 1.15, '6th of October City': 0.85,
                'Dokki': 1.02, 'Mohandessin': 0.95, 'Nasr City': 0.82,
                'Shubra': 0.72, 'Downtown': 0.90,
                'Rehab City': 1.1, 'Sheikh Zayed City': 1.05, 'Katameya': 1.12, 'Obour City': 0.78, 'Al Shorouk': 0.82, 'Corniche El Nil': 1.05, 'Hadayek El Maadi': 1.02, 'Ain Shams': 0.68, 'El Marg': 0.65
            },
            'Marrakech': {
                'Gueliz': 1.18, 'Hivernage': 1.25, 'Medina (Riads)': 1.15,
                'Palmeraie': 1.30, 'Agdal': 1.08, 'Targa': 1.02,
                'Massira': 0.78, 'Sidi Youssef Ben Ali': 0.72, 'Menara': 0.88,
                'Amelkis': 1.12,
                'Route de Fès': 0.82, 'Route de Ouarzazate': 0.75, 'Tamesna': 0.7, 'Sidi Ghanem': 0.92, 'Bab Doukkala': 0.95, 'Route de Casablanca': 0.8, "M'hamid": 0.82
            },
            'Casablanca': {
                'Corniche (Ain Diab)': 1.25, 'Maarif': 1.15, 'Anfa': 1.22,
                'Gauthier': 1.12, 'Bourgogne': 1.08, 'Racine': 1.05,
                'Sidi Moumen': 0.68, 'Hay Hassani': 0.78, 'Derb Sultan': 0.82,
                'CIL': 0.88,
                'Dar Bouazza': 0.85, 'Oulfa': 0.72, 'Oasis': 1.02, 'Palmier': 0.95, "Triangle d'Or": 1.18, 'Ain Chock': 0.75, 'Sidi Bernoussi': 0.68, 'Ain Sebaa': 0.78
            },

            # ===== SOUTH AMERICA =====
            'São Paulo': {
                'Jardins': 1.30, 'Vila Madalena': 1.15, 'Pinheiros': 1.18,
                'Itaim Bibi': 1.25, 'Vila Olímpia': 1.20, 'Moema': 1.12,
                'Centro': 0.78, 'Liberdade': 0.85, 'Bela Vista': 0.92,
                'Santana': 0.82, 'Tatuapé': 0.80,
                'Brooklin': 1.18, 'Perdizes': 1.1, 'Alto de Pinheiros': 1.22, 'Consolação': 1.02, 'Higienópolis': 1.2, 'Butantã': 0.85, 'Morumbi': 1.15, 'Campo Belo': 1.08, 'Paraíso': 1.05, 'Lapa': 0.88, 'Ipiranga': 0.78, 'Vila Mariana': 1.02, 'Aclimação': 0.92
            },
            'Buenos Aires': {
                'Palermo (Soho)': 1.25, 'Recoleta': 1.28, 'Puerto Madero': 1.35,
                'San Telmo': 1.02, 'Belgrano': 1.10, 'Núñez': 1.05,
                'Caballito': 0.88, 'Almagro': 0.85, 'Flores': 0.75,
                'Villa Crespo': 0.92, 'Colegiales': 1.02,
                'La Boca': 0.78, 'Palermo Hollywood': 1.18, 'Montserrat': 0.88, 'Retiro': 1.02, 'Barrio Norte': 1.15, 'Balvanera': 0.82, 'Chacarita': 0.88, 'Saavedra': 0.82, 'Villa Devoto': 0.8, 'Palermo Chico': 1.3, 'Olivos': 1.05, 'Vicente López': 1.02
            },
            'Bogotá': {
                'Zona T (Zona Rosa)': 1.25, 'Usaquén': 1.22, 'Chicó': 1.20,
                'Chapinero Alto': 1.12, 'La Candelaria': 0.88, 'Cedritos': 1.02,
                'Suba': 0.82, 'Kennedy': 0.72, 'Teusaquillo': 0.95,
                'Santa Bárbara': 1.15,
                'Rosales': 1.18, 'El Virrey': 1.15, 'Galerías': 0.92, 'La Soledad': 0.88, 'La Macarena': 0.95, 'Niza': 1.02, 'Engativá': 0.75, 'Fontibón': 0.78, 'Modelia': 0.88
            },
            'Lima': {
                'Miraflores': 1.28, 'San Isidro': 1.30, 'Barranco': 1.15,
                'Surco': 1.08, 'La Molina': 1.05, 'San Borja': 1.02,
                'Jesús María': 0.90, 'Lince': 0.85, 'San Juan de Lurigancho': 0.68,
                'Callao': 0.72,
                'Pueblo Libre': 0.88, 'Magdalena': 0.92, 'San Miguel': 0.85, 'La Victoria': 0.72, 'Chorrillos': 0.78, 'Surquillo': 0.82, 'Ate': 0.72, 'Comas': 0.65, 'Los Olivos': 0.75
            },
            'Santiago': {
                'Providencia': 1.22, 'Las Condes': 1.25, 'Vitacura': 1.35,
                'Ñuñoa': 1.08, 'La Reina': 1.05, 'Santiago Centro': 0.92,
                'Lo Barnechea': 1.18, 'Macul': 0.82, 'La Florida': 0.78,
                'Puente Alto': 0.70,
                'Peñalolén': 0.85, 'San Miguel': 0.78, 'Recoleta': 0.72, 'Maipú': 0.7, 'Independencia': 0.75, 'Pedro de Valdivia': 1.15, 'El Golf': 1.22, 'Tobalaba': 1.02, 'Bellavista': 1.0
            },
            'Medellín': {
                'El Poblado': 1.30, 'Laureles': 1.12, 'Envigado': 1.08,
                'Sabaneta': 0.95, 'Belén': 0.88, 'La Floresta': 1.02,
                'Centro': 0.78, 'Robledo': 0.75, 'Aranjuez': 0.72,
                'Estadio': 0.85,
                'Manila': 1.05, 'San Lucas': 1.18, 'La Estrella': 0.82, 'Itagüí': 0.78, 'Bello': 0.72, 'Calasanz': 0.8, 'Castropol': 1.08, 'Boston': 0.75, 'Provenza': 1.15
            },
            'Montevideo': {
                'Pocitos': 1.22, 'Punta Carretas': 1.25, 'Carrasco': 1.30,
                'Ciudad Vieja': 1.08, 'Parque Rodó': 1.05, 'Buceo': 1.02,
                'Cordón': 0.92, 'Tres Cruces': 0.88, 'La Blanqueada': 0.85,
                'Cerro': 0.70,
                'Malvín': 1.0, 'Parque Batlle': 0.95, 'Paso Molino': 0.78, 'La Comercial': 0.82, 'Prado': 0.85, 'Aguada': 0.75, 'Unión': 0.72, 'Punta Gorda': 1.12
            },
            'San José (CR)': {
                'Escazú': 1.28, 'Santa Ana': 1.22, 'Rohrmoser': 1.12,
                'Los Yoses': 1.08, 'Barrio Escalante': 1.10, 'San Pedro': 0.92,
                'Sabana': 1.05, 'Heredia': 0.85, 'Alajuela': 0.78,
                'Cartago': 0.75,
                'Curridabat': 0.92, 'Moravia': 0.85, 'Tibás': 0.78, 'Desamparados': 0.72, 'Montes de Oca': 0.9, 'San Rafael': 0.82, 'Guadalupe': 0.78, 'Zapote': 0.85
            },
            'Playa del Carmen': {
                'Playacar': 1.30, 'Centro (5th Avenue)': 1.18, 'Gonzalo Guerrero': 1.05,
                'Ejidal': 0.82, 'Colosio': 0.78, 'Playa Mamitas': 1.22,
                'Zazil Ha': 0.88, 'Luis Donaldo Colosio': 0.75,
                'Villas del Sol': 0.72,
                'Selvanova': 0.85, 'Real Ibiza': 0.68, 'Riviera Maya Zona': 1.15, 'Puerto Aventuras': 1.1, 'Mayakoba Area': 1.25, 'Playa Paraíso': 1.08, 'La Guadalupana': 0.72
            }
        }

# City to region mapping for organization
cityRegions = {
    'North America': ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Miami', 'Austin',
                      'Seattle', 'Denver', 'Boston', 'Washington DC', 'Houston',
                      'Charlotte', 'Las Vegas', 'Tampa', 'Raleigh',
                      'Dallas', 'Atlanta', 'Philadelphia', 'Phoenix',
                      'San Diego', 'Nashville', 'Minneapolis', 'Portland',
                      'Toronto', 'Vancouver', 'Montreal', 'Mexico City', 'Cancún', 'Panama City'],
    'Western Europe': ['London', 'Paris', 'Amsterdam', 'Berlin', 'Munich', 'Dublin', 'Brussels',
                       'Luxembourg City', 'Zurich', 'Geneva', 'Edinburgh', 'Nice'],
    'Southern Europe': ['Madrid', 'Barcelona', 'Valencia', 'Málaga', 'Lisbon', 'Porto', 'Rome',
                        'Milan', 'Athens', 'Split'],
    'Northern Europe': ['Stockholm', 'Copenhagen', 'Helsinki', 'Oslo', 'Vienna'],
    'Eastern Europe': ['Prague', 'Budapest', 'Warsaw', 'Krakow', 'Bucharest', 'Tallinn', 'Riga', 'Istanbul'],
    'East Asia': ['Tokyo', 'Osaka', 'Fukuoka', 'Seoul', 'Hong Kong', 'Taipei', 'Shanghai', 'Beijing', 'Shenzhen', 'Guangzhou'],
    'Southeast Asia': ['Singapore', 'Bangkok', 'Chiang Mai', 'Phuket', 'Kuala Lumpur',
                       'Ho Chi Minh City', 'Hanoi', 'Manila', 'Jakarta', 'Bali (Denpasar)', 'Phnom Penh'],
    'South Asia': ['Mumbai', 'Bangalore', 'Delhi', 'Chennai'],
    'Oceania': ['Sydney', 'Melbourne', 'Perth', 'Auckland'],
    'Middle East': ['Dubai', 'Abu Dhabi', 'Doha', 'Riyadh', 'Tel Aviv'],
    'Africa': ['Cape Town', 'Nairobi', 'Lagos', 'Cairo', 'Marrakech', 'Casablanca'],
    'South America': ['São Paulo', 'Buenos Aires', 'Bogotá', 'Lima', 'Santiago', 'Medellín',
                      'Montevideo', 'San José (CR)', 'Playa del Carmen']
}

# City to country mapping
cityCountry = {
    'New York': 'United States', 'San Francisco': 'United States', 'Los Angeles': 'United States',
    'Chicago': 'United States', 'Miami': 'United States', 'Austin': 'United States',
    'Seattle': 'United States', 'Denver': 'United States', 'Boston': 'United States',
    'Washington DC': 'United States', 'Houston': 'United States',
    'Charlotte': 'United States', 'Las Vegas': 'United States',
    'Tampa': 'United States', 'Raleigh': 'United States',
    'Dallas': 'United States', 'Atlanta': 'United States',
    'Philadelphia': 'United States', 'Phoenix': 'United States',
    'San Diego': 'United States', 'Nashville': 'United States',
    'Minneapolis': 'United States', 'Portland': 'United States',
    'Toronto': 'Canada', 'Vancouver': 'Canada', 'Montreal': 'Canada',
    'Mexico City': 'Mexico', 'Cancún': 'Mexico', 'Panama City': 'Panama',
    'London': 'United Kingdom', 'Edinburgh': 'United Kingdom',
    'Paris': 'France', 'Nice': 'France',
    'Amsterdam': 'Netherlands', 'Berlin': 'Germany', 'Munich': 'Germany',
    'Dublin': 'Ireland', 'Brussels': 'Belgium', 'Luxembourg City': 'Luxembourg',
    'Zurich': 'Switzerland', 'Geneva': 'Switzerland',
    'Madrid': 'Spain', 'Barcelona': 'Spain', 'Valencia': 'Spain', 'Málaga': 'Spain',
    'Lisbon': 'Portugal', 'Porto': 'Portugal',
    'Rome': 'Italy', 'Milan': 'Italy',
    'Athens': 'Greece', 'Split': 'Croatia',
    'Stockholm': 'Sweden', 'Copenhagen': 'Denmark', 'Helsinki': 'Finland',
    'Oslo': 'Norway', 'Vienna': 'Austria',
    'Prague': 'Czech Republic', 'Budapest': 'Hungary', 'Warsaw': 'Poland', 'Krakow': 'Poland',
    'Bucharest': 'Romania', 'Tallinn': 'Estonia', 'Riga': 'Latvia', 'Istanbul': 'Turkey',
    'Tokyo': 'Japan', 'Osaka': 'Japan', 'Fukuoka': 'Japan',
    'Seoul': 'South Korea', 'Hong Kong': 'China (SAR)', 'Taipei': 'Taiwan',
    'Shanghai': 'China', 'Beijing': 'China', 'Shenzhen': 'China', 'Guangzhou': 'China',
    'Singapore': 'Singapore', 'Bangkok': 'Thailand', 'Chiang Mai': 'Thailand', 'Phuket': 'Thailand',
    'Kuala Lumpur': 'Malaysia', 'Ho Chi Minh City': 'Vietnam', 'Hanoi': 'Vietnam',
    'Manila': 'Philippines', 'Jakarta': 'Indonesia', 'Bali (Denpasar)': 'Indonesia',
    'Phnom Penh': 'Cambodia',
    'Mumbai': 'India', 'Bangalore': 'India', 'Delhi': 'India', 'Chennai': 'India',
    'Sydney': 'Australia', 'Melbourne': 'Australia', 'Perth': 'Australia', 'Auckland': 'New Zealand',
    'Dubai': 'UAE', 'Abu Dhabi': 'UAE', 'Doha': 'Qatar', 'Riyadh': 'Saudi Arabia', 'Tel Aviv': 'Israel',
    'Cape Town': 'South Africa', 'Nairobi': 'Kenya', 'Lagos': 'Nigeria',
    'Cairo': 'Egypt', 'Marrakech': 'Morocco', 'Casablanca': 'Morocco',
    'São Paulo': 'Brazil', 'Buenos Aires': 'Argentina',
    'Bogotá': 'Colombia', 'Medellín': 'Colombia',
    'Lima': 'Peru', 'Santiago': 'Chile', 'Montevideo': 'Uruguay',
    'San José (CR)': 'Costa Rica', 'Playa del Carmen': 'Mexico'
}

# Progressive income tax brackets by country [[upperBound, marginalRate%], ...]
# Brackets in local currency, annual. Tax computed progressively on each slice.
taxBrackets = {
    # Tax-free
    'UAE': [], 'Qatar': [], 'Saudi Arabia': [], 'Cambodia': [],
    # Americas
    'United States': [[11600,10],[47150,12],[100525,22],[191950,24],[243725,32],[609350,35],[float('inf'),37]],
    'Canada': [[55867,15],[111733,20.5],[154906,26],[220000,29],[float('inf'),33]],
    'Mexico': [[8952,1.92],[75985,6.4],[133536,10.88],[155230,16],[185853,17.92],[374838,21.36],[590797,23.52],[1127927,30],[1503902,32],[4511707,34],[float('inf'),35]],
    'Panama': [[11000,0],[50000,15],[float('inf'),25]],
    'Brazil': [[24512,0],[33920,7.5],[45013,15],[55976,22.5],[float('inf'),27.5]],
    'Argentina': [[419254,5],[838508,9],[1257762,12],[1677016,15],[2516524,19],[3356032,23],[5034048,27],[6712063,31],[float('inf'),35]],
    'Colombia': [[46229000,0],[72066000,19],[163386000,28],[368076000,33],[624096000,35],[969456000,37],[float('inf'),39]],
    'Peru': [[29050,0],[54250,8],[81375,14],[116250,17],[232500,20],[float('inf'),30]],
    'Chile': [[8775702,0],[19501560,4],[32502600,8],[45503640,13.5],[58504680,23],[78006240,30.4],[101508120,35],[float('inf'),40]],
    'Uruguay': [[468720,0],[670320,10],[1005480,15],[1536000,24],[2421600,25],[3643200,27],[5685600,31],[float('inf'),36]],
    'Costa Rica': [[11160000,0],[16380000,10],[float('inf'),15]],
    # UK
    'United Kingdom': [[12570,0],[50270,20],[125140,40],[float('inf'),45]],
    # Europe
    'France': [[11294,0],[28797,11],[82341,30],[177106,41],[float('inf'),45]],
    'Netherlands': [[38098,9.32],[75518,36.97],[float('inf'),49.50]],
    'Germany': [[11604,0],[17005,14],[66760,24],[277826,42],[float('inf'),45]],
    'Ireland': [[42000,20],[float('inf'),40]],
    'Belgium': [[15200,0],[28730,25],[40580,40],[float('inf'),50]],
    'Luxembourg': [[11265,0],[25000,14],[50000,30],[100000,38],[200000,41],[float('inf'),42]],
    'Switzerland': [[14500,0],[50000,10],[100000,16],[200000,22],[float('inf'),22]],
    'Spain': [[12450,19],[20200,24],[35200,30],[60000,37],[300000,45],[float('inf'),47]],
    'Portugal': [[7703,13.25],[11623,18],[16472,23],[21321,26],[27146,32.75],[39791,37],[51997,43.5],[81199,45],[float('inf'),48]],
    'Italy': [[15000,23],[28000,25],[50000,35],[float('inf'),43]],
    'Greece': [[10000,9],[20000,22],[30000,28],[40000,36],[float('inf'),44]],
    'Croatia': [[50400,20],[float('inf'),30]],
    'Sweden': [[614942,32],[float('inf'),52]],
    'Denmark': [[46700,0],[588900,37],[float('inf'),52]],
    'Finland': [[19900,0],[29700,32.64],[49000,37.4],[85800,41.25],[float('inf'),51.25]],
    'Norway': [[198350,22],[279150,23.7],[642950,26],[926800,35.4],[1500000,38.4],[float('inf'),39.4]],
    'Austria': [[12816,0],[21816,20],[35016,30],[68016,40],[103816,48],[1000000,50],[float('inf'),55]],
    'Czech Republic': [[1935552,15],[float('inf'),23]],
    'Hungary': [[float('inf'),15]],
    'Poland': [[30000,0],[120000,12],[float('inf'),32]],
    'Romania': [[float('inf'),10]],
    'Estonia': [[7848,0],[float('inf'),20]],
    'Latvia': [[20004,20],[78100,23],[float('inf'),31]],
    'Turkey': [[110000,15],[230000,20],[580000,27],[3000000,35],[float('inf'),40]],
    # Asia
    'Japan': [[1950000,5],[3300000,10],[6950000,20],[9000000,23],[18000000,33],[40000000,40],[float('inf'),45]],
    'South Korea': [[14000000,6],[50000000,15],[88000000,24],[150000000,35],[300000000,38],[500000000,40],[1000000000,42],[float('inf'),45]],
    'China (SAR)': [[50000,2],[100000,6],[150000,10],[200000,14],[float('inf'),17]],
    'Taiwan': [[560000,5],[1260000,12],[2520000,20],[4720000,30],[float('inf'),40]],
    'China': [[36000,3],[144000,10],[300000,20],[420000,25],[660000,30],[960000,35],[float('inf'),45]],
    'Singapore': [[20000,0],[30000,2],[40000,3.5],[80000,7],[120000,11.5],[160000,15],[200000,18],[240000,19],[280000,19.5],[320000,20],[500000,22],[1000000,23],[float('inf'),24]],
    'Thailand': [[150000,0],[300000,5],[500000,10],[750000,15],[1000000,20],[2000000,25],[5000000,30],[float('inf'),35]],
    'Malaysia': [[5000,0],[20000,1],[35000,3],[50000,6],[70000,11],[100000,19],[400000,25],[600000,26],[2000000,28],[float('inf'),30]],
    'Vietnam': [[60000000,5],[120000000,10],[216000000,15],[384000000,20],[624000000,25],[960000000,30],[float('inf'),35]],
    'Philippines': [[250000,0],[400000,15],[800000,20],[2000000,25],[8000000,30],[float('inf'),35]],
    'Indonesia': [[60000000,5],[250000000,15],[500000000,25],[5000000000,30],[float('inf'),35]],
    'India': [[300000,0],[700000,5],[1000000,10],[1200000,15],[1500000,20],[float('inf'),30]],
    # Oceania
    'Australia': [[18200,0],[45000,16],[135000,30],[190000,37],[float('inf'),45]],
    'New Zealand': [[14000,10.5],[48000,17.5],[70000,30],[180000,33],[float('inf'),39]],
    # Middle East & Africa
    'Israel': [[84120,10],[120720,14],[193800,20],[269280,31],[560280,35],[721560,47],[float('inf'),50]],
    'South Africa': [[237100,18],[370500,26],[512800,31],[673000,36],[857900,39],[1817000,41],[float('inf'),45]],
    'Kenya': [[288000,10],[388000,25],[6000000,30],[9600000,32.5],[float('inf'),35]],
    'Nigeria': [[300000,7],[600000,11],[1100000,15],[1600000,19],[3200000,21],[float('inf'),24]],
    'Egypt': [[40000,0],[55000,10],[70000,15],[200000,20],[400000,22.5],[float('inf'),25]],
    'Morocco': [[30000,0],[50000,10],[60000,20],[80000,30],[180000,34],[float('inf'),38]],
}


def calculate_tax(income, country_name):
    """Calculate progressive tax. Returns dict with tax, effective_rate, net."""
    brackets = taxBrackets.get(country_name, [])
    if not brackets:
        return {'tax': 0, 'effective_rate': 0, 'net': income}
    tax, prev = 0, 0
    for limit, rate in brackets:
        if income <= prev:
            break
        tax += (min(income, limit) - prev) * (rate / 100)
        prev = limit
    effective_rate = round((tax / income) * 100) if income > 0 else 0
    return {'tax': tax, 'effective_rate': effective_rate, 'net': income - tax}

# Social security & mandatory deductions by country
# Each country: social_security = {local: %, expat: %, cap: amount_or_None, label: str}
# Optional: church_tax, solidarity, council_tax, etc.
countryDeductions = {
    # Tax-free / minimal
    'UAE': {},
    'Qatar': {},
    'Saudi Arabia': {'social_security': {'local': 9.75, 'expat': 0, 'cap': None, 'label': 'GOSI'}},
    'Cambodia': {},
    # Americas
    'United States': {
        'social_security': {'local': 7.65, 'expat': 7.65, 'cap': 168600, 'label': 'Social Security + Medicare (FICA)'},
    },
    'Canada': {
        'social_security': {'local': 6.8, 'expat': 0, 'cap': 68500, 'label': 'CPP + EI'},
    },
    'Mexico': {
        'social_security': {'local': 2.78, 'expat': 0, 'cap': None, 'label': 'IMSS'},
    },
    'Panama': {
        'social_security': {'local': 9.75, 'expat': 0, 'cap': None, 'label': 'CSS'},
    },
    'Brazil': {
        'social_security': {'local': 14, 'expat': 0, 'cap': 105432, 'label': 'INSS'},
    },
    'Argentina': {
        'social_security': {'local': 17, 'expat': 0, 'cap': None, 'label': 'Social Security'},
    },
    'Colombia': {
        'social_security': {'local': 8, 'expat': 0, 'cap': None, 'label': 'Health + Pension'},
    },
    'Peru': {
        'social_security': {'local': 13, 'expat': 0, 'cap': None, 'label': 'ONP/AFP + EsSalud'},
    },
    'Chile': {
        'social_security': {'local': 19.5, 'expat': 0, 'cap': None, 'label': 'AFP + Health + Unemployment'},
    },
    'Uruguay': {
        'social_security': {'local': 18.1, 'expat': 0, 'cap': None, 'label': 'BPS Contributions'},
    },
    'Costa Rica': {
        'social_security': {'local': 10.67, 'expat': 0, 'cap': None, 'label': 'CCSS + Worker Risks'},
    },
    # UK
    'United Kingdom': {
        'social_security': {'local': 8, 'expat': 0, 'cap': 50270, 'reduced_rate': 2, 'label': 'National Insurance (NI)'},
    },
    # Europe
    'France': {
        'social_security': {'local': 22, 'expat': 0, 'cap': None, 'label': 'Social Charges (CSG/CRDS)'},
    },
    'Netherlands': {
        'social_security': {'local': 27.65, 'expat': 0, 'cap': 38098, 'label': 'Social Premiums'},
    },
    'Germany': {
        'social_security': {'local': 20.2, 'expat': 20.2, 'cap': 90600, 'label': 'Social Security (Pension+Health+Unemp+Care)'},
        'solidarity': {'rate': 5.5, 'of': 'income_tax', 'label': 'Solidarity Surcharge'},
    },
    'Ireland': {
        'social_security': {'local': 4, 'expat': 0, 'cap': None, 'label': 'PRSI'},
    },
    'Belgium': {
        'social_security': {'local': 13.07, 'expat': 0, 'cap': None, 'label': 'Social Security'},
    },
    'Luxembourg': {
        'social_security': {'local': 12.45, 'expat': 12.45, 'cap': None, 'label': 'Social Security'},
    },
    'Switzerland': {
        'social_security': {'local': 6.4, 'expat': 6.4, 'cap': None, 'label': 'AHV/IV/EO + ALV'},
    },
    'Spain': {
        'social_security': {'local': 6.35, 'expat': 0, 'cap': 56646, 'label': 'Social Security'},
    },
    'Portugal': {
        'social_security': {'local': 11, 'expat': 0, 'cap': None, 'label': 'Social Security'},
    },
    'Italy': {
        'social_security': {'local': 9.19, 'expat': 0, 'cap': 119650, 'label': 'INPS Contributions'},
    },
    'Greece': {
        'social_security': {'local': 13.87, 'expat': 0, 'cap': None, 'label': 'Social Insurance'},
    },
    'Croatia': {
        'social_security': {'local': 20, 'expat': 0, 'cap': None, 'label': 'Pension + Health'},
    },
    'Sweden': {
        'social_security': {'local': 7, 'expat': 0, 'cap': None, 'label': 'Employee Social Fees'},
    },
    'Denmark': {
        'social_security': {'local': 8, 'expat': 0, 'cap': None, 'label': 'AM-bidrag + ATP'},
    },
    'Finland': {
        'social_security': {'local': 10.5, 'expat': 0, 'cap': None, 'label': 'Pension + Unemployment + Health'},
    },
    'Norway': {
        'social_security': {'local': 7.8, 'expat': 0, 'cap': None, 'label': 'Trygdeavgift'},
    },
    'Austria': {
        'social_security': {'local': 18.07, 'expat': 0, 'cap': 78660, 'label': 'Social Security'},
    },
    'Czech Republic': {
        'social_security': {'local': 11, 'expat': 0, 'cap': None, 'label': 'Social + Health Insurance'},
    },
    'Hungary': {
        'social_security': {'local': 18.5, 'expat': 0, 'cap': None, 'label': 'Social Contribution (TB)'},
    },
    'Poland': {
        'social_security': {'local': 13.71, 'expat': 0, 'cap': None, 'label': 'ZUS Contributions'},
    },
    'Romania': {
        'social_security': {'local': 35, 'expat': 0, 'cap': None, 'label': 'CAS + CASS'},
    },
    'Estonia': {
        'social_security': {'local': 1.6, 'expat': 0, 'cap': None, 'label': 'Unemployment Insurance'},
    },
    'Latvia': {
        'social_security': {'local': 10.5, 'expat': 0, 'cap': None, 'label': 'Social Security'},
    },
    'Turkey': {
        'social_security': {'local': 15, 'expat': 0, 'cap': None, 'label': 'SSI + Unemployment'},
    },
    # Asia
    'Japan': {
        'social_security': {'local': 14.75, 'expat': 14.75, 'cap': None, 'label': 'Health + Pension + Employment'},
    },
    'South Korea': {
        'social_security': {'local': 9.4, 'expat': 0, 'cap': None, 'label': 'NPS + Health + Employment'},
    },
    'China (SAR)': {
        'social_security': {'local': 5, 'expat': 0, 'cap': 18000, 'label': 'MPF'},
    },
    'Taiwan': {
        'social_security': {'local': 5.17, 'expat': 0, 'cap': None, 'label': 'Labor + Health Insurance'},
    },
    'China': {
        'social_security': {'local': 22.5, 'expat': 0, 'cap': None, 'label': 'Five Insurances + Housing Fund'},
    },
    'Singapore': {
        'social_security': {'local': 20, 'expat': 0, 'cap': 102000, 'label': 'CPF (Employee Share)'},
    },
    'Thailand': {
        'social_security': {'local': 5, 'expat': 0, 'cap': 180000, 'label': 'Social Security'},
    },
    'Malaysia': {
        'social_security': {'local': 11, 'expat': 0, 'cap': None, 'label': 'EPF'},
    },
    'Vietnam': {
        'social_security': {'local': 10.5, 'expat': 0, 'cap': None, 'label': 'Social + Health + Unemployment'},
    },
    'Philippines': {
        'social_security': {'local': 5, 'expat': 0, 'cap': None, 'label': 'SSS + PhilHealth + Pag-IBIG'},
    },
    'Indonesia': {
        'social_security': {'local': 5, 'expat': 0, 'cap': None, 'label': 'BPJS (Health + Employment)'},
    },
    'India': {
        'social_security': {'local': 12, 'expat': 0, 'cap': 180000, 'label': 'PF + ESI'},
    },
    # Oceania
    'Australia': {},  # Super is employer-paid, no employee deduction
    'New Zealand': {
        'social_security': {'local': 3, 'expat': 0, 'cap': None, 'label': 'KiwiSaver (default)'},
    },
    # Middle East & Africa
    'Israel': {
        'social_security': {'local': 12, 'expat': 0, 'cap': None, 'label': 'National Insurance + Health'},
    },
    'South Africa': {
        'social_security': {'local': 1, 'expat': 0, 'cap': 17712, 'label': 'UIF'},
    },
    'Kenya': {
        'social_security': {'local': 6, 'expat': 0, 'cap': None, 'label': 'NSSF + NHIF + Housing Levy'},
    },
    'Nigeria': {
        'social_security': {'local': 8, 'expat': 0, 'cap': None, 'label': 'Pension + NHF'},
    },
    'Egypt': {
        'social_security': {'local': 11, 'expat': 0, 'cap': None, 'label': 'Social Insurance'},
    },
    'Morocco': {
        'social_security': {'local': 6.29, 'expat': 0, 'cap': None, 'label': 'CNSS'},
    },
}

# City-level deduction overrides (state/provincial/cantonal taxes, council tax, etc.)
cityDeductions = {
    # US state+city income tax (effective mid-range rates)
    'New York': {'state_tax': {'rate': 10.3, 'label': 'State + City Income Tax (NY)'}},
    'San Francisco': {'state_tax': {'rate': 9.3, 'label': 'State Income Tax (CA)'}},
    'Los Angeles': {'state_tax': {'rate': 9.3, 'label': 'State Income Tax (CA)'}},
    'Chicago': {'state_tax': {'rate': 4.95, 'label': 'State Income Tax (IL)'}},
    'Austin': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (TX)'}},
    'Miami': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (FL)'}},
    'Seattle': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (WA)'}},
    'Denver': {'state_tax': {'rate': 4.4, 'label': 'State Income Tax (CO)'}},
    'Boston': {'state_tax': {'rate': 9.0, 'label': 'State Income Tax (MA)'}},
    'Washington DC': {'state_tax': {'rate': 8.5, 'label': 'District Income Tax (DC)'}},
    'Houston': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (TX)'}},
    'Charlotte': {'state_tax': {'rate': 4.5, 'label': 'State Income Tax (NC)'}},
    'Las Vegas': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (NV)'}},
    'Tampa': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (FL)'}},
    'Raleigh': {'state_tax': {'rate': 4.5, 'label': 'State Income Tax (NC)'}},
    'Dallas': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (TX)'}},
    'Atlanta': {'state_tax': {'rate': 5.49, 'label': 'State Income Tax (GA)'}},
    'Philadelphia': {'state_tax': {'rate': 3.07, 'label': 'State Income Tax (PA)'}},
    'Phoenix': {'state_tax': {'rate': 2.5, 'label': 'State Income Tax (AZ)'}},
    'San Diego': {'state_tax': {'rate': 9.3, 'label': 'State Income Tax (CA)'}},
    'Nashville': {'state_tax': {'rate': 0, 'label': 'No State Income Tax (TN)'}},
    'Minneapolis': {'state_tax': {'rate': 7.85, 'label': 'State Income Tax (MN)'}},
    'Portland': {'state_tax': {'rate': 9.9, 'label': 'State Income Tax (OR)'}},
    # Swiss cantonal+municipal tax (approximate effective rates for mid-range earners)
    'Zurich': {'cantonal_tax': {'rate': 22, 'label': 'Cantonal + Municipal Tax (Zürich)'}},
    'Geneva': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève)'}},
    # Canadian provincial tax
    'Toronto': {'provincial_tax': {'rate': 9.15, 'label': 'Provincial Tax (Ontario)'}},
    'Vancouver': {'provincial_tax': {'rate': 7.7, 'label': 'Provincial Tax (BC)'}},
    'Montreal': {'provincial_tax': {'rate': 15, 'label': 'Provincial Tax (Québec)'}},
    # German solidarity surcharge (city-level because it applies via income tax)
    'Berlin': {'solidarity': {'rate': 5.5, 'of': 'income_tax', 'label': 'Solidarity Surcharge'}},
    'Munich': {'solidarity': {'rate': 5.5, 'of': 'income_tax', 'label': 'Solidarity Surcharge'}},
    # UK council tax (average Band D)
    'London': {'council_tax': {'flat_annual': 1800, 'label': 'Council Tax (avg)'}},
    'Edinburgh': {'council_tax': {'flat_annual': 1500, 'label': 'Council Tax (avg)'}},
}

# Neighborhood-level deduction overrides (Tier 1: exact researched rates)
# Format: {city: {neighborhood: {deduction_key: {rate/flat_annual, label}}}}
neighborhoodDeductions = {
    # London boroughs — actual Band D council tax (2024/25 rates in GBP)
    'London': {
        'Mayfair': {'council_tax': {'flat_annual': 972, 'label': 'Council Tax (Westminster)'}},
        'Chelsea': {'council_tax': {'flat_annual': 972, 'label': 'Council Tax (Kensington & Chelsea)'}},
        'Kensington': {'council_tax': {'flat_annual': 972, 'label': 'Council Tax (Kensington & Chelsea)'}},
        'Soho': {'council_tax': {'flat_annual': 972, 'label': 'Council Tax (Westminster)'}},
        'Marylebone': {'council_tax': {'flat_annual': 972, 'label': 'Council Tax (Westminster)'}},
        'Notting Hill': {'council_tax': {'flat_annual': 972, 'label': 'Council Tax (Kensington & Chelsea)'}},
        'Shoreditch': {'council_tax': {'flat_annual': 1672, 'label': 'Council Tax (Hackney)'}},
        'Hackney': {'council_tax': {'flat_annual': 1672, 'label': 'Council Tax (Hackney)'}},
        'Camden': {'council_tax': {'flat_annual': 1942, 'label': 'Council Tax (Camden)'}},
        'Islington': {'council_tax': {'flat_annual': 1635, 'label': 'Council Tax (Islington)'}},
        'Brixton': {'council_tax': {'flat_annual': 1844, 'label': 'Council Tax (Lambeth)'}},
        'Peckham': {'council_tax': {'flat_annual': 1820, 'label': 'Council Tax (Southwark)'}},
        'Canary Wharf': {'council_tax': {'flat_annual': 1541, 'label': 'Council Tax (Tower Hamlets)'}},
        'Greenwich': {'council_tax': {'flat_annual': 1808, 'label': 'Council Tax (Greenwich)'}},
        'Clapham': {'council_tax': {'flat_annual': 1844, 'label': 'Council Tax (Lambeth)'}},
        'Stratford': {'council_tax': {'flat_annual': 1637, 'label': 'Council Tax (Newham)'}},
        'Hampstead': {'council_tax': {'flat_annual': 1942, 'label': 'Council Tax (Camden)'}},
        'Battersea': {'council_tax': {'flat_annual': 898, 'label': 'Council Tax (Wandsworth)'}},
        'Fulham': {'council_tax': {'flat_annual': 1375, 'label': 'Council Tax (Hammersmith & Fulham)'}},
        'Wimbledon': {'council_tax': {'flat_annual': 1694, 'label': 'Council Tax (Merton)'}},
        'Ealing': {'council_tax': {'flat_annual': 1765, 'label': 'Council Tax (Ealing)'}},
        'Dalston': {'council_tax': {'flat_annual': 1672, 'label': 'Council Tax (Hackney)'}},
        'Tooting': {'council_tax': {'flat_annual': 898, 'label': 'Council Tax (Wandsworth)'}},
        'Walthamstow': {'council_tax': {'flat_annual': 2050, 'label': 'Council Tax (Waltham Forest)'}},
        'Richmond': {'council_tax': {'flat_annual': 1994, 'label': 'Council Tax (Richmond)'}},
        'Putney': {'council_tax': {'flat_annual': 898, 'label': 'Council Tax (Wandsworth)'}},
        'Chiswick': {'council_tax': {'flat_annual': 1666, 'label': 'Council Tax (Hounslow)'}},
        'Balham': {'council_tax': {'flat_annual': 898, 'label': 'Council Tax (Wandsworth)'}},
        'Lewisham': {'council_tax': {'flat_annual': 1859, 'label': 'Council Tax (Lewisham)'}},
        'Croydon': {'council_tax': {'flat_annual': 2081, 'label': 'Council Tax (Croydon)'}},
        'Barking': {'council_tax': {'flat_annual': 1751, 'label': 'Council Tax (Barking & Dagenham)'}},
        'Angel (Islington)': {'council_tax': {'flat_annual': 1635, 'label': 'Council Tax (Islington)'}},
        'Vauxhall': {'council_tax': {'flat_annual': 1844, 'label': 'Council Tax (Lambeth)'}},
        'Bermondsey': {'council_tax': {'flat_annual': 1820, 'label': 'Council Tax (Southwark)'}},
        'Kentish Town': {'council_tax': {'flat_annual': 1942, 'label': 'Council Tax (Camden)'}},
    },
    # Geneva municipalities — effective cantonal + municipal tax rates
    'Geneva': {
        'Eaux-Vives': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève ville)'}},
        'Champel': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève ville)'}},
        'Carouge': {'cantonal_tax': {'rate': 25, 'label': 'Cantonal + Municipal Tax (Carouge)'}},
        'Plainpalais': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève ville)'}},
        'Pâquis': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève ville)'}},
        'Nations': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève ville)'}},
        'Servette': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève ville)'}},
        'Meyrin': {'cantonal_tax': {'rate': 27, 'label': 'Cantonal + Municipal Tax (Meyrin)'}},
        'Vernier': {'cantonal_tax': {'rate': 28, 'label': 'Cantonal + Municipal Tax (Vernier)'}},
        'Cologny': {'cantonal_tax': {'rate': 21, 'label': 'Cantonal + Municipal Tax (Cologny)'}},
        'Florissant': {'cantonal_tax': {'rate': 26, 'label': 'Cantonal + Municipal Tax (Genève ville)'}},
        'Grand-Saconnex': {'cantonal_tax': {'rate': 25, 'label': 'Cantonal + Municipal Tax (Grand-Saconnex)'}},
        'Lancy': {'cantonal_tax': {'rate': 27, 'label': 'Cantonal + Municipal Tax (Lancy)'}},
        'Onex': {'cantonal_tax': {'rate': 28, 'label': 'Cantonal + Municipal Tax (Onex)'}},
        'Thônex': {'cantonal_tax': {'rate': 27, 'label': 'Cantonal + Municipal Tax (Thônex)'}},
        'Chêne-Bourg': {'cantonal_tax': {'rate': 27, 'label': 'Cantonal + Municipal Tax (Chêne-Bourg)'}},
        'Bernex': {'cantonal_tax': {'rate': 27, 'label': 'Cantonal + Municipal Tax (Bernex)'}},
        'Plan-les-Ouates': {'cantonal_tax': {'rate': 25, 'label': 'Cantonal + Municipal Tax (Plan-les-Ouates)'}},
    },
}

# Property-linked deduction keys that scale with neighborhood cost multiplier
SCALABLE_DEDUCTIONS = {'council_tax', 'property_tax'}

# Colors for deduction breakdown bars
DEDUCTION_COLORS = {
    'income_tax': '#ef4444',
    'social_security': '#f59e0b',
    'state_tax': '#8b5cf6',
    'cantonal_tax': '#8b5cf6',
    'provincial_tax': '#8b5cf6',
    'solidarity': '#06b6d4',
    'church_tax': '#06b6d4',
    'council_tax': '#6b7280',
    'trash_tax': '#6b7280',
}


def calculate_all_deductions(income, country_name, city_name, is_expat=False, neighborhood=None):
    """Calculate all deductions: income tax + social security + city/state taxes + levies.
    Supports 3-tier neighborhood lookup: exact override → scaled → city fallback.
    Returns dict with items list, total, total_rate, net."""
    if income <= 0:
        return {'items': [], 'total': 0, 'total_rate': 0, 'net': 0}

    items = []
    nhood_overrides = neighborhoodDeductions.get(city_name, {}).get(neighborhood, {}) if neighborhood else {}
    nhood_multiplier = cityNeighborhoods.get(city_name, {}).get(neighborhood, 1.0) if neighborhood else 1.0

    # 1. Income Tax (existing progressive calculation — not neighborhood-dependent)
    tax_result = calculate_tax(income, country_name)
    items.append({
        'key': 'income_tax',
        'label': 'Income Tax',
        'amount': tax_result['tax'],
        'rate': tax_result['effective_rate']
    })

    # 2. Social Security from country-level data (not neighborhood-dependent)
    country_ded = countryDeductions.get(country_name, {})
    ss = country_ded.get('social_security', {})
    if ss:
        ss_rate = ss.get('expat' if is_expat else 'local', 0)
        if ss_rate > 0:
            ss_cap = ss.get('cap')
            ss_base = min(income, ss_cap) if ss_cap else income
            ss_amount = ss_base * (ss_rate / 100)
            # Handle UK-style reduced rate above cap
            if ss.get('reduced_rate') and ss_cap and income > ss_cap:
                ss_amount += (income - ss_cap) * (ss['reduced_rate'] / 100)
            ss_eff_rate = round((ss_amount / income) * 100, 1)
            items.append({
                'key': 'social_security',
                'label': ss.get('label', 'Social Security'),
                'amount': ss_amount,
                'rate': ss_eff_rate
            })

    # 3. City/neighborhood-level taxes (state, cantonal, provincial)
    # Tier 1: Check neighborhood override first, then city, then country
    city_ded = cityDeductions.get(city_name, {})
    for tax_key in ['state_tax', 'cantonal_tax', 'provincial_tax']:
        tax_info = nhood_overrides.get(tax_key, city_ded.get(tax_key, country_ded.get(tax_key, {})))
        if tax_info and tax_info.get('rate', 0) > 0:
            rate = tax_info['rate']
            amount = income * (rate / 100)
            items.append({
                'key': tax_key,
                'label': tax_info['label'],
                'amount': amount,
                'rate': rate
            })

    # 4. Country/city/neighborhood levies (solidarity, church tax, council tax, etc.)
    # 3-tier: neighborhood override → scaled by multiplier → city/country fallback
    for levy_key in ['solidarity', 'church_tax', 'council_tax', 'trash_tax']:
        # Tier 1: Exact neighborhood override
        levy = nhood_overrides.get(levy_key)
        if not levy:
            # Tier 2: Scale property-linked deductions by neighborhood multiplier
            base_levy = city_ded.get(levy_key, country_ded.get(levy_key))
            if not base_levy:
                continue
            if levy_key in SCALABLE_DEDUCTIONS and neighborhood and base_levy.get('flat_annual'):
                scaled_amount = round(base_levy['flat_annual'] * nhood_multiplier)
                levy = {**base_levy, 'flat_annual': scaled_amount, 'label': base_levy['label'] + ' (est.)'}
            else:
                # Tier 3: City/country fallback unchanged
                levy = base_levy

        if levy.get('flat_annual'):
            amount = levy['flat_annual']
            eff_rate = round((amount / income) * 100, 1)
            items.append({
                'key': levy_key,
                'label': levy['label'],
                'amount': amount,
                'rate': eff_rate
            })
        elif levy.get('of') == 'income_tax':
            base = tax_result['tax']
            amount = base * (levy['rate'] / 100)
            eff_rate = round((amount / income) * 100, 1)
            items.append({
                'key': levy_key,
                'label': levy['label'],
                'amount': amount,
                'rate': eff_rate
            })
        elif levy.get('rate'):
            rate = levy['rate']
            amount = income * (rate / 100)
            items.append({
                'key': levy_key,
                'label': levy['label'],
                'amount': amount,
                'rate': rate
            })

    total_deductions = sum(item['amount'] for item in items)
    total_rate = round((total_deductions / income) * 100, 1)
    net = income - total_deductions

    return {'items': items, 'total': total_deductions, 'total_rate': total_rate, 'net': net}


# Approximate average monthly rent for 1BR in city center (USD)
cityRent1BR = {
    'New York': 3500, 'San Francisco': 3200, 'Los Angeles': 2400, 'Chicago': 2000,
    'Miami': 2500, 'Austin': 1800, 'Seattle': 2200, 'Denver': 1900, 'Boston': 2800,
    'Washington DC': 2400, 'Houston': 1600,
    'Charlotte': 1500, 'Las Vegas': 1400, 'Tampa': 1700, 'Raleigh': 1450,
    'Dallas': 1550, 'Atlanta': 1650, 'Philadelphia': 1550, 'Phoenix': 1450,
    'San Diego': 2600, 'Nashville': 1700, 'Minneapolis': 1550, 'Portland': 1800,
    'Toronto': 2000, 'Vancouver': 2100,
    'Montreal': 1400, 'Mexico City': 700, 'Cancún': 600, 'Panama City': 1000,
    'London': 2500, 'Paris': 1400, 'Amsterdam': 1800, 'Berlin': 1200, 'Munich': 1500,
    'Dublin': 2000, 'Brussels': 1100, 'Luxembourg City': 1800, 'Zurich': 2800,
    'Geneva': 2600, 'Edinburgh': 1300, 'Nice': 1100,
    'Madrid': 1100, 'Barcelona': 1200, 'Valencia': 850, 'Málaga': 800,
    'Lisbon': 1000, 'Porto': 800, 'Rome': 1200, 'Milan': 1400, 'Athens': 700, 'Split': 650,
    'Stockholm': 1500, 'Copenhagen': 1800, 'Helsinki': 1200, 'Oslo': 1600, 'Vienna': 1000,
    'Prague': 800, 'Budapest': 600, 'Warsaw': 700, 'Krakow': 550, 'Bucharest': 500,
    'Tallinn': 650, 'Riga': 550, 'Istanbul': 450,
    'Tokyo': 1500, 'Osaka': 1000, 'Fukuoka': 700, 'Seoul': 1200, 'Hong Kong': 2500,
    'Taipei': 800, 'Shanghai': 1100, 'Beijing': 1000, 'Shenzhen': 900, 'Guangzhou': 750,
    'Singapore': 2200, 'Bangkok': 600, 'Chiang Mai': 350, 'Phuket': 500,
    'Kuala Lumpur': 550, 'Ho Chi Minh City': 500, 'Hanoi': 450, 'Manila': 500,
    'Jakarta': 500, 'Bali (Denpasar)': 450, 'Phnom Penh': 450,
    'Mumbai': 700, 'Bangalore': 400, 'Delhi': 350, 'Chennai': 300,
    'Sydney': 2200, 'Melbourne': 1800, 'Perth': 1500, 'Auckland': 1400,
    'Dubai': 1800, 'Abu Dhabi': 1500, 'Doha': 1600, 'Riyadh': 800, 'Tel Aviv': 1800,
    'Cape Town': 650, 'Nairobi': 500, 'Lagos': 600, 'Cairo': 300,
    'Marrakech': 350, 'Casablanca': 400,
    'São Paulo': 600, 'Buenos Aires': 400, 'Bogotá': 400, 'Lima': 450,
    'Santiago': 550, 'Medellín': 350, 'Montevideo': 500,
    'San José (CR)': 550, 'Playa del Carmen': 500
}

# Salary ranges by job title (USD, global baseline)
salaryRanges = {
    # Healthcare
    'Doctor (General)': {'low': 80000, 'mid': 180000, 'high': 350000},
    'Surgeon': {'low': 120000, 'mid': 280000, 'high': 500000},
    'Dentist': {'low': 70000, 'mid': 160000, 'high': 300000},
    'Pharmacist': {'low': 60000, 'mid': 125000, 'high': 200000},
    'Nurse': {'low': 30000, 'mid': 58000, 'high': 100000},
    'Psychologist': {'low': 45000, 'mid': 85000, 'high': 150000},
    # Engineering & Tech
    'Software Engineer': {'low': 45000, 'mid': 85000, 'high': 180000},
    'DevOps Engineer': {'low': 50000, 'mid': 95000, 'high': 175000},
    'Data Scientist': {'low': 50000, 'mid': 95000, 'high': 170000},
    'Mechanical Engineer': {'low': 40000, 'mid': 78000, 'high': 140000},
    'Civil Engineer': {'low': 38000, 'mid': 72000, 'high': 135000},
    'Electrical Engineer': {'low': 42000, 'mid': 80000, 'high': 145000},
    'Architect': {'low': 38000, 'mid': 72000, 'high': 130000},
    'UX Designer': {'low': 40000, 'mid': 75000, 'high': 140000},
    # Business & Finance
    'Product Manager': {'low': 55000, 'mid': 100000, 'high': 190000},
    'Project Manager': {'low': 45000, 'mid': 80000, 'high': 150000},
    'Financial Analyst': {'low': 42000, 'mid': 78000, 'high': 145000},
    'Accountant': {'low': 35000, 'mid': 62000, 'high': 110000},
    'Business Analyst': {'low': 42000, 'mid': 75000, 'high': 140000},
    'Consultant': {'low': 45000, 'mid': 90000, 'high': 180000},
    'Investment Banker': {'low': 80000, 'mid': 150000, 'high': 350000},
    'Actuary': {'low': 60000, 'mid': 110000, 'high': 200000},
    # Legal
    'Lawyer': {'low': 50000, 'mid': 100000, 'high': 220000},
    'Paralegal': {'low': 30000, 'mid': 52000, 'high': 85000},
    # Marketing & Sales
    'Marketing Manager': {'low': 38000, 'mid': 72000, 'high': 135000},
    'Sales Manager': {'low': 40000, 'mid': 80000, 'high': 160000},
    'Graphic Designer': {'low': 30000, 'mid': 55000, 'high': 100000},
    'Content Writer': {'low': 25000, 'mid': 50000, 'high': 90000},
    # Management & HR
    'HR Manager': {'low': 38000, 'mid': 70000, 'high': 130000},
    'Operations Manager': {'low': 45000, 'mid': 82000, 'high': 150000},
    'CEO / Executive': {'low': 100000, 'mid': 220000, 'high': 500000},
    # Education & Research
    'Teacher': {'low': 25000, 'mid': 48000, 'high': 85000},
    'Professor': {'low': 50000, 'mid': 95000, 'high': 180000},
    'Research Scientist': {'low': 45000, 'mid': 85000, 'high': 155000},
    # Skilled Trades & Other
    'Pilot': {'low': 50000, 'mid': 120000, 'high': 250000},
    'Chef': {'low': 25000, 'mid': 50000, 'high': 100000},
    'Journalist': {'low': 25000, 'mid': 52000, 'high': 95000},
}

CURRENT_YEAR = date.today().year
TOTAL_NEIGHBORHOODS = sum(len(v) for v in cityNeighborhoods.values())
ROUNDED_NEIGHBORHOODS = (TOTAL_NEIGHBORHOODS // 100) * 100

# Wise affiliate link (replace with real invite link when approved)
WISE_LINK = 'https://wise.com/invite/u/placeholder'

# Google Analytics 4 + Consent Mode v2 snippet (injected into all page templates)
GA4_SNIPPET = '''
    <!-- Google Consent Mode v2 — ad signals denied in strict consent regions only -->
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('consent', 'default', {
            'ad_storage': 'denied',
            'ad_user_data': 'denied',
            'ad_personalization': 'denied',
            'analytics_storage': 'granted',
            'wait_for_update': 500,
            'regions': ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV','LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE','IS','LI','NO','GB','CH','BR','CA']
        });
        gtag('consent', 'default', {
            'ad_storage': 'granted',
            'ad_user_data': 'granted',
            'ad_personalization': 'granted',
            'analytics_storage': 'granted'
        });
    </script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-MMZSM2Z96B"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-MMZSM2Z96B');
    </script>
    <!-- Google AdSense Auto Ads -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4472082543745200" crossorigin="anonymous"></script>'''

# Map cities to relevant blog articles for cross-linking
cityBlogLinks = {
    'London': [
        {'url': '/blog/articles/london-vs-new-york-true-cost-comparison', 'title': 'London vs New York: The True Cost Comparison'},
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026', 'title': 'Most Expensive Cities in the World'},
    ],
    'New York': [
        {'url': '/blog/articles/london-vs-new-york-true-cost-comparison', 'title': 'London vs New York: The True Cost Comparison'},
        {'url': '/blog/articles/average-salary-by-city-2026-global-comparison', 'title': 'Average Salary by City: Global Comparison'},
    ],
    'Dubai': [
        {'url': '/blog/articles/dubai-vs-singapore-expat-comparison', 'title': 'Dubai vs Singapore: Expat Comparison'},
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026', 'title': 'Most Expensive Cities in the World'},
    ],
    'Singapore': [
        {'url': '/blog/articles/dubai-vs-singapore-expat-comparison', 'title': 'Dubai vs Singapore: Expat Comparison'},
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
    ],
    'Bangkok': [
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
        {'url': '/blog/articles/top-10-cities-for-remote-workers-2026', 'title': 'Top 10 Cities for Remote Workers'},
    ],
    'Chiang Mai': [
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
        {'url': '/blog/articles/top-10-cities-for-remote-workers-2026', 'title': 'Top 10 Cities for Remote Workers'},
    ],
    'Ho Chi Minh City': [
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
    ],
    'Lisbon': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026', 'title': 'Affordable Cities in Europe for Americans'},
        {'url': '/blog/articles/top-10-cities-for-remote-workers-2026', 'title': 'Top 10 Cities for Remote Workers'},
    ],
    'Barcelona': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'Prague': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'Budapest': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'San Francisco': [
        {'url': '/blog/articles/tech-salary-comparison-by-city-2026', 'title': 'Tech Salary Comparison by City'},
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026', 'title': 'Most Expensive Cities in the World'},
    ],
    'Tokyo': [
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026', 'title': 'Most Expensive Cities in the World'},
        {'url': '/blog/articles/average-salary-by-city-2026-global-comparison', 'title': 'Average Salary by City: Global Comparison'},
    ],
    'Berlin': [
        {'url': '/blog/articles/tech-salary-comparison-by-city-2026', 'title': 'Tech Salary Comparison by City'},
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'Zurich': [
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026', 'title': 'Most Expensive Cities in the World'},
    ],
    '_default': [
        {'url': '/blog/articles/how-cost-of-living-affects-your-salary', 'title': 'How Cost of Living Affects Your Salary'},
        {'url': '/blog/articles/salary-negotiation-when-relocating-abroad', 'title': 'Salary Negotiation When Relocating Abroad'},
    ],
}

TODAY = date.today().isoformat()

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def slugify(name):
    """Convert city name to URL-safe slug"""
    slug = name.lower()
    slug = slug.replace(' (denpasar)', '')
    slug = slug.replace(' (cr)', '')
    slug = slug.replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('ü', 'u')
    slug = slug.replace('ú', 'u').replace('í', 'i').replace('ó', 'o')
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def get_region(city):
    """Get the region for a city"""
    for region, cities in cityRegions.items():
        if city in cities:
            return region
    return 'Other'

def get_coli_rank(city):
    """Get the rank of a city by COLI (1 = most expensive)"""
    sorted_cities = sorted(coliData.items(), key=lambda x: x[1], reverse=True)
    for i, (c, _) in enumerate(sorted_cities):
        if c == city:
            return i + 1
    return 0

def format_currency_amount(amount, currency):
    """Format a number with currency symbol"""
    symbols = {
        'USD': '$', 'GBP': '£', 'EUR': '€', 'JPY': '¥', 'CNY': '¥',
        'AUD': 'A$', 'CAD': 'C$', 'CHF': 'CHF ', 'SGD': 'S$', 'HKD': 'HK$',
        'NZD': 'NZ$', 'SEK': 'kr ', 'NOK': 'kr ', 'DKK': 'kr ',
        'INR': '₹', 'KRW': '₩', 'THB': '฿', 'MYR': 'RM ',
        'AED': 'AED ', 'SAR': 'SAR ', 'QAR': 'QAR ', 'ILS': '₪',
        'ZAR': 'R ', 'BRL': 'R$', 'MXN': 'MX$', 'TRY': '₺',
        'PLN': 'zł ', 'CZK': 'Kč ', 'HUF': 'Ft ', 'RON': 'lei ',
        'TWD': 'NT$', 'PHP': '₱', 'IDR': 'Rp ', 'VND': '₫',
        'EGP': 'E£', 'KES': 'KSh ', 'NGN': '₦', 'MAD': 'MAD ',
        'ARS': 'AR$', 'COP': 'COP ', 'PEN': 'S/', 'CLP': 'CLP ',
        'UYU': '$U ', 'CRC': '₡', 'PAB': 'B/.'
    }
    sym = symbols.get(currency, currency + ' ')
    if amount >= 1000:
        return f'{sym}{amount:,.0f}'
    return f'{sym}{amount:.0f}'

def get_equivalent_salary(salary_usd, from_city, to_city):
    """Calculate equivalent salary from one city to another, return in USD"""
    coli_from = coliData[from_city]
    coli_to = coliData[to_city]
    return salary_usd * (coli_to / coli_from)

def get_expense_breakdown(city):
    """Return estimated expense percentages based on city COLI and rent data"""
    coli = coliData[city]
    rent = cityRent1BR.get(city, 0)
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    rate_to_local = exchangeRates.get(currency, 1) / exchangeRates.get('USD', 1)
    mid_salary_local = 75000 * (coli / 100) * rate_to_local
    tax_result = calculate_tax(mid_salary_local, country)
    monthly_after_tax = (tax_result['net'] / rate_to_local) / 12
    if monthly_after_tax > 0:
        housing_pct = min(45, max(20, round((rent / monthly_after_tax) * 100)))
    else:
        housing_pct = 30
    remaining = 100 - housing_pct
    food_pct = round(remaining * 0.28)
    transport_pct = round(remaining * 0.15)
    utilities_pct = round(remaining * 0.10)
    healthcare_pct = round(remaining * 0.08)
    savings_pct = 100 - housing_pct - food_pct - transport_pct - utilities_pct - healthcare_pct
    return {
        'housing': housing_pct,
        'food': food_pct,
        'transport': transport_pct,
        'utilities': utilities_pct,
        'healthcare': healthcare_pct,
        'other_savings': savings_pct,
    }

def get_city_comparisons(city, comparison_pairs):
    """Return list of comparison info for a city"""
    results = []
    for c1, c2 in comparison_pairs:
        if c1 == city or c2 == city:
            slug1 = slugify(c1)
            slug2 = slugify(c2)
            other = c2 if c1 == city else c1
            results.append({
                'url': f'/compare/{slug1}-vs-{slug2}',
                'other_city': other,
            })
    return results


# ============================================================
# SHARED DARK MODE THEME CONSTANTS
# ============================================================

THEME_CSS_VARS = '''
        :root {
            --bg: #f5f5f7;
            --card-bg: #ffffff;
            --text-primary: #1d1d1f;
            --text-secondary: #86868b;
            --text-body: #4a4a4c;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --shadow: 0 2px 20px rgba(0,0,0,0.06);
            --border: #e5e5ea;
            --border-light: #f0f0f2;
            --table-stripe: #f9f9fb;
            --tag-bg: #f0f0f2;
            --stat-card-bg: #f5f5f7;
        }
        [data-theme="dark"] {
            --bg: #000000;
            --card-bg: #1c1c1e;
            --text-primary: #f5f5f7;
            --text-secondary: #98989f;
            --text-body: #b0b0b5;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --shadow: 0 2px 20px rgba(0,0,0,0.3);
            --border: #38383a;
            --border-light: #2c2c2e;
            --table-stripe: #2c2c2e;
            --tag-bg: #2c2c2e;
            --stat-card-bg: #2c2c2e;
        }
'''

THEME_TOGGLE_CSS = '''
        .theme-toggle {
            position: relative;
            display: inline-flex;
            align-items: center;
            width: 38px;
            height: 22px;
            background: var(--border);
            border: none;
            border-radius: 11px;
            cursor: pointer;
            padding: 0;
            transition: background 0.3s;
            flex-shrink: 0;
        }
        .theme-toggle:hover {
            background: var(--text-secondary);
        }
        .theme-toggle .toggle-thumb {
            position: absolute;
            left: 2px;
            width: 18px;
            height: 18px;
            background: var(--card-bg);
            border-radius: 50%;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
        }
        [data-theme="dark"] .theme-toggle {
            background: #3b82f6;
        }
        [data-theme="dark"] .theme-toggle:hover {
            background: #60a5fa;
        }
        [data-theme="dark"] .theme-toggle .toggle-thumb {
            transform: translateX(16px);
            box-shadow: 0 0 0 2px #93c5fd, 0 1px 3px rgba(0,0,0,0.2);
        }
        .theme-toggle .toggle-icon {
            width: 11px;
            height: 11px;
        }
        .theme-toggle .icon-sun {
            color: #f59e0b;
        }
        .theme-toggle .icon-moon {
            display: none;
            color: #3b82f6;
        }
        [data-theme="dark"] .theme-toggle .icon-sun {
            display: none;
        }
        [data-theme="dark"] .theme-toggle .icon-moon {
            display: block;
            color: #3b82f6;
        }
        @media (max-width: 768px) {
            .theme-toggle {
                position: fixed !important;
                top: 16px !important;
                right: 16px !important;
                z-index: 10001 !important;
            }
        }
'''

THEME_TOGGLE_HTML = '''<button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" type="button">
            <span class="toggle-thumb">
                <svg class="toggle-icon icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
                <svg class="toggle-icon icon-moon" viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            </span>
        </button>'''

THEME_JS = '''
    <script>
    (function(){
        var t=document.getElementById('themeToggle');
        function g(){var s=localStorage.getItem('theme');if(s)return s;return matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'}
        function a(m){document.documentElement.setAttribute('data-theme',m);localStorage.setItem('theme',m);t.setAttribute('aria-label',m==='dark'?'Switch to light mode':'Switch to dark mode')}
        a(g());
        t.addEventListener('click',function(){a(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')});
        matchMedia('(prefers-color-scheme:dark)').addEventListener('change',function(e){if(!localStorage.getItem('theme'))a(e.matches?'dark':'light')});
    })();
    </script>
'''

SHARE_JS = '''
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
    </script>
'''

SHARE_ICON_X = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" fill="currentColor"/></svg>'
SHARE_ICON_LI = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="currentColor"/></svg>'
SHARE_ICON_WA = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" fill="currentColor"/></svg>'
SHARE_ICON_COPY = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SHARE_ICON_EMAIL = '<svg viewBox="0 0 24 24" width="16" height="16"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="22,6 12,13 2,6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def build_share_bar(share_text, share_url):
    """Build share bar HTML for templates."""
    import html as html_mod
    t = html_mod.escape(share_text, quote=True)
    u = html_mod.escape(share_url, quote=True)
    return f'''<div class="share-bar" data-share-text="{t}" data-share-url="{u}">
            <span class="share-bar-label">Share</span>
            <button class="share-btn" data-platform="twitter" aria-label="Share on X" type="button">{SHARE_ICON_X}</button>
            <button class="share-btn" data-platform="linkedin" aria-label="Share on LinkedIn" type="button">{SHARE_ICON_LI}</button>
            <button class="share-btn" data-platform="whatsapp" aria-label="Share on WhatsApp" type="button">{SHARE_ICON_WA}</button>
            <button class="share-btn" data-platform="copy" aria-label="Copy link" type="button">{SHARE_ICON_COPY}</button>
            <button class="share-btn" data-platform="email" aria-label="Share via email" type="button">{SHARE_ICON_EMAIL}</button>
        </div>'''


# ============================================================
# CITY PAGE TEMPLATE
# ============================================================

def generate_city_page(city, comparison_pairs):
    slug = slugify(city)
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    coli = coliData[city]
    rank = get_coli_rank(city)
    total_cities = len(coliData)
    region = get_region(city)
    rent = cityRent1BR.get(city, 0)
    neighborhoods = cityNeighborhoods.get(city, {})

    # Convert $75K USD to local currency equivalent for the "sample salary"
    rate_to_local = exchangeRates[currency] / exchangeRates['USD']
    # Calculate effective tax rate for reference salary in local currency
    ref_salary_local = 75000 * (coli / 100) * rate_to_local
    tax_result_ref = calculate_tax(ref_salary_local, country)
    tax_rate = tax_result_ref['effective_rate']
    # Calculate full deductions breakdown for reference salary
    ded_result = calculate_all_deductions(ref_salary_local, country, city, is_expat=False)
    total_deduction_rate = ded_result['total_rate']
    sample_local = 75000 * rate_to_local
    sample_formatted = format_currency_amount(sample_local, currency)

    # Get equivalent salaries for popular comparison cities
    comparison_cities = ['New York', 'London', 'Singapore', 'Dubai', 'Berlin', 'Tokyo', 'Sydney', 'Toronto', 'Bangkok', 'Lisbon']
    comparisons = []
    for comp in comparison_cities:
        if comp == city:
            continue
        equiv_usd = get_equivalent_salary(75000, city, comp)
        comp_currency = cityToCurrency[comp]
        comp_rate = exchangeRates[comp_currency] / exchangeRates['USD']
        equiv_local = equiv_usd * comp_rate
        comparisons.append({
            'city': comp,
            'slug': slugify(comp),
            'equivalent': format_currency_amount(equiv_local, comp_currency),
            'currency': comp_currency,
            'coli': coliData[comp],
            'diff_pct': (coliData[comp] - coli) / max(coli, coliData[comp]) * 100 if max(coli, coliData[comp]) > 0 else 0
        })

    # Sort neighborhoods
    sorted_neighborhoods = sorted(neighborhoods.items(), key=lambda x: x[1], reverse=True) if neighborhoods else []

    # Neighborhood rows
    neighborhood_rows = ''
    if sorted_neighborhoods:
        for name, mult in sorted_neighborhoods:
            pct = (mult - 1) * 100
            sign = '+' if pct >= 0 else ''
            bar_width = int(mult * 50)
            color = '#22c55e' if pct < 0 else '#2563eb' if pct < 15 else '#f59e0b' if pct < 30 else '#ef4444'
            n_slug = slugify(name)
            neighborhood_rows += f'''
                        <tr>
                            <td><a href="/city/{slug}/{n_slug}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{name}</a></td>
                            <td style="text-align: center;">{mult:.2f}x</td>
                            <td style="text-align: right;">
                                <span style="color: {color}; font-weight: 600;">{sign}{pct:.0f}%</span>
                            </td>
                        </tr>'''

    # Comparison rows
    comparison_rows = ''
    for comp in comparisons[:8]:
        diff = comp['diff_pct']
        color = '#22c55e' if diff < 0 else '#ef4444'
        sign = '+' if diff > 0 else ''
        comp_slug = comp['slug']
        comp_city_name = comp['city']
        comp_coli_val = comp['coli']
        comp_equiv = comp['equivalent']
        comparison_rows += f'''
                        <tr>
                            <td><a href="/city/{comp_slug}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{comp_city_name}</a></td>
                            <td style="text-align: center;">{comp_coli_val}</td>
                            <td style="text-align: center;">{comp_equiv}</td>
                            <td style="text-align: right;">
                                <span style="color: {color}; font-weight: 600;">{sign}{diff:.0f}%</span>
                            </td>
                        </tr>'''

    # Similar cities (same region, sorted by COLI proximity)
    region_cities = [c for c in cityRegions.get(region, []) if c != city]
    region_cities.sort(key=lambda c: abs(coliData[c] - coli))
    similar_links = ''
    for sc in region_cities[:6]:
        sc_slug = slugify(sc)
        similar_links += f'<a href="/city/{sc_slug}" class="similar-city-link">{sc}</a>\n'

    # Calculate what $75K in this city buys vs NY
    purchasing_power_vs_ny = (100 / coli) * 100  # percentage of NY purchasing power

    # Determine COLI description
    if coli >= 90:
        coli_desc = 'very high'
    elif coli >= 70:
        coli_desc = 'high'
    elif coli >= 50:
        coli_desc = 'moderate'
    elif coli >= 30:
        coli_desc = 'low'
    else:
        coli_desc = 'very low'

    # Expense breakdown
    expenses = get_expense_breakdown(city)

    # Salary ranges for this city
    salary_rows = ''
    job_titles_list = list(salaryRanges.keys())
    for title in job_titles_list:
        ranges = salaryRanges[title]
        local_low = ranges['low'] * (coli / 100) * rate_to_local
        local_mid = ranges['mid'] * (coli / 100) * rate_to_local
        local_high = ranges['high'] * (coli / 100) * rate_to_local
        fmt_low = format_currency_amount(local_low, currency)
        fmt_mid = format_currency_amount(local_mid, currency)
        fmt_high = format_currency_amount(local_high, currency)
        salary_rows += f'''
                        <tr>
                            <td style="font-weight: 500;">{title}</td>
                            <td style="text-align: center;">{fmt_low}</td>
                            <td style="text-align: center; font-weight: 600;">{fmt_mid}</td>
                            <td style="text-align: right;">{fmt_high}</td>
                        </tr>'''

    # How much do you need section
    annual_rent = rent * 12
    mid_salary_local = 75000 * (coli / 100) * rate_to_local
    monthly_salary_after_tax = (mid_salary_local * (1 - total_deduction_rate / 100)) / 12
    fmt_annual_rent = format_currency_amount(annual_rent * rate_to_local, currency)
    fmt_monthly_salary = format_currency_amount(monthly_salary_after_tax, currency)
    fmt_mid_salary_local = format_currency_amount(mid_salary_local, currency)

    # City comparisons links
    city_comps = get_city_comparisons(city, comparison_pairs)
    comp_links_html = ''
    for cc in city_comps:
        other = cc['other_city']
        cc_url = cc['url']
        comp_links_html += f'<a href="{cc_url}" class="similar-city-link">{city} vs {other}</a>\n'

    # FAQ items - build outside f-string
    tax_note = 'a tax-free jurisdiction' if tax_rate == 0 else f'approximately {tax_rate}%'
    neigh_names = [n for n, m in sorted_neighborhoods[-3:]] if sorted_neighborhoods else []
    neigh_answer = ('The most affordable neighborhoods include ' + ', '.join(neigh_names) + '.') if neigh_names else 'Neighborhood-level data is not yet available for this city.'
    expensive_neigh_names = [n for n, m in sorted_neighborhoods[:3]] if sorted_neighborhoods else []
    expensive_neigh_answer = ('The most expensive neighborhoods are ' + ', '.join(expensive_neigh_names) + '.') if expensive_neigh_names else 'Neighborhood-level data is not yet available for this city.'

    equiv_salary_in_city = get_equivalent_salary(75000, 'New York', city) * rate_to_local
    fmt_equiv = format_currency_amount(equiv_salary_in_city, currency)

    faq_items = [
        {
            'q': f'What is the cost of living index for {city}?',
            'a': f'The cost of living index (COLI) for {city} is {coli}, which ranks #{rank} out of {total_cities} cities globally. New York is the baseline at 100.'
        },
        {
            'q': f'How much salary do I need in {city} to match $75,000 in New York?',
            'a': f'To maintain the same purchasing power as $75,000 USD in New York, you would need approximately {fmt_equiv} in {city}.'
        },
        {
            'q': f'What is the average rent in {city}?',
            'a': f'The average monthly rent for a one-bedroom apartment in the city center of {city} is approximately ${rent:,} USD.'
        },
        {
            'q': f'What are the total payroll deductions in {country}?',
            'a': f'The approximate effective income tax rate for a mid-range earner in {country} is {tax_note}. Including social security and other mandatory contributions, total deductions are approximately {total_deduction_rate}%.'
        },
        {
            'q': f'What are the cheapest neighborhoods in {city}?',
            'a': neigh_answer
        },
        {
            'q': f'What are the most expensive areas in {city}?',
            'a': expensive_neigh_answer
        },
    ]

    # Build FAQ schema JSON items
    faq_schema_items = []
    for item in faq_items:
        q_escaped = item['q'].replace('"', '&quot;')
        a_escaped = item['a'].replace('"', '&quot;')
        faq_schema_items.append(
            '{"@type": "Question", "name": "' + q_escaped + '", "acceptedAnswer": {"@type": "Answer", "text": "' + a_escaped + '"}}'
        )
    faq_schema_list = ', '.join(faq_schema_items)

    # Build FAQ HTML
    faq_html = ''
    for item in faq_items:
        faq_html += '<div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #f0f0f2;">'
        faq_html += '<h3 style="font-size: 0.95rem; font-weight: 600; margin-bottom: 8px; color: #1d1d1f;">' + item['q'] + '</h3>'
        faq_html += '<p style="font-size: 0.9rem; color: #4a4a4c; line-height: 1.7; margin: 0;">' + item['a'] + '</p>'
        faq_html += '</div>'

    # Blog links
    blog_links = cityBlogLinks.get(city, cityBlogLinks['_default'])
    blog_links_html = ''
    for bl in blog_links:
        bl_url = bl['url']
        bl_title = bl['title']
        blog_links_html += f'<a href="{bl_url}" style="display: block; padding: 12px 0; border-bottom: 1px solid #f0f0f2; color: #2563eb; text-decoration: none; font-weight: 500; font-size: 0.9rem;">{bl_title}</a>\n'

    # About section tax paragraph
    if tax_rate == 0 and total_deduction_rate == 0:
        tax_paragraph = '<p>The approximate average effective income tax rate in ' + country + ' is <strong>0%</strong>. This is a tax-free jurisdiction with no mandatory employee deductions.</p>'
    elif tax_rate == 0:
        tax_paragraph = '<p>' + country + ' is a tax-free jurisdiction, but employees may still face mandatory deductions of approximately <strong>' + str(total_deduction_rate) + '%</strong> (including social security contributions).</p>'
    elif tax_rate is not None:
        tax_paragraph = '<p>The approximate effective income tax rate in ' + country + ' is <strong>' + str(tax_rate) + '%</strong> for a mid-range earner. Including social security and other mandatory deductions, the total deduction rate is approximately <strong>' + str(total_deduction_rate) + '%</strong>.</p>'
    else:
        tax_paragraph = ''

    # Neighborhood section
    if neighborhoods:
        neigh_count = str(len(neighborhoods))
        neigh_section = '<section class="content-card"><h2>Neighborhoods in ' + city + '</h2><p>' + neigh_count + ' neighborhoods tracked with cost multipliers relative to the city average. This neighborhood-level data helps you understand exactly how costs vary within ' + city + '.</p><table><thead><tr><th>Neighborhood</th><th style="text-align:center;">Multiplier</th><th style="text-align:right;">vs City Avg</th></tr></thead><tbody>' + neighborhood_rows + '</tbody></table></section>'
    else:
        neigh_section = ''

    # Expense breakdown rows
    expense_colors = {
        'housing': '#2563eb',
        'food': '#f59e0b',
        'transport': '#8b5cf6',
        'utilities': '#06b6d4',
        'healthcare': '#22c55e',
        'other_savings': '#6b7280',
    }
    expense_labels = {
        'housing': 'Housing',
        'food': 'Food & Groceries',
        'transport': 'Transportation',
        'utilities': 'Utilities',
        'healthcare': 'Healthcare',
        'other_savings': 'Other & Savings',
    }
    expense_rows = ''
    for key in ['housing', 'food', 'transport', 'utilities', 'healthcare', 'other_savings']:
        pct = expenses[key]
        label = expense_labels[key]
        ecolor = expense_colors[key]
        expense_rows += '<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">'
        expense_rows += '<div style="width: 130px; font-size: 0.85rem; font-weight: 500; color: #4a4a4c;">' + label + '</div>'
        expense_rows += '<div style="flex: 1; background: #f0f0f2; border-radius: 6px; height: 12px; overflow: hidden;">'
        expense_rows += '<div style="width: ' + str(pct) + '%; height: 100%; background: ' + ecolor + '; border-radius: 6px;"></div>'
        expense_rows += '</div>'
        expense_rows += '<div style="width: 40px; text-align: right; font-size: 0.85rem; font-weight: 600; color: #1d1d1f;">' + str(pct) + '%</div>'
        expense_rows += '</div>'

    # Deductions breakdown rows (reuses expense bar pattern)
    deduction_rows = ''
    fmt_ref_salary = format_currency_amount(ref_salary_local, currency)
    fmt_net_salary = format_currency_amount(ded_result['net'], currency)
    max_ded_rate = max((item['rate'] for item in ded_result['items']), default=1) or 1
    for item in ded_result['items']:
        dcolor = DEDUCTION_COLORS.get(item['key'], '#6b7280')
        bar_width = round((item['rate'] / max_ded_rate) * 100) if max_ded_rate > 0 else 0
        bar_width = max(bar_width, 2)  # minimum visible width
        fmt_amount = format_currency_amount(item['amount'], currency)
        deduction_rows += '<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">'
        deduction_rows += '<div style="width: 200px; font-size: 0.85rem; font-weight: 500; color: var(--text-body, #4a4a4c);">' + item['label'] + '</div>'
        deduction_rows += '<div style="flex: 1; background: var(--border-light, #f0f0f2); border-radius: 6px; height: 12px; overflow: hidden;">'
        deduction_rows += '<div style="width: ' + str(bar_width) + '%; height: 100%; background: ' + dcolor + '; border-radius: 6px;"></div>'
        deduction_rows += '</div>'
        deduction_rows += '<div style="width: 48px; text-align: right; font-size: 0.85rem; font-weight: 600; color: var(--text-primary, #1d1d1f);">' + str(item['rate']) + '%</div>'
        deduction_rows += '</div>'

    deduction_section = ''
    if ded_result['items']:
        deduction_section = f'''<section class="content-card">
            <h2>Tax &amp; Deductions Breakdown in {city}</h2>
            <p>Estimated annual deductions for a mid-range salary of <strong>{fmt_ref_salary}</strong> in {city}. This shows all mandatory payroll deductions as a local employee.</p>
            {deduction_rows}
            <div style="border-top: 1px solid var(--border, #e5e5ea); margin-top: 16px; padding-top: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-primary, #1d1d1f);">Total Deductions: {total_deduction_rate}%</span>
                </div>
                <div>
                    <span style="font-size: 0.9rem; color: var(--text-secondary, #86868b);">Est. Take-Home: </span>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #22c55e;">{fmt_net_salary}/yr</span>
                </div>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary, #86868b); margin-top: 12px; margin-bottom: 0;">Rates shown are for a local employee. Expat rates may differ — use the <a href="/" style="color: var(--accent, #2563eb);">main converter</a> for personalized calculations.</p>
        </section>'''

    # Compare with other cities section
    comp_section = ''
    if city_comps:
        comp_section = '<section class="content-card"><h2>Compare ' + city + ' With Other Cities</h2><p>See detailed side-by-side comparisons of salaries, rent, taxes, and neighborhoods.</p><div class="similar-cities">' + comp_links_html + '</div></section>'

    # Related articles section
    related_section = ''
    if blog_links_html:
        related_section = '<section class="content-card"><h2>Related Articles</h2>' + blog_links_html + '</section>'

    # Share bar
    share_text = f'{city} cost of living index: {coli}'
    if rank:
        share_text += f' (ranked #{rank} of {total_cities})'
    share_text += '. Compare salaries & neighborhoods on salary:converter'
    share_bar_html = build_share_bar(share_text, f'https://salary-converter.com/city/{slug}')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{city} Cost of Living: ${rent:,}/mo Rent ({CURRENT_YEAR})</title>
    <meta name="description" content="1BR rent: ${rent:,}/mo. Ranked #{rank}/{total_cities} globally. {len(neighborhoods)} neighborhoods ranked.">
    <meta name="keywords" content="{city} cost of living, {city} salary, {city} neighborhoods, cost of living {country}, salary comparison {city}, {city} rent prices {CURRENT_YEAR}">
    <meta name="author" content="salary:converter">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/city/{slug}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://salary-converter.com/city/{slug}">
    <meta property="og:title" content="{city} Cost of Living: ${rent:,}/mo Rent ({CURRENT_YEAR})">
    <meta property="og:description" content="1BR rent: ${rent:,}/mo. Ranked #{rank}/{total_cities} globally. {len(neighborhoods)} neighborhoods ranked.">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{city} Cost of Living: ${rent:,}/mo Rent ({CURRENT_YEAR})">
    <meta name="twitter:description" content="1BR rent: ${rent:,}/mo. Ranked #{rank}/{total_cities} globally. {len(neighborhoods)} neighborhoods ranked.">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Cost of Living in {city}, {country} — {CURRENT_YEAR} Guide",
        "description": "Comprehensive cost of living guide for {city} with neighborhood data, salary comparisons, and tax information.",
        "url": "https://salary-converter.com/city/{slug}",
        "datePublished": "{TODAY}",
        "dateModified": "{TODAY}",
        "publisher": {{
            "@type": "Organization",
            "name": "salary:converter",
            "url": "https://salary-converter.com"
        }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"}},
            {{"@type": "ListItem", "position": 2, "name": "Cities", "item": "https://salary-converter.com/city/"}},
            {{"@type": "ListItem", "position": 3, "name": "{city}", "item": "https://salary-converter.com/city/{slug}"}}
        ]
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{faq_schema_list}]
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--bg); color: var(--text-primary); min-height: 100vh;
            padding: 20px 12px;
            -webkit-font-smoothing: antialiased;
            transition: background 0.3s, color 0.3s;
        }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .breadcrumb {{
            font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px;
        }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .hero {{
            background: var(--card-bg); border-radius: 20px; padding: 40px 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{
            font-size: 2.2rem; font-weight: 700; letter-spacing: -0.5px;
            margin-bottom: 8px; color: var(--text-primary);
        }}
        .hero .subtitle {{
            font-size: 1.05rem; color: var(--text-secondary); margin-bottom: 24px;
        }}
        .stat-grid {{
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
            margin-top: 24px;
        }}
        .stat-card {{
            background: var(--stat-card-bg); border-radius: 14px; padding: 16px 12px;
            text-align: center;
        }}
        .stat-card .stat-value {{
            font-size: 1.5rem; font-weight: 700; color: var(--accent);
        }}
        .stat-card .stat-label {{
            font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px;
            text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;
        }}
        .content-card {{
            background: var(--card-bg); border-radius: 20px; padding: 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
        }}
        .content-card h2 {{
            font-size: 1.3rem; font-weight: 700; margin-bottom: 16px;
            color: var(--text-primary); letter-spacing: -0.3px;
        }}
        .content-card p {{
            font-size: 0.92rem; color: var(--text-body); line-height: 1.7;
            margin-bottom: 16px;
        }}
        table {{
            width: 100%; border-collapse: collapse; font-size: 0.88rem;
        }}
        table th {{
            text-align: left; padding: 10px 12px; font-size: 0.75rem;
            text-transform: uppercase; letter-spacing: 0.5px;
            color: var(--text-secondary); border-bottom: 2px solid var(--border); font-weight: 600;
        }}
        table td {{
            padding: 10px 12px; border-bottom: 1px solid var(--border-light); color: var(--text-primary);
        }}
        table tr:hover td {{ background: var(--table-stripe); }}
        .cta-section {{
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            border-radius: 20px; padding: 40px 32px; text-align: center;
            margin-bottom: 24px;
        }}
        .cta-section h2 {{ color: white; font-size: 1.4rem; margin-bottom: 8px; }}
        .cta-section p {{ color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-bottom: 20px; }}
        .cta-btn {{
            display: inline-block; background: white; color: #2563eb;
            padding: 14px 32px; border-radius: 100px; font-weight: 600;
            font-size: 0.95rem; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s;
        }}
        .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.15); }}
        .similar-cities {{
            display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px;
        }}
        .similar-city-link {{
            display: inline-block; padding: 8px 16px; background: var(--tag-bg);
            border-radius: 100px; font-size: 0.82rem; font-weight: 500;
            color: var(--text-primary); text-decoration: none; transition: all 0.2s;
        }}
        .similar-city-link:hover {{
            background: var(--accent); color: white;
        }}
        .page-footer {{
            text-align: center; padding: 32px 0 16px; margin-top: 16px;
            border-top: 1px solid var(--border);
            display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: var(--text-secondary); text-decoration: none;
        }}
        .page-footer a:hover {{ color: var(--accent); }}
        .tax-bar {{
            background: var(--tag-bg); border-radius: 10px; padding: 3px; margin: 8px 0;
        }}
        .tax-bar-fill {{
            height: 8px; border-radius: 8px;
            background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
        }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}

        @media (max-width: 768px) {{
            body {{ padding: 0; background: var(--bg); }}
            .page-wrapper {{ padding: 0 16px; }}
            .nav-links {{ padding-right: 48px; }}
            .hero {{ border-radius: 0; padding: 32px 20px; box-shadow: none; }}
            .stat-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .content-card {{ border-radius: 16px; padding: 20px; }}
            .hero h1 {{ font-size: 1.6rem; }}
            .two-col {{ grid-template-columns: 1fr; }}
            .cta-section {{ border-radius: 16px; padding: 32px 20px; }}
            table {{ font-size: 0.82rem; }}
            table th, table td {{ padding: 8px; }}
        }}
        .share-bar {{
            display: flex; align-items: center; gap: 8px;
            margin: 16px 0 20px; padding: 12px 16px;
            background: var(--stat-card-bg, #f5f5f7); border-radius: 12px;
        }}
        .share-bar-label {{
            font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);
            text-transform: uppercase; letter-spacing: 0.5px; margin-right: 4px;
        }}
        .share-btn {{
            display: flex; align-items: center; justify-content: center;
            width: 34px; height: 34px; border-radius: 50%;
            border: 1px solid var(--border, #e5e5ea); background: var(--card-bg, #fff);
            color: var(--text-secondary, #86868b); cursor: pointer; transition: all 0.2s;
            padding: 0;
        }}
        .share-btn:hover {{ color: var(--accent); border-color: var(--accent); transform: scale(1.08); }}
        .share-btn.copied {{ color: #22c55e; border-color: #22c55e; }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/city/">Cities</a> &rsaquo; {city}
        </div>

        <section class="hero">
            <h1>Cost of Living in {city}</h1>
            <p class="subtitle">{country} &middot; {region} &middot; Currency: {currency}</p>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-value">{coli}</div>
                    <div class="stat-label">COLI Index</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">#{rank}</div>
                    <div class="stat-label">of {total_cities} Cities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_deduction_rate}%</div>
                    <div class="stat-label">Total Deductions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${rent:,}</div>
                    <div class="stat-label">1BR Rent/mo</div>
                </div>
            </div>
        </section>
        {share_bar_html}

        <section class="content-card">
            <h2>About {city}</h2>
            <p>
                {city} has a cost of living index of <strong>{coli}</strong>, making it a <strong>{coli_desc}</strong> cost city
                compared to New York (baseline = 100). It ranks <strong>#{rank} out of {total_cities}</strong> cities tracked globally.
            </p>
            <p>
                The local currency is <strong>{currency}</strong>. A salary of <strong>$75,000 USD</strong> in New York
                would need to be approximately <strong>{fmt_equiv}</strong>
                in {city} to maintain the same purchasing power.
            </p>
            {tax_paragraph}
        </section>

        <section class="content-card">
            <h2>Monthly Cost Breakdown in {city}</h2>
            <p>Estimated monthly expense allocation for a mid-range earner living in {city}. Housing costs are based on average one-bedroom rent in the city center (${rent:,}/month), with other categories adjusted for the local cost of living index.</p>
            {expense_rows}
            <p style="font-size: 0.8rem; color: var(--text-secondary, #86868b); margin-top: 16px; margin-bottom: 0;">Estimates based on a mid-range salary adjusted for {city}'s COLI of {coli} and {country}'s total deduction rate of {total_deduction_rate}%. Individual expenses will vary.</p>
        </section>

        {deduction_section}

        <section class="content-card">
            <h2>Salary Ranges by Job Title in {city} ({CURRENT_YEAR})</h2>
            <p>Estimated annual salaries in {city} ({currency}) adjusted for cost of living. These figures represent local purchasing-power-adjusted ranges based on global baseline data.</p>
            <div style="overflow-x: auto;">
            <table>
                <thead>
                    <tr>
                        <th>Job Title</th>
                        <th style="text-align: center;">Entry Level</th>
                        <th style="text-align: center;">Mid Level</th>
                        <th style="text-align: right;">Senior Level</th>
                    </tr>
                </thead>
                <tbody>{salary_rows}
                </tbody>
            </table>
            </div>
            <p style="font-size: 0.8rem; color: #86868b; margin-top: 16px; margin-bottom: 0;">Salary ranges are estimates adjusted by {city}'s COLI ({coli}) relative to the New York baseline (100). Actual salaries depend on experience, company, and industry.</p>
        </section>

        <section class="content-card">
            <h2>How Much Do You Need to Earn in {city}?</h2>
            <p>Understanding your take-home pay is critical when evaluating a move to {city}. With total deductions of approximately <strong>{total_deduction_rate}%</strong> (income tax + social security) in {country} and average one-bedroom rent of <strong>${rent:,}/month</strong>, here is what a mid-range salary looks like:</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0;">
                <div class="stat-card">
                    <div class="stat-value" style="font-size: 1.2rem;">{fmt_mid_salary_local}</div>
                    <div class="stat-label">Gross Annual (Mid-Range)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="font-size: 1.2rem;">{fmt_monthly_salary}</div>
                    <div class="stat-label">Monthly Take-Home</div>
                </div>
            </div>
            <p>After taxes, a mid-range earner in {city} takes home approximately <strong>{fmt_monthly_salary}</strong> per month. With housing consuming roughly <strong>{expenses['housing']}%</strong> of after-tax income, careful budgeting is essential in this <strong>{coli_desc}</strong> cost city. Your purchasing power in {city} is <strong>{purchasing_power_vs_ny:.0f}%</strong> of what it would be in New York for the same nominal salary.</p>
        </section>

        {neigh_section}

        <section class="content-card">
            <h2>Salary Comparison: {city} vs Other Cities</h2>
            <p>To maintain the same standard of living as $75,000 USD in {city}, here's what you'd need in other cities:</p>
            <table>
                <thead>
                    <tr>
                        <th>City</th>
                        <th style="text-align: center;">COLI</th>
                        <th style="text-align: center;">Equivalent Salary</th>
                        <th style="text-align: right;">Difference</th>
                    </tr>
                </thead>
                <tbody>{comparison_rows}
                </tbody>
            </table>
        </section>

        {comp_section}

        <section class="content-card wise-cta" style="border: 1px solid #9fe870; border-left: 4px solid #9fe870; background: var(--card-bg);">
            <div style="display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap;">
                <div style="flex:1; min-width:200px;">
                    <p style="font-size:0.65rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin:0 0 6px;">Sponsored</p>
                    <h3 style="font-size:1rem; font-weight:600; margin:0 0 6px; color:var(--text-primary);">Moving to {city}?</h3>
                    <p style="font-size:0.85rem; color:var(--text-body); line-height:1.5; margin:0 0 12px;">Open a multi-currency account to manage {currency} and your home currency. No hidden fees, real exchange rate.</p>
                    <a href="{WISE_LINK}" rel="noopener noreferrer sponsored" target="_blank"
                       style="display:inline-block; padding:10px 24px; background:#9fe870; color:#1a1a1a; border-radius:100px; font-weight:600; font-size:0.85rem; text-decoration:none; transition:transform 0.2s;">
                        Open a Wise Account &rarr;
                    </a>
                </div>
            </div>
        </section>

        <section class="cta-section">
            <h2>Calculate Your Exact Salary</h2>
            <p>Use our free converter tool with {ROUNDED_NEIGHBORHOODS:,}+ neighborhood adjustments</p>
            <a href="/" class="cta-btn">Open Salary Converter</a>
        </section>

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {faq_html}
        </section>

        <section class="content-card">
            <h2>Data Sources &amp; Methodology</h2>
            <p>Our cost of living index (COLI) uses New York City as the baseline (COLI&nbsp;=&nbsp;100). Indices are derived from multiple sources including <a href="https://www.numbeo.com/cost-of-living/" target="_blank" rel="noopener">Numbeo</a>, <a href="https://www.expatistan.com/cost-of-living" target="_blank" rel="noopener">Expatistan</a>, and national statistics agencies. Exchange rates are sourced from the <a href="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html" target="_blank" rel="noopener">European Central Bank</a>.</p>
            <p>Tax rates represent approximate effective rates for mid-range earners based on <a href="https://www.oecd.org/tax/tax-policy/taxing-wages-brochure.pdf" target="_blank" rel="noopener">OECD Taxing Wages</a> data and do not constitute tax advice. Neighborhood cost multipliers are estimated from local rental indices and property data. Salary ranges are modeled by adjusting global baseline figures by each city's COLI.</p>
            <p style="font-size: 0.8rem; color: #86868b; margin-bottom: 0;">Last updated: {TODAY}. Data is refreshed periodically and may not reflect very recent changes. All figures are estimates for informational purposes only.</p>
        </section>

        <section class="content-card">
            <h2>Explore Similar Cities</h2>
            <p>Other cities in {region}:</p>
            <div class="similar-cities">
                {similar_links}
            </div>
        </section>

        {related_section}

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/">All Cities</a>
            <a href="/compare/">City Comparisons</a>
            <a href="/blog/">Blog</a>
            <a href="/privacy/">Privacy</a>
        </footer>
    </div>
{THEME_JS}
{SHARE_JS}
</body>
</html>'''

    return html


# ============================================================
# NEIGHBORHOOD HUB PAGE TEMPLATE (Cheapest / Most Expensive)
# ============================================================

def generate_neighborhood_hub_page(city, mode='cheapest'):
    """Generate a cheapest or most-expensive neighborhoods hub page for a city.
    mode: 'cheapest' or 'most-expensive'
    """
    slug = slugify(city)
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    coli = coliData[city]
    rent = cityRent1BR.get(city, 0)
    neighborhoods = cityNeighborhoods.get(city, {})

    if not neighborhoods:
        return ''

    # Sort neighborhoods
    is_cheapest = mode == 'cheapest'
    sorted_nhoods = sorted(neighborhoods.items(), key=lambda x: x[1], reverse=not is_cheapest)
    total_nhoods = len(sorted_nhoods)

    # Key data points
    cheapest_name, cheapest_mult = sorted(neighborhoods.items(), key=lambda x: x[1])[0]
    most_exp_name, most_exp_mult = sorted(neighborhoods.items(), key=lambda x: x[1])[-1]
    cheapest_rent = round(rent * cheapest_mult)
    most_exp_rent = round(rent * most_exp_mult)
    featured_name = sorted_nhoods[0][0]  # #1 on this page
    featured_rent = round(rent * sorted_nhoods[0][1])

    # Title & meta
    if is_cheapest:
        page_title = f"{min(10, total_nhoods)} Cheapest Neighborhoods in {city} ({CURRENT_YEAR})"
        page_desc = f"Find the most affordable neighborhoods in {city}. {cheapest_name} starts at ${cheapest_rent:,}/mo. Ranked by cost index with rent &amp; salary data."
        hero_label = "Cheapest Neighborhoods"
        hero_stat_label = "Cheapest Rent"
        hero_stat_value = f"${cheapest_rent:,}/mo"
        table_label = "% Below Avg"
        url_path = f"city/{slug}/cheapest-neighborhoods"
        opposite_label = f"Most Expensive Neighborhoods in {city}"
        opposite_url = f"/city/{slug}/most-expensive-neighborhoods"
    else:
        page_title = f"{min(10, total_nhoods)} Most Expensive Neighborhoods in {city} ({CURRENT_YEAR})"
        page_desc = f"Discover the priciest neighborhoods in {city}. {most_exp_name} reaches ${most_exp_rent:,}/mo. Full rankings with rent &amp; cost data."
        hero_label = "Most Expensive Neighborhoods"
        hero_stat_label = "Highest Rent"
        hero_stat_value = f"${most_exp_rent:,}/mo"
        table_label = "% Above Avg"
        url_path = f"city/{slug}/most-expensive-neighborhoods"
        opposite_label = f"Cheapest Neighborhoods in {city}"
        opposite_url = f"/city/{slug}/cheapest-neighborhoods"

    canonical_url = f"https://salary-converter.com/{url_path}"
    share_text = f"{page_title} | salary:converter"
    share_bar = build_share_bar(share_text, canonical_url)

    # Build table rows
    table_rows = ''
    for i, (name, mult) in enumerate(sorted_nhoods):
        n_slug = slugify(name)
        n_rent = round(rent * mult)
        pct_diff = round((mult - 1.0) * 100)
        if pct_diff > 0:
            pct_class = 'color: #ef4444; font-weight: 600;'
            pct_text = f'+{pct_diff}%'
        elif pct_diff < 0:
            pct_class = 'color: #22c55e; font-weight: 600;'
            pct_text = f'{pct_diff}%'
        else:
            pct_class = 'color: var(--text-secondary); font-weight: 600;'
            pct_text = 'Avg'

        table_rows += f'''
                        <tr>
                            <td style="text-align:center; color:var(--text-secondary);">{i+1}</td>
                            <td><a href="/city/{slug}/{n_slug}" style="color: var(--accent); text-decoration: none; font-weight: 500;">{name}</a></td>
                            <td style="text-align:center;">${n_rent:,}/mo</td>
                            <td style="text-align:center;">{mult:.2f}x</td>
                            <td style="text-align:right;"><span style="{pct_class}">{pct_text}</span></td>
                        </tr>'''

    # FAQ schema
    if is_cheapest:
        faq1_q = f"What is the cheapest neighborhood in {city}?"
        faq1_a = f"The cheapest neighborhood in {city} is {cheapest_name}, with an estimated 1-bedroom rent of ${cheapest_rent:,}/month \u2014 {abs(round((cheapest_mult - 1.0) * 100))}% below the city average."
        faq2_q = f"What is the average rent in {city}?"
        faq2_a = f"The average 1-bedroom rent in {city} is approximately ${rent:,}/month. Rents range from ${cheapest_rent:,}/mo ({cheapest_name}) to ${most_exp_rent:,}/mo ({most_exp_name})."
        faq3_q = f"How many neighborhoods does {city} have?"
        faq3_a = f"Our database covers {total_nhoods} neighborhoods in {city}, each with detailed cost-of-living and salary data."
    else:
        faq1_q = f"What is the most expensive neighborhood in {city}?"
        faq1_a = f"The most expensive neighborhood in {city} is {most_exp_name}, with an estimated 1-bedroom rent of ${most_exp_rent:,}/month \u2014 {round((most_exp_mult - 1.0) * 100)}% above the city average."
        faq2_q = f"How much more expensive is {most_exp_name} than the city average?"
        faq2_a = f"{most_exp_name} is approximately {round((most_exp_mult - 1.0) * 100)}% more expensive than the {city} average. 1-bedroom rent is ${most_exp_rent:,}/mo vs ${rent:,}/mo city-wide."
        faq3_q = f"How many neighborhoods does {city} have?"
        faq3_a = f"Our database covers {total_nhoods} neighborhoods in {city}, each with detailed cost-of-living and salary data."

    import json
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": faq1_q, "acceptedAnswer": {"@type": "Answer", "text": faq1_a}},
            {"@type": "Question", "name": faq2_q, "acceptedAnswer": {"@type": "Answer", "text": faq2_a}},
            {"@type": "Question", "name": faq3_q, "acceptedAnswer": {"@type": "Answer", "text": faq3_a}},
        ]
    })

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"},
            {"@type": "ListItem", "position": 2, "name": "Cities", "item": "https://salary-converter.com/city/"},
            {"@type": "ListItem", "position": 3, "name": city, "item": f"https://salary-converter.com/city/{slug}"},
            {"@type": "ListItem", "position": 4, "name": hero_label},
        ]
    })

    # Wise CTA
    wise_cta = f'''
        <section class="content-card wise-cta" style="border: 1px solid #9fe870; border-left: 4px solid #9fe870; background: var(--card-bg);">
            <div style="display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap;">
                <div style="flex:1; min-width:200px;">
                    <p style="font-size:0.65rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin:0 0 6px;">Sponsored</p>
                    <h3 style="font-size:1rem; font-weight:600; margin:0 0 6px; color:var(--text-primary);">Moving to {city}?</h3>
                    <p style="font-size:0.85rem; color:var(--text-body); line-height:1.5; margin:0 0 12px;">Open a multi-currency account to manage {currency} and your home currency. No hidden fees, real exchange rate.</p>
                    <a href="{WISE_LINK}" rel="noopener noreferrer sponsored" target="_blank"
                       style="display:inline-block; padding:10px 24px; background:#9fe870; color:#1a1a1a; border-radius:100px; font-weight:600; font-size:0.85rem; text-decoration:none; transition:transform 0.2s;">
                        Open a Wise Account &rarr;
                    </a>
                </div>
            </div>
        </section>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{page_title}</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta name="description" content="{page_desc}">
    <link rel="canonical" href="{canonical_url}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{page_desc}">
    <meta property="og:url" content="{canonical_url}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:description" content="{page_desc}">
    <script type="application/ld+json">{breadcrumb_schema}</script>
    <script type="application/ld+json">{faq_schema}</script>
{GA4_SNIPPET}
    <style>
{THEME_CSS_VARS}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text-primary); line-height: 1.5; -webkit-font-smoothing: antialiased; }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; padding: 32px 24px 60px; }}
        .nav-bar {{ display: flex; align-items: center; justify-content: space-between; padding: 16px 0 24px; border-bottom: 1px solid var(--border-light); margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }}
        .nav-bar a {{ color: var(--text-secondary); text-decoration: none; font-size: 0.8rem; font-weight: 500; }}
        .nav-bar a:hover {{ color: var(--accent); }}
        .logo {{ font-size: 1rem; font-weight: 700; color: var(--text-primary) !important; letter-spacing: -0.5px; }}
        .breadcrumb {{ font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        .hero {{ margin-bottom: 24px; }}
        .hero h1 {{ font-size: 1.6rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .hero p {{ font-size: 0.9rem; color: var(--text-body); }}
        .stat-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px; }}
        .stat-card {{ background: var(--stat-card-bg); border-radius: 12px; padding: 16px; text-align: center; }}
        .stat-card .label {{ font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); margin-bottom: 4px; }}
        .stat-card .value {{ font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }}
        .content-card {{ background: var(--card-bg); border-radius: 16px; padding: 28px 24px; box-shadow: var(--shadow); margin-bottom: 20px; }}
        .content-card h2 {{ font-size: 1.15rem; font-weight: 700; margin-bottom: 16px; }}
        .content-card p {{ font-size: 0.9rem; color: var(--text-body); line-height: 1.6; margin-bottom: 12px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        th {{ text-align: left; padding: 10px 8px; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); border-bottom: 2px solid var(--border); }}
        td {{ padding: 10px 8px; border-bottom: 1px solid var(--border-light); }}
        tr:nth-child(even) {{ background: var(--table-stripe); }}
        .similar-cities {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .similar-city-link {{ display: inline-block; padding: 8px 16px; background: var(--stat-card-bg); border-radius: 8px; color: var(--accent); text-decoration: none; font-size: 0.82rem; font-weight: 500; transition: background 0.2s; }}
        .similar-city-link:hover {{ background: var(--border); }}
        .page-footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border-light); display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; }}
        .page-footer a {{ font-size: 0.78rem; color: var(--text-secondary); text-decoration: none; }}
        .page-footer a:hover {{ color: var(--accent); }}
        .faq-item {{ margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid var(--border-light); }}
        .faq-item:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .faq-item h3 {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 8px; color: var(--text-primary); }}
        .faq-item p {{ font-size: 0.9rem; color: var(--text-body); line-height: 1.7; margin: 0; }}
{THEME_TOGGLE_CSS}
        @media (max-width: 600px) {{
            .page-wrapper {{ padding: 16px 16px 48px; }}
            .hero h1 {{ font-size: 1.3rem; }}
            .stat-grid {{ grid-template-columns: 1fr; }}
            table {{ font-size: 0.8rem; }}
            th, td {{ padding: 8px 6px; }}
        }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        <nav class="nav-bar">
            <a href="/" class="logo">salary:converter</a>
            <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
                <a href="/city/">Cities</a>
                <a href="/compare/">Compare</a>
                <a href="/blog/">Blog</a>
                <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme" type="button">
                    <span class="toggle-thumb">
                        <svg class="toggle-icon icon-sun" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/></svg>
                        <svg class="toggle-icon icon-moon" viewBox="0 0 20 20" fill="currentColor"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/></svg>
                    </span>
                </button>
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/city/">Cities</a> &rsaquo; <a href="/city/{slug}">{city}</a> &rsaquo; {hero_label}
        </div>

        <div class="hero">
            <h1>{hero_label} in {city}</h1>
            <p>All {total_nhoods} neighborhoods in {city} ranked by cost of living index. Updated {CURRENT_YEAR}.</p>
        </div>

        <div class="stat-grid">
            <div class="stat-card">
                <div class="label">{hero_stat_label}</div>
                <div class="value">{hero_stat_value}</div>
            </div>
            <div class="stat-card">
                <div class="label">City Avg Rent</div>
                <div class="value">${rent:,}/mo</div>
            </div>
            <div class="stat-card">
                <div class="label">Neighborhoods</div>
                <div class="value">{total_nhoods}</div>
            </div>
        </div>

        {share_bar}

        <section class="content-card">
            <h2>{hero_label} in {city} &mdash; Full Rankings</h2>
            <div style="overflow-x:auto;">
            <table>
                <thead>
                    <tr>
                        <th style="text-align:center; width:40px;">#</th>
                        <th>Neighborhood</th>
                        <th style="text-align:center;">1BR Rent</th>
                        <th style="text-align:center;">Index</th>
                        <th style="text-align:right;">vs Avg</th>
                    </tr>
                </thead>
                <tbody>{table_rows}
                </tbody>
            </table>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 16px; margin-bottom: 0;">Rent estimates based on city average of ${rent:,}/mo adjusted by neighborhood cost index. Index 1.00 = city average.</p>
        </section>

{wise_cta}

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-item"><h3>{faq1_q}</h3><p>{faq1_a}</p></div>
            <div class="faq-item"><h3>{faq2_q}</h3><p>{faq2_a}</p></div>
            <div class="faq-item"><h3>{faq3_q}</h3><p>{faq3_a}</p></div>
        </section>

        <section class="content-card">
            <h2>Explore More</h2>
            <div class="similar-cities">
                <a href="{opposite_url}" class="similar-city-link">{opposite_label}</a>
                <a href="/city/{slug}" class="similar-city-link">{city} Cost of Living Guide</a>
                <a href="/salary-needed/{slug}" class="similar-city-link">Salary Needed in {city}</a>
                <a href="/city/" class="similar-city-link">All Cities</a>
            </div>
        </section>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/{slug}">{city}</a>
            <a href="/city/">Cities</a>
            <a href="/compare/">Compare</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
{THEME_JS}
{SHARE_JS}
</body>
</html>'''
    return html


# ============================================================
# COMPARISON PAGE TEMPLATE
# ============================================================

def generate_comparison_page(city1, city2):
    slug1 = slugify(city1)
    slug2 = slugify(city2)
    country1 = cityCountry.get(city1, '')
    country2 = cityCountry.get(city2, '')
    currency1 = cityToCurrency.get(city1, 'USD')
    currency2 = cityToCurrency.get(city2, 'USD')
    coli1 = coliData[city1]
    coli2 = coliData[city2]
    rank1 = get_coli_rank(city1)
    rank2 = get_coli_rank(city2)
    # Calculate effective tax rates for reference salary in each city's local currency
    rate1_local = exchangeRates.get(currency1, 1) / exchangeRates.get('USD', 1)
    rate2_local = exchangeRates.get(currency2, 1) / exchangeRates.get('USD', 1)
    ref_salary_local_1 = 75000 * (coli1 / 100) * rate1_local
    ref_salary_local_2 = 75000 * (coli2 / 100) * rate2_local
    tax1 = calculate_tax(ref_salary_local_1, country1)['effective_rate']
    tax2 = calculate_tax(ref_salary_local_2, country2)['effective_rate']
    # Full deductions breakdown for both cities
    ded1 = calculate_all_deductions(ref_salary_local_1, country1, city1, is_expat=False)
    ded2 = calculate_all_deductions(ref_salary_local_2, country2, city2, is_expat=False)
    total_ded_rate1 = ded1['total_rate']
    total_ded_rate2 = ded2['total_rate']
    rent1 = cityRent1BR.get(city1, 0)
    rent2 = cityRent1BR.get(city2, 0)
    neighborhoods1 = cityNeighborhoods.get(city1, {})
    neighborhoods2 = cityNeighborhoods.get(city2, {})
    total_cities = len(coliData)

    coli_ratio = coli2 / coli1
    coli_diff_pct = abs(coli2 - coli1) / max(coli1, coli2) * 100

    # Equivalent salaries at $75K baseline
    rate1 = exchangeRates[currency1] / exchangeRates['USD']
    rate2 = exchangeRates[currency2] / exchangeRates['USD']
    salary_in_city1 = 75000 * rate1
    equiv_in_city2 = get_equivalent_salary(75000, city1, city2) * rate2

    cheaper_city = city1 if coli1 < coli2 else city2
    pct_cheaper = abs(coli_diff_pct)

    # Cross-rate
    cross_rate = exchangeRates[currency2] / exchangeRates[currency1]

    # Salary difference text
    if coli2 > coli1:
        salary_diff_text = f"That is <strong>{pct_cheaper:.0f}%</strong> more due to higher cost of living."
    else:
        salary_diff_text = f"That is <strong>{pct_cheaper:.0f}%</strong> less thanks to lower cost of living."

    # Neighborhood comparison (top 5 each)
    sorted_n1 = sorted(neighborhoods1.items(), key=lambda x: x[1], reverse=True)[:5] if neighborhoods1 else []
    sorted_n2 = sorted(neighborhoods2.items(), key=lambda x: x[1], reverse=True)[:5] if neighborhoods2 else []

    neigh_rows_1 = ''
    for name, mult in sorted_n1:
        pct = (mult - 1) * 100
        neigh_rows_1 += f'<tr><td>{name}</td><td style="text-align:right;">{mult:.2f}x ({pct:+.0f}%)</td></tr>'

    neigh_rows_2 = ''
    for name, mult in sorted_n2:
        pct = (mult - 1) * 100
        neigh_rows_2 += f'<tr><td>{name}</td><td style="text-align:right;">{mult:.2f}x ({pct:+.0f}%)</td></tr>'

    # Neighborhood comparison section
    neigh_section = ''
    if sorted_n1 or sorted_n2:
        neigh_section = (
            '<section class="content-card"><h2>Neighborhoods</h2><div class="two-col">'
            '<div><h3 style="font-size:0.95rem; margin-bottom:12px;">' + city1 + ' (Top 5)</h3>'
            '<table><thead><tr><th>Neighborhood</th><th style="text-align:right;">Multiplier</th></tr></thead>'
            '<tbody>' + neigh_rows_1 + '</tbody></table></div>'
            '<div><h3 style="font-size:0.95rem; margin-bottom:12px;">' + city2 + ' (Top 5)</h3>'
            '<table><thead><tr><th>Neighborhood</th><th style="text-align:right;">Multiplier</th></tr></thead>'
            '<tbody>' + neigh_rows_2 + '</tbody></table></div></div></section>'
        )

    # Key Takeaways narrative
    more_expensive_city = city2 if coli2 > coli1 else city1
    less_expensive_city = city1 if coli1 < coli2 else city2
    rent_diff_pct = abs(rent2 - rent1) / max(rent1, rent2) * 100 if max(rent1, rent2) > 0 else 0
    rent_cheaper_city = city1 if rent1 < rent2 else city2
    rent_more_city = city1 if rent1 >= rent2 else city2

    # Tax comparison text (using total deductions)
    if total_ded_rate1 == total_ded_rate2:
        tax_compare_text = f'Both cities have similar total deduction rates of approximately {total_ded_rate1}% (income tax + social security + local taxes).'
    elif total_ded_rate1 < total_ded_rate2:
        tax_compare_text = f'{city1} has lower total deductions ({total_ded_rate1}%) compared to {city2} ({total_ded_rate2}%), meaning you keep more of your gross salary in {city1}.'
    else:
        tax_compare_text = f'{city2} has lower total deductions ({total_ded_rate2}%) compared to {city1} ({total_ded_rate1}%), meaning you keep more of your gross salary in {city2}.'

    # Tax-free note
    if tax1 == 0:
        tax_free_note_1 = f' {country1} is a tax-free jurisdiction, which is a significant financial advantage.'
    else:
        tax_free_note_1 = ''
    if tax2 == 0:
        tax_free_note_2 = f' {country2} is a tax-free jurisdiction, which is a significant financial advantage.'
    else:
        tax_free_note_2 = ''

    # Salary comparison by job title (6 popular jobs)
    job_compare_titles = ['Doctor (General)', 'Software Engineer', 'Product Manager', 'Lawyer', 'Data Scientist', 'Marketing Manager', 'Teacher', 'Nurse']
    job_compare_rows = ''
    for title in job_compare_titles:
        ranges = salaryRanges[title]
        mid_usd = ranges['mid']
        local_1 = mid_usd * (coli1 / 100) * rate1
        local_2 = mid_usd * (coli2 / 100) * rate2
        fmt_1 = format_currency_amount(local_1, currency1)
        fmt_2 = format_currency_amount(local_2, currency2)
        job_compare_rows += f'''
                        <tr>
                            <td style="font-weight: 500;">{title}</td>
                            <td style="text-align: center;">{fmt_1}</td>
                            <td style="text-align: center;">{fmt_2}</td>
                        </tr>'''

    # FAQ items for comparison
    fmt_salary_city1 = format_currency_amount(salary_in_city1, currency1)
    fmt_equiv_city2 = format_currency_amount(equiv_in_city2, currency2)

    comp_faq_items = [
        {
            'q': f'Is {city1} or {city2} more expensive?',
            'a': f'{more_expensive_city} is more expensive overall. {city1} has a COLI of {coli1} while {city2} has a COLI of {coli2}, making {less_expensive_city} approximately {pct_cheaper:.0f}% cheaper.'
        },
        {
            'q': f'What salary in {city2} equals {fmt_salary_city1} in {city1}?',
            'a': f'To maintain the same standard of living as {fmt_salary_city1} in {city1}, you would need approximately {fmt_equiv_city2} in {city2}.'
        },
        {
            'q': f'Is rent cheaper in {city1} or {city2}?',
            'a': f'Average one-bedroom rent in {city1} is ${rent1:,}/month compared to ${rent2:,}/month in {city2}. {rent_cheaper_city} has lower rent by approximately {rent_diff_pct:.0f}%.'
        },
        {
            'q': f'Which city has lower taxes, {city1} or {city2}?',
            'a': tax_compare_text + tax_free_note_1 + tax_free_note_2
        },
    ]

    # Build FAQ schema
    comp_faq_schema_items = []
    for item in comp_faq_items:
        q_escaped = item['q'].replace('"', '&quot;')
        a_escaped = item['a'].replace('"', '&quot;')
        comp_faq_schema_items.append(
            '{"@type": "Question", "name": "' + q_escaped + '", "acceptedAnswer": {"@type": "Answer", "text": "' + a_escaped + '"}}'
        )
    comp_faq_schema_list = ', '.join(comp_faq_schema_items)

    # Build FAQ HTML
    comp_faq_html = ''
    for item in comp_faq_items:
        comp_faq_html += '<div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #f0f0f2;">'
        comp_faq_html += '<h3 style="font-size: 0.95rem; font-weight: 600; margin-bottom: 8px; color: #1d1d1f;">' + item['q'] + '</h3>'
        comp_faq_html += '<p style="font-size: 0.9rem; color: #4a4a4c; line-height: 1.7; margin: 0;">' + item['a'] + '</p>'
        comp_faq_html += '</div>'

    # Winner class helpers
    coli1_winner = 'winner' if coli1 <= coli2 else ''
    coli2_winner = 'winner' if coli2 <= coli1 else ''
    rent1_winner = 'winner' if rent1 <= rent2 else ''
    rent2_winner = 'winner' if rent2 <= rent1 else ''
    tax1_winner = 'winner' if total_ded_rate1 <= total_ded_rate2 else ''
    tax2_winner = 'winner' if total_ded_rate2 <= total_ded_rate1 else ''

    # Build side-by-side deductions breakdown section
    def build_ded_bars(ded_result, currency):
        """Build horizontal bar HTML for a city's deductions."""
        rows = ''
        max_rate = max((item['rate'] for item in ded_result['items']), default=1) or 1
        for item in ded_result['items']:
            dcolor = DEDUCTION_COLORS.get(item['key'], '#6b7280')
            bar_w = round((item['rate'] / max_rate) * 100) if max_rate > 0 else 0
            bar_w = max(bar_w, 2)
            rows += '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">'
            rows += '<div style="width: 140px; font-size: 0.8rem; font-weight: 500; color: var(--text-body, #4a4a4c); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + item['label'] + '</div>'
            rows += '<div style="flex: 1; background: var(--border-light, #f0f0f2); border-radius: 4px; height: 10px; overflow: hidden;">'
            rows += '<div style="width: ' + str(bar_w) + '%; height: 100%; background: ' + dcolor + '; border-radius: 4px;"></div>'
            rows += '</div>'
            rows += '<div style="width: 38px; text-align: right; font-size: 0.8rem; font-weight: 600; color: var(--text-primary, #1d1d1f);">' + str(item['rate']) + '%</div>'
            rows += '</div>'
        fmt_net = format_currency_amount(ded_result['net'], currency)
        rows += '<div style="border-top: 1px solid var(--border, #e5e5ea); margin-top: 8px; padding-top: 8px;">'
        rows += '<div style="display: flex; justify-content: space-between; font-size: 0.85rem;">'
        rows += '<span style="font-weight: 600; color: var(--text-primary, #1d1d1f);">Total: ' + str(ded_result['total_rate']) + '%</span>'
        rows += '<span style="color: #22c55e; font-weight: 700;">Take-Home: ' + fmt_net + '/yr</span>'
        rows += '</div></div>'
        return rows

    ded_bars_1 = build_ded_bars(ded1, currency1)
    ded_bars_2 = build_ded_bars(ded2, currency2)
    ded_comparison_section = f'''<section class="content-card">
            <h2>Tax &amp; Deductions Comparison</h2>
            <p>Full breakdown of mandatory payroll deductions for a mid-range salary as a local employee in each city.</p>
            <div class="two-col">
                <div>
                    <h3 style="font-size: 0.95rem; margin-bottom: 12px; color: var(--text-primary, #1d1d1f);">{city1}</h3>
                    {ded_bars_1}
                </div>
                <div>
                    <h3 style="font-size: 0.95rem; margin-bottom: 12px; color: var(--text-primary, #1d1d1f);">{city2}</h3>
                    {ded_bars_2}
                </div>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary, #86868b); margin-top: 12px; margin-bottom: 0;">Rates shown for local employees. Expat deductions may differ — use the <a href="/" style="color: var(--accent, #2563eb);">main converter</a> for personalized calculations.</p>
        </section>'''

    # Share bar
    share_text = f'Yes, {cheaper_city} is {pct_cheaper:.0f}% cheaper than {more_expensive_city} — See the full comparison on salary:converter'
    share_bar_html = build_share_bar(share_text, f'https://salary-converter.com/compare/{slug1}-vs-{slug2}')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{city1} vs {city2}: {pct_cheaper:.0f}% Cost Difference ({CURRENT_YEAR})</title>
    <meta name="description" content="Rent: ${rent1:,}/mo vs ${rent2:,}/mo. {cheaper_city} is {pct_cheaper:.0f}% cheaper overall. Salary equivalents, taxes & 2,000+ neighborhoods compared.">
    <meta name="keywords" content="{city1} vs {city2}, cost of living comparison, salary comparison, {city1} {city2} relocation, {city1} or {city2}">
    <meta name="author" content="salary:converter">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/compare/{slug1}-vs-{slug2}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://salary-converter.com/compare/{slug1}-vs-{slug2}">
    <meta property="og:title" content="{city1} vs {city2}: {pct_cheaper:.0f}% Cost Difference ({CURRENT_YEAR})">
    <meta property="og:description" content="Rent: ${rent1:,}/mo vs ${rent2:,}/mo. {cheaper_city} is {pct_cheaper:.0f}% cheaper overall. Salary equivalents, taxes & 2,000+ neighborhoods compared.">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{city1} vs {city2}: {pct_cheaper:.0f}% Cost Difference ({CURRENT_YEAR})">
    <meta name="twitter:description" content="Rent: ${rent1:,}/mo vs ${rent2:,}/mo. {cheaper_city} is {pct_cheaper:.0f}% cheaper overall. Salary equivalents, taxes & 2,000+ neighborhoods compared.">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{city1} vs {city2}: Cost of Living & Salary Comparison {CURRENT_YEAR}",
        "description": "Detailed comparison of cost of living, salaries, neighborhoods, and tax rates between {city1} and {city2}.",
        "url": "https://salary-converter.com/compare/{slug1}-vs-{slug2}",
        "datePublished": "{TODAY}",
        "dateModified": "{TODAY}",
        "publisher": {{
            "@type": "Organization",
            "name": "salary:converter",
            "url": "https://salary-converter.com"
        }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"}},
            {{"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://salary-converter.com/compare/"}},
            {{"@type": "ListItem", "position": 3, "name": "{city1} vs {city2}", "item": "https://salary-converter.com/compare/{slug1}-vs-{slug2}"}}
        ]
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{comp_faq_schema_list}]
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--bg); color: var(--text-primary); min-height: 100vh;
            padding: 20px 12px;
            -webkit-font-smoothing: antialiased;
            transition: background 0.3s, color 0.3s;
        }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .breadcrumb {{
            font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px;
        }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .hero {{
            background: var(--card-bg); border-radius: 20px; padding: 40px 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .hero .subtitle {{ font-size: 1rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .vs-badge {{
            display: inline-block; background: #2563eb; color: white;
            font-weight: 700; font-size: 0.85rem; padding: 6px 14px;
            border-radius: 100px; margin: 0 8px;
        }}
        .compare-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 0;
            margin-top: 24px;
        }}
        .compare-col {{
            padding: 20px; text-align: center;
        }}
        .compare-col:first-child {{ border-right: 2px solid var(--border); }}
        .compare-col .city-name {{
            font-size: 1.1rem; font-weight: 700; margin-bottom: 4px;
        }}
        .compare-col .country {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 16px; }}
        .compare-stat {{
            margin-bottom: 12px;
        }}
        .compare-stat .value {{
            font-size: 1.3rem; font-weight: 700; color: var(--accent);
        }}
        .compare-stat .label {{
            font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase;
            letter-spacing: 0.5px; font-weight: 500;
        }}
        .content-card {{
            background: var(--card-bg); border-radius: 20px; padding: 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
        }}
        .content-card h2 {{
            font-size: 1.3rem; font-weight: 700; margin-bottom: 16px;
            color: var(--text-primary);
        }}
        .content-card p {{
            font-size: 0.92rem; color: var(--text-body); line-height: 1.7; margin-bottom: 16px;
        }}
        table {{
            width: 100%; border-collapse: collapse; font-size: 0.88rem;
        }}
        table th {{
            text-align: left; padding: 10px 12px; font-size: 0.75rem;
            text-transform: uppercase; letter-spacing: 0.5px;
            color: var(--text-secondary); border-bottom: 2px solid var(--border); font-weight: 600;
        }}
        table td {{
            padding: 10px 12px; border-bottom: 1px solid var(--border-light);
        }}
        .metric-row {{
            display: grid; grid-template-columns: 1fr 2fr 2fr; gap: 12px;
            padding: 14px 0; border-bottom: 1px solid var(--border-light);
            align-items: center; font-size: 0.9rem;
        }}
        .metric-row:last-child {{ border-bottom: none; }}
        .metric-label {{ color: var(--text-secondary); font-weight: 500; font-size: 0.82rem; }}
        .metric-value {{ font-weight: 600; text-align: center; }}
        .winner {{ color: #22c55e; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
        .similar-cities {{
            display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px;
        }}
        .similar-city-link {{
            display: inline-block; padding: 8px 16px; background: var(--tag-bg);
            border-radius: 100px; font-size: 0.82rem; font-weight: 500;
            color: var(--text-primary); text-decoration: none; transition: all 0.2s;
        }}
        .similar-city-link:hover {{
            background: var(--accent); color: white;
        }}
        .cta-section {{
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            border-radius: 20px; padding: 40px 32px; text-align: center;
            margin-bottom: 24px;
        }}
        .cta-section h2 {{ color: white; font-size: 1.4rem; margin-bottom: 8px; }}
        .cta-section p {{ color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-bottom: 20px; }}
        .cta-btn {{
            display: inline-block; background: white; color: #2563eb;
            padding: 14px 32px; border-radius: 100px; font-weight: 600;
            font-size: 0.95rem; text-decoration: none; transition: transform 0.2s;
        }}
        .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.15); }}
        .page-footer {{
            text-align: center; padding: 32px 0 16px; margin-top: 16px;
            border-top: 1px solid var(--border);
            display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: var(--text-secondary); text-decoration: none;
        }}
        .page-footer a:hover {{ color: var(--accent); }}
        @media (max-width: 768px) {{
            body {{ padding: 0; background: var(--bg); }}
            .page-wrapper {{ padding: 0 16px; }}
            .nav-links {{ padding-right: 48px; }}
            .hero {{ border-radius: 0; padding: 32px 16px; box-shadow: none; }}
            .hero h1 {{ font-size: 1.4rem; }}
            .compare-col {{ padding: 12px 8px; }}
            .compare-stat .value {{ font-size: 1.1rem; }}
            .content-card {{ border-radius: 16px; padding: 20px; }}
            .two-col {{ grid-template-columns: 1fr; }}
            .metric-row {{ grid-template-columns: 1fr 1fr 1fr; gap: 8px; font-size: 0.82rem; }}
            .cta-section {{ border-radius: 16px; padding: 32px 16px; }}
        }}
        .share-bar {{
            display: flex; align-items: center; gap: 8px;
            margin: 16px 0 20px; padding: 12px 16px;
            background: var(--stat-card-bg, #f5f5f7); border-radius: 12px;
        }}
        .share-bar-label {{
            font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);
            text-transform: uppercase; letter-spacing: 0.5px; margin-right: 4px;
        }}
        .share-btn {{
            display: flex; align-items: center; justify-content: center;
            width: 34px; height: 34px; border-radius: 50%;
            border: 1px solid var(--border, #e5e5ea); background: var(--card-bg, #fff);
            color: var(--text-secondary, #86868b); cursor: pointer; transition: all 0.2s;
            padding: 0;
        }}
        .share-btn:hover {{ color: var(--accent); border-color: var(--accent); transform: scale(1.08); }}
        .share-btn.copied {{ color: #22c55e; border-color: #22c55e; }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/compare/">City Comparisons</a> &rsaquo; {city1} vs {city2}
        </div>

        <section class="hero">
            <h1>{city1} <span class="vs-badge">VS</span> {city2}</h1>
            <p class="subtitle">Cost of Living & Salary Comparison {CURRENT_YEAR}</p>

            <div class="compare-grid">
                <div class="compare-col">
                    <div class="city-name">{city1}</div>
                    <div class="country">{country1}</div>
                    <div class="compare-stat">
                        <div class="value">{coli1}</div>
                        <div class="label">COLI Index</div>
                    </div>
                    <div class="compare-stat">
                        <div class="value">#{rank1}</div>
                        <div class="label">Global Rank</div>
                    </div>
                    <div class="compare-stat">
                        <div class="value">{currency1}</div>
                        <div class="label">Currency</div>
                    </div>
                </div>
                <div class="compare-col">
                    <div class="city-name">{city2}</div>
                    <div class="country">{country2}</div>
                    <div class="compare-stat">
                        <div class="value">{coli2}</div>
                        <div class="label">COLI Index</div>
                    </div>
                    <div class="compare-stat">
                        <div class="value">#{rank2}</div>
                        <div class="label">Global Rank</div>
                    </div>
                    <div class="compare-stat">
                        <div class="value">{currency2}</div>
                        <div class="label">Currency</div>
                    </div>
                </div>
            </div>
        </section>
        {share_bar_html}

        <section class="content-card">
            <h2>Key Differences</h2>
            <div class="metric-row">
                <div class="metric-label">Cost of Living</div>
                <div class="metric-value {coli1_winner}">{coli1}</div>
                <div class="metric-value {coli2_winner}">{coli2}</div>
            </div>
            <div class="metric-row">
                <div class="metric-label">1BR Rent (USD/mo)</div>
                <div class="metric-value {rent1_winner}">${rent1:,}</div>
                <div class="metric-value {rent2_winner}">${rent2:,}</div>
            </div>
            <div class="metric-row">
                <div class="metric-label">Total Deductions</div>
                <div class="metric-value {tax1_winner}">{total_ded_rate1}%</div>
                <div class="metric-value {tax2_winner}">{total_ded_rate2}%</div>
            </div>
            <div class="metric-row">
                <div class="metric-label">Exchange Rate</div>
                <div class="metric-value" colspan="2" style="grid-column: span 2; text-align: center;">1 {currency1} = {cross_rate:.4f} {currency2}</div>
            </div>
        </section>

        <section class="content-card">
            <h2>Key Takeaways: {city1} vs {city2}</h2>
            <p>Overall, <strong>{less_expensive_city}</strong> is approximately <strong>{pct_cheaper:.0f}% cheaper</strong> than {more_expensive_city} based on our cost of living index. {city1} has a COLI of {coli1} (ranked #{rank1} of {total_cities} cities), while {city2} has a COLI of {coli2} (ranked #{rank2}).</p>
            <p>When it comes to housing, one-bedroom apartment rent in {city1} averages <strong>${rent1:,}/month</strong> compared to <strong>${rent2:,}/month</strong> in {city2}. That makes {rent_cheaper_city} approximately <strong>{rent_diff_pct:.0f}% cheaper</strong> for rent alone.</p>
            <p>{tax_compare_text}{tax_free_note_1}{tax_free_note_2} When evaluating a relocation, remember that total deductions directly impact your take-home pay and should be weighed alongside cost of living differences.</p>
        </section>

        {ded_comparison_section}

        <section class="content-card">
            <h2>Salary Equivalent</h2>
            <p>
                If you earn <strong>{format_currency_amount(salary_in_city1, currency1)}</strong> in {city1},
                you would need approximately <strong>{format_currency_amount(equiv_in_city2, currency2)}</strong> in {city2}
                to maintain the same purchasing power.
                {salary_diff_text}
            </p>
        </section>

        <section class="content-card">
            <h2>Salary Comparison by Job Title</h2>
            <p>Estimated mid-level annual salaries in local currency, adjusted for each city's cost of living:</p>
            <div style="overflow-x: auto;">
            <table>
                <thead>
                    <tr>
                        <th>Job Title</th>
                        <th style="text-align: center;">{city1} ({currency1})</th>
                        <th style="text-align: center;">{city2} ({currency2})</th>
                    </tr>
                </thead>
                <tbody>{job_compare_rows}
                </tbody>
            </table>
            </div>
            <p style="font-size: 0.8rem; color: #86868b; margin-top: 16px; margin-bottom: 0;">Salary estimates are adjusted by each city's COLI relative to the New York baseline. Actual salaries vary by company, experience, and industry.</p>
        </section>

        {neigh_section}

        <section class="content-card wise-cta" style="border: 1px solid #9fe870; border-left: 4px solid #9fe870; background: var(--card-bg);">
            <div style="display:flex; align-items:flex-start; gap:16px; flex-wrap:wrap;">
                <div style="flex:1; min-width:200px;">
                    <p style="font-size:0.65rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin:0 0 6px;">Sponsored</p>
                    <h3 style="font-size:1rem; font-weight:600; margin:0 0 6px; color:var(--text-primary);">Moving between {city1} and {city2}?</h3>
                    <p style="font-size:0.85rem; color:var(--text-body); line-height:1.5; margin:0 0 12px;">Save up to 6x on international transfers. Send money at the real exchange rate with no hidden fees.</p>
                    <a href="{WISE_LINK}" rel="noopener noreferrer sponsored" target="_blank"
                       style="display:inline-block; padding:10px 24px; background:#9fe870; color:#1a1a1a; border-radius:100px; font-weight:600; font-size:0.85rem; text-decoration:none; transition:transform 0.2s;">
                        Compare Transfer Fees &rarr;
                    </a>
                </div>
            </div>
        </section>

        <section class="cta-section">
            <h2>Get Your Exact Number</h2>
            <p>Use our converter with {ROUNDED_NEIGHBORHOODS:,}+ neighborhood adjustments for a precise salary comparison</p>
            <a href="/" class="cta-btn">Open Salary Converter</a>
        </section>

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {comp_faq_html}
        </section>

        <section class="content-card">
            <h2>Explore Each City</h2>
            <div class="similar-cities">
                <a href="/city/{slug1}" class="similar-city-link">{city1} Cost of Living Guide</a>
                <a href="/city/{slug2}" class="similar-city-link">{city2} Cost of Living Guide</a>
            </div>
        </section>

        <section class="content-card">
            <h2>Data Sources &amp; Methodology</h2>
            <p>Cost of living indices (COLI) are benchmarked to New York City = 100 and derived from <a href="https://www.numbeo.com/cost-of-living/" target="_blank" rel="noopener noreferrer">Numbeo</a> and <a href="https://www.expatistan.com/cost-of-living" target="_blank" rel="noopener noreferrer">Expatistan</a> crowd-sourced price surveys, cross-referenced with national statistics agencies. Rent data from <a href="https://www.numbeo.com/property-investment/" target="_blank" rel="noopener noreferrer">Numbeo Property Prices</a>.</p>
            <p>Salary ranges are compiled from the <a href="https://www.bls.gov/oes/" target="_blank" rel="noopener noreferrer">U.S. Bureau of Labor Statistics (OES)</a>, <a href="https://www.glassdoor.com/Salaries/index.htm" target="_blank" rel="noopener noreferrer">Glassdoor</a>, and <a href="https://www.payscale.com/research/US/Country=United_States/Salary" target="_blank" rel="noopener noreferrer">PayScale</a>. Tax rates are approximate effective rates for mid-range earners based on <a href="https://www.oecd.org/tax/tax-policy/taxing-wages-brochure.pdf" target="_blank" rel="noopener noreferrer">OECD Taxing Wages</a> and national tax authorities. Exchange rates from the <a href="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html" target="_blank" rel="noopener noreferrer">European Central Bank</a>. Neighborhood multipliers are estimated from local rental indices and property data.</p>
            <p style="font-size: 0.8rem; color: #86868b; margin-bottom: 0;">Last updated: {TODAY}. Data is refreshed periodically. All figures are estimates for informational purposes only.</p>
        </section>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/{slug1}">{city1}</a>
            <a href="/city/{slug2}">{city2}</a>
            <a href="/compare/">City Comparisons</a>
            <a href="/blog/">Blog</a>
            <a href="/privacy/">Privacy</a>
        </footer>
    </div>
{THEME_JS}
{SHARE_JS}
</body>
</html>'''

    return html


# ============================================================
# CITY INDEX PAGE
# ============================================================

def generate_city_index():
    sorted_cities = sorted(coliData.items(), key=lambda x: x[1], reverse=True)

    city_rows = ''
    for i, (city, coli) in enumerate(sorted_cities, 1):
        country = cityCountry.get(city, '')
        currency = cityToCurrency.get(city, 'USD')
        region = get_region(city)
        slug = slugify(city)
        num_neighborhoods = len(cityNeighborhoods.get(city, {}))

        city_rows += f'''
                <tr>
                    <td style="font-weight: 600;">
                        <a href="/city/{slug}" style="color: #2563eb; text-decoration: none;">{city}</a>
                    </td>
                    <td>{country}</td>
                    <td style="text-align: center; font-weight: 600;">{coli}</td>
                    <td style="text-align: center;" class="col-currency">{currency}</td>
                    <td style="text-align: center;" class="col-neighborhoods">{num_neighborhoods or "—"}</td>
                </tr>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cost of Living by City {CURRENT_YEAR} — Compare {len(coliData)} Cities Worldwide | salary:converter</title>
    <meta name="description" content="Compare cost of living across {len(coliData)} cities worldwide. See COLI indices, salary equivalents, neighborhood data, and tax rates for every city we track.">
    <meta name="keywords" content="cost of living by city, city comparison, COLI index, cost of living ranking {CURRENT_YEAR}, cheapest cities, most expensive cities">
    <meta name="author" content="salary:converter">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/city/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://salary-converter.com/city/">
    <meta property="og:title" content="Cost of Living by City {CURRENT_YEAR} — {len(coliData)} Cities Ranked">
    <meta property="og:description" content="Compare cost of living, salaries, and neighborhoods across {len(coliData)} cities worldwide.">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Cost of Living by City {CURRENT_YEAR}",
        "description": "Compare cost of living across {len(coliData)} cities worldwide",
        "url": "https://salary-converter.com/city/",
        "isPartOf": {{
            "@type": "WebSite",
            "name": "salary:converter",
            "url": "https://salary-converter.com"
        }}
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--bg); color: var(--text-primary); min-height: 100vh;
            padding: 20px 12px; -webkit-font-smoothing: antialiased;
            transition: background 0.3s, color 0.3s;
        }}
        .page-wrapper {{ max-width: 960px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .hero {{
            background: var(--card-bg); border-radius: 20px; padding: 40px 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 8px; }}
        .hero p {{ color: var(--text-secondary); font-size: 1rem; }}
        .search-box {{
            margin-top: 20px; position: relative; max-width: 400px; margin-left: auto; margin-right: auto;
        }}
        .search-box input {{
            width: 100%; padding: 12px 16px; border: 2px solid var(--border);
            border-radius: 12px; font-size: 0.95rem; font-family: inherit;
            outline: none; transition: border-color 0.2s;
            background: var(--card-bg); color: var(--text-primary);
        }}
        .search-box input:focus {{ border-color: var(--accent); }}
        .content-card {{
            background: var(--card-bg); border-radius: 20px; padding: 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
        }}
        table {{
            width: 100%; border-collapse: collapse; font-size: 0.88rem;
        }}
        table th {{
            text-align: left; padding: 10px 12px; font-size: 0.75rem;
            text-transform: uppercase; letter-spacing: 0.5px;
            color: var(--text-secondary); border-bottom: 2px solid var(--border); font-weight: 600;
            position: sticky; top: 0; background: var(--card-bg);
        }}
        table td {{
            padding: 10px 12px; border-bottom: 1px solid var(--border-light);
        }}
        table tr:hover td {{ background: var(--table-stripe); }}
        .page-footer {{
            text-align: center; padding: 32px 0 16px; border-top: 1px solid var(--border);
            display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: var(--text-secondary); text-decoration: none;
        }}
        .page-footer a:hover {{ color: var(--accent); }}
        .col-currency {{ }}
        .col-neighborhoods {{ }}
        @media (max-width: 768px) {{
            body {{ padding: 0; background: var(--bg); }}
            .page-wrapper {{ padding: 0 16px; }}
            .nav-links {{ padding-right: 48px; }}
            .hero {{ border-radius: 0; padding: 32px 16px; box-shadow: none; }}
            .hero h1 {{ font-size: 1.5rem; }}
            .content-card {{ border-radius: 16px; padding: 12px; overflow-x: auto; -webkit-overflow-scrolling: touch; }}
            table {{ font-size: 0.78rem; min-width: 0; }}
            table th, table td {{ padding: 8px 5px; white-space: nowrap; }}
            .col-currency {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <section class="hero">
            <h1>Cost of Living by City {CURRENT_YEAR}</h1>
            <p>{len(coliData)} cities ranked by cost of living index (New York = 100)</p>
            <div class="search-box">
                <input type="text" id="citySearch" placeholder="Search cities..." oninput="filterCities(this.value)">
            </div>
        </section>

        <section class="content-card">
            <table id="cityTable">
                <thead>
                    <tr>
                        <th>City</th>
                        <th>Country</th>
                        <th style="text-align: center;">COLI</th>
                        <th style="text-align: center;" class="col-currency">Currency</th>
                        <th style="text-align: center;" class="col-neighborhoods">Neighborhoods</th>
                    </tr>
                </thead>
                <tbody>{city_rows}
                </tbody>
            </table>
        </section>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/compare/">City Comparisons</a>
            <a href="/blog/">Blog</a>
            <a href="/privacy/">Privacy</a>
        </footer>
    </div>

    <script>
        function filterCities(query) {{
            const rows = document.querySelectorAll('#cityTable tbody tr');
            const q = query.toLowerCase();
            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(q) ? '' : 'none';
            }});
        }}
    </script>
{THEME_JS}
</body>
</html>'''

    return html


# ============================================================
# COMPARE INDEX PAGE
# ============================================================

def generate_compare_index(comparison_pairs, featured_pairs=None):
    if featured_pairs is None:
        featured_pairs = set()

    # Build featured section — limit to 10 cards (5 rows of 2)
    featured_html = ''
    featured_shown = 0
    for city1, city2 in comparison_pairs:
        if featured_shown >= 10:
            break
        if (city1, city2) in featured_pairs or (city2, city1) in featured_pairs:
            slug1 = slugify(city1)
            slug2 = slugify(city2)
            coli1 = coliData[city1]
            coli2 = coliData[city2]
            diff = abs(coli2 - coli1) / max(coli1, coli2) * 100
            featured_html += f'''
                <a href="/compare/{slug1}-vs-{slug2}" class="compare-card">
                    <div class="compare-card-cities">{city1} <span class="vs">vs</span> {city2}</div>
                    <div class="compare-card-stats">COLI: {coli1} vs {coli2} &middot; {diff:.0f}% difference</div>
                </a>'''
            featured_shown += 1

    total = len(comparison_pairs)

    # Build city options for dropdowns
    city_options = '\n'.join(f'                        <option value="{city}">{city}</option>' for city in sorted(coliData.keys()))

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>City Comparisons — {total:,} Cost of Living & Salary Comparisons {CURRENT_YEAR}</title>
    <meta name="description" content="Compare cost of living and salaries between any two cities. {total:,} city-to-city comparisons with neighborhoods, tax rates, and purchasing power.">
    <meta name="author" content="salary:converter">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/compare/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://salary-converter.com/compare/">
    <meta property="og:title" content="{total:,} City Cost of Living Comparisons {CURRENT_YEAR}">
    <meta property="og:description" content="Side-by-side comparison of salaries and cost of living between any two of 101 cities worldwide.">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "City Cost of Living Comparisons",
        "description": "{total:,} city-to-city comparisons across 101 cities worldwide",
        "url": "https://salary-converter.com/compare/",
        "numberOfItems": {total}
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--bg); color: var(--text-primary); min-height: 100vh;
            padding: 20px 12px; -webkit-font-smoothing: antialiased;
            transition: background 0.3s, color 0.3s;
        }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .hero {{
            background: var(--card-bg); border-radius: 20px; padding: 40px 32px;
            box-shadow: var(--shadow); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 8px; }}
        .hero p {{ color: var(--text-secondary); font-size: 1rem; margin-bottom: 24px; }}
        .compare-form {{
            display: flex; align-items: center; justify-content: center;
            gap: 12px; flex-wrap: wrap;
        }}
        .compare-form-label {{
            font-size: 1rem; font-weight: 600; color: var(--text-primary);
        }}
        .city-select {{
            padding: 12px 16px; border: 2px solid var(--border);
            border-radius: 12px; font-size: 0.95rem; font-family: inherit;
            outline: none; transition: border-color 0.2s;
            background: var(--stat-card-bg); color: var(--text-primary);
            cursor: pointer; min-width: 180px;
            -webkit-appearance: none; -moz-appearance: none; appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2386868b' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: right 14px center;
            padding-right: 36px;
        }}
        .city-select:focus {{ border-color: var(--accent); background-color: var(--card-bg); }}
        .compare-btn {{
            padding: 12px 28px; border: none; border-radius: 12px;
            background: var(--accent); color: white; font-size: 0.95rem;
            font-weight: 600; font-family: inherit; cursor: pointer;
            transition: background 0.2s, transform 0.2s;
        }}
        .compare-btn:hover {{ background: var(--accent-hover); transform: translateY(-1px); }}
        .compare-btn:disabled {{
            opacity: 0.5; cursor: not-allowed; transform: none;
        }}
        .compare-error {{
            color: #ef4444; font-size: 0.82rem; margin-top: 12px;
            min-height: 1.2em;
        }}
        .section-title {{
            font-size: 1.1rem; font-weight: 700; margin: 32px 0 16px;
            letter-spacing: -0.3px;
        }}
        .compare-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
        }}
        .compare-card {{
            background: var(--card-bg); border-radius: 14px; padding: 18px;
            box-shadow: var(--shadow); text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s; display: block;
        }}
        .compare-card:hover {{
            transform: translateY(-2px); box-shadow: 0 6px 24px rgba(0,0,0,0.1);
        }}
        .compare-card-cities {{
            font-size: 0.9rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;
        }}
        .compare-card-cities .vs {{
            color: var(--accent); font-size: 0.75rem; margin: 0 4px;
        }}
        .compare-card-stats {{
            font-size: 0.75rem; color: var(--text-secondary);
        }}
        .page-footer {{
            text-align: center; padding: 32px 0 16px; margin-top: 24px;
            border-top: 1px solid var(--border);
            display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: var(--text-secondary); text-decoration: none;
        }}
        .page-footer a:hover {{ color: var(--accent); }}
        @media (max-width: 768px) {{
            body {{ padding: 0; background: var(--bg); }}
            .page-wrapper {{ padding: 0 16px; }}
            .nav-links {{ padding-right: 48px; }}
            .hero {{ border-radius: 0; padding: 32px 16px; box-shadow: none; }}
            .hero h1 {{ font-size: 1.5rem; }}
            .compare-form {{ flex-direction: column; gap: 10px; }}
            .city-select {{ min-width: 100%; }}
            .compare-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="page-wrapper">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <section class="hero">
            <h1>City Comparisons</h1>
            <p>{total:,} city-to-city comparisons across 101 cities</p>
            <div class="compare-form">
                <span class="compare-form-label">Compare</span>
                <select id="cityA" class="city-select">
                    <option value="">Select a city...</option>
{city_options}
                </select>
                <span class="compare-form-label">to</span>
                <select id="cityB" class="city-select">
                    <option value="">Select a city...</option>
{city_options}
                </select>
                <button id="compareBtn" class="compare-btn" disabled>Compare</button>
            </div>
            <div class="compare-error" id="compareError"></div>
        </section>

        <h2 class="section-title">Popular Comparisons</h2>
        <div class="compare-grid">{featured_html}
        </div>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/">All Cities</a>
            <a href="/blog/">Blog</a>
            <a href="/privacy/">Privacy</a>
        </footer>
    </div>

    <script>
    (function() {{
        var cityA = document.getElementById('cityA');
        var cityB = document.getElementById('cityB');
        var btn = document.getElementById('compareBtn');
        var err = document.getElementById('compareError');

        function slugify(s) {{
            return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        }}

        function validate() {{
            var a = cityA.value, b = cityB.value;
            if (!a || !b) {{
                btn.disabled = true;
                err.textContent = '';
            }} else if (a === b) {{
                btn.disabled = true;
                err.textContent = 'Please select two different cities.';
            }} else {{
                btn.disabled = false;
                err.textContent = '';
            }}
        }}

        cityA.addEventListener('change', validate);
        cityB.addEventListener('change', validate);

        btn.addEventListener('click', function() {{
            var a = cityA.value, b = cityB.value;
            if (!a || !b || a === b) return;
            var cities = [a, b].sort();
            var url = '/compare/' + slugify(cities[0]) + '-vs-' + slugify(cities[1]);
            window.location.href = url;
        }});
    }})();
    </script>
{THEME_JS}
</body>
</html>'''

    return html


# ============================================================
# NEIGHBORHOOD PAGE TEMPLATE
# ============================================================

def generate_neighborhood_page(city, neighborhood, multiplier):
    """Generate an individual neighborhood page"""
    city_slug = slugify(city)
    nhood_slug = slugify(neighborhood)
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    city_coli = coliData[city]
    nhood_coli = round(city_coli * multiplier, 1)
    rate_to_local = exchangeRates[currency] / exchangeRates['USD']

    # Multiplier description
    pct_diff = (multiplier - 1) * 100
    sign = '+' if pct_diff >= 0 else ''
    if pct_diff > 20:
        cost_desc = 'significantly above'
    elif pct_diff > 5:
        cost_desc = 'above'
    elif pct_diff > -5:
        cost_desc = 'near'
    elif pct_diff > -20:
        cost_desc = 'below'
    else:
        cost_desc = 'well below'

    # Rank within city
    all_nhoods = cityNeighborhoods.get(city, {})
    sorted_nhoods = sorted(all_nhoods.items(), key=lambda x: x[1], reverse=True)
    rank_in_city = 1
    for i, (n, m) in enumerate(sorted_nhoods):
        if n == neighborhood:
            rank_in_city = i + 1
            break
    total_in_city = len(sorted_nhoods)

    # Estimated rent (scaled from city rent)
    city_rent = cityRent1BR.get(city, 0)
    nhood_rent = city_rent * multiplier
    nhood_rent_local = nhood_rent * rate_to_local
    fmt_rent = format_currency_amount(nhood_rent_local, currency)

    # Salary equivalents from reference cities
    ref_cities = ['New York', 'London', 'Dubai']
    salary_equivs = []
    for ref in ref_cities:
        if ref == city:
            continue
        ref_currency = cityToCurrency[ref]
        ref_rate = exchangeRates[ref_currency] / exchangeRates['USD']
        equiv_usd = 75000 * (nhood_coli / coliData[ref])
        equiv_local = equiv_usd * ref_rate
        salary_equivs.append({
            'city': ref,
            'formatted': format_currency_amount(equiv_local, ref_currency),
            'currency': ref_currency,
        })

    # Salary equiv rows
    salary_equiv_rows = ''
    for se in salary_equivs:
        se_city = se['city']
        se_fmt = se['formatted']
        se_cur = se['currency']
        salary_equiv_rows += f'''
                        <tr>
                            <td style="font-weight: 500;">{se_city}</td>
                            <td style="text-align: center;">{se_cur}</td>
                            <td style="text-align: right; font-weight: 600;">{se_fmt}</td>
                        </tr>'''

    # Comparison with other neighborhoods in same city (up to 5)
    other_nhoods = [(n, m) for n, m in sorted_nhoods if n != neighborhood][:5]
    nhood_comparison_rows = ''
    for on_name, on_mult in other_nhoods:
        on_coli = round(city_coli * on_mult, 1)
        on_pct = (on_mult - 1) * 100
        on_sign = '+' if on_pct >= 0 else ''
        on_color = '#22c55e' if on_pct < 0 else '#2563eb' if on_pct < 15 else '#f59e0b' if on_pct < 30 else '#ef4444'
        on_slug = slugify(on_name)
        nhood_comparison_rows += f'''
                        <tr>
                            <td><a href="/city/{city_slug}/{on_slug}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{on_name}</a></td>
                            <td style="text-align: center;">{on_coli}</td>
                            <td style="text-align: center;">{on_mult:.2f}x</td>
                            <td style="text-align: right;"><span style="color: {on_color}; font-weight: 600;">{on_sign}{on_pct:.0f}%</span></td>
                        </tr>'''

    # Color for this neighborhood
    nhood_color = '#22c55e' if pct_diff < 0 else '#2563eb' if pct_diff < 15 else '#f59e0b' if pct_diff < 30 else '#ef4444'

    # Build comparison links for this neighborhood
    nhood_comp_pairs = get_neighborhood_comparison_pairs(city)
    compare_links_html = ''
    for cn1, cm1, cn2, cm2 in nhood_comp_pairs:
        if cn1 == neighborhood or cn2 == neighborhood:
            cn1_slug = slugify(cn1)
            cn2_slug = slugify(cn2)
            other_n = cn2 if cn1 == neighborhood else cn1
            compare_links_html += f'<a href="/compare/{city_slug}/{cn1_slug}-vs-{cn2_slug}" style="display: inline-block; padding: 6px 14px; background: #f5f5f7; border-radius: 100px; font-size: 0.8rem; color: #1d1d1f; text-decoration: none; margin: 4px;">{neighborhood} vs {other_n}</a>\n'

    # Build city-level comparison links
    city_comp_links_html = ''
    # Check which city-vs-city comparisons include this city
    popular_pairs = [
        ('London', 'New York'), ('London', 'Dubai'), ('London', 'Singapore'),
        ('London', 'Paris'), ('New York', 'San Francisco'), ('New York', 'Los Angeles'),
        ('Dubai', 'Singapore'), ('Singapore', 'Hong Kong'), ('Tokyo', 'Seoul'),
        ('Paris', 'Berlin'), ('Sydney', 'Melbourne'), ('Bangkok', 'Chiang Mai'),
    ]
    for c1, c2 in popular_pairs:
        if c1 == city or c2 == city:
            # Sort alphabetically for URL (files are named alphabetically)
            sorted_pair = sorted([c1, c2])
            s1 = slugify(sorted_pair[0])
            s2 = slugify(sorted_pair[1])
            city_comp_links_html += f'<a href="/compare/{s1}-vs-{s2}" style="display: inline-block; padding: 6px 14px; background: #f5f5f7; border-radius: 100px; font-size: 0.8rem; color: #1d1d1f; text-decoration: none; margin: 4px;">{c1} vs {c2}</a>\n'

    # Build cross-city similar neighborhood links (same cost tier)
    similar_global_html = ''
    similar_global = []
    for other_city, other_nhoods in cityNeighborhoods.items():
        if other_city == city:
            continue
        other_coli = coliData[other_city]
        for on_name, on_mult in other_nhoods.items():
            on_abs = other_coli * on_mult
            if abs(on_abs - nhood_coli) < 5 and abs(on_mult - multiplier) < 0.15:
                similar_global.append((on_name, other_city, on_abs, on_mult))
    # Sort by closest COLI match, take top 6
    similar_global.sort(key=lambda x: abs(x[2] - nhood_coli))
    for sg_name, sg_city, sg_coli, sg_mult in similar_global[:6]:
        sg_cs = slugify(sg_city)
        sg_ns = slugify(sg_name)
        similar_global_html += f'<a href="/city/{sg_cs}/{sg_ns}" style="display: inline-block; padding: 6px 14px; background: #f5f5f7; border-radius: 100px; font-size: 0.8rem; color: #1d1d1f; text-decoration: none; margin: 4px;">{sg_name}, {sg_city}</a>\n'

    # Tax & Deductions breakdown for this neighborhood
    nhood_ref_salary_local = 75000 * (nhood_coli / 100) * rate_to_local
    nhood_ded_result = calculate_all_deductions(nhood_ref_salary_local, country, city, is_expat=False, neighborhood=neighborhood)
    nhood_deduction_rows = ''
    nhood_fmt_ref_salary = format_currency_amount(nhood_ref_salary_local, currency)
    nhood_fmt_net = format_currency_amount(nhood_ded_result['net'], currency)
    nhood_total_ded_rate = nhood_ded_result['total_rate']
    if nhood_ded_result['items']:
        max_ded_r = max((item['rate'] for item in nhood_ded_result['items']), default=1) or 1
        for item in nhood_ded_result['items']:
            dcolor = DEDUCTION_COLORS.get(item['key'], '#6b7280')
            bar_w = round((item['rate'] / max_ded_r) * 100) if max_ded_r > 0 else 0
            bar_w = max(bar_w, 2)
            fmt_amt = format_currency_amount(item['amount'], currency)
            nhood_deduction_rows += '<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">'
            nhood_deduction_rows += '<div style="width: 200px; font-size: 0.85rem; font-weight: 500; color: var(--text-body, #4a4a4c);">' + item['label'] + '</div>'
            nhood_deduction_rows += '<div style="flex: 1; background: var(--border-light, #f0f0f2); border-radius: 6px; height: 12px; overflow: hidden;">'
            nhood_deduction_rows += '<div style="width: ' + str(bar_w) + '%; height: 100%; background: ' + dcolor + '; border-radius: 6px;"></div>'
            nhood_deduction_rows += '</div>'
            nhood_deduction_rows += '<div style="width: 48px; text-align: right; font-size: 0.85rem; font-weight: 600; color: var(--text-primary, #1d1d1f);">' + str(item['rate']) + '%</div>'
            nhood_deduction_rows += '</div>'

    nhood_deduction_section = ''
    if nhood_ded_result['items']:
        nhood_deduction_section = f'''<div class="card">
            <h2>Tax &amp; Deductions in {neighborhood}</h2>
            <p style="font-size: 0.85rem; color: var(--text-secondary, #86868b); margin-bottom: 16px;">Estimated annual deductions on a <strong>{nhood_fmt_ref_salary}</strong> salary in {neighborhood}, {city} (local employee).</p>
            {nhood_deduction_rows}
            <div style="border-top: 1px solid var(--border, #e5e5ea); margin-top: 16px; padding-top: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="font-size: 0.9rem; font-weight: 600; color: var(--text-primary, #1d1d1f);">Total Deductions: {nhood_total_ded_rate}%</span>
                </div>
                <div>
                    <span style="font-size: 0.9rem; color: var(--text-secondary, #86868b);">Est. Take-Home: </span>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #22c55e;">{nhood_fmt_net}/yr</span>
                </div>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-secondary, #86868b); margin-top: 12px; margin-bottom: 0;">Rates shown are for a local employee. Use the <a href="/" style="color: var(--accent, #2563eb);">salary converter</a> for expat calculations.</p>
        </div>'''

    # FAQ answers
    if pct_diff > 10:
        expensive_answer = f'Yes, {neighborhood} is one of the more expensive neighborhoods in {city}. It costs about {sign}{pct_diff:.0f}% more than the city average, ranking #{rank_in_city} out of {total_in_city} neighborhoods.'
    elif pct_diff > -5:
        expensive_answer = f'{neighborhood} is near the city average for {city}. Costs are about {sign}{pct_diff:.0f}% vs the average, making it a mid-range neighborhood.'
    else:
        expensive_answer = f'{neighborhood} is one of the more affordable neighborhoods in {city}. It costs about {pct_diff:.0f}% less than the city average, ranking #{rank_in_city} out of {total_in_city} neighborhoods.'

    avg_comparison = f'The cost of living in {neighborhood} is {cost_desc} the {city} average. With a multiplier of {multiplier:.2f}x, everyday expenses including rent, food, and transportation are {sign}{pct_diff:.0f}% compared to the city baseline.'

    # Share bar
    share_text = f'{neighborhood}, {city} cost of living index: {nhood_coli} ({sign}{pct_diff:.0f}% vs city avg). Compare on salary:converter'
    share_bar_html = build_share_bar(share_text, f'https://salary-converter.com/city/{city_slug}/{nhood_slug}')

    # --- Enriched prose content ---
    # Expense breakdown (scaled from city)
    expenses = get_expense_breakdown(city)
    nhood_housing_pct = min(55, max(18, round(expenses['housing'] * multiplier)))
    nhood_food_pct = expenses['food']
    nhood_transport_pct = expenses['transport']

    # Monthly rent in local currency
    monthly_rent_local = nhood_rent_local

    # Salary needed to live comfortably (50/30/20: rent = 30% of gross)
    comfortable_annual = (monthly_rent_local * 12) / 0.30
    fmt_comfortable = format_currency_amount(comfortable_annual, currency)

    above_below = 'above' if pct_diff > 0 else 'below'
    meta_desc = f'{abs(pct_diff):.0f}% {above_below} {city} avg. 1BR: ~{fmt_rent}/mo. #{rank_in_city} of {total_in_city} neighborhoods. Salary needed & full cost breakdown inside.'

    # Pick 3 representative job titles and show local salaries
    representative_jobs = ['Software Engineer', 'Teacher', 'Nurse']
    job_salary_lines = ''
    for job_title in representative_jobs:
        ranges = salaryRanges.get(job_title, {})
        if not ranges:
            continue
        local_mid = ranges['mid'] * (nhood_coli / 100) * rate_to_local
        fmt_job_salary = format_currency_amount(local_mid, currency)
        job_salary_lines += f'<li>A <strong>{job_title}</strong> earns approximately <strong>{fmt_job_salary}</strong> per year.</li>\n'

    # Cost tier description
    tier_pct = rank_in_city / total_in_city
    if tier_pct <= 0.1:
        tier_desc = f'the most expensive area in {city}'
        tier_context = f'Only the top {rank_in_city} of {total_in_city} neighborhoods cost more.'
    elif tier_pct <= 0.25:
        tier_desc = f'one of the pricier neighborhoods in {city}'
        tier_context = f'It ranks #{rank_in_city} out of {total_in_city} areas by cost.'
    elif tier_pct <= 0.5:
        tier_desc = f'a moderately-priced area within {city}'
        tier_context = f'It sits around the middle of the pack at #{rank_in_city} out of {total_in_city} neighborhoods.'
    elif tier_pct <= 0.75:
        tier_desc = f'a relatively affordable area in {city}'
        tier_context = f'At #{rank_in_city} of {total_in_city}, it is below the city average in cost.'
    else:
        tier_desc = f'one of the most affordable neighborhoods in {city}'
        tier_context = f'Ranked #{rank_in_city} of {total_in_city}, it offers some of the lowest costs in the city.'

    # Most affordable and most expensive for context
    cheapest_name = sorted_nhoods[-1][0] if sorted_nhoods else ''
    cheapest_mult = sorted_nhoods[-1][1] if sorted_nhoods else 1.0
    priciest_name = sorted_nhoods[0][0] if sorted_nhoods else ''
    priciest_mult = sorted_nhoods[0][1] if sorted_nhoods else 1.0
    cheapest_rent = city_rent * cheapest_mult * rate_to_local
    priciest_rent = city_rent * priciest_mult * rate_to_local
    fmt_cheapest_rent = format_currency_amount(cheapest_rent, currency)
    fmt_priciest_rent = format_currency_amount(priciest_rent, currency)

    # Build the prose section
    prose_section = f'''<div class="card neighborhood-guide">
            <h2>Living in {neighborhood}, {city}</h2>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75; margin-bottom: 14px;">
                {neighborhood} is {tier_desc}, with a cost of living index of <strong>{nhood_coli}</strong> — that is <strong>{sign}{pct_diff:.0f}%</strong> compared to the {city} average. {tier_context} Estimated rent for a one-bedroom apartment here is around <strong>{fmt_rent}/month</strong>, compared to a range of {fmt_cheapest_rent} in {cheapest_name} to {fmt_priciest_rent} in {priciest_name}.
            </p>
            <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 10px;">Monthly Budget Breakdown</h3>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75; margin-bottom: 14px;">
                For a typical resident of {neighborhood}, housing takes up roughly <strong>{nhood_housing_pct}%</strong> of monthly expenses. Food and groceries account for about <strong>{nhood_food_pct}%</strong>, while transportation costs around <strong>{nhood_transport_pct}%</strong>. To live comfortably here — meaning rent stays at or below 30% of gross income — you would need an annual salary of approximately <strong>{fmt_comfortable}</strong> before tax.
            </p>
            <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 10px;">Typical Salaries in {neighborhood}</h3>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75; margin-bottom: 8px;">
                Salaries in {neighborhood} reflect the local cost of living. Based on the neighborhood COLI of {nhood_coli}:
            </p>
            <ul style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.85; margin-bottom: 14px; padding-left: 20px;">
                {job_salary_lines}
            </ul>
            <p style="font-size: 0.92rem; color: var(--text-body, #4a4a4c); line-height: 1.75;">
                After tax and deductions of <strong>{nhood_total_ded_rate}%</strong> in {country}, take-home pay for someone earning {fmt_comfortable} would be roughly <strong>{format_currency_amount(comfortable_annual * (1 - nhood_total_ded_rate / 100), currency)}/year</strong>. Use the <a href="/" style="color: var(--accent, #2563eb);">salary converter</a> to calculate an exact figure for your situation, including expat-specific tax adjustments.
            </p>
        </div>'''

    # Data sources section with authoritative external links
    country_sources = {
        'United States': [
            ('U.S. Bureau of Labor Statistics', 'https://www.bls.gov/cpi/'),
            ('U.S. Census Bureau', 'https://www.census.gov/topics/income-poverty.html'),
        ],
        'United Kingdom': [
            ('UK Office for National Statistics', 'https://www.ons.gov.uk/economy/inflationandpriceindices'),
            ('HM Revenue &amp; Customs', 'https://www.gov.uk/government/organisations/hm-revenue-customs'),
        ],
        'Germany': [
            ('Statistisches Bundesamt (Destatis)', 'https://www.destatis.de/EN/Themes/Prices/_node.html'),
            ('Bundesagentur für Arbeit', 'https://www.arbeitsagentur.de/'),
        ],
        'Japan': [
            ('Statistics Bureau of Japan', 'https://www.stat.go.jp/english/data/cpi/index.html'),
            ('Ministry of Health, Labour and Welfare', 'https://www.mhlw.go.jp/english/'),
        ],
        'France': [
            ('INSEE (Institut national de la statistique)', 'https://www.insee.fr/en/accueil'),
            ('Ministère de l\'Économie', 'https://www.economie.gouv.fr/'),
        ],
        'Australia': [
            ('Australian Bureau of Statistics', 'https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation'),
            ('Australian Taxation Office', 'https://www.ato.gov.au/'),
        ],
        'Canada': [
            ('Statistics Canada', 'https://www.statcan.gc.ca/en/subjects-start/prices_and_price_indexes'),
            ('Canada Revenue Agency', 'https://www.canada.ca/en/revenue-agency.html'),
        ],
        'Singapore': [
            ('Singapore Department of Statistics', 'https://www.singstat.gov.sg/'),
            ('Inland Revenue Authority of Singapore', 'https://www.iras.gov.sg/'),
        ],
        'UAE': [
            ('Federal Competitiveness and Statistics Centre', 'https://fcsc.gov.ae/en-us'),
        ],
        'South Korea': [
            ('Statistics Korea (KOSTAT)', 'https://kostat.go.kr/portal/eng/index.action'),
        ],
        'Spain': [
            ('Instituto Nacional de Estadística (INE)', 'https://www.ine.es/en/index.htm'),
        ],
        'Italy': [
            ('Istituto Nazionale di Statistica (ISTAT)', 'https://www.istat.it/en/'),
        ],
        'Switzerland': [
            ('Swiss Federal Statistical Office', 'https://www.bfs.admin.ch/bfs/en/home.html'),
        ],
        'Netherlands': [
            ('Statistics Netherlands (CBS)', 'https://www.cbs.nl/en-gb'),
        ],
    }
    # Get country-specific + universal sources
    c_sources = country_sources.get(country, [])
    # Always add OECD
    all_sources = c_sources + [('OECD Better Life Index', 'https://www.oecdbetterlifeindex.org/')]
    source_links = ' · '.join([f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: var(--accent, #2563eb); text-decoration: none;">{name}</a>' for name, url in all_sources])
    sources_section = f'''<div style="margin-top: 24px; padding: 16px; background: var(--stat-card-bg, #f5f5f7); border-radius: 12px; font-size: 0.78rem; color: var(--text-secondary, #86868b); line-height: 1.7;">
            <strong>Data Sources:</strong> Cost of living indices based on crowd-sourced price data and official statistics. Tax calculations follow {CURRENT_YEAR} rates. Sources include {source_links}. Figures are estimates and may vary based on individual circumstances.
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{neighborhood}, {city}: {fmt_rent}/mo Rent ({CURRENT_YEAR})</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/city/{city_slug}/{nhood_slug}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{neighborhood}, {city}: {fmt_rent}/mo Rent ({CURRENT_YEAR})">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://salary-converter.com/city/{city_slug}/{nhood_slug}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Place",
        "name": "{neighborhood}, {city}",
        "containedInPlace": {{
            "@type": "City",
            "name": "{city}",
            "containedInPlace": {{
                "@type": "Country",
                "name": "{country}"
            }}
        }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"}},
            {{"@type": "ListItem", "position": 2, "name": "Cities", "item": "https://salary-converter.com/city/"}},
            {{"@type": "ListItem", "position": 3, "name": "{city}", "item": "https://salary-converter.com/city/{city_slug}"}},
            {{"@type": "ListItem", "position": 4, "name": "{neighborhood}"}}
        ]
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "Is {neighborhood} expensive in {city}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{expensive_answer}"
                }}
            }},
            {{
                "@type": "Question",
                "name": "How does {neighborhood} compare to the {city} average?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{avg_comparison}"
                }}
            }}
        ]
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text-primary); -webkit-font-smoothing: antialiased; transition: background 0.3s, color 0.3s; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .breadcrumb {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        .hero {{ text-align: center; margin-bottom: 40px; }}
        .hero h1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .hero .subtitle {{ font-size: 1.05rem; color: var(--text-secondary); }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 100px; font-size: 0.8rem; font-weight: 600; margin-top: 12px; }}
        .card {{ background: var(--card-bg); border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: var(--shadow); }}
        .card h2 {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 16px; letter-spacing: -0.3px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; }}
        .stat-item {{ text-align: center; padding: 16px; background: var(--stat-card-bg); border-radius: 12px; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }}
        .stat-label {{ font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); padding: 8px 12px; border-bottom: 2px solid var(--border); }}
        td {{ padding: 10px 12px; border-bottom: 1px solid var(--border-light); font-size: 0.85rem; }}
        .cta-box {{ text-align: center; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border-radius: 16px; padding: 32px; margin: 32px 0; }}
        .cta-box h2 {{ color: white; margin-bottom: 8px; }}
        .cta-box p {{ color: rgba(255,255,255,0.85); font-size: 0.9rem; margin-bottom: 16px; }}
        .cta-btn {{ display: inline-block; background: white; color: #2563eb; padding: 12px 28px; border-radius: 100px; font-weight: 600; text-decoration: none; font-size: 0.9rem; }}
        .faq-item {{ margin-bottom: 20px; }}
        .faq-item h3 {{ font-size: 1rem; font-weight: 600; margin-bottom: 8px; }}
        .faq-item p {{ font-size: 0.9rem; color: var(--text-body); line-height: 1.6; }}
        .page-footer {{ text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border); display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px; }}
        .page-footer a {{ font-size: 0.85rem; color: var(--accent); text-decoration: none; font-weight: 500; }}
        @media (max-width: 600px) {{
            .hero h1 {{ font-size: 1.5rem; }}
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
            .card {{ padding: 20px; }}
        }}
        .share-bar {{
            display: flex; align-items: center; gap: 8px;
            margin: 16px 0 20px; padding: 12px 16px;
            background: var(--stat-card-bg, #f5f5f7); border-radius: 12px;
        }}
        .share-bar-label {{
            font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);
            text-transform: uppercase; letter-spacing: 0.5px; margin-right: 4px;
        }}
        .share-btn {{
            display: flex; align-items: center; justify-content: center;
            width: 34px; height: 34px; border-radius: 50%;
            border: 1px solid var(--border, #e5e5ea); background: var(--card-bg, #fff);
            color: var(--text-secondary, #86868b); cursor: pointer; transition: all 0.2s;
            padding: 0;
        }}
        .share-btn:hover {{ color: var(--accent); border-color: var(--accent); transform: scale(1.08); }}
        .share-btn.copied {{ color: #22c55e; border-color: #22c55e; }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/city/">Cities</a> &rsaquo; <a href="/city/{city_slug}">{city}</a> &rsaquo; {neighborhood}
        </div>

        <section class="hero">
            <h1>{neighborhood}</h1>
            <p class="subtitle">{city}, {country}</p>
            <span class="badge" style="background: {nhood_color}15; color: {nhood_color};">{sign}{pct_diff:.0f}% vs {city} avg</span>
        </section>
        {share_bar_html}

        {prose_section}

        <div class="card">
            <h2>Key Stats</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{nhood_coli}</div>
                    <div class="stat-label">COLI Index</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{multiplier:.2f}x</div>
                    <div class="stat-label">vs City Avg</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{fmt_rent}</div>
                    <div class="stat-label">Est. 1BR Rent</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">#{rank_in_city}</div>
                    <div class="stat-label">of {total_in_city} Areas</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{nhood_total_ded_rate}%</div>
                    <div class="stat-label">Total Deductions</div>
                </div>
            </div>
        </div>

        {nhood_deduction_section}

        <div class="card">
            <h2>Salary Equivalents</h2>
            <p style="font-size: 0.85rem; color: #86868b; margin-bottom: 16px;">What a $75,000 USD salary in {neighborhood} would need to be elsewhere:</p>
            <table>
                <thead>
                    <tr>
                        <th>City</th>
                        <th style="text-align: center;">Currency</th>
                        <th style="text-align: right;">Equivalent</th>
                    </tr>
                </thead>
                <tbody>{salary_equiv_rows}
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>Other Neighborhoods in {city}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Neighborhood</th>
                        <th style="text-align: center;">COLI</th>
                        <th style="text-align: center;">Multiplier</th>
                        <th style="text-align: right;">vs Avg</th>
                    </tr>
                </thead>
                <tbody>{nhood_comparison_rows}
                </tbody>
            </table>
            <p style="font-size: 0.8rem; color: #86868b; margin-top: 12px;"><a href="/city/{city_slug}" style="color: #2563eb; text-decoration: none;">View all {total_in_city} neighborhoods in {city} &rarr;</a></p>
        </div>

        <div class="cta-box">
            <h2>Convert Your Salary</h2>
            <p>See exactly what you need to earn in {neighborhood}, {city} to maintain your lifestyle.</p>
            <a href="/" class="cta-btn">Open Salary Converter</a>
        </div>

        {f"""<div class="card">
            <h2>Compare {neighborhood}</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                {compare_links_html}
            </div>
        </div>""" if compare_links_html else ""}

        {f"""<div class="card">
            <h2>{city} City Comparisons</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                {city_comp_links_html}
            </div>
        </div>""" if city_comp_links_html else ""}

        {f"""<div class="card">
            <h2>Similar Neighborhoods Worldwide</h2>
            <p style="font-size: 0.85rem; color: #86868b; margin-bottom: 12px;">Neighborhoods with a similar cost of living to {neighborhood}:</p>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                {similar_global_html}
            </div>
        </div>""" if similar_global_html else ""}

        <div class="card">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-item">
                <h3>Is {neighborhood} expensive in {city}?</h3>
                <p>{expensive_answer}</p>
            </div>
            <div class="faq-item">
                <h3>How does {neighborhood} compare to the {city} average?</h3>
                <p>{avg_comparison}</p>
            </div>
        </div>

        {sources_section}

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/{city_slug}">{city}</a>
            <a href="/city/">All Cities</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
{THEME_JS}
{SHARE_JS}
</body>
</html>'''

    return html


# ============================================================
# NEIGHBORHOOD COMPARISON PAGE TEMPLATE
# ============================================================

def generate_neighborhood_comparison_page(city, n1, m1, n2, m2):
    """Generate a comparison page between two neighborhoods in the same city"""
    city_slug = slugify(city)
    n1_slug = slugify(n1)
    n2_slug = slugify(n2)
    country = cityCountry.get(city, '')
    currency = cityToCurrency.get(city, 'USD')
    city_coli = coliData[city]
    rate_to_local = exchangeRates[currency] / exchangeRates['USD']

    coli1 = round(city_coli * m1, 1)
    coli2 = round(city_coli * m2, 1)
    pct1 = (m1 - 1) * 100
    pct2 = (m2 - 1) * 100
    sign1 = '+' if pct1 >= 0 else ''
    sign2 = '+' if pct2 >= 0 else ''

    # Determine which is more expensive
    if m1 > m2:
        more_expensive = n1
        more_affordable = n2
        diff_pct = abs(m1 - m2) / max(m1, m2) * 100
    else:
        more_expensive = n2
        more_affordable = n1
        diff_pct = abs(m2 - m1) / max(m1, m2) * 100

    # Estimated rents
    city_rent = cityRent1BR.get(city, 0)
    rent1 = city_rent * m1 * rate_to_local
    rent2 = city_rent * m2 * rate_to_local
    fmt_rent1 = format_currency_amount(rent1, currency)
    fmt_rent2 = format_currency_amount(rent2, currency)

    # Salary equivalents for $75K
    equiv1 = 75000 * (coli1 / 100) * rate_to_local
    equiv2 = 75000 * (coli2 / 100) * rate_to_local
    fmt_equiv1 = format_currency_amount(equiv1, currency)
    fmt_equiv2 = format_currency_amount(equiv2, currency)

    # Bar widths (normalize to 100)
    max_mult = max(m1, m2)
    bar1 = int((m1 / max_mult) * 100)
    bar2 = int((m2 / max_mult) * 100)
    color1 = '#2563eb'
    color2 = '#f59e0b'

    # Other neighborhoods in this city
    all_nhoods = cityNeighborhoods.get(city, {})
    other_links = ''
    for on_name in sorted(all_nhoods.keys()):
        if on_name != n1 and on_name != n2:
            on_s = slugify(on_name)
            other_links += f'<a href="/city/{city_slug}/{on_s}" style="display: inline-block; padding: 6px 14px; background: #f5f5f7; border-radius: 100px; font-size: 0.8rem; color: #1d1d1f; text-decoration: none; margin: 4px;">{on_name}</a>\n'

    # Related comparison pages (other comparisons in same city)
    related_comps = get_neighborhood_comparison_pairs(city)
    related_comp_links = ''
    for rc_n1, rc_m1, rc_n2, rc_m2 in related_comps:
        if (rc_n1 == n1 and rc_n2 == n2) or (rc_n1 == n2 and rc_n2 == n1):
            continue  # Skip self
        rc_s1 = slugify(rc_n1)
        rc_s2 = slugify(rc_n2)
        related_comp_links += f'<a href="/compare/{city_slug}/{rc_s1}-vs-{rc_s2}" style="display: inline-block; padding: 6px 14px; background: #f5f5f7; border-radius: 100px; font-size: 0.8rem; color: #1d1d1f; text-decoration: none; margin: 4px;">{rc_n1} vs {rc_n2}</a>\n'

    meta_desc = f'{more_affordable} is {diff_pct:.0f}% cheaper than {more_expensive} in {city}. Compare rent, groceries & salary equivalents neighborhood by neighborhood.'

    # Share bar
    share_text = f'{n1} vs {n2} in {city}: {more_affordable} is {diff_pct:.0f}% more affordable — salary:converter'
    share_bar_html = build_share_bar(share_text, f'https://salary-converter.com/compare/{city_slug}/{n1_slug}-vs-{n2_slug}')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{n1} vs {n2}, {city}: {diff_pct:.0f}% Cost Difference ({CURRENT_YEAR})</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/compare/{city_slug}/{n1_slug}-vs-{n2_slug}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{n1} vs {n2}, {city}: {diff_pct:.0f}% Cost Difference ({CURRENT_YEAR})">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://salary-converter.com/compare/{city_slug}/{n1_slug}-vs-{n2_slug}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://salary-converter.com/"}},
            {{"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://salary-converter.com/compare/"}},
            {{"@type": "ListItem", "position": 3, "name": "{n1} vs {n2} ({city})"}}
        ]
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text-primary); -webkit-font-smoothing: antialiased; transition: background 0.3s, color 0.3s; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .breadcrumb {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        .hero {{ text-align: center; margin-bottom: 40px; }}
        .hero h1 {{ font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .hero .subtitle {{ font-size: 1rem; color: var(--text-secondary); }}
        .card {{ background: var(--card-bg); border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: var(--shadow); }}
        .card h2 {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 16px; letter-spacing: -0.3px; }}
        .vs-grid {{ display: grid; grid-template-columns: 1fr 60px 1fr; gap: 0; align-items: center; }}
        .vs-side {{ text-align: center; padding: 20px; }}
        .vs-side h3 {{ font-size: 1.1rem; font-weight: 700; margin-bottom: 4px; }}
        .vs-side .coli {{ font-size: 2rem; font-weight: 700; }}
        .vs-side .label {{ font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; }}
        .vs-divider {{ text-align: center; font-size: 1.2rem; font-weight: 700; color: var(--text-secondary); }}
        .winner-badge {{ display: inline-block; padding: 4px 10px; border-radius: 100px; font-size: 0.7rem; font-weight: 600; margin-top: 8px; }}
        .compare-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
        .compare-item {{ text-align: center; padding: 16px; background: var(--stat-card-bg); border-radius: 12px; }}
        .compare-item .val {{ font-size: 1.2rem; font-weight: 700; }}
        .compare-item .lbl {{ font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }}
        .bar-chart {{ margin: 20px 0; }}
        .bar-row {{ display: flex; align-items: center; margin-bottom: 12px; gap: 12px; }}
        .bar-label {{ width: 140px; font-size: 0.8rem; font-weight: 600; text-align: right; flex-shrink: 0; }}
        .bar-track {{ flex: 1; height: 28px; background: var(--tag-bg); border-radius: 8px; overflow: hidden; }}
        .bar-fill {{ height: 100%; border-radius: 8px; display: flex; align-items: center; padding-left: 10px; font-size: 0.75rem; font-weight: 600; color: white; }}
        .cta-box {{ text-align: center; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border-radius: 16px; padding: 32px; margin: 32px 0; }}
        .cta-box h2 {{ color: white; margin-bottom: 8px; }}
        .cta-box p {{ color: rgba(255,255,255,0.85); font-size: 0.9rem; margin-bottom: 16px; }}
        .cta-btn {{ display: inline-block; background: white; color: #2563eb; padding: 12px 28px; border-radius: 100px; font-weight: 600; text-decoration: none; font-size: 0.9rem; }}
        .page-footer {{ text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border); display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px; }}
        .page-footer a {{ font-size: 0.85rem; color: var(--accent); text-decoration: none; font-weight: 500; }}
        @media (max-width: 600px) {{
            .hero h1 {{ font-size: 1.3rem; }}
            .vs-grid {{ grid-template-columns: 1fr 40px 1fr; }}
            .vs-side h3 {{ font-size: 0.9rem; }}
            .bar-label {{ width: 100px; font-size: 0.7rem; }}
            .card {{ padding: 20px; }}
        }}
        .share-bar {{
            display: flex; align-items: center; gap: 8px;
            margin: 16px 0 20px; padding: 12px 16px;
            background: var(--stat-card-bg, #f5f5f7); border-radius: 12px;
        }}
        .share-bar-label {{
            font-size: 0.75rem; font-weight: 600; color: var(--text-secondary);
            text-transform: uppercase; letter-spacing: 0.5px; margin-right: 4px;
        }}
        .share-btn {{
            display: flex; align-items: center; justify-content: center;
            width: 34px; height: 34px; border-radius: 50%;
            border: 1px solid var(--border, #e5e5ea); background: var(--card-bg, #fff);
            color: var(--text-secondary, #86868b); cursor: pointer; transition: all 0.2s;
            padding: 0;
        }}
        .share-btn:hover {{ color: var(--accent); border-color: var(--accent); transform: scale(1.08); }}
        .share-btn.copied {{ color: #22c55e; border-color: #22c55e; }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/compare/">City Comparisons</a> &rsaquo; <a href="/city/{city_slug}">{city}</a> &rsaquo; {n1} vs {n2}
        </div>

        <section class="hero">
            <h1>{n1} vs {n2}</h1>
            <p class="subtitle">Neighborhood comparison in {city}, {country}</p>
        </section>
        {share_bar_html}

        <div class="card">
            <div class="vs-grid">
                <div class="vs-side">
                    <h3><a href="/city/{city_slug}/{n1_slug}" style="color: #1d1d1f; text-decoration: none;">{n1}</a></h3>
                    <div class="coli" style="color: {color1};">{coli1}</div>
                    <div class="label">COLI Index</div>
                    {'<span class="winner-badge" style="background: #dcfce7; color: #16a34a;">More Affordable</span>' if m1 < m2 else '<span class="winner-badge" style="background: #fef3c7; color: #d97706;">More Expensive</span>' if m1 > m2 else ''}
                </div>
                <div class="vs-divider">VS</div>
                <div class="vs-side">
                    <h3><a href="/city/{city_slug}/{n2_slug}" style="color: #1d1d1f; text-decoration: none;">{n2}</a></h3>
                    <div class="coli" style="color: {color2};">{coli2}</div>
                    <div class="label">COLI Index</div>
                    {'<span class="winner-badge" style="background: #dcfce7; color: #16a34a;">More Affordable</span>' if m2 < m1 else '<span class="winner-badge" style="background: #fef3c7; color: #d97706;">More Expensive</span>' if m2 > m1 else ''}
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Side-by-Side Comparison</h2>
            <div class="compare-row">
                <div class="compare-item">
                    <div class="val">{m1:.2f}x</div>
                    <div class="lbl">{n1} Multiplier</div>
                </div>
                <div class="compare-item">
                    <div class="val">{m2:.2f}x</div>
                    <div class="lbl">{n2} Multiplier</div>
                </div>
            </div>
            <div class="compare-row">
                <div class="compare-item">
                    <div class="val">{fmt_rent1}</div>
                    <div class="lbl">Est. 1BR Rent</div>
                </div>
                <div class="compare-item">
                    <div class="val">{fmt_rent2}</div>
                    <div class="lbl">Est. 1BR Rent</div>
                </div>
            </div>
            <div class="compare-row">
                <div class="compare-item">
                    <div class="val">{fmt_equiv1}</div>
                    <div class="lbl">$75K Equivalent</div>
                </div>
                <div class="compare-item">
                    <div class="val">{fmt_equiv2}</div>
                    <div class="lbl">$75K Equivalent</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Cost Comparison</h2>
            <div class="bar-chart">
                <div class="bar-row">
                    <div class="bar-label">{n1}</div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: {bar1}%; background: {color1};">{m1:.2f}x</div>
                    </div>
                </div>
                <div class="bar-row">
                    <div class="bar-label">{n2}</div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: {bar2}%; background: {color2};">{m2:.2f}x</div>
                    </div>
                </div>
            </div>
            <p style="font-size: 0.85rem; color: #424245; line-height: 1.6;">
                {more_expensive} is <strong>{diff_pct:.0f}% more expensive</strong> than {more_affordable} within {city}.
                Living in {more_affordable} instead of {more_expensive} could save you significantly on rent and daily expenses.
            </p>
        </div>

        <div class="cta-box">
            <h2>Calculate Your Exact Salary</h2>
            <p>See what you need to earn in {city} to maintain your lifestyle, with neighborhood-level precision.</p>
            <a href="/" class="cta-btn">Open Salary Converter</a>
        </div>

        {f"""<div class="card">
            <h2>More Comparisons in {city}</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                {related_comp_links}
            </div>
        </div>""" if related_comp_links else ""}

        <div class="card">
            <h2>More Neighborhoods in {city}</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                {other_links}
            </div>
        </div>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/{city_slug}">{city}</a>
            <a href="/compare/">All Comparisons</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
{THEME_JS}
{SHARE_JS}
</body>
</html>'''

    return html


# ============================================================
# NEIGHBORHOOD COMPARISON PAIR SELECTION
# ============================================================

def get_neighborhood_comparison_pairs(city):
    """Select interesting neighborhood comparison pairs for a city"""
    nhoods = cityNeighborhoods.get(city, {})
    if len(nhoods) < 2:
        return []

    sorted_nhoods = sorted(nhoods.items(), key=lambda x: x[1], reverse=True)
    pairs = set()

    # Most expensive vs most affordable
    pairs.add((sorted_nhoods[0][0], sorted_nhoods[-1][0]))

    # Top 3 paired with each other
    top = sorted_nhoods[:3]
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            pairs.add((top[i][0], top[j][0]))

    # Bottom 3 paired with each other
    bottom = sorted_nhoods[-3:]
    for i in range(len(bottom)):
        for j in range(i + 1, len(bottom)):
            pairs.add((bottom[i][0], bottom[j][0]))

    # 1st vs middle, middle vs last
    mid_idx = len(sorted_nhoods) // 2
    pairs.add((sorted_nhoods[0][0], sorted_nhoods[mid_idx][0]))
    pairs.add((sorted_nhoods[mid_idx][0], sorted_nhoods[-1][0]))

    return [(n1, nhoods[n1], n2, nhoods[n2]) for n1, n2 in pairs]


# ============================================================
# DATA-DRIVEN BLOG ARTICLE GENERATORS
# ============================================================

def generate_blog_undervalued_neighborhoods():
    """Article 1: 50 Most Undervalued Neighborhoods in the World"""
    # Compute absolute COLI for all neighborhoods
    all_nhoods = []
    for city, nhoods in cityNeighborhoods.items():
        city_coli = coliData[city]
        country = cityCountry.get(city, '')
        city_slug = slugify(city)
        for name, mult in nhoods.items():
            abs_coli = round(city_coli * mult, 1)
            nhood_slug = slugify(name)
            all_nhoods.append({
                'name': name,
                'city': city,
                'country': country,
                'coli': abs_coli,
                'multiplier': mult,
                'city_slug': city_slug,
                'nhood_slug': nhood_slug,
            })

    # Sort by lowest COLI
    all_nhoods.sort(key=lambda x: x['coli'])
    top50 = all_nhoods[:50]

    # Build table rows
    rows = ''
    for i, n in enumerate(top50, 1):
        n_name = n['name']
        n_city = n['city']
        n_country = n['country']
        n_coli = n['coli']
        n_mult = n['multiplier']
        n_cs = n['city_slug']
        n_ns = n['nhood_slug']
        rows += f'''
                        <tr>
                            <td style="font-weight: 600;">{i}</td>
                            <td><a href="/city/{n_cs}/{n_ns}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{n_name}</a></td>
                            <td>{n_city}</td>
                            <td>{n_country}</td>
                            <td style="text-align: center; font-weight: 600;">{n_coli}</td>
                            <td style="text-align: center;">{n_mult:.2f}x</td>
                        </tr>'''

    article_date = TODAY
    total = TOTAL_NEIGHBORHOODS

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>50 Most Undervalued Neighborhoods in the World ({CURRENT_YEAR}) — salary:converter</title>
    <meta name="description" content="Discover the 50 most affordable neighborhoods globally, ranked by cost of living index. Data-driven analysis of {total:,} neighborhoods across 101 cities.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/blog/articles/50-most-undervalued-neighborhoods-in-the-world">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="50 Most Undervalued Neighborhoods in the World ({CURRENT_YEAR})">
    <meta property="og:description" content="Discover the 50 most affordable neighborhoods globally, ranked by cost of living index.">
    <meta property="og:url" content="https://salary-converter.com/blog/articles/50-most-undervalued-neighborhoods-in-the-world">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "50 Most Undervalued Neighborhoods in the World ({CURRENT_YEAR})",
        "datePublished": "{article_date}",
        "dateModified": "{article_date}",
        "author": {{"@type": "Organization", "name": "salary:converter"}},
        "publisher": {{"@type": "Organization", "name": "salary:converter", "url": "https://salary-converter.com"}},
        "url": "https://salary-converter.com/blog/articles/50-most-undervalued-neighborhoods-in-the-world"
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text-primary); -webkit-font-smoothing: antialiased; transition: background 0.3s, color 0.3s; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .breadcrumb {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        article {{ background: var(--card-bg); border-radius: 16px; padding: 40px; box-shadow: var(--shadow); }}
        article h1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; line-height: 1.2; }}
        .meta {{ font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 32px; }}
        article h2 {{ font-size: 1.3rem; font-weight: 700; margin: 32px 0 12px; letter-spacing: -0.3px; }}
        article p {{ font-size: 0.95rem; line-height: 1.7; color: var(--text-body); margin-bottom: 16px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ text-align: left; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); padding: 8px 10px; border-bottom: 2px solid var(--border); }}
        td {{ padding: 8px 10px; border-bottom: 1px solid var(--border-light); font-size: 0.8rem; }}
        .cta-box {{ text-align: center; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border-radius: 16px; padding: 32px; margin: 32px 0; }}
        .cta-box h2 {{ color: white; margin-bottom: 8px; }}
        .cta-box p {{ color: rgba(255,255,255,0.85); }}
        .cta-btn {{ display: inline-block; background: white; color: #2563eb; padding: 12px 28px; border-radius: 100px; font-weight: 600; text-decoration: none; font-size: 0.9rem; }}
        .page-footer {{ text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border); display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px; }}
        .page-footer a {{ font-size: 0.85rem; color: var(--accent); text-decoration: none; font-weight: 500; }}
        @media (max-width: 600px) {{
            article {{ padding: 24px; }}
            article h1 {{ font-size: 1.5rem; }}
            table {{ font-size: 0.75rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; 50 Most Undervalued Neighborhoods
        </div>

        <article>
            <h1>50 Most Undervalued Neighborhoods in the World ({CURRENT_YEAR})</h1>
            <div class="meta">Published {article_date} &middot; salary:converter Research &middot; Based on {total:,} neighborhoods</div>

            <p>Not all neighborhoods are created equal. While city-level cost of living data gives you a general picture, the real story is at the neighborhood level. We analyzed <strong>{total:,} neighborhoods across 101 cities</strong> to find the most affordable places to live worldwide.</p>

            <p>Each neighborhood is scored using an absolute COLI (Cost of Living Index), calculated by multiplying the city's baseline COLI by the neighborhood's local multiplier. A lower score means a more affordable place to live.</p>

            <h2>The 50 Most Affordable Neighborhoods Globally</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Neighborhood</th>
                            <th>City</th>
                            <th>Country</th>
                            <th style="text-align: center;">COLI</th>
                            <th style="text-align: center;">Multiplier</th>
                        </tr>
                    </thead>
                    <tbody>{rows}
                    </tbody>
                </table>
            </div>

            <h2>Key Takeaways</h2>
            <p>The most affordable neighborhoods tend to be in cities with already-low costs of living in South and Southeast Asia, Africa, and parts of Eastern Europe and Latin America. Within these cities, outer suburbs and working-class districts push costs even lower.</p>

            <p>However, affordability always comes with trade-offs. The cheapest neighborhoods may have longer commutes, fewer amenities, or less developed infrastructure. Always balance cost against quality of life when choosing where to live.</p>

            <div class="cta-box">
                <h2>Compare Any Neighborhood</h2>
                <p>Use our converter with {ROUNDED_NEIGHBORHOODS:,}+ neighborhood-level adjustments for precise salary comparisons.</p>
                <a href="/" class="cta-btn">Open Salary Converter</a>
            </div>

            <h2>Methodology</h2>
            <p>Our COLI data is compiled from multiple sources including Numbeo, Expatistan, OECD, and ECB. Neighborhood multipliers are based on local rent differentials, consumer price surveys, and expatriate community reports. The absolute COLI for each neighborhood is calculated as: City COLI x Neighborhood Multiplier.</p>
        </article>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/blog/">Blog</a>
            <a href="/city/">All Cities</a>
        </footer>
    </div>
{THEME_JS}
</body>
</html>'''

    return html


def generate_blog_salary_goes_furthest():
    """Article 2: Where Your Salary Goes Furthest - Neighborhood Edition"""
    # Compute $100K USD equivalent in each neighborhood
    all_nhoods = []
    for city, nhoods in cityNeighborhoods.items():
        city_coli = coliData[city]
        currency = cityToCurrency.get(city, 'USD')
        rate = exchangeRates[currency] / exchangeRates['USD']
        city_slug = slugify(city)
        for name, mult in nhoods.items():
            abs_coli = city_coli * mult
            # Purchasing power: how far does $100K go here vs NYC baseline
            purchasing_power = (100 / abs_coli) * 100
            nhood_slug = slugify(name)
            all_nhoods.append({
                'name': name,
                'city': city,
                'coli': round(abs_coli, 1),
                'power': round(purchasing_power, 0),
                'city_slug': city_slug,
                'nhood_slug': nhood_slug,
            })

    # Sort by highest purchasing power (most bang for your buck)
    all_nhoods.sort(key=lambda x: x['power'], reverse=True)

    top30 = all_nhoods[:30]
    bottom30 = all_nhoods[-30:]
    bottom30.reverse()

    top_rows = ''
    for i, n in enumerate(top30, 1):
        n_name = n['name']
        n_city = n['city']
        n_coli = n['coli']
        n_power = int(n['power'])
        n_cs = n['city_slug']
        n_ns = n['nhood_slug']
        top_rows += f'''
                        <tr>
                            <td style="font-weight: 600;">{i}</td>
                            <td><a href="/city/{n_cs}/{n_ns}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{n_name}</a></td>
                            <td>{n_city}</td>
                            <td style="text-align: center;">{n_coli}</td>
                            <td style="text-align: right; font-weight: 600; color: #22c55e;">{n_power}%</td>
                        </tr>'''

    bottom_rows = ''
    for i, n in enumerate(bottom30, 1):
        n_name = n['name']
        n_city = n['city']
        n_coli = n['coli']
        n_power = int(n['power'])
        n_cs = n['city_slug']
        n_ns = n['nhood_slug']
        bottom_rows += f'''
                        <tr>
                            <td style="font-weight: 600;">{i}</td>
                            <td><a href="/city/{n_cs}/{n_ns}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{n_name}</a></td>
                            <td>{n_city}</td>
                            <td style="text-align: center;">{n_coli}</td>
                            <td style="text-align: right; font-weight: 600; color: #ef4444;">{n_power}%</td>
                        </tr>'''

    article_date = TODAY
    total = TOTAL_NEIGHBORHOODS

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Where Your Salary Goes Furthest: Neighborhood Edition ({CURRENT_YEAR}) — salary:converter</title>
    <meta name="description" content="Discover which neighborhoods give you the most purchasing power. Analysis of {total:,} neighborhoods across 101 cities worldwide.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/blog/articles/where-your-salary-goes-furthest-neighborhood-edition">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="Where Your Salary Goes Furthest: Neighborhood Edition ({CURRENT_YEAR})">
    <meta property="og:description" content="Discover which neighborhoods give you the most purchasing power worldwide.">
    <meta property="og:url" content="https://salary-converter.com/blog/articles/where-your-salary-goes-furthest-neighborhood-edition">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "Where Your Salary Goes Furthest: Neighborhood Edition ({CURRENT_YEAR})",
        "datePublished": "{article_date}",
        "dateModified": "{article_date}",
        "author": {{"@type": "Organization", "name": "salary:converter"}},
        "publisher": {{"@type": "Organization", "name": "salary:converter", "url": "https://salary-converter.com"}},
        "url": "https://salary-converter.com/blog/articles/where-your-salary-goes-furthest-neighborhood-edition"
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text-primary); -webkit-font-smoothing: antialiased; transition: background 0.3s, color 0.3s; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .breadcrumb {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        article {{ background: var(--card-bg); border-radius: 16px; padding: 40px; box-shadow: var(--shadow); }}
        article h1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; line-height: 1.2; }}
        .meta {{ font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 32px; }}
        article h2 {{ font-size: 1.3rem; font-weight: 700; margin: 32px 0 12px; letter-spacing: -0.3px; }}
        article p {{ font-size: 0.95rem; line-height: 1.7; color: var(--text-body); margin-bottom: 16px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ text-align: left; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); padding: 8px 10px; border-bottom: 2px solid var(--border); }}
        td {{ padding: 8px 10px; border-bottom: 1px solid var(--border-light); font-size: 0.8rem; }}
        .cta-box {{ text-align: center; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border-radius: 16px; padding: 32px; margin: 32px 0; }}
        .cta-box h2 {{ color: white; margin-bottom: 8px; }}
        .cta-box p {{ color: rgba(255,255,255,0.85); }}
        .cta-btn {{ display: inline-block; background: white; color: #2563eb; padding: 12px 28px; border-radius: 100px; font-weight: 600; text-decoration: none; font-size: 0.9rem; }}
        .page-footer {{ text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border); display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px; }}
        .page-footer a {{ font-size: 0.85rem; color: var(--accent); text-decoration: none; font-weight: 500; }}
        @media (max-width: 600px) {{
            article {{ padding: 24px; }}
            article h1 {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; Where Your Salary Goes Furthest
        </div>

        <article>
            <h1>Where Your Salary Goes Furthest: Neighborhood Edition ({CURRENT_YEAR})</h1>
            <div class="meta">Published {article_date} &middot; salary:converter Research &middot; {total:,} neighborhoods analyzed</div>

            <p>A $100,000 salary means very different things depending on where you live &mdash; not just which city, but which <em>neighborhood</em>. We calculated the purchasing power of the same salary across <strong>{total:,} neighborhoods in 101 cities</strong> to find where your money goes furthest.</p>

            <p>Purchasing power is shown as a percentage of New York City baseline (100%). A score of 500% means your dollar buys 5x more than in NYC.</p>

            <h2>Top 30: Where Your Salary Stretches Furthest</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Neighborhood</th>
                            <th>City</th>
                            <th style="text-align: center;">COLI</th>
                            <th style="text-align: right;">Buying Power</th>
                        </tr>
                    </thead>
                    <tbody>{top_rows}
                    </tbody>
                </table>
            </div>

            <div class="cta-box">
                <h2>Calculate Your Exact Salary</h2>
                <p>Pick any two neighborhoods and see precisely what you need to earn to maintain your lifestyle.</p>
                <a href="/" class="cta-btn">Open Salary Converter</a>
            </div>

            <h2>Bottom 30: Where Your Salary Stretches Least</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Neighborhood</th>
                            <th>City</th>
                            <th style="text-align: center;">COLI</th>
                            <th style="text-align: right;">Buying Power</th>
                        </tr>
                    </thead>
                    <tbody>{bottom_rows}
                    </tbody>
                </table>
            </div>

            <h2>Key Insights</h2>
            <p>The gap between the most and least affordable neighborhoods is staggering. Your purchasing power can differ by <strong>10x or more</strong> depending on where you choose to live. Even within the same city, choosing the right neighborhood can effectively give you a 30-50% raise.</p>

            <p>Remote workers in particular can leverage this data: earning a Western salary while living in a high-purchasing-power neighborhood lets you build wealth dramatically faster.</p>

            <h2>Methodology</h2>
            <p>Purchasing power is calculated as: (100 / Absolute COLI) x 100, where Absolute COLI = City COLI x Neighborhood Multiplier. Data sourced from Numbeo, Expatistan, OECD, and ECB, combined with local rental and consumer surveys.</p>
        </article>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/blog/">Blog</a>
            <a href="/city/">All Cities</a>
        </footer>
    </div>
{THEME_JS}
</body>
</html>'''

    return html


def generate_blog_major_cities_breakdown():
    """Article 3: The Real Cost of Living in 10 Major Cities: Neighborhood Breakdown"""
    focus_cities = ['New York', 'London', 'Tokyo', 'Singapore', 'Dubai', 'Paris', 'Sydney', 'Berlin', 'Bangkok', 'São Paulo']

    city_sections = ''
    for city in focus_cities:
        nhoods = cityNeighborhoods.get(city, {})
        if not nhoods:
            continue
        city_slug = slugify(city)
        currency = cityToCurrency.get(city, 'USD')
        city_coli = coliData[city]
        sorted_nhoods = sorted(nhoods.items(), key=lambda x: x[1], reverse=True)
        most_expensive = sorted_nhoods[0]
        most_affordable = sorted_nhoods[-1]
        gap_pct = abs(most_expensive[1] - most_affordable[1]) / max(most_expensive[1], most_affordable[1]) * 100
        rate_to_local = exchangeRates[currency] / exchangeRates['USD']

        # Monthly savings: difference in estimated rent
        city_rent = cityRent1BR.get(city, 0)
        exp_rent = city_rent * most_expensive[1] * rate_to_local
        aff_rent = city_rent * most_affordable[1] * rate_to_local
        monthly_saving = exp_rent - aff_rent
        fmt_saving = format_currency_amount(monthly_saving, currency)

        rows = ''
        for name, mult in sorted_nhoods:
            nhood_slug = slugify(name)
            abs_coli = round(city_coli * mult, 1)
            pct = (mult - 1) * 100
            sign = '+' if pct >= 0 else ''
            color = '#22c55e' if pct < 0 else '#2563eb' if pct < 15 else '#f59e0b' if pct < 30 else '#ef4444'
            rows += f'''
                        <tr>
                            <td><a href="/city/{city_slug}/{nhood_slug}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{name}</a></td>
                            <td style="text-align: center;">{abs_coli}</td>
                            <td style="text-align: center;">{mult:.2f}x</td>
                            <td style="text-align: right;"><span style="color: {color}; font-weight: 600;">{sign}{pct:.0f}%</span></td>
                        </tr>'''

        me_name = most_expensive[0]
        ma_name = most_affordable[0]
        city_sections += f'''
            <h2>{city}</h2>
            <p><strong>{len(sorted_nhoods)} neighborhoods</strong> &middot; Most expensive: {me_name} &middot; Most affordable: {ma_name} &middot; Gap: {gap_pct:.0f}% &middot; Potential monthly savings: {fmt_saving}</p>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Neighborhood</th>
                            <th style="text-align: center;">COLI</th>
                            <th style="text-align: center;">Multiplier</th>
                            <th style="text-align: right;">vs Average</th>
                        </tr>
                    </thead>
                    <tbody>{rows}
                    </tbody>
                </table>
            </div>
            <p style="font-size: 0.85rem;"><a href="/city/{city_slug}" style="color: #2563eb; text-decoration: none;">View full {city} salary data &rarr;</a></p>
'''

    article_date = TODAY
    total = TOTAL_NEIGHBORHOODS

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Real Cost of Living in 10 Major Cities: Neighborhood Breakdown ({CURRENT_YEAR}) — salary:converter</title>
    <meta name="description" content="Detailed neighborhood-level cost of living breakdown for New York, London, Tokyo, Singapore, Dubai, Paris, Sydney, Berlin, Bangkok, and S&#227;o Paulo.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/blog/articles/real-cost-of-living-major-cities-neighborhood-breakdown">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="Real Cost of Living in 10 Major Cities: Neighborhood Breakdown ({CURRENT_YEAR})">
    <meta property="og:description" content="Detailed neighborhood-level cost of living data for 10 major world cities.">
    <meta property="og:url" content="https://salary-converter.com/blog/articles/real-cost-of-living-major-cities-neighborhood-breakdown">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "Real Cost of Living in 10 Major Cities: Neighborhood Breakdown ({CURRENT_YEAR})",
        "datePublished": "{article_date}",
        "dateModified": "{article_date}",
        "author": {{"@type": "Organization", "name": "salary:converter"}},
        "publisher": {{"@type": "Organization", "name": "salary:converter", "url": "https://salary-converter.com"}},
        "url": "https://salary-converter.com/blog/articles/real-cost-of-living-major-cities-neighborhood-breakdown"
    }}
    </script>
{GA4_SNIPPET}
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html, body {{ overflow-x: hidden; }}
        html {{ touch-action: manipulation; -ms-touch-action: manipulation; }}
{THEME_CSS_VARS}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text-primary); -webkit-font-smoothing: antialiased; transition: background 0.3s, color 0.3s; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: var(--text-primary); text-decoration: none;
        }}
        .nav-logo span {{ color: var(--accent); }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: var(--text-secondary);
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}
{THEME_TOGGLE_CSS}
        .breadcrumb {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px; }}
        .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
        article {{ background: var(--card-bg); border-radius: 16px; padding: 40px; box-shadow: var(--shadow); }}
        article h1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; line-height: 1.2; }}
        .meta {{ font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 32px; }}
        article h2 {{ font-size: 1.3rem; font-weight: 700; margin: 32px 0 12px; letter-spacing: -0.3px; }}
        article p {{ font-size: 0.95rem; line-height: 1.7; color: var(--text-body); margin-bottom: 16px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ text-align: left; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); padding: 8px 10px; border-bottom: 2px solid var(--border); }}
        td {{ padding: 8px 10px; border-bottom: 1px solid var(--border-light); font-size: 0.8rem; }}
        .cta-box {{ text-align: center; background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border-radius: 16px; padding: 32px; margin: 32px 0; }}
        .cta-box h2 {{ color: white; margin-bottom: 8px; }}
        .cta-box p {{ color: rgba(255,255,255,0.85); }}
        .cta-btn {{ display: inline-block; background: white; color: #2563eb; padding: 12px 28px; border-radius: 100px; font-weight: 600; text-decoration: none; font-size: 0.9rem; }}
        .page-footer {{ text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border); display: flex; justify-content: center; flex-wrap: wrap; gap: 8px 20px; }}
        .page-footer a {{ font-size: 0.85rem; color: var(--accent); text-decoration: none; font-weight: 500; }}
        @media (max-width: 600px) {{
            article {{ padding: 24px; }}
            article h1 {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="nav-bar">
            <a href="/" class="nav-logo">salary<span>:</span>converter</a>
            <div class="nav-links">
                <a href="/">Converter</a>
                <a href="/city/">Cities</a>
                <a href="/compare/">City Comparisons</a>
                <a href="/blog/">Blog</a>
                {THEME_TOGGLE_HTML}
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; Real Cost of Living: Neighborhood Breakdown
        </div>

        <article>
            <h1>The Real Cost of Living in 10 Major Cities: A Neighborhood Breakdown ({CURRENT_YEAR})</h1>
            <div class="meta">Published {article_date} &middot; salary:converter Research &middot; {total:,} neighborhoods analyzed</div>

            <p>City-level averages hide enormous variation. In most major cities, the most expensive neighborhood costs <strong>50-100% more</strong> than the most affordable one. This guide breaks down the real cost of living across every neighborhood in 10 of the world's most popular cities for expats and remote workers.</p>

            <p>Each neighborhood is rated using a multiplier against the city average (1.00x). Below 1.00 is cheaper than average; above 1.00 is more expensive.</p>

            {city_sections}

            <div class="cta-box">
                <h2>Compare Any Two Neighborhoods</h2>
                <p>Our converter handles {ROUNDED_NEIGHBORHOODS:,}+ neighborhoods across 101 cities with real-time salary equivalents.</p>
                <a href="/" class="cta-btn">Open Salary Converter</a>
            </div>

            <h2>Methodology</h2>
            <p>All data is compiled from Numbeo, Expatistan, OECD, and ECB combined with local rent indices, consumer surveys, and expatriate community reports. Neighborhood multipliers reflect relative cost differences within each city, covering housing, food, transportation, and general consumer prices.</p>
        </article>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/blog/">Blog</a>
            <a href="/city/">All Cities</a>
        </footer>
    </div>
{THEME_JS}
</body>
</html>'''

    return html


# ============================================================
# SITEMAP GENERATION
# ============================================================

def generate_sitemaps(base_dir, comparison_pairs, neighborhood_comparison_data=None):
    """Generate split sitemaps + sitemap index (avoids host truncation of large files)"""
    CHUNK_SIZE = 2000

    urls = []
    # Main pages
    urls.append('https://salary-converter.com/')
    urls.append('https://salary-converter.com/widget')
    urls.append('https://salary-converter.com/city/')
    urls.append('https://salary-converter.com/compare/')
    urls.append('https://salary-converter.com/blog/')

    # Blog articles
    blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog', 'articles')
    if os.path.isdir(blog_dir):
        for fname in sorted(os.listdir(blog_dir)):
            if fname.endswith('.html'):
                urls.append(f'https://salary-converter.com/blog/articles/{fname[:-5]}')

    # City pages
    for city in coliData:
        slug = slugify(city)
        urls.append(f'https://salary-converter.com/city/{slug}')

    # Neighborhood pages
    for city, nhoods in cityNeighborhoods.items():
        city_slug = slugify(city)
        for nhood in nhoods:
            nhood_slug = slugify(nhood)
            urls.append(f'https://salary-converter.com/city/{city_slug}/{nhood_slug}')
        # Cheapest/most-expensive neighborhood hub pages
        urls.append(f'https://salary-converter.com/city/{city_slug}/cheapest-neighborhoods')
        urls.append(f'https://salary-converter.com/city/{city_slug}/most-expensive-neighborhoods')

    # City-vs-city comparison pages
    for city1, city2 in comparison_pairs:
        slug1 = slugify(city1)
        slug2 = slugify(city2)
        urls.append(f'https://salary-converter.com/compare/{slug1}-vs-{slug2}')

    # Neighborhood comparison pages
    if neighborhood_comparison_data:
        for city, pairs in neighborhood_comparison_data.items():
            city_slug = slugify(city)
            for n1, m1, n2, m2 in pairs:
                n1_slug = slugify(n1)
                n2_slug = slugify(n2)
                urls.append(f'https://salary-converter.com/compare/{city_slug}/{n1_slug}-vs-{n2_slug}')

    # Salary-needed hub + city pages + neighborhood pages
    urls.append('https://salary-converter.com/salary-needed/')
    for city in coliData:
        slug = slugify(city)
        urls.append(f'https://salary-converter.com/salary-needed/{slug}')
        if city in cityNeighborhoods:
            for nhood in cityNeighborhoods[city]:
                nhood_slug = slugify(nhood)
                urls.append(f'https://salary-converter.com/salary-needed/{slug}/{nhood_slug}')

    # Privacy page
    urls.append('https://salary-converter.com/privacy/')

    # Split into chunks and write individual sitemaps
    num_chunks = (len(urls) + CHUNK_SIZE - 1) // CHUNK_SIZE
    sitemap_files = []

    for i in range(num_chunks):
        chunk = urls[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
        filename = f'sitemap-{i + 1}.xml'
        filepath = os.path.join(base_dir, filename)

        xml_entries = ''
        for url in chunk:
            xml_entries += f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>\n'

        sitemap_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{xml_entries}</urlset>\n'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        sitemap_files.append(filename)

    # Write sitemap index
    index_entries = ''
    for filename in sitemap_files:
        index_entries += f'  <sitemap>\n    <loc>https://salary-converter.com/{filename}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </sitemap>\n'

    index_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{index_entries}</sitemapindex>\n'

    with open(os.path.join(base_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(index_content)

    return len(urls), num_chunks


# ============================================================
# MAIN GENERATION LOGIC
# ============================================================

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    city_dir = os.path.join(base_dir, 'city')
    compare_dir = os.path.join(base_dir, 'compare')

    os.makedirs(city_dir, exist_ok=True)
    os.makedirs(compare_dir, exist_ok=True)

    # Featured comparison pairs (high-traffic searches — shown first on index)
    featured_pairs = {
        ('London', 'New York'), ('London', 'Dubai'), ('London', 'Singapore'),
        ('London', 'Paris'), ('London', 'Berlin'), ('London', 'Amsterdam'),
        ('London', 'Sydney'), ('London', 'Toronto'), ('London', 'Tokyo'),
        ('London', 'Dublin'), ('New York', 'San Francisco'), ('New York', 'Los Angeles'),
        ('New York', 'Chicago'), ('New York', 'Miami'), ('New York', 'Toronto'),
        ('New York', 'Tokyo'), ('New York', 'Singapore'), ('New York', 'Dubai'),
        ('New York', 'Berlin'), ('Dubai', 'Singapore'), ('Dubai', 'Abu Dhabi'),
        ('Dubai', 'Doha'), ('Dubai', 'Bangkok'), ('Dubai', 'Sydney'),
        ('Singapore', 'Hong Kong'), ('Singapore', 'Bangkok'), ('Singapore', 'Tokyo'),
        ('Singapore', 'Sydney'), ('Singapore', 'Kuala Lumpur'), ('Tokyo', 'Seoul'),
        ('Tokyo', 'Osaka'), ('Tokyo', 'Sydney'), ('Paris', 'Berlin'),
        ('Paris', 'Amsterdam'), ('Paris', 'Barcelona'), ('Paris', 'Rome'),
        ('Berlin', 'Munich'), ('Berlin', 'Amsterdam'), ('Berlin', 'Prague'),
        ('Berlin', 'Vienna'), ('Lisbon', 'Barcelona'), ('Lisbon', 'Madrid'),
        ('Lisbon', 'Porto'), ('Sydney', 'Melbourne'), ('Sydney', 'Auckland'),
        ('San Francisco', 'Austin'), ('San Francisco', 'Seattle'),
        ('Boston', 'Washington DC'), ('Bangkok', 'Bali (Denpasar)'),
        ('Bangkok', 'Ho Chi Minh City'), ('Bangkok', 'Chiang Mai'),
        ('Mexico City', 'Bogotá'), ('Mexico City', 'Medellín'),
        ('Buenos Aires', 'São Paulo'), ('Buenos Aires', 'Santiago'),
        ('Dubai', 'Tel Aviv'), ('Zurich', 'Geneva'), ('Stockholm', 'Copenhagen'),
        ('Mumbai', 'Bangalore'), ('Hong Kong', 'Taipei'),
    }

    # Generate ALL city pairs (101 cities = 5,050 pairs)
    all_cities = sorted(coliData.keys())
    comparison_pairs = []
    for i, c1 in enumerate(all_cities):
        for c2 in all_cities[i+1:]:
            comparison_pairs.append((c1, c2))

    # Generate all city pages
    print(f"Generating {len(coliData)} city pages...")
    for city in coliData:
        slug = slugify(city)
        filepath = os.path.join(city_dir, f'{slug}.html')
        html = generate_city_page(city, comparison_pairs)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"  Done: {len(coliData)} city pages created in /city/")

    # Generate city index page
    index_path = os.path.join(city_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(generate_city_index())
    print("  Done: City index page created at /city/index")

    # Generate individual neighborhood pages
    nhood_count = 0
    for city, nhoods in cityNeighborhoods.items():
        city_slug = slugify(city)
        nhood_dir = os.path.join(city_dir, city_slug)
        os.makedirs(nhood_dir, exist_ok=True)
        for name, mult in nhoods.items():
            nhood_slug = slugify(name)
            filepath = os.path.join(nhood_dir, f'{nhood_slug}.html')
            html = generate_neighborhood_page(city, name, mult)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            nhood_count += 1
    print(f"  Done: {nhood_count} neighborhood pages created in /city/{{city}}/")

    # Generate cheapest/most-expensive neighborhood hub pages
    hub_count = 0
    for city in cityNeighborhoods:
        city_slug = slugify(city)
        nhood_dir = os.path.join(city_dir, city_slug)
        os.makedirs(nhood_dir, exist_ok=True)
        for mode in ('cheapest', 'most-expensive'):
            filepath = os.path.join(nhood_dir, f'{mode}-neighborhoods.html')
            html = generate_neighborhood_hub_page(city, mode)
            if html:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                hub_count += 1
    print(f"  Done: {hub_count} neighborhood hub pages (cheapest + most expensive)")

    # Generate comparison pages (city vs city)
    print(f"Generating {len(comparison_pairs)} city comparison pages...")
    for city1, city2 in comparison_pairs:
        slug1 = slugify(city1)
        slug2 = slugify(city2)
        filepath = os.path.join(compare_dir, f'{slug1}-vs-{slug2}.html')
        html = generate_comparison_page(city1, city2)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"  Done: {len(comparison_pairs)} city comparison pages in /compare/")

    # Generate neighborhood comparison pages
    nhood_comp_count = 0
    nhood_comp_data = {}
    for city in cityNeighborhoods:
        pairs = get_neighborhood_comparison_pairs(city)
        if not pairs:
            continue
        nhood_comp_data[city] = pairs
        city_slug = slugify(city)
        nhood_comp_dir = os.path.join(compare_dir, city_slug)
        os.makedirs(nhood_comp_dir, exist_ok=True)
        for n1, m1, n2, m2 in pairs:
            n1_slug = slugify(n1)
            n2_slug = slugify(n2)
            filepath = os.path.join(nhood_comp_dir, f'{n1_slug}-vs-{n2_slug}.html')
            html = generate_neighborhood_comparison_page(city, n1, m1, n2, m2)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            nhood_comp_count += 1
    print(f"  Done: {nhood_comp_count} neighborhood comparison pages in /compare/{{city}}/")

    # Generate compare index page
    compare_index_path = os.path.join(compare_dir, 'index.html')
    with open(compare_index_path, 'w', encoding='utf-8') as f:
        f.write(generate_compare_index(comparison_pairs, featured_pairs))
    print("  Done: Compare index page at /compare/index")

    # Generate data-driven blog articles
    blog_articles_dir = os.path.join(base_dir, 'blog', 'articles')
    os.makedirs(blog_articles_dir, exist_ok=True)

    blog_articles = [
        ('50-most-undervalued-neighborhoods-in-the-world.html', generate_blog_undervalued_neighborhoods),
        ('where-your-salary-goes-furthest-neighborhood-edition.html', generate_blog_salary_goes_furthest),
        ('real-cost-of-living-major-cities-neighborhood-breakdown.html', generate_blog_major_cities_breakdown),
    ]
    for filename, generator in blog_articles:
        filepath = os.path.join(blog_articles_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(generator())
    print(f"  Done: {len(blog_articles)} data-driven blog articles generated")

    # Generate split sitemaps
    url_count, chunk_count = generate_sitemaps(base_dir, comparison_pairs, nhood_comp_data)
    print(f"  Done: Sitemap index + {chunk_count} sitemaps ({url_count} URLs)")

    # Summary
    total_pages = len(coliData) + nhood_count + hub_count + len(comparison_pairs) + nhood_comp_count + len(blog_articles) + 2
    print(f"\nTotal pages generated: {total_pages}")
    print(f"  City pages: {len(coliData)}")
    print(f"  Neighborhood pages: {nhood_count}")
    print(f"  Neighborhood hub pages: {hub_count}")
    print(f"  City comparisons: {len(comparison_pairs)}")
    print(f"  Neighborhood comparisons: {nhood_comp_count}")
    print(f"  Blog articles: {len(blog_articles)}")
    print(f"  Index pages: 2")
