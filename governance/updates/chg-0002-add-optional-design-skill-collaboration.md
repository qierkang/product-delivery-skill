# chg-0002 add optional design skill collaboration

## 时间

`2026-04-12`

## 变更

- 新增 `shared/references/design-baseline.md`
- 主入口与 README 补充“`ui-ux-pro-max` 优先、内置规则兜底”说明
- UI 方案模板与 UI 验收模板补齐风格、token、动效、可访问性字段
- `stage-gate.py` 对 UI 方案和 UI 验收的检查口径同步增强

## 原因

`product-delivery-skill` 不应自己演化成设计主仓，但在真实交付里，UI 方案和 UI 验收需要一个更清晰的设计基线来源。

## 后续

- 后续如需要更细的设计审查清单，再继续在 `shared/references/` 中收敛，不把外部 skill 当成强依赖
