# WordPress Integration Evaluation

## Goal

Integrate the resume download system into dheerajchand.com (WordPress/Blocksy) so visitors can download resumes without leaving the personal site.

---

## Options

### Option 1: Subdomain (resumes.dheerajchand.com → Railway)

**How it works:** Point a CNAME record from `resumes.dheerajchand.com` to your Railway app. The resume generator runs independently; visitors go to the subdomain to download.

| Pros | Cons |
|------|------|
| Zero WordPress changes | Separate domain — doesn't feel integrated |
| Fully independent deployment | Different visual styling from main site |
| Already working on Railway | Two separate logins (WordPress + Django admin) |
| 5 minutes to set up | SEO: separate domain authority |

**Implementation:** Add a CNAME DNS record, configure the custom domain in Railway, update `ALLOWED_HOSTS`.

**Effort:** 30 minutes.

---

### Option 2: Iframe Embed on WordPress Page

**How it works:** Create a WordPress page at `dheerajchand.com/resumes/` that embeds the Railway-hosted form in an iframe.

| Pros | Cons |
|------|------|
| Visitors stay on dheerajchand.com | Iframe feels clunky (scrolling, sizing) |
| No WordPress plugin needed | Download may not work correctly inside iframe |
| Simple shortcode or Gutenberg block | Cross-origin issues with CSRF |
| 15 minutes to set up | Looks unprofessional |

**Implementation:** Add a Custom HTML block or shortcode with `<iframe src="https://your-railway-url.railway.app/" width="100%" height="800px"></iframe>`.

**Effort:** 15 minutes, but UX is poor.

---

### Option 3: WordPress Page with API Proxy

**How it works:** Build a WordPress page with a form that matches the site's Blocksy theme. The form submits to a small PHP handler that proxies the request to the Railway API and returns the generated file.

| Pros | Cons |
|------|------|
| Fully integrated — looks native | Requires PHP code on WordPress |
| Same styling, same domain | WordPress server becomes a proxy |
| No iframe, no cross-origin | Maintenance: two codebases for the form |
| Good SEO (content on main domain) | File size limits on WordPress hosting |

**Implementation:**
1. Create a WordPress page template with the form (HTML/CSS matching Blocksy)
2. Write a small PHP handler that:
   - Receives the form POST
   - Forwards it to Railway's `/download/` endpoint
   - Streams the response back to the browser

**Effort:** 2-4 hours.

---

### Option 4: WordPress Shortcode Plugin

**How it works:** Build a lightweight WordPress plugin that adds a `[resume_download]` shortcode. The shortcode renders the form using WordPress's styling. Form submission hits Railway's API directly via JavaScript (AJAX).

| Pros | Cons |
|------|------|
| Native WordPress integration | Need to build a plugin |
| Reusable shortcode on any page | JavaScript AJAX for cross-origin download |
| Plugin can be shared/open-sourced | CORS configuration needed on Railway |
| Clean separation of concerns | More complex than iframe |

**Implementation:**
1. WordPress plugin with shortcode
2. JavaScript that fetches from Railway API
3. Railway CORS configuration to allow dheerajchand.com
4. Download triggered via JavaScript blob

**Effort:** 4-6 hours.

---

### Option 5: Full WordPress Plugin Port

**How it works:** Port the entire resume generator to a WordPress plugin with its own admin pages, database tables, and PDF generation (using a PHP PDF library like TCPDF or FPDI).

| Pros | Cons |
|------|------|
| Single platform | Massive effort — rewrite everything |
| No external service needed | PHP PDF libraries are weaker than ReportLab |
| All content in WordPress DB | Lose Django admin, Grappelli, signals, caching |
| | Maintaining two versions of the same system |

**Effort:** 40-80 hours. Not recommended.

---

## Recommendation: Option 3 (API Proxy) or Option 1 (Subdomain)

**If you want zero WordPress changes:** Option 1 (subdomain). Set up `resumes.dheerajchand.com` pointing to Railway. It's running in 30 minutes and the branding already matches your site.

**If you want full integration:** Option 3 (API proxy). A WordPress page with a form that matches Blocksy's styling, proxying downloads through a small PHP handler. Takes 2-4 hours but feels completely native.

**Why not the others:**
- Option 2 (iframe): Poor UX, download issues
- Option 4 (shortcode plugin): Over-engineered for a single-user site
- Option 5 (full port): Massive effort with no benefit — the Django system is better than anything PHP-native

---

## Next Steps

1. Decide between Option 1 and Option 3
2. If Option 1: Add DNS CNAME, configure Railway custom domain
3. If Option 3: Build the WordPress page template and PHP proxy handler
4. Either way: Add a link from dheerajchand.com navigation to the resume download page
