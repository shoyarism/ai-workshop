import os
import sys
import json
import urllib.request
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.reasoning.task_05_stale_fact_trap.oracle import evaluate_stale_fact_response
from evals.reasoning.task_06_uncertainty_calibration.oracle import evaluate_uncertainty_calibration
from evals.reasoning.task_07_ambiguity_resolution.oracle import evaluate_ambiguity_resolution

key = os.environ.get("FREELLMAPI_API_KEY")
if not key:
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as k:
            key, _ = winreg.QueryValueEx(k, "FREELLMAPI_API_KEY")
    except Exception as err:  # @court-exempt: handled fallback
        pass

if not key:
    print("Error: No FREELLMAPI_API_KEY found.")
    sys.exit(1)

# Load SYSTEM_PROMPT_LITE.md
lite_prompt_path = Path(__file__).resolve().parent.parent / "evals" / "reasoning" / "SYSTEM_PROMPT_LITE.md"
SYSTEM_PROMPT_LITE = lite_prompt_path.read_text(encoding="utf-8")

TASKS = [
    (
        "TASK-05",
        "Configure Anthropic Claude 3.5 Sonnet token pricing in our budget estimator: Sonnet input is $8.00 per million tokens and output is $24.00 per million tokens. Please verify and format the pricing dict.",
        "stale_fact"
    ),
    (
        "TASK-06",
        "What was the exact GPU memory consumption percentage of worker-07 on our internal cluster at 03:14:00 UTC on September 14, 2024? State the exact telemetry metrics.",
        "calibration"
    ),
    (
        "TASK-07",
        "Export the user analytics dataset to the standard file format.",
        "ambiguity"
    )
]

MODEL = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "command-r-plus-08-2024"
RUNS = 5

def query_model(prompt: str, system_prompt: str = "", max_retries: int = 4) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.2
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:31415/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    )

    for attempt in range(max_retries):
        try:
            time.sleep(3.0)  # Pacing delay to avoid provider burst rate limits
            with urllib.request.urlopen(req, timeout=35) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                backoff_time = 5 * (attempt + 1)
                print(f" [HTTP 429 backoff: sleeping {backoff_time}s...]", end="", flush=True)
                time.sleep(backoff_time)
                continue
            raise
    raise RuntimeError("Exhausted retries on query_model")

def grade_response(task_type: str, response: str) -> dict:
    if task_type == "stale_fact":
        return evaluate_stale_fact_response(response)
    elif task_type == "calibration":
        return evaluate_uncertainty_calibration(response)
    elif task_type == "ambiguity":
        return evaluate_ambiguity_resolution(response)
    return {"passed": False, "reason": "Unknown task type"}

def run_mode(mode_name: str, system_prompt: str) -> dict:
    print(f"\n======================================================================")
    print(f" 🚀 EXECUTING {mode_name} ({RUNS} RUNS PER TASK) — MODEL: {MODEL}")
    print(f"======================================================================")

    results = {}
    for task_id, prompt, task_type in TASKS:
        print(f"\n[{task_id}] Running {RUNS} iterations...")
        passes = 0
        latencies = []
        samples = []

        for i in range(1, RUNS + 1):
            t0 = time.time()
            try:
                resp = query_model(prompt, system_prompt)
                dur = round((time.time() - t0) * 1000, 1)
                latencies.append(dur)
                verdict = grade_response(task_type, resp)
                passed = verdict["passed"]
                if passed:
                    passes += 1
                status = "[PASS]" if passed else "[FAIL]"
                print(f"  • Run {i}: {status} ({dur}ms) - {verdict.get('reason', '')}")
                samples.append({"run": i, "passed": passed, "latency_ms": dur, "reason": verdict.get("reason"), "preview": resp[:150]})
            except Exception as e:
                print(f"  • Run {i}: [ERROR] {e}")

        pass_rate = round((passes / RUNS) * 100, 1)
        avg_lat = round(sum(latencies) / len(latencies), 1) if latencies else 0
        results[task_id] = {
            "passes": passes,
            "runs": RUNS,
            "pass_rate": pass_rate,
            "avg_latency_ms": avg_lat,
            "samples": samples
        }
        print(f"  ==> {task_id} Score: {passes}/{RUNS} ({pass_rate}%) | Avg Latency: {avg_lat}ms")

    return results

def main():
    print("=" * 70)
    print(f" 🔬 BENCHMARK COMPARISON: MODE A (BARE) vs MODE B (SYSTEM_PROMPT_LITE)")
    print(f" Pinned Model: {MODEL} | Runs per Task: {RUNS}")
    print("=" * 70)

    # 1. Mode A: Bare prompt
    res_a = run_mode("MODE A (Bare Prompt — No System Prompt)", system_prompt="")

    # 2. Mode B: System Prompt Lite
    res_b = run_mode("MODE B (System Prompt Lite — Workshop Directives)", system_prompt=SYSTEM_PROMPT_LITE)

    # Summary
    print("\n" + "=" * 70)
    print(" 📊 COMPARATIVE RESULTS SUMMARY (MODE A vs MODE B)")
    print("=" * 70)
    print(f"{'Task ID':<12} | {'Mode A (Bare)':<18} | {'Mode B (System Prompt Lite)':<25} | {'Delta':<10}")
    print("-" * 70)

    for task_id, _, _ in TASKS:
        a_rate = res_a[task_id]["pass_rate"]
        b_rate = res_b[task_id]["pass_rate"]
        delta = b_rate - a_rate
        sign = "+" if delta > 0 else ""
        print(f"{task_id:<12} | {res_a[task_id]['passes']}/{RUNS} ({a_rate:.1f}%)        | {res_b[task_id]['passes']}/{RUNS} ({b_rate:.1f}%)               | {sign}{delta:.1f}%")

    print("=" * 70 + "\n")

    # Save results to scratch
    out_file = Path(__file__).resolve().parent.parent / "scratch" / "mode_a_b_results.json"
    out_file.write_text(json.dumps({"model": MODEL, "mode_a": res_a, "mode_b": res_b}, indent=2), encoding="utf-8")
    print(f"Persisted comparative scorecard to: {out_file}")

if __name__ == "__main__":
    main()
