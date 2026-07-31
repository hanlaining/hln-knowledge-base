# 从 0 到 1 手写桌面 Agent：框架选型与 MVP 学习路线

> 文档状态：第二版方案，已按“两版本、分阶段迁移到 Rust”纠偏<br>
> 更新时间：2026-07-31<br>
> 当前阶段：只做产品形态、框架选型、验收用例和任务拆分，不进入代码实现<br>
> 核心目标：不是复制完整 Codex，而是亲手做出一个最小、真实、可运行、架构边界正确的桌面 Agent。

## 0. 本次用户纠偏

> “如果 Electron 的话，我后期要换架构岂不是都要重弄么？或者可以分两个版本，先来个简易学习版先理解整个链路搭建，然后开始在 Rust 搭建。”

### 需求变化

- Added：正式增加第二个 Rust/Tauri 版本，不再只把 Tauri 当作可选性能实验。
- Changed：原 R10 从“Electron 后做 Tauri 替壳”改为“两版本、三步迁移”。
- Added：迁移时先保持 Electron、单独替换 Rust Runtime，再替换 Tauri 客户端，避免同时改变两层。
- Unchanged：第一版仍然从最小 Agent Loop、Tool、审批和协议开始。
- Unchanged：第一版仍然不做 Skills、多 Agent、RAG 和生产级 Sandbox。

### 结论

可以分成两个版本，而且这是更适合学习的路线。但工程上不能直接从：

```text
Electron + TypeScript Runtime
```

一次跳到：

```text
Tauri + Rust Runtime
```

因为 UI 壳和 Runtime 同时变化，出现问题时无法判断是 Tauri、Rust、协议还是 Agent Loop 导致的。

推荐采用“两版本、三步迁移”：

```text
版本 A：Electron + TypeScript Runtime       学习完整链路
                         ↓
版本 B-1：Electron + Rust Runtime           只替换 Runtime
                         ↓
版本 B-2：Tauri + Rust Runtime              再替换客户端壳
```

这样最终仍是两个产品版本，但中间增加一个只用于验证架构的迁移检查点。

## 1. 我理解你要做什么

你希望从零开始亲手实现一个桌面 Agent，用真实编码理解以下概念，而不是只停留在文档层面：

- Model、Agent Runtime、Agent Loop 分别负责什么。
- 客户端与本地 Runtime 为什么要分离。
- JSON-RPC-like 和事件流怎样连接 UI 与 Runtime。
- Tool Call 是怎样生成、路由、审批和执行的。
- Sandbox、权限和 Tool 之间是什么关系。
- Agent 如何流式输出、停止、失败和恢复。
- Electron 与 Tauri 对 Agent 客户端分别意味着什么。

第一版从简单开始，只实现一个 Agent、少量 Tool 和最小审批，不做专家团、复杂 Skills、知识库或生产级 Sandbox。

---

## 2. 先给选型结论

### 2.1 版本 A：Electron 学习版

推荐组合：

```text
Electron + React + TypeScript
            ↓ stdio + JSONL
独立 TypeScript App Server / Runtime Sidecar
            ↓ HTTPS
一个可用的模型 API
```

推荐 Electron 不是因为它在所有维度都优于 Tauri，而是因为版本 A 的首要目标是看懂并亲手跑通整个 Agent 链路，而不是立即追求长期技术栈。

Electron 第一版的优势：

- UI、主进程、协议类型和 Runtime 都可以先用 TypeScript。
- 减少同时学习 Rust、WebView 差异和 Tauri Capability 的认知负担。
- React、Markdown、代码块、事件流和调试工具成熟。
- 容易观察 Renderer、Main、Sidecar 三层之间的通信。
- TypeScript 适合快速加日志、断点和事件面板，便于观察内部链路。

### 2.2 Runtime 必须从第一天独立

虽然第一版使用 Electron，但不把 Agent Loop 塞进 Renderer 或 Electron Main Process。

```text
Electron Renderer
只负责页面与交互
        ↓ IPC
Electron Main/Preload
只负责窗口、生命周期和受控桥接
        ↓ stdio + JSONL
Agent App Server Sidecar
负责协议、Runtime、模型与 Tool
```

这样做的学习价值是：

- 能真正理解 C/S 和 App Server。
- UI 崩溃与 Agent 核心错误更容易区分。
- 后续能用 Tauri、CLI 或 IDE 接入同一个 Runtime。
- Tool 权限不会直接暴露给页面。

### 2.3 版本 B：Rust/Tauri 深入版

版本 B 不直接同时替换两层，而是分两步。

第一步保留 Electron，只替换 Runtime：

```text
Electron UI
   ↓ 原协议
Rust App Server / Runtime Sidecar
```

这一阶段验证：

- JSON-RPC-like 协议是否真正与语言无关。
- Rust Runtime 是否通过版本 A 的相同验收用例。
- Electron UI 是否完全不需要理解 Runtime 内部实现。
- Tool、审批、取消和错误语义是否保持一致。

第二步再替换客户端壳：

```text
Tauri UI
   ↓ 同一套 JSON-RPC-like 协议
Rust Agent Runtime Sidecar
```

这一阶段验证：

- Rust Runtime 不需要因为 UI 从 Electron 变成 Tauri 而修改。
- React 展示组件可以尽量复用。
- 只有进程生命周期、IPC Adapter、打包和系统集成需要变化。

### 2.4 后期到底哪些要重写

| 内容 | 版本 A → Rust Runtime | Electron → Tauri |
|---|---|---|
| Agent Loop 实现 | TypeScript 改写为 Rust | 不改 |
| State Machine 实现 | TypeScript 改写为 Rust | 不改 |
| Tool Executor 实现 | TypeScript 改写为 Rust | 不改 |
| Model Adapter 实现 | TypeScript 改写为 Rust | 不改 |
| JSON-RPC 方法和事件语义 | 复用协议 | 复用协议 |
| JSON Schema/协议 Fixture | 直接复用 | 直接复用 |
| AC01-AC09 验收用例 | 直接复用 | 直接复用 |
| Demo Workspace 和测试数据 | 直接复用 | 直接复用 |
| React 展示组件 | 不改 | 大部分可复用 |
| Electron Main/Preload | 不改 | 改写为 Tauri Host/Command |
| Sidecar 启停 Adapter | 不改 | 改写 |
| 安装、签名、更新配置 | 不改 | 改写 |

所以不会“全部重弄”，但也不能说“完全不用重写”：

- Rust 版本的 Runtime 实现会重写，这是第二版的学习目标。
- 协议、状态语义、测试、验收、Tool Schema 和 UI 业务组件应复用。
- Electron 专属 Main/Preload 代码在 Tauri 版中会被替换。

### 2.5 要想避免全部重做，版本 A 必须遵守的边界

```text
禁止 Renderer 直接调用模型
禁止 Renderer 直接执行 Tool
禁止 Electron Main 承载 Agent Loop
禁止协议只使用 TypeScript 内存对象
禁止 React 组件直接 import electron API
```

必须做到：

```text
协议使用 JSON/JSON Schema 定义
Renderer 只依赖 Client Adapter
Electron IPC 封装在 Electron Adapter
Runtime 通过独立进程启动
同一套黑盒验收同时测试 TypeScript 和 Rust Runtime
```

### 2.6 什么时候应该跳过学习版直接选 Tauri

如果你的真实目标发生变化，以下情况可以直接选择 Tauri：

- 主要目标是同时学习 Rust 和 Agent Runtime。
- 可以接受第一版开发速度更慢。
- 明确希望 Runtime 最终使用 Rust。
- 非常在意包体积和空闲内存。
- 愿意处理不同系统 WebView 的兼容问题。

当前目标是从零学习完整链路，所以仍然保留 Electron 学习版，再进入 Rust/Tauri 深入版。

---

## 3. 最终用户会看到什么

第一版是一个简单桌面窗口：

```text
┌──────────────────────────────────────────────────────┐
│ Agent Lab                              Runtime: Ready │
├──────────────────────────────────────────────────────┤
│ 任务                                                 │
│ ┌──────────────────────────────────────────────────┐ │
│ │ 请读取示例目录中的 README，并告诉我项目做什么。   │ │
│ └──────────────────────────────────────────────────┘ │
│                                      [发送] [停止]  │
├──────────────────────────────────────────────────────┤
│ Agent 输出                                            │
│ 正在分析任务……                                       │
│ 准备调用 read_file                                   │
│ 已读取 README.md                                     │
│ 这个项目是……                                         │
├──────────────────────────────────────────────────────┤
│ 执行事件                                              │
│ MODEL_STARTED → TOOL_REQUESTED → TOOL_COMPLETED      │
└──────────────────────────────────────────────────────┘
```

当 Agent 请求执行命令时，显示审批：

```text
┌──────────────────────────────────────────────────────┐
│ Agent 请求执行命令                                   │
│                                                      │
│ 工作目录：<已授权示例目录>                            │
│ 命令：npm test                                       │
│                                                      │
│                         [拒绝] [仅允许这一次]         │
└──────────────────────────────────────────────────────┘
```

第一版不追求漂亮 UI，重点是能看见 Agent 内部发生了什么。

---

## 4. 最短用户旅程

```text
启动 Agent Lab
    ↓
看到 Runtime Ready
    ↓
输入一个需要读取示例文件的任务
    ↓
模型返回 Tool Call
    ↓
Runtime 校验并执行只读 Tool
    ↓
Tool Result 回到模型
    ↓
模型生成最终答案
    ↓
用户在事件面板看到完整执行过程
```

第二条验收旅程：

```text
输入需要执行命令的任务
    ↓
Runtime 发出审批请求
    ↓
用户选择拒绝
    ↓
命令没有执行
    ↓
Agent 收到拒绝结果并给出替代说明
```

---

## 5. 需求清单 Rxx

| ID | 状态 | 需求 | 来源或说明 |
|---|---|---|---|
| R01 | confirmed | 从 0 到 1 亲手实现一个 Agent，用实际编码学习 Agent 架构。 | 用户明确提出 |
| R02 | confirmed | 第一版从简易版本开始，不直接做完整 Codex。 | 用户明确提出 |
| R03 | confirmed | 先完成客户端框架选型，重点比较 Tauri 与 Electron。 | 用户明确提出 |
| R04 | confirmed | 形成 Markdown 文档供用户验收。 | 用户明确提出 |
| R05 | inferred | 最终形态是独立桌面客户端，而不是只做终端脚本。 | 来自连续讨论上下文，待确认 |
| R06 | inferred | 第一版应该真实调用一个模型，而不是使用假数据。 | 学习 Agent Loop 所需，待确认 |
| R07 | inferred | 第一版需要至少一个真实 Tool Call，才能称为 Agent，而不是普通 Chatbox。 | 学习目标推导 |
| R08 | inferred | Tool 执行必须体现最小权限和审批边界。 | 学习 Execution Infrastructure 所需 |
| R09 | inferred | UI 与 Runtime 使用独立进程和清晰协议。 | 为学习 Codex 式分层而提出 |
| R10 | confirmed | 分为两个版本：先用 Electron/TypeScript 做简易学习版，再进入 Rust/Tauri 深入版。 | 用户本次明确提出 |
| R11 | inferred | 第一阶段由你亲手单线实现，不使用多 Agent 并行替你完成主体代码。 | “手戳学习”的合理解释，待确认 |
| R12 | inferred | 第二版采用三步迁移：先保持 Electron 将 Runtime 换成 Rust，再将客户端壳换成 Tauri。 | 为避免同时重写两层而推导，待确认 |
| R13 | inferred | 两版共享语言无关协议、验收用例、测试 Fixture、Tool Schema 和 UI 业务组件。 | 保证学习成果可迁移所需 |

### 当前未知项

| ID | 未知项 | 是否阻塞当前文档 |
|---|---|---|
| U01 | 第一版只支持 macOS，还是同时要求 Windows？ | 不阻塞；默认先在当前 macOS 开发，架构保留跨平台 |
| U02 | 你的 TypeScript、React、Rust 熟练程度分别如何？ | 不阻塞；版本 A 按 TypeScript 入门，版本 B 系统学习 Rust |
| U03 | 第一版使用 OpenAI、Gundam/企业 Gateway，还是其他兼容模型？ | 不阻塞；通过 Model Adapter 隔离 |
| U04 | 第一版是否要求修改文件？ | 不阻塞；默认只读文件，写文件延后 |
| U05 | 学习项目最终是否需要公开到 GitHub？ | 不阻塞；当前不执行 Git 操作 |

---

## 6. MVP 做什么

第一版只做以下能力：

1. 启动一个真实 Electron 桌面窗口。
2. Electron 启动一个独立 Runtime Sidecar。
3. UI 与 Runtime 通过 `stdio + JSONL` 通信。
4. 消息采用最小 JSON-RPC-like 结构。
5. Runtime 能调用一个真实模型。
6. 实现一个最小 Agent Loop。
7. 实现 `list_files` 和 `read_file` 两个只读 Tool。
8. 实现一个受审批保护的 `run_command` Tool。
9. UI 能显示流式文本、状态和 Tool 事件。
10. 用户可以停止当前 Turn。
11. 退出桌面客户端后不残留 Runtime 子进程。
12. Key 不出现在页面、日志和 Git 文件中。

### 第一版 Agent Loop

```text
接收用户任务
    ↓
组装 Context
    ↓
调用模型
    ↓
模型返回什么？
├─ Final Answer → 完成
└─ Tool Call
      ↓
   校验 Tool 和参数
      ↓
   是否需要审批？
   ├─ 是 → 等待用户 Allow/Deny
   └─ 否
      ↓
   执行 Tool
      ↓
   将 Tool Result 加入 Context
      ↓
   再次调用模型
```

---

## 7. MVP 明确不做什么

以下能力全部延后：

- 不做多 Agent。
- 不做专家团和 Agent Profile 商店。
- 不做完整 Skills 系统。
- 不做向量数据库或 RAG。
- 不做长期 Memory。
- 不做云端任务同步。
- 不做账号、计费和团队系统。
- 不做自动更新。
- 不做生产级容器或虚拟机 Sandbox。
- 不做任意目录访问。
- 不做任意文件写入。
- 不做自动部署和生产环境操作。
- 不做完整 Codex 协议兼容。
- 不追求第一版 UI 视觉效果。

原因：这些能力会遮住最值得学习的主链路：

```text
用户任务 → Model → Tool Call → Tool Result → Model → Final Answer
```

---

## 8. Electron 与 Tauri 针对本项目的对比

| 维度 | Electron | Tauri | 第一版判断 |
|---|---|---|---|
| UI 技术 | React/TypeScript | React/TypeScript + Rust Host | 都可以 |
| Runtime 最小实现 | Node/TypeScript Sidecar | Rust 或其他 Sidecar | Electron 更快 |
| 同时学习内容 | Electron IPC + Agent | Tauri Capability + Rust + Agent | Electron 变量更少 |
| 代码编辑/Markdown 生态 | 非常成熟 | 可复用 Web 生态 | 接近 |
| 包体积与内存 | 通常较高 | 通常较低 | Tauri 更优 |
| 跨平台渲染一致性 | 自带 Chromium，一致性较好 | 使用系统 WebView，有差异 | Electron 更省心 |
| 系统权限边界 | 依赖 Main/Preload/IPC 设计 | Command/Capability 较明确 | Tauri 概念更清晰 |
| 学习 Rust | 不要求 | 通常需要 | Tauri 更适合 Rust 目标 |
| Sidecar 支持 | 可自行管理子进程 | 有 Sidecar 思路 | 都适合 |
| 第一版完成概率 | 高 | 中 | Electron |
| 长期本地基础设施潜力 | 高，但资源较重 | 高，适合 Rust | 第二阶段再比较 |

### 选 Electron 的真正条件

选择 Electron 后必须遵守：

```text
Renderer 不执行 Shell
Renderer 不读取任意文件
Preload 只暴露最小接口
Main 不承载 Agent Loop
Runtime 必须是独立模块或独立进程
```

否则虽然用了 Electron，学到的仍然是一个耦合的桌面脚本，而不是 Agent 架构。

---

## 9. 第一版技术架构

```text
┌─────────────────────────────────────────┐
│ Electron Renderer                       │
│ Chat UI / Event Panel / Approval Dialog │
└──────────────────┬──────────────────────┘
                   │ 受控 IPC
┌──────────────────▼──────────────────────┐
│ Electron Main + Preload                 │
│ Window / Sidecar Lifecycle / IPC Bridge │
└──────────────────┬──────────────────────┘
                   │ stdio + JSONL
┌──────────────────▼──────────────────────┐
│ Agent App Server                        │
│ JSON-RPC-like / Events / Request Map    │
├─────────────────────────────────────────┤
│ Agent Runtime                           │
│ Loop / State / Context / Cancel         │
├─────────────────────────────────────────┤
│ Tool Router / Policy / Approval         │
│ list_files / read_file / run_command    │
└───────────────┬────────────────┬────────┘
                │                │
        Model Adapter      Restricted Workspace
                │                │
          Model API        File / Child Process
```

### 9.1 为什么第一版仍然需要 App Server

如果 UI 直接调用模型并执行 Tool，主链路会变成：

```text
React Component
├─ 保存消息
├─ 调用模型
├─ 解析 Tool
├─ 读文件
├─ 执行命令
└─ 管理取消
```

这种结构很快会失控，也无法迁移到 Tauri。

App Server 的价值是建立协议边界：

```text
UI 只知道：startTurn、cancelTurn、approvalResponse、events
Runtime 只知道：任务、模型、Tool、状态
```

### 9.2 最小 JSON-RPC-like 消息

客户端开始任务：

```json
{"id":1,"method":"turn/start","params":{"input":"读取 README 并总结"}}
```

Runtime 流式通知：

```json
{"method":"agent/textDelta","params":{"turnId":"turn-1","delta":"我正在读取"}}
```

Runtime 发起审批：

```json
{"id":101,"method":"tool/requestApproval","params":{"tool":"run_command","command":"npm test"}}
```

客户端返回审批结果：

```json
{"id":101,"result":{"decision":"allowOnce"}}
```

任务完成通知：

```json
{"method":"turn/completed","params":{"turnId":"turn-1","status":"completed"}}
```

这些方法名是本学习项目自定义的最小协议，不宣称与 Codex App Server 完全兼容。

---

## 10. 建议的目录结构

第一版不追求复杂 Monorepo，保持边界可见即可：

```text
agent-lab/
├─ apps/
│  └─ desktop-electron/
│     ├─ src/renderer/
│     ├─ src/main/
│     └─ src/preload/
├─ packages/
│  ├─ protocol/
│  │  ├─ messages.ts
│  │  └─ schemas.ts
│  ├─ runtime/
│  │  ├─ app-server.ts
│  │  ├─ agent-loop.ts
│  │  ├─ context.ts
│  │  └─ state-machine.ts
│  ├─ model/
│  │  ├─ adapter.ts
│  │  └─ provider.ts
│  └─ tools/
│     ├─ registry.ts
│     ├─ list-files.ts
│     ├─ read-file.ts
│     └─ run-command.ts
├─ fixtures/
│  └─ demo-workspace/
├─ tests/
└─ README.md
```

第一版 Runtime 即使与桌面端处于同一仓库，也必须保持独立入口和独立测试。

---

## 11. Agent 状态机

第一版至少使用显式状态，而不是只写一个无限 `while`：

```text
IDLE
  ↓ turn/start
CALLING_MODEL
  ├─ final answer → COMPLETED
  ├─ tool call → VALIDATING_TOOL
  ├─ model error → FAILED
  └─ cancel → CANCELLED

VALIDATING_TOOL
  ├─ invalid → CALLING_MODEL（把错误返回模型）
  ├─ approval required → WAITING_APPROVAL
  └─ allowed → RUNNING_TOOL

WAITING_APPROVAL
  ├─ allow → RUNNING_TOOL
  ├─ deny → CALLING_MODEL（把拒绝结果返回模型）
  └─ cancel → CANCELLED

RUNNING_TOOL
  ├─ success → CALLING_MODEL
  ├─ failure → CALLING_MODEL（返回结构化错误）
  └─ cancel → CANCELLED
```

第一版完成条件：

- 模型返回最终答案。
- 达到最大循环次数。
- 用户取消。
- 出现不可恢复错误。

建议限制：

```text
最大模型循环次数：8
最大连续 Tool 调用：5
命令超时：30 秒
单次 Tool 输出：限制长度
```

具体数字可以实现时调整，但必须存在上限。

---

## 12. Tool 设计

### 12.1 `list_files`

用途：列出授权示例目录内的文件。

限制：

- 只能访问 Demo Workspace。
- 禁止 `..` 路径逃逸。
- 不跟随越过 Workspace 的符号链接。
- 限制最大返回文件数量。

### 12.2 `read_file`

用途：读取授权目录中的文本文件。

限制：

- 只能读取 Demo Workspace。
- 限制最大文件大小。
- 二进制文件拒绝或只返回元数据。
- Tool Result 包含规范化后的相对路径。

### 12.3 `run_command`

用途：在 Demo Workspace 中运行无害命令，例如测试。

第一版限制：

- 每次都请求用户审批。
- UI 展示完整命令和工作目录。
- 只允许在 Demo Workspace 执行。
- 设置超时和输出上限。
- 支持取消子进程。
- 不允许生产部署、提权和任意系统目录操作。

第一版的“安全执行”只是教学级约束，不宣称达到容器或虚拟机级 Sandbox。

---

## 13. Model Adapter

不要把 Runtime 写死在某一家模型接口上。

```ts
interface ModelAdapter {
  stream(input: ModelInput, signal: AbortSignal): AsyncIterable<ModelEvent>
}
```

Runtime 只依赖统一事件：

```text
text_delta
tool_call_delta
tool_call_completed
usage
completed
error
```

第一版只实现一个真实 Provider，其他 Provider 不实现，只保留接口边界。

Key 规则：

- 不写入源码。
- 不提交到 Git。
- 不发送到 Renderer。
- 日志中必须脱敏。
- 由 Runtime 进程读取安全配置或环境变量。

---

## 14. 验收用例 ACxx

以下全部为草案，用户确认后才成为正式 Definition of Done。

### AC01：启动真实桌面客户端

- Related requirements: R01, R03, R05, R10
- Status: draft
- Precondition: 已安装项目依赖。
- User action: 启动 Agent Lab。
- Expected observable result: 出现独立桌面窗口，显示输入框、输出区、事件区和 Runtime 状态。
- Negative or boundary behavior: Runtime 启动失败时，页面显示明确错误，不假装 Ready。
- Required evidence: 真实应用窗口截图和启动日志。

### AC02：完成一次真实模型对话

- Related requirements: R01, R02, R06
- Status: draft
- Precondition: 已配置一个可访问的模型 Provider。
- User action: 输入普通问题并发送。
- Expected observable result: 页面收到真实流式输出，最终 Turn 状态为 Completed。
- Negative or boundary behavior: 模型失败时显示可理解错误，Key 不出现在错误信息中。
- Required evidence: 真实流式过程录屏或事件日志，敏感值脱敏。

### AC03：模型自主调用只读 Tool

- Related requirements: R01, R07, R09
- Status: draft
- Precondition: Demo Workspace 中存在已知 README 文件。
- User action: 要求 Agent 读取 README 并总结。
- Expected observable result: 模型产生 `read_file` Tool Call，Runtime 执行后把结果送回模型，最终答案与文件内容一致。
- Negative or boundary behavior: Agent 不能绕过 Tool 直接声称已经读取文件。
- Required evidence: Tool 请求、Tool Result、最终回答和文件原文对照。

### AC04：拒绝命令审批

- Related requirements: R07, R08, R09
- Status: draft
- Precondition: Agent 请求调用 `run_command`。
- User action: 在审批窗口点击拒绝。
- Expected observable result: 命令没有执行；Runtime 将拒绝结果返回模型；Agent 给出替代说明。
- Negative or boundary behavior: 不产生子进程、不修改文件、不把拒绝当成 Allow。
- Required evidence: 审批事件、无命令启动记录、Agent 后续回复。

### AC05：仅允许一次命令

- Related requirements: R07, R08
- Status: draft
- Precondition: Agent 请求执行一个无害测试命令。
- User action: 点击“仅允许这一次”。
- Expected observable result: 命令只执行一次，输出回传模型，后续新命令仍需重新审批。
- Negative or boundary behavior: 一次授权不能扩大成整个会话永久授权。
- Required evidence: 两次命令请求分别产生审批的事件记录。

### AC06：阻止目录越界

- Related requirements: R08
- Status: draft
- Precondition: Demo Workspace 已配置。
- User action: 请求读取 Workspace 外部路径，例如 `../` 指向的文件。
- Expected observable result: Tool Router 或 Policy 拒绝请求；模型只收到结构化拒绝信息。
- Negative or boundary behavior: 页面、日志和模型上下文都不能出现外部文件内容。
- Required evidence: 拒绝事件、目标文件未读取的验证记录。

### AC07：停止正在运行的 Turn

- Related requirements: R01, R09
- Status: draft
- Precondition: 模型正在输出或命令正在运行。
- User action: 点击停止。
- Expected observable result: Turn 进入 Cancelled；流式输出停止；正在运行的受控子进程被终止。
- Negative or boundary behavior: UI 不能只隐藏输出而让后台继续执行。
- Required evidence: 状态事件、子进程终止记录、停止后的 UI。

### AC08：退出后无残留 Runtime

- Related requirements: R05, R09, R10
- Status: draft
- Precondition: Electron 已启动 Runtime Sidecar。
- User action: 正常退出客户端。
- Expected observable result: Runtime 子进程正常退出，不残留 Agent Lab 相关子进程。
- Negative or boundary behavior: 强制终止 Runtime 时也要清理已启动的受控 Tool 进程。
- Required evidence: 退出前后的进程检查结果。

### AC09：Key 不进入页面和仓库

- Related requirements: R06, R08
- Status: draft
- Precondition: 已配置真实模型凭证。
- User action: 完成一次成功和一次失败的模型请求。
- Expected observable result: 页面和日志只显示脱敏信息；项目文件中不存在真实 Key。
- Negative or boundary behavior: 网络错误堆栈不能打印完整 Authorization Header。
- Required evidence: 脱敏日志和敏感字符串扫描结果。

### AC10：Rust Runtime 等价替换

- Related requirements: R03, R09, R10, R12, R13
- Status: deferred
- Precondition: Electron/TypeScript 学习版已通过 AC01-AC09，协议和测试 Fixture 已冻结一个版本。
- User action: 保持 Electron 客户端不变，将 Sidecar 切换为 Rust Runtime，并重新执行 AC02-AC09。
- Expected observable result: Electron UI 不修改业务流程即可完成相同任务；Rust Runtime 的事件和错误语义与 TypeScript 版一致。
- Negative or boundary behavior: 不允许在 Electron 中增加仅为掩盖 Rust 协议不兼容而存在的特殊业务分支。
- Required evidence: TypeScript/Rust 两个 Runtime 的协议契约测试、相同 AC 结果和事件 Trace 对比。

### AC11：Tauri 替换 Electron 壳

- Related requirements: R03, R09, R10, R12, R13
- Status: deferred
- Precondition: Rust Runtime 已通过 AC10，协议版本保持不变。
- User action: 使用 Tauri 客户端启动同一个 Rust Runtime，执行 AC02-AC05、AC07-AC09。
- Expected observable result: 不修改 Rust Agent Loop、Tools 和 Model Adapter 即可完成核心旅程；React 业务组件尽量复用。
- Negative or boundary behavior: 不允许为 Tauri 复制第二套 Runtime，也不允许页面直接绕过协议调用 Tool。
- Required evidence: Electron/Rust 与 Tauri/Rust 两种组合的录屏、协议 Trace 和代码边界检查。

---

## 15. 从验收用例倒推任务 Txx

| Task | 可独立验收的结果 | Requirements | Acceptance |
|---|---|---|---|
| T00 | 确认框架、目标平台和模型 Provider | R03, R06, R10 | AC01, AC02 |
| T01 | 终端中跑通一次真实模型流式响应 | R01, R02, R06 | AC02 |
| T02 | 在无桌面 UI 条件下跑通最小 Agent Loop 和只读 Tool | R01, R02, R07 | AC03, AC06 |
| T03 | 定义最小 JSON-RPC-like 协议并通过 stdio 驱动 Runtime | R09 | AC03, AC07 |
| T04 | Electron 真实窗口启动并管理 Runtime Sidecar | R03, R05, R10 | AC01, AC08 |
| T05 | Chat UI 展示流式输出、状态和停止操作 | R01, R05, R09 | AC02, AC07 |
| T06 | Tool Router、路径校验和只读 Tool 完整接入 | R07, R08 | AC03, AC06 |
| T07 | `run_command` 审批、执行、超时和取消 | R07, R08 | AC04, AC05, AC07 |
| T08 | Key、日志、进程清理和端到端验收 | R06, R08, R09 | AC01-AC09 |
| T09 | 保持 Electron 不变，用 Rust 重写 Runtime 并通过协议等价验收 | R03, R09, R10, R12, R13 | AC10 |
| T10 | Tauri 复用 Rust Runtime，替换 Electron 客户端壳 | R03, R09, R10, R12, R13 | AC11 |

---

## 16. 为什么先做终端 Runtime PoC

虽然最终产品是桌面客户端，但第一个代码切片不应该是画 Chat 页面。

推荐顺序：

```text
先在终端跑通 Model
        ↓
再跑通 Agent Loop + Tool
        ↓
再封装 JSON-RPC-like App Server
        ↓
最后接 Electron UI
```

原因：

- 如果模型或 Tool Loop 没跑通，先做 UI 只会隐藏问题。
- Runtime 可以通过自动化测试验证，不依赖点页面。
- UI 接入时只需要消费一个已经工作的协议。
- 更容易区分模型问题、Runtime 问题和客户端问题。

这不代表最终产品是 CLI。终端只用于早期消除最大不确定性。

---

## 17. 任务依赖

```text
T00 选型确认
   ↓
T01 真实模型 PoC
   ↓
T02 Agent Loop + 只读 Tool
   ↓
T03 JSON-RPC-like App Server
   ↓
T04 Electron + Sidecar 生命周期
   ↓
T05 Chat/Stream/Stop
   ↓
T06 Tool Router 与目录边界
   ↓
T07 Approval + Command
   ↓
T08 端到端、安全与进程验收
   ↓
T09 Electron + Rust Runtime 等价替换
   ↓
T10 Tauri + Rust Runtime 替壳验收
```

这条路线故意串行。当前目标是学习，不建议用多个 CLI 同时生成核心代码，否则你会得到项目，却未必真正理解 Runtime。

---

## 18. 每个学习切片怎么验收

| Slice | 目标 | 计划文件边界 | 验证方式 | 回滚点 |
|---|---|---|---|---|
| S1 | 真实模型输出 | `packages/model`、最小 CLI 入口 | 看到真实流式文本和 usage/error | 删除 Provider 实现，不影响 UI |
| S2 | Agent Loop | `packages/runtime` | 固定任务触发一次 Tool 后完成 | 回到单轮模型调用 |
| S3 | Tool 安全边界 | `packages/tools`、fixtures | 允许 Workspace 内读取，拒绝 `../` | 移除新 Tool 注册 |
| S4 | App Server | `packages/protocol`、Runtime 入口 | 用测试客户端发送一行 JSON 并收到事件 | 保留 Runtime，移除协议适配 |
| S5 | Electron 壳 | `apps/desktop-electron` | 窗口启动、Runtime Ready、退出无残留 | 删除桌面 App，不影响 Runtime |
| S6 | 审批和取消 | Runtime、Protocol、Approval UI | Deny 不执行，AllowOnce 只生效一次，Stop 真取消 | 禁用 `run_command` |
| S7 | 端到端验收 | tests、fixtures、文档 | 逐条执行 AC01-AC09 | 回到最后一个通过验收的 Slice |
| S8 | Rust Runtime 等价替换 | `rust/runtime`、protocol fixtures | Electron 切换 Rust Sidecar 后通过 AC10 | 切回 TypeScript Sidecar |
| S9 | Tauri 替壳 | `apps/desktop-tauri` | 同一 Rust Runtime 通过 AC11 | 删除 Tauri App，不影响 Electron/Rust 组合 |

原则：每个 Slice 验收通过以后才进入下一步。

---

## 19. 需求、验收、任务追踪矩阵

| Requirement | 需求摘要 | Acceptance cases | Tasks | 最终证据 | 状态 |
|---|---|---|---|---|---|
| R01 | 亲手实现 Agent | AC01-AC07 | T01-T08 | 真实桌面端到端录屏与 Trace | pending |
| R02 | 从简易版本开始 | AC02, AC03 | T01, T02 | 最小 Loop 测试 | pending |
| R03 | 比较 Tauri/Electron | AC01, AC10, AC11 | T00, T04, T09, T10 | 两壳及两 Runtime 组合验收 | pending |
| R04 | Markdown 供验收 | 本文档本身 | 当前文档任务 | 文件路径与内容检查 | complete-local |
| R05 | 独立桌面客户端 | AC01, AC08 | T04, T05 | 真实窗口与进程记录 | draft |
| R06 | 真实模型 | AC02, AC09 | T01, T08 | 脱敏真实响应 | draft |
| R07 | 真实 Tool Call | AC03-AC05 | T02, T06, T07 | Tool Trace | draft |
| R08 | 权限与审批 | AC04-AC06, AC09 | T06-T08 | 拒绝、审批和扫描证据 | draft |
| R09 | UI/Runtime 分离 | AC03, AC07, AC08, AC10, AC11 | T03-T10 | 协议测试和进程边界 | draft |
| R10 | 两版本：Electron 学习版、Rust/Tauri 深入版 | AC01, AC10, AC11 | T00, T04, T09, T10 | 两版本验收报告 | confirmed |
| R11 | 亲手单线学习 | AC01-AC09 | T01-T08 | 每个 Slice 的学习记录 | draft |
| R12 | 先替换 Rust Runtime，再替换 Tauri 壳 | AC10, AC11 | T09, T10 | 分阶段迁移记录 | draft |
| R13 | 共享协议、Fixture、验收和 UI 业务组件 | AC10, AC11 | T09, T10 | 契约测试与复用清单 | draft |

---

## 20. 学习时每一阶段必须回答的问题

### 阶段一：Model

- 模型 API 的输入输出是什么？
- 流式事件怎样到达 Runtime？
- Tool Call 与普通文本如何区分？
- 如何取消模型请求？

### 阶段二：Runtime

- Agent Loop 为什么不是一次模型调用？
- Context、State 和 Message History 有什么区别？
- 如何判断任务完成？
- 如何防止无限循环？

### 阶段三：Protocol

- Request、Response、Notification 有什么区别？
- `id` 怎样匹配响应？
- 为什么默认使用 JSONL 分隔消息？
- 服务端如何反向请求审批？

### 阶段四：Tool

- Tool Schema 解决什么问题？
- 参数正确是否代表动作安全？
- Tool Router 与 Tool Executor 有什么区别？
- Tool Result 如何避免撑爆 Context？

### 阶段五：安全执行

- Allow、AllowOnce、Deny 的授权范围是什么？
- Approval 与 Sandbox 的区别是什么？
- 怎样限制工作目录和路径逃逸？
- UI 点击停止后，后台进程是否真的停止？

### 阶段六：桌面客户端

- Renderer、Preload、Main、Sidecar 各自负责什么？
- 哪些 IPC 能力可以暴露给页面？
- Runtime 崩溃后 UI 如何表示？
- 客户端退出时怎样清理子进程？

---

## 21. 学习版结束后怎样迁移到 Rust/Tauri

### 21.1 迁移原则：一次只改变一层

错误迁移：

```text
Electron + TypeScript Runtime
            ↓ 同时重写
Tauri + Rust Runtime
```

这种方式一旦出现 Tool、取消或流式事件问题，很难定位责任层。

推荐迁移：

```text
Electron + TypeScript Runtime
            ↓ 只换 Runtime
Electron + Rust Runtime
            ↓ 只换 UI 壳
Tauri + Rust Runtime
```

### 21.2 版本 A 留下什么

版本 A 不是用完即丢，它应该产出以下长期资产：

```text
protocol/schema/*.json
protocol/fixtures/*.jsonl
tests/contract/*
tests/acceptance/*
fixtures/demo-workspace/*
Tool Schema
事件名称和状态语义
React 业务组件
架构与踩坑笔记
```

TypeScript Runtime 实现本身可以在完成教学使命后冻结，不要求继续演进为生产版本。

### 21.3 Rust Runtime 重写什么

Rust 版应该重新实现：

- App Server 连接与消息分发。
- Agent Loop 和状态机。
- Context 组装。
- Model Adapter。
- Tool Registry、Router 和 Executor。
- Approval Pending Map。
- 取消、超时和子进程管理。
- 路径边界和输出限制。

但它必须消费原来的协议 Fixture，并通过相同黑盒测试。这样才能证明是“等价替换”，而不是做了另一个相似项目。

### 21.4 Tauri 替壳重写什么

Tauri 版主要替换：

- Electron Main Process。
- Electron Preload。
- Electron IPC Adapter。
- Sidecar 启停和资源路径处理。
- 打包、签名、更新和系统集成配置。

应该保留：

- Rust Runtime。
- JSON-RPC-like 协议。
- Tool 和安全策略。
- Model Adapter。
- 大部分 React 页面和状态展示逻辑。
- ACxx 验收用例。

### 21.5 真实对比指标

不要只比较网上的安装包数字，使用同一个 Rust Runtime 做真实实验。

| 指标 | Electron + Rust | Tauri + Rust | 测量方式 |
|---|---:|---:|---|
| 开发环境首次搭建时间 | 待测 | 待测 | 从空目录到窗口启动 |
| 冷启动时间 | 待测 | 待测 | 同一机器多次测量 |
| 空闲内存 | 待测 | 待测 | 窗口 Ready 后观察 |
| 安装包大小 | 待测 | 待测 | 同等 Release 配置 |
| Sidecar 启停可靠性 | 待测 | 待测 | 连续启动退出测试 |
| JSON-RPC 接入改动 | 待测 | 待测 | Runtime 应为零业务改动 |
| React 组件复用率 | 待测 | 待测 | 统计 UI 业务组件改动 |
| 系统菜单和托盘接入 | 待测 | 待测 | 完成同一功能 |
| 跨平台 UI 差异 | 待测 | 待测 | Windows/macOS 截图对比 |
| 权限边界理解成本 | 待测 | 待测 | 记录踩坑与实现代码 |

最终选型不只看性能，还要看：

```text
完成速度
+ 团队能力
+ 安全边界
+ 跨平台成本
+ Runtime 复用程度
+ 协议稳定性
```

---

## 22. 与 Codex 的复用关系

本项目第一阶段不直接复用 Codex Runtime，因为目标是亲手理解 Agent 核心。

### Concept reference：概念借鉴

借鉴 Codex 的：

- UI 与 App Server 分离。
- JSON-RPC-like 双向通信。
- Thread、Turn、Item 思路。
- 流式事件。
- 服务端发起审批请求。
- Runtime、Tool、Approval、Sandbox 分层。

### 不直接复制

- 不直接复制完整 Codex 协议。
- 不直接复制复杂 Sandbox。
- 不直接复制全部持久化和多 Agent 能力。
- 不追求第一版兼容 Codex App。

### 后续对照学习

每完成一个 Slice，再阅读 Codex 对应实现：

```text
先自己实现最小版本
        ↓
记录遇到的问题
        ↓
阅读 Codex 怎样解决
        ↓
比较差异并写学习笔记
```

这样比先照抄源码更容易理解设计理由。

---

## 23. 当前需要用户确认的架构决策

在开始写代码前，只需要确认下面四点：

### D01：第一版桌面壳

```text
版本 A：Electron
版本 B：Tauri
```

### D02：Runtime 技术栈

```text
版本 A：TypeScript/Node Sidecar，用于学习完整链路
版本 B：Rust Runtime，使用相同协议和验收重写
```

### D03：第一版目标平台

```text
推荐：先在当前 macOS 跑通
架构保留 Windows 支持
```

### D04：第一版模型入口

```text
推荐：选择你当前确实能调用的一个 OpenAI-compatible Provider
要求：base URL、model、key 不写死在代码中
```

### D05：版本迁移顺序

```text
Electron + TypeScript
→ Electron + Rust
→ Tauri + Rust
```

确认后才进入 T00/T01，不在本方案阶段提前创建项目或安装依赖。

---

## 24. 第一阶段 Definition of Done

这个学习项目的 MVP 只有在以下条件全部满足时才算完成：

1. AC01-AC09 经用户确认后逐条通过。
2. 运行的是一个真实桌面窗口，不是截图或 Mock。
3. 使用真实模型返回，不是假响应。
4. 模型真实地产生 Tool Call。
5. Tool Result 真实回到模型并影响最终回答。
6. Deny 后命令确定没有执行。
7. AllowOnce 没有扩大成永久权限。
8. Stop 确实取消模型或受控子进程。
9. Key 未进入页面、日志和 Git 文件。
10. 桌面客户端退出后没有残留 Runtime。
11. 每个阶段有自己的学习笔记，能用自己的话解释设计。

Rust Runtime 等价替换 AC10 和 Tauri 替壳 AC11 属于版本 B，不阻塞版本 A 的 Electron MVP 完成。

---

## 25. 下一步

用户验收并确认本方案中的 D01-D04 后，进入第一个实现切片：

```text
T00：建立最小项目骨架
   ↓
T01：在终端跑通一个真实模型流式响应
```

第一步不会直接画完整 Chat 页面，也不会直接加入 Skills、多 Agent 或复杂 Sandbox。

---

## 26. LangChain 技术决策记录

### 26.1 用户原始判断

> LangChain 现在已经被淘汰了。

### 26.2 事实校正

截至 2026-07-31，不能把“LangChain 已经被淘汰”当作客观事实。

更准确的判断是：

```text
LangChain 没有被行业淘汰，也没有停止维护；
但早期“什么都用 Chain 包一层”的开发方式已经不再是 Agent 工程的唯一主流答案。
对于本学习项目，我们主动淘汰 LangChain 方案，选择手写核心 Runtime。
```

官方当前仍将 LangChain 定位为一个可配置的 Agent Harness，用来组合模型、工具、Prompt 和中间件；其官方仓库也仍在持续更新。因此，“我们不采用它”与“它已经不存在或无人维护”是两件不同的事。

### 26.3 LangChain 家族当前分别是什么

| 名称 | 当前定位 | 主要解决的问题 |
|---|---|---|
| LangChain | Agent Framework / Harness | 模型与 Tool 集成、Prompt、中间件、常见 Agent Loop |
| LangGraph | 低层 Agent 编排框架与 Runtime | 状态图、持久执行、流式输出、人工介入、恢复与长任务 |
| LangSmith | 可观测性与评测平台 | Trace、调试、评测、监控和部署观测 |
| Deep Agents | 更高层、开箱即用的 Agent Harness | 规划、子 Agent、文件系统工具和上下文管理 |

这里最容易产生的误解是：

```text
LangGraph 不是“新版 LangChain”这么简单；
LangChain 也不是 LangGraph 的旧名字。

LangChain 偏向可复用 Agent 组件和现成 Harness；
LangGraph 偏向可控的状态与执行编排；
两者可以一起使用，LangGraph 也可以不依赖 LangChain 使用。
```

### 26.4 为什么本项目不使用 LangChain

本项目的目标不是最快拼出一个 Demo，而是亲手理解 Agent 的核心执行链：

```text
User Input
→ Model Request
→ Model Tool Call
→ Tool Router
→ Approval
→ Tool Execution
→ Tool Result
→ Model Continuation
→ Final Answer
```

如果第一版直接使用 LangChain，下面这些关键机制很可能会被框架封装隐藏：

1. 消息怎样进入 Model Adapter。
2. Tool Schema 怎样交给模型。
3. 模型返回 Tool Call 后，Runtime 怎样判断下一步。
4. Tool Router 怎样校验参数和选择执行器。
5. Approval 怎样暂停并恢复 Agent Loop。
6. Tool Result 怎样重新加入上下文。
7. Runtime 怎样限制循环次数、取消任务和处理异常。
8. 状态怎样落盘，以及进程退出后怎样恢复。

所以我们不采用 LangChain 的核心理由是：

> 它会降低第一阶段的学习透明度，而不是因为它已经失效。

### 26.5 本项目的明确决策

```text
版本 A：Electron + TypeScript 手写 Agent Runtime，不使用 LangChain

版本 B：Electron/Tauri + Rust 手写 Agent Runtime，不使用 LangChain

对照实验：MVP 完成后，可以使用 LangGraph 重做同一组 ACxx，
比较手写 Runtime 与编排框架在状态、恢复、人工审批和可观测性上的差异。
```

这里的“淘汰”只表示项目选型结论：

```text
LangChain：不进入本项目版本 A、版本 B 的核心依赖
LangGraph：暂不使用，完成手写 MVP 后保留为对照研究对象
LangSmith：不是必需依赖，后期研究 Trace 和评测时再判断
```

### 26.6 什么时候应该重新评估 LangGraph

当手写版已经通过 AC01-AC11，并且开始遇到以下问题时，可以做一次对照实验：

- 长任务中断后需要从指定节点恢复。
- Workflow 同时包含确定性步骤和模型自主决策。
- 需要复杂分支、循环、并行节点或人工介入。
- 自己维护状态机、Checkpoint 和重试逻辑的成本明显上升。
- 团队更关心交付速度和可观测性，而不再以理解底层链路为第一目标。

即使到这个阶段，也不是默认迁移，而是让手写版与 LangGraph 版运行同一组验收用例，再比较复杂度、控制力、调试成本和框架绑定程度。

### 26.7 最终结论

```text
错误表述：LangChain 现在已经被淘汰。

准确表述：LangChain 仍是活跃的 Agent 框架生态；
但本项目为了学透 Agent Runtime，明确不采用 LangChain，
并把 LangGraph 留作完成手写 MVP 后的对照实验对象。
```

---

## 27. 参考资料

- [OpenAI Codex 开源仓库](https://github.com/openai/codex)
- [Codex App Server 协议](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md)
- [Electron 官方文档](https://www.electronjs.org/docs/latest/)
- [Electron 安全建议](https://www.electronjs.org/docs/latest/tutorial/security)
- [Tauri 官方文档](https://tauri.app/)
- [Tauri Sidecar 文档](https://v2.tauri.app/develop/sidecar/)
- [LangChain 官方概览](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph 官方概览](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangSmith Observability](https://docs.langchain.com/langsmith/observability)
- [LangChain GitHub 仓库](https://github.com/langchain-ai/langchain)
