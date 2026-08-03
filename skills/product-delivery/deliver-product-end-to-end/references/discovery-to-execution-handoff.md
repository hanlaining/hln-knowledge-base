# Discovery to Execution Handoff

## 目的

把孵化任务中已经确认的产品事实压缩成一个自包含交接包，供全新的执行任务直接继续。不要复制完整聊天记录，也不要让执行任务重新发现已经确认的内容。

## 创建前检查

- 用户明确要求“新开任务落地”或同义动作。
- 项目名称或安全目录名已经明确。
- 目标是绿地 projectless 任务，或已经确认一个 Codex 项目。
- 已确认事实与推断已经分开。
- 当前审批状态有用户证据；没有证据时保持较早状态。
- 交接内容不含密码、Cookie、Token、二维码、个人敏感信息或无关仓库内容。
- 当前项目没有仍在运行的主执行任务；有则优先继续原任务。

## 交接包模板

```markdown
# Project Launch Brief

## Launch
- source_task: <孵化任务标题或 ID；未知填 unknown>
- launch_request: <用户要求新开任务落地的原话>
- execution_target: <projectless:directory-name 或 project:project-id>
- approved_stage: <有证据的最远状态；默认 DISCOVERY>

## Product
- name: <项目名>
- one_liner: <一句话定位>
- target_users: <目标用户>
- trigger_scenarios: <触发场景>
- core_problem: <核心问题>
- expected_value: <预期价值>

## Confirmed Requirements
- R01: <用户确认的需求>

## Acceptance
- AC01: <可观察验收行为>

## MVP
- in_scope: <本期包含>
- out_of_scope: <本期不做>
- core_journey: <最短成功路径>
- pages_or_surfaces: <已确认页面；未知填待设计>

## Experience and Identity
- experience_goals: <体验目标>
- visual_direction: <视觉偏好>
- logo_direction: <Logo 偏好或待设计>
- references: <已确认参考与复用边界>

## Constraints
- user_rules: <用户原始约束>
- repository_rules: <已知仓库规则>
- authorization_granted: <本次已授权动作>
- authorization_not_granted: <Git、账号、付费、生产等未授权动作>

## Inferred, Not Confirmed
- I01: <Agent 推断；不得当作事实>

## Open Questions
- Q01: <尚未确认且会影响后续审批的问题>
```

没有 Rxx 或 ACxx 编号时，执行任务使用 `requirement-acceptance-planner` 根据确认内容生成并请求用户确认；不要编造确认状态。

## 新任务 Prompt 合同

```text
使用 $deliver-product-end-to-end，以 EXECUTE 模式接手下面的 Project Launch Brief。

这是从产品孵化任务创建的全新执行任务。把 confirmed 内容当作用户已确认事实，不要重复询问；把 inferred 保持为待确认假设。先验证交接合同，再从 approved_stage 有证据支持的状态继续。严格遵守 Figma、技术方案、服务合同、Git、外部账号、付费、生产和发布审批门。

<完整 Project Launch Brief>

先回复：已接收的确认事实、当前状态、下一步和仍未授权的动作，然后推进当前允许的步骤。
```

## 创建目标

- 绿地项目：创建 `projectless` 任务，使用小写字母、数字和连字符组成的目录名。
- 已有项目：先列出 Codex 项目；确认项目后，根据是否为 Git 仓库选择 worktree 或 local。除非用户明确要求，不从带有未提交内容的 working tree 启动。
- 不使用 fork；fork 会携带孵化任务的冗长历史，违背精简交接目标。

## 失败处理

新任务创建失败时，在当前任务输出“新任务 Prompt 合同”与完整交接包，标记 `HANDOFF_BLOCKED` 并停止。不要在孵化任务切换到 `EXECUTE`。
