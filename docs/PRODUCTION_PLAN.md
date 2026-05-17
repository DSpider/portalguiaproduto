# Plano de Producao do Guia Produto Radar

## Objetivo

Definir o caminho pratico para levar o Guia Produto Radar para producao sem deploy automatico, sem credenciais reais no repositorio e sem risco desnecessario para o WordPress atual.

Este plano nao executa deploy. Ele descreve a arquitetura final, decisoes recomendadas, checklists e procedimentos de reversao.

## 1. Arquitetura final de producao

### Componentes

- WordPress publico: continua servindo `https://www.guiaproduto.com.br`.
- Plugin WordPress Guia Produto Radar: ponte leve entre WordPress e API.
- API FastAPI: regras de negocio, produtos, tendencias, scores, briefings e endpoints de consulta.
- Worker: tarefas recorrentes de coleta, atualizacao de scores, geracao de rascunhos e manutencao.
- PostgreSQL: banco principal do Radar.
- Redis: cache, filas e controle de jobs.
- Admin interno: painel operacional para produtos, tendencias, scores e briefings.
- Nginx da VPS: proxy reverso e TLS.
- Cloudflare: DNS, TLS de borda, WAF, regras de cache e protecao de acesso.

### Separacao recomendada

```text
Visitante
  -> Cloudflare
  -> Nginx VPS
  -> WordPress em /home/guiaproduto/htdocs/www.guiaproduto.com.br
  -> Plugin WordPress
  -> API Radar via http://127.0.0.1:<porta interna>

Operador interno
  -> Cloudflare Access ou Basic Auth
  -> Nginx VPS
  -> Admin Radar
  -> API Radar

Worker
  -> PostgreSQL
  -> Redis
  -> APIs externas futuras, com credenciais fora do Git
```

### Recomendacao operacional

Manter a API de producao acessivel internamente para o WordPress por `127.0.0.1`. Expor publicamente apenas rotas realmente necessarias e protegidas.

## 2. Dominios e subdominios sugeridos

### Publico

- `www.guiaproduto.com.br`: WordPress publico atual.
- `guiaproduto.com.br`: redirecionar para `www.guiaproduto.com.br` ou manter padrao atual.

### Staging

- `radar-staging.guiaproduto.com.br`: ambiente de validacao.
- Deve ter `noindex,nofollow`.
- Deve exigir senha, Cloudflare Access ou regra equivalente.

### Producao interna

Opcoes recomendadas:

- `radar.guiaproduto.com.br`: admin/API protegidos.
- `api-radar.guiaproduto.com.br`: apenas se for necessario expor API para consumo externo.

Decisao recomendada para primeira producao:

- WordPress consome API por `http://127.0.0.1:38080`.
- Admin usa `radar.guiaproduto.com.br` protegido por Cloudflare Access ou Basic Auth.
- Nao expor API publica alem de health/version se nao houver necessidade.

## 3. Estrategia de backup

### Antes de qualquer deploy

Criar backups de:

- arquivos do WordPress;
- banco MySQL/MariaDB do WordPress;
- banco PostgreSQL do Radar;
- `.env.production`;
- configuracoes Nginx;
- versao Git atual.

### Frequencia recomendada

- WordPress arquivos: diario incremental ou snapshot da VPS.
- WordPress banco: diario, com retencao minima de 7 a 14 dias.
- Radar PostgreSQL: diario, antes de cada deploy e antes de migrations.
- Nginx: antes de qualquer alteracao.
- `.env.production`: copia segura local na VPS, fora da pasta publica e fora do Git.

### Local de backup

Usar diretorio fora do webroot:

```text
/var/backups/guia-produto-radar/production/
/root/backups/guiaproduto/
```

Quando possivel, replicar para armazenamento externo seguro.

### Validacao de backup

Um backup so deve ser considerado valido se:

- o arquivo existe;
- tem tamanho coerente;
- o dump do banco consegue ser listado/restaurado em ambiente de teste;
- o caminho e timestamp foram registrados.

## 4. Estrategia de rollback

### Rollback da aplicacao Radar

1. Parar containers atuais.
2. Voltar para o commit anterior validado.
3. Rebuildar imagens.
4. Subir containers.
5. Rodar healthcheck.

### Rollback de banco Radar

Usar dump pre-deploy somente se a migration causou problema real.

Ponto importante:

- rollback de codigo nao desfaz migration automaticamente;
- migrations destrutivas devem ser proibidas ate haver estrategia formal.

### Rollback do WordPress

1. Desativar plugin.
2. Remover shortcodes da pagina afetada ou voltar a revisao da pagina.
3. Restaurar arquivos do plugin se necessario.
4. Restaurar banco WordPress apenas em caso extremo.

### Tempo alvo

- Reversao do plugin: menos de 5 minutos.
- Reversao do Radar: menos de 15 minutos.
- Restauracao completa do WordPress: depende do tamanho do site e deve ser testada antes de producao.

## 5. Estrategia de logs

### API

Registrar:

- start/stop da aplicacao;
- erros de validacao;
- erros de banco;
- chamadas a integrações futuras;
- tempo de resposta em endpoints principais.

Nao registrar:

- tokens;
- senhas;
- cookies;
- payloads com credenciais;
- URLs de afiliado completas se contiverem parametros sensiveis.

### Worker

Registrar:

- inicio/fim de jobs;
- duracao;
- quantidade de itens processados;
- falhas por fonte;
- retry/backoff.

### WordPress plugin

Manter debug desligado por padrao.

Quando ativo:

- registrar erros da API apenas se `WP_DEBUG` estiver ativo;
- nao exibir stack trace para visitante.

### Retencao

Recomendacao inicial:

- logs de containers: 7 dias;
- logs Nginx: 14 dias;
- logs de aplicacao estruturados: 30 dias quando houver volume controlado.

## 6. Estrategia de monitoramento

### Healthchecks minimos

- `GET /health`
- `GET /version`
- `GET /api/v1/radar/summary`
- status dos containers;
- uso de disco;
- uso de memoria;
- disponibilidade do WordPress.

### Alertas recomendados

- API fora por mais de 2 minutos.
- PostgreSQL sem resposta.
- Redis sem resposta.
- worker parado.
- uso de disco acima de 80%.
- erro 5xx frequente no Nginx.
- pagina publica com shortcode retornando fallback por tempo prolongado.

### Ferramentas possiveis

Fase inicial:

- cron com `curl` e logs;
- UptimeRobot, Better Stack ou equivalente;
- Cloudflare Health Checks se disponivel;
- logs Docker/Nginx revisados manualmente.

Fase posterior:

- Prometheus;
- Grafana;
- Loki;
- Sentry ou OpenTelemetry.

## 7. Seguranca de variaveis de ambiente

### Arquivos

Nao versionar:

- `.env`;
- `.env.production`;
- credenciais de marketplace;
- credenciais WordPress;
- tokens Cloudflare;
- chaves privadas;
- cookies.

### Permissoes

Na VPS:

```bash
chmod 600 .env.production
chown root:root .env.production
```

### Rotacao

Rotacionar credenciais:

- antes de producao;
- apos qualquer exposicao acidental;
- quando um colaborador perder acesso;
- periodicamente para integrações externas.

### Decisao recomendada

Usar `.env.production` manual na VPS nesta fase. GitHub Secrets e GitHub Actions ficam para uma fase posterior, depois que o deploy manual estiver estavel.

## 8. Fluxo de deploy

### Fase manual inicial

1. Validar staging.
2. Rodar testes locais.
3. Rodar testes na VPS/staging.
4. Fazer backup WordPress e Radar.
5. Congelar janela de mudanca.
6. Fazer `git pull` na pasta de producao do Radar.
7. Validar Compose.
8. Buildar containers.
9. Rodar migrations.
10. Subir containers.
11. Validar healthchecks.
12. Atualizar plugin WordPress, se houver nova versao.
13. Testar pagina de controle.
14. Monitorar logs.

### GitHub Actions

Nao criar agora.

Planejamento futuro:

- CI para lint/testes;
- build de imagem;
- deploy manual aprovado;
- secrets no GitHub;
- ambiente separado para staging e producao.

## 9. Checklist antes de producao

- [ ] Staging validado por pelo menos alguns dias.
- [ ] Backup completo do WordPress testado.
- [ ] Backup do PostgreSQL Radar testado.
- [ ] Rollback do plugin testado.
- [ ] Rollback do Radar testado.
- [ ] `php -l` executado no plugin.
- [ ] Pytest executado.
- [ ] Docker Compose de producao validado.
- [ ] Nginx validado com `nginx -t`.
- [ ] Certificado TLS valido.
- [ ] Cloudflare configurado.
- [ ] Admin protegido.
- [ ] API interna acessivel por `127.0.0.1`.
- [ ] `.env.production` criado e protegido.
- [ ] Nenhuma credencial real no Git.
- [ ] Paginas de teste com `noindex`.
- [ ] Plugin configurado com cache.
- [ ] Modo debug desligado.
- [ ] Plano de reversao aprovado.

## 10. Checklist depois de producao

- [ ] `GET /health` OK.
- [ ] `GET /version` OK.
- [ ] WordPress carregando normalmente.
- [ ] Pagina de teste com shortcode OK.
- [ ] Nenhum erro PHP no log.
- [ ] Nenhum erro 5xx no Nginx.
- [ ] Plugin usando cache.
- [ ] Admin protegido.
- [ ] Backup pos-deploy criado.
- [ ] Sitemap sem paginas indevidas.
- [ ] `robots.txt` validado.
- [ ] Search Console sem erro critico.
- [ ] Core Web Vitals sem regressao evidente.
- [ ] Monitoramento ativo.

## 11. Plano de reversao do plugin WordPress

### Reversao rapida

Desativar plugin pelo painel:

```text
Plugins > Guia Produto Radar > Desativar
```

Ou via WP-CLI:

```bash
WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
sudo -u guiaproduto wp --path="$WP_PATH" plugin deactivate guia-produto-radar
```

### Remover arquivos

```bash
rm -rf /home/guiaproduto/htdocs/www.guiaproduto.com.br/wp-content/plugins/guia-produto-radar
```

### Remover opcoes somente se necessario

```bash
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_environment
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_api_base_url
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_cache_ttl
sudo -u guiaproduto wp --path="$WP_PATH" option delete gpr_debug_mode
```

### Reverter pagina

- remover shortcodes da pagina afetada;
- voltar revisao anterior da pagina no WordPress;
- limpar caches do WordPress/Cloudflare.

## 12. Plano de indexacao SEO

### Fase 1: teste sem indexar

- `/radar-teste/` com `noindex,nofollow`.
- Shortcodes testados sem entrada em menu ou sitemap.

### Fase 2: paginas editoriais controladas

- publicar poucas paginas revisadas manualmente;
- exigir H1 unico;
- title e meta description revisados;
- schema apenas com dados reais;
- data de atualizacao visivel;
- fonte/origem dos dados quando aplicavel.

### Fase 3: escala progressiva

- liberar novas paginas por lote pequeno;
- medir indexacao, CTR, posicao media e conversao;
- pausar escala se houver sinais de conteudo fino ou queda de qualidade.

## 13. Plano de sitemap

### Regra inicial

Nao incluir paginas geradas/teste no sitemap automaticamente.

### Quando incluir

Somente incluir se:

- pagina foi revisada por humano;
- possui conteudo suficiente;
- possui dados confiaveis;
- nao inventa preco, rating ou review;
- possui canonical correto;
- tem intencao de busca clara.

### Operacao

- validar sitemap do plugin SEO atual do WordPress;
- excluir `/radar-teste/`;
- incluir paginas finais apenas quando publicadas;
- enviar sitemap ao Search Console apos validacao.

## 14. Plano de robots.txt

### Staging

Bloquear indexacao:

```text
User-agent: *
Disallow: /
```

Ou usar `X-Robots-Tag: noindex,nofollow` no Nginx.

### Producao

Nao bloquear o site inteiro.

Garantir bloqueio ou noindex para:

- staging;
- paginas de teste;
- admin;
- endpoints internos;
- paginas sem revisao editorial.

Exemplo conceitual:

```text
User-agent: *
Disallow: /wp-admin/
Disallow: /radar-teste/

Sitemap: https://www.guiaproduto.com.br/sitemap.xml
```

Validar com o plugin SEO atual antes de editar manualmente.

## 15. Plano de Search Console

Antes de producao:

- verificar propriedade do dominio;
- validar sitemap atual;
- registrar baseline de indexacao, CTR e Core Web Vitals.

Depois de producao:

- enviar sitemap atualizado;
- inspecionar manualmente primeiras URLs;
- monitorar cobertura;
- verificar rich results;
- acompanhar erros de rastreamento;
- acompanhar paginas com `noindex` inesperado.

Frequencia inicial:

- diariamente nos primeiros 7 dias;
- depois 2 a 3 vezes por semana.

## 16. Plano de Core Web Vitals

### Meta

Nao piorar performance do WordPress publico.

### Cuidados no plugin

- CSS carregado apenas com shortcode.
- Sem JavaScript no front nesta fase.
- Cache com transients.
- Sem chamadas externas no browser para montar bloco publico.

### Validacao

Testar:

- pagina sem shortcode antes/depois;
- pagina `/radar-teste/`;
- mobile e desktop;
- PageSpeed Insights;
- Search Console Core Web Vitals;
- waterfall no navegador.

### Limites iniciais recomendados

- LCP sem regressao relevante.
- INP sem regressao relevante.
- CLS proximo de zero no bloco do shortcode.
- HTML renderizado pelo plugin sem layout instavel.

## 17. Plano de atualizacao recorrente dos dados

### Fase atual

- dados mockados e fluxos manuais;
- sem scraping pesado;
- sem credenciais reais de marketplace.

### Producao inicial controlada

- worker com jobs agendados leves;
- registrar inicio/fim/falhas;
- limitar volume por fonte;
- cachear respostas;
- nao gerar paginas automaticamente.

### Frequencias sugeridas

- healthcheck: a cada 1 minuto por monitor externo.
- score de produtos prioritarios: 1 a 4 vezes por dia.
- ofertas marketplace: conforme regras da API e limites de afiliado.
- briefings editoriais: sob demanda.
- revisao SEO: semanal por lote.

### Regras editoriais

- IA gera rascunho, nao publicacao final.
- humano aprova antes de indexar.
- nao inventar preco, nota, review ou experiencia pratica.
- marcar dados insuficientes como pendentes.

## Decisoes recomendadas

1. Manter WordPress como vitrine publica.
2. Manter Radar como servico separado em Docker.
3. Consumir API pelo plugin via `127.0.0.1` quando estiver na mesma VPS.
4. Proteger admin com Cloudflare Access ou Basic Auth.
5. Fazer deploy de producao manual nas primeiras fases.
6. Criar GitHub Actions apenas depois que deploy manual, backup e rollback estiverem comprovados.
7. Publicar primeiras paginas SEO em lotes pequenos e revisados.

## Riscos principais

- Expor admin sem autenticacao.
- Indexar paginas de teste ou conteudo fino.
- Rodar migration sem backup.
- Quebrar WordPress por plugin sem rollback testado.
- Vazamento de credenciais em `.env`.
- Sobrecarga por chamadas externas sem cache.
- Dependencia de dados mockados em paginas publicas.

## Proximos passos

1. Finalizar validacao de staging.
2. Testar plugin em `/radar-teste/` com `noindex`.
3. Validar backup e restore em ambiente controlado.
4. Criar compose/env de producao somente depois do staging aprovado.
5. Definir protecao do admin.
6. Definir primeiras paginas SEO candidatas.
7. Implementar observabilidade minima antes da virada para producao.
