# AI-Powered Lead Generation Service (Full Automation)

## Overview
Combine B2B lead extraction with AI qualification and outreach automation. The system finds leads, qualifies them via AI analysis, generates personalized outreach, and schedules follow-ups — all without human intervention until deal close.

## Startup Cost: $0–$100/mo (APIs, email service)
## Expected Monthly Revenue: $3,000–$20,000 (after 3–6 months)

---

## Tools & Skills

### Core Tools
| Tool | Purpose | Cost |
|------|---------|------|
| Apollo.io / ZoomInfo | Lead database access | Free tier – $500/mo |
| Clay.com | Data enrichment | Free tier |
| Instantly.ai / Smartlead | Email sending | Free tier – $30/mo |
| Calendly | Scheduling | Free tier |
| Google Sheets / Airtable | Lead management | Free tier |

### Workshop Skills
| Skill | Path | Purpose |
|-------|------|---------|
| google-maps-contact-extract | `skills/google-maps-contact-extract` | Business contact extraction |
| google-maps-search-api-skill | `skills/google-maps-search-api-skill` | Maps data extraction |
| prospecting | `skills/prospecting` | Lead list building |
| offers | `skills/offers` | Value proposition design |
| marketing-plan | `skills/marketing-plan` | Outreach strategy |
| business-contact-social-links-skill | `skills/business-contact-social-links-skill` | Cross-platform discovery |
| trustpilot-company-info | `skills/trustpilot-company-info` | Reputation analysis |
| browser-testing-with-devtools | `skills/browser-testing-with-devtools` | Website audit generation |

---

## Setup Steps

### Step 1: Choose Target Market
**High-value B2B segments**:
- SaaS companies needing sales help
- Marketing agencies needing clients
- E-commerce brands needing growth
- Service businesses (lawyers, accountants, consultants)
- Manufacturers needing distributors

### Step 2: Build the Lead Pipeline
```python
# Full automation pipeline
1. LEAD DISCOVERY:
   - Scrape LinkedIn company pages
   - Extract decision-maker contacts
   - Verify email addresses (NeverBounce, ZeroBounce)
   - Score leads by fit (industry, size, tech stack)

2. AI QUALIFICATION:
   - Analyze company website for pain points
   - Check recent news/funding for triggers
   - Score lead quality (1–10)
   - Tag by intent level (hot, warm, cold)

3. PERSONALIZED OUTREACH:
   - Generate custom email referencing specific trigger
   - Include relevant case studies/examples
   - A/B test subject lines and CTAs
   - Send via Instantly/Smartlead with inbox rotation

4. FOLLOW-UP SEQUENCE:
   - Day 1: Initial outreach
   - Day 3: Follow-up with additional value
   - Day 7: Case study or social proof
   - Day 14: Breakup email
   - Day 30: Re-engagement (quarterly)
```

### Step 3: Set Up Automation
```bash
# Recommended stack
- Make.com or Zapier: Workflow automation
- Clay.com: Data enrichment and lead scoring
- Instantly.ai: Cold email sending and tracking
- Calendly: Booking automation
- Stripe: Payment collection
```

### Step 4: Scale the Service
- Target: 100–500 leads per week per client
- Goal: 30–50% reply rate, 10–20% meeting booked
- Close rate: 20–30% of meetings to paid clients

---

## Workflow & Best Practices

### Daily Workflow
| Time | Task | Automation Level |
|------|------|-----------------|
| Morning (15 min) | Check lead flow, review qualified leads | Manual |
| Midday (automated) | Outreach emails sent, follow-ups queued | 100% automated |
| Afternoon (15 min) | Review replies, qualify hot leads | Manual |
| Evening (automated) | Calendar bookings, follow-up sequences | 100% automated |

### Quality Standards
- **Lead accuracy**: 90%+ email deliverability rate
- **Personalization**: Every email must reference specific company details
- **Response time**: Reply to inbound leads within 1 hour
- **Compliance**: CAN-SPAM/GDPR compliant (include unsubscribe)

### Outreach Best Practices
- Keep emails under 150 words
- Lead with value, not features
- Include social proof (logos, testimonials)
- One clear CTA per email
- Mobile-optimized format

### Warning Signs
- **Bounce rate > 10%**: Clean your list immediately
- **Spam complaints**: Review content, add unsubscribe link
- **Low reply rate**: Improve personalization, test new angles
- **Low close rate**: Refine targeting, improve sales pitch

---

## Pricing Models
| Model | Price | Best For |
|-------|-------|----------|
| Per qualified lead | $50–$200/lead | High-ticket B2B |
| Per booked meeting | $100–$500/meeting | Service businesses |
| Monthly retainer | $1,000–$5,000/mo | Ongoing lead gen |
| Performance-based | 10–20% of closed deals | Enterprise sales |

---

## Timeline to First Dollar
- **Month 1**: Setup, test with 500 leads, 0 revenue
- **Month 2**: 2,000 leads, 10–20 meetings booked ($1,000–$5,000)
- **Month 3**: 5,000 leads, 50+ meetings ($3,000–$10,000)
- **Month 6**: 15,000 leads, 150+ meetings ($8,000–$20,000)

---

## Key Metrics to Track
- Leads generated per week (target: 500–1,000)
- Email deliverability rate (target: 90%+)
- Open rate (target: 40%+)
- Reply rate (target: 10%+)
- Meeting booked rate (target: 5%+)
- Close rate (target: 20%+)
- Cost per acquisition (target: < 30% of first payment)