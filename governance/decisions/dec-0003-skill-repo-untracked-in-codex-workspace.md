# Decision 0003 — product-delivery-skill 暂不纳入 codex-workspace 主仓跟踪

- **状态**：superseded by [dec-0004](./dec-0004-standalone-gitlab-repo.md)
- **日期**：2026-06-27（superseded 2026-06-29）
- **关联**：v0.2.0 生产级整改

## 背景

`product-delivery-skill` 目录位于 `codex-workspace/ai-workspace/skills/product-delivery-skill/` 下，但 codex-workspace 主仓 HEAD 只追踪 `ai-workspace/ai-projects/` 子树，整个 skill 目录处于 untracked 状态（约 200+ 文件）。

整改过程中（v0.2.0），曾尝试在 worktree 分支 `claude/suspicious-villani-df9f7a` 上做 `git add` + commit + push，但因下列原因决定**暂不入库**：

1. 一次性 `git add` 200+ 文件等同于"首次入库"，超出本轮整改授权范围
2. skill 目录历史一直以"独立技能包 + 工作目录"形式协作，commit 时机需先与"是否在 codex-workspace 主仓托管 skill 包"做出整体决策
3. 多个 worktree 同时在线（54+），将该目录入库可能干扰其它分支的 working tree

## 决策

**暂不在 codex-workspace 主仓追踪本 skill 目录。** 改动以本地文件持久化形式生效，由用户决定何时单独建仓或并入主仓。

## 何时重新评估

任一条件触发即重新评估：

- 准备公开发布（必须落 git 历史）
- 多人协作（必须有 commit 责任链）
- 准备做对外 PR
- skill 包内出现重大破坏性变更，需要可回滚

## 短期权宜

- 本地改动可通过 `tar -czf` 或文件级备份保护
- 重要决策走 `governance/decisions/` 保留意图记录
- 版本号通过 `SKILL.md` frontmatter `version:` + `CHANGELOG.md` 双轨记录

## 影响

- `governance/health-check.md` 第 5 节"治理与版本"中"PR / commit"字段当前为"N/A"
- `README.md` 的"版本与治理"段已说明此状态
