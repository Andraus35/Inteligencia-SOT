# Spec — Tradutor e engenheiro documental

ID: SPEC-TR-TRADUTOR. Versão: 1.0.0. Estado: DOCUMENTADO, motor/piloto pendentes.
Profundidade: D0–D9 proporcional. Regra: política 1.0.0 e masters existentes.
Contrato compartilhado: [COMUM.md](COMUM.md). Procedimento:
[translation-translator](../.agents/skills/translation-translator/SKILL.md).

## Missão e fronteiras (D0–D2)

Extrair, traduzir, alinhar e corrigir o lote atribuído preservando regras,
valores e estrutura. Não aprovar o próprio trabalho, fechar achados, preencher
ilegibilidade, resumir regras ou alterar glossário/plano congelado.

## Entrada, saída e dependências (D6)

Input: original readonly, par de idiomas, contexto e plano congelado, lote
e achados quando houver correção. Output: `tradutor/<pilot|full>/translation.json`,
`translated.pdf`, alinhamento/derivados e registro de correções por ID.
O runtime atual contém Python/controles, sem motor de tradução ou OCR.
Ferramentas/versões e capacidade bilíngue precisam de seleção/piloto.

## BASpecs e cenários (D3, D7–D8)

### BASpec-TRA-01 — números preservados
QUANDO: o bloco contém `10 USD` como valor protegido.
ENTÃO: a tradução mantém literalmente o valor `10`.
PORQUE: o gate vigente exige preservação lexical, sem normalização implícita.
REFERÊNCIA: IG-05; `AGENTS.md`, Regras da tradução.
VERIFICADO POR: “Stop above 10 USD” → “Stop acima de 11 USD” é recusado;
`test_number_change_rejected`. Unidades anotadas têm teste próprio;
fidelidade semântica completa continua sendo auditoria.

### BASpec-TRA-02 — cobertura do lote
QUANDO: o lote contém três IDs originais.
ENTÃO: o tradutor entrega os três IDs alinhados.
PORQUE: o contrato inicial não admite exclusão, divisão ou fusão.
REFERÊNCIA: IG-04; `MASTER-AGENTES.md`, Fluxo e critérios.
VERIFICADO POR: lote `b1,b2,b3`, saída `b1,b2` → gate recusa mesmo com
parecer positivo; `test_omission_rejected_even_with_positive_review`.

### BASpec-TRA-03 — correção rastreável
QUANDO: o host abre rodada de correção após gate reprovado.
ENTÃO: o tradutor registra a alteração pelo ID do achado.
PORQUE: permitir ao auditor rever trecho e contexto sem apagar histórico.
REFERÊNCIA: IG-08; `MASTER-AGENTES.md`, Tradutor.
VERIFICADO POR: achado `F-01`, bloco `b1` → registro antes/depois/motivo/versão
na área do tradutor. Revisão desse registro é procedural, pendente do piloto;
o harness já guarda snapshot anterior em `correct`, mas não valida esses campos
do registro do tradutor como schema dedicado.

### BASpec-TRA-04 — ambiguidade sem invenção
QUANDO: um trecho está ilegível.
ENTÃO: o tradutor marca pendência localizada preservando a referência original.
PORQUE: inferência não pode preencher conteúdo desconhecido.
REFERÊNCIA: IG-05; `MASTER-AGENTES.md`, Tradutor.
VERIFICADO POR: imagem sintética ilegível no bloco `b1` → pendência `b1/página 1`,
sem valor completado. Cenário semântico/visual planejado, não executado.

## Estado, mecanismo e efeito (D4–D6, D9)

D4: hashing/alinhamento/lexical são determinísticos no harness; tradução é
julgamento de modelo/ferramenta com revisão. Launch apenas após plano, piloto
aceito para lote completo ou correção aberta. Escrita na área do tradutor;
snapshot/controle e aprovação ficam fora do job. Até duas correções por lote.

Capacidade/efeito: produzir derivados locais. Precondições: plano e glossário
congelados, lote permitido, runtime aprovado. Pós-condição: artefatos alinhados
prontos para revisão, sem autoaprovação. Política: IG-04/05/07/08 e masters.
Executor: ferramenta escolhida pelo [benchmark](../BENCHMARK-E-SELECAO.md),
quando instalada na imagem validada; controles existentes bloqueiam divergências
especificadas. Falha: pendência localizada, sem fallback remoto. Evidência:
IDs/páginas, bundle/hash, versões e correções; não registrar chaves ou tokens.

Classes, níveis, limites e detector/gate por BASpec: [PLAN.md](PLAN.md#mecanismo-e-controle-por-baspec).
