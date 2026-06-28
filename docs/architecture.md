# Architecture — Product Delivery Skill 详解

> 本文档从根 README 拆出，用于不需要在每个会话都把架构细节拉进 token 的场景。
> 一般任务读 [README.md](../README.md) 即可；只在需要回答"为什么这样分层 / 如何扩展"时阅读本文。

## 设计目标

Product Delivery Skill 不是一段 prompt，也不是模板仓库。它是一个：

- 独立设计、可分发、可复刻、可审计的产品交付技能包
- 不绑定某一个模型，由运行端识别并执行
- 在多类型项目（B 端 / C 端 / APP / 小程序 / H5）之间保持同一套阶段口径

## 核心特色

- **统一入口**：所有需求统一从 `product-delivery-skill` 进入
- **流程标准化**：固定 `Requirement → Design → Dev → Review → Smoke → QA → UI Acceptance → Product Acceptance → Release`
- **产物结构化**：每个 request 都有固定目录、固定主文档、固定元数据
- **设计基线显式化**：`DESIGN.md` 作为 AI 可读设计基线纳入正式交付物
- **阶段 Gate**：每一阶段都能做显式校验，减少口头放行
- **项目画像可配置**：通过 `profiles/` 注入项目差异，而不是改主流程
- **多类型项目适配**：B 端、C 端、APP、小程序、H5 等
- **多运行端兼容**：不强绑定 Claude / Codex / OpenClaw 任一单端
- **运行与治理分层**：规则、样例、运行产物、治理记录各自独立

## 目录分层

```text
product-delivery-skill/
├── SKILL.md                  # 根入口（仅路由）
├── START-HERE.md             # 新接手最短阅读路径
├── install/                  # 初始化、doctor、同步
├── skills/
│   ├── product-delivery-skill/      # 主流程
│   └── product-delivery-methods/    # 方法增强
├── profiles/                 # 项目画像
├── shared/
│   ├── references/           # 规则、写作基线、设计、README 参考
│   ├── scripts/              # init-request / stage-gate / project-check
│   ├── templates/            # 标准产物模板
│   └── workflow/             # 不同类型 request 的流程路由
├── workspace/                # 运行中的 request（gitignored）
├── examples/                 # 参考样例 + historical-runs/
├── docs/                     # 长文档（不走 token 默认路径）
└── governance/               # 治理记录
```

| 目录 | 用途 |
|------|------|
| `SKILL.md` | 兼容只识别根级 skill 的平台 |
| `install/` | 新环境初始化、doctor |
| `skills/` | 主流程与方法增强 |
| `profiles/` | 项目画像、业务背景、默认策略 |
| `shared/templates/` | 标准产物模板 |
| `shared/scripts/` | 自动化脚本 |
| `shared/references/` | 公共规则与参考 |
| `shared/workflow/` | 不同 request 类型的流程 |
| `workspace/` | 实际运行中的 request（gitignored）|
| `examples/` | 参考样例与历史完整运行 |
| `governance/` | 决策、CHANGELOG、health-check |

## 固定交付链路

`Requirement → Design → Dev → Review → Smoke → QA → UI Acceptance → Product Acceptance → Release`

三条强约束：
1. 不跳步骤
2. 不口头完成
3. 不模糊放行

其中：
- `QA` 负责功能、边界、回归与缺陷收口
- `UI Acceptance` 负责视觉、交互、token、动效与响应式
- `Product Acceptance` 负责业务口径、范围边界与最终交付确认

阶段总线由 `stage-gate.py` 收口，`qa → ui_acceptance → product_acceptance → release` 是强顺序。

## 标准产物体系（21 项）

| 阶段 | 产物 | 作用 |
|------|------|------|
| Requirement | `00-需求总览.md` | request 导航与总体口径 |
| Requirement | `需求文档.md` | 业务需求、范围、规则、验收标准 |
| Requirement | `manifest.json` | 机器可读元数据 |
| Design | `DESIGN.md` | AI 可读设计基线 |
| Design | `技术方案.md` | 架构、数据、接口、回滚 |
| Design | `UI交互设计规范.md` | 页面结构、交互、状态、端差异 |
| Design | `任务分解.md` | 执行任务拆分与责任 |
| Dev | `实现控制总表.md` | 需求到实现的追踪 |
| Dev | `页面接口验收总表.md` | 页面动作与接口映射 |
| Dev | `开发放行报告.md` | 开发自测与放行结论 |
| Dev | `覆盖率报告.md` | 覆盖率与测试证据 |
| Dev | `前端关键流程覆盖清单.md` | 前端关键链路核对 |
| Review | `代码审查报告.md` | 风险与审查结论 |
| Smoke | `冒烟测试脚本.sh` | 可重复执行的冒烟脚本 |
| Smoke | `冒烟测试报告.md` | 冒烟结果记录 |
| QA | `测试用例.md` | 功能、边界、异常测试设计 |
| QA | `QA验收报告.md` | QA 验收结论 |
| UI Acceptance | `UI验收报告.md` | UI 还原和交互验收 |
| Product Acceptance | `产品验收报告.md` | 产品侧最终验收 |
| Release | `发布记录.md` | 发布与回滚记录 |
| Release | `stage-status.json` | request 当前阶段状态机 |

模板入口：[shared/templates/README.md](../shared/templates/README.md)

## Workflow 路由

- [shared/workflow/new-feature.md](../shared/workflow/new-feature.md)
- [shared/workflow/change-request.md](../shared/workflow/change-request.md)
- [shared/workflow/bugfix.md](../shared/workflow/bugfix.md)
- [shared/workflow/growth-campaign.md](../shared/workflow/growth-campaign.md)

## 运行端兼容

- 单接 Claude / Codex / OpenClaw 均可
- 多运行端可按同一套流程协作
- 规则、模板、Gate、画像均沉淀在仓库
