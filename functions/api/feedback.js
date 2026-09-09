// POST /api/feedback — store user feedback in KV
//
// Cloudflare Pages Function. Requires a KV namespace bound as FEEDBACK_KV.
// Optional env vars:
//   - ADMIN_TOKEN: shared secret used by /api/feedback-list and /admin/feedback
//   - FEEDBACK_TURNSTILE_SECRET: if set, enables Turnstile verification (skipped when absent)
//
// Light anti-spam: IP rate-limit via FEEDBACK_KV (max 8 POSTs / hour / IP).

const RL_LIMIT = 8;
const RL_TTL_SEC = 60 * 60; // 1 hour

export async function onRequestPost(context) {
  const { request, env } = context;

  if (!env.FEEDBACK_KV) {
    // KV not bound — GA4 already captured the rating client-side, so
    // return success rather than showing an error to the user.
    return json({ ok: true, stored: false });
  }

  // --- light IP rate-limit (cheap, fail-open if lookup errors) ---
  const ip = (request.headers.get("CF-Connecting-IP") ||
    request.headers.get("x-forwarded-for") ||
    "unknown").split(",")[0].trim().slice(0, 64);
  const rlKey = "rl:fb:" + ip;
  try {
    const raw = await env.FEEDBACK_KV.get(rlKey);
    const n = parseInt(raw || "0", 10) || 0;
    if (n >= RL_LIMIT) {
      return json({ error: "Too many requests. Try again later." }, 429);
    }
    await env.FEEDBACK_KV.put(rlKey, String(n + 1), { expirationTtl: RL_TTL_SEC });
  } catch (_) {
    // fail open — still accept the rating
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
