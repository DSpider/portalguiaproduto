# Setup Local

## Estado atual

O repositorio agora possui uma base minima executavel localmente com Docker Compose.

Servicos disponiveis:

- `api`: FastAPI minima com healthcheck;
- `worker`: processo Python minimo para tarefas futuras;
- `postgres`: PostgreSQL local;
- `redis`: Redis local.

Ainda nao existem:

- modelos de banco;
- migrations;
- conectores reais de marketplaces;
- plugin WordPress funcional;
- painel administrativo;
- testes automatizados.

## Requisitos no Windows

- Git;
- Docker Desktop;
- PowerShell;
- acesso ao repositorio em `C:\gp_projects\portalguiaproduto`.

Python local nao e obrigatorio para subir o ambiente via Docker Compose nesta fase.

## Portas locais

As portas do host foram escolhidas para reduzir conflito com WordPress local:

- API: `18080`;
- PostgreSQL: `15432`;
- Redis: `16379`.

Dentro da rede Docker:

- API: `api:8000`;
- PostgreSQL: `postgres:5432`;
- Redis: `redis:6379`.

## Primeiro uso

No PowerShell:

```powershell
cd C:\gp_projects\portalguiaproduto
Copy-Item .env.example .env
docker compose up --build
```

O arquivo `.env` e local e nao deve ser versionado.

## Validar a API

Em outro terminal:

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

Tambem e possivel abrir no navegador:

```text
http://localhost:18080/health
```

## Validar os containers

```powershell
docker compose ps
```

Os servicos esperados sao:

- `gp_radar_api`;
- `gp_radar_worker`;
- `gp_radar_postgres`;
- `gp_radar_redis`.

## Logs

API:

```powershell
docker compose logs -f api
```

Worker:

```powershell
docker compose logs -f worker
```

PostgreSQL:

```powershell
docker compose logs -f postgres
```

Redis:

```powershell
docker compose logs -f redis
```

## Parar o ambiente

```powershell
docker compose down
```

Para parar e apagar dados locais de PostgreSQL e Redis:

```powershell
docker compose down -v
```

Use `docker compose down -v` somente quando quiser limpar os volumes locais.

## Variaveis de ambiente

O arquivo `.env.example` contem valores locais e placeholders.

Principais variaveis:

```env
APP_ENV=local
API_PORT=18080
POSTGRES_PORT=15432
REDIS_PORT=16379
POSTGRES_DB=guia_produto_radar
POSTGRES_USER=gp_local_user
POSTGRES_PASSWORD=gp_local_password_change_me
DATABASE_URL=postgresql+psycopg://gp_local_user:gp_local_password_change_me@postgres:5432/guia_produto_radar
REDIS_URL=redis://redis:6379/0
WORKER_HEARTBEAT_SECONDS=30
```

Nao inserir credenciais reais em `.env.example`.

## Estrutura local criada

```text
apps/
|-- api/
|-- worker/
`-- admin/
packages/
|-- connectors/
|-- scoring/
|-- seo/
`-- shared/
wordpress/
`-- plugins/
    `-- guia-produto-radar/
infra/
|-- nginx/
`-- scripts/
tests/
```

## Troubleshooting

### Docker Desktop fechado

```powershell
docker version
docker compose version
```

Se o comando falhar, abra o Docker Desktop e tente novamente.

### Erro 500 no Docker Desktop Linux Engine

Se `docker compose up --build` retornar erro 500 ao consultar uma imagem local, valide se o engine Linux do Docker Desktop esta saudavel:

```powershell
docker version
docker context ls
docker context use desktop-linux
docker info
docker run --rm hello-world
```

Se os comandos falharem com erro parecido, reinicie o engine:

```powershell
wsl --shutdown
```

Depois feche e abra novamente o Docker Desktop, aguarde o status ficar ativo e rode:

```powershell
docker compose build --no-cache api worker
docker compose up
```

### Porta em uso

```powershell
netstat -ano | Select-String ":18080"
netstat -ano | Select-String ":15432"
netstat -ano | Select-String ":16379"
```

Se houver conflito, altere `API_PORT`, `POSTGRES_PORT` ou `REDIS_PORT` no `.env`.

### Rebuild limpo

```powershell
docker compose build --no-cache
docker compose up
```

### Reset de dados locais

```powershell
docker compose down -v
docker compose up --build
```

## O que nao fazer nesta fase

- usar credenciais reais;
- conectar marketplaces reais;
- conectar WordPress de producao;
- criar scraping pesado;
- publicar conteudo automaticamente;
- criar paginas SEO em massa.

## Admin interno local

Com a API em execucao, rode o admin estatico a partir da raiz do repositorio para servir tambem os ativos em `img/`:

```powershell
cd C:\gp_projects\portalguiaproduto
python -m http.server 18090
```

Acesse:

```text
http://localhost:18090/apps/admin/
```

O painel usa a URL `http://localhost:18080` por padrao e salva alteracoes de configuracao no `localStorage`.
