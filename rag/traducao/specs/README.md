# Especificações dos agentes e skills de tradução

Versão 1.0.0; contratos documentados e implementação parcial. Autorização de
especificar não é homologação de ferramenta, tradução ou corpus.

Para desenvolvimento, ler a [metodologia](../../../docs/ESPECIFICACAO-TRADUCAO.md).
Para atuar num job, ler governança obrigatória da etapa, contrato comum e somente
o aprofundamento do papel, além do plano/bundle reais:

| Papel | Spec | Skill de uso |
|---|---|---|
| coordenador | [COORDENADOR.spec.md](COORDENADOR.spec.md) | [translation-coordinator](../.agents/skills/translation-coordinator/SKILL.md) |
| tradutor | [TRADUTOR.spec.md](TRADUTOR.spec.md) | [translation-translator](../.agents/skills/translation-translator/SKILL.md) |
| auditor | [AUDITOR.spec.md](AUDITOR.spec.md) | [translation-auditor](../.agents/skills/translation-auditor/SKILL.md) |

[COMUM.md](COMUM.md) contém invariantes, efeitos e BASpecs compartilhadas.
[PLAN.md](PLAN.md) separa mecanismos existentes de escolhas pendentes;
[TASKS.md](TASKS.md) mapeia evidências e próximos passos;
[PESQUISA.md](PESQUISA.md) preserva origem da adaptação e conflitos de fonte.

O contexto `agent_contract` contém documentos do papel e hashes; o manifesto
vincula o conjunto dos três contratos. Ausência ou mudança bloqueia a operação
afetada. Uma skill é procedimento, não agente adicional ou motor de tradução.
