"""
Inbound Event Stream Pipeline.
"""
from typing import Dict, Any, List
from .dispatcher import Dispatcher

dispatcher = Dispatcher()

def process_inbound_stream(event: Dict[str, Any]) -> List[str]:
    results = []
    mode = event.get("mode", "single")
    
    if mode == "single":
        res = dispatcher.route_event(event)
        results.append(res)
    elif mode == "batch":
        # BUG: Batch payloads receive items with key 'text' or 'data',
        # but the code blindly packages it without normalizing to 'content'
        for item in event.get("items", []):
            sub_event = {
                "kind": item.get("kind", "message"),
                "payload": item.get("payload", {})
            }
            # Bug: when item directly provides {"kind": "message", "text": "hello"},
            # item.get("payload") is {} which lacks 'content'!
            results.append(dispatcher.route_event(sub_event))
    elif mode == "ping":
        results.append("PONG")
    else:
        raise ValueError(f"Unsupported pipeline mode: {mode}")

    return results
