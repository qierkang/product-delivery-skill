#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


TEMPLATE_MAP = {
    "00-需求总览.md": "request/需求总览.md",
    "需求文档.md": "request/需求文档.md",
    "manifest.json": "request/manifest.json",
    "DESIGN.md": "design/DESIGN.md",
    "技术方案.md": "design/技术方案.md",
    "UI交互设计规范.md": "design/UI交互设计规范.md",
    "服务端开发任务.md": "design/服务端开发任务.md",
    "任务分解.md": "design/任务分解.md",
    "实现控制总表.md": "control/实现控制总表.md",
    "页面接口验收总表.md": "control/页面接口验收总表.md",
    "开发放行报告.md": "qa/开发放行报告.md",
    "覆盖率报告.md": "qa/覆盖率报告.md",
    "前端关键流程覆盖清单.md": "qa/前端关键流程覆盖清单.md",
    "代码审查报告.md": "qa/代码审查报告.md",
    "冒烟测试脚本.sh": "qa/冒烟测试脚本.sh",
    "冒烟测试报告.md": "qa/冒烟测试报告.md",
    "测试用例.md": "qa/测试用例.md",
    "QA验收报告.md": "qa/QA验收报告.md",
    "UI验收报告.md": "qa/UI验收报告.md",
    "产品验收报告.md": "qa/产品验收报告.md",
    "发布记录.md": "release/发布记录.md",
}


def copy_templates(req_dir: Path) -> None:
    template_root = Path(__file__).resolve().parents[1] / "templates"
    for output_name, template_rel_path in TEMPLATE_MAP.items():
        output_path = req_dir / output_name
        if output_path.exists():
            continue
        template_path = template_root / template_rel_path
        output_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
        if output_path.suffix == ".sh":
            output_path.chmod(0o755)


def normalize_title(request_key: str, title: str) -> str:
    if title.strip():
        return title.strip()
    return request_key.replace("-", " ").strip()


def hydrate_manifest(
    req_dir: Path,
    request_key: str,
    title: str,
    owner: str,
    workflow: str,
    priority: str,
    platforms: list[str],
) -> None:
    manifest_path = req_dir / "manifest.json"
    if not manifest_path.exists():
        return
    now = datetime.now().isoformat(timespec="seconds")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["request_key"] = payload.get("request_key") or request_key
    payload["title"] = payload.get("title") or normalize_title(request_key, title)
    payload["owner"] = payload.get("owner") or owner
    payload["workflow"] = payload.get("workflow") or workflow
    payload["priority"] = payload.get("priority") or priority
    payload["platforms"] = payload.get("platforms") or platforms
    payload["status"] = payload.get("status") or "in_progress"
    payload["created_at"] = payload.get("created_at") or now
    payload["updated_at"] = now
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hydrate_stage_status(req_dir: Path, request_key: str) -> None:
    stage_status_path = req_dir / "stage-status.json"
    now = datetime.now().isoformat(timespec="seconds")
    if stage_status_path.exists():
        payload = json.loads(stage_status_path.read_text(encoding="utf-8"))
        payload["request_key"] = payload.get("request_key") or request_key
        payload["current_stage"] = payload.get("current_stage") or "requirement"
        payload["status"] = payload.get("status") or "IN_PROGRESS"
        payload["updated_at"] = now
        stage_status_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return

    stage_status = {
        "request_key": request_key,
        "current_stage": "requirement",
        "status": "IN_PROGRESS",
        "updated_at": now,
    }
    stage_status_path.write_text(
        json.dumps(stage_status, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-key", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--owner", default="xyqierkang@gmail（claude+codex）")
    parser.add_argument("--workflow", default="new-feature")
    parser.add_argument("--priority", default="P1")
    parser.add_argument("--platforms", default="web")
    args = parser.parse_args()

    req_dir = Path(args.workspace) / args.request_key
    req_dir.mkdir(parents=True, exist_ok=True)
    (req_dir / "assets").mkdir(exist_ok=True)
    (req_dir / "logs").mkdir(exist_ok=True)

    copy_templates(req_dir)
    platforms = [item.strip() for item in args.platforms.split(",") if item.strip()]
    hydrate_manifest(
        req_dir=req_dir,
        request_key=args.request_key,
        title=args.title,
        owner=args.owner,
        workflow=args.workflow,
        priority=args.priority,
        platforms=platforms or ["web"],
    )
    hydrate_stage_status(req_dir=req_dir, request_key=args.request_key)

    print(f"[init-request] ready: {req_dir}")


if __name__ == "__main__":
    main()
