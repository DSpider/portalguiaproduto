# Seguranca

## Objetivo

Definir controles minimos de seguranca para o Guia Produto Radar desde o inicio do projeto.

O foco principal e proteger credenciais, impedir publicacao automatica indevida, validar entradas, escapar saidas e reduzir risco na integracao entre API, worker, WordPress e marketplaces.

## Segredos e credenciais

Nunca versionar:

- senhas;
- tokens;
- chaves de API;
- cookies;
- credenciais WordPress;
- credenciais de banco;
- credenciais de marketplaces;
- arquivos `.env` reais.

O repositorio deve manter apenas `.env.example`, com nomes de variaveis e valores ficticios ou vazios.

## Variaveis de ambiente

Credenciais devem ser lidas por variaveis de ambiente.

Categorias planejadas:

- banco de dados;
- Redis;
- token interno entre WordPress e API;
- credenciais de marketplaces;
- configuracoes de IA;
- chaves de observabilidade.

Nenhuma credencial deve aparecer em:

- commits;
- logs;
- mensagens de erro exibidas ao usuario;
- paginas publicas;
- screenshots de documentacao.

## API

### Entradas

Todas as entradas devem ser validadas com Pydantic ou mecanismo equivalente.

Validar:

- tipos;
- tamanho maximo;
- campos obrigatorios;
- slugs;
- URLs;
- identificadores externos;
- parametros de paginacao;
- filtros.

### Autenticacao

Endpoints que alteram dados devem exigir autenticacao.

Exemplos:

- criar produto;
- editar produto;
- recalcular score;
- criar rascunho;
- aprovar pagina;
- atualizar oferta;
- disparar job.

Endpoints publicos de leitura devem retornar apenas dados seguros e cacheaveis.

Nesta fase, o admin interno usa autenticacao simples por token:

- `ADMIN_AUTH_ENABLED=false` em desenvolvimento local por padrao;
- `ADMIN_AUTH_ENABLED=true` em staging e producao;
- `ADMIN_API_TOKEN` gerado no servidor e nunca versionado;
- API aceita token por `Authorization: Bearer ...` ou `X-GPR-Admin-Token`;
- o admin interno usa `X-GPR-Admin-Token` para nao conflitar com Basic Auth ou Cloudflare Access;
- validacao em tempo constante para reduzir vazamento por timing;
- retorno `503` quando a autenticacao esta ativa, mas o token nao foi configurado.

Rotas protegidas nesta fase:

- `GET /api/v1/admin/status`;
- `POST /api/v1/content/briefing`, quando `ADMIN_AUTH_ENABLED=true`.

O painel admin salva o token apenas no `sessionStorage` do navegador. Nao salvar token administrativo em `localStorage`, HTML, JavaScript versionado ou documentacao.

### Autorizacao

Separar permissoes futuras por perfil:

- leitura publica;
- operador editorial;
- administrador;
- worker interno;
- integracao WordPress.

### Erros

Erros devem ser sanitizados.

Nao retornar:

- stack trace em producao;
- string de conexao;
- tokens;
- payloads sensiveis;
- detalhes internos de marketplace.

## Worker

O worker deve:

- usar filas controladas;
- limitar retentativas;
- registrar falhas sem expor segredos;
- tratar timeouts;
- evitar jobs longos sem controle;
- nao executar publicacao automatica em producao.

Jobs que acessam servicos externos devem respeitar limites de taxa e politicas de uso.

## WordPress

O plugin deve seguir praticas de seguranca do WordPress:

- prefixar funcoes com `gp_`;
- sanitizar atributos de shortcode;
- escapar HTML com funcoes apropriadas;
- validar URLs;
- usar transients para cache;
- carregar assets somente quando necessario;
- nao depender do Elementor;
- nao quebrar o tema atual;
- exibir fallback quando a API estiver fora.

Funcoes esperadas:

- `sanitize_text_field`;
- `sanitize_key`;
- `esc_html`;
- `esc_attr`;
- `esc_url`;
- `wp_kses_post` quando HTML controlado for necessario.

## Conteudo gerado por IA

IA deve gerar rascunhos, nao publicacoes finais.

Todo rascunho deve conter:

- nivel de confianca;
- fontes usadas;
- limitacoes;
- campos pendentes de revisao;
- alerta de dados insuficientes quando aplicavel.

Nao permitir:

- publicacao automatica sem revisao humana;
- inventar preco;
- inventar avaliacao;
- inventar disponibilidade;
- inventar fonte;
- criar schema falso.

## Marketplaces e afiliados

Integracoes devem usar APIs oficiais quando possivel.

Cuidados obrigatorios:

- armazenar credenciais fora do repositorio;
- respeitar termos de uso;
- registrar origem dos dados;
- atualizar disponibilidade e preco com data de verificacao;
- nao exibir preco sem confianca;
- nao mascarar links de forma enganosa.

## Banco de dados

Controles planejados:

- usuario de banco com permissoes limitadas;
- migrations versionadas;
- indices para consultas frequentes;
- timestamps;
- campos de origem;
- backups em staging e producao;
- ausencia de dados sensiveis desnecessarios.

## Logs

Logs podem conter:

- rota;
- status HTTP;
- tempo de resposta;
- identificador interno;
- erro sanitizado;
- status de job.

Logs nao devem conter:

- tokens;
- senhas;
- cookies;
- payload integral de credenciais;
- dados pessoais desnecessarios;
- chaves de afiliado completas.

## Checklist antes de staging

- `.env` real fora do git;
- `.env.example` atualizado;
- endpoints de escrita autenticados;
- CORS restrito;
- logs sanitizados;
- healthcheck sem dados sensiveis;
- migrations revisadas;
- testes basicos executados;
- plugin escapando saidas;
- plugin com fallback de API;
- sem publicacao automatica.

## Checklist antes de producao

- staging validado;
- backup configurado;
- HTTPS ativo;
- secrets configurados no ambiente;
- rate limit definido para endpoints sensiveis;
- monitoramento basico ativo;
- revisao de seguranca do plugin;
- revisao de performance;
- revisao manual do fluxo de conteudo;
- plano de rollback documentado.

## Fora de escopo por enquanto

- pentest completo;
- WAF dedicado;
- SSO;
- RBAC avancado;
- automacao de deploy em producao;
- rotacao automatica de segredos.

Esses itens devem ser avaliados depois que a base funcional estiver estavel.
