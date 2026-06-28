---
name: product-delivery-methods
description: Use when 主流程已确定但在规划、调试、验证或评审决策上需要更严格的方法论执行。
---

# Product Delivery Methods

## 目标

为主流程提供方法层补强，避免“流程有了但执行质量不稳”。

## 参考入口

- `references/planning.md`
- `references/tdd.md`
- `references/debugging.md`
- `references/verification.md`
- `references/review.md`
- `references/parallel-and-isolation.md`
- `references/code-simplicity.md`

## 默认执行原则

1. 先识别当前问题属于哪类方法问题，再选择对应参考
2. 优先把方法落实到当前需求目录中的真实产物、脚本、测试和验证记录
3. 不把宿主机外部 skill 当成运行依赖
4. 如需引入外部 skill 内容，先登记到 `../../governance/vendor-skills.yaml`
5. 如需长期收编外部方法，优先内化到本 skill 的 `references/`，而不是运行时引用外部路径
6. 多人并行时必须先划分写入边界，再分派 worker；同一文件不能被两个 worker 同时改写
7. 开发或审查阶段出现代码膨胀、过度抽象、新依赖、重复样板、单实现接口时，读取 `references/code-simplicity.md`
