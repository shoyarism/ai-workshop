# OpenCode & Workshop Master Arsenal — Unified Reference

**Master Reference**: [`WORKSHOP_ARSENAL.md`](file:///WORKSHOP_ARSENAL.md)  
**Universal Standard**: [`WORKSHOP.md`](file:///WORKSHOP.md)  
**Universal Rules**: [`AGENTS.md`](file:///AGENTS.md) | [`CLAUDE.md`](file:///CLAUDE.md)  
**Master CLI**: `uv run python scripts/workshop.py`

---

## Centralized Quick Commands

```bash
# 👁️ Visual & Multimodal Media Inspection
python scripts/workshop.py see "<file_or_dir>" [--prompt "<question>"]
python scripts/workshop.py vision inspect "<image_path>"
python scripts/workshop.py vision storyboard "<video_path>"
python scripts/workshop.py vision ocr "<image_path>"
python scripts/workshop.py vision transcribe "<audio_or_video>"

# 🔍 Search 820+ skills, MCPs, and 1,500+ APIs
python scripts/workshop.py search "<keyword>"

# 🩺 Diagnostic health check
python scripts/workshop.py doctor

# 🌐 Live Browser Hub (Dashboard at http://localhost:7860)
python scripts/workshop.py hub --port 7860

# 🤖 Autonomous browser execution with live stream
python scripts/workshop.py browser --url "https://news.ycombinator.com" --task "Inspect top stories" --live

# 🛠️ MCP servers manager
python scripts/workshop.py mcp list
python scripts/workshop.py mcp test playwright

# 📊 Matrix status
python scripts/workshop.py status
```
