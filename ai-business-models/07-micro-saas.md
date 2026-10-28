# Micro-SaaS (AI Wrapper) on Vercel

## Overview
Build a single-purpose AI tool (e.g., "AI Resume Tailor", "Contract Risk Analyzer", "E-commerce Image Enhancer"). Host on Vercel (free tier). Use Stripe for billing (free tier). Build programmatic SEO pages for organic traffic.

## Startup Cost: $0–$50/mo (Vercel Pro, custom domain, Stripe fees)
## Expected Monthly Revenue: $1,000–$25,000+ (after 6–12 months)

---

## Tools & Skills

### Core Tools
| Tool | Purpose | Cost |
|------|---------|------|
| Next.js / React | Frontend framework | Free |
| OpenRouter / Claude API | AI backend | Pay-per-use |
| Vercel | Hosting | Free tier |
| Stripe | Billing | Free tier (2.9% + 30¢ per transaction) |
| Neon / Supabase | Database | Free tier |
| Vercel Analytics | Usage tracking | Free |

### Workshop Skills
| Skill | Path | Purpose |
|-------|------|---------|
| deploy-to-vercel | `skills/deploy-to-vercel` | Zero-friction deployment |
| vercel-composition-patterns | `skills/vercel-composition-patterns` | React best practices |
| using-neon | `skills/using-neon` | Serverless PostgreSQL |
| convex-suggest | `skills/convex-suggest` | Reactive backend patterns |
| landing-page-design | `skills/landing-page-design` | High-converting UI |
| uiux-designer | `skills/uiux-designer` | Product design |
| directory-submissions | `skills/directory-submissions` | Product discovery |
| marketing-ideas | `skills/marketing-ideas` | Growth strategies |
| browser-extension-builder | `skills/browser-extension-builder` | Chrome extension packaging |
| api-scout | `skills/api-scout` | Find free APIs and tools |

---

## Setup Steps

### Step 1: Choose a Niche Tool
**High-demand micro-SaaS ideas**:
- **Resume Tailor**: Optimizes resumes for ATS systems
- **Contract Reviewer**: Analyzes contracts for risks
- **Image Enhancer**: Upscales/edits product photos
- **Email Writer**: Generates professional emails
- **Landing Page Generator**: Creates conversion-optimized pages
- **Data Scraper**: Extracts data from websites
- **PDF Converter**: Converts between formats
- **Code Reviewer**: Analyzes code quality and suggests improvements

### Step 2: Set Up the Tech Stack
```bash
# Initialize Next.js project
npx create-next-app@latest my-saas --typescript --tailwind

# Install dependencies
npm install stripe @stripe/stripe-js
npm install @supabase/supabase-js
npm install openai # or claude

# Deploy to Vercel
vercel --prod
```

### Step 3: Build the Core Features
```python
# Core architecture
1. FRONTEND:
   - Simple UI: Upload/input → Process → Download/output
   - Landing page with pricing table
   - Dashboard for paid users

2. BACKEND (API Routes):
   - /api/process: Handle user input, call AI model
   - /api/payment: Create Stripe checkout session
   - /api/webhook: Handle Stripe events (subscription updates)

3. DATABASE:
   - Store user data, subscription status, usage limits
   - Track API call history for billing

4. AI INTEGRATION:
   - Use OpenRouter for multiple model access
   - Implement rate limiting and cost controls
   - Add fallback models for reliability
```

### Step 4: Programmatic SEO Pages
```python
# Generate thousands of landing pages automatically
1. IDENTIFY KEYWORD PATTERNS:
   - "best ai tool for [industry]"
   - "how to [task] with ai"
   - "[tool] alternatives"
   - "[tool] vs [competitor]"

2. AUTOMATED GENERATION:
   - Create template pages with dynamic content
   - Include user-generated content (reviews, use cases)
   - Optimize each page for specific keywords

3. INTERLINKING:
   - Link related pages together
   - Create hub pages for each topic cluster
```

### Step 5: Launch & Marketing
1. Submit to Product Hunt, alternative.to, futurepedia.io
2. Create comparison pages targeting competitor keywords
3. Write guest posts on industry blogs
4. Build email waitlist before launch

---

## Workflow & Best Practices

### Daily Workflow
| Time | Task | Automation Level |
|------|------|-----------------|
| Morning (15 min) | Check analytics, user feedback, bugs | Manual |
| Midday (automated) | Process API calls, serve users | 100% automated |
| Afternoon (15 min) | Review metrics, plan next feature | Manual |
| Evening (automated) | Scale infrastructure, backups | 100% automated |

### Product-Market Fit Validation
- **Pre-launch**: Build waitlist, validate with 5–10 target users
- **Post-launch**: Monitor activation rate (> 30% is good)
- **Retention**: Target 7-day retention > 40%
- **Revenue**: Target < $50 CAC, > $100 LTV

### Pricing Strategy
- **Freemium**: Free tier with usage limits, paid tiers start at $9–$29/mo
- **Pay-per-use**: Charge per API call or output (good for variable usage)
- **Annual discount**: Offer 20% off for annual billing (improves cash flow)

### Warning Signs
- **High churn**: Fix onboarding, add more features, improve UX
- **Low activation**: Simplify the interface, add tutorials
- **High CAC**: Improve SEO, build community, get referrals
- **API costs exceeding revenue**: Optimize prompts, add rate limits, raise prices

---

## Timeline to First Dollar
- **Month 1**: Launch MVP, 0–10 users ($0)
- **Month 2**: 10–50 users, 1–5 paying ($100–$500)
- **Month 3**: 50–100 users, 10–20 paying ($1,000–$2,000)
- **Month 6**: 200+ users, 50+ paying ($5,000–$10,000)
- **Month 12**: 500+ users, 100+ paying ($10,000–$25,000)

---

## Key Metrics to Track
- Monthly Active Users (MAU)
- Activation rate (target: > 30%)
- Conversion rate to paid (target: 5–10%)
- Monthly Recurring Revenue (MRR)
- Churn rate (target: < 5%)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Net Promoter Score (NPS)
- API usage per user