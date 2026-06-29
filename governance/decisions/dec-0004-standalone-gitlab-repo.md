# Decision 0004 — product-delivery-skill 以独立 git 仓库托管

- **状态**：accepted
- **日期**：2026-06-29
- **取代**：[dec-0003](./dec-0003-skill-repo-untracked-in-codex-workspace.md)（"暂不纳入 codex-workspace 主仓跟踪"）

## 背景

dec-0003 暂缓决策的本意是不向 codex-workspace 主仓做 200+ 文件首次入库。本次明确：

- skill 包从语义上就**不属于** codex-workspace 子树，它是可分发、可复刻、独立演化的技能包
- 已有独立 Git 远端用于内部托管
- 寄生在 codex-workspace 内做 worktree 是工作便利，**不是托管目标**

## 决策

**product-delivery-skill 在本目录内以独立 git 仓库托管**，内部远端保留为 `origin`，公开分发远端使用 GitHub，主分支为 `master`。

## 实施口径

1. 在 `ai-workspace/skills/product-delivery-skill/` 内 `git init`，**不**寄生 codex-workspace
2. 遵循本目录已有 `.gitignore`：忽略 `workspace/requests/*`、`.DS_Store`、`__pycache__/`、`node_modules/` 等
3. 额外忽略 `graphify-out/`（本地符号链接，跨机不可移植）
4. 分支命名：主分支 `master`（用户指定）
5. 提交统一署名 `xyqierkang@gmail.com`

## 与父目录的关系

- codex-workspace 主仓的 `git status` 会把本目录视为 untracked（因为含 `.git`）
- 父仓**不再尝试追踪本目录内容**，避免双重 git 状态
- 建议在 codex-workspace 主仓的 `.gitignore` 加 `ai-workspace/skills/*/` 一条，明确边界（可选，本决策不强制）

## 重新评估触发

- 改为多人协作且需细粒度权限控制 → 评估托管平台权限拆分
- skill 包外部化到独立 namespace → 评估迁出 `ai-workspace/skills/` 物理位置
- 出现破坏性变更需要回滚 → 启用 tag + release

## 关联记录

- `CHANGELOG.md` v0.2.0 顶部追加"首次独立入库"条目
- `governance/updates/2026-06-29-initial-gitlab-push.md` 记录首次 push 实际结果
