"""Contratos dos adaptadores de hooks e do gate oficial de maturidade."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


guard = module(".claude/hooks/guard_tools.py", "guard_tools")
feedback = module(".claude/hooks/feedback.py", "feedback")
score = module("scripts/harness_score.py", "harness_score")


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def payload(self, tool="Bash", **data):
        return {
            "hook_event_name": "PreToolUse",
            "tool_name": tool,
            "tool_input": data,
            "cwd": str(self.root),
        }

    def test_shell_read_and_test_commands_preserve_executor_permissions(self):
        for command in (
            "git status --short",
            "make test-docker",
            "rg --files",
            "git push origin main",
        ):
            with self.subTest(command=command):
                self.assertTrue(guard.decide(self.payload(command=command), self.root)[0])
        result = subprocess.run(
            [sys.executable, str(ROOT / ".claude/hooks/guard_tools.py")],
            input=json.dumps(self.payload(command="git status")),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(json.loads(result.stdout), {})

    def test_explicit_destructive_commands_denied(self):
        for command in (
            "rm -rf /",
            "rm -fr /*",
            "rm -rf ~",
            "git reset --hard HEAD",
            "git clean -fdx",
            "git push --force origin main",
            "git push -f origin main",
            "git -C /tmp/repo push --force-with-lease",
            'sqlite3 db "DROP TABLE sources"',
        ):
            with self.subTest(command=command):
                self.assertFalse(guard.decide(self.payload(command=command), self.root)[0])

    def test_malformed_payload_returns_deny_in_protocol(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / ".claude/hooks/guard_tools.py")],
            input="{invalid",
            capture_output=True,
            text=True,
            check=True,
        )
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(output["permissionDecision"], "deny")
        self.assertEqual(output["hookEventName"], "PreToolUse")

    def test_protected_destinations_and_escape_denied(self):
        for target in (
            ".git/config",
            ".env",
            ".env.local",
            "private.key",
            "rag/traducao/harness/vendor/harness-eval/SKILL.md",
            "rag/traducao/input/source.pdf",
            "../outside.txt",
        ):
            with self.subTest(target=target):
                self.assertFalse(
                    guard.decide(self.payload("Write", file_path=target), self.root)[0]
                )
        self.assertTrue(
            guard.decide(self.payload("Write", file_path="scripts/new.py"), self.root)[0]
        )
        self.assertTrue(guard.decide(self.payload("Write", file_path=".env.example"), self.root)[0])

    def test_symlink_and_unknown_tool_denied(self):
        (self.root / "alias").symlink_to(self.root, target_is_directory=True)
        self.assertFalse(guard.decide(self.payload("Edit", file_path="alias/new.py"), self.root)[0])
        self.assertFalse(guard.decide(self.payload("Unknown", command="anything"), self.root)[0])

    def test_registered_gate_command_works_outside_checkout_cwd(self):
        settings = json.loads((ROOT / ".claude/settings.json").read_text())
        command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.root,
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT)},
            input=json.dumps(self.payload(command="git push --force origin main")),
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(
            json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "deny"
        )

    def test_feedback_cannot_hide_failure_or_timeout(self):
        payload = json.dumps(
            {"hook_event_name": "PostToolUse", "tool_name": "Edit", "tool_input": {}}
        )
        with patch.object(sys, "stdin") as stream:
            stream.read.return_value = payload
            with patch.object(
                feedback.subprocess, "run", return_value=subprocess.CompletedProcess([], 1)
            ):
                self.assertEqual(feedback.main(), 2)
            with patch.object(
                feedback.subprocess, "run", side_effect=subprocess.TimeoutExpired([], 50)
            ):
                self.assertEqual(feedback.main(), 2)


class ScoreTests(unittest.TestCase):
    def test_official_cli_rejects_empty_repository_below_l4(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                ["node", str(score.CLI), directory, "--json", "--min-level", "4"],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["tool"]["name"], "harness-score")
        self.assertLess(report["level"]["index"], 4)
        self.assertFalse(report["truncated"])

    def test_below_l4_exit_is_preserved(self):
        report = {
            "tool": {"name": "harness-score", "version": "1.8.1"},
            "level": {"index": 2},
            "score": {"percent": 47},
        }
        with patch.object(score, "verify_vendor"), patch.object(score.subprocess, "run") as runner:
            runner.return_value = subprocess.CompletedProcess([], 1, json.dumps(report))
            result, status = score.scan(ROOT, 4)
        self.assertEqual(status, 1)
        self.assertEqual(result["root"], ".")
        self.assertIn("--min-level", runner.call_args.args[0])
        self.assertIn("maturity", runner.call_args.args[0])

    def test_incomplete_scan_never_green(self):
        with patch.object(score, "verify_vendor"), patch.object(score.subprocess, "run") as runner:
            runner.return_value = subprocess.CompletedProcess([], 2, "")
            with self.assertRaisesRegex(ValueError, "incompleto"):
                score.scan(ROOT, 4)

    def test_custom_reweighting_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".harness-score.json").write_text('{"rules":{}}')
            with (
                patch.object(score, "verify_vendor"),
                patch.object(score.subprocess, "run") as runner,
            ):
                with self.assertRaisesRegex(ValueError, "reponderação"):
                    score.scan(root, 4)
                runner.assert_not_called()


if __name__ == "__main__":
    unittest.main()
