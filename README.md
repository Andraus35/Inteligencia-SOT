# Inteligência SOT

Projeto documental independente do Sistema Operacional de Trading. Destino: repositório privado `Andraus35/Inteligencia-SOT`.

**Destino confirmado:** o usuário criou `Andraus35/Inteligencia-SOT`; a integração confirmou visibilidade privada e permissão de escrita em 2026-10-09. A entrega inicial utilizou o conector GitHub; o acesso Git nativo foi revalidado na implantação L4. O envio dos arquivos de governança e qualidade para `main` foi autorizado por DEC-ENVIO-003. Nenhum token deve ser enviado em mensagens.

O objetivo é traduzir documentos e preparar uma base RAG com fontes rastreáveis. A [entrada dos agentes](AGENTS.md), a [política geral 1.0.0](docs/governanca/POLITICA.md), a [matriz de leitura](docs/governanca/LEITURA-AGENTES.md) e as [decisões](docs/governanca/DECISOES.md) orientam o projeto inteiro. A etapa implementada é a tradução auditável de PDF em [`rag/traducao/`](rag/traducao/); PDF e idiomas ainda não foram fornecidos.

- [Master dos agentes](rag/traducao/MASTER-AGENTES.md)
- [Master do projeto de tradução](rag/traducao/MASTER-PROJETO-TRADUCAO.md)
- [Operação e limites do harness](rag/traducao/README-HARNESS.md)
- [Pesquisa, popularidade e protocolo de benchmark](rag/traducao/BENCHMARK-E-SELECAO.md)
- [Evidências de validação](rag/traducao/harness/reports/VALIDACAO.md)
- [Operação do Harness Eval A/B/C](docs/HARNESS-EVAL.md)
- [Resultado do Harness Eval de 2026-10-09](docs/HARNESS-EVAL-RESULTADO.md)
- [Sensores, hooks, CI e gate L4 de Paladini](docs/HARNESS-QUALIDADE.md)
- [Evidências do nível L4](docs/HARNESS-L4-RESULTADO.md)

O `AGENTS.md` da raiz define governança geral; o da tradução especializa somente sua etapa. Não há `AGENTS.md` intermediário em `rag/`. O harness verifica a versão e integridade da governança geral e transporta um snapshot no contexto, sem montar a raiz nos jobs. [Contratos de preparação e RAG](docs/governanca/CONTRATOS.md) permanecem em desenho; LangChain, LangGraph, indexação e integração ao SOT não estão implementados. Revisão da tradução e liberação ao corpus têm aprovações separadas.

Os dados de PDFs, execuções, caches e relatórios locais não são publicados automaticamente, mesmo neste repositório privado. A pasta de tradução é um workspace de etapa; não contém a governança do repositório SOT.

Para futuras publicações por Git, o coordenador pode usar `bash rag/traducao/harness/publicar.sh` com uma credencial válida e checkout sincronizado com o remoto. O conector cria commits próprios: o commit local de preparação não é o histórico remoto. O script confere projeto, branch e privacidade antes do push e não força substituição de histórico. Ele é uma operação de implantação no host, fora dos processos de tradução, e não recebe dados de PDF.
