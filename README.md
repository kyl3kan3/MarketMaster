# MarketMaster

MarketMaster is a Vercel-ready validation command center for the Distribution
Engine checklist in `validation-tracker.md`.

The app completes the tracker as an operating system: every phase, task,
connector, fallback, owner, blocker, and evidence requirement is represented.
It does not falsely mark live business execution complete. External-account
items remain blocked or evidence-pending until real Mailchimp/Brevo, social,
SEO, creative, analytics, Apollo, domain warmup, and audience metrics are
attached.

## Getting Started

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Routes

- `/` - command center overview
- `/channels` - connector matrix and fallback status
- `/validations` - phase-by-phase evidence tracker
- `/reports` - readiness readout and next evidence packet

## Validation

```bash
npm run lint
npm run build
```

## Fallback Docs

- `docs/manual-fallbacks.md`
- `docs/external-execution-log.md`

## Deploy on Vercel

Deploy as a preview unless explicitly promoting production:

```bash
vercel deploy . -y
```
