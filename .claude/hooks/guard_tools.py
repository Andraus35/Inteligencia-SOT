#!/usr/bin/env python3
"""Gate local de ferramentas: valida payload, destruição explícita e caminhos de escrita."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LIMIT = 1024 * 1024
# Defesa em profundidade para padrões explícitos; não é um parser/sandbox de shell.
DANGEROUS = (
    re.compile(r"\brm\s+[^\n;&|]*(?:-\w*[rf]\w*\s+)+(?:/\s*(?:$|[;&|])|/\*|~(?:/\*|\s|$))"),
    re.compile(
        r"\bgit\s+(?:[^\n;&|]*\s)?push\b[^\n;&|]*(?:--force(?:-with-lease)?\b|(?:^|\s)-\w*f\w*\b)"
    ),
    re.compile(r"\bgit\s+reset\s+--hard\b"),
    re.compile(r"\bgit\s+clean\s+[^\n;&|]*-[\w]*[fd][\w]*"),
    re.compile(r"\bDROP\s+(?:TABLE|DATABASE)\b", re.I),
)


def protected_path(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    parts = relative.parts
    return (
        ".git" in parts
        or path.name == ".env"
        or (path.name.startswith(".env.") and path.name != ".env.example")
        or path.suffix.lower() in {".pem", ".key"}
        or relative.is_relative_to("rag/traducao/harness/vendor")
        or relative.is_relative_to("rag/traducao/input")
    )


def decide(payload: dict[str, Any], root: Path = ROOT) -> tuple[bool, str]:
    if payload.get("hook_event_name") != "PreToolUse":
        return False, "Evento inválido; esperado PreToolUse."
    tool = payload.get("tool_name")
    data = payload.get("tool_input")
    if not isinstance(data, dict):
        return False, "Entrada de ferramenta inválida."
    if tool == "Bash":
        command = data.get("command")
        if not isinstance(command, str) or not command.strip():
            return False, "Comando ausente ou inválido."
        if any(pattern.search(command) for pattern in DANGEROUS):
            return (
                False,
                "Operação destrutiva explícita bloqueada; use revisão humana fora do hook.",
            )
        return (
            True,
            "Nenhum padrão destrutivo explícito reconhecido; permissões do executor continuam válidas.",
        )
    if tool in {"Edit", "Write"}:
        value = data.get("file_path")
        if not isinstance(value, str) or not value:
            return False, "Caminho de escrita ausente."
        path = Path(value)
        if not path.is_absolute():
            cwd = payload.get("cwd")
            if not isinstance(cwd, str) or not Path(cwd).is_absolute():
                return False, "Caminho relativo exige cwd absoluto."
            path = Path(cwd) / path
        root = root.resolve()
        if any(parent.is_symlink() for parent in (path, *path.parents)):
            return False, "Escrita por link simbólico não permitida."
        path = path.resolve()
        if not path.is_relative_to(root):
            return False, "Escrita fora do checkout não permitida por este adaptador."
        if protected_path(path, root):
            return False, "Destino protegido: original, dependência, metadados Git ou credencial."
        return True, "Caminho permitido; aprovação de política e governança continuam obrigatórias."
    return False, "Ferramenta inesperada no gate registrado."


def output(allowed: bool, reason: str) -> None:
    if allowed:
        # Ausência de decisão explícita preserva a política de permissões da ferramenta.
        print("{}")
    else:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": reason,
                    }
                },
                ensure_ascii=False,
            )
        )


def main() -> int:
    try:
        text = sys.stdin.read(LIMIT + 1)
        if len(text) > LIMIT:
            raise ValueError("Payload excede o limite")
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("Payload não é objeto")
        allowed, reason = decide(payload)
    except (ValueError, OSError):
        allowed, reason = False, "Payload malformado; operação bloqueada."
    output(allowed, reason)
    return 0  # Claude lê a decisão JSON; deny não deve virar erro ignorado do hook.


if __name__ == "__main__":
    sys.exit(main())
