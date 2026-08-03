---
name: define-service-contracts
description: "Define and freeze frontend-backend service contracts after the user approves the product prototype and technical direction, including endpoints, data models, validation, errors, authentication and authorization, idempotency, pagination, concurrency, events, compatibility, and contract-test examples. Use before frontend and backend implementation begins or when a correction changes cross-layer behavior."
---

# 前后端服务合同

## 前置闸门

只在 `FIGMA_PROTOTYPE_APPROVED` 后运行。技术栈、数据存储、身份角色、网络边界和复用方案必须先由用户确认；原型未冻结时返回设计阶段。

读取 [service-contract-checklist.md](references/service-contract-checklist.md)，从 [service-contract-template.md](assets/service-contract-template.md) 复制一份项目合同，不直接修改模板。

## 定义顺序

1. 从 Rxx、ACxx 和点击旅程提取真实业务动作，不从数据库表反推产品。
2. 定义领域对象、权威 Owner、状态机与不变量。
3. 为每个动作定义请求、响应、校验、错误和权限。
4. 定义认证、租户/角色隔离、敏感字段、审计和拒绝路径。
5. 对创建、支付、任务、重试等动作定义幂等、并发和重复请求行为。
6. 定义分页、排序、过滤、时间、时区、金额/精度和 null/缺省语义。
7. 定义兼容、版本、弃用、超时、重试和部分失败。
8. 给出成功与失败的真实示例，并建立消费者/提供者合同测试。
9. 把每条合同映射到 Rxx、ACxx、前端节点和后端节点。

## 冻结结果

合同只有在以下条件成立时进入 `CONTRACT_APPROVED`：

- 前端可以根据合同实现所有可见状态。
- 后端可以唯一解释校验、错误、权限和状态转换。
- 测试可以从合同生成或编写成功与失败用例。
- 用户确认所有会改变产品体验、数据或权限的选择。
- 未决问题全部显式列出，不用 TODO 伪装冻结。

冻结后变更必须作为版本化 delta：更新 Rxx、ACxx、消费者、提供者和测试节点，再重新审批；不允许 Worker 私自修改共享合同。

## Evidence

- 合同文件和版本/哈希。
- Rxx ↔ ACxx ↔ endpoint/event 映射。
- 成功、失败、无权限、冲突和重试示例。
- 合同测试计划与 Owner。
- 用户 `CONTRACT_APPROVED` 确认。
