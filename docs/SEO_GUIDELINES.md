# Diretrizes de SEO

## Objetivo

Orientar a construcao do Guia Produto Radar para gerar paginas uteis, tecnicamente corretas e sustentaveis para busca organica.

O projeto deve priorizar qualidade, confiabilidade dos dados e utilidade editorial. Nao deve gerar paginas em massa sem criterio.

## Principios

- Criar conteudo para usuarios, nao apenas para indexacao.
- Priorizar long tail, comparativos e rankings uteis.
- Usar dados reais e verificaveis.
- Exibir fonte ou origem dos dados quando aplicavel.
- Mostrar data de ultima atualizacao.
- Evitar conteudo fino, repetitivo ou duplicado.
- Nao inventar preco, avaliacao, disponibilidade ou review.
- Manter WordPress leve e rapido.

## Estrutura de paginas

Cada pagina publica deve ter:

- H1 unico;
- hierarquia clara de H2 e H3;
- title unico;
- meta description objetiva;
- slug legivel;
- conteudo principal acima de elementos secundarios;
- data de ultima atualizacao;
- fonte dos dados quando aplicavel;
- chamadas para afiliado transparentes.

## Tipos de pagina planejados

### Ranking

Exemplos:

- melhores celulares custo-beneficio;
- melhores notebooks para estudar;
- melhores fones Bluetooth baratos.

Requisitos:

- criterio de ordenacao claro;
- data de atualizacao;
- origem dos dados;
- lista de produtos;
- motivo resumido para cada posicao;
- aviso quando preco ou disponibilidade nao forem confiaveis.

### Comparativo

Exemplos:

- celular A vs celular B;
- notebook gamer vs notebook para trabalho;
- Echo Dot vs Google Nest.

Requisitos:

- diferencas objetivas;
- tabela comparativa quando util;
- recomendacao por perfil de usuario;
- dados reais;
- sem inventar reviews.

### Tendencia

Exemplos:

- produtos de tecnologia em alta esta semana;
- categorias com aumento de busca;
- termos emergentes.

Requisitos:

- explicar o sinal de tendencia;
- registrar fonte;
- informar periodo analisado;
- separar dado observado de inferencia editorial.

### Guia de compra

Exemplos:

- como escolher um roteador Wi-Fi;
- o que observar antes de comprar um SSD;
- como escolher um monitor para home office.

Requisitos:

- foco educativo;
- criterios de escolha;
- erros comuns;
- perguntas frequentes;
- links internos para rankings e comparativos relacionados.

## Slugs

Slugs devem ser:

- curtos;
- legiveis;
- em minusculas;
- sem acentos;
- com hifens;
- sem parametros desnecessarios.

Exemplos:

```text
melhores-celulares-custo-beneficio
notebook-para-estudar
fone-bluetooth-barato
echo-dot-vs-google-nest
```

## Title e meta description

### Title

Deve:

- conter a palavra-chave principal;
- ser especifico;
- evitar excesso de separadores;
- nao prometer dado inexistente.

Exemplo:

```text
Melhores celulares custo-beneficio: modelos para comparar
```

### Meta description

Deve:

- resumir a utilidade da pagina;
- indicar o tipo de comparacao ou ranking;
- evitar clickbait;
- nao inventar preco ou desconto.

Exemplo:

```text
Veja criterios para comparar celulares custo-beneficio, pontos de atencao e modelos que merecem acompanhamento antes da compra.
```

## Dados estruturados

Schemas planejados:

- `Product`;
- `Review`;
- `Offer`;
- `FAQPage`;
- `BreadcrumbList`;
- `ItemList`;
- `Organization`;
- `WebSite`.

Regras obrigatorias:

- gerar JSON-LD apenas quando os dados forem reais;
- nao preencher `aggregateRating` sem avaliacao confiavel;
- nao preencher preco sem preco confiavel;
- nao preencher disponibilidade sem verificacao;
- registrar data de atualizacao;
- validar schema antes de publicar.

## Conteudo com IA

Conteudo gerado por IA deve ser tratado como rascunho.

Cada rascunho deve incluir:

- nivel de confianca;
- fontes usadas;
- limitacoes;
- campos pendentes;
- alerta de dados insuficientes quando aplicavel.

Fluxo obrigatorio:

```text
dados reais -> rascunho -> revisao humana -> publicacao
```

Nao permitir publicacao automatica.

## Links internos

O projeto deve planejar links entre:

- rankings e guias de compra;
- comparativos e produtos;
- tendencias e categorias;
- paginas long tail e paginas principais;
- posts WordPress existentes e novas paginas Radar quando fizer sentido.

Links internos devem ser contextuais e uteis.

## Afiliados

Links de afiliado devem:

- ser transparentes;
- apontar para ofertas validas quando possivel;
- nao prometer preco fixo sem verificacao;
- respeitar politicas dos marketplaces;
- ser atualizados quando houver dado confiavel.

Quando preco ou disponibilidade forem instaveis, exibir aviso.

## Performance SEO

Priorizar:

- HTML semantico;
- CSS leve;
- JavaScript minimo;
- carregamento condicional de assets;
- imagens otimizadas em WebP ou AVIF;
- lazy loading;
- cache;
- boa experiencia mobile;
- baixo tempo de resposta da API.

Evitar:

- sliders;
- pop-ups invasivos;
- bibliotecas pesadas sem necessidade;
- imagens grandes sem compressao;
- chamadas externas excessivas;
- renderizacao dependente de JavaScript para conteudo principal.

## Checklist antes de publicar uma pagina

- H1 unico;
- title definido;
- meta description definida;
- slug limpo;
- hierarquia H2/H3 revisada;
- data de atualizacao visivel;
- fontes indicadas quando aplicavel;
- schema validado ou ausente quando nao houver dados;
- links internos relevantes;
- conteudo revisado por humano;
- sem preco inventado;
- sem avaliacao inventada;
- sem disponibilidade inventada;
- pagina testada em mobile;
- carregamento rapido.

## Metricas a acompanhar

- impressoes;
- cliques;
- CTR;
- posicao media;
- paginas indexadas;
- paginas excluidas;
- tempo de carregamento;
- Core Web Vitals;
- conversao em clique afiliado;
- receita por pagina;
- paginas com queda de desempenho.

## Conteudos a evitar

- paginas quase identicas;
- rankings sem criterio;
- comparativos sem dados;
- resumos automaticos sem revisao;
- schema falso;
- promessas de desconto sem verificacao;
- conteudo que apenas replica descricoes de marketplace;
- paginas indexaveis criadas em massa sem demanda ou utilidade.
