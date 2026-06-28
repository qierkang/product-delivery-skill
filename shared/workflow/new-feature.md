# 新需求工作流

1. 执行环境预检：
   - `bash install/doctor.sh --capability docs`
   - `bash install/doctor.sh --capability dev`
   - `bash install/doctor.sh --capability db`
   - `bash install/doctor.sh --capability deploy`
2. 初始化 request：
   - `python3 shared/scripts/init-request.py --request-key <request-key> --workspace workspace/requests`
3. 完成 Requirement 产物并过 Gate：
   - `stage-gate.py --stage requirement`
4. 完成 Design 产物并过 Gate：
   - `stage-gate.py --stage design`
5. 进入开发并补齐 Dev 证据：
   - `stage-gate.py --stage dev`
6. 审查/冒烟/验收：
   - `stage-gate.py --stage review`
   - `stage-gate.py --stage smoke`
   - `stage-gate.py --stage qa`
   - `stage-gate.py --stage ui_acceptance`
   - `stage-gate.py --stage product_acceptance`
7. 发布前检查与发布记录：
   - `stage-gate.py --stage release`
8. 全量放行复核（推荐）：
   - `stage-gate.py --stage all`
