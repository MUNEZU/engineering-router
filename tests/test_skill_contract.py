from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills" / "engineering-router"


class EngineeringRouterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    def test_linked_skill_resources_exist(self) -> None:
        references = set(re.findall(r"\]\((references/[^)#]+)\)", self.skill))
        scripts = set(re.findall(r"scripts/[a-z_]+\.py", self.skill))
        self.assertEqual(
            references,
            {
                "references/evaluation.md",
                "references/explore.md",
                "references/interactive-testing.md",
                "references/profiles-routing.md",
                "references/simplify.md",
            },
        )
        self.assertEqual(scripts, {"scripts/current_model.py", "scripts/usage_by_model.py"})
        for target in references | scripts:
            with self.subTest(target=target):
                self.assertTrue((SKILL / target).is_file())

    def test_activation_contract_contains_each_exact_line_once(self) -> None:
        activation = self.skill.split("## Activation", 1)[1].split("## Root ownership", 1)[0]
        self.assertEqual(activation.count("🐈 已开启小队模式。"), 1)
        self.assertEqual(activation.count("🐈 Team Mode activated."), 1)
        self.assertIn("exactly one commentary line", activation)
        self.assertIn("Do not repeat", activation)

    def test_root_and_child_boundaries_are_explicit(self) -> None:
        required = (
            "Simple work may use zero children",
            "One bounded question defaults to one child",
            "two discretionary children",
            "fork_context=false",
            'fork_turns="none"',
            "Children must not spawn descendants",
            "Never assign overlapping writes",
            "fresh `independent_reviewer`",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.skill)

    def test_public_skill_has_no_private_machine_paths(self) -> None:
        public_files = [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
        ]
        public_files = [path for path in public_files if "local-overlay" not in path.parts]
        user_prefix = "/" + "Users" + "/"
        private_control_plane = "Documents" + "/" + "ai-control-plane"
        for path in public_files:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8", errors="ignore")
                self.assertNotRegex(text, re.escape(user_prefix) + r"[^/]+/")
                self.assertNotIn(private_control_plane, text)

    def test_skill_is_implicit_and_package_keeps_single_name(self) -> None:
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertFalse((ROOT / "skills" / "team-mode").exists())
        self.assertFalse((ROOT / "skills" / "codex-team-mode").exists())


if __name__ == "__main__":
    unittest.main()
