# Harness Eval no Inteligência SOT

Executar a partir da raiz com Python 3. O adaptador `scripts/harness_eval.py`
usa o Harness Eval 1.8.3 vendorizado e verifica sua integridade antes de operar.
Não altera a dependência e não aplica cortes em documentos.

## Escopo e escolhas

A descoberta local considera `AGENTS.md` da raiz e de `rag/traducao/`, bem como
skills nos diretórios ativos `.agents/skills`, `.cursor/skills` e `.claude/skills`
dessas entradas. Dependências vendorizadas não são skills ativas. Novas etapas
precisam ser acrescentadas a `ENTRY_PATHS`, com revisão e teste da descoberta.

Leia o protocolo completo da skill em
`rag/traducao/harness/vendor/harness-eval/references/PROTOCOL.md` antes da rodada.
Q1 define documentos opcionais; Q2 define o orçamento de julgamentos:

| Opção | Documentos / trilhas |
|---|---|
| `--docs none` | Somente entradas e skills, incluindo suas referências descobertas |
| `--docs core` | Acrescenta política e matriz de leitura |
| `--docs full` | Acrescenta contratos e os dois masters de tradução ao núcleo |
| `--tracks A` | Correção determinística; sem juízes |
| `--tracks AB` | Correção e redundância; dois juízes independentes |
| `--tracks AC` | Correção e utilidade; dois juízes independentes |
| `--tracks ABC` | Todas; dois juízes por trilha subjetiva, em rodadas separadas |

README fica fora da pontuação e das evidências dos juízes. ADRs/RFCs e
`docs/governanca/DECISOES.md` ficam fora da pontuação, mesmo se solicitados como
tipo opcional. Continuam válidos como registros de decisões do projeto.

As opções registram escolhas declaradas pelo coordenador; não autenticam a
aprovação humana. Obtenha as escolhas do usuário antes de começar. A skill
define os custos e perguntas; não interprete uma opção padrão como resposta.

## Rodada reproduzível

Exemplo para uma rodada autorizada com os cinco documentos e A+B+C; substitua
`RODADA` por um ID novo, sem espaços nem barras:

```sh
python3 -B scripts/harness_eval.py inventory --run-id RODADA --docs full --tracks ABC
python3 -B scripts/harness_eval.py correctness --run-id RODADA
```

O inventário grava `evaluation-scope.json` com escolhas e hashes. Um ID já
registrado não pode ser sobrescrito pelo adaptador. Mudança de fonte exige
nova rodada. Track A retorna erro se houver BROKEN; B/C bloqueiam enquanto
houver BROKEN ou faltar seu relatório. A verifica referências e comandos
reconhecidos pelo scanner; não executa os comandos nem valida semântica.

Para B, siga os prompts da skill e despache dois juízes em contextos separados.
Eles pontuam todos os IDs de `claims.md`, incluindo calibração. O segundo não
recebe scores do primeiro, chaves de armadilhas, `claims.jsonl` ou relatórios
anteriores. Ambos verificam evidência no checkout, sem usar README. Registre
o modelo realmente disponível; se a variante exata não for exposta, declare
essa limitação. Não invente um ID.

```sh
python3 -B scripts/harness_eval.py merge-b --run-id RODADA
python3 -B scripts/harness_eval.py surfaces --run-id RODADA
```

Para C, use uma nova dupla independente e o deck `surfaces.md`. Não forneça
`surfaces.json`, chaves, scores do outro juiz ou resultados B como base para
utilidade. As tabelas devem seguir `references/judge-prompts.md`; células
KEEP/CUT de MIXED precisam nomear conteúdo concreto. Depois:

```sh
python3 -B scripts/harness_eval.py merge-c --run-id RODADA
```

O adaptador bloqueia IDs ausentes, extras ou duplicados, modelo não registrado,
linhas inválidas e classificação REDUNDANT com custo >= 2. Os merges originais
produzem relatórios e verificam calibração; PASS não é uma certificação de
qualidade. O gate da versão vendorizada admite a tolerância de erros indicada
no relatório e calibra o segundo juiz, não mede a precisão geral dos dois.

O gate de fan-in foi ampliado para as entradas e skills aninhadas, documentos
locais, caminhos relativos ao leitor e verbos de leitura em português. Ele
procura citações próximas de linguagem mandatória; é uma heurística textual,
não uma prova completa de dependência. Para caminhos Slim bloqueados, é preciso
preservar o documento ou atualizar consumidores na mesma mudança autorizada.

## Resultados e manutenção

Artefatos ficam em `.harness-eval/runs/RODADA/`, ignorados pelo Git: inventário,
decks, chaves, scores, `04-correctness.md`, `07-agreement.md`,
`10-usefulness-agreement.md`, `11-mixed-apply.md` e `slim-fanin.json`.
Mantenha um resumo sem dados documentais em `docs/` para revisão do projeto.

Ship (B) sugere instruções removíveis; Slim (C) sugere superfície enxugável.
Review/Keep-core preservam conteúdo; Hold indica desacordo, incerteza ou gate.
MIXED exige o plano KEEP/CUT de `11-mixed-apply.md`. Apresente o resultado antes
de aplicar cortes; alterações de política seguem a aprovação prevista pela
governança geral. Após emenda autorizada, atualize integridade e dependentes e
rode uma nova avaliação. Não altere hashes apenas para silenciar uma falha.

Verificação do adaptador e do harness existente:

```sh
python3 -B -m unittest discover -s tests -v
cd rag/traducao
python3 -B harness/harness.py selfcheck
python3 -B harness/harness.py doctor
TRANSLATION_TEST_DOCKER=1 python3 -B -m unittest discover -s harness/tests -v
```

Esses testes verificam controles operacionais. Não aprovam tradução, inclusão
no corpus, fidelidade linguística ou uma resposta RAG.
