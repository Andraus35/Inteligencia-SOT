# Redundancy Judge1
> run: bootstrap
> model: codex-gpt-6-inherited (exact API model id not exposed)

27 claims: KEEP-POLICY 15; KEEP-CAVEAT 4; KEEP-ROUTING 4; KEEP-COMPRESSED 2; REDUNDANT-GENERAL 1; UNCLEAR 1; REDUNDANT-CODE 0. Avaliação report-only; nenhum trim aplicado. Custos seguem rediscovery do significado completo, não apenas tokens idênticos em policy.json. Não foram lidos chaves de traps, claims.jsonl, superfícies JSON ou resultados de outro juiz.

| ID | Cost | Class | Evidence | Confidence | Trim suggestion |
|---|---|---|---|---|---|
| C001 | 3 | KEEP-POLICY | AGENTS.md; harness/harness.py:launch_command limita mount e carrega instructions | Alta | Manter fronteira e ressalva Markdown. |
| C002 | 3 | KEEP-ROUTING | AGENTS.md; harness/harness.py:launch_command carrega AGENTS e masters | Alta | Manter checklist de entrada; sem README como evidência. |
| C003 | 1 | KEEP-ROUTING | AGENTS.md aponta .agents/skills/translation-quality/SKILL.md existente | Alta | Manter ponteiro. |
| C004 | 3 | KEEP-POLICY | harness/policy.json roles; harness/harness.py:freeze_plan e launch_command | Alta | Manter autoridade do coordenador. |
| C005 | 3 | KEEP-POLICY | harness/harness.py:launch_command; _evaluate exige role auditor | Alta | Manter separação aprovação/tradução. |
| C006 | 3 | KEEP-POLICY | harness/harness.py:launch_command monta apenas root/role gravável | Alta | Manter independência e proibição de edição. |
| C007 | 3 | KEEP-POLICY | harness/policy.json max_agents; harness/harness.py:launch_command | Alta | Manter limite e versões comuns; limite cognitivo não provado pelo Docker. |
| C008 | 3 | KEEP-POLICY | harness/harness.py:init_run, freeze_plan, validate_blocks; sem gate de prompt injection semântico | Alta | Manter fidelidade e tratamento do PDF como dados. |
| C009 | 3 | KEEP-POLICY | harness/harness.py:_evaluate valida numeric_tokens/preserved_content/glossary | Alta | Manter regras e política de normalização. |
| C010 | 3 | KEEP-POLICY | harness/harness.py:_evaluate, correct; harness/policy.json thresholds | Alta | Manter sequência independente e bloqueios. |
| C011 | 3 | KEEP-POLICY | harness/harness.py:launch_command --network=none e mounts; policy.json | Alta | Manter autorização remota e proibição de integração. |
| C012 | 3 | KEEP-CAVEAT | harness/harness.py:doctor, load_run, launch; tests/test_harness.py:test_no_unsandboxed_fallback | Alta | Manter fail-closed e evidência de aprovação. |
| C013 | 1 | KEEP-ROUTING | AGENTS.md comandos; harness/harness.py:main | Alta | Manter cwd requerido; não julgar fragmento isolado como comando completo. |
| C014 | 3 | KEEP-CAVEAT | harness/harness.py:launch_command instructions/mount; _evaluate | Alta | Manter distinção infraestrutura/linguística. |
| C015 | 3 | KEEP-ROUTING | .agents/skills/translation-quality/SKILL.md frontmatter; AGENTS.md rota | Alta | Manter trigger exclusivo. |
| C016 | 3 | KEEP-POLICY | AGENTS.md fronteira; harness/harness.py:STAGE e launch_command | Alta | Manter isolamento de governança. |
| C017 | 3 | KEEP-COMPRESSED | harness/harness.py:init_run/freeze_plan; templates/plan.json | Alta | Manter checklist compacto de preparação. |
| C018 | 3 | KEEP-POLICY | harness/harness.py:freeze_plan aprovação/hash; templates/plan.json | Alta | Manter aprovação e proveniência. |
| C019 | 3 | KEEP-COMPRESSED | harness/harness.py:mark_translated, launch_command, bundle | Alta | Manter piloto e runtime aprovado. |
| C020 | 3 | KEEP-POLICY | harness/harness.py:_evaluate review bundle_sha256/checks | Alta | Manter independência e vínculo ao bundle. |
| C021 | 3 | KEEP-POLICY | harness/harness.py:evaluate/correct; policy.json max_correction_rounds | Alta | Manter ciclo e bloqueio. |
| C022 | 3 | KEEP-POLICY | harness/harness.py:mark_translated exige PILOT_ACCEPTED; deliver | Alta | Manter gates antes de lote/entrega. |
| C023 | 3 | KEEP-CAVEAT | harness/harness.py não contém tradutor; policy.json imagem python | Alta | Manter limite semântico e seleção pelo piloto. |
| P003 | 1 | REDUNDANT-GENERAL | harness/harness.py define funções pequenas/nomeadas; deck sem regra específica | Média | Remover conselho genérico da governança de tradução. |
| P004 | 2 | UNCLEAR | harness/harness.py funções e gates; não há arquitetura multicamada formal | Média | Não remover sem contexto dos limites de camada; claim amplo. |
| P005 | 3 | KEEP-POLICY | harness/harness.py:docker_base/launch_command não herdam credenciais; regra cobre commits externos ao launcher | Alta | Manter política de segredos. |
| P006 | 3 | KEEP-CAVEAT | harness/harness.py:docker_base/doctor dependem runtime; CI entrypoint não demonstrado no escopo | Média | Manter caveat local/CI; esclarecer entrypoint apenas quando existir. |
