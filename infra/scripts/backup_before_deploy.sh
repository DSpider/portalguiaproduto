#!/usr/bin/env bash
set -Eeuo pipefail

APP_DIR="${GPR_APP_DIR:-/opt/guia-produto-radar}"
ENV_FILE="${GPR_ENV_FILE:-$APP_DIR/.env.staging}"
COMPOSE_FILE="${GPR_COMPOSE_FILE:-$APP_DIR/docker-compose.staging.yml}"

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

BACKUP_DIR="${GPR_BACKUP_DIR:-$APP_DIR/backups/staging}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_PATH="$BACKUP_DIR/$TIMESTAMP"
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE")

mkdir -p "$BACKUP_PATH"
chmod 700 "$BACKUP_DIR" "$BACKUP_PATH"

echo "Criando backup pre-deploy em $BACKUP_PATH"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git rev-parse HEAD > "$BACKUP_PATH/git_ref.txt"
  git status --short > "$BACKUP_PATH/git_status.txt"
fi

cp "$ENV_FILE" "$BACKUP_PATH/env.staging.backup"
chmod 600 "$BACKUP_PATH/env.staging.backup"

if "${COMPOSE[@]}" ps --services --filter "status=running" | grep -qx "postgres"; then
  "${COMPOSE[@]}" exec -T postgres pg_dump \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    -Fc > "$BACKUP_PATH/postgres.dump"
  chmod 600 "$BACKUP_PATH/postgres.dump"
  echo "Backup PostgreSQL criado: $BACKUP_PATH/postgres.dump"
else
  echo "PostgreSQL nao esta rodando; backup do banco foi ignorado." >&2
fi

cat > "$BACKUP_PATH/manifest.txt" <<EOF
Guia Produto Radar - backup pre-deploy staging
Data UTC: $TIMESTAMP
App dir: $APP_DIR
Compose file: $COMPOSE_FILE
Env file: $ENV_FILE
Banco: ${POSTGRES_DB}
EOF

echo "Backup pre-deploy concluido."
