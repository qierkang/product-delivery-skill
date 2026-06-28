# README 生成参考索引

本目录收口 GitHub 开源 README 的生成参考，供 `product-delivery-skill` 在文档生成、模板改写和开源发布场景中统一复用。

## 阅读顺序（按 token 成本递增）

| 层 | 文件 | 何时读 |
|---|------|--------|
| **必读 Hook**（≤120 行） | [core-sections.md](./core-sections.md) | **任何 README 任务都先读这一篇** |
| 主提示词 | [spec-open-source-readme-master-prompt.md](./spec-open-source-readme-master-prompt.md) | 准备让模型生成完整 README 时 |
| 风格参考 | [spec-open-source-readme-style-reference.md](./spec-open-source-readme-style-reference.md) | 需要精调信息密度 / 排版语气时 |
| 完整模板 | [spec-open-source-readme-template.md](./spec-open-source-readme-template.md) | 需要完整字段槽位 / 长样例时（444 行，按需展开） |

## 校验

```bash
python3 ../../scripts/readme-gate.py --readme <path-to-README.md>
```

## 工作流约定

- 这是 skill 包内的本地参考副本，不依赖 `docs/documents/` 的上层路径
- 如果模板被迁移到别的 skill 或别的仓库，优先连同本目录一起迁移
- 涉及 skill 包本身维护，按 `governance/` 规则补 CHANGELOG
