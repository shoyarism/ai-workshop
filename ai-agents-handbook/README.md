# AI Agents Handbook

The operational prompt suite, agent persona packs, and routing knowledge base for AI coding agents. This is the "loaded magazine": load the master prompt, route work to the skill library, and swap in persona packs as needed.

## Contents

| Path | Purpose |
|---|---|
| [`AI-AGENT-MASTER-PROMPT.md`](./AI-AGENT-MASTER-PROMPT.md) | **Entry point (v2.1.1).** Senior full-stack engineer agent rules, operational protocols, and skill routing. Load this as the system prompt. |
| [`ai-agent-suite/`](./ai-agent-suite/) | Modular companion docs (canonical master prompt + operational spec + output schemas + verification matrix + 796-skill catalog). |
| [`packs/`](./packs/README.md) | **Agent persona & config packs** — complete ready-to-drop agent configurations (skills, AGENTS.md, hooks, MCP). |
| [`references/`](./references/README.md) | **Reference collections** — awesome-lists, system prompt archives, plugin & MCP directories. |

## Packs (persona / config)

| Pack | What it is |
|---|---|
| [`packs/ponytail`](./packs/ponytail) | "Laziest senior dev" coding persona — anti-overengineering rules, 6 skills, MCP server. |
| [`packs/karpathy`](./packs/karpathy) | Andrej Karpathy-style coding guidelines as an agent skill. |
| [`packs/ecc`](./packs/ecc) | ECC agent harness performance system (skills, instincts, memory, security) for 15+ agent tools. |
| [`packs/huashu-design`](./packs/huashu-design) | HTML-native design skill for Claude Code (visual design via HTML canvases). |
| [`packs/baoyu-design`](./packs/baoyu-design) | Run "Claude Design" locally as an agent skill (Cursor, Claude Code, others). |
| [`packs/garden-skills`](./packs/garden-skills) | Web design, article, and knowledge-base skills collection. |
| [`packs/styleseed`](./packs/styleseed) | Design-method engine for Claude Code / Codex / Cursor (23 style skills + token system). |

## References

| Reference | What it is |
|---|---|
| [`references/awesome-claude-code`](./references/awesome-claude-code) | Curated resources for Claude Code (agents, skills, guides). |
| [`references/awesome-mcp-servers`](./references/awesome-mcp-servers) | Huge directory of MCP servers (punkpeye). |
| [`references/awesome-agent-skills`](./references/awesome-agent-skills) | Curated list of 1000+ agent skills (VoltAgent). |
| [`references/awesome-design-skills`](./references/awesome-design-skills) | 67+ DESIGN.md / SKILL.md design skills for agents. |
| [`references/system-prompts-of-ai-tools`](./references/system-prompts-of-ai-tools) | System prompts + models of AI tools (Augment, Claude Code, Cursor, ...). |
| [`references/chatgpt-system-prompts`](./references/chatgpt-system-prompts) | OpenAI system prompt archive (README pointer). |
| [`references/awesome-ai-system-prompts`](./references/awesome-ai-system-prompts) | System prompts from top AI tools & apps. |
| [`references/awesome-claude-code-toolkit`](./references/awesome-claude-code-toolkit) | Toolkit of agents, skills, MCPs, hooks for Claude Code. |
| [`references/claude-plugins-official`](./references/claude-plugins-official) | Anthropic's official plugins directory. |

## Related knowledge bases

- **Skills:** `skills/SKILLS_INDEX.md` (796 skills, categorized) · `skills/SOURCES.md` (provenance)
- **Prompts:** `prompts/README.md` (website-recon system prompt suite + reusable prompt templates)

## How to use

1. Load `AI-AGENT-MASTER-PROMPT.md` as the agent system prompt.
2. For a specialized persona, drop the matching `packs/<pack>` config (AGENTS.md / `.claude` / skills) into your agent project, then load the master prompt on top.
3. Match task types to skills via `ai-agent-suite/04-SKILLS-CATALOG.md` (or `skills/SKILLS_INDEX.md`) and follow the skill's `SKILL.md`.
4. Consult `ai-agent-suite/01-OPERATIONAL-SPEC.md` for edge-case execution protocols; score output against `03-VERIFICATION-MATRIX.md` before declaring done.
5. Mine `references/` when hunting for new skills, MCP servers, or system prompts to fold into the library.
