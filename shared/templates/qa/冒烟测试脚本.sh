#!/usr/bin/env bash
set -euo pipefail

# 冒烟测试脚本模板
# 用法：bash 冒烟测试脚本.sh
# 默认按两关执行：
# 1. API 健康检查
# 2. 页面主链路检查

echo "[smoke] health check"
# curl -fS http://127.0.0.1:3000/health
# curl -fS http://127.0.0.1:3000/api/health

echo "[smoke] api check"
# curl -fS http://127.0.0.1:3000/api/xxx

echo "[smoke] page check"
# 浏览器自动化 / curl / 其他页面验证脚本
# 需要登录时先补 token / cookie 获取步骤

echo "[smoke] done"
