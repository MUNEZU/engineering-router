from __future__ import annotations

import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
FIXED_PROFILES = {
    "code-explorer.toml": ("code_explorer", "gpt-5.6-luna", "medium", "read-only"),
    "code-writer.toml": ("code_writer", "gpt-5.6-luna", "medium", "workspace-write"),
    "luna-worker.toml": ("luna_worker", "gpt-5.6-luna", "max", "workspace-write"),
    "hard-code-writer.toml": ("hard_code_writer", "gpt-6.1-sol", "high", "workspace-write"),
    "independent-reviewer.toml": (
        "independent_reviewer",
        "gpt-6.1-sol",
        "high",
        "read-only",
    ),
}


class AgentProfileTests(unittest.TestCase):
    def profile(self, name: str) -> dict:
        return tomllib.loads((ROOT / "agents" / name).read_text(encoding="utf-8"))

    def test_fixed_profile_runtime_contracts(self) -> None:
        for filename, expected in FIXED_PROFILES.items():
            with self.subTest(filename=filename):
                data = self.profile(filename)
                actual = (
                    data["name"],
                    data["model"],
                    data["model_reasoning_effort"],
                    data["sandbox_mode"],
                )
                self.assertEqual(actual, expected)
                self.assertNotIn("service_tier", data)
                self.assertIn("spawn agents", data["developer_instructions"].lower())

    def test_expert_advisor_is_read_only_and_selected_at_spawn(self) -> None:
        data = self.profile("expert-advisor.toml")
        self.assertEqual(data["name"], "expert_advisor")
        self.assertEqual(data["sandbox_mode"], "read-only")
        self.assertNotIn("model", data)
        self.assertNotIn("model_reasoning_effort", data)
        instructions = data["developer_instructions"]
        self.assertIn("gpt-6.1-sol", instructions)
        self.assertIn("gpt-6-astra", instructions)
        self.assertIn("exact runtime model", instructions)

    def test_fixed_profiles_preserve_luna_and_migrate_sol(self) -> None:
        for path in (ROOT / "agents").glob("*.toml"):
            with self.subTest(path=path.name):
                data = tomllib.loads(path.read_text(encoding="utf-8"))
                if "model" in data:
                    self.assertEqual(data["model"], FIXED_PROFILES[path.name][1])

    def test_only_v2_profiles_are_shipped(self) -> None:
        names = {path.name for path in (ROOT / "agents").glob("*.toml")}
        self.assertEqual(names, set(FIXED_PROFILES) | {"expert-advisor.toml"})
        self.assertNotIn("sol-design-architect.toml", names)
        self.assertNotIn("default.toml", names)


if __name__ == "__main__":
    unittest.main()
