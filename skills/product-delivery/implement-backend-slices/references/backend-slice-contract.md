# 后端切片合同

每个切片必须声明：

- Rxx、ACxx、endpoint/event、领域 Owner。
- dependsOn、produces、validates。
- allowed/forbidden files 与唯一 worktree。
- 成功、validation、unauthorized/forbidden、conflict、duplicate、retry。
- 数据写入、事务、幂等和 migration 影响。
- Red/Green 命令与真实入口。
- Evidence、P0–P3、回退点。

共享合同或 schema 变化必须创建上游 delta，不得埋在实现 diff 中。
