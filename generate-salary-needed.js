#!/usr/bin/env node
/**
 * Generates "What Salary Do I Need in {City}?" pages
 * Reads data from index.html, generates static HTML for each city + neighborhood
 */

const fs = require('fs');
const path = require('path');

// Read index.html and extract data
const indexHtml = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');

function extractObject(varName) {
    // Match: const varName = { ... };
    const regex = new RegExp(`const ${varName}\\s*=\\s*\\{([\\s\\S]*?)\\};`, 'm');
    const match = indexHtml.match(regex);
    if (!match) { console.error(`Could not find ${varName}`); return {}; }
    try {
        // Clean up JS object to valid JSON-ish, then eval
        let raw = '{' + match[1] + '}';
        raw = raw.replace(/\/\/[^\n]*/g, ''); // remove comments
        raw = raw.replace(/Infinity/g, '999999999');
        raw = raw.replace(/'/g, '"');
        // Handle trailing commas
        raw = raw.replace(/,\s*}/g, '}');
        raw = raw.replace(/,\s*]/g, ']');
        return JSON.parse(raw);
    } catch (e) {
        // Fallback: use eval in a sandbox
        try {
            return new Function(`return {${match[1]}};`)();
        } catch (e2) {
            console.error(`Failed to parse ${varName}:`, e2.message);
            return {};
        }
    }
}

const coliData = extractObject('coliData');
const exchangeRates = extractObject('exchangeRates');
const cityToCurrency = extractObject('cityToCurrency');
const cityToCountry = extractObject('cityToCountry');
const taxBrackets = extractObject('taxBrackets');
const cityRent1BR = extractObject('cityRent1BR');
const cityLivingCosts = extractObject('cityLivingCosts');
const cityNeighborhoods = extractObject('cityNeighborhoods');
const countryDeductions = extractObject('countryDeductions');
const cityDeductionOverrides = extractObject('cityDeductionOverrides');

console.log(`Loaded: ${Object.keys(coliData).length} cities, ${Object.keys(exchangeRates).length} currencies`);

// Currency symbols
const currencySymbols = {
    USD:'$',GBP:'£',EUR:'€',JPY:'¥',CNY:'¥',CHF:'CHF ',AUD:'A$',CAD:'C$',
    SGD:'S$',HKD:'HK$',NZD:'NZ$',SEK:'kr ',NOK:'kr ',DKK:'kr ',CZK:'Kč ',
    HUF:'Ft ',PLN:'zł ',TRY:'₺',BRL:'R$',MXN:'MX$',ZAR:'R ',KRW:'₩',
    TWD:'NT$',IDR:'Rp ',VND:'₫',PHP:'₱',ILS:'₪',EGP:'E£',KES:'KSh ',
    NGN:'₦',MAD:'MAD ',ARS:'AR$',COP:'CO$',PEN:'S/',CLP:'CL$',UYU:'$U ',
    CRC:'₡',QAR:'QR ',SAR:'SR ',PAB:'B/',RON:'lei ',AED:'AED ',INR:'₹',MYR:'RM ',THB:'฿'
};

// Tax calculation (progressive)
function calcTax(income, countryCode) {
    const brackets = taxBrackets[countryCode] || [];
    let tax = 0, prev = 0;
    for (const [upper, rate] of brackets) {
        if (income <= prev) break;
        const taxable = Math.min(income, upper) - prev;
        tax += taxable * (rate / 100);
        prev = upper;
    }
    return tax;
}

// Social security / deductions calculation
function calcDeductions(income, countryCode, cityName) {
    let total = 0;
    const d = countryDeductions[countryCode];
    if (!d) return 0;

    if (d.social_security) {
        const ss = d.social_security;
        const rate = ss.local / 100;
        const cap = ss.cap || Infinity;
        let base = Math.min(income, cap);
        total += base * rate;
        // Reduced rate above cap (UK NI)
        if (ss.reduced_rate && income > cap) {
            total += (income - cap) * (ss.reduced_rate / 100);
        }
    }

    // City/state overrides
    const override = cityDeductionOverrides[cityName];
    if (override) {
        for (const [key, val] of Object.entries(override)) {
            if (val.rate !== undefined) {
                total += income * (val.rate / 100);
            } else if (val.flat_annual !== undefined) {
                total += val.flat_annual;
            }
        }
    }

    // Solidarity surcharge (Germany)
    if (d.solidarity) {
        const incomeTax = calcTax(income, countryCode);
        total += incomeTax * (d.solidarity.rate / 100);
    }

    return total;
}

// Convert USD to local currency
function usdToLocal(usd, currency) {
    return usd * exchangeRates[currency] / exchangeRates['USD'];
}

// Format currency
function formatCurrency(amount, currency) {
    const sym = currencySymbols[currency] || currency + ' ';
    const rounded = Math.round(amount);
    if (rounded >= 1000000) return sym + (rounded / 1000000).toFixed(1) + 'M';
    if (rounded >= 10000) return sym + rounded.toLocaleString('en-US');
    return sym + rounded.toLocaleString('en-US');
}

// Calculate salary needed for a given lifestyle tier
function calcSalaryNeeded(cityName, nbMultiplier = 1.0) {
    const currency = cityToCurrency[cityName];
    const country = cityToCountry[cityName];
    if (!currency || !country) return null;

    // Monthly costs in USD (base)
    const rent = (cityRent1BR[cityName] || 1500) * nbMultiplier;
    const living = cityLivingCosts[cityName] || { groceries: 350, utilities: 200, transport: 100, healthcare: 300, childcare: 0 };
    const essentials = living.groceries + living.utilities + living.transport + living.healthcare;

    // Three tiers (monthly in USD)
    const monthlyGetBy = rent + essentials; // Just rent + essentials
    const monthlyComfortable = monthlyGetBy / 0.5; // 50/30/20 rule: essentials = 50%
    const monthlyLiveWell = monthlyGetBy / 0.4; // essentials = 40%, more discretionary

    // Convert monthly to annual gross (need to reverse-engineer from take-home)
    // Take-home = Gross - Tax - Deductions
    // We need: Gross such that Gross - Tax(Gross) - Ded(Gross) = Annual_Net
    function grossFromNet(annualNet) {
        // Binary search for gross salary
        let lo = annualNet, hi = annualNet * 3;
        for (let i = 0; i < 50; i++) {
            const mid = (lo + hi) / 2;
            // Convert mid (in local currency) to calculate tax
            const tax = calcTax(mid, country);
            const ded = calcDeductions(mid, country, cityName);
            const net = mid - tax - ded;
            if (net < annualNet) lo = mid;
            else hi = mid;
        }
        return Math.round((lo + hi) / 2);
    }

    // Annual net needed in local currency
    const annualGetByUSD = monthlyGetBy * 12;
    const annualComfortableUSD = monthlyComfortable * 12;
    const annualLiveWellUSD = monthlyLiveWell * 12;

    const annualGetByLocal = usdToLocal(annualGetByUSD, currency);
    const annualComfortableLocal = usdToLocal(annualComfortableUSD, currency);
    const annualLiveWellLocal = usdToLocal(annualLiveWellUSD, currency);

    const grossGetBy = grossFromNet(annualGetByLocal);
    const grossComfortable = grossFromNet(annualComfortableLocal);
    const grossLiveWell = grossFromNet(annualLiveWellLocal);

    // Effective tax rate for the "comfortable" tier
    const taxComf = calcTax(grossComfortable, country);
    const dedComf = calcDeductions(grossComfortable, country, cityName);
    const effectiveTaxRate = ((taxComf + dedComf) / grossComfortable * 100).toFixed(1);

    // Monthly breakdown in local currency
    const monthlyRentLocal = usdToLocal(rent, currency);
    const monthlyEssentialsLocal = usdToLocal(essentials, currency);

    return {
        currency,
        grossGetBy, grossComfortable, grossLiveWell,
        monthlyRentLocal, monthlyEssentialsLocal,
        effectiveTaxRate,
        rentUSD: rent, essentialsUSD: essentials
    };
}

// Slug helper
function toSlug(name) {
    return name.toLowerCase()
        .replace(/\s*\(.*?\)\s*/g, '') // remove parenthetical
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');
}

// Country name lookup
const countryNames = {
    US:'United States',CA:'Canada',MX:'Mexico',PA:'Panama',GB:'United Kingdom',
    FR:'France',NL:'Netherlands',DE:'Germany',IE:'Ireland',BE:'Belgium',LU:'Luxembourg',
    CH:'Switzerland',ES:'Spain',PT:'Portugal',IT:'Italy',GR:'Greece',HR:'Croatia',
    SE:'Sweden',DK:'Denmark',FI:'Finland',NO:'Norway',AT:'Austria',CZ:'Czech Republic',
    HU:'Hungary',PL:'Poland',RO:'Romania',EE:'Estonia',LV:'Latvia',TR:'Turkey',
    JP:'Japan',KR:'South Korea',HK:'Hong Kong',TW:'Taiwan',CN:'China',SG:'Singapore',
    TH:'Thailand',MY:'Malaysia',VN:'Vietnam',PH:'Philippines',ID:'Indonesia',KH:'Cambodia',
    IN:'India',AU:'Australia',NZ:'New Zealand',AE:'UAE',QA:'Qatar',SA:'Saudi Arabia',
    IL:'Israel',ZA:'South Africa',KE:'Kenya',NG:'Nigeria',EG:'Egypt',MA:'Morocco',
    BR:'Brazil',AR:'Argentina',CO:'Colombia',PE:'Peru',CL:'Chile',UY:'Uruguay',CR:'Costa Rica'
};

// Generate HTML page
function generatePage(cityName, neighborhoodName, nbMultiplier) {
    const data = calcSalaryNeeded(cityName, nbMultiplier || 1.0);
    if (!data) return null;

    const isNeighborhood = !!neighborhoodName;
    const displayName = isNeighborhood ? `${neighborhoodName}, ${cityName}` : cityName;
    const title = `What Salary Do You Need in ${displayName}? (2026)`;
    const desc = isNeighborhood
        ? `Find out the minimum salary to live in ${neighborhoodName}, ${cityName} in 2026. From ${formatCurrency(data.grossGetBy, data.currency)} to get by, to ${formatCurrency(data.grossComfortable, data.currency)} to live comfortably.`
        : `Find out the minimum salary to live in ${cityName} in 2026. From ${formatCurrency(data.grossGetBy, data.currency)} to get by, to ${formatCurrency(data.grossComfortable, data.currency)} to live comfortably. After-tax breakdown included.`;

    const citySlug = toSlug(cityName);
    const country = cityToCountry[cityName];
    const countryName = countryNames[country] || country;
    const canonical = isNeighborhood
        ? `https://salary-converter.com/salary-needed/${citySlug}/${toSlug(neighborhoodName)}.html`
        : `https://salary-converter.com/salary-needed/${citySlug}.html`;

    // Neighborhood list for city pages
    let neighborhoodSection = '';
    if (!isNeighborhood && cityNeighborhoods[cityName]) {
        const nbs = cityNeighborhoods[cityName];
        const nbEntries = Object.entries(nbs).map(([name, mult]) => {
            const nbData = calcSalaryNeeded(cityName, mult);
            return { name, mult, data: nbData };
        }).sort((a, b) => b.data.grossComfortable - a.data.grossComfortable);

        const rows = nbEntries.map(({ name, mult, data: d }) =>
            `<tr>
                <td><a href="/salary-needed/${citySlug}/${toSlug(name)}.html" style="color:var(--accent);text-decoration:none;font-weight:500;">${name}</a></td>
                <td style="text-align:right">${formatCurrency(d.grossGetBy, d.currency)}</td>
                <td style="text-align:right;font-weight:600">${formatCurrency(d.grossComfortable, d.currency)}</td>
                <td style="text-align:right">${formatCurrency(d.grossLiveWell, d.currency)}</td>
            </tr>`
        ).join('\n');

        neighborhoodSection = `
        <section class="content-card">
            <h2>Salary Needed by Neighborhood</h2>
            <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:16px;">How much you need varies dramatically within ${cityName}. Here's the breakdown for ${nbEntries.length} neighborhoods:</p>
            <div style="overflow-x:auto;">
            <table>
                <thead><tr>
                    <th>Neighborhood</th>
                    <th style="text-align:right">Get By</th>
                    <th style="text-align:right">Comfortable</th>
                    <th style="text-align:right">Live Well</th>
                </tr></thead>
                <tbody>${rows}</tbody>
            </table>
            </div>
        </section>`;
    }

    // Related links for neighborhood pages
    let relatedSection = '';
    if (isNeighborhood) {
        relatedSection = `
        <section class="content-card">
            <h2>More in ${cityName}</h2>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <a href="/salary-needed/${citySlug}.html" style="display:inline-block;padding:8px 16px;background:var(--accent,#2563eb);color:#fff;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:600;">All ${cityName} neighborhoods</a>
                <a href="/city/${citySlug}/${toSlug(neighborhoodName)}.html" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:600;">Cost of living in ${neighborhoodName}</a>
                <a href="/" style="display:inline-block;padding:8px 16px;background:var(--stat-card-bg,#f5f5f7);border-radius:10px;text-decoration:none;color:var(--text-primary);font-size:0.85rem;font-weight:600;">Salary Converter →</a>
            </div>
        </section>`;
    }

    // FAQ Schema
    const faqItems = [
        {
            q: `What salary do you need to live in ${displayName}?`,
            a: `To live comfortably in ${displayName} in 2026, you need a gross annual salary of approximately ${formatCurrency(data.grossComfortable, data.currency)}. This covers rent, groceries, utilities, transport, healthcare, and leaves 30% for wants and 20% for savings (50/30/20 rule). The minimum to get by is ${formatCurrency(data.grossGetBy, data.currency)}.`
        },
        {
            q: `What is the cost of living in ${displayName}?`,
            a: `Monthly rent for a 1-bedroom apartment in ${displayName} is approximately ${formatCurrency(data.monthlyRentLocal, data.currency)}. Essential monthly expenses (groceries, utilities, transport, healthcare) add roughly ${formatCurrency(data.monthlyEssentialsLocal, data.currency)}. The effective tax rate is ${data.effectiveTaxRate}%.`
        },
        {
            q: `Is ${formatCurrency(data.grossGetBy, data.currency)} enough to live in ${displayName}?`,
            a: `${formatCurrency(data.grossGetBy, data.currency)} is the bare minimum salary to get by in ${displayName} — it covers rent and essential expenses with very little left over. For a comfortable lifestyle with savings, you'd want at least ${formatCurrency(data.grossComfortable, data.currency)}.`
        }
    ];

    const faqSchema = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqItems.map(item => ({
            "@type": "Question",
            "name": item.q,
            "acceptedAnswer": { "@type": "Answer", "text": item.a }
        }))
    }, null, 8);

    const breadcrumbItems = isNeighborhood ? [
        { pos: 1, name: "Home", item: "https://salary-converter.com" },
        { pos: 2, name: "Salary Needed", item: "https://salary-converter.com/salary-needed/" },
        { pos: 3, name: cityName, item: `https://salary-converter.com/salary-needed/${citySlug}.html` },
        { pos: 4, name: neighborhoodName, item: canonical }
    ] : [
        { pos: 1, name: "Home", item: "https://salary-converter.com" },
        { pos: 2, name: "Salary Needed", item: "https://salary-converter.com/salary-needed/" },
        { pos: 3, name: cityName, item: canonical }
    ];

    const breadcrumbSchema = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumbItems.map(i => ({
            "@type": "ListItem", "position": i.pos, "name": i.name, "item": i.item
        }))
    }, null, 8);

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} — salary:converter</title>
    <meta name="description" content="${desc}">
    <meta name="keywords" content="salary needed ${displayName}, minimum salary ${displayName}, cost of living ${displayName}, ${displayName} salary 2026, what salary ${cityName}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="${canonical}">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="manifest" href="/manifest.json">
    <meta property="og:type" content="article">
    <meta property="og:title" content="${title}">
    <meta property="og:description" content="${desc}">
    <meta property="og:url" content="${canonical}">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:image:alt" content="Salary Converter - Compare cost of living and salaries between cities">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${title}">
    <meta name="twitter:description" content="${desc}">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    ${faqSchema}
    </script>
    <script type="application/ld+json">
    ${breadcrumbSchema}
    </script>
    <style>
        :root {
            --bg: #f5f5f7; --card-bg: #ffffff; --text-primary: #1d1d1f;
            --text-secondary: #86868b; --text-body: #4a4a4c; --accent: #2563eb;
            --accent-hover: #1d4ed8; --shadow: 0 2px 20px rgba(0,0,0,0.06);
            --border: #e5e5ea; --border-light: #f0f0f2; --stat-card-bg: #f5f5f7;
            --table-stripe: #f9f9fb;
        }
        [data-theme="dark"] {
            --bg: #000000; --card-bg: #1c1c1e; --text-primary: #f5f5f7;
            --text-secondary: #98989f; --text-body: #b0b0b5; --accent: #3b82f6;
            --accent-hover: #2563eb; --shadow: 0 2px 20px rgba(0,0,0,0.3);
            --border: #38383a; --border-light: #2c2c2e; --stat-card-bg: #2c2c2e;
            --table-stripe: #2c2c2e;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif; background:var(--bg); color:var(--text-primary); min-height:100vh; }
        .page-container { max-width:800px; margin:0 auto; padding:24px 20px 60px; }
        .breadcrumb { font-size:0.8rem; color:var(--text-secondary); margin-bottom:24px; }
        .breadcrumb a { color:var(--accent); text-decoration:none; }
        h1 { font-size:2rem; font-weight:700; letter-spacing:-1px; line-height:1.2; margin-bottom:8px; }
        .subtitle { font-size:0.95rem; color:var(--text-body); margin-bottom:32px; line-height:1.5; }
        .salary-cards { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:32px; }
        .salary-card { background:var(--card-bg); border-radius:16px; padding:24px 20px; box-shadow:var(--shadow); text-align:center; }
        .salary-card.highlight { border:2px solid var(--accent); }
        .salary-card-label { font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-secondary); margin-bottom:8px; }
        .salary-card-amount { font-size:1.5rem; font-weight:700; color:var(--text-primary); margin-bottom:6px; }
        .salary-card-note { font-size:0.75rem; color:var(--text-secondary); line-height:1.4; }
        .content-card { background:var(--card-bg); border-radius:16px; padding:28px 24px; box-shadow:var(--shadow); margin-bottom:20px; }
        .content-card h2 { font-size:1.15rem; font-weight:700; margin-bottom:16px; }
        .content-card p { font-size:0.9rem; color:var(--text-body); line-height:1.6; margin-bottom:12px; }
        table { width:100%; border-collapse:collapse; font-size:0.85rem; }
        th { text-align:left; font-size:0.7rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-secondary); padding:10px 12px; border-bottom:2px solid var(--border); }
        td { padding:10px 12px; border-bottom:1px solid var(--border-light); }
        tr:nth-child(even) td { background:var(--table-stripe); }
        .stat-row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid var(--border-light); font-size:0.9rem; }
        .stat-label { color:var(--text-secondary); }
        .stat-value { font-weight:600; }
        .faq-item { margin-bottom:20px; }
        .faq-item h3 { font-size:0.95rem; font-weight:600; margin-bottom:6px; }
        .faq-item p { font-size:0.85rem; color:var(--text-body); line-height:1.5; }
        .page-footer { margin-top:40px; padding-top:24px; border-top:1px solid var(--border-light); text-align:center; display:flex; justify-content:center; gap:20px; flex-wrap:wrap; }
        .page-footer a { font-size:0.8rem; color:var(--text-secondary); text-decoration:none; font-weight:500; }
        .page-footer a:hover { color:var(--accent); }
        .theme-toggle { position:fixed; top:16px; right:16px; width:38px; height:22px; background:var(--border); border:none; border-radius:11px; cursor:pointer; z-index:100; }
        [data-theme="dark"] .theme-toggle { background:#3b82f6; }
        .theme-toggle .thumb { position:absolute; left:2px; top:2px; width:18px; height:18px; background:var(--card-bg); border-radius:50%; transition:transform 0.3s; }
        [data-theme="dark"] .theme-toggle .thumb { transform:translateX(16px); }
        @media (max-width:600px) {
            .salary-cards { grid-template-columns:1fr; }
            h1 { font-size:1.5rem; }
            .salary-card-amount { font-size:1.3rem; }
        }
    </style>
    <script>/* early-theme-detect */(function(){var t=localStorage.getItem("theme");if(t){document.documentElement.setAttribute("data-theme",t)}else if(window.matchMedia("(prefers-color-scheme:dark)").matches){document.documentElement.setAttribute("data-theme","dark")}})();</script>
</head>
<body>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode"><span class="thumb"></span></button>

    <div class="page-container">
        <div class="breadcrumb">
            <a href="/">Home</a> › <a href="/salary-needed/">Salary Needed</a>${isNeighborhood ? ` › <a href="/salary-needed/${citySlug}.html">${cityName}</a>` : ''} › ${isNeighborhood ? neighborhoodName : cityName}
        </div>

        <h1>What Salary Do You Need to Live in ${displayName}?</h1>
        <p class="subtitle">Based on 2026 cost of living data, here's how much you need to earn (before tax) in ${displayName}, ${countryName} — from bare minimum to living well.</p>

        <div class="salary-cards">
            <div class="salary-card">
                <div class="salary-card-label">Get By</div>
                <div class="salary-card-amount">${formatCurrency(data.grossGetBy, data.currency)}</div>
                <div class="salary-card-note">Covers rent & essentials. No savings, tight budget.</div>
            </div>
            <div class="salary-card highlight">
                <div class="salary-card-label">Comfortable</div>
                <div class="salary-card-amount">${formatCurrency(data.grossComfortable, data.currency)}</div>
                <div class="salary-card-note">50/30/20 rule. Savings, dining out, some travel.</div>
            </div>
            <div class="salary-card">
                <div class="salary-card-label">Live Well</div>
                <div class="salary-card-amount">${formatCurrency(data.grossLiveWell, data.currency)}</div>
                <div class="salary-card-note">Premium lifestyle with strong savings & flexibility.</div>
            </div>
        </div>

        <section class="content-card">
            <h2>Monthly Cost Breakdown</h2>
            <div class="stat-row"><span class="stat-label">Rent (1BR)</span><span class="stat-value">${formatCurrency(data.monthlyRentLocal, data.currency)}/mo</span></div>
            <div class="stat-row"><span class="stat-label">Groceries + Utilities + Transport + Healthcare</span><span class="stat-value">${formatCurrency(data.monthlyEssentialsLocal, data.currency)}/mo</span></div>
            <div class="stat-row"><span class="stat-label">Total essentials</span><span class="stat-value">${formatCurrency(data.monthlyRentLocal + data.monthlyEssentialsLocal, data.currency)}/mo</span></div>
            <div class="stat-row" style="border-bottom:none;"><span class="stat-label">Effective tax + deductions rate</span><span class="stat-value">${data.effectiveTaxRate}%</span></div>
        </section>

        <section class="content-card">
            <h2>How We Calculate This</h2>
            <p>We start with actual monthly costs in ${displayName}: rent for a 1-bedroom apartment, groceries, utilities, transport, and healthcare. For the <strong>"comfortable"</strong> tier, we apply the 50/30/20 rule — your essentials should be 50% of take-home pay, leaving 30% for wants and 20% for savings.</p>
            <p>We then reverse-calculate the gross (pre-tax) salary you'd need, using ${countryName}'s progressive tax brackets and mandatory deductions${cityDeductionOverrides[cityName] ? ` (including local taxes for ${cityName})` : ''}. All figures are in ${data.currency} for 2026.</p>
        </section>

        ${neighborhoodSection}

        <section class="content-card">
            <h2>Frequently Asked Questions</h2>
            ${faqItems.map(item => `
            <div class="faq-item">
                <h3>${item.q}</h3>
                <p>${item.a}</p>
            </div>`).join('')}
        </section>

        ${relatedSection}

        <section class="content-card" style="text-align:center;background:var(--accent);color:#fff;border:none;">
            <h2 style="color:#fff;">Compare Your Salary</h2>
            <p style="color:rgba(255,255,255,0.85);">See what your current salary is worth in ${cityName} — or any other city.</p>
            <a href="/" style="display:inline-block;margin-top:8px;padding:12px 28px;background:#fff;color:var(--accent);border-radius:12px;text-decoration:none;font-weight:600;">Open Salary Converter →</a>
        </section>

        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/${citySlug}.html">${cityName} Cost of Living</a>
            <a href="/salary-needed/">All Cities</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>

    <script>
    (function(){
        var t=document.getElementById('themeToggle');
        function g(){var s=localStorage.getItem('theme');if(s)return s;return matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'}
        function a(m){document.documentElement.setAttribute('data-theme',m);localStorage.setItem('theme',m)}
        a(g());
        t.addEventListener('click',function(){a(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')});
    })();
    </script>
    <script src="/chat.js?v=2"></script>
</body>
</html>`;
}

// ============ GENERATE ALL PAGES ============

const outDir = path.join(__dirname, 'salary-needed');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

let cityCount = 0, nbCount = 0;

for (const cityName of Object.keys(coliData)) {
    const citySlug = toSlug(cityName);

    // Generate city page
    const cityHtml = generatePage(cityName, null, 1.0);
    if (cityHtml) {
        fs.writeFileSync(path.join(outDir, `${citySlug}.html`), cityHtml);
        cityCount++;
    }

    // Generate neighborhood pages
    const neighborhoods = cityNeighborhoods[cityName];
    if (neighborhoods) {
        const nbDir = path.join(outDir, citySlug);
        if (!fs.existsSync(nbDir)) fs.mkdirSync(nbDir, { recursive: true });

        for (const [nbName, mult] of Object.entries(neighborhoods)) {
            const nbSlug = toSlug(nbName);
            const nbHtml = generatePage(cityName, nbName, mult);
            if (nbHtml) {
                fs.writeFileSync(path.join(nbDir, `${nbSlug}.html`), nbHtml);
                nbCount++;
            }
        }
    }
}

// Generate index page
const indexPage = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>What Salary Do You Need? 2026 — Compare ${cityCount} Cities — salary:converter</title>
    <meta name="description" content="Find out the minimum salary to live comfortably in ${cityCount} cities worldwide. Neighborhood-level data for 2,000+ locations. Updated for 2026.">
    <meta name="keywords" content="salary needed, minimum salary, cost of living, salary by city, comfortable salary 2026">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://salary-converter.com/salary-needed/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <link rel="manifest" href="/manifest.json">
    <meta property="og:type" content="website">
    <meta property="og:title" content="What Salary Do You Need? 2026 — ${cityCount} Cities Compared">
    <meta property="og:description" content="Find the minimum salary to live comfortably in ${cityCount} cities. Neighborhood-level breakdown.">
    <meta property="og:url" content="https://salary-converter.com/salary-needed/">
    <meta property="og:image" content="https://salary-converter.com/og-image.svg">
    <meta property="og:image:alt" content="Salary Converter - Compare cost of living and salaries between cities">
    <meta property="og:site_name" content="salary:converter">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="What Salary Do You Need? ${cityCount} Cities Compared 2026">
    <meta name="twitter:description" content="Minimum salary to live comfortably in ${cityCount} cities. With neighborhood-level data.">
    <meta name="twitter:image" content="https://salary-converter.com/og-image.svg">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Salary Needed by City 2026",
        "description": "Find out the salary you need in ${cityCount} cities worldwide",
        "url": "https://salary-converter.com/salary-needed/"
    }
    </script>
    <style>
        :root { --bg:#f5f5f7;--card-bg:#fff;--text-primary:#1d1d1f;--text-secondary:#86868b;--text-body:#4a4a4c;--accent:#2563eb;--shadow:0 2px 20px rgba(0,0,0,0.06);--border:#e5e5ea;--border-light:#f0f0f2; }
        [data-theme="dark"] { --bg:#000;--card-bg:#1c1c1e;--text-primary:#f5f5f7;--text-secondary:#98989f;--text-body:#b0b0b5;--accent:#3b82f6;--shadow:0 2px 20px rgba(0,0,0,0.3);--border:#38383a;--border-light:#2c2c2e; }
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text-primary);min-height:100vh}
        .page{max-width:900px;margin:0 auto;padding:32px 20px 60px}
        h1{font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:8px}
        .subtitle{font-size:0.95rem;color:var(--text-body);margin-bottom:32px;line-height:1.5}
        .city-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
        .city-link{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:var(--card-bg);border-radius:12px;box-shadow:var(--shadow);text-decoration:none;color:var(--text-primary);transition:all 0.2s}
        .city-link:hover{border-color:var(--accent);transform:translateY(-1px)}
        .city-name{font-weight:600;font-size:0.9rem}
        .city-salary{font-size:0.85rem;color:var(--accent);font-weight:600}
        .page-footer{margin-top:40px;padding-top:24px;border-top:1px solid var(--border-light);text-align:center;display:flex;justify-content:center;gap:20px;flex-wrap:wrap}
        .page-footer a{font-size:0.8rem;color:var(--text-secondary);text-decoration:none;font-weight:500}
        .page-footer a:hover{color:var(--accent)}
    </style>
    <script>/* early-theme-detect */(function(){var t=localStorage.getItem("theme");if(t){document.documentElement.setAttribute("data-theme",t)}else if(window.matchMedia("(prefers-color-scheme:dark)").matches){document.documentElement.setAttribute("data-theme","dark")}})();</script>
</head>
<body>
    <div class="page">
        <h1>What Salary Do You Need? (2026)</h1>
        <p class="subtitle">Find the minimum salary to live comfortably in ${cityCount} cities worldwide — with neighborhood-level breakdowns for 2,000+ locations.</p>
        <div class="city-grid">
${Object.keys(coliData).sort().map(city => {
    const d = calcSalaryNeeded(city, 1.0);
    return d ? `            <a href="/salary-needed/${toSlug(city)}.html" class="city-link">
                <span class="city-name">${city}</span>
                <span class="city-salary">${formatCurrency(d.grossComfortable, d.currency)}</span>
            </a>` : '';
}).filter(Boolean).join('\n')}
        </div>
        <footer class="page-footer">
            <a href="/">Salary Converter</a>
            <a href="/city/">All Cities</a>
            <a href="/compare/">City Comparisons</a>
            <a href="/blog/">Blog</a>
        </footer>
    </div>
    <script>
    (function(){
        var b=document.body;
        var t=localStorage.getItem('theme');
        if(!t)t=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
        document.documentElement.setAttribute('data-theme',t);
    })();
    </script>
    <script src="/chat.js?v=2"></script>
</body>
</html>`;

fs.writeFileSync(path.join(outDir, 'index.html'), indexPage);

console.log(`Generated: ${cityCount} city pages + ${nbCount} neighborhood pages + 1 index page`);
console.log(`Total: ${cityCount + nbCount + 1} pages in /salary-needed/`);
