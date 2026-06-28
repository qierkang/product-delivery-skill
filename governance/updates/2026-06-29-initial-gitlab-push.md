# 2026-06-29 — 首次入库 GitLab

## 远程

- URL：`http://gitlab.zhgcraft.com/skills/product-delivery-skill.git`
- 主分支：`master`
- 跟踪：`origin/master` ✓

## 入库规模

- 文件数：208（按 `.gitignore` 收口）
- 仓库体积：约 7 MB
- 最大单文件：`assets/architecture/workflow-architecture.png`（2.5 MB）
- 排除：`workspace/requests/*`、`graphify-out`、`__pycache__`、`.DS_Store`、`node_modules`、`.venv`

## Commit 链

```text
ac06bb3 (origin/master) Merge branch 'master' of gitlab  ← 合并远程 Initial commit
0539021                 feat: product-delivery-skill v0.2.0 首次入库
04375ae                 Initial commit （GitLab 自动 init，已被 -X ours 策略保留为空 merge 节点）
```

## 处理远程已存在 Initial commit 的策略

远程在仓库创建时被 GitLab 自动塞了一个 `Initial commit`，含一行 `README.md`。
本地首次 commit 已含 v0.2.0 完整 README。处理：

```bash
git pull origin master --allow-unrelated-histories --no-rebase --no-edit -X ours
git push -u origin master
```

`-X ours` 在 merge 冲突时优先保留本地版本，结果：本地 v0.2.0 README（123 行）保留不变，远程的 placeholder README 被覆盖。

## 与 dec-0004 的对齐

- `dec-0003` 已标记为 superseded
- `dec-0004` accepted
- `CHANGELOG.md` v0.2.0 顶部已记录"首次入库 gitlab"

## 后续动作建议

- [ ] 在 GitLab 配置 default branch protection（禁 force push 到 master）
- [ ] 配置 CI 跑 `python3 shared/scripts/health-check.py --fail-on-warn`
- [ ] 评估是否在 codex-workspace 父仓 `.gitignore` 加 `ai-workspace/skills/*/`（避免双重 git 状态）
