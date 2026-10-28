# The 14-Bot AI Company — Hermes Bot Team

A team of 14 Hermes **bots** (profiles) that build products and make revenue. Each bot has its own persona (ported from `auto-company/.claude/agents/*.md` + a Hermes team-operating frame in its `SOUL.md`). They share **one model**, **one kanban board**, and **one group chat**.

- **Model (all bots):** `auto/best-reasoning` via OmniRoute gateway `http://127.0.0.1:20128/v1` (re-pin any bot: `hermes -p <handle> config set model.default <model>`).
- **Profiles:** `C:\Users\TRIAL\AppData\Local\hermes\profiles\<handle>\`
- **Personas:** ported verbatim from your `auto-company` agent files; the team frame (language, guardrails, coordination) is added fresh.

## Roster

| Bot (handle) | Persona | Role | Layer | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `ceo` | Bezos · CEO — Strategy & Priorities | Strategy & Priorities | Strategy | `docs/ceo/` |
| `cto` | Vogels · CTO — Architecture & Reliability | Architecture & Tech Selection | Strategy | `docs/cto/` |
| `critic` | Munger · Critic — Inversion & Pre-Mortem | Inversion & Pre-Mortem | Strategy | `docs/critic/` |
| `product` | Norman · Product — UX & Usability | Product & Usability | Product | `docs/product/` |
| `ui` | Duarte · UI — Visual Design & Design System | Visual Design & Design System | Product | `docs/ui/` |
| `interaction` | Cooper · Interaction — Flows & Personas | Interaction & Flows | Product | `docs/interaction/` |
| `fullstack` | DHH · Full-Stack — Implementation & Dev Workflow | Implementation | Engineering | `docs/fullstack/` |
| `qa` | Bach · QA — Test Strategy & Quality | Testing & Quality | Engineering | `docs/qa/` |
| `devops` | Hightower · DevOps — CI/CD & Ops | CI/CD & Infrastructure | Engineering | `docs/devops/` |
| `marketing` | Godin · Marketing — Positioning & Brand | Positioning & Brand | Business | `docs/marketing/` |
| `ops` | Graham · Operations — Growth & Retention | Growth & Retention | Business | `docs/ops/` |
| `sales` | Ross · Sales — Funnel & Conversion | Pricing & Conversion | Business | `docs/sales/` |
| `cfo` | Campbell · CFO — Pricing & Unit Economics | Financials & Unit Economics | Business | `docs/cfo/` |
| `research` | Thompson · Research — Market & Competitive | Market & Competitive Research | Intelligence | `docs/research/` |

## Talk to one bot
```powershell
hermes -p critic chat -q "Inversion review this plan: <paste>"   # in its persona
# each bot also has a launcher:  C:\Users\TRIAL\.local\bin\<handle>.bat
```

## Convene the team on a task
Two ways — see `CONVENE.md` for the copy-paste orchestrator prompt.
1. **Kanban** (async, parallel): an orchestrator bot decomposes the task into tasks on the shared board, each `assignee` = the right handle. The kanban orchestrator routes by role (each profile's description says what it does). Workers run, hand off, and the orchestrator consolidates.
2. **Group chat** (synchronous deliberation): in the desktop **Bots** tab, create a group, add the 14 bots, post the task; bots speak in character and @mention each other; founder decides.

## The 6 team workflows (from auto-company)
- **New Product Evaluation**: `research` → `ceo` → `critic` → `product` → `cto` → `cfo`
- **Feature Development**: `interaction` → `ui` → `fullstack` → `qa` → `devops`
- **Product Launch**: `qa` → `devops` → `marketing` → `sales` → `ops` → `ceo`
- **Pricing & Monetization**: `research` → `cfo` → `sales` → `critic` → `ceo`
- **Weekly Review**: `ops` → `sales` → `cfo` → `qa` → `ceo`
- **Opportunity Discovery**: `research` → `ceo` → `critic` → `cfo`

## Safety guardrails (all bots, non-negotiable)
- No destructive git on shared branches; no deleting repos/projects/system files; no force-push to protected branches; no implicit publishing; never leak credentials to public repos/logs. Bots flag and ask before destructive/irreversible actions.
- Founder is the final decision-maker; `critic` may veto but not delay indefinitely; `ceo` breaks ties.
