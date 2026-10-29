"""
Unit tests for Workshop Agent Watchdog supervisor (scripts/agent_watchdog.py).
Verifies health checking invariants, process supervision primitives, and state serialization.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import scripts.agent_watchdog as watchdog_mod


class TestAgentWatchdog(unittest.TestCase):
    """Verify watchdog supervisor invariants."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_file = Path(self.temp_dir.name) / "watchdog_state.json"
        self.state_patcher = patch.object(watchdog_mod, "STATE_FILE", self.state_file)
        self.state_patcher.start()

    def tearDown(self):
        self.state_patcher.stop()
        self.temp_dir.cleanup()

    def test_services_registry_schema(self):
        required_keys = {"name", "command", "health_check", "restart_delay", "max_restarts", "restart_window"}
        for svc_name, svc_conf in watchdog_mod.SERVICES.items():
            for key in required_keys:
                self.assertIn(key, svc_conf, f"Service {svc_name} missing configuration key: {key}")
            self.assertIsInstance(svc_conf["command"], list)
            self.assertTrue(callable(svc_conf["health_check"]))
            self.assertGreater(svc_conf["max_restarts"], 0)

    def test_state_load_and_save(self):
        initial_state = watchdog_mod.load_state()
        self.assertEqual(initial_state, {})

        sample_state = {
            "agent_runtime": {
                "pid": 12345,
                "restarts": 1,
                "last_started": 1700000000.0,
            }
        }
        watchdog_mod.save_state(sample_state)
        loaded_state = watchdog_mod.load_state()
        self.assertEqual(loaded_state, sample_state)

    def test_check_http_health_unreachable_endpoint(self):
        # Local port 59999 should not have any service listening
        res = watchdog_mod.check_http_health("http://127.0.0.1:59999/health", timeout=0.1)
        self.assertFalse(res, "Unreachable health endpoint must return False")

    def test_check_http_health_mock_success(self):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp):
            res = watchdog_mod.check_http_health("http://127.0.0.1:7861/health")
            self.assertTrue(res, "200 OK health endpoint must return True")

    def test_is_pid_alive_current_process(self):
        my_pid = os.getpid()
        self.assertTrue(watchdog_mod.is_pid_alive(my_pid), "Current process PID must be reported alive")
        self.assertFalse(watchdog_mod.is_pid_alive(-999), "Negative PID must be reported not alive")


if __name__ == "__main__":
    unittest.main()
