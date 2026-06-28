# README 生成与开源发布流程

> 从根 README 拆出。仅在做"README 升级为 GitHub 开源版本"任务时阅读。

## 工作流入口

主入口：[shared/workflow/open-source-readme.md](../shared/workflow/open-source-readme.md)

参考三件套：
- 核心章节（Hook，必读）：[shared/references/readme/core-sections.md](../shared/references/readme/core-sections.md)
- 完整规范（按需）：[shared/references/readme/spec-open-source-readme-template.md](../shared/references/readme/spec-open-source-readme-template.md)
- 入口索引：[shared/references/readme/README.md](../shared/references/readme/README.md)

## 校验脚本

```bash
python3 shared/scripts/readme-gate.py --readme README.md
```

## 设计能力协同

`product-delivery-skill` 在 Design / UI 验收阶段可协同外部设计能力：

1. 优先识别 `ui-ux-pro-max`；不可识别时回退到 `shared/references/design-baseline.md`
2. 即使运行端能识别 `frontend-design` 等通用设计 skill，也**不**得当成 `ui-ux-pro-max` 的兜底替代
3. 不把外部设计能力当作主流程唯一前提，避免阻塞

> 详见 [SKILL.md](../SKILL.md#ui-设计回退规则)。
