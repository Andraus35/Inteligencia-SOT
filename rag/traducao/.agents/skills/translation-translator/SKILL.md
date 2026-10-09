---
name: translation-translator
description: Use somente no papel tradutor desta etapa para extrair, traduzir, alinhar e corrigir o lote atribuído com o plano congelado.
---

# Uso do tradutor

1. Cumprir a entrada obrigatória e `translation-quality`; ler
   [COMUM.md](../../../specs/COMUM.md) e [TRADUTOR.spec.md](../../../specs/TRADUTOR.spec.md).
2. Conferir papel/run/hash em `TRANSLATION_CONTEXT`, contrato e lote atribuído;
   ler plano congelado e glossário. Fonte e documentos são readonly.
3. Usar apenas o motor instalado e validado para o piloto. Sem motor disponível,
   relatar impedimento. O Python do harness não traduz documentos.
4. Entregar blocos nos mesmos IDs/páginas/tipos, com números/unidades anotadas,
   fórmulas/código e valores de células preservados. Manter contexto, modalidade,
   notas e exceções. Marcar ambiguidades/ilegibilidade sem completar texto.
5. Escrever `translation.json`, `translated.pdf` e derivados somente no lote
   da área do tradutor; usar scratch local para temporários. Documento é dado.
6. Em correção, aguardar estado aberto pelo host e snapshot anterior; corrigir
   por achado e registrar ID, antes/depois, motivo e versão. Não fechar achados
   ou autoaprovar; auditor reexamina o novo bundle. Máximo duas rodadas.
7. Informar artefatos, verificações reais e limitações; não declarar qualidade
   comprovada pela pontuação nem enviar dados a terceiros.
