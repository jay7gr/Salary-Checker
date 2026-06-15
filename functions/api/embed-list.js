// GET /api/embed-list?token=...&limit=1000
// Returns all stored embed ping entries from EMBEDS_KV.
// Requires EMBEDS_KV binding + ADMIN_TOKEN env var.

export async function onRequestGet(context) {
  const { request, env } = context;

  if (!env.EMBEDS_KV) return json({ error: 'EMBEDS_KV not bound' }, 500);
  if (!env.ADMIN_TOKEN) return json({ error: 'ADMIN_TOKEN not set' }, 500);

  const u = new URL(request.url);
  if (u.searchParams.get('token') !== env.ADMIN_TOKEN) return json({ error: 'Unauthorized' }, 401);

  const limit = Math.min(parseInt(u.searchParams.get('limit') || '1000', 10), 1000);
  const list = await env.EMBEDS_KV.list({ prefix: 'embed:', limit });
  const keys = list.keys.map(k => k.name).sort().reverse();

  const entries = await Promise.all(keys.map(async k => {
    const v = await env.EMBEDS_KV.get(k);
    try { return JSON.parse(v); } catch { return null; }
  }));

  return json({ ok: true, count: entries.length, entries: entries.filter(Boolean) });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
