#!/usr/bin/env python3
"""
product-delivery-skill health-check

把 governance/health-check.md 的 6 节脚本化。

用法:
    python3 shared/scripts/health-check.py                  # 全量，人类可读 + JSON
    python3 shared/scripts/health-check.py --json           # 只输出 JSON（CI 友好）
    python3 shared/scripts/health-check.py --section structure  # 只跑一节
    python3 shared/scripts/health-check.py --fail-on-warn   # warn 也算失败

退出码:
    0  全部通过
    1  存在 FAIL
    2  存在 WARN 且开启 --fail-on-warn
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class Check:
    section: str
    name: str
    status: str  # PASS / WARN / FAIL
    detail: str = ""


@dataclass
class Report:
    checks: list[Check] = field(default_factory=list)

    def add(self, section: str, name: str, status: str, detail: str = "") -> None:
        self.checks.append(Check(section, name, status, detail))

    def summary(self) -> dict[str, int]:
        s = {"PASS": 0, "WARN": 0, "FAIL": 0}
        for c in self.checks:
            s[c.status] = s.get(c.status, 0) + 1
        return s


# ---------- section 1: structure ----------

def section_structure(rep: Report) -> None:
    sec = "1.structure"
    files = {
        "root SKILL.md ≤ 50": (ROOT / "SKILL.md", 50),
        "root README.md exists": (ROOT / "README.md", None),
        "main SKILL ≤ 120": (ROOT / "skills/product-delivery-skill/SKILL.md", 120),
        "methods SKILL exists": (ROOT / "skills/product-delivery-methods/SKILL.md", None),
        "START-HERE exists": (ROOT / "START-HERE.md", None),
    }
    for name, (path, line_cap) in files.items():
        if not path.exists():
            rep.add(sec, name, "FAIL", f"missing: {path.relative_to(ROOT)}")
            continue
        if line_cap is None:
            rep.add(sec, name, "PASS")
            continue
        lines = sum(1 for _ in path.open(encoding="utf-8"))
        if lines <= line_cap:
            rep.add(sec, name, "PASS", f"{lines} lines")
        else:
            rep.add(sec, name, "FAIL", f"{lines} lines > {line_cap}")


# ---------- section 2: token hygiene ----------

def section_token(rep: Report) -> None:
    sec = "2.token"

    # workspace/requests should be empty (only .gitkeep)
    wr = ROOT / "workspace/requests"
    if wr.exists():
        leftovers = [p.name for p in wr.iterdir() if p.name != ".gitkeep"]
        if leftovers:
            rep.add(sec, "workspace/requests is clean", "WARN",
                    f"leftover: {leftovers}")
        else:
            rep.add(sec, "workspace/requests is clean", "PASS")
    else:
        rep.add(sec, "workspace/requests exists", "FAIL", "directory missing")

    # historical-runs has README
    hr = ROOT / "examples/historical-runs"
    if hr.exists() and (hr / "README.md").exists():
        rep.add(sec, "historical-runs/README.md", "PASS")
    else:
        rep.add(sec, "historical-runs/README.md", "FAIL")

    # spec-open-source-readme-template not in "必读" list of main SKILL
    main_skill = ROOT / "skills/product-delivery-skill/SKILL.md"
    if main_skill.exists():
        text = main_skill.read_text(encoding="utf-8")
        # extract section between "## 必读" and next "##"
        m = re.search(r"## 必读[\s\S]*?(?=\n## )", text)
        required_block = m.group(0) if m else ""
        if "spec-open-source-readme-template" in required_block:
            rep.add(sec, "heavy spec not in required list", "FAIL",
                    "spec-open-source-readme-template.md 出现在必读")
        else:
            rep.add(sec, "heavy spec not in required list", "PASS")


# ---------- section 3: assets ----------

ARTIFACT_TEMPLATES = [
    "shared/templates/request/需求总览.md",
    "shared/templates/request/需求文档.md",
    "shared/templates/request/manifest.json",
    "shared/templates/request/stage-status.json",
    "shared/templates/design/DESIGN.md",
    "shared/templates/design/技术方案.md",
    "shared/templates/design/UI交互设计规范.md",
    "shared/templates/design/任务分解.md",
    "shared/templates/control/实现控制总表.md",
    "shared/templates/control/页面接口验收总表.md",
    "shared/templates/qa/开发放行报告.md",
    "shared/templates/qa/覆盖率报告.md",
    "shared/templates/qa/前端关键流程覆盖清单.md",
    "shared/templates/qa/代码审查报告.md",
    "shared/templates/qa/冒烟测试脚本.sh",
    "shared/templates/qa/冒烟测试报告.md",
    "shared/templates/qa/测试用例.md",
    "shared/templates/qa/QA验收报告.md",
    "shared/templates/qa/UI验收报告.md",
    "shared/templates/qa/产品验收报告.md",
    "shared/templates/release/发布记录.md",
]


def section_assets(rep: Report) -> None:
    sec = "3.assets"
    missing = [p for p in ARTIFACT_TEMPLATES if not (ROOT / p).exists()]
    if missing:
        rep.add(sec, "21 artifact templates", "FAIL",
                f"missing: {missing}")
    else:
        rep.add(sec, "21 artifact templates", "PASS",
                f"all {len(ARTIFACT_TEMPLATES)} present")

    profiles_dir = ROOT / "profiles"
    if not profiles_dir.exists():
        rep.add(sec, "profiles/", "FAIL", "missing")
        return
    for p in sorted(profiles_dir.iterdir()):
        if not p.is_dir():
            continue
        readme = p / "README.md"
        yaml = p / "profile.yaml"
        if readme.exists() and yaml.exists():
            rep.add(sec, f"profile {p.name}", "PASS")
        else:
            missing_bits = []
            if not readme.exists():
                missing_bits.append("README.md")
            if not yaml.exists():
                missing_bits.append("profile.yaml")
            rep.add(sec, f"profile {p.name}", "FAIL", f"missing {missing_bits}")


# ---------- section 4: scripts runnable ----------

def section_scripts(rep: Report) -> None:
    sec = "4.scripts"
    tmp_root = Path(tempfile.mkdtemp(prefix="pd-hc-"))
    try:
        # doctor docs
        r = subprocess.run(
            ["bash", "install/doctor.sh", "--capability", "docs"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        rep.add(sec, "doctor docs", "PASS" if r.returncode == 0 else "FAIL",
                r.stdout.strip().splitlines()[-1] if r.stdout else "")

        # init-request
        r = subprocess.run(
            ["python3", "shared/scripts/init-request.py",
             "--request-key", "hc-smoke", "--title", "health-check",
             "--workspace", str(tmp_root)],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0 and (tmp_root / "hc-smoke").exists():
            rep.add(sec, "init-request", "PASS")
        else:
            rep.add(sec, "init-request", "FAIL", r.stderr.strip()[:200])
            return

        # stage-gate requirement
        r = subprocess.run(
            ["python3", "shared/scripts/stage-gate.py",
             "--request-dir", str(tmp_root / "hc-smoke"),
             "--stage", "requirement"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        # ok if exits 0 OR prints a JSON status (even if pass=false)
        if r.returncode == 0 or ('"pass"' in r.stdout):
            rep.add(sec, "stage-gate runnable", "PASS")
        else:
            rep.add(sec, "stage-gate runnable", "FAIL", r.stderr.strip()[:200])

        # readme-gate --help
        r = subprocess.run(
            ["python3", "shared/scripts/readme-gate.py", "--help"],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
        rep.add(sec, "readme-gate --help", "PASS" if r.returncode == 0 else "FAIL")
    finally:
        # best-effort cleanup
        try:
            import shutil
            shutil.rmtree(tmp_root, ignore_errors=True)
        except Exception:
            pass


# ---------- section 5: governance ----------

def section_governance(rep: Report) -> None:
    sec = "5.governance"
    changelog = ROOT / "governance/CHANGELOG.md"
    main_skill = ROOT / "skills/product-delivery-skill/SKILL.md"

    if not changelog.exists():
        rep.add(sec, "CHANGELOG.md exists", "FAIL")
        return
    rep.add(sec, "CHANGELOG.md exists", "PASS")

    # extract version from SKILL frontmatter
    version = None
    if main_skill.exists():
        text = main_skill.read_text(encoding="utf-8")
        m = re.search(r"^version:\s*([0-9][0-9a-zA-Z.\-]*)", text, re.MULTILINE)
        if m:
            version = m.group(1)
    if not version:
        rep.add(sec, "SKILL frontmatter version", "FAIL", "no version: line")
    else:
        cl_text = changelog.read_text(encoding="utf-8")
        if f"v{version}" in cl_text or version in cl_text:
            rep.add(sec, "version in CHANGELOG", "PASS", f"v{version}")
        else:
            rep.add(sec, "version in CHANGELOG", "WARN",
                    f"version {version} not found in CHANGELOG")

    # decisions have status
    dec_dir = ROOT / "governance/decisions"
    if dec_dir.exists():
        for d in sorted(dec_dir.glob("*.md")):
            t = d.read_text(encoding="utf-8", errors="ignore").lower()
            if any(s in t for s in ("accepted", "superseded", "deprecated", "proposed")):
                rep.add(sec, f"decision {d.name} has status", "PASS")
            else:
                rep.add(sec, f"decision {d.name} has status", "WARN", "no status: line")

    # vendor-skills.yaml structurally complete
    vendor = ROOT / "governance/vendor-skills.yaml"
    if vendor.exists():
        text = vendor.read_text(encoding="utf-8")
        ok = all(k in text for k in ("source", "license", "commit"))
        rep.add(sec, "vendor-skills.yaml fields", "PASS" if ok else "WARN",
                "missing one of source/license/commit" if not ok else "")


# ---------- section 6: link spot-check ----------

def section_links(rep: Report) -> None:
    sec = "6.links"
    hr = ROOT / "examples/historical-runs"
    sample_dir = None
    if hr.exists():
        for p in sorted(hr.iterdir()):
            if p.is_dir() and any(p.iterdir()):
                sample_dir = p
                break
    if sample_dir is None:
        rep.add(sec, "historical-runs sample", "WARN", "no non-empty historical run")
    else:
        artifact_count = sum(1 for f in sample_dir.iterdir() if f.is_file())
        rep.add(sec, f"sample {sample_dir.name} has artifacts", "PASS",
                f"{artifact_count} files")

    # spot-check one profile workspace_dir reachable (only on this user's machine)
    profiles_dir = ROOT / "profiles"
    if profiles_dir.exists():
        for p in sorted(profiles_dir.iterdir()):
            yaml = p / "profile.yaml"
            if not yaml.exists():
                continue
            text = yaml.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"workspace_dir:\s*(\S+)", text)
            if not m:
                continue
            raw_target = m.group(1).strip().strip('"').strip("'")
            if (
                raw_target.startswith("<")
                or raw_target.startswith("${")
                or raw_target.startswith("$")
                or raw_target.startswith("./")
            ):
                rep.add(sec, f"profile {p.name} workspace placeholder", "PASS",
                        raw_target)
                continue
            target = Path(raw_target)
            if target.exists():
                rep.add(sec, f"profile {p.name} workspace reachable", "PASS")
            else:
                rep.add(sec, f"profile {p.name} workspace reachable", "WARN",
                        f"path not found: {target}")


# ---------- main ----------

SECTIONS = {
    "structure": section_structure,
    "token": section_token,
    "assets": section_assets,
    "scripts": section_scripts,
    "governance": section_governance,
    "links": section_links,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true",
                    help="only emit JSON to stdout")
    ap.add_argument("--section", choices=list(SECTIONS),
                    help="run a single section")
    ap.add_argument("--fail-on-warn", action="store_true",
                    help="exit non-zero if any WARN")
    args = ap.parse_args()

    rep = Report()
    sections = [args.section] if args.section else list(SECTIONS)
    for s in sections:
        SECTIONS[s](rep)

    summary = rep.summary()
    out = {
        "summary": summary,
        "checks": [asdict(c) for c in rep.checks],
    }

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for c in rep.checks:
            tag = {"PASS": "✓", "WARN": "!", "FAIL": "✗"}.get(c.status, "?")
            line = f"[{tag}] {c.section} :: {c.name}"
            if c.detail:
                line += f"  ({c.detail})"
            print(line)
        print()
        print(f"summary: PASS={summary['PASS']}  WARN={summary['WARN']}  FAIL={summary['FAIL']}")

    if summary["FAIL"]:
        return 1
    if args.fail_on_warn and summary["WARN"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
