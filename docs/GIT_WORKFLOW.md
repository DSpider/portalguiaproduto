# Fluxo Git do Guia Produto Radar

Este documento define o fluxo Git recomendado para o Guia Produto Radar durante as fases local, staging e producao.

O objetivo e simples: todo codigo nasce no Windows/local, passa pelo GitHub e pelo CI, depois a VPS apenas puxa a versao aprovada. A VPS nao deve ser usada como ambiente de desenvolvimento.

## Estado decidido

- Repositorio oficial: `https://github.com/DSpider/portalguiaproduto.git`
- Branch principal: `main`
- Ambiente local: `C:\gp_projects\portalguiaproduto`
- Ambiente staging na VPS: `/opt/guia-produto-radar`
- WordPress publico: `/home/guiaproduto/htdocs/www.guiaproduto.com.br`

## Regras principais

1. Nao commitar arquivos `.env` reais.
2. Nao commitar credenciais, tokens, cookies ou senhas.
3. Nao desenvolver diretamente na VPS.
4. Nao alterar o WordPress real antes de backup.
5. Toda alteracao de codigo deve passar por branch, commit, push e pull request.
6. O merge para `main` so deve acontecer depois do CI passar.
7. O staging da VPS deve sempre rodar codigo vindo da `main`.

## Branches

Use a `main` como branch estavel.

Use branches curtas para cada trabalho:

```text
feat/nome-da-funcionalidade
fix/nome-do-ajuste
chore/nome-da-tarefa
docs/nome-do-documento
```

Exemplos:

```text
feat/amazon-creators-connector
fix/admin-api-status
chore/git-workflow
docs/wordpress-manual
```

## Ciclo local no Windows

Antes de comecar uma tarefa:

```powershell
cd C:\gp_projects\portalguiaproduto
git switch main
git pull --ff-only origin main
git status --short --branch
```

Crie uma branch:

```powershell
git switch -c feat/minha-tarefa
```

Depois de alterar os arquivos, valide:

```powershell
pytest
git status --short
```

Se estiver tudo certo:

```powershell
git add .
git commit -m "feat: descreve a mudanca"
git push -u origin feat/minha-tarefa
```

Abra um pull request no GitHub para `main`.

## Pull request

Antes de fazer merge:

1. Conferir se o CI passou.
2. Conferir se nao ha `.env` real no diff.
3. Conferir se nao ha credenciais no diff.
4. Conferir se migrations foram criadas quando o banco mudou.
5. Conferir se README/docs foram atualizados quando o uso mudou.

Depois do merge:

```powershell
git switch main
git pull --ff-only origin main
git status --short --branch
```

## Atualizar staging na VPS

Na VPS, entre no projeto:

```bash
cd /opt/guia-produto-radar
```

Atualize a branch `main`:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
```

Rode o deploy manual de staging:

```bash
bash infra/scripts/deploy_staging.sh
```

Valide a API:

```bash
curl http://127.0.0.1:28080/health
```

Valide os containers:

```bash
docker compose \
  --env-file /opt/guia-produto-radar/.env.staging \
  -f /opt/guia-produto-radar/docker-compose.staging.yml \
  ps
```

## Atualizar plugin no WordPress

Antes de atualizar o plugin em producao, faca backup do plugin atual:

```bash
WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
PLUGIN_SRC=/opt/guia-produto-radar/wordpress/plugins/guia-produto-radar
PLUGIN_DST=$WP_PATH/wp-content/plugins/guia-produto-radar
PLUGIN_BACKUP=/home/guiaproduto/backups/plugin-guia-produto-radar-$(date +%Y%m%d_%H%M%S)

mkdir -p /home/guiaproduto/backups
[ -d "$PLUGIN_DST" ] && mv "$PLUGIN_DST" "$PLUGIN_BACKUP"
cp -a "$PLUGIN_SRC" "$PLUGIN_DST"
chown -R guiaproduto:guiaproduto "$PLUGIN_DST"
find "$PLUGIN_DST" -type d -exec chmod 755 {} \;
find "$PLUGIN_DST" -type f -exec chmod 644 {} \;
```

Depois, entre no painel WordPress e valide:

```text
Configuracoes > Guia Produto Radar
Configuracoes > Manual Guia Produto Radar
```

## Arquivos de ambiente

Arquivos permitidos no Git:

```text
.env.example
.env.staging.example
```

Arquivos proibidos no Git:

```text
.env
.env.staging
.env.production
*.env.local
```

O `.env.staging` deve existir apenas na VPS.

## Rollback de staging

Para voltar rapidamente o staging para um commit anterior:

```bash
cd /opt/guia-produto-radar
git log --oneline -5
git checkout COMMIT_ANTERIOR
bash infra/scripts/deploy_staging.sh
```

Depois que a correcao definitiva for feita no GitHub, volte para a `main`:

```bash
git checkout main
git pull --ff-only origin main
bash infra/scripts/deploy_staging.sh
```

## Rollback do plugin WordPress

Se o plugin causar problema, restaure o backup criado antes da copia:

```bash
WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
PLUGIN_DST=$WP_PATH/wp-content/plugins/guia-produto-radar
PLUGIN_BACKUP=/home/guiaproduto/backups/NOME_DA_PASTA_DE_BACKUP
PLUGIN_FAILED=/home/guiaproduto/backups/plugin-guia-produto-radar-falhou-$(date +%Y%m%d_%H%M%S)

[ -d "$PLUGIN_DST" ] && mv "$PLUGIN_DST" "$PLUGIN_FAILED"
cp -a "$PLUGIN_BACKUP" "$PLUGIN_DST"
chown -R guiaproduto:guiaproduto "$PLUGIN_DST"
find "$PLUGIN_DST" -type d -exec chmod 755 {} \;
find "$PLUGIN_DST" -type f -exec chmod 644 {} \;
```

Se necessario, desative o plugin pelo painel WordPress.

## Hotfix

Para uma correcao urgente:

1. Crie uma branch `fix/nome-do-problema` a partir da `main`.
2. Corrija apenas o problema urgente.
3. Rode os testes.
4. Abra PR.
5. Aguarde CI.
6. Faca merge.
7. Atualize staging.
8. Atualize o plugin no WordPress somente se o hotfix envolver o plugin.

## Proximo passo apos este fluxo

Com o Git estabilizado, o proximo passo tecnico recomendado e trabalhar em uma branch propria para autenticacao simples do admin interno e protecao dos endpoints administrativos futuros.
