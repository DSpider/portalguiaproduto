# Guia Produto Radar Admin

Admin interno inicial, leve e sem framework, para uso local.

## Telas

- Dashboard;
- Produtos;
- Produto detalhe;
- Briefings;
- Configuracoes.

## Como rodar no Windows

Suba a API primeiro:

```powershell
cd C:\gp_projects\portalguiaproduto
docker compose up --build
```

Em outro terminal, rode o admin a partir da raiz do repositorio para que a pasta `img/` tambem seja servida:

```powershell
cd C:\gp_projects\portalguiaproduto
python -m http.server 18090
```

Acesse:

```text
http://localhost:18090/apps/admin/
```

## Configuracao

Na tela `Configuracoes`, informe a URL da API:

```text
http://localhost:18080
```

O valor fica salvo no `localStorage` do navegador.

## Autenticacao

O admin valida acesso em:

```text
GET /api/v1/admin/status
```

Em local, a autenticacao pode ficar desativada com:

```text
ADMIN_AUTH_ENABLED=false
```

Em staging e producao, use:

```text
ADMIN_AUTH_ENABLED=true
ADMIN_API_TOKEN=valor-gerado-no-servidor
```

O token deve ser gerado fora do Git. Na VPS, use:

```bash
openssl rand -hex 32
```

O painel salva o token apenas no `sessionStorage`, ou seja, ele dura somente enquanto a sessao do navegador estiver aberta.

## Limites atuais

- Autenticacao simples por token administrativo.
- Briefings gerados ficam no `localStorage`.
- Ofertas e tendencias detalhadas dependem de endpoints futuros.
- Produtos ainda vêm dos endpoints mockados da API.

## Identidade visual

O admin usa os ativos salvos em `img/`:

- logo branca para sidebar;
- favicon;
- paleta inicial em azul, roxo e branco;
- suporte inicial a modo escuro via preferencia do sistema.
