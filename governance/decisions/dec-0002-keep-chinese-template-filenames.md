# Decision 0002 — 保留中文模板文件名

- **日期**：2026-06-27
- **状态**：accepted
- **关联整改**：v0.2.0 生产级整改

## 背景

`shared/templates/` 下的产物模板文件大量使用中文文件名（如 `需求文档.md`、`QA验收报告.md`、`UI交互设计规范.md` 等）。在某些终端用 `cat -v` 或非 UTF-8 locale 查看时，会显示为 `M-eM-^FM-^R...` 之类的 escape 序列，可能被误判为"乱码"。

## 决策

**保留中文模板文件名，不改为英文 slug。**

## 理由

1. **21 项标准产物的命名约定一致性**
   - README.md / SKILL.md / `shared/templates/README.md` / `init-request.py` / `stage-gate.py` / `examples/historical-runs/` 全部引用中文名
   - 改名会同步破坏阅读路径、脚本、历史归档对齐
2. **中文名在交付现场更易读**
   - 真实运行的 request 目录给中国团队 PM / QA / 设计直接阅读
   - 英文 slug（如 `requirement-doc.md`）反而需要二次心理映射
3. **文件名本身是合法 UTF-8**
   - `python3 -c "import os; print(repr(os.listdir(...)))"` 能正确读出中文
   - `ls --quoting-style=literal` 或现代终端均能直接显示
   - "乱码"是 `cat -v` / `od -c` 的可视化产物，不是文件系统损坏

## 验证

```bash
# 任意现代终端
ls shared/templates/qa/
# QA验收报告.md  UI验收报告.md  ...

# 编程方式确认
python3 -c "
import os
print([f for f in os.listdir('shared/templates/qa')])
"
```

## 何时重新评估

- 若未来要把 skill 包面向纯英文团队对外开源，再考虑提供英文别名层（不动现有中文主名）
- 若 CI 环境出现 locale 编码问题，优先解决环境而不是改文件名
