# Pesquisa e desenho do benchmark

Consulta: 2026-10-09 UTC. Esta pesquisa orienta o piloto; nenhum parser, tradutor ou benchmark foi executado sobre o PDF do usuário.

## Popularidade observável e seleção preliminar

Dados da API pública GitHub, consultados na conta autenticada sem exportar credenciais. Stars e forks são sinais de interesse; não medem acessos, instalações, uso efetivo nem qualidade. Não há evidência de que estes sejam os dois projetos mais usados de todo o GitHub/GitLab. Projetos de software também não equivalem automaticamente a skills no formato `SKILL.md`.

| Projeto | Stars | Forks | Função | Licença informada pela API |
|---|---:|---:|---|---|
| [MinerU](https://github.com/opendatalab/MinerU) | 81.312 | 6.766 | Parsing/OCR e estrutura documental | NOASSERTION: conferir arquivos e componentes antes de instalar |
| [Docling](https://github.com/docling-project/docling) | 68.570 | 5.027 | Conversão estruturada, tabelas/OCR e exportação | MIT para o projeto; modelos/componentes requerem conferência própria |
| [PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | 37.401 | 3.341 | Tradução de PDF com preservação de formato | AGPL-3.0 |
| [BabelDOC](https://github.com/funstory-ai/BabelDOC) | 9.670 | 813 | Tradução via representação intermediária e reconstrução de layout | AGPL-3.0 |

Para duas capacidades complementares, a shortlist é **Docling para extração estruturada** e **PDFMathTranslate/BabelDOC para tradução e reconstrução documental**. São recomendações preliminares de adequação, não um ranking global. MinerU tem o maior número de stars desta amostra e deve ser comparado no piloto se parsing/OCR for o gargalo. A skill local `translation-quality` organiza essas capacidades; ela não instala ou implementa esses motores. Compatibilidade entre versões de PDFMathTranslate e BabelDOC precisa ser confirmada antes de escolher uma combinação.

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
