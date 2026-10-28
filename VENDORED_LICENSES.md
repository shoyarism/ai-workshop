# 📜 Vendored Licenses & Upstream Attribution

Workshop OS is an integrated orchestration environment that organizes and indexes open-source skills, playbooks, and tooling. 

While the core Workshop OS runtime, Slop Court tribunal, CLI tooling, and orchestration architecture are licensed under the **Apache License, Version 2.0** (see [LICENSE](LICENSE)), individual vendored skill packs and upstream runbooks preserve their original open-source licenses as granted by their respective authors.

All vendored components use permissive open-source licenses (MIT, Apache-2.0, BSD-3-Clause) compatible with the root project license.

---

## 🏛️ Upstream Skill Packs & Repositories

| Component / Subsystem | Directory | Upstream License | Description & Attribution |
| :--- | :--- | :---: | :--- |
| **Community Cybersecurity Skills** | `skills/security-house/anthropic-cybersecurity-skills/` | **Apache-2.0** | Defensive security, threat modeling, and forensic response runbooks. Authored by independent open-source cybersecurity contributors (community project inspired by Claude security guidelines; not officially authored, sponsored, or endorsed by Anthropic, PBC). |
| **Baoyu Design** | `skills/design-house/baoyu-design/` | **MIT** | PPTX presentation, visual design, and video layout engine. Authored by Baoyu (@baoyu9936). |
| **Everything Claude Code (ECC)** | `skills/dev-house/ecc/` | **MIT** | Senior engineering, architecture patterns, and TDD runbooks. Authored by the ECC community. |
| **StyleSeed** | `skills/design-house/styleseed/` | **MIT** | Design tokens, design systems, and visual styling presets. Authored by the StyleSeed project. |
| **Garden Skills** | `skills/dev-house/garden-skills/` | **MIT** | Bot, web, and development automation playbooks. Authored by the Garden project. |
| **Huashu Design** | `skills/design-house/huashu-design/` | **MIT** | Graphic layouts, aesthetic templates, and visual composition. Authored by Huashu. |
| **PinchTab** | `skills/cloud-and-apis/pinchtab/` | **Apache-2.0** | Browser automation and headless browser agent connectors. Authored by the PinchTab contributors. |
| **Hackingtool** | `skills/ops-house/hackingtool/` | **MIT** | Security penetration testing toolkit reference. Authored by Z4nzu. |
| **OpenMontage & Remotion** | `skills/media-house/` | **MIT** | Programmatic video generation and motion design runbooks. Authored by the Remotion & OpenMontage communities. |
| **Office & Document Toolkits (PDF, XLSX, DOCX)** | `skills/cloud-and-apis/`, `skills/growth-house/` | **MIT** | Parsers and generators for spreadsheets, documents, and PDF reporting. Authored by respective open-source tool authors. |
| **Modern UI & Theme Factory** | `skills/design-house/` | **MIT** | Frontend styling, brand guidelines, and canvas design utilities. Authored by open-source UI design contributors. |
| **Ponytail & Styleseed Handbook Packs** | `ai agents handbook/packs/` | **MIT** | Curated workflow runbooks, dev templates, and generative prompt presets. |

---

## ⚖️ License Verification & Invariant

Every vendored subdirectory contains a copy of its original license text (845+ `LICENSE` / `LICENSE.txt` files retained across vendored packs). When modifying or updating upstream skills, maintainers must preserve upstream copyright notices and license headers.
