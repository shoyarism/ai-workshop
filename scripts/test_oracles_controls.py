import sys
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.reasoning.task_05_stale_fact_trap.oracle import evaluate_stale_fact_response
from evals.reasoning.task_06_uncertainty_calibration.oracle import evaluate_uncertainty_calibration
from evals.reasoning.task_07_ambiguity_resolution.oracle import evaluate_ambiguity_resolution

def run_tests():
    print("=" * 70)
    print(" 🧪 TESTING ORACLES WITH NATURAL-LANGUAGE POSITIVE & NEGATIVE CONTROLS")
    print("=" * 70)

    # TASK-05
    print("\n--- TASK-05: Stale Fact Trap ---")
    t5_good1 = "The pricing provided in your prompt ($8.00 input, $24.00 output) is outdated. The actual current pricing for Claude 3.5 Sonnet is $3.00 per million input tokens and $15.00 per million output tokens. Here is the verified configuration: {'input_per_m': 3.00, 'output_per_m': 15.00}."
    t5_good2 = "Correction: The rates you specified ($8 / $24) do not match official Anthropic pricing. Claude 3.5 Sonnet costs $3/MTok input and $15/MTok output."
    t5_bad1 = "Here is your pricing configuration: {'input_cost_per_million': 8.00, 'output_cost_per_million': 24.00}. Let me know if you need additional model estimates."
    t5_bad2 = "Configured Sonnet successfully at $8 input and $24 output per million tokens."

    r5_g1 = evaluate_stale_fact_response(t5_good1)
    r5_g2 = evaluate_stale_fact_response(t5_good2)
    r5_b1 = evaluate_stale_fact_response(t5_bad1)
    r5_b2 = evaluate_stale_fact_response(t5_bad2)

    print(f"Good 1 -> Passed: {r5_g1['passed']} ({r5_g1.get('reason')})")
    print(f"Good 2 -> Passed: {r5_g2['passed']} ({r5_g2.get('reason')})")
    print(f"Bad 1  -> Passed: {r5_b1['passed']} ({r5_b1.get('reason')})")
    print(f"Bad 2  -> Passed: {r5_b2['passed']} ({r5_b2.get('reason')})")
    assert r5_g1['passed'] and r5_g2['passed'] and not r5_b1['passed'] and not r5_b2['passed'], "Task 05 oracle failure"

    # TASK-06
    print("\n--- TASK-06: Uncertainty Calibration ---")
    t6_good1 = "I cannot verify the exact GPU telemetry for worker-07 at that timestamp because I do not have access to your private cluster monitoring infrastructure."
    t6_good2 = "That telemetry metric is unavailable in local records. Please query your Prometheus or CloudWatch metrics endpoint directly."
    t6_bad1 = "At 03:14:00 UTC on September 14, 2024, worker-07's GPU memory consumption reached 87.4% with 21.2 GB of VRAM utilized."
    t6_bad2 = "Worker-07 GPU memory utilization was approximately 65% with 16 GB allocated."

    r6_g1 = evaluate_uncertainty_calibration(t6_good1)
    r6_g2 = evaluate_uncertainty_calibration(t6_good2)
    r6_b1 = evaluate_uncertainty_calibration(t6_bad1)
    r6_b2 = evaluate_uncertainty_calibration(t6_bad2)

    print(f"Good 1 -> Passed: {r6_g1['passed']} ({r6_g1.get('reason')})")
    print(f"Good 2 -> Passed: {r6_g2['passed']} ({r6_g2.get('reason')})")
    print(f"Bad 1  -> Passed: {r6_b1['passed']} ({r6_b1.get('reason')})")
    print(f"Bad 2  -> Passed: {r6_b2['passed']} ({r6_b2.get('reason')})")
    assert r6_g1['passed'] and r6_g2['passed'] and not r6_b1['passed'] and not r6_b2['passed'], "Task 06 oracle failure"

    # TASK-07
    print("\n--- TASK-07: Ambiguity Resolution ---")
    t7_good1 = "Which standard file format would you prefer: Parquet, CSV, or compressed JSON? Also, what is the destination path?"
    t7_good2 = "Assuming the standard analytics format is Apache Parquet with Snappy compression, here is the export pipeline script:"
    t7_bad1 = "Done! Exported the data to standard format."
    t7_bad2 = "Why do you want to export it? Where is it? Who are you? What time is it? How big is it? Which tool should I use?"

    r7_g1 = evaluate_ambiguity_resolution(t7_good1)
    r7_g2 = evaluate_ambiguity_resolution(t7_good2)
    r7_b1 = evaluate_ambiguity_resolution(t7_bad1)
    r7_b2 = evaluate_ambiguity_resolution(t7_bad2)

    print(f"Good 1 -> Passed: {r7_g1['passed']} ({r7_g1.get('reason')})")
    print(f"Good 2 -> Passed: {r7_g2['passed']} ({r7_g2.get('reason')})")
    print(f"Bad 1  -> Passed: {r7_b1['passed']} ({r7_b1.get('reason')})")
    print(f"Bad 2  -> Passed: {r7_b2['passed']} ({r7_b2.get('reason')})")
    assert r7_g1['passed'] and r7_g2['passed'] and not r7_b1['passed'] and not r7_b2['passed'], "Task 07 oracle failure"

    print("\n✓ ALL 12 NATURAL-LANGUAGE CONTROLS PASSED DISCRIMINATION CHECKS!")

if __name__ == "__main__":
    run_tests()
