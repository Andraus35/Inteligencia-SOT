#!/usr/bin/env python3
"""Feedback pós-edição sem reescrita automática: lint, governança e diff."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        data = json.loads(sys.stdin.read(1024 * 1024))
        if not isinstance(data, dict) or data.get("hook_event_name") != "PostToolUse":
            raise ValueError("Evento inválido")
        if data.get("tool_name") not in {"Edit", "Write"}:
            raise ValueError("Ferramenta inválida")
        if not isinstance(data.get("tool_input"), dict):
            raise ValueError("Payload inválido")
    except (ValueError, OSError):
        print("Feedback bloqueado: payload inválido.", file=sys.stderr)
        return 2
    try:
        result = subprocess.run(["make", "feedback"], cwd=ROOT, timeout=50, check=False)
    except (OSError, subprocess.TimeoutExpired):
        print("Feedback indisponível; não declarar validação concluída.", file=sys.stderr)
        return 2
    return 0 if result.returncode == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
