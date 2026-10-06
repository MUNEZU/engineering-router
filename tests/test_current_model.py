from __future__ import annotations

import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "skills" / "engineering-router" / "scripts" / "current_model.py"
SPEC = importlib.util.spec_from_file_location("current_model", SCRIPT)
assert SPEC and SPEC.loader
current_model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(current_model)


def write_trace(path: Path, session_id: str, model: str, effort: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    events = [
        {"type": "session_meta", "payload": {"id": session_id}},
        {
            "type": "turn_context",
            "timestamp": "2026-09-26T00:00:00Z",
            "payload": {"model": model, "effort": effort},
        },
    ]
    path.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")


class CurrentModelTests(unittest.TestCase):
    def run_main(self, env: dict[str, str]) -> tuple[int, dict]:
        output = io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), redirect_stdout(output):
            code = current_model.main()
        return code, json.loads(output.getvalue())

    def test_missing_thread_id_returns_explicit_unknown(self) -> None:
        code, payload = self.run_main({})
        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "unknown")
        self.assertIn("CODEX_THREAD_ID", payload["reason"])

    def test_reads_root_trace_and_ignores_child_with_matching_filename(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            write_trace(
                home / "sessions" / "root-task-123.jsonl",
                "task-123",
                "gpt-5.6-sol",
                "high",
            )
            write_trace(
                home / "sessions" / "child-task-123.jsonl",
                "child-456",
                "gpt-5.6-luna",
                "medium",
            )
            code, payload = self.run_main(
                {"CODEX_HOME": str(home), "CODEX_THREAD_ID": "task-123"}
            )
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["model"], "gpt-5.6-sol")
        self.assertEqual(payload["effort"], "high")
        self.assertEqual(payload["source"], "local_codex_session_trace")


if __name__ == "__main__":
    unittest.main()
