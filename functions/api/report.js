// POST /api/report — generate and email a salary negotiation PDF report
//
// Cloudflare Pages Function.
// Required env vars:
//   RESEND_API_KEY   — Resend API key (resend.com)
// Optional env vars:
//   REPORT_FROM_EMAIL — sender address (default: reports@salary-converter.com)
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
  const pdfBase64 = String(body.pdfBase64 || '');
  const rd = body.reportData || {};

  // Basic email validation
  if (!email || !email.includes('@') || !email.includes('.')) {
    return json({ error: 'Invalid email address' }, 400);
  }

  if (!pdfBase64 || pdfBase64.length < 200) {
    return json({ error: 'Missing or invalid PDF data' }, 400);
  }

  if (!env.RESEND_API_KEY) {
    return json({ error: 'Email service not configured' }, 500);
  }

  const fromEmail = env.REPORT_FROM_EMAIL || 'reports@salary-converter.com';
  const fromName = env.REPORT_FROM_NAME || 'salary:converter';

  const currentLabel = String(rd.currentLabel || '').slice(0, 100);
  const targetLabel = String(rd.targetLabel || '').slice(0, 100);
  const formattedAmount = String(rd.formattedAmount || '').slice(0, 60);
  const formattedOriginalCurrent = String(rd.formattedOriginalCurrent || '').slice(0, 60);

  const subject = currentLabel && targetLabel
    ? `Your Salary Negotiation Report — ${currentLabel} → ${targetLabel}`
    : 'Your Salary Negotiation Report';

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
        html: buildEmailHtml({ currentLabel, targetLabel, formattedAmount, formattedOriginalCurrent }),
        attachments: [{ filename: 'salary-negotiation-report.pdf', content: pdfBase64 }],
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

  // Optionally store lead in KV for 2 years
  if (env.LEADS_KV) {
    try {
      const ts = new Date().toISOString();
      const key = `lead:${ts}-${crypto.randomUUID().slice(0, 8)}`;
      await env.LEADS_KV.put(key, JSON.stringify({
        email, currentLabel, targetLabel, formattedAmount, ts,
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

function buildEmailHtml({ currentLabel, targetLabel, formattedAmount, formattedOriginalCurrent }) {
  const route = currentLabel && targetLabel ? `${currentLabel} → ${targetLabel}` : '';
  return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Your Salary Negotiation Report</title></head>
<body style="margin:0;padding:0;background:#f9fafb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f9fafb;padding:28px 0;">
<tr><td align="center">
<table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 16px rgba(0,0,0,0.07);">
  <tr><td style="background:#16a34a;padding:28px 32px 24px;">
    <div style="font-size:12px;font-weight:700;color:rgba(255,255,255,0.75);letter-spacing:0.4px;margin-bottom:6px;">salary:converter</div>
    <div style="font-size:22px;font-weight:700;color:#ffffff;line-height:1.3;">Your Salary Negotiation Report</div>
    ${route ? `<div style="font-size:13px;color:rgba(255,255,255,0.8);margin-top:6px;">${route}</div>` : ''}
  </td></tr>
  <tr><td style="padding:28px 32px 10px;">
    <p style="font-size:15px;color:#374151;line-height:1.65;margin:0 0 18px;">Hi,</p>
    <p style="font-size:15px;color:#374151;line-height:1.65;margin:0 0 20px;">Your personalized salary comparison report is attached. It includes your true equivalent salary, negotiation talking points, a monthly cash-flow breakdown, and a relocation checklist — everything you need to walk into a salary conversation with confidence.</p>
    ${formattedAmount ? `
    <div style="background:#f0fdf4;border-left:4px solid #16a34a;border-radius:0 10px 10px 0;padding:16px 20px;margin:0 0 22px;">
      <div style="font-size:11px;font-weight:700;color:#16a34a;letter-spacing:0.6px;text-transform:uppercase;margin-bottom:5px;">Your True Equivalent Salary</div>
      <div style="font-size:26px;font-weight:700;color:#111827;letter-spacing:-0.5px;">${formattedAmount}</div>
      ${formattedOriginalCurrent && route ? `<div style="font-size:12px;color:#6b7280;margin-top:5px;">${formattedOriginalCurrent} · ${route}</div>` : ''}
    </div>` : ''}
    <p style="font-size:14px;color:#6b7280;line-height:1.6;margin:0 0 24px;">Open the attached PDF for the full breakdown, or recalculate anytime at <a href="https://salary-converter.com" style="color:#16a34a;text-decoration:none;font-weight:600;">salary-converter.com</a>.</p>
    <div style="border-top:1px solid #f3f4f6;padding-top:20px;font-size:12px;color:#9ca3af;line-height:1.6;">
      This report is an estimate based on publicly available cost-of-living data, estimated tax rates, and live exchange rates. It is not financial or legal advice — consult a qualified professional for your specific situation.<br><br>
      You received this because you requested it at salary-converter.com. <a href="mailto:hello@salary-converter.com?subject=Unsubscribe%20from%20reports" style="color:#9ca3af;">Unsubscribe</a>
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

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}
