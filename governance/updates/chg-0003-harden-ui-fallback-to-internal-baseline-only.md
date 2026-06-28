# chg-0003 harden ui fallback to internal baseline only

## 时间

`2026-04-12`

## 变更

- 在 `AGENTS.md`、根级 `SKILL.md`、主入口 skill、`README.md`、`design-baseline.md` 中补充硬约束
- 新增根级 `CLAUDE.md`
- 明确 `ui-ux-pro-max` 缺失时，唯一允许的回退路径是 `shared/references/design-baseline.md`
- 显式禁止把 `frontend-design` 等通用设计 skill 当成默认兜底

## 原因

真实 Claude 隔离回归显示：当用户级 `ui-ux-pro-max` 不可见时，模型会自行跳去 `frontend-design`，这与仓库预期不一致。

## 后续

- 后续若新增其他设计增强 skill，也必须先显式声明“是否允许作为 fallback”，否则默认不参与兜底
