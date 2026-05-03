# Project guardrails for Claude Code

## NEVER without explicit user confirmation in the current session

These changes have caused 3+ months of Google credibility loss in the past.
Even if the user previously approved a similar change in another session, ask
again. Every time. No exceptions.

- Add `noindex` to any page (even thin, old, low-traffic, or "draft" content)
- Modify any `<meta name="robots">` tag
- Change `robots.txt` to add `Disallow:` rules
- Remove pages from any sitemap (`sitemap*.xml`)
- Change canonical URLs (`<link rel="canonical">`)
- Delete or rename pages that may have inbound links or organic traffic
- Add `nofollow` to internal links at scale
- Block crawlers via headers, `.htaccess`, or Cloudflare rules

If you think one of the above is necessary, **STOP** and explain the
trade-off in plain English before touching anything. The user will decide.

The only files where `noindex` is currently expected and correct:
- `/404.html`
- `/admin/**`

## Other risky areas — confirm before acting

- Deleting committed files
- Mass renames or directory restructures (changes URLs)
- Force-pushing or rewriting git history
- Changing analytics IDs or AdSense client IDs
- Editing `_redirects`, `_headers`, or Cloudflare config
- Removing structured data (JSON-LD) blocks from pages

## Safe defaults

- For UX/copy/feature work, just do it.
- For bug fixes inside a single tool's logic, just do it.
- For new pages, scripts, or backend functions, just do it.
- Cache-bust `app.js?v=N` whenever app.js changes.

## Branch

All work goes on `claude/fix-page-title-ctr-eKhVq` unless the user says
otherwise. Push when changes are complete. Do not open PRs unless asked.
