---
name: translation-coordinator
description: Use somente no papel coordenador desta etapa para preparar inventário, plano, glossário e encaminhar pendências da tradução.
---

# Uso do coordenador

1. Cumprir a entrada obrigatória da etapa e a skill `translation-quality`;
   ler [COMUM.md](../../../specs/COMUM.md) e
   [COORDENADOR.spec.md](../../../specs/COORDENADOR.spec.md).
2. Conferir `TRANSLATION_CONTEXT`: etapa, papel coordenador, run/hash e
   `agent_contract`. Sem PDF/idiomas reais, registrar lacuna; não iniciar tradução.
3. Inventariar blocos/páginas e selecionar piloto representativo, confrontando
   o inventário com o PDF. Propor glossário com fontes e dúvidas para o usuário.
4. Preencher `runs/<id>/coordenador/plan.json` usando
   [template](../../../templates/plan.json). Registrar somente aprovação real,
   ferramentas/modelos/versões e hash do prompt efetivamente escolhido.
5. Solicitar ao host confiável freeze/gates/correct/deliver conforme
   [manual](../../../README-HARNESS.md). O job não escreve em `control/` e
   não executa controles como se tivesse permissão para alterar manifesto.
6. Encaminhar ambiguidades/erros persistentes; não apagar achados nem dispensar
   zero críticos/maiores e duas correções. Entrega técnica não libera corpus.
7. Ao especificar ferramentas, usar o benchmark e as decisões reais de adoção;
   não instalar motores/frameworks nem iniciar rede a partir do job.
