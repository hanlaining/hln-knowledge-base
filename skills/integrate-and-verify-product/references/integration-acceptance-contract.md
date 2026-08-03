# 集成验收合同

## 候选范围

列出精确 Issue、文件/提交、合同版本、migration、资产和环境。一个候选树只有一个集成 Owner。

## 验收层级

1. 启动与 shutdown。
2. unit、contract、integration、frontend。
3. 真实前端 → 真实后端 → 数据读回。
4. 浏览器 E2E 与 Figma 同 viewport 视觉验证。
5. 响应式、a11y、失败、取消、恢复。
6. auth、permission、tenant、输入拒绝、secret 不可见。
7. 从自然入口完成首次成功、高频核心任务和关键失败恢复，记录步骤、时间、犹豫点、理解偏差与结果理解。
8. 全部确认 ACxx 与用户体验。

## 报告

每个 ACxx 记录 target user/scenario、user job、precondition、action、observable result、experience target、failure recovery、Evidence、status。没有真实体验数据时标记待验证；failed 返回原 Owner，deferred 必须由用户知情，不得算 passed。
