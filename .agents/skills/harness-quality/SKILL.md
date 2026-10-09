---
name: harness-quality
description: Use quando a tarefa pedir Harness Eval, Harness Score de Paladini, melhoria de diretrizes ou validação dos controles e sensores deste projeto.
---

# Qualidade do harness do Inteligência SOT

1. Ler a entrada raiz, política e matriz aplicáveis; registrar tarefa e efeito.
2. Consultar `docs/HARNESS-QUALIDADE.md` e `docs/HARNESS-EVAL.md` para comandos,
   escopo e limites. Usar o checkout existente e preservar artefatos anteriores.
3. Medir o Score upstream com `make score-check`: Paladini 1.8.1, raiz do projeto,
   gate maturity L4, sem pesos customizados nem dependências globalmente detectadas.
4. Executar `make check` após mudança dos controles; informar passados, falhados,
   pulados e não executados. O runtime Docker é necessário ao teste de isolamento.
5. Para Eval, ler integralmente o protocolo vendorizado apontado pelo guia.
   Confirmar Q1 (opcionais) e Q2 (A/AB/AC/ABC) com o usuário antes da rodada;
   autorização já explícita na conversa pode ser reutilizada no mesmo escopo.
6. Criar um ID novo; executar inventário e A pelo adaptador. B/C exigem escolhas
   registradas, dois juízes por trilha, contextos novos e segundo juiz cego.
   Máximo três agentes ativos com coordenador; juízes não criam outros agentes.
7. Separar redundância de utilidade; preservar contratos/checklists exigidos por
   consumidores. Apresentar scores, calibração, modelo e limites, sem autoaplicar
   Ship/Slim/Mixed. Emenda autorizada exige compatibilidade, integridade e nova rodada.
8. Score é evidência estrutural; execução de CI/hooks e conteúdo documental exigem
   evidência própria. DELIVERED não libera RAG. Não ativar modelos, corpus, publicação
   ou serviços com base na nota.
