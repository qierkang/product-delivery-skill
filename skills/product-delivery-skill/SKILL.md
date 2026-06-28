---
name: product-delivery-skill-main
description: Use when 需要用统一流程推进产品项目，从需求、方案、开发、验证到发布形成完整证据链，并可按 profile 适配不同业务。
version: 0.2.0
---

# Product Delivery Main

## 定位

通用产品交付主入口。把任务路由到标准流程，不跳过流程直接写实现。

## 必读（3 项，先读这些）

1. `../../README.md` — 项目概述、目录、快速开始
2. `../../shared/templates/README.md` — 21 项标准产物模板入口
3. `../../shared/references/quality-gates.md` — 阶段 Gate 总览

## 按需阅读（按触发条件加载，不要预先全读）

| # | 文件 | 触发条件 |
|---|------|---------|
| 1 | `../../shared/references/naming.md` | 创建新 request 或确定文件命名时 |
| 2 | `../../shared/references/artifact-standard.md` | 起草 / 校对产物结构时 |
| 3 | `../../shared/references/requirement-writing-rules.md` | **编写需求文档前必读** |
| 4 | `../../shared/references/design-baseline.md` | UI 阶段且运行端无 `ui-ux-pro-max` 时 |
| 5 | `../../skills/product-delivery-methods/references/code-simplicity.md` | 进入 Dev / Review 阶段，涉及新代码 / 依赖 / 重构 |

## Workflow 路由（按 request 类型挑一个进入）

- 新项目初始化 → `../../shared/workflow/new-project.md`
- 新需求 → `../../shared/workflow/new-feature.md`
- 需求变更 → `../../shared/workflow/change-request.md`
- Bug 修复 → `../../shared/workflow/bugfix.md`
- 增长实验 → `../../shared/workflow/growth-campaign.md`
- README 开源发布 → `../../shared/workflow/open-source-readme.md`

## 阶段规则

1. `doctor` 先行：`docs/dev/db/deploy`
2. 产物先行：见 `../../shared/templates/README.md` 的 21 项清单
3. Gate 先行：`Requirement → Design → Dev → Review → Smoke → QA → UI Acceptance → Product Acceptance → Release`
4. 证据先行：无日志、无截图、无测试记录、无回流说明 = 未完成
5. QA 阶段强制拆成三份独立产物：`QA验收报告.md` / `UI验收报告.md` / `产品验收报告.md`
6. 涉及菜单、字典、SQL、页面接口映射时，补 `shared/templates/config/` 与 `shared/templates/ui/page-api-mapping.md`

## UI 设计回退规则

进入 `UI方案` 或 `UI验收` 阶段：

1. 优先识别 `ui-ux-pro-max`，借助它补设计基线或做审查
2. 不可识别时回退到 `../../shared/references/design-baseline.md`
3. **不**得用 `frontend-design` 等通用 skill 充当 `ui-ux-pro-max` 的兜底
4. 最终都必须落回本仓模板与 Gate

## README 门禁

涉及 README 生成 / 改写 / 开源发布：

1. 读 `../../shared/references/readme/core-sections.md`（核心 hook）
2. 按 `../../shared/workflow/open-source-readme.md` 组织输出
3. 用 `../../shared/scripts/readme-gate.py` 做结构校验
4. 不允许保留模板占位符或伪造外链

## 编码效率与复杂度门禁

进入 `Dev` / `Review`，且涉及新增代码 / 重构 / 依赖选择 / 审查时：

1. 先读 `../../skills/product-delivery-methods/references/code-simplicity.md`
2. 优先标准库、平台原生能力和项目既有依赖
3. 不为单实现 / 单调用方 / "以后可能需要" 新增抽象层
4. 有意简化的实现，用 `ponytail:` 注释写清上限和升级触发条件
5. 非平凡逻辑仍必须留下最小可运行检查

## 标准链路

`需求分析 → 技术方案 → UI方案 → 任务分解 → 开发 → 自测 → 审查 → 冒烟 → 验收 → 发布`

"验收"默认是 QA / UI / 产品三类并行收口，由 `stage-gate.py` 强制顺序。

## Companion

需要方法论增强时调用 `../../skills/product-delivery-methods/SKILL.md`。
