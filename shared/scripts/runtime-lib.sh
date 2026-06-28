#!/usr/bin/env bash
set -euo pipefail

wait_for_http() {
  local url="$1"
  local retry="${2:-30}"
  local sleep_sec="${3:-1}"
  for ((i=1; i<=retry; i++)); do
    if curl -fsS "${url}" >/dev/null 2>&1; then
      echo "[runtime] ready: ${url}"
      return 0
    fi
    sleep "${sleep_sec}"
  done
  echo "[runtime] timeout: ${url}" >&2
  return 1
}

