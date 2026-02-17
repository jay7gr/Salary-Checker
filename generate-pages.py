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
    'Washington DC': 79.8, 'Houston': 60.2, 'Toronto': 62.3, 'Vancouver': 65.4,
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
    'New York': {
        'Manhattan (Midtown)': 1.25, 'Manhattan (Upper East Side)': 1.30, 'Manhattan (Lower East Side)': 1.10,
        'Brooklyn (Williamsburg)': 1.05, 'Brooklyn (Park Slope)': 1.08, 'Brooklyn (Bushwick)': 0.88,
        'Queens (Astoria)': 0.90, 'Queens (Long Island City)': 0.95, 'Harlem': 0.82,
        'The Bronx': 0.72, 'Staten Island': 0.75, 'SoHo / Tribeca': 1.35
    },
    'San Francisco': {
        'Financial District': 1.20, 'SoMa': 1.15, 'Mission District': 1.05,
        'Castro': 1.08, 'Sunset District': 0.92, 'Richmond District': 0.90,
        'Nob Hill': 1.18, 'Pacific Heights': 1.25, 'Tenderloin': 0.78,
        'Oakland (Downtown)': 0.80, 'Oakland (Rockridge)': 0.88, 'Berkeley': 0.90
    },
    'Los Angeles': {
        'Santa Monica': 1.25, 'Beverly Hills': 1.40, 'Hollywood': 1.10,
        'Downtown LA': 1.05, 'Silver Lake': 1.08, 'Venice': 1.20,
        'Koreatown': 0.85, 'Echo Park': 0.90, 'Pasadena': 0.92,
        'Long Beach': 0.80, 'Culver City': 1.02, 'Burbank': 0.88
    },
    'London': {
        'Mayfair': 1.45, 'Chelsea': 1.38, 'Kensington': 1.35,
        'Notting Hill': 1.28, 'Soho': 1.22, 'Shoreditch': 1.10,
        'Camden': 1.05, 'Islington': 1.12, 'Brixton': 0.88,
        'Hackney': 0.92, 'Peckham': 0.82, 'Canary Wharf': 1.15,
        'Greenwich': 0.90, 'Clapham': 0.95, 'Stratford': 0.78,
        'Marylebone': 1.32, 'Hampstead': 1.30
    },
    'Paris': {
        'Le Marais (3rd/4th)': 1.30, 'Saint-Germain (6th)': 1.35, 'Champs-Élysées (8th)': 1.40,
        'Montmartre (18th)': 0.92, 'Bastille (11th)': 1.05, 'Oberkampf (11th)': 1.02,
        'Belleville (20th)': 0.82, 'La Défense': 1.10, 'Pigalle (9th)': 0.95,
        'Nation (12th)': 0.88, 'Batignolles (17th)': 0.98, 'Boulogne-Billancourt': 1.08
    },
    'Tokyo': {
        'Minato (Roppongi)': 1.30, 'Shibuya': 1.25, 'Shinjuku': 1.18,
        'Chiyoda (Marunouchi)': 1.35, 'Meguro': 1.15, 'Setagaya': 1.08,
        'Nakano': 0.92, 'Suginami': 0.88, 'Koto (Toyosu)': 1.05,
        'Adachi': 0.75, 'Edogawa': 0.78, 'Bunkyo': 1.10
    },
    'Singapore': {
        'Orchard Road': 1.30, 'Marina Bay': 1.35, 'Raffles Place': 1.25,
        'Holland Village': 1.12, 'Tiong Bahru': 1.10, 'Tanjong Pagar': 1.15,
        'Bukit Timah': 1.18, 'Clementi': 0.88, 'Woodlands': 0.75,
        'Tampines': 0.78, 'Jurong East': 0.80, 'Sentosa': 1.40
    },
    'Dubai': {
        'Downtown Dubai': 1.35, 'Dubai Marina': 1.28, 'Palm Jumeirah': 1.40,
        'JBR': 1.22, 'Business Bay': 1.18, 'DIFC': 1.30,
        'JLT': 1.05, 'Deira': 0.78, 'Al Barsha': 0.88,
        'Jumeirah': 1.15, 'Silicon Oasis': 0.72, 'Sports City': 0.80
    },
    'Sydney': {
        'CBD': 1.25, 'Bondi': 1.22, 'Surry Hills': 1.15,
        'Darlinghurst': 1.12, 'Newtown': 1.05, 'Manly': 1.10,
        'Parramatta': 0.82, 'Bankstown': 0.72, 'Chatswood': 0.95,
        'Pyrmont': 1.18, 'Mosman': 1.28, 'Marrickville': 0.90
    },
    'Berlin': {
        'Mitte': 1.22, 'Prenzlauer Berg': 1.12, 'Kreuzberg': 1.08,
        'Friedrichshain': 1.02, 'Charlottenburg': 1.15, 'Neukölln': 0.85,
        'Schöneberg': 1.05, 'Wedding': 0.78, 'Tempelhof': 0.82,
        'Spandau': 0.72, 'Steglitz': 0.88, 'Grunewald': 1.30
    },
    'Bangkok': {
        'Sukhumvit (Asoke)': 1.25, 'Silom / Sathorn': 1.22, 'Siam': 1.18,
        'Thonglor': 1.28, 'Ekkamai': 1.15, 'Ari': 1.10,
        'Khao San': 0.85, 'On Nut': 0.88, 'Phra Khanong': 0.92,
        'Bang Na': 0.78, 'Chatuchak': 0.90, 'Ladprao': 0.82
    },
    'Lisbon': {
        'Chiado': 1.28, 'Príncipe Real': 1.25, 'Alfama': 1.10,
        'Bairro Alto': 1.15, 'Estrela / Lapa': 1.12, 'Avenidas Novas': 1.05,
        'Alcântara': 0.95, 'Benfica': 0.82, 'Amadora': 0.72,
        'Parque das Nações': 1.08, 'Campo de Ourique': 1.02
    },
    'Barcelona': {
        'Eixample': 1.15, 'Gràcia': 1.08, 'Born / El Born': 1.20,
        'Gothic Quarter': 1.18, 'Barceloneta': 1.10, 'Poblenou': 1.02,
        'Raval': 0.88, 'Sants': 0.85, 'Sant Andreu': 0.78,
        'Sarrià-Sant Gervasi': 1.25, 'Horta-Guinardó': 0.80
    },
    'Amsterdam': {
        'Canal Ring (Centrum)': 1.30, 'Jordaan': 1.25, 'De Pijp': 1.10,
        'Oud-West': 1.15, 'Oud-Zuid': 1.28, 'Oost': 0.95,
        'Noord': 0.82, 'Nieuw-West': 0.75, 'Amstelveen': 0.88,
        'Zuidas': 1.20, 'Westerpark': 1.05
    },
    'Toronto': {
        'Yorkville': 1.30, 'King West': 1.22, 'Liberty Village': 1.10,
        'Queen West': 1.08, 'The Annex': 1.12, 'Leslieville': 0.95,
        'Kensington Market': 0.92, 'Etobicoke': 0.80, 'Scarborough': 0.75,
        'North York': 0.85, 'Downtown Core': 1.18, 'Danforth': 0.90
    },
}

# City to region mapping for organization
cityRegions = {
    'North America': ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Miami', 'Austin',
                      'Seattle', 'Denver', 'Boston', 'Washington DC', 'Houston', 'Toronto',
                      'Vancouver', 'Montreal', 'Mexico City', 'Cancún', 'Panama City'],
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

# Tax rates by country (approximate effective income tax rate for mid-range earner ~$60-80K equivalent)
countryTaxRates = {
    'United States': 24, 'Canada': 26, 'Mexico': 20, 'Panama': 15,
    'United Kingdom': 25, 'France': 30, 'Netherlands': 37, 'Germany': 32,
    'Ireland': 27, 'Belgium': 40, 'Luxembourg': 28, 'Switzerland': 18,
    'Spain': 24, 'Portugal': 25, 'Italy': 31, 'Greece': 22, 'Croatia': 20,
    'Sweden': 32, 'Denmark': 36, 'Finland': 31, 'Norway': 28, 'Austria': 30,
    'Czech Republic': 15, 'Hungary': 15, 'Poland': 17, 'Romania': 10,
    'Estonia': 20, 'Latvia': 20, 'Turkey': 15,
    'Japan': 23, 'South Korea': 19, 'China (SAR)': 15, 'Taiwan': 12,
    'China': 20, 'Singapore': 7, 'Thailand': 15, 'Malaysia': 16,
    'Vietnam': 15, 'Philippines': 20, 'Indonesia': 15, 'Cambodia': 0,
    'India': 20, 'Australia': 27, 'New Zealand': 24,
    'UAE': 0, 'Qatar': 0, 'Saudi Arabia': 0, 'Israel': 25,
    'South Africa': 26, 'Kenya': 20, 'Nigeria': 18, 'Egypt': 15,
    'Morocco': 20, 'Brazil': 22, 'Argentina': 21, 'Colombia': 19,
    'Peru': 15, 'Chile': 13, 'Uruguay': 20, 'Costa Rica': 15
}

# Approximate average monthly rent for 1BR in city center (USD)
cityRent1BR = {
    'New York': 3500, 'San Francisco': 3200, 'Los Angeles': 2400, 'Chicago': 2000,
    'Miami': 2500, 'Austin': 1800, 'Seattle': 2200, 'Denver': 1900, 'Boston': 2800,
    'Washington DC': 2400, 'Houston': 1600, 'Toronto': 2000, 'Vancouver': 2100,
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
    'Software Engineer': {'low': 45000, 'mid': 85000, 'high': 180000},
    'Data Scientist': {'low': 50000, 'mid': 95000, 'high': 170000},
    'Product Manager': {'low': 55000, 'mid': 100000, 'high': 190000},
    'UX Designer': {'low': 40000, 'mid': 75000, 'high': 140000},
    'Marketing Manager': {'low': 38000, 'mid': 72000, 'high': 135000},
    'Financial Analyst': {'low': 42000, 'mid': 78000, 'high': 145000},
    'Project Manager': {'low': 45000, 'mid': 80000, 'high': 150000},
    'DevOps Engineer': {'low': 50000, 'mid': 95000, 'high': 175000},
    'Graphic Designer': {'low': 30000, 'mid': 55000, 'high': 100000},
    'Sales Manager': {'low': 40000, 'mid': 80000, 'high': 160000},
    'HR Manager': {'low': 38000, 'mid': 70000, 'high': 130000},
    'Business Analyst': {'low': 42000, 'mid': 75000, 'high': 140000},
    'Accountant': {'low': 35000, 'mid': 62000, 'high': 110000},
    'Teacher': {'low': 25000, 'mid': 48000, 'high': 85000},
    'Nurse': {'low': 30000, 'mid': 58000, 'high': 100000},
    'Mechanical Engineer': {'low': 40000, 'mid': 78000, 'high': 140000},
    'Architect': {'low': 38000, 'mid': 72000, 'high': 130000},
    'Lawyer': {'low': 50000, 'mid': 100000, 'high': 220000},
    'Consultant': {'low': 45000, 'mid': 90000, 'high': 180000},
    'Content Writer': {'low': 25000, 'mid': 50000, 'high': 90000},
}

CURRENT_YEAR = date.today().year

# Map cities to relevant blog articles for cross-linking
cityBlogLinks = {
    'London': [
        {'url': '/blog/articles/london-vs-new-york-true-cost-comparison.html', 'title': 'London vs New York: The True Cost Comparison'},
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026.html', 'title': 'Most Expensive Cities in the World'},
    ],
    'New York': [
        {'url': '/blog/articles/london-vs-new-york-true-cost-comparison.html', 'title': 'London vs New York: The True Cost Comparison'},
        {'url': '/blog/articles/average-salary-by-city-2026-global-comparison.html', 'title': 'Average Salary by City: Global Comparison'},
    ],
    'Dubai': [
        {'url': '/blog/articles/dubai-vs-singapore-expat-comparison.html', 'title': 'Dubai vs Singapore: Expat Comparison'},
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026.html', 'title': 'Most Expensive Cities in the World'},
    ],
    'Singapore': [
        {'url': '/blog/articles/dubai-vs-singapore-expat-comparison.html', 'title': 'Dubai vs Singapore: Expat Comparison'},
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026.html', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
    ],
    'Bangkok': [
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026.html', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
        {'url': '/blog/articles/top-10-cities-for-remote-workers-2026.html', 'title': 'Top 10 Cities for Remote Workers'},
    ],
    'Chiang Mai': [
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026.html', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
        {'url': '/blog/articles/top-10-cities-for-remote-workers-2026.html', 'title': 'Top 10 Cities for Remote Workers'},
    ],
    'Ho Chi Minh City': [
        {'url': '/blog/articles/cost-of-living-southeast-asia-digital-nomads-2026.html', 'title': 'Cost of Living in Southeast Asia for Digital Nomads'},
    ],
    'Lisbon': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026.html', 'title': 'Affordable Cities in Europe for Americans'},
        {'url': '/blog/articles/top-10-cities-for-remote-workers-2026.html', 'title': 'Top 10 Cities for Remote Workers'},
    ],
    'Barcelona': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026.html', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'Prague': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026.html', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'Budapest': [
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026.html', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'San Francisco': [
        {'url': '/blog/articles/tech-salary-comparison-by-city-2026.html', 'title': 'Tech Salary Comparison by City'},
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026.html', 'title': 'Most Expensive Cities in the World'},
    ],
    'Tokyo': [
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026.html', 'title': 'Most Expensive Cities in the World'},
        {'url': '/blog/articles/average-salary-by-city-2026-global-comparison.html', 'title': 'Average Salary by City: Global Comparison'},
    ],
    'Berlin': [
        {'url': '/blog/articles/tech-salary-comparison-by-city-2026.html', 'title': 'Tech Salary Comparison by City'},
        {'url': '/blog/articles/affordable-cities-in-europe-for-americans-2026.html', 'title': 'Affordable Cities in Europe for Americans'},
    ],
    'Zurich': [
        {'url': '/blog/articles/most-expensive-cities-in-the-world-2026.html', 'title': 'Most Expensive Cities in the World'},
    ],
    '_default': [
        {'url': '/blog/articles/how-cost-of-living-affects-your-salary.html', 'title': 'How Cost of Living Affects Your Salary'},
        {'url': '/blog/articles/salary-negotiation-when-relocating-abroad.html', 'title': 'Salary Negotiation When Relocating Abroad'},
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
    tax = countryTaxRates.get(country, 20)
    mid_salary_annual = 75000 * (coli / 100)
    monthly_after_tax = (mid_salary_annual * (1 - tax / 100)) / 12
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
                'url': f'/compare/{slug1}-vs-{slug2}.html',
                'other_city': other,
            })
    return results


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
    tax_rate = countryTaxRates.get(country, 0)
    rent = cityRent1BR.get(city, 0)
    neighborhoods = cityNeighborhoods.get(city, {})

    # Convert $75K USD to local currency equivalent for the "sample salary"
    rate_to_local = exchangeRates[currency] / exchangeRates['USD']
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
            'diff_pct': ((coliData[comp] / coli) - 1) * 100
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
            neighborhood_rows += f'''
                        <tr>
                            <td style="font-weight: 500;">{name}</td>
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
                            <td><a href="/city/{comp_slug}.html" style="color: #2563eb; text-decoration: none; font-weight: 500;">{comp_city_name}</a></td>
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
        similar_links += f'<a href="/city/{sc_slug}.html" class="similar-city-link">{sc}</a>\n'

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
    monthly_salary_after_tax = (mid_salary_local * (1 - tax_rate / 100)) / 12
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
            'q': f'What is the income tax rate in {country}?',
            'a': f'The approximate effective income tax rate for a mid-range earner in {country} is {tax_note}.'
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
    if tax_rate == 0:
        tax_paragraph = '<p>The approximate average effective income tax rate in ' + country + ' is <strong>0%</strong>. This is a tax-free jurisdiction.</p>'
    elif tax_rate is not None:
        tax_paragraph = '<p>The approximate average effective income tax rate in ' + country + ' is <strong>' + str(tax_rate) + '%</strong> for a mid-range earner.</p>'
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

    # Compare with other cities section
    comp_section = ''
    if city_comps:
        comp_section = '<section class="content-card"><h2>Compare ' + city + ' With Other Cities</h2><p>See detailed side-by-side comparisons of salaries, rent, taxes, and neighborhoods.</p><div class="similar-cities">' + comp_links_html + '</div></section>'

    # Related articles section
    related_section = ''
    if blog_links_html:
        related_section = '<section class="content-card"><h2>Related Articles</h2>' + blog_links_html + '</section>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cost of Living in {city}, {country} — Salary Comparison & Neighborhood Guide {CURRENT_YEAR}</title>
    <meta name="description" content="Compare salaries and cost of living in {city}. COLI index: {coli} (rank #{rank}/{total_cities}). Explore {len(neighborhoods)} neighborhoods, tax rates, and equivalent salaries across cities.">
    <meta name="keywords" content="{city} cost of living, {city} salary, {city} neighborhoods, cost of living {country}, salary comparison {city}, {city} rent prices {CURRENT_YEAR}">
    <meta name="author" content="salary:converter">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/city/{slug}.html">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://salary-converter.com/city/{slug}.html">
    <meta property="og:title" content="Cost of Living in {city} — Salary & Neighborhood Guide {CURRENT_YEAR}">
    <meta property="og:description" content="COLI index: {coli} (#{rank}/{total_cities}). Compare salaries, explore {len(neighborhoods)} neighborhoods, and see what your salary is worth in {city}.">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Cost of Living in {city} — Salary & Neighborhood Guide {CURRENT_YEAR}">
    <meta name="twitter:description" content="COLI index: {coli} (#{rank}/{total_cities}). Compare salaries, explore neighborhoods, and plan your move to {city}.">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Cost of Living in {city}, {country} — {CURRENT_YEAR} Guide",
        "description": "Comprehensive cost of living guide for {city} with neighborhood data, salary comparisons, and tax information.",
        "url": "https://salary-converter.com/city/{slug}.html",
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
            {{"@type": "ListItem", "position": 3, "name": "{city}", "item": "https://salary-converter.com/city/{slug}.html"}}
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
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f7; color: #1d1d1f; min-height: 100vh;
            padding: 20px 12px;
            -webkit-font-smoothing: antialiased;
        }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: #1d1d1f; text-decoration: none;
        }}
        .nav-logo span {{ color: #2563eb; }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: #86868b;
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: #2563eb; }}
        .breadcrumb {{
            font-size: 0.8rem; color: #86868b; margin-bottom: 24px;
        }}
        .breadcrumb a {{ color: #2563eb; text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .hero {{
            background: white; border-radius: 20px; padding: 40px 32px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{
            font-size: 2.2rem; font-weight: 700; letter-spacing: -0.5px;
            margin-bottom: 8px; color: #1d1d1f;
        }}
        .hero .subtitle {{
            font-size: 1.05rem; color: #86868b; margin-bottom: 24px;
        }}
        .stat-grid {{
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
            margin-top: 24px;
        }}
        .stat-card {{
            background: #f5f5f7; border-radius: 14px; padding: 16px 12px;
            text-align: center;
        }}
        .stat-card .stat-value {{
            font-size: 1.5rem; font-weight: 700; color: #2563eb;
        }}
        .stat-card .stat-label {{
            font-size: 0.75rem; color: #86868b; margin-top: 4px;
            text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;
        }}
        .content-card {{
            background: white; border-radius: 20px; padding: 32px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); margin-bottom: 24px;
        }}
        .content-card h2 {{
            font-size: 1.3rem; font-weight: 700; margin-bottom: 16px;
            color: #1d1d1f; letter-spacing: -0.3px;
        }}
        .content-card p {{
            font-size: 0.92rem; color: #4a4a4c; line-height: 1.7;
            margin-bottom: 16px;
        }}
        table {{
            width: 100%; border-collapse: collapse; font-size: 0.88rem;
        }}
        table th {{
            text-align: left; padding: 10px 12px; font-size: 0.75rem;
            text-transform: uppercase; letter-spacing: 0.5px;
            color: #86868b; border-bottom: 2px solid #e5e5ea; font-weight: 600;
        }}
        table td {{
            padding: 10px 12px; border-bottom: 1px solid #f0f0f2; color: #1d1d1f;
        }}
        table tr:hover td {{ background: #f9f9fb; }}
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
            display: inline-block; padding: 8px 16px; background: #f5f5f7;
            border-radius: 100px; font-size: 0.82rem; font-weight: 500;
            color: #1d1d1f; text-decoration: none; transition: all 0.2s;
        }}
        .similar-city-link:hover {{
            background: #2563eb; color: white;
        }}
        .page-footer {{
            text-align: center; padding: 32px 0 16px; margin-top: 16px;
            border-top: 1px solid #e5e5ea;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: #86868b; text-decoration: none; margin: 0 12px;
        }}
        .page-footer a:hover {{ color: #2563eb; }}
        .tax-bar {{
            background: #f5f5f7; border-radius: 10px; padding: 3px; margin: 8px 0;
        }}
        .tax-bar-fill {{
            height: 8px; border-radius: 8px;
            background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
        }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}

        @media (max-width: 768px) {{
            body {{ padding: 0; background: white; }}
            .page-wrapper {{ padding: 0 16px; }}
            .hero {{ border-radius: 0; padding: 32px 20px; box-shadow: none; }}
            .stat-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .content-card {{ border-radius: 16px; padding: 20px; }}
            .hero h1 {{ font-size: 1.6rem; }}
            .two-col {{ grid-template-columns: 1fr; }}
            .cta-section {{ border-radius: 16px; padding: 32px 20px; }}
            table {{ font-size: 0.82rem; }}
            table th, table td {{ padding: 8px; }}
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
                <a href="/compare/">Compare</a>
                <a href="/blog/">Blog</a>
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
                    <div class="stat-value">{tax_rate}%</div>
                    <div class="stat-label">Avg Tax Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${rent:,}</div>
                    <div class="stat-label">1BR Rent/mo</div>
                </div>
            </div>
        </section>

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
            <p style="font-size: 0.8rem; color: #86868b; margin-top: 16px; margin-bottom: 0;">Estimates based on a mid-range salary adjusted for {city}'s COLI of {coli} and {country}'s effective tax rate of {tax_rate}%. Individual expenses will vary.</p>
        </section>

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
            <p>Understanding your take-home pay is critical when evaluating a move to {city}. With an effective tax rate of <strong>{tax_rate}%</strong> in {country} and average one-bedroom rent of <strong>${rent:,}/month</strong>, here is what a mid-range salary looks like:</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0;">
                <div class="stat-card">
                    <div class="stat-value" style="font-size: 1.2rem;">{fmt_mid_salary_local}</div>
                    <div class="stat-label">Gross Annual (Mid-Range)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="font-size: 1.2rem;">{fmt_monthly_salary}</div>
                    <div class="stat-label">Monthly After Tax</div>
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

        <section class="cta-section">
            <h2>Calculate Your Exact Salary</h2>
            <p>Use our free converter tool with 1,000+ neighborhood adjustments</p>
            <a href="/" class="cta-btn">Open Salary Converter</a>
        </section>

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {faq_html}
        </section>

        <section class="content-card">
            <h2>Data Sources &amp; Methodology</h2>
            <p>Our cost of living index uses New York City as the baseline (COLI = 100). Data is compiled from Numbeo, Expatistan, government statistics, and proprietary surveys. Salary ranges are estimated by adjusting global baseline figures by each city's COLI. Tax rates represent approximate effective rates for mid-range earners and do not constitute tax advice. Rent figures reflect average one-bedroom apartments in the city center.</p>
            <p style="font-size: 0.8rem; color: #86868b; margin-bottom: 0;">Last updated: {TODAY}. Data is refreshed periodically and may not reflect very recent changes.</p>
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
            <a href="/compare/">Compare</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
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
    tax1 = countryTaxRates.get(country1, 0)
    tax2 = countryTaxRates.get(country2, 0)
    rent1 = cityRent1BR.get(city1, 0)
    rent2 = cityRent1BR.get(city2, 0)
    neighborhoods1 = cityNeighborhoods.get(city1, {})
    neighborhoods2 = cityNeighborhoods.get(city2, {})
    total_cities = len(coliData)

    coli_ratio = coli2 / coli1
    coli_diff_pct = (coli_ratio - 1) * 100

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
    rent_diff_pct = abs(((rent2 / rent1) - 1) * 100) if rent1 > 0 else 0
    rent_cheaper_city = city1 if rent1 < rent2 else city2
    rent_more_city = city1 if rent1 >= rent2 else city2

    # Tax comparison text
    if tax1 == tax2:
        tax_compare_text = f'Both cities have the same effective tax rate of {tax1}%.'
    elif tax1 < tax2:
        tax_compare_text = f'{city1} has a lower effective tax rate ({tax1}%) compared to {city2} ({tax2}%), meaning you keep more of your gross salary in {city1}.'
    else:
        tax_compare_text = f'{city2} has a lower effective tax rate ({tax2}%) compared to {city1} ({tax1}%), meaning you keep more of your gross salary in {city2}.'

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
    job_compare_titles = ['Software Engineer', 'Product Manager', 'Data Scientist', 'Marketing Manager', 'Teacher', 'Nurse']
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
    tax1_winner = 'winner' if tax1 <= tax2 else ''
    tax2_winner = 'winner' if tax2 <= tax1 else ''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{city1} vs {city2}: Cost of Living & Salary Comparison {CURRENT_YEAR}</title>
    <meta name="description" content="Compare cost of living between {city1} (COLI: {coli1}) and {city2} (COLI: {coli2}). {cheaper_city} is {pct_cheaper:.0f}% cheaper. See salary equivalents, neighborhoods, and tax rates.">
    <meta name="keywords" content="{city1} vs {city2}, cost of living comparison, salary comparison, {city1} {city2} relocation, {city1} or {city2}">
    <meta name="author" content="salary:converter">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/compare/{slug1}-vs-{slug2}.html">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://salary-converter.com/compare/{slug1}-vs-{slug2}.html">
    <meta property="og:title" content="{city1} vs {city2}: Cost of Living & Salary Comparison {CURRENT_YEAR}">
    <meta property="og:description" content="{cheaper_city} is {pct_cheaper:.0f}% cheaper. Compare salaries, neighborhoods, tax rates, and more.">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{city1} vs {city2}: Salary & Cost of Living {CURRENT_YEAR}">
    <meta name="twitter:description" content="{cheaper_city} is {pct_cheaper:.0f}% cheaper. Full comparison with neighborhood data.">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{city1} vs {city2}: Cost of Living & Salary Comparison {CURRENT_YEAR}",
        "description": "Detailed comparison of cost of living, salaries, neighborhoods, and tax rates between {city1} and {city2}.",
        "url": "https://salary-converter.com/compare/{slug1}-vs-{slug2}.html",
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
            {{"@type": "ListItem", "position": 3, "name": "{city1} vs {city2}", "item": "https://salary-converter.com/compare/{slug1}-vs-{slug2}.html"}}
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
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f7; color: #1d1d1f; min-height: 100vh;
            padding: 20px 12px;
            -webkit-font-smoothing: antialiased;
        }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: #1d1d1f; text-decoration: none;
        }}
        .nav-logo span {{ color: #2563eb; }}
        .nav-links {{ display: flex; gap: 20px; align-items: center; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: #86868b;
            text-decoration: none; transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: #2563eb; }}
        .breadcrumb {{
            font-size: 0.8rem; color: #86868b; margin-bottom: 24px;
        }}
        .breadcrumb a {{ color: #2563eb; text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .hero {{
            background: white; border-radius: 20px; padding: 40px 32px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; }}
        .hero .subtitle {{ font-size: 1rem; color: #86868b; margin-bottom: 24px; }}
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
        .compare-col:first-child {{ border-right: 2px solid #e5e5ea; }}
        .compare-col .city-name {{
            font-size: 1.1rem; font-weight: 700; margin-bottom: 4px;
        }}
        .compare-col .country {{ font-size: 0.8rem; color: #86868b; margin-bottom: 16px; }}
        .compare-stat {{
            margin-bottom: 12px;
        }}
        .compare-stat .value {{
            font-size: 1.3rem; font-weight: 700; color: #2563eb;
        }}
        .compare-stat .label {{
            font-size: 0.7rem; color: #86868b; text-transform: uppercase;
            letter-spacing: 0.5px; font-weight: 500;
        }}
        .content-card {{
            background: white; border-radius: 20px; padding: 32px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); margin-bottom: 24px;
        }}
        .content-card h2 {{
            font-size: 1.3rem; font-weight: 700; margin-bottom: 16px;
            color: #1d1d1f;
        }}
        .content-card p {{
            font-size: 0.92rem; color: #4a4a4c; line-height: 1.7; margin-bottom: 16px;
        }}
        table {{
            width: 100%; border-collapse: collapse; font-size: 0.88rem;
        }}
        table th {{
            text-align: left; padding: 10px 12px; font-size: 0.75rem;
            text-transform: uppercase; letter-spacing: 0.5px;
            color: #86868b; border-bottom: 2px solid #e5e5ea; font-weight: 600;
        }}
        table td {{
            padding: 10px 12px; border-bottom: 1px solid #f0f0f2;
        }}
        .metric-row {{
            display: grid; grid-template-columns: 1fr 2fr 2fr; gap: 12px;
            padding: 14px 0; border-bottom: 1px solid #f0f0f2;
            align-items: center; font-size: 0.9rem;
        }}
        .metric-row:last-child {{ border-bottom: none; }}
        .metric-label {{ color: #86868b; font-weight: 500; font-size: 0.82rem; }}
        .metric-value {{ font-weight: 600; text-align: center; }}
        .winner {{ color: #22c55e; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
        .similar-cities {{
            display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px;
        }}
        .similar-city-link {{
            display: inline-block; padding: 8px 16px; background: #f5f5f7;
            border-radius: 100px; font-size: 0.82rem; font-weight: 500;
            color: #1d1d1f; text-decoration: none; transition: all 0.2s;
        }}
        .similar-city-link:hover {{
            background: #2563eb; color: white;
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
            border-top: 1px solid #e5e5ea;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: #86868b; text-decoration: none; margin: 0 12px;
        }}
        .page-footer a:hover {{ color: #2563eb; }}
        @media (max-width: 768px) {{
            body {{ padding: 0; background: white; }}
            .page-wrapper {{ padding: 0 16px; }}
            .hero {{ border-radius: 0; padding: 32px 16px; box-shadow: none; }}
            .hero h1 {{ font-size: 1.4rem; }}
            .compare-col {{ padding: 12px 8px; }}
            .compare-stat .value {{ font-size: 1.1rem; }}
            .content-card {{ border-radius: 16px; padding: 20px; }}
            .two-col {{ grid-template-columns: 1fr; }}
            .metric-row {{ grid-template-columns: 1fr 1fr 1fr; gap: 8px; font-size: 0.82rem; }}
            .cta-section {{ border-radius: 16px; padding: 32px 16px; }}
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
                <a href="/compare/">Compare</a>
                <a href="/blog/">Blog</a>
            </div>
        </nav>

        <div class="breadcrumb">
            <a href="/">Home</a> &rsaquo; <a href="/compare/">Compare</a> &rsaquo; {city1} vs {city2}
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
                <div class="metric-label">Income Tax Rate</div>
                <div class="metric-value {tax1_winner}">{tax1}%</div>
                <div class="metric-value {tax2_winner}">{tax2}%</div>
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
            <p>{tax_compare_text}{tax_free_note_1}{tax_free_note_2} When evaluating a relocation, remember that tax rates directly impact your take-home pay and should be weighed alongside cost of living differences.</p>
        </section>

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

        <section class="cta-section">
            <h2>Get Your Exact Number</h2>
            <p>Use our converter with 1,000+ neighborhood adjustments for a precise salary comparison</p>
            <a href="/" class="cta-btn">Open Salary Converter</a>
        </section>

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            {comp_faq_html}
        </section>

        <section class="content-card">
            <h2>Explore Each City</h2>
            <div class="similar-cities">
                <a href="/city/{slug1}.html" class="similar-city-link">{city1} Cost of Living Guide</a>
                <a href="/city/{slug2}.html" class="similar-city-link">{city2} Cost of Living Guide</a>
            </div>
        </section>

        <section class="content-card">
            <h2>Data Sources</h2>
            <p>Cost of living data is compiled from Numbeo, Expatistan, government statistics, and proprietary surveys. New York City is the baseline (COLI = 100). Tax rates represent approximate effective rates for mid-range earners. Rent figures reflect average one-bedroom apartments in the city center.</p>
            <p style="font-size: 0.8rem; color: #86868b; margin-bottom: 0;">Last updated: {TODAY}</p>
        </section>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/{slug1}.html">{city1}</a>
            <a href="/city/{slug2}.html">{city2}</a>
            <a href="/compare/">Compare</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
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
                        <a href="/city/{slug}.html" style="color: #2563eb; text-decoration: none;">{city}</a>
                    </td>
                    <td>{country}</td>
                    <td style="text-align: center; font-weight: 600;">{coli}</td>
                    <td style="text-align: center;">{currency}</td>
                    <td style="text-align: center;">{num_neighborhoods or "—"}</td>
                </tr>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f7; color: #1d1d1f; min-height: 100vh;
            padding: 20px 12px; -webkit-font-smoothing: antialiased;
        }}
        .page-wrapper {{ max-width: 960px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: #1d1d1f; text-decoration: none;
        }}
        .nav-logo span {{ color: #2563eb; }}
        .nav-links {{ display: flex; gap: 20px; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: #86868b;
            text-decoration: none;
        }}
        .nav-links a:hover {{ color: #2563eb; }}
        .hero {{
            background: white; border-radius: 20px; padding: 40px 32px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 8px; }}
        .hero p {{ color: #86868b; font-size: 1rem; }}
        .search-box {{
            margin-top: 20px; position: relative; max-width: 400px; margin-left: auto; margin-right: auto;
        }}
        .search-box input {{
            width: 100%; padding: 12px 16px; border: 2px solid #e5e5ea;
            border-radius: 12px; font-size: 0.95rem; font-family: inherit;
            outline: none; transition: border-color 0.2s;
        }}
        .search-box input:focus {{ border-color: #2563eb; }}
        .content-card {{
            background: white; border-radius: 20px; padding: 32px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); margin-bottom: 24px;
        }}
        table {{
            width: 100%; border-collapse: collapse; font-size: 0.88rem;
        }}
        table th {{
            text-align: left; padding: 10px 12px; font-size: 0.75rem;
            text-transform: uppercase; letter-spacing: 0.5px;
            color: #86868b; border-bottom: 2px solid #e5e5ea; font-weight: 600;
            position: sticky; top: 0; background: white;
        }}
        table td {{
            padding: 10px 12px; border-bottom: 1px solid #f0f0f2;
        }}
        table tr:hover td {{ background: #f9f9fb; }}
        .page-footer {{
            text-align: center; padding: 32px 0 16px; border-top: 1px solid #e5e5ea;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: #86868b; text-decoration: none; margin: 0 12px;
        }}
        .page-footer a:hover {{ color: #2563eb; }}
        @media (max-width: 768px) {{
            body {{ padding: 0; background: white; }}
            .page-wrapper {{ padding: 0 16px; }}
            .hero {{ border-radius: 0; padding: 32px 16px; box-shadow: none; }}
            .hero h1 {{ font-size: 1.5rem; }}
            .content-card {{ border-radius: 16px; padding: 16px; }}
            table {{ font-size: 0.8rem; }}
            table th, table td {{ padding: 8px 6px; }}
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
                <a href="/compare/">Compare</a>
                <a href="/blog/">Blog</a>
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
                        <th style="text-align: center;">Currency</th>
                        <th style="text-align: center;">Neighborhoods</th>
                    </tr>
                </thead>
                <tbody>{city_rows}
                </tbody>
            </table>
        </section>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/compare/">Compare Cities</a>
            <a href="/blog/">Blog</a>
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
</body>
</html>'''

    return html


# ============================================================
# COMPARE INDEX PAGE
# ============================================================

def generate_compare_index(comparison_pairs):
    pair_links = ''
    for city1, city2 in comparison_pairs:
        slug1 = slugify(city1)
        slug2 = slugify(city2)
        coli1 = coliData[city1]
        coli2 = coliData[city2]
        diff = abs(((coli2/coli1) - 1) * 100)
        pair_links += f'''
                <a href="/compare/{slug1}-vs-{slug2}.html" class="compare-card">
                    <div class="compare-card-cities">{city1} <span class="vs">vs</span> {city2}</div>
                    <div class="compare-card-stats">COLI: {coli1} vs {coli2} &middot; {diff:.0f}% difference</div>
                </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>City Comparisons — Cost of Living & Salary Side-by-Side {CURRENT_YEAR}</title>
    <meta name="description" content="Compare cost of living and salaries between popular city pairs. Side-by-side comparison of neighborhoods, tax rates, and purchasing power.">
    <meta name="author" content="salary:converter">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/compare/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://salary-converter.com/compare/">
    <meta property="og:title" content="City Cost of Living Comparisons {CURRENT_YEAR}">
    <meta property="og:description" content="Side-by-side comparison of salaries and cost of living between popular city pairs.">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:site_name" content="salary:converter">
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f7; color: #1d1d1f; min-height: 100vh;
            padding: 20px 12px; -webkit-font-smoothing: antialiased;
        }}
        .page-wrapper {{ max-width: 900px; margin: 0 auto; }}
        .nav-bar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
        }}
        .nav-logo {{
            font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
            color: #1d1d1f; text-decoration: none;
        }}
        .nav-logo span {{ color: #2563eb; }}
        .nav-links {{ display: flex; gap: 20px; }}
        .nav-links a {{
            font-size: 0.85rem; font-weight: 500; color: #86868b;
            text-decoration: none;
        }}
        .nav-links a:hover {{ color: #2563eb; }}
        .hero {{
            background: white; border-radius: 20px; padding: 40px 32px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); margin-bottom: 24px;
            text-align: center;
        }}
        .hero h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 8px; }}
        .hero p {{ color: #86868b; font-size: 1rem; }}
        .compare-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
        }}
        .compare-card {{
            background: white; border-radius: 16px; padding: 24px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.06); text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s; display: block;
        }}
        .compare-card:hover {{
            transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }}
        .compare-card-cities {{
            font-size: 1rem; font-weight: 700; color: #1d1d1f; margin-bottom: 6px;
        }}
        .compare-card-cities .vs {{
            color: #2563eb; font-size: 0.8rem; margin: 0 4px;
        }}
        .compare-card-stats {{
            font-size: 0.8rem; color: #86868b;
        }}
        .page-footer {{
            text-align: center; padding: 32px 0 16px; margin-top: 24px;
            border-top: 1px solid #e5e5ea;
        }}
        .page-footer a {{
            font-size: 0.82rem; color: #86868b; text-decoration: none; margin: 0 12px;
        }}
        .page-footer a:hover {{ color: #2563eb; }}
        @media (max-width: 768px) {{
            body {{ padding: 0; background: white; }}
            .page-wrapper {{ padding: 0 16px; }}
            .hero {{ border-radius: 0; padding: 32px 16px; box-shadow: none; }}
            .hero h1 {{ font-size: 1.5rem; }}
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
                <a href="/compare/">Compare</a>
                <a href="/blog/">Blog</a>
            </div>
        </nav>

        <section class="hero">
            <h1>City Comparisons</h1>
            <p>{len(comparison_pairs)} popular city-to-city comparisons with salary equivalents</p>
        </section>

        <div class="compare-grid">{pair_links}
        </div>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/">All Cities</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
</body>
</html>'''

    return html


# ============================================================
# SITEMAP GENERATION
# ============================================================

def generate_sitemap(comparison_pairs):
    """Generate sitemap.xml for all pages"""
    urls = []
    # Main pages
    urls.append('https://salary-converter.com/')
    urls.append('https://salary-converter.com/widget.html')
    urls.append('https://salary-converter.com/city/')
    urls.append('https://salary-converter.com/compare/')
    urls.append('https://salary-converter.com/blog/')

    # Blog articles
    blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog', 'articles')
    if os.path.isdir(blog_dir):
        for fname in sorted(os.listdir(blog_dir)):
            if fname.endswith('.html'):
                urls.append(f'https://salary-converter.com/blog/articles/{fname}')

    # City pages
    for city in coliData:
        slug = slugify(city)
        urls.append(f'https://salary-converter.com/city/{slug}.html')

    # Comparison pages
    for city1, city2 in comparison_pairs:
        slug1 = slugify(city1)
        slug2 = slugify(city2)
        urls.append(f'https://salary-converter.com/compare/{slug1}-vs-{slug2}.html')

    xml_entries = ''
    for url in urls:
        xml_entries += f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>\n'

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_entries}</urlset>
'''
    return sitemap


# ============================================================
# MAIN GENERATION LOGIC
# ============================================================

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    city_dir = os.path.join(base_dir, 'city')
    compare_dir = os.path.join(base_dir, 'compare')

    os.makedirs(city_dir, exist_ok=True)
    os.makedirs(compare_dir, exist_ok=True)

    # Define popular comparison pairs (high-traffic searches)
    comparison_pairs = [
        ('London', 'New York'),
        ('London', 'Dubai'),
        ('London', 'Singapore'),
        ('London', 'Paris'),
        ('London', 'Berlin'),
        ('London', 'Amsterdam'),
        ('London', 'Sydney'),
        ('London', 'Toronto'),
        ('London', 'Tokyo'),
        ('London', 'Dublin'),
        ('New York', 'San Francisco'),
        ('New York', 'Los Angeles'),
        ('New York', 'Chicago'),
        ('New York', 'Miami'),
        ('New York', 'Toronto'),
        ('New York', 'Tokyo'),
        ('New York', 'Singapore'),
        ('New York', 'Dubai'),
        ('New York', 'Berlin'),
        ('Dubai', 'Singapore'),
        ('Dubai', 'Abu Dhabi'),
        ('Dubai', 'Doha'),
        ('Dubai', 'Bangkok'),
        ('Dubai', 'Sydney'),
        ('Singapore', 'Hong Kong'),
        ('Singapore', 'Bangkok'),
        ('Singapore', 'Tokyo'),
        ('Singapore', 'Sydney'),
        ('Singapore', 'Kuala Lumpur'),
        ('Tokyo', 'Seoul'),
        ('Tokyo', 'Osaka'),
        ('Tokyo', 'Sydney'),
        ('Paris', 'Berlin'),
        ('Paris', 'Amsterdam'),
        ('Paris', 'Barcelona'),
        ('Paris', 'Rome'),
        ('Berlin', 'Munich'),
        ('Berlin', 'Amsterdam'),
        ('Berlin', 'Prague'),
        ('Berlin', 'Vienna'),
        ('Lisbon', 'Barcelona'),
        ('Lisbon', 'Madrid'),
        ('Lisbon', 'Porto'),
        ('Sydney', 'Melbourne'),
        ('Sydney', 'Auckland'),
        ('San Francisco', 'Austin'),
        ('San Francisco', 'Seattle'),
        ('Boston', 'Washington DC'),
        ('Bangkok', 'Bali (Denpasar)'),
        ('Bangkok', 'Ho Chi Minh City'),
        ('Bangkok', 'Chiang Mai'),
        ('Mexico City', 'Bogotá'),
        ('Mexico City', 'Medellín'),
        ('Buenos Aires', 'São Paulo'),
        ('Buenos Aires', 'Santiago'),
        ('Dubai', 'Tel Aviv'),
        ('Zurich', 'Geneva'),
        ('Stockholm', 'Copenhagen'),
        ('Mumbai', 'Bangalore'),
        ('Hong Kong', 'Taipei'),
    ]

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
    print("  Done: City index page created at /city/index.html")

    # Generate comparison pages
    print(f"Generating {len(comparison_pairs)} comparison pages...")
    for city1, city2 in comparison_pairs:
        slug1 = slugify(city1)
        slug2 = slugify(city2)
        filepath = os.path.join(compare_dir, f'{slug1}-vs-{slug2}.html')
        html = generate_comparison_page(city1, city2)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    print(f"  Done: {len(comparison_pairs)} comparison pages in /compare/")

    # Generate compare index page
    compare_index_path = os.path.join(compare_dir, 'index.html')
    with open(compare_index_path, 'w', encoding='utf-8') as f:
        f.write(generate_compare_index(comparison_pairs))
    print("  Done: Compare index page at /compare/index.html")

    # Generate sitemap
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(generate_sitemap(comparison_pairs))
    print("  Done: Sitemap generated at /sitemap.xml")

    # Summary
    print(f"\nTotal new pages: {len(coliData) + len(comparison_pairs) + 2}")
    print(f"Sitemap entries: {len(coliData) + len(comparison_pairs) + 4}")
