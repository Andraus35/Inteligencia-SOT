# Avaliação do harness — 2026-10-09

Rodada `2026-10-09-adaptado`, Harness Eval vendorizado 1.8.3 com adaptador local.
O usuário escolheu os cinco documentos opcionais e A+B+C com dois juízes e
armadilhas de calibração. Foram usados pares independentes em contextos novos
para B e C, sem transportar resultados B para os juízes de utilidade.

## Escopo e resultado

Entradas: `AGENTS.md` da raiz e de tradução. Skill:
`rag/traducao/.agents/skills/translation-quality/SKILL.md`. Opcionais: política,
matriz de leitura, contratos e os dois masters de tradução. README foi excluído
da pontuação e das evidências; registros de decisões ficaram fora da pontuação.
Versões dessas oito fontes estão vinculadas aos hashes de
`evaluation-scope.json` na pasta local da rodada.

| Trilha | Resultado real, sem contar armadilhas | Calibração formal |
|---|---|---|
| A — correção | 0 BROKEN; 5 citações de caminhos reconhecidas como válidas | Determinística, sem juiz |
| B — redundância | 44 trechos: 1 Ship, 43 Review, 0 Hold | PASS; segundo juiz acertou 4/4 armadilhas |
| C — utilidade | 8 documentos: 0 Slim, 4 Keep-core, 3 Mixed, 1 Hold | PASS; segundo juiz acertou 3/3 armadilhas |

Cada juiz B pontuou os 48 IDs (44 reais + 4 armadilhas). Cada juiz C pontuou
os 11 IDs (8 reais + 3 armadilhas). Os quatro relatórios registram
`GPT-6 inherited (exact API variant not exposed)`: a família foi declarada,
mas a variante exata não foi exposta pela ferramenta. Não houve comparação
entre modelos diferentes.

## Recomendações para revisão

Ship em B: somente C007, a enumeração de arquivos de `docs/governanca/` no
mapa da entrada raiz. É informação redescoberta por uma listagem. Isso não
autoriza remover a entrada raiz: C marcou a superfície como Hold, pois J1
considerou KEEP-CORE e J2 MIXED.

| Documento | Acordo C | Implicação |
|---|---|---|
| `AGENTS.md` | Hold | Preservar; desacordo sobre extensão da compressão |
| `rag/traducao/AGENTS.md` | Keep-core | Preservar checklist e limites |
| Skill `translation-quality` | Keep-core | Preservar procedimento operacional |
| `docs/governanca/POLITICA.md` | Keep-core | Preservar regras IG-01..10 |
| `docs/governanca/LEITURA-AGENTES.md` | Keep-core | Preservar matriz e releitura |
| `docs/governanca/CONTRATOS.md` | Mixed | Preservar contratos/campos; rever repetição dos exemplos futuros |
| `rag/traducao/MASTER-AGENTES.md` | Mixed | Preservar papéis/gates; rever fundamentação e narrativa repetida |
| `rag/traducao/MASTER-PROJETO-TRADUCAO.md` | Mixed | Preservar insumos/invariantes; rever bibliografia e explicações repetidas |

Os itens exatos KEEP/CUT dos três Mixed estão em `11-mixed-apply.md`.
Antes de aplicar, compatibilize os dois conjuntos: KEEP prevalece; conflito
entre KEEP e CUT deixa o item em espera. Não substituir regras mantidas por
ponteiros para exemplos de código. Nenhum corte recomendado foi aplicado nesta
rodada. A política permanece na versão 1.0.0 aprovada anteriormente.

## Adaptação implantada e verificação

`scripts/harness_eval.py` descobre a skill aninhada como T1, exclui explicitamente
`DECISOES.md`, registra escolhas e hashes e reconhece leituras mandatórias em
português e caminhos relativos ao leitor no gate de dependências. Bloqueia
fontes alteradas, execução sem Track A válido, trilha não escolhida, pontuações
incompletas/duplicadas, linhas inválidas e REDUNDANT com custo >= 2. A dependência
vendorizada foi preservada e sua integridade conferida.

Passaram 12 testes do adaptador e 41 do harness de tradução. `selfcheck` passou;
`doctor` confirmou Docker e runtime pinado. O teste real de sandbox negou sete
escritas e verificou snapshot de governança somente leitura, ausência de raiz
do projeto/SOT/credenciais nas montagens e rede bloqueada. `git diff --check`
não encontrou problemas. O [guia operacional](HARNESS-EVAL.md) contém comandos
e requisitos de reprodução. Relatórios locais estão ignorados pelo Git; não
houve commit, push nem publicação do ambiente nesta rodada.

## Limites da interpretação

A verifica apenas referências reconhecidas; não executa comandos nem certifica
consistência semântica. Os cinco trechos T2 de B representam destinos de leitura,
não uma extração de todas as frases dos documentos; C examinou seu conteúdo.

O gate de calibração vendorizado mede o segundo juiz e admite a tolerância
descrita pela chave. Nesta rodada ele teve zero erros nas duas trilhas. O
primeiro juiz C marcou S903 como UNCLEAR, enquanto o esperado era KEEP-CORE;
esse resultado não entra no gate formal. PASS não equivale a precisão geral
comprovada dos dois juízes.

O merge C registrou fan-in PASS com zero candidatos Slim reais. Isso não prova
ausência de consumidores: não havia candidata a remoção para esse gate testar.
Os testes do adaptador demonstraram bloqueio com leitura mandatória em
português. A descoberta e o detector de mandatos continuam heurísticos e
específicos às entradas cadastradas; revise consumidores antes de uma emenda.

A cegueira dos juízes foi orientada por instruções e contextos separados, sem
ACL adicional no filesystem compartilhado. Utilidade depende do modelo; cortes
grandes exigiriam nova comparação antes de decisão. Esta avaliação não aprova
tradução ou inclusão no corpus e não valida um sistema RAG ainda não implementado.

## Evidências detalhadas locais

- [Correção A](../.harness-eval/runs/2026-10-09-adaptado/04-correctness.md)
- [Acordo de redundância B](../.harness-eval/runs/2026-10-09-adaptado/07-agreement.md)
- [Acordo de utilidade C](../.harness-eval/runs/2026-10-09-adaptado/10-usefulness-agreement.md)
- [Plano KEEP/CUT de Mixed](../.harness-eval/runs/2026-10-09-adaptado/11-mixed-apply.md)
- [Escopo e hashes](../.harness-eval/runs/2026-10-09-adaptado/evaluation-scope.json)

Esses links requerem os artefatos locais da rodada; somente o resumo e o guia
estão preparados para acompanhamento no repositório.
