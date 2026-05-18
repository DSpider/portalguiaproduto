const STORAGE_KEYS = {
  apiUrl: 'gpr_admin_api_url',
  authToken: 'gpr_admin_auth_token',
  briefings: 'gpr_admin_briefings',
};
const DEFAULT_API_URL = getDefaultApiUrl();

const state = {
  apiUrl: getInitialApiUrl(),
  adminToken: sessionStorage.getItem(STORAGE_KEYS.authToken) || '',
  authenticated: false,
  products: [],
  radar: null,
  version: null,
  adminStatus: null,
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
  await authenticateAdminSession({ silent: true });
}

async function authenticateAdminSession({ silent = false } = {}) {
  if (!silent) {
    setConnection('checking', 'Validando acesso...');
  }

  try {
    state.adminStatus = await apiGet('/api/v1/admin/status', { auth: true });
    state.authenticated = true;
    await refreshApiData();
    handleRoute();
  } catch (error) {
    state.authenticated = false;
    state.connectionOk = false;
    setConnection('error', getAuthErrorMessage(error));
    renderAuthGate(error);
  }
}

function getAuthErrorMessage(error) {
  if (error?.status === 401) return 'Login necessario';
  if (error?.status === 503) return 'Auth nao configurada';
  return 'API offline';
}

function renderAuthGate(error = null) {
  setTitle('Acesso ao admin');
  const message = error?.status === 503
    ? 'A API esta exigindo token, mas o ADMIN_API_TOKEN ainda nao foi configurado no ambiente.'
    : 'Informe a URL da API e o token administrativo para acessar o painel.';

  view.innerHTML = `
    <section class="panel auth-panel">
      <img class="auth-logo" src="/img/guia-produto-logo-color.png" alt="Guia Produto">
      <h2>Guia Produto Radar Admin</h2>
      <p class="muted">${escapeHtml(message)}</p>
      <form id="auth-form" class="stack">
        <div class="field">
          <label for="auth-api-url">URL da API</label>
          <input id="auth-api-url" name="apiUrl" type="url" value="${escapeAttr(state.apiUrl)}" placeholder="${DEFAULT_API_URL}" required>
        </div>
        <div class="field">
          <label for="admin-token">Token administrativo</label>
          <input id="admin-token" name="adminToken" type="password" value="${escapeAttr(state.adminToken)}" autocomplete="current-password" placeholder="Cole o token do ambiente">
        </div>
        <button class="button" type="submit">Entrar no painel</button>
      </form>
      <p class="muted small-note">Em local, o token pode ficar desativado. Em staging e producao, use um token forte salvo apenas no arquivo de ambiente do servidor.</p>
    </section>
  `;
}

async function authenticatedRefresh() {
  if (!state.authenticated) {
    renderAuthGate();
    return;
  }

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
  if (!state.authenticated) {
    renderAuthGate();
    return;
  }

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
          <p><strong>Auth:</strong> ${state.adminStatus?.auth_enabled ? 'token ativo' : 'desativada neste ambiente'}</p>
          <p class="muted">O token administrativo fica salvo apenas na sessao atual do navegador.</p>
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
          ${detail('Autenticacao', state.adminStatus?.auth_enabled ? 'token ativo' : 'desativada neste ambiente')}
        </div>
        <div class="field">
          <label for="settings-admin-token">Token administrativo</label>
          <input id="settings-admin-token" name="adminToken" type="password" autocomplete="current-password" placeholder="Preencha apenas para trocar o token da sessao">
        </div>
        <div>
          <button class="button" type="submit">Salvar e testar conexao</button>
          <button class="button secondary" type="button" data-action="refresh-api">Recarregar dados</button>
          <button class="button secondary" type="button" data-action="logout">Sair</button>
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
    authenticatedRefresh();
  }
  if (action === 'logout') {
    logoutAdmin();
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
  if (event.target.id === 'auth-form') {
    event.preventDefault();
    const formData = new FormData(event.target);
    state.apiUrl = normalizeApiUrl(String(formData.get('apiUrl') || DEFAULT_API_URL));
    state.adminToken = String(formData.get('adminToken') || '').trim();
    localStorage.setItem(STORAGE_KEYS.apiUrl, state.apiUrl);
    sessionStorage.setItem(STORAGE_KEYS.authToken, state.adminToken);
    authenticateAdminSession();
    return;
  }

  if (event.target.id !== 'settings-form') return;
  event.preventDefault();
  const formData = new FormData(event.target);
  state.apiUrl = normalizeApiUrl(String(formData.get('apiUrl') || DEFAULT_API_URL));
  const newToken = String(formData.get('adminToken') || '').trim();
  if (newToken) {
    state.adminToken = newToken;
    sessionStorage.setItem(STORAGE_KEYS.authToken, state.adminToken);
  }
  localStorage.setItem(STORAGE_KEYS.apiUrl, state.apiUrl);
  authenticateAdminSession();
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
    const briefing = await apiPost('/api/v1/content/briefing', payload, { auth: true });
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

async function apiGet(path, options = {}) {
  const response = await fetch(`${state.apiUrl}${path}`, {
    headers: buildHeaders(options),
  });
  if (!response.ok) throw await createApiError(response, `GET ${path} failed`);
  return response.json();
}

async function apiPost(path, payload, options = {}) {
  const response = await fetch(`${state.apiUrl}${path}`, {
    method: 'POST',
    headers: buildHeaders({ ...options, json: true }),
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw await createApiError(response, `POST ${path} failed`);
  return response.json();
}

function buildHeaders(options = {}) {
  const headers = {};
  if (options.json) headers['Content-Type'] = 'application/json';
  if (options.auth && state.adminToken) headers['X-GPR-Admin-Token'] = state.adminToken;
  return headers;
}

async function createApiError(response, fallbackMessage) {
  const error = new Error(fallbackMessage);
  error.status = response.status;
  try {
    const payload = await response.json();
    error.detail = payload.detail;
  } catch (parseError) {
    error.detail = fallbackMessage;
  }
  return error;
}

function normalizeApiUrl(value) {
  return value.replace(/\/+$/, '');
}

function getDefaultApiUrl() {
  if (window.location.protocol === 'file:' || isLocalBrowserHost()) {
    return 'http://localhost:18080';
  }

  return window.location.origin;
}

function getInitialApiUrl() {
  const storedApiUrl = localStorage.getItem(STORAGE_KEYS.apiUrl);
  if (!storedApiUrl) return DEFAULT_API_URL;

  const normalizedStoredApiUrl = normalizeApiUrl(storedApiUrl);
  if (!isLocalBrowserHost() && isLocalApiUrl(normalizedStoredApiUrl)) {
    return DEFAULT_API_URL;
  }

  return normalizedStoredApiUrl;
}

function isLocalBrowserHost() {
  return ['localhost', '127.0.0.1', ''].includes(window.location.hostname);
}

function isLocalApiUrl(value) {
  return /^https?:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/i.test(value);
}

function logoutAdmin() {
  state.adminToken = '';
  state.authenticated = false;
  state.adminStatus = null;
  sessionStorage.removeItem(STORAGE_KEYS.authToken);
  setConnection('error', 'Login necessario');
  renderAuthGate();
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
