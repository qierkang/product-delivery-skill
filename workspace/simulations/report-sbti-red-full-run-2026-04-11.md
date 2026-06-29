# sbti-red 全量模拟陪跑报告（2026-04-11）

作者：`xyqierkang@gmail（claude+codex）`

## 1. 本次模拟范围

- 使用技能包：`<path-to-product-delivery-skill>`
- 验证对象项目：`<path-to-sbti-red>`
- 模拟链路：
  1. `doctor` 四能力检查
  2. `init-request` 从零建单
  3. `stage-gate` 全阶段校验
  4. 项目级开源交付检查
  5. Docker 部署与访问验证

## 2. 执行证据

### 2.1 环境检查

- `bash install/doctor.sh --capability docs`：PASS
- `bash install/doctor.sh --capability dev`：PASS
- `bash install/doctor.sh --capability db`：PASS（MySQL/Redis 使用 Docker fallback 鉴权）
- `bash install/doctor.sh --capability deploy`：PASS

### 2.2 从零建单与 Gate

- 新建 request：`sbti-red-fullrun-2026-04-11-v2`
- 命令：
  - `python3 shared/scripts/init-request.py --request-key sbti-red-fullrun-2026-04-11-v2 --workspace workspace/requests --title 'SBTI RED 全量陪跑验证 v2' --owner 'xyqierkang@gmail（claude+codex）' --workflow 'new-feature' --priority 'P1' --platforms 'web,h5'`
  - `python3 shared/scripts/stage-gate.py --request-dir workspace/requests/sbti-red-fullrun-2026-04-11-v2 --stage all`
- 结果：`requirement/design/dev/review/smoke/qa/release` 全部 PASS

### 2.3 项目级检查

- 命令：
  - `python3 shared/scripts/project-ready-check.py --project-dir <path-to-sbti-red>`
- 结果：PASS（missing/issues 均为空）

### 2.4 部署与可访问性

- `bash <path-to-sbti-red>/deploy.sh`：成功
- 运行状态：
  - `sbti-red-web`：Up
  - `sbti-red-api`：Up
  - `sbti-red-mysql`：Up (healthy)
  - `sbti-red-redis`：Up (healthy)
- 访问验证：
  - `GET http://127.0.0.1:18081/health` => HTTP 200，`{"ok":true,"mysql":true,"redis":true,...}`
  - `GET http://127.0.0.1:18080` => HTTP 200

## 3. 本轮暴露问题与已修复项

### 问题 1：`init-request` 生成后首关直接失败

- 现象：`manifest.json` 的 `request_key/title/owner` 为空，`requirement` Gate 失败。
- 修复：
  - `shared/scripts/init-request.py` 新增参数与自动回填：
    - `--title --owner --workflow --priority --platforms`
  - 自动补齐 `manifest.json` 字段与时间戳
  - 自动更新 `stage-status.json` 的 `updated_at`

### 问题 2：缺少“一键全链路校验”命令

- 现象：原流程需逐阶段手动执行，陪跑复核效率低。
- 修复：
  - `shared/scripts/stage-gate.py` 新增 `--stage all`
  - 一次性输出所有阶段结果，失败返回非 0 退出码
  - 新增 `stage-status.json` 回写（当前阶段、状态、历史）

### 问题 3：模板与 Gate 规则不一致

- 现象：`前端关键流程覆盖清单` 模板缺少“列表/查询/新增/编辑”等关键词，`dev` Gate 会误卡。
- 修复：
  - 更新模板 `shared/templates/qa/frontend-keyflow-checklist.md`
  - 预置“列表/查询/新增/编辑/查看/删除”流程行

## 4. 从 picasso-dev-skill 提炼并落地的能力

- 已落地：
  - 阶段化硬 Gate（且支持全链路复核）
  - Gate 结果写回状态文件（可追踪）
  - 先 `doctor` 再执行主流程
- 建议下一步继续迁移：
  - `smoke` 阶段引入“真实脚本执行 + 日志落盘 + 超时控制”
  - `release` 阶段增加“回滚演练记录”硬性标记
  - 增加 `validate-artifacts.py` 风格的文档结构审计（元信息+证据块）

## 5. sbti-red 开源与商业化就绪结论

- 当前结论：**可进入 GitHub 开源第一版**，并可作为商业试点 MVP 持续迭代。
- 已补的开源项：
  - `CONTRIBUTING.md`
  - `README.md` 增加贡献入口
  - 清理 `.DS_Store` 与 `database/.idea` 噪音文件
  - `.gitignore` 增加 `**/.DS_Store` 与 `.idea/`
- 商业化支撑：
  - 已有 `docs/documents/spec-sbti-red-commercialization.md`
  - 数据链路（访问/事件/结果/在线）+ Docker 一键部署链路已实跑通过
