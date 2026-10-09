# Leitura por tarefa e papel

Versão de política: 1.0.0. Governança geral implantada por DEC-GOV-001.

## Núcleo e aprofundamento

Núcleo: `AGENTS.md` da raiz → política vigente → linha aplicável nesta matriz → governança da etapa → procedimento do papel. Ler decisões novas que afetem o escopo. Sem versão confiável ou com contexto incompleto, recarregar os documentos necessários; um carimbo não prova leitura.

Tarefa local simples: núcleo e documentos diretamente afetados. Mudança de contrato, política, fonte ou aprovação: acrescentar decisões, interfaces, impacto e verificação correspondente. Efeito crítico, exposição externa ou regressão de isolamento: acrescentar análise de falha, testes negativos e revisão apropriada. Economia de leitura não remove precondições obrigatórias.

| Tarefa / papel | Leitura específica | Evidência esperada |
|---|---|---|
| Setup e manutenção geral | README; matriz; contratos e decisões afetados | Estado do checkout, operações executadas e limitações |
| Desenvolvimento do harness de tradução | `rag/traducao/AGENTS.md`, os dois masters, `README-HARNESS.md`, implementação e testes afetados | Checagens proporcionais; integração Docker quando o launcher/isolamento mudar |
| Manutenção de Harness Eval/Score | Skill `harness-quality`, `docs/HARNESS-QUALIDADE.md`, `docs/HARNESS-EVAL.md`, protocolo vendorizado de Eval e controles afetados | Score oficial por escopo; checks executados; leitura de dependentes; modelos/calibração quando houver juízes |
| Coordenação de tradução | Governança local completa; skill `translation-quality`; política local; plano e inventário reais | PDF/hash, idiomas, glossário aprovado, plano congelado, ID de execução |
| Tradução/correção | Governança local completa; procedimento; contexto de execução, fonte e plano congelado; lote atribuído | Artefatos na área permitida, blocos alinhados e registro de correções |
| Auditoria de tradução | Mesma governança e bundle; original e tradução antes de justificativas do tradutor | Achados com localização/evidência, checks reais e hash revisado |
| Proposta de preparação documental | Contrato candidato da etapa; fontes e transformações; requisitos de privacidade | Metadados rastreáveis e critérios verificáveis; implementação ainda pendente |
| Proposta de indexação/recuperação | Contratos candidatos; corpus autorizado, versões, conflitos e casos de avaliação | Plano de citação, invalidação e avaliação sem inventar resultados |
| Mudança de política | Política atual, proposta, decisões e todos os dependentes afetados | Justificativa, impacto, testes e solicitação de aprovação concreta |

## Releitura e sincronização

Reabrir documentos quando seu hash/versão mudar, houver nova decisão em escopo, surgir conflito, mudar o papel ou faltar contexto. O launcher registra versão e hashes da política e documentos transportados; isso não comprova leitura pelo agente. Pendências de leitura devem ser relatadas pelo agente. O livro-razão registra decisão, escopo e propagação; a checagem compara referências, sem decidir sozinha o escopo semântico.

Não duplicar no perfil listas do “próximo trabalho” que podem envelhecer; apontar o registro atual. A governança local da tradução mantém suas leituras obrigatórias até eventual emenda aprovada.
