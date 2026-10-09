# Pesquisa e desenho do benchmark

Consulta: 2026-10-09 UTC. Esta pesquisa orienta o piloto; nenhum parser, tradutor ou benchmark foi executado sobre o PDF do usuário.

## Popularidade observável e seleção preliminar

Dados da API pública GitHub, consultados na conta autenticada sem exportar credenciais. Stars e forks são sinais de interesse; não medem acessos, instalações, uso efetivo nem qualidade. Não há evidência de que estes sejam os dois projetos mais usados de todo o GitHub/GitLab. Projetos de software também não equivalem automaticamente a skills no formato `SKILL.md`.

| Projeto | Stars | Forks | Função | Licença / fonte indicada |
|---|---:|---:|---|---|
| [MinerU](https://github.com/opendatalab/MinerU) | 81.312 | 6.766 | Parsing/OCR e estrutura documental | NOASSERTION: conferir arquivos e componentes antes de instalar |
| [Docling](https://github.com/docling-project/docling) | 68.570 | 5.027 | Conversão estruturada, tabelas/OCR e exportação | MIT para o projeto; modelos/componentes requerem conferência própria |
| [PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | 37.401 | 3.341 | Tradução de PDF com preservação de formato | AGPL-3.0 |
| [BabelDOC](https://github.com/funstory-ai/BabelDOC) | 9.670 | 813 | Tradução via representação intermediária e reconstrução de layout | AGPL-3.0 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Não consultado | Não consultado | Framework de orquestração de fluxos e agentes com estado | MIT, conferida no arquivo LICENSE upstream; componentes de persistência e integrações requerem revisão própria |
| [LangChain](https://github.com/langchain-ai/langchain) | Não consultado | Não consultado | Framework de aplicações LLM, interfaces de modelos/ferramentas e agentes | MIT, conferida no LICENSE upstream; integrações/dependências têm revisão própria |

LangGraph foi acrescentado em 2026-10-09 por solicitação do usuário. Suas contagens de stars/forks não foram consultadas nesta inclusão; não inferir popularidade relativa a partir das outras linhas. As fontes do framework são seu [README](https://github.com/langchain-ai/langgraph/blob/cba111d8d600a027324eba1120a22e82b7f07432/README.md) e [LICENSE](https://github.com/langchain-ai/langgraph/blob/cba111d8d600a027324eba1120a22e82b7f07432/LICENSE), conferidos no commit `cba111d8d600a027324eba1120a22e82b7f07432`. Essa revisão documental não fixa a versão de um futuro experimento nem comprova desempenho local.

LangChain foi incluído por solicitação do usuário. Fontes: [README](https://github.com/langchain-ai/langchain/blob/34489d61433cbf5044a630de2e7797e361672900/README.md) e [LICENSE](https://github.com/langchain-ai/langchain/blob/34489d61433cbf5044a630de2e7797e361672900/LICENSE), commit `34489d61433cbf5044a630de2e7797e361672900`. SHA-256 dos bytes: README `9e6d706b38215c6979ef398ba72181b0f9099b8150f317c4c221877456c2dc2e`; LICENSE `4ec67e4ca6e6721dba849b2ca82261597c86a61ee214bbf21416006b7b2d0478`. Stars/forks não consultados.

Para duas capacidades complementares, a shortlist é **Docling para extração estruturada** e **PDFMathTranslate/BabelDOC para tradução e reconstrução documental**. São recomendações preliminares de adequação, não um ranking global. MinerU tem o maior número de stars desta amostra e deve ser comparado no piloto se parsing/OCR for o gargalo. A skill local `translation-quality` organiza essas capacidades; ela não instala ou implementa esses motores. Compatibilidade entre versões de PDFMathTranslate e BabelDOC precisa ser confirmada antes de escolher uma combinação.

**LangGraph e LangChain entram como candidatos de framework**, com protocolo próprio abaixo. Podem organizar chamadas aos motores/modelos escolhidos, mas não são, por si, parser/OCR, tradutor, modelo de embeddings ou banco vetorial. Comparar essas funções separadamente evita atribuir ao framework a qualidade produzida por um motor ou modelo.

## Evidência técnica

- [BabelDOC, ACL 2026](https://aclanthology.org/2026.acl-demo.25/): representação intermediária, contexto entre páginas, glossário e proteção de fórmulas; avaliação em 200 páginas. Os resultados publicados não substituem avaliação no idioma e domínio do SOT.
- [AIDA, ACL 2026](https://aclanthology.org/2026.acl-industry.63/): pipeline especializado, terminologia compartilhada e revisão. Relata 99,4% de precisão terminológica em TI en→de/es/ru. A arquitetura original tem quatro agentes; aqui planejamento/terminologia e pós-edição são distribuídos entre três funções. Essa adaptação não herdou a pontuação do paper.
- [OmniDocBench](https://github.com/opendatalab/OmniDocBench): avaliação separada de texto, tabelas, fórmulas e ordem de leitura. Versões do dataset, método de matching e configuração precisam ser registrados; não misturar resultados de versões diferentes. Mede parsing, não tradução.
- [From PDF to RAG-Ready](https://arxiv.org/abs/2604.04948v2): comparação de conversores para QA em domínio específico. A extração deve preservar estrutura e metadados; superioridade em um corpus não garante desempenho no SOT.
- [MQM contextual](https://aclanthology.org/2021.tacl-1.87/): avaliação bilíngue contextual por erros localizados. A gravidade operacional deste projeto exige interpretação competente das regras de trading.

## Protocolo do piloto real

1. Congelar PDF/hash, idiomas, glossário, inventário revisado e páginas representativas. Incluir os tipos difíceis presentes: regras e exceções, tabelas, sinais/percentuais, fórmulas, múltiplas colunas, notas e OCR. Não impor um número arbitrário de páginas sem conhecer o documento.
2. Preparar referência humana para os blocos do piloto. Usar exatamente a mesma amostra, configuração registrada e orçamento comparável para os candidatos. Não enviar conteúdo remoto sem escolha explícita do usuário.
3. Comparar extração separadamente: cobertura por bloco e página, ordem de leitura, erro de texto; TEDS para tabelas e CDM para fórmulas somente quando houver referência e runtime adequados. Métrica não substitui conferência das células/operadores críticos.
4. Comparar tradução: MQM adaptado por severidade/categoria, conformidade terminológica, invariantes numéricas e negações/condições, omissões/adições. COMET/XCOMET são complementares se adequados ao par de idiomas e com versão/condições registradas. Não aceitar por média agregada.
5. Inspecionar o PDF reconstruído: cortes, sobreposição, ilegibilidade, associação entre legenda/tabela/nota e preservação de fórmulas. Manter representação estruturada alinhada como derivado independente do PDF de leitura.
6. Registrar tempo, custo, memória/GPU, versões, prompts, parâmetros, falhas e correções. Selecionar pelo cumprimento dos critérios e evidências; custo/velocidade não dispensam zero críticos/maiores abertos.
7. Congelar a configuração vencedora após auditoria e decisões necessárias. Reavaliar mudanças relevantes. Só depois da tradução aceita abrir a etapa de RAG com seus próprios contratos e benchmarks.

O benchmark inicial será local e documental. Não atribuir a este projeto desempenho dos papers, do leaderboard ou do harness-score. Sem PDF e idiomas, o resultado atual é um protocolo reproduzível de comparação, não um vencedor comprovado.

## Benchmark dos frameworks LangGraph e LangChain

Estado: **candidato incluído; experimento não executado**. A documentação oficial descreve execução durável, persistência de estado e intervenção humana; a implementação escolhida precisa demonstrar essas capacidades no cenário do Inteligência SOT. LangGraph pode ser usado sem LangChain. Serviços de observabilidade ou hospedagem como LangSmith não são necessários a esta comparação local e não ficam autorizados por sua inclusão.

### Alternativas e critério de escolha durante a especificação

| Configuração candidata | O que varia | Dependências a registrar |
|---|---|---|
| Python explícito atual | Baseline de controles e fluxo | Python, imagem pinada e ferramentas/modelos fixados |
| LangGraph | Orquestração/estado e backend de checkpoint | Pacote/versão, persistência e integrações efetivamente usadas |
| LangChain | Interfaces/composição/modelos/ferramentas e fluxo de agentes escolhido | Pacote/versão, providers, middleware e LangGraph quando usado internamente |

LangChain oferece abstrações de aplicação e integrações; LangGraph oferece
controle de fluxo/estado em nível inferior. Podem compor a mesma arquitetura.
Não assumir que são alternativas independentes: registrar todas as dependências
transitivas e distinguir LangGraph isolado de LangChain com runtime LangGraph.
Não incluir Deep Agents ou agentes adicionais automaticamente. Modelos remotos,
LangSmith/traces e serviços externos não são autorizados por esta pesquisa.

Durante a especificação dos agentes/skills, selecionar pelo cumprimento dos
contratos, fidelidade e evidência medidos no orçamento acordado. Não declarar
vencedor antecipado. A primeira etapa avalia somente tradução; os experimentos
RAG abaixo pertencem à etapa seguinte. Reprovação em controle material exclui
configuração; custo/tempo orientam comparação entre configurações compatíveis.

### Comparação controlada

Comparar o fluxo Python explícito e os controles atuais com futuros protótipos equivalentes em LangGraph e LangChain, usando as mesmas entradas, ferramentas, modelos, prompts, glossário, política e gates. Primeiro usar fixtures sintéticas sem conteúdo privado, com respostas de ferramentas controladas, para isolar a orquestração. O piloto documental real mantém seus pré-requisitos próprios. Fixar pacote/versão, dependências e backend de checkpoint do protótipo; registrar commits, configuração, IDs de execução e hashes dos artefatos.

O grafo deve representar preparação → piloto → auditoria → correção limitada → lote completo → revisão final → entrega. Nós não equivalem a agentes adicionais: preservar os três papéis, ownership exclusivo, independência da auditoria e limite de duas correções por lote. A orquestração só encaminha resultados aos validadores; não substitui o launcher, amplia montagens ou transforma decisões de um LLM em aprovação humana. Retomada de checkpoint não dispensa revalidação de fonte, política, glossário e bundle.

| Eixo | Cenário a comparar | Medida e evidência |
|---|---|---|
| Estados e gates | Tentar pular piloto, entregar com crítico/maior aberto e exceder duas correções | Transições recusadas e logs vinculados aos artefatos; zero avanços indevidos |
| Retomada e persistência | Interromper antes/depois de checkpoint e de escrita de resultado; reiniciar execução | Recuperação do último estado válido, trabalho repetido/perdido e tempo de retomada |
| Idempotência | Repetir uma chamada ou reexecutar um nó após falha | Contagem de efeitos duplicados e rastreio por documento/lote/versão; não presumir execução exatamente uma vez |
| Aprovação humana | Pausar para revisão; tentar retomar sem decisão ou com aprovação de hash antigo | Decisão vinculada ao artefato correto; aprovações de tradução e corpus permanecem separadas |
| Rastreabilidade | Seguir um bloco da fonte até tradução, achado, correção e entrega | Cobertura dos IDs/páginas, hashes, papel responsável e histórico de transições |
| Isolamento e conteúdo como dado | Documento com instrução embutida; tentativa de escrita fora do papel ou transmissão não autorizada | Efeito negado pelo executor/gate correspondente; zero violações observadas nos cenários definidos |
| Custo da orquestração | Executar o mesmo workload com respostas controladas; depois repetir com os motores fixados | Tempo total, overhead de checkpoints, CPU/memória, chamadas/tokens/custo quando aplicáveis e volume de estado persistido |
| Manutenção | Alterar uma etapa e reproduzir a mesma falha em todos os candidatos | Mudanças necessárias, testes afetados, clareza do estado e evidência de recuperação, sem usar tamanho de código como prova de qualidade |

Definir número de repetições e orçamento antes de executar; registrar execuções frias/quentes, erros e dispersão, além da média. Usar percentis apenas com amostra suficiente. Qualquer bypass de gate, efeito não autorizado ou perda de vínculo documental reprova o candidato no cenário, independentemente de ganho de velocidade. Checkpoints podem conter texto e estado sensíveis: mantê-los locais, com retenção definida e sem exportação automática de traces.

### Relação com os benchmarks de RAG

Após revisão da tradução e liberação explícita do corpus, uma comparação separada pode avaliar os frameworks como orquestradores de recuperação e resposta. Fixar corpus/manifesto, chunking, embeddings, índice, modelo e conjunto de perguntas; variar somente a orquestração. Medir qualidade de recuperação quando houver referência, cobertura/correção de citações, respostas sem suporte, apresentação de conflitos com citações, custo e latência. A inclusão do framework não escolhe a arquitetura RAG nem instala ou autoriza sua execução nesta etapa.

O relatório de seleção deve distinguir resultados de parsing, tradução, orquestração e recuperação. A escolha de framework depende de evidência do experimento e decisão sobre sua adoção; sua documentação e popularidade não concedem aprovação ao corpus nem certificam a tradução.
