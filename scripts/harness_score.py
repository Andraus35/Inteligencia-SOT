#!/usr/bin/env python3
"""Executa o scanner oficial Paladini pinado, com escopo de repositório e sem ajustes."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "rag/traducao/harness/vendor/harness-score/dist/cli.js"


def verify_vendor() -> None:
    spec = importlib.util.spec_from_file_location(
        "score_translation_harness", ROOT / "rag/traducao/harness/harness.py"
    )
    if spec is None or spec.loader is None:
        raise ValueError("Loader do harness indisponível")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.vendor_check()


def scan(root: Path, minimum: int | None = None) -> tuple[dict[str, Any], int]:
    verify_vendor()
    # Configuração externa não pode reponderar nem desabilitar checks nesta medição.
    if (root / ".harness-score.json").exists():
        raise ValueError("Remova configuração de reponderação; esta medição usa defaults upstream")
    command = ["node", str(CLI), str(root), "--json", "--gate", "maturity"]
    if minimum is not None:
        command += ["--min-level", str(minimum)]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if completed.returncode not in (0, 1):
        raise ValueError("Scanner incompleto ou inválido; código " + str(completed.returncode))
    report: dict[str, Any] = json.loads(completed.stdout)
    if report["tool"] != {"name": "harness-score", "version": "1.8.1"}:
        raise ValueError("Identidade/versão do scanner divergente")
    report["root"] = root.relative_to(ROOT).as_posix()
    return report, completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-level", type=int, choices=range(5))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report, status = scan(ROOT, args.min_level)
    if args.output:
        output = (ROOT / args.output).resolve()
        if not output.is_relative_to(ROOT) or output.suffix != ".json":
            raise ValueError("Relatório deve ser JSON dentro do projeto")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "tool": report["tool"],
                "root": report["root"],
                "level": report["level"],
                "score": report["score"],
                "limits": "Scanner estrutural; não certifica execução de CI, hooks ou tradução.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return status


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError) as error:
        print("BLOCKED:", error, file=sys.stderr)
        sys.exit(2)
