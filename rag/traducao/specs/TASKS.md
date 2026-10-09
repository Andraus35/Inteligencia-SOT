# Tasks rastreáveis — agentes e skills de tradução

ID: TASKS-TR-001. Versão: 1.0.0. Resultado desta rodada será registrado em
`docs/ESPECIFICACAO-RESULTADO.md`; status aqui distingue mecanismo de piloto real.

| Tarefa | BASpec / contrato | Mecanismo / evidência de aceite | Estado |
|---|---|---|---|
| TR-01 documentar papel/procedimento e origem | Todas; IG-07 | Specs, skills, metodologia e pesquisa; revisão independente | Documentado |
| TR-02 transportar e vincular contratos atuais | COM-01 | agent_contracts/init/load/launch; mudança/ausência/legado/read-only testados | Implementado; checar resultado da rodada |
| TR-03 preservar áreas e limites de correção | COM-02/04 | Docker real e `test_two_corrections_limit` | Implementado no harness |
| TR-04 preservar planejamento e gates | COO-01/02/03 | Idiomas/plan validation; crítico aberto e piloto obrigatório | Implementado; inventário contra PDF pendente |
| TR-05 proteger derivados e cobertura | TRA-01/02 | Lexical, IDs/páginas, cells, formulas, glossary; testes negativos | Implementado; tradução real pendente |
| TR-06 confirmar correção por achado | TRA-03 | Snapshot atual + registro antes/depois pelo tradutor | Snapshot implementado; schema do registro e piloto pendentes |
| TR-07 testar ambiguidade/injeção semântica | TRA-04/COM-03 | Fixture adversarial e modelo/runtime escolhido; revisor competente | Planejado; rede bloqueada já testável |
| TR-08 validar auditoria atual e gravidade | AUD-02/03/04 | Hash/achados/checks; testes de stale, crítico e false | Controle implementado; detecção bilíngue/visual pendente |
| TR-09 verificar independência procedural | AUD-01 | Fonte/tradução antes de justificativas; parecer localizado | Planejado; mount não garante leitura cega |
| TR-10 comparar motores/frameworks | PLAN-TR-001 | Benchmark com Python/LangGraph/LangChain, versões e mesmos inputs | Protocolado; experimento e escolha pendentes |
| TR-11 manter separação entrega/corpus | COM-05 | DELIVERED sem RAG; contrato IG-09 | Implementado o fluxo; liberação corpus não executada |

Próxima execução documental depende de PDF/par de idiomas/glossário. Não marcar
tarefa semântica concluída por teste de infraestrutura, Eval A ou Score L4.
