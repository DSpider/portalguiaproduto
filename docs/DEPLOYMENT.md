# Deploy Manual em Staging

## Objetivo

Preparar o Guia Produto Radar para rodar em uma VPS Linux como ambiente de staging, sem alterar o WordPress de producao e sem apontar o dominio principal.

Subdominio sugerido:

```text
radar-staging.guiaproduto.com.br
```

Este fluxo e manual e controlado. Ele serve para validar API, admin interno e plugin WordPress antes de qualquer decisao de producao.

## Arquivos de staging

- `docker-compose.staging.yml`: Compose isolado para staging.
- `.env.staging.example`: modelo de variaveis sem credenciais reais.
- `infra/scripts/backup_before_deploy.sh`: backup antes de alteracoes.
- `infra/scripts/deploy_staging.sh`: deploy manual com build, migration, restart e healthcheck.
- `infra/nginx/gpr-staging.conf.example`: exemplo de proxy Nginx para o subdominio.

## Servicos e portas

No Compose de staging:

| Servico | Container | Porta interna | Porta no host | Exposicao |
| --- | --- | ---: | ---: | --- |
| API | `gpr_staging_api` | `8000` | `127.0.0.1:28080` | somente local na VPS |
| Admin | `gpr_staging_admin` | `80` | `127.0.0.1:28090` | somente local na VPS |
| PostgreSQL | `gpr_staging_postgres` | `5432` | nao publicada | rede Docker |
| Redis | `gpr_staging_redis` | `6379` | nao publicada | rede Docker |
| Worker | `gpr_staging_worker` | n/a | n/a | rede Docker |

O Nginx da VPS deve ser o unico ponto publico do staging.

## Pre-requisitos na VPS

Instalar:

- Git;
- Docker Engine;
- Docker Compose plugin;
- Nginx;
- `curl`;
- acesso SSH com usuario autorizado para Docker;
- certificado TLS para `radar-staging.guiaproduto.com.br`.

Validar:

```bash
git --version
docker --version
docker compose version
nginx -v
curl --version
```

## Primeira instalacao

Na VPS, escolha um diretorio fora do WordPress principal:

```bash
sudo mkdir -p /opt/guia-produto-radar
sudo chown "$USER:$USER" /opt/guia-produto-radar
git clone https://github.com/DSpider/portalguiaproduto.git /opt/guia-produto-radar
cd /opt/guia-produto-radar
```

Criar o arquivo de ambiente real de staging:

```bash
cp .env.staging.example .env.staging
nano .env.staging
chmod 600 .env.staging
```

Obrigatorio trocar:

- `POSTGRES_PASSWORD`;
- a senha embutida em `DATABASE_URL`;
- `ADMIN_CORS_ORIGINS`, se o dominio final for diferente;
- `GPR_BRANCH`, se staging usar uma branch diferente de `main`.

Se a senha tiver caracteres reservados em URL, encode a senha em `DATABASE_URL`.

Nao commitar `.env.staging`.

Permitir execucao dos scripts:

```bash
chmod +x infra/scripts/backup_before_deploy.sh
chmod +x infra/scripts/deploy_staging.sh
```

## Deploy manual

Execute:

```bash
cd /opt/guia-produto-radar
./infra/scripts/deploy_staging.sh
```

O script executa:

1. valida working tree limpo;
2. backup pre-deploy;
3. `git fetch`;
4. `git checkout` da branch configurada;
5. `git pull --ff-only`;
6. validacao do Compose;
7. build dos containers;
8. subida de PostgreSQL e Redis;
9. `alembic upgrade head`;
10. restart controlado dos servicos;
11. healthcheck da API;
12. exibicao de status e logs finais.

Para rodar testes dentro da imagem antes do restart, edite `.env.staging`:

```env
GPR_RUN_TESTS=1
```

## Backup antes do deploy

O backup e executado automaticamente pelo deploy, mas tambem pode ser rodado manualmente:

```bash
cd /opt/guia-produto-radar
./infra/scripts/backup_before_deploy.sh
```

Por padrao, os arquivos ficam em:

```text
/var/backups/guia-produto-radar/staging/<timestamp>/
```

Conteudo esperado:

- `postgres.dump`, quando o banco ja estiver rodando;
- copia protegida de `.env.staging`;
- `git_ref.txt`;
- `git_status.txt`;
- `manifest.txt`.

O dump do PostgreSQL usa formato custom `pg_dump -Fc`.

## Rollback basico

Se o healthcheck falhar depois do deploy, `deploy_staging.sh` tenta voltar a aplicacao para o commit anterior usando checkout em modo detached, rebuild e restart.

Limites importantes:

- rollback automatico nao desfaz migration de banco;
- se uma migration quebrar dados, restaure manualmente o dump;
- revisar logs antes de tentar novo deploy.

Restauracao manual de banco, somente se necessario:

```bash
cd /opt/guia-produto-radar
docker compose --env-file .env.staging -f docker-compose.staging.yml exec -T postgres \
  sh -lc 'pg_restore --clean --if-exists -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  < /var/backups/guia-produto-radar/staging/<timestamp>/postgres.dump
```

Antes de restaurar banco, confirme que esta no ambiente de staging.

## Nginx

Copie o exemplo:

```bash
sudo cp infra/nginx/gpr-staging.conf.example /etc/nginx/sites-available/gpr-staging.conf
sudo ln -s /etc/nginx/sites-available/gpr-staging.conf /etc/nginx/sites-enabled/gpr-staging.conf
```

Edite:

```bash
sudo nano /etc/nginx/sites-available/gpr-staging.conf
```

Ajuste:

- caminhos de `ssl_certificate`;
- caminhos de `ssl_certificate_key`;
- `server_name`, se usar outro subdominio;
- protecao com `auth_basic`, se o staging ficar acessivel publicamente.

Validar e recarregar:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Cloudflare

Se usar Cloudflare:

1. Criar registro `A` ou `CNAME` para `radar-staging.guiaproduto.com.br` apontando para a VPS.
2. Usar SSL/TLS em `Full` ou `Full (strict)`.
3. Preferir Cloudflare Origin Certificate na VPS quando usar `Full (strict)`.
4. Nao usar o dominio principal do WordPress nesta fase.
5. Desativar cache para `/api/*`, `/health`, `/version`, `/docs` e `/openapi.json`.
6. Ativar regra de acesso, WAF ou Basic Auth para limitar o admin de staging.
7. Manter `X-Robots-Tag: noindex, nofollow` no Nginx.

## Validacao da API

Na VPS:

```bash
curl -fsS http://127.0.0.1:28080/health
curl -fsS http://127.0.0.1:28080/version
curl -fsS http://127.0.0.1:28080/api/v1/radar/summary
```

Pelo dominio:

```bash
curl -fsS https://radar-staging.guiaproduto.com.br/health
curl -fsS https://radar-staging.guiaproduto.com.br/version
curl -fsS https://radar-staging.guiaproduto.com.br/api/v1/radar/summary
```

## Validacao do admin

Acesse:

```text
https://radar-staging.guiaproduto.com.br/
```

Na tela `Configuracoes`, defina a URL da API:

```text
https://radar-staging.guiaproduto.com.br
```

Validar:

- status de conexao online;
- listagem de produtos mockados;
- geracao de briefing demo;
- abertura do JSON do briefing.

## Validacao do plugin WordPress

No WordPress de staging ou em uma copia controlada:

1. instalar o plugin `wordpress/plugins/guia-produto-radar`;
2. ativar o plugin;
3. configurar a URL da API como `https://radar-staging.guiaproduto.com.br`;
4. testar shortcodes:

```text
[guia_produto_radar]
[guia_produto_ranking categoria="tecnologia" limite="10"]
[guia_produto_tendencias limite="10"]
```

Nao testar diretamente no WordPress de producao sem janela e backup.

## Logs e operacao

Status:

```bash
docker compose --env-file .env.staging -f docker-compose.staging.yml ps
```

Logs:

```bash
docker compose --env-file .env.staging -f docker-compose.staging.yml logs -f api
docker compose --env-file .env.staging -f docker-compose.staging.yml logs -f worker
docker compose --env-file .env.staging -f docker-compose.staging.yml logs -f admin
```

Migration atual:

```bash
docker compose --env-file .env.staging -f docker-compose.staging.yml exec -T api alembic current
```

Aplicar migrations manualmente:

```bash
docker compose --env-file .env.staging -f docker-compose.staging.yml run --rm api alembic upgrade head
```

## Checklist antes de liberar staging

- [ ] `.env.staging` criado na VPS e fora do Git.
- [ ] Senha do PostgreSQL trocada nos dois campos: `POSTGRES_PASSWORD` e `DATABASE_URL`.
- [ ] Docker Compose de staging valida com `config`.
- [ ] Scripts validam com `bash -n infra/scripts/deploy_staging.sh` e `bash -n infra/scripts/backup_before_deploy.sh`.
- [ ] Backup pre-deploy executado.
- [ ] Containers sobem com healthcheck saudavel.
- [ ] Alembic em `head`.
- [ ] Nginx validado com `nginx -t`.
- [ ] HTTPS funcionando no subdominio.
- [ ] Cloudflare configurado sem cache para API.
- [ ] Admin protegido por Basic Auth, Access ou regra equivalente.
- [ ] API responde `/health`, `/version` e `/api/v1/radar/summary`.
- [ ] Plugin WordPress aponta para a API de staging.
- [ ] Paginas de staging com `noindex`.

## Riscos conhecidos

- O admin ainda nao possui login proprio.
- O rollback automatico nao reverte schema de banco.
- O plugin deve ser testado primeiro em WordPress de staging ou copia controlada.
- O staging nao deve usar credenciais reais de marketplaces.
- O subdominio de staging nao deve substituir o dominio principal.
