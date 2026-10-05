// Reverse city-vs-city slugs: /compare/b-vs-a 301s to /compare/a-vs-b when only
// one direction exists as HTML.
//
// City-vs-city ONLY (this file matches a single path segment). Nested
// compare/{city}/* is not generated and is not redirected — those HTML files
// were removed to stay under the Cloudflare Pages 20k file cap.
//
// Why a Function instead of _redirects or extra HTML:
// - 6,328 reverse slugs exceed Pages _redirects limits (~2,100 rules / 20 KB)
// - Generating reverse HTML would push the repo from ~19.4k files over the 20k cap
// Existing static compare pages are served via ASSETS.fetch (no new HTML).
//
// Affiliate CTA: inject shared /js/wise-affiliate.js before </body> so compare
// pages pick up the flagged Wise line without regenerating ~16k HTML files.
// The script no-ops when WISE_AFFILIATE_URL is empty.

const AFFILIATE_SCRIPT =
  '<script src="/js/wise-affiliate.js?v=1" defer></script>';

function injectAffiliateScript(response) {
  const ct = response.headers.get("content-type") || "";
  if (!ct.includes("text/html")) return response;
  return new HTMLRewriter()
    .on("body", {
      element(el) {
        el.append(AFFILIATE_SCRIPT, { html: true });
      },
    })
    .transform(response);
}

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const pair = context.params.pair || "";
  const slug = String(pair).replace(/\.html$/i, "");

  const serve = async () => {
    const res = await context.env.ASSETS.fetch(context.request);
    return injectAffiliateScript(res);
  };

  if (!slug.includes("-vs-")) {
    return serve();
  }

  const existing = await context.env.ASSETS.fetch(context.request);
  if (existing.ok) {
    return injectAffiliateScript(existing);
  }

  const idx = slug.indexOf("-vs-");
  const a = slug.slice(0, idx);
  const b = slug.slice(idx + 4);
  if (!a || !b) {
    return existing;
  }

  const reversePath = `/compare/${b}-vs-${a}`;
  const reverseUrl = new URL(reversePath, url.origin);
  const probe = await context.env.ASSETS.fetch(
    new Request(reverseUrl.toString(), { method: "GET" })
  );
  if (probe.ok) {
    return Response.redirect(reverseUrl.toString(), 301);
  }
  return existing;
}
