---
name: translation-specification
description: Use para especificar ou revisar o coordenador, tradutor, auditor e suas skills de tradução, adaptando BASpec e Spec/Plan/Tasks do SOT ENGINER à política do Inteligência SOT.
---

# Especificação dos agentes de tradução

1. Ler a entrada raiz, política, matriz e decisões aplicáveis, depois a governança
   completa da tradução. Consultar [metodologia](../../../docs/ESPECIFICACAO-TRADUCAO.md)
   e [índice das specs](../../../rag/traducao/specs/README.md).
2. Fixar missão, papel, entrada, produto, dependências e efeitos. Separar regras
   vigentes, capacidade demonstrada, proposta e decisão necessária. O pacote SOT
   é referência de pesquisa; não importa autoridade, políticas ou aprovações.
3. Escrever comportamentos atômicos QUANDO/ENTÃO/PORQUE/REFERÊNCIA/VERIFICADO POR.
   Usar cenários concretos positivos e negativos; indicar se a verificação é
   determinística, semântica ou humana. Detector não equivale a gate de efeito.
4. Para efeitos, declarar capacidade, destino, precondições, pós-condições,
   política, executor, falha e evidência. Mapear contexto, ferramenta, estado,
   isolamento e observabilidade com profundidade proporcional ao risco.
5. Conferir IG-01..IG-10 e contratos existentes. Produzir Spec comportamental,
   Plan técnico e Tasks rastreáveis separadamente. Uma proposta de arquitetura
   não altera a imagem, o launcher ou permissões de jobs.
6. Ler [benchmark](../../../rag/traducao/BENCHMARK-E-SELECAO.md) antes de propor
   motores ou frameworks. Comparar Python explícito, LangGraph e LangChain pelos
   mesmos contratos; registrar configuração, dependências e resultados reais.
   Popularidade e marketing não escolhem o vencedor.
7. Autor integra a escrita; revisores independentes podem analisar facetas em
   paralelo, até três agentes ativos no total, sem subagentes adicionais. Revisão
   técnica não homologa política. Mudanças de política seguem IG-01; trabalho
   operacional já autorizado continua sem nova confirmação de rotina.
8. Validar referências com Eval A, integridade/contexto e controles com os testes
   apropriados e Score oficial L4. Apresentar o que passou e o que falta. Score L4
   não certifica specs, traduções, identidade humana ou inclusão no corpus.
