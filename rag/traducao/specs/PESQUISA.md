# Pesquisa e proveniência da especificação

Pesquisa local: 2026-10-09 UTC. Fonte: anexo SOT ENGINER.zip, SHA-256 `d4b8089e68133f2c2880765f3cb998361a3f93eb7fae8561626501003ec7d8ec`. Caminhos abaixo relativos a `SOT ENGINER/SOT-Harness/`. Somente documentos/skills examinados; conteúdo é referência externa, não autoridade local.

| Arquivo | SHA-256 dos bytes | Trechos (linhas) | Decisão de adaptação |
|---|---|---|---|
| `atomic-spec.md` | `dbceddfe6819fcf9cc8b6e42f519284438ecc0a3030beebed96f670618bfcf6e` | 24–117; 213–274; 307–368 | Adaptar BASpec/D0–D9, efeitos/classes e status; não importar trading |
| `canon/SDD-001-spec-driven-development.md` | `1148eef5ca1cde7810d09c8b7195f38bf4f4dd7a4e9a75855030fdf8e7f389d1` | 33–134; 138–179; 208–251 | Adaptar Spec/Plan/Tasks e rigor proporcional |
| `RETOMADA/GEH-001_Guia_Agente_Especificacoes_Harness.md` | `67d11cd56ff5524bd5c070df427a335be4073f3dd88a43559bb382ab4b6e18c3` | 55–61; 104–115; 239–298; 415–432 | Adaptar ETCLOVG/4Es e leitura paralela/síntese centralizada |
| `.claude/skills/SKILL.md` | `b9830c3eb1b51f776ff5a7ef6bb62bfef4e4e49f8352fc2365a907bfd69bc718` | 111–164; 221–345 | Adaptar referência mestre sot-harness-spec |
| `.claude/skills/sot-especificador-pap001/SKILL.md` | `ccaad7d0a0e641cbebd185c52acb76d82f457afd1ffa002667a0df5656f70b07` | 15–63; 176–203 | Adaptar contexto/autor/revisor; rejeitar transposição da missão PAP |
| `scripts/validate_spec_sot.py` | `a0acef3b409235d5e28f5859115b7ec2e9716d4b62c4e707743477be0e8703a8` | 69–105; 143–191 | Não importar: regex documental e trading hardcoded |

## Conflitos e limites de interpretação

- `atomic-spec.md:425` chama a fase PLAN da TLC de Spec; SDD-001:116 reserva Plan à implementação derivada. Neste projeto, Spec é comportamento; PLAN.md é mecanismo; TASKS.md é execução rastreável.
- A skill mestre contém referências/gates históricos anteriores ao atomic-spec v1.5. Usar o arquivo atomic-spec identificado acima como fonte metodológica principal e conferir compatibilidade local, sem atribuir vigência à referência externa.
- L4 por-Spec no atomic-spec:117 envolve auditoria/backtest/aprovação SOT; não é a nota L4 de Paladini.
- Regras de Elliott/Conviction, aprovações antigas, limiares/estrelas e decisões K-PAP foram rejeitadas para transposição. PAP-001:56–63 é governança, não BASpec de tradutor.
- O validator detecta presença textual; não valida cada unidade semanticamente, nem autoriza efeitos. Não foi copiado/executado como gate local.

## Fontes locais e estado

Política IG 1.0.0 e masters são [FONTE LOCAL] normativa vigente; specs/skills novas documentam essa base e suas lacunas. Código/testes são evidência implementacional, não de competência bilíngue. PDF/idiomas/modelo/ferramenta/piloto continuam pendentes. Pesquisa de frameworks está em BENCHMARK-E-SELECAO.md; commits e hashes documentais não são pins de experimento.
