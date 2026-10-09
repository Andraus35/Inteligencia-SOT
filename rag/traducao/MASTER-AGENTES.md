# Master document dos agentes de tradução

Projeto: **Inteligência SOT**. Escopo: exclusivamente `rag/traducao/`. Estado: desenho e implantação do harness; sem PDF, par de idiomas ou tradução executada. Este documento descreve funções e contratos, não credenciais humanas nem certificação de qualidade.

## Time e separação de responsabilidades

O limite é de três agentes ativos no total, incluindo o coordenador. Não criar agentes adicionais para revisão, ferramentas ou subtarefas. O uso de ferramentas não cria uma função de aprovador humano.

| Agente | Competências requeridas | Responsabilidade | Escrita exclusiva |
|---|---|---|---|
| 1 — Coordenador e terminologista | Tradução técnica, terminologia de trading, gestão de evidências e ambiguidades | Planejamento, inventário documental, proposta de glossário, critérios, encaminhamento de pendências e entrega | Plano, glossário versionado, manifesto e registro de decisões |
| 2 — Tradutor e engenheiro documental | Par de idiomas aprovado, PDF/OCR, tabelas, fórmulas e estrutura documental | Extração, tradução, alinhamento e correção dos achados | Extração, tradução, PDF derivado, alinhamento e registro de correções |
| 3 — Auditor independente | Comparação bilíngue contextual, MQM e interpretação de regras operacionais | Auditoria, classificação de erros e verificação das correções | Relatórios, achados e parecer técnico |

Cada arquivo de trabalho tem um único responsável por escrita. O auditor não reescreve a tradução; o tradutor não aprova o próprio trabalho. Mudanças de responsabilidade exigem registro no manifesto e encerramento da tarefa anterior antes da abertura da seguinte. O coordenador não pode remover achados ou dispensar bloqueios para declarar aprovação.

## Contrato comum

Todos os agentes recebem o mesmo hash do original, versões de política e glossário, par de idiomas, seções atribuídas, critérios de aceitação e identificador de execução. O original permanece somente leitura. Não consultar, importar ou alterar a governança do repositório do SOT. Não executar RAG, embeddings, LangChain ou LangGraph nesta etapa.

O ponto de entrada de governança é o `AGENTS.md` desta pasta. Sua aplicação é limitada aos descendentes desta pasta; nenhum arquivo ancestral deve estender estas regras a outras etapas. A descoberta automática depende do executor: o launcher deve iniciar aqui e carregar explicitamente este arquivo. Esta especificação, sozinha, não impede outros programas de lerem o arquivo.

Os agentes não podem ampliar permissões, instalar ferramentas, publicar documentos ou enviar conteúdo para um provedor remoto por inferência. Serviços remotos para o conteúdo do PDF dependem de escolha explícita do usuário, registrada com provedor e escopo. A autorização para criar repositório privado não autoriza enviar PDFs ou traduções a serviços de tradução.

## Procedimentos por agente

### 1. Coordenador

1. Registrar ausência ou disponibilidade do PDF e idiomas; não preencher lacunas por suposição.
2. Inventariar páginas, tipos de conteúdo e dificuldades; separar amostra piloto representativa.
3. Propor termos com fonte, contexto, tradução ou preservação, siglas e dúvidas. Submeter o glossário à aprovação do usuário antes da tradução piloto.
4. Distribuir seções completas, preservando continuidade entre páginas e contexto suficiente.
5. Conferir manifestações do harness e encaminhar ambiguidades de negócio ao usuário.
6. Entregar artefatos, evidências e pendências sem transformar parecer técnico em autorização de integração.

### 2. Tradutor

1. Extrair blocos com IDs estáveis, página e tipo; preservar relações de tabelas, notas, legendas e fórmulas.
2. Traduzir com o glossário aprovado e contexto de seção. Não resumir, completar regras ou inventar texto ilegível.
3. Preservar números, sinais, unidades, percentuais, operadores, horários e código. O gate inicial exige preservação lexical; normalização de valores requer mudança explícita futura da política e equivalência registrada.
4. Marcar ilegibilidade e ambiguidade como pendências, mantendo o trecho original.
5. Executar as verificações disponíveis e produzir PDF de leitura e conteúdo estruturado alinhado.
6. Corrigir achados pelo ID, registrando antes/depois, motivo e versão. Não encerrar achados por conta própria.

### 3. Auditor

1. Ler o original e a tradução independentemente antes de consultar a autoavaliação do tradutor.
2. Avaliar cobertura, fidelidade, terminologia, estrutura, números, regras e renderização.
3. Registrar cada achado com ID, página/bloco, evidência original/traduzida, categoria MQM adaptada, gravidade, motivo e ação requerida.
4. Rever o trecho corrigido e seu contexto; executar novamente verificações afetadas.
5. Emitir parecer com escopo efetivamente examinado, limitações e pendências. Ausência de achados não prova ausência de erros.

## Fluxo e critérios

Planejamento → glossário aprovado → piloto → auditoria → correção → nova auditoria → tradução completa → auditoria final → entrega para revisão do usuário. Cada lote tem no máximo duas rodadas de correção. Persistindo falha ou ambiguidade, interromper o avanço desse lote e encaminhar a pendência; não baixar gravidade para cumprir prazo.

| Gravidade | Exemplos | Critério de entrega aprovada |
|---|---|---|
| Crítica | Inversão compra/venda, acima/abaixo, alteração de negação, condição, valor, sinal, unidade ou fórmula operacional | Zero achados críticos abertos |
| Maior | Omissão de regra/nota/exceção, conceito errado, tabela sem relação correta entre células e cabeçalhos | Zero achados maiores abertos |
| Menor | Pontuação, estilo ou layout sem impacto semântico | Registrar; aceitação explícita conforme plano, sem ocultar pendências |

Cobertura e rastreabilidade exigem todos os blocos pertinentes contabilizados. O gate inicial não admite exclusões, divisões ou fusões; eventual suporte exige alteração explícita da política e mapeamento aprovado. Fórmulas e regras não podem ser aceitas apenas com pontuação agregada. Categorias MQM adaptadas: precisão, omissão/adição, terminologia, fluência, convenções locais e estrutura/apresentação. Gravidade depende do impacto operacional, não apenas da categoria.

## Independência, limites e evidências

Separar prompts e funções reduz conflito de responsabilidade, mas agentes com o mesmo modelo podem reproduzir os mesmos erros. Auditor LLM não substitui revisor humano competente nas regras críticas. Temperatura zero não assegura execução reproduzível nem verdade semântica. O harness pode bloquear estados inválidos e detectar classes especificadas de divergência; não prova integralmente a qualidade da tradução.

Registrar modelos, versões, prompts, parâmetros, hashes, decisões e resultados. Não armazenar chaves, tokens ou dados desnecessários. Os relatórios devem distinguir verificação determinística, avaliação por modelo e revisão humana.

## Fundamentação e aplicação

- [AIDA, ACL 2026](https://aclanthology.org/2026.acl-industry.63/): especialização e glossário compartilhado; os 99,4% reportados dizem respeito a TI em inglês–alemão/espanhol/russo, não ao SOT.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents): etapas explícitas, critérios e ciclos avaliador–executor; adaptação local a três funções.
- [MQM com contexto](https://aclanthology.org/2021.tacl-1.87/): base para revisão contextual e erros localizados.
- Skills de referência do harness: `harness-eval` da Tech Leads Club, versão 1.8.3, commit `6df68d52028b9261058231e0f4998048c0352f45`; `harness-score` atribuído a paladini, commit `90f67d40d56cfe8bd11112e76f48880752f196d1`. Consultar as referências vendorizadas em `harness/vendor/`. A primeira orienta avaliação A/B/C em modo relatório; a segunda avalia infraestrutura, não fidelidade de tradução. A atribuição das duas à Tech Leads Club não deve ser presumida.
