# 架构图手绘风格规范

> 建立日期：2026-05-09（来源：memory/logs/2026-05-09-hand-drawn-architecture-style-preference.md）
> 更新：2026-05-30（接入 new-project.md 初始化流程）

---

## 风格定位

所有新项目的架构图默认采用**手绘草图风格（Hand-drawn Whiteboard Sketch）**，
而非现代扁平化信息图风格。

参考样本：
- `picasso-dev-skill/assets/architecture/workflow-architecture.png`
- `product-delivery-skill/assets/architecture/workflow-architecture.png`

---

## 必用关键词（生成 prompt 时必须包含）

```
hand-drawn marker sketch, graph paper background, doodle arrows,
uneven rounded rectangles, colored pencil fills, classroom poster feel,
warm off-white beige background #faf7f0, pen-on-paper feeling,
bold Chinese section labels, sketch pen text
```

## 禁用关键词（生成 prompt 时必须排除）

```
corporate infographic, glossy, neon, gradient-heavy, 3D render,
flat design, modern UI, polished, vector clean
```

---

## 生成工具

**优先工具：nano-banana-pro（Google Gemini 3 Pro Image API）**

```bash
uv run ~/.openclaw/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "<STYLE_KEYWORDS> + <CONTENT_DESCRIPTION>" \
  --filename "<TIMESTAMP>-<project>-<type>-arch.png" \
  --resolution 2K \
  --aspect-ratio 16:9
```

- 分辨率：`2K`（架构图默认）
- 宽高比：`16:9`（横版架构图）
- 文件名格式：`YYYY-MM-DD-HH-MM-SS-{project}-{frontend|backend}-arch.png`
- 落盘位置：`docs/技术/` 目录下

---

## Prompt 模板（可直接复用）

### 通用骨架

```
Hand-drawn whiteboard sketch architecture diagram.
Title at top: "{项目名} · {前端|后端}技术架构".
Style: warm off-white beige background #faf7f0, hand-drawn marker borders,
doodle arrows, uneven rounded rectangles, colored pencil section fills,
graph paper texture, classroom poster feel, sketch pen Chinese labels.
Layout: {N} horizontal layers with bold Chinese label on left, content blocks on right.
{逐层描述：Layer N "层名": 组件1, 组件2, ...}
Right vertical sidebar "{侧边栏标题}" with red/green dashed border: 条目1, 条目2, ...
Hand-drawn aesthetic, no corporate polish, pen-on-paper feeling.
```

### 前端架构模板变量说明

| 变量 | 说明 | 示例 |
|---|---|---|
| `{项目名}` | 项目中文/英文名 | Haloo |
| `N 层描述` | 从接入层→场景层→状态层→业务层→构建层 | 见下方示例 |
| 右侧栏 | 跨切关注点 | JWT Auth, WebSocket心跳 |

### 后端架构模板变量说明

| 变量 | 说明 | 示例 |
|---|---|---|
| `{项目名}` | 项目中文/英文名 | Haloo |
| `N 层描述` | 从接入层→网关层→控制层→服务层→数据层→基础设施层 | 见下方示例 |
| 右侧栏 | DevOps 运维关注点 | Nginx, Docker, CI/CD |

---

## 完整 Prompt 示例（haloo 前端）

```
Hand-drawn whiteboard sketch architecture diagram. Title at top: 'Haloo · 前端技术架构'.
Style: warm off-white beige background #faf7f0, hand-drawn marker borders, doodle arrows,
uneven rounded rectangles, colored pencil section fills, graph paper texture,
classroom poster feel, sketch pen Chinese labels.
Layout: 5 horizontal layers with bold Chinese label on left, content blocks on right.
Layer 1 '接入层': H5扫码入口, URL?v=venueId, 微信小程序(规划).
Layer 2 'H5沙盘层 haloo-venue': subgroup 'Phaser3场景引擎'(BootScene VenueScene UIScene Avatar RemotePlayer),
  subgroup '网络通信层'(SocketClient Socket.io WS_EVENTS types/index.ts).
Layer 3 '状态管理层': Pinia Store, 玩家状态缓存, 场馆信息缓存, Vue Router 4.
Layer 4 '管理后台层 haloo-admin': subgroup '业务模块'(商家管理 场景配置 数据统计 玩家管理),
  subgroup '基础框架'(Vben Admin 5 Ant Design Vue Axios).
Layer 5 '构建基础层': Vite 6, TypeScript 5, pnpm workspace, Node.js 20.
Right vertical sidebar '跨切关注点' with red dashed border:
  JWT Auth, WebSocket心跳, 响应式适配H5, 国际化i18n, 性能监控, PWA离线缓存.
Hand-drawn aesthetic, no corporate polish, pen-on-paper feeling.
```

## 完整 Prompt 示例（haloo 后端）

```
Hand-drawn whiteboard sketch architecture diagram. Title at top: 'Haloo · 后端技术架构'.
Style: warm off-white beige background #faf7f0, hand-drawn marker borders, doodle arrows,
uneven rounded rectangles, colored pencil section fills, graph paper texture,
classroom poster feel, sketch pen Chinese labels.
Layout: 6 horizontal layers with bold Chinese label on left, content blocks on right.
Layer 1 '客户端接入层': haloo-venue H5(Socket.io+Axios), haloo-admin(Axios REST), 第三方/OpenAPI.
Layer 2 '网关过滤层': Spring Security, JwtAuthFilter, CORS Filter, Rate Limiter.
Layer 3 '控制层': subgroup 'REST Controllers'(VenueController PlayerController AuthController),
  subgroup 'WebSocket Handlers'(GameRoomHandler ChatMessageHandler Socket.io Namespace /venue).
Layer 4 '服务层': VenueService, PlayerService, RoomService, TokenService(JWT), NotifyService, CacheService.
Layer 5 '数据访问层': subgroup 'PostgreSQL·JPA/MyBatis-Plus'(haloo_venue haloo_player system_*芋道底座),
  subgroup 'Redis·在线玩家缓存'(haloo:room:{venueId}:players Hash TTL3600s, token:blacklist, Pub/Sub房间广播).
Layer 6 '基础设施层': Java 21(LTS), Spring Boot 3.5, Docker Compose, Actuator/health.
Right vertical sidebar 'DevOps运维' with green dashed border:
  Nginx反向代理, Docker Compose, 日志ELK/本地, Actuator监控, CI/CD Pipeline, 数据库备份策略.
Hand-drawn aesthetic, no corporate polish, pen-on-paper feeling.
```

---

## 快速生成命令（复制即用）

```bash
SCRIPT="$HOME/.openclaw/skills/nano-banana-pro/scripts/generate_image.py"
TS=$(date +%Y-%m-%d-%H-%M-%S)
PROJECT="your-project"   # 替换项目名
DOCS="./docs/技术"       # 替换为项目 docs/技术 目录

# 前端架构图
uv run "$SCRIPT" \
  --prompt "$(cat ./docs/技术/arch-prompt-frontend.txt)" \
  --filename "${TS}-${PROJECT}-frontend-arch.png" \
  --resolution 2K --aspect-ratio 16:9

# 后端架构图
uv run "$SCRIPT" \
  --prompt "$(cat ./docs/技术/arch-prompt-backend.txt)" \
  --filename "${TS}-${PROJECT}-backend-arch.png" \
  --resolution 2K --aspect-ratio 16:9
```

> **提示**：把 prompt 内容提前存入 `docs/技术/arch-prompt-frontend.txt` 和 `arch-prompt-backend.txt`，
> 方便下次迭代时直接复用或调整。

---

## 验收标准

生成后目视检查：
- [ ] 背景是暖奶油色，不是纯白或深色
- [ ] 边框有手绘不规则感，不是完美圆角矩形
- [ ] 中文标签可读
- [ ] 整体有"白板草图"感，没有企业宣传图风格
- [ ] 图片分辨率 ≥ 2K，文字清晰不模糊
