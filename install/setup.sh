#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[product-delivery-skill] setup start"
mkdir -p "${ROOT_DIR}/workspace/requests"
mkdir -p "${ROOT_DIR}/governance/updates"
mkdir -p "${ROOT_DIR}/governance/decisions"
echo "[product-delivery-skill] setup done"

