# Product Delivery Skill Claude Rules

1. 本仓库 UI 相关任务默认先遵守 `AGENTS.md`、`SKILL.md`、`skills/product-delivery-skill/SKILL.md`。
2. 进入 UI 方案或 UI 验收阶段时：
   - 若当前运行端可识别 `ui-ux-pro-max`，优先使用它补设计基线或做 UI 审查。
   - 若当前运行端不可识别 `ui-ux-pro-max`，唯一允许的回退路径是 `shared/references/design-baseline.md`。
3. 即使当前运行端还能识别 `frontend-design` 或其他通用设计 skill，也不得把它们当成 `ui-ux-pro-max` 缺失时的默认兜底。
4. 最终产出必须落回本仓模板与 Gate，不允许因为外部设计 skill 缺失而改走别的通用设计流程。
