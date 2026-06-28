# Environments - sbti-red

- `local`：本地开发与联调
- `dev`：开发环境验证
- `test/uat/prod`：仅描述，不在本 skill 默认执行范围内

## 本地数据库连接（默认口径）

- JDBC：`jdbc:mysql://127.0.0.1:3306`
- 用户名：`root`
- 密码：`qierkang`
- 说明：MySQL 以 Docker 运行时，`doctor --capability db` 会优先做 TCP 检测，并在本机无 `mysql` 客户端时自动尝试 Docker 容器内登录校验。

## 本地 Redis 连接（默认口径）

- 地址：`127.0.0.1:6379`
- 密码：`qierkang`
- 说明：`doctor --capability db` 会做 Redis TCP 检测和鉴权检测；本机无 `redis-cli` 时会自动尝试 Docker 容器内检测。
