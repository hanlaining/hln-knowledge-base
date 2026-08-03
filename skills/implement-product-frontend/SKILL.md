---
name: implement-product-frontend
description: "Implement an approved structured Figma prototype as a production frontend with 1:1 visual and interaction fidelity, project-native components and tokens, real states, accessibility, responsive behavior, contract-driven data access, and screenshot evidence. Use only after the Figma prototype, technical plan, and frontend-backend contracts are approved; supports Claude CLI Graph workers and Element Plus or Iconfont only when explicitly selected in the technical plan."
---

# 设计稿前端实现

## 前置闸门

要求 `FIGMA_PROTOTYPE_APPROVED`、`TECH_PLAN_APPROVED` 和 `CONTRACT_APPROVED`。必须有目标 Figma 文件/节点、页面验收脚本和已批准 worktree。

读取 [frontend-delivery-contract.md](references/frontend-delivery-contract.md)。

## Figma 到代码

1. 使用当前官方 `figma-design-to-code`；需要结构化上下文时同时遵循 `figma-implement-design`。
2. 先获取精确节点的 `get_design_context` 与 `get_screenshot`，响应过大时先读 metadata 再按子节点获取。
3. 使用 Figma 提供的真实资产，不安装新的图标包、不用占位图替代已有资产。
4. 分析项目组件、Token、路由、状态、数据获取和测试约定；需要时使用 `figma-create-design-system-rules` 建立项目规则。
5. 把 Figma 表达翻译成项目原生技术，不把生成的 React/Tailwind 代码直接当最终代码。

## 实现规则

- 每个共享页面/设计系统同一时刻只有一个 UI 写入 Worker。
- 优先扩展已有组件，不重复造相同按钮、表单、弹窗和布局。
- 使用设计 Token，不散落硬编码颜色、间距、圆角和阴影。
- Element Plus 与 Iconfont 只有在技术方案明确选用时接入；Logo 使用独立 SVG，不进入 Iconfont。
- 实现 default、hover、focus、active、disabled、loading、empty、error、success、无权限、取消和恢复。
- 遵守键盘、焦点、语义标签、对比度、reduced motion 和目标响应式状态。
- 数据请求严格遵循冻结合同；不得为了方便让前端猜测字段或吞掉后端错误。

## Graph Worker

把页面按可独立验收的用户结果拆 Issue，不按模糊技术层拆。使用 `agent-task-supervisor` 和 `claude-code-cli-development`；每个 Issue 绑定 Rxx、ACxx、精确文件范围、Red/Green 和视觉 Evidence。

## 1:1 验收

1. 在与 Figma 相同 viewport 运行真实页面。
2. 使用 Playwright 或项目现有浏览器工具截图主页面和关键状态。
3. 比较布局、字体、颜色、资产、组件状态和交互；差异必须有数值或可观察描述。
4. 运行真实点击旅程、响应式、可访问性和前端测试。
5. 不用 AI 生成图或 Worker 自述替代真实浏览器截图。

交付：完整 diff、测试命令/退出码、Figma 与浏览器截图、差异结论、未验证项、P0–P3 Review 和相关 ACxx 状态。
