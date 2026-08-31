"""Local-market salary provenance copied from /is-my-salary-good/.

Do not invent new baselines here. NY/US mid figures live in salaryRanges
(generate-pages.py). Country multipliers and source badges are the same
verified / OECD-estimated / COLI tiers already shown on the benchmark tool.
"""

# Profession → market category used by countryMultipliers
JOB_TO_MARKET_CAT = {
    'Doctor (General)': 'medical_physician',
    'Surgeon': 'medical_physician',
    'Dentist': 'medical_dental',
    'Pharmacist': 'medical_other',
    'Nurse': 'medical_other',
    'Psychologist': 'medical_other',
    'Software Engineer': 'tech',
    'DevOps Engineer': 'tech',
    'Data Scientist': 'tech',
    'UX Designer': 'tech',
    'Product Manager': 'tech',
    'Mechanical Engineer': 'engineering',
    'Civil Engineer': 'engineering',
    'Electrical Engineer': 'engineering',
    'Architect': 'engineering',
    'Project Manager': 'business',
    'Financial Analyst': 'finance',
    'Accountant': 'finance',
    'Business Analyst': 'business',
    'Consultant': 'business',
    'Investment Banker': 'finance',
    'Actuary': 'finance',
    'Lawyer': 'law',
    'Paralegal': 'law',
    'Marketing Manager': 'business',
    'Sales Manager': 'business',
    'Graphic Designer': None,
    'Content Writer': None,
    'HR Manager': 'business',
    'Operations Manager': 'business',
    'CEO / Executive': 'business',
    'Teacher': 'education',
    'Professor': 'education',
    'Research Scientist': 'education',
    'Pilot': None,
    'Chef': None,
    'Journalist': None,
}

COUNTRY_MULTIPLIERS = {
    'United States': {'tech': 1.0, 'medical_physician': 1.0, 'medical_dental': 1.0, 'medical_other': 1.0, 'law': 1.0, 'finance': 1.0, 'business': 1.0, 'engineering': 1.0, 'education': 1.0},
    'Canada': {'tech': 0.66, 'medical_physician': 0.68, 'medical_dental': 0.65, 'medical_other': 0.65, 'law': 0.6, 'finance': 0.68, 'business': 0.57, 'engineering': 0.68, 'education': 1.04},
    'United Kingdom': {'tech': 0.46, 'medical_physician': 0.51, 'medical_dental': 0.4, 'medical_other': 0.54, 'law': 0.52, 'finance': 0.7, 'business': 0.58, 'engineering': 0.64, 'education': 1.06},
    'Ireland': {'tech': 0.58, 'medical_physician': 0.4, 'medical_dental': 0.48, 'medical_other': 0.45, 'law': 0.48, 'finance': 0.52, 'business': 0.5, 'engineering': 0.5, 'education': 0.5},
    'Germany': {'tech': 0.59, 'medical_physician': 0.39, 'medical_dental': 0.4, 'medical_other': 0.59, 'law': 0.55, 'finance': 0.65, 'business': 0.59, 'engineering': 0.89, 'education': 1.13},
    'Netherlands': {'tech': 0.58, 'medical_physician': 0.45, 'medical_dental': 0.42, 'medical_other': 0.49, 'law': 0.54, 'finance': 0.73, 'business': 0.59, 'engineering': 0.7, 'education': 0.86},
    'Switzerland': {'tech': 0.75, 'medical_physician': 0.55, 'medical_dental': 0.6, 'medical_other': 0.58, 'law': 0.58, 'finance': 0.72, 'business': 0.65, 'engineering': 0.68, 'education': 0.72},
    'France': {'tech': 0.46, 'medical_physician': 0.43, 'medical_dental': 0.3, 'medical_other': 0.46, 'law': 0.55, 'finance': 0.65, 'business': 0.51, 'engineering': 0.63, 'education': 0.69},
    'Belgium': {'tech': 0.45, 'medical_physician': 0.3, 'medical_dental': 0.36, 'medical_other': 0.38, 'law': 0.38, 'finance': 0.45, 'business': 0.42, 'engineering': 0.44, 'education': 0.48},
    'Luxembourg': {'tech': 0.58, 'medical_physician': 0.4, 'medical_dental': 0.46, 'medical_other': 0.44, 'law': 0.48, 'finance': 0.65, 'business': 0.55, 'engineering': 0.54, 'education': 0.58},
    'Sweden': {'tech': 0.45, 'medical_physician': 0.42, 'medical_dental': 0.4, 'medical_other': 0.49, 'law': 0.53, 'finance': 0.68, 'business': 0.55, 'engineering': 0.63, 'education': 0.75},
    'Norway': {'tech': 0.52, 'medical_physician': 0.4, 'medical_dental': 0.48, 'medical_other': 0.48, 'law': 0.48, 'finance': 0.52, 'business': 0.5, 'engineering': 0.55, 'education': 0.58},
    'Denmark': {'tech': 0.5, 'medical_physician': 0.35, 'medical_dental': 0.45, 'medical_other': 0.44, 'law': 0.44, 'finance': 0.5, 'business': 0.47, 'engineering': 0.5, 'education': 0.55},
    'Finland': {'tech': 0.45, 'medical_physician': 0.32, 'medical_dental': 0.4, 'medical_other': 0.4, 'law': 0.4, 'finance': 0.44, 'business': 0.42, 'engineering': 0.45, 'education': 0.48},
    'Austria': {'tech': 0.45, 'medical_physician': 0.32, 'medical_dental': 0.4, 'medical_other': 0.38, 'law': 0.38, 'finance': 0.44, 'business': 0.42, 'engineering': 0.46, 'education': 0.52},
    'Spain': {'tech': 0.32, 'medical_physician': 0.28, 'medical_dental': 0.32, 'medical_other': 0.28, 'law': 0.3, 'finance': 0.32, 'business': 0.32, 'engineering': 0.32, 'education': 0.32},
    'Portugal': {'tech': 0.28, 'medical_physician': 0.22, 'medical_dental': 0.28, 'medical_other': 0.24, 'law': 0.25, 'finance': 0.28, 'business': 0.28, 'engineering': 0.28, 'education': 0.28},
    'Italy': {'tech': 0.32, 'medical_physician': 0.28, 'medical_dental': 0.35, 'medical_other': 0.3, 'law': 0.3, 'finance': 0.32, 'business': 0.32, 'engineering': 0.32, 'education': 0.32},
    'Greece': {'tech': 0.25, 'medical_physician': 0.22, 'medical_dental': 0.26, 'medical_other': 0.22, 'law': 0.24, 'finance': 0.25, 'business': 0.24, 'engineering': 0.25, 'education': 0.24},
    'Czech Republic': {'tech': 0.28, 'medical_physician': 0.22, 'medical_dental': 0.26, 'medical_other': 0.22, 'law': 0.24, 'finance': 0.26, 'business': 0.26, 'engineering': 0.26, 'education': 0.26},
    'Poland': {'tech': 0.28, 'medical_physician': 0.2, 'medical_dental': 0.24, 'medical_other': 0.2, 'law': 0.22, 'finance': 0.24, 'business': 0.24, 'engineering': 0.24, 'education': 0.24},
    'Hungary': {'tech': 0.22, 'medical_physician': 0.18, 'medical_dental': 0.2, 'medical_other': 0.18, 'law': 0.18, 'finance': 0.2, 'business': 0.2, 'engineering': 0.2, 'education': 0.2},
    'Romania': {'tech': 0.2, 'medical_physician': 0.16, 'medical_dental': 0.18, 'medical_other': 0.16, 'law': 0.16, 'finance': 0.18, 'business': 0.18, 'engineering': 0.18, 'education': 0.16},
    'Estonia': {'tech': 0.3, 'medical_physician': 0.22, 'medical_dental': 0.26, 'medical_other': 0.22, 'law': 0.24, 'finance': 0.26, 'business': 0.26, 'engineering': 0.26, 'education': 0.26},
    'Latvia': {'tech': 0.25, 'medical_physician': 0.18, 'medical_dental': 0.22, 'medical_other': 0.18, 'law': 0.2, 'finance': 0.22, 'business': 0.22, 'engineering': 0.22, 'education': 0.2},
    'Croatia': {'tech': 0.25, 'medical_physician': 0.18, 'medical_dental': 0.22, 'medical_other': 0.18, 'law': 0.2, 'finance': 0.22, 'business': 0.22, 'engineering': 0.22, 'education': 0.2},
    'Turkey': {'tech': 0.18, 'medical_physician': 0.15, 'medical_dental': 0.16, 'medical_other': 0.14, 'law': 0.15, 'finance': 0.17, 'business': 0.16, 'engineering': 0.16, 'education': 0.15},
    'Israel': {'tech': 0.65, 'medical_physician': 0.4, 'medical_dental': 0.45, 'medical_other': 0.38, 'law': 0.44, 'finance': 0.55, 'business': 0.5, 'engineering': 0.52, 'education': 0.48},
    'UAE': {'tech': 0.58, 'medical_physician': 0.5, 'medical_dental': 0.52, 'medical_other': 0.44, 'law': 0.52, 'finance': 0.58, 'business': 0.5, 'engineering': 0.52, 'education': 0.42},
    'Qatar': {'tech': 0.52, 'medical_physician': 0.55, 'medical_dental': 0.5, 'medical_other': 0.42, 'law': 0.46, 'finance': 0.52, 'business': 0.46, 'engineering': 0.5, 'education': 0.4},
    'Saudi Arabia': {'tech': 0.42, 'medical_physician': 0.48, 'medical_dental': 0.44, 'medical_other': 0.38, 'law': 0.38, 'finance': 0.44, 'business': 0.4, 'engineering': 0.44, 'education': 0.36},
    'Japan': {'tech': 0.32, 'medical_physician': 0.32, 'medical_dental': 0.35, 'medical_other': 0.3, 'law': 0.35, 'finance': 0.38, 'business': 0.35, 'engineering': 0.4, 'education': 0.45},
    'South Korea': {'tech': 0.35, 'medical_physician': 0.35, 'medical_dental': 0.38, 'medical_other': 0.3, 'law': 0.36, 'finance': 0.38, 'business': 0.35, 'engineering': 0.38, 'education': 0.45},
    'China': {'tech': 0.22, 'medical_physician': 0.15, 'medical_dental': 0.18, 'medical_other': 0.14, 'law': 0.18, 'finance': 0.22, 'business': 0.2, 'engineering': 0.22, 'education': 0.16},
    'China (SAR)': {'tech': 0.58, 'medical_physician': 0.45, 'medical_dental': 0.48, 'medical_other': 0.4, 'law': 0.58, 'finance': 0.65, 'business': 0.52, 'engineering': 0.5, 'education': 0.45},
    'Taiwan': {'tech': 0.32, 'medical_physician': 0.3, 'medical_dental': 0.32, 'medical_other': 0.28, 'law': 0.28, 'finance': 0.32, 'business': 0.3, 'engineering': 0.32, 'education': 0.32},
    'Singapore': {'tech': 0.62, 'medical_physician': 0.55, 'medical_dental': 0.55, 'medical_other': 0.45, 'law': 0.55, 'finance': 0.62, 'business': 0.58, 'engineering': 0.55, 'education': 0.55},
    'Malaysia': {'tech': 0.18, 'medical_physician': 0.2, 'medical_dental': 0.2, 'medical_other': 0.16, 'law': 0.18, 'finance': 0.2, 'business': 0.18, 'engineering': 0.18, 'education': 0.16},
    'Thailand': {'tech': 0.14, 'medical_physician': 0.15, 'medical_dental': 0.15, 'medical_other': 0.12, 'law': 0.12, 'finance': 0.14, 'business': 0.13, 'engineering': 0.13, 'education': 0.12},
    'Vietnam': {'tech': 0.1, 'medical_physician': 0.08, 'medical_dental': 0.08, 'medical_other': 0.07, 'law': 0.07, 'finance': 0.09, 'business': 0.08, 'engineering': 0.09, 'education': 0.07},
    'Philippines': {'tech': 0.1, 'medical_physician': 0.08, 'medical_dental': 0.09, 'medical_other': 0.07, 'law': 0.07, 'finance': 0.09, 'business': 0.08, 'engineering': 0.08, 'education': 0.07},
    'Indonesia': {'tech': 0.1, 'medical_physician': 0.08, 'medical_dental': 0.09, 'medical_other': 0.07, 'law': 0.07, 'finance': 0.09, 'business': 0.08, 'engineering': 0.09, 'education': 0.07},
    'Cambodia': {'tech': 0.1, 'medical_physician': 0.07, 'medical_dental': 0.07, 'medical_other': 0.06, 'law': 0.06, 'finance': 0.08, 'business': 0.07, 'engineering': 0.07, 'education': 0.06},
    'India': {'tech': 0.13, 'medical_physician': 0.08, 'medical_dental': 0.09, 'medical_other': 0.07, 'law': 0.07, 'finance': 0.1, 'business': 0.1, 'engineering': 0.11, 'education': 0.08},
    'Australia': {'tech': 0.57, 'medical_physician': 0.51, 'medical_dental': 0.62, 'medical_other': 0.54, 'law': 0.45, 'finance': 0.55, 'business': 0.67, 'engineering': 0.64, 'education': 1.04},
    'New Zealand': {'tech': 0.48, 'medical_physician': 0.53, 'medical_dental': 0.5, 'medical_other': 0.52, 'law': 0.4, 'finance': 0.52, 'business': 0.41, 'engineering': 0.57, 'education': 0.76},
    'Brazil': {'tech': 0.18, 'medical_physician': 0.18, 'medical_dental': 0.18, 'medical_other': 0.15, 'law': 0.15, 'finance': 0.18, 'business': 0.16, 'engineering': 0.16, 'education': 0.14},
    'Argentina': {'tech': 0.14, 'medical_physician': 0.12, 'medical_dental': 0.12, 'medical_other': 0.1, 'law': 0.1, 'finance': 0.12, 'business': 0.11, 'engineering': 0.12, 'education': 0.1},
    'Colombia': {'tech': 0.12, 'medical_physician': 0.12, 'medical_dental': 0.12, 'medical_other': 0.1, 'law': 0.1, 'finance': 0.11, 'business': 0.1, 'engineering': 0.11, 'education': 0.09},
    'Chile': {'tech': 0.17, 'medical_physician': 0.18, 'medical_dental': 0.18, 'medical_other': 0.14, 'law': 0.14, 'finance': 0.16, 'business': 0.15, 'engineering': 0.16, 'education': 0.13},
    'Peru': {'tech': 0.12, 'medical_physician': 0.12, 'medical_dental': 0.12, 'medical_other': 0.09, 'law': 0.09, 'finance': 0.1, 'business': 0.09, 'engineering': 0.1, 'education': 0.08},
    'Uruguay': {'tech': 0.18, 'medical_physician': 0.16, 'medical_dental': 0.16, 'medical_other': 0.13, 'law': 0.13, 'finance': 0.15, 'business': 0.14, 'engineering': 0.14, 'education': 0.13},
    'Mexico': {'tech': 0.18, 'medical_physician': 0.15, 'medical_dental': 0.15, 'medical_other': 0.12, 'law': 0.12, 'finance': 0.16, 'business': 0.14, 'engineering': 0.14, 'education': 0.12},
    'Costa Rica': {'tech': 0.22, 'medical_physician': 0.18, 'medical_dental': 0.18, 'medical_other': 0.14, 'law': 0.14, 'finance': 0.18, 'business': 0.16, 'engineering': 0.16, 'education': 0.14},
    'Panama': {'tech': 0.22, 'medical_physician': 0.18, 'medical_dental': 0.18, 'medical_other': 0.14, 'law': 0.14, 'finance': 0.2, 'business': 0.18, 'engineering': 0.18, 'education': 0.14},
    'South Africa': {'tech': 0.18, 'medical_physician': 0.18, 'medical_dental': 0.2, 'medical_other': 0.15, 'law': 0.16, 'finance': 0.18, 'business': 0.16, 'engineering': 0.18, 'education': 0.14},
    'Kenya': {'tech': 0.1, 'medical_physician': 0.08, 'medical_dental': 0.08, 'medical_other': 0.06, 'law': 0.06, 'finance': 0.08, 'business': 0.07, 'engineering': 0.07, 'education': 0.06},
    'Nigeria': {'tech': 0.1, 'medical_physician': 0.07, 'medical_dental': 0.07, 'medical_other': 0.06, 'law': 0.06, 'finance': 0.08, 'business': 0.07, 'engineering': 0.07, 'education': 0.06},
    'Egypt': {'tech': 0.08, 'medical_physician': 0.07, 'medical_dental': 0.07, 'medical_other': 0.06, 'law': 0.05, 'finance': 0.07, 'business': 0.06, 'engineering': 0.07, 'education': 0.05},
    'Morocco': {'tech': 0.1, 'medical_physician': 0.08, 'medical_dental': 0.08, 'medical_other': 0.07, 'law': 0.07, 'finance': 0.09, 'business': 0.08, 'engineering': 0.08, 'education': 0.07},
}

COUNTRY_SOURCES = {
    'United States': {
        "verified": True,
        "source": 'BLS OES May 2024 · Doximity 2025 · NALP 2025 · Levels.fyi',
        "url": 'https://www.bls.gov/oes/',
        "unverifiedCats": [],
    },
    'United Kingdom': {
        "verified": True,
        "source": 'ONS ASHE April 2024 · DfE School Workforce England 2024',
        "url": 'https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2024',
        "unverifiedCats": ['medical_dental'],
    },
    'Germany': {
        "verified": True,
        "source": 'Bundesagentur für Arbeit Entgeltatlas 2024 · Destatis',
        "url": 'https://web.arbeitsagentur.de/entgeltatlas/',
        "unverifiedCats": ['medical_dental'],
    },
    'Canada': {
        "verified": True,
        "source": 'Canada Job Bank LFS 2023–2024 · CIHI Physician Data',
        "url": 'https://www.jobbank.gc.ca/trend-analysis/search-wages',
        "unverifiedCats": ['medical_dental'],
    },
    'Australia': {
        "verified": True,
        "source": 'ABS Employee Earnings Aug 2024 · Jobs and Skills Australia',
        "url": 'https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/employee-earnings/aug-2024',
        "unverifiedCats": ['medical_dental', 'law'],
    },
    'Sweden': {
        "verified": True,
        "source": 'SCB Salary Structures, Whole Economy 2024',
        "url": 'https://www.scb.se/en/finding-statistics/statistics-by-subject-area/labour-market/wages-salaries-and-labour-costs/salary-structures-whole-economy/',
        "unverifiedCats": ['medical_dental'],
    },
    'France': {
        "verified": True,
        "source": 'INSEE DADS 2022 (most recent full-year data)',
        "url": 'https://www.insee.fr/fr/statistiques/7707884',
        "unverifiedCats": ['medical_dental', 'medical_physician'],
    },
    'Netherlands': {
        "verified": True,
        "source": 'CBS Statistics Netherlands 2022 · Eurostat SES 2022',
        "url": 'https://www.cbs.nl/en-gb/labour-and-income',
        "unverifiedCats": ['medical_dental'],
    },
    'New Zealand': {
        "verified": True,
        "source": 'Stats NZ Labour Market Income Jun 2024 · Immigration NZ',
        "url": 'https://www.stats.govt.nz/information-releases/labour-market-statistics-income-june-2024-quarter/',
        "unverifiedCats": ['medical_dental'],
    },
    'Ireland': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + CSO Ireland',
        "url": '',
        "unverifiedCats": [],
    },
    'Switzerland': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + FSO Switzerland',
        "url": '',
        "unverifiedCats": [],
    },
    'Belgium': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Statbel',
        "url": '',
        "unverifiedCats": [],
    },
    'Luxembourg': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios',
        "url": '',
        "unverifiedCats": [],
    },
    'Norway': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + SSB Norway',
        "url": '',
        "unverifiedCats": [],
    },
    'Denmark': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Statistics Denmark',
        "url": '',
        "unverifiedCats": [],
    },
    'Finland': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Statistics Finland',
        "url": '',
        "unverifiedCats": [],
    },
    'Austria': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Statistik Austria',
        "url": '',
        "unverifiedCats": [],
    },
    'Spain': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + INE Spain',
        "url": '',
        "unverifiedCats": [],
    },
    'Portugal': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + INE Portugal',
        "url": '',
        "unverifiedCats": [],
    },
    'Italy': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + ISTAT',
        "url": '',
        "unverifiedCats": [],
    },
    'Greece': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Eurostat',
        "url": '',
        "unverifiedCats": [],
    },
    'Czech Republic': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Czech Statistical Office',
        "url": '',
        "unverifiedCats": [],
    },
    'Poland': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + GUS Poland',
        "url": '',
        "unverifiedCats": [],
    },
    'Hungary': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + HCSO',
        "url": '',
        "unverifiedCats": [],
    },
    'Romania': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + INS Romania',
        "url": '',
        "unverifiedCats": [],
    },
    'Estonia': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Statistics Estonia',
        "url": '',
        "unverifiedCats": [],
    },
    'Latvia': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + CSB Latvia',
        "url": '',
        "unverifiedCats": [],
    },
    'Croatia': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + DZS Croatia',
        "url": '',
        "unverifiedCats": [],
    },
    'Japan': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + MHLW Japan',
        "url": '',
        "unverifiedCats": [],
    },
    'South Korea': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + Statistics Korea',
        "url": '',
        "unverifiedCats": [],
    },
    'Singapore': {
        "verified": False,
        "source": 'Estimated · MOM Singapore surveys',
        "url": '',
        "unverifiedCats": [],
    },
    'Israel': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + CBS Israel',
        "url": '',
        "unverifiedCats": [],
    },
    'Turkey': {
        "verified": False,
        "source": 'Estimated · OECD wage ratios + TURKSTAT',
        "url": '',
        "unverifiedCats": [],
    },
    'UAE': {
        "verified": False,
        "source": 'Estimated · Mercer Gulf surveys',
        "url": '',
        "unverifiedCats": [],
    },
    'Qatar': {
        "verified": False,
        "source": 'Estimated · Mercer Gulf surveys',
        "url": '',
        "unverifiedCats": [],
    },
    'Saudi Arabia': {
        "verified": False,
        "source": 'Estimated · Mercer Gulf surveys',
        "url": '',
        "unverifiedCats": [],
    },
    'China': {
        "verified": False,
        "source": 'Estimated · NBS China wage surveys',
        "url": '',
        "unverifiedCats": [],
    },
    'China (SAR)': {
        "verified": False,
        "source": 'Estimated · Census & Statistics HK',
        "url": '',
        "unverifiedCats": [],
    },
    'Taiwan': {
        "verified": False,
        "source": 'Estimated · DGBAS Taiwan',
        "url": '',
        "unverifiedCats": [],
    },
    'India': {
        "verified": False,
        "source": 'Estimated · NSSO India (limited coverage)',
        "url": '',
        "unverifiedCats": [],
    },
    'Malaysia': {
        "verified": False,
        "source": 'Estimated · DOSM Malaysia',
        "url": '',
        "unverifiedCats": [],
    },
    'Thailand': {
        "verified": False,
        "source": 'Estimated · NSO Thailand',
        "url": '',
        "unverifiedCats": [],
    },
    'Vietnam': {
        "verified": False,
        "source": 'Estimated · GSO Vietnam',
        "url": '',
        "unverifiedCats": [],
    },
    'Philippines': {
        "verified": False,
        "source": 'Estimated · PSA Philippines',
        "url": '',
        "unverifiedCats": [],
    },
    'Indonesia': {
        "verified": False,
        "source": 'Estimated · BPS Indonesia',
        "url": '',
        "unverifiedCats": [],
    },
    'Cambodia': {
        "verified": False,
        "source": 'Estimated · NIS Cambodia',
        "url": '',
        "unverifiedCats": [],
    },
    'Brazil': {
        "verified": False,
        "source": 'Estimated · IBGE Brazil PNAD',
        "url": '',
        "unverifiedCats": [],
    },
    'Argentina': {
        "verified": False,
        "source": 'Estimated · INDEC Argentina',
        "url": '',
        "unverifiedCats": [],
    },
    'Colombia': {
        "verified": False,
        "source": 'Estimated · DANE Colombia',
        "url": '',
        "unverifiedCats": [],
    },
    'Chile': {
        "verified": False,
        "source": 'Estimated · INE Chile',
        "url": '',
        "unverifiedCats": [],
    },
    'Peru': {
        "verified": False,
        "source": 'Estimated · INEI Peru',
        "url": '',
        "unverifiedCats": [],
    },
    'Uruguay': {
        "verified": False,
        "source": 'Estimated · INE Uruguay',
        "url": '',
        "unverifiedCats": [],
    },
    'Mexico': {
        "verified": False,
        "source": 'Estimated · INEGI Mexico',
        "url": '',
        "unverifiedCats": [],
    },
    'Costa Rica': {
        "verified": False,
        "source": 'Estimated · INEC Costa Rica',
        "url": '',
        "unverifiedCats": [],
    },
    'Panama': {
        "verified": False,
        "source": 'Estimated · INEC Panama',
        "url": '',
        "unverifiedCats": [],
    },
    'South Africa': {
        "verified": False,
        "source": 'Estimated · Stats SA',
        "url": '',
        "unverifiedCats": [],
    },
    'Kenya': {
        "verified": False,
        "source": 'Estimated · KNBS Kenya',
        "url": '',
        "unverifiedCats": [],
    },
    'Nigeria': {
        "verified": False,
        "source": 'Estimated · NBS Nigeria',
        "url": '',
        "unverifiedCats": [],
    },
    'Egypt': {
        "verified": False,
        "source": 'Estimated · CAPMAS Egypt',
        "url": '',
        "unverifiedCats": [],
    },
    'Morocco': {
        "verified": False,
        "source": 'Estimated · HCP Morocco',
        "url": '',
        "unverifiedCats": [],
    },
}


def market_quality(job_title, country):
    """Return (multiplier, quality, source_info).

    quality is 'verified' | 'estimated' | 'coli' — same badges as
    /is-my-salary-good/.
    """
    cat = JOB_TO_MARKET_CAT.get(job_title)
    src = COUNTRY_SOURCES.get(country)
    mults = COUNTRY_MULTIPLIERS.get(country)
    cat_unverified = bool(src and cat and cat in (src.get('unverifiedCats') or []))
    if cat and mults and cat in mults:
        quality = 'verified' if (src and src.get('verified') and not cat_unverified) else 'estimated'
        return mults[cat], quality, src
    return None, 'coli', src


def badge_html(quality, src):
    if quality == 'verified':
        source = (src or {}).get('source') or 'national statistics'
        return f'<span class="src-badge src-verified">Verified</span> <span class="src-note">{source}</span>'
    if quality == 'estimated':
        source = (src or {}).get('source') or 'OECD wage ratios'
        return f'<span class="src-badge src-estimated">OECD / estimated</span> <span class="src-note">{source}</span>'
    return '<span class="src-badge src-coli">COLI estimate</span> <span class="src-note">No local salary survey for this role — scaled from the US baseline by city COLI. Not market pay.</span>'


def badge_plain(quality, src):
    if quality == 'verified':
        return 'Verified · ' + ((src or {}).get('source') or 'national statistics')
    if quality == 'estimated':
        return 'OECD / estimated · ' + ((src or {}).get('source') or 'OECD wage ratios')
    return 'COLI estimate only — not market pay'
