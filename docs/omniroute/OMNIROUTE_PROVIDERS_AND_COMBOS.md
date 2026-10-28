# OmniRoute - Official Built-In Auto-Routing Templates & Providers Master Reference

*Source Database:* `~/.omniroute/storage.sqlite`  
*Last Exported & Updated:* `2026-09-02 12:15:19`  
*Total Configured Providers:* **48**  
*Total Account Connections:* **101** (**67 Active**, **34 Standby**)  
*Routing Mode:* **100% Zero-Config Dynamic Auto-Routing Catalog (17 Official Built-In Templates)**  

---

## Table of Contents

- [1. Auto-Routing Catalog (17 Built-In Templates)](#1-auto-routing-catalog-17-built-in-templates)
- [2. Configured AI Providers & Accounts](#2-configured-ai-providers--accounts)
- [3. Quick Import & Restore Instructions](#3-quick-import--restore-instructions)

---

## 1. Auto-Routing Catalog (17 Built-In Templates)

Built-in `auto/*` combos are resolved dynamically in real-time from all connected, active, and healthy providers.

| Model ID / Route | Display Name | Strategy | Categories | Tiers | Key Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`auto/best-coding`** | Best Coding | `WEIGHTED` | `coding` | `premium`, `balanced` | High-quality coding assistant across connected premium/balanced coding models. |
| **`auto/best-reasoning`** | Best Reasoning | `WEIGHTED` | `reasoning_deep`, `reasoning` | `premium` | Deep multi-step reasoning and architecture planning across high-intelligence models. |
| **`auto/best-fast`** | Best Fast | `WEIGHTED` | `fast` | `fast`, `balanced` | Ultra-low latency responses (<2s) with balanced accuracy for autocomplete. |
| **`auto/best-vision`** | Best Vision | `WEIGHTED` | `vision` | `premium`, `balanced` | Image understanding, UI inspection, diagram analysis, and multimodal reasoning. |
| **`auto/best-chat`** | Best Chat | `WEIGHTED` | `chat` | `balanced`, `premium` | Natural conversational responses for pair programming and Q&A. |
| **`auto/best-coding-fast`** | Best Coding Fast | `WEIGHTED` | `coding`, `fast` | `fast`, `balanced` | Fast code generation with quick turnaround for edits and tests. |
| **`auto/pro-coding`** | Pro Coding | `PRIORITY` | `coding` | `premium` | Top-tier premium coding models with strict priority cascade. |
| **`auto/pro-reasoning`** | Pro Reasoning | `PRIORITY` | `reasoning_deep` | `premium` | Strict priority cascade for deep reasoning problems. |
| **`auto/pro-vision`** | Pro Vision | `PRIORITY` | `vision` | `premium` | Strict priority cascade for high-resolution image analysis. |
| **`auto/pro-chat`** | Pro Chat | `PRIORITY` | `chat` | `premium` | Priority routing across premium conversational models. |
| **`auto/pro-fast`** | Pro Fast | `PRIORITY` | `fast` | `fast` | Priority routing for sub-second responses. |
| **`auto/coding`** | Coding | `WEIGHTED` | `coding` | `balanced`, `fast`, `premium` | Broad-spectrum coding router spanning all active coding endpoints. |
| **`auto/fast`** | Fast | `WEIGHTED` | `fast` | `fast` | General fast routing pool. |
| **`auto/chat`** | Chat | `WEIGHTED` | `chat` | `balanced`, `fast` | Balanced conversational model pool. |
| **`auto/claude-opus`** | Claude Opus | `PRIORITY` | `reasoning_deep`, `coding`, `reasoning` | `premium` | Priority cascade targeting Claude Opus / deep thinking compatible endpoints. |
| **`auto/claude-sonnet`** | Claude Sonnet | `PRIORITY` | `coding`, `reasoning`, `chat` | `premium`, `balanced` | Priority cascade targeting Claude Sonnet compatible endpoints. |
| **`auto/best-free`** | Best Free | `WEIGHTED` | `coding`, `chat`, `fast` | `free` | Zero-cost router selecting only 100% free-tier active models. |

---

## 2. Configured AI Providers & Accounts

### Provider: `AGNES` (5 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Key 5** | `apikey` | Active | `active` | 1 | `d0402978-ebb5-49a0-984d-bde4c30d42d2` |
| **Key 4** | `apikey` | Active | `active` | 2 | `8c6b95be-9111-4377-b8c5-792ac91f66c3` |
| **Key 3** | `apikey` | Active | `active` | 3 | `0c6c505a-f350-4183-aeee-9a5f7b5fb873` |
| **Key 2** | `apikey` | Active | `active` | 4 | `f0bc3175-4493-44f8-b848-769fdf7a9c71` |
| **Key 1** | `apikey` | Active | `active` | 5 | `480a0c30-d9e6-464e-92a1-608068679984` |

### Provider: `AION` (5 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Key 5** | `apikey` | Active | `active` | 1 | `b7f1d8c8-65b7-426e-b390-9fa338eb7984` |
| **Key 4** | `apikey` | Active | `active` | 2 | `19a6b208-7116-4330-832a-da0135552e3f` |
| **Key 3** | `apikey` | Active | `active` | 3 | `21041961-0b3f-45ec-88cf-8567f3d73c7a` |
| **Key 2** | `apikey` | Active | `active` | 4 | `b986ea9e-4eae-4232-8528-49ec492907a1` |
| **Key 1** | `apikey` | Active | `active` | 5 | `418e9f4e-0329-4db4-8b9c-da86e1b7bfa0` |

### Provider: `ANTHROPIC` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `8884e9be-31ab-4149-8ab6-39d1f32472b2` |

### Provider: `API-AIRFORCE` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `a5058c4c-f54e-4696-a138-ec9c27ac7e83` |

### Provider: `BAZAARLINK` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `9198cfbe-106e-4222-88e9-32e1b52ba1a6` |

### Provider: `BYTEPLUS` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `8f15f957-c5c8-4b94-ac15-8f6f80d9af3b` |

### Provider: `CEREBRAS` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `438c8072-2fbe-41b8-af69-24691e884116` |

### Provider: `CHUTES` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `f6af7c27-0944-4f8b-bedd-11157e364c19` |

### Provider: `CLINE` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **voruebergehend.past@gmail.com** | `oauth` | Active | `active` | 1 | `614f3341-a5cc-4f81-a91c-12445d6ac1fc` |

### Provider: `CLINEPASS` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **voruebergehend.past@gmail.com** | `oauth` | Standby | `active` | 1 | `9b123657-6e9e-48b9-be14-ec35fa51de88` |

### Provider: `CLOUDFLARE-AI` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Standby | `active` | 1 | `410d74ac-4781-48fc-a985-3b756f4b6644` |

### Provider: `CODEBUDDY-INTL` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Account 1** | `oauth` | Active | `error` | 1 | `79e985d8-8ef7-4cff-a625-51b82cc3662a` |

### Provider: `CODEX` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ariya.digitalmarketing.rsuimb@gmail.com** | `oauth` | Active | `active` | 1 | `fefd702e-1ffe-4576-834c-68f1da4b44db` |

### Provider: `COHERE` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `13f8dd12-0c5f-4dbc-a3e8-4598ce9720c9` |

### Provider: `COMMANDCODE` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `error` | 1 | `d46190f4-82f6-4b1b-b2e4-86d9f0731974` |

### Provider: `DEEPSEEK` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `774e8932-999c-4d5b-85be-8cbb69563b74` |

### Provider: `EXA-SEARCH` (4 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Key 4** | `apikey` | Active | `active` | 1 | `a7df7138-1542-4e46-8ab4-77a1b63d64e3` |
| **Key 3** | `apikey` | Active | `active` | 2 | `38d99202-d404-4693-accd-b18eead577a1` |
| **Key 2** | `apikey` | Active | `active` | 3 | `87e6ff26-1a4a-4083-a4a0-28748bff178d` |
| **Key 1** | `apikey` | Active | `active` | 4 | `90bca7fb-5d96-4ebf-ab11-01b19055e97c` |

### Provider: `FIRECRAWL` (5 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `apikey` | Active | `error` | 1 | `3f16bf88-363a-485c-82df-048406a263a5` |
| **2** | `apikey` | Active | `active` | 1 | `6facbe7c-650f-4ba0-bf71-054a0a88027d` |
| **3** | `apikey` | Active | `active` | 1 | `5c375215-fed5-4446-86bf-f1573018d464` |
| **4** | `apikey` | Active | `active` | 1 | `f8be5e35-f7f3-4e06-a2b0-f6cbc1bff43f` |
| **Key 1** | `apikey` | Active | `active` | 5 | `d9d2fb40-d2a3-4a6e-b98b-b9a7819daa14` |

### Provider: `GEMINI` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `cbb582a5-32b4-438b-84e6-de9e93352029` |

### Provider: `GEMINI-CLI` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ariya.digitalmarketing.rsuimb@gmail.com** | `oauth` | Active | `error` | 1 | `836e8239-805f-48e5-9381-b08e6135aa59` |

### Provider: `GITHUB` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Voruebergehend** | `oauth` | Standby | `active` | 1 | `f45f5ac4-89b3-49a8-80a4-51481c30f385` |

### Provider: `GROK-CLI` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ariya.digitalmarketing.rsuimb@gmail.com** | `oauth` | Standby | `error` | 1 | `36a3c3e9-dc72-4ed7-a7c5-b31aa527c8d8` |

### Provider: `GROQ` (2 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main2** | `apikey` | Active | `active` | 1 | `47adf355-655e-4460-b26d-3fb0ed3ca84f` |
| **main** | `apikey` | Active | `active` | 2 | `730cd4cc-da02-491e-878a-ad5909e50b6c` |

### Provider: `HYPERBOLIC` (3 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main3** | `apikey` | Active | `active` | 1 | `e874f979-86b4-4514-89bb-595847d84e10` |
| **main2** | `apikey` | Active | `active` | 2 | `7b479bed-4f81-48e6-b5d1-e7242b441d9e` |
| **main** | `apikey` | Active | `active` | 3 | `6773f295-0a2b-4a3c-a354-1392d97cb81c` |

### Provider: `KILO-GATEWAY` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `4cd8d38f-6855-4915-bcad-a763922e0557` |

### Provider: `KILOCODE` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ariya.digitalmarketing.rsuimb@gmail.com** | `oauth` | Active | `active` | 1 | `2164559b-0084-47c9-b211-a34acf72283f` |

### Provider: `KIMCHI` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **voruebergehend.past@gmail.com** | `oauth` | Active | `error` | 1 | `53a94f87-7df2-4596-ae3b-9ce03e495b25` |

### Provider: `KIMI` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Account 1** | `oauth` | Active | `error` | 1 | `62a7215b-2226-4356-af6a-0f826beae9f0` |

### Provider: `KIRO` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Account 1** | `oauth` | Standby | `active` | 1 | `d0471cbf-ef5a-4aba-acdf-3b227d783070` |

### Provider: `LLM7` (2 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main2** | `apikey` | Active | `active` | 1 | `0130dec8-d4db-4447-816e-c120c3d2113b` |
| **main** | `apikey` | Active | `active` | 2 | `26855981-25ac-4836-ad46-8110dd64f660` |

### Provider: `MISTRAL` (3 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main3** | `apikey` | Active | `active` | 1 | `b55e54f9-b323-4dca-a792-aba48eaf2586` |
| **main2** | `apikey` | Active | `active` | 2 | `9a7df3a9-eded-4e31-a8e7-7d6a630d1c27` |
| **main** | `apikey` | Active | `active` | 3 | `1c1532fd-4868-401e-b7ac-4ee86d91efba` |

### Provider: `MORPH` (4 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main4** | `apikey` | Standby | `active` | 1 | `697d954f-9f34-4655-a3bc-e769b0267724` |
| **main3** | `apikey` | Standby | `active` | 2 | `1eb0b790-f7ad-4b25-a84e-e89135b862c5` |
| **main2** | `apikey` | Standby | `active` | 3 | `638e15e4-d9ca-4543-b5e0-e8645ccc340f` |
| **main** | `apikey` | Standby | `active` | 4 | `ed9c7dd6-c85b-476f-a278-b532f7fe0a7a` |

### Provider: `NVIDIA` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `7a196c7b-8a68-49ae-91b5-c2e8d1073ab7` |

### Provider: `OLLAMA` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `error` | 1 | `44c1d0c5-227f-4f38-9b9e-ac1bb3683bd9` |

### Provider: `OPENAI` (4 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main4** | `apikey` | Standby | `active` | 1 | `732d9713-f4b2-417f-89c9-98cc23b035c4` |
| **main3** | `apikey` | Standby | `active` | 2 | `e7e30c00-a263-4563-80a8-dd88bdf2b1ee` |
| **main2** | `apikey` | Standby | `active` | 3 | `6bd6d341-6d2e-4605-a7fd-fde9784fc037` |
| **main** | `apikey` | Standby | `active` | 4 | `e6f0b631-9315-44d9-a07e-338e552c4cb0` |

### Provider: `OPENCODE-GO` (6 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main6** | `apikey` | Standby | `active` | 1 | `a6f1ded1-d105-46dc-ac44-7bab82d2cde7` |
| **main5** | `apikey` | Standby | `active` | 2 | `c7cd9164-2c35-4287-b6ac-c6962b2b1ab7` |
| **main4** | `apikey` | Standby | `active` | 3 | `c7aaf933-9471-48f1-ac4e-edbc58c63487` |
| **main3** | `apikey` | Standby | `active` | 4 | `b4c28511-a597-4c82-b791-2ec82fca48e5` |
| **main2** | `apikey` | Standby | `active` | 5 | `57d50f06-13b2-483f-97fa-6f2c5a9642a5` |
| **main** | `apikey` | Standby | `active` | 6 | `8e040ee1-bc9d-4519-9ff0-291ae50ce3f5` |

### Provider: `OPENROUTER` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `dc21bd7d-e356-465e-82c7-556f6505d1cc` |

### Provider: `PERPLEXITY-AGENT` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `error` | 1 | `bcc9637e-a7cd-4d5a-92e5-d864145a2ba1` |

### Provider: `POOLSIDE` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `error` | 1 | `34acb9d4-f2f3-44de-9f0f-043d5c5e4d11` |

### Provider: `SILICONFLOW` (3 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main3** | `apikey` | Active | `active` | 1 | `e1874d1d-5227-40f0-9c9c-dcf29b9dfcf8` |
| **main2** | `apikey` | Active | `active` | 2 | `710c937a-2fd0-41fe-a5ec-ab64442fed03` |
| **main1** | `apikey` | Active | `active` | 3 | `5d58f829-4c04-467c-97ea-803c111df7ac` |

### Provider: `TOGETHER` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Standby | `error` | 1 | `d0f7297d-5eca-4665-8ac6-8bbbfbe5f49a` |

### Provider: `TOKENROUTER` (4 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main4** | `apikey` | Active | `active` | 1 | `75bf89a6-5560-4b6b-8a06-b014f3897d23` |
| **main3** | `apikey` | Active | `active` | 2 | `60bd433d-3124-45d4-8cee-5b39fec6fca2` |
| **main2** | `apikey` | Active | `active` | 3 | `40e0e1c5-e693-46d4-b0ad-8fadc3ac25c9` |
| **main1** | `apikey` | Active | `active` | 4 | `eca74840-3d1d-4c0c-89c6-b1fa91d41fe3` |

### Provider: `TRAE` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Voruebergehend** | `oauth` | Active | `error` | 1 | `f4615dfa-2300-4df2-8a01-392562cf7b11` |

### Provider: `VENICE` (3 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main3** | `apikey` | Active | `active` | 1 | `42551d29-4a73-4132-85ce-b466d4b74161` |
| **main2** | `apikey` | Active | `active` | 2 | `97c3a84b-1c7b-4589-8529-1fd805c0931b` |
| **main1** | `apikey` | Active | `active` | 3 | `8f3d3333-083d-46a7-98fb-3e47c679b7bf` |

### Provider: `VERCEL-AI-GATEWAY` (3 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Key 3** | `apikey` | Active | `active` | 1 | `95795d32-316d-46ac-8416-e0be9cb7a0e6` |
| **Key 2** | `apikey` | Active | `active` | 2 | `ff424a51-0ecc-46e9-bf61-57a9ad6bf04b` |
| **Key 1** | `apikey` | Active | `active` | 3 | `8fa12f56-f759-462b-9612-ca749c2b7011` |

### Provider: `VERTEX-PARTNER` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **main** | `apikey` | Active | `active` | 1 | `ae62a5d9-32f5-4b39-bf7d-9928e9487be1` |

### Provider: `XAI` (1 connection)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ariya.digitalmarketing.rsuimb@gmail.com** | `oauth` | Standby | `error` | 1 | `addf778a-a290-4459-9535-26b49d2292da` |

### Provider: `XIAOMI-MIMO` (13 connections)

| Account / Name | Auth Method | Status | Health Status | Priority | ID |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Key 12** | `apikey` | Standby | `active` | 1 | `b008ea4a-1719-4140-ab40-d355adff8b9f` |
| **Key 11** | `apikey` | Standby | `active` | 2 | `1091ad74-d6a1-4ae0-a920-d6c51f25700e` |
| **Key 10** | `apikey` | Standby | `active` | 3 | `dc39aea7-c69d-4e23-bf5e-3c8be3fbec1e` |
| **Key 9** | `apikey` | Standby | `active` | 4 | `9a591a45-1873-4ccc-a5bf-ec3847915013` |
| **Key 8** | `apikey` | Standby | `active` | 5 | `a3de320f-ab2c-4eca-a9fd-6345ec4cd2af` |
| **Key 7** | `apikey` | Standby | `active` | 6 | `5a81d412-6d0b-4d93-912c-400c855975e5` |
| **Key 6** | `apikey` | Standby | `active` | 7 | `cd96c9d0-4a4e-4c94-b154-6444263ec3d4` |
| **Key 5** | `apikey` | Standby | `active` | 8 | `15450895-0dce-4d72-a51f-c37d5b708cec` |
| **Key 4** | `apikey` | Standby | `active` | 9 | `2bbddff3-f345-42cb-9c59-5bac4ecb6af3` |
| **Key 3** | `apikey` | Standby | `active` | 10 | `171cc688-8448-4d00-917b-b018cc313a0f` |
| **Key 2** | `apikey` | Standby | `active` | 11 | `95e94340-68fa-4713-9188-082bb7b0c2d8` |
| **Key 1** | `apikey` | Standby | `error` | 12 | `dd649bc2-c177-4dcd-b25e-8ec1853aa76a` |
| **main1** | `apikey` | Standby | `error` | 13 | `2d4247e7-dfec-462f-9269-a5d0c76e2b32` |

---

## 3. Quick Import & Restore Instructions

To import these settings on any device:

```powershell
# Run standalone import
& '.\Backup\omniroute\Import-OmniRoute.ps1'
```
