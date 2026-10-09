# Resultado — especificação dos agentes e skills

Data: 2026-10-09. Escopo: tradução primeiro; RAG efetivo posterior.

Referência principal adaptada: `atomic-spec.md` v1.5 do pacote SOT ENGINER;
pesquisa/hash em `rag/traducao/specs/PESQUISA.md`. Foram criados método local,
contrato comum, três specs, quatro skills (uma de especificação, três de uso),
Plan/Tasks, roadmap e catálogo/handoff. A skill comum existente direciona cada
papel. LangGraph e LangChain entram no protocolo, sem vencedor antecipado.

O launcher transporta contrato/spec/skills do papel em contexto readonly e
vincula o conjunto dos três contratos ao manifesto. Ausência, arquivo vazio,
symlink, mudança ou legado sem vínculo bloqueiam a operação; nenhuma migração
silenciosa de execuções. Permissões, estados, três papéis, duas correções e IG
1.0.0 permanecem vigentes. Corrigido também o manual que ainda descrevia CI
como não criado, apesar da autorização/implementação anterior na raiz.

## Verificação

- Lint, tipos, formato e integridade: passaram.
- Testes: **69 passaram**, incluindo Docker real, sem pulados nesta execução.
  Cinco novos testes cobrem contexto específico por papel, mudança da spec de
  outro papel, ausência de spec/skill, vazio/symlink e manifesto legado.
- Harness Score oficial Paladini 1.8.1, raiz: **L4, 98/105 (93%)**,
  sem alteração de pesos ou dependências vendorizadas.
- Eval A final: `2026-10-09-spec-final`, **zero BROKEN**, duas entradas, seis
  skills ativas e cinco documentos opcionais. B/C novas não executadas; resultados
  A+B+C anteriores permanecem vinculados às fontes históricas.
- Dois revisores independentes examinaram método/specs e integração/skills.
  Corrigidos mapa das 16 BASpecs, correspondência exata entre cenários/testes
  e tabela de candidatos. Releitura confirmou resolução, sem impedimento adicional.
  Essa revisão documental não é julgamento B/C do Harness Eval.

## Limitações e sequência

Não foi executado benchmark de frameworks, tradução/PDF/OCR, piloto semântico
ou RAG. O runtime contém controles Python, sem motor/modelo selecionado. A ordem
de leitura do auditor é procedural; mounts não escondem justificativas. Campos
de aprovação/identidade são declarações, não autenticação de pessoa.

Próximo: preparar configurações e comparação (T2), obter entrada/reference do
piloto (T3), avaliar controles/qualidade (T4/T5) e selecionar por evidência (T6).
`CATÁLOGO.md` registra posição e handoff; `ROADMAP.md` conduz entregas seguintes.
Score L4 e Eval estrutural não certificam competência bilíngue nem corpus.
