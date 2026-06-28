# START HERE

第一次使用 `product-delivery-skill`，先看这份文档（≤ 5 分钟）。

## 1. 必读链路（按顺序）

| # | 文件 | 用途 |
|---|------|------|
| 1 | [README.md](./README.md) | 项目概述 + 目录 + 快速开始 |
| 2 | [SKILL.md](./SKILL.md) | 根入口路由 |
| 3 | [skills/product-delivery-skill/SKILL.md](./skills/product-delivery-skill/SKILL.md) | 主流程入口（必读 3 项 + 按需 5 项）|
| 4 | [shared/templates/README.md](./shared/templates/README.md) | 21 项产物模板索引 |

## 2. 选择 profile

| Profile | 适用场景 |
|---------|---------|
| [sbti-red](./profiles/sbti-red/README.md) | C 端内容产品（最完整画像）|
| [ai-rpa](./profiles/ai-rpa/README.md) | 制造业 RPA / 决策引擎 |
| [ai-trade-platform](./profiles/ai-trade-platform/README.md) | AI 外贸获客 / SDR |
| [haloo](./profiles/haloo/README.md) | 数字人社交 / 3DGS |
| [worldcup-predictor](./profiles/worldcup-predictor/README.md) | 体育数据可视化 / H5 |

## 3. 入口分工

- 根 `SKILL.md` 只路由，不堆规则
- 主流程入口 `skills/product-delivery-skill/SKILL.md`（必读 3 + 按需 5）
- 方法增强入口 `skills/product-delivery-methods/SKILL.md`
- 长文档全部下沉到 [docs/](./docs/)（架构 / profiles / readme-spec）

## 4. 最小执行命令

```bash
# 环境体检（按需逐个跑）
bash install/doctor.sh --capability docs
bash install/doctor.sh --capability dev
bash install/doctor.sh --capability db
bash install/doctor.sh --capability deploy

# 新建一个 request
python3 shared/scripts/init-request.py \
  --request-key my-first-request \
  --workspace workspace/requests

# 单阶段 / 一键 Gate
python3 shared/scripts/stage-gate.py \
  --request-dir workspace/requests/my-first-request --stage requirement
python3 shared/scripts/stage-gate.py \
  --request-dir workspace/requests/my-first-request --stage all

# skill 包自检（CI 友好，输出 PASS/WARN/FAIL）
python3 shared/scripts/health-check.py
python3 shared/scripts/health-check.py --json
```

## 5. 看真实样例

- 精简参考：[examples/sbti-red-mvp/](./examples/sbti-red-mvp/)
- 历史完整运行：[examples/historical-runs/](./examples/historical-runs/README.md)
  > 仅供参考，**不要当作当前任务读取**。
- 当前任务必须落到 `workspace/requests/<key>/`（该目录 gitignored）。

## 6. 当前版本

- v0.2.0 — 见 [governance/CHANGELOG.md](./governance/CHANGELOG.md)
- 健康检查：[governance/health-check.md](./governance/health-check.md) + `shared/scripts/health-check.py`
- 决策记录：[governance/decisions/](./governance/decisions/)
