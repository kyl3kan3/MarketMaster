# Cold-Email Warmup Runbook & Schedule

> The concrete, do-this runbook for the day-one warmup task. It implements the
> playbook at
> [`skills/distribution-engine/references/domain-warmup.md`](../skills/distribution-engine/references/domain-warmup.md)
> and feeds the activation gate in
> [`skills/distribution-engine/references/outbound-apollo.md`](../skills/distribution-engine/references/outbound-apollo.md).
>
> **Why now:** warmup takes **2–6 weeks and cannot be rushed.** It finishes last
> but must start on day one. Track it as a **date-based countdown**, not a one-shot
> test. There are **no MCP tools** for this — it is infrastructure + process you (or
> ops/IT) drive by hand.

**Anchor the countdown:** record a **start date** the moment the warmup tool turns
on. Target activation = start date **+ 4–6 weeks**, contingent on the gate below.

---

## 1. Buy a separate sending domain

Register a **distinct** domain used ONLY for cold outreach — never the primary
brand domain. A `.com` close to the brand name (e.g. `getbrand.com`,
`brandhq.com`, `try-brand.com`) is ideal. Optionally 301-redirect it to the main
site for legitimacy. A deliverability hit on this domain must never threaten the
primary domain's reputation.

---

## 2. Authentication — SPF, DKIM, DMARC DNS records (templated)

Publish all three before any real send. Authentication is **non-negotiable**.
Replace `sending-domain.com`, the selector, and the provider includes with your
ESP's actual values (check your provider's docs for the exact records they issue).

### SPF — TXT record on the root
Authorizes which servers may send for the domain. **One** SPF record only; merge
all senders into a single `include:` chain.

```dns
; host: @  (sending-domain.com)
; type: TXT
sending-domain.com.   IN  TXT  "v=spf1 include:_spf.google.com include:spf.youresp.com ~all"
```
- `~all` = softfail (good during warmup); tighten to `-all` once alignment is confirmed.
- Replace `include:` entries with your actual sending provider(s).

### DKIM — TXT record on the provider's selector
Cryptographically signs mail. Your ESP gives you the **selector** and the **public
key**; publish exactly what they provide.

```dns
; host: <selector>._domainkey   (e.g. s1._domainkey.sending-domain.com)
; type: TXT
s1._domainkey.sending-domain.com.  IN  TXT  "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQ...REPLACE_WITH_PROVIDER_PUBLIC_KEY...IDAQAB"
```
- The `p=` value is the long public key string issued by your ESP — paste it verbatim.
- Some providers use CNAME-style DKIM (e.g. `s1._domainkey → s1.dkim.youresp.com`); use whichever form they specify.

### DMARC — TXT record on `_dmarc`
Tells receivers what to do with mail that fails SPF/DKIM, and where to send
reports. **Start at `p=none`** (monitor only), then tighten.

```dns
; host: _dmarc   (_dmarc.sending-domain.com)
; type: TXT
_dmarc.sending-domain.com.  IN  TXT  "v=DMARC1; p=none; rua=mailto:dmarc-reports@sending-domain.com; ruf=mailto:dmarc-reports@sending-domain.com; fo=1; adkim=s; aspf=s; pct=100"
```
- **`p=none`** during warmup → review `rua` aggregate reports → move to
  **`p=quarantine`** → then **`p=reject`** once SPF/DKIM alignment is clean.
- Optionally add **BIMI** later, only after DMARC is aligned and enforced.

**Verify before sending:** send a test to a mail-tester style report (or inspect a
delivered message's headers) and confirm **SPF=pass, DKIM=pass, DMARC=pass**.

---

## 3. Create sending mailboxes

Stand up **1–3 mailboxes** on the new domain using **real names**, each with a
complete profile and a proper signature. More than ~3 per domain spreads
reputation too thin this early. These real-name mailboxes are also the sender you
will select in Apollo at activation (never the primary domain).

---

## 4. Week-by-week volume ramp (per mailbox, per day)

Turn on an automated warmup tool that auto-sends and auto-replies to build positive
engagement. **Start tiny, ramp gradually, NEVER spike** — a sudden jump looks like
spam and undoes the ramp. Multiply by the number of mailboxes for the domain total.

| Week | Warmup sends/day (per mailbox) | Real cold sends/day (per mailbox) | Notes |
|------|-------------------------------:|----------------------------------:|-------|
| **Wk 1** | ~10 | 0 | Warmup only. Auth verified. Establish baseline engagement. |
| **Wk 2** | ~20 | 0 | Warmup only. Double gradually, never in one jump. |
| **Wk 3** | ~40 | 0 | Warmup only. Watch placement/reputation flags. |
| **Wk 4** | ~50+ | start ~10–20 (only if gate green) | Earliest real cold send — small, to your cleanest verified contacts. |
| **Wk 5** | ~50+ (hold) | ~20–30 | Hold warmup steady; grow real volume slowly. Keep warmup running alongside. |
| **Wk 6** | ~50+ (hold) | ~30–40 | Full ramp complete if metrics stayed healthy. Steady-state cold outbound. |

Rules:
- **Never spike volume.** Gradual increases only; if a metric goes bad, drop a step.
- Keep warmup running **even after** real sends begin — don't switch it off at wk 4.
- Keep content un-spammy: avoid spam-trigger words, balanced text-to-link ratio, no
  heavy images/attachments early, one clear CTA.
- 2 weeks is the floor for a low-volume program; **4–6 weeks** is the safe target —
  do not promise outbound to a client before the ramp is done.

---

## 5. Build & verify the recipient list (target bounce <2–3%)

Run this **in parallel** with the ramp so the list is ready before wk 4.

1. **Assemble a permission-aware / opt-in list** matched to the ICP (titles,
   industries, company size). **No scraped or purchased lists** — they spike
   bounces/complaints and burn the domain.
2. **Run the full list through an email verifier** (e.g. NeverBounce, ZeroBounce,
   Bouncer) before the first real send — clean it *before* sending, not after.
3. **Remove** invalid, risky/catch-all, role-based, and duplicate addresses.
4. **Target a verified bounce rate of <2–3%.** If projected bounce is higher,
   re-verify or trim until it clears. Bounces and spam complaints are exactly what
   burn a domain.
5. Keep spam complaints negligible: only contact people you have a legitimate basis
   to reach; include a working opt-out; honor CAN-SPAM / GDPR.

This list is what gets enrolled into the Apollo sequence — keep it within Apollo's
remaining **lead-credit budget** (2,500 lead credits; cycle resets ~2026-07-12).

---

## 6. The gate that unblocks Apollo activation

The Apollo sequence **`6a3aeafb2181cc0014f1ff73`** is built **INACTIVE** and must
**not** send until **ALL** of the following hold. This is the date-based gate, not a
single test — re-check (a)–(c) across the full ramp window:

- **(a) Auth passes** — a test message from the sending domain passes **SPF, DKIM,
  and DMARC** (confirm via headers or a mail-tester report).
- **(b) Healthy ramp** — the warmup tool reports a **steady, un-spiked** ramp across
  the full **2–6 weeks**, with good warmup engagement and **no reputation flags**.
- **(c) Low bounce/complaint** — verified-list bounce stays **<2–3%** and spam
  complaints stay negligible.

Plus the Apollo-side activation conditions from
[`outbound-apollo.md`](../skills/distribution-engine/references/outbound-apollo.md)
THE HARD RULE — activation requires (a)–(d) all true:
- **(a)** domain warm (the gate above),
- **(b)** a warm sender mailbox selected (from §3, via
  `mcp__Apollo_io__apollo_email_accounts_index`),
- **(c)** contacts enrolled (the verified list from §5, via
  `mcp__Apollo_io__apollo_emailer_campaigns_add_contact_ids`), and
- **(d)** the user explicitly confirms activation **in the same turn**.

**Only then** call `mcp__Apollo_io__apollo_emailer_campaigns_approve` to activate
sequence `6a3aeafb2181cc0014f1ff73`. That is the **only** step that sends real email,
and it must **never** run on a cold domain.

If any check fails mid-ramp (rising bounces/complaints, dropping placement): **pause
sending, lower volume, fix the cause** (list hygiene, content, auth), resume from a
lower step, and **restart the countdown** if reputation was damaged. There is no
"send anyway" shortcut.

---

## Quick checklist

- [ ] Separate sending domain registered (not the primary)
- [ ] SPF, DKIM, DMARC published; DMARC at `p=none`; test passes all three
- [ ] 1–3 real-name mailboxes with signatures
- [ ] Warmup tool on; **start date recorded**; ramp per the table (no spikes)
- [ ] Verified, permission-aware list built; **bounce <2–3%**
- [ ] Gate (a)+(b)+(c) green AND Apollo (b)+(c)+(d) met
- [ ] → Activate `6a3aeafb2181cc0014f1ff73` via `apollo_emailer_campaigns_approve`
