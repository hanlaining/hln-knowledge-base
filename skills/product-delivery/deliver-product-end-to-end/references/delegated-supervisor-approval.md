# Delegated Supervisor Approval

## 目的

让用户在需求聊清后把可逆的中间产品决策委托给独立监工。保留全部阶段门禁，但由与产出 Worker 不同的 Reviewer 根据 Rxx、ACxx 和真实 Evidence 审核；用户只处理保留动作、无法安全推断的高影响歧义和最终结果。

## 启用条件

仅在用户明确表达“采用监工委托审批”“中间不用问我”“我只看最终结果”或同义授权时启用 `DELEGATED_SUPERVISOR`。在项目状态和 Project Launch Brief 中记录：

- `approval_policy: DELEGATED_SUPERVISOR`
- `delegated_scope`：允许监工批准的阶段。
- `reserved_user_actions`：仍需用户亲自批准的动作。
- `approved_by`、`reviewed_artifacts`、`evidence`、`decision_reason`。

未记录明确授权时使用 `INTERACTIVE`，不得推断委托。

## 职责分离

```text
Worker 产出
→ 独立 Reviewer 按阶段合同审核
→ 不通过：带 P0–P3 问题回原 Worker
→ 重新产出与复审
→ 通过：主 Codex 验证 Evidence 后推进状态
```

- Reviewer 不能是该产物的写入 Owner。
- 主 Codex 不能用 Reviewer 的一句“通过”代替检查产物、累计 diff 和 Evidence。
- P0–P2 未清零不得推进；P3 必须记录残余影响。
- 监工可以选择需求内最合理的可逆方案，不能新增用户未要求的产品范围。
- 推断必须标记 `inferred`；一旦影响安全、钱、权限、真实数据、法律、不可逆行为或产品根本方向，立即升级给用户。

## 阶段质量合同

| 状态 | 独立审核重点 |
|---|---|
| `PRODUCT_CONFIRMED` | 用户、场景、问题、价值、最短成功路径、MVP、排除项以及 Rxx→ACxx 可追溯 |
| `STRUCTURE_APPROVED` | 信息架构、核心旅程、首次成功、高频任务、空/加载/错误/权限/恢复状态 |
| `BRAND_AND_VISUAL_APPROVED` | 主题贴合、清新简洁、层级清楚、品牌一致、可访问性与多主题变体 |
| `FIGMA_PROTOTYPE_APPROVED` | 真实结构化 Figma、组件/Token、主流程与异常流程、交互连线、响应式关键尺寸 |
| `TECH_PLAN_APPROVED` | 与产品规模、仓库、团队、数据、权限、维护成本和回退要求匹配 |
| `CONTRACT_APPROVED` | API、模型、校验、错误、认证、权限、幂等、版本与前后端一致性 |
| `BACKEND_FOUNDATION_PASSED` | 真实启动、数据库/迁移、健康检查、日志、认证安全和基础测试 |
| `FRONTEND_AND_BACKEND_IMPLEMENTED` | Figma 1:1、真实状态、接口契约、负向路径、代码审查与相关测试 |
| `INTEGRATION_PASSED` | 真实数据库、服务、浏览器、视觉差异、权限、安全、失败恢复与端到端证据 |
| `ACCEPTANCE_PASSED` | 所有本期 ACxx 有真实成功/失败证据，延期与残余风险已记录 |
| `USER_ACCEPTED` | 只能由用户在查看最终 Figma、真实产品和验收证据后确认 |

“符合标准”必须同时满足本期 Rxx/ACxx、阶段质量合同和用户原始约束，不能只凭视觉精致或测试数量判断。

## 自动返工

1. Reviewer 输出问题等级、证据、受影响的 Rxx/ACxx 和最小修复要求。
2. 主 Codex 把问题送回原 Worker，同一写入范围不更换 Owner。
3. Worker 完成修复和相关回归。
4. Reviewer 检查完整累计产物，不只检查最后一小段修改。
5. 直到 P0–P2 为 0 才允许推进。

默认不向用户发送每次返工消息；仅在用户要求时给里程碑摘要。

## 用户保留动作

即使启用委托审批，也必须由用户亲自处理或明确授权：

- Figma、第三方账号的 OAuth、扫码、文件/团队权限。
- 付费、购买资源、额度或会产生费用的外部调用。
- 生产环境、真实用户数据、数据库写入或迁移。
- 删除、覆盖、公开发布等不可逆或高影响动作。
- Git 分支、worktree、commit、push、PR、merge；用户可以在项目启动时一次性明确授权固定范围，未授权部分仍需询问。
- 正式发布、部署、合并主分支。
- 两个方向都合理但会改变产品根本价值、隐私、安全或商业边界的歧义。

## 用户可见输出

委托模式默认只打断用户三类事情：

1. 用户保留动作。
2. 无法安全推断的高影响阻塞。
3. 最终验收。

最终一次性交付：

- 需求与实际产品的 Rxx→ACxx→Evidence 追踪。
- Logo、品牌和结构化 Figma。
- 可真实运行的前端、后端和数据库。
- 核心任务、异常恢复、安全、无障碍与视觉对齐证据。
- 监工批准记录、自动返工摘要、延期项和残余风险。

用户不接受最终结果时进入 `CORRECT`，把纠偏传播到需求、设计、Figma、代码、合同和测试，重新通过监工链路。
