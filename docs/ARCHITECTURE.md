# Arquitetura

## Visao geral

O Guia Produto Radar deve separar exibicao publica, regras de negocio e processamento pesado.

A decisao principal e manter o WordPress leve, usando-o como vitrine publica e motor editorial, enquanto a inteligencia de produtos, tendencias, scoring, integracoes e dados estruturados fica em servicos proprios.

## Componentes

### WordPress

Responsabilidades:

- hospedar paginas publicas;
- manter posts e conteudo editorial;
- renderizar shortcodes do Guia Produto Radar;
- expor a experiencia publica ao usuario;
- manter SEO tecnico da camada publica.

Nao deve:

- executar coleta pesada de dados;
- calcular scores complexos;
- armazenar segredos de marketplaces sem necessidade;
- depender de JavaScript pesado;
- publicar conteudo gerado por IA sem revisao.

### Plugin WordPress

Responsabilidades:

- conectar o WordPress a API;
- criar shortcodes publicos;
- usar cache com transients;
- sanitizar entradas;
- escapar saidas;
- oferecer fallback quando a API estiver indisponivel.

Shortcodes planejados:

- `[guia_produto]`;
- `[guia_produto_ranking categoria="tecnologia"]`;
- `[guia_produto_tendencias limite="10"]`.

### API

Responsabilidades:

- concentrar regras de negocio;
- gerenciar produtos, fontes, palavras-chave, tendencias, ofertas, scores e paginas SEO;
- validar entradas;
- expor endpoints para o plugin WordPress e para interfaces administrativas;
- gerar dados estruturados somente com dados confiaveis;
- registrar logs tecnicos sem expor dados sensiveis.

Stack recomendada:

- Python;
- FastAPI;
- Pydantic;
- SQLAlchemy ou SQLModel;
- Alembic;
- Pytest.

### Worker

Responsabilidades:

- executar tarefas agendadas;
- atualizar tendencias;
- processar filas;
- recalcular scores;
- preparar rascunhos;
- integrar com marketplaces em fases futuras.

Stack recomendada:

- Python;
- Redis;
- Celery, RQ ou APScheduler.

### PostgreSQL

Responsabilidades:

- banco principal do dominio;
- historico de tendencias;
- produtos;
- ofertas;
- execucoes de scoring;
- paginas SEO;
- rascunhos de IA;
- logs de API.

### Redis

Responsabilidades:

- cache;
- filas;
- controle de jobs;
- reducao de chamadas repetidas a API.

### Admin

Responsabilidades futuras:

- revisar tendencias;
- revisar scores;
- aprovar rascunhos;
- acompanhar integracoes;
- gerenciar paginas SEO.

Deve comecar simples. Um painel administrativo completo so deve ser criado depois da API estar validada.

## Fluxo de dados planejado

```text
Fontes externas
  -> Worker
  -> PostgreSQL
  -> API
  -> Plugin WordPress
  -> Paginas publicas no WordPress
```

Fluxo editorial com IA:

```text
Dados confiaveis
  -> API
  -> Rascunho com fontes, confianca e limitacoes
  -> Revisao humana
  -> WordPress
```

## Limites entre sistemas

### WordPress pode

- renderizar conteudo;
- chamar endpoints de leitura da API;
- cachear respostas;
- exibir rankings, tendencias e blocos editoriais;
- manter posts e paginas.

### WordPress nao deve

- executar scoring;
- coletar dados externos pesados;
- fazer jobs longos;
- publicar automaticamente conteudo de IA;
- armazenar segredos desnecessarios.

### API pode

- validar dados;
- calcular scores;
- preparar schema;
- servir dados para WordPress;
- criar rascunhos;
- registrar auditoria.

### Worker pode

- executar tarefas demoradas;
- recalcular rankings;
- consultar integracoes externas;
- atualizar snapshots.

## Modelo de dominio inicial

### `products`

Representa produtos monitorados.

Campos esperados:

- nome;
- slug;
- categoria;
- marca;
- status;
- datas de criacao e atualizacao.

### `product_sources`

Registra origens de dados associadas a produtos.

Campos esperados:

- produto;
- tipo de fonte;
- URL ou identificador externo;
- confianca;
- ultima verificacao.

### `keywords`

Representa termos de busca e oportunidades SEO.

Campos esperados:

- termo;
- slug;
- categoria;
- intencao de busca;
- dificuldade estimada;
- volume estimado quando disponivel.

### `trend_snapshots`

Registra historico de sinais de tendencia.

Campos esperados:

- produto ou palavra-chave;
- fonte;
- valor observado;
- data de coleta;
- metadados da origem.

### `marketplace_offers`

Registra ofertas vindas de marketplaces.

Campos esperados:

- produto;
- marketplace;
- preco quando confiavel;
- disponibilidade;
- URL de afiliado quando aplicavel;
- data da verificacao.

### `scoring_runs`

Registra execucoes do motor de scoring.

Campos esperados:

- produto;
- versao do algoritmo;
- score final;
- componentes do score;
- data da execucao.

### `seo_pages`

Representa paginas SEO planejadas ou publicadas.

Campos esperados:

- titulo;
- slug;
- tipo;
- status;
- palavra-chave principal;
- meta description;
- ultima atualizacao.

### `ai_content_drafts`

Registra rascunhos gerados por IA para revisao humana.

Campos esperados:

- pagina SEO;
- conteudo;
- nivel de confianca;
- fontes usadas;
- limitacoes;
- pendencias de revisao;
- status editorial.

### `api_logs`

Registra eventos tecnicos da API.

Campos esperados:

- timestamp;
- rota;
- status;
- tempo de resposta;
- origem da chamada;
- erro sanitizado quando aplicavel.

## Autenticacao e autorizacao

Endpoints de leitura publica podem existir somente quando forem seguros e cacheaveis.

Endpoints que alteram dados devem exigir autenticacao.

Integracoes administrativas devem usar credenciais de ambiente e controles de permissao.

## Cache

Camadas planejadas:

- Redis para cache interno da API e filas;
- transients no WordPress para respostas do plugin;
- cache HTTP quando aplicavel;
- cache de pagina no WordPress ou CDN.

## Observabilidade

O projeto deve registrar:

- erros da API;
- falhas de worker;
- latencia de endpoints;
- execucoes de scoring;
- falhas de integracao;
- indisponibilidade de fontes externas.

Logs nao devem conter segredos, tokens, cookies ou dados sensiveis.

## Ambientes

Ambientes planejados:

- local no Windows;
- staging na VPS;
- producao.

Deploy direto para producao nao deve ser feito.
