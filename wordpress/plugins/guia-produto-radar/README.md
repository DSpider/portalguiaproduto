# Guia Produto Radar para WordPress

Plugin inicial para conectar o WordPress a API do Guia Produto Radar.

## Shortcodes

```text
[guia_produto_radar]
[guia_produto_ranking categoria="tecnologia" limite="10"]
[guia_produto_tendencias limite="10"]
```

## Configuracao

No painel do WordPress:

```text
Configuracoes > Guia Produto Radar
Configuracoes > Manual Guia Produto Radar
```

Informe a URL base da API. Em desenvolvimento local:

```text
http://localhost:18080
```

Em staging/producao na mesma VPS, prefira a URL interna:

```text
http://127.0.0.1:28080
```

Opcoes disponiveis:

- ambiente: local, staging ou producao;
- URL base da API;
- tempo de cache em segundos;
- modo debug para registrar erros no log quando `WP_DEBUG` estiver ativo.

Nao salve tokens ou credenciais reais no codigo do plugin.

## Comportamento

- Usa `wp_remote_get` para consultar a API.
- Usa transients para cache.
- Mostra fallback amigavel quando a API esta offline.
- Carrega CSS apenas quando algum shortcode e renderizado.
- Aplica `noindex,nofollow` automaticamente na pagina `/radar-teste/`.
- Nao depende do Elementor.

## Manual completo

O manual completo esta disponivel no painel do WordPress em:

```text
Configuracoes > Manual Guia Produto Radar
```

Tambem existe uma copia tecnica versionada em:

```text
docs/WORDPRESS_PLUGIN_MANUAL.md
```
