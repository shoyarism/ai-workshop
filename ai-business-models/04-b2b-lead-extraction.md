# Automated B2B Lead Extraction & Audit Service

## Overview
Scrape Google Maps for businesses in a niche (dentists, HVAC, lawyers). Run automated website audits (speed, SEO, mobile-friendliness). Generate PDF audit reports. Send personalized outreach emails. Close clients on fixed-fee or monthly retainer.

## Startup Cost: $0–$30/mo (SendGrid/SMTP, domain)
## Expected Monthly Revenue: $2,000–$15,000 (after 3–6 months)

---

## Tools & Skills

### Core Tools
| Tool | Purpose | Cost |
|------|---------|------|
| Google Maps API / Scraping | Business data extraction | Free tier |
| Website audit tools | SEO, speed, mobile analysis | Free tier |
| PDF generation | Audit report creation | Free (Python libraries) |
| SendGrid / SMTP | Email outreach | Free tier |
| Google Calendar | Scheduling calls | Free |
| Stripe | Payment collection | Free tier |

### Workshop Skills
| Skill | Path | Purpose |
|-------|------|---------|
| google-maps-contact-extract | `skills/google-maps-contact-extract` | Extract business contacts from Maps |
| google-maps-search-api-skill | `skills/google-maps-search-api-skill` | Search and extract business data |
| trustpilot-company-info | `skills/trustpilot-company-info` | Reputation analysis |
| business-contact-social-links-skill | `skills/business-contact-social-links-skill` | Cross-platform discovery |
| prospecting | `skills/prospecting` | Lead list building |
| offers | `skills/offers` | Value proposition design |
| marketing-plan | `skills/marketing-plan` | Outreach strategy |
| browser-testing-with-devtools | `skills/browser-testing-with-devtools` | Website audits |
| domain | `skills/domain` | Landing page design |

---

## Setup Steps

### Step 1: Choose a Niche
**High-value B2B niches**:
- Dentists / Medical clinics (high ticket services)
- HVAC / Plumbing / Electrical contractors
- Real estate agents
- Law firms (personal injury, family law)
- Boutique hotels / B&Bs
- Restaurants with good locations but poor websites

### Step 2: Build the Scraping Pipeline
```python
# Pseudo-code for automated lead extraction
1. GOOGLE MAPS SCRAPING:
   - Search for "dentist in [city]"
   - Extract: business name, address, phone, website, rating
   - Filter by rating (exclude < 4.0 stars)
   - Filter by review count (> 50 reviews)

2. WEBSITE EXTRACTION:
   - For each business, visit their website
   - Extract: contact email, social media links
   - Check if they have a contact form

3. AUDIT GENERATION:
   - Run website speed test (PageSpeed Insights API)
   - Check SEO (meta tags, H1/H2 structure)
   - Check mobile-friendliness
   - Check SSL certificate
   - Generate score: 0–100

4. REPORT GENERATION:
   - Create personalized PDF audit
   - Include: current score, issues found, improvement recommendations
   - Add CTA: "Book a free consultation"
```

### Step 3: Set Up Email Automation
```python
# Email pipeline
1. OUTREACH EMAIL TEMPLATE:
   - Subject: "{Business Name} website audit results"
   - Body: Personalized intro + audit findings + CTA
   - Attach: PDF audit report
   - Track: Open rate, click rate

2. FOLLOW-UP SEQUENCE:
   - Day 1: Initial outreach
   - Day 3: Follow-up #1
   - Day 7: Follow-up #2
   - Day 14: Breakup email

3. APPOINTMENT BOOKING:
   - Link to Calendly/Google Calendar
   - Offer free 15-minute consultation
```

### Step 4: Scale & Automate
- Target: 50–100 leads per week
- Goal: 10–20% response rate
- Close rate: 5–10% of responses
- Average deal size: $500–$2,000/month

---

## Workflow & Best Practices

### Daily Workflow
| Time | Task | Automation Level |
|------|------|-----------------|
| Morning (30 min) | Run scraping pipeline, generate reports | 100% automated |
| Midday (automated) | Send outreach emails | 100% automated |
| Afternoon (15 min) | Check responses, reply to prospects | Manual |
| Evening (automated) | Schedule follow-ups | 100% automated |

### Quality Standards
- **Lead quality**: Only target businesses with good ratings (4.0+)
- **Personalization**: Mention specific issues found on their site
- **Value-first**: Provide free audit before asking for payment
- **Professionalism**: Clean PDF reports, professional email templates

### Outreach Best Practices
- Keep emails under 150 words
- Focus on ONE specific issue (not 10)
- Include a screenshot of the problem
- Make CTA low-friction ("free audit", "quick call")
- Avoid salesy language

### Warning Signs
- **Email bounce rate > 5%**: Clean your list, use double opt-in
- **Spam complaints**: Review email content, add unsubscribe link
- **Low response rate**: Improve subject lines, personalize better
- **Low close rate**: Improve offer, provide more value upfront

---

## Timeline to First Dollar
- **Month 1**: 200 leads, 20 responses, 2 clients ($1,000–$4,000)
- **Month 2**: 400 leads, 40 responses, 4 clients ($2,000–$8,000)
- **Month 3**: 600 leads, 60 responses, 6 clients ($3,000–$12,000)
- **Month 6**: 1,000+ leads, 100+ responses, 10+ clients ($5,000–$15,000)

---

## Key Metrics to Track
- Leads generated per week (target: 50–100)
- Email open rate (target: 40%+)
- Reply rate (target: 10%+)
- Consultation booked rate (target: 5%+)
- Close rate (target: 20%+)
- Average deal size (target: $500–$2,000/month)
- Client lifetime value (target: $1,500–$6,000)