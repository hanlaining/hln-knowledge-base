# 项目状态合同

Canonical 状态位于项目根目录 `.product-delivery/`：

```text
.product-delivery/
├─ manifest.json
├─ requirements.md
├─ acceptance.md
├─ graph.json
├─ decisions.md
├─ runtime/
└─ evidence/
   └─ index.md
```

## manifest.json

必需字段：`schemaVersion`、`product`、`stage`、`approvedStages`、`contractVersion`、`updatedAt`、`nextAction`、`blockedBy`。

`approvedStages` 只记录用户或真实 Evidence 已批准的阶段；不能因为文件存在自动追加。

## graph.json

每个 Issue 必需字段：

```json
{
  "id": "BACKEND-FOUNDATION-01",
  "title": "后端底座",
  "state": "ready",
  "requirements": ["R17"],
  "acceptanceCases": ["AC09"],
  "dependsOn": ["CONTRACT_APPROVED"],
  "blocks": ["BACKEND-SLICE-01"],
  "produces": ["BACKEND_FOUNDATION_PASSED"],
  "validates": ["startup_smoke", "health_check"],
  "owner": "backend-foundation",
  "worker": "claude-code-cli",
  "worktree": "/absolute/path",
  "allowedFiles": [],
  "forbiddenFiles": [],
  "resourceClass": "medium",
  "evidence": []
}
```

状态允许：`pending`、`ready`、`running`、`review`、`blocked`、`passed`、`failed`、`deferred`。

## Markdown 编号

- 需求标题使用 `## R01 [confirmed] 标题`。
- 验收标题使用 `## AC01 标题`，正文必须有 `Related requirements:` 与 `Status:`。
- 每个 confirmed Rxx 至少映射一个 ACxx；unknown 可以不映射。
- passed ACxx 必须在 Evidence 索引中有真实路径或 URL。
