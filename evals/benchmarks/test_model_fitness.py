#!/usr/bin/env python3
"""
Free-Model Fitness Benchmark (FreeLLMAPI)
=========================================
Tests enabled candidate models from FreeLLMAPI across 4 rigorous dimensions:
1. Basic Reply: Responsiveness & format compliance.
2. Simple Tool Call: 1-tool schema generation.
3. Multi-Tool Call: Disambiguation with >= 3 tools present.
4. 20k Context Recall: Needle-in-a-haystack at 20,000 tokens depth.

Paces requests by >= 2.5s and implements exponential backoff on HTTP 429.
Generates ranked table, recommended Fallback Chain order, and models to drop.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import winreg
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass


def get_freellmapi_key() -> str:
    """Retrieve API key from process environment or User environment registry without logging."""
    val = os.environ.get("FREELLMAPI_API_KEY")
    if not val:
        try:
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
            val, _ = winreg.QueryValueEx(k, "FREELLMAPI_API_KEY")
            if val:
                os.environ["FREELLMAPI_API_KEY"] = val
        except Exception:  # @court-exempt: handled fallback
            pass
    return val or ""


def call_freellmapi_chat(
    model: str,
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None,
    max_tokens: int = 400,
    temperature: float = 0.0,
    max_retries: int = 3,
) -> Tuple[Optional[Dict[str, Any]], float, Optional[str]]:
    """Execute chat completion request with backoff on 429."""
    key = get_freellmapi_key()
    url = "http://127.0.0.1:31415/v1/chat/completions"
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    data_bytes = json.dumps(payload).encode("utf-8")
    t0 = time.perf_counter()

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                },
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                raw = resp.read().decode("utf-8")
                dur = (time.perf_counter() - t0) * 1000
                res_json = json.loads(raw)
                return res_json, dur, None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 2.5 * (2**attempt)
                time.sleep(wait_time)
                continue
            err_msg = f"HTTP {e.code}: {e.reason}"
            try:
                err_body = e.read().decode("utf-8")
                err_msg += f" - {err_body[:100]}"
            except Exception:  # @court-exempt: handled fallback
                pass
            return None, (time.perf_counter() - t0) * 1000, err_msg
        except Exception as e:
            return None, (time.perf_counter() - t0) * 1000, str(e)

    return None, (time.perf_counter() - t0) * 1000, "Max retries exceeded (HTTP 429)"


def generate_20k_needle_prompt(needle_code: str = "739218") -> str:
    """Generate a prompt of ~20,000 tokens with a needle in the middle."""
    filler_sentence = "The telemetry monitor continuously records baseline system state and CPU utilization metrics. "
    # ~15 words per sentence, ~20 tokens per sentence. 1,000 sentences = ~20,000 tokens.
    half_count = 500
    part1 = filler_sentence * half_count
    needle = f"\n\n[CRITICAL RECORD: The security verification code is {needle_code}. Remember this code.]\n\n"
    part2 = filler_sentence * half_count
    return part1 + needle + part2 + "\nWhat is the security verification code? Reply with ONLY the code."


def test_model_fitness(model_id: str) -> Dict[str, Any]:
    """Test all 4 dimensions for a given model."""
    print(f"\n---> Testing Model: {model_id}")
    results: Dict[str, Any] = {
        "model": model_id,
        "basic_reply": False,
        "single_tool": False,
        "multi_tool": False,
        "context_20k": False,
        "latencies": [],
        "errors": [],
        "score": 0,
    }

    # 1. Basic Reply Test
    time.sleep(2.5)
    res, lat, err = call_freellmapi_chat(
        model=model_id,
        messages=[{"role": "user", "content": "Respond with the single word 'READY'."}],
        max_tokens=20,
    )
    if res and "choices" in res and res["choices"]:
        content = res["choices"][0]["message"].get("content", "").strip()
        if "READY" in content.upper():
            results["basic_reply"] = True
            results["latencies"].append(lat)
            print("  [PASS] Test 1: Basic Reply")
        else:
            results["errors"].append(f"Basic reply unexpected: {content[:40]}")
            print(f"  [FAIL] Test 1: Basic Reply unexpected content: {content[:40]}")
    else:
        results["errors"].append(f"Basic reply error: {err}")
        print(f"  [FAIL] Test 1: Basic Reply error: {err}")

    # 2. Single Tool Call Test
    time.sleep(2.5)
    single_tool = [{
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"],
            },
        },
    }]
    res, lat, err = call_freellmapi_chat(
        model=model_id,
        messages=[{"role": "user", "content": "What is the weather in Jakarta right now?"}],
        tools=single_tool,
        max_tokens=150,
    )
    if res and "choices" in res and res["choices"]:
        msg = res["choices"][0]["message"]
        tool_calls = msg.get("tool_calls", [])
        if tool_calls and tool_calls[0].get("function", {}).get("name") == "get_current_weather":
            results["single_tool"] = True
            results["latencies"].append(lat)
            print("  [PASS] Test 2: Single Tool Call")
        else:
            results["errors"].append(f"No tool call returned for single tool: {msg.get('content', '')[:40]}")
            print("  [FAIL] Test 2: Single Tool Call not invoked")
    else:
        results["errors"].append(f"Single tool error: {err}")
        print(f"  [FAIL] Test 2: Single Tool Call error: {err}")

    # 3. Multi-Tool Call Test (>= 3 tools)
    time.sleep(2.5)
    multi_tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate_tax",
                "description": "Calculate tax on purchase",
                "parameters": {"type": "object", "properties": {"subtotal": {"type": "number"}}, "required": ["subtotal"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_database",
                "description": "Search customer database",
                "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_workspace_file",
                "description": "Read file from disk",
                "parameters": {"type": "object", "properties": {"filepath": {"type": "string"}}, "required": ["filepath"]},
            },
        },
    ]
    res, lat, err = call_freellmapi_chat(
        model=model_id,
        messages=[{"role": "user", "content": "Please read the file 'config.yaml' to check our settings."}],
        tools=multi_tools,
        max_tokens=150,
    )
    if res and "choices" in res and res["choices"]:
        msg = res["choices"][0]["message"]
        tool_calls = msg.get("tool_calls", [])
        if tool_calls and tool_calls[0].get("function", {}).get("name") == "read_workspace_file":
            results["multi_tool"] = True
            results["latencies"].append(lat)
            print("  [PASS] Test 3: Multi-Tool Call (3 tools)")
        else:
            called = tool_calls[0].get("function", {}).get("name") if tool_calls else "none"
            results["errors"].append(f"Multi-tool call failed, called: {called}")
            print(f"  [FAIL] Test 3: Multi-Tool Call incorrect invocation: {called}")
    else:
        results["errors"].append(f"Multi-tool error: {err}")
        print(f"  [FAIL] Test 3: Multi-Tool Call error: {err}")

    # 4. 20k-Token Context Recall Test
    time.sleep(2.5)
    needle_code = "739218"
    prompt_20k = generate_20k_needle_prompt(needle_code)
    res, lat, err = call_freellmapi_chat(
        model=model_id,
        messages=[{"role": "user", "content": prompt_20k}],
        max_tokens=60,
    )
    if res and "choices" in res and res["choices"]:
        content = res["choices"][0]["message"].get("content", "").strip()
        if needle_code in content:
            results["context_20k"] = True
            results["latencies"].append(lat)
            print("  [PASS] Test 4: 20k Context Recall")
        else:
            results["errors"].append(f"20k needle missed: {content[:40]}")
            print(f"  [FAIL] Test 4: 20k Context Recall missed needle: {content[:40]}")
    else:
        results["errors"].append(f"20k context error: {err}")
        print(f"  [FAIL] Test 4: 20k Context Recall error: {err}")

    # Compute score (each test = 25 pts)
    score = (
        (25 if results["basic_reply"] else 0)
        + (25 if results["single_tool"] else 0)
        + (25 if results["multi_tool"] else 0)
        + (25 if results["context_20k"] else 0)
    )
    results["score"] = score
    results["avg_latency_ms"] = round(sum(results["latencies"]) / len(results["latencies"]), 1) if results["latencies"] else 0.0
    return results


def main():
    parser = argparse.ArgumentParser(description="Evaluate free model fitness for agentic workflows.")
    parser.add_argument("--models", nargs="+", help="Specific model IDs to test")
    parser.add_argument("--output", default="evals/results/model_fitness_report.json", help="Path to save results")
    args = parser.parse_args()

    # Candidate roster of top free-tier models across architectures
    candidates = args.models or [
        "codestral-latest",
        "codestral",
        "command-r",
        "command-r-plus-08-2024",
        "gemini-2.5-flash",
        "mistral-small-3-2-24b-instruct",
        "openai-gpt-4o-mini",
        "hyperbolic-llama-3.3-70b",
    ]

    all_results: List[Dict[str, Any]] = []
    for mid in candidates:
        res = test_model_fitness(mid)
        all_results.append(res)

    # Sort results: highest score first, then lowest latency
    all_results.sort(key=lambda x: (-x["score"], x["avg_latency_ms"]))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print("\n=======================================================")
    print(" [*] FREE-MODEL FITNESS BENCHMARK RANKING TABLE")
    print("=======================================================")
    print(f"{'Rank':<5} {'Model ID':<30} {'Score':<7} {'Basic':<7} {'1-Tool':<7} {'3-Tool':<7} {'20k-Ctx':<8} {'Avg Latency':<12}")
    print("-" * 90)

    recommended_chain: List[str] = []
    models_to_drop: List[Tuple[str, str]] = []

    for idx, r in enumerate(all_results, 1):
        basic = "PASS" if r["basic_reply"] else "FAIL"
        t1 = "PASS" if r["single_tool"] else "FAIL"
        t3 = "PASS" if r["multi_tool"] else "FAIL"
        c20k = "PASS" if r["context_20k"] else "FAIL"
        lat = f"{r['avg_latency_ms']} ms"
        print(f"{idx:<5} {r['model']:<30} {r['score']:<7} {basic:<7} {t1:<7} {t3:<7} {c20k:<8} {lat:<12}")

        if r["score"] >= 75 and r["multi_tool"]:
            recommended_chain.append(r["model"])
        else:
            reasons = []
            if not r["single_tool"] or not r["multi_tool"]:
                reasons.append("unreliable tool calling")
            if not r["context_20k"]:
                reasons.append("failed 20k context recall")
            if not r["basic_reply"]:
                reasons.append("unresponsive / rate-limited")
            models_to_drop.append((r["model"], ", ".join(reasons)))

    print("\n-------------------------------------------------------")
    print(" Recommended Fallback Chain (Top Fit Models):")
    for pos, m in enumerate(recommended_chain, 1):
        print(f"   {pos}. {m}")

    print("\n Models to Drop from Agentic Chain:")
    for m, reason in models_to_drop:
        print(f"   • {m}: {reason}")
    print("=======================================================")


if __name__ == "__main__":
    main()
