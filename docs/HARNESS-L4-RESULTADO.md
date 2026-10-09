# Harness Score Paladini — L4

Data: 2026-10-09. Escopo: raiz do `Andraus35/Inteligencia-SOT`.
Scanner oficial Paladini **harness-score 1.8.1**, checksums conferidos, defaults
upstream e gate maturity. Sem reponderação, checks desligados ou scopes globais.

| Medição | Nível | Pontos |
|---|---|---|
| Antes desta implantação na raiz | L2 — Guided | 49/105 (47%) |
| Após implantação e validação | **L4 — Self-correcting** | **98/105 (93%)** |

[Relatório inicial](harness-score-before-L4.json) ·
[Relatório atual](harness-score-current.json) ·
[Operação e limites](HARNESS-QUALIDADE.md)

## Arquivos e controles implantados

- Raiz: `AGENTS.md`, `Makefile`, `pyproject.toml`, `uv.lock`, `.gitignore` e
  `.pre-commit-config.yaml`, com dependências de desenvolvimento fixadas.
- `.agents/skills/harness-quality/`: procedimento local de Eval/Score e leitura
  sob demanda, preservando governança geral e especializada da tradução.
- `.claude/`: comandos intencionais, gate PreToolUse e feedback PostToolUse.
  Scripts testados; sem permissões automáticas nem configuração global.
- `.github/workflows/harness-quality.yml`: lint, tipos, formato, testes Docker,
  gate L4 e Eval A. Actions pinadas, permissões de conteúdo somente leitura.
- `scripts/`: adaptadores que usam as ferramentas oficiais pinadas; `tests/`:
  regressões de escopo, integridade, hooks, calibração estrutural e códigos de saída.
- `docs/governanca/`: política 1.0.0, matriz, decisões e integridade compatíveis
  com o snapshot enviado aos jobs. Papéis, limites e aprovações de tradução/RAG
  foram preservados.

Não foram criados agentes customizados, MCP ou licença de distribuição geral
para pontuar checks sem necessidade. Os vendors e suas licenças permanecem intactos.
O script legado de publicação foi compatibilizado com a entrada geral aprovada;
seus checks de destino privado, branch e histórico continuam presentes.

## Evidência executada neste ambiente

- Script reutilizável de instalação executado: ambiente, lock e pre-commit prontos.
- `make check`: selfcheck PASS, lint PASS, mypy sem erros em cinco arquivos,
  formato conferido em oito arquivos e **64 testes passaram**, sem skips, incluindo
  o teste real de isolamento Docker. O gate oficial `--min-level 4` retornou 0.
- Um checkout vazio de teste retornou código 1 no gate L4 da CLI oficial; o
  adaptador também foi testado contra retorno abaixo da meta e scanner incompleto.
- Quatro checks de pre-commit passaram em execução manual nos arquivos próprios;
  hook pre-commit instalado no checkout. Bash syntax do script de publicação válida.
- Gate registrado de pré-uso invocado fora do cwd do checkout: force-push negado.
  Feedback registrado pós-edição executou lint/governança/diff com sucesso.
- Workflow YAML, eventos, permissões e pins SHA conferidos localmente.
- Eval A, rodada `2026-10-09-l4`: duas entradas, duas skills e os cinco opcionais
  anteriormente escolhidos; **0 BROKEN**. Referências e integrações atuais foram
  revalidadas. B/C da rodada anterior continuam históricos, sem corte automático.
- `git diff --check` sem problemas; sem alteração de dependências vendorizadas.

## Ativação e escopos

L4 é a nota estrutural oficial do projeto. A nota da pasta `rag/traducao` continua
sendo uma medição separada; não foi substituída artificialmente pela nota geral.

Os hooks `.claude` dependem de um cliente Claude Code carregar a configuração.
Foram testados diretamente; não são hooks automáticos de Codex. No Codex, a
skill local orienta os comandos `make feedback` e `make check`, e o pre-commit
funciona via Git. O filtro de shell reconhece padrões explícitos; não é sandbox
nem prova de bloqueio de shell arbitrário. Os jobs de tradução conservam seu Docker
com rede bloqueada e áreas de escrita por papel.

O workflow foi preparado e seus comandos executados localmente. A primeira
execução no GitHub, status checks obrigatórios e branch protection dependem do
estado remoto; este documento não declara execução remota já concluída.
As instruções cloud são salvas em rascunho, sem publicar o ambiente automaticamente.
Score/Eval não aprovam tradução, qualidade linguística ou inclusão no corpus.
