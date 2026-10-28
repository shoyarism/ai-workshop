import asyncio
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workshop_paths import ROOT, SCRIPTS, python_executable

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def inspect_server(args: list[str]) -> list[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["WORKSHOP_ROOT"] = str(ROOT)
    
    server_params = StdioServerParameters(
        command=str(python_executable()),
        args=[str(SCRIPTS / "workshop_mcp.py")] + args,
        env=env,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            return sorted([t.name for t in tools_result.tools])

async def main():
    print("=" * 70)
    print(" 🛡️ TESTING DUAL MCP SERVER ARCHITECTURE (FULL VS READ-ONLY)")
    print("=" * 70)

    # 1. Full Mode
    full_tools = await inspect_server([])
    print(f"\n[1. Full Server ('workshop') - Tool Count: {len(full_tools)}]")
    for t in full_tools:
        print(f"  + {t}")
    assert "verify" in full_tools, "Full server missing verify"
    assert "memory_write" in full_tools, "Full server missing memory_write"
    assert "critique" in full_tools, "Full server missing critique"

    # 2. Read-Only Mode
    ro_tools = await inspect_server(["--read-only"])
    print(f"\n[2. Read-Only Server ('workshop_ro') - Tool Count: {len(ro_tools)}]")
    for t in ro_tools:
        print(f"  + {t}")
    assert "verify" not in ro_tools, "Read-only server unexpectedly has verify!"
    assert "memory_write" not in ro_tools, "Read-only server unexpectedly has memory_write!"
    assert "critique" not in ro_tools, "Read-only server unexpectedly has critique!"
    assert "skill_search" in ro_tools, "Read-only server missing skill_search"

    print("\n" + "=" * 70)
    print(" ✓ VERIFIED: Architectural split guarantees dangerous tools DO NOT EXIST on workshop_ro!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
