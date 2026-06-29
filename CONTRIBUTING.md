# Contributing

## Local Validation

```bash
bash install/doctor.sh --capability docs
python3 shared/scripts/health-check.py
python3 shared/scripts/readme-gate.py --readme README.md
```

## Change Rules

- Keep the root `SKILL.md` focused on routing.
- Put reusable rules in `shared/` and project-specific values in `profiles/`.
- Do not commit credentials, customer data, local runtime artifacts, or real `.env` files.
- Include verification evidence for workflow, template, or gate changes.

## Pull Request Checklist

- [ ] Scope is documented.
- [ ] Validation commands pass.
- [ ] README and governance records are updated when behavior changes.
- [ ] No unrelated generated files are included.
