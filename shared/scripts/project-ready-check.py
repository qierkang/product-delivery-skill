#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    ".env.example",
    "docker-compose.yml",
    "docker-compose.app.yml",
    "deploy.sh",
    "database/schema.sql",
    "apps/api/package.json",
    "apps/web/package.json",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    missing: list[str] = []
    issues: list[str] = []

    for rel_path in REQUIRED_FILES:
        if not (project_dir / rel_path).exists():
            missing.append(rel_path)

    readme_path = project_dir / "README.md"
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding="utf-8")
        for marker in ["项目目标", "技术栈", "快速开始", "一键部署", "API"]:
            if marker not in readme_content:
                issues.append(f"README.md 缺少关键章节：{marker}")

    schema_path = project_dir / "database/schema.sql"
    if schema_path.exists():
        schema_content = schema_path.read_text(encoding="utf-8")
        if "作者: xyqierkang@gmail（claude+codex）" not in schema_content:
            issues.append("schema.sql 缺少作者标记（xyqierkang@gmail（claude+codex））")
        if "COMMENT" not in schema_content.upper():
            issues.append("schema.sql 缺少注释定义（COMMENT）")

    deploy_path = project_dir / "deploy.sh"
    if deploy_path.exists() and not deploy_path.stat().st_mode & 0o111:
        issues.append("deploy.sh 不是可执行文件")

    result = {
        "project_dir": str(project_dir),
        "pass": len(missing) == 0 and len(issues) == 0,
        "missing": missing,
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False))
    if missing or issues:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
