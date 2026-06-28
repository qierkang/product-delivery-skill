---
name: product-delivery-skill
description: Use when 需要把一个产品需求从目标定义推进到可发布交付，并希望统一执行需求、方案、开发、验证和发布证据链。
---

# Product Delivery Skill

根入口只做路由，真实执行入口在：

- `skills/product-delivery-skill/SKILL.md`

方法增强在：

- `skills/product-delivery-methods/SKILL.md`
- 编码效率与复杂度门禁：`skills/product-delivery-methods/references/code-simplicity.md`

README 生成与开源发布工作流在：

- `shared/workflow/open-source-readme.md`
- `shared/references/readme/README.md`
- `shared/scripts/readme-gate.py`

## 编码效率增强

`ponytail` 已作为外部方法来源登记在 `governance/vendor-skills.yaml`，核心规则已内化到 `skills/product-delivery-methods/references/code-simplicity.md`。

该增强只在 `Dev` / `Review` 阶段约束代码实现和复杂度审查，不替代主交付流程，也不依赖外部 hooks、slash command 或运行时模式文件。

## UI 设计回退规则

进入 UI 方案或 UI 验收阶段时：

1. 若当前运行端可识别 `ui-ux-pro-max`，优先协同它
2. 若不可识别，唯一允许的回退路径是 `shared/references/design-baseline.md`
3. 即使当前运行端还能识别 `frontend-design` 一类通用设计 skill，也不得把它们当成 `ui-ux-pro-max` 缺失时的兜底替代
