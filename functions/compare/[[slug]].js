// Reverse city-vs-city slugs: /compare/b-vs-a 301s to /compare/a-vs-b when only
// one direction exists as HTML. Nested compare/{city}/* stays 404 (Pages cap).
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const raw = context.params.slug;
  const parts = Array.isArray(raw) ? raw : raw ? [raw] : [];

  // Nested neighborhood compares are banned. Do not generate or redirect them.
  if (parts.length !== 1) {
    return context.next();
  }

  const slug = String(parts[0]).replace(/\.html$/i, "");
  if (!slug.includes("-vs-")) {
    return context.next();
  }

  const existing = await context.env.ASSETS.fetch(context.request);
  if (existing.ok) {
    return existing;
  }

  const idx = slug.indexOf("-vs-");
  const a = slug.slice(0, idx);
  const b = slug.slice(idx + 4);
  if (!a || !b) {
    return existing;
  }

  const reversePath = `/compare/${b}-vs-${a}`;
  const reverseUrl = new URL(reversePath, url.origin);
  const probe = await context.env.ASSETS.fetch(new Request(reverseUrl.toString()));
  if (probe.ok) {
    return Response.redirect(reverseUrl, 301);
  }

  return existing;
}
