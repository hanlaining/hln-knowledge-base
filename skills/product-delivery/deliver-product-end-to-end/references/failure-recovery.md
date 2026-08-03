# 失败与恢复

## Figma

- MCP/权限缺失：保留设计合同，标记 blocked，不用截图冒充结构化文件。
- mutation 报错：停止、读错误与 metadata、修正后串行重试；不得并行补写。

## Claude Worker

- `BLOCKED_USER_DECISION`：只把产品、安全、权限、外部成本和不可逆选择升级给用户。
- `SCOPE_DRIFT`：停止写入，更新 Issue/Rxx/ACxx 后再继续。
- TUI 异常退出：确认精确 session 已停止和 Git 现场安全，再在同一 worktree 启动唯一替代 TUI。
- 禁止同时存在两个写入同一 Issue 的 Worker。

## Graph

- 一个节点失败不阻塞无依赖、无冲突 ready 节点。
- Evidence 失败时把节点退回原 Owner，不让集成者代修。
- 用户纠偏时从最早受影响阶段重新计算，不全量重做仍有效产物。

## 资源

- YELLOW/RED 只暂停新启动；不按模糊进程名批量终止。
- 磁盘不足、Swap 持续增长或模型限流恢复后，先重新采样再扩容。
