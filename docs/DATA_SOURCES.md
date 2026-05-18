# Fontes de Dados e Conectores

## Objetivo

Definir a arquitetura de conectores de dados do Guia Produto Radar para integrar fontes externas no futuro sem acoplar credenciais, chamadas HTTP e regras especificas diretamente na regra de negocio.

Nesta fase, todos os conectores sao mockados e deterministicos. Nenhum conector faz chamada real, scraping ou uso de credenciais.

## Principios

- Cada fonte deve implementar a mesma interface base.
- Cada conector deve retornar dados normalizados.
- Falha de uma fonte nao pode travar todo o sistema.
- Rate limit interno deve existir mesmo antes das chamadas reais.
- Logs devem indicar falhas sem expor segredos.
- Credenciais reais nunca entram no repositorio.
- Scraping agressivo nao e permitido.
- Dados editoriais e comerciais devem ser separados de inferencias.

## Estrutura

```text
packages/connectors/
|-- __init__.py
|-- base.py
|-- config.py
|-- errors.py
|-- manager.py
|-- mock_sources.py
|-- models.py
`-- rate_limit.py
```

## Interface base

Todo conector herda de:

```python
BaseConnector
```

Metodo publico:

```python
fetch(request: ConnectorRequest) -> ConnectorResponse
```

O metodo publico cuida de:

- conector desabilitado;
- rate limit;
- captura de erros controlados;
- captura de erros inesperados;
- logs;
- retorno padronizado.

Cada fonte implementa apenas:

```python
_fetch(request: ConnectorRequest) -> list[NormalizedRecord]
```

## Formato padrao de entrada

```python
ConnectorRequest(
    query="melhor fone bluetooth",
    category="audio",
    product_slug="fone-bluetooth-demo",
    product_name="Fone Bluetooth Demo",
    country="BR",
    locale="pt-BR",
    limit=10,
)
```

Campos:

- `query`: termo principal de busca.
- `category`: categoria editorial/comercial.
- `product_slug`: slug interno quando houver produto mapeado.
- `product_name`: nome do produto quando houver.
- `country`: pais alvo.
- `locale`: idioma/regiao.
- `limit`: limite operacional para resultados.

## Formato padrao de retorno

Cada conector retorna:

```python
ConnectorResponse(
    source="google_trends",
    ok=True,
    records=[...],
    errors=[],
    rate_limited=False,
    duration_ms=1.2,
)
```

Cada item normalizado segue:

```python
NormalizedRecord(
    source="google_trends",
    record_type="trend",
    subject="Fone Bluetooth Demo",
    title=None,
    url=None,
    external_id=None,
    metrics={
        "trend_growth_percent": 38.0,
        "search_interest": 74,
    },
    attributes={
        "country": "BR",
        "locale": "pt-BR",
        "category": "audio",
    },
    confidence=0.72,
    observed_at=datetime(...),
    raw_payload={"mock": True},
)
```

Campos principais:

- `source`: fonte de origem.
- `record_type`: tipo normalizado de dado.
- `subject`: termo/produto principal.
- `title`: titulo quando aplicavel.
- `url`: URL quando aplicavel.
- `external_id`: ID externo quando aplicavel.
- `metrics`: numeros e sinais usados em score.
- `attributes`: dados auxiliares sem peso direto.
- `confidence`: confianca entre 0 e 1.
- `observed_at`: data/hora de observacao.
- `raw_payload`: payload bruto controlado, sem segredos.

## Conectores mockados

### Google Trends ou alternativa

Classe:

```python
MockGoogleTrendsConnector
```

Tipo de retorno:

- `record_type`: `trend`
- metricas:
  - `trend_growth_percent`
  - `search_interest`
  - `period_days`

Uso futuro:

- validar crescimento de tendencia;
- detectar sazonalidade;
- alimentar score de tendencia.

### Google Ads Keyword Planner

Classe:

```python
MockGoogleAdsKeywordPlannerConnector
```

Tipo de retorno:

- `record_type`: `keyword`
- metricas:
  - `estimated_search_volume`
  - `competition_index`
  - `suggested_bid_brl`

Uso futuro:

- estimar volume de busca;
- avaliar competicao paga;
- apoiar priorizacao SEO/comercial.

### Google Search Console

Classe:

```python
MockGoogleSearchConsoleConnector
```

Tipo de retorno:

- `record_type`: `search_console`
- metricas:
  - `clicks`
  - `impressions`
  - `ctr`
  - `average_position`

Uso futuro:

- medir paginas existentes;
- encontrar oportunidades de atualizacao;
- comparar CTR e posicao media.

### Amazon Creators API ou alternativa

Classe:

```python
MockAmazonCreatorsConnector
```

Tipo de retorno:

- `record_type`: `offer`
- metricas:
  - `price`
  - `old_price`
  - `rating`
  - `reviews_count`
  - `commission_rate_percent`

Uso futuro:

- ofertas;
- disponibilidade;
- comissao;
- links de afiliado aprovados.

Variaveis de ambiente previstas:

```text
AMAZON_CREDENTIAL_ID=
AMAZON_CREDENTIAL_SECRET=
AMAZON_CREATORS_VERSION=2.1
```

Essas variaveis devem ser preenchidas somente em `.env.staging` ou `.env.production` na VPS. Nunca preencher valores reais em `.env.example`, `.env.staging.example`, codigo, WordPress, prints ou mensagens.

Nesta fase, o mock apenas informa se as credenciais estao configuradas e qual versao foi selecionada. O segredo nao entra no retorno normalizado, logs ou payload bruto.

### Mercado Livre

Classe:

```python
MockMercadoLivreConnector
```

Tipo de retorno:

- `record_type`: `offer`

Uso futuro:

- comparar preco;
- disponibilidade;
- volume de avaliacoes;
- complementar oferta quando Amazon nao for suficiente.

### Shopee

Classe:

```python
MockShopeeConnector
```

Tipo de retorno:

- `record_type`: `offer`

Uso futuro:

- ofertas alternativas;
- ticket baixo;
- comissao;
- produtos com bom apelo comercial.

### SERP API terceirizada

Classe:

```python
MockSerpApiConnector
```

Tipo de retorno:

- `record_type`: `serp`
- metricas:
  - `seo_competition`
  - `ads_count`
  - `organic_results_count`
  - `featured_snippet_present`

Uso futuro:

- medir dificuldade SEO;
- identificar tipo de resultado;
- apoiar escolha de formato da pagina.

### Dados internos do Guia Produto

Classe:

```python
MockInternalDataConnector
```

Tipo de retorno:

- `record_type`: `internal_product`
- metricas:
  - `editorial_priority`
  - `existing_page`
  - `internal_score`

Uso futuro:

- cruzar dados do WordPress;
- identificar paginas ja existentes;
- evitar duplicidade editorial.

## Manager de fontes

Classe:

```python
DataSourceManager
```

Exemplo:

```python
from packages.connectors import ConnectorRequest, DataSourceManager, build_default_mock_connectors

manager = DataSourceManager(build_default_mock_connectors())
responses = manager.collect(
    ConnectorRequest(
        query="melhor fone bluetooth",
        category="audio",
        product_slug="fone-bluetooth-demo",
        product_name="Fone Bluetooth Demo",
    )
)

records = manager.collect_records(...)
```

Se um conector falhar, ele retorna `ConnectorResponse(ok=False, errors=[...])`. Os demais conectores continuam executando.

## Configuracao por variavel de ambiente

Padrao:

```text
GPR_CONNECTOR_<FONTE>_ENABLED=true
GPR_CONNECTOR_<FONTE>_RATE_LIMIT_PER_MINUTE=60
GPR_CONNECTOR_<FONTE>_TIMEOUT_SECONDS=5
```

Exemplos:

```text
GPR_CONNECTOR_GOOGLE_TRENDS_ENABLED=true
GPR_CONNECTOR_GOOGLE_TRENDS_RATE_LIMIT_PER_MINUTE=60

GPR_CONNECTOR_SERP_API_ENABLED=true
GPR_CONNECTOR_SERP_API_RATE_LIMIT_PER_MINUTE=20

GPR_CONNECTOR_SHOPEE_ENABLED=false
```

Arquivos de exemplo:

- `.env.example`
- `.env.staging.example`

## Rate limit interno

O rate limit atual e em memoria e por processo.

Ele evita excesso acidental durante testes e prepara o contrato para fontes reais.

Limites atuais sugeridos:

- Google Trends: 60/min
- Keyword Planner: 30/min
- Search Console: 60/min
- Amazon: 30/min
- Mercado Livre: 30/min
- Shopee: 30/min
- SERP API: 20/min
- Dados internos: 120/min

Para producao com multiplos processos, considerar Redis para rate limit distribuido.

## Tratamento de erro

Erros controlados usam:

```python
ConnectorRuntimeError(code, message, retryable)
```

O `BaseConnector` converte isso em:

```python
ConnectorError(
    source="...",
    code="...",
    message="...",
    retryable=True,
)
```

Erros inesperados sao capturados como:

```text
unexpected_error
```

Nenhum erro de conector deve derrubar a coleta inteira.

## Logs

Os conectores usam loggers com o padrao:

```text
guia_produto_radar.connectors.<source>
guia_produto_radar.connectors.manager
```

Regras:

- logar falhas e rate limits;
- nao logar credenciais;
- nao logar tokens;
- nao logar payload sensivel;
- preservar mensagem suficiente para diagnostico.

## Testes

Arquivo:

```text
tests/test_connectors.py
```

Cobre:

- todos os conectores mockados retornando registros normalizados;
- configuracao por variavel de ambiente;
- rate limit;
- conector desabilitado;
- falha isolada sem travar o manager.

Comando:

```bash
pytest tests/test_connectors.py
```

## Proximos passos para integracao real

1. Rotacionar qualquer credencial que tenha sido exposta fora do cofre/ambiente seguro.
2. Escolher Amazon como primeira fonte real de menor risco.
3. Criar classe real mantendo a mesma interface do mock.
4. Guardar credenciais fora do Git, preferencialmente em `.env.staging` com permissao 600.
5. Implementar timeout e retry com backoff.
6. Criar testes com responses falsas.
7. Registrar limites de uso da API.
8. Persistir dados normalizados no PostgreSQL.
9. Integrar registros normalizados ao motor de score.
10. Adicionar monitoramento por fonte.
11. Ativar em staging antes de producao.

## Sobre edicao de chaves pelo painel

Nao e recomendado salvar credenciais de marketplace no WordPress ou no admin estatico atual.

Motivos:

- o admin interno ainda nao possui login proprio de aplicacao;
- localStorage do navegador nao e armazenamento seguro;
- opcoes do WordPress ficam no banco do WordPress e aumentam o impacto de um vazamento;
- credenciais de marketplace pertencem ao backend, nao a vitrine publica.

Decisao recomendada nesta fase:

- configurar chaves por `.env.staging` e `.env.production`;
- exibir no painel apenas status mascarado, como "configurado" ou "nao configurado", quando houver endpoint autenticado;
- criar editor de segredos somente depois de autenticacao, auditoria e armazenamento criptografado.

## Nao fazer nesta fase

- Nao usar credenciais reais.
- Nao fazer scraping agressivo.
- Nao gerar paginas automaticamente.
- Nao usar dados mockados como se fossem dados reais.
- Nao publicar ofertas, precos ou ratings sem fonte confiavel.
