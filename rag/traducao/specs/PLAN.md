# Plan técnico das specs e skills de tradução

ID: PLAN-TR-001. Versão: 1.0.0. Estado: adaptação operacional autorizada;
arquitetura de motores/frameworks ainda candidata. Derivado das três specs e
de [COMUM.md](COMUM.md); não é plano de execução `coordenador/plan.json`.

## Mecanismos existentes e integração

| Camada ETCLOVG | Mecanismo e limite |
|---|---|
| Ambiente | Docker pinado, sem rede, mounts readonly, área writable por papel; host continua confiável |
| Ferramentas | CLI Python de controle no host; ferramentas de tradução/OCR não instaladas na imagem |
| Contexto | Governança/snapshot, masters, manual e novo contrato de papel com duas skills/specs e hashes |
| Ciclo | Estados/gates/correções/locks existentes; jobs sequenciais; pesquisa independente pode ser paralela |
| Observabilidade | Manifesto/eventos, hashes de fonte/plano/bundle/contratos, review/snapshots; custo/modelos reais pendentes |
| Verificação | Testes sintéticos/isolamento, checks lexicais e Eval A; revisão bilíngue/PDF real pendente |
| Governança | IG 1.0.0 e papéis existentes; dados de aprovação não autenticam humano |

`agent_contracts()` lê documentos obrigatórios sem symlinks, calcula hashes dos
bytes e fornece conteúdo por papel. `init_run` vincula hash do conjunto ao
manifesto. `load_run` recusa versão alterada ou legado sem vínculo. O launcher
transporta apenas contrato comum + spec e skills do papel em `agent_contract`,
readonly, e verifica correspondência com manifesto antes da escrita do contexto.
Todos os três contratos são conferidos no host para preservar compatibilidade
do time. Não alterar snapshots antigos para absorver a mudança.

O estágio continua montado readonly por inteiro: seleção do contexto reduz
carga de leitura, mas não restringe leitura de outras specs/justificativas.
Nenhum prompt de papel é executado automaticamente; a ferramenta/modelo precisa
consumir contexto e procedimento quando houver runtime aprovado.

## Mecanismo e controle por BASpec

Classes e níveis são os da referência local `atomic-spec.md`, usados para análise
do comportamento, sem criar novas permissões. E0 não é enforcement; E1 estrutura,
E2 controle demonstrável de estado/integridade. E3 de identidade/consentimento
humano não é reivindicado. Prioridade 4Es em cada linha: fidelidade/conformidade
antes de prazo, recursos e custo; essa ordem não é substituída por score agregado.

| BASpec | Classe / nível | Mecanismo e executor | Limite/parada | Detector / gate e evidência |
|---|---|---|---|---|
| COM-01 | D / E2 | Host compara hash do conjunto | Uma verificação por operação; divergência exige nova run | Recusa determinística; testes de mudança/ausência/legado |
| COM-02 | D / E2 | Docker mounts readonly e writable do papel | Duração do job ≤900s; sem fallback | Sistema nega escrita; teste Docker real |
| COM-03 | P / E0 semântico | Agente trata documento como dados | Sem retry semântico automático; pendência encaminhada | Cenário semântico planejado; sandbox D/E2 nega rede, sem provar interpretação |
| COM-04 | C / E2 | Host controla estado/contador | Duas correções por lote; terceira recusada | Gate determinístico de `correct`; teste de limite |
| COM-05 | P / E0 relato | Coordenador relata alcance técnico | Um handoff; autorização de RAG é distinta | Revisão do relato pendente; fluxo D/E2 não possui indexação |
| COO-01 | H / E0 relato, E2 início | Agente identifica lacuna; host valida idiomas | Parar tradução sem par definido | `init_run` recusa idioma vazio; identificação procedural pendente |
| COO-02 | D / E2 | Host valida piloto contido no inventário | Um freeze; falha não muda estado | Gate de plano e teste de piloto inválido |
| COO-03 | H / E0 coordenação, E2 gate | Coordenador encaminha; host confere achados | Falha bloqueia lote; até duas correções | Achado semântico não é gate; gate determinístico recusa crítico aberto |
| TRA-01 | H / E2 lexical | Modelo/motor produz texto; host compara números | Até duas correções; persistência encaminhada | Gate lexical demonstrado; modelo/piloto pendentes |
| TRA-02 | H / E2 cobertura | Tradutor alinha; host compara IDs | Até duas correções | Gate determinístico de cobertura; teste de omissão |
| TRA-03 | P / E0 registro | Tradutor registra antes/depois por achado | Até duas correções; não fecha achado | Revisão procedural pendente; snapshot D/E2 não valida schema desse registro |
| TRA-04 | P / E0 | Tradutor marca ilegibilidade | Não completar; encaminhar decisão | Detector semântico/visual planejado, sem gate de percepção implementado |
| AUD-01 | P / E0 | Auditor lê fonte/tradução antes de justificativas | Um primeiro parecer; revisão após correção | Procedural e planejado; mount não obriga ordem de leitura |
| AUD-02 | D / E2 | Host compara hash atual e review | Uma avaliação; stale recusa | Gate/hash e testes de stale/entrega |
| AUD-03 | P / E0 identificação | Auditor julga inversão e registra achado | Não rebaixar para avançar; duas correções do lote | Detecção semântica planejada; achado declarado é bloqueado pelo gate D/E2 existente |
| AUD-04 | H / E0 exame, E1 declaração | Auditor examina PDF/check; host valida campo | Exame não feito impede aceite | Check false bloqueado por controle D/E2; true não comprova inspeção real |

Contratos de efeito completos ficam no documento comum e nas specs por papel;
esta tabela liga cada unidade ao mecanismo, sem repetir normas nos perfis.

## Decisão de motores e frameworks

Seguir [BENCHMARK-E-SELECAO.md](../BENCHMARK-E-SELECAO.md): parsing/OCR,
tradução/renderização e orquestração têm eixos separados. Comparar fluxo Python
explícito, LangGraph e LangChain com o mesmo contrato e workloads controlados.
LangChain pode acrescentar dependências de LangGraph; registrar grafo/lock,
sem tratar as alternativas como independentes quando compartilham runtime.

Escolha durante a especificação: primeiro excluir opções incompatíveis com gates,
privacidade, licença e ambiente. Entre opções compatíveis, comparar fidelidade,
retomada, manutenção, tempo/recursos/custo e evidência dos cenários. Não há
vencedor declarado nem instalação nesta rodada. Adoção que altere launcher,
rede, imagem ou política exige plano/testes e decisão de escopo correspondente.

## Decisões e validação pendentes

- PDF real, idiomas, termos/glossário e referência humana do piloto.
- Motor/OCR/modelo e imagem validada, prompts por papel e dados de comparação.
- Seleção de framework, versões transitivas, checkpoint local e retenção se usado.
- Inspeção semântica/visual competente; não inferir de testes sintéticos.
- Política alterada, serviços remotos ou corpus: aprovação própria quando aplicável.

Verificação operacional: `make check`, `make eval-a RUN_ID=<novo-id>` e revisão
independente. Mudança de política não está incluída. [TASKS.md](TASKS.md) registra
evidências por comportamento sem declarar cenários planejados como executados.
