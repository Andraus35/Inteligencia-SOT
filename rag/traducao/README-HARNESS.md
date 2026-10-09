# Operação do harness exclusivo da tradução

Este workspace está em `rag/traducao/`, separado do repositório SOT. Todos os comandos abaixo são executados a partir desta pasta. O único arquivo de descoberta de instruções é `AGENTS.md` aqui; não há cópia na raiz, em `rag/` ou em diretório global de agente. O loader gera `work/<run-id>/<papel>/context.json` com a etapa, papel, hash e instruções. A presença de um Markdown não impede leitores genéricos de abri-lo fora da etapa: o isolamento aplicado é ao processo iniciado pelo launcher.

## Capacidades implementadas

- Validação de caminhos relativos, traversal e links simbólicos; escrita atômica de JSON.
- Hash do PDF original, da política, do plano congelado e do conjunto de artefatos de cada lote. Mudanças invalidam a revisão anterior.
- Inventário original congelado pelo coordenador; cobertura e IDs, páginas e tipos de bloco conferidos contra esse inventário.
- Comparação lexical de números, tokens protegidos e termos obrigatórios; preservação literal de fórmulas/código e valores por célula de tabela.
- Auditoria identificada, cobertura integral declarada e checks obrigatórios. Erros críticos/maiores não podem ser dispensados; menores precisam estar resolvidos ou aceitos explicitamente.
- Estados `CREATED → PLANNED → PILOT_TRANSLATED → PILOT_ACCEPTED → TRANSLATED → ACCEPTED → DELIVERED`, sem pular piloto. Reprovação passa para `PILOT_FAILED`/`FULL_FAILED`; somente `correct` abre `PILOT_CORRECTING`/`FULL_CORRECTING`, seguido de novo `mark-translated`. Até duas correções por lote, com snapshot anterior e motivo.
- Sandbox Docker: etapa montada somente leitura, escrita liberada apenas no diretório do papel e scratch, sem rede, sem socket Docker montado, usuário não privilegiado, capabilities removidas, recursos limitados e imagem fixada por digest. Nenhum token do host é passado pelo launcher.
- Locks no host: este fluxo lança jobs sequencialmente (limite mais restrito que o time de três agentes). Controles não competem com jobs e não há escritores concorrentes. Timeout de 900 segundos com remoção explícita do container; cleanup não confirmado coloca runtime em quarentena. Containers órfãos bloqueiam novos jobs. Encerramento por limite não equivale a tradução concluída.
- Integridade das referências upstream e avaliação independente da infraestrutura.

O coordenador confiável executa comandos de controle no host. Processos de trabalho não podem editar manifesto, política, governança ou o original. O launcher não restringe ferramentas externas usadas diretamente fora dele nem autentica uma pessoa por uma string em JSON. Agentes da interface só ficam sujeitos a essas montagens se suas ferramentas forem efetivamente executadas pelo launcher.

O gate usa locks exclusivos contra os jobs, confere o mesmo bundle antes/depois da avaliação e vincula a aprovação a esse hash. Um `SIGKILL` do launcher não executa cleanup; por isso containers remanescentes com o label da etapa bloqueiam o próximo launch. A recuperação exige conferir/parar o container identificado e remover a quarentena somente após verificação; não existe comando automático que dispense essa evidência.

## Limites explícitos

O runtime base tem Python, não um tradutor instalado. Este harness **não traduz PDFs**, não implementa RAG e não prova equivalência semântica. Comparação lexical não detecta todas as alterações de significado, unidades não anotadas ou inversões de regras: isso depende da auditoria contextual. O inventário exige revisão contra o PDF, pois cobertura perfeita de um inventário incompleto não comprova cobertura da fonte.

A verificação de PDF confere assinatura e integridade, não validade completa, OCR, paginação ou renderização. Esses aspectos devem ser conferidos pelo auditor e, quando necessário, ferramentas específicas instaladas na imagem aprovada do piloto. A revisão registra `layout=true` somente após inspeção real. Hash do bundle inclui PDF e todos os arquivos do lote; novos arquivos ou alterações após revisão requerem novo hash e nova auditoria.

São declarações registradas, e não autenticação de consentimento humano: `glossary_approved_by`, `reviewer` e `accepted_by`. O coordenador deve registrar apenas decisões efetivamente dadas pelo usuário. O runtime é offline por padrão. Tradução remota, imagem com modelos e mudanças de política exigem escopo próprio; não há fallback remoto nem bypass sem sandbox.

## Estrutura e ownership

```text
rag/traducao/
  AGENTS.md
  MASTER-AGENTES.md
  MASTER-PROJETO-TRADUCAO.md
  README-HARNESS.md
  .agents/skills/translation-quality/SKILL.md
  harness/
    harness.py
    policy.json
    tests/test_harness.py
    vendor/                     # referências fixadas, sem registro global
  templates/                    # incompletos por intenção; não são dados de execução
  input/                        # PDF fonte; ignorado pelo Git
  runs/<run-id>/
    control/                    # manifesto, gates, snapshots: coordenador confiável
    coordenador/                # plano e inventário congelado
    tradutor/pilot/              # translation.json, translated.pdf e derivados
    tradutor/full/
    auditor/pilot/               # review.json
    auditor/full/
  work/                         # scratch, contextos, locks: ignorado pelo Git
  .harness-eval/                 # relatórios upstream locais: ignorado pelo Git
```

## Validação da infraestrutura

```sh
python3 -B harness/harness.py doctor
python3 -B harness/harness.py selfcheck
python3 -B -m unittest discover -s harness/tests -v
TRANSLATION_TEST_DOCKER=1 python3 -B -m unittest discover -s harness/tests -v
python3 -B harness/harness.py score
```

O teste Docker tenta escrever no original, governança, manifesto, papel alheio e sistema; testa também ausência do SOT/credenciais, escrita permitida do papel e bloqueio de conexão externa. A imagem deve estar previamente disponível no daemon; o launcher usa `--pull=never`. Sua falta bloqueia a execução.

Para disponibilizar exatamente a imagem fixada (download de infraestrutura, sem conteúdo documental):

```sh
docker pull python@sha256:05cda9777409a9c3ffddd94a4c476b79f0769a0b4857f0c7ed9226b6800b0d6f
```

## Execução do PDF real

Ainda não há PDF ou par de idiomas. O exemplo abaixo usa um arquivo e ID deliberadamente ilustrativos e **não foi executado**; substituí-los conforme o documento real. Criar/importar o PDF em `input/` com autorização, e não publicar seu conteúdo por inferência.

```sh
python3 -B harness/harness.py init-run --run-id documento-001 --source input/documento.pdf --source-language en --target-language pt-BR
```

Preencher `templates/plan.json` em `runs/documento-001/coordenador/plan.json`. Registrar o par escolhido, glossário aprovado, inventário revisado, piloto, ferramentas/versões, modelos/parâmetros e SHA-256 do prompt. `privacy` deve ser `local`. `source_blocks` usa IDs, página, tipo e texto; tabelas acrescentam `cells`, fórmula/código `preserved_content`, unidades/identificadores podem usar `protected_tokens`.

```sh
python3 -B harness/harness.py freeze-plan --run-id documento-001 --plan runs/documento-001/coordenador/plan.json
python3 -B harness/harness.py launch --run-id documento-001 --role tradutor -- python -c 'import os; print(os.environ["TRANSLATION_CONTEXT"])'
```

O segundo comando só demonstra o loader, não executa tradução. Após instalar e validar uma imagem adequada para o tradutor, o comando real deverá produzir `translation.json` (lista dos blocos traduzidos no mesmo esquema) e `translated.pdf` no diretório do lote. A versão inicial não suporta exclusões/divisões/fusões de blocos: o inventário é preservado integralmente.

```sh
python3 -B harness/harness.py mark-translated --run-id documento-001 --batch pilot
python3 -B harness/harness.py bundle --run-id documento-001 --batch pilot
```

O auditor usa o hash retornado em seu `review.json`, preenche todos os checks após revisão e relaciona todos os blocos. Para cada achado: `id`, `block_id`, `severity` (`critical|major|minor`), `status` (`open|resolved|accepted`), `source_evidence`, `translation_evidence`, `reason`; resolvidos requerem `resolution_evidence`, menores aceitos requerem `accepted_by`.

```sh
python3 -B harness/harness.py gate --run-id documento-001 --batch pilot
python3 -B harness/harness.py correct --run-id documento-001 --batch pilot --reason 'Corrigir os achados documentados na revisão do piloto'
```

Executar `correct` apenas após gate reprovado. O snapshot é feito **antes** da alteração. Depois o tradutor corrige, o auditor atualiza o hash e revisa novamente, e o gate é repetido. Após piloto aceito, repetir para `full`; por fim executar `deliver --run-id documento-001`. `DELIVERED` significa bundle estruturado com os contratos implementados atendidos, não integração ao SOT nem certificação da tradução.

## Harness Eval: procedimento upstream, escopo local

Fonte: Tech Leads Club `harness-eval` v1.8.3, commit `6df68d52028b9261058231e0f4998048c0352f45`. A skill é de **avaliação**, não de setup; foi consultada para desenhar a avaliação deste harness. Cópia integral e protocolo estão em `harness/vendor/harness-eval/`.

```sh
python3 -B harness/harness.py eval-inventory --run-id bootstrap
```

Antes de Track A, ler os candidatos opcionais e cumprir Q1/Q2 do `SKILL.md`: escolher documentos opcionais e orçamento de B/C. Não executar B/C por inferência. A verifica caminhos/comandos; B examina redundância com dois juízes e armadilhas; C utilidade com dois juízes, armadilhas e dependências de leitura. Relatório não autoriza cortes.

Após registrar a escolha do usuário:

```sh
python3 -B harness/vendor/harness-eval/scripts/track_a_correctness.py --root . --run-id bootstrap
```

Os resultados ficam nesta etapa, nunca na raiz do projeto/SOT. Se forem autorizados B/C, usar o coordenador e dois juízes independentes, sem exceder três agentes; o segundo não vê as notas do primeiro ou o gabarito das armadilhas. Ler os prompts upstream antes disso. Correções do harness devem responder a evidência; cortes de governança propostos por B/C exigem decisão após relatório.

## Harness Score: diagnóstico, não meta artificial

Fonte: [paladini/harness-score](https://github.com/paladini/harness-score), ligado à comunidade Tech Leads Club. A skill upstream se chama `harness-engineering`, não `harness-score`; está em `harness/vendor/harness-engineering/`. Referência fixada no commit `90f67d40d56cfe8bd11112e76f48880752f196d1`. CLI npm `harness-score@1.8.1`, sem dependências runtime, fixada por integridade SHA-512 e hashes individuais em `provenance.json`.

O scanner recebe apenas esta pasta e não faz chamadas LLM. Mede presença/estrutura de infraestrutura; não testa verdade das regras ou fidelidade do PDF. Não criar regras globais ou CI fora desta etapa para aumentar pontuação. CI automático GitHub não foi criado: workflows são descobertos na raiz `.github/workflows/`, incompatível com a restrição atual de manter todos os mecanismos dentro da etapa. As verificações são executáveis manualmente e podem ser conectadas por uma futura autorização explícita de dispatcher.

## Prevenção e correção de regressões

Reproduzir erro com fixture sem conteúdo do PDF → corrigir o mecanismo responsável → executar testes afetados → auditoria independente → suíte completa e avaliação de infraestrutura. Não alterar fontes upstream vendorizadas; adaptações são implementadas no harness local e atribuídas. Nunca apagar achados para melhorar nota. Configurações, scripts e masters são revisados como artefatos do projeto, e não por agentes de tradução com permissão de escrita na governança.
