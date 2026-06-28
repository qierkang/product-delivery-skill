# Profiles 详解

> 从根 README 拆出。仅在新增 profile / 调整画像策略时阅读。

`product-delivery-skill` 不把项目差异硬编码进主流程，而是通过 `profiles/` 注入画像。

## 可配置内容

- 项目名称和品牌信息
- 目标用户和业务类型
- 技术栈
- 平台范围
- 环境边界
- 默认流程策略

## 当前画像

| Profile | 适用场景 | 入口 |
|---------|----------|------|
| `sbti-red` | SBTI Red 试点项目 | [profiles/sbti-red/profile.yaml](../profiles/sbti-red/profile.yaml) |
| `ai-rpa` | AI RPA 类自动化项目 | [profiles/ai-rpa/](../profiles/ai-rpa/) |
| `ai-trade-platform` | AI 交易平台类项目 | [profiles/ai-trade-platform/](../profiles/ai-trade-platform/) |
| `worldcup-predictor` | 世界杯预测类活动项目 | [profiles/worldcup-predictor/](../profiles/worldcup-predictor/) |
| `haloo` | Haloo 3D 类社交模拟项目 | [profiles/haloo/](../profiles/haloo/) |

每个 profile 目录下若有 `README.md`，先读 README 再读 `profile.yaml`。

## 适用项目类型

| 项目类型 | 适配情况 | 说明 |
|------|------|------|
| B 端后台 / SaaS | 强适配 | 多阶段、多角色、可审计的交付方式 |
| C 端产品 | 强适配 | 需求、UI、QA、验收链路明确 |
| APP | 适配 | 建议补兼容性、崩溃监控、发版说明 |
| 小程序 | 适配 | 建议补审核、分包、弱网降级 |
| H5 活动页 | 适配 | 建议补分享链路、并发预案、统计验证 |
| 单页 Demo | 可用 | 沉淀规范，不一定需要全部产物 |
