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
```

Informe a URL base da API. Em desenvolvimento local:

```text
http://localhost:18080
```

Nao salve tokens ou credenciais reais no codigo do plugin.

## Comportamento

- Usa `wp_remote_get` para consultar a API.
- Usa transients para cache.
- Mostra fallback amigavel quando a API esta offline.
- Carrega CSS apenas quando algum shortcode e renderizado.
- Nao depende do Elementor.
