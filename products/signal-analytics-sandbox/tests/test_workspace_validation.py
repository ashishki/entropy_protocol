import json
import os
import stat
import subprocess
import unittest
from pathlib import Path

PRODUCT_ROOT = Path(__file__).resolve().parents[1]


class WorkspaceValidationTests(unittest.TestCase):
    def test_required_planning_documents_exist(self) -> None:
        required_paths = [
            "README.md",
            "RUNBOOK.md",
            "docs/ARCHITECTURE.md",
            "docs/CODEX_PROMPT.md",
            "docs/IMPLEMENTATION_CONTRACT.md",
            "docs/spec.md",
            "docs/tasks.md",
        ]

        missing = [
            path for path in required_paths if not (PRODUCT_ROOT / path).is_file()
        ]

        self.assertEqual(missing, [])

    def test_engineering_phase_zero_gates_are_acknowledged(self) -> None:
        prompt = (PRODUCT_ROOT / "docs/CODEX_PROMPT.md").read_text()

        self.assertIn("Engineering Phase 1 (T01+) may begin", prompt)
        self.assertIn(
            "| SAS-001: Paid Pilot Demand Validation | acknowledged |", prompt
        )
        self.assertIn(
            "| SAS-002: Public-Source Legal/Terms Memo | acknowledged |", prompt
        )
        self.assertTrue((PRODUCT_ROOT / "docs/PILOT_LOG.md").is_file())
        self.assertTrue((PRODUCT_ROOT / "docs/legal_risk_memo.md").is_file())

    def test_hook_scripts_are_executable_and_parse(self) -> None:
        hooks = sorted((PRODUCT_ROOT / "hooks").glob("*.sh"))

        self.assertGreater(len(hooks), 0)
        for hook in hooks:
            mode = hook.stat().st_mode
            self.assertTrue(
                mode & stat.S_IXUSR,
                f"{hook.relative_to(PRODUCT_ROOT)} is not user-executable",
            )
            subprocess.run(
                ["bash", "-n", str(hook)],
                cwd=PRODUCT_ROOT,
                check=True,
                text=True,
            )

    def test_guard_files_blocks_existing_immutable_file(self) -> None:
        payload = {
            "tool_name": "Edit",
            "tool_input": {"file_path": "docs/IMPLEMENTATION_CONTRACT.md"},
        }

        result = self._run_hook("guard_files.sh", payload)

        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("immutable at runtime", result.stderr)

    def test_enforce_codex_exec_blocks_direct_test_edits(self) -> None:
        payload = {
            "tool_name": "Write",
            "tool_input": {"file_path": "tests/example.py"},
        }

        result = self._run_hook("enforce_codex_exec.sh", payload)

        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("direct tool edits to application code", result.stderr)

    def test_phase_boundary_guard_blocks_phase_increment(self) -> None:
        payload = {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "docs/CODEX_PROMPT.md",
                "old_string": "Phase: 6",
                "new_string": "Phase: 7",
            },
        }

        result = self._run_hook("guard_phase_boundary.sh", payload)

        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("phase boundary update", result.stderr)

    def test_phase_boundary_guard_blocks_next_task_phase_increment(self) -> None:
        payload = {
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "docs/CODEX_PROMPT.md",
                "old_string": "**T16: ManualExtractionAdapter**",
                "new_string": "**T18: ExchangePublicOHLCVProvider**",
            },
        }

        result = self._run_hook("guard_phase_boundary.sh", payload)

        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("requires archived deep review for Phase 6", result.stderr)

    def _run_hook(
        self, hook_name: str, payload: dict[str, object]
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PLAYBOOK_CODEX_PROMPT_PATH"] = "docs/CODEX_PROMPT.md"
        env["PLAYBOOK_AUDIT_INDEX_PATH"] = "docs/audit/AUDIT_INDEX.md"
        env["PLAYBOOK_TASKS_PATH"] = "docs/tasks.md"

        return subprocess.run(
            [str(PRODUCT_ROOT / "hooks" / hook_name)],
            input=json.dumps(payload),
            cwd=PRODUCT_ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
