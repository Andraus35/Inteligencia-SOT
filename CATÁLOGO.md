# Catálogo e timeline — Inteligência SOT

Atualização: 2026-10-09 UTC. Este é o handoff de sessão; ler junto ao
[ROADMAP.md](ROADMAP.md), à política vigente e à matriz. Não concede aprovação,
não substitui evidência nem traz cópias de PDFs/dados privados.

## Onde estamos

**Etapa 1, T1 concluída para documentação/integração; próximo T2 — desenho de avaliação.** Governança
geral 1.0.0 e harness de controle já implantados; novas specs e seleção de
frameworks não equivalem a tradução executada. O usuário confirmou tradução
primeiro e RAG efetivo depois. PDF documental, par de idiomas, glossário,
motor/modelo e piloto reais permanecem ausentes desta etapa.

## Timeline e entregas

| Data | Marco observado | Entrega / evidência | Limitação |
|---|---|---|---|
| 2026-10-09 | Governança adaptada | [Política](docs/governanca/POLITICA.md), [decisões](docs/governanca/DECISOES.md), matriz/registro | Política não implementa serviços RAG |
| 2026-10-09 | Controles e qualidade L4 | [Resultado L4](docs/HARNESS-L4-RESULTADO.md), ferramentas/CI/hooks locais; 64 testes na rodada anterior | L4 de Paladini é infraestrutura; CI remoto não confirmado |
| 2026-10-09 | Eval A+B+C anterior | [Relatório](docs/HARNESS-EVAL-RESULTADO.md), duas duplas de juízes/calibração | Fonte histórica; novas specs não receberam B/C nessa rodada |
| 2026-10-09 | Publicação da base | Commit remoto `d64ea64aa7a3c6efc3b3f645b4581b93dddd9e82`, branch main | Arquivos técnicos; nenhum corpus/PDF publicado |
| 2026-10-09 | Método e agentes especificados | [atomic-spec.md](atomic-spec.md), [metodologia](docs/ESPECIFICACAO-TRADUCAO.md), [specs/skills](rag/traducao/specs/README.md), Plan/Tasks | Piloto bilíngue/visual ainda pendente |
| 2026-10-09 | Frameworks adicionados ao benchmark | [Benchmark](rag/traducao/BENCHMARK-E-SELECAO.md): Python explícito, LangGraph, LangChain | Candidatos; nenhum framework escolhido ou experimento executado |
| 2026-10-09 | Integração/revisão das specs e skills | 69 testes passaram com Docker, lint/tipos/formato/integridade; L4 98/105; Eval A final zero BROKEN; duas revisões independentes | Controles demonstrados; cenários semânticos/modelos/frameworks pendentes |

Resultado da integração/revisão desta rodada: [ESPECIFICACAO-RESULTADO.md](docs/ESPECIFICACAO-RESULTADO.md).
O histórico Git conserva versões; marcos anteriores não certificam fontes novas.

## Onde vamos e próxima ação

Próximo: T2, fechar o desenho dos benchmarks e configurações; T3, obter PDF,
idiomas e referência/glossário para o piloto; depois comparar execução
determinística e qualidade probabilística antes de selecionar em T6. Manter
estados e evidências reais em [TASKS.md](rag/traducao/specs/TASKS.md).

Etapa 2: RAG somente após entrega/revisão da tradução, com especificação própria,
corpus aprovado por documento/lote e citações/conflitos rastreáveis.

## Início e encerramento de sessão

No início: conferir checkout/Git e alterações locais, ler este catálogo e roadmap,
identificar tarefa/etapa/papel, verificar documentos atuais e pendências. Se o
catálogo divergir de código/decisões/evidência, registrar e corrigir o fato após
checagem; não inferir autorização. Jobs usam contexto readonly da execução.

Ao encerrar entrega relevante: acrescentar marco com data/artefatos/verificação,
atualizar posição e próxima ação, registrar limites/decisões pendentes. Novas
aprovações devem entrar no livro de decisões, não surgir de atualização do catálogo.
