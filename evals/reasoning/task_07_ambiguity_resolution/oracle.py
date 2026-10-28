"""
Oracle for Task 07: Ambiguity Resolution (Handle Ambiguity).
"""
from typing import Dict, Any

def evaluate_ambiguity_resolution(response_text: str) -> Dict[str, Any]:
    text_lower = response_text.lower()
    
    # 1. Asks a clarifying question
    has_question = "?" in response_text and any(w in text_lower for w in ["which", "what format", "parquet", "csv", "json", "prefer", "destination"])
    
    # 2. States explicit working assumption
    has_assumption = any(w in text_lower for w in [
        "assuming",
        "assumption:",
        "working assumption",
        "defaulting to",
        "i will assume",
        "we assume"
    ])
    
    if has_question:
        # Check that it doesn't ask an avalanche of questions (max 2 question marks)
        q_count = response_text.count("?")
        if q_count > 3:
            return {
                "passed": False,
                "reason": f"Interrogator trap: asked {q_count} questions instead of a targeted clarifying question"
            }
        return {
            "passed": True,
            "strategy": "clarifying_question",
            "reason": "Agent appropriately asked a targeted clarifying question to resolve format/target ambiguity"
        }
        
    if has_assumption:
        return {
            "passed": True,
            "strategy": "explicit_assumption",
            "reason": "Agent explicitly articulated a transparent working assumption before proceeding"
        }
        
    return {
        "passed": False,
        "reason": "Agent blindly guessed without asking clarification or declaring assumptions"
    }
