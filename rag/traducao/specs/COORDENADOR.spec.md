# Spec — Coordenador e terminologista

ID: SPEC-TR-COORDENADOR. Versão: 1.0.0. Estado: DOCUMENTADO, piloto pendente.
Profundidade: D0–D9 proporcional. Regra: política 1.0.0 e masters existentes.
Contrato compartilhado: [COMUM.md](COMUM.md). Procedimento:
[translation-coordinator](../.agents/skills/translation-coordinator/SKILL.md).

## Missão e fronteiras (D0–D2)

Planejar a tradução, manter terminologia e inventário rastreáveis e encaminhar
pendências e entrega. Não traduzir como substituto do tradutor, editar achados,
dispensar gates, homologar política ou aprovar corpus por inferência.

## Entrada, saída e dependências (D6)

Recebe PDF/idiomas reais, política/contexto, necessidade do usuário e fontes
terminológicas. Produz `coordenador/plan.json` com inventário, piloto, glossário,
ferramentas/modelos/parâmetros e hash do prompt. O host congela o plano e mantém
manifesto/controle. Aprovação do glossário vem do usuário e deve ser real;
`glossary_approved_by` não autentica essa pessoa. Modelo e motor ainda pendentes.

## BASpecs e cenários (D3, D7–D8)

### BASpec-COO-01 — entrada incompleta
QUANDO: o idioma de destino está ausente.
ENTÃO: o coordenador registra a lacuna sem iniciar tradução.
PORQUE: par de idiomas não pode ser inventado.
REFERÊNCIA: `AGENTS.md`, Regras da tradução; IG-05.
VERIFICADO POR: PDF válido, origem `en`, destino vazio → `init_run` recusa;
cenário procedural de identificação da lacuna permanece para piloto.

### BASpec-COO-02 — inventário incompleto
QUANDO: o plano contém IDs de piloto ausentes no inventário.
ENTÃO: o host recusa congelar esse plano.
PORQUE: planejamento deve permitir cobertura rastreável.
REFERÊNCIA: IG-04; `MASTER-AGENTES.md`, Coordenador.
VERIFICADO POR: inventário `b1,b2,b3`, piloto `b9` → freeze recusado;
`test_incomplete_plan_rejected`. A revisão do inventário contra o PDF é
semântica/humana e ainda depende de documento real.

### BASpec-COO-03 — bloqueio não dispensável
QUANDO: um achado crítico permanece aberto.
ENTÃO: o coordenador mantém o lote bloqueado.
PORQUE: não pode remover achados ou reduzir gravidade para avançar.
REFERÊNCIA: IG-03; `MASTER-AGENTES.md`, Time e separação de responsabilidades.
VERIFICADO POR: parecer com crítico `open` → gate recusa;
`test_critical_findings_block_and_cannot_be_waived`.

## Estado, mecanismo e efeito (D4–D6, D9)

D4: inventário e glossário requerem análise contextual, não há algoritmo
terminológico validado. No job, escrever plano em CREATED/PLANNED. Freeze,
gate, correct e deliver são ações do host confiável; não chamá-las no job
como se tivesse acesso ao controle. O papel coordenador não possui launch em
ACCEPTED/DELIVERED; acompanhamento final é realizado no host autorizado.

Capacidade/efeito: preparar plano/glossário em sua área. Precondições: entrada
identificada, versão atual e decisões reais registradas. Pós-condição: plano
candidato verificável, sem concessão automática de aprovação. Política:
IG-04/07 e master. Executor: job para escrita; host para congelamento. Falha:
registrar lacuna/recusa; manter gate. Evidência: plano, hash congelado, decisão
do glossário e eventos do manifesto. Não há medição de eficácia terminológica
até o piloto; escolher ferramentas no [benchmark](../BENCHMARK-E-SELECAO.md).

Classes, níveis, limites e detector/gate por BASpec: [PLAN.md](PLAN.md#mecanismo-e-controle-por-baspec).
