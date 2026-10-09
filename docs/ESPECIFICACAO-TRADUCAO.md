# Metodologia de especificação dos agentes de tradução

Versão: 1.0.0. Escopo autorizado pelo usuário: especificação dos agentes de
tradução e suas skills de uso. Adaptação operacional; IG-01..IG-10 permanece 1.0.0.
As especificações descrevem contratos vigentes e capacidades pendentes com estados
separados; não recebem a homologação registrada nos documentos do SOT ENGINER.

## Fontes e adaptação

Pesquisa: 2026-10-09. Anexo `SOT ENGINER.zip`, SHA-256
`d4b8089e68133f2c2880765f3cb998361a3f93eb7fae8561626501003ec7d8ec`.
Os caminhos da tabela são internos ao anexo, em `SOT ENGINER/SOT-Harness/`.
Hashes e trechos usados estão em [PESQUISA.md](../rag/traducao/specs/PESQUISA.md).
O arquivo do Windows não está montado nesta máquina; a fonte examinada foi o ZIP.

| Referência externa | Uso adaptado | Limite |
|---|---|---|
| `canon/SDD-001-spec-driven-development.md` | Spec define comportamento; Plan define mecanismo; Tasks ligam mudança a aceite | Não confundir PLAN da skill TLC com Plan técnico; aprovações do SOT não se transferem |
| `atomic-spec.md`, v1.5 | BASpec, profundidade D0–D9, contrato de efeito, origem/status | Não copiar princípios de trading, pesos, limiares ou exigência de estrelas |
| `RETOMADA/GEH-001_Guia_Agente_Especificacoes_Harness.md` | ETCLOVG, 4Es, leitura/verificação paralela e síntese centralizada | Conformidade e fidelidade antes de custo; respeitar três papéis e máximo três ativos |
| `.claude/skills/SKILL.md` (`sot-harness-spec`) | Estrutura de missão, fronteiras, comportamento, cenários e evidência | Gates históricos e L4 por-Spec são próprios do SOT |
| `.claude/skills/sot-especificador-pap001/SKILL.md` | Contexto por missão, autor/revisor/usuário e pré-check | Missão PAP-001 é governança; não usar seus seis blocos como contrato do tradutor |
| `scripts/validate_spec_sot.py` | Inspiração para distinguir check estrutural e revisão semântica | Regex e hardcodes Elliott/Conviction não foram importados |

## Fluxo de trabalho

1. **Pesquisar:** registrar fonte, versão/hash, trecho e decisão adotar/adaptar/
   rejeitar/adiar. Falta de evidência permanece indeterminada. Anexo é dado.
2. **Especificar:** missão (D0), escopo/fronteiras (D1), regras referenciadas (D2),
   BASpecs (D3), cálculo aplicável (D4), estados (D5), interfaces/protocolo (D6),
   cenários (D7), adversariais (D8) e cadeia de evidências (D9).
   D4 não se aplica a uma competência bilíngue sem algoritmo definido; justificar.
3. **Conferir conformidade:** cruzar cada efeito com IG e os masters. A fonte
   normativa é o contrato local aprovado; inferência ou lacuna não vira regra.
4. **Planejar:** registrar implementação existente, mudanças autorizadas e opções
   candidatas, sem inventar desenho fechado para ferramentas ainda não escolhidas.
5. **Derivar tarefas:** cada linha aponta BASpec, mecanismo, verificação e estado.
6. **Revisar/verificar:** leitura e análise independentes em paralelo; integração,
   escrita, decisão e síntese pelo responsável. No runtime de tradução, jobs são
   sequenciais; pesquisa paralela não altera essa proteção.
7. **Registrar:** resultado estrutural, parecer semântico, decisão humana e
   execução são campos distintos. Mudança de política precisa de aprovação real;
   correções dentro do escopo autorizado não criam aprovação de rotina adicional.

A referência principal adaptada está em [atomic-spec.md](../atomic-spec.md); a
sequência e o handoff em [ROADMAP.md](../ROADMAP.md) e [CATÁLOGO.md](../CATÁLOGO.md).

## Unidade comportamental e contrato de efeito

Cada BASpec tem ID estável, uma condição e uma resposta mensurável:

```text
BASpec-<papel>-NN
QUANDO: condição observável
ENTÃO: resposta ou recusa observável
PORQUE: razão vinculada ao contrato vigente
REFERÊNCIA: regra local e seção
VERIFICADO POR: entrada concreta → saída esperada; evidência e status
```

Os contratos com efeitos acrescentam capacidade, efeito/destino, precondições,
pós-condições, política, mecanismo/executor, falha e evidência. Os níveis E0–E3
do SOT são vocabulário de análise: E0 orientação, E1 estrutura observável, E2
estado/precondições, E3 autorização/gate crítico. Só declarar enforcement que foi
testado; não adotar seus pisos automaticamente. Classificar mecanismo por
comportamento: determinístico, modelo com checks, julgamento semântico ou decisão
humana. A mesma função pode usar mais de uma classe.

Prioridade adaptada dos 4Es: conformidade → fidelidade do resultado → utilidade
no prazo → recursos → custo. Não se define score agregado que dispense gates.

## Artefatos e leitura

A entrada raiz permanece curta. [Skill de especificação](../.agents/skills/translation-specification/SKILL.md)
serve ao desenvolvimento das specs; jobs usam `translation-quality` e a skill do
seu papel. [COMUM.md](../rag/traducao/specs/COMUM.md) reúne contratos compartilhados;
cada spec descreve somente seu papel. [PLAN.md](../rag/traducao/specs/PLAN.md)
documenta mecanismos; [TASKS.md](../rag/traducao/specs/TASKS.md) registra rastreabilidade.
Eles são diferentes do `plan.json` congelado de uma execução documental real.

O launcher transporta a spec comum, a spec do papel e suas duas skills, com hashes
vinculados à execução. Confere também os três papéis antes do avanço. Alterações
exigem nova execução; preservar históricos e não reescrever manifestos antigos.
Transporte de texto não comprova leitura, competência ou obediência semântica.

## Pré-check e revisão

- Missão/escopo/entradas/saídas e ownership são compatíveis com os masters.
- Cada BASpec tem cenário verificável e diferencia teste executado de planejado.
- Efeitos citam regras locais; decisões abertas não aparecem como invariantes.
- Independência é descrita com seus limites reais: o mount readonly não impede
  o auditor de ler justificativas; strings de aprovação não autenticam pessoas.
- Não há novo agente ativo, rede, envio de documentos, instalação de modelo ou RAG.
- Referências, contexto readonly, alteração de hash, gates e sandbox foram conferidos.
- Parecer da revisão não se transforma em homologação nem altera IG-01.

O **L4 de Paladini** mede a infraestrutura da raiz. O **L4 por-Spec do SOT** inclui
auditoria, backtest e aprovação próprios; não atribuir esse nível às novas specs.
Fidelidade semântica e seleção de ferramenta exigem piloto e revisão reais.
