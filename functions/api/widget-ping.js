// GET /api/widget-ping?ref=<referrer-url>
// Called by embed.html on every load to log external embed locations.
// Stores to EMBEDS_KV (bind in Cloudflare Pages → Settings → Functions → KV namespace bindings).

export async function onRequestGet(context) {
  const { request, env } = context;

  const u = new URL(request.url);
  const ref = (u.searchParams.get('ref') || '').slice(0, 500);

  let origin = '';
  try {
    if (ref) origin = new URL(ref).origin;
  } catch {}

  // Ignore direct visits and self-referrals
  if (!origin || origin.includes('salary-converter.com')) {
    return new Response(null, { status: 204 });
  }

  if (env.EMBEDS_KV) {
    try {
      const ts = new Date().toISOString();
      const key = `embed:${ts}-${crypto.randomUUID().slice(0, 8)}`;
      await env.EMBEDS_KV.put(key, JSON.stringify({
        ref,
        origin,
        country: request.cf?.country || '',
        ts,
      }), { expirationTtl: 60 * 60 * 24 * 90 });
    } catch (_) {}
  }

  return new Response(null, { status: 204 });
}
