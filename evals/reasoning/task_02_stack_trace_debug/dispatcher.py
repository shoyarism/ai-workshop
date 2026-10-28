"""
Event Dispatcher module.
"""
from typing import Dict, Any, Callable

class Dispatcher:
    def __init__(self):
        self.handlers: Dict[str, Callable[[str], str]] = {
            "message": lambda content: f"PROCESSED: {content.strip().upper()}",
            "system": lambda content: f"SYSTEM: {content.strip()}",
        }

    def route_event(self, event: Dict[str, Any]) -> str:
        kind = event.get("kind", "message")
        if kind not in self.handlers:
            raise ValueError(f"Unknown event kind: {kind}")
        # Invariant contract: payload must contain 'content' string
        return self.handlers[kind](event["payload"]["content"])
