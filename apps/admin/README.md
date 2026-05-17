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

## Limites atuais

- Sem login nesta fase.
- Briefings gerados ficam no `localStorage`.
- Ofertas e tendencias detalhadas dependem de endpoints futuros.
- Produtos ainda vêm dos endpoints mockados da API.

## Identidade visual

O admin usa os ativos salvos em `img/`:

- logo branca para sidebar;
- favicon;
- paleta inicial em azul, roxo e branco;
- suporte inicial a modo escuro via preferencia do sistema.
