// GET /api/feedback-list?token=...&limit=200&cursor=...
// Returns stored feedback entries, newest first.
// Requires ?token= matching env.ADMIN_TOKEN.

export async function onRequestGet(context) {
  const { request, env } = context;

  if (!env.FEEDBACK_KV) {
    return json({ error: "FEEDBACK_KV namespace is not bound" }, 500);
  }
  if (!env.ADMIN_TOKEN) {
    return json({ error: "ADMIN_TOKEN env var is not set" }, 500);
  }

  const u = new URL(request.url);
  const token = u.searchParams.get("token") || "";
  if (token !== env.ADMIN_TOKEN) {
    return json({ error: "Unauthorized" }, 401);
  }

  const limit = Math.min(parseInt(u.searchParams.get("limit") || "200", 10) || 200, 1000);
  const cursor = u.searchParams.get("cursor") || undefined;

  const list = await env.FEEDBACK_KV.list({ prefix: "fb:", limit, cursor });

  // Keys are "fb:<iso-timestamp>-<rand>"; sort lexicographically descending = newest first.
  const keys = list.keys.map((k) => k.name).sort().reverse();

  const entries = await Promise.all(
    keys.map(async (k) => {
      const v = await env.FEEDBACK_KV.get(k);
      try {
        return JSON.parse(v);
      } catch {
        return null;
      }
    })
  );

  return json({
    ok: true,
    count: entries.length,
    cursor: list.list_complete ? null : list.cursor,
    entries: entries.filter(Boolean),
  });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
