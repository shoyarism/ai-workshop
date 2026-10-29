"""
Unit and integration tests for Workshop Agent Runtime daemon (scripts/agent_runtime.py).
Verifies SQLite task queue invariants, state transitions, and loopback health server.
"""

import json
import sqlite3
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import urllib.request

import scripts.agent_runtime as runtime_mod


class TestAgentRuntime(unittest.TestCase):
    """Verify AgentRuntime daemon core components."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_agent_runtime.db"
        self.db_patcher = patch.object(runtime_mod, "DB_PATH", self.db_path)
        self.db_patcher.start()

    def tearDown(self):
        self.db_patcher.stop()
        self.temp_dir.cleanup()

    def test_database_initialization_schema(self):
        runtime_mod.init_db()
        self.assertTrue(self.db_path.exists(), "Runtime DB must be created")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        self.assertIn("tasks", tables)
        self.assertIn("memory", tables)
        self.assertIn("logs", tables)

    def test_task_queue_crud_and_status(self):
        runtime = runtime_mod.AgentRuntime()

        # 1. Enqueue task
        task_id = runtime.add_task("Execute security audit")
        self.assertIsInstance(task_id, int)

        # 2. Dequeue task
        task = runtime.get_next_task()
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], task_id)
        self.assertEqual(task["goal"], "Execute security audit")

        # 3. Update task status
        runtime.update_task_status(task_id, "completed", "Audit passed with 0 findings")

        # 4. Assert no more pending tasks
        next_task = runtime.get_next_task()
        self.assertIsNone(next_task)

    def test_health_server_loopback_binding(self):
        runtime = runtime_mod.AgentRuntime()
        # Bind health server to a high random port for test isolation
        test_port = 7899
        with patch.object(runtime_mod, "HEALTH_PORT", test_port):
            runtime.start_health_server()
            try:
                time.sleep(0.1)  # allow server thread to bind
                url = f"http://127.0.0.1:{test_port}/health"
                req = urllib.request.Request(url, headers={"User-Agent": "RuntimeTest/1.0"})
                with urllib.request.urlopen(req, timeout=2.0) as resp:
                    self.assertEqual(resp.status, 200)
                    data = json.loads(resp.read().decode("utf-8"))
                    self.assertEqual(data.get("status"), "ok")
                    self.assertEqual(data.get("service"), "agent_runtime")
            finally:
                if runtime.health_server:
                    runtime.health_server.shutdown()
                    runtime.health_server.server_close()


if __name__ == "__main__":
    unittest.main()
