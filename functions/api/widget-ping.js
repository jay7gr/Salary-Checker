// GET /api/widget-ping?w=<widget>&host=<hostname>&ref=<referrer-url>
// Called by embed pages on iframe load to log external embed locations.
// Stores to EMBEDS_KV (bind in Cloudflare Pages → Settings → Functions → KV namespace bindings).
// host= is preferred when document.referrer is stripped by the publisher.

function normalizeHost(raw) {
  let host = String(raw || '').trim().toLowerCase().slice(0, 253);
  if (!host || host === '(unknown)' || host === '(direct)') return '';
  try {
    if (host.includes('://')) host = new URL(host).hostname;
    else if (host.includes('/')) host = host.split('/')[0];
  } catch {
    return '';
  }
  host = host.replace(/^www\./, '').replace(/:\d+$/, '');
  if (!/^[a-z0-9]([a-z0-9.-]*[a-z0-9])?$/i.test(host)) return '';
  return host;
}

function isOurHost(host) {
  return !!(host && (host === 'salary-converter.com' || host.endsWith('.salary-converter.com')));
}

export async function onRequestGet(context) {
  const { request, env } = context;

  const u = new URL(request.url);
  const ref = (u.searchParams.get('ref') || '').slice(0, 500);
  const widget = (u.searchParams.get('w') || 'unknown').slice(0, 40);
  const explicitHost = normalizeHost(u.searchParams.get('host'));
  let host = explicitHost;

  let origin = '';
  try {
    if (ref) origin = new URL(ref).origin;
  } catch {}

  if (!host && origin) {
    try { host = normalizeHost(new URL(origin).hostname); } catch {}
  }

  // Synthesize origin from explicit host so admin can group when referrer is blank
  if (!origin && host) {
    origin = 'https://' + host;
  }

  if (!host) host = '(unknown)';

  // Ignore self-referrals. Explicit external host= wins over a blank/self referrer.
  if (isOurHost(host === '(unknown)' ? '' : host)) {
    return new Response(null, { status: 204 });
  }
  if (!explicitHost) {
    if (!origin || origin.includes('salary-converter.com')) {
      return new Response(null, { status: 204 });
    }
  } else if (origin && origin.includes('salary-converter.com')) {
    origin = 'https://' + host;
  }

  if (env.EMBEDS_KV) {
    try {
      const ts = new Date().toISOString();
      const key = `embed:${ts}-${crypto.randomUUID().slice(0, 8)}`;
      await env.EMBEDS_KV.put(key, JSON.stringify({
        host,
        ref,
        origin,
        widget,
        country: request.cf?.country || '',
        ts,
      }), { expirationTtl: 60 * 60 * 24 * 90 });
    } catch (_) {}
  }

  return new Response(null, { status: 204 });
}
