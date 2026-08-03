---
name: bootstrap-backend-foundation
description: "Define, implement, and independently verify a production-oriented backend foundation through one isolated owner after the prototype, technical plan, and service contracts are approved. Use for a new backend or substantial backend reset requiring service entry points, configuration and secret boundaries, health and lifecycle, errors and logging, database and migrations when needed, auth and security baseline, API contract hooks, and test scaffolding before business slices begin."
---

# 后端底座交付

## 前置闸门

要求同时成立：

- `FIGMA_PROTOTYPE_APPROVED`
- `TECH_PLAN_APPROVED`
- `CONTRACT_APPROVED`
- 后端底座 Issue 已映射 Rxx 与 ACxx
- 用户已批准精确 worktree 和需要的 Git 动作

读取 [foundation-contract.md](references/foundation-contract.md) 与 [foundation-evidence.md](references/foundation-evidence.md)。

## 唯一 Owner

使用三层结构：

```text
主 Codex Epic
→ 独立 Backend Foundation Issue 任务
→ 一个 Claude CLI 唯一写入 Worker
```

使用 `agent-task-supervisor` 管理 Graph，使用 `claude-code-cli-development` 启动可见 Terminal + tmux Worker。不得让第二个 Worker 同时创建入口、配置、schema、migration 或鉴权底座。

## 底座范围

只实现技术方案和合同需要的能力：

- 服务入口、模块边界、启动与优雅退出。
- 配置分层、secret 读取与禁止泄露边界。
- health/readiness；只有真实需要时加入外部依赖检查。
- 统一错误、结构化日志、request/trace id 与必要可观测性。
- 数据库连接、schema、migration、事务与测试隔离；没有数据库需求时不创建。
- 已确认的认证、授权、租户隔离和审计基线。
- API/事件合同校验入口。
- 单元、集成、合同测试与本地 smoke 入口。

不要提前实现业务切片，不创建用户未确认的账号、权限、队列、缓存或云依赖。

## Red → Green → Review

1. Issue 任务先把底座不变量绑定到真实入口和可观察结果。
2. Claude Worker 只提交 Red 测试/验证 Evidence；Issue 审核失败原因确实是能力缺失。
3. 同一 Worker 进入 Green/Refactor。
4. Issue 任务从完整累计 diff 开始独立 Review，并复跑启动、health、合同、安全和必要 migration smoke。
5. P0–P2 回到原 Worker 修复；不得由 Review 任务代写。

## 解锁条件

只有以下 Evidence 齐全才产生 `BACKEND_FOUNDATION_PASSED`：

- 精确变更文件和完整 diff Review。
- 服务真实启动、health 和退出结果。
- 配置/secret 不泄露检查。
- 数据库和 migration 证据（适用时）。
- 合同、安全和测试脚手架结果。
- P0–P2 清零，未验证项与残余风险已披露。

完成标记不是 Git 授权。commit、push、PR、合并和 worktree 回收继续按 hln 规则逐项确认。
