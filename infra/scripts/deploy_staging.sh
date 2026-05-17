#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${GPR_APP_DIR:-/opt/guia-produto-radar}"
ENV_FILE="${GPR_ENV_FILE:-$APP_DIR/.env.staging}"
COMPOSE_FILE="${GPR_COMPOSE_FILE:-$APP_DIR/docker-compose.staging.yml}"
BACKUP_SCRIPT="${GPR_BACKUP_SCRIPT:-$APP_DIR/infra/scripts/backup_before_deploy.sh}"

if [[ ! -d "$APP_DIR" ]]; then
  echo "Diretorio do projeto nao encontrado: $APP_DIR" >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Arquivo de ambiente nao encontrado: $ENV_FILE" >&2
  exit 1
fi

cd "$APP_DIR"

load_env_file() {
  local line key value

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" != *"="* ]] && continue

    key="${line%%=*}"
    value="${line#*=}"
    key="${key//[[:space:]]/}"

    [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue

    if [[ "$value" == \"*\" && "$value" == *\" ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "$value" == \'*\' && "$value" == *\' ]]; then
      value="${value:1:${#value}-2}"
    fi

    export "$key=$value"
  done < "$ENV_FILE"
}

load_env_file

COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")
BRANCH="${GPR_BRANCH:-$(git rev-parse --abbrev-ref HEAD)}"
HEALTH_URL="${GPR_HEALTH_URL:-http://127.0.0.1:${API_PORT:-28080}/health}"
PREVIOUS_REF="$(git rev-parse HEAD)"
ROLLBACK_ON_FAILURE="${GPR_ROLLBACK_ON_FAILURE:-1}"
RUN_TESTS="${GPR_RUN_TESTS:-0}"

require_clean_tree() {
  if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Working tree com alteracoes locais. Commit, stash ou limpe antes do deploy." >&2
    git status --short >&2
    exit 1
  fi
}

healthcheck() {
  local attempts="${1:-20}"
  local delay_seconds="${2:-3}"

  for attempt in $(seq 1 "$attempts"); do
    if curl -fsS "$HEALTH_URL" >/dev/null; then
      echo "Healthcheck OK: $HEALTH_URL"
      return 0
    fi

    echo "Aguardando API ficar saudavel ($attempt/$attempts)..."
    sleep "$delay_seconds"
  done

  return 1
}

rollback_app() {
  if [[ "$ROLLBACK_ON_FAILURE" != "1" ]]; then
    echo "Rollback automatico desativado por GPR_ROLLBACK_ON_FAILURE=$ROLLBACK_ON_FAILURE" >&2
    return 1
  fi

  echo "Tentando rollback basico para commit anterior: $PREVIOUS_REF" >&2
  git checkout --detach "$PREVIOUS_REF"
  "${COMPOSE[@]}" build
  "${COMPOSE[@]}" up -d --remove-orphans
  healthcheck 10 3 || true
  echo "Rollback de aplicacao finalizado. Verifique logs e banco manualmente." >&2
}

echo "Iniciando deploy manual de staging do Guia Produto Radar"
echo "Diretorio: $APP_DIR"
echo "Branch: $BRANCH"
echo "Healthcheck: $HEALTH_URL"

require_clean_tree

if [[ -x "$BACKUP_SCRIPT" ]]; then
  "$BACKUP_SCRIPT"
else
  bash "$BACKUP_SCRIPT"
fi

git fetch --prune origin
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

"${COMPOSE[@]}" config >/dev/null
"${COMPOSE[@]}" build

if [[ "$RUN_TESTS" == "1" ]]; then
  "${COMPOSE[@]}" run --rm --no-deps api pytest
fi

"${COMPOSE[@]}" up -d postgres redis
"${COMPOSE[@]}" run --rm api alembic upgrade head
"${COMPOSE[@]}" up -d --remove-orphans

if ! healthcheck 20 3; then
  echo "Healthcheck falhou apos deploy." >&2
  "${COMPOSE[@]}" ps >&2 || true
  "${COMPOSE[@]}" logs --tail=120 api worker >&2 || true
  rollback_app
  exit 1
fi

"${COMPOSE[@]}" ps
"${COMPOSE[@]}" logs --tail=80 api worker

echo "Deploy de staging concluido com sucesso."
