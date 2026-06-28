# Product Delivery Skill

> 独立设计的通用产品交付技能包 · 单入口调度 · 标准产物链路 · 阶段 Gate · 模型无关 · 多运行端兼容

面向 Web、B 端、C 端、APP、小程序、H5 的标准化产品交付技能包。
覆盖需求分析、方案设计、开发推进、审查、冒烟、QA、UI/产品验收与发布。

第一次接手请看 [START-HERE.md](./START-HERE.md)。

## 项目概述

一套独立、可分发、可复刻、可审计的产品交付技能包。它提供统一入口、固定阶段、标准产物、脚本化 Gate 和项目画像机制，把"需求 → 方案 → 开发联调 → 测试验收 → 发布"收敛成稳定流程。

- 不绑定特定模型；任何运行端识别后即可执行
- 单端或多运行端协作均可
- 任务若为"README 升级为 GitHub 开源版本"，走 [shared/workflow/open-source-readme.md](./shared/workflow/open-source-readme.md)

## 目录结构

```text
product-delivery-skill/
├── SKILL.md                  # 根入口（仅路由）
├── START-HERE.md             # 新接手最短路径
├── docs/                     # 长文档（架构 / readme-spec / profiles）
├── install/                  # 初始化、doctor
├── skills/                   # 主流程 + 方法增强
├── profiles/                 # 项目画像
├── shared/
│   ├── references/           # 规则、参考
│   ├── scripts/              # init-request / stage-gate / readme-gate
│   ├── templates/            # 标准产物模板
│   └── workflow/             # 流程路由
├── workspace/                # 运行中 request（gitignored）
├── examples/
│   ├── sbti-red-mvp/         # 精简参考样例
│   └── historical-runs/      # 历史已完成全量运行（仅供参考）
└── governance/               # 决策、CHANGELOG、health-check
```

> 架构详解、产物清单、workflow 路由：[docs/architecture.md](./docs/architecture.md)
> 项目画像与适用场景：[docs/profiles.md](./docs/profiles.md)
> README 开源规范：[docs/readme-spec.md](./docs/readme-spec.md)

## 链路简图

```text
Requirement → Design → Dev → Review → Smoke → QA → UI Acceptance → Product Acceptance → Release
                                              └─ qa → ui_acceptance → product_acceptance → release 为强顺序
```

- 阶段总线由 `shared/scripts/stage-gate.py` 收口
- 每阶段都有显式 Gate，不口头放行
- 21 项标准产物模板见 [docs/architecture.md](./docs/architecture.md#标准产物体系21-项)

## 快速开始

```bash
# 1. 克隆
git clone <your-repo-url> product-delivery-skill && cd product-delivery-skill

# 2. 初始化与体检
bash install/setup.sh
bash install/doctor.sh --capability docs

# 3. 初始化一个 request
python3 shared/scripts/init-request.py \
  --request-key my-first-request \
  --workspace workspace/requests

# 4. 阶段 Gate
python3 shared/scripts/stage-gate.py \
  --request-dir workspace/requests/my-first-request \
  --stage requirement

# 5. 一键全量校验
python3 shared/scripts/stage-gate.py \
  --request-dir workspace/requests/my-first-request \
  --stage all
```

## 常用命令

```bash
# 单阶段 Gate（stage ∈ requirement/design/dev/review/smoke/qa/release）
python3 shared/scripts/stage-gate.py --request-dir <dir> --stage <stage>

# 项目级交付检查
python3 shared/scripts/project-ready-check.py --project-dir <project-dir>

# README 开源规范校验
python3 shared/scripts/readme-gate.py --readme README.md
```

## 环境要求

**基础**：`git` · `python3` · 任一运行端或模型 CLI
**常见开发**：`node`/`pnpm` · `java`/`maven` · `psql`
具体能力按承接的真实项目决定，skill 包本身不强制全部具备。

## 建议阅读路径

1. [START-HERE.md](./START-HERE.md)
2. 本 README
3. [SKILL.md](./SKILL.md)
4. [skills/product-delivery-skill/SKILL.md](./skills/product-delivery-skill/SKILL.md)
5. [shared/templates/README.md](./shared/templates/README.md)

如需直接看真实样例，参考：
- 精简版：[examples/sbti-red-mvp/](./examples/sbti-red-mvp/)
- 完整运行存档：[examples/historical-runs/](./examples/historical-runs/README.md) （**仅供参考，不要当成当前任务读取**）

## 版本与治理

- 当前版本：`v0.2.0`（见 [SKILL.md](./SKILL.md) frontmatter）
- 变更记录：[governance/CHANGELOG.md](./governance/CHANGELOG.md)
- 健康检查清单：[governance/health-check.md](./governance/health-check.md)
- 自检脚本：`python3 shared/scripts/health-check.py`（输出 PASS/WARN/FAIL；加 `--json` 供 CI 消费）
- 决策记录：[governance/decisions/](./governance/decisions/)
- Git 托管：**独立 gitlab 仓库** `http://gitlab.zhgcraft.com/skills/product-delivery-skill.git`（master 分支），详见 [dec-0004](./governance/decisions/dec-0004-standalone-gitlab-repo.md)

## License / 使用说明

如准备长期对外维护，建议补充 `LICENSE`、`CONTRIBUTING.md`、`CHANGELOG.md`（后者已位于 `governance/`）。
