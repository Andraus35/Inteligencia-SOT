# Controles de qualidade de Eval e Score

O alvo é o projeto Inteligência SOT inteiro. O scanner é o **harness-score de
Paladini, 1.8.1**, pinado em `rag/traducao/harness/vendor/harness-score/` com
checksums em `vendor/provenance.json`. A skill de receitas é
`harness-engineering`; o Eval é a versão 1.8.3, preservada como dependência.
A skill ativa local `harness-quality` aplica esses procedimentos ao projeto.

## Instalação e sensores reais

Requisitos do host: Linux, Python >= 3.12, uv 0.12.19, Node >= 18, Make, Git e
Docker funcional. O runtime dos jobs de tradução continua sendo a imagem Python
pinada na política da etapa; instalar ferramentas no host não altera essa imagem.

```sh
make setup
make check
make score
make eval-a RUN_ID=rodada-nova
```

`make setup` usa `uv sync --locked --group dev` e instala o pre-commit no checkout.
O lock fixa dependências e hashes; `.venv` e caches são locais e ignorados. O cache
do Make fica no checkout para funcionar no ambiente cloud com home somente leitura.
Sem dependências instaladas, `--offline` falha; não tratar isso como validação verde.

`make check` executa selfcheck de governança, Ruff lint, mypy, Ruff format em modo
de conferência, pytest com integração Docker e `--min-level 4`. `make test` permite
o diagnóstico sem Docker e informa os dois testes de integração pulados.
O mypy verifica todos os scripts próprios e o harness: hooks/Score exigem assinaturas
de funções e chamadas tipadas; o código existente ainda sem assinaturas usa
`check_untyped_defs`. JSON e imports dinâmicos continuam exigindo validadores runtime.
Dependências vendorizadas estão excluídas de lint/formato/tipos, sem supressão de
checks sobre código próprio. `make format` é uma ação explícita e reversível.

O pre-commit registra lint, formato, integridade geral e gate L4. A suíte completa
e verificação de tipos ficam no comando `make check` e no CI. Para execução manual
fora do Make na nuvem, declarar `UV_CACHE_DIR=.cache/uv` e
`PRE_COMMIT_HOME=.cache/pre-commit`. A instalação dos hooks deve ser refeita ao
restaurar o checkout em outro ambiente.

## Hooks locais e limites de ativação

`.claude/settings.json` registra PreToolUse para Bash/Edit/Write e PostToolUse para
Edit/Write. São configurações de Claude Code, sem permissões automáticas `allow`.
O gate lê JSON, nega payload inválido, reconhece padrões destrutivos explícitos,
protege escrita direta em originais/vendor/credenciais/metadados Git e recusa
escrita fora do checkout ou por symlink. Não executa texto recebido. Decisões deny
usam o protocolo do cliente; entradas aprovadas pelo filtro retornam `{}` para
preservar as permissões do executor.

O filtro de shell é defesa em profundidade por padrões, não um parser completo:
shells aninhados, código arbitrário e comandos ofuscados podem escapar. O guard
de escrita direta não cobre toda escrita feita por Bash. A sandbox Docker e as
permissões da ferramenta continuam sendo a fronteira de execução. Operações
negadas não devem ser disfarçadas; encaminhar a decisão ao coordenador conforme
o escopo autorizado. O hook não autentica aprovação humana nem decide semântica.

O feedback pós-edição chama `make feedback` (lint, governança, diff), sem modificar
arquivos. Falha, timeout e indisponibilidade não viram PASS. Testes invocam o gate
real com JSON e verificam a configuração registrada. A ativação automática em um
cliente Claude depende desse cliente carregar as configurações e da autorização
de seus hooks. Nesta sessão Codex, use `make feedback`/`make check`; esses arquivos
não criam suporte de hooks automático no Codex. Nenhuma configuração global foi criada.

## Score oficial e regressões

`scripts/harness_score.py` verifica integridade do vendor, chama a CLI oficial
com defaults, escopo raiz e gate `maturity`, conserva código 1 abaixo do alvo
e código 2 em falha/incompletude. Não aceita `.harness-score.json` de reponderação.
`make score` grava `docs/harness-score-current.json`; `make score-check` não
reescreve relatórios. O comando legado da etapa continua emitindo seu diagnóstico
local: `python3 -B rag/traducao/harness/harness.py score`. Esse escopo não herda
artificialmente a nota da raiz.

Paladini define L4 por contexto/higiene, skills ou hooks, sensores >= 60%,
CI >= 50%, hooks >= 70% e total >= 80%. O scanner detecta arquivos/configurações;
não executa ferramentas nem prova que CI/hooks estão ativos. Ausência de agentes
customizados ou licença geral não será preenchida apenas para ganhar pontos.
Não adicionar MCP sem necessidade, publicar conteúdo ou alterar contratos para
aumentar a nota. Preservar licenças e atribuições dos vendors.

`.github/workflows/harness-quality.yml` prepara dependências pinadas e runtime,
executa sensores/testes, gate L4 e Eval A em pull requests e pushes à main.
Actions são referenciadas por commit; permissões são somente leitura. Não há
upload de PDFs, corpus ou decks dos juízes. Configuração local e comandos testados
não provam execução remota; publicação e primeira rodada no GitHub são estados
separados. Branch protection exige configuração do repositório e não foi ativada
por este workflow.

## Eval e governança de leitura

Seguir [HARNESS-EVAL.md](HARNESS-EVAL.md): Q1/Q2 reais, ID novo, hashes de fontes,
A antes de B/C, dois juízes independentes por trilha, plantas, segundo juiz cego
e modelo identificado. README não pontua no Eval; no Score, é orientação útil.
Registros de decisão não pontuam no Eval, mas continuam parte da governança.

Uma skill de instruções ativa está na raiz; vendors não são ativados como regras
globais. A nova rodada de A inclui essa skill e a skill de tradução. Resultados
B/C anteriores permanecem vinculados às fontes daquela rodada; não reinterpretar
seus pareceres como avaliação atual após uma alteração de leitura.
Ship, Slim e Mixed são propostas: aplicar somente no escopo autorizado, manter
checklists obrigatórios, respeitar consumidores e o plano KEEP/CUT. Aprovação de
política continua com o usuário; Score não aprova tradução nem corpus.
