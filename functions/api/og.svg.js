// Returns a 1200x630 SVG OG card with the user's specific result.
// Most preview platforms (Slack, Discord, LinkedIn, WhatsApp on iOS,
// Telegram, Signal, Teams) handle SVG OG images; Twitter and Facebook
// will fall through to the default. Acceptable trade-off vs the
// complexity of adding a build step for PNG generation.

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const p = url.searchParams;

  const from = (p.get("from") || "").slice(0, 40);
  const to = (p.get("to") || "").slice(0, 40);
  const fromSalary = parseFloat(p.get("fromSal") || "0");
  const toSalary = parseFloat(p.get("toSal") || "0");
  const fromCur = (p.get("fromCur") || "USD").slice(0, 4).toUpperCase();
  const toCur = (p.get("toCur") || fromCur).slice(0, 4).toUpperCase();
  const stretch = parseFloat(p.get("stretch") || "0");

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

  let headline, sub;
  if (from && to && fromSalary && toSalary) {
    if (Math.abs(stretch) >= 3) {
      const dir = stretch > 0 ? "further" : "less";
      const pct = Math.abs(Math.round(stretch));
      headline = `${pct}% ${dir} purchasing power`;
      sub = `${fromFmt} in ${from}  →  ${toFmt} in ${to}`;
    } else {
      headline = `Roughly on par`;
      sub = `${fromFmt} in ${from}  ≈  ${toFmt} in ${to}`;
    }
  } else {
    headline = "What's your salary actually worth?";
    sub = "Compare salaries across 113 cities";
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]
    );
  }

  // Truncate long strings so they fit
  function clamp(s, n) {
    s = String(s);
    return s.length > n ? s.slice(0, n - 1) + "…" : s;
  }

  const stretchHigh = Math.abs(stretch) >= 3;
  const stretchPositive = stretch > 0;
  const accent = "#2563eb";
  const verdictColor = stretchHigh ? (stretchPositive ? "#16a34a" : "#dc2626") : accent;

  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f5f5f7"/>
      <stop offset="1" stop-color="#e8e9ee"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="${accent}"/>
      <stop offset="1" stop-color="#7c3aed"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bg)"/>

  <!-- Soft accent strip -->
  <rect x="60" y="60" width="1080" height="510" rx="32" ry="32" fill="#ffffff"/>

  <!-- Brand mark -->
  <text x="100" y="130" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="700" fill="#1d1d1f" letter-spacing="-0.5">salary<tspan fill="${accent}">:</tspan>converter</text>

  <!-- Eyebrow -->
  <text x="100" y="220" font-family="-apple-system, sans-serif" font-size="22" font-weight="700" fill="${accent}" letter-spacing="3" text-transform="uppercase">SALARY FINDINGS</text>

  <!-- Headline -->
  <text x="100" y="290" font-family="-apple-system, sans-serif" font-size="${headline.length > 30 ? 56 : 64}" font-weight="800" fill="#1d1d1f" letter-spacing="-1.5">${esc(clamp(headline, 38))}</text>

  <!-- Sub-line / from→to -->
  <text x="100" y="360" font-family="-apple-system, sans-serif" font-size="30" font-weight="500" fill="#4a4a4c">${esc(clamp(sub, 60))}</text>

  ${
    from && to && fromSalary && toSalary
      ? `<!-- Two boxes for the figures -->
  <g transform="translate(100, 410)">
    <rect x="0" y="0" width="450" height="120" rx="16" ry="16" fill="#f5f5f7"/>
    <text x="24" y="36" font-family="-apple-system, sans-serif" font-size="18" font-weight="700" fill="#86868b" letter-spacing="1.2">FROM</text>
    <text x="24" y="80" font-family="-apple-system, sans-serif" font-size="40" font-weight="700" fill="#1d1d1f">${esc(clamp(fromFmt, 14))}</text>
    <text x="24" y="106" font-family="-apple-system, sans-serif" font-size="20" font-weight="500" fill="#86868b">${esc(clamp(from, 30))}</text>

    <rect x="478" y="0" width="450" height="120" rx="16" ry="16" fill="#f5f5f7"/>
    <text x="502" y="36" font-family="-apple-system, sans-serif" font-size="18" font-weight="700" fill="${verdictColor}" letter-spacing="1.2">EQUIVALENT</text>
    <text x="502" y="80" font-family="-apple-system, sans-serif" font-size="40" font-weight="700" fill="#1d1d1f">${esc(clamp(toFmt, 14))}</text>
    <text x="502" y="106" font-family="-apple-system, sans-serif" font-size="20" font-weight="500" fill="#86868b">${esc(clamp(to, 30))}</text>

    <!-- Arrow connecting the two boxes -->
    <circle cx="465" cy="60" r="18" fill="${verdictColor}"/>
    <path d="M 458 60 L 472 60 M 467 55 L 472 60 L 467 65" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  </g>`
      : ""
  }

  <!-- Footer -->
  <text x="600" y="565" text-anchor="middle" font-family="-apple-system, sans-serif" font-size="20" font-weight="500" fill="#86868b">salary-converter.com  ·  free  ·  instant  ·  113 cities</text>
</svg>`;

  return new Response(svg, {
    headers: {
      "Content-Type": "image/svg+xml; charset=utf-8",
      "Cache-Control": "public, max-age=86400",
    },
  });
}
