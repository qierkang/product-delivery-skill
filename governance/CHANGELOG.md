# CHANGELOG

## 2026-06-29 — v0.2.0 首次独立入库

- **首次以独立 git 仓库托管**：内部远端完成首次入库，后续公开分发以 GitHub 仓库为准
- 新增决策 [dec-0004](./decisions/dec-0004-standalone-gitlab-repo.md)，[dec-0003](./decisions/dec-0003-skill-repo-untracked-in-codex-workspace.md) 标记为 superseded
- 本次入库范围由 `.gitignore` 收口：忽略 `workspace/requests/*`、`graphify-out/`、`__pycache__`、`.DS_Store`、`node_modules/`、`.venv/` 等

## 2026-06-27 — v0.2.0 生产级整改

- **examples/historical-runs/ 归档机制**：将 `workspace/requests/sbti-red-mvp`、`sbti-red-fullrun-2026-04-11`、`sbti-red-fullrun-2026-04-11-v2`、`design-md-smoke` 4 个历史完整运行迁出到 `examples/historical-runs/`，避免被模型当成当前任务读取，明显降低 token 污染
- **新增根 `.gitignore`**：`workspace/requests/*` 默认忽略（保留 `.gitkeep`），实际任务运行不再纳入仓库
- **README.md 瘦身**：从 381 行 → 121 行（≤180 行目标）。详细架构 / profiles / readme-spec 拆到 `docs/architecture.md`、`docs/profiles.md`、`docs/readme-spec.md`
- **主 SKILL 必读清单分级**：`skills/product-delivery-skill/SKILL.md` 重写为"必读 3 项 + 按需 5 项（带触发条件）"，避免一次性加载所有规则
- **README 参考三件套去重**：新增 `shared/references/readme/core-sections.md`（≤120 行 hook），把 `spec-open-source-readme-template.md`（444 行）降级为按需展开
- **profiles 索引补齐**：5 个 profile（sbti-red / ai-rpa / ai-trade-platform / haloo / worldcup-predictor）各加 `README.md`
- **新增 `governance/health-check.md`**：自检清单，让 skill 包可被周期性验收
- **SKILL frontmatter 升级**：`skills/product-delivery-skill/SKILL.md` 新增 `version: 0.2.0`
- **新增决策 `dec-0002-keep-chinese-template-filenames.md`**：澄清"shared/templates 中文文件名"不是乱码，是命名约定，不重命名

## 2026-04-11

- 初始化 `product-delivery-skill` 骨架
- 新增 `sbti-red` 试点 profile
- 新增基础 workflow / templates / scripts

## 2026-04-12

- 新增 `shared/references/design-baseline.md`，作为 `ui-ux-pro-max` 缺失时的设计兜底说明
- 主入口、README、模板说明已明确“外部设计 skill 优先、内置规则兜底”
- UI 方案模板与 UI 验收模板已补风格、token、动效、可访问性结构
- 真实 Claude 隔离回归后，已显式禁止把 `frontend-design` 之类通用设计 skill 当成默认回退路径
- 新增根级 `CLAUDE.md`，把上述 UI 路由规则直接前置给 Claude 运行端

## 2026-05-30

- 新增 `profiles/haloo/profile.yaml`，接入 haloo（数字人社交平台）项目
- 新增 `shared/scripts/init-project-docs.py`，支持新项目一键初始化 consolidated docs/ 四层结构（需求/设计/技术/交付）
- 新增 `shared/workflow/new-project.md`，定义新项目初始化标准流程
- 明确 init-request.py（需求迭代）与 init-project-docs.py（新项目初始化）的分工边界
- sbti-red profile 的 workspace_dir 需同步更新为 solutionsWorkSpace 路径（旧路径已废弃）

## 2026-04-21

- 新增 `shared/references/readme/`，将 GitHub 开源 README 的主提示词、风格参考和结构模板内化到 skill 包内
- 新增 `shared/workflow/open-source-readme.md`，把 README 生成、改写与校验串成标准工作流
- 新增 `shared/scripts/readme-gate.py`，用于校验 README 章节完整性与占位符残留
- `README.md`、`SKILL.md`、`skills/product-delivery-skill/SKILL.md` 已同步接入新的 README 路由

## 2026-06-17

- 全局安装 `DietrichGebert/ponytail` 的五个 skill：`ponytail`、`ponytail-review`、`ponytail-audit`、`ponytail-debt`、`ponytail-help`
- 新增 `governance/vendor-skills.yaml`，登记 `ponytail` 来源、许可证、commit 与集成边界
- 新增 `skills/product-delivery-methods/references/code-simplicity.md`，将 `ponytail` 的编码精简、复杂度 review 和 deferred shortcut ledger 规则内化为方法增强
- 主入口已在 `Dev` / `Review` 阶段接入编码效率与复杂度门禁，但不依赖外部 hooks 或 slash command
