const DEFAULT_API_URL = 'http://localhost:18080';
const STORAGE_KEYS = {
  apiUrl: 'gpr_admin_api_url',
  briefings: 'gpr_admin_briefings',
};

const state = {
  apiUrl: localStorage.getItem(STORAGE_KEYS.apiUrl) || DEFAULT_API_URL,
  products: [],
  radar: null,
  version: null,
  connectionOk: false,
};

const view = document.querySelector('#view');
const pageTitle = document.querySelector('#page-title');
const connectionStatus = document.querySelector('#connection-status');
const jsonDialog = document.querySelector('#json-dialog');
const jsonOutput = document.querySelector('#json-output');

const routes = {
  dashboard: renderDashboard,
  produtos: renderProducts,
  briefings: renderBriefings,
  configuracoes: renderSettings,
};

window.addEventListener('hashchange', handleRoute);
document.addEventListener('click', handleDocumentClick);
document.addEventListener('submit', handleSubmit);

init();

async function init() {
  await refreshApiData();
  handleRoute();
}

async function refreshApiData() {
  setConnection('checking', 'Verificando API...');

  try {
    const [health, version, radar, products] = await Promise.all([
      apiGet('/health'),
      apiGet('/version'),
      apiGet('/api/v1/radar/summary'),
      apiGet('/api/v1/products'),
    ]);

    state.version = version;
    state.radar = radar;
    state.products = products;
    state.connectionOk = true;
    setConnection('ok', `API online: ${health.environment}`);
  } catch (error) {
    state.connectionOk = false;
    setConnection('error', 'API offline');
  }
}

function handleRoute() {
  const rawHash = window.location.hash.replace('#', '') || 'dashboard';
  const [route, param] = rawHash.split('/');

  document.querySelectorAll('.nav a').forEach((link) => {
    link.classList.toggle('active', link.dataset.route === route);
  });

  if (route === 'produto' && param) {
    renderProductDetail(param);
    return;
  }

  const renderer = routes[route] || routes.dashboard;
  renderer();
}

function setTitle(title) {
  pageTitle.textContent = title;
}

function setConnection(status, text) {
  connectionStatus.textContent = text;
  connectionStatus.className = 'connection';
  if (status === 'ok') connectionStatus.classList.add('is-ok');
  if (status === 'error') connectionStatus.classList.add('is-error');
}

function renderDashboard() {
  setTitle('Dashboard');
  const briefings = getStoredBriefings();
  const products = state.products || [];
  const topProducts = [...products].sort((a, b) => b.trend_score - a.trend_score).slice(0, 5);

  view.innerHTML = `
    <div class="grid metrics">
      ${metric('Total de produtos', products.length)}
      ${metric('Produtos monitorados', state.radar?.total_products ?? products.length)}
      ${metric('Paginas SEO em rascunho', briefings.length)}
      ${metric('Maior score', topProducts[0]?.trend_score ?? 0)}
    </div>
    <div class="grid two" style="margin-top: 16px;">
      <section class="panel">
        <h2>Produtos com maior score</h2>
        ${renderProductsTable(topProducts, false)}
      </section>
      <section class="panel">
        <h2>Status operacional</h2>
        <div class="stack">
          <p><strong>API:</strong> ${escapeHtml(state.apiUrl)}</p>
          <p><strong>Ambiente:</strong> ${escapeHtml(state.version?.environment || 'indisponivel')}</p>
          <p><strong>Versao:</strong> ${escapeHtml(state.version?.version || 'indisponivel')}</p>
          <p class="muted">Admin local sem autenticacao. Preparado para auth futura.</p>
        </div>
      </section>
    </div>
  `;
}

function renderProducts() {
  setTitle('Produtos');
  const products = state.products || [];
  const categories = uniqueValues(products.map((product) => product.category));
  const statuses = ['mock', 'draft', 'active', 'monitorar'];

  view.innerHTML = `
    <section class="panel">
      <div class="toolbar">
        <div class="field">
          <label for="product-search">Busca</label>
          <input id="product-search" data-filter="search" type="search" placeholder="Nome, marca ou slug">
        </div>
        <div class="field">
          <label for="category-filter">Categoria</label>
          <select id="category-filter" data-filter="category">
            <option value="">Todas</option>
            ${categories.map((category) => `<option value="${escapeAttr(category)}">${escapeHtml(category)}</option>`).join('')}
          </select>
        </div>
        <div class="field">
          <label for="status-filter">Status</label>
          <select id="status-filter" data-filter="status">
            <option value="">Todos</option>
            ${statuses.map((status) => `<option value="${escapeAttr(status)}">${escapeHtml(status)}</option>`).join('')}
          </select>
        </div>
      </div>
      <div id="products-table">${renderProductsTable(products, true)}</div>
    </section>
  `;

  document.querySelectorAll('[data-filter]').forEach((field) => {
    field.addEventListener('input', updateProductFilters);
  });
}

function updateProductFilters() {
  const search = document.querySelector('[data-filter="search"]').value.toLowerCase().trim();
  const category = document.querySelector('[data-filter="category"]').value;
  const status = document.querySelector('[data-filter="status"]').value;
  const filtered = state.products.filter((product) => {
    const text = `${product.name} ${product.brand} ${product.slug}`.toLowerCase();
    const statusValue = product.confidence || 'mock';
    return (!search || text.includes(search))
      && (!category || product.category === category)
      && (!status || statusValue === status);
  });

  document.querySelector('#products-table').innerHTML = renderProductsTable(filtered, true);
}

async function renderProductDetail(slug) {
  setTitle('Produto detalhe');
  view.innerHTML = '<section class="panel"><p>Carregando produto...</p></section>';

  try {
    const product = await apiGet(`/api/v1/products/${encodeURIComponent(slug)}`);
    const recommendation = product.trend_score >= 75
      ? 'Priorizar criacao ou atualizacao'
      : product.trend_score >= 50
        ? 'Monitorar e revisar oportunidade'
        : 'Aguardar novos sinais';

    view.innerHTML = `
      <div class="grid two">
        <section class="panel">
          <h2>${escapeHtml(product.name)}</h2>
          <div class="detail-list">
            ${detail('Slug', product.slug)}
            ${detail('Marca', product.brand)}
            ${detail('Categoria', product.category)}
            ${detail('Score', product.trend_score)}
            ${detail('Confianca', product.confidence)}
            ${detail('Ultima atualizacao', product.last_updated)}
          </div>
          <p style="margin-top: 16px;">${escapeHtml(product.summary)}</p>
          <button class="button" data-action="generate-briefing" data-slug="${escapeAttr(product.slug)}">Gerar briefing rascunho</button>
        </section>
        <section class="panel">
          <h2>Score e recomendacao</h2>
          <p class="score">${escapeHtml(String(product.trend_score))}/100</p>
          <p>${escapeHtml(recommendation)}</p>
          <h3>Ofertas</h3>
          <p class="muted">Ainda nao ha endpoint de ofertas. A integracao sera conectada ao banco/API em fase futura.</p>
          <h3>Tendencias</h3>
          <p class="muted">Resumo disponivel via Radar; historico detalhado depende dos snapshots reais.</p>
        </section>
      </div>
    `;
  } catch (error) {
    view.innerHTML = `<section class="panel"><p class="empty">Produto nao encontrado ou API indisponivel.</p></section>`;
  }
}

function renderBriefings() {
  setTitle('Briefings');
  const briefings = getStoredBriefings();

  view.innerHTML = `
    <section class="panel">
      <div class="topbar-like">
        <h2>Rascunhos editoriais</h2>
        <button class="button" data-action="generate-demo-briefing">Gerar briefing demo</button>
      </div>
      ${briefings.length ? renderBriefingsTable(briefings) : '<p class="empty">Nenhum briefing salvo localmente. Gere um rascunho a partir de um produto ou pelo botao demo.</p>'}
    </section>
  `;
}

function renderSettings() {
  setTitle('Configuracoes');
  view.innerHTML = `
    <section class="panel">
      <form id="settings-form" class="stack">
        <div class="field">
          <label for="api-url">URL da API</label>
          <input id="api-url" name="apiUrl" type="url" value="${escapeAttr(state.apiUrl)}" placeholder="${DEFAULT_API_URL}">
        </div>
        <div class="detail-list">
          ${detail('Ambiente', state.version?.environment || 'indisponivel')}
          ${detail('Versao da API', state.version?.version || 'indisponivel')}
          ${detail('Status de conexao', state.connectionOk ? 'online' : 'offline')}
          ${detail('Autenticacao', 'pendente para fase futura')}
        </div>
        <div>
          <button class="button" type="submit">Salvar e testar conexao</button>
          <button class="button secondary" type="button" data-action="refresh-api">Recarregar dados</button>
        </div>
      </form>
    </section>
  `;
}

function renderProductsTable(products, clickable) {
  if (!products.length) {
    return '<p class="empty">Nenhum produto encontrado.</p>';
  }

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Produto</th>
            <th>Categoria</th>
            <th>Status</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          ${products.map((product) => `
            <tr class="${clickable ? 'clickable' : ''}" ${clickable ? `data-href="#produto/${escapeAttr(product.slug)}"` : ''}>
              <td>
                <strong>${escapeHtml(product.name)}</strong><br>
                <span class="muted">${escapeHtml(product.brand || '')}</span>
              </td>
              <td><span class="pill">${escapeHtml(product.category)}</span></td>
              <td>${escapeHtml(product.confidence || 'mock')}</td>
              <td><span class="score">${escapeHtml(String(product.trend_score))}</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

function renderBriefingsTable(briefings) {
  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Titulo SEO</th>
            <th>Status</th>
            <th>Confianca</th>
            <th>Alertas</th>
            <th>JSON</th>
          </tr>
        </thead>
        <tbody>
          ${briefings.map((briefing, index) => `
            <tr>
              <td><strong>${escapeHtml(briefing.title_seo)}</strong><br><span class="muted">${escapeHtml(briefing.slug)}</span></td>
              <td>rascunho</td>
              <td>${escapeHtml(briefing.nivel_de_confianca)}</td>
              <td>${escapeHtml(String(briefing.alertas_de_revisao?.length || 0))}</td>
              <td><button class="button secondary" data-action="show-json" data-index="${index}">Visualizar</button></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

function handleDocumentClick(event) {
  const row = event.target.closest('[data-href]');
  if (row) {
    window.location.hash = row.dataset.href;
    return;
  }

  const actionTarget = event.target.closest('[data-action]');
  if (!actionTarget) return;

  const { action } = actionTarget.dataset;
  if (action === 'refresh-api') {
    refreshApiData().then(handleRoute);
  }
  if (action === 'generate-demo-briefing') {
    generateBriefingForProduct(state.products[0]);
  }
  if (action === 'generate-briefing') {
    const product = state.products.find((item) => item.slug === actionTarget.dataset.slug);
    generateBriefingForProduct(product);
  }
  if (action === 'show-json') {
    const briefing = getStoredBriefings()[Number(actionTarget.dataset.index)];
    showJson(briefing);
  }
}

function handleSubmit(event) {
  if (event.target.id !== 'settings-form') return;
  event.preventDefault();
  const formData = new FormData(event.target);
  state.apiUrl = String(formData.get('apiUrl') || DEFAULT_API_URL).replace(/\/+$/, '');
  localStorage.setItem(STORAGE_KEYS.apiUrl, state.apiUrl);
  refreshApiData().then(handleRoute);
}

async function generateBriefingForProduct(product) {
  if (!product) return;

  const payload = {
    produto: {
      name: product.name,
      brand: product.brand,
      description: 'Rascunho local gerado a partir dos dados mockados da API.',
      updated_at: new Date().toISOString().slice(0, 10),
      ficha_tecnica: {},
      tested_by_guia_produto: false,
    },
    categoria: product.category,
    palavra_chave_principal: product.name,
    palavras_chave_secundarias: [product.category],
    tendencia: {
      trend_growth_percent: product.trend_score,
      source_name: 'mock',
    },
    ofertas_disponiveis: [],
    dados_de_avaliacao: {
      source_is_reliable: false,
    },
    concorrentes: [],
    score_calculado: {
      score_total: product.trend_score,
      score_confidence: product.trend_score,
      recommendation: product.trend_score >= 75 ? 'criar_pagina' : 'monitorar',
    },
  };

  try {
    const briefing = await apiPost('/api/v1/content/briefing', payload);
    const briefings = getStoredBriefings();
    briefings.unshift({ ...briefing, created_at: new Date().toISOString() });
    localStorage.setItem(STORAGE_KEYS.briefings, JSON.stringify(briefings.slice(0, 25)));
    window.location.hash = '#briefings';
    renderBriefings();
  } catch (error) {
    alert('Nao foi possivel gerar o briefing. Verifique a conexao com a API.');
  }
}

function showJson(value) {
  jsonOutput.textContent = JSON.stringify(value, null, 2);
  jsonDialog.showModal();
}

function getStoredBriefings() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.briefings) || '[]');
  } catch (error) {
    return [];
  }
}

async function apiGet(path) {
  const response = await fetch(`${state.apiUrl}${path}`);
  if (!response.ok) throw new Error(`GET ${path} failed`);
  return response.json();
}

async function apiPost(path, payload) {
  const response = await fetch(`${state.apiUrl}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(`POST ${path} failed`);
  return response.json();
}

function metric(label, value) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value))}</strong></div>`;
}

function detail(label, value) {
  return `<div><span>${escapeHtml(label)}</span><strong>${escapeHtml(String(value || '-'))}</strong></div>`;
}

function uniqueValues(values) {
  return [...new Set(values.filter(Boolean))].sort();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function escapeAttr(value) {
  return escapeHtml(value);
}
