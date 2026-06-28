#!/usr/bin/env python3
"""
init-project-docs.py
新项目 docs/ 目录初始化脚本（consolidated layout）

用法：
  python3 init-project-docs.py --project-dir /path/to/project --project-name MyProject

说明：
  在 <project-dir>/docs/ 下创建标准四层结构并复制对应模板，同时生成架构图 prompt 骨架文件。

架构图生成（手绘风格）：
  脚本完成后在 docs/技术/ 会生成两个 prompt 模板文件：
    arch-prompt-frontend.txt  — 填入前端层次后用 nano-banana-pro 生成手绘架构图
    arch-prompt-backend.txt   — 填入后端层次后用 nano-banana-pro 生成手绘架构图
  风格规范见：shared/references/architecture-image-style.md
  生成命令见：shared/workflow/new-project.md Step 3

  风格来源：memory/logs/2026-05-09-hand-drawn-architecture-style-preference.md
  参考样本：
    picasso-dev-skill/assets/architecture/workflow-architecture.png
    product-delivery-skill/assets/architecture/workflow-architecture.png

  在 <project-dir>/docs/ 下创建标准四层结构并复制对应模板：
    docs/需求/   — 需求总览、需求文档
    docs/设计/   — DESIGN.md、UI交互设计规范
    docs/技术/   — 技术方案、任务分解、系统架构总览
    docs/交付/   — 实现控制总表、开发放行报告、代码审查报告、冒烟测试报告、QA/UI/产品验收报告、发布记录
    docs/INDEX.md — 导航索引

  与 init-request.py 的区别：
  - init-request.py  → 面向单次需求（在 REQUEST_DIR/{request-key}/ 下创建交付物）
  - init-project-docs.py → 面向新项目（在 <project>/docs/ 下一次性创建全量文档骨架）
"""
import argparse
from datetime import datetime
from pathlib import Path

# template_root 相对路径 → docs/ 下的目标路径
CONSOLIDATED_MAP = {
    "request/需求总览.md":          "需求/需求总览.md",
    "request/需求文档.md":          "需求/需求文档.md",
    "design/DESIGN.md":             "设计/DESIGN.md",
    "design/UI交互设计规范.md":      "设计/UI交互设计规范.md",
    "design/技术方案.md":           "技术/技术方案.md",
    "design/任务分解.md":           "技术/任务分解.md",
    "control/实现控制总表.md":       "交付/实现控制总表.md",
    "qa/开发放行报告.md":            "交付/开发放行报告.md",
    "qa/代码审查报告.md":            "交付/代码审查报告.md",
    "qa/冒烟测试报告.md":            "交付/冒烟测试报告.md",
    "qa/QA验收报告.md":              "交付/QA验收报告.md",
    "qa/UI验收报告.md":              "交付/UI验收报告.md",
    "qa/产品验收报告.md":            "交付/产品验收报告.md",
    "release/发布记录.md":           "交付/发布记录.md",
}

ARCH_OVERVIEW_TEMPLATE = """# 系统架构总览

> 生成时间：{date}
> 项目名：{project_name}

## 子包列表

| 子包 | 职责 | 端口 |
|---|---|---|
| （待填写） | | |

## 架构图（手绘风格）

- `{project_name}-frontend-arch.png` — 前端技术架构（手绘图，由 nano-banana-pro 生成）
- `{project_name}-backend-arch.png` — 后端技术架构（手绘图，由 nano-banana-pro 生成）
- `arch-prompt-frontend.txt` — 前端架构图生成 prompt（编辑后执行 Step 3.2）
- `arch-prompt-backend.txt` — 后端架构图生成 prompt（编辑后执行 Step 3.2）

> 生成方式见：shared/workflow/new-project.md Step 3
> 风格规范见：shared/references/architecture-image-style.md

## 核心数据流

（待填写）
"""

INDEX_TEMPLATE = """# {project_name} · 文档索引

> 生成时间：{date}

## 需求

- [需求总览](需求/需求总览.md)
- [需求文档](需求/需求文档.md)

## 设计

- [DESIGN.md（设计规范）](设计/DESIGN.md)
- [UI交互设计规范](设计/UI交互设计规范.md)

## 技术

- [系统架构总览](技术/系统架构总览.md)
- [技术方案](技术/技术方案.md)
- [任务分解](技术/任务分解.md)

## 交付

- [实现控制总表](交付/实现控制总表.md)
- [开发放行报告](交付/开发放行报告.md)
- [代码审查报告](交付/代码审查报告.md)
- [冒烟测试报告](交付/冒烟测试报告.md)
- [QA验收报告](交付/QA验收报告.md)
- [UI验收报告](交付/UI验收报告.md)
- [产品验收报告](交付/产品验收报告.md)
- [发布记录](交付/发布记录.md)
"""


def init_docs(project_dir: Path, project_name: str) -> None:
    docs_dir = project_dir / "docs"
    template_root = Path(__file__).resolve().parents[1] / "templates"
    now = datetime.now().strftime("%Y-%m-%d")

    # 创建四层目录
    for sub in ("需求", "设计", "技术", "交付"):
        (docs_dir / sub).mkdir(parents=True, exist_ok=True)

    # 复制模板（已存在则跳过）
    for template_rel, dest_rel in CONSOLIDATED_MAP.items():
        dest = docs_dir / dest_rel
        if dest.exists():
            continue
        src = template_root / template_rel
        if src.exists():
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            dest.write_text(f"# {dest.stem}\n\n（模板文件 {template_rel} 不存在，请手动补充）\n", encoding="utf-8")

    # 写架构图 prompt 骨架（手绘风格，已存在则跳过）
    fe_prompt = docs_dir / "技术/arch-prompt-frontend.txt"
    be_prompt = docs_dir / "技术/arch-prompt-backend.txt"
    if not fe_prompt.exists():
        fe_prompt.write_text(
            f"Hand-drawn whiteboard sketch architecture diagram. Title at top: '{project_name} · 前端技术架构'.\n"
            "Style: warm off-white beige background #faf7f0, hand-drawn marker borders, doodle arrows,\n"
            "uneven rounded rectangles, colored pencil section fills, graph paper texture,\n"
            "classroom poster feel, sketch pen Chinese labels.\n"
            "Layout: N horizontal layers with bold Chinese label on left, content blocks on right.\n"
            "Layer 1 '接入层': （填写接入方式）.\n"
            "Layer 2 '前端核心层': （填写核心框架和组件）.\n"
            "Layer 3 '状态管理层': （填写状态管理方案）.\n"
            "Layer 4 '业务层': （填写业务模块）.\n"
            "Layer 5 '构建基础层': （填写构建工具链）.\n"
            "Right vertical sidebar '跨切关注点' with red dashed border:\n"
            "  （填写跨切关注点）.\n"
            "Hand-drawn aesthetic, no corporate polish, pen-on-paper feeling.\n",
            encoding="utf-8",
        )
    if not be_prompt.exists():
        be_prompt.write_text(
            f"Hand-drawn whiteboard sketch architecture diagram. Title at top: '{project_name} · 后端技术架构'.\n"
            "Style: warm off-white beige background #faf7f0, hand-drawn marker borders, doodle arrows,\n"
            "uneven rounded rectangles, colored pencil section fills, graph paper texture,\n"
            "classroom poster feel, sketch pen Chinese labels.\n"
            "Layout: N horizontal layers with bold Chinese label on left, content blocks on right.\n"
            "Layer 1 '客户端接入层': （填写客户端类型）.\n"
            "Layer 2 '网关过滤层': （填写鉴权/过滤组件）.\n"
            "Layer 3 '控制层': （填写 Controller 和 Handler）.\n"
            "Layer 4 '服务层': （填写 Service 列表）.\n"
            "Layer 5 '数据访问层': （填写数据库和缓存）.\n"
            "Layer 6 '基础设施层': （填写运行时和部署）.\n"
            "Right vertical sidebar 'DevOps运维' with green dashed border:\n"
            "  （填写 DevOps 关注点）.\n"
            "Hand-drawn aesthetic, no corporate polish, pen-on-paper feeling.\n",
            encoding="utf-8",
        )

    # 写系统架构总览（总是生成，已存在则跳过）
    arch_path = docs_dir / "技术/系统架构总览.md"
    if not arch_path.exists():
        arch_path.write_text(
            ARCH_OVERVIEW_TEMPLATE.format(date=now, project_name=project_name),
            encoding="utf-8",
        )

    # 写 INDEX.md
    index_path = docs_dir / "INDEX.md"
    if not index_path.exists():
        index_path.write_text(
            INDEX_TEMPLATE.format(date=now, project_name=project_name),
            encoding="utf-8",
        )

    print(f"[init-project-docs] docs/ 初始化完成：{docs_dir}")
    print("  目录：需求/ 设计/ 技术/ 交付/ INDEX.md")
    print("  架构图 prompt：技术/arch-prompt-frontend.txt  技术/arch-prompt-backend.txt")
    print("  下一步：编辑 prompt 文件，再执行 shared/workflow/new-project.md Step 3 生成手绘架构图")


def main() -> None:
    parser = argparse.ArgumentParser(description="为新项目初始化 consolidated docs/ 结构")
    parser.add_argument("--project-dir", required=True, help="项目根目录路径")
    parser.add_argument("--project-name", default="新项目", help="项目显示名称")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists():
        print(f"[error] 项目目录不存在：{project_dir}")
        raise SystemExit(1)

    init_docs(project_dir, args.project_name)


if __name__ == "__main__":
    main()
