# Owned-Audience Setup

Stand up the signup landing page, wire it to a real email list, host it for free,
and add a Canva brand kit so generated carousels come out on-brand.

Time: ~30 minutes end to end. No build step, no code beyond pasting one URL.

The page you're wiring up: `skills/distribution-engine/assets/signup-landing.html`
(the embed-only version lives at `skills/distribution-engine/assets/signup-form.html`).

---

## 1. Create an audience/list

Pick **one** provider. All three have a free tier that's enough to launch.

### Option A — Mailchimp

1. Sign up / log in at <https://mailchimp.com>.
2. Left sidebar → **Audience** → **Audience dashboard**.
3. If you have no audience yet, click **Create Audience** and fill in the
   required From name, From email, and physical mailing address (CAN-SPAM
   requires it). Save.

### Option B — Brevo (formerly Sendinblue)

1. Sign up / log in at <https://www.brevo.com>.
2. Top nav → **Contacts** → **Lists** → **Add a new list**.
3. Name it (e.g. `Distribution Playbook`) and save.

### Option C — ConvertKit (now Kit)

1. Sign up / log in at <https://kit.com>.
2. Left sidebar → **Grow** → **Landing Pages & Forms** → **Create New** → **Form**.
3. Choose any inline template (you only need its action URL, not its design).
4. Name it and save.

---

## 2. Get the form action / endpoint URL

You want the raw `action` URL the `<form>` POSTs to — not an embed iframe.

### Mailchimp

1. **Audience** → **Signup forms** → **Embedded forms** → **Condensed**.
2. In the generated code, find `<form action="https://YOURDC.list-manage.com/subscribe/post?u=XXXX&id=YYYY" ...>`.
3. Copy the full `action` URL. Note the field names Mailchimp uses:
   - email field is `EMAIL` (not `email`)
   - first name (if enabled) is usually `FNAME`
   - there's an anti-bot hidden field like `b_XXXX_YYYY` — leave it out; our
     honeypot already covers bots.
   - **Adjust the page**: in `signup-landing.html`, rename the email input's
     `name="email"` to `name="EMAIL"` and `name="name"` to `name="FNAME"` so
     Mailchimp accepts them. (Or map them server-side if you proxy the post.)

### Brevo

1. **Contacts** → **Forms** → **Create a form**, pick your list, then
   **Share** → **Get the code**.
2. Either copy the `<form action="https://sibforms.com/serve/XXXX">` URL from
   the embed, or use the Brevo subscription API endpoint. Brevo's default field
   names are `EMAIL` and `FIRSTNAME` — rename the page inputs to match.

### ConvertKit / Kit

1. Open the form you created → **Embed** → **HTML**.
2. Copy the `action="https://app.kit.com/forms/XXXXXX/subscriptions"` URL.
3. Kit expects `email_address` and `fields[first_name]`. Rename the page's
   email input to `name="email_address"` and the name input to
   `name="fields[first_name]"`.

> Field-name note: every ESP names its fields slightly differently. The fastest
> path is to copy the provider's own embedded-form HTML, look at its `name=`
> attributes, and match those names in `signup-landing.html`. The endpoint URL
> is the only thing that's truly provider-specific magic.

---

## 3. Paste it into `data-endpoint`

1. Open `skills/distribution-engine/assets/signup-landing.html`.
2. Find this line (around the form tag):

   ```html
   <form id="signup" data-endpoint="REPLACE_WITH_YOUR_LIST_ENDPOINT" method="post">
   ```

3. Replace `REPLACE_WITH_YOUR_LIST_ENDPOINT` with your copied action URL, e.g.:

   ```html
   <form id="signup" data-endpoint="https://abc123.list-manage.com/subscribe/post?u=1a2b&id=3c4d" method="post">
   ```

4. If your ESP uses different field names (see step 2), rename the matching
   `name=` attributes on the `<input>` tags. Keep the honeypot input
   (`company_website`) and the four hidden UTM/referrer inputs as-is — they're
   harmless extra fields the ESP ignores, and the UTM ones give you attribution.
5. Save. Open the file in a browser and submit a test email; confirm the contact
   lands in your list.

---

## 4. Host it free (Cloudflare Pages or Netlify)

Either works. Both give you HTTPS and a free subdomain; point a custom domain
later if you want.

### Cloudflare Pages — drag-and-drop click-path

1. Put `signup-landing.html` in its own folder and **rename it `index.html`**
   so it loads at the site root.
2. Go to <https://dash.cloudflare.com> → **Workers & Pages** → **Create** →
   **Pages** tab → **Upload assets**.
3. Name the project (e.g. `distribution-playbook`) → **Create project**.
4. Drag the folder (or `index.html`) onto the upload area → **Deploy site**.
5. You get a live URL like `https://distribution-playbook.pages.dev`.
6. To update later: same project → **Create new deployment** → drop the new file.
7. (Optional) **Custom domains** tab → **Set up a domain** → enter yours and
   follow the DNS prompt.

### Netlify — drag-and-drop click-path

1. Rename `signup-landing.html` to `index.html` (same reason as above).
2. Log in at <https://app.netlify.com>.
3. On the **Sites** screen, find the **"Drag and drop your site output folder
   here"** drop zone (or **Add new site** → **Deploy manually**).
4. Drop the folder containing `index.html`.
5. You get a live URL like `https://random-name-123.netlify.app`.
6. **Site configuration** → **Change site name** to rename it.
7. To update later: drag the new folder onto the same site's **Deploys** tab.
8. (Optional) **Domain management** → **Add a domain** for a custom domain.

> Git alternative (either host): push the file to a GitHub repo, then in
> Cloudflare Pages / Netlify choose **Connect to Git**, pick the repo, and every
> push auto-deploys. Build command: none. Output directory: the folder with
> `index.html`.

---

## 5. Add a Canva brand kit (on-brand carousels)

A brand kit makes every generated carousel pull your real colors, logo, and
fonts automatically.

1. Log in at <https://www.canva.com>. (Brand Kit needs **Canva Pro** or a
   Teams plan; one brand kit is available on some free accounts.)
2. Left sidebar → **Brand** → **Brand Kit** (or <https://www.canva.com/brand/>).
3. **Colors** → **Add new** → enter your palette as hex. Match the landing
   page so the funnel looks consistent:
   - Brand: `#4F46E5`
   - Brand accent: `#7C3AED`
   - Ink (text): `#0F172A`
   - Muted: `#64748B`
   - Background: `#F8FAFC`
4. **Logos** → **Upload** → add your logo (PNG/SVG, transparent background
   preferred). Add a light and a dark version if you have them.
5. **Fonts** (Brand fonts) → set a **Heading** and **Body** font. To mirror the
   page's system stack, pick a clean sans-serif (e.g. Inter, Work Sans, or
   Roboto) for both.
6. (Optional) **Brand voice / templates** → save any carousel template so new
   designs start from it.
7. When generating a carousel in Canva, open **Brand Kit** in the editor's left
   panel and apply your colors/fonts/logo in one click — or start from a
   template that already uses them.

> Keeping the Canva palette identical to the landing page's CSS variables
> (`--brand`, `--brand-2`, `--ink`, `--muted`, `--bg`) means every atom — page,
> email, and carousel — reads as one brand.

---

## Quick checklist

- [ ] List/audience created in Mailchimp, Brevo, or ConvertKit
- [ ] Form action URL copied
- [ ] `data-endpoint` replaced in `signup-landing.html`
- [ ] Input `name=` attributes match the ESP's field names
- [ ] Test signup lands in the list
- [ ] File renamed to `index.html` and deployed to Pages/Netlify
- [ ] Live URL works on mobile
- [ ] Canva brand kit set with matching colors, logo, and fonts
