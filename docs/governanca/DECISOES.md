# Decisões do Inteligência SOT

## DEC-GOV-001 — política geral e primeira implantação

- Data: 2026-10-09. Autoridade: usuário. Estado: APROVADA.
- Evidência: respostas explícitas nesta conversa: “Adotar as dez regras propostas,
  com versões e mudanças aprovadas por você”; “Governança geral e leitura dos agentes,
  ajustando e testando a compatibilidade do harness de tradução”; “Decisões separadas:
  tradução revisada e depois inclusão no corpus aprovada por você”.
- Versão aprovada: IG-01..IG-10, 1.0.0, em [POLITICA.md](POLITICA.md).
- Preferências: regras por etapa, entrada curta, leitura por tarefa/papel, bloqueios
  objetivos para efeitos críticos e aprovação humana de alterações de política.
- RAG: mostrar versões e conflitos com citações, sem escolher verdade por inferência;
  inclusão aprovada por documento/lote após testes e revisão. A aprovação de tradução
  e a aprovação de inclusão são atos distintos, vinculados aos artefatos correspondentes.
- Escopo autorizado agora: documentos gerais, leitura, registro, compatibilidade do
  selfcheck/loader, testes e atualização das instruções reutilizáveis do ambiente.
- Fora desta implantação: serviços RAG, modelos/bancos, envio de documentos,
  publicação Git, integração ao SOT e agentes novos.

## DEC-HARNESS-002 — controles de desenvolvimento e meta L4

- Data: 2026-10-09. Autoridade: usuário. Estado: AUTORIZADA.
- Evidência nesta conversa: “realize as configurações e diretrizes de boas práticas
  tanto do harness eval skill quanto de harness score. deixar o harness score em L4”;
  complemento explícito: “usar harness score de paladini”.
- Escopo: ferramentas pinadas de teste/lint/tipos/formato, hooks locais testáveis,
  workflow CI, pre-commit, leitura operacional e medição oficial da raiz com gate L4.
- Não altera IG-01..IG-10, papéis/limites de tradução, aprovação separada do corpus,
  autorizações de transmissão ou política de publicação. Não aprova cortes de
  conteúdo normativo pelo simples resultado de Score ou Eval.
- Os adaptadores Claude são locais ao projeto; sua configuração não instala hooks
  automáticos no Codex. O scanner mede estrutura; execução exige evidência própria.
- Propagação operacional: entrada raiz, matriz, skill local, guia, Makefile,
  sensores, testes e instruções do ambiente. Recalcular hashes dessas alterações
  autorizadas; snapshots antigos permanecem históricos e não são migrados.

## DEC-ENVIO-003 — enviar arquivos de desenvolvimento ao repositório

- Data: 2026-10-09. Autoridade: usuário. Estado: AUTORIZADA.
- Evidência explícita nesta conversa: “enviar os arquivos necessários para a raiz do repo”.
- Destino: `Andraus35/Inteligencia-SOT`, branch remota `main`, repositório confirmado
  privado na entrega anterior desta sessão. A base Git remota foi conferida antes
  de preparar o envio. Publicar somente fontes, configurações, governança e evidências
  técnicas necessárias; não publicar PDFs, execuções, caches ou decks locais do Eval.
- Não autoriza force-push, substituição de histórico, divulgação de credenciais,
  publicação do ambiente cloud ou liberação de corpus. A regra de aprovação humana
  de mudanças de política continua vigente.

## DEC-SPEC-004 — agentes, skills, benchmark e continuidade

- Data: 2026-10-09. Autoridade: usuário. Estado: AUTORIZADA para elaboração
  e integração operacional; não homologa ferramenta, tradução ou corpus.
- Evidência: “use a metodologia e as skills de especificação utilizadas no projeto
  SOT ENGINER. USE AGENTES PARALELOS PARA AGILIZAR”; escopo respondido:
  “ESPECIFICAÇÃO DOS AGENTES DE TRADUÇÃO E SUAS SKILLS DE USO”.
- Complementos: usar `atomic-spec.md` como referência; elaborar `ROADMAP.md`
  sequencial e `CATÁLOGO.md` com timeline/entregas/contexto de novas sessões;
  incluir LangGraph e LangChain no benchmark, escolhendo durante a especificação.
- Fase atual: somente tradução, buscando desempenho probabilístico e
  determinístico dos agentes/skills/frameworks; elaboração efetiva RAG depois.
- Escopo: método adaptado, specs dos três papéis, skills de uso, contexto/hash
  do harness, testes proporcionais, roadmap/handoff, protocolo comparativo e
  leitura/verificação independente em paralelo, respeitando máximo três ativos.
- IG-01..IG-10 permanece versão 1.0.0; não importa autoridade/aprovações do ZIP,
  regras de trading ou novas permissões. Sem instalação/execução de frameworks,
  PDF real, modelo, corpus ou transmissão por inferência.
- Propagar leitura operacional e hashes dos documentos gerais alterados;
  novas execuções vinculam specs/skills. Históricos/manifestos antigos não são
  migrados, sobrescritos ou apagados. Publicação técnica segue DEC-ENVIO-003.

## Registro e propagação

`registro.json` identifica versão, decisão e hashes dos documentos gerais carregados
e conferidos pelo harness. Não é assinatura de aprovação nem autenticação do usuário:
o coordenador confiável mantém o registro conforme a decisão real. A sandbox impede
escrita dos jobs nesse registro; ferramentas usadas diretamente no host continuam
sujeitas à autorização e às permissões de seu executor.

Documentos transportados: entrada da raiz, política, matriz de leitura e decisões.
Contratos são conferidos por hash no host, sem transporte; nenhum arquivo da raiz é montado nos jobs.
O contexto registra hashes de todos os documentos conferidos. O manifesto conserva
o hash do snapshot geral, e sua alteração exige nova execução, sem migração automática.
Execuções anteriores sem esse vínculo também exigem nova execução; seus arquivos
não são apagados. Os estados de tradução existentes não concedem aprovação ao corpus.

## Mudanças futuras

Propor texto, justificativa, escopo, compatibilidade, impacto em dependentes e testes.
Depois da aprovação real, registrar nova decisão/versão, propagar os documentos e
recalcular os hashes explicitamente. Não atualizar hashes apenas para fazer um gate
passar. Manter decisão anterior identificável pelo histórico e por registros aditivos.

Resultado técnico da implantação: ver [VALIDACAO.md](VALIDACAO.md). Validação técnica
não cria uma decisão humana nem comprova capacidade RAG ainda não implementada.
