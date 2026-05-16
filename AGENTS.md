# AGENTS.md — Guia Produto

## Visão geral do projeto

Este repositório contém a refatoração completa do portal Guia Produto.

O Guia Produto era originalmente um blog WordPress. O novo objetivo é transformar o site em uma plataforma de inteligência, tendência e recomendação de produtos de tecnologia, com foco em SEO, performance, dados estruturados e integração futura com marketplaces.

O projeto deve preservar o WordPress como vitrine pública e motor editorial, mas mover a inteligência pesada para serviços próprios.

## Objetivo de negócio

Criar uma ferramenta chamada Guia Produto capaz de:

1. Identificar produtos de tecnologia em tendência.
2. Cruzar sinais de busca, tendência, disponibilidade, preço e oportunidade comercial.
3. Gerar rankings, briefings e páginas SEO.
4. Criar rascunhos de conteúdo para revisão humana.
5. Apoiar a operação para ter links de vendas como afiliado (esta será a principal fonte de receita).
6. Integrar com Amazon, Mercado Livre e Shopee.
7. Melhorar tráfego orgânico, CTR, conversão e monetização como afiliado.

## Decisão arquitetural principal

Não transformar o WordPress em um sistema pesado.

Use esta separação:

- WordPress: conteúdo público, SEO, páginas, posts, shortcodes e interface com usuário.
- API: regras de negócio, produtos, tendências, scores e integrações.
- Worker: tarefas agendadas, coleta de dados, atualização de tendências e processamento em background.
- PostgreSQL: banco principal.
- Redis: cache, filas e controle de jobs.
- Plugin WordPress: ponte entre o WordPress e a API.

## Stack recomendada

Backend:
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ou SQLModel
- Alembic para migrations
- Pydantic para validação
- Pytest para testes

Worker:
- Python
- Celery, RQ ou APScheduler
- Redis

WordPress:
- Plugin próprio em PHP
- Shortcodes
- REST API
- Cache com transients
- Saídas sanitizadas e escapadas

Frontend administrativo:
- Começar simples.
- Pode ser HTML/CSS/JS leve ou Next.js em fase posterior.
- Não criar complexidade antes do backend estar validado.

Infra:
- Docker Compose local
- Docker Compose na VPS
- Nginx ou Cloudflare Tunnel quando necessário
- GitHub Actions somente depois da base estar estável

## Regras de desenvolvimento

Antes de alterar qualquer coisa:

1. Inspecione a estrutura atual do repositório.
2. Leia README.md, AGENTS.md e arquivos em docs/.
3. Não assuma que arquivos existem.
4. Não sobrescreva código sem explicar.
5. Prefira pequenas alterações por fase.
6. Não implemente tudo de uma vez.
7. Ao final de cada tarefa, liste:
   - arquivos criados
   - arquivos alterados
   - comandos executados
   - testes executados
   - riscos ou pendências

## Segurança

Nunca versionar:

- senhas
- tokens
- chaves de API
- cookies
- credenciais WordPress
- credenciais de banco
- credenciais de marketplaces
- arquivos .env reais

Sempre criar e manter `.env.example`.

Validar entradas na API.

Sanitizar e escapar saídas no WordPress.

Não criar endpoints públicos sem autenticação quando eles alterarem dados.

Não expor logs sensíveis.

Não permitir publicação automática de conteúdo gerado por IA sem etapa de revisão.

## SEO

O projeto deve priorizar SEO técnico desde o começo.

Regras:

1. Cada página pública deve ter H1 único.
2. Usar H2 e H3 com hierarquia clara.
3. Gerar title e meta description.
4. Criar URLs limpas e slugs legíveis.
5. Gerar schema JSON-LD apenas quando os dados forem reais.
6. Não inventar avaliações.
7. Não inventar preço.
8. Exibir data da última atualização.
9. Exibir fonte ou origem dos dados quando aplicável.
10. Evitar conteúdo fino, repetitivo ou gerado em massa sem critério.
11. Priorizar páginas long tail e comparativos úteis.

## Dados estruturados

Quando aplicável, preparar suporte para:

- Product
- Review
- Offer
- FAQPage
- BreadcrumbList
- ItemList
- Organization
- WebSite

Mas não gerar schema falso.

Se não houver preço confiável, não preencher preço.

Se não houver avaliação confiável, não preencher aggregateRating.

## Conteúdo com IA

A IA deve criar rascunhos, não publicações finais.

Todo conteúdo gerado deve conter:

- nível de confiança
- fontes usadas
- limitações
- campos pendentes de revisão
- alerta quando houver dados insuficientes

## Performance

O site público deve ser leve.

Evitar:

- JavaScript desnecessário
- CSS global pesado
- sliders
- pop-ups invasivos
- imagens sem compressão
- chamadas externas em excesso

Priorizar:

- cache
- imagens WebP/AVIF
- lazy loading
- HTML semântico
- carregamento condicional de assets
- páginas rápidas em mobile

## WordPress

O plugin deve:

1. Usar prefixo `gp_` nas funções.
2. Usar shortcodes claros.
3. Carregar assets apenas quando necessário.
4. Usar transients para cache.
5. Escapar HTML com funções WordPress adequadas.
6. Sanitizar dados recebidos.
7. Evitar conflito com plugins existentes.
8. Não depender do Elementor.
9. Não quebrar o tema atual.
10. Permitir fallback se a API estiver fora.

Shortcodes iniciais desejados:

- `[guia_produto]`
- `[guia_produto_ranking categoria="tecnologia"]`
- `[guia_produto_tendencias limite="10"]`

## Banco de dados

Criar modelos pensando em evolução.

Entidades iniciais:

- products
- product_sources
- keywords
- trend_snapshots
- marketplace_offers
- scoring_runs
- seo_pages
- ai_content_drafts
- api_logs

Cada tabela deve ter:

- id
- created_at
- updated_at
- campos de origem quando aplicável
- índices para consultas frequentes

## Testes

Criar testes para:

- healthcheck da API
- modelos principais
- cálculo de score
- geração de slug
- geração de schema
- validação de conteúdo
- plugin WordPress quando possível
- pen test (teste de penetração)
- validações de segurança (quando aplicável)

Não considerar uma fase concluída sem pelo menos testes básicos.

## Deploy

O deploy deve seguir fases:

1. Localhost no Windows.
2. Staging na VPS.
3. Testes de segurança.
4. Testes de performance.
5. Integração com WordPress real.
6. Produção.

Não fazer deploy direto para produção.

## Branches

Use branches por fase:

- chore/bootstrap-guia-produto
- feat/api-base
- feat/wordpress-plugin
- feat/scoring-engine
- feat/seo-pages
- feat/deploy-staging
- feat/production-integration

## Estilo de resposta esperado

Ao concluir uma tarefa, responda de forma objetiva:

1. O que foi feito.
2. Arquivos criados.
3. Arquivos alterados.
4. Como testar.
5. Próximo passo recomendado.
6. Riscos ou pontos de atenção.

## Não fazer agora

Não implementar:

- scraping pesado
- publicação automática em produção
- integração real com credenciais
- deploy automático sem staging
- geração massiva de páginas indexáveis
- compra de tráfego
- alteração do WordPress real em produção

Primeiro criar uma base sólida, testável e versionada.