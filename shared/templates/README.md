# 模板索引与产物规范

本目录用于维护 `product-delivery-skill` 的标准文档模板，供未来任意项目复用。

## 模板来源

- 主来源：`picasso-dev-skill/shared/templates`
- 策略：保留其“全链路交付 + 阶段 Gate + 证据放行”能力，去除 Picasso 业务耦合字段，沉淀为通用版本。
- UI 设计部分允许优先协同外部 `ui-ux-pro-max`，若不可用则回退到 `shared/references/design-baseline.md`。
- 若项目存在 `DESIGN.md`，它是页面风格、组件语气和视觉边界的第一设计输入；`UI交互设计规范.md` 负责把它展开到页面与交互层。

## 目录结构

```text
shared/templates/
├── request/
├── design/
├── control/
├── qa/
├── release/
├── ui/
├── config/
└── governance/
```

## 标准产物映射（21 项）

| 产物文件 | 本仓模板路径 | 来源模板（picasso） |
|---|---|---|
| `00-需求总览.md` | `request/overview.md` | `需求总览模板.md` |
| `需求文档.md` | `request/requirement.md` | `需求文档模板.md` |
| `manifest.json` | `request/manifest.json` | `manifest模板.json` |
| `DESIGN.md` | `design/design.md` | 新增：AI 可读设计基线 |
| `技术方案.md` | `design/tech-design.md` | `技术方案模板.md` |
| `UI交互设计规范.md` | `design/ui-spec.md` | `UI交互设计模板.md` |
| `任务分解.md` | `design/task-breakdown.md` | `任务分解模板.md` |
| `实现控制总表.md` | `control/implementation-control.md` | `实现控制总表模板.md` |
| `页面接口验收总表.md` | `control/page-api-acceptance.md` | `页面接口验收总表模板.md` |
| `开发放行报告.md` | `qa/dev-release-report.md` | `开发放行报告模板.md` |
| `覆盖率报告.md` | `qa/coverage-report.md` | `覆盖率报告模板.md` |
| `前端关键流程覆盖清单.md` | `qa/frontend-keyflow-checklist.md` | `前端关键流程覆盖清单模板.md` |
| `代码审查报告.md` | `qa/code-review-report.md` | `代码审查报告模板.md` |
| `冒烟测试脚本.sh` | `qa/smoke-test-script.sh` | `冒烟测试脚本模板.sh` |
| `冒烟测试报告.md` | `qa/smoke-test-report.md` | `冒烟测试报告模板.md` |
| `测试用例.md` | `qa/test-cases.md` | `测试用例模板.md` |
| `QA验收报告.md` | `qa/qa-acceptance-report.md` | `QA验收报告模板.md` |
| `UI验收报告.md` | `qa/ui-acceptance-report.md` | `UI验收报告模板.md` |
| `产品验收报告.md` | `qa/product-acceptance-report.md` | `产品验收报告模板.md` |
| `发布记录.md` | `release/release-record.md` | `发布记录模板.md` |
| `stage-status.json` | `request/stage-status.json` | `stage-status模板.json` |

## 可选扩展模板

当项目需要更完整的交付闭环时，建议再补以下扩展模板：

| 扩展文件 | 用途 |
|---|---|
| `ui/page-api-mapping.md` | 页面动作与接口对照，便于联调、验收和回流 |
| `config/MENU_DATA.md` | 菜单结构与权限点配置 |
| `config/DICT_DATA.md` | 字典类型与字典值配置 |
| `config/sql-change.sql` | SQL 变更、初始化或回滚脚本 |

## 阶段最低放行要求

| 阶段 | 最低必备产物 |
|---|---|
| Requirement | `00-需求总览.md`、`需求文档.md`、`manifest.json` |
| Design | `DESIGN.md`、`技术方案.md`、`UI交互设计规范.md`、`任务分解.md` |
| Dev | `实现控制总表.md`、`页面接口验收总表.md`、`开发放行报告.md`、`覆盖率报告.md`、`前端关键流程覆盖清单.md` |
| Review | `代码审查报告.md` |
| Smoke | `冒烟测试脚本.sh`、`冒烟测试报告.md` |
| QA | `测试用例.md`、`QA验收报告.md` |
| UI Acceptance | `UI验收报告.md` |
| Product Acceptance | `产品验收报告.md` |
| Release | `发布记录.md`、`stage-status.json` |

## 写作要求（通用）

1. 每份文档必须有元信息：版本、日期、负责人、状态。
2. 文档元信息中的作者默认写 `xyqierkang@gmail（claude+codex）`。
3. 每份结论型文档必须有“证据清单”字段。
4. 每个阶段默认结论是 `NEEDS_WORK`，证据完整才允许写 `READY`。
5. 涉及跨端时必须补端差异说明（Web/APP/小程序/H5）。
6. 涉及数据、交易、权限、审批场景时必须写回滚策略。
7. SQL 文件必须包含中文表/字段注释与作者头注释。
8. UI 方案必须补：风格方向、token、动效、可访问性结构。
9. UI 验收必须补：风格方向符合度、token 一致性、动效与响应式检查。
10. 若项目创建了 `DESIGN.md`，页面实现、UI 设计规范与 UI 验收都必须显式说明是否对齐该文件。
11. QA、UI、产品验收默认分开产出，不再合并成单一最终报告。
