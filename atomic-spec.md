# Unidade atômica de especificação — Inteligência SOT

ID: ATOMIC-TR-001. Versão: 1.0.0. Estado: referência operacional adaptada.
Escopo atual: agentes, skills e frameworks da tradução. Política vigente:
IG-01..IG-10, 1.0.0. Fonte principal: `atomic-spec.md` v1.5 do SOT ENGINER,
identificada por caminho, hash e trechos em
[PESQUISA.md](rag/traducao/specs/PESQUISA.md). Aprovações do SOT não se transferem.

## Unidade mínima: BASpec

```text
BASpec-<papel>-NN:
  QUANDO: uma condição observável
  ENTÃO: uma resposta mensurável
  PORQUE: razão ligada ao contrato vigente
  REFERÊNCIA: regra local e seção; origem e status da alegação
  VERIFICADO POR:
    DADO: entrada/estado concreto
    QUANDO: evento
    ENTÃO: saída/recusa esperada
    EVIDÊNCIA: teste, parecer ou decisão; executado ou planejado
```

Uma condição, uma resposta e cenário verificável; evitar reunir obrigações
independentes num único ID. Referir no máximo duas regras centrais por unidade;
aplicabilidade ampla fica no contrato comum. Não confundir teste determinístico
com prova de significado, nem parecer com consentimento humano.

## Profundidade D0–D9

| Dimensão | Entrega proporcional para a tradução |
|---|---|
| D0 intenção | Missão curta do papel |
| D1 escopo | Responsabilidade, fronteiras e ownership |
| D2 regras | Referências a IG, masters e política especializada vigentes |
| D3 comportamento | BASpec por situação/efeito |
| D4 algoritmo | Fórmula/pseudocódigo de checks determinísticos; justificar inaplicabilidade semântica |
| D5 estado | Estados permitidos, transições e recusa |
| D6 protocolo | Input/output, leitura, dependências e handoff |
| D7 teste | Cenários positivos/negativos concretos com resultado esperado |
| D8 adversarial | Omissão, adulteração, stale hash, injeção, autoaprovação e bypass |
| D9 auditoria | Hashes, eventos, evidências, versão e limitações reconstituíveis |

## Efeitos, mecanismos e limites

Contrato de efeito: **CAPABILITY / EFFECT / PRECOND / POSTCOND / POLICY /
LEVEL / FAILURE-MODE / EVIDENCE**; acrescentar executor real e o que falta
implementar. Detector aponta suspeita; gate impede efeito no executor.

E0 orientação; E1 estrutura/evidência; E2 estado/precondições; E3 autorização/
gate crítico. São categorias de análise, sem importar os pisos obrigatórios do
SOT. Nunca declarar E3 de autenticação humana com base numa string JSON.

Classes por comportamento, adaptadas da fonte: D determinístico; H modelo mais
checks determinísticos; P julgamento probabilístico avaliado; C controle de
autorização/efeito. Não reduzir agente inteiro a uma classe. Declarar mecanismo,
limite de tentativas, critério de parada e gate correspondente. O fluxo vigente
permite no máximo duas correções por lote; esgotamento bloqueia e encaminha.

**Desempenho determinístico:** casos válidos/negativos, integridade, gates,
isolamento e erros de recusa nos cenários definidos. **Desempenho probabilístico:**
fidelidade bilíngue/contextual, MQM por gravidade, qualidade terminológica e
visual, repetição controlada e discordância entre revisores. Não converter
temperatura zero ou zero falhas numa amostra em garantia universal.

4Es adaptados: conformidade/fidelidade primeiro, utilidade no prazo depois,
recursos e custo subordinados. Gate material não pode ser compensado por média.
Seleção compara agentes, skills, motores e frameworks sem atribuir ao framework
a qualidade do modelo. Evidências desconhecidas continuam indeterminadas.

## Origem, conformidade e ciclo

Classificar alegações: `[FONTE LOCAL]`, `[EXTERNO]`, `[INFERÊNCIA]`, `[PROPOSTA]`,
`[DECISÃO NECESSÁRIA]`. Documentado, testado, revisado, aprovado e executado são
estados diferentes. Não usar decisão aberta como invariante fechado.

Constitution Check adaptado = conferir IG-01..IG-10 e contrato especializado,
com impacto/compatibilidade dos efeitos. Não importar Elliott, Conviction,
Blackboard ou homologações históricas de outro projeto.

Pesquisa → Spec comportamental → revisão/conformidade → Plan técnico → Tasks
rastreáveis → execução autorizada → Verify → atualização do
[CATÁLOGO.md](CATÁLOGO.md). A aprovação humana aplica-se às decisões exigidas
pelas regras locais; a metodologia não cria paradas adicionais de rotina.
Mudança de política segue IG-01, com proposta concreta, impacto e testes.

O [ROADMAP.md](ROADMAP.md) conduz as entregas. [Metodologia e skills](docs/ESPECIFICACAO-TRADUCAO.md)
operacionalizam esta referência. L4 de Paladini não equivale ao L4 por-Spec do SOT.
