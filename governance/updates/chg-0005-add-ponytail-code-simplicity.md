# chg-0005 add ponytail code simplicity

## 时间

`2026-06-17`

## 变更

- 将 `DietrichGebert/ponytail` 安装为全局 skill，路径为 `<agent-skills-dir>/ponytail*`
- 新增 `governance/vendor-skills.yaml`，记录外部 skill 来源、许可证、commit 与集成方式
- 新增 `skills/product-delivery-methods/references/code-simplicity.md`
- 更新根入口与主入口，在 `Dev` / `Review` 阶段接入编码效率与复杂度门禁

## 原因

`product-delivery-skill` 原有方法层已经覆盖规划、TDD、验证、审查和并行隔离，但编码阶段仍偏原则化，缺少“少写代码但不牺牲质量”的可执行规则。

`ponytail` 的价值在于把 YAGNI、标准库优先、平台原生优先、少依赖、少抽象、最小验证这些原则压成一套短决策链，适合增强代码实现效率和审查质量。

## 集成边界

- 只内化方法，不依赖 upstream hooks、slash command、状态文件或运行时模式。
- 只影响 `Dev` / `Review` 阶段，不替代需求、方案、验收和发布 gate。
- 安全、数据、权限、可访问性、真实硬件校准、用户明确要求的完整能力不得被“少写代码”省略。

## 后续

- 后续如果出现大量 `ponytail:` 注释，可按需生成项目级 `PONYTAIL-DEBT.md` 或纳入 `代码审查报告.md`。
- 若全局 skill 版本升级，先更新 `governance/vendor-skills.yaml` 的 commit，再评估是否同步内化规则。
