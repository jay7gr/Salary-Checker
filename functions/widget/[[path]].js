// 301 /widget and /widget/* → /widgets
//
// Why a Function instead of relying on _redirects alone:
// Pages _redirects force rules (`/widget /widgets 301!`) are present and other
// redirects work, but /widget force rules do not apply on this project — uncached
// /widget returns 404.html. Functions run ahead of static/404 and reliably redirect.
// Keep the _redirects lines (harmless); this is the authoritative fix.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const dest = new URL("/widgets", url.origin);
  return Response.redirect(dest.toString(), 301);
}
