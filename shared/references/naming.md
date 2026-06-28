# 命名规范

> 命名是机器可读性的第一道关口。`init-request.py` / `stage-gate.py` / `readme-gate.py` 都会依赖这里的约定。

## 1. Request 目录

| 规则 | 示例 | 反例 |
|------|------|------|
| 必须 `kebab-case` | `beiweite-phase1-menu-sql-20260527` | `BeiweitePhase1`、`beiweite_phase_1` |
| 含日期时用 `YYYYMMDD` 后缀 | `sbti-red-fullrun-20260411` | `2026.04.11`、`apr-11` |
| 多版本同主题用 `-v2` 后缀 | `sbti-red-fullrun-20260411-v2` | `sbti-red-fullrun-20260411-rev2` |
| 长度 ≤ 60 字符 | 见上 | 写成一段话 |

**校验**：`init-request.py --request-key <key>` 会拒绝不合规命名。

## 2. 文档文件名

| 类型 | 命名约定 | 备注 |
|------|---------|------|
| 21 项标准产物 | 沿用中文固定名（`需求文档.md` / `QA验收报告.md` 等）| 见 [artifact-standard.md](./artifact-standard.md)，**不可改名** |
| 自定义补充文档 | `功能名-文档类型.md` | 例：`登录流程-状态机.md` |
| 临时调研 | `TMP-<主题>.md` | 项目交付前必须清理或并入正式产物 |
| 接口契约 | `api-<模块>.md` | 例：`api-auth.md` |
| 决策记录 | `dec-<4 位编号>-<主题>.md` | 放 `governance/decisions/` |

> 详见 [dec-0002-keep-chinese-template-filenames.md](../../governance/decisions/dec-0002-keep-chinese-template-filenames.md) 为什么 21 项产物名保留中文。

## 3. 脚本与代码

| 类型 | 前缀/约定 |
|------|----------|
| 一次性脚本 | `tmp-` 或 `util-`（用完即弃） |
| 长期工具脚本 | 无前缀，名词化（`stage-gate.py`、`init-request.py`） |
| 冒烟脚本 | 固定 `冒烟测试脚本.sh` |
| Python 函数 | `snake_case` |
| Python 类 | `PascalCase` |
| 常量 | `UPPER_SNAKE_CASE` |

## 4. 配置 / 数据文件

| 类型 | 命名 | 位置 |
|------|------|------|
| 菜单数据 | `MENU_DATA.md` | request 目录或 `shared/templates/config/` |
| 字典数据 | `DICT_DATA.md` | 同上 |
| SQL 变更 | `sql-change.sql` | 同上 |
| 机器元数据 | `manifest.json` | request 目录根 |
| 阶段状态机 | `stage-status.json` | request 目录根 |

## 5. 不允许的命名

- 含空格：`需求 文档.md`
- 含 emoji：`✅QA报告.md`
- 含中文标点：`需求文档（最终版）.md`
- 含版本时间但格式不一致：`需求文档-2026年4月11日.md`
- 文件名含 `final` / `最终` / `new` 字眼 — 用 `-v2` 取代

## 6. 强制校验入口

```bash
# 单 request 命名校验
python3 shared/scripts/init-request.py --request-key <key> --dry-run

# 全仓产物名核对（待 health-check.py 集成后用）
python3 shared/scripts/health-check.py --section naming
```
