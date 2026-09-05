// POST /api/email-result — email a durable homepage reopen link (no PDF)
//
// Cloudflare Pages Function.
// Required env vars:
//   RESEND_API_KEY   — Resend API key (resend.com)
// Optional env vars:
//   REPORT_FROM_EMAIL — sender address (default: hello@salary-converter.com)
//   REPORT_FROM_NAME  — sender display name (default: salary:converter)
//   LEADS_KV          — KV namespace binding; if present, email leads are stored for 2 years

export async function onRequestPost(context) {
  const { request, env } = context;

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON' }, 400);
  }

  const email = String(body.email || '').trim().slice(0, 320);
  const resultUrl = String(body.resultUrl || '').trim().slice(0, 2000);
  const rd = body.reportData || {};

  if (!email || !email.includes('@') || !email.includes('.')) {
    return json({ error: 'Invalid email address' }, 400);
  }

  const safeUrl = sanitizeHomepageDeepLink(resultUrl, request);
  if (!safeUrl) {
    return json({ error: 'Missing or invalid result link' }, 400);
  }

  if (!env.RESEND_API_KEY) {
    return json({ error: 'Email service not configured' }, 500);
  }

  const fromEmail = env.REPORT_FROM_EMAIL || 'hello@salary-converter.com';
  const fromName = env.REPORT_FROM_NAME || 'salary:converter';

  const currentLabel = String(rd.currentLabel || '').slice(0, 100);
  const targetLabel = String(rd.targetLabel || '').slice(0, 100);
  const formattedAmount = String(rd.formattedAmount || '').slice(0, 60);
  const formattedOriginalCurrent = String(rd.formattedOriginalCurrent || '').slice(0, 60);

  const route = currentLabel && targetLabel ? `${currentLabel} → ${targetLabel}` : '';
  const subject = route
    ? `Your cost-of-living comparison — ${route}`
    : 'Your cost-of-living comparison — reopen your True Equivalent';

  let resendRes;
  try {
    resendRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: `${fromName} <${fromEmail}>`,
        to: [email],
        subject,
        html: buildEmailHtml({
          currentLabel,
          targetLabel,
          formattedAmount,
          formattedOriginalCurrent,
          resultUrl: safeUrl,
          route,
        }),
      }),
    });
  } catch {
    return json({ error: 'Network error contacting email service' }, 502);
  }

  if (!resendRes.ok) {
    const errText = await resendRes.text().catch(() => '');
    console.error('Resend error:', resendRes.status, errText);
    return json({ error: 'Failed to send email', status: resendRes.status }, 502);
  }

  if (env.LEADS_KV) {
    try {
      const ts = new Date().toISOString();
      const key = `lead:link:${ts}-${crypto.randomUUID().slice(0, 8)}`;
      await env.LEADS_KV.put(key, JSON.stringify({
        email,
        type: 'email-result',
        currentLabel,
        targetLabel,
        formattedAmount,
        resultUrl: safeUrl,
        ts,
        country: request.cf?.country || '',
        city: request.cf?.city || '',
      }), { expirationTtl: 60 * 60 * 24 * 365 * 2 });
    } catch (_) {}
  }

  return json({ ok: true });
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    },
  });
}

/** Only allow homepage deep links on this site — never /r/ /saved/ /share landings. */
function sanitizeHomepageDeepLink(raw, request) {
  if (!raw) return null;
  let u;
  try {
    u = new URL(raw, new URL(request.url).origin);
  } catch {
    return null;
  }
  const host = u.hostname.toLowerCase();
  const allowed =
    host === 'salary-converter.com' ||
    host === 'www.salary-converter.com' ||
    host.endsWith('.salary-converter.com') ||
    host.endsWith('.pages.dev') ||
    host === 'localhost' ||
    host === '127.0.0.1';
  if (!allowed) return null;
  if (u.pathname !== '/' && u.pathname !== '') return null;
  // Require at least from/to/salary style query (durable reopen contract)
  const from = u.searchParams.get('from');
  const to = u.searchParams.get('to');
  const salary = u.searchParams.get('salary');
  if (!from || !to || !salary) return null;
  u.hash = '';
  return u.origin + '/?' + u.searchParams.toString();
}

function buildEmailHtml({ currentLabel, targetLabel, formattedAmount, formattedOriginalCurrent, resultUrl, route }) {
  return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Your cost-of-living comparison</title></head>
<body style="margin:0;padding:0;background:#f9fafb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f9fafb;padding:28px 0;">
<tr><td align="center">
<table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 16px rgba(0,0,0,0.07);">
  <tr><td style="background:#16a34a;padding:28px 32px 24px;">
    <div style="font-size:12px;font-weight:700;color:rgba(255,255,255,0.75);letter-spacing:0.4px;margin-bottom:6px;">salary:converter</div>
    <div style="font-size:22px;font-weight:700;color:#ffffff;line-height:1.3;">Your cost-of-living comparison</div>
    ${route ? `<div style="font-size:13px;color:rgba(255,255,255,0.8);margin-top:6px;">${escapeHtml(route)}</div>` : ''}
  </td></tr>
  <tr><td style="padding:28px 32px 10px;">
    <p style="font-size:15px;color:#374151;line-height:1.65;margin:0 0 18px;">Hi,</p>
    <p style="font-size:15px;color:#374151;line-height:1.65;margin:0 0 20px;">Here&rsquo;s a link that reopens your True Equivalent / lifestyle comparison — no account needed. We&rsquo;ll take you straight back to this result on salary-converter.com.</p>
    ${formattedAmount ? `
    <div style="background:#f0fdf4;border-left:4px solid #16a34a;border-radius:0 10px 10px 0;padding:16px 20px;margin:0 0 22px;">
      <div style="font-size:11px;font-weight:700;color:#16a34a;letter-spacing:0.6px;text-transform:uppercase;margin-bottom:5px;">Your True Equivalent</div>
      <div style="font-size:26px;font-weight:700;color:#111827;letter-spacing:-0.5px;">${escapeHtml(formattedAmount)}</div>
      ${formattedOriginalCurrent && route ? `<div style="font-size:12px;color:#6b7280;margin-top:5px;">${escapeHtml(formattedOriginalCurrent)} · ${escapeHtml(route)}</div>` : ''}
    </div>` : ''}
    <div style="text-align:center;margin:0 0 24px;">
      <a href="${escapeAttr(resultUrl)}" style="display:inline-block;padding:14px 28px;background:#16a34a;color:#ffffff;text-decoration:none;font-weight:700;font-size:15px;border-radius:100px;">Reopen this comparison</a>
    </div>
    <p style="font-size:13px;color:#6b7280;line-height:1.6;margin:0 0 24px;word-break:break-all;">Or paste this link: <a href="${escapeAttr(resultUrl)}" style="color:#16a34a;text-decoration:none;">${escapeHtml(resultUrl)}</a></p>
    <div style="border-top:1px solid #f3f4f6;padding-top:20px;font-size:12px;color:#9ca3af;line-height:1.6;">
      This is an estimate based on publicly available cost-of-living data, estimated tax rates, and live exchange rates. It is not financial or legal advice.<br><br>
      You received this because you asked us to email this result. <a href="mailto:hello@salary-converter.com?subject=Unsubscribe" style="color:#9ca3af;">Unsubscribe</a>
    </div>
  </td></tr>
  <tr><td style="padding:0 32px 28px;">
    <div style="background:#f9fafb;border-radius:10px;padding:14px 18px;font-size:12px;color:#9ca3af;text-align:center;">
      salary-converter.com &nbsp;·&nbsp; Compare salaries across 113 cities
    </div>
  </td></tr>
</table>
</td></tr>
</table>
</body></html>`;
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function escapeAttr(s) {
  return escapeHtml(s).replace(/'/g, '&#39;');
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}
