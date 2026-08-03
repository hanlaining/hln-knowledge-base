---
name: design-product-experience
description: "Design a complete user-centered product experience from confirmed requirements and product value, including user jobs, friction analysis, information architecture, user journeys, clean-fresh-minimal page visuals, real copy, components, responsive layouts, interaction states, failure recovery, accessibility, trust, and motion, then prepare or create a structured Figma prototype with explicit user checkpoints. Use for new products, new pages, substantial UI redesigns, or vague requests that need a useful, intuitive, polished, and theme-aligned experience before code implementation."
---

# 产品体验设计

## 前置条件

要求 `PRODUCT_CONFIRMED`：目标人群、核心问题、最短旅程、MVP、非目标和草案 ACxx 已由用户确认。没有确认时返回需求阶段，不画高保真页面。

读取 [product-experience-quality-gate.md](references/product-experience-quality-gate.md)、[clean-fresh-minimal-pages.md](references/clean-fresh-minimal-pages.md) 和 [interaction-state-contract.md](references/interaction-state-contract.md)。

## 设计顺序

1. 先输出 Product Experience Brief：目标用户、触发场景、核心任务、期望结果、当前摩擦、风险、非目标和可观察体验目标。
2. 分别设计首次使用、高频核心任务、低频高级任务和高风险失败恢复；说明为什么保留每个页面或功能。
3. 输出页面地图、入口、核心对象、信息优先级、用户旅程和摩擦地图。
4. 为每个旅程列出默认、hover、focus、active、disabled、loading、empty、error、success、无权限、取消与恢复。
5. 使用真实产品文案，不用 Lorem ipsum、无意义大标题或空泛 AI 副标题。
6. 先确认低保真结构与体验取舍，再调用 `design-product-identity` 形成 Logo 与品牌方向。
7. 把 Logo、视觉 Token 和推荐主题放入第一版核心页面，让用户在真实上下文中评审。
8. 用户确认品牌与视觉后，完成所有核心页面、组件变体、异常状态和交互连接。
9. 为最短旅程和关键失败路径编写逐步点击验收脚本，并记录完成步骤、理解偏差、犹豫点和恢复结果。

## Figma 路由

从零创建 Figma 时：

1. 确认 Figma MCP、OAuth 和目标文件权限真实可用。
2. 使用 `figma-create-new-file` 创建文件；所有 Plugin API 写入同时遵循 `figma-use`。
3. 使用 `figma-generate-library` 先建立变量、字体、组件和 Token；每个阶段要求用户确认。
4. 使用 `figma-generate-design` 按页面 wrapper → section 顺序逐段创建页面。
5. 每次 Figma mutation 严格串行；不得并行执行 `use_figma`。
6. 每个 section 用 metadata 与 screenshot 验证，修复裁切、重叠、占位文案和错误变体。

若 `figma-use` 或 Figma MCP 不可用，交付结构、页面规格、Token、交互合同和 blocked 证据；不得用扁平图片冒充正式 Figma。

## 必须展示给用户

```text
Logo 与品牌区
→ 核心首页/工作台
→ 一个核心任务页
→ 一个表单或操作流程
→ loading / empty / error / 无权限
→ 主要弹窗或抽屉
→ 完整可点击主路径
```

## 质量门禁

- 每个功能都能追溯到目标用户、真实场景、核心任务和 ACxx；无法解释价值的功能移出 MVP。
- 一个页面只有一个清晰主任务。
- 首次用户无需先理解系统内部结构就能获得第一次成功；高频任务减少重复输入和无意义跳转。
- 信息按决策顺序出现，高级项渐进披露；默认值可预测且允许撤销。
- 用户始终知道系统状态、当前结果、下一步和退出/恢复方式；危险操作说明后果并防误触。
- Logo、页面、组件、图标和动效共享同一套 Token 与气质。
- 不堆叠无意义卡片、渐变、玻璃拟态、光晕和装饰球。
- 图片、插画和图标必须能解释与产品主题的关系。
- 键盘、焦点、对比度、触控目标和 reduced motion 有明确处理。
- 响应式按真实目标窗口设计，不以“自适应”一句话代替状态。

## 交付 Evidence

- Product Experience Brief、功能价值说明、信息优先级和摩擦地图。
- 页面地图、用户旅程和状态矩阵。
- Figma 文件、关键节点 ID、组件/变量清单和交互链接。
- 核心页面与各异常状态截图。
- 点击验收脚本和实际体验结果。
- 核心任务完成观察：入口是否被发现、完成步骤/时间、主要犹豫点、错误恢复和结果是否被正确理解；不伪造量化结论。
- 用户对 `STRUCTURE_APPROVED`、`BRAND_AND_VISUAL_APPROVED`、`FIGMA_PROTOTYPE_APPROVED` 的明确确认。
- 推断项、未解决项和设计偏差。

未获得 `FIGMA_PROTOTYPE_APPROVED` 时不得触发真实项目技术方案或业务代码。
