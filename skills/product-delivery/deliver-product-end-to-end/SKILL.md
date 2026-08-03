---
name: deliver-product-end-to-end
description: "Orchestrate a complete product delivery from a vague idea through active discovery, product requirements, clean minimal branding and Figma prototype, user approval, technical planning, frontend and backend contracts, resource-aware multi-CLI implementation, integration, testing, and evidence-backed user acceptance. Use when the user asks to build a new product or substantial feature end to end, says the prompt is incomplete, wants design-to-full-stack automation, wants one Codex supervisor coordinating Claude CLI workers, or needs corrections propagated across requirements, design, code, and acceptance."
---

# 端到端产品交付总控

把自己当作产品真相、Graph、审批和 Evidence 的总负责人，不把自己当作包办所有设计与代码的单一 Worker。

## 核心事实

只把两类产物视为产品真相：

1. 用户需求 `Rxx`。
2. 用户确认的验收用例 `ACxx`。

架构、Figma、任务、代码、分支和测试都是中间产物。只有集成后的真实产品通过确认的 `ACxx`，且用户接受最终体验，才能说产品完成。

## 产品与体验原则

先解决用户问题，再决定功能和页面。每个进入 MVP 的能力都必须回答：谁在什么场景触发、原来为什么困难、用户最短怎样得到结果、系统如何反馈、失败后如何恢复、怎样观察价值是否成立。

- 不用功能数量、页面数量或视觉精致度代替产品价值。
- 优先优化首次成功、核心高频任务和高风险失败恢复；低频高级能力使用渐进披露。
- 把用户注意力、输入成本、等待、不确定性、信任和可访问性当作真实设计约束。
- “丝滑”必须落到可观察行为：入口可发现、下一步明确、状态及时、结果可预测、错误可修复、返回不丢失。
- 产品假设未得到用户确认时标记 `inferred`，不能包装成既定事实。

## 选择运行模式

- `DISCUSS`：讨论产品方向，不写文件、不调用外部写入工具。
- `PLAN`：形成 Rxx、ACxx、产品结构、Graph 和闸门，不实现。
- `EXECUTE`：用户明确要求开始实现后，按状态机推进。
- `CORRECT`：用户纠偏时更新所有受影响的需求、验收、设计、Graph 和实现节点。
- `RESUME`：读取项目状态与 Evidence，恢复未完成节点，不从头重做。

用户说“开始实现”“按方案落地”“把整个产品做出来”时进入 `EXECUTE`。授权只覆盖当前阶段和明确范围，不自动包含 Git、外部账号、付费、生产或发布动作。

## 首次启动

1. 读取项目 `AGENTS.md`、`CLAUDE.md` 和适用的 hln 规则；规则冲突时以用户与项目规则为准。
2. 使用 `requirement-acceptance-planner` 保存用户原意，建立或更新 Rxx 与 ACxx；同时明确目标用户、触发场景、核心任务、预期结果和当前摩擦。
3. 每轮只问 1–3 个会改变产品价值、体验、验收、安全或授权的问题；用户不清楚时给一个推荐答案和最多两个备选。
4. 在用户批准写入当前项目后，运行 `scripts/init_delivery_workspace.py --root <project>` 创建轻量状态目录；已存在时不得覆盖。
5. 运行 `scripts/validate_delivery_state.py --root <project>`，修复状态合同错误后再推进。
6. 读取 [stage-contracts.md](references/stage-contracts.md) 和 [artifact-schema.md](references/artifact-schema.md)。

## 阶段状态机

严格按以下顺序推进：

```text
DISCOVERY
→ PRODUCT_CONFIRMED
→ STRUCTURE_APPROVED
→ BRAND_AND_VISUAL_APPROVED
→ FIGMA_PROTOTYPE_APPROVED
→ TECH_PLAN_APPROVED
→ CONTRACT_APPROVED
→ BACKEND_FOUNDATION_PASSED
→ FRONTEND_AND_BACKEND_IMPLEMENTED
→ INTEGRATION_PASSED
→ ACCEPTANCE_PASSED
→ USER_ACCEPTED
```

允许在依赖成立时并行：

- `CONTRACT_APPROVED` 后并行前端工程壳、后端底座和测试脚手架。
- 后端业务切片必须等待 `BACKEND_FOUNDATION_PASSED`。
- 同一个页面、共享入口、全局 Token、schema、migration 和合同同一时刻只能有一个写入 Owner。

禁止越级：

- `PRODUCT_CONFIRMED` 前不创建高保真设计。
- `FIGMA_PROTOTYPE_APPROVED` 前不确定真实项目技术栈、不写业务代码。
- `CONTRACT_APPROVED` 前前后端不能分别猜接口。
- `INTEGRATION_PASSED` 前不能声称全栈完成。
- 用户未明确确认时不得进入下一项不可逆或外部写入阶段。

## 技术选型规则

- 原型冻结后先读取目标仓库、团队约束、运行环境、数据规模、权限风险和维护成本，再提出技术方案。
- 已有项目优先沿用可满足 Rxx/ACxx 的现有栈；绿地项目必须给出与产品规模匹配的推荐及理由，不设置 Vue、React、Java、Node 或数据库的万能默认值。
- 用户说“你自己决定”表示可以给出推荐，不表示可以跳过 `TECH_PLAN_APPROVED`、服务合同、worktree 或 Git 审批。
- Element Plus、Iconfont 或开源项目只有在技术方案获批后才能进入实现合同。

## 专业 Skill 路由

| 结果 | 使用能力 | 解锁条件 |
| --- | --- | --- |
| Rxx、ACxx、MVP 与纠偏 | `requirement-acceptance-planner` | 用户提出产品想法 |
| 竞品与 GitHub 参考 | `research-product-references` | 场景、人群、核心问题已明确 |
| 产品体验、页面、状态、用户旅程 | `design-product-experience` | 产品价值、核心任务与 `PRODUCT_CONFIRMED` 已成立 |
| Logo 与最小品牌系统 | `design-product-identity` | 产品定位与名称状态明确 |
| 从零 Figma 文件 | `figma-create-new-file` + `figma-use` | Figma MCP 已连接且用户批准写入 |
| Figma 页面与组件 | `figma-generate-design`、`figma-generate-library` | 结构、品牌方向获批 |
| 项目 Figma 代码规则 | `figma-create-design-system-rules` | 原型冻结、目标项目已确定 |
| API、数据、错误与权限合同 | `define-service-contracts` | `FIGMA_PROTOTYPE_APPROVED` |
| 后端工程底座 | `bootstrap-backend-foundation` | `TECH_PLAN_APPROVED` + `CONTRACT_APPROVED` |
| Figma 1:1 前端 | `implement-product-frontend` | 原型、技术方案、合同均冻结 |
| 后端业务切片 | `implement-backend-slices` | `BACKEND_FOUNDATION_PASSED` |
| 前后端联调与最终验收 | `integrate-and-verify-product` | 候选实现已汇总 |
| Graph 多 Worker 监工 | `agent-task-supervisor` | 两个以上互不冲突 ready Issue |
| 可见 Claude CLI 实现 | `claude-code-cli-development` + [Claude CLI 本机适配](references/claude-cli-adapter.md) | Issue 合同、worktree 和授权已成立 |
| 代码风险门禁 | `hln-code-risk-gate` | 实现与相关测试完成后立即执行 |

Figma 写入前检查：

- `figma-use`、目标 Figma 能力与 MCP 工具必须真实可用。
- 缺少 MCP、OAuth、文件权限或目标文件时，继续完成产品合同和设计计划，但把 Figma 写入标为 blocked；不得用静态截图冒充结构化 Figma。
- Figma mutation 必须严格串行，不能用多 Worker 并行写同一个 Figma 文件。

## Graph Engineering

读取 [worker-routing.md](references/worker-routing.md)，组织：

```text
Spec → Epic → Issue → Agent Task → Evidence
```

使用三层职责：

```text
主 Codex：Spec / Epic 总监工
→ 独立 Codex Issue 任务：合同、用户决策、Red 审核、完整 diff Review
→ Claude CLI：隔离 worktree 中的唯一写入 Worker
```

每个 Issue 必须包含：

- `Rxx` 与 `ACxx` 映射。
- `depends_on`、`blocks`、`produces`、`validates`。
- 唯一 Owner、绝对 worktree、允许和禁止文件。
- Red/Green/Refactor 或经说明的豁免。
- 状态文件、handoff 文件和终态标记。
- 测试、用户可见 Evidence、风险与回退点。

Worker 的完成标记只表示等待 Review。Issue 任务必须独立检查完整累计 diff、真实调用链、测试和 P0–P3；P0–P2 回到原 Worker 修复。

Akasha 的默认 commit、push 和 worktree 回收授权不适用于 hln/smy。所有 Git 动作继续逐项征求明确批准，不得把本 Skill 当成 Git 授权。

## 无固定上限的资源调度

读取 [resource-aware-concurrency.md](references/resource-aware-concurrency.md)。并发不设置固定数字上限，但只能逐个扩容：

1. 运行 `scripts/collect_resource_snapshot.py --output <snapshot.json>`。
2. 准备只含 ready、已授权且无写入冲突的候选 JSON。
3. 运行 `scripts/plan_worker_concurrency.py --snapshot <snapshot.json> --candidates <ready.json>`。
4. `GREEN` 时按优先级启动返回的一个或多个轻量节点；每轮默认只增加一个 heavy Worker。
5. `YELLOW` 时保持现有 Worker，禁止启动新的 heavy Worker。
6. `RED` 时停止所有新启动，不粗暴杀死正在交付的 Worker。
7. Review 积压、模型限流或前台响应明显变慢时，即使 CPU 允许也暂停扩容。

资源允许不代表文件允许。共享入口、合同、schema、migration、全局样式和同一页面冲突永远优先阻止并发。

## 用户确认规则

必须主动发起确认：

- 产品定位、用户价值、核心任务、体验目标、用户旅程和 MVP。
- Logo 与第一版实际页面效果。
- Figma 完整主流程和异常流程。
- 原型冻结与进入技术方案。
- 技术栈、数据、权限和服务合同。
- 外部账号写入、付费、Git、生产和不可逆动作。

不必打断用户：

- 可逆的间距、基础状态、常见布局和轻量动效。
- 能从已有项目事实直接查明的实现细节。
- 不改变 Rxx、ACxx、安全和产品边界的低风险建议。

## 纠偏与恢复

用户说“不对”“我指的是”“还要”时：

1. 原样记录纠偏。
2. 列出新增、修改、删除和不变的 Rxx。
3. 更新受影响的 ACxx。
4. 重新计算 Graph 依赖与 ready 集合。
5. 标记需要重做、保留或废弃的设计和实现节点。
6. 不允许只改当前页面而留下下游合同、代码和测试继续偏离。

阻塞和异常恢复读取 [failure-recovery.md](references/failure-recovery.md)。

## Evidence 与完成

读取 [evidence-contract.md](references/evidence-contract.md)。至少要求：

- 核心任务的真实完成观察，包括入口发现、步骤/时间、关键犹豫点、失败恢复和结果理解；指标必须来自真实测试，不伪造数据。
- Figma 节点、页面截图、交互原型链接和用户确认。
- 前端真实浏览器截图与 Figma 同 viewport 差异证据。
- 真实前后端请求、成功/失败路径和集成测试。
- 自动化命令、退出码、测试 totals 与时间。
- 安全、权限和拒绝路径 Evidence。
- 未验证、延期和残余风险清单。

只有 `ACCEPTANCE_PASSED` 与 `USER_ACCEPTED` 同时成立才能关闭 Spec。生产发布不属于默认终点，除非用户另行明确授权并启用对应发布 Skill。
