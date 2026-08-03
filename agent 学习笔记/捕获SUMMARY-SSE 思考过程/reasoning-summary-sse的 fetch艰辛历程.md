# Reasoning Summary SSE Fetch 排障 SOP

god-agent 没有接收到 Summary SSE，是因为 Responses 请求少传了 `reasoning.effort: "high"`；补齐请求参数并完整解析 `response.reasoning_summary_*` 事件后即可展示，与选择 5.4 还是 5.6 无关，前提是模型本身支持 Reasoning Summary。

## 1. 适用场景

出现以下情况时使用本 SOP：

- CLI 一直显示 `Thinking…`，但没有 Summary 正文。
- Mock SSE 能显示 Summary，真实 Provider 却没有。
- Provider 已返回 Summary SSE，但 Agent Event 或 CLI 没有展示。
- 更换模型后现象变化，无法判断是模型还是请求参数造成的。

目标只包含 Provider 公开返回的 Reasoning Summary，不获取、不展示模型隐藏思维链，也不允许用最终回答伪造 Thinking。

## 2. 完成标准

- Responses 请求明确携带 `reasoning.summary: "auto"` 和 `reasoning.effort: "high"`。
- 原始 SSE 中能观察到 `response.reasoning_summary_*` 事件。
- `summary_index`、文本增量和完成边界没有在解析时丢失。
- Summary 能经过 Provider → Agent Loop → Event System → JSON-RPC → CLI。
- 真实 CLI 能展示 Thinking Summary，相关自动化测试全部通过。

## 3. 排障前检查

1. 使用需要一定推理的测试问题；过于简单的问候不一定产生 Summary。
2. 先消除 HTTP 400、Tool Schema 等前置错误，否则还没有进入 Summary 排障阶段。
3. 日志只记录请求字段名、事件类型、状态和数量，不读取或输出 Key、Cookie、Authorization 或加密推理内容。
4. 暂时不要引入 Browser Bridge、MCP 或伪造 Thinking；先验证原生 Responses 请求和 SSE。

## 4. 标准操作步骤

### Step 1：记录最小复现

记录 HTTP 状态码、CLI 表现、原始 SSE 事件类型和当前请求参数。先区分以下三种情况：

- HTTP 请求失败：先修请求或 Tool Schema。
- HTTP 200，但原始 SSE 没有 Summary：检查请求参数和 Provider。
- 原始 SSE 有 Summary，但 CLI 没有：检查 Runtime 内部事件链。

### Step 2：核对 Responses 请求

请求至少应明确包含：

```json
{
  "reasoning": {
    "effort": "high",
    "summary": "auto"
  },
  "stream": true
}
```

`include: ["reasoning.encrypted_content"]` 用于携带加密推理状态，不是可见 Summary 的开关，也不能作为用户可见内容展示。

### Step 3：做单变量 A/B 测试

固定同一个模型、问题、Base URL 和其他参数，只切换 Reasoning 参数：

| 测试组 | 参数 | 本次 Provider 的结果 |
|---|---|---|
| A | 只有 `summary: "auto"` | 无 Summary |
| B | `summary` + `include` | 无 Summary |
| C | `summary` + `effort: "high"` | 有 Summary |
| D | 完整 Codex 同形参数 | 有 Summary |

事件数量会随回答长度变化，验收时判断事件类型是否出现，不要求固定数量。本次事故中 C、D 两组各观察到 12 个 Summary 事件。

### Step 4：排除模型版本误判

保持完整参数一致，再切换模型。本次控制变量测试中，`gpt-5.4`、`gpt-5.4-mini` 和 `gpt-5.6-sol` 都返回了 Summary，因此不能把“参数变化”误判成“必须升级模型”。

### Step 5：捕获原始 Summary SSE

重点识别：

```text
response.reasoning_summary_part.added
response.reasoning_summary_text.delta
response.reasoning_summary_text.done
response.reasoning_summary_part.done
```

不要把 `response.reasoning_text.delta` 当作公开 Summary 展示；两者不是同一种内容。

### Step 6：规范化 Runtime 事件

Provider 解析时必须保留 `item_id`、`summary_index`、文本增量和完成边界：

```text
reasoning_summary_part.added
  -> reasoning_summary_part_added

reasoning_summary_text.delta
  -> reasoning_summary_delta(summaryIndex)

reasoning_summary_text.done / part.done
  -> reasoning_summary_completed
```

### Step 7：逐层验证传递链路

```text
Responses SSE
  -> Provider Parser
  -> LLM Stream Event
  -> Agent Loop
  -> Agent Event System
  -> JSON-RPC Notification
  -> CLI Renderer
```

- 原始 SSE 没有事件：回到请求参数或 Provider。
- 原始 SSE 有、LLM Event 没有：检查 Parser。
- LLM Event 有、Agent Event 没有：检查 Agent Loop 映射。
- Agent Event 有、CLI 没有：检查通知和 Renderer。

### Step 8：使用真实场景验收

优先使用需要推理或联网搜索的问题，预期 CLI 至少能出现：

```text
Thinking: ...
Search › 正在联网搜索…
Search ✓ ...
Assistant › ...
Sources:
• ... — https://...
```

如果没有使用搜索，至少应验证 Thinking Summary、Assistant 和 Turn 正常完成。

### Step 9：检查两个集成边界

1. Compaction 必须发送 `allowHostedTools: false`，避免内部压缩请求意外获得 `web_search`。
2. CLI Smoke Test 必须等待 Citation、Sources 和 Turn 完成，不能看到第一段 Assistant 文本就立即发送 `/exit`。

### Step 10：运行回归验证

```powershell
npm run check
npm test
```

本次修复的最终基线为 `npm run check` 通过、`npm test` 130/130 通过，并完成真实 CLI 验收。

## 5. 常见故障判断表

| 现象 | 优先检查 | 本次解决办法 |
|---|---|---|
| Function Schema 返回 400 | `required` 是否覆盖所有 `properties` | 修正 `list_files.path` 的严格 Schema |
| Mock 有 Summary，真实请求没有 | 实际 Responses 请求参数 | 补传 `reasoning.effort: "high"` |
| 原始 SSE 有，Runtime 没有 | SSE Parser | 补齐 part、delta、done 和 `summary_index` |
| Agent Event 有，CLI 没有 | JSON-RPC 通知和 Renderer | 补齐事件转发与展示 |
| 换成 5.6 后才成功 | 是否同时改了模型和参数 | 固定模型重新做单变量 A/B |
| Compaction 触发联网 | 托管 Tool 是否被 Provider 自动注入 | 设置 `allowHostedTools: false` |
| 测试报 `Turn is not running` | CLI 是否提前 `/exit` | 等待完整 Turn 完成边界 |

## 6. 验收清单

- [ ] 已修复所有 HTTP 400 和 Tool Schema 前置错误。
- [ ] 已确认请求包含 `reasoning.summary` 与 `reasoning.effort`。
- [ ] 已固定模型完成单变量 A/B，而不是一次更换多个变量。
- [ ] 已确认 `include` 不是可见 Summary 开关。
- [ ] 已观察到真实 `response.reasoning_summary_*` SSE。
- [ ] 已保留 `summary_index` 和完成边界。
- [ ] 已逐层验证 Provider 到 CLI 的事件链。
- [ ] 已确认没有展示隐藏思维链或加密推理内容。
- [ ] 已完成真实 CLI 验收。
- [ ] 已通过 `npm run check` 和全量测试。

## 7. 本次事故时间线

1. `list_files` 的严格 Schema 不合法，请求先返回 400。
2. Schema 修复后，CLI 只剩 `Thinking…`，Summary 正文仍缺失。
3. 明确目标是公开 Reasoning Summary，而非隐藏思维链。
4. 对照 Codex 协议补齐 Summary SSE 事件类型与 `summary_index`。
5. Mock 全链路成功，但真实 Provider 仍然没有 Summary。
6. 先后怀疑 CLI、模型、Key、Base URL、Provider 和 Browser Bridge。
7. 对比完整请求后，发现 god-agent 少传 `reasoning.effort: "high"`。
8. 第一次 A/B 同时更换模型和参数，无法锁定真实变量。
9. 根据“Codex 使用 5.4 也能显示”的反证，重新设计控制变量实验。
10. 跨模型测试排除版本因素，同模型参数测试锁定 `effort: "high"`。
11. 补齐请求参数和 Summary SSE Parser，贯通 Agent Event System 与 CLI。
12. 接通托管搜索、搜索生命周期和 URL Citation，完成真实场景验收。
13. 修复 Compaction 意外获得托管搜索的能力边界。
14. 修复 CLI Smoke Test 提前退出导致的 129/130 竞态。
15. 最终达到 130/130，并在真实 CLI 中看到 Thinking、Search、Assistant 和 Sources。
