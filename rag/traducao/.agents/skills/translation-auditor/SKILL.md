---
name: translation-auditor
description: Use somente no papel auditor desta etapa para comparar original e tradução, registrar achados e rever correções com independência.
---

# Uso do auditor

1. Cumprir a entrada obrigatória e `translation-quality`; ler
   [COMUM.md](../../../specs/COMUM.md) e [AUDITOR.spec.md](../../../specs/AUDITOR.spec.md).
2. Conferir papel/run/hash em `TRANSLATION_CONTEXT`, plano/glossário e bundle.
   Comparar original/tradução antes de justificativas e autoavaliação do tradutor.
   O mount readonly não esconde essas justificativas nem prova a ordem de leitura.
3. Examinar cobertura, significado/modalidade, termos, valores, condições,
   tabelas, fórmulas, código e PDF renderizado. Declarar somente checks realizados.
4. Preencher [review.json](../../../templates/review.json) na área do auditor,
   vinculando hash e IDs efetivamente examinados. Localizar achados e evidências;
   classificar gravidade pelo impacto, sem reescrever a tradução.
5. Após correção, rever trecho/contexto e atualizar hash/parecer; não aceitar
   revisão antiga. Crítico/maior aberto bloqueia. Menor aceito requer decisão real.
6. Informar limitações e necessidade de revisão humana competente. Booleans e
   nomes em JSON são declarações, não prova de competência ou consentimento.
7. Entregar parecer ao host para gate; não alterar manifesto, aprovar corpus
   ou usar Score como certificação semântica.
