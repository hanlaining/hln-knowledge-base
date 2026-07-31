# C/S 客户端架构与桌面壳框架选型

> 更新时间：2026-07-31<br>
> 适用范围：需要访问本地文件、Shell、Git、浏览器、MCP 或远程模型的桌面 Agent 产品。<br>
> 重点：区分“桌面壳框架选择”和“Agent C/S 架构选择”。二者相关，但不是同一个问题。

## 1. 先说结论

桌面 Agent 不应该被简单理解为“给网页套一个壳”。一个完整产品至少包含五层：

```text
展示层：Desktop App / IDE / CLI
协议层：JSON-RPC-like / Event Stream
控制层：App Server / Agent Runtime / Workflow
执行层：Tool Router / Approval / Sandbox / Worker
模型层：OpenAI、其他模型服务或企业 Model Gateway
```

Electron、Tauri、Flutter、Qt、原生框架主要解决展示层和桌面集成问题；它们不会自动提供 Agent Runtime、工具审批、Sandbox 或任务恢复。

针对 Agent 产品的默认建议：

| 场景 | 推荐方案 |
|---|---|
| 快速做跨平台 MVP，团队熟悉 React/TypeScript | Electron + 独立 App Server Sidecar |
| 重视包体积、资源占用，后端准备使用 Rust | Tauri + Rust App Server/Runtime |
| 只做 macOS 且追求原生体验 | SwiftUI/AppKit + Runtime Sidecar |
| 只做 Windows 企业桌面软件 | WinUI/WPF/Avalonia + Runtime Service |
| 主要能力在云端，不需要深度操作本机 | Web/PWA + Remote Runtime |
| 本地 Coding Agent、企业数据 Agent | 厚客户端 + 本地 Runtime + 云端模型 |

真正决定 Agent 产品上限的，通常不是 Electron 和 Tauri 谁更“高级”，而是是否建立了稳定的：

```text
UI 与 Runtime 分层
+ 双向协议
+ 安全工具执行
+ 状态持久化
+ 可观测性
```

---

## 2. 基础概念

### 2.1 什么是桌面壳

桌面壳负责把 UI 和本地能力包装成可安装的桌面应用，常见职责包括：

- 创建和管理窗口。
- 渲染 Web UI 或原生 UI。
- 系统菜单、托盘、通知和快捷键。
- 文件选择器、剪贴板和拖拽。
- 自动更新、安装、签名和分发。
- 启动本地 Runtime 子进程。
- 提供 UI 与本地进程之间的 IPC。

桌面壳不等于 Agent Runtime。

```text
桌面壳：负责“用户怎样使用产品”
Runtime：负责“Agent 怎样持续完成任务”
```

### 2.2 什么是页面套壳

典型页面套壳：

```text
Electron/WebView 窗口
        ↓
加载远程网页
        ↓
所有核心能力都在云端
```

它的本地能力通常很少，主要负责显示页面、保存登录状态和系统通知。

### 2.3 什么是厚客户端

典型 Agent 厚客户端：

```text
桌面 UI
   ↓
本地 App Server / Runtime
   ├─ 读取和修改文件
   ├─ 执行 Shell
   ├─ 操作 Git
   ├─ 调用本地 Skills/MCP
   ├─ 处理审批
   └─ 执行 Sandbox
   ↓
云端模型
```

UI 即使使用 React 和 WebView，只要核心 Runtime 和执行能力在本地，它仍然是厚客户端，不是简单网页套壳。

### 2.4 C/S 是相对关系

同一个组件可能同时扮演客户端和服务端：

```text
Desktop UI ──客户端──→ 本地 App Server
本地 App Server ──客户端──→ 云端模型服务
```

因此“App Server 是服务端”和“整个 Codex 本地程序是云端模型的客户端”可以同时成立。

---

## 3. 桌面壳框架对比

## 3.1 Electron

### 架构

```text
Electron
├─ Chromium：渲染 HTML/CSS/React/Vue
├─ Main Process：窗口、系统能力、进程管理
├─ Renderer Process：页面 UI
└─ Preload/IPC：受控桥接页面与主进程
```

### 优点

- Web 前端团队上手快。
- React、Vue、Markdown、Monaco Editor、代码 Diff 生态成熟。
- Windows、macOS、Linux 的渲染一致性较好。
- 窗口、托盘、快捷键、自动更新和安装方案成熟。
- 很适合复杂工作台、编辑器和多面板 Agent UI。
- 可以方便地启动 App Server、CLI 或其他 Sidecar。

### 缺点

- 通常需要携带 Chromium，包体积较大。
- 内存占用一般高于系统 WebView 方案。
- 如果开启不受控的 Node 权限，页面漏洞可能升级为本地代码执行。
- Main、Renderer、Preload 和 Runtime 的边界容易被写乱。
- 如果把所有 Agent 逻辑都塞入 Main Process，后期很难复用到 CLI 和 IDE。

### 安全要求

- Renderer 不直接开启完整 Node 权限。
- 使用 `contextIsolation` 等隔离能力。
- Preload 只暴露最小白名单接口。
- 所有 IPC 参数必须验证。
- Shell、文件和网络操作进入独立执行层，不直接相信页面参数。

### 适合

- 快速构建 Agent MVP。
- 团队以 TypeScript/React 为主。
- 需要复杂代码编辑、Diff、Markdown 和多窗口 UI。
- 可以接受相对较大的安装包和内存占用。

---

## 3.2 Tauri

### 架构

```text
Tauri
├─ Web UI：React/Vue/Svelte 等
├─ 系统 WebView：不自带完整 Chromium
├─ Rust Host：本地命令、窗口和系统能力
└─ Sidecar：可启动独立 Runtime/App Server
```

### 优点

- 一般比 Electron 有更小的包体积和内存开销。
- 可以复用 Web 前端技术。
- Rust 适合实现本地 Runtime、协议、并发和系统能力。
- Command、Capability、Sidecar 边界比较适合最小权限设计。
- 如果 Agent Runtime 本来就是 Rust，技术栈衔接自然。

### 缺点

- Windows、macOS、Linux 使用的系统 WebView 不完全相同。
- UI 兼容性可能不如自带 Chromium 的 Electron 一致。
- Rust 的开发和调试门槛高于纯 Node 方案。
- 桌面插件和案例数量少于 Electron。
- 复杂系统集成仍可能需要平台原生代码。

### 安全要求

Tauri 不会自动让应用绝对安全。仍然需要：

- 缩小 Command 白名单。
- 对参数、路径和 URL 做校验。
- 限制 Sidecar 可执行文件和启动参数。
- 将工具权限、用户审批和 Sandbox 放在 Runtime/执行层。
- 防止 WebView 内容获得超出需要的本地能力。

### 适合

- 准备深耕 Rust Agent Runtime。
- 重视安装包、启动速度和资源占用。
- 需要 Web UI，但不想携带完整 Chromium。
- 愿意投入跨平台 WebView 适配成本。

---

## 3.3 原生客户端

常见选项：

```text
macOS：SwiftUI / AppKit
Windows：WinUI / WPF
Linux：GTK
```

### 优点

- 操作系统集成最好。
- 原生菜单、窗口、快捷键、通知和无障碍体验更自然。
- 启动速度、内存和包体积更容易精细控制。
- 更容易使用平台特有安全能力和系统 API。

### 缺点

- 跨平台开发成本最高。
- macOS、Windows、Linux 可能需要不同 UI 代码。
- 团队需要掌握多种原生技术栈。
- Markdown、代码 Diff、富文本编辑器等需要额外组件。
- 产品高速迭代时，通常不如 Web 技术灵活。

### 适合

- 只做一个平台。
- 对原生体验要求极高。
- 需要深度操作系统集成。
- 有成熟原生客户端团队。

---

## 3.4 Flutter Desktop

### 架构

```text
Dart 业务代码
    ↓
Flutter 自有渲染引擎
    ↓
Windows / macOS / Linux
```

### 优点

- 多平台 UI 高度一致。
- 复杂动画和自定义界面表现较好。
- 可以与移动端共享大量代码。
- 不依赖各平台 WebView 的 DOM/CSS 差异。

### 缺点

- 不能直接复用 React/Vue 组件生态。
- 桌面端生态弱于 Flutter 移动端和 Electron。
- 深度本地能力经常需要插件或平台通道。
- Agent Runtime 通常仍适合独立为 Sidecar。
- 部分控件的桌面原生感需要额外打磨。

### 适合

- 已有 Flutter/Dart 团队。
- 同时建设桌面和移动端。
- UI 一致性比原生外观更重要。

---

## 3.5 Qt

### 架构

```text
C++ / Python
    ↓
Qt 跨平台 UI 与系统库
```

### 优点

- 专业桌面和工业软件领域成熟。
- 跨平台能力强。
- 系统、网络、多媒体和图形能力完整。
- 适合高性能和复杂本地应用。

### 缺点

- C++ 开发和内存安全成本较高。
- Web UI 组件无法直接复用。
- UI 设计可能需要较多定制。
- 商业分发前需要认真评估许可证要求。

### 适合

- 工业软件和专业桌面工具。
- 已有 C++/Qt 团队。
- 大量能力完全在本地运行。

---

## 3.6 .NET：WPF、WinUI、Avalonia、MAUI

### 特点

- WPF/WinUI 适合 Windows 企业客户端。
- Avalonia 更强调 .NET 跨平台桌面。
- MAUI 适合已有 .NET 移动和桌面技术栈的团队。

### 优点

- C# 工程效率和企业生态成熟。
- Windows 系统集成好。
- 适合企业认证、办公集成和内部软件。

### 缺点

- 不同框架的跨平台成熟度和 UI 一致性不同。
- 如果 Runtime 使用 Rust/Go/Node，仍需要进程协议或 FFI。
- Web 编辑器和前端组件复用不如 Electron 直接。

### 适合

- Windows 为主的银行、政企和内部桌面 Agent。
- 团队已有 .NET 技术积累。

---

## 3.7 Wails 等轻量 WebView 壳

Wails 采用 Web UI + Go 本地后端，整体思路与 Tauri 类似：

```text
React/Vue UI
     ↓
系统 WebView
     ↓
Go Host
```

优点是 Go 服务端团队容易上手，包体积通常低于 Electron；代价是生态、桌面插件和社区规模相对较小。

---

## 3.8 Web/PWA

### 优点

- 无需传统安装或安装成本低。
- 更新统一在服务端完成。
- 天然跨平台。
- 适合云端模型与云端 Runtime。

### 缺点

- 浏览器安全模型限制本地文件、Shell、Git 和进程操作。
- 很难实现完整 Coding Agent 的本地执行能力。
- 本地目录访问依赖浏览器能力和用户授权。
- 长任务、后台执行和系统集成受到浏览器生命周期限制。

### 适合

- 云端 Agent。
- 普通 Chatbox。
- 不需要深度控制用户电脑的场景。

---

## 4. 桌面框架总对比

| 方案 | UI 技术 | 包体积/内存 | 跨平台一致性 | 本地能力 | 开发速度 | 主要风险 |
|---|---|---|---|---|---|---|
| Electron | Web + 自带 Chromium + Node | 较高 | 高 | 强 | 快 | 资源占用、IPC/Node 权限 |
| Tauri | Web + 系统 WebView + Rust | 较低 | 中高 | 强 | 中 | WebView 差异、Rust 门槛 |
| 原生 | Swift/WinUI 等 | 可控 | 低 | 最强 | 单平台快、跨平台慢 | 多平台重复开发 |
| Flutter | Dart + 自绘引擎 | 中 | 高 | 中强 | 中 | 桌面插件、原生集成 |
| Qt | C++/Python + Qt | 中 | 高 | 强 | 中 | C++复杂度、许可证 |
| .NET | C# + 对应 UI 框架 | 中 | 取决于框架 | 强 | Windows 快 | 跨平台差异 |
| Wails | Web + WebView + Go | 较低 | 中高 | 强 | 中 | 生态规模 |
| PWA | Browser | 低 | 高 | 弱 | 最快 | 无法承担完整本地执行 |

“较高、较低”是相对比较，不代表固定数字；实际结果取决于依赖、资源、调试信息和打包策略。

---

## 5. C/S 部署架构选项

桌面壳选完以后，还要决定 UI 与 Runtime 怎样组合。

## 5.1 单进程内嵌

```text
Desktop Process
├─ UI
├─ Agent Runtime
└─ Tool Execution
```

### 优点

- 架构简单。
- 不需要跨进程协议。
- 调试路径短。
- 适合最小 Demo。

### 缺点

- UI 和 Agent 生命周期强耦合。
- Runtime 崩溃可能拖垮 UI。
- 很难复用到 CLI、IDE 和其他客户端。
- 权限边界容易混乱。
- 长任务恢复和独立升级困难。

### 判断

适合验证想法，不适合作为复杂 Agent 的长期架构。

---

## 5.2 UI + Sidecar 子进程

```text
Desktop UI
    ↓ stdio / Pipe
App Server Sidecar
    ↓
Agent Runtime
```

Sidecar 是由桌面应用启动和管理的独立本地进程。

### 优点

- UI 与 Runtime 语言解耦。
- 默认不需要监听 TCP 端口。
- 生命周期明确：客户端启动、关闭和监控 Sidecar。
- Runtime 可以被 CLI、IDE 和桌面端复用。
- 进程崩溃边界比单进程清晰。
- 适合使用 JSONL + JSON-RPC-like。

### 缺点

- 需要处理进程启动、退出和崩溃。
- 需要定义稳定协议和 Schema。
- stderr、stdout 和业务消息必须严格分离。
- UI 关闭后任务是否继续，需要明确设计。
- 升级时要保证 UI 与 Sidecar 版本匹配。

### 判断

这是本地 Agent 客户端非常实用的默认方案，也是理解 Codex App Server 架构的关键。

---

## 5.3 本地常驻服务 + Unix Socket/Named Pipe

```text
Desktop App ──┐
IDE Plugin ───┼→ Local Agent Service
CLI ──────────┘   ↑
                  Unix Socket / Named Pipe
```

### 优点

- 一个 Runtime 服务多个本地客户端。
- UI 关闭后任务可以继续运行。
- 适合共享缓存、模型连接和任务队列。
- Unix Socket 可使用文件权限限制本机访问。

### 缺点

- 服务安装、启动、升级和卸载复杂。
- macOS/Linux 和 Windows 的 IPC 机制不同。
- 多客户端并发和任务归属需要额外设计。
- 需要处理旧服务残留、Socket 清理和版本兼容。

### 判断

适合成熟产品、多客户端或长任务，不一定适合第一版 MVP。

---

## 5.4 本地 WebSocket/TCP 服务

```text
Desktop UI
    ↓ ws://127.0.0.1:PORT
Local App Server
```

### 优点

- 客户端库成熟。
- Web 页面、IDE 和其他语言容易连接。
- 天然支持双向消息和流式事件。
- 调试方便。

### 缺点

- 需要端口管理。
- 可能发生端口冲突。
- 监听地址配置错误时可能暴露到局域网。
- 需要认证、Origin 检查和连接权限控制。
- 不能因为监听在 localhost 就忽略本机恶意程序。

### 判断

适合多客户端和调试，但单一桌面 UI 通常优先考虑 stdio 或本地 Socket。

---

## 5.5 远程 Runtime / 云端 Agent

```text
Desktop/Web Client
       ↓ HTTPS/WSS
Cloud Agent Runtime
       ↓
Remote Sandbox / Worker
```

### 优点

- 任务可以在客户端关闭后继续。
- 计算和环境统一管理。
- 易于企业审计、配额和集中更新。
- 适合多设备访问同一任务。

### 缺点

- 本地代码和数据需要上传或远程挂载。
- 隐私、安全与合规成本高。
- 依赖网络。
- 本地 IDE、文件和进程集成更复杂。
- 云端 Worker 和 Sandbox 成本较高。

### 判断

适合云端 Coding Agent、企业集中式 Agent，不适合所有本地隐私场景。

---

## 5.6 本地 + 云端混合架构

```text
桌面 UI
   ↓
本地 Runtime
   ├─ 本地文件、Git、Shell、Sandbox
   └─ HTTPS → 云端模型/企业 Model Gateway
```

这是当前很多 Coding Agent 的实际形态：

- 本地负责上下文、工具和真实执行。
- 云端负责模型推理。
- 可选云端负责账号、同步、远程任务和企业策略。

它兼顾本地能力和云端模型，但必须认真处理代码数据上传边界。

---

## 6. 本地通信方式怎么选

| 传输方式 | 最适合 | 优点 | 缺点 |
|---|---|---|---|
| stdio + JSONL | UI 管理一个 Sidecar | 无端口、简单、天然一对一 | 不适合多客户端，生命周期绑定明显 |
| Unix Socket | macOS/Linux 本地常驻服务 | 本机专用、文件权限、无端口 | Windows 需替代方案，清理和服务管理复杂 |
| Named Pipe | Windows 本地服务 | Windows 原生、本地权限控制 | 跨平台抽象成本 |
| localhost WebSocket | 多语言、多客户端、调试 | 双向、生态成熟、易接入 | 端口、认证和暴露风险 |
| HTTPS/WSS | 远程 Runtime | 跨网络、标准化 | 网络、安全、延迟、成本 |

推荐规则：

```text
一对一桌面 Sidecar      → stdio + JSONL
本机多个客户端共享服务   → Unix Socket / Named Pipe
需要浏览器或多语言连接   → localhost WebSocket
远程 Agent             → HTTPS/WSS
```

---

## 7. Agent 客户端为什么适合分层架构

## 7.1 多入口复用同一个 Runtime

```text
CLI ─────────┐
IDE ─────────┼→ App Server / Agent Runtime
Desktop ─────┤
Automation ──┘
```

如果每个客户端自己实现 Runtime，会产生：

- Agent 行为不一致。
- Tool、权限和审批重复实现。
- Bug 需要多处修复。
- Skills、MCP 和配置逻辑分叉。
- 安全策略无法统一。

## 7.2 支持长任务和状态管理

Agent 任务不是普通聊天请求，可能经历：

```text
分析 → Tool → 审批 → 执行 → 测试 → 重试 → 完成
```

Runtime 需要维护：

- Thread、Turn、Item。
- 当前 Workflow 节点。
- Tool 调用和输出。
- 用户审批结果。
- 取消、恢复和失败状态。
- Token、成本和执行日志。

这些状态不适合只保存在 UI 组件中。

## 7.3 安全边界更清晰

推荐：

```text
UI
只负责展示和收集用户输入
        ↓
App Server
协议校验、连接管理
        ↓
Runtime
任务状态、上下文、模型循环
        ↓
Policy / Approval
权限判断和用户授权
        ↓
Sandbox / Worker
限制实际执行范围
```

但必须强调：分进程本身不是 Sandbox。两个进程如果拥有相同系统权限，仍然需要额外的权限策略和隔离机制。

## 7.4 UI 技术可以替换

只要协议保持稳定：

```text
Electron UI
    ↕
Tauri UI
    ↕        都可以接入同一个 App Server
Native UI
```

这样可以独立演进界面和 Runtime。

---

## 8. Codex 采用这套架构的可确认事实

以下来自 OpenAI 公开仓库和 App Server 文档：

1. `openai/codex` 是运行在用户电脑上的本地 Coding Agent。
2. 仓库包含 Codex CLI、本地 Core/Runtime、App Server、工具与安全执行相关实现。
3. `codex app-server` 用于支撑 VS Code Extension 等丰富客户端。
4. App Server 使用双向 JSON-RPC 2.0 消息，线上省略 `"jsonrpc":"2.0"` 字段。
5. 默认传输是 `stdio + JSONL`。
6. 可选 WebSocket、Unix Socket 和关闭本地监听。
7. 协议核心对象包括 Thread、Turn 和 Item。
8. 客户端可以接收流式事件、Tool 进度和服务端发起的审批请求。

Codex 的公开主链路可以理解为：

```text
CLI / IDE / Rich Client
          ↓
      App Server
          ↓
   Codex Core/Runtime
      ├─ Model API
      └─ Tool/Approval/Sandbox
```

## 8.1 能合理推断的工程原因

下面是基于公开架构的工程分析，不是 OpenAI 内部选型会议原话：

- CLI、IDE、桌面端可以复用同一套 Runtime。
- JSON-RPC 让 UI 技术与 Rust Runtime 解耦。
- 双向连接适合流式输出、Tool 事件和审批请求。
- stdio 适合由客户端启动的一对一 Sidecar，避免开放本地端口。
- 独立 Runtime 更适合长任务、状态、取消和恢复。
- 本地执行可以直接使用用户项目、Git、编译器和测试环境。
- Sandbox 和 Approval 可以集中实现，而不是散落在多个 UI 中。

## 8.2 当前不能从公开资料直接确认的内容

- Codex 桌面 App 完整 UI 是否全部开源。
- 桌面壳最终使用 Electron、Tauri 还是其他框架的完整实现细节。
- OpenAI 内部选择某个桌面框架的原始决策记录。
- 桌面客户端、App Server 和云端服务的所有私有组件边界。

因此，不应仅根据 `openai/codex` 仓库就断言 Codex 桌面 App 一定使用某种壳框架。

---

## 9. 选型维度

正式选型前至少回答以下问题。

### 9.1 产品范围

- 只支持 Windows，还是支持三平台？
- 是普通 Chatbox，还是 Coding Agent？
- 是否需要离线或内网使用？
- UI 关闭后，任务是否必须继续？
- 是否需要多个客户端连接同一个 Runtime？

### 9.2 团队能力

- 团队主要掌握 React、Rust、Go、C#、Swift 还是 Flutter？
- 是否能维护平台原生模块？
- 是否具备桌面签名、打包和自动更新经验？
- 是否能维护 Sandbox 和安全执行层？

### 9.3 本地能力

- 是否需要 Shell、Git、编译器和浏览器自动化？
- 是否需要读写整个项目目录？
- 是否需要访问数据库、企业系统或硬件？
- Tool 在本机执行还是远程 Worker 执行？

### 9.4 安全合规

- 哪些数据可以发送给云端模型？
- 是否需要本地脱敏？
- 哪些 Tool 必须审批？
- Sandbox 限制哪些目录、网络和进程？
- 日志是否可能包含 Key、Token 和业务数据？

### 9.5 生命周期

- Runtime 是否跟随 UI 启停？
- 任务中断以后能否恢复？
- 客户端与 Runtime 如何升级和兼容？
- 如何取消模型请求、Tool 和子进程树？

### 9.6 交付成本

- 安装包允许多大？
- 首次启动时间要求是什么？
- 是否需要增量更新？
- Windows 签名、macOS 公证如何处理？
- 三个平台怎样做自动化验收？

---

## 10. 决策树

```text
是否需要深度访问本地文件、Shell、Git？
├─ 否
│  └─ Web/PWA + Remote Runtime
└─ 是
   ↓
是否只支持单一平台并追求原生体验？
├─ 是
│  └─ 原生 UI + Runtime Sidecar
└─ 否
   ↓
团队是否以 React/TypeScript 为主，并要求快速交付？
├─ 是
│  └─ Electron + App Server Sidecar
└─ 否
   ↓
是否重视小体积、低资源，并愿意投入 Rust？
├─ 是
│  └─ Tauri + Rust Runtime
└─ 否
   ↓
根据现有技术栈选择 Flutter、.NET、Qt 或 Wails
```

运行时通信继续判断：

```text
一个 UI 管理一个 Runtime？
├─ 是 → stdio + JSONL
└─ 否
   ↓
是否只允许本机客户端？
├─ 是 → Unix Socket / Named Pipe
└─ 否 → WebSocket/HTTPS + 身份认证
```

---

## 11. 针对本地 Agent 的推荐架构

### 11.1 MVP 推荐

```text
Electron + React
        ↓ stdio + JSONL
App Server Sidecar
        ↓
Agent Runtime
        ├─ Model Gateway
        ├─ Tool Router
        ├─ Approval
        └─ Sandbox
```

选择理由：

- 前端迭代快。
- 代码编辑器、Diff 和 Markdown 生态成熟。
- stdio 无需端口和本地网络认证。
- Runtime 独立，后续可以迁移到 Tauri 或其他 UI。

### 11.2 长期基础设施推荐

```text
Tauri/Native UI
        ↓ stdio 或 Local Socket
Rust App Server
        ↓
Durable Agent Runtime
        ├─ Workflow
        ├─ State Store
        ├─ Tool Router
        ├─ Policy/Approval
        ├─ Sandbox/Worker
        └─ Trace/Evaluation
```

选择理由：

- 运行时、协议和系统执行能力可以集中在 Rust。
- UI 框架可以替换。
- 更适合深耕 Agent Runtime 与 Execution Infrastructure。
- 后期可以增加 IDE、CLI 和远程客户端。

### 11.3 企业混合架构

```text
企业桌面客户端
    ↓
本地 Runtime
    ├─ 本地知识与文件
    ├─ 本地脱敏
    ├─ Tool Approval
    └─ Sandbox
    ↓ HTTPS/WSS
企业 Model Gateway
    ├─ 模型路由
    ├─ 配额
    ├─ 审计
    └─ 多模型供应商
```

本地 Runtime 负责真实工作环境，企业 Gateway 负责模型、账号、审计和供应商管理。

---

## 12. 常见错误

### 错误一：认为选了 Electron 就等于页面套壳

错误原因：框架只决定 UI 技术，不决定业务是否在本地运行。

### 错误二：让 Renderer 直接执行 Shell

风险：页面漏洞可能直接获得本地命令执行能力。

### 错误三：把 Agent 状态全部保存在前端 Store

风险：刷新、崩溃或升级会导致长任务状态丢失。

### 错误四：用 localhost 就认为安全

风险：本机其他进程仍可能尝试连接，错误绑定还可能暴露到局域网。

### 错误五：把分进程当作 Sandbox

风险：如果两个进程拥有相同系统权限，攻击影响范围并没有自动缩小。

### 错误六：第一版就做复杂多 Agent

风险：单 Agent 的状态、Tool、安全和恢复还没稳定，多 Agent 会放大问题。

### 错误七：UI 和 Runtime 使用私有、无版本协议

风险：升级后客户端和 Runtime 无法兼容，历史任务也难以恢复。

---

## 13. 最小 PoC 验收清单

选型不应该只看文章，应通过同一组任务对不同方案做 PoC。

### 功能验收

- 能启动和停止 Runtime Sidecar。
- UI 能发送 `initialize` 和任务请求。
- 能接收流式文本和 Tool 事件。
- 能展示审批并返回 Allow/Deny。
- 能安全读取指定工作区文件。
- 能在限定目录运行测试命令。
- Tool 超时后可以取消完整进程树。
- UI 重启后能读取已保存任务。

### 性能验收

- 冷启动时间。
- 空闲内存。
- 一个完整任务的峰值内存。
- 安装包大小。
- 长日志流对 UI 的影响。
- 多任务并发时的稳定性。

### 安全验收

- Renderer 无法直接调用任意系统命令。
- 路径遍历不能越过工作区。
- 未审批的写操作不能执行。
- 日志不包含完整 Key、Token 和 Cookie。
- localhost 服务不能被无授权页面调用。
- Sandbox 网络和文件限制真实有效。

### 跨平台验收

- Windows 安装、升级和卸载。
- macOS 签名、公证和权限提示。
- 路径、换行符和 Shell 差异。
- Unix Socket 与 Named Pipe 的替代实现。
- 子进程退出和残留清理。

---

## 14. 最终建议

如果目标是快速做出可验收的桌面 Agent：

```text
Electron + React
+ 独立 App Server Sidecar
+ stdio/JSONL
+ 明确的 Tool/Approval/Sandbox 边界
```

如果目标是长期深耕 Agent Runtime 和本地执行基础设施：

```text
Web UI 或原生 UI
+ Rust App Server/Runtime
+ 可替换的 UI 壳
+ Durable Workflow
+ Secure Tool Execution
+ Trace/Evaluation
```

选型时最应该坚持的原则：

> UI 壳可以更换，Runtime 不应跟着重写；模型供应商可以更换，Tool 安全边界不应失效；客户端可以升级，进行中的任务状态不应无故丢失。

---

## 15. 参考资料

- [OpenAI Codex 开源仓库](https://github.com/openai/codex)
- [Codex App Server 协议与传输](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md)
- [Electron 官方文档](https://www.electronjs.org/docs/latest/)
- [Tauri 官方文档](https://tauri.app/)
- [Flutter Desktop 官方文档](https://docs.flutter.dev/platform-integration/desktop)
- [Qt 官方文档](https://doc.qt.io/)
- [Avalonia 官方文档](https://docs.avaloniaui.net/)
- [Wails 官方文档](https://wails.io/docs/introduction/)
