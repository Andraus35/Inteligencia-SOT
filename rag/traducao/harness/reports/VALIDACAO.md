# Validação da entrega inicial

Executada em 2026-10-09 UTC. Sem PDF do usuário, sem tradução real e sem implementação de RAG. As fixtures são sintéticas. Não equivalem a auditoria linguística ou certificação de segurança absoluta.

## Verificações executadas

| Verificação | Resultado observado |
|---|---|
| `python3 -B harness/harness.py doctor` | Docker 28.4.0 disponível; imagem fixada presente; jobs com rede `none` |
| `python3 -B harness/harness.py selfcheck` | PASS: escopo, arquivos obrigatórios, política e referências upstream íntegros |
| `TRANSLATION_TEST_DOCKER=1 python3 -B -m unittest discover -s harness/tests -v` | **32 testes, OK**; última execução em 2,772 s |
| Probe real de sandbox | Seis escritas proibidas recusadas; escrita do papel permitida; SOT, credenciais e rede ausentes no job |
| Timeout real | Container de teste explicitamente removido; ausência conferida |
| Revisão técnica independente | Seis problemas encontrados ao longo das revisões foram corrigidos; releitura final sem bloqueador confirmado no escopo examinado |
| SOT original | `git status --porcelain` vazio e HEAD `dcf77fa5f3de5729ab47a4446b6eea0985b5e334`, iguais ao baseline anterior |

Regressões cobrem fonte/plano alterados, symlinks/traversal, omissões, números/unidades, valores de tabela, fórmulas, glossário, achados, revisão desatualizada, fluxo sem piloto, bypass de correções, limite de duas rodadas, concorrência controlada, mutação durante gate, ausência de fallback, preparação do plano e recuperação de JSON inválido/ausente. Ver [revisão técnica](REVISAO-TECNICA.md) para o modelo de ameaça e limitações.

## Harness-eval oficial A+B+C

Escolha expressa do usuário: avaliar **somente AGENTS.md e skill local**, sem os masters; executar **A+B+C completo**. Protocolo upstream 1.8.3, scripts vendorizados íntegros; leitura dos prompts antes dos juízes. Máximo três agentes: coordenador e dois juízes. Segundo juiz sem acesso às notas do primeiro ou gabaritos. Nenhum corte aplicado.

- **A:** zero caminhos/comandos classificados BROKEN. O scanner é de alta precisão e prefere falsos negativos; não executa cada comando.
- **B:** 23 claims reais e quatro plantas; 23 em Review/KEEP, zero Ship/Hold. Gate upstream de armadilhas PASS, sem misses do Judge2.
- **C:** duas superfícies reais e três plantas; ambas Keep-core, zero Slim/Mixed/Hold. Gate de armadilhas PASS, sem misses do Judge2; fan-in sem bloqueios.
- **Limite da calibração:** os scripts upstream usam Judge2 para o gate de plantas. Judge1 marcou duas plantas C como UNCLEAR; PASS não significa acerto perfeito de ambos os juízes. As duas superfícies reais tiveram concordância KEEP-CORE.
- **Modelo:** família Codex/GPT-6 herdada em ambos. ID exato da variante API não é exposto nesta sessão; registrado explicitamente como indisponível, sem inventar identificação. Isso limita reprodução exata e comparação entre modelos. Juízes do mesmo modelo não garantem independência de vieses.

Decks, notas individuais, merges e hashes dos artefatos avaliados estão em [harness-eval-bootstrap](harness-eval-bootstrap/). Os masters foram revisados documentalmente, porém **não receberam pontuação oficial A/B/C**.

## Harness-score

CLI upstream `harness-score@1.8.1`: **37/105 (35%), L1 — Documented**, sem truncamento. Resultado inicial: 32/105; o aumento corresponde à proteção local de arquivos ignorados. O scanner recebe apenas a pasta de tradução; evidência integral em [harness-score.json](harness-score.json). Arquivos vendorizados também estão nessa árvore: a descoberta por convenções é um diagnóstico e não prova integração efetiva de cada ferramenta detectada.

O resultado não mede fidelidade, equivalência semântica ou qualidade do PDF. Não foi criado workflow GitHub na raiz para subir a nota: todos os mecanismos autorizados permanecem dentro de `rag/traducao/`. A infraestrutura tem comandos manuais executáveis; automatização em CI exige futura definição de dispatcher e escopo.

## Pendências para tradução

PDF e par de idiomas; inventário real revisado; glossário aprovado; seleção e instalação confinada de ferramentas/modelos após piloto; auditoria contextual e visual. O runtime inicial contém Python e controles, **não o motor de tradução**. Os campos de aprovação registram declarações, não autenticação humana. O launcher confina seus processos; não governa ferramentas externas executadas diretamente nem um administrador do host.

## Histórico da publicação em nuvem

Criação privada autorizada pelo usuário. `gh repo create Andraus35/Inteligencia-SOT --private` retornou `GraphQL: Resource not accessible by integration (createRepository)`. A alternativa REST `POST /user/repos` com `private=true` retornou HTTP 403 com a mesma mensagem. Os conectores disponíveis não oferecem outra ação de criação. Não é recusa de revisão automática de aprovação: é uma limitação da credencial/integração GitHub.

Na tentativa inicial, nenhum repositório remoto novo ou push foi confirmado. A entrega foi preservada em repositório local independente. `harness/publicar.sh` valida projeto, branch, estado Git e privacidade antes de enviar. O pacote de entrega exclui `.git`, PDFs, runs, scratch e credenciais.

Após o usuário criar o destino e liberar acesso, em 2026-10-09 a integração confirmou `Andraus35/Inteligencia-SOT`, visibilidade privada e permissão de escrita. A credencial do terminal retornou 401, portanto a publicação usa o conector GitHub com commits próprios. O commit local original identifica a preparação; não representa o histórico remoto. A conferência final deve comparar arquivos e conteúdo publicado com o manifesto desta entrega e confirmar novamente a privacidade. Isso não altera os resultados de testes ou os hashes das superfícies avaliadas.

**Publicação concluída e conferida:** a árvore remota no commit `6a28cf97edd89cee890af9d7bc62a9a19de6579f` contém os 63 arquivos da entrega. Todos os caminhos e hashes Git dos blobs coincidem com o índice local, sem árvore truncada; o master dos agentes também foi relido integralmente pelo conector e comparado ao texto enviado. A visibilidade privada foi reconfirmada. Este parágrafo é um registro posterior dessa verificação, publicado em commit subsequente, sem alterar os artefatos de tradução avaliados. Não foram enviados PDFs, runs ou credenciais; o SOT permaneceu intacto.
