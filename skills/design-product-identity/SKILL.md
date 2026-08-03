---
name: design-product-identity
description: "Create a theme-aligned clean and minimal product identity during the design phase, including logo concept, symbol, wordmark, lockups, light/dark/monochrome variants, favicon or app icon, color and typography tokens, usage rules, editable Figma structure, and production SVG evidence. Use when a new product or major redesign needs a logo and minimum brand system that must appear inside the first high-fidelity product screens."
---

# 产品品牌与 Logo

## 输入门禁

要求产品定位、目标人群、核心问题、使用场景、名称状态和主要载体已明确。名称未定时使用清楚标记的临时名，不擅自替用户定名。

读取 [identity-contract.md](references/identity-contract.md) 和 [clean-fresh-minimal-identity.md](references/clean-fresh-minimal-identity.md)。

## 默认方向

使用 `clean-fresh-minimal`：一个 Logo 表达一个核心意象；色彩有限；轮廓清晰；留白充分；小尺寸可识别；每个元素都能解释与产品主题的关系。

禁止无意义叠加叶子、星光、圆环、渐变和装饰图形。若产品属于安全、工业或严肃场景，保留干净简洁，但调整色彩与气质并说明原因。

## 工作流

1. 提取 3–5 个品牌关键词、一个核心意象和明确 avoid list。
2. 默认给一个经过判断的推荐主方向；只有语义确实分叉时再给最多两个备选。
3. 可使用 `imagegen` 探索 `logo-brand` 位图方向，但生成图只能作为草图，不能冒充最终 Logo。
4. 在 Figma 中重建可编辑的几何、文字和矢量结构；所有 Figma Plugin API 写入遵循 `figma-use` 且严格串行。
5. 把推荐 Logo 应用到核心页面、导航、登录区或产品封面中，与 UI 一起评审。
6. 用户确认后完成图形标、文字标、横向组合、深浅色、单色、反白和小图标版本。
7. 导出 SVG；运行 `scripts/validate_svg.py <file.svg>` 检查 XML、viewBox、尺寸、外链位图和脚本风险。

## 交付合同

- 核心创意与一句话解释。
- 图形标、文字标、横向组合。
- 浅色、深色、单色、反白版本。
- favicon / App Icon；具体尺寸按已确认载体输出。
- 主色、辅助色、中性色与字体方向。
- 安全距离、最小尺寸和禁止用法。
- 可编辑 Figma 节点和生产 SVG；需要时补 PNG 尺寸集。
- Logo 与核心页面同框截图。
- 原创性和近似风险初筛；明确这不等于法律商标结论。

## 用户闸门

Logo 单体与页面应用必须同时确认。用户未确认 `BRAND_AND_VISUAL_APPROVED` 时，不得把 Logo、颜色或字体作为前端定稿。
