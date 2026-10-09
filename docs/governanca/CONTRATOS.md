# Contratos de etapas — proposta

Estado: DESENHO DE ETAPAS. Política geral 1.0.0 aprovada; somente tradução tem runtime existente. Os contratos e campos para RAG são candidatos à futura especificação/implementação.

| Etapa | Entrada | Saída | Precondições e controle proposto |
|---|---|---|---|
| Tradução existente | PDF, idiomas, plano e glossário aprovados | Tradução, PDF derivado, revisão e bundle | Preservar estados e gates atuais. Revisão/aprovação de tradução e liberação ao corpus são decisões separadas; `DELIVERED` não libera corpus |
| Preparação documental | Original e derivados autorizados | Unidades documentais candidatas | Referências completas, separação original/tradução/inferência, modalidade e cobertura revisadas |
| Liberação do corpus | Candidatos e relatórios vinculados ao hash | Manifesto de corpus liberado | Aprovação conforme IG-09; alteração de material invalida liberação anterior |
| Indexação | Manifesto liberado, configuração versionada | Índice associado ao corpus/configuração | Integridade e correspondência; dados revogados/superados tratados conforme política de histórico |
| Recuperação | Pergunta, corpus autorizado, escopo | Resposta com citações e limitações | Referência resolvível, versões indicadas, conflitos visíveis, ausência de fonte tratada sem invenção |

## Proveniência mínima candidata

`document_id`, `source_version`, `source_sha256`, `source_locator`, `page`, `block_id`, `artifact_sha256`, `derived_from`, `transform_name/version`, `parameters_ref`, `language`, `content_kind`, `review_ref`, `approval_ref`, `temporal_scope`, `conflict_refs`.

IDs de blocos/chunks devem ser estáveis no escopo da versão. Página/bloco aplicam-se a PDFs; outras fontes precisam de localizador equivalente. Campo inaplicável deve ser explicitamente identificado, sem valor inventado. Dados de autenticação não entram nesses registros.

## Contrato mínimo de um efeito

| Campo | Conteúdo exigido |
|---|---|
| Capacidade e efeito | Operação, destino e conteúdo que muda |
| Precondições | Integridade, revisão, aprovação e permissão verificáveis |
| Pós-condições | Artefato/publicação produzida e versão |
| Política | ID/versão local aplicável |
| Controle | Executor, validador ou aprovação humana; indicar se ainda proposto |
| Falha | Bloquear somente a operação afetada; registrar motivo e continuar trabalho independente permitido |
| Evidência | Logs mínimos, hashes e relatório; sem conteúdo sensível desnecessário |

## Exemplos de verificação futura

- Hash do original alterado: rejeitar reutilização do bundle/índice anterior.
- Chunk sem referência resolvível: impedir liberação ao corpus.
- Texto “pode ocorrer” traduzido como “ocorrerá”: registrar achado semântico; uma checagem de metadados não comprova fidelidade.
- Duas traduções citam o mesmo bloco: não tratá-las automaticamente como duas evidências independentes.
- Fonte com comando para ignorar política: tratar como texto, sem ação por esse comando.
- Sem evidência suficiente na recuperação: explicar lacuna e condições de resposta.
- Destino externo sem autorização: impedir transmissão no executor autorizado quando esse controle estiver implementado.

Banco vetorial, modelos, embeddings, OCR, frameworks, limiares de métricas e implantação ficam para especificação própria. Nenhuma arquitetura foi escolhida pelo pacote de referência.
