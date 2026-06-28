# Historical Runs（历史完整运行存档）

本目录为 product-delivery-skill 的历史已完成实际运行存档，**仅供参考**。

## 重要约定

- **模型不应当作"当前任务"读取**：这里的产物已固化，对应需求都已交付完毕。
- 任何新需求请落到 `workspace/requests/<request-key>/`，由 `shared/scripts/init-request.py` 初始化。
- 若仅查看"参考样例"，请前往 `examples/sbti-red-mvp/`（精简示例，仅 5 个核心文件）。

## 当前归档

| 目录 | 性质 | 备注 |
|------|------|------|
| `sbti-red-mvp-fullrun/` | SBTI Red MVP 全量产物运行 | 与 `examples/sbti-red-mvp/`（精简版）配对参考 |
| `sbti-red-fullrun-2026-04-11/` | SBTI Red 2026-04-11 全量回归 | 含冒烟脚本 |
| `sbti-red-fullrun-2026-04-11-v2/` | 同上 v2 修订 | 含冒烟脚本 |
| `design-md-smoke/` | DESIGN.md 流程冒烟 | 仅用于回归 design 工作流 |
| `beiweite-phase1-menu-sql-20260527/` | 北京贝威通采购系统 Phase1（菜单 + SQL） | 已 RELEASED |
| `beiweite-phase2-stats-backend-20260527/` | Phase2 统计后端（占位）| 待运行 |
| `beiweite-phase2-stats-frontend-20260527/` | Phase2 统计前端（占位） | 待运行 |
| `beiweite-phase3-workbench-20260527/` | Phase3 工作台（占位）| 待运行 |
| `beiweite-phase4-5-data-polish-20260527/` | Phase4-5 数据打磨（占位）| 待运行 |

## 触发条件

仅在以下场景读取本目录：
- 用户明确要求"参考某次历史运行的产物"
- 排查 product-delivery 工作流为什么产物长成这样（取真实样本）
- 写新模板时校对历史结构

> 不要在常规交付任务中扫描或加载本目录。
