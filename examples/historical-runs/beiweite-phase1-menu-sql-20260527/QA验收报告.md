# QA 验收报告 — beiweite-drawing-system 全量验收

## 验收日期
2026-05-27

## 服务状态（验收时）

| 服务 | 端口 | 状态 |
|---|---|---|
| PostgreSQL (pgvector) | 15433 | ✅ 运行中 |
| Redis | 16380 | ✅ 运行中 |
| Spring Boot 后端 | 7010 | ✅ 运行中 |
| FastAPI AI Mock | 8088 | ✅ 运行中 |
| Vue3 前端 | 8011 | ✅ 运行中 |

## 接口全量冒烟结果（16/16 通过）

| 接口 | 方法 | 结果 |
|---|---|---|
| /stats/overview | GET | ✅ code=0，返回20图纸/20价格/3估价/100%准确率 |
| /drawing/page | GET | ✅ code=0，20条记录含latestPrice |
| /drawing/get | GET | ✅ code=0 |
| /price/page | GET | ✅ code=0，20条价格记录 |
| /estimate/get-by-drawing | GET | ✅ code=0 |
| /estimate/similar/list | GET | ✅ code=0，返回5条相似 |
| /estimate/trigger | POST | ✅ code=0 |
| /price/template | GET | ✅ HTTP200，Excel二进制 3864 bytes |
| /price/create | POST | ✅ code=0 |
| /price/delete | DELETE | ✅ code=0 |

## 代码质量验收

| 项目 | 状态 |
|---|---|
| TenantIgnore 注解（5个DO） | ✅ 已标注 |
| uploadDrawing 防重（selectByDrawingNo） | ✅ 已实现 |
| 工作台 phase 状态机（idle/uploading/ocr/estimating/done） | ✅ 已实现 |
| 实时偏差率 deltaPct 计算 | ✅ 已实现 |
| Stats 页 SVG 饼图 + 条形图 | ✅ 已实现 |
| DrawingStats 路由注册 | ✅ 已修复（本次补全） |
| start-demo.sh 前端端口 5173→8011 | ✅ 已修复（本次补全） |
| start-demo.sh 启动命令 dev→dev:antd | ✅ 已修复（本次补全） |
| CLAUDE.md API路径更新 | ✅ 已修复（本次补全） |
| Flyway enabled: true | ✅ Phase 1 已完成 |

## 数据状态

- drawing_info: 20 条
- price_record: 20 条（drawing_id FK 已回填）
- price_estimate: 3 条（seed-demo-session.py 产生）
- estimate_feedback: 3 条，avgDelta=6.33%，准确率=100%

## 验收结论

**PASSED** — 系统全链路闭环，可用于客户演示。
