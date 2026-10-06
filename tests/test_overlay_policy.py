from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
OVERLAY = ROOT / "local-overlay"
EXTERNAL = OVERLAY / "external-skills"


class OverlayPolicyTests(unittest.TestCase):
    def test_machine_overlay_is_excluded_from_public_git(self) -> None:
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/local-overlay/", gitignore.splitlines())

    @unittest.skipUnless(OVERLAY.is_dir(), "Optional local overlays are not distributed")
    def test_external_skills_are_explicit_only(self) -> None:
        forbidden = (
            "may select this Skill automatically",
            "default router selects",
            "Default domain routing",
            "Default frontend routing",
            "When routing is unresolved",
        )
        for skill_dir in sorted(path for path in EXTERNAL.iterdir() if path.is_dir()):
            with self.subTest(skill=skill_dir.name):
                skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                metadata = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn("explicit", skill.lower())
                self.assertIn("allow_implicit_invocation: false", metadata)
                for phrase in forbidden:
                    self.assertNotIn(phrase, skill)

    @unittest.skipUnless(OVERLAY.is_dir(), "Optional local overlays are not distributed")
    def test_local_agreement_uses_native_team_mode_without_external_matrix(self) -> None:
        agreement = (OVERLAY / "AGENTS.md").read_text(encoding="utf-8")
        for role in (
            "code_explorer",
            "code_writer",
            "luna_worker",
            "hard_code_writer",
            "independent_reviewer",
            "expert_advisor",
        ):
            self.assertIn(f"`{role}`", agreement)
        self.assertIn("explicit-user-or-valid-handoff only", agreement)
        self.assertNotIn("Model responsibility matrix", agreement)
        self.assertNotIn("codex-multi-model-agents routing policy", agreement)
        self.assertNotIn("sol_design_architect", agreement)
        self.assertIn("The shared AI Control Plane is the private repository at", agreement)
        self.assertIn("projects/index.md", agreement)


if __name__ == "__main__":
    unittest.main()
