# 阶段合同

## 状态与进入条件

| 状态 | 必需输入 | 必需 Evidence | 下一步需用户确认 |
| --- | --- | --- | --- |
| `DISCOVERY` | 原始想法 | 原话记录、未知项 | 产品解释是否正确 |
| `PRODUCT_CONFIRMED` | Rxx、MVP、非目标、Product Experience Brief | 用户价值、核心任务、体验目标、用户确认、ACxx 草案 | 页面结构与旅程 |
| `STRUCTURE_APPROVED` | 页面地图、旅程、摩擦地图、状态矩阵 | 功能价值说明、信息优先级、草图/流程确认 | 品牌与视觉方向 |
| `BRAND_AND_VISUAL_APPROVED` | Logo、Token、核心页面 | Logo 与页面同框截图 | 完整 Figma 原型 |
| `FIGMA_PROTOTYPE_APPROVED` | 结构化 Figma、交互脚本 | 节点、截图、点击结果 | 是否进入技术方案 |
| `TECH_PLAN_APPROVED` | 项目现状、选型、复用边界 | 用户确认、风险 | 前后端合同 |
| `CONTRACT_APPROVED` | API/数据/错误/权限合同 | 合同版本、测试计划 | 是否启动实现 |
| `BACKEND_FOUNDATION_PASSED` | 底座合同与实现 | 启动、health、测试、Review | 解锁业务切片 |
| `FRONTEND_AND_BACKEND_IMPLEMENTED` | 已 Review 的 Issue | diff、测试、视觉/接口证据 | 集成候选范围 |
| `INTEGRATION_PASSED` | 单一候选树 | 真实前后端和 E2E 证据 | 最终 ACxx |
| `ACCEPTANCE_PASSED` | 全部确认 ACxx | Evidence 索引、核心任务完成观察、失败恢复结果 | 用户最终体验 |
| `USER_ACCEPTED` | 用户明确接受 | 接受记录、延期项 | 无；Spec 可关闭 |

## 变更规则

- 阶段不得倒序伪装完成；纠偏可把状态退回最早受影响的闸门。
- 退回时保留仍有效 Evidence，标记过期证据，不删除历史。
- 外部写入、Git、付费和生产授权与阶段批准分开记录。
- `blocked` 必须记录阻塞事实、解除条件和仍可并行的节点。
