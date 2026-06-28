# Product Delivery Skill Work Rules

1. 默认语言：中文简体。
2. 先 `doctor` 后执行真实开发动作。
3. 没有验证证据不允许宣称完成。
4. profile 参数化优先，不在主流程里硬编码业务规则。
5. 输出优先包含可执行结果与关键证据路径。
6. 涉及 UI 方案或 UI 验收时：
   - 若当前运行端可识别 `ui-ux-pro-max`，优先借助它做设计基线与审查；
   - 若不可识别，自动回退到仓库模板与内置设计参考，不因外部 skill 缺失而阻塞交付；
   - 唯一允许的回退入口是 `shared/references/design-baseline.md`；
   - 默认不得改用 `frontend-design` 或其他通用设计 skill 充当兜底。
