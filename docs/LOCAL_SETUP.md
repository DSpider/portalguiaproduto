# Setup Local

## Estado atual

O repositorio ainda nao possui aplicacao executavel.

Atualmente existem apenas:

- `README.md`;
- `AGENTS.md`;
- documentos em `docs/`.

Nao ha, nesta fase:

- dependencias instalaveis;
- `docker-compose.yml`;
- API;
- worker;
- plugin WordPress;
- testes automatizados;
- `.env.example`.

Este documento define o setup esperado para as proximas fases.

## Requisitos locais planejados

Para desenvolvimento futuro no Windows:

- Git;
- Python 3.11 ou superior;
- Docker Desktop;
- PostgreSQL via Docker;
- Redis via Docker;
- editor de codigo;
- WordPress local somente na fase do plugin.

Nao instalar dependencias agora sem uma fase especifica para bootstrap.

## Clonagem

```powershell
git clone https://github.com/DSpider/portalguiaproduto.git
cd portalguiaproduto
```

## Conferencia inicial

```powershell
git status --short --branch
Get-ChildItem -Force
```

## Variaveis de ambiente

Na fase de bootstrap tecnico, criar um arquivo `.env.example` com nomes de variaveis, sem valores reais.

Exemplo planejado:

```env
APP_ENV=local
API_HOST=127.0.0.1
API_PORT=8000
DATABASE_URL=postgresql+psycopg://gp_user:gp_password@localhost:5432/guia_produto
REDIS_URL=redis://localhost:6379/0
WORDPRESS_API_TOKEN=
AMAZON_ACCESS_KEY=
MERCADO_LIVRE_CLIENT_ID=
SHOPEE_PARTNER_ID=
```

O arquivo `.env` real deve ficar fora do versionamento.

## Docker local planejado

Na fase de bootstrap, o `docker-compose.yml` deve conter inicialmente:

- PostgreSQL;
- Redis.

Servicos de API e worker podem entrar depois que o esqueleto da aplicacao existir.

Comando planejado:

```powershell
docker compose up -d
```

## API planejada

Depois da criacao da API:

```powershell
cd api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
uvicorn app.main:app --reload
```

Endpoint minimo esperado:

```text
GET /health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

## Worker planejado

Depois da criacao do worker, o comando dependera da biblioteca escolhida.

Opcoes aceitas:

- Celery;
- RQ;
- APScheduler.

O worker deve ser introduzido somente apos a API e o banco terem base minima.

## WordPress local planejado

O plugin deve ser criado em fase propria.

Fluxo planejado:

1. subir WordPress local ou usar uma instalacao local existente;
2. copiar ou montar `wordpress-plugin/` em `wp-content/plugins/`;
3. ativar o plugin;
4. configurar URL da API local;
5. testar shortcodes em uma pagina de teste.

Shortcodes iniciais:

- `[guia_produto]`;
- `[guia_produto_ranking categoria="tecnologia"]`;
- `[guia_produto_tendencias limite="10"]`.

## Testes planejados

Testes minimos esperados nas proximas fases:

- healthcheck da API;
- modelos principais;
- geracao de slug;
- calculo de score;
- geracao de schema;
- validacao de conteudo;
- sanitizacao e escape do plugin WordPress quando possivel.

Comando planejado para API:

```powershell
pytest
```

## Troubleshooting inicial

### Porta em uso

Verificar processos usando portas planejadas:

```powershell
netstat -ano | Select-String ":8000"
netstat -ano | Select-String ":5432"
netstat -ano | Select-String ":6379"
```

### Docker indisponivel

Verificar se o Docker Desktop esta aberto:

```powershell
docker version
docker compose version
```

### Ambiente Python incorreto

Verificar versao:

```powershell
python --version
```

## O que nao fazer no setup local agora

- instalar dependencias sem necessidade;
- criar credenciais reais;
- conectar marketplaces reais;
- conectar WordPress de producao;
- rodar scraping pesado;
- publicar conteudo automaticamente.
