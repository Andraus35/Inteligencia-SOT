#!/usr/bin/env python3
"""Harness exclusivo da tradução. Sem dependências Python externas ou chamadas LLM."""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
from functools import wraps
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile

STAGE = Path(__file__).resolve().parent.parent
ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}\Z")
NUMBERS = re.compile(r"[+−-]?\d+(?:[.,:/]\d+)*(?:%|‰)?")
ROLES = ("coordenador", "tradutor", "auditor")
ROLE_SPECS = {
    "coordenador": "COORDENADOR.spec.md",
    "tradutor": "TRADUTOR.spec.md",
    "auditor": "AUDITOR.spec.md",
}
ROLE_SKILLS = {
    "coordenador": "translation-coordinator",
    "tradutor": "translation-translator",
    "auditor": "translation-auditor",
}
PROJECT_DOCUMENTS = (
    "AGENTS.md",
    "docs/governanca/POLITICA.md",
    "docs/governanca/LEITURA-AGENTES.md",
    "docs/governanca/CONTRATOS.md",
    "docs/governanca/DECISOES.md",
)
PROJECT_CONTEXT_DOCUMENTS = tuple(
    name for name in PROJECT_DOCUMENTS if name != "docs/governanca/CONTRATOS.md"
)


class GateError(ValueError):
    """Violação de um contrato verificável; execução bloqueada."""


def require(condition, message):
    if not condition:
        raise GateError(message)


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Chave JSON duplicada: {key}")
        result[key] = value
    return result


def read_json(path):
    path = inside(Path(path).relative_to(STAGE))
    require(path.is_file(), "JSON não é arquivo regular")
    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
        parse_constant=lambda x: (_ for _ in ()).throw(GateError(f"JSON inválido: {x}")),
    )


def digest(path):
    path = inside(Path(path).relative_to(STAGE))
    require(path.is_file(), "Artefato não é arquivo regular")
    h = hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def object_hash(value):
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


def inside(relative, base=None):
    base = Path(base or STAGE).resolve()
    path = Path(relative)
    require(not path.is_absolute(), "Caminho absoluto não permitido")
    require(".." not in path.parts, "Traversal não permitido")
    candidate = base / path
    for parent in (candidate, *candidate.parents):
        if parent == base.parent:
            break
        require(not parent.is_symlink(), f"Link simbólico não permitido: {parent.name}")
    resolved = candidate.resolve()
    require(resolved.is_relative_to(base), "Caminho fora da etapa")
    return resolved


def write_json(path, value):
    path = Path(path)
    require(path.resolve().is_relative_to(STAGE), "Escrita fora da etapa")
    require(not path.is_symlink(), "Destino é link simbólico")
    inside(path.relative_to(STAGE))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".atomic-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(value, file, ensure_ascii=False, indent=2, allow_nan=False)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def policy():
    require(STAGE.name == "traducao" and STAGE.parent.name == "rag", "Raiz de etapa inválida")
    value = read_json(STAGE / "harness/policy.json")
    require(
        value["stage"] == "traducao" and value["roles"] == list(ROLES), "Política de etapa inválida"
    )
    require(value["max_agents"] == 3 and value["max_correction_rounds"] == 2, "Limites inválidos")
    require(
        value["critical_open_max"] == 0 and value["major_open_max"] == 0,
        "Gravidade crítica/maior não pode ser dispensada",
    )
    return value


def project_governance():
    """Trusted host reads the approved registry; jobs receive only a bounded snapshot."""
    project = STAGE.parent.parent
    require(
        not (STAGE.parent / "AGENTS.md").exists() and not (STAGE.parent / "AGENTS.md").is_symlink(),
        "Governança intermediária em rag não registrada",
    )
    registry_path = inside("docs/governanca/registro.json", project)
    require(registry_path.is_file(), "Registro de governança geral ausente")
    registry = json.loads(
        registry_path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    version = policy()["project_governance_version"]
    require(
        registry.get("schema_version") == 1 and registry.get("policy_version") == version,
        "Versão de governança geral incompatível",
    )
    require(
        registry.get("status") == "APROVADA" and bool(registry.get("approval_id")),
        "Governança geral sem registro de aprovação",
    )
    hashes = registry.get("documents")
    require(
        isinstance(hashes, dict) and set(hashes) == set(PROJECT_DOCUMENTS),
        "Dependências obrigatórias de governança divergentes",
    )
    documents = {}
    for name in PROJECT_DOCUMENTS:
        path = inside(name, project)
        require(path.is_file(), f"Documento geral ausente: {name}")
        data = path.read_bytes()
        require(
            isinstance(hashes[name], str)
            and re.fullmatch(r"[a-f0-9]{64}", hashes[name])
            and hashlib.sha256(data).hexdigest() == hashes[name],
            f"Governança geral alterada: {name}",
        )
        if name in PROJECT_CONTEXT_DOCUMENTS:
            documents[name] = data.decode("utf-8")
    require(
        documents["AGENTS.md"].splitlines()[0]
        == f"<!-- inteligencia-sot:scope=project; policy={version} -->",
        "Entrada ancestral não declara escopo geral aprovado",
    )
    require(
        f"<!-- inteligencia-sot:policy={version} -->" in documents["docs/governanca/POLITICA.md"],
        "Documento de política geral incompatível",
    )
    return {
        "policy_version": version,
        "approval_id": registry["approval_id"],
        "verified_sha256": hashes,
        "documents": documents,
    }


def run_root(run_id):
    require(bool(ID.fullmatch(run_id)), "ID de execução inválido")
    return inside(Path("runs") / run_id)


def agent_contracts():
    """Read role procedures as data; their hashes bind a run, not human approval."""
    contracts = {}
    for role in ROLES:
        names = (
            "specs/COMUM.md",
            f"specs/{ROLE_SPECS[role]}",
            ".agents/skills/translation-quality/SKILL.md",
            f".agents/skills/{ROLE_SKILLS[role]}/SKILL.md",
        )
        documents = {}
        hashes = {}
        for name in names:
            path = inside(name)
            require(path.is_file(), f"Contrato de agente ausente: {name}")
            data = path.read_bytes()
            require(bool(data.strip()), f"Contrato de agente vazio: {name}")
            documents[name] = data.decode("utf-8")
            hashes[name] = hashlib.sha256(data).hexdigest()
        contracts[role] = {"role": role, "documents": documents, "verified_sha256": hashes}
    return contracts


@contextmanager
def execution_lock(run_id, shared=False):
    run_root(run_id)
    lock_root = inside("work/runtime-locks")
    lock_root.mkdir(parents=True, exist_ok=True)
    path = inside(Path("work/runtime-locks") / f"control-{run_id}.lock")
    with path.open("a") as handle:
        try:
            fcntl.flock(handle, (fcntl.LOCK_SH if shared else fcntl.LOCK_EX) | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise GateError("Execução ocupada; controles e jobs não podem competir") from error
        yield


def controlled(function):
    @wraps(function)
    def wrapped(run_id, *args, **kwargs):
        with execution_lock(run_id):
            return function(run_id, *args, **kwargs)

    return wrapped


def load_run(run_id):
    root = run_root(run_id)
    value = read_json(root / "control/manifest.json")
    require(value["run_id"] == run_id and value["stage"] == "traducao", "Manifesto inválido")
    require(
        value["policy_sha256"] == digest(STAGE / "harness/policy.json"),
        "Política mudou; requer nova execução",
    )
    require(
        value.get("project_governance_sha256") == object_hash(project_governance()),
        "Governança geral mudou ou não foi vinculada; requer nova execução",
    )
    require(
        value.get("agent_contracts_sha256") == object_hash(agent_contracts()),
        "Contrato de agente mudou ou não foi vinculado; requer nova execução",
    )
    source = inside(value["source_path"])
    require(source.is_relative_to(STAGE / "input"), "Fonte fora de input")
    require(digest(source) == value["source_sha256"], "PDF fonte foi alterado")
    return root, value


def save_run(root, value, action):
    value.setdefault("events", []).append(
        {"action": action, "at": datetime.now(timezone.utc).isoformat()}
    )
    write_json(root / "control/manifest.json", value)


@controlled
def init_run(run_id, source_relative, source_language, target_language):
    cfg = policy()
    governance = project_governance()
    contracts = agent_contracts()
    require(source_language.strip() and target_language.strip(), "Idiomas obrigatórios")
    require(source_language != target_language, "Origem e destino devem diferir")
    source = inside(source_relative)
    require(
        source.is_relative_to(STAGE / "input") and source.suffix.lower() == ".pdf",
        "Fonte deve ser PDF em input",
    )
    with source.open("rb") as file:
        require(file.read(5) == b"%PDF-", "Assinatura PDF inválida")
    root = run_root(run_id)
    require(not root.exists(), "Execução já existe; não sobrescrever")
    for folder in ("control", "coordenador", "tradutor", "auditor"):
        (root / folder).mkdir(parents=True)
    value = {
        "schema_version": 1,
        "project": cfg["project"],
        "stage": "traducao",
        "run_id": run_id,
        "source_path": str(source.relative_to(STAGE)),
        "source_sha256": digest(source),
        "source_language": source_language,
        "target_language": target_language,
        "policy_sha256": digest(STAGE / "harness/policy.json"),
        "state": "CREATED",
        "project_governance_sha256": object_hash(governance),
        "agent_contracts_sha256": object_hash(contracts),
        "corrections": {"pilot": 0, "full": 0},
        "accepted": {},
        "events": [],
    }
    save_run(root, value, "init")
    return value


def validate_blocks(blocks):
    require(isinstance(blocks, list) and bool(blocks), "Inventário de blocos vazio/inválido")
    ids = set()
    for block in blocks:
        require(isinstance(block, dict), "Bloco inválido")
        key = block.get("id")
        require(
            isinstance(key, str) and bool(ID.fullmatch(key)) and key not in ids,
            "ID de bloco ausente/duplicado/inválido",
        )
        ids.add(key)
        require(type(block.get("page")) is int and block["page"] > 0, f"Página inválida: {key}")
        require(
            block.get("kind")
            in ("text", "heading", "table", "formula", "code", "caption", "note", "figure"),
            f"Tipo inválido: {key}",
        )
        require(
            isinstance(block.get("text"), str) and bool(block["text"].strip()),
            f"Texto vazio: {key}",
        )
        tokens = block.get("protected_tokens", [])
        require(
            isinstance(tokens, list) and all(isinstance(t, str) and t for t in tokens),
            "Tokens protegidos inválidos",
        )
        if block["kind"] in ("formula", "code"):
            require(
                isinstance(block.get("preserved_content"), str)
                and bool(block["preserved_content"]),
                "Fórmula/código requer preserved_content",
            )
        if block["kind"] == "table":
            cells = block.get("cells")
            require(
                isinstance(cells, list)
                and bool(cells)
                and all(
                    isinstance(r, list) and bool(r) and all(isinstance(c, str) for c in r)
                    for r in cells
                ),
                "Tabela requer células em matriz",
            )
    return ids


@controlled
def freeze_plan(run_id, plan_relative):
    root, manifest = load_run(run_id)
    require(manifest["state"] == "CREATED", "Plano só pode ser congelado em CREATED")
    plan = read_json(inside(plan_relative))
    require(plan.get("schema_version") == 1, "Versão de plano inválida")
    for key in ("source_language", "target_language"):
        require(plan.get(key) == manifest[key], f"Idioma diverge: {key}")
    require(
        isinstance(plan.get("glossary_approved_by"), str) and plan["glossary_approved_by"].strip(),
        "Aprovação do glossário não registrada",
    )
    require(plan.get("privacy") == "local", "Launcher atual só suporta execução local/offline")
    require(
        isinstance(plan.get("tools"), list) and bool(plan["tools"]),
        "Ferramentas e versões obrigatórias",
    )
    require(isinstance(plan.get("models"), list) and bool(plan["models"]), "Modelos obrigatórios")
    require(
        bool(re.fullmatch(r"[a-f0-9]{64}", plan.get("prompt_sha256", ""))),
        "Hash de prompt inválido",
    )
    for tool in plan["tools"]:
        require(
            isinstance(tool, dict) and tool.get("name") and tool.get("version"),
            "Ferramenta sem nome/versão",
        )
    for model in plan["models"]:
        require(
            isinstance(model, dict) and model.get("id") and model.get("parameters") is not None,
            "Modelo sem id/parâmetros",
        )
    glossary = plan.get("glossary")
    require(isinstance(glossary, list), "Glossário inválido")
    terms = set()
    for entry in glossary:
        require(
            isinstance(entry, dict)
            and isinstance(entry.get("source"), str)
            and entry["source"].strip()
            and isinstance(entry.get("target"), str)
            and entry["target"].strip()
            and type(entry.get("mandatory")) is bool,
            "Termo inválido",
        )
        require(entry["source"] not in terms, "Termo duplicado")
        terms.add(entry["source"])
    ids = validate_blocks(plan.get("source_blocks"))
    pilot = plan.get("pilot_block_ids")
    require(
        isinstance(pilot, list)
        and bool(pilot)
        and len(set(pilot)) == len(pilot)
        and set(pilot) <= ids,
        "Piloto inválido",
    )
    destination = root / "coordenador/plan-frozen.json"
    write_json(destination, plan)
    manifest["plan_sha256"] = digest(destination)
    manifest["state"] = "PLANNED"
    save_run(root, manifest, "freeze-plan")
    return manifest


def frozen_plan(root, manifest):
    path = root / "coordenador/plan-frozen.json"
    require(
        manifest.get("plan_sha256") == digest(path),
        "Plano/inventário/glossário congelado foi alterado",
    )
    return read_json(path)


def translation_path(root, batch):
    require(batch in ("pilot", "full"), "Lote inválido")
    return inside((root / "tradutor" / batch / "translation.json").relative_to(STAGE))


def bundle(root, manifest, batch):
    directory = translation_path(root, batch).parent
    require(
        (directory / "translated.pdf").is_file(), "PDF traduzido obrigatório para auditar o lote"
    )
    with (directory / "translated.pdf").open("rb") as file:
        require(file.read(5) == b"%PDF-", "Assinatura do PDF traduzido inválida")
    artifacts = {}
    for path in sorted(directory.rglob("*")):
        require(not path.is_symlink(), "Link simbólico em artefatos")
        if path.is_file():
            artifacts[str(path.relative_to(directory))] = digest(path)
    return object_hash(
        {
            "source_sha256": manifest["source_sha256"],
            "plan_sha256": manifest["plan_sha256"],
            "policy_sha256": manifest["policy_sha256"],
            "batch": batch,
            "artifacts": artifacts,
        }
    )


@controlled
def mark_translated(run_id, batch):
    root, manifest = load_run(run_id)
    frozen_plan(root, manifest)
    expected = "PLANNED" if batch == "pilot" else "PILOT_ACCEPTED"
    correcting = "PILOT_CORRECTING" if batch == "pilot" else "FULL_CORRECTING"
    require(
        manifest["state"] in (expected, correcting), f"Estado esperado: {expected} ou {correcting}"
    )
    if batch == "full":
        require(
            manifest["accepted"]["pilot"] == bundle(root, manifest, "pilot"),
            "Piloto mudou após aprovação",
        )
    read_json(translation_path(root, batch))
    manifest.setdefault("attempt_bundles", {})[batch] = bundle(root, manifest, batch)
    manifest["state"] = "PILOT_TRANSLATED" if batch == "pilot" else "TRANSLATED"
    save_run(root, manifest, f"translated:{batch}")
    return manifest


def numeric_tokens(text):
    return Counter(NUMBERS.findall(text))


def _evaluate(run_id, batch):
    root, manifest = load_run(run_id)
    plan = frozen_plan(root, manifest)
    require(
        manifest["state"] == ("PILOT_TRANSLATED" if batch == "pilot" else "TRANSLATED"),
        "Lote não está pronto para auditoria",
    )
    if batch == "full":
        require(
            manifest["accepted"]["pilot"] == bundle(root, manifest, "pilot"),
            "Piloto mudou após aprovação",
        )
    audit_bundle = bundle(root, manifest, batch)
    require(
        manifest["attempt_bundles"][batch] == audit_bundle, "Artefatos mudaram após mark-translated"
    )
    errors = []
    original = plan["source_blocks"]
    if batch == "pilot":
        original = [x for x in original if x["id"] in plan["pilot_block_ids"]]
    expected = {x["id"]: x for x in original}
    translation = read_json(translation_path(root, batch))
    ids = validate_blocks(translation)
    if ids != set(expected):
        errors.append("Cobertura difere do inventário congelado")
    for item in translation:
        source = expected.get(item["id"])
        if source is None:
            continue
        key = item["id"]
        if item["page"] != source["page"] or item["kind"] != source["kind"]:
            errors.append(f"Localização/tipo divergente: {key}")
        if numeric_tokens(item["text"]) != numeric_tokens(source["text"]):
            errors.append(f"Valores numéricos divergentes: {key}")
        for token in source.get("protected_tokens", []):
            if item["text"].count(token) != source["text"].count(token):
                errors.append(f"Token protegido divergente: {key}: {token}")
        if (
            source["kind"] in ("formula", "code")
            and item.get("preserved_content") != source["preserved_content"]
        ):
            errors.append(f"Fórmula/código alterado: {key}")
        if source["kind"] == "table":
            sc, tc = source["cells"], item["cells"]
            if [len(r) for r in sc] != [len(r) for r in tc]:
                errors.append(f"Estrutura de tabela divergente: {key}")
            else:
                for row_source, row_target in zip(sc, tc):
                    if any(
                        numeric_tokens(a) != numeric_tokens(b)
                        for a, b in zip(row_source, row_target)
                    ):
                        errors.append(f"Valor deslocado/alterado em tabela: {key}")
        for term in plan["glossary"]:

            def occurrences(term_text: str, text: str) -> int:
                return len(
                    re.findall(r"(?<!\w)" + re.escape(term_text) + r"(?!\w)", text, re.IGNORECASE)
                )

            if term["mandatory"] and occurrences(term["source"], source["text"]) > occurrences(
                term["target"], item["text"]
            ):
                errors.append(f"Termo obrigatório ausente: {key}: {term['source']}")
    report_path = root / "auditor" / batch / "review.json"
    review = read_json(report_path)
    require(
        review.get("schema_version") == 1
        and review.get("role") == "auditor"
        and review.get("reviewer"),
        "Revisor independente não identificado",
    )
    require(
        review.get("batch") == batch and review.get("bundle_sha256") == audit_bundle,
        "Auditoria ausente/desatualizada: hash do bundle diverge",
    )
    reviewed = review.get("reviewed_block_ids")
    require(
        isinstance(reviewed, list)
        and len(set(reviewed)) == len(reviewed)
        and set(reviewed) == set(expected),
        "Auditoria não cobriu todos os blocos do lote",
    )
    checks = review.get("checks", {})
    for check in policy()["required_review_checks"]:
        if checks.get(check) is not True:
            errors.append(f"Revisão obrigatória não concluída: {check}")
    findings = review.get("findings")
    require(isinstance(findings, list), "Achados inválidos")
    seen = set()
    for finding in findings:
        require(isinstance(finding, dict), "Achado inválido")
        require(finding.get("id") and finding["id"] not in seen, "ID de achado ausente/duplicado")
        seen.add(finding["id"])
        require(finding.get("severity") in ("critical", "major", "minor"), "Gravidade inválida")
        require(
            finding.get("status") in ("open", "resolved", "accepted"), "Estado do achado inválido"
        )
        require(
            finding.get("block_id") in expected
            and finding.get("source_evidence")
            and finding.get("translation_evidence")
            and finding.get("reason"),
            "Achado sem localização/evidência",
        )
        require(
            finding["status"] != "accepted"
            or (finding["severity"] == "minor" and finding.get("accepted_by")),
            "Somente erro menor pode ser aceito explicitamente",
        )
        require(
            finding["status"] != "resolved" or finding.get("resolution_evidence"),
            "Correção sem evidência de resolução",
        )
        if finding["status"] == "open":
            errors.append(f"Achado aberto: {finding['id']} ({finding['severity']})")
    require(audit_bundle == bundle(root, manifest, batch), "Artefatos mudaram durante a auditoria")
    result = {
        "run_id": run_id,
        "stage": "traducao",
        "batch": batch,
        "bundle_sha256": audit_bundle,
        "review_sha256": digest(report_path),
        "passed": not errors,
        "errors": errors,
        "limits": "Checks sintáticos e declaração de auditoria; não prova equivalência semântica ou identidade humana.",
    }
    write_json(root / "control" / f"gate-{batch}.json", result)
    manifest["last_gate"] = {
        "batch": batch,
        "passed": result["passed"],
        "bundle_sha256": result["bundle_sha256"],
    }
    if result["passed"]:
        manifest["accepted"][batch] = result["bundle_sha256"]
        manifest.setdefault("accepted_reviews", {})[batch] = result["review_sha256"]
        manifest["state"] = "PILOT_ACCEPTED" if batch == "pilot" else "ACCEPTED"
    else:
        manifest["state"] = "PILOT_FAILED" if batch == "pilot" else "FULL_FAILED"
    save_run(root, manifest, f"gate:{batch}:{result['passed']}")
    return result


@controlled
def evaluate(run_id, batch):
    root, manifest = load_run(run_id)
    require(
        manifest["state"] == ("PILOT_TRANSLATED" if batch == "pilot" else "TRANSLATED"),
        "Lote fora da etapa de auditoria",
    )
    try:
        return _evaluate(run_id, batch)
    except (GateError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        manifest["state"] = "PILOT_FAILED" if batch == "pilot" else "FULL_FAILED"
        manifest["last_gate"] = {"batch": batch, "passed": False, "error": str(error)}
        save_run(root, manifest, f"invalid-gate:{batch}")
        raise


@controlled
def correct(run_id, batch, reason):
    root, manifest = load_run(run_id)
    frozen_plan(root, manifest)
    require(
        manifest["state"] == ("PILOT_FAILED" if batch == "pilot" else "FULL_FAILED"),
        "Correção exige lote reprovado",
    )
    require(
        manifest.get("last_gate", {}).get("batch") == batch
        and manifest["last_gate"]["passed"] is False,
        "Correção requer reprovação registrada",
    )
    require(reason.strip(), "Motivo de correção obrigatório")
    require(
        manifest["corrections"][batch] < policy()["max_correction_rounds"],
        "Limite de duas correções atingido; decisão do usuário necessária",
    )
    manifest["corrections"][batch] += 1
    snapshot = root / "control" / f"before-correction-{batch}-{manifest['corrections'][batch]}.json"
    previous = translation_path(root, batch)
    record = {"reason": reason, "translation_exists": previous.exists()}
    if previous.exists():
        require(previous.is_file(), "Artefato de tradução não é arquivo regular")
        raw = previous.read_bytes()
        record.update(
            {
                "translation_raw_hex": raw.hex(),
                "translation_sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
    # Preserve malformed bytes or an explicit absence; repair must not require valid JSON.
    write_json(snapshot, record)
    manifest.pop("last_gate", None)
    manifest["state"] = "PILOT_CORRECTING" if batch == "pilot" else "FULL_CORRECTING"
    save_run(root, manifest, f"correction:{batch}")
    return manifest


@controlled
def deliver(run_id):
    root, manifest = load_run(run_id)
    frozen_plan(root, manifest)
    require(manifest["state"] == "ACCEPTED", "Entrega exige ACCEPTED")
    for batch in ("pilot", "full"):
        require(
            manifest["accepted"][batch] == bundle(root, manifest, batch),
            f"Tradução {batch} mudou após auditoria",
        )
        require(
            manifest["accepted_reviews"][batch] == digest(root / "auditor" / batch / "review.json"),
            f"Revisão {batch} mudou após auditoria",
        )
        require(
            read_json(root / "auditor" / batch / "review.json")["bundle_sha256"]
            == manifest["accepted"][batch],
            "Revisão não corresponde ao bundle aceito",
        )
    manifest["state"] = "DELIVERED"
    save_run(root, manifest, "deliver-structured-bundle")
    return manifest


def docker_base():
    env = os.environ.copy()
    for key in (
        "DOCKER_HOST",
        "DOCKER_CONTEXT",
        "DOCKER_TLS",
        "DOCKER_TLS_VERIFY",
        "DOCKER_CERT_PATH",
    ):
        env.pop(key, None)
    return ["docker", "--host=unix:///var/run/docker.sock"], env


def launch_command(run_id, role, command):
    root, manifest = load_run(run_id)
    require(role in ROLES, "Papel inválido")
    allowed = {
        "coordenador": ("CREATED", "PLANNED"),
        "tradutor": ("PLANNED", "PILOT_ACCEPTED", "PILOT_CORRECTING", "FULL_CORRECTING"),
        "auditor": ("PILOT_TRANSLATED", "TRANSLATED"),
    }
    require(manifest["state"] in allowed[role], "Papel não autorizado neste estado")
    if not (role == "coordenador" and manifest["state"] == "CREATED"):
        frozen_plan(root, manifest)
    require(command and all(isinstance(c, str) for c in command), "Comando obrigatório")
    cfg = policy()["runtime"]
    require(
        cfg["network"] == "none"
        and cfg["readonly_root"] is True
        and re.fullmatch(r"python@sha256:[a-f0-9]{64}", cfg["image"]),
        "Runtime deve estar fixado, readonly e sem rede",
    )
    # Symlinks in the exposed tree are refused, including dependency/source links.
    require(not any(p.is_symlink() for p in STAGE.rglob("*")), "Link simbólico presente na etapa")
    workspace = inside(Path("work") / run_id / role)
    for part in ("tmp", "cache"):
        (workspace / part).mkdir(parents=True, exist_ok=True)
    contracts = agent_contracts()
    require(
        object_hash(contracts) == manifest["agent_contracts_sha256"],
        "Contrato de agente mudou durante preparação do contexto",
    )
    context = {
        "stage": "traducao",
        "role": role,
        "run_id": run_id,
        "source_sha256": manifest["source_sha256"],
        "agent_contract": contracts[role],
        "instructions": (STAGE / "AGENTS.md").read_text(),
        "project_governance": project_governance(),
        "manual": (STAGE / "README-HARNESS.md").read_text(),
        "masters": {
            name: (STAGE / name).read_text()
            for name in ("MASTER-AGENTES.md", "MASTER-PROJETO-TRADUCAO.md")
        },
    }
    require(
        object_hash(context["project_governance"]) == manifest["project_governance_sha256"],
        "Governança geral mudou durante preparação do contexto",
    )
    require(
        object_hash(agent_contracts()) == manifest["agent_contracts_sha256"],
        "Contrato de agente mudou durante preparação do contexto",
    )
    write_json(workspace / "context.json", context)
    base, env = docker_base()
    # No inherited GitHub/API credentials, docker socket or parent workspace mounts.
    argv = base + [
        "run",
        "--rm",
        "--pull=never",
        "--network=none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--pids-limit",
        str(cfg["pids_limit"]),
        "--memory",
        cfg["memory"],
        "--cpus",
        cfg["cpus"],
        "--user",
        f"{os.getuid()}:{os.getgid()}",
        "--mount",
        f"type=bind,src={STAGE},dst=/stage,readonly",
        "--mount",
        f"type=bind,src={root / role},dst=/stage/runs/{run_id}/{role}",
        "--mount",
        f"type=bind,src={workspace},dst=/scratch",
        "--mount",
        f"type=bind,src={workspace / 'context.json'},dst=/scratch/context.json,readonly",
        "--mount",
        f"type=bind,src={workspace / 'tmp'},dst=/tmp",
        "--workdir",
        "/stage",
        "--env",
        "PYTHONDONTWRITEBYTECODE=1",
        "--env",
        "XDG_CACHE_HOME=/scratch/cache",
        "--env",
        "TMPDIR=/tmp",
        "--env",
        "TRANSLATION_CONTEXT=/scratch/context.json",
        cfg["image"],
        *command,
    ]
    return argv, env


def launch(run_id, role, command, timeout=900):
    require(0 < timeout <= 900, "Timeout inválido")
    require(shutil.which("docker") is not None, "Docker indisponível; sem fallback sem sandbox")
    # Serial launch is deliberate: this document workflow is sequential.
    # A stage-wide lock and daemon labels also reject orphan containers after a crash.
    lock_root = inside(Path("work") / "runtime-locks")
    lock_root.mkdir(parents=True, exist_ok=True)
    stage_label = object_hash(str(STAGE))[:16]
    require(ID.fullmatch(run_id) and role in ROLES, "Execução/papel inválido")
    name = f"traducao-{stage_label}-{run_id}-{role}"
    base, env = docker_base()
    with (
        execution_lock(run_id, shared=True),
        (lock_root / "stage-job.lock").open("a") as stage_lock,
    ):
        try:
            fcntl.flock(stage_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise GateError("Job desta etapa já ativo; execução documental é sequencial") from error
        quarantine = inside("work/runtime-quarantine.json")
        require(
            not quarantine.exists(),
            "Runtime em quarentena; verificar containers antes de recuperar",
        )
        active = subprocess.run(
            base + ["ps", "-aq", "--filter", f"label=translation-harness={stage_label}"],
            env=env,
            check=True,
            text=True,
            capture_output=True,
        )
        require(
            not active.stdout.strip(),
            "Container órfão da etapa detectado; recuperação explícita necessária",
        )
        argv, env = launch_command(run_id, role, command)
        position = argv.index("run") + 1
        argv[position:position] = ["--name", name, "--label", f"translation-harness={stage_label}"]
        previous_handler = signal.getsignal(signal.SIGTERM)

        def interrupted(signum, frame):
            raise KeyboardInterrupt("Runtime interrompido")

        signal.signal(signal.SIGTERM, interrupted)
        try:
            return subprocess.run(argv, env=env, check=False, timeout=timeout).returncode
        finally:
            # Timeout/interrupt kills the Docker client, so explicitly stop its container.
            try:
                subprocess.run(
                    base + ["rm", "-f", name], env=env, text=True, capture_output=True, timeout=30
                )
                remaining = subprocess.run(
                    base + ["ps", "-aq", "--filter", f"name=^/{name}$"],
                    env=env,
                    check=True,
                    text=True,
                    capture_output=True,
                    timeout=30,
                )
                require(not remaining.stdout.strip(), "Container não foi encerrado")
            except (GateError, subprocess.SubprocessError, OSError) as error:
                write_json(
                    quarantine, {"container": name, "reason": str(error), "stage": "traducao"}
                )
                raise GateError(
                    "Cleanup não confirmado; runtime bloqueado em quarentena"
                ) from error
            finally:
                signal.signal(signal.SIGTERM, previous_handler)


def vendor_check():
    root = STAGE / "harness/vendor"
    for entry in read_json(root / "provenance.json"):
        require(
            digest(inside(entry["path"], root)) == entry["sha256"],
            f"Referência alterada: {entry['path']}",
        )
    return {"vendor_integrity": "PASS"}


def selfcheck():
    policy()
    vendor_check()
    governance = project_governance()
    contracts = agent_contracts()
    required = [
        "AGENTS.md",
        "MASTER-AGENTES.md",
        "MASTER-PROJETO-TRADUCAO.md",
        "README-HARNESS.md",
        "templates/plan.json",
        "templates/review.json",
    ]
    for name in required:
        require(inside(name).is_file(), f"Arquivo obrigatório ausente: {name}")
    require(
        len((STAGE / "AGENTS.md").read_text().splitlines()) <= 150, "AGENTS.md excede 150 linhas"
    )
    return {
        "stage": "traducao",
        "status": "PASS",
        "project_policy_version": governance["policy_version"],
        "agent_contracts_sha256": object_hash(contracts),
        "limits": "Escopo de arquivo + integridade; sandbox exige doctor e testes reais.",
    }


def doctor():
    policy()
    require(shutil.which("docker"), "Docker ausente")
    base, env = docker_base()
    subprocess.run(base + ["info", "--format", "{{.ServerVersion}}"], env=env, check=True)
    subprocess.run(
        base + ["image", "inspect", policy()["runtime"]["image"], "--format", "{{.Id}}"],
        env=env,
        check=True,
    )
    return {"docker": "ready", "stage": "traducao", "network_in_jobs": "none"}


def eval_inventory(run_id):
    require(ID.fullmatch(run_id), "ID inválido")
    vendor_check()
    script = STAGE / "harness/vendor/harness-eval/scripts/inventory_extract.py"
    subprocess.run(
        [
            sys.executable,
            "-B",
            str(script),
            "--root",
            str(STAGE),
            "--run-id",
            run_id,
            "--seed",
            "AGENTS.md",
        ],
        cwd=STAGE,
        check=True,
    )
    return {
        "inventory": f".harness-eval/runs/{run_id}",
        "next": "Ler candidatos; Q1 e Q2 do upstream antes de Track A. Não executar B/C por inferência.",
    }


def score():
    vendor_check()
    binary = STAGE / "harness/vendor/harness-score/dist/cli.js"
    require(binary.is_file(), "CLI harness-score ausente")
    completed = subprocess.run(
        ["node", str(binary), str(STAGE), "--json"],
        cwd=STAGE,
        check=True,
        text=True,
        capture_output=True,
    )
    report = json.loads(completed.stdout)
    report["root"] = "rag/traducao"
    write_json(STAGE / "harness/reports/harness-score.json", report)
    return {
        "tool": report["tool"],
        "level": report["level"],
        "score": report["score"],
        "report": "harness/reports/harness-score.json",
        "limits": "Score de infraestrutura, não de tradução; sem editar regras para aumentar nota.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("doctor", "selfcheck", "score"):
        sub.add_parser(name)
    p = sub.add_parser("eval-inventory")
    p.add_argument("--run-id", required=True)
    p = sub.add_parser("init-run")
    p.add_argument("--run-id", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--source-language", required=True)
    p.add_argument("--target-language", required=True)
    p = sub.add_parser("freeze-plan")
    p.add_argument("--run-id", required=True)
    p.add_argument("--plan", required=True)
    for name in ("mark-translated", "bundle", "gate", "correct"):
        p = sub.add_parser(name)
        p.add_argument("--run-id", required=True)
        p.add_argument("--batch", choices=("pilot", "full"), required=True)
        if name == "correct":
            p.add_argument("--reason", required=True)
    p = sub.add_parser("deliver")
    p.add_argument("--run-id", required=True)
    p = sub.add_parser("launch")
    p.add_argument("--run-id", required=True)
    p.add_argument("--role", choices=ROLES, required=True)
    p.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.cmd in ("doctor", "selfcheck", "score"):
            result = globals()[args.cmd]()
        elif args.cmd == "eval-inventory":
            result = eval_inventory(args.run_id)
        elif args.cmd == "init-run":
            result = init_run(args.run_id, args.source, args.source_language, args.target_language)
        elif args.cmd == "freeze-plan":
            result = freeze_plan(args.run_id, args.plan)
        elif args.cmd == "mark-translated":
            result = mark_translated(args.run_id, args.batch)
        elif args.cmd == "bundle":
            root, manifest = load_run(args.run_id)
            frozen_plan(root, manifest)
            result = {"bundle_sha256": bundle(root, manifest, args.batch)}
        elif args.cmd == "gate":
            result = evaluate(args.run_id, args.batch)
        elif args.cmd == "correct":
            result = correct(args.run_id, args.batch, args.reason)
        elif args.cmd == "deliver":
            result = deliver(args.run_id)
        elif args.cmd == "launch":
            command = args.command[1:] if args.command[:1] == ["--"] else args.command
            return launch(args.run_id, args.role, command)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.cmd == "gate" and not result["passed"] else 0
    except (
        GateError,
        OSError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
