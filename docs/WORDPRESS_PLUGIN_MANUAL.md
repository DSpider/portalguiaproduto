# Manual do Plugin Guia Produto Radar

## Objetivo principal

O plugin Guia Produto Radar conecta o WordPress do Guia Produto a API do Guia Produto Radar.

O WordPress continua sendo a vitrine publica do portal. A API, o worker, o PostgreSQL e o Redis ficam responsaveis por dados, tendencias, scores, briefings e integracoes futuras.

## Manual do usuario

### Onde acessar

No painel do WordPress:

```text
Configuracoes > Guia Produto Radar
```

O plugin tambem adiciona:

```text
Configuracoes > Manual Guia Produto Radar
```

### Configuracoes

Ambiente:

- `local`: desenvolvimento no Windows.
- `staging`: testes na VPS antes de producao.
- `production`: uso futuro quando a integracao estiver aprovada.

URL base da API:

- local Windows: `http://localhost:18080`
- staging na mesma VPS: `http://127.0.0.1:28080`
- admin staging pelo navegador: `https://radar-staging.guiaproduto.com.br`
- producao futura sugerida: `http://127.0.0.1:38080`

Tempo de cache:

- recomendado: `300` segundos;
- minimo: `60` segundos;
- maximo: `86400` segundos.

Modo debug:

- desligado por padrao;
- usar apenas para diagnostico;
- so grava log se `WP_DEBUG` tambem estiver ativo.

### Shortcodes

Resumo do Radar:

```text
[guia_produto_radar]
```

Ranking por categoria:

```text
[guia_produto_ranking categoria="tecnologia" limite="10"]
```

Tendencias:

```text
[guia_produto_tendencias limite="10"]
```

### Pagina de teste

Crie manualmente uma pagina:

```text
Titulo: Radar Teste
Slug: radar-teste
Conteudo: [guia_produto_radar]
```

O plugin adiciona `noindex,nofollow` automaticamente para paginas com slug `radar-teste`.

### Comportamento seguro

Se a API estiver offline:

- a pagina nao quebra;
- o shortcode mostra uma mensagem amigavel;
- detalhes tecnicos nao aparecem para visitantes;
- o CSS continua carregando apenas quando o shortcode e usado.

## Manual tecnico

### Caminhos importantes na VPS

WordPress publico:

```text
/home/guiaproduto/htdocs/www.guiaproduto.com.br
```

Plugin instalado:

```text
/home/guiaproduto/htdocs/www.guiaproduto.com.br/wp-content/plugins/guia-produto-radar
```

Repositorio do Radar:

```text
/opt/guia-produto-radar
```

Backups sugeridos:

```text
/root/backups/guiaproduto
/var/backups/guia-produto-radar
```

### Portas e servicos

Local Windows:

- API: `localhost:18080`
- Admin: `localhost:18090`
- PostgreSQL: `localhost:15432`
- Redis: `localhost:16379`

Staging VPS:

- API interna: `127.0.0.1:28080`
- Admin interno: `127.0.0.1:28090`
- Admin publico protegido: `radar-staging.guiaproduto.com.br`
- PostgreSQL: somente rede Docker
- Redis: somente rede Docker

Producao futura recomendada:

- API interna: `127.0.0.1:38080`
- Admin publico protegido: `radar.guiaproduto.com.br`
- PostgreSQL e Redis sem exposicao publica.

### Opcoes no banco do WordPress

O plugin salva apenas opcoes simples:

- `gpr_environment`
- `gpr_api_base_url`
- `gpr_cache_ttl`
- `gpr_debug_mode`

Ele nao cria posts automaticamente, nao altera tema e nao cria tabela propria no WordPress.

### Cache

O plugin usa transients do WordPress. As chaves usam prefixo:

```text
gpr_api_
```

O cache considera ambiente, URL da API e caminho da rota.

### Atualizacao manual do plugin na VPS

```bash
cd /opt/guia-produto-radar
git pull

find wordpress/plugins/guia-produto-radar -name "*.php" -exec php -l {} \;

WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
PLUGIN_SRC=/opt/guia-produto-radar/wordpress/plugins/guia-produto-radar
PLUGIN_DST=$WP_PATH/wp-content/plugins/guia-produto-radar

rm -rf "$PLUGIN_DST"
cp -a "$PLUGIN_SRC" "$PLUGIN_DST"
chown -R guiaproduto:guiaproduto "$PLUGIN_DST"
find "$PLUGIN_DST" -type d -exec chmod 755 {} \;
find "$PLUGIN_DST" -type f -exec chmod 644 {} \;
```

### Diagnostico

API:

```bash
curl http://127.0.0.1:28080/health
curl http://127.0.0.1:28080/api/v1/radar/summary
```

Containers:

```bash
cd /opt/guia-produto-radar
docker compose --env-file .env.staging -f docker-compose.staging.yml ps
docker compose --env-file .env.staging -f docker-compose.staging.yml logs -f api
```

WordPress:

```bash
WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
sudo -u guiaproduto wp --path="$WP_PATH" plugin status guia-produto-radar
sudo -u guiaproduto wp --path="$WP_PATH" option get gpr_api_base_url
```

### Reversao

Desativar plugin:

```bash
WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
sudo -u guiaproduto wp --path="$WP_PATH" plugin deactivate guia-produto-radar
```

Remover arquivos:

```bash
rm -rf /home/guiaproduto/htdocs/www.guiaproduto.com.br/wp-content/plugins/guia-produto-radar
```

Remover opcoes, somente se quiser limpar totalmente:

```bash
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_environment
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_api_base_url
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_cache_ttl
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_debug_mode
```

### Cuidados de seguranca

- Nunca coloque token, senha ou cookie na URL da API.
- Nao exponha PostgreSQL e Redis na internet.
- Proteja o admin do Radar com senha ou Cloudflare Access.
- Desligue o modo debug quando terminar o diagnostico.
- Faca backup antes de atualizar o plugin.
- Teste primeiro em `/radar-teste/`.
