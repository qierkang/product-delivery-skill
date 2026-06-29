# Product Delivery Skill

[Simplified Chinese](../README.md) | English

> A model-agnostic delivery workflow with a single entry point, explicit stage gates, reusable artifacts, and auditable evidence.

![Product Delivery Skill Architecture](../assets/platform/architecture/en/product-delivery-skill-architecture.png)

## Overview

Product Delivery Skill turns a product request into a controlled delivery process covering requirements, design, implementation, review, smoke testing, QA, UI acceptance, product acceptance, and release.

## Core Capabilities

- Routes requests through one root `SKILL.md`
- Provides 21 reusable delivery artifact templates
- Enforces stage transitions with `stage-gate.py`
- Keeps project-specific rules in profiles
- Preserves evidence for review, acceptance, and release

## Quick Start

```bash
bash install/setup.sh
bash install/doctor.sh --capability docs
python3 shared/scripts/init-request.py \
  --request-key my-first-request \
  --workspace workspace/requests
python3 shared/scripts/stage-gate.py \
  --request-dir workspace/requests/my-first-request \
  --stage all
```

## Repository Layout

| Path | Purpose |
|---|---|
| `skills/` | Main workflow and method extensions |
| `shared/templates/` | Standard delivery artifacts |
| `shared/scripts/` | Initialization, gates, and validation |
| `profiles/` | Project-specific configuration |
| `governance/` | Decisions, changes, risks, and health checks |

## Validation

```bash
bash install/doctor.sh --capability docs
python3 shared/scripts/health-check.py
python3 shared/scripts/readme-gate.py --readme README.md
```

## License

Licensed under the [MIT License](../LICENSE).

## Maintainer

- Qierkang Qi
- `xyqierkang@gmail.com`
- https://github.com/qierkang
