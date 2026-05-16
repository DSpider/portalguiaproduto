# Plano Tecnico do Projeto

## Diagnostico do repositorio atual

O repositorio esta em fase inicial de bootstrap.

Arquivos versionados identificados:

- `README.md`: descricao curta da refatoracao total do Guia Produto.
- `AGENTS.md`: diretrizes de negocio, arquitetura, seguranca, SEO, WordPress, banco de dados, testes e deploy.

Nao foram encontrados, nesta fase:

- codigo de API;
- codigo de worker;
- plugin WordPress;
- configuracao Docker;
- migrations;
- testes;
- dependencias;
- arquivos em `docs/` antes desta tarefa.

Conclusao: o projeto esta vazio ou quase vazio, com apenas documentos iniciais de orientacao.

## Objetivo do Guia Produto Radar

O Guia Produto Radar sera uma plataforma de inteligencia para produtos de tecnologia, orientada a:

- identificacao de produtos em tendencia;
- analise de oportunidade SEO e comercial;
- organizacao de rankings e comparativos;
- suporte a afiliados;
- geracao de rascunhos editoriais com revisao humana;
- integracao futura com Amazon, Mercado Livre e Shopee;
- exposicao publica via WordPress sem sobrecarregar o WordPress.

## Principios tecnicos

- Manter o WordPress como camada publica, editorial e de exibicao.
- Concentrar regras de negocio, scoring, integracoes e processamento em servicos proprios.
- Implementar em fases pequenas e verificaveis.
- Priorizar testes basicos desde a primeira fase funcional.
- Nao publicar conteudo gerado por IA sem revisao humana.
- Nao criar schema, preco, avaliacao ou disponibilidade sem dado confiavel.
- Nao versionar segredos.

## Estrutura ideal de pastas

Estrutura proposta para evolucao do repositorio:

```text
.
|-- api/
|   |-- app/
|   |   |-- core/
|   |   |-- db/
|   |   |-- models/
|   |   |-- schemas/
|   |   |-- services/
|   |   |-- routers/
|   |   `-- tests/
|   |-- alembic/
|   |-- pyproject.toml
|   `-- README.md
|-- worker/
|   |-- app/
|   |   |-- jobs/
|   |   |-- services/
|   |   `-- tests/
|   `-- README.md
|-- wordpress-plugin/
|   |-- guia-produto-radar.php
|   |-- includes/
|   |-- assets/
|   |-- templates/
|   `-- README.md
|-- admin/
|   `-- README.md
|-- docs/
|   |-- PROJECT_PLAN.md
|   |-- ARCHITECTURE.md
|   |-- LOCAL_SETUP.md
|   |-- SECURITY.md
|   `-- SEO_GUIDELINES.md
|-- infra/
|   |-- docker/
|   |-- nginx/
|   `-- README.md
|-- scripts/
|-- tests/
|-- .env.example
|-- .gitignore
|-- docker-compose.yml
|-- README.md
`-- AGENTS.md
```

Observacao: esta estrutura e uma proposta. As pastas devem ser criadas gradualmente, conforme cada fase for implementada.

## Fases sugeridas

### Fase 0: Planejamento e documentacao

Objetivo: documentar o desenho inicial antes de implementar.

Entregas:

- plano tecnico;
- arquitetura;
- setup local;
- seguranca;
- diretrizes de SEO.

Status atual: em andamento nesta tarefa.

### Fase 1: Bootstrap tecnico local

Objetivo: criar base minima executavel sem funcionalidades de negocio complexas.

Entregas:

- `.env.example`;
- `.gitignore`;
- `docker-compose.yml` com PostgreSQL e Redis;
- esqueleto da API;
- healthcheck;
- teste de healthcheck.

Branch sugerida: `chore/bootstrap-guia-produto`.

### Fase 2: API base

Objetivo: criar fundacao de dominio e persistencia.

Entregas:

- FastAPI;
- configuracao por ambiente;
- SQLAlchemy ou SQLModel;
- Alembic;
- modelos iniciais;
- testes basicos de modelos e validacoes.

Branch sugerida: `feat/api-base`.

### Fase 3: Motor de scoring

Objetivo: calcular oportunidade de produto com dados controlados.

Entregas:

- servico de scoring;
- pesos configuraveis;
- registro de execucoes em `scoring_runs`;
- testes de calculo;
- sem scraping pesado.

Branch sugerida: `feat/scoring-engine`.

### Fase 4: Worker

Objetivo: executar tarefas agendadas e processamento em background.

Entregas:

- fila com Redis;
- jobs de atualizacao;
- logs;
- retentativas;
- testes de jobs criticos.

### Fase 5: Plugin WordPress

Objetivo: conectar o WordPress a API de forma segura e cacheada.

Entregas:

- plugin com prefixo `gp_`;
- shortcodes iniciais;
- transients;
- fallback quando a API estiver indisponivel;
- sanitizacao e escape de saida.

Branch sugerida: `feat/wordpress-plugin`.

### Fase 6: Paginas SEO e rascunhos editoriais

Objetivo: preparar paginas e rascunhos para revisao humana.

Entregas:

- entidades de paginas SEO;
- slugs limpos;
- metadados;
- schema JSON-LD apenas com dados reais;
- rascunhos com fontes, confianca, limitacoes e pendencias.

Branch sugerida: `feat/seo-pages`.

### Fase 7: Staging

Objetivo: validar o ambiente fora do localhost.

Entregas:

- Docker Compose na VPS;
- Nginx ou Cloudflare Tunnel;
- testes de seguranca;
- testes de performance;
- integracao com WordPress de staging.

Branch sugerida: `feat/deploy-staging`.

### Fase 8: Integracoes reais e producao

Objetivo: ativar integracoes com marketplaces e WordPress real com seguranca.

Entregas:

- credenciais via variaveis de ambiente;
- integracoes oficiais quando disponiveis;
- monitoramento;
- rollout controlado;
- revisao manual de conteudo.

Branch sugerida: `feat/production-integration`.

## Entidades iniciais propostas

- `products`;
- `product_sources`;
- `keywords`;
- `trend_snapshots`;
- `marketplace_offers`;
- `scoring_runs`;
- `seo_pages`;
- `ai_content_drafts`;
- `api_logs`.

Cada entidade deve incluir, quando aplicavel:

- `id`;
- `created_at`;
- `updated_at`;
- origem do dado;
- nivel de confianca;
- indices para consultas frequentes.

## Criterios de pronto por fase

Uma fase so deve ser considerada concluida quando tiver:

- escopo pequeno e claro;
- documentacao atualizada;
- testes basicos executados;
- ausencia de segredos versionados;
- riscos conhecidos registrados;
- nenhum deploy direto em producao.

## Fora de escopo neste momento

- scraping pesado;
- integracoes reais com credenciais;
- publicacao automatica de conteudo;
- geracao massiva de paginas indexaveis;
- deploy automatico;
- alteracao do WordPress real em producao;
- compra de trafego.
