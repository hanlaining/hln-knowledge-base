# Agent 学习笔记

本目录按学习阶段、源码专题和自主 Runtime 研究分类，避免把桌面客户端、Agent Runtime、LLM 模型原理与远期系统愿景混在一起。

## 目录结构

```text
agent 学习笔记/
├─ 01-入门与架构选型/
│  ├─ cs架构选型.md
│  └─ 从0到1手写Agent-框架选型与MVP学习路线.md
├─ 02-Codex源码学习/
│  └─ Codex-Skill选择加载与多Skill执行机制.md
├─ 03-Grok源码学习/
│  ├─ Grok-Build-CLI-Agent架构深度解析.md
│  └─ Grok-1开源项目源码架构深度解析.md
├─ 04-从0手戳Agent/
│  └─ 01-MCP入门与JSONRPC安全机制.md
└─ 05-God-Agent与统一智能体体系/
   └─ God-Agent中央大脑统一Agent-Runtime持续架构讨论.md
```

## 推荐阅读顺序

1. [CS 架构选型](./01-入门与架构选型/cs架构选型.md)：先理解桌面客户端、Runtime 与通信边界。
2. [从 0 到 1 手写 Agent](./01-入门与架构选型/从0到1手写Agent-框架选型与MVP学习路线.md)：确定 Electron 学习版到 Rust Runtime 的实现路线。
3. [Codex Skill 机制](./02-Codex源码学习/Codex-Skill选择加载与多Skill执行机制.md)：理解 Skill 的发现、选择、加载与多 Skill 行为。
4. [MCP 入门与 JSON-RPC 安全机制](./04-从0手戳Agent/01-MCP入门与JSONRPC安全机制.md)：理解 MCP、Tool、Skill、Runtime、JSON-RPC、Approval 与 Sandbox 的边界。
5. [Grok Build Agent 架构](./03-Grok源码学习/Grok-Build-CLI-Agent架构深度解析.md)：研究完整 Coding Agent CLI、Runtime、ACP、Tool 与 Sandbox。
6. [Grok-1 模型架构](./03-Grok源码学习/Grok-1开源项目源码架构深度解析.md)：补充 Transformer、GQA、KV Cache、MoE 与模型推理原理。
7. [God-Agent 中央大脑统一 Agent Runtime](./05-God-Agent与统一智能体体系/God-Agent中央大脑统一Agent-Runtime持续架构讨论.md)：从耐久执行底座进入 Task Contract、Context Compiler、Completion Proof、双执行链路和统一智能体体系研究。

## 分类说明

- `01-入门与架构选型`：回答“先做什么、客户端与 Runtime 怎样拆”。
- `02-Codex源码学习`：记录 OpenAI Codex 的具体实现机制。
- `03-Grok源码学习`：同时区分 Grok Build 的 Agent 系统和 Grok-1 的模型推理层。
- `04-从0手戳Agent`：按 Codex-like 架构逐步实现 Protocol、App Server、Runtime、安全执行、Skills 与 MCP。
- `05-God-Agent与统一智能体体系`：记录自主 Agent Runtime、中央控制闭环、可靠执行、完成证明和远期统一智能体体系的持续研究。
