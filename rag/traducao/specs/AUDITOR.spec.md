# Spec — Auditor independente

ID: SPEC-TR-AUDITOR. Versão: 1.0.0. Estado: DOCUMENTADO, revisão bilíngue real pendente.
Profundidade: D0–D9 proporcional. Regra: política 1.0.0 e masters existentes.
Contrato compartilhado: [COMUM.md](COMUM.md). Procedimento:
[translation-auditor](../.agents/skills/translation-auditor/SKILL.md).

## Missão e fronteiras (D0–D2)

Comparar original e tradução, classificar erros contextualizados e rever
correções de forma independente. Não reescrever tradução, encerrar pendências
por conveniência, aprovar política ou conceder liberação de corpus.

## Entrada, saída e dependências (D6)

Recebe original, plano/glossário congelados e bundle do lote/hash, com versões
iguais às dos outros papéis. Produz `auditor/<pilot|full>/review.json`: reviewer,
batch, hash, reviewed_block_ids, checks e findings localizados, limitations.
Cada achado: ID, bloco, evidências fonte/tradução, categoria/gravidade, motivo
e ação requerida; JSON atual valida o subconjunto descrito no manual.

## BASpecs e cenários (D3, D7–D8)

### BASpec-AUD-01 — leitura independente
QUANDO: o auditor inicia exame de um lote.
ENTÃO: ele compara fonte e tradução antes das justificativas do tradutor.
PORQUE: reduzir ancoragem na autoavaliação do autor.
REFERÊNCIA: IG-07; `MASTER-AGENTES.md`, Auditor.
VERIFICADO POR: bundle com negação omitida e justificativa “sem erros” →
primeiro parecer identifica omissão pelo trecho, sem usar justificativa como
evidência de qualidade. Cenário semântico planejado; mesma família de modelo
pode repetir erros. Mount readonly permite ler justificativas: ordem de leitura
é procedimento, não barreira de acesso nem prova automática de independência.

### BASpec-AUD-02 — review atual
QUANDO: o bundle mudou depois da auditoria.
ENTÃO: o gate recusa reutilizar o review anterior.
PORQUE: parecer deve cobrir exatamente o material examinado.
REFERÊNCIA: IG-04; `README-HARNESS.md`, Limites explícitos.
VERIFICADO POR: alterar arquivo após `bundle_sha256` → gate falha;
`test_stale_review_rejected` e `test_delivery_rejects_changed_audit`.

### BASpec-AUD-03 — crítico aberto
QUANDO: a revisão identifica inversão operacional crítica.
ENTÃO: o auditor registra achado crítico localizado.
PORQUE: erro material não pode ser reduzido para permitir entrega.
REFERÊNCIA: IG-05; `MASTER-AGENTES.md`, Gravidade.
VERIFICADO POR: fonte “above”, tradução “abaixo” → achado crítico em `b1`,
com duas evidências e motivo. Identificação semântica planejada; achado crítico
já registrado bloqueia pelo `test_critical_findings_block_and_cannot_be_waived`.

### BASpec-AUD-04 — check sem exame
QUANDO: o auditor não inspecionou a renderização do PDF.
ENTÃO: ele relata essa limitação sem declarar `layout=true`.
PORQUE: check declarado deve corresponder à verificação real.
REFERÊNCIA: IG-02; `README-HARNESS.md`, Limites explícitos.
VERIFICADO POR: `layout=false` → gate não aceita o lote;
`test_semantic_check_false_blocks`. O booleano verdadeiro não prova que o
exame ocorreu; registro é declaração do revisor.

## Estado, mecanismo e efeito (D4–D6, D9)

D4: MQM adaptado classifica erros, sem score agregado de aceite. Review é
julgamento contextual mais controles de hash/schema; semanticamente não é
algoritmo determinístico. Launch em PILOT_TRANSLATED/TRANSLATED. Após correção,
examinar trecho e contexto e vincular novo parecer ao novo bundle.

Capacidade/efeito: escrever review/achados na área do auditor. Precondições:
bundle disponível, estado adequado e contexto atual. Pós-condição: parecer
com cobertura/limites declarados; host decide estado pelo gate implementado.
Política: IG-02/04/05/07. Executor: auditor para parecer, harness para checks;
não autentica identidade humana do `reviewer`. Falha: bloquear aceite e registrar
pendência. Evidência: achados/trechos/IDs, hash revisado e checks executados.
Parecer LLM não substitui revisão humana competente em regras críticas.

Classes, níveis, limites e detector/gate por BASpec: [PLAN.md](PLAN.md#mecanismo-e-controle-por-baspec).
