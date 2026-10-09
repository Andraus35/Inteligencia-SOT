#!/usr/bin/env python3
"""Adaptador local do Harness Eval 1.8.3; avaliação sem aplicação automática."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "rag/traducao/harness/vendor/harness-eval"
TOOLS = SKILL / "scripts"
ENTRY_PATHS = ("AGENTS.md", "rag/traducao/AGENTS.md")
CORE_DOCS = ("docs/governanca/POLITICA.md", "docs/governanca/LEITURA-AGENTES.md")
FULL_DOCS = (
    *CORE_DOCS,
    "docs/governanca/CONTRATOS.md",
    "rag/traducao/MASTER-AGENTES.md",
    "rag/traducao/MASTER-PROJETO-TRADUCAO.md",
)
DOC_SETS = {"none": (), "core": CORE_DOCS, "full": FULL_DOCS}


def load(name):
    sys.path.insert(0, str(TOOLS))
    spec = importlib.util.spec_from_file_location("local_eval_" + name, TOOLS / (name + ".py"))
    if spec is None or spec.loader is None:
        raise ValueError("Loader do Harness Eval indisponível")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def active_entries(root):
    return [root / p for p in ENTRY_PATHS if (root / p).is_file()]


def active_skills(root):
    found: set[Path] = set()
    for entry in active_entries(root):
        for folder in (".agents/skills", ".cursor/skills", ".claude/skills"):
            found.update(p for p in (entry.parent / folder).glob("**/SKILL.md") if p.is_file())
    return sorted(found)


def configure_inventory():
    module = load("inventory_extract")
    doc_scope = importlib.import_module("doc_scope")

    native = getattr(doc_scope, "_local_native_exclusion", doc_scope.is_excluded_decision_record)
    setattr(doc_scope, "_local_native_exclusion", native)
    setattr(
        doc_scope,
        "is_excluded_decision_record",
        (lambda p: native(p) or p.replace("\\", "/") == "docs/governanca/DECISOES.md"),
    )
    module.discover_t0 = active_entries
    module.discover_t1_skills = active_skills
    return module


def configure_fanin():
    slim_fanin = importlib.import_module("slim_fanin")

    native_aliases = getattr(slim_fanin, "_local_native_aliases", slim_fanin.path_aliases)
    setattr(slim_fanin, "_local_native_aliases", native_aliases)

    def aliases(root, target, source):
        relative = os.path.relpath(root / target, (root / source).parent).replace("\\", "/")
        return sorted(
            set(native_aliases(root, target, source)) | {relative, "./" + relative},
            key=len,
            reverse=True,
        )

    def corpus(root):
        found = set(active_entries(root))
        for skill in active_skills(root):
            found.update(
                p for p in skill.parent.rglob("*.md") if not p.name.lower().startswith("readme")
            )
        found.update(root / p for p in FULL_DOCS if (root / p).is_file())
        return sorted(found)

    setattr(slim_fanin, "path_aliases", aliases)
    setattr(slim_fanin, "discover_harness_markdown", corpus)
    original = getattr(slim_fanin, "_local_native_mandate", slim_fanin.MANDATE_RE)
    setattr(slim_fanin, "_local_native_mandate", original)
    portuguese = r"\b(?:leia|ler|carregue|carregar|leitura obrigat[oó]ria|fonte de verdade|antes de trabalhar)\b"
    setattr(
        slim_fanin,
        "MANDATE_RE",
        re.compile("(?:" + original.pattern.replace("(?i)", "") + ")|(?:" + portuguese + ")", re.I),
    )


def invoke(module, argv):
    previous = sys.argv
    try:
        sys.argv = [module.__file__, *argv]
        return module.main()
    finally:
        sys.argv = previous


def verify_vendor():
    spec = importlib.util.spec_from_file_location(
        "eval_translation_harness", ROOT / "rag/traducao/harness/harness.py"
    )
    if spec is None or spec.loader is None:
        raise ValueError("Loader do harness de tradução indisponível")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.vendor_check()


def require_scores(run, names, deck_name, pattern, score_pattern=None):
    expected = set(re.findall(pattern, (run / deck_name).read_text(), re.M))
    if not expected:
        raise ValueError("Deck vazio: " + deck_name)
    for name in names:
        text = (run / name).read_text()
        actual = re.findall(score_pattern or pattern, text, re.M)
        if set(actual) != expected or len(actual) != len(set(actual)):
            raise ValueError("Pontuação ausente, duplicada ou fora do deck: " + name)
        if not re.search(r"model:\s*\S", text):
            raise ValueError("Modelo não registrado: " + name)


def require_rubric(run, names, track):
    allowed_b = {
        "REDUNDANT-CODE",
        "REDUNDANT-GENERAL",
        "KEEP-POLICY",
        "KEEP-CAVEAT",
        "KEEP-ROUTING",
        "KEEP-COMPRESSED",
        "UNCLEAR",
    }
    allowed_c = {"KEEP-CORE", "MIXED", "SLIM", "ROUTING-ONLY", "UNCLEAR"}
    for name in names:
        for line in (run / name).read_text().splitlines():
            if not re.match(r"^\|\s*[CPS]\d{3}\s*\|", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if track == "B":
                if (
                    len(cells) != 6
                    or cells[1] not in {"0", "1", "2", "3"}
                    or cells[2] not in allowed_b
                ):
                    raise ValueError("Linha inválida de Track B: " + name + ": " + cells[0])
                if int(cells[1]) >= 2 and cells[2].startswith("REDUNDANT-"):
                    raise ValueError("Custo >= 2 não pode ser REDUNDANT: " + cells[0])
            elif len(cells) != 7 or cells[1] not in allowed_c:
                raise ValueError("Linha inválida de Track C: " + name + ": " + cells[0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action", choices=("inventory", "correctness", "surfaces", "merge-b", "merge-c")
    )
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--docs", choices=tuple(DOC_SETS))
    parser.add_argument("--tracks", choices=("A", "AB", "AC", "ABC"))
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,80}", args.run_id):
        parser.error("run-id inválido")
    run = ROOT / ".harness-eval/runs" / args.run_id
    verify_vendor()
    scope_path = run / "evaluation-scope.json"
    if args.action == "inventory":
        if args.docs is None or args.tracks is None:
            parser.error("registre as escolhas reais Q1/Q2 com --docs e --tracks")
        if scope_path.exists():
            parser.error("run-id já registrado; use um novo ID para preservar o relatório")
        module = configure_inventory()
        argv = ["--root", str(ROOT), "--run-id", args.run_id]
        for path in DOC_SETS[args.docs]:
            argv += ["--include-doc", path]
        result = invoke(module, argv)
        if result:
            return result
        inv = json.loads((run / "inventory.json").read_text())
        import hashlib

        paths = inv["t0"] + inv["t1"] + inv["t2"]
        scope_path.write_text(
            json.dumps(
                {
                    "docs": args.docs,
                    "tracks": args.tracks,
                    "report_only": True,
                    "source_sha256": {
                        p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths
                    },
                    "limits": "Flags registram escolha declarada pelo coordenador, sem autenticação humana; fan-in local inclui português.",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        return 0
    if not scope_path.is_file():
        parser.error("inventário e escolhas Q1/Q2 não registrados")
    scope = json.loads(scope_path.read_text())
    import hashlib

    for path, digest in scope["source_sha256"].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise ValueError("Superfície mudou desde o inventário: " + path)
    if args.action == "correctness":
        result = invoke(load("track_a_correctness"), ["--root", str(ROOT), "--run-id", args.run_id])
        findings = json.loads((run / "04-correctness.json").read_text())
        return result or int(any(f["severity"] == "BROKEN" for f in findings))
    if not (run / "04-correctness.md").is_file():
        parser.error("execute Track A antes de B/C")
    findings = json.loads((run / "04-correctness.json").read_text())
    if any(f["severity"] == "BROKEN" for f in findings):
        raise ValueError("Track A contém BROKEN; corrija e reavalie antes de B/C")
    track = "B" if args.action == "merge-b" else "C"
    if track not in scope["tracks"]:
        parser.error("trilha não selecionada em Q2")
    if args.action == "surfaces":
        return invoke(load("surfaces_extract"), ["--root", str(ROOT), "--run-id", args.run_id])
    if args.action == "merge-b":
        names = ("05-redundancy-j1.md", "06-blind-scores.md")
        require_scores(run, names, "claims.md", r"^\|\s*([CP]\d{3})\s*\|")
        require_rubric(run, names, "B")
        return invoke(load("merge_agreement"), ["--run-dir", str(run)])
    names = ("08-usefulness-j1.md", "09-usefulness-j2.md")
    require_scores(run, names, "surfaces.md", r"^###\s+(S\d{3})\b", r"^\|\s*(S\d{3})\s*\|")
    require_rubric(run, names, "C")
    module = load("merge_usefulness")
    configure_fanin()
    return invoke(module, ["--run-dir", str(run)])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError) as error:
        print("BLOCKED:", error, file=sys.stderr)
        sys.exit(2)
