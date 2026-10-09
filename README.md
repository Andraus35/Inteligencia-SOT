# Inteligência SOT

Projeto documental independente do Sistema Operacional de Trading. Destino: repositório privado `Andraus35/Inteligencia-SOT`.

**Destino confirmado:** o usuário criou `Andraus35/Inteligencia-SOT`; a integração confirmou visibilidade privada e permissão de escrita em 2026-10-09. A publicação desta entrega utiliza o conector GitHub. A tentativa anterior de criação automática retornou 403; a credencial do terminal agora retorna 401. Nenhum token deve ser enviado em mensagens.

A etapa inicial é a tradução auditável de PDF. Seus documentos, instruções e mecanismos estão exclusivamente em [`rag/traducao/`](rag/traducao/). O PDF e os idiomas ainda não foram fornecidos.

- [Master dos agentes](rag/traducao/MASTER-AGENTES.md)
- [Master do projeto de tradução](rag/traducao/MASTER-PROJETO-TRADUCAO.md)
- [Operação e limites do harness](rag/traducao/README-HARNESS.md)
- [Pesquisa, popularidade e protocolo de benchmark](rag/traducao/BENCHMARK-E-SELECAO.md)
- [Evidências de validação](rag/traducao/harness/reports/VALIDACAO.md)

Não há `AGENTS.md` na raiz ou em `rag/`: as instruções de tradução não são governança geral deste projeto. Outras etapas devem ter seus próprios diretórios e contratos. LangChain, LangGraph e integração ao SOT permanecem fora desta entrega.

Os dados de PDFs, execuções, caches e relatórios locais não são publicados automaticamente, mesmo neste repositório privado. A pasta de tradução é um workspace de etapa; não contém a governança do repositório SOT.

Para futuras publicações por Git, o coordenador pode usar `bash rag/traducao/harness/publicar.sh` com uma credencial válida e checkout sincronizado com o remoto. O conector cria commits próprios: o commit local de preparação não é o histórico remoto. O script confere projeto, branch e privacidade antes do push e não força substituição de histórico. Ele é uma operação de implantação no host, fora dos processos de tradução, e não recebe dados de PDF.
