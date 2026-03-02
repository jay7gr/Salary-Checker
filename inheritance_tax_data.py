INHERITANCE_TAX_DATA = {
    # =====================================================================
    # North America
    # =====================================================================
    'United States': {'rate': 40, 'threshold': 13610000, 'currency': 'USD', 'note': 'Federal estate tax above $13.61M exemption (2024, indexed)'},
    'Canada': None,  # No inheritance/estate tax; deemed disposition at death triggers capital gains
    'Mexico': None,  # No inheritance tax; inheritances are exempt from income tax
    'Panama': None,  # No inheritance tax

    # =====================================================================
    # Central America / Caribbean
    # =====================================================================
    'Costa Rica': None,  # No inheritance tax
    'Guatemala': None,  # Abolished inheritance tax in 2008
    'Dominican Republic': {'rate': 3, 'threshold': 0, 'currency': 'DOP', 'note': '3% flat tax on net estate value'},
    'Puerto Rico (US territory)': {'rate': 10, 'threshold': 1000000, 'currency': 'USD', 'note': 'Separate estate tax from US federal; 10% flat rate above $1M exemption'},

    # =====================================================================
    # South America
    # =====================================================================
    'Brazil': {'rate': 8, 'threshold': 0, 'currency': 'BRL', 'note': 'ITCMD state tax; 2-8% varies by state; Sao Paulo 4%; max constitutional cap 8%'},
    'Argentina': {'rate': 6.5, 'threshold': 0, 'currency': 'ARS', 'note': 'Only Buenos Aires province levies inheritance tax; 2.2-6.5% progressive for direct heirs'},
    'Colombia': {'rate': 10, 'threshold': 0, 'currency': 'COP', 'note': 'Ganancia Ocasional; 10% flat on inherited amounts; first 1,000 UVT (~$12k USD) exempt'},
    'Peru': None,  # No inheritance tax
    'Chile': {'rate': 25, 'threshold': 0, 'currency': 'CLP', 'note': 'Impuesto a las herencias; 1-25% progressive; direct heirs get significant deductions'},
    'Uruguay': None,  # No inheritance tax
    'Ecuador': {'rate': 35, 'threshold': 71870, 'currency': 'USD', 'note': '0-35% progressive on inheritances above base threshold (~$72k)'},
    'Bolivia': {'rate': 1, 'threshold': 0, 'currency': 'BOB', 'note': '1% transaction tax on property transfers; no formal inheritance tax'},

    # =====================================================================
    # Europe Western
    # =====================================================================
    'United Kingdom': {'rate': 40, 'threshold': 325000, 'currency': 'GBP', 'note': 'IHT above nil-rate band; residence nil-rate adds up to 175k for family home'},
    'France': {'rate': 45, 'threshold': 100000, 'currency': 'EUR', 'note': 'Succession tax; 100k allowance per child from each parent; 5-45% progressive'},
    'Netherlands': {'rate': 20, 'threshold': 25187, 'currency': 'EUR', 'note': 'Erfbelasting; 10-20% for children; threshold indexed annually'},
    'Germany': {'rate': 30, 'threshold': 400000, 'currency': 'EUR', 'note': 'Erbschaftsteuer; 400k exemption per child; 7-30% progressive for Class I heirs'},
    'Ireland': {'rate': 33, 'threshold': 335000, 'currency': 'EUR', 'note': 'Capital Acquisitions Tax; Group A threshold for children (2024)'},
    'Belgium': {'rate': 30, 'threshold': 0, 'currency': 'EUR', 'note': 'Regional inheritance tax; 3-30% for direct heirs in Flanders; Brussels/Wallonia differ'},
    'Luxembourg': {'rate': 5, 'threshold': 0, 'currency': 'EUR', 'note': 'Low rates for direct line heirs; 0% for spouses; 2-5% for children on amounts above exemption'},
    'Switzerland': None,  # No federal inheritance tax; most cantons exempt direct heirs (spouse/children)
    'Austria': None,  # Abolished inheritance tax in 2008

    # =====================================================================
    # Europe Southern
    # =====================================================================
    'Spain': {'rate': 34, 'threshold': 0, 'currency': 'EUR', 'note': 'Impuesto sobre Sucesiones; heavily varies by region; many regions offer 95-99% reduction for direct heirs'},
    'Portugal': None,  # No inheritance tax; 10% stamp duty applies but direct heirs (spouse/children) are exempt
    'Italy': {'rate': 8, 'threshold': 1000000, 'currency': 'EUR', 'note': 'Imposta sulle successioni; 4% above 1M for children/spouse; 6-8% for others'},
    'Greece': {'rate': 10, 'threshold': 150000, 'currency': 'EUR', 'note': '1-10% for Category A heirs (children/spouse); 150k exemption'},
    'Croatia': {'rate': 4, 'threshold': 0, 'currency': 'EUR', 'note': 'Inheritance tax 4% on property; direct heirs (spouse/children) are exempt'},
    'Cyprus': None,  # No inheritance tax

    # =====================================================================
    # Europe Northern / Scandinavia
    # =====================================================================
    'Sweden': None,  # Abolished inheritance tax in 2005
    'Denmark': {'rate': 15, 'threshold': 321700, 'currency': 'DKK', 'note': 'Boafgift 15% for close family; additional 25% tax for non-close heirs'},
    'Finland': {'rate': 19, 'threshold': 20000, 'currency': 'EUR', 'note': 'Perintovero; Class I (close relatives) 7-19% progressive; 20k exemption'},
    'Norway': None,  # Abolished inheritance tax in 2014

    # =====================================================================
    # Europe Eastern / Central
    # =====================================================================
    'Czech Republic': None,  # Abolished inheritance tax in 2014; direct heirs were already exempt
    'Hungary': {'rate': 18, 'threshold': 0, 'currency': 'HUF', 'note': '18% general rate; direct heirs (children/spouse) fully exempt'},
    'Poland': {'rate': 7, 'threshold': 36120, 'currency': 'PLN', 'note': 'Group I 3-7% for close family; close family can claim full exemption if reported within 6 months'},
    'Romania': None,  # No inheritance tax; only notary fees apply
    'Estonia': None,  # No inheritance tax
    'Latvia': None,  # No inheritance tax; income tax may apply to some inherited assets
    'Turkey': {'rate': 10, 'threshold': 1371632, 'currency': 'TRY', 'note': 'Veraset ve Intikal Vergisi; 1-10% progressive; exemption indexed annually'},
    'Slovakia': None,  # Abolished inheritance tax in 2004
    'Slovenia': {'rate': 14, 'threshold': 0, 'currency': 'EUR', 'note': '5-14% for second inheritance class; first class (children/spouse) exempt'},
    'Lithuania': {'rate': 10, 'threshold': 150000, 'currency': 'EUR', 'note': '5% up to 150k, 10% above; close family members can be exempt'},
    'Bulgaria': {'rate': 6.6, 'threshold': 0, 'currency': 'BGN', 'note': '0.4-6.6% depending on relation; direct heirs (spouse/children) exempt'},
    'Serbia': {'rate': 2.5, 'threshold': 0, 'currency': 'RSD', 'note': '1.5-2.5% for second/third order heirs; first order (children/spouse) exempt'},
    'Bosnia and Herzegovina': {'rate': 5, 'threshold': 0, 'currency': 'BAM', 'note': 'Varies by entity; direct heirs generally exempt; 5% for non-direct heirs'},
    'Montenegro': {'rate': 3, 'threshold': 0, 'currency': 'EUR', 'note': '3% for second order heirs; first order (children/spouse) exempt'},
    'Albania': None,  # No inheritance tax

    # =====================================================================
    # East Asia
    # =====================================================================
    'Japan': {'rate': 55, 'threshold': 30000000, 'currency': 'JPY', 'note': 'Sozokuzei; 10-55% progressive; 30M JPY + 6M per legal heir base exemption'},
    'South Korea': {'rate': 50, 'threshold': 500000000, 'currency': 'KRW', 'note': '10-50% progressive; 500M KRW exemption; surcharge for large estates'},
    'Hong Kong': None,  # Abolished estate duty in 2006
    'Taiwan': {'rate': 20, 'threshold': 13330000, 'currency': 'TWD', 'note': '10-20% progressive; 13.33M TWD exemption plus various deductions'},
    'China': None,  # No inheritance tax (draft law discussed but not enacted)

    # =====================================================================
    # Southeast Asia
    # =====================================================================
    'Singapore': None,  # Abolished estate duty in 2008
    'Thailand': {'rate': 10, 'threshold': 100000000, 'currency': 'THB', 'note': '5% for 100M-300M THB; 10% above 300M; applies to direct heirs'},
    'Malaysia': None,  # No inheritance tax; abolished estate duty in 1991
    'Vietnam': {'rate': 10, 'threshold': 10000000, 'currency': 'VND', 'note': '10% personal income tax on inherited assets above 10M VND'},
    'Philippines': {'rate': 6, 'threshold': 5000000, 'currency': 'PHP', 'note': 'Flat 6% estate tax on net estate above 5M PHP standard deduction (TRAIN Law)'},
    'Indonesia': None,  # No inheritance tax; income tax may apply to gains on inherited assets
    'Cambodia': None,  # No inheritance tax
    'Laos': None,  # No inheritance tax
    'Myanmar': None,  # No inheritance tax; stamp duty may apply to property transfers

    # =====================================================================
    # South Asia
    # =====================================================================
    'India': None,  # Abolished estate duty in 1985
    'Nepal': None,  # No inheritance tax
    'Sri Lanka': None,  # No inheritance tax

    # =====================================================================
    # Oceania
    # =====================================================================
    'Australia': None,  # No inheritance/estate tax; abolished in 1979
    'New Zealand': None,  # No inheritance/estate tax; abolished in 1992

    # =====================================================================
    # Middle East
    # =====================================================================
    'UAE': None,  # No inheritance tax
    'Qatar': None,  # No inheritance tax
    'Saudi Arabia': None,  # No inheritance tax; Islamic inheritance law (Sharia) governs distribution
    'Israel': None,  # No inheritance tax
    'Jordan': None,  # No inheritance tax; property transfer fees apply
    'Lebanon': {'rate': 12, 'threshold': 0, 'currency': 'LBP', 'note': 'Succession duty 3-12% for direct heirs; varies by degree of kinship'},
    'Oman': None,  # No inheritance tax

    # =====================================================================
    # Caucasus
    # =====================================================================
    'Georgia': None,  # No inheritance tax
    'Armenia': None,  # No inheritance tax

    # =====================================================================
    # Africa
    # =====================================================================
    'South Africa': {'rate': 25, 'threshold': 3500000, 'currency': 'ZAR', 'note': 'Estate duty; 20% on first 30M ZAR above 3.5M exemption; 25% above 30M'},
    'Kenya': None,  # No inheritance/estate tax; stamp duty applies to property transfers
    'Nigeria': None,  # No federal inheritance tax
    'Egypt': None,  # No inheritance tax; 2.5% real estate registration tax on property transfers
    'Morocco': None,  # No inheritance tax; property registration fees apply
    'Ghana': None,  # No inheritance tax
    'Tunisia': {'rate': 25, 'threshold': 0, 'currency': 'TND', 'note': '2.5% for direct heirs on real property; up to 25% for unrelated heirs; close family rates very low'},
    'Tanzania': None,  # No inheritance tax
    'Uganda': None,  # No inheritance tax
    'Ethiopia': None,  # No inheritance tax
    'Senegal': {'rate': 10, 'threshold': 0, 'currency': 'XOF', 'note': 'Succession duty; 1-10% for direct heirs depending on relationship'},
}
