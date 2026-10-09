---
name: translation-quality
description: Use exclusivamente nesta etapa para preparar, traduzir, corrigir e auditar um PDF de trading com rastreabilidade e gates documentais.
---

# Procedimento da tradução

1. Entrar em `rag/traducao/` e carregar somente sua governança, sem importar regras do SOT.
2. Inventariar o PDF, fixar hash, idiomas e contexto; preparar plano a partir do template.
3. O coordenador congela o inventário e o glossário aprovado pelo usuário. Registrar modelos, prompts e ferramentas.
4. Tradutor executa piloto pelo launcher de papel, com números, fórmulas e código protegidos. Produzir blocos alinhados e PDF de leitura quando a ferramenta de tradução estiver instalada no runtime aprovado.
5. Auditor compara com o original de forma independente e registra evidências, checks e limitações. Vincular revisão ao hash do bundle auditado.
6. O gate valida o bundle. Correções voltam ao tradutor; o auditor revisa novamente. Máximo duas rodadas por lote; desacordo ou erro persistente bloqueia avanço.
7. Só iniciar lote completo após piloto aceito. Entregar após gate completo aprovado, sem integração automática ao RAG.

O Python do harness não traduz PDFs e não confirma equivalência semântica. Modelo, ferramenta e par de idiomas precisam ser escolhidos com o piloto real. O runtime base contém apenas Python e os controles, sem BabelDOC/Docling instalados.
