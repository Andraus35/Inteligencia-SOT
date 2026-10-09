"""Regressão de gates e isolamento. Fixtures sintéticas não são tradução real."""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

MODULE = Path(__file__).resolve().parents[1] / "harness.py"
spec = importlib.util.spec_from_file_location("translation_harness", MODULE)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
REAL_STAGE = h.STAGE


class HarnessTests(unittest.TestCase):
    def setUp(self):
        work = REAL_STAGE / "work"
        work.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=work, prefix="test-")
        self.base = Path(self.temporary.name)
        self.stage = self.base / "project/rag/traducao"
        (self.stage / "input").mkdir(parents=True)
        (self.stage / "harness").mkdir()
        for name in (
            "AGENTS.md",
            "MASTER-AGENTES.md",
            "MASTER-PROJETO-TRADUCAO.md",
            "README-HARNESS.md",
            "harness/policy.json",
        ):
            shutil.copyfile(REAL_STAGE / name, self.stage / name)
        for name in (*h.PROJECT_DOCUMENTS, "docs/governanca/registro.json"):
            target = self.stage.parent.parent / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REAL_STAGE.parent.parent / name, target)
        h.STAGE = self.stage
        (self.stage / "input/source.pdf").write_bytes(
            b"%PDF-1.7\nsynthetic fixture, not a document\n"
        )
        self.original = [
            {
                "id": "b1",
                "page": 1,
                "kind": "text",
                "text": "Stop above 10 USD.",
                "protected_tokens": ["USD"],
            },
            {
                "id": "b2",
                "page": 1,
                "kind": "table",
                "text": "Entry 20, Exit 30",
                "cells": [["Entry", "20"], ["Exit", "30"]],
            },
            {
                "id": "b3",
                "page": 2,
                "kind": "formula",
                "text": "Risk = 2 * capital",
                "preserved_content": "R=2*C",
            },
        ]
        self.translated = copy.deepcopy(self.original)
        self.translated[0]["text"] = "Stop acima de 10 USD."
        self.translated[1]["text"] = "Entrada 20, Saída 30"
        self.translated[1]["cells"] = [["Entrada", "20"], ["Saída", "30"]]
        self.translated[2]["text"] = "Risco = 2 * capital"
        self.plan = {
            "schema_version": 1,
            "source_language": "en",
            "target_language": "pt-BR",
            "privacy": "local",
            "glossary_approved_by": "synthetic-test-user",
            "glossary": [{"source": "Stop", "target": "Stop", "mandatory": True}],
            "source_blocks": self.original,
            "pilot_block_ids": [x["id"] for x in self.original],
            "tools": [{"name": "synthetic-extractor", "version": "fixture-1"}],
            "models": [{"id": "synthetic-test-no-model-call", "parameters": {}}],
            "prompt_sha256": "a" * 64,
        }
        h.init_run("case", "input/source.pdf", "en", "pt-BR")
        self.root = h.run_root("case")

    def tearDown(self):
        h.STAGE = REAL_STAGE
        self.temporary.cleanup()

    def freeze(self):
        h.write_json(self.root / "coordenador/plan.json", self.plan)
        h.freeze_plan("case", "runs/case/coordenador/plan.json")

    def rewrite_registry(self, **changes):
        path = self.stage.parent.parent / "docs/governanca/registro.json"
        registry = json.loads(path.read_text())
        registry.update(changes)
        path.write_text(json.dumps(registry))

    def test_general_governance_is_bound_and_scoped(self):
        governance = h.project_governance()
        self.assertEqual(governance["policy_version"], "1.0.0")
        self.assertEqual(set(governance["documents"]), set(h.PROJECT_CONTEXT_DOCUMENTS))
        self.assertEqual(
            h.load_run("case")[1]["project_governance_sha256"], h.object_hash(governance)
        )

    def test_general_policy_mutation_blocks_control(self):
        path = self.stage.parent.parent / "docs/governanca/POLITICA.md"
        path.write_text(path.read_text() + "\nAltered without approved registration")
        with self.assertRaisesRegex(h.GateError, "Governança geral alterada"):
            h.load_run("case")

    def test_missing_general_dependency_blocks_launch(self):
        self.freeze()
        (self.stage.parent.parent / "docs/governanca/LEITURA-AGENTES.md").unlink()
        with self.assertRaisesRegex(h.GateError, "Documento geral ausente"):
            h.launch_command("case", "tradutor", ["python", "-c", "pass"])

    def test_incompatible_general_policy_blocks(self):
        self.rewrite_registry(policy_version="2.0.0")
        with self.assertRaisesRegex(h.GateError, "incompatível"):
            h.project_governance()

    def test_general_policy_requires_approval_record(self):
        self.rewrite_registry(status="PROPOSTA", approval_id=None)
        with self.assertRaisesRegex(h.GateError, "aprovação"):
            h.project_governance()

    def test_translation_cannot_be_promoted_to_project_scope(self):
        root = self.stage.parent.parent
        (root / "AGENTS.md").write_bytes((self.stage / "AGENTS.md").read_bytes())
        registry = json.loads((root / "docs/governanca/registro.json").read_text())
        registry["documents"]["AGENTS.md"] = hashlib.sha256(
            (root / "AGENTS.md").read_bytes()
        ).hexdigest()
        self.rewrite_registry(documents=registry["documents"])
        with self.assertRaisesRegex(h.GateError, "escopo geral"):
            h.project_governance()

    def test_intermediate_governance_and_symlink_are_rejected(self):
        path = self.stage.parent / "AGENTS.md"
        path.write_text("translation instructions")
        with self.assertRaisesRegex(h.GateError, "intermediária"):
            h.project_governance()
        path.unlink()
        policy = self.stage.parent.parent / "docs/governanca/POLITICA.md"
        saved = self.base / "external-policy.md"
        saved.write_bytes(policy.read_bytes())
        policy.unlink()
        policy.symlink_to(saved)
        with self.assertRaisesRegex(h.GateError, "Link simbólico"):
            h.project_governance()

    def test_registered_change_still_invalidates_old_run(self):
        root = self.stage.parent.parent
        path = root / "docs/governanca/POLITICA.md"
        path.write_text(path.read_text() + "\nNew approved content fixture")
        registry = json.loads((root / "docs/governanca/registro.json").read_text())
        registry["documents"]["docs/governanca/POLITICA.md"] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        self.rewrite_registry(documents=registry["documents"])
        with self.assertRaisesRegex(h.GateError, "requer nova execução"):
            h.load_run("case")

    def test_legacy_run_is_not_migrated_silently(self):
        path = self.root / "control/manifest.json"
        manifest = h.read_json(path)
        del manifest["project_governance_sha256"]
        h.write_json(path, manifest)
        with self.assertRaisesRegex(h.GateError, "não foi vinculada"):
            h.load_run("case")

    def prepare(self, batch="pilot", blocks=None):
        if batch == "pilot":
            self.freeze()
        h.write_json(h.translation_path(self.root, batch), blocks or self.translated)
        (h.translation_path(self.root, batch).parent / "translated.pdf").write_bytes(
            b"%PDF-1.7\nsynthetic translated fixture\n"
        )
        h.mark_translated("case", batch)
        self.review(batch)

    def review(self, batch="pilot"):
        _, manifest = h.load_run("case")
        report = {
            "schema_version": 1,
            "role": "auditor",
            "reviewer": "synthetic-auditor",
            "batch": batch,
            "bundle_sha256": h.bundle(self.root, manifest, batch),
            "reviewed_block_ids": [x["id"] for x in self.original],
            "checks": {x: True for x in h.policy()["required_review_checks"]},
            "findings": [],
            "limitations": "Fixture only",
        }
        h.write_json(self.root / f"auditor/{batch}/review.json", report)
        return report

    def test_happy_flow_with_fresh_independent_reviews(self):
        self.prepare()
        self.assertTrue(h.evaluate("case", "pilot")["passed"])
        self.prepare("full")
        self.assertTrue(h.evaluate("case", "full")["passed"])
        self.assertEqual(h.deliver("case")["state"], "DELIVERED")

    def test_coordinator_can_prepare_plan_before_freeze(self):
        self.assertTrue(h.launch_command("case", "coordenador", ["python", "-c", "pass"])[0])
        for role in ("tradutor", "auditor"):
            with self.assertRaises(h.GateError):
                h.launch_command("case", role, ["python", "-c", "pass"])

    def test_malformed_translation_can_enter_correction_with_raw_snapshot(self):
        self.prepare()
        path = h.translation_path(self.root, "pilot")
        path.write_bytes(b"{broken-json")
        with self.assertRaises((h.GateError, json.JSONDecodeError)):
            h.evaluate("case", "pilot")
        self.assertEqual(
            h.correct("case", "pilot", "Repair malformed output")["state"], "PILOT_CORRECTING"
        )
        snapshot = h.read_json(self.root / "control/before-correction-pilot-1.json")
        self.assertEqual(bytes.fromhex(snapshot["translation_raw_hex"]), b"{broken-json")
        self.assertTrue(h.launch_command("case", "tradutor", ["python", "-c", "pass"])[0])
        h.write_json(path, self.translated)
        h.mark_translated("case", "pilot")
        self.review()
        self.assertTrue(h.evaluate("case", "pilot")["passed"])

    def test_missing_translation_can_enter_correction_with_absence_snapshot(self):
        self.prepare()
        h.translation_path(self.root, "pilot").unlink()
        with self.assertRaises((h.GateError, OSError)):
            h.evaluate("case", "pilot")
        h.correct("case", "pilot", "Restore missing output")
        snapshot = h.read_json(self.root / "control/before-correction-pilot-1.json")
        self.assertFalse(snapshot["translation_exists"])
        self.assertTrue(h.launch_command("case", "tradutor", ["python", "-c", "pass"])[0])

    def test_absolute_and_parent_traversal_rejected(self):
        for path in ("/workspace/foreign.txt", "../../outside", "input/../source.pdf"):
            with self.assertRaises(h.GateError):
                h.inside(path)

    def test_symlink_escape_rejected(self):
        (self.stage / "input/escape").symlink_to(self.base)
        with self.assertRaises(h.GateError):
            h.inside("input/escape/anything")

    def test_pdf_mutation_invalidates_run(self):
        (self.stage / "input/source.pdf").write_bytes(b"%PDF-changed")
        with self.assertRaises(h.GateError):
            h.load_run("case")

    def test_incomplete_plan_rejected(self):
        self.plan["glossary_approved_by"] = ""
        with self.assertRaises(h.GateError):
            self.freeze()

    def test_unknown_or_duplicate_blocks_rejected(self):
        self.prepare()
        blocks = self.translated + [self.translated[0]]
        h.write_json(h.translation_path(self.root, "pilot"), blocks)
        with self.assertRaises(h.GateError):
            h.evaluate("case", "pilot")

    def test_omission_rejected_even_with_positive_review(self):
        self.prepare(blocks=self.translated[:2])
        self.assertFalse(h.evaluate("case", "pilot")["passed"])

    def test_number_change_rejected(self):
        blocks = copy.deepcopy(self.translated)
        blocks[0]["text"] = "Stop acima de 100 USD."
        self.prepare(blocks=blocks)
        self.assertFalse(h.evaluate("case", "pilot")["passed"])

    def test_protected_unit_change_rejected(self):
        blocks = copy.deepcopy(self.translated)
        blocks[0]["text"] = "Stop acima de 10 EUR."
        self.prepare(blocks=blocks)
        self.assertFalse(h.evaluate("case", "pilot")["passed"])

    def test_swapped_table_cells_rejected(self):
        blocks = copy.deepcopy(self.translated)
        blocks[1]["cells"] = [["Entrada", "30"], ["Saída", "20"]]
        self.prepare(blocks=blocks)
        self.assertFalse(h.evaluate("case", "pilot")["passed"])

    def test_formula_change_rejected(self):
        blocks = copy.deepcopy(self.translated)
        blocks[2]["preserved_content"] = "R=3*C"
        self.prepare(blocks=blocks)
        self.assertFalse(h.evaluate("case", "pilot")["passed"])

    def test_glossary_mismatch_rejected(self):
        blocks = copy.deepcopy(self.translated)
        blocks[0]["text"] = "Parada acima de 10 USD."
        self.prepare(blocks=blocks)
        self.assertFalse(h.evaluate("case", "pilot")["passed"])

    def test_stale_review_rejected(self):
        self.prepare()
        blocks = copy.deepcopy(self.translated)
        blocks[0]["text"] += " Alteração."
        h.write_json(h.translation_path(self.root, "pilot"), blocks)
        with self.assertRaises(h.GateError):
            h.evaluate("case", "pilot")

    def test_unknown_severity_not_silently_accepted(self):
        self.prepare()
        review = self.review()
        review["findings"] = [{"id": "f1", "severity": "critcal", "status": "open"}]
        h.write_json(self.root / "auditor/pilot/review.json", review)
        with self.assertRaises(h.GateError):
            h.evaluate("case", "pilot")

    def test_semantic_check_false_blocks(self):
        self.prepare()
        review = self.review()
        review["checks"]["conditions"] = False
        h.write_json(self.root / "auditor/pilot/review.json", review)
        self.assertFalse(h.evaluate("case", "pilot")["passed"])

    def test_critical_findings_block_and_cannot_be_waived(self):
        self.prepare()
        review = self.review()
        finding = {
            "id": "f1",
            "block_id": "b1",
            "severity": "critical",
            "status": "open",
            "source_evidence": "above",
            "translation_evidence": "abaixo",
            "reason": "inversão",
        }
        review["findings"] = [finding]
        h.write_json(self.root / "auditor/pilot/review.json", review)
        self.assertFalse(h.evaluate("case", "pilot")["passed"])
        finding.update(status="accepted", accepted_by="coordinator")
        h.correct("case", "pilot", "synthetic correction")
        h.mark_translated("case", "pilot")
        h.write_json(self.root / "auditor/pilot/review.json", review)
        with self.assertRaises(h.GateError):
            h.evaluate("case", "pilot")

    def test_two_corrections_limit(self):
        self.prepare()
        review = self.review()
        review["checks"]["meaning"] = False
        h.write_json(self.root / "auditor/pilot/review.json", review)
        for count in range(2):
            self.assertFalse(h.evaluate("case", "pilot")["passed"])
            h.correct("case", "pilot", f"synthetic round {count}")
            h.mark_translated("case", "pilot")
        self.assertFalse(h.evaluate("case", "pilot")["passed"])
        with self.assertRaises(h.GateError):
            h.correct("case", "pilot", "third")

    def test_full_translation_cannot_skip_pilot(self):
        self.freeze()
        with self.assertRaises(h.GateError):
            h.mark_translated("case", "full")

    def test_plan_mutation_rejected(self):
        self.freeze()
        changed = copy.deepcopy(self.plan)
        changed["pilot_block_ids"] = ["b1"]
        h.write_json(self.root / "coordenador/plan-frozen.json", changed)
        with self.assertRaises(h.GateError):
            h.frozen_plan(self.root, h.load_run("case")[1])

    def test_delivery_rejects_changed_audit(self):
        self.prepare()
        h.evaluate("case", "pilot")
        self.prepare("full")
        h.evaluate("case", "full")
        review = h.read_json(self.root / "auditor/full/review.json")
        review["reviewer"] = "changed"
        h.write_json(self.root / "auditor/full/review.json", review)
        with self.assertRaises(h.GateError):
            h.deliver("case")

    def test_invalid_json_duplicates_rejected(self):
        path = self.root / "coordenador/bad.json"
        path.write_text('{"x":1,"x":2}')
        with self.assertRaises(h.GateError):
            h.read_json(path)

    def test_launcher_has_only_role_mount_and_no_host_credentials(self):
        self.freeze()
        command, env = h.launch_command("case", "tradutor", ["python", "-c", "pass"])
        self.assertIn("--network=none", command)
        self.assertIn("--read-only", command)
        self.assertIn("--cap-drop=ALL", command)
        self.assertNotIn(
            "/var/run/docker.sock", " ".join(x for x in command if x.startswith("type=bind"))
        )
        self.assertTrue(any("dst=/stage/runs/case/tradutor" in x for x in command))
        self.assertFalse(any(x == "GH_TOKEN" or x.startswith("GH_TOKEN=") for x in command))
        mounts = [x for x in command if x.startswith("type=bind")]
        self.assertFalse(any(f"src={self.stage.parent.parent}," in x for x in mounts))
        self.assertTrue(any("dst=/scratch/context.json,readonly" in x for x in mounts))
        context = h.read_json(self.stage / "work/case/tradutor/context.json")
        self.assertEqual(
            h.object_hash(context["project_governance"]),
            h.load_run("case")[1]["project_governance_sha256"],
        )
        self.assertEqual(context["manual"], (self.stage / "README-HARNESS.md").read_text())

    def test_no_unsandboxed_fallback(self):
        self.freeze()
        with mock.patch.object(h.shutil, "which", return_value=None):
            with self.assertRaises(h.GateError):
                h.launch("case", "tradutor", ["python", "-c", "pass"])

    def test_failed_gate_cannot_bypass_registered_correction(self):
        self.prepare()
        review = self.review()
        review["checks"]["conditions"] = False
        h.write_json(self.root / "auditor/pilot/review.json", review)
        h.evaluate("case", "pilot")
        self.review()
        with self.assertRaises(h.GateError):
            h.evaluate("case", "pilot")
        with self.assertRaises(h.GateError):
            h.launch_command("case", "tradutor", ["python", "-c", "pass"])
        h.correct("case", "pilot", "resolve finding")
        self.assertTrue(h.launch_command("case", "tradutor", ["python", "-c", "pass"])[0])

    def test_control_refuses_active_job_lock(self):
        self.freeze()
        with h.execution_lock("case", shared=True):
            with self.assertRaises(h.GateError):
                h.mark_translated("case", "pilot")

    def test_bundle_rejects_symlink_batch_directory(self):
        self.freeze()
        external = self.base / "outside"
        external.mkdir()
        (external / "translation.json").write_text("[]")
        (external / "translated.pdf").write_bytes(b"%PDF-1.7")
        (self.root / "tradutor/pilot").symlink_to(external)
        with self.assertRaises(h.GateError):
            h.bundle(self.root, h.load_run("case")[1], "pilot")

    def test_artifact_mutation_during_gate_cannot_be_accepted(self):
        self.prepare()
        original_numeric = h.numeric_tokens
        changed = False

        def mutate_after_checks(text):
            nonlocal changed
            if not changed:
                changed = True
                (self.root / "tradutor/pilot/translated.pdf").write_bytes(
                    b"%PDF-mutated during check"
                )
            return original_numeric(text)

        with mock.patch.object(h, "numeric_tokens", side_effect=mutate_after_checks):
            with self.assertRaises(h.GateError):
                h.evaluate("case", "pilot")
        self.assertEqual(h.load_run("case")[1]["state"], "PILOT_FAILED")

    @unittest.skipUnless(
        os.environ.get("TRANSLATION_TEST_DOCKER") == "1", "Docker timeout integration opt-in"
    )
    def test_timeout_explicitly_removes_container(self):
        self.freeze()
        with self.assertRaises(h.subprocess.TimeoutExpired):
            h.launch(
                "case", "tradutor", ["python", "-c", "import time; time.sleep(30)"], timeout=0.7
            )
        base, env = h.docker_base()
        result = h.subprocess.run(
            base
            + [
                "ps",
                "-aq",
                "--filter",
                "label=translation-harness=" + h.object_hash(str(h.STAGE))[:16],
            ],
            env=env,
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.stdout.strip(), "")

    @unittest.skipUnless(
        os.environ.get("TRANSLATION_TEST_DOCKER") == "1",
        "Integração Docker opt-in; executar no ambiente com daemon autorizado",
    )
    def test_real_container_blocks_writes_and_network(self):
        self.freeze()
        probe = """import os, pathlib, socket, json, hashlib
denied = 0
for path in ["/stage/AGENTS.md", "/stage/input/source.pdf", "/stage/runs/case/control/manifest.json", "/stage/runs/case/auditor/illegal.json", "/etc/illegal", "/workspace/Sistema-Operacional-de-Trading--SOT/illegal", "/scratch/context.json"]:
    try: pathlib.Path(path).write_text("forbidden")
    except OSError: denied += 1
assert denied == 7, denied
assert not pathlib.Path("/workspace/Sistema-Operacional-de-Trading--SOT").exists()
assert not pathlib.Path("/workspace/Inteligencia-SOT").exists()
assert not pathlib.Path("/docs/governanca").exists()
ctx = json.loads(pathlib.Path(os.environ["TRANSLATION_CONTEXT"]).read_text())
gov = ctx["project_governance"]
assert gov["policy_version"] == "1.0.0"
for name, text in gov["documents"].items():
    assert hashlib.sha256(text.encode()).hexdigest() == gov["verified_sha256"][name]
assert not any(k in os.environ for k in ["GH_TOKEN", "GITHUB_TOKEN", "SOT_AUDITOR_TOKEN"])
pathlib.Path("/stage/runs/case/tradutor/allowed.json").write_text("ok")
try:
    socket.create_connection(("1.1.1.1", 443), timeout=1)
except OSError: pass
else: raise AssertionError("network escaped")
print("sandbox probe PASS: 7 denied writes, readonly governance snapshot, no project/SOT/credentials/network")
"""
        self.assertEqual(h.launch("case", "tradutor", ["python", "-c", probe]), 0)
        self.assertEqual((self.root / "tradutor/allowed.json").read_text(), "ok")


if __name__ == "__main__":
    unittest.main()
