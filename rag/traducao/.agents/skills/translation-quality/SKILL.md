---
name: translation-quality
description: Use exclusivamente nesta etapa para preparar, traduzir, corrigir e auditar um PDF de trading com rastreabilidade e gates documentais.
---

# Procedimento da tradução

1. Entrar em `rag/traducao/`, cumprir a entrada obrigatória geral/local e carregar
   a governança da etapa, sem importar regras do SOT. No job, usar o snapshot geral
   readonly; não montar a raiz. Ler `specs/COMUM.md` e spec/skill do papel.
2. Inventariar o PDF, fixar hash, idiomas e contexto; preparar plano a partir do template.
3. O coordenador congela o inventário e o glossário aprovado pelo usuário. Registrar modelos, prompts e ferramentas.
4. Tradutor executa piloto pelo launcher de papel, com números, fórmulas e código protegidos. Produzir blocos alinhados e PDF de leitura quando a ferramenta de tradução estiver instalada no runtime aprovado.
5. Auditor compara com o original de forma independente e registra evidências, checks e limitações. Vincular revisão ao hash do bundle auditado.
6. O gate valida o bundle. Correções voltam ao tradutor; o auditor revisa novamente. Máximo duas rodadas por lote; desacordo ou erro persistente bloqueia avanço.
7. Só iniciar lote completo após piloto aceito. Entregar após gate completo aprovado, sem integração automática ao RAG.

## Procedimento por papel

- Coordenador: [translation-coordinator](../translation-coordinator/SKILL.md).
- Tradutor: [translation-translator](../translation-translator/SKILL.md).
- Auditor: [translation-auditor](../translation-auditor/SKILL.md).

O contexto `agent_contract` fornece contrato comum, spec e duas skills do papel;
hashes vinculados ao manifesto não comprovam leitura. Mudança requer nova execução.

O Python do harness não traduz PDFs e não confirma equivalência semântica. Modelo, ferramenta e par de idiomas precisam ser escolhidos com o piloto real. O runtime base contém apenas Python e os controles, sem BabelDOC/Docling instalados.
