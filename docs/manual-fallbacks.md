# MarketMaster Manual Fallbacks

The validation tracker is complete as an operating system, but live connector
execution still requires real accounts and evidence. Use these fallbacks when a
connector cannot execute directly.

## Email: Mailchimp or Brevo

1. Generate the campaign subject, preview text, body, CTA, and destination URL.
2. Create the draft manually in the provider.
3. Send a test to yourself.
4. Record the provider, draft name, test recipient, and screenshot in the log.

## Social: LinkedIn, X, or Scheduler

1. Generate platform-specific post copy and link.
2. Queue in Buffer/Zapier if available, otherwise publish manually.
3. Capture the scheduled timestamp or live URL.
4. Mark the connector as pass or fallback only after the URL exists.

## SEO: Ahrefs or Semrush

1. Pull keyword, difficulty, search intent, SERP notes, and AI-citation notes from
   the paid tool when available.
2. If no paid tool is available, run manual SERP review and label the result as a
   fallback assumption.
3. Attach the query set to the pillar brief.

## Creative: Canva and Higgsfield

1. Use the generated carousel outline or short-form script as the production spec.
2. Create the asset manually if the connector is unavailable.
3. Review output quality before using it as client evidence.
4. Store export links or screenshots in the external execution log.

## Analytics: GA4 or Supermetrics

1. Pull impressions, clicks, replies, signups, and source/channel data.
2. If no connector is available, record numbers manually from platform dashboards.
3. Include screenshots or export files for every reported metric.

## Outbound: Apollo

1. Build the sequence copy and targeting criteria now.
2. Do not send until the domain has completed warmup.
3. Record warmup status, first sequence send, replies, and bounces.
