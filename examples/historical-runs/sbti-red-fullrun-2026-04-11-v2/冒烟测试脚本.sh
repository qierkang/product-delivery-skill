#!/usr/bin/env bash
set -euo pipefail

# 冒烟测试脚本模板
# 用法：bash 冒烟测试脚本.sh

echo "[smoke] health check"
# curl -fS http://127.0.0.1:3000/health

echo "[smoke] api check"
# curl -fS http://127.0.0.1:3000/api/xxx

echo "[smoke] done"
