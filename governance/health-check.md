# Health Check — Product Delivery Skill

> 周期性自检清单。每次 skill 包发版前过一遍，结果写入 `governance/updates/`。

## 1. 结构与入口

- [ ] 根 `SKILL.md` ≤ 50 行，只路由不堆规则
- [ ] 根 `README.md` 存在，并通过 README gate；开源展示内容不再使用固定行数上限
- [ ] `skills/product-delivery-skill/SKILL.md` ≤ 120 行，必读 ≤ 3 项 + 按需带触发条件
- [ ] `skills/product-delivery-methods/SKILL.md` 存在且能从主入口路由到
- [ ] `START-HERE.md` 指向当前真实文件，无 404 链接

## 2. Token 卫生

- [ ] `workspace/requests/` 不含未在 `.gitignore` 内的任务（避免历史运行污染）
- [ ] 历史完整运行全部放在 `examples/historical-runs/`，附 `README.md` 警示"不要当作当前任务"
- [ ] `shared/references/readme/spec-open-source-readme-template.md` 不出现在任何"必读清单"，只作为按需展开

## 3. 资产与模板

- [ ] `shared/templates/` 21 项标准产物模板全部存在
- [ ] `shared/templates/README.md` 与 `docs/architecture.md` 的产物清单一致
- [ ] 每个 profile 目录下都有 `README.md` + `profile.yaml`

## 4. 可执行脚本

```bash
# 体检脚本能跑
bash install/doctor.sh --capability docs

# 初始化脚本能跑（用临时目录）
python3 shared/scripts/init-request.py --request-key hc-smoke --title "health-check" --workspace /tmp/pd-hc

# Gate 脚本能跑（允许 fail，只要不崩）
python3 shared/scripts/stage-gate.py --request-dir /tmp/pd-hc/hc-smoke --stage requirement || true

# README 校验脚本能跑（仅检查 --help）
python3 shared/scripts/readme-gate.py --help

# 清理
rm -rf /tmp/pd-hc
```

## 5. 治理与版本

- [ ] `governance/CHANGELOG.md` 包含当前版本条目
- [ ] `SKILL.md` frontmatter `version` 与 CHANGELOG 顶部对齐
- [ ] `governance/decisions/` 内每个决策都有 status（accepted / superseded / deprecated）
- [ ] `governance/vendor-skills.yaml` 中第三方 skill 来源、commit、license 都填齐

## 6. 链路抽样

- [ ] 任取一个 `examples/historical-runs/<key>/`，对照 21 项产物清单确认覆盖
- [ ] 任取一个真实 profile，对照其 `profile.yaml` 中 `workspace_dir` 路径确认目录可达

## 失败处理

任何 `[ ]` 未打勾即视为不健康。修复后在 `governance/updates/<date>-health-check.md` 写一行：

```text
- 修复项：<短描述>
- 关联 PR / commit：<sha or link>
- 健康度：<x/y 通过>
```
