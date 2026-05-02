// POST /api/feedback — store user feedback in KV
//
// Cloudflare Pages Function. Requires a KV namespace bound as FEEDBACK_KV.
// Optional env vars:
//   - ADMIN_TOKEN: shared secret used by /api/feedback-list and /admin/feedback
//   - FEEDBACK_TURNSTILE_SECRET: if set, enables Turnstile verification (skipped when absent)

export async function onRequestPost(context) {
  const { request, env } = context;

  if (!env.FEEDBACK_KV) {
    return json({ error: "FEEDBACK_KV namespace is not bound" }, 500);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Invalid JSON" }, 400);
  }

  const rating = Number(body.rating);
  if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
    return json({ error: "rating must be 1..5" }, 400);
  }

  const comment = String(body.comment || "").slice(0, 2000);
  const name = String(body.name || "").slice(0, 120);
  const tool = String(body.tool || "").slice(0, 60);
  const url = String(body.url || "").slice(0, 500);

  const ts = new Date().toISOString();
  const id = ts + "-" + crypto.randomUUID().slice(0, 8);
  const key = "fb:" + id;

  const entry = {
    id,
    ts,
    rating,
    comment,
    name,
    tool,
    url,
    ua: (request.headers.get("user-agent") || "").slice(0, 200),
    country: request.cf?.country || "",
    city: request.cf?.city || "",
  };

  // 365-day retention by default
  await env.FEEDBACK_KV.put(key, JSON.stringify(entry), {
    expirationTtl: 60 * 60 * 24 * 365,
  });

  return json({ ok: true, id });
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
    },
  });
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  });
}
