#!/usr/bin/env python3
"""Add 48 new retirement destination cities to retire/index.html"""

import re

# ═══════════════════════════════════════════════════════════════
# NEW CITY DATA — 48 cities
# ═══════════════════════════════════════════════════════════════

NEW_CITIES = {
    # Greece (5)
    'Chania': {'country': 'GR', 'currency': 'EUR', 'coli': 28, 'rent': 500, 'living': {'groceries':240,'utilities':200,'transport':25,'healthcare':30,'childcare':350}, 'safety': 68, 'healthcare': 55, 'climate': 84, 'infra': 48, 'english': 45, 'expat': 'medium', 'culture': 72, 'charm': 82, 'attract': 80, 'lifestyle': ['smaller_city','beach','mountain'], 'region': 'europe', 'coords': [35.5138, 24.0180]},
    'Thessaloniki': {'country': 'GR', 'currency': 'EUR', 'coli': 26, 'rent': 450, 'living': {'groceries':250,'utilities':210,'transport':30,'healthcare':32,'childcare':380}, 'safety': 52, 'healthcare': 62, 'climate': 72, 'infra': 58, 'english': 50, 'expat': 'medium', 'culture': 80, 'charm': 75, 'attract': 72, 'lifestyle': ['major_city','beach'], 'region': 'europe', 'coords': [40.6401, 22.9444]},
    'Rhodes': {'country': 'GR', 'currency': 'EUR', 'coli': 30, 'rent': 480, 'living': {'groceries':260,'utilities':210,'transport':20,'healthcare':28,'childcare':340}, 'safety': 70, 'healthcare': 50, 'climate': 84, 'infra': 45, 'english': 50, 'expat': 'medium', 'culture': 75, 'charm': 85, 'attract': 82, 'lifestyle': ['smaller_city','beach'], 'region': 'europe', 'coords': [36.4341, 28.2176]},
    'Corfu': {'country': 'GR', 'currency': 'EUR', 'coli': 30, 'rent': 480, 'living': {'groceries':255,'utilities':205,'transport':22,'healthcare':30,'childcare':340}, 'safety': 72, 'healthcare': 48, 'climate': 78, 'infra': 44, 'english': 55, 'expat': 'medium', 'culture': 72, 'charm': 88, 'attract': 85, 'lifestyle': ['smaller_city','beach','mountain'], 'region': 'europe', 'coords': [39.6243, 19.9217]},
    'Kalamata': {'country': 'GR', 'currency': 'EUR', 'coli': 25, 'rent': 400, 'living': {'groceries':230,'utilities':190,'transport':20,'healthcare':25,'childcare':320}, 'safety': 70, 'healthcare': 50, 'climate': 82, 'infra': 42, 'english': 40, 'expat': 'small', 'culture': 68, 'charm': 78, 'attract': 75, 'lifestyle': ['smaller_city','beach','mountain'], 'region': 'europe', 'coords': [37.0388, 22.1143]},

    # Italy (5)
    'Florence': {'country': 'IT', 'currency': 'EUR', 'coli': 52, 'rent': 1300, 'living': {'groceries':350,'utilities':260,'transport':40,'healthcare':45,'childcare':700}, 'safety': 58, 'healthcare': 72, 'climate': 70, 'infra': 65, 'english': 50, 'expat': 'large', 'culture': 95, 'charm': 95, 'attract': 95, 'lifestyle': ['major_city'], 'region': 'europe', 'coords': [43.7696, 11.2558]},
    'Lecce': {'country': 'IT', 'currency': 'EUR', 'coli': 30, 'rent': 550, 'living': {'groceries':260,'utilities':200,'transport':25,'healthcare':35,'childcare':450}, 'safety': 72, 'healthcare': 62, 'climate': 82, 'infra': 45, 'english': 35, 'expat': 'medium', 'culture': 78, 'charm': 88, 'attract': 85, 'lifestyle': ['smaller_city','beach'], 'region': 'europe', 'coords': [40.3516, 18.1750]},
    'Bologna': {'country': 'IT', 'currency': 'EUR', 'coli': 45, 'rent': 900, 'living': {'groceries':320,'utilities':240,'transport':38,'healthcare':42,'childcare':650}, 'safety': 55, 'healthcare': 72, 'climate': 58, 'infra': 68, 'english': 48, 'expat': 'medium', 'culture': 88, 'charm': 85, 'attract': 82, 'lifestyle': ['major_city'], 'region': 'europe', 'coords': [44.4949, 11.3426]},
    'Naples': {'country': 'IT', 'currency': 'EUR', 'coli': 35, 'rent': 650, 'living': {'groceries':280,'utilities':210,'transport':30,'healthcare':38,'childcare':500}, 'safety': 42, 'healthcare': 65, 'climate': 78, 'infra': 52, 'english': 38, 'expat': 'medium', 'culture': 88, 'charm': 82, 'attract': 80, 'lifestyle': ['major_city','beach'], 'region': 'europe', 'coords': [40.8518, 14.2681]},
    'Cagliari': {'country': 'IT', 'currency': 'EUR', 'coli': 35, 'rent': 580, 'living': {'groceries':270,'utilities':200,'transport':28,'healthcare':35,'childcare':480}, 'safety': 68, 'healthcare': 62, 'climate': 82, 'infra': 50, 'english': 35, 'expat': 'small', 'culture': 72, 'charm': 78, 'attract': 78, 'lifestyle': ['major_city','beach'], 'region': 'europe', 'coords': [39.2238, 9.1217]},

    # Turkey (4)
    'Antalya': {'country': 'TR', 'currency': 'TRY', 'coli': 20, 'rent': 400, 'living': {'groceries':180,'utilities':120,'transport':18,'healthcare':20,'childcare':250}, 'safety': 60, 'healthcare': 65, 'climate': 85, 'infra': 62, 'english': 40, 'expat': 'large', 'culture': 68, 'charm': 75, 'attract': 78, 'lifestyle': ['major_city','beach'], 'region': 'europe', 'coords': [36.8969, 30.7133]},
    'Bodrum': {'country': 'TR', 'currency': 'TRY', 'coli': 25, 'rent': 480, 'living': {'groceries':200,'utilities':130,'transport':15,'healthcare':22,'childcare':280}, 'safety': 65, 'healthcare': 58, 'climate': 82, 'infra': 52, 'english': 45, 'expat': 'medium', 'culture': 72, 'charm': 82, 'attract': 82, 'lifestyle': ['smaller_city','beach'], 'region': 'europe', 'coords': [37.0344, 27.4305]},
    'Fethiye': {'country': 'TR', 'currency': 'TRY', 'coli': 18, 'rent': 350, 'living': {'groceries':160,'utilities':110,'transport':12,'healthcare':18,'childcare':220}, 'safety': 68, 'healthcare': 52, 'climate': 82, 'infra': 45, 'english': 50, 'expat': 'medium', 'culture': 65, 'charm': 85, 'attract': 85, 'lifestyle': ['smaller_city','beach','mountain'], 'region': 'europe', 'coords': [36.6515, 29.1164]},
    'Alanya': {'country': 'TR', 'currency': 'TRY', 'coli': 18, 'rent': 320, 'living': {'groceries':155,'utilities':105,'transport':12,'healthcare':18,'childcare':210}, 'safety': 62, 'healthcare': 55, 'climate': 84, 'infra': 50, 'english': 35, 'expat': 'large', 'culture': 60, 'charm': 72, 'attract': 72, 'lifestyle': ['smaller_city','beach'], 'region': 'europe', 'coords': [36.5437, 31.9994]},

    # Spain (3)
    'Alicante': {'country': 'ES', 'currency': 'EUR', 'coli': 35, 'rent': 700, 'living': {'groceries':280,'utilities':200,'transport':30,'healthcare':35,'childcare':500}, 'safety': 68, 'healthcare': 76, 'climate': 88, 'infra': 65, 'english': 55, 'expat': 'large', 'culture': 72, 'charm': 75, 'attract': 75, 'lifestyle': ['major_city','beach'], 'region': 'europe', 'coords': [38.3452, -0.4810]},
    'Granada': {'country': 'ES', 'currency': 'EUR', 'coli': 30, 'rent': 550, 'living': {'groceries':260,'utilities':190,'transport':25,'healthcare':32,'childcare':450}, 'safety': 68, 'healthcare': 74, 'climate': 75, 'infra': 58, 'english': 45, 'expat': 'medium', 'culture': 88, 'charm': 90, 'attract': 88, 'lifestyle': ['major_city','mountain'], 'region': 'europe', 'coords': [37.1773, -3.5986]},
    'Seville': {'country': 'ES', 'currency': 'EUR', 'coli': 33, 'rent': 650, 'living': {'groceries':270,'utilities':200,'transport':28,'healthcare':34,'childcare':480}, 'safety': 60, 'healthcare': 76, 'climate': 72, 'infra': 62, 'english': 45, 'expat': 'medium', 'culture': 90, 'charm': 92, 'attract': 90, 'lifestyle': ['major_city'], 'region': 'europe', 'coords': [37.3891, -5.9845]},

    # France (3)
    'Bordeaux': {'country': 'FR', 'currency': 'EUR', 'coli': 45, 'rent': 800, 'living': {'groceries':320,'utilities':240,'transport':38,'healthcare':40,'childcare':650}, 'safety': 52, 'healthcare': 80, 'climate': 65, 'infra': 72, 'english': 45, 'expat': 'medium', 'culture': 85, 'charm': 88, 'attract': 85, 'lifestyle': ['major_city'], 'region': 'europe', 'coords': [44.8378, -0.5792]},
    'Montpellier': {'country': 'FR', 'currency': 'EUR', 'coli': 40, 'rent': 700, 'living': {'groceries':300,'utilities':220,'transport':32,'healthcare':38,'childcare':600}, 'safety': 48, 'healthcare': 78, 'climate': 82, 'infra': 65, 'english': 42, 'expat': 'medium', 'culture': 78, 'charm': 80, 'attract': 78, 'lifestyle': ['major_city','beach'], 'region': 'europe', 'coords': [43.6108, 3.8767]},
    'Lyon': {'country': 'FR', 'currency': 'EUR', 'coli': 42, 'rent': 750, 'living': {'groceries':310,'utilities':230,'transport':35,'healthcare':40,'childcare':620}, 'safety': 48, 'healthcare': 82, 'climate': 60, 'infra': 72, 'english': 42, 'expat': 'medium', 'culture': 88, 'charm': 85, 'attract': 82, 'lifestyle': ['major_city'], 'region': 'europe', 'coords': [45.7640, 4.8357]},

    # Croatia (3)
    'Dubrovnik': {'country': 'HR', 'currency': 'EUR', 'coli': 40, 'rent': 700, 'living': {'groceries':300,'utilities':220,'transport':25,'healthcare':30,'childcare':450}, 'safety': 72, 'healthcare': 58, 'climate': 78, 'infra': 52, 'english': 58, 'expat': 'small', 'culture': 80, 'charm': 95, 'attract': 95, 'lifestyle': ['smaller_city','beach'], 'region': 'europe', 'coords': [42.6507, 18.0944]},
    'Zadar': {'country': 'HR', 'currency': 'EUR', 'coli': 30, 'rent': 500, 'living': {'groceries':260,'utilities':190,'transport':22,'healthcare':28,'childcare':380}, 'safety': 75, 'healthcare': 55, 'climate': 78, 'infra': 48, 'english': 55, 'expat': 'small', 'culture': 72, 'charm': 82, 'attract': 80, 'lifestyle': ['smaller_city','beach'], 'region': 'europe', 'coords': [44.1194, 15.2314]},
    'Rovinj': {'country': 'HR', 'currency': 'EUR', 'coli': 38, 'rent': 620, 'living': {'groceries':290,'utilities':210,'transport':20,'healthcare':28,'childcare':420}, 'safety': 78, 'healthcare': 55, 'climate': 72, 'infra': 48, 'english': 52, 'expat': 'small', 'culture': 75, 'charm': 92, 'attract': 90, 'lifestyle': ['smaller_city','beach'], 'region': 'europe', 'coords': [45.0812, 13.6387]},

    # Mexico (3)
    'San Miguel de Allende': {'country': 'MX', 'currency': 'MXN', 'coli': 28, 'rent': 650, 'living': {'groceries':200,'utilities':120,'transport':15,'healthcare':25,'childcare':300}, 'safety': 55, 'healthcare': 58, 'climate': 78, 'infra': 48, 'english': 50, 'expat': 'large', 'culture': 85, 'charm': 95, 'attract': 92, 'lifestyle': ['smaller_city','mountain'], 'region': 'north_america', 'coords': [20.9144, -100.7452]},
    'Ajijic': {'country': 'MX', 'currency': 'MXN', 'coli': 22, 'rent': 450, 'living': {'groceries':170,'utilities':100,'transport':10,'healthcare':20,'childcare':250}, 'safety': 55, 'healthcare': 55, 'climate': 82, 'infra': 40, 'english': 55, 'expat': 'large', 'culture': 70, 'charm': 82, 'attract': 78, 'lifestyle': ['smaller_city','mountain'], 'region': 'north_america', 'coords': [20.2955, -103.2629]},
    'Guanajuato': {'country': 'MX', 'currency': 'MXN', 'coli': 22, 'rent': 380, 'living': {'groceries':165,'utilities':95,'transport':10,'healthcare':18,'childcare':240}, 'safety': 48, 'healthcare': 52, 'climate': 76, 'infra': 42, 'english': 35, 'expat': 'medium', 'culture': 82, 'charm': 90, 'attract': 88, 'lifestyle': ['smaller_city','mountain'], 'region': 'north_america', 'coords': [21.0190, -101.2574]},

    # Panama (2)
    'Boquete': {'country': 'PA', 'currency': 'USD', 'coli': 30, 'rent': 550, 'living': {'groceries':220,'utilities':120,'transport':10,'healthcare':25,'childcare':300}, 'safety': 55, 'healthcare': 52, 'climate': 76, 'infra': 38, 'english': 60, 'expat': 'large', 'culture': 55, 'charm': 78, 'attract': 75, 'lifestyle': ['smaller_city','mountain'], 'region': 'central_america', 'coords': [8.7833, -82.4333]},
    'Coronado': {'country': 'PA', 'currency': 'USD', 'coli': 32, 'rent': 580, 'living': {'groceries':230,'utilities':130,'transport':12,'healthcare':25,'childcare':320}, 'safety': 52, 'healthcare': 55, 'climate': 75, 'infra': 42, 'english': 55, 'expat': 'medium', 'culture': 48, 'charm': 65, 'attract': 62, 'lifestyle': ['smaller_city','beach'], 'region': 'central_america', 'coords': [8.5878, -79.9286]},

    # Costa Rica (2)
    'Tamarindo': {'country': 'CR', 'currency': 'CRC', 'coli': 35, 'rent': 700, 'living': {'groceries':280,'utilities':140,'transport':15,'healthcare':28,'childcare':350}, 'safety': 45, 'healthcare': 52, 'climate': 78, 'infra': 40, 'english': 55, 'expat': 'medium', 'culture': 55, 'charm': 75, 'attract': 72, 'lifestyle': ['smaller_city','beach'], 'region': 'central_america', 'coords': [10.2994, -85.8371]},
    'Nosara': {'country': 'CR', 'currency': 'CRC', 'coli': 38, 'rent': 800, 'living': {'groceries':300,'utilities':150,'transport':12,'healthcare':30,'childcare':380}, 'safety': 48, 'healthcare': 42, 'climate': 78, 'infra': 35, 'english': 55, 'expat': 'medium', 'culture': 52, 'charm': 78, 'attract': 75, 'lifestyle': ['smaller_city','beach'], 'region': 'central_america', 'coords': [9.9765, -85.6530]},

    # Colombia (2)
    'Cartagena': {'country': 'CO', 'currency': 'COP', 'coli': 25, 'rent': 520, 'living': {'groceries':200,'utilities':120,'transport':15,'healthcare':22,'childcare':280}, 'safety': 40, 'healthcare': 60, 'climate': 72, 'infra': 55, 'english': 40, 'expat': 'medium', 'culture': 82, 'charm': 90, 'attract': 88, 'lifestyle': ['major_city','beach'], 'region': 'south_america', 'coords': [10.3910, -75.5364]},
    'Santa Marta': {'country': 'CO', 'currency': 'COP', 'coli': 20, 'rent': 380, 'living': {'groceries':170,'utilities':100,'transport':10,'healthcare':18,'childcare':220}, 'safety': 42, 'healthcare': 50, 'climate': 78, 'infra': 42, 'english': 35, 'expat': 'small', 'culture': 65, 'charm': 75, 'attract': 72, 'lifestyle': ['smaller_city','beach','mountain'], 'region': 'south_america', 'coords': [11.2408, -74.1990]},

    # Brazil (2)
    'Florianopolis': {'country': 'BR', 'currency': 'BRL', 'coli': 28, 'rent': 450, 'living': {'groceries':220,'utilities':130,'transport':20,'healthcare':25,'childcare':300}, 'safety': 40, 'healthcare': 62, 'climate': 75, 'infra': 55, 'english': 30, 'expat': 'small', 'culture': 65, 'charm': 78, 'attract': 78, 'lifestyle': ['major_city','beach'], 'region': 'south_america', 'coords': [-27.5954, -48.5480]},
    'Salvador': {'country': 'BR', 'currency': 'BRL', 'coli': 22, 'rent': 340, 'living': {'groceries':190,'utilities':110,'transport':15,'healthcare':20,'childcare':250}, 'safety': 28, 'healthcare': 55, 'climate': 82, 'infra': 48, 'english': 25, 'expat': 'small', 'culture': 82, 'charm': 80, 'attract': 78, 'lifestyle': ['major_city','beach'], 'region': 'south_america', 'coords': [-12.9714, -38.5124]},

    # Malaysia (2)
    'Penang': {'country': 'MY', 'currency': 'MYR', 'coli': 26, 'rent': 420, 'living': {'groceries':180,'utilities':100,'transport':15,'healthcare':20,'childcare':250}, 'safety': 55, 'healthcare': 68, 'climate': 75, 'infra': 62, 'english': 70, 'expat': 'large', 'culture': 78, 'charm': 80, 'attract': 80, 'lifestyle': ['major_city','beach'], 'region': 'southeast_asia', 'coords': [5.4164, 100.3327]},
    'Langkawi': {'country': 'MY', 'currency': 'MYR', 'coli': 24, 'rent': 380, 'living': {'groceries':170,'utilities':90,'transport':10,'healthcare':18,'childcare':220}, 'safety': 60, 'healthcare': 52, 'climate': 78, 'infra': 45, 'english': 65, 'expat': 'medium', 'culture': 60, 'charm': 78, 'attract': 78, 'lifestyle': ['smaller_city','beach'], 'region': 'southeast_asia', 'coords': [6.3500, 99.8000]},

    # Indonesia (2)
    'Lombok': {'country': 'ID', 'currency': 'IDR', 'coli': 20, 'rent': 300, 'living': {'groceries':140,'utilities':60,'transport':8,'healthcare':15,'childcare':120}, 'safety': 55, 'healthcare': 35, 'climate': 80, 'infra': 35, 'english': 35, 'expat': 'small', 'culture': 62, 'charm': 82, 'attract': 82, 'lifestyle': ['smaller_city','beach','mountain'], 'region': 'southeast_asia', 'coords': [-8.5650, 116.3510]},
    'Yogyakarta': {'country': 'ID', 'currency': 'IDR', 'coli': 16, 'rent': 250, 'living': {'groceries':120,'utilities':50,'transport':6,'healthcare':12,'childcare':100}, 'safety': 60, 'healthcare': 45, 'climate': 75, 'infra': 45, 'english': 35, 'expat': 'small', 'culture': 85, 'charm': 82, 'attract': 80, 'lifestyle': ['major_city'], 'region': 'southeast_asia', 'coords': [-7.7956, 110.3695]},

    # Philippines (1)
    'Cebu': {'country': 'PH', 'currency': 'PHP', 'coli': 22, 'rent': 350, 'living': {'groceries':170,'utilities':90,'transport':10,'healthcare':18,'childcare':200}, 'safety': 45, 'healthcare': 52, 'climate': 75, 'infra': 50, 'english': 80, 'expat': 'large', 'culture': 65, 'charm': 68, 'attract': 68, 'lifestyle': ['major_city','beach'], 'region': 'southeast_asia', 'coords': [10.3157, 123.8854]},

    # Thailand (1)
    'Krabi': {'country': 'TH', 'currency': 'THB', 'coli': 25, 'rent': 350, 'living': {'groceries':180,'utilities':100,'transport':10,'healthcare':18,'childcare':220}, 'safety': 65, 'healthcare': 48, 'climate': 78, 'infra': 42, 'english': 38, 'expat': 'medium', 'culture': 60, 'charm': 82, 'attract': 82, 'lifestyle': ['smaller_city','beach'], 'region': 'southeast_asia', 'coords': [8.0863, 98.9063]},

    # Morocco (2)
    'Fez': {'country': 'MA', 'currency': 'MAD', 'coli': 18, 'rent': 300, 'living': {'groceries':150,'utilities':90,'transport':10,'healthcare':15,'childcare':180}, 'safety': 55, 'healthcare': 45, 'climate': 72, 'infra': 42, 'english': 30, 'expat': 'small', 'culture': 90, 'charm': 92, 'attract': 88, 'lifestyle': ['major_city'], 'region': 'africa', 'coords': [34.0181, -5.0078]},
    'Agadir': {'country': 'MA', 'currency': 'MAD', 'coli': 20, 'rent': 340, 'living': {'groceries':160,'utilities':95,'transport':10,'healthcare':16,'childcare':200}, 'safety': 58, 'healthcare': 48, 'climate': 82, 'infra': 45, 'english': 30, 'expat': 'medium', 'culture': 62, 'charm': 68, 'attract': 68, 'lifestyle': ['major_city','beach'], 'region': 'africa', 'coords': [30.4278, -9.5981]},

    # South Africa (1)
    'Stellenbosch': {'country': 'ZA', 'currency': 'ZAR', 'coli': 25, 'rent': 480, 'living': {'groceries':200,'utilities':110,'transport':15,'healthcare':25,'childcare':300}, 'safety': 38, 'healthcare': 62, 'climate': 78, 'infra': 55, 'english': 90, 'expat': 'medium', 'culture': 72, 'charm': 85, 'attract': 82, 'lifestyle': ['smaller_city','mountain'], 'region': 'africa', 'coords': [-33.9321, 18.8602]},

    # Australia (2)
    'Brisbane': {'country': 'AU', 'currency': 'AUD', 'coli': 60, 'rent': 1300, 'living': {'groceries':380,'utilities':280,'transport':55,'healthcare':60,'childcare':1200}, 'safety': 58, 'healthcare': 78, 'climate': 78, 'infra': 78, 'english': 98, 'expat': 'large', 'culture': 72, 'charm': 68, 'attract': 68, 'lifestyle': ['major_city'], 'region': 'oceania', 'coords': [-27.4698, 153.0251]},
    'Gold Coast': {'country': 'AU', 'currency': 'AUD', 'coli': 55, 'rent': 1100, 'living': {'groceries':360,'utilities':260,'transport':45,'healthcare':55,'childcare':1100}, 'safety': 55, 'healthcare': 72, 'climate': 82, 'infra': 68, 'english': 98, 'expat': 'large', 'culture': 55, 'charm': 65, 'attract': 65, 'lifestyle': ['major_city','beach'], 'region': 'oceania', 'coords': [-28.0167, 153.4000]},

    # New Zealand (3)
    'Wellington': {'country': 'NZ', 'currency': 'NZD', 'coli': 58, 'rent': 1100, 'living': {'groceries':370,'utilities':260,'transport':50,'healthcare':55,'childcare':1100}, 'safety': 55, 'healthcare': 75, 'climate': 55, 'infra': 72, 'english': 98, 'expat': 'medium', 'culture': 82, 'charm': 78, 'attract': 75, 'lifestyle': ['major_city'], 'region': 'oceania', 'coords': [-41.2865, 174.7762]},
    'Tauranga': {'country': 'NZ', 'currency': 'NZD', 'coli': 52, 'rent': 1000, 'living': {'groceries':350,'utilities':240,'transport':35,'healthcare':50,'childcare':1000}, 'safety': 58, 'healthcare': 68, 'climate': 68, 'infra': 58, 'english': 98, 'expat': 'medium', 'culture': 55, 'charm': 72, 'attract': 70, 'lifestyle': ['smaller_city','beach'], 'region': 'oceania', 'coords': [-37.6878, 176.1651]},
    'Queenstown': {'country': 'NZ', 'currency': 'NZD', 'coli': 62, 'rent': 1200, 'living': {'groceries':380,'utilities':270,'transport':30,'healthcare':52,'childcare':1050}, 'safety': 68, 'healthcare': 62, 'climate': 55, 'infra': 52, 'english': 98, 'expat': 'medium', 'culture': 60, 'charm': 92, 'attract': 92, 'lifestyle': ['smaller_city','mountain'], 'region': 'oceania', 'coords': [-45.0312, 168.6626]},
}


def inject_into_object(content, marker_pattern, new_entries_str):
    """Insert new entries after a marker line in a JS object."""
    match = re.search(marker_pattern, content)
    if not match:
        print(f"WARNING: Could not find pattern: {marker_pattern}")
        return content
    pos = match.end()
    # Find end of the line
    newline = content.index('\n', pos)
    return content[:newline] + '\n' + new_entries_str + content[newline:]


def main():
    filepath = 'retire/index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # 1. coliData — insert after Athens line
    entries = ', '.join(f"'{name}': {d['coli']}" for name, d in NEW_CITIES.items())
    # Add after the last entry before closing brace
    content = content.replace(
        "'Athens': 30.6,",
        f"'Athens': 30.6,\n            {entries},",
        1
    )
    print("✓ coliData")

    # 2. cityToCurrency — insert after Athens
    entries = ', '.join(f"'{name}': '{d['currency']}'" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 'EUR', 'Split': 'EUR',",
        f"'Athens': 'EUR', 'Split': 'EUR',\n            {entries},",
        1
    )
    print("✓ cityToCurrency")

    # 3. cityToCountry — insert after Athens
    entries = ', '.join(f"'{name}': '{d['country']}'" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 'GR', 'Split': 'HR',",
        f"'Athens': 'GR', 'Split': 'HR',\n            {entries},",
        1
    )
    print("✓ cityToCountry")

    # 4. cityRent1BR — insert after Athens
    entries = ', '.join(f"'{name}': {d['rent']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 700, 'Split': 650,",
        f"'Athens': 700, 'Split': 650,\n            {entries},",
        1
    )
    print("✓ cityRent1BR")

    # 5. cityLivingCosts — insert after Athens
    living_entries = []
    for name, d in NEW_CITIES.items():
        lv = d['living']
        living_entries.append(f"'{name}':{{groceries:{lv['groceries']},utilities:{lv['utilities']},transport:{lv['transport']},healthcare:{lv['healthcare']}}}")
    entries = ',\n            '.join(living_entries)
    content = content.replace(
        "'Athens': {groceries:270,utilities:230,transport:35,healthcare:35,childcare:400},",
        f"'Athens': {{groceries:270,utilities:230,transport:35,healthcare:35,childcare:400}},\n            {entries},",
        1
    )
    print("✓ cityLivingCosts")

    # 6-12. QOL indices — each uses a similar pattern near Athens
    # retireSafetyIndex
    entries = ', '.join(f"'{name}': {d['safety']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 45,",
        f"'Athens': 45,\n  {entries},",
        1
    )
    print("✓ retireSafetyIndex")

    # retireHealthcareIndex
    entries = ', '.join(f"'{name}': {d['healthcare']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 59,",
        f"'Athens': 59,\n  {entries},",
        1
    )
    print("✓ retireHealthcareIndex")

    # retireClimateScore
    entries = ', '.join(f"'{name}': {d['climate']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 82,",
        f"'Athens': 82,\n  {entries},",
        1
    )
    print("✓ retireClimateScore")

    # retireInfrastructureScore
    entries = ', '.join(f"'{name}': {d['infra']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 60,",
        f"'Athens': 60,\n  {entries},",
        1
    )
    print("✓ retireInfrastructureScore")

    # retireEnglishScore
    entries = ', '.join(f"'{name}': {d['english']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 55,",
        f"'Athens': 55,\n  {entries},",
        1
    )
    print("✓ retireEnglishScore")

    # retireExpatCommunity
    entries = ', '.join(f"'{name}': '{d['expat']}'" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 'medium',",
        f"'Athens': 'medium',\n  {entries},",
        1
    )
    print("✓ retireExpatCommunity")

    # retireCultureScore
    entries = ', '.join(f"'{name}': {d['culture']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 78,",
        f"'Athens': 78,\n  {entries},",
        1
    )
    print("✓ retireCultureScore")

    # 13. retireCityCharmScore — Athens entry
    entries = ', '.join(f"'{name}': {d['charm']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 72, 'Budapest': 90,",
        f"'Athens': 72, 'Budapest': 90,\n    {entries},",
        1
    )
    print("✓ retireCityCharmScore")

    # 14. cityLifestyleMap — add after existing entries
    lifestyle_entries = []
    for name, d in NEW_CITIES.items():
        if d.get('lifestyle'):
            tags = ', '.join(f"'{t}'" for t in d['lifestyle'])
            lifestyle_entries.append(f"'{name}': [{tags}]")
    entries = ',\n    '.join(lifestyle_entries)
    # Find a known entry near the end of cityLifestyleMap
    content = content.replace(
        "'Taormina': ['smaller_city', 'beach', 'mountain'],",
        f"'Taormina': ['smaller_city', 'beach', 'mountain'],\n    {entries},",
        1
    )
    print("✓ cityLifestyleMap")

    # 15. cityAttractivenessScore
    entries = ', '.join(f"'{name}': {d['attract']}" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 72, 'Budapest': 90,",
        f"'Athens': 72, 'Budapest': 90,\n    {entries},",
        1
    )
    print("✓ cityAttractivenessScore")

    # 16. retireCityToCountry — full country names
    country_names = {
        'GR': 'Greece', 'IT': 'Italy', 'TR': 'Turkey', 'ES': 'Spain',
        'FR': 'France', 'HR': 'Croatia', 'MX': 'Mexico', 'PA': 'Panama',
        'CR': 'Costa Rica', 'CO': 'Colombia', 'BR': 'Brazil', 'MY': 'Malaysia',
        'ID': 'Indonesia', 'PH': 'Philippines', 'TH': 'Thailand', 'MA': 'Morocco',
        'ZA': 'South Africa', 'AU': 'Australia', 'NZ': 'New Zealand'
    }
    entries = ', '.join(f"'{name}': '{country_names[d['country']]}'" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': 'Greece',",
        f"'Athens': 'Greece',\n  {entries},",
        1
    )
    print("✓ retireCityToCountry")

    # 17. Coordinates
    entries = ', '.join(f"'{name}': [{d['coords'][0]}, {d['coords'][1]}]" for name, d in NEW_CITIES.items())
    content = content.replace(
        "'Athens': [37.9838, 23.7275], 'Split': [43.5081, 16.4402],",
        f"'Athens': [37.9838, 23.7275], 'Split': [43.5081, 16.4402],\n  {entries},",
        1
    )
    print("✓ coordinates")

    # 18. regionSets — add cities to correct region arrays
    region_cities = {}
    for name, d in NEW_CITIES.items():
        region = d['region']
        if region not in region_cities:
            region_cities[region] = []
        region_cities[region].append(name)

    for region, cities in region_cities.items():
        # Find the region array and add cities
        pattern = f"'{region}':\\s*\\[([^\\]]*?)\\]"
        match = re.search(pattern, content)
        if match:
            existing = match.group(1).rstrip().rstrip(',')
            new_cities_str = ', '.join(f"'{c}'" for c in cities)
            replacement = f"'{region}': [{existing}, {new_cities_str}]"
            content = content[:match.start()] + replacement + content[match.end():]
            print(f"  ✓ regionSets[{region}]")
        else:
            print(f"  WARNING: Could not find regionSets[{region}]")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    new_len = len(content)
    print(f"\nDone! Added {len(NEW_CITIES)} cities.")
    print(f"File size: {original_len:,} → {new_len:,} bytes (+{new_len - original_len:,})")


if __name__ == '__main__':
    main()
