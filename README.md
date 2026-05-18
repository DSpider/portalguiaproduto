# Guia Produto Radar

Refatoracao total do Guia Produto para uma plataforma de inteligencia, tendencias, rankings, comparativos, SEO tecnico e afiliados para produtos de tecnologia.

O WordPress continuara sendo a vitrine publica e editorial. A inteligencia pesada ficara em servicos proprios: API, worker, banco de dados, cache e integracoes futuras.

## Estado atual

Esta e a base inicial para desenvolvimento local no Windows.

Ja existe:

- estrutura de pastas do monorepo;
- API base com routers, services, repositories, schemas e dados mockados;
- worker minimo;
- Docker Compose com API, worker, PostgreSQL e Redis;
- configuracao por variaveis de ambiente;
- base de SQLAlchemy e Alembic;
- testes Pytest dos endpoints iniciais;
- motor deterministico de Trend Score em `packages/scoring`;
- admin interno estatico em `apps/admin`;
- plugin WordPress inicial em `wordpress/plugins/guia-produto-radar`;
- documentos tecnicos iniciais em `docs/`.

Ainda nao existe:

- conectores reais de marketplaces;
- autenticacao no admin interno;
- publicacao automatica de conteudo.

## Estrutura

```text
.
|-- apps/
|   |-- api/
|   |-- worker/
|   `-- admin/
|-- packages/
|   |-- connectors/
|   |-- scoring/
|   |-- seo/
|   `-- shared/
|-- wordpress/
|   `-- plugins/
|       `-- guia-produto-radar/
|-- infra/
|   |-- nginx/
|   `-- scripts/
|-- docs/
|-- tests/
|-- docker-compose.yml
|-- .env.example
`-- AGENTS.md
```

## Portas locais

Para evitar conflitos comuns com WordPress local, o Compose usa portas altas no host:

- API: `http://localhost:18080`
- PostgreSQL: `localhost:15432`
- Redis: `localhost:16379`

Dentro da rede Docker, os servicos usam as portas padrao:

- API: `api:8000`
- PostgreSQL: `postgres:5432`
- Redis: `redis:6379`

## Como iniciar no Windows

No PowerShell, dentro de `C:\gp_projects\portalguiaproduto`:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Em outro terminal, valide a API:

```powershell
Invoke-RestMethod http://localhost:18080/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "guia-produto-radar-api",
  "environment": "local"
}
```

## Endpoints iniciais

API local:

```text
http://localhost:18080
```

Endpoints:

- `GET /health`
- `GET /version`
- `GET /api/v1/radar/summary`
- `GET /api/v1/products`
- `GET /api/v1/products/{slug}`
- `POST /api/v1/content/briefing`

Exemplos:

```powershell
Invoke-RestMethod http://localhost:18080/version
Invoke-RestMethod http://localhost:18080/api/v1/radar/summary
Invoke-RestMethod http://localhost:18080/api/v1/products
Invoke-RestMethod http://localhost:18080/api/v1/products/notebook-ultrafino-14
```

Documentacao interativa do FastAPI:

```text
http://localhost:18080/docs
```

O endpoint `POST /api/v1/content/briefing` gera rascunhos editoriais para revisao humana. Ele nao publica conteudo automaticamente e nao inventa preco, nota ou experiencia pratica.

## Admin interno

O admin inicial fica em:

```text
apps/admin
```

Para rodar localmente:

```powershell
cd C:\gp_projects\portalguiaproduto
docker compose up --build
```

Em outro terminal:

```powershell
cd C:\gp_projects\portalguiaproduto
python -m http.server 18090
```

Acesse:

```text
http://localhost:18090/apps/admin/
```

Telas disponiveis:

- Dashboard;
- Produtos;
- Produto detalhe;
- Briefings;
- Configuracoes.

O admin consome a API em `http://localhost:18080` por padrao. A URL pode ser alterada na tela `Configuracoes`.

## Identidade visual

Os ativos oficiais do Guia Produto ficam em:

```text
img/
```

Arquivos principais:

- `guia-produto-logo-color.png`
- `guia-produto-logo-white.png`
- `guia-produto-favicon-150x150.png`
- `guia-produto-logo-centered.png`

A paleta inicial do portal usa azul, roxo e branco, com suporte previsto a modo escuro.

## Testes

Os testes ficam em `apps/api/tests` e `tests`.

Para rodar fora do Docker, crie um ambiente Python local:

```powershell
cd C:\gp_projects\portalguiaproduto
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r apps\api\requirements.txt
pytest
```

Para rodar dentro do container da API:

```powershell
docker compose run --rm --no-deps api pytest
```

## CI no GitHub Actions

O workflow fica em:

```text
.github/workflows/ci.yml
```

Ele roda automaticamente em:

- `pull_request` para `main`;
- `push` na `main`.

Validacoes executadas:

- instalacao das dependencias Python com cache de pip;
- lint basico por compilacao Python;
- testes Pytest da API e pacotes;
- migrations Alembic contra PostgreSQL de CI;
- sintaxe PHP do plugin WordPress;
- estrutura obrigatoria do plugin;
- ausencia de `.env` real versionado;
- varredura de padroes comuns de segredos;
- presenca de `AGENTS.md`, `README.md`, `.env.example` e `docker-compose.yml`.

Falhas comuns:

- erro em `Run tests`: algum teste Pytest falhou;
- erro em `Validate Alembic migrations`: migration quebrada ou banco inacessivel;
- erro em `Validate no real env files or hardcoded secrets`: arquivo sensivel ou token foi versionado;
- erro em `PHP syntax lint`: plugin WordPress com erro de sintaxe;
- erro em `Validate required files`: arquivo base obrigatorio ausente.

## Fluxo Git

O fluxo oficial de trabalho esta documentado em:

```text
docs/GIT_WORKFLOW.md
```

Resumo operacional:

- desenvolver no Windows/local;
- criar branch por tarefa;
- abrir pull request para `main`;
- aguardar o CI passar;
- fazer merge;
- atualizar a VPS com `git pull --ff-only origin main`;
- rodar `bash infra/scripts/deploy_staging.sh`.

Nao desenvolva diretamente na VPS. Ela deve apenas receber codigo aprovado pelo GitHub.

## Plugin WordPress

O plugin inicial fica em:

```text
wordpress/plugins/guia-produto-radar
```

Shortcodes disponiveis:

```text
[guia_produto_radar]
[guia_produto_ranking categoria="tecnologia" limite="10"]
[guia_produto_tendencias limite="10"]
```

Para instalar localmente, copie ou monte a pasta `wordpress/plugins/guia-produto-radar` em:

```text
wp-content/plugins/guia-produto-radar
```

Depois ative o plugin no painel do WordPress e configure a API em:

```text
Configuracoes > Guia Produto Radar
```

URL local da API:

```text
http://localhost:18080
```

Se o WordPress estiver rodando dentro de outro container Docker, talvez seja necessario usar:

```text
http://host.docker.internal:18080
```

## Banco e migrations

A base de conexao com PostgreSQL esta preparada em `apps/api/app/db`.

O Alembic esta configurado em:

- `apps/api/alembic.ini`
- `apps/api/alembic/`

A migration inicial cria as tabelas principais do Radar:

- `products`
- `keywords`
- `product_sources`
- `trend_snapshots`
- `marketplace_offers`
- `scoring_runs`
- `seo_pages`
- `ai_content_drafts`

Com o Docker Compose rodando, aplique a migration:

```powershell
docker compose exec api alembic upgrade head
```

Para inserir dados mockados de exemplo:

```powershell
docker compose exec api python -m app.db.seed
```

Para consultar o status do Alembic:

```powershell
docker compose exec api alembic current
```

Se preferir rodar Alembic pelo Python local, use uma URL de banco acessivel pelo host:

```powershell
cd C:\gp_projects\portalguiaproduto\apps\api
$env:DATABASE_URL="postgresql+psycopg://gp_local_user:gp_local_password_change_me@localhost:15432/guia_produto_radar"
..\..\.venv\Scripts\python -m alembic upgrade head
..\..\.venv\Scripts\python -m app.db.seed
```

## Comandos uteis

Ver containers:

```powershell
docker compose ps
```

Ver logs da API:

```powershell
docker compose logs -f api
```

Ver logs do worker:

```powershell
docker compose logs -f worker
```

Parar o ambiente:

```powershell
docker compose down
```

Parar e apagar volumes locais de banco/cache:

```powershell
docker compose down -v
```

Use `docker compose down -v` apenas quando quiser perder os dados locais de PostgreSQL e Redis.

## Seguranca

Nao versionar `.env` real, tokens, senhas, cookies, chaves de API, credenciais de banco, credenciais WordPress ou credenciais de marketplaces.

O arquivo `.env.example` contem apenas valores locais de desenvolvimento e placeholders.

## Proximo passo recomendado

Antes de staging, concluir o checklist em `docs/PRE_DEPLOY_CHECKLIST.md`, definir configuracoes da VPS, aplicar migrations em um banco limpo e decidir o primeiro nivel de autenticacao para o admin interno e futuros endpoints administrativos.
