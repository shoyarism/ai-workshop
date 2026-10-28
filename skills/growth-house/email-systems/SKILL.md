---
name: email-systems
description: Email has the highest ROI of any marketing channel. $36 for every
  $1 spent. Yet most startups treat it as an afterthought - bulk blasts, no
  personalization, landing in spam folders.
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Email Systems

Email has the highest ROI of any marketing channel. $36 for every $1 spent.
Yet most startups treat it as an afterthought - bulk blasts, no personalization,
landing in spam folders.

This skill covers transactional email that works, marketing automation that
converts, deliverability that reaches inboxes, and the infrastructure decisions
that scale.

## Principles

- Transactional vs Marketing separation | Description: Transactional emails (password reset, receipts) need 100% delivery.
Marketing emails (newsletters, promos) have lower priority. Use separate
IP addresses and providers to protect transactional deliverability. | Examples: Good: Password resets via Postmark, marketing via ConvertKit | Bad: All emails through one SendGrid account
- Permission is everything | Description: Only email people who asked to hear from you. Double opt-in for marketing.
Easy unsubscribe. Clean your list ruthlessly. Bad lists destroy deliverability. | Examples: Good: Confirmed subscription + one-click unsubscribe | Bad: Scraped email list, hidden unsubscribe, bought contacts
- Deliverability is infrastructure | Description: SPF, DKIM, DMARC are not optional. Warm up new IPs. Monitor bounce rates.
Deliverability is earned through technical setup and good behavior. | Examples: Good: All DNS records configured, dedicated IP warmed for 4 weeks | Bad: Using free tier shared IP, no authentication records
- One email, one goal | Description: Each email should have exactly one purpose and one CTA. Multiple asks