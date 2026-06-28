# Workflow: 新项目初始化

> 适用场景：使用 product-delivery-skill 接入一个全新项目，为其创建标准 docs/ 文档骨架。

---

## 触发条件

用户说：「创建新项目」、「为 XXX 项目初始化文档」、「新项目用 product-delivery-skill」。

---

## 执行步骤

### Step 1 — 确认 profile

检查 `profiles/{项目名}/profile.yaml` 是否存在：
- 已存在 → 直接读取
- 不存在 → 按以下字段创建（参考 `profiles/haloo/profile.yaml`）：
  - `name`, `project_name`, `brand_name`
  - `workspace_dir`, `docs_dir`
  - `database`, `cache`
  - `docs_layout: consolidated`
  - `tech_stack`, `ports`, `modes`

### Step 2 — 运行初始化脚本

```bash
python3 shared/scripts/init-project-docs.py \
  --project-dir <workspace_dir> \
  --project-name "<project_name>"
```

脚本会在 `<workspace_dir>/docs/` 下创建：

```
docs/
├── INDEX.md                  # 文档导航索引
├── 需求/
│   ├── 需求总览.md
│   └── 需求文档.md
├── 设计/
│   ├── DESIGN.md
│   └── UI交互设计规范.md
├── 技术/
│   ├── 系统架构总览.md       # 自动生成骨架
│   ├── 技术方案.md
│   └── 任务分解.md
└── 交付/
    ├── 实现控制总表.md
    ├── 开发放行报告.md
    ├── 代码审查报告.md
    ├── 冒烟测试报告.md
    ├── QA验收报告.md
    ├── UI验收报告.md
    ├── 产品验收报告.md
    └── 发布记录.md
```

### Step 3 — 生成手绘风格架构图（必做）

> 风格规范详见：`../../shared/references/architecture-image-style.md`
> 风格来源：`memory/logs/2026-05-09-hand-drawn-architecture-style-preference.md`

架构图默认采用**手绘草图风格**，使用 nano-banana-pro（Google Gemini 3 Pro Image API）生成。

#### 3.1 写 prompt 文件

在 `docs/技术/` 下创建两个 prompt 文件（替换项目内容）：
- `arch-prompt-frontend.txt` — 前端技术架构 prompt
- `arch-prompt-backend.txt` — 后端技术架构 prompt

**必用风格关键词（每个 prompt 都必须包含）：**
```
Hand-drawn whiteboard sketch architecture diagram.
Style: warm off-white beige background #faf7f0, hand-drawn marker borders,
doodle arrows, uneven rounded rectangles, colored pencil section fills,
graph paper texture, classroom poster feel, sketch pen Chinese labels.
...（内容描述）...
Hand-drawn aesthetic, no corporate polish, pen-on-paper feeling.
```

**禁用关键词：** `corporate infographic, glossy, neon, gradient-heavy, 3D render`

参考完整模板：`../../shared/references/architecture-image-style.md`

#### 3.2 运行生成命令

```bash
SCRIPT="$HOME/.openclaw/skills/nano-banana-pro/scripts/generate_image.py"
TS=$(date +%Y-%m-%d-%H-%M-%S)
PROJECT="{项目名}"   # 替换为实际项目名

# 前端架构图
GEMINI_API_KEY="$(grep GEMINI_API_KEY ~/.zprofile | cut -d'"' -f2)" \
uv run "$SCRIPT" \
  --prompt "$(cat docs/技术/arch-prompt-frontend.txt)" \
  --filename "${TS}-${PROJECT}-frontend-arch.png" \
  --resolution 2K --aspect-ratio 16:9

# 后端架构图
GEMINI_API_KEY="$(grep GEMINI_API_KEY ~/.zprofile | cut -d'"' -f2)" \
uv run "$SCRIPT" \
  --prompt "$(cat docs/技术/arch-prompt-backend.txt)" \
  --filename "${TS}-${PROJECT}-backend-arch.png" \
  --resolution 2K --aspect-ratio 16:9
```

#### 3.3 复制产物到 docs/技术/

生成后从 `~/generated_images/` 移动到项目：
```bash
cp ~/generated_images/${TS}-${PROJECT}-frontend-arch.png docs/技术/
cp ~/generated_images/${TS}-${PROJECT}-backend-arch.png docs/技术/
```

#### 3.4 Gemini 配额不足时的降级方案

若遇 `429 RESOURCE_EXHAUSTED`：
1. **等待重置**：免费配额每日重置，48s 后可重试（小批量）
2. **draw.io sketch 降级**：用 bruce-drawio skill 生成 `.drawio`，加 `sketch=1;roughness=1;` style，暖背景色 `#faf7f0`，CLI 导出 PNG：
   ```bash
   /Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --scale 2 \
     -o docs/技术/{项目名}-backend-arch-sketch.png \
     docs/技术/{项目名}-backend-arch-sketch.drawio
   ```
3. prompt 文件已保存，配额恢复后直接重新执行 Step 3.2

### Step 4 — 更新知识库

在共享知识库创建项目初始化条目：
- 路径：`/Users/qierkang/.obsidian/obsidian-wiki/wiki/synthesis/{项目名}-项目初始化-{YYYY-MM-DD}.md`
- 参考 `haloo-项目初始化-2026-05-30.md` 的格式

### Step 5 — 进入需求阶段

docs/ 骨架生成后，直接进入标准链路：
`需求分析 → 技术方案 → UI方案 → 任务分解 → 开发 → 自测 → 审查 → 冒烟 → 验收 → 发布`

---

## Consolidated vs REQUEST_DIR 对比

| 维度 | 旧结构（REQUEST_DIR） | 新结构（docs/） |
|---|---|---|
| 适用 | 单次需求迭代 | 新项目全量文档 |
| 脚本 | `init-request.py` | `init-project-docs.py` |
| 目录 | `REQUEST_DIR/{key}/` | `{project}/docs/需求|设计|技术|交付/` |
| 导航 | manifest.json | docs/INDEX.md |
| 并存 | ✅ 两套可同时使用 | ✅ 同一项目可以同时有两套 |

旧结构（init-request.py）用于需求变更迭代，新结构（init-project-docs.py）用于新项目初始化，两者不冲突。

---

## 验证清单

- [ ] `profiles/{名}/profile.yaml` 已创建
- [ ] `docs/INDEX.md` 可读
- [ ] `docs/需求/需求总览.md` 存在
- [ ] `docs/技术/系统架构总览.md` 存在
- [ ] `docs/技术/arch-prompt-frontend.txt` 已创建（手绘图 prompt）
- [ ] `docs/技术/arch-prompt-backend.txt` 已创建（手绘图 prompt）
- [ ] `docs/技术/{项目名}-frontend-arch.png` 已生成（或已记录待 Gemini 配额恢复后生成）
- [ ] `docs/技术/{项目名}-backend-arch.png` 已生成（或已记录待 Gemini 配额恢复后生成）
- [ ] `docs/交付/发布记录.md` 存在
- [ ] 知识库条目已创建
