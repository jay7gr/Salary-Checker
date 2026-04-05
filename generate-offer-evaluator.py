import sys,re,json,math,os
ROOT='/home/user/Salary-Checker'
sys.path.insert(0,ROOT)
_src=open(os.path.join(ROOT,'generate-pages.py'),encoding='utf-8').read()
_ns={}
exec(_src.split("if __name__ == '__main__':")[0],_ns)
coliData=_ns['coliData'];cityToCurrency=_ns['cityToCurrency'];cityCountry=_ns['cityCountry']
cityRent1BR=_ns['cityRent1BR'];exchangeRates=_ns['exchangeRates'];taxBrackets=_ns['taxBrackets']
countryDeductions=_ns['countryDeductions'];cityDeductions=_ns.get('cityDeductions',{})
GA4=_ns['GA4_SNIPPET'];WISE_LINK=_ns['WISE_LINK'];TOGGLE_CSS=_ns['THEME_TOGGLE_CSS'];THEME_JS=_ns['THEME_JS']
def _exjs(txt,name):
    m=re.search(rf'{re.escape(name)}\s*=\s*({{.*?}});',txt,re.DOTALL)
    if not m: return {}
    raw=re.sub(r'//[^\n]*','',m.group(1))
    raw=re.sub(r"'([^']*)':",r'"\1":',raw)
    raw=re.sub(r":\s*'([^']*)'([,}])",r': "\1"\2',raw)
    try: return json.loads(raw)
    except: return {}
with open(os.path.join(ROOT,'retire','index.html')) as f: _rc=f.read()
safety_scores=_exjs(_rc,'retireSafetyIndex');health_scores=_exjs(_rc,'retireHealthcareIndex');climate_scores=_exjs(_rc,'retireClimateScore')
def _san(b): return [[1e15 if math.isinf(l) else l,r] for l,r in b]
tb_json={k:_san(v) for k,v in taxBrackets.items()}
ss_json={}
for country,ded in countryDeductions.items():
    ss=ded.get('social_security',{})
    if ss and ss.get('local',0)>0:
        ss_json[country]={'rate':ss['local'],'cap':ss.get('cap'),'reducedRate':ss.get('reduced_rate'),'label':ss.get('label','Social Security')}
city_state_json={}
for city,ded in cityDeductions.items():
    for key in ('state_tax','cantonal_tax','provincial_tax'):
        if key in ded and ded[key].get('rate',0)>0:
            city_state_json[city]={'rate':ded[key]['rate'],'label':ded[key]['label']};break
CSYM={'USD':'$','GBP':'£','EUR':'€','JPY':'¥','CNY':'¥','CAD':'C$','AUD':'A$','CHF':'CHF ','SGD':'S$','HKD':'HK$','KRW':'₩','INR':'₹','AED':'AED ','SAR':'SAR ','QAR':'QAR ','ILS':'₪','THB':'฿','MYR':'RM ','IDR':'Rp ','PHP':'₱','VND':'₫','BRL':'R$','MXN':'MX$','ARS':'AR$','COP':'COP ','PEN':'S/ ','CLP':'CLP ','UYU':'UYU ','CRC':'₡','TWD':'NT$','NZD':'NZ$','SEK':'kr ','NOK':'kr ','DKK':'kr ','PLN':'zł ','CZK':'Kč ','HUF':'Ft ','RON':'lei ','ZAR':'R ','KES':'KSh ','NGN':'₦','EGP':'E£ ','MAD':'MAD ','TRY':'₺'}
cities_sorted=sorted(coliData.keys())
city_options='<option value="" disabled selected>Select a city…</option>\n'+'\n'.join('<option value="'+c+'">'+c+'</option>' for c in cities_sorted)
DATA=json.dumps({'coliData':coliData,'cityToCurrency':cityToCurrency,'cityCountry':cityCountry,'cityRent1BR':cityRent1BR,'exchangeRates':exchangeRates,'taxBrackets':tb_json,'socialSecurity':ss_json,'cityStateTax':city_state_json,'currencySymbols':CSYM,'safetyScores':safety_scores,'healthScores':health_scores,'climateScores':climate_scores},separators=(',',':'))
os.makedirs(os.path.join(ROOT,'offer-evaluator'),exist_ok=True)
print("Data ready, building HTML...")

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Job Offer Evaluator 2026 — Which Offer Is Really Worth More?</title>
<meta name="description" content="Compare two job offers side-by-side. See take-home pay, rent-adjusted disposable income, and real purchasing power after cost-of-living adjustment. Free tool.">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://salary-converter.com/offer-evaluator/">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:title" content="Job Offer Evaluator — Which Offer Is Really Worth More?">
<meta property="og:description" content="Paste two job offers and get a definitive verdict. Take-home pay, rent, purchasing power — all compared side-by-side.">
<meta property="og:url" content="https://salary-converter.com/offer-evaluator/">
<meta property="og:image" content="https://salary-converter.com/og-image.png">
<meta property="og:site_name" content="salary:converter">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Job Offer Evaluator — Which Offer Is Really Worth More?">
<meta name="twitter:description" content="Compare two job offers: take-home pay, rent, purchasing power, and a definitive verdict.">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebApplication","name":"Job Offer Evaluator","url":"https://salary-converter.com/offer-evaluator/","description":"Compare two job offers by take-home pay, cost of living, and real purchasing power.","applicationCategory":"FinanceApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://salary-converter.com/"},{"@type":"ListItem","position":2,"name":"Offer Evaluator"}]}</script>
'''

CSS = '''<style>
:root{--bg:#f5f5f7;--card-bg:#fff;--text-primary:#1d1d1f;--text-secondary:#86868b;--text-body:#4a4a4c;--accent:#2563eb;--accent-hover:#1d4ed8;--shadow:0 2px 20px rgba(0,0,0,.06);--border:#e5e5ea;--border-light:#f0f0f2;--stat-card-bg:#f5f5f7;--amber:#d97706;--green:#16a34a;--red:#dc2626}
[data-theme=dark]{--bg:#000;--card-bg:#1c1c1e;--text-primary:#f5f5f7;--text-secondary:#98989f;--text-body:#b0b0b5;--accent:#3b82f6;--shadow:0 2px 20px rgba(0,0,0,.3);--border:#38383a;--border-light:#2c2c2e;--stat-card-bg:#2c2c2e}
*,::before,::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text-primary);line-height:1.5;-webkit-font-smoothing:antialiased}
.page-wrap{max-width:900px;margin:0 auto;padding:32px 20px 80px}
.nav{display:flex;align-items:center;justify-content:space-between;padding-bottom:24px;border-bottom:1px solid var(--border-light);margin-bottom:32px;flex-wrap:wrap;gap:12px}
.nav a{color:var(--text-secondary);text-decoration:none;font-size:.82rem;font-weight:500}
.nav a:hover{color:var(--accent)}
.logo{font-size:1rem;font-weight:700;color:var(--text-primary)!important;letter-spacing:-.5px}
.breadcrumb{font-size:.78rem;color:var(--text-secondary);margin-bottom:20px}
.breadcrumb a{color:var(--accent);text-decoration:none}
.hero{text-align:center;margin-bottom:36px}
.hero h1{font-size:2rem;font-weight:800;letter-spacing:-.5px;margin-bottom:10px}
.hero p{font-size:1rem;color:var(--text-body);max-width:560px;margin:0 auto}
.offers-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px}
@media(max-width:640px){.offers-grid{grid-template-columns:1fr}}
.offer-card{background:var(--card-bg);border-radius:16px;padding:24px;box-shadow:var(--shadow);border-top:4px solid var(--accent)}
.offer-card.offer-b{border-top-color:var(--amber)}
.offer-label{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent);margin-bottom:16px}
.offer-card.offer-b .offer-label{color:var(--amber)}
.field{margin-bottom:16px}
.field label{display:block;font-size:.8rem;font-weight:600;color:var(--text-secondary);margin-bottom:6px}
.field select,.field input{width:100%;padding:10px 14px;border:1.5px solid var(--border);border-radius:10px;font-size:.9rem;background:var(--bg);color:var(--text-primary);outline:none;transition:border-color .2s}
.field select:focus,.field input:focus{border-color:var(--accent)}
.salary-row{display:flex;gap:8px;align-items:center}
.currency-badge{background:var(--stat-card-bg);border:1px solid var(--border);border-radius:8px;padding:9px 12px;font-size:.85rem;font-weight:600;color:var(--text-secondary);white-space:nowrap;min-width:54px;text-align:center}
.compare-btn{display:block;width:100%;max-width:320px;margin:0 auto 32px;padding:16px 32px;background:var(--accent);color:#fff;border:none;border-radius:100px;font-size:1rem;font-weight:700;cursor:pointer;transition:background .2s,transform .1s}
.compare-btn:hover{background:var(--accent-hover);transform:translateY(-1px)}
.compare-btn:active{transform:translateY(0)}
#results{display:none}
.verdict{border-radius:16px;padding:24px 28px;margin-bottom:24px;text-align:center}
.verdict.a-wins{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #93c5fd}
.verdict.b-wins{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1px solid #fcd34d}
.verdict.tied{background:var(--stat-card-bg);border:1px solid var(--border)}
.verdict-title{font-size:1.35rem;font-weight:800;margin-bottom:6px}
.verdict.a-wins .verdict-title{color:var(--accent)}
.verdict.b-wins .verdict-title{color:var(--amber)}
.verdict-sub{font-size:.88rem;color:var(--text-secondary)}
.content-card{background:var(--card-bg);border-radius:16px;padding:24px;box-shadow:var(--shadow);margin-bottom:20px}
.content-card h2{font-size:1.05rem;font-weight:700;margin-bottom:16px}
.cmp-table{width:100%;border-collapse:collapse;font-size:.88rem}
.cmp-table th{text-align:left;padding:8px 10px;font-size:.72rem;text-transform:uppercase;letter-spacing:.5px;color:var(--text-secondary);border-bottom:2px solid var(--border)}
.cmp-table th.a-col{color:var(--accent)}
.cmp-table th.b-col{color:var(--amber)}
.cmp-table td{padding:10px 10px;border-bottom:1px solid var(--border-light)}
.cmp-table tr:last-child td{border-bottom:none}
.cmp-table .row-label{color:var(--text-secondary);font-size:.82rem}
.cmp-table .highlight td{background:var(--stat-card-bg);font-weight:700}
.cmp-table .top-row td{font-size:1.05rem;font-weight:800}
.winner-badge{display:inline-block;background:var(--green);color:#fff;border-radius:6px;padding:2px 8px;font-size:.7rem;font-weight:700;margin-left:6px;vertical-align:middle}
.tax-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:600px){.tax-grid{grid-template-columns:1fr}}
.tax-card{background:var(--stat-card-bg);border-radius:12px;padding:16px}
.tax-card h3{font-size:.82rem;font-weight:700;margin-bottom:12px;color:var(--text-secondary);text-transform:uppercase;letter-spacing:.5px}
.tax-item{display:flex;justify-content:space-between;font-size:.82rem;padding:4px 0;border-bottom:1px solid var(--border-light)}
.tax-item:last-child{border-bottom:none;font-weight:700;padding-top:8px}
.life-bars{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:600px){.life-bars{grid-template-columns:1fr}}
.life-metric{margin-bottom:4px}
.life-label{font-size:.78rem;color:var(--text-secondary);margin-bottom:4px}
.bar-wrap{display:flex;gap:8px;align-items:center}
.bar-track{flex:1;height:6px;background:var(--border);border-radius:3px;overflow:hidden}
.bar-fill-a{height:100%;background:var(--accent);border-radius:3px;transition:width .6s ease}
.bar-fill-b{height:100%;background:var(--amber);border-radius:3px;transition:width .6s ease}
.bar-val{font-size:.75rem;font-weight:600;min-width:28px;text-align:right}
.share-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:8px}
.share-btn-action{padding:10px 20px;border:1.5px solid var(--border);border-radius:100px;background:var(--card-bg);color:var(--text-primary);font-size:.85rem;font-weight:600;cursor:pointer;transition:all .2s}
.share-btn-action:hover{border-color:var(--accent);color:var(--accent)}
.wise-cta{border:1px solid #9fe870;border-left:4px solid #9fe870;border-radius:16px;padding:20px 24px;background:var(--card-bg);margin-bottom:20px}
footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--border-light);display:flex;flex-wrap:wrap;gap:16px;justify-content:center}
footer a{font-size:.78rem;color:var(--text-secondary);text-decoration:none}
footer a:hover{color:var(--accent)}
</style>
'''

BODY = ('''<body>
<div class="page-wrap">
  <nav class="nav">
    <a href="/" class="logo">salary<span style="color:var(--accent)">:</span>converter</a>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
      <a href="/city/">Cities</a><a href="/compare/">Compare</a>
      <a href="/salary/">Salaries</a><a href="/retire/">Retire</a><a href="/blog/">Blog</a>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme" type="button">
        <span class="toggle-thumb">
          <svg class="toggle-icon icon-sun" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/></svg>
          <svg class="toggle-icon icon-moon" viewBox="0 0 20 20" fill="currentColor"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/></svg>
        </span>
      </button>
    </div>
  </nav>
  <div class="breadcrumb"><a href="/">Home</a> &rsaquo; Offer Evaluator</div>
  <div class="hero">
    <h1>Which Job Offer Is Actually Better?</h1>
    <p>Enter two offers — we calculate take-home pay, rent-adjusted disposable income, and real purchasing power. You get a verdict.</p>
  </div>
  <div class="offers-grid">
    <div class="offer-card offer-a">
      <div class="offer-label">&#9679; Offer A</div>
      <div class="field"><label for="labelA">Label (optional)</label><input id="labelA" type="text" placeholder="e.g. Google London" maxlength="40"></div>
      <div class="field"><label for="cityA">City</label><select id="cityA" onchange="onCityChange('A')">''' +
city_options +
'''</select></div>
      <div class="field"><label>Annual Salary</label>
        <div class="salary-row">
          <input id="salaryA" type="number" placeholder="e.g. 65000" min="0" step="1000" style="flex:1">
          <div class="currency-badge" id="currBadgeA">USD</div>
        </div>
      </div>
    </div>
    <div class="offer-card offer-b">
      <div class="offer-label" style="color:var(--amber)">&#9679; Offer B</div>
      <div class="field"><label for="labelB">Label (optional)</label><input id="labelB" type="text" placeholder="e.g. Meta New York" maxlength="40"></div>
      <div class="field"><label for="cityB">City</label><select id="cityB" onchange="onCityChange('B')">''' +
city_options +
'''</select></div>
      <div class="field"><label>Annual Salary</label>
        <div class="salary-row">
          <input id="salaryB" type="number" placeholder="e.g. 130000" min="0" step="1000" style="flex:1">
          <div class="currency-badge" id="currBadgeB">USD</div>
        </div>
      </div>
    </div>
  </div>
  <button class="compare-btn" onclick="compare()">Compare Offers &rarr;</button>

  <div id="results">
    <div id="verdict" class="verdict"></div>
    <div class="content-card">
      <h2>Side-by-Side Breakdown</h2>
      <div style="overflow-x:auto">
      <table class="cmp-table">
        <thead><tr>
          <th style="width:44%">Metric</th>
          <th class="a-col" id="headA" style="width:28%">Offer A</th>
          <th class="b-col" id="headB" style="width:28%">Offer B</th>
        </tr></thead>
        <tbody id="cmpBody"></tbody>
      </table>
      </div>
    </div>
    <div class="content-card">
      <h2>Tax &amp; Deductions Breakdown</h2>
      <div class="tax-grid">
        <div class="tax-card"><h3 id="taxTitleA">Offer A</h3><div id="taxListA"></div></div>
        <div class="tax-card"><h3 id="taxTitleB">Offer B</h3><div id="taxListB"></div></div>
      </div>
    </div>
    <div class="content-card" id="lifeCard" style="display:none">
      <h2>Lifestyle Comparison</h2>
      <div class="life-bars" id="lifeBars"></div>
      <p style="font-size:.78rem;color:var(--text-secondary);margin-top:12px">Scores out of 100 from our retirement data index.</p>
    </div>
    <div class="content-card">
      <h2>Share This Comparison</h2>
      <p style="font-size:.85rem;color:var(--text-body);margin-bottom:8px">Send this comparison to a friend or save it for later.</p>
      <div class="share-row">
        <button class="share-btn-action" onclick="copyShareLink()">&#128279; Copy shareable link</button>
        <span id="copyMsg" style="font-size:.82rem;color:var(--green);display:none">Copied!</span>
      </div>
    </div>
    <div class="wise-cta">
      <p style="font-size:.65rem;color:var(--text-secondary);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">Sponsored</p>
      <strong style="font-size:.95rem">Moving money between countries?</strong>
      <p style="font-size:.85rem;color:var(--text-body);margin:6px 0 12px">Send your salary internationally at the real exchange rate — save up to 6x vs banks.</p>
      <a href="''' + WISE_LINK + '''" rel="noopener noreferrer sponsored" target="_blank" style="display:inline-block;padding:10px 24px;background:#9fe870;color:#1a1a1a;border-radius:100px;font-weight:700;font-size:.85rem;text-decoration:none">Try Wise for Free &rarr;</a>
    </div>
  </div>

  <div class="content-card" style="margin-top:32px">
    <h2>How It Works</h2>
    <p style="font-size:.88rem;color:var(--text-body);margin-bottom:8px">1. <strong>Gross salary in local currency</strong> — you enter this directly.</p>
    <p style="font-size:.88rem;color:var(--text-body);margin-bottom:8px">2. <strong>Tax &amp; social security</strong> — calculated using the progressive income tax brackets and social security rates for each city's country.</p>
    <p style="font-size:.88rem;color:var(--text-body);margin-bottom:8px">3. <strong>Take-home converted to USD</strong> — using ECB reference rates for a like-for-like comparison.</p>
    <p style="font-size:.88rem;color:var(--text-body);margin-bottom:8px">4. <strong>Rent deducted</strong> — average 1-bedroom rent for each city (USD/month).</p>
    <p style="font-size:.88rem;color:var(--text-body);margin-bottom:8px">5. <strong>Cost-of-living adjustment</strong> — the remaining disposable income is divided by the city's COLI index (New York = 100). This shows how far your money actually goes locally — a dollar in Bangkok buys 3× what it buys in New York.</p>
    <p style="font-size:.78rem;color:var(--text-secondary);margin-top:12px">Tax calculations are estimates for a single filer with no special deductions. Actual figures depend on your individual circumstances. <a href="/about/" style="color:var(--accent)">Data sources &rarr;</a></p>
  </div>

  <footer>
    <a href="/">Salary Converter</a><a href="/salary/">Salaries</a><a href="/city/">Cities</a>
    <a href="/compare/">Compare</a><a href="/retire/">Retire Abroad</a><a href="/blog/">Blog</a>
    <a href="/privacy/">Privacy</a>
  </footer>
</div>
''')

JS = '''<script>
const D=''' + DATA + ''';
const {coliData,cityToCurrency,cityCountry,cityRent1BR,exchangeRates,taxBrackets,socialSecurity,cityStateTax,currencySymbols,safetyScores,healthScores,climateScores}=D;

function sym(cur){return currencySymbols[cur]||cur+' ';}
function toUSD(amt,cur){return amt*(exchangeRates['USD']/exchangeRates[cur]);}
function fmtCur(amt,cur){
  const s=sym(cur); const a=Math.round(amt);
  return s+(a>=1e6?(a/1e6).toFixed(1)+'M':a>=1000?a.toLocaleString():a);
}
function fmtUSD(amt,short){
  const a=Math.round(amt);
  if(short&&Math.abs(a)>=1000)return '$'+(a/1000).toFixed(1)+'K';
  return '$'+a.toLocaleString();
}
function calcTax(income,country){
  const brackets=taxBrackets[country]||[];
  if(!brackets.length)return{tax:0,rate:0};
  let tax=0,prev=0;
  for(const[lim,r]of brackets){
    if(income<=prev)break;
    tax+=(Math.min(income,lim)-prev)*(r/100);
    prev=lim;
  }
  return{tax,rate:income>0?(tax/income)*100:0};
}
function calcSS(income,country){
  const ss=socialSecurity[country];
  if(!ss||!ss.rate)return null;
  let base=ss.cap?Math.min(income,ss.cap):income;
  let amt=base*(ss.rate/100);
  if(ss.reducedRate&&ss.cap&&income>ss.cap)amt+=(income-ss.cap)*(ss.reducedRate/100);
  return{amount:amt,rate:income>0?(amt/income)*100:0,label:ss.label||'Social Security'};
}
function calcCityTax(income,city){
  const ct=cityStateTax[city];
  if(!ct||!ct.rate)return null;
  return{amount:income*(ct.rate/100),rate:ct.rate,label:ct.label};
}
function evaluate(city,salaryLocal){
  const cur=cityToCurrency[city]||'USD';
  const country=cityCountry[city]||'';
  const coli=coliData[city]||50;
  const salaryUSD=toUSD(salaryLocal,cur);
  const{tax,rate:taxRate}=calcTax(salaryLocal,country);
  const ss=calcSS(salaryLocal,country);
  const ct=calcCityTax(salaryLocal,city);
  const totalDed=tax+(ss?ss.amount:0)+(ct?ct.amount:0);
  const takeHomeLocal=salaryLocal-totalDed;
  const takeHomeUSD=toUSD(takeHomeLocal,cur);
  const takeHomeMonthly=takeHomeUSD/12;
  const rentMonthly=cityRent1BR[city]||800;
  const afterRent=takeHomeMonthly-rentMonthly;
  const purchPower=afterRent/(coli/100);
  const totalRate=salaryLocal>0?(totalDed/salaryLocal)*100:0;
  return{city,cur,coli,country,salaryLocal,salaryUSD,tax,taxRate,ss,ct,
    totalDed,totalRate,takeHomeLocal,takeHomeUSD,takeHomeMonthly,
    rentMonthly,afterRent,purchPower};
}
function onCityChange(ab){
  const city=document.getElementById('city'+ab).value;
  if(!city)return;
  const cur=cityToCurrency[city]||'USD';
  document.getElementById('currBadge'+ab).textContent=cur;
}
function compare(){
  const cityA=document.getElementById('cityA').value;
  const cityB=document.getElementById('cityB').value;
  const salA=parseFloat(document.getElementById('salaryA').value);
  const salB=parseFloat(document.getElementById('salaryB').value);
  if(!cityA||!cityB||!salA||!salB){alert('Please fill in both cities and salaries.');return;}
  const a=evaluate(cityA,salA);
  const b=evaluate(cityB,salB);
  renderResults(a,b);
  const el=document.getElementById('results');
  el.style.display='block';
  el.scrollIntoView({behavior:'smooth',block:'start'});
  updateURL(cityA,salA,cityB,salB);
}
function nameA(){const l=document.getElementById('labelA').value.trim();return l||'Offer A';}
function nameB(){const l=document.getElementById('labelB').value.trim();return l||'Offer B';}
function renderResults(a,b){
  // Verdict
  const diff=b.purchPower-a.purchPower;
  const pct=Math.abs(a.purchPower)>0?Math.abs(diff/a.purchPower)*100:0;
  const vEl=document.getElementById('verdict');
  const nA=nameA(),nB=nameB();
  if(pct<5){
    vEl.className='verdict tied';
    vEl.innerHTML='<div class="verdict-title">These offers are roughly equivalent</div><div class="verdict-sub">Real purchasing power is within 5% after tax, rent &amp; cost-of-living adjustment.</div>';
  } else if(diff>0){
    vEl.className='verdict b-wins';
    vEl.innerHTML='<div class="verdict-title">'+nB+' gives you '+fmtUSD(Math.abs(diff),false)+' more per month</div><div class="verdict-sub">In real purchasing power after tax, average rent, and cost-of-living adjustment — '+nB+' wins.</div>';
  } else {
    vEl.className='verdict a-wins';
    vEl.innerHTML='<div class="verdict-title">'+nA+' gives you '+fmtUSD(Math.abs(diff),false)+' more per month</div><div class="verdict-sub">In real purchasing power after tax, average rent, and cost-of-living adjustment — '+nA+' wins.</div>';
  }
  // Headers
  document.getElementById('headA').textContent=nA+' ('+a.city+')';
  document.getElementById('headB').textContent=nB+' ('+b.city+')';
  // Table
  const winA=a.purchPower>=b.purchPower;
  const badge=(who)=>who?'<span class="winner-badge">&#10003; Winner</span>':'';
  const rows=[
    ['row-label','Gross Salary (local)',fmtCur(a.salaryLocal,a.cur)+'/yr',fmtCur(b.salaryLocal,b.cur)+'/yr',false],
    ['row-label','Gross Salary (USD)',fmtUSD(a.salaryUSD)+'/yr',fmtUSD(b.salaryUSD)+'/yr',false],
    ['row-label','Income Tax',fmtCur(a.tax,a.cur)+' ('+a.taxRate.toFixed(0)+'%)',fmtCur(b.tax,b.cur)+' ('+b.taxRate.toFixed(0)+'%)',false],
    ['row-label','Social Security',a.ss?fmtCur(a.ss.amount,a.cur)+' ('+a.ss.rate.toFixed(0)+'%)':'—',b.ss?fmtCur(b.ss.amount,b.cur)+' ('+b.ss.rate.toFixed(0)+'%)':'—',false],
    ['row-label highlight','Take-Home / Month (USD)',fmtUSD(a.takeHomeMonthly)+'/mo',fmtUSD(b.takeHomeMonthly)+'/mo',false],
    ['row-label','Avg 1BR Rent / Month',fmtUSD(a.rentMonthly)+'/mo',fmtUSD(b.rentMonthly)+'/mo',false],
    ['row-label highlight','After-Rent Disposable',fmtUSD(a.afterRent)+'/mo',fmtUSD(b.afterRent)+'/mo',false],
    ['row-label','Cost of Living Index','COLI '+a.coli,'COLI '+b.coli,false],
    ['row-label highlight top-row','Real Purchasing Power',fmtUSD(a.purchPower)+'/mo'+(winA?badge(true):''),fmtUSD(b.purchPower)+'/mo'+(!winA?badge(true):''),true],
  ];
  let tbody='';
  for(const[cls,label,va,vb,isTop]of rows){
    tbody+='<tr class="'+cls+'"><td class="row-label">'+label+'</td><td>'+va+'</td><td>'+vb+'</td></tr>';
  }
  document.getElementById('cmpBody').innerHTML=tbody;
  // Tax cards
  document.getElementById('taxTitleA').textContent=nA+' — '+a.city;
  document.getElementById('taxTitleB').textContent=nB+' — '+b.city;
  document.getElementById('taxListA').innerHTML=taxHTML(a);
  document.getElementById('taxListB').innerHTML=taxHTML(b);
  // Lifestyle
  const metrics=[
    ['Safety',safetyScores[a.city],safetyScores[b.city]],
    ['Healthcare',healthScores[a.city],healthScores[b.city]],
    ['Climate',climateScores[a.city],climateScores[b.city]],
  ];
  const hasAny=metrics.some(([,av,bv])=>av||bv);
  if(hasAny){
    let html='';
    for(const[label,av,bv]of metrics){
      if(!av&&!bv)continue;
      const ma=av||0,mb=bv||0,mx=Math.max(ma,mb,1);
      html+='<div>'+
        '<div class="life-label">'+label+'</div>'+
        '<div class="bar-wrap">'+
          '<div style="flex:1"><div style="font-size:.7rem;color:var(--accent);margin-bottom:2px">'+nA+'</div>'+
          '<div class="bar-track"><div class="bar-fill-a" style="width:'+(ma/100*100)+'%"></div></div></div>'+
          '<div class="bar-val">'+ma+'</div></div>'+
        '<div class="bar-wrap" style="margin-top:4px">'+
          '<div style="flex:1"><div style="font-size:.7rem;color:var(--amber);margin-bottom:2px">'+nB+'</div>'+
          '<div class="bar-track"><div class="bar-fill-b" style="width:'+(mb/100*100)+'%"></div></div></div>'+
          '<div class="bar-val">'+mb+'</div></div>'+
      '</div>';
    }
    document.getElementById('lifeBars').innerHTML=html;
    document.getElementById('lifeCard').style.display='block';
  }
}
function taxHTML(r){
  const items=[];
  items.push(['Income Tax',fmtCur(r.tax,r.cur),r.taxRate.toFixed(1)+'%']);
  if(r.ss)items.push([r.ss.label,fmtCur(r.ss.amount,r.cur),r.ss.rate.toFixed(1)+'%']);
  if(r.ct)items.push([r.ct.label,fmtCur(r.ct.amount,r.cur),r.ct.rate.toFixed(1)+'%']);
  items.push(['Total Deductions',fmtCur(r.totalDed,r.cur),r.totalRate.toFixed(1)+'%']);
  return items.map(([l,a,p])=>'<div class="tax-item"><span>'+l+'</span><span>'+a+' <small style="color:var(--text-secondary)">('+p+')</small></span></div>').join('');
}
function updateURL(cA,sA,cB,sB){
  const u=new URL(location.href);
  u.searchParams.set('a',cA+':'+sA);
  u.searchParams.set('b',cB+':'+sB);
  history.replaceState({},'',u);
}
function copyShareLink(){
  navigator.clipboard.writeText(location.href).then(()=>{
    const m=document.getElementById('copyMsg');
    m.style.display='inline';setTimeout(()=>m.style.display='none',2500);
  });
}
window.addEventListener('DOMContentLoaded',()=>{
  const p=new URLSearchParams(location.search);
  const a=p.get('a'),b=p.get('b');
  if(a&&b){
    const[cA,sA]=a.split(':');const[cB,sB]=b.split(':');
    const setCity=(id,city,ab)=>{
      const sel=document.getElementById('city'+ab);
      for(const opt of sel.options)if(opt.value===city){sel.value=city;break;}
      onCityChange(ab);
    };
    setCity('cityA',cA,'A');document.getElementById('salaryA').value=sA;
    setCity('cityB',cB,'B');document.getElementById('salaryB').value=sB;
    compare();
  }
});
</script>
'''

HTML = (HEAD + CSS + GA4 + TOGGLE_CSS.replace('<style>','<style>') +
        '</head>\n' + BODY + JS + THEME_JS + '</body>\n</html>')

out = os.path.join(ROOT,'offer-evaluator','index.html')
with open(out,'w',encoding='utf-8') as f:
    f.write(HTML)
kb = os.path.getsize(out)//1024
print(f"Written: {out} ({kb} KB)")
