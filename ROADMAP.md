# Roadmap — Inteligência SOT

Versão: 1.0.0. Escopo confirmado: **tradução primeiro; elaboração efetiva do RAG
depois**. Posição atual e histórico: [CATÁLOGO.md](CATÁLOGO.md). Método:
[atomic-spec.md](atomic-spec.md). Atualizar o catálogo após entregas/impedimentos
relevantes; este roadmap define sequência, não inventa datas ou progresso.

## Etapa 1 — tradução

| Sequência | Trabalho e responsável | Entrega | Critério de avanço / situação |
|---|---|---|---|
| T0 base de governança e ambiente | Responsável pelo desenvolvimento | Política/leitura, launcher e ferramentas pinadas, Eval/Score | Infraestrutura verificada; L4 da raiz. Sem certificação linguística |
| T1 especificar agentes e skills | Autor + leitura/revisão independente | Contrato comum, três specs, skills por papel, Plan/Tasks, pesquisa | Referências resolvíveis, compatibilidade IG, testes de contexto/hash; conclusão registrada no catálogo |
| T2 fechar desenho e comparação | Coordenador/desenvolvimento | Protocolos, orçamento/repetições e configurações candidatas de agentes/skills/motores/frameworks | Definir workloads sintéticos e piloto; Python explícito, LangGraph e LangChain no benchmark; escolha ainda aberta |
| T3 preparar documento e referência | Coordenador + usuário/revisor competente | PDF/hash, idiomas, inventário revisado, glossário aprovado, amostra representativa | Entrada real e decisões necessárias registradas; não inventar aprovação/idiomas |
| T4 executar benchmark determinístico | Desenvolvimento, revisão independente | Resultados de gates, integridade, estados, retomada, isolamento, overhead e falhas | Zero bypass/efeitos não autorizados nos casos definidos; versões/dependências fixadas. Protótipos sob escopo próprio |
| T5 executar piloto probabilístico | Tradutor → auditor → coordenação | Blocos/PDF alinhados, MQM/evidências, divergências, custo/tempo e repetições | Fidelidade/estrutura verificadas; zero críticos/maiores abertos, até duas correções; revisão humana competente para regras críticas |
| T6 selecionar e congelar configuração | Coordenação + decisões do usuário quando exigidas | Relatório comparativo e configuração escolhida | Escolha por contrato/evidência, registrando trade-offs; mudança de política/runtime/exposição com autorização correspondente |
| T7 traduzir lote completo | Tradutor → auditor → host confiável | Tradução completa, PDF, alinhamento, revisões/correções | Piloto aceito, cobertura integral, hashes atuais e gates; sem autoaprovação |
| T8 entregar tradução | Coordenador/host + revisão do usuário | Bundle entregue, pendências/limites, proveniência e handoff | Estado técnico DELIVERED e revisão da tradução separados de inclusão no corpus |

T2 prepara ambas as avaliações; T4 e T5 comparam configurações antes de T6.
T3 é obrigatório para qualquer avaliação documental real. O harness atual só
executa controles/testes; motor/modelo/idiomas/PDF/piloto continuam pendentes.
Configurações inviáveis nos controles determinísticos não avançam como vencedoras
por qualidade média ou custo. Medir significado/visual de forma independente das
checagens estruturais. “Melhor” significa melhor evidência no domínio/idiomas e
orçamento acordados, sem promessa de ótimo universal.

Não instalar ou iniciar LangChain/LangGraph em jobs existentes por sua presença
na shortlist. Protótipo e eventual nova imagem serão especificados e testados;
papéis, ownership, sandbox e limites continuam vigentes.

## Etapa 2 — elaboração efetiva do RAG

**Posterior à entrega/revisão da tradução**, sem implementação nesta rodada.
Não confundir autorização de iniciar desenho RAG com aprovação de corpus.

| Sequência futura | Entrega esperada | Dependência |
|---|---|---|
| R1 especificar preparação e recuperação | Contratos por etapa, cenários e critérios de citação/conflito | Handoff da tradução e escopo próprio |
| R2 preparar unidades rastreáveis | Metadados/chunks candidatos, versões e transformações | Originais/derivados autorizados e revisão |
| R3 liberar corpus | Manifesto por documento/lote vinculado ao hash | Aprovação explícita do usuário após testes/revisão |
| R4 comparar e implementar indexação/recuperação | Benchmark de chunking/embeddings/índice/framework, implementação escolhida | Corpus aprovado, privacidade e arquitetura definidas |
| R5 avaliar e entregar RAG | Citações resolvíveis, ausência de suporte declarada, conflitos com versões/fontes | Avaliação própria e autorizações de destino/implantação |

Não escolher verdade entre fontes conflitantes por inferência. Aprovação do
corpus não permite transmissão externa. Controles e decisões RAG exigem suas
próprias evidências; tradução entregue ou Score L4 não os substituem.

## Handoff entre sessões

Sessão de projeto: entrada raiz → catálogo → roadmap → documentos da tarefa/
papel pela matriz. Registrar posição, entregas verificadas, hashes/versões,
pendências, próxima ação e permissões necessárias. Atualizar o catálogo com
fatos observados; preservar marcos e decisões anteriores. Jobs isolados usam
o snapshot/contexto transportado e não tentam montar a raiz para essa leitura.
