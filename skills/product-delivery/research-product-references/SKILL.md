---
name: research-product-references
description: "Research competing products and high-quality open-source GitHub projects for a confirmed product scenario, explain what product structure or interaction can be borrowed, classify direct reuse versus selective extraction versus concept reference, and report maintenance, license, security, and fit risks. Use after the target users, scenario, and core problem are known and before the product prototype freezes; do not use references to prematurely lock the implementation stack."
---

# 产品参考调研

## 输入门禁

要求至少存在：应用场景、目标人群、核心问题、最短用户任务和非目标。缺少会改变产品方向的信息时，每轮只问 1–3 个问题。

原型冻结前只研究产品结构、信息架构、文案组织和交互模式；不得因为某仓库好看就提前绑定框架或复制代码。

## 调研流程

1. 从 Rxx 与 ACxx 提取 3–6 个检索维度：用户、任务、设备、数据密度、协作方式、风险等级。
2. 搜索真实可访问的产品、Demo、文档和 GitHub 仓库；记录 URL、访问日期与事实来源。
3. 先检查目标任务是否真的相似，再看 star 数；star 不能替代适配判断。
4. 对 GitHub 候选检查许可证、最近维护、Issue/PR 活跃、依赖风险、Demo 可运行性与安全边界。
5. 把每项借鉴分类：
   - `concept_reference`：只借鉴产品结构或交互思想。
   - `selective_extraction`：原型冻结后评估有限代码或行为适配。
   - `direct_reuse`：只有许可证、维护、技术和安全均成立时才推荐。
6. 明确哪些元素必须移除或重新设计，避免品牌、视觉和用户流程照抄。
7. 把采用/排除结论映射回 Rxx、ACxx 和设计任务。

## 输出合同

| 项目 | 链接与证据 | 可借鉴内容 | 复用级别 | 适配原因 | 必须调整 | 许可证/维护/安全风险 | 结论 |
| --- | --- | --- | --- | --- | --- | --- | --- |

最后只保留 2–5 个有明显价值的候选，并给一个推荐顺序。说明哪些结论是事实、哪些是推断。

## 禁止项

- 不推荐无法验证存在或无法访问的项目。
- 不把截图相似当作代码可复用。
- 不复制来源不明、许可证不明或长期失维护代码。
- 不让外部项目替代本产品的从零设计与用户确认。
- 不在 `FIGMA_PROTOTYPE_APPROVED` 前给出最终依赖或工程选型。

详细检查读取 [reference-evaluation.md](references/reference-evaluation.md)。
