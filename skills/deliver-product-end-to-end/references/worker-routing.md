# Worker 路由

## 默认结构

```text
Epic 总监工
→ Issue 负责/验收 Codex 任务
→ 唯一写入 Worker
```

主 Codex 不直接实现后再自审；Issue 任务不替 Claude 修代码；Worker 不改变产品合同。

## 默认 Worker

- 用户已指定 Claude Code 时，最低层实现统一使用 `claude-code-cli-development`。
- Figma canvas 写入使用官方 Figma 能力，严格串行，不放进多 CLI 并发。
- 只读调研可与代码 Issue 并行，但不得修改共享事实文件。
- 集成候选树只有一个 Owner。

## Ready 计算

Issue 只有同时满足以下条件才 ready：

1. 所有 `dependsOn` 已有有效 Evidence。
2. Rxx、ACxx 与输出可独立验收。
3. 用户授权、账号和 worktree 条件成立。
4. 与 active Issue 的 `allowedFiles`、权威 Owner、schema 和合同无冲突。
5. 机器资源调度允许启动。

## 监控

- Issue 任务监控直属 Worker；Epic 只监控 Issue。
- 每条父子边只有一个 monitor。
- 状态文件只保存最新单行状态；handoff 只在 Red/终态产生。
- Worker delivery 进入 `review`，不是 `passed`。
- hln 的 Git 逐项审批覆盖 Akasha 的自动 Git 默认值。
