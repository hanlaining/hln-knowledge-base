# Product Delivery Skill Group

这是一套把模糊产品想法推进到可验收全栈产品的 Skill 分组。它统一管理产品发现、体验设计、品牌与 Logo、Figma 原型、前端、后端、契约和测试交付，同时保留每个 Skill 独立安装与复用的能力。

## 从这里开始

- 总编排入口：[deliver-product-end-to-end](./deliver-product-end-to-end/SKILL.md)
- 完整方案：[从烂 Prompt 到全栈产品交付 Meta-Skill 方案 V0.3](./docs/从烂Prompt到全栈产品交付_Meta-Skill方案V0.3.md)
- 验收方法：[端到端产品交付 Skill 验收 SOP](./docs/端到端产品交付Skill_验收SOP.md)
- Agent 共享上下文：[CONTEXT.md](./CONTEXT.md)

## Skill 地图

| 阶段 | Skill | 作用 |
|---|---|---|
| 总编排 | [deliver-product-end-to-end](./deliver-product-end-to-end/SKILL.md) | 管理阶段、审批门、证据和并发 worker |
| 产品体验 | [design-product-experience](./design-product-experience/SKILL.md) | 澄清用户、场景、问题、旅程、状态与体验门禁 |
| 品牌设计 | [design-product-identity](./design-product-identity/SKILL.md) | 生成贴合主题的清新简洁 Logo 与品牌规范 |
| 参考研究 | [research-product-references](./research-product-references/SKILL.md) | 研究竞品和优质开源项目，区分借鉴与直接复用 |
| 前端实现 | [implement-product-frontend](./implement-product-frontend/SKILL.md) | 在原型确认后按 Figma 1:1 实现前端与交互 |
| 服务契约 | [define-service-contracts](./define-service-contracts/SKILL.md) | 冻结接口、模型、错误、认证和状态约定 |
| 后端底座 | [bootstrap-backend-foundation](./bootstrap-backend-foundation/SKILL.md) | 建立可生产化、可独立验证的后端基础 |
| 后端切片 | [implement-backend-slices](./implement-backend-slices/SKILL.md) | 按冻结契约实现可独立验收的业务切片 |
| 集成验收 | [integrate-and-verify-product](./integrate-and-verify-product/SKILL.md) | 完成真实启动、浏览器、契约、安全与端到端验收 |

## 默认流程

```text
孵化 Chat：模糊 Prompt → 主动产品提问 → 项目确认
  → 用户说“现在去把这个项目落地”
  → 结构化 Project Launch Brief
  → 新建执行 Chat
  → 用户价值与体验方案
  → Logo、视觉和交互原型
  → 用户审核确认 Figma
  → 技术方案与服务契约
  → 前后端并行实现
  → 集成、测试和证据验收
  → 用户确认交付
```

产品原型未确认前，不进入前后端实现。技术选型默认在产品原型确认后讨论并冻结。

孵化 Chat 只负责讨论，不写项目；执行 Chat 只接收精简交接包，不复制整段聊天，也不重复询问已经确认的内容。

## 安装说明

本目录是知识库中的分组容器，不是一个可直接安装的单体 Skill。需要使用哪个能力，就把对应的子目录安装到 `~/.codex/skills/<skill-name>/`；若希望自动编排整套流程，至少安装 `deliver-product-end-to-end` 及它在任务中调用的子 Skill。
