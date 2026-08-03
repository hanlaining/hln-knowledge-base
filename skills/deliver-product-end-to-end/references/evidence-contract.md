# Evidence 合同

## Evidence 最小字段

```text
id
related Rxx / ACxx / Issue
kind
source
captured_at
command_or_action
observable_result
status
redaction
```

## 可接受 Evidence

- Figma 文件/节点、结构化 metadata、原型链接与真实截图。
- 真实应用窗口截图或录像。
- 目标用户视角的核心任务观察：入口发现、实际步骤/时间、犹豫点、理解偏差、失败与恢复结果；没有真实样本时明确标为待验证。
- 精确命令、退出码、时间与测试 totals。
- 真实前后端请求/响应和持久化读回，敏感值脱敏。
- 完整累计 diff Review 与 P0–P3 结果。
- 用户确认原话与对应阶段。

## 不可替代

- Worker 自述不能替代 diff 和复测。
- AI mockup 不能替代真实浏览器或 Figma。
- PR/commit 数不能替代 ACxx。
- 单独前端 mock 数据不能替代真实集成。
- 文件存在不能证明行为成立。
- AI 推测的满意度、成功率或节省时间不能替代真实用户或验收人员的操作记录。

passed ACxx 必须列出 Evidence ID；过期或被纠偏影响的 Evidence 标记 `stale`，不得静默复用。
