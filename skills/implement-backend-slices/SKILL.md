---
name: implement-backend-slices
description: "Implement independently verifiable backend business slices on an approved backend foundation and frozen service contracts, using Graph issues, one isolated Claude CLI writer per slice, contract and integration tests, real success and failure evidence, and independent review. Use after BACKEND_FOUNDATION_PASSED for APIs, domain workflows, events, persistence, permissions, or background jobs required by confirmed acceptance cases."
---

# 后端业务切片实现

## 前置条件

要求 `BACKEND_FOUNDATION_PASSED`、冻结合同、明确 Rxx/ACxx、真实业务入口和已批准 worktree。读取 [backend-slice-contract.md](references/backend-slice-contract.md)。

## 拆分方式

从 ACxx 倒推最小业务切片：

```text
ACxx 用户结果
→ 必要领域不变量
→ 请求/事件入口
→ 状态变化与持久化
→ 成功、拒绝和恢复
→ 可独立运行的测试与 Evidence
```

每个 Issue 只允许一个权威状态 Owner。避免两个 Worker 同时修改共享 schema、migration 顺序、合同、事务边界或同一领域聚合。

## 执行

1. 使用 `agent-task-supervisor` 建立依赖和文件所有权。
2. 使用 `claude-code-cli-development` 在独立 worktree 启动唯一写入 Worker。
3. 先交付从真实入口失败的 Red，拒绝 mock 掉核心逻辑的假测试。
4. 同一 Worker 实现 Green/Refactor，不扩大合同和产品范围。
5. 覆盖成功、校验失败、无权限、冲突、重复请求、超时/重试及适用的事务回滚。
6. migration 必须有目标环境、顺序、兼容、回滚/前向恢复和测试数据库 Evidence。
7. Issue 任务独立审完整累计 diff、调用链、测试和安全风险；P0–P2 返回原 Worker。

## 合同变化

实现中发现合同不完整时写 `SCOPE_DRIFT` 或 `BLOCKED_USER_DECISION`，回到 `define-service-contracts` 更新版本、消费者和测试；不得由后端单方面改变响应让前端适配。

## 完成 Evidence

- Rxx/ACxx/合同映射。
- 完整累计 diff 与文件范围。
- Red/Green/Refactor、合同测试和集成测试。
- 真实请求/事件、持久化读回和拒绝路径。
- 权限、幂等、事务和迁移证据（适用时）。
- P0–P2 清零、未验证项与残余风险。

Worker 完成不等于产品完成；只有进入集成候选并通过真实前端路径后才能更新上层 ACxx。
