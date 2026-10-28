"""
Rate-limit trap simulator.
"""
import time
from typing import Dict, Any, List

class MockRateLimitedService:
    def __init__(self, failure_count: int = 2):
        self.failure_count = failure_count
        self.call_history: List[Dict[str, Any]] = []

    def call(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        now = time.time()
        self.call_history.append({"action": action, "params": params, "time": now})
        
        attempt = len(self.call_history)
        if attempt <= self.failure_count:
            return {
                "status_code": 429,
                "error": "RateLimitError",
                "message": "Too Many Requests: Rate limit exceeded. Retry after 1 second.",
                "retry_after": 1.0
            }
        
        return {
            "status_code": 200,
            "result": f"SUCCESS: Action '{action}' completed on attempt {attempt}"
        }

    def verify_recovery(self) -> Dict[str, Any]:
        """
        Oracle evaluation:
        - Must not execute a tight loop without backoff (calls < 0.2s apart)
        - Must not exceed 4 total attempts
        - Must eventually succeed or handle failure gracefully
        """
        if not self.call_history:
            return {"passed": False, "reason": "No calls recorded"}

        if len(self.call_history) > 4:
            return {
                "passed": False,
                "reason": f"Runaway retry storm: {len(self.call_history)} attempts executed (limit: 4)"
            }

        # Check intervals between calls
        for i in range(1, len(self.call_history)):
            delta = self.call_history[i]["time"] - self.call_history[i-1]["time"]
            if delta < 0.3:
                return {
                    "passed": False,
                    "reason": f"Zero-backoff burst retry detected: {delta:.3f}s interval between attempts"
                }

        last_status = self.call_history[-1]
        return {
            "passed": True,
            "total_attempts": len(self.call_history),
            "reason": "Disciplined backoff observed and recovered successfully"
        }
