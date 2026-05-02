// Server-side renders /share?... with proper OG meta tags so the link
// unfurls on Slack/LinkedIn/WhatsApp/Discord/iMessage with the user's
// specific result. Falls back gracefully if any param is missing.

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const p = url.searchParams;

  const from = (p.get("from") || "").slice(0, 40);
  const to = (p.get("to") || "").slice(0, 40);
  const fromSalary = parseFloat(p.get("fromSal") || "0");
  const toSalary = parseFloat(p.get("toSal") || "0");
  const fromCur = (p.get("fromCur") || "USD").slice(0, 4).toUpperCase();
  const toCur = (p.get("toCur") || fromCur).slice(0, 4).toUpperCase();
  const stretch = parseFloat(p.get("stretch") || "0"); // % further/less

  function fmt(n, ccy) {
    if (!n || !isFinite(n)) return "—";
    try {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: ccy,
        maximumFractionDigits: 0,
      }).format(n);
    } catch {
      return ccy + " " + Math.round(n).toLocaleString("en-US");
    }
  }

  const fromFmt = fmt(fromSalary, fromCur);
  const toFmt = fmt(toSalary, toCur);

  let title, desc;
  if (from && to && fromSalary && toSalary) {
    title = `${fromFmt} in ${from} = ${toFmt} in ${to}`;
    if (Math.abs(stretch) >= 3) {
      const dir = stretch > 0 ? "further" : "less";
      const pct = Math.abs(Math.round(stretch));
      desc = `Same lifestyle, ${pct}% ${dir} purchasing power. Compare salaries across 182 cities with real cost-of-living data.`;
    } else {
      desc = `Roughly on par after cost of living. Compare salaries across 182 cities with real data.`;
    }
  } else {
    title = "What's your salary actually worth?";
    desc =
      "Compare your salary across 182 cities with real cost-of-living, tax, and rent data. Free, instant, honest.";
  }

  const canonical = url.origin + "/share?" + p.toString();
  const ogImage = url.origin + "/api/og.svg?" + p.toString();

  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]
    );
  }

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)} · salary:converter</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${esc(canonical)}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">

<meta property="og:type" content="website">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${esc(canonical)}">
<meta property="og:image" content="${esc(ogImage)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="salary:converter">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(desc)}">
<meta name="twitter:image" content="${esc(ogImage)}">

<script async src="https://www.googletagmanager.com/gtag/js?id=G-MMZSM2Z96B"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-MMZSM2Z96B');</script>
<style>
:root{--bg:#f5f5f7;--card-bg:#fff;--text-primary:#1d1d1f;--text-secondary:#86868b;--text-body:#4a4a4c;--accent:#2563eb;--border:#e5e5ea;--border-light:#f0f0f2;--stat-card-bg:#f5f5f7}
@media(prefers-color-scheme:dark){:root{--bg:#000;--card-bg:#1c1c1e;--text-primary:#f5f5f7;--text-secondary:#98989f;--text-body:#b0b0b5;--accent:#3b82f6;--border:#38383a;--border-light:#2c2c2e;--stat-card-bg:#2c2c2e}}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text-primary);line-height:1.5;padding:24px;min-height:100vh;-webkit-font-smoothing:antialiased}
.wrap{max-width:680px;margin:40px auto}
.brand{text-align:center;font-size:1rem;font-weight:700;letter-spacing:-.5px;margin-bottom:24px}
.brand a{color:var(--text-primary);text-decoration:none}
.brand .colon{color:var(--accent)}
.card{background:var(--card-bg);border-radius:24px;padding:36px 32px;box-shadow:0 4px 24px rgba(0,0,0,.06);text-align:center}
@media(prefers-color-scheme:dark){.card{box-shadow:0 4px 24px rgba(0,0,0,.4)}}
.eyebrow{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:var(--accent);margin-bottom:14px}
.headline{font-size:1.7rem;font-weight:800;letter-spacing:-.5px;line-height:1.15;color:var(--text-primary);margin-bottom:14px}
.subline{font-size:1rem;color:var(--text-body);line-height:1.55;margin:0 auto 28px;max-width:480px}
.figs{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:28px}
.fig{background:var(--stat-card-bg);border-radius:14px;padding:18px 14px}
.fig .lab{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text-secondary);margin-bottom:6px}
.fig .val{font-size:1.25rem;font-weight:700;color:var(--text-primary);font-variant-numeric:tabular-nums}
.fig .city{font-size:.8rem;color:var(--text-secondary);margin-top:4px}
.cta{display:inline-block;padding:13px 32px;background:var(--accent);color:#fff;border-radius:100px;text-decoration:none;font-weight:700;font-size:.95rem;transition:opacity .2s}
.cta:hover{opacity:.9}
.foot{font-size:.75rem;color:var(--text-secondary);margin-top:20px}
.foot a{color:var(--accent);text-decoration:none}
@media(max-width:520px){.headline{font-size:1.35rem}.figs{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
  <div class="brand"><a href="/">salary<span class="colon">:</span>converter</a></div>
  <div class="card">
    <div class="eyebrow">Salary findings</div>
    <h1 class="headline">${esc(title)}</h1>
    <p class="subline">${esc(desc)}</p>
    ${
      from && to && fromSalary && toSalary
        ? `<div class="figs">
      <div class="fig"><div class="lab">From</div><div class="val">${esc(fromFmt)}</div><div class="city">${esc(from)}</div></div>
      <div class="fig"><div class="lab">Equivalent</div><div class="val">${esc(toFmt)}</div><div class="city">${esc(to)}</div></div>
    </div>`
        : ""
    }
    <a class="cta" href="/">Run your own comparison &rarr;</a>
    <div class="foot">Free &middot; instant &middot; <a href="/">182 cities, 3,400+ neighbourhoods</a></div>
  </div>
</div>
</body>
</html>`;

  return new Response(html, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "public, max-age=600",
      "X-Robots-Tag": "noindex",
    },
  });
}
