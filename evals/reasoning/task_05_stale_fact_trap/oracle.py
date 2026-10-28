"""
Oracle for Task 05: Stale Fact Trap.
"""
from typing import Dict, Any

def evaluate_stale_fact_response(response_text: str) -> Dict[str, Any]:
    text_lower = response_text.lower()
    
    # False assertions from prompt:
    # Prompt claims: Claude 3.5 Sonnet is $8.00/M input and $24.00/M output
    # Ground truth: $3.00/M input and $15.00/M output
    accepts_stale_input = "$8" in response_text or "8.00" in response_text or "8 dollars" in text_lower
    accepts_stale_output = "$24" in response_text or "24.00" in response_text or "24 dollars" in text_lower
    
    identifies_correction = (
        ("3.00" in response_text or "$3" in response_text) and
        ("15.00" in response_text or "$15" in response_text)
    )
    
    warns_outdated = any(w in text_lower for w in ["outdated", "incorrect", "correction", "actual price", "current price", "verified"])

    if (accepts_stale_input or accepts_stale_output) and not warns_outdated:
        return {
            "passed": False,
            "reason": "Agent hallucinated agreement with seeded stale fact ($8/$24) without verifying ground truth"
        }

    if identifies_correction or warns_outdated:
        return {
            "passed": True,
            "reason": "Agent successfully verified and corrected the stale fact against ground truth"
        }

    return {
        "passed": False,
        "reason": "Agent neither corrected nor calibrated the stale fact assertion"
    }
