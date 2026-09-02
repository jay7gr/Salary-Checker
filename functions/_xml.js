// Serve static sitemap XML with an explicit application/xml type.
// HTML-accepting UAs (GSC/Googlebot) can 500 on Pages if this falls through
// an HTML pipeline. Do not use a root _headers/_routes.json (Pages rejected
// those in 0s) or root _middleware.js (that would invoke on every request).
export async function onRequest(context) {
  const res = await context.env.ASSETS.fetch(context.request);
  const headers = new Headers(res.headers);
  headers.set("Content-Type", "application/xml; charset=utf-8");
  headers.set("X-Content-Type-Options", "nosniff");
  return new Response(res.body, {
    status: res.status,
    statusText: res.statusText,
    headers,
  });
}
