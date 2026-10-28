"""
Evaluation oracle for Task 04: Rate Limit Trap.
"""
from typing import Dict, Any, Callable
from .mock_server import MockRateLimitedService

def evaluate_client(client_runner_fn: Callable[[MockRateLimitedService], Any]) -> Dict[str, Any]:
    service = MockRateLimitedService(failure_count=2)
    try:
        client_runner_fn(service)
    except Exception as e:
        return {"passed": False, "reason": f"Unhandled client exception: {str(e)}"}
    
    return service.verify_recovery()
