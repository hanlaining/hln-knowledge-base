---
name: integrate-and-verify-product
description: "Integrate approved frontend and backend implementations into one candidate product, run real startup, contract, database, browser, visual, accessibility, security, negative-path, and end-to-end acceptance checks, collect traceable evidence, and obtain user acceptance. Use after implementation Graph issues are reviewed and ready for integration; do not use isolated branch tests or worker claims as proof of product completion."
---

# 全栈集成与验收

## 前置条件

要求前端、后端底座、后端切片和测试节点均已独立 Review，合同版本一致，候选集成范围明确。读取 [integration-acceptance-contract.md](references/integration-acceptance-contract.md)。

## 集成顺序

1. 选择一个单一集成 Owner；其他 Worker 停止修改共享候选树。
2. 核对候选包含的精确 Issue、提交/文件、合同版本、migration 与资产。
3. 在非生产环境启动真实前端、后端和必要依赖；已运行服务不因并行聊天而随意重启。
4. 运行合同、单元、集成、migration、前端和浏览器测试。
5. 使用真实前端调用真实后端，从目标用户自然入口覆盖首次成功、高频核心任务和关键失败恢复，不用测试专用捷径绕过真实体验。
6. 在同 viewport 比较 Figma 与真实浏览器页面，验证状态、响应式、可访问性和动效。
7. 验证认证、授权、租户/角色隔离、输入拒绝、敏感数据和凭据不可见性。
8. 按 ACxx 逐条记录 passed、failed 或 deferred；失败回到原 Graph Owner，不由集成者随手改业务代码。
9. 实现和相关测试完成后立即使用 `hln-code-risk-gate` 审计中高风险。

## Evidence 要求

- 精确启动与测试命令、退出码、时间和 totals。
- 真实请求/响应、数据读回和必要日志片段，敏感信息脱敏。
- 真实应用窗口截图或录像。
- 核心任务体验观察：入口发现、实际步骤/时间、主要犹豫点、理解偏差、失败恢复和结果理解。
- Figma/浏览器视觉比较与偏差结论。
- 权限拒绝、错误、重试、取消和恢复路径。
- 每个 ACxx 的证据路径和用户可观察结果。
- 未验证、延期、残余低风险和回退点。

## 完成语言

区分：代码存在、Issue 完成、候选集成、自动化通过、ACxx 通过、用户接受。只有最后两项成立才能输出 `USER_ACCEPTED`；PR、分支、截图或 Worker 自述不能替代。

生产发布、线上迁移和外部系统写入不属于本 Skill 的默认授权。
