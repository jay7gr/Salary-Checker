// Durable Content-Type for sitemap XML. Do not use a root _headers/_routes.json
// (those failed Pages builds in 0s). This middleware no-ops for every other path.
const SITEMAP_RE = /^\/sitemap(?:-s\d+)?\.xml$/;

export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (!SITEMAP_RE.test(url.pathname)) {
    return context.next();
  }

  const res = await context.next();
  const headers = new Headers(res.headers);
  headers.set("Content-Type", "application/xml; charset=utf-8");
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
}
