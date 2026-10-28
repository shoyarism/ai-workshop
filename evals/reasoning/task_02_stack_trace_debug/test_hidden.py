from .pipeline import process_inbound_stream

def test_batch_normalization_without_crash():
    batch_event = {
        "mode": "batch",
        "items": [
            {"kind": "message", "text": "hello world"},
            {"kind": "system", "text": "status healthy"},
            {"kind": "message", "payload": {"content": "already normalized"}}
        ]
    }
    results = process_inbound_stream(batch_event)
    assert len(results) == 3
    assert results[0] == "PROCESSED: HELLO WORLD"
    assert results[1] == "SYSTEM: status healthy"
    assert results[2] == "PROCESSED: ALREADY NORMALIZED"

def test_single_event_preservation():
    single_event = {
        "mode": "single",
        "kind": "message",
        "payload": {"content": "direct event"}
    }
    results = process_inbound_stream(single_event)
    assert results == ["PROCESSED: DIRECT EVENT"]
