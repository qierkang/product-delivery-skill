# README 核心章节（Hook）

> 适用场景：把一个项目的 README 升级为可对外开源的版本。
> 本文是**必读 hook**（≤120 行），先读完这一篇再决定是否展开 [完整规范](./spec-open-source-readme-template.md)。

## 必备章节顺序（不可省略）

| # | 章节 | 一句话用途 |
|---|------|-----------|
| 1 | `# {{项目名}}` + 一句话定位 | 让人 3 秒内知道这是什么 |
| 2 | 项目概述（2–4 段） | 做什么、解决什么、给谁用、在系统中的位置 |
| 3 | 核心特色（5–8 条） | 架构 / 工程化 / 业务 / 可扩展 / 部署 / 安全 各挑 1–2 条 |
| 4 | 快速开始 | 克隆 → 安装 → 运行 → 验证，命令必须可复制执行 |
| 5 | 目录结构 | 只放关键目录树 + 说明表，不机械贴整棵树 |
| 6 | 版本与维护状态 | 当前版本、维护方式、稳定度 |
| 7 | License / 使用说明 | 法律边界与二次使用前提 |

## 强烈建议章节（按项目类型挑选）

| 章节 | 何时加 |
|------|--------|
| 在线演示 / 截图 | UI / 平台 / 工作流类项目 |
| 功能模块 | 业务域 ≥ 3 个时拆分罗列 |
| 技术栈 | 跨多层（前端 / 后端 / 数据 / 基础设施）|
| 系统架构 | 涉及多服务 / 数据流 / 状态流 |
| 配置说明 | 有 `.env` / config 文件需要使用者填 |
| 部署指南 | 提供 Docker / K8s / 云部署路径 |
| 贡献指南 | 接受外部 PR |
| FAQ / 故障排查 | 已知反复出现的安装 / 配置坑 |

## 章节质量底线（readme-gate.py 会校验）

- 标题层级不能跳级（H1 → H3 是错误）
- 代码块必须标语言（` ```bash` 而不是 ` ``` `）
- 命令必须复制即可执行，禁止 `{{placeholder}}` 残留
- 外链优先指向项目内部文件（`./docs/...`），外部链接必须真实可访问
- 图片必须有 `alt` 文字（`![alt](path)`），不允许 `![](path)`
- License 段不允许只写"see LICENSE"不附路径

## 风格底线

- 中性、可验证。**禁止**营销话术（"业内领先"、"颠覆性"、"完美解决"）
- 默认中文 + 关键名词英文（如 `Skill Gate`、`Profile`），不要全英文也不要全中文音译
- 一段不超过 4 行；一个列表项不超过 2 行
- 命令行 / 文件路径用反引号包裹

## 何时进一步阅读

| 需求 | 进阶文件 |
|------|---------|
| 整套字段槽位、Badge、图表、长样例 | [spec-open-source-readme-template.md](./spec-open-source-readme-template.md) |
| 给模型生成 README 的主提示词 | [spec-open-source-readme-master-prompt.md](./spec-open-source-readme-master-prompt.md) |
| 信息密度 / 排版语气参考 | [spec-open-source-readme-style-reference.md](./spec-open-source-readme-style-reference.md) |
| 校验脚本与可执行 Gate | [shared/scripts/readme-gate.py](../../scripts/readme-gate.py) |
| 完整工作流（含 PR 阶段） | [shared/workflow/open-source-readme.md](../../workflow/open-source-readme.md) |

## 最小检查清单（落盘前过一遍）

- [ ] H1 标题与项目名一致
- [ ] 7 个必备章节全部存在
- [ ] 没有 `{{placeholder}}` 残留
- [ ] 所有命令在干净环境验证可执行
- [ ] 截图 / 图片真实存在且有 alt
- [ ] 内部链接全部可点击且文件存在
- [ ] License 段路径正确
- [ ] `python3 shared/scripts/readme-gate.py --readme README.md` 通过
