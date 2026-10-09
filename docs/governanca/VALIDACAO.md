# Validação da primeira implantação

Data: 2026-10-09. Decisão autorizadora: DEC-GOV-001. Política geral: 1.0.0.

## Resultado na instância atual

A partir de `rag/traducao/`:

- `python3 -B harness/harness.py selfcheck`: PASS, política geral 1.0.0 e integridade
  das referências vendorizadas conferidas.
- `python3 -B harness/harness.py doctor`: Docker disponível e imagem fixada presente.
- `TRANSLATION_TEST_DOCKER=1 python3 -B -m unittest discover -s harness/tests -v`:
  **41 testes passaram; zero falhas e zero skips**.
- `git diff --check`: sem erros de whitespace.

Nove regressões novas cobrem vínculo do snapshot, alteração de política, documento
ausente, versão incompatível, aprovação não registrada, promoção indevida da governança
de tradução para a raiz, governança intermediária/links simbólicos, mudança registrada
após início de execução e execução legada sem vínculo.

O teste real de contêiner verificou sete escritas negadas (incluindo contexto), escrita
permitida ao papel, integridade do snapshot, ausência da raiz do projeto e do SOT,
ausência das credenciais verificadas e bloqueio de conexão externa. O teste de timeout
confirmou remoção explícita do contêiner. A documentação não substitui esses controles.

## Limites

Fixtures sintéticas validam controles e fluxo; não houve tradução real, auditoria
linguística independente ou ingestão RAG. Hashes e registro detectam inconsistência,
mas não autenticam uma pessoa nem provam leitura/compreensão pelos agentes. O host
coordenador é confiável e continua responsável por manter hashes após decisões reais.
O snapshot protege contexto no contêiner; não controla ferramentas executadas no host.

Os contratos de RAG permanecem em desenho. Revisão da tradução e autorização de inclusão
no corpus são decisões separadas; o harness de tradução não implementa a liberação.

Mudanças estão no checkout local, sem commit, push ou publicação do ambiente. As
instruções de inicialização salvas no rascunho são configuração, não prova de restauração
em tarefa nova. Publicação/snapshot ficam a cargo do produto e do usuário.
