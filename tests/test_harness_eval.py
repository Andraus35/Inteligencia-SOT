"""Regressões da integração local: escopo, fan-in e bloqueios de avaliação."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("adapter", REPO / "scripts/harness_eval.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class EvalIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def test_nested_active_skill_is_t1_without_vendor_instructions(self):
        self.write("AGENTS.md", "root")
        self.write("rag/traducao/AGENTS.md", "stage")
        active = self.write("rag/traducao/.agents/skills/quality/SKILL.md", "active")
        self.write("rag/traducao/harness/vendor/sample/SKILL.md", "dependency")
        module = adapter.configure_inventory()
        self.assertEqual(module.discover_t1_skills(self.root), [active])
        self.assertEqual(len(module.discover_t0(self.root)), 2)

    def test_portuguese_decisions_cannot_be_opted_into_scoring(self):
        adapter.configure_inventory()
        import doc_scope

        decision = self.write("docs/governanca/DECISOES.md", "decisions")
        policy = self.write("docs/governanca/POLITICA.md", "rules")
        kept, report = doc_scope.filter_t2_paths(
            self.root,
            [decision, policy],
            include_docs={"docs/governanca/DECISOES.md"},
            include_doc_types={"docs/governanca"},
        )
        self.assertEqual(kept, [policy])
        self.assertEqual(
            report["excluded_decision_records"][0]["path"], "docs/governanca/DECISOES.md"
        )

    def test_portuguese_relative_mandatory_reader_blocks_slim(self):
        adapter.load("merge_usefulness")
        adapter.configure_fanin()
        import slim_fanin

        self.write("rag/traducao/AGENTS.md", "Antes de trabalhar, ler `MASTER-AGENTES.md`.\n")
        self.write("rag/traducao/MASTER-AGENTES.md", "checklist")
        hits = slim_fanin.find_mandate_fanin(self.root, "rag/traducao/MASTER-AGENTES.md")
        self.assertTrue(any(h["citer"] == "rag/traducao/AGENTS.md" for h in hits))

    def test_readme_is_not_fanin_evidence_and_mere_cite_is_not_mandatory(self):
        adapter.load("merge_usefulness")
        adapter.configure_fanin()
        import slim_fanin

        self.write("AGENTS.md", "Índice: docs/governanca/POLITICA.md\n")
        self.write("rag/traducao/AGENTS.md", "Índice\n")
        self.write("docs/governanca/POLITICA.md", "policy")
        self.write("README.md", "Leia docs/governanca/POLITICA.md\n")
        self.assertEqual(
            slim_fanin.find_mandate_fanin(self.root, "docs/governanca/POLITICA.md"), []
        )

    def test_surface_scores_use_heading_deck_and_table_rows(self):
        self.write("surfaces.md", "### S001 | T0 | real\n### S901 | T1 | calibration\n")
        self.write("scores.md", "> model: inherited\n| S001 | KEEP-CORE |\n| S901 | SLIM |\n")
        adapter.require_scores(
            self.root, ("scores.md",), "surfaces.md", r"^###\s+(S\d{3})\b", r"^\|\s*(S\d{3})\s*\|"
        )

    def test_incomplete_duplicate_or_extra_scores_block_merge(self):
        self.write("claims.md", "| C001 | x |\n| P003 | x |\n")
        for rows in (
            "| C001 | x |\n",
            "| C001 | x |\n| C001 | x |\n| P003 | x |\n",
            "| C001 | x |\n| P003 | x |\n| C999 | x |\n",
        ):
            with self.subTest(rows=rows):
                self.write("scores.md", "> model: inherited\n" + rows)
                with self.assertRaises(ValueError):
                    adapter.require_scores(
                        self.root, ("scores.md",), "claims.md", r"^\|\s*([CP]\d{3})\s*\|"
                    )

    def test_invalid_class_or_cost_cannot_reach_ship(self):
        for row in (
            "| C001 | 2 | REDUNDANT-CODE | evidence | high | cut |",
            "| C001 | 0 | NOT-A-CLASS | evidence | high | cut |",
        ):
            with self.subTest(row=row):
                self.write("scores.md", row)
                with self.assertRaises(ValueError):
                    adapter.require_rubric(self.root, ("scores.md",), "B")

    def test_partial_usefulness_row_cannot_merge(self):
        self.write("scores.md", "| S001 | MIXED |")
        with self.assertRaises(ValueError):
            adapter.require_rubric(self.root, ("scores.md",), "C")

    def prepare_scope(self, tracks="ABC"):
        run = self.root / ".harness-eval/runs/test"
        run.mkdir(parents=True)
        source = self.write("AGENTS.md", "rules")
        (run / "evaluation-scope.json").write_text(
            json.dumps(
                {
                    "tracks": tracks,
                    "source_sha256": {"AGENTS.md": hashlib.sha256(source.read_bytes()).hexdigest()},
                }
            )
        )
        return run

    def main(self, *args):
        with (
            patch.object(adapter, "ROOT", self.root),
            patch.object(adapter, "verify_vendor"),
            patch.object(sys, "argv", ["harness_eval.py", *args]),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return adapter.main()

    def test_missing_q1_q2_flags_block_inventory_before_execution(self):
        with self.assertRaises(SystemExit) as caught:
            self.main("inventory", "--run-id", "test")
        self.assertEqual(caught.exception.code, 2)
        self.assertFalse((self.root / ".harness-eval").exists())

    def test_source_change_blocks_evaluation(self):
        self.prepare_scope()
        self.write("AGENTS.md", "modified policy")
        with self.assertRaisesRegex(ValueError, "Superfície mudou"):
            self.main("correctness", "--run-id", "test")

    def test_no_track_a_no_c_and_broken_a_blocks_c(self):
        run = self.prepare_scope()
        with self.assertRaises(SystemExit):
            self.main("surfaces", "--run-id", "test")
        (run / "04-correctness.md").write_text("BROKEN")
        (run / "04-correctness.json").write_text('[{"severity":"BROKEN"}]')
        with self.assertRaisesRegex(ValueError, "Track A contém BROKEN"):
            self.main("surfaces", "--run-id", "test")

    def test_track_not_selected_cannot_execute(self):
        run = self.prepare_scope(tracks="A")
        (run / "04-correctness.md").write_text("clean")
        (run / "04-correctness.json").write_text("[]")
        with self.assertRaises(SystemExit) as caught:
            self.main("surfaces", "--run-id", "test")
        self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
