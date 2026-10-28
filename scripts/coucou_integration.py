#!/usr/bin/env python3
"""
Coucou Integration for Workshop OS
===================================
Sets up coucou hooks for Antigravity and OpenCode desktop applications.
Coucou is a notch/menubar companion that monitors AI coding agent sessions.

Repository: https://github.com/Louis-CFM/coucou
"""

from __future__ import annotations

import json
import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Any, Dict

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workshop_paths import ROOT


class CoucouIntegration:
    """Manages coucou hook integration for multiple agent desktop apps."""

    def __init__(self):
        self.system = platform.system().lower()
        self.home = Path.home()
        self.workshop_root = ROOT

    def get_coucou_paths(self) -> Dict[str, str]:
        """Get coucou hook executable and socket paths based on OS."""
        if self.system == "darwin":  # macOS
            return {
                "hook_cmd": "nb-hook",
                "socket_path": "~/Library/Application Support/NotchBuddy/nb.sock",
                "app_support": "~/Library/Application Support/NotchBuddy",
            }
        elif self.system == "windows":
            return {
                "hook_cmd": "coucou-hook.exe",
                "socket_path": r"\\.\pipe\coucou-<user-SID>",
                "app_support": r"%APPDATA%\Coucou",
            }
        else:  # Linux
            xdg_runtime = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
            return {
                "hook_cmd": "~/.local/share/coucou/bin/coucou-hook",
                "socket_path": f"{xdg_runtime}/coucou.sock",
                "app_support": "~/.local/share/coucou",
            }

    def get_antigravity_hooks_path(self) -> Path:
        """Get Antigravity hooks config path."""
        if self.system == "windows":
            local_appdata = os.environ.get("LOCALAPPDATA", "")
            return Path(local_appdata) / "gemini" / "config" / "hooks.json"
        elif self.system == "darwin":
            return self.home / ".gemini" / "config" / "hooks.json"
        else:
            return self.home / ".gemini" / "config" / "hooks.json"

    def get_opencode_hooks_path(self) -> Path:
        """Get OpenCode hooks config path."""
        if self.system == "windows":
            local_appdata = os.environ.get("LOCALAPPDATA", "")
            return Path(local_appdata) / "opencode" / "hooks.json"
        elif self.system == "darwin":
            return self.home / ".config" / "opencode" / "hooks.json"
        else:
            return self.home / ".config" / "opencode" / "hooks.json"

    def create_hook_config(self, agent_name: str, hook_cmd: str) -> Dict[str, Any]:
        """Create coucou hook configuration for an agent."""
        events = [
            "UserPromptSubmit",
            "PreToolUse",
            "PostToolUse",
            "PostToolUseFailure",
            "Notification",
            "Stop",
            "StopFailure",
            "SessionStart",
            "SessionEnd",
            "SubagentStart",
            "SubagentStop",
        ]

        hooks = {}
        for event in events:
            hooks[event] = [
                {"type": "command", "command": f"{hook_cmd} --agent {agent_name}"}
            ]

        return {"hooks": hooks, "coucou_agent": agent_name}

    def install_antigravity_hooks(self, dry_run: bool = False) -> bool:
        """Install coucou hooks for Antigravity desktop."""
        print("\n[Coucou] Installing hooks for Antigravity (agent: antigravity)...")

        hooks_path = self.get_antigravity_hooks_path()
        hooks_path.parent.mkdir(parents=True, exist_ok=True)

        coucou_paths = self.get_coucou_paths()
        hook_cmd = coucou_paths["hook_cmd"]

        config = self.create_hook_config("antigravity", hook_cmd)

        if dry_run:
            print(f"  Would write to: {hooks_path}")
            print(f"  Config: {json.dumps(config, indent=2)}")
            return True

        # Backup existing config
        if hooks_path.exists():
            backup_path = hooks_path.with_suffix(".json.bak")
            hooks_path.rename(backup_path)
            print(f"  Backed up existing config to: {backup_path}")

        hooks_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"  ✓ Installed hooks to: {hooks_path}")
        return True

    def install_opencode_hooks(self, dry_run: bool = False) -> bool:
        """Install coucou hooks for OpenCode desktop."""
        print("\n[Coucou] Installing hooks for OpenCode (agent: opencode)...")

        hooks_path = self.get_opencode_hooks_path()
        hooks_path.parent.mkdir(parents=True, exist_ok=True)

        coucou_paths = self.get_coucou_paths()
        hook_cmd = coucou_paths["hook_cmd"]

        config = self.create_hook_config("opencode", hook_cmd)

        if dry_run:
            print(f"  Would write to: {hooks_path}")
            print(f"  Config: {json.dumps(config, indent=2)}")
            return True

        if hooks_path.exists():
            backup_path = hooks_path.with_suffix(".json.bak")
            hooks_path.rename(backup_path)
            print(f"  Backed up existing config to: {backup_path}")

        hooks_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        print(f"  ✓ Installed hooks to: {hooks_path}")
        return True

    def install_all(self, dry_run: bool = False) -> bool:
        """Install coucou hooks for supported desktop apps."""
        print(f"\n{'=' * 60}")
        print("  COUCOU INTEGRATION SETUP")
        print(f"  OS: {self.system} ({platform.platform()})")
        print(f"  Workshop: {self.workshop_root}")
        print(f"{'=' * 60}")

        results = []
        results.append(self.install_antigravity_hooks(dry_run))
        results.append(self.install_opencode_hooks(dry_run))

        print(f"\n{'=' * 60}")
        if all(results):
            print("  ✓ All coucou hooks installed successfully!")
        else:
            print("  ✗ Some installations failed")
        print(f"{'=' * 60}\n")

        return all(results)

    def verify_installation(self) -> bool:
        """Verify coucou hooks are installed correctly."""
        print("\n[Coucou] Verifying installation...")

        coucou_paths = self.get_coucou_paths()
        hook_cmd = coucou_paths["hook_cmd"]

        agents = [
            ("Antigravity", "antigravity", self.get_antigravity_hooks_path()),
            ("OpenCode", "opencode", self.get_opencode_hooks_path()),
        ]

        all_ok = True
        for name, agent, path in agents:
            if path.exists():
                try:
                    config = json.loads(path.read_text(encoding="utf-8"))
                    if config.get("coucou_agent") == agent:
                        print(f"  ✓ {name}: hooks configured for '{agent}'")
                    else:
                        print(f"  ✗ {name}: invalid coucou_agent field")
                        all_ok = False
                except Exception as e:
                    print(f"  ✗ {name}: failed to parse config - {e}")
                    all_ok = False
            else:
                print(f"  ✗ {name}: hooks config not found at {path}")
                all_ok = False

        # Check if coucou hook executable exists
        try:
            if self.system == "windows":
                result = subprocess.run(
                    ["where", hook_cmd], capture_output=True, text=True
                )
            else:
                result = subprocess.run(
                    ["which", hook_cmd], capture_output=True, text=True
                )

            if result.returncode == 0:
                print(f"  ✓ coucou hook executable found: {hook_cmd}")
            else:
                print(f"  ⚠ coucou hook executable NOT found: {hook_cmd}")
                print("     Install coucou first: https://github.com/Louis-CFM/coucou")
                all_ok = False
        except Exception:
            print("  ⚠ Could not verify coucou hook executable")
            all_ok = False

        return all_ok

    def generate_claude_md_section(self) -> str:
        """Generate CLAUDE.md section for coucou integration."""
        coucou_paths = self.get_coucou_paths()

        return f"""## Coucou Integration (AI Agent Session Monitor)

Coucou (Mochi) lives in your menu bar/notch and shows live AI agent sessions.
Approve permissions, watch agents work, chat with Claude — all from the notch.

### Installed Hooks
- **Antigravity** (agent: `antigravity`) → `{self.get_antigravity_hooks_path()}`
- **OpenCode** (agent: `opencode`) → `{self.get_opencode_hooks_path()}`

### Hook Command
```bash
# {self.system.title()}
{coucou_paths["hook_cmd"]} --agent <agent-name> <EventName>
```

### Socket Path
- **macOS (GitHub build)**: `~/Library/Application Support/NotchBuddy/nb.sock`
- **macOS (App Store)**: `~/Library/Containers/fr.louisraille.Coucou/Data/nb.sock`
- **Windows**: `\\\\.\\pipe\\coucou-<user-SID>`
- **Linux**: `$XDG_RUNTIME_DIR/coucou.sock`

### Quick Test
```bash
echo '{{\"hook_event_name\":\"UserPromptSubmit\",\"session_id\":\"t1\",\"prompt\":\"hello\",\"coucou_agent\":\"demo\"}}' \\
  | {coucou_paths["hook_cmd"]} --agent demo
```

### Resources
- Repository: https://github.com/Louis-CFM/coucou
- Website: https://louis-cfm.github.io/coucou/
- iPhone App: TestFlight beta available
"""


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Coucou Integration for Workshop OS")
    parser.add_argument(
        "command",
        choices=["install", "verify", "dry-run", "claude-md"],
        help="Command to execute",
    )
    parser.add_argument(
        "--agent",
        choices=["antigravity", "opencode", "all"],
        default="all",
        help="Specific agent to configure",
    )

    args = parser.parse_args()

    integration = CoucouIntegration()

    if args.command == "dry-run":
        integration.install_all(dry_run=True)
    elif args.command == "install":
        if args.agent == "all":
            integration.install_all()
        elif args.agent == "antigravity":
            integration.install_antigravity_hooks()
        elif args.agent == "opencode":
            integration.install_opencode_hooks()
    elif args.command == "verify":
        integration.verify_installation()
    elif args.command == "claude-md":
        print(integration.generate_claude_md_section())


if __name__ == "__main__":
    main()
