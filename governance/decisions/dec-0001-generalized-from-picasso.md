# dec-0001 generalized from picasso

- **状态**：accepted
- **日期**：2026-04-11

## 决策

`product-delivery-skill` 继承 `picasso-dev-skill` 的流程控制能力，但移除 Picasso 专有业务约束，采用 profile 参数化方式适配项目。

## 原因

- 复用成熟流程
- 降低跨项目迁移成本
- 保持脚本和模板可执行

