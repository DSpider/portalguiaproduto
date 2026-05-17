# Integracao Segura com WordPress Real

## Objetivo

Permitir testar o plugin Guia Produto Radar no WordPress real do Guia Produto sem quebrar o site atual, sem alterar o tema, sem criar posts automaticamente e sem publicar nada em massa.

Site atual:

```text
https://www.guiaproduto.com.br
```

Caminho do WordPress na VPS:

```text
/home/guiaproduto/htdocs/www.guiaproduto.com.br
```

API de staging na mesma VPS:

```text
http://127.0.0.1:28080
```

## Principios de seguranca

- Nao alterar a home.
- Nao alterar o tema ativo.
- Nao depender do Elementor.
- Nao criar posts automaticamente.
- Nao criar paginas automaticamente.
- Testar primeiro em pagina isolada.
- Manter backup de arquivos e banco antes de instalar.
- Manter a API interna no plugin quando WordPress e Radar estiverem na mesma VPS.
- Reverter rapidamente desativando o plugin.

## Checklist de backup antes da instalacao

Entre na VPS:

```bash
ssh root@195.35.18.232
```

Crie uma pasta de backup:

```bash
BACKUP_DIR="/root/backups/guiaproduto/wp-before-radar-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"
```

Backup dos arquivos do WordPress:

```bash
tar -czf "$BACKUP_DIR/www.guiaproduto.com.br-files.tar.gz" \
  -C /home/guiaproduto/htdocs \
  www.guiaproduto.com.br
```

Descubra os dados do banco:

```bash
grep -E "DB_NAME|DB_USER|DB_PASSWORD|DB_HOST" \
  /home/guiaproduto/htdocs/www.guiaproduto.com.br/wp-config.php
```

Faca o dump do banco substituindo os valores:

```bash
mysqldump -u DB_USER_AQUI -p DB_NAME_AQUI > "$BACKUP_DIR/www.guiaproduto.com.br-db.sql"
```

Proteja os arquivos:

```bash
chmod -R 600 "$BACKUP_DIR"/*
ls -lh "$BACKUP_DIR"
```

## Pre-checks antes do plugin

Confirme que a API esta online na VPS:

```bash
curl http://127.0.0.1:28080/health
curl http://127.0.0.1:28080/api/v1/radar/summary
```

Confirme que o plugin existe no repositorio:

```bash
ls -la /opt/guia-produto-radar/wordpress/plugins/guia-produto-radar
```

Se houver PHP CLI, valide sintaxe:

```bash
find /opt/guia-produto-radar/wordpress/plugins/guia-produto-radar -name "*.php" \
  -exec php -l {} \;
```

## Instalacao manual do plugin

Copie o plugin para o WordPress:

```bash
WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
PLUGIN_SRC=/opt/guia-produto-radar/wordpress/plugins/guia-produto-radar
PLUGIN_DST=$WP_PATH/wp-content/plugins/guia-produto-radar

rm -rf "$PLUGIN_DST"
cp -a "$PLUGIN_SRC" "$PLUGIN_DST"
chown -R guiaproduto:guiaproduto "$PLUGIN_DST"
find "$PLUGIN_DST" -type d -exec chmod 755 {} \;
find "$PLUGIN_DST" -type f -exec chmod 644 {} \;
```

Ative pelo painel:

```text
Plugins > Guia Produto Radar > Ativar
```

Ou, se houver WP-CLI:

```bash
sudo -u guiaproduto wp --path="$WP_PATH" plugin activate guia-produto-radar
```

## Configuracao recomendada

No painel:

```text
Configuracoes > Guia Produto Radar
```

Use:

```text
Ambiente: staging
URL base da API: http://127.0.0.1:28080
Tempo de cache: 300
Modo debug: desativado
```

Motivo: como WordPress e API estao na mesma VPS, `127.0.0.1` evita expor a comunicacao interna pela Cloudflare.

Se usar WP-CLI:

```bash
sudo -u guiaproduto wp --path="$WP_PATH" option update gpr_environment staging
sudo -u guiaproduto wp --path="$WP_PATH" option update gpr_api_base_url "http://127.0.0.1:28080"
sudo -u guiaproduto wp --path="$WP_PATH" option update gpr_cache_ttl 300
sudo -u guiaproduto wp --path="$WP_PATH" option update gpr_debug_mode 0
```

## Pagina de teste sugerida

Crie manualmente no WordPress:

```text
Titulo: Radar Teste
Slug: radar-teste
Status: rascunho ou privado no inicio
Conteudo:
[guia_produto_radar]
```

O plugin adiciona `noindex,nofollow` automaticamente para a pagina com slug:

```text
radar-teste
```

Ainda assim, mantenha a pagina como rascunho ou privada ate validar visualmente.

Depois teste tambem:

```text
[guia_produto_ranking categoria="tecnologia" limite="10"]
[guia_produto_tendencias limite="10"]
```

## Comportamento seguro do plugin

Se a API estiver offline:

- o WordPress nao quebra;
- o shortcode retorna uma mensagem amigavel;
- detalhes tecnicos nao aparecem para visitantes;
- CSS continua carregando somente quando o shortcode e usado.

Cache:

- usa transients do WordPress;
- TTL configuravel no admin;
- minimo de 60 segundos;
- maximo de 86400 segundos;
- recomendado para teste: 300 segundos.

Debug:

- desligado por padrao;
- so grava log se o modo debug estiver ativo e `WP_DEBUG` tambem estiver ativo;
- nao mostra erro tecnico para o visitante.

## Como testar

Teste API pela VPS:

```bash
curl http://127.0.0.1:28080/health
```

Teste o shortcode em uma pagina de rascunho:

```text
/radar-teste/
```

Verifique:

- a pagina carrega normalmente;
- o shortcode renderiza um bloco do Radar;
- se a API parar, aparece fallback amigavel;
- nao aparecem erros PHP no front;
- o CSS do plugin nao carrega em paginas sem shortcode;
- a pagina `/radar-teste/` tem `noindex,nofollow`.

Para ver os headers ou meta robots, use o inspecionador do navegador ou:

```bash
curl -I https://www.guiaproduto.com.br/radar-teste/
```

## Como reverter

Desativar plugin pelo painel:

```text
Plugins > Guia Produto Radar > Desativar
```

Ou via WP-CLI:

```bash
WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
sudo -u guiaproduto wp --path="$WP_PATH" plugin deactivate guia-produto-radar
```

Remover arquivos do plugin:

```bash
rm -rf /home/guiaproduto/htdocs/www.guiaproduto.com.br/wp-content/plugins/guia-produto-radar
```

Remover opcoes do plugin, somente se quiser limpar totalmente:

```bash
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_environment
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_api_base_url
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_cache_ttl
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_debug_mode
```

Se houver problema maior, restaure o backup de arquivos e banco feito antes da instalacao.

## Riscos e cuidados

- A API ainda usa dados mockados em algumas rotas.
- A pagina de teste nao deve entrar em menu, home ou sitemap antes da validacao.
- O cache pode manter dados antigos por alguns minutos.
- O modo debug nao deve ficar ativo permanentemente em producao.
- Nao inserir tokens ou credenciais na URL da API.
- Nao usar o plugin para publicar conteudo automaticamente nesta fase.
