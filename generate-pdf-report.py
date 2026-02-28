#!/usr/bin/env python3
"""
Generate a professional PDF report: "2026 Global Salary & Cost of Living Report"
Uses data from generate-pages.py and the reportlab library.
Output: 2026-global-salary-report.pdf
"""

import os
import sys

# ── Check for reportlab ──────────────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, cm, inch
    from reportlab.lib.colors import HexColor, white, black, Color
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, KeepTogether, NextPageTemplate, PageTemplate, Frame,
        BaseDocTemplate
    )
    from reportlab.platypus.tableofcontents import TableOfContents
    from reportlab.graphics.shapes import Drawing, Rect, String, Line
    from reportlab.graphics.charts.barcharts import VerticalBarChart
except ImportError:
    print("reportlab is not installed. Install it with:")
    print("  pip3 install reportlab")
    sys.exit(1)

# ── Load data from generate-pages.py ─────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))

_source = open(os.path.join(ROOT, 'generate-pages.py'), encoding='utf-8').read()
_data_portion = _source.split("if __name__ == '__main__':")[0]

_namespace = {}
exec(_data_portion, _namespace)

# Pull data into module scope
coliData           = _namespace['coliData']
exchangeRates      = _namespace['exchangeRates']
cityToCurrency     = _namespace['cityToCurrency']
cityCountry        = _namespace['cityCountry']
cityRent1BR        = _namespace['cityRent1BR']
cityRegions        = _namespace['cityRegions']
taxBrackets        = _namespace['taxBrackets']
countryDeductions  = _namespace['countryDeductions']
salaryRanges       = _namespace['salaryRanges']
cityNeighborhoods  = _namespace['cityNeighborhoods']
calculate_tax      = _namespace['calculate_tax']
calculate_all_deductions = _namespace['calculate_all_deductions']

TOTAL_CITIES = len(coliData)
TOTAL_JOBS = len(salaryRanges)
TOTAL_NEIGHBORHOODS = sum(len(v) for v in cityNeighborhoods.values())

# ── Color scheme ──────────────────────────────────────────────────────────────
DARK_BLUE    = HexColor('#1a1a2e')
MID_BLUE     = HexColor('#16213e')
ACCENT_GREEN = HexColor('#9fe870')
LIGHT_GREEN  = HexColor('#e8f5e0')
LIGHT_GRAY   = HexColor('#f4f4f6')
MID_GRAY     = HexColor('#e0e0e4')
TEXT_DARK     = HexColor('#1a1a2e')
TEXT_MID      = HexColor('#444466')
WHITE         = white
ROW_EVEN      = HexColor('#f8f8fa')
ROW_ODD       = WHITE
HEADER_BG     = DARK_BLUE
HEADER_FG     = WHITE
ACCENT_BG     = HexColor('#eef7e6')
SUBTLE_LINE   = HexColor('#ccccdd')

PAGE_W, PAGE_H = A4  # 595.27, 841.89 points
MARGIN = 54  # ~0.75 inch

# ── Paragraph styles ─────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    'ReportTitle', parent=styles['Title'],
    fontName='Helvetica-Bold', fontSize=28, leading=34,
    textColor=WHITE, alignment=TA_CENTER, spaceAfter=6,
)
style_subtitle = ParagraphStyle(
    'ReportSubtitle', parent=styles['Normal'],
    fontName='Helvetica', fontSize=14, leading=18,
    textColor=HexColor('#c0e0b0'), alignment=TA_CENTER, spaceAfter=4,
)
style_cover_byline = ParagraphStyle(
    'CoverByline', parent=styles['Normal'],
    fontName='Helvetica', fontSize=11, leading=14,
    textColor=HexColor('#aaaacc'), alignment=TA_CENTER, spaceAfter=0,
)
style_section = ParagraphStyle(
    'SectionHeader', parent=styles['Heading1'],
    fontName='Helvetica-Bold', fontSize=20, leading=26,
    textColor=DARK_BLUE, spaceBefore=10, spaceAfter=14,
    borderWidth=0, borderPadding=0,
)
style_subsection = ParagraphStyle(
    'SubsectionHeader', parent=styles['Heading2'],
    fontName='Helvetica-Bold', fontSize=14, leading=18,
    textColor=MID_BLUE, spaceBefore=10, spaceAfter=6,
)
style_body = ParagraphStyle(
    'BodyText2', parent=styles['Normal'],
    fontName='Helvetica', fontSize=9.5, leading=13,
    textColor=TEXT_DARK, spaceAfter=6, alignment=TA_JUSTIFY,
)
style_body_small = ParagraphStyle(
    'BodySmall', parent=style_body,
    fontSize=8, leading=10.5, spaceAfter=3,
)
style_stat_label = ParagraphStyle(
    'StatLabel', parent=styles['Normal'],
    fontName='Helvetica', fontSize=8, leading=10,
    textColor=TEXT_MID, alignment=TA_CENTER,
)
style_stat_value = ParagraphStyle(
    'StatValue', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=14, leading=18,
    textColor=DARK_BLUE, alignment=TA_CENTER,
)
style_toc_entry = ParagraphStyle(
    'TOCEntry', parent=styles['Normal'],
    fontName='Helvetica', fontSize=11, leading=22,
    textColor=TEXT_DARK, leftIndent=0,
)
style_table_header = ParagraphStyle(
    'TableHeader', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
    textColor=WHITE, alignment=TA_CENTER,
)
style_table_cell = ParagraphStyle(
    'TableCell', parent=styles['Normal'],
    fontName='Helvetica', fontSize=7.5, leading=9.5,
    textColor=TEXT_DARK, alignment=TA_CENTER,
)
style_table_cell_left = ParagraphStyle(
    'TableCellLeft', parent=style_table_cell,
    alignment=TA_LEFT,
)
style_region_title = ParagraphStyle(
    'RegionTitle', parent=styles['Heading2'],
    fontName='Helvetica-Bold', fontSize=15, leading=20,
    textColor=DARK_BLUE, spaceBefore=14, spaceAfter=6,
)
style_footer = ParagraphStyle(
    'Footer', parent=styles['Normal'],
    fontName='Helvetica', fontSize=7, leading=9,
    textColor=TEXT_MID, alignment=TA_CENTER,
)

# ── Utility helpers ──────────────────────────────────────────────────────────

def usd(amount):
    """Format as USD string."""
    if amount >= 1000:
        return f'${amount:,.0f}'
    return f'${amount:.0f}'


def pct(value):
    """Format as percentage string."""
    return f'{value:.1f}%'


def compute_comfortable_salary(city):
    """Estimate a 'comfortable' annual salary in USD for a city.
    Formula: (1BR rent * 12 / 0.30) scaled by COLI relative to NY.
    The idea: rent should be ~30% of gross income for comfort."""
    rent = cityRent1BR.get(city, 0)
    if rent == 0:
        return 0
    # Gross needed so rent is 30% of gross
    base = rent * 12 / 0.30
    return round(base)


def get_top_marginal_rate(country):
    """Return the top marginal tax rate for a country."""
    brackets = taxBrackets.get(country, [])
    if not brackets:
        return 0.0
    return brackets[-1][1]


def get_ss_rate(country):
    """Return the employee social security rate for a country."""
    ded = countryDeductions.get(country, {})
    ss = ded.get('social_security', {})
    return ss.get('local', 0.0)


def effective_rate_at_income(income_usd, country):
    """Calculate effective total deduction rate at a given USD income for a country.
    Converts income to local currency first."""
    # Find a city in that country to get the currency
    city_for_country = None
    for c, co in cityCountry.items():
        if co == country:
            city_for_country = c
            break
    if not city_for_country:
        return 0.0
    currency = cityToCurrency.get(city_for_country, 'USD')
    # Convert USD to local
    rate_usd = exchangeRates.get('USD', 1)
    rate_local = exchangeRates.get(currency, 1)
    income_local = income_usd * (rate_local / rate_usd)
    result = calculate_all_deductions(income_local, country, city_for_country)
    return result['total_rate']


def col_adjusted_salary(job_mid, city):
    """COL-adjusted salary: job_mid * (100 / city_COLI).
    Higher = more purchasing power."""
    coli = coliData.get(city, 100)
    if coli == 0:
        return 0
    return job_mid * (100.0 / coli)


def green_line():
    """Return a thin green horizontal rule as a Drawing."""
    d = Drawing(PAGE_W - 2 * MARGIN, 3)
    d.add(Line(0, 1.5, PAGE_W - 2 * MARGIN, 1.5,
               strokeColor=ACCENT_GREEN, strokeWidth=1.5))
    return d


def gray_line():
    """Return a thin gray horizontal rule as a Drawing."""
    d = Drawing(PAGE_W - 2 * MARGIN, 2)
    d.add(Line(0, 1, PAGE_W - 2 * MARGIN, 1,
               strokeColor=SUBTLE_LINE, strokeWidth=0.5))
    return d


# ── Section builders ─────────────────────────────────────────────────────────

def build_cover_page():
    """Return list of Platypus flowables for cover page."""
    elems = []

    # Vertical spacing to center content
    elems.append(Spacer(1, 120))

    # Green accent line
    elems.append(green_line())
    elems.append(Spacer(1, 18))

    # Title
    elems.append(Paragraph('2026 Global Salary &amp;<br/>Cost of Living Report', style_title))
    elems.append(Spacer(1, 12))

    # Subtitle stats
    elems.append(Paragraph(
        f'{TOTAL_CITIES} Cities &middot; {TOTAL_JOBS} Professions &middot; {TOTAL_NEIGHBORHOODS:,}+ Neighborhoods',
        style_subtitle
    ))
    elems.append(Spacer(1, 8))

    # Green line
    elems.append(green_line())
    elems.append(Spacer(1, 30))

    # Byline
    elems.append(Paragraph('by salary-converter.com', style_cover_byline))
    elems.append(Spacer(1, 6))
    elems.append(Paragraph('Data compiled January 2026', style_cover_byline))

    elems.append(PageBreak())
    return elems


def build_toc():
    """Return list of flowables for table of contents."""
    elems = []
    elems.append(Paragraph('Table of Contents', style_section))
    elems.append(green_line())
    elems.append(Spacer(1, 16))

    toc_items = [
        ('1.', 'Executive Summary', '3'),
        ('2.', 'City Rankings by Cost of Living', '4'),
        ('3.', 'Salary by Job Title', '9'),
        ('4.', 'Regional Breakdowns', '14'),
        ('5.', 'Neighborhood Guide', '20'),
        ('6.', 'Tax & Deductions Reference', '25'),
        ('', 'About & Methodology', '29'),
    ]

    for num, title, page in toc_items:
        if num:
            text = f'<b>{num}</b>&nbsp;&nbsp;&nbsp;{title}'
        else:
            text = f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{title}'
        row_style = ParagraphStyle(
            'TOCRow', parent=style_toc_entry,
        )
        dots = '.' * max(1, 65 - len(title))
        line = f'{text} <font color="#aaaacc">{dots}</font> {page}'
        elems.append(Paragraph(line, row_style))

    elems.append(PageBreak())
    return elems


def build_executive_summary():
    """Return list of flowables for executive summary."""
    elems = []

    elems.append(Paragraph('1. Executive Summary', style_section))
    elems.append(green_line())
    elems.append(Spacer(1, 10))

    # Compute key stats
    sorted_by_coli = sorted(coliData.items(), key=lambda x: x[1])
    cheapest_city = sorted_by_coli[0]
    most_expensive_city = sorted_by_coli[-1]

    # Best value: lowest comfortable salary (rent-based)
    comfort = {c: compute_comfortable_salary(c) for c in coliData if compute_comfortable_salary(c) > 0}
    best_value_city = min(comfort, key=comfort.get)
    best_value_sal = comfort[best_value_city]

    # Highest salary city: city with highest mid software engineer salary adjusted for COL
    se_mid = salaryRanges.get('Software Engineer', {}).get('mid', 85000)
    highest_sal_city = max(coliData.keys(), key=lambda c: col_adjusted_salary(se_mid, c))

    # Lowest tax
    all_countries = set(cityCountry.values())
    tax_free = [co for co in all_countries if not taxBrackets.get(co, [])]
    lowest_tax_note = ', '.join(sorted(tax_free)[:4]) if tax_free else 'N/A'

    intro = (
        f"This report covers {TOTAL_CITIES} cities across 12 global regions, spanning {TOTAL_JOBS} "
        f"professional roles and {TOTAL_NEIGHBORHOODS:,}+ individual neighborhoods. It provides a comprehensive "
        f"snapshot of where salaries go furthest, where living costs are lowest, and how taxes "
        f"vary from country to country. Whether you are considering relocation, negotiating a remote "
        f"work salary, or benchmarking compensation across borders, this data gives you the edge."
    )
    elems.append(Paragraph(intro, style_body))
    elems.append(Spacer(1, 10))

    # Key findings as stat cards
    elems.append(Paragraph('<b>Key Findings at a Glance</b>', style_subsection))
    elems.append(Spacer(1, 6))

    stats_data = [
        ['Most Affordable City', f'{cheapest_city[0]}', f'COLI: {cheapest_city[1]}'],
        ['Most Expensive City', f'{most_expensive_city[0]}', f'COLI: {most_expensive_city[1]}'],
        ['Best Purchasing Power*', f'{highest_sal_city}', f'For Software Engineers'],
        ['Best Value (Low Rent)', f'{best_value_city}', usd(best_value_sal) + '/yr needed'],
        ['Tax-Free Countries', lowest_tax_note, 'No income tax'],
    ]

    for label, value, note in stats_data:
        card_data = [[
            Paragraph(f'<b>{value}</b>', ParagraphStyle('sv', parent=style_body, fontName='Helvetica-Bold', fontSize=11, textColor=DARK_BLUE)),
            Paragraph(f'{label} \u2014 {note}', ParagraphStyle('sn', parent=style_body, fontSize=9, textColor=TEXT_MID)),
        ]]
        card = Table(card_data, colWidths=[160, 320])
        card.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, 0), 8),
            ('LEFTPADDING', (1, 0), (1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BACKGROUND', (0, 0), (0, 0), ACCENT_BG),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ]))
        elems.append(card)
        elems.append(Spacer(1, 3))

    elems.append(Spacer(1, 8))
    elems.append(Paragraph(
        '* Purchasing power = mid-range salary adjusted by Cost of Living Index. '
        'A lower COLI means your dollars stretch further.',
        ParagraphStyle('fn', parent=style_body_small, textColor=TEXT_MID, fontName='Helvetica-Oblique')
    ))

    elems.append(Spacer(1, 8))
    elems.append(Paragraph('<b>Methodology</b>', style_subsection))
    elems.append(Paragraph(
        'Cost of Living Index (COLI) is benchmarked against New York City (100). Rent figures represent '
        'average 1-bedroom city-center apartments in USD. Salary ranges are global baselines for each '
        'profession. Tax calculations use 2025/2026 published brackets and include social security '
        'contributions. Neighborhood rent multipliers reflect relative pricing within each city.',
        style_body
    ))

    elems.append(PageBreak())
    return elems


def build_city_rankings():
    """Return list of flowables for city rankings table."""
    elems = []

    elems.append(Paragraph('2. City Rankings by Cost of Living', style_section))
    elems.append(green_line())
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        f'All {TOTAL_CITIES} cities ranked from most affordable to most expensive. '
        f'The Comfortable Salary column shows the estimated annual gross income (USD) needed '
        f'so that 1-bedroom rent consumes no more than 30% of gross pay.',
        style_body
    ))
    elems.append(Spacer(1, 8))

    # Build ranking data
    ranked = sorted(coliData.items(), key=lambda x: x[1])
    rows = []
    for rank, (city, coli) in enumerate(ranked, 1):
        country = cityCountry.get(city, '')
        rent = cityRent1BR.get(city, 0)
        comfortable = compute_comfortable_salary(city)
        rows.append([rank, city, country, coli, rent, comfortable])

    # Split into pages of ~38 rows each
    PER_PAGE = 38
    chunks = [rows[i:i + PER_PAGE] for i in range(0, len(rows), PER_PAGE)]

    for chunk_idx, chunk in enumerate(chunks):
        header = [
            Paragraph('<b>#</b>', style_table_header),
            Paragraph('<b>City</b>', style_table_header),
            Paragraph('<b>Country</b>', style_table_header),
            Paragraph('<b>COLI</b>', style_table_header),
            Paragraph('<b>1BR Rent</b>', style_table_header),
            Paragraph('<b>Comfortable<br/>Salary (USD)</b>', style_table_header),
        ]
        table_data = [header]
        for r in chunk:
            table_data.append([
                Paragraph(str(r[0]), style_table_cell),
                Paragraph(r[1], style_table_cell_left),
                Paragraph(r[2], style_table_cell_left),
                Paragraph(f'{r[3]:.1f}', style_table_cell),
                Paragraph(usd(r[4]), style_table_cell),
                Paragraph(usd(r[5]), style_table_cell),
            ])

        col_widths = [28, 110, 100, 42, 70, 90]
        t = Table(table_data, colWidths=col_widths, repeatRows=1)

        # Build style commands
        cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_FG),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.4, SUBTLE_LINE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        # Alternating row colors
        for i in range(1, len(table_data)):
            bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
            cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

        t.setStyle(TableStyle(cmds))
        elems.append(t)

        if chunk_idx < len(chunks) - 1:
            elems.append(PageBreak())

    elems.append(PageBreak())
    return elems


def build_salary_section():
    """Return list of flowables for salary by job title."""
    elems = []

    elems.append(Paragraph('3. Salary by Job Title', style_section))
    elems.append(green_line())
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        f'Global salary ranges (USD) for {TOTAL_JOBS} professions, with the top 5 best-value cities '
        f'for each role. Best value = highest purchasing power (mid salary adjusted by COLI).',
        style_body
    ))
    elems.append(Spacer(1, 8))

    # Group jobs by category
    categories = [
        ('Healthcare', ['Doctor (General)', 'Surgeon', 'Dentist', 'Pharmacist', 'Nurse', 'Psychologist']),
        ('Engineering & Tech', ['Software Engineer', 'DevOps Engineer', 'Data Scientist',
                                'Mechanical Engineer', 'Civil Engineer', 'Electrical Engineer',
                                'Architect', 'UX Designer']),
        ('Business & Finance', ['Product Manager', 'Project Manager', 'Financial Analyst',
                                'Accountant', 'Business Analyst', 'Consultant',
                                'Investment Banker', 'Actuary']),
        ('Legal', ['Lawyer', 'Paralegal']),
        ('Marketing & Sales', ['Marketing Manager', 'Sales Manager', 'Graphic Designer', 'Content Writer']),
        ('Management & HR', ['HR Manager', 'Operations Manager', 'CEO / Executive']),
        ('Education & Research', ['Teacher', 'Professor', 'Research Scientist']),
        ('Skilled Trades & Other', ['Pilot', 'Chef', 'Journalist']),
    ]

    job_count = 0
    for cat_name, jobs in categories:
        cat_elems = []
        cat_elems.append(Paragraph(f'<b>{cat_name}</b>', style_subsection))

        for job in jobs:
            sr = salaryRanges.get(job)
            if not sr:
                continue

            # Top 5 best value cities
            best_cities = sorted(
                coliData.keys(),
                key=lambda c: col_adjusted_salary(sr['mid'], c),
                reverse=True
            )[:5]

            best_info = []
            for c in best_cities:
                adj = col_adjusted_salary(sr['mid'], c)
                best_info.append(f'{c} ({usd(round(adj))})')

            cat_elems.append(Spacer(1, 4))

            # Job header row
            header_data = [[
                Paragraph(f'<b>{job}</b>', ParagraphStyle('jh', parent=style_body, fontName='Helvetica-Bold', fontSize=9.5, textColor=DARK_BLUE)),
                Paragraph(f'{usd(sr["low"])} \u2013 {usd(sr["mid"])} \u2013 {usd(sr["high"])}',
                          ParagraphStyle('jr', parent=style_body, fontSize=8.5, textColor=TEXT_MID, alignment=TA_RIGHT)),
            ]]
            ht = Table(header_data, colWidths=[240, 240])
            ht.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BACKGROUND', (0, 0), (-1, -1), ACCENT_BG),
                ('LEFTPADDING', (0, 0), (0, 0), 6),
                ('RIGHTPADDING', (1, 0), (1, 0), 6),
            ]))
            cat_elems.append(ht)

            # Best value cities
            bv_text = '<font color="#444466">Best value:  </font>' + '  |  '.join(best_info)
            cat_elems.append(Paragraph(bv_text, ParagraphStyle('bv', parent=style_body_small, leftIndent=6)))
            cat_elems.append(Spacer(1, 2))

            job_count += 1

        elems.extend(cat_elems)

        # Page break after roughly every 12-14 jobs
        if job_count >= 12:
            elems.append(PageBreak())
            job_count = 0

    if job_count > 0:
        elems.append(PageBreak())
    return elems


def build_regional_section():
    """Return list of flowables for regional breakdowns."""
    elems = []

    elems.append(Paragraph('4. Regional Breakdowns', style_section))
    elems.append(green_line())
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        f'Cities organized into {len(cityRegions)} global regions. Each table shows cost of living index, '
        f'1-bedroom rent, and the top marginal income tax rate for the country.',
        style_body
    ))
    elems.append(Spacer(1, 8))

    region_count = 0
    for region, cities in cityRegions.items():
        region_elems = []
        region_elems.append(Paragraph(f'{region}', style_region_title))
        region_elems.append(Paragraph(
            f'{len(cities)} cities',
            ParagraphStyle('rc', parent=style_body_small, textColor=TEXT_MID)
        ))
        region_elems.append(Spacer(1, 4))

        header = [
            Paragraph('<b>City</b>', style_table_header),
            Paragraph('<b>Country</b>', style_table_header),
            Paragraph('<b>COLI</b>', style_table_header),
            Paragraph('<b>1BR Rent<br/>(USD/mo)</b>', style_table_header),
            Paragraph('<b>Top Tax<br/>Rate</b>', style_table_header),
            Paragraph('<b>SS Rate</b>', style_table_header),
        ]
        table_data = [header]

        for city in sorted(cities, key=lambda c: coliData.get(c, 0)):
            country = cityCountry.get(city, '')
            coli = coliData.get(city, 0)
            rent = cityRent1BR.get(city, 0)
            top_tax = get_top_marginal_rate(country)
            ss = get_ss_rate(country)

            table_data.append([
                Paragraph(city, style_table_cell_left),
                Paragraph(country, style_table_cell_left),
                Paragraph(f'{coli:.1f}', style_table_cell),
                Paragraph(usd(rent), style_table_cell),
                Paragraph(f'{top_tax:.0f}%', style_table_cell),
                Paragraph(f'{ss:.1f}%', style_table_cell),
            ])

        col_widths = [100, 95, 42, 70, 55, 55]
        t = Table(table_data, colWidths=col_widths, repeatRows=1)

        cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_FG),
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.4, SUBTLE_LINE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        for i in range(1, len(table_data)):
            bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
            cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

        t.setStyle(TableStyle(cmds))
        region_elems.append(t)

        # Comparative note
        colis = [coliData.get(c, 0) for c in cities]
        avg_coli = sum(colis) / len(colis) if colis else 0
        rents = [cityRent1BR.get(c, 0) for c in cities]
        avg_rent = sum(rents) / len(rents) if rents else 0
        region_elems.append(Spacer(1, 4))
        region_elems.append(Paragraph(
            f'<i>Regional average: COLI {avg_coli:.1f}, 1BR rent {usd(round(avg_rent))}/month</i>',
            ParagraphStyle('rn', parent=style_body_small, textColor=TEXT_MID, fontName='Helvetica-Oblique')
        ))
        region_elems.append(Spacer(1, 6))

        elems.extend(region_elems)
        region_count += 1

        # Page break every 2-3 regions depending on size
        if region_count % 2 == 0:
            elems.append(PageBreak())

    if region_count % 2 != 0:
        elems.append(PageBreak())
    return elems


def build_neighborhood_section():
    """Return list of flowables for neighborhood guide."""
    elems = []

    elems.append(Paragraph('5. Neighborhood Guide', style_section))
    elems.append(green_line())
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        f'For {len(cityNeighborhoods)} cities with detailed neighborhood data, we show the top 3 cheapest '
        f'and top 3 most expensive neighborhoods. Multipliers are relative to the city-center average rent '
        f'(1.00 = city average).',
        style_body
    ))
    elems.append(Spacer(1, 8))

    city_count = 0
    page_items = []

    for city in sorted(cityNeighborhoods.keys()):
        hoods = cityNeighborhoods[city]
        if not hoods:
            continue

        sorted_hoods = sorted(hoods.items(), key=lambda x: x[1])
        cheapest = sorted_hoods[:3]
        priciest = sorted_hoods[-3:][::-1]

        base_rent = cityRent1BR.get(city, 0)
        num_hoods = len(hoods)

        city_elems = []
        city_elems.append(Paragraph(
            f'<b>{city}</b> &mdash; {num_hoods} neighborhoods, base rent {usd(base_rent)}/mo',
            ParagraphStyle('nh', parent=style_body, fontName='Helvetica-Bold', fontSize=9)
        ))

        # Mini table: cheapest vs priciest
        header = [
            Paragraph('<b>Cheapest</b>', style_table_header),
            Paragraph('<b>Mult.</b>', style_table_header),
            Paragraph('<b>Est. Rent</b>', style_table_header),
            Paragraph('<b>Most Expensive</b>', style_table_header),
            Paragraph('<b>Mult.</b>', style_table_header),
            Paragraph('<b>Est. Rent</b>', style_table_header),
        ]
        table_data = [header]

        for i in range(3):
            ch_name = cheapest[i][0] if i < len(cheapest) else ''
            ch_mult = cheapest[i][1] if i < len(cheapest) else 0
            ch_rent = round(base_rent * ch_mult) if ch_mult else 0

            pr_name = priciest[i][0] if i < len(priciest) else ''
            pr_mult = priciest[i][1] if i < len(priciest) else 0
            pr_rent = round(base_rent * pr_mult) if pr_mult else 0

            table_data.append([
                Paragraph(ch_name, style_table_cell_left),
                Paragraph(f'{ch_mult:.2f}x' if ch_mult else '', style_table_cell),
                Paragraph(usd(ch_rent) if ch_rent else '', style_table_cell),
                Paragraph(pr_name, style_table_cell_left),
                Paragraph(f'{pr_mult:.2f}x' if pr_mult else '', style_table_cell),
                Paragraph(usd(pr_rent) if pr_rent else '', style_table_cell),
            ])

        col_widths = [95, 38, 55, 95, 38, 55]
        t = Table(table_data, colWidths=col_widths, repeatRows=0)
        cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_FG),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('GRID', (0, 0), (-1, -1), 0.3, SUBTLE_LINE),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEAFTER', (2, 0), (2, -1), 1.2, ACCENT_GREEN),
        ]
        for i in range(1, len(table_data)):
            bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
            cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
        t.setStyle(TableStyle(cmds))

        city_elems.append(t)
        city_elems.append(Spacer(1, 6))

        page_items.append(KeepTogether(city_elems))
        city_count += 1

        # Page break every ~6 cities
        if city_count % 6 == 0:
            elems.extend(page_items)
            elems.append(PageBreak())
            page_items = []

    if page_items:
        elems.extend(page_items)
        elems.append(PageBreak())

    return elems


def build_tax_section():
    """Return list of flowables for tax reference."""
    elems = []

    elems.append(Paragraph('6. Tax &amp; Deductions Reference', style_section))
    elems.append(green_line())
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        'Country-by-country breakdown of top marginal income tax rate, employee social security rate, '
        'and the effective total deduction rate on a $50,000 USD gross salary. Rates reflect 2025/2026 '
        'published brackets.',
        style_body
    ))
    elems.append(Spacer(1, 8))

    # Build country list from unique countries
    countries = sorted(set(cityCountry.values()))

    header = [
        Paragraph('<b>Country</b>', style_table_header),
        Paragraph('<b>Top Marginal<br/>Tax Rate</b>', style_table_header),
        Paragraph('<b>Employee<br/>SS Rate</b>', style_table_header),
        Paragraph('<b>Effective Rate<br/>at $50K USD</b>', style_table_header),
    ]
    table_data = [header]

    for country in countries:
        top_rate = get_top_marginal_rate(country)
        ss_rate = get_ss_rate(country)
        eff = effective_rate_at_income(50000, country)

        table_data.append([
            Paragraph(country, style_table_cell_left),
            Paragraph(f'{top_rate:.0f}%', style_table_cell),
            Paragraph(f'{ss_rate:.1f}%', style_table_cell),
            Paragraph(f'{eff:.1f}%', style_table_cell),
        ])

    col_widths = [140, 100, 100, 100]
    t = Table(table_data, colWidths=col_widths, repeatRows=1)

    cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), HEADER_FG),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.4, SUBTLE_LINE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    for i in range(1, len(table_data)):
        bg = ROW_EVEN if i % 2 == 0 else ROW_ODD
        cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
        # Highlight tax-free countries in green
        country = countries[i - 1]
        if not taxBrackets.get(country, []):
            cmds.append(('BACKGROUND', (0, i), (-1, i), LIGHT_GREEN))

    t.setStyle(TableStyle(cmds))
    elems.append(t)

    elems.append(Spacer(1, 10))
    elems.append(Paragraph(
        '<i>Green rows indicate zero income tax countries. SS Rate = employee-side social security '
        'contribution. Effective rate includes income tax + social security + applicable local taxes.</i>',
        ParagraphStyle('taxnote', parent=style_body_small, textColor=TEXT_MID, fontName='Helvetica-Oblique')
    ))

    elems.append(PageBreak())
    return elems


def build_final_page():
    """Return list of flowables for about/methodology page."""
    elems = []

    elems.append(Spacer(1, 60))
    elems.append(green_line())
    elems.append(Spacer(1, 16))

    elems.append(Paragraph('About This Report', style_section))
    elems.append(Spacer(1, 8))

    elems.append(Paragraph(
        'This report was compiled by the team at <b>salary-converter.com</b>, a free online tool that '
        'helps professionals compare salaries and cost of living across cities worldwide.',
        style_body
    ))
    elems.append(Spacer(1, 8))

    elems.append(Paragraph('<b>Data Sources &amp; Methodology</b>', style_subsection))
    elems.append(Paragraph(
        'Cost of Living Index (COLI) values are based on a composite of consumer price data, benchmarked '
        'to New York City = 100. Rent figures represent average 1-bedroom city-center apartments converted '
        'to USD at current exchange rates. Salary ranges are researched global baselines from industry '
        'surveys, job postings, and government labor statistics. Tax brackets use officially published '
        '2025/2026 rates for each jurisdiction. Neighborhood rent multipliers are derived from local '
        'real estate listings and rental market data.',
        style_body
    ))
    elems.append(Spacer(1, 8))

    elems.append(Paragraph('<b>Disclaimer</b>', style_subsection))
    elems.append(Paragraph(
        'All data is provided for informational purposes only and should not be used as the sole basis '
        'for relocation, salary negotiation, or financial decisions. Actual costs and salaries vary based '
        'on individual circumstances, employer, experience level, and local market conditions. Tax calculations '
        'are simplified estimates and do not account for all possible deductions, credits, or exemptions. '
        'Consult a qualified tax professional for personalized advice.',
        style_body
    ))
    elems.append(Spacer(1, 20))

    elems.append(green_line())
    elems.append(Spacer(1, 12))

    elems.append(Paragraph(
        '<b>salary-converter.com</b>',
        ParagraphStyle('url', parent=style_body, fontSize=14, fontName='Helvetica-Bold',
                       textColor=DARK_BLUE, alignment=TA_CENTER)
    ))
    elems.append(Spacer(1, 4))
    elems.append(Paragraph(
        'Compare salaries across 113 cities, calculate taxes, and explore neighborhoods.',
        ParagraphStyle('tagline', parent=style_body, fontSize=10, textColor=TEXT_MID, alignment=TA_CENTER)
    ))
    elems.append(Spacer(1, 20))
    elems.append(Paragraph(
        '\u00a9 2026 salary-converter.com. All rights reserved.',
        ParagraphStyle('copy', parent=style_body_small, fontSize=8, textColor=TEXT_MID, alignment=TA_CENTER)
    ))

    return elems


# ── Page number + footer callback ────────────────────────────────────────────

def add_page_number(canvas, doc):
    """Draw page number and footer on each page."""
    page_num = canvas.getPageNumber()
    canvas.saveState()

    # Footer line
    canvas.setStrokeColor(SUBTLE_LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 36, PAGE_W - MARGIN, 36)

    # Page number
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(TEXT_MID)
    canvas.drawCentredString(PAGE_W / 2, 24, f'Page {page_num}')

    # Footer text
    canvas.setFont('Helvetica', 6)
    canvas.drawString(MARGIN, 24, '2026 Global Salary & Cost of Living Report')
    canvas.drawRightString(PAGE_W - MARGIN, 24, 'salary-converter.com')

    canvas.restoreState()


def add_cover_background(canvas, doc):
    """Draw the dark blue background for the cover page."""
    canvas.saveState()
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    """Generate the PDF report."""
    output_path = os.path.join(ROOT, '2026-global-salary-report.pdf')

    # We use BaseDocTemplate with two page templates:
    # 1. 'cover' — dark blue background, no page number
    # 2. 'content' — white background with page numbers
    from reportlab.platypus import PageTemplate, Frame, BaseDocTemplate

    content_frame = Frame(
        MARGIN, 48, PAGE_W - 2 * MARGIN, PAGE_H - MARGIN - 48,
        id='content_frame'
    )
    cover_frame = Frame(
        MARGIN, 48, PAGE_W - 2 * MARGIN, PAGE_H - MARGIN - 48,
        id='cover_frame'
    )

    class SalaryReportDoc(BaseDocTemplate):
        def __init__(self, filename, **kw):
            BaseDocTemplate.__init__(self, filename, **kw)
            self.addPageTemplates([
                PageTemplate(id='cover', frames=[cover_frame],
                             onPage=add_cover_background),
                PageTemplate(id='content', frames=[content_frame],
                             onPage=add_page_number),
            ])

    doc = SalaryReportDoc(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=48,
        title='2026 Global Salary & Cost of Living Report',
        author='salary-converter.com',
        subject='Salary comparison and cost of living data for 113 cities worldwide',
    )

    story = []

    # Cover page (uses 'cover' template)
    print('Building cover page...')
    story.extend(build_cover_page())

    # Switch to content template after cover
    story.append(NextPageTemplate('content'))

    # TOC
    print('Building table of contents...')
    story.extend(build_toc())

    # Executive Summary
    print('Building executive summary...')
    story.extend(build_executive_summary())

    # City Rankings
    print('Building city rankings...')
    story.extend(build_city_rankings())

    # Salary by Job Title
    print('Building salary section...')
    story.extend(build_salary_section())

    # Regional Breakdowns
    print('Building regional breakdowns...')
    story.extend(build_regional_section())

    # Neighborhood Guide
    print('Building neighborhood guide...')
    story.extend(build_neighborhood_section())

    # Tax Reference
    print('Building tax reference...')
    story.extend(build_tax_section())

    # Final page
    print('Building final page...')
    story.extend(build_final_page())

    # Build the PDF
    print(f'Rendering PDF ({len(story)} flowables)...')
    doc.build(story)

    # Report file size
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f'PDF generated: {output_path}')
    print(f'File size: {size_mb:.2f} MB')


if __name__ == '__main__':
    main()
