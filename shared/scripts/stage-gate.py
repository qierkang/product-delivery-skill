#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


REQUIRED_FILES = {
    "requirement": ["00-需求总览.md", "需求文档.md", "manifest.json"],
    "design": ["DESIGN.md", "技术方案.md", "UI交互设计规范.md", "任务分解.md"],
    "dev": [
        "实现控制总表.md",
        "页面接口验收总表.md",
        "开发放行报告.md",
        "覆盖率报告.md",
        "前端关键流程覆盖清单.md",
    ],
    "review": ["代码审查报告.md"],
    "smoke": ["冒烟测试脚本.sh", "冒烟测试报告.md"],
    "qa": ["测试用例.md", "QA验收报告.md"],
    "ui_acceptance": ["UI验收报告.md"],
    "product_acceptance": ["产品验收报告.md"],
    "release": ["发布记录.md", "stage-status.json"],
}

REQUIRED_MARKERS = {
    "00-需求总览.md": ["业务目标", "范围", "风险"],
    "需求文档.md": ["背景", "目标", "验收标准"],
    "DESIGN.md": [
        "Visual Theme & Atmosphere",
        "Color Palette & Roles",
        "Typography Rules",
        "Component Stylings",
        "Layout Principles",
        "Depth & Elevation",
        "Do's and Don'ts",
        "Responsive Behavior",
        "Agent Prompt Guide",
    ],
    "技术方案.md": ["架构", "数据设计", "接口设计"],
    "UI交互设计规范.md": ["风格方向", "设计 Token", "页面", "交互", "状态", "动效", "可访问性"],
    "任务分解.md": ["任务", "Gate", "回流"],
    "实现控制总表.md": ["需求", "字段", "状态"],
    "页面接口验收总表.md": ["页面", "接口", "验收"],
    "开发放行报告.md": ["结论", "证据"],
    "覆盖率报告.md": ["覆盖率", "结论"],
    "前端关键流程覆盖清单.md": ["列表", "查询", "新增", "编辑", "查看"],
    "代码审查报告.md": ["审查结论", "问题"],
    "冒烟测试报告.md": ["冒烟范围", "结论"],
    "测试用例.md": ["功能测试", "边界"],
    "QA验收报告.md": ["QA结论"],
    "UI验收报告.md": ["UI", "交互", "token", "动效", "是否UI验收通过"],
    "产品验收报告.md": ["业务验收"],
    "发布记录.md": ["发布前", "发布后", "回滚"],
}

STAGE_ORDER = [
    "requirement",
    "design",
    "dev",
    "review",
    "smoke",
    "qa",
    "ui_acceptance",
    "product_acceptance",
    "release",
]


def validate_markers(path: Path, markers: list[str]) -> list[str]:
    content = path.read_text(encoding="utf-8")
    issues: list[str] = []
    if len(content.strip()) < 80:
        issues.append(f"{path.name} 内容过少，疑似未填写")
    if path.suffix == ".md" and "#" not in content:
        issues.append(f"{path.name} 缺少 Markdown 标题结构")
    for marker in markers:
        if marker not in content:
            issues.append(f"{path.name} 缺少关键内容：{marker}")
    return issues


def validate_manifest(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [f"{path.name} 不是合法 JSON"]

    required_keys = ["request_key", "title", "owner", "workflow", "status"]
    for key in required_keys:
        if not payload.get(key):
            issues.append(f"{path.name} 缺少字段：{key}")
    return issues


def validate_stage_status(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [f"{path.name} 不是合法 JSON"]

    required_keys = ["request_key", "current_stage", "status", "updated_at"]
    for key in required_keys:
        if not payload.get(key):
            issues.append(f"{path.name} 缺少字段：{key}")
    if payload.get("current_stage") and payload.get("current_stage") not in STAGE_ORDER:
        issues.append(f"{path.name} current_stage 非法：{payload.get('current_stage')}")
    if payload.get("status") and payload.get("status") not in ["IN_PROGRESS", "PASSED", "FAILED"]:
        issues.append(f"{path.name} status 非法：{payload.get('status')}")
    return issues


def check_stage(request_dir: Path, stage: str) -> dict:
    missing = []
    issues: list[str] = []
    for file_name in REQUIRED_FILES[stage]:
        file_path = request_dir / file_name
        if not file_path.exists():
            missing.append(file_name)
            continue
        if file_name in REQUIRED_MARKERS:
            issues.extend(validate_markers(file_path, REQUIRED_MARKERS[file_name]))
        if file_name == "manifest.json":
            issues.extend(validate_manifest(file_path))
        if file_name == "stage-status.json":
            issues.extend(validate_stage_status(file_path))
    return {
        "stage": stage,
        "pass": len(missing) == 0 and len(issues) == 0,
        "missing": missing,
        "issues": issues,
    }


def upsert_stage_status(request_dir: Path, stage: str, passed: bool) -> None:
    stage_status_path = request_dir / "stage-status.json"
    now = datetime.now().isoformat(timespec="seconds")
    payload: dict = {}
    if stage_status_path.exists():
        try:
            payload = json.loads(stage_status_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}

    payload["request_key"] = payload.get("request_key") or request_dir.name
    payload["current_stage"] = stage
    payload["status"] = "PASSED" if passed else "FAILED"
    payload["updated_at"] = now

    history = payload.get("history")
    if not isinstance(history, list):
        history = []
    history.append({"stage": stage, "pass": passed, "checked_at": now})
    payload["history"] = history[-30:]

    stage_status_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-dir", required=True)
    parser.add_argument(
        "--stage",
        required=True,
        choices=STAGE_ORDER + ["all"],
    )
    args = parser.parse_args()

    request_dir = Path(args.request_dir)
    if args.stage == "all":
        results = [check_stage(request_dir, stage) for stage in STAGE_ORDER]
        final_result = {
            "stage": "all",
            "pass": all(item["pass"] for item in results),
            "results": results,
        }
        failed = [item for item in results if not item["pass"]]
        final_stage = failed[0]["stage"] if failed else STAGE_ORDER[-1]
        upsert_stage_status(request_dir=request_dir, stage=final_stage, passed=final_result["pass"])
        print(json.dumps(final_result, ensure_ascii=False))
        if not final_result["pass"]:
            raise SystemExit(2)
        return

    result = check_stage(request_dir, args.stage)
    upsert_stage_status(request_dir=request_dir, stage=args.stage, passed=result["pass"])
    print(json.dumps(result, ensure_ascii=False))
    if not result["pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
