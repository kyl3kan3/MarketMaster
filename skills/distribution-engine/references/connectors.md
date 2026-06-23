# Connector matrix (master index)

Live status from real read-only probes on **2026-06-23**. The machine-readable
source of truth is `../scripts/connectors.json`; this file is the human index.
Update status as connectors get fixed:

```bash
python3 ../scripts/engine.py validate --set keyword=pass --set measurement=pass
python3 ../scripts/engine.py validate --infra owned_list_exists=true
```

| Connector | Engine modes | Status | One-line reason | Playbook |
|---|---|---|---|---|
| Email — Mailchimp | distribute, validate | 🟡 fallback | MCP plans/designs/saves but cannot send; no Brevo | [email-mailchimp.md](email-mailchimp.md) |
| Social — LinkedIn & X | distribute, schedule | 🟡 fallback | No native publish API; Zapier→Buffer or manual | [social-linkedin-x.md](social-linkedin-x.md) |
| Keyword & AI-citation — Ahrefs / Semrush | diagnose | ❌ fail | Both plans lack MCP/API access | [keyword-ahrefs-semrush.md](keyword-ahrefs-semrush.md) |
| Design / carousels — Canva | atomize, distribute | ✅ pass* | Authenticated; *0 brand kits → off-brand risk | [design-canva.md](design-canva.md) |
| Short-form video — Higgsfield | atomize, distribute | ✅ pass | Ultra plan, ~2,044 credits | [video-higgsfield.md](video-higgsfield.md) |
| Measurement — Supermetrics / GA4 | validate, optimize | ❌ fail | GA4 NOT_AUTHENTICATED (0/172 sources) | [measurement-ga4.md](measurement-ga4.md) |
| Cold outbound — Apollo | distribute | ✅ build only | Provisioned; sends gated on warmup | [outbound-apollo.md](outbound-apollo.md) |
| Domain warmup | process (gates outbound) | ⛔ not started | 2–6 week floor; start day one | [domain-warmup.md](domain-warmup.md) |

## Read of the board
- **Production is the strong side** — Canva + Higgsfield are live and funded; the
  engine can *make* assets today.
- **Research + measurement are blind** — both keyword tools are plan-blocked and
  GA4 is unauthenticated, so Diagnose's research wing and the Optimize loop run
  on manual data until cleared.
- **Distribution is mixed** — email has a draft-then-finish path plus a Gmail
  fallback; social is manual/Zapier, exactly as the tracker predicted.

## Owner-only unblockers (priority order)
1. **GA4 login** — one click via the Supermetrics login link → unblocks the
   whole measurement loop.
2. **Keyword data** — upgrade Ahrefs/Semrush to an MCP-enabled plan, or accept
   the manual research fallback and scope offers accordingly.
3. **Owned audience** — stand up the list + signup form, add a Canva brand kit.
4. **Domain warmup** — buy the sending domain, set SPF/DKIM/DMARC, start warming.
