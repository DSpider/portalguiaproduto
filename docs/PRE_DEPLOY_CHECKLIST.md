# Checklist Pre-Deploy para Staging

## Objetivo

Validar a base atual do Guia Produto Radar antes de qualquer deploy em staging.

Este checklist nao autoriza producao. A etapa atual e somente preparacao para staging.

## Status da revisao local

Data da revisao: 2026-05-16

### Testes

- [x] Suite local executada com Pytest.
- [x] Suite dentro do container da API executada com Pytest.
- [x] Testes de endpoints publicos executados.
- [x] Testes de validacao do endpoint de briefing executados.
- [x] Testes de modelos ORM e constraints executados.
- [x] Testes de scoring executados.
- [x] Testes de SEO tecnico executados.
- [x] Teste de CORS local do admin executado.

### Qualidade e imports

- [x] Compilacao basica dos arquivos Python executada.
- [x] Imports principais validados.
- [x] Sintaxe JavaScript do admin validada com `node --check`.
- [x] Compose validado com `docker compose config`.
- [x] API validada dentro do container.
- [ ] Sintaxe PHP validada com `php -l`.

Observacao: o PHP CLI nao estava disponivel no ambiente local usado nesta revisao. Antes do staging, rodar `php -l` nos arquivos do plugin em ambiente com PHP instalado.

### Docker e banco

- [x] Docker Compose sobe `api`, `worker`, `postgres` e `redis`.
- [x] API fica healthy em `http://localhost:18080/health`.
- [x] Redis fica healthy.
- [x] PostgreSQL fica healthy.
- [x] Migration Alembic aplicada no PostgreSQL local.
- [x] Revisao Alembic atual confirmada: `20260516_0001`.
- [x] Tabelas iniciais confirmadas no banco local.

### Seguranca

- [x] `.env` real esta ignorado pelo Git.
- [x] `.dockerignore` exclui `.env`, `.venv`, `.git`, caches e logs.
- [x] `.env.example` existe e contem as variaveis locais necessarias.
- [x] Varredura de padroes de tokens/chaves privadas nao encontrou segredos reais.
- [x] Valores de senha encontrados sao placeholders locais de desenvolvimento.
- [x] Endpoint `POST /api/v1/content/briefing` usa schemas Pydantic e retorna 422 para payload invalido.
- [x] Endpoint de briefing nao persiste dados nem publica conteudo.
- [x] CORS da API esta restrito ao admin local por padrao.
- [x] Plugin WordPress usa Settings API com nonce via `settings_fields`.
- [x] Plugin WordPress sanitiza URL da API e atributos de shortcode.
- [x] Plugin WordPress escapa saidas renderizadas.
- [x] Funcoes do plugin WordPress usam prefixo `gpr_`.
- [x] Plugin WordPress usa transients e fallback quando API falha.

## Comandos de validacao executados

```powershell
.\.venv\Scripts\python -m pytest
```

```powershell
docker compose config
docker compose build api
docker compose run --rm --no-deps api pytest
docker compose up -d --build
Invoke-RestMethod http://localhost:18080/health
docker compose exec -T api alembic upgrade head
docker compose exec -T api alembic current
```

## Checklist obrigatorio antes de staging

- [ ] Criar arquivo `.env` especifico da VPS de staging fora do Git.
- [ ] Trocar placeholders locais de banco por credenciais de staging.
- [ ] Definir `APP_ENV=staging`.
- [ ] Definir `ADMIN_CORS_ORIGINS` com a origem real do admin em staging.
- [ ] Subir banco PostgreSQL limpo em staging.
- [ ] Aplicar `alembic upgrade head` em staging.
- [ ] Validar `GET /health` e `GET /version` em staging.
- [ ] Validar `POST /api/v1/content/briefing` com payload mockado.
- [ ] Rodar `docker compose run --rm --no-deps api pytest` na VPS ou em ambiente equivalente.
- [ ] Rodar `php -l` nos arquivos do plugin WordPress.
- [ ] Ativar plugin em WordPress de staging, nunca em producao direta.
- [ ] Configurar URL da API de staging no plugin.
- [ ] Validar shortcodes em pagina de teste nao indexada.
- [ ] Bloquear indexacao de staging via WordPress, Nginx ou Cloudflare.
- [ ] Definir estrategia de autenticacao para admin antes de expor fora de localhost.
- [ ] Definir politica de backup do banco de staging.

## Pendencias conhecidas

- Admin interno ainda nao possui login.
- Endpoints administrativos reais ainda nao existem.
- Produtos e ranking da API ainda usam dados mockados.
- Briefings gerados pelo admin ficam em `localStorage`.
- Plugin WordPress ainda nao possui testes automatizados porque falta ambiente PHP/WordPress de teste.
- Nao ha CI configurado.
- Nao ha rate limit.
- Nao ha observabilidade estruturada.
- Nao ha deploy automatizado.

## Bloqueios para producao

- Nao publicar em producao sem staging validado.
- Nao conectar marketplaces reais sem gestao de segredos.
- Nao liberar admin sem autenticacao.
- Nao permitir publicacao automatica de conteudo gerado.
- Nao indexar paginas geradas sem revisao editorial humana.
