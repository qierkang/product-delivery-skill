# 质量 Gate

> 阶段总线由 `shared/scripts/stage-gate.py` 收口。本文件把每个 Gate 的"通过条件"和"必须留下的证据"列成可对照检查表。
> 任何 Gate 未通过即视为该阶段未完成，**不允许口头放行**。

## 1. Requirement Gate

| 检查点 | 必须存在 | 验证方式 |
|--------|---------|---------|
| 需求总览 | `00-需求总览.md` | 文件存在且含目标、范围、相关方 |
| 业务规则 | `需求文档.md` | 含验收标准、边界、异常路径 |
| 机器元数据 | `manifest.json` | JSON 合法、含 `request_key` |
| 命名合规 | request 目录名 | 遵循 [naming.md](./naming.md) `kebab-case` |

**放行条件**：`stage-gate.py --stage requirement` 退出码 0 且 `missing=[]`。

## 2. Design Gate

| 检查点 | 必须存在 |
|--------|---------|
| AI 可读设计基线 | `DESIGN.md`（含风格方向、token、组件策略、动效） |
| 技术方案 | `技术方案.md`（架构、数据、接口、回滚） |
| UI 规范 | `UI交互设计规范.md`（页面、状态、端差异） |
| 任务拆分 | `任务分解.md`（含责任与依赖） |

**放行条件**：`stage-gate.py --stage design` 通过 + 设计基线在 UI 阶段可独立读懂。

## 3. Dev Gate

| 检查点 | 必须存在 |
|--------|---------|
| 实现追踪 | `实现控制总表.md`（需求→实现一一映射） |
| 页面接口映射 | `页面接口验收总表.md` |
| 自测放行 | `开发放行报告.md` |
| 测试覆盖证据 | `覆盖率报告.md` |
| 前端关键链路 | `前端关键流程覆盖清单.md`（前端项目必填） |

**放行条件**：通过 stage-gate + 单元 / 集成测试有真实运行日志（截图或 stdout）。

## 4. Review Gate

| 检查点 | 通过条件 |
|--------|---------|
| `代码审查报告.md` | 无阻塞级（CRITICAL/HIGH）问题 |
| 必要时含"采纳/拒绝"说明 | 拒绝项必须给理由 |
| 关键安全 / 性能问题 | 已修复或转入下次迭代且记入风险表 |

## 5. Smoke Gate

| 检查点 | 必须存在 |
|--------|---------|
| 可重复执行的 `冒烟测试脚本.sh` | 干净环境一键运行 |
| `冒烟测试报告.md` | 含运行日志、关键链路截图 |

**放行条件**：脚本退出码 0；接口和页面主链路通过。

## 6. QA Gate

- 功能、边界、数据、权限场景全部覆盖
- `测试用例.md` 含正向 / 反向 / 异常用例
- `QA验收报告.md` 给出 PASS / FAIL 结论 + 缺陷收口状态

## 7. UI Acceptance Gate

- 视觉、交互、token、动效、响应式、可访问性逐项核对
- `UI验收报告.md` 含还原度评分 + 截图对比

## 8. Product Acceptance Gate

- 业务范围、流程边界、目标指标全部确认
- `产品验收报告.md` 由产品角色签字（默认 `xyqierkang@gmail（claude+codex）`）

## 9. Release Gate

| 检查点 | 必须存在 |
|--------|---------|
| 发布记录 | `发布记录.md`（版本号、变更摘要） |
| 回滚预案 | 写在 `技术方案.md` 或 `发布记录.md` |
| 发布后验证 | 至少一次冒烟回归 + 日志归档 |
| 状态机回写 | `stage-status.json` `current_stage=release, status=PASSED` |

## 一键全量校验

```bash
python3 shared/scripts/stage-gate.py --request-dir <request-dir> --stage all
```

输出 JSON 包含 `pass / missing / issues`，CI 应基于此判定。

## 不通过时的回流路径

- `missing` 列出的产物：直接补对应模板，参考 [artifact-standard.md](./artifact-standard.md)
- `issues` 列出的问题：在对应阶段产物里加"修复记录"段并重跑 Gate
- 反复失败超过 3 次：在 `governance/updates/` 写一条根因记录
