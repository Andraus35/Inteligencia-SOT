# Revisão técnica do harness de tradução

Revisão estática de `harness/harness.py` e `harness/tests/test_harness.py`. Não executou nova suíte nem alterou código, governança ou notas B/C. O coordenador informou 32 testes aprovados com Docker após três novas regressões; essa informação não foi reproduzida por este revisor. Fixtures sintéticas não validam uma tradução real. Modelo: codex-gpt-6-inherited (exact API model id not exposed).

## Resultado

Os controles solicitados estão presentes para o fluxo válido e os cenários específicos cobertos pelos testes. Dois bloqueadores de disponibilidade identificados na primeira leitura foram corrigidos e suas mudanças foram verificadas nesta releitura. Não permanece bloqueador confirmado no escopo revisado; os limites abaixo continuam aplicáveis. Não foi identificado um bypass simples de FAILED para aprovação pelos comandos públicos sem correção registrada. Este relatório não certifica segurança absoluta, identidade dos agentes ou qualidade linguística.

## Histórico dos achados — resolvidos

### B1 — Resolvido: preparação do coordenador em CREATED

Na primeira versão, `launch_command` exigia plano congelado antes de permitir o coordenador em CREATED. A versão final verifica papel/estado e dispensa `frozen_plan` exclusivamente para coordenador em CREATED. `load_run` continua verificando política e hash da fonte; controles de runtime, mounts e rede permanecem. Tradutor/auditor não recebem essa exceção. Evidência de regressão: `test_coordinator_can_prepare_plan_before_freeze` cobre preparação e rejeição dos outros papéis.

### B2 — Resolvido: recuperação de JSON inválido ou ausente

Na primeira versão, `correct` exigia parse válido do JSON que precisava de reparo. A versão final salva bytes em hexadecimal e SHA-256 quando o arquivo existe, ou ausência explícita, sem fazer parse do artefato. Mantém estado FAILED obrigatório, reprovação registrada, motivo e limite de duas rodadas; só então registra CORRECTING. Isso permite reparo sem aprovar o conteúdo inválido. `mark_translated` e nova auditoria continuam obrigatórios.

Evidência: `test_malformed_translation_can_enter_correction_with_raw_snapshot` cobre bytes preservados, liberação do tradutor, reparo e nova aprovação; `test_missing_translation_can_enter_correction_with_absence_snapshot` cobre ausência e liberação para reparo.

## Controles confirmados por leitura

| Controle | Evidência | Limite |
|---|---|---|
| FAILED → CORRECTING obrigatório | `evaluate`, `correct`, `mark_translated`, estados em `launch_command`; teste `test_failed_gate_cannot_bypass_registered_correction` | B2 corrigido com snapshot bruto/ausência; não há autenticação forte do usuário que chama controles no host |
| Bundle único no início/fim | `mark_translated` grava attempt_bundles; `_evaluate` fixa audit_bundle, compara ao attempt e repete bundle ao final; teste de mutação durante gate | Hashes não tornam snapshots atômicos contra escritor arbitrário no host; locks cobrem participantes cooperativos |
| Review vinculada e entrega íntegra | `_evaluate` exige bundle_sha256, IDs de todos blocos, checks e hash review; `deliver` compara accepted bundles e accepted_reviews | `reviewer` é declaração, não identidade autenticada; revisão semântica não é comprovada pelo esquema |
| Controles versus job | decorator `controlled` adquire lock exclusivo; `launch` mantém lock compartilhado do run e lock exclusivo de job da etapa | Chamadas diretas externas que não usam API/locks ou processos host com mesmas permissões não são isoladas por fcntl |
| Symlink em ancestrais | `inside` verifica candidato e seus ancestrais; `read_json`/`digest` usam inside; launcher recusa links na árvore | Check/open são operações separadas; adversário host com acesso de escrita pode disputar caminhos. Docker limita participantes lançados |
| Timeout e interrupção | `launch` finally executa docker rm -f e confirma ausência com docker ps; teste real opt-in de timeout | Pré-verificação docker ps não tem timeout; daemon travado pode prender o launcher antes do job. SIGKILL não executa finally |
| Órfãos e quarentena | label por etapa, verificação de containers antes de job; falha de cleanup grava runtime-quarantine.json e bloqueia novo launcher | Não há teste dedicado de falha de cleanup/quarentena ou SIGKILL no arquivo revisado; recuperação explícita ainda operacional |
| Confinamento runtime | somente `/stage` read-only, papel gravável, scratch e tmp; network none, cap-drop ALL, no-new-privileges, imagem por digest | Não é barreira contra administrador do host/daemon Docker; mounts de toda etapa permitem leitura de dados de outros runs da tradução |

## Limitações e observações sem bloqueio adicional

- O hash da revisão é calculado depois de sua leitura e validação, sem comparação inicial/final do próprio review. Jobs auditados não correm durante o gate graças ao lock, mas um escritor host alheio aos locks poderia trocar o report entre leitura e digest. Modelo de ameaça deve excluir esse escritor ou exigir snapshot/verificação adicional. Não é alegada proteção contra administrador host.
- PDF é verificado apenas pela assinatura `%PDF-`; validade estrutural, renderização e correspondência com translation.json dependem de ferramentas e auditor. Um arquivo sintético passa assinatura e isso é intencional nos testes, não evidência de PDF de leitura válido.
- numeric_tokens usa Counter: preserva multiplicidade de valores, não a associação de números a condições dentro de prosa. Tabelas acrescentam comparação por célula. Negação, operadores não numéricos, condições e significado dependem de tokens selecionados e revisão declarada.
- `correct` mantém snapshot dos bytes do JSON em hexadecimal, hash e motivo, ou ausência explícita. Não preserva cópia integral de PDF e demais artefatos anteriores; hashes/relatórios ajudam rastreabilidade, mas não recuperam bytes sobrescritos.
- Política possui thresholds críticos/maiores zero; implementação bloqueia qualquer achado aberto, inclusive menor. É mais estrita e não constitui bypass, porém deve ser explicada para evitar expectativas de aprovação com menores abertos.
- O launcher monta a pasta do coordenador gravável quando esse papel atua. Depois de congelado, alterações ao plano são detectadas por hash em operações subsequentes; imutabilidade lógica não equivale a filesystem somente leitura para esse proprietário.
- Não foram examinados bugs do kernel/daemon, isolamento de modelos, tradução do PDF real nem segurança de ferramentas futuras. Nenhuma afirmação de enforcement integral de prompts ou correção semântica deriva desta revisão.

## Próxima validação sugerida

B1/B2 estão resolvidos por leitura e cobertos pelas três novas regressões; o coordenador informou 32 testes PASS incluindo Docker. Para sustentar adicionalmente as alegações de recuperação de runtime, acrescentar testes controlados de cleanup falho/quarentena e órfão detectado. Antes de traduzir, validar o fluxo com PDF real, idioma, ferramentas aprovadas e revisão semântica. Não ampliar permissões ou oferecer fallback sem sandbox como solução.
