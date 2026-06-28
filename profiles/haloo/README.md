# Profile: haloo

- **项目**：Haloo · 数字人社交平台
- **类型**：C 端 / 实时社交
- **技术口径**：PostgreSQL + Redis + WebSocket；docs_layout=consolidated

## 适用场景

- 数字人 / 实时社交 / WebSocket 长连接类项目
- 文档采用 consolidated 布局（统一在 `docs/`），不再按需求拆 docs 树
- 主项目位于 `.../3dgs/haloo-3d`（PlayCanvas + 3DGS）

## 文件清单

| 文件 | 用途 |
|------|------|
| `profile.yaml` | 画像主入口 |

## 何时切到本 profile

承接 Haloo 社交模拟场景、3DGS 渲染、实时互动类需求时。
