#!/usr/bin/env bash
set -euo pipefail

CAPABILITY="docs"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --capability)
      CAPABILITY="${2:-docs}"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

echo "[doctor] capability=${CAPABILITY}"

DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD:-qierkang}"
DB_NAME="${DB_NAME:-}"
DB_JDBC_URL="${DB_JDBC_URL:-jdbc:mysql://${DB_HOST}:${DB_PORT}/}"
REDIS_HOST="${REDIS_HOST:-127.0.0.1}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_PASSWORD="${REDIS_PASSWORD:-qierkang}"

check_cmd() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "[doctor][FAIL] missing command: ${cmd}" >&2
    exit 2
  fi
}

check_tcp_port() {
  local host="$1"
  local port="$2"
  python3 - "$host" "$port" <<'PY'
import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)
try:
    sock.connect((host, port))
except Exception as exc:  # noqa: BLE001
    print(f"[doctor][FAIL] tcp connect failed: {host}:{port} ({exc})", file=sys.stderr)
    sys.exit(2)
finally:
    sock.close()

print(f"[doctor][PASS] tcp connect: {host}:{port}")
PY
}

check_mysql_login() {
  local -a mysql_args
  mysql_args=(--connect-timeout=5 -h "${DB_HOST}" -P "${DB_PORT}" -u "${DB_USER}")
  if [[ -n "${DB_NAME}" ]]; then
    mysql_args+=(-D "${DB_NAME}")
  fi
  if MYSQL_PWD="${DB_PASSWORD}" mysql "${mysql_args[@]}" -e "SELECT 1;" >/dev/null 2>&1; then
    echo "[doctor][PASS] mysql auth: ${DB_USER}@${DB_HOST}:${DB_PORT}"
    return 0
  fi
  echo "[doctor][FAIL] mysql auth failed: ${DB_USER}@${DB_HOST}:${DB_PORT}" >&2
  return 2
}

check_mysql_login_via_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    return 1
  fi
  local container_name
  container_name="$(docker ps --format '{{.Names}} {{.Image}}' | awk 'tolower($0) ~ /mysql|mariadb/ {print $1; exit}')"
  if [[ -z "${container_name}" ]]; then
    return 1
  fi
  if docker exec "${container_name}" sh -lc \
    "mysql -h${DB_HOST} -P${DB_PORT} -u${DB_USER} -p${DB_PASSWORD} -e 'SELECT 1;'" >/dev/null 2>&1; then
    echo "[doctor][PASS] mysql auth via docker: ${container_name} (${DB_USER}@${DB_HOST}:${DB_PORT})"
    return 0
  fi
  echo "[doctor][FAIL] mysql auth via docker failed: ${container_name} (${DB_USER}@${DB_HOST}:${DB_PORT})" >&2
  return 2
}

check_redis_auth() {
  if redis-cli -h "${REDIS_HOST}" -p "${REDIS_PORT}" -a "${REDIS_PASSWORD}" ping 2>/dev/null | grep -q "PONG"; then
    echo "[doctor][PASS] redis auth: ${REDIS_HOST}:${REDIS_PORT}"
    return 0
  fi
  echo "[doctor][FAIL] redis auth failed: ${REDIS_HOST}:${REDIS_PORT}" >&2
  return 2
}

check_redis_auth_via_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    return 1
  fi
  local container_name
  container_name="$(docker ps --format '{{.Names}} {{.Image}}' | awk 'tolower($0) ~ /redis/ {print $1; exit}')"
  if [[ -z "${container_name}" ]]; then
    return 1
  fi
  if docker exec "${container_name}" sh -lc \
    "redis-cli -h ${REDIS_HOST} -p ${REDIS_PORT} -a ${REDIS_PASSWORD} ping" 2>/dev/null | grep -q "PONG"; then
    echo "[doctor][PASS] redis auth via docker: ${container_name} (${REDIS_HOST}:${REDIS_PORT})"
    return 0
  fi
  echo "[doctor][FAIL] redis auth via docker failed: ${container_name} (${REDIS_HOST}:${REDIS_PORT})" >&2
  return 2
}

case "${CAPABILITY}" in
  docs)
    check_cmd python3
    ;;
  dev)
    check_cmd python3
    check_cmd git
    check_cmd node
    check_cmd npm
    ;;
  db)
    check_cmd python3
    echo "[doctor] mysql jdbc=${DB_JDBC_URL}"
    check_tcp_port "${DB_HOST}" "${DB_PORT}"
    if command -v mysql >/dev/null 2>&1; then
      check_mysql_login
    else
      echo "[doctor][WARN] missing mysql client, trying docker fallback auth check"
      if ! check_mysql_login_via_docker; then
        rc=$?
        if [[ ${rc} -eq 1 ]]; then
          echo "[doctor][WARN] mysql auth check skipped (no mysql client and docker fallback unavailable)"
        else
          exit 2
        fi
      fi
    fi
    echo "[doctor] redis addr=${REDIS_HOST}:${REDIS_PORT}"
    check_tcp_port "${REDIS_HOST}" "${REDIS_PORT}"
    if command -v redis-cli >/dev/null 2>&1; then
      check_redis_auth
    else
      echo "[doctor][WARN] missing redis-cli, trying docker fallback auth check"
      if ! check_redis_auth_via_docker; then
        rc=$?
        if [[ ${rc} -eq 1 ]]; then
          echo "[doctor][WARN] redis auth check skipped (no redis-cli and docker fallback unavailable)"
        else
          exit 2
        fi
      fi
    fi
    ;;
  deploy)
    check_cmd python3
    check_cmd docker
    ;;
  *)
    echo "[doctor][FAIL] unsupported capability: ${CAPABILITY}" >&2
    exit 3
    ;;
esac

echo "[doctor][PASS] ${CAPABILITY}"
