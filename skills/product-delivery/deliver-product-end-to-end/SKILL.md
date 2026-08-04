---
name: deliver-product-end-to-end
description: "Orchestrate a complete product delivery from a vague idea through active discovery, product requirements, clean minimal branding and Figma prototype, approval, technical planning, frontend and backend contracts, resource-aware multi-CLI implementation, integration, testing, and evidence-backed user acceptance. Use when the user asks to build a new product or substantial feature end to end, wants to chat casually until choosing a project and then launch it in a fresh Codex task, wants independent supervisors to approve and automatically return intermediate work while the user only provides requirements and reviews the final result, says the prompt is incomplete, wants design-to-full-stack automation, wants one Codex supervisor coordinating Claude CLI workers, or needs corrections propagated across requirements, design, code, and acceptance."
---

# 端到端产品交付总控

把自己当作产品真相、Graph、审批和 Evidence 的总负责人，不把自己当作包办所有设计与代码的单一 Worker。

## 核心事实

只把两类产物视为产品真相：

1. 用户原始或澄清确认的需求 `Rxx`。
2. 可追溯到 Rxx、可观察且经当前审批策略确认的验收用例 `ACxx`。

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
- `HANDOFF`：冻结已确认的项目事实，把精简交接包传给新 Codex 任务；当前任务不执行产品。
- `EXECUTE`：用户明确要求开始实现后，按状态机推进。
- `CORRECT`：用户纠偏时更新所有受影响的需求、验收、设计、Graph 和实现节点。
- `RESUME`：读取项目状态与 Evidence，恢复未完成节点，不从头重做。

用户要求在当前任务直接实现时进入 `EXECUTE`。用户说“现在去把这个项目落地”“新开一个 Chat 开始执行”或同义表达时进入 `HANDOFF`，不得在当前讨论任务偷偷执行。授权只覆盖创建执行任务和当前阶段的明确范围，不自动包含 Git、外部账号、付费、生产或发布动作。

## 选择审批策略

运行模式与审批策略相互独立：

- `INTERACTIVE`：关键中间阶段由用户逐项确认。
- `DELEGATED_SUPERVISOR`：用户明确委托后，由独立 Reviewer 审核可逆中间阶段，主 Codex 根据 Evidence 自动推进；用户只处理保留动作、高影响阻塞和最终验收。

用户说“采用监工委托审批”“中间不用问我”“需求聊完直接做，我只看结果”或同义表达时，读取 [delegated-supervisor-approval.md](references/delegated-supervisor-approval.md)，并把审批策略、委托范围和用户保留动作写入项目状态与 Project Launch Brief。没有明确授权时默认 `INTERACTIVE`，不得自行启用委托。

`DELEGATED_SUPERVISOR` 不表示取消门禁。每个阶段必须由非写入 Owner 的独立 Reviewer 检查 Rxx/ACxx、完整产物和真实 Evidence；P0–P2 自动回原 Worker 返工直至清零。所有通过记录 `approved_by`、`reviewed_artifacts`、`evidence` 和 `decision_reason`。

## 双 Chat 启动协议

把产品孵化和项目执行分成两个任务：

```text
孵化任务（DISCUSS）
→ 用户明确要求新开任务落地
→ 结构化交接（HANDOFF）
→ 执行任务（EXECUTE）
```

进入 `HANDOFF` 时读取 [discovery-to-execution-handoff.md](references/discovery-to-execution-handoff.md)，并严格执行：

1. 只打包用户已确认事实、明确标记的推断、原始约束、Rxx/ACxx、MVP、排除项、体验方向、审批状态和待决问题；不要复制整段聊天、Cookie、Token、账号或无关历史。
2. 已确认执行目标时直接使用；绿地项目使用独立 projectless 任务和安全目录名，已有仓库先列出 Codex 项目并确认目标。缺少会造成写错目录的执行目标时只补问这一个阻塞问题。
3. 使用 Codex App 的新建任务能力创建全新执行任务，不 fork 孵化任务。新任务 Prompt 必须显式调用 `$deliver-product-end-to-end`、进入 `EXECUTE`、携带审批策略、嵌入完整交接包并要求不重复询问已确认内容。
4. 新任务从交接包证据支持的最远审批状态继续；没有明确用户确认时不得自行提升状态。执行任务仍必须遵守 Figma、技术方案、Git、外部账号、付费、生产和发布审批门。
5. 创建成功后在孵化任务返回新任务入口、交接摘要和未授权边界；只有用户明确要求打开时才导航到新任务。孵化任务继续保持 `DISCUSS`。
6. 创建失败或能力不可用时输出可复制的执行 Prompt 和完整交接包并停止；不得退回当前孵化任务继续实现。

一个项目只能有一个主执行任务。再次收到落地指令时，优先找到并继续已有执行任务；只有用户明确要求重开时才创建第二个。

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
- 用户或获明确委托的独立监工未按当前审批策略确认时不得推进；不可逆、外部写入和用户保留动作只能由用户授权。

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

委托审批时，把产品、体验、品牌、Figma、架构、合同、实现、集成和验收分别建立 Reviewer 节点。产出 Worker 与对应 Reviewer 不得是同一任务；主 Codex 只有在 Reviewer 问题清零并亲自核对 Evidence 后才能改变阶段状态。

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

`INTERACTIVE` 必须主动请求用户确认：产品定位与 MVP、体验与旅程、Logo 与第一版页面、Figma 主/异常流程、原型冻结、技术栈、数据/权限和服务合同。

`DELEGATED_SUPERVISOR` 不把上述可逆中间阶段发给用户审批；按委托审批合同独立审核、自动返工并记录证据。只有以下情况打断用户：

- Figma 或第三方账号的 OAuth、扫码和文件/团队权限。
- 付费、生产环境、真实用户数据、删除覆盖和其他不可逆动作。
- 未在启动时明确预授权的 Git、PR、merge、发布和部署。
- 两个方向都合理但会改变产品根本价值、隐私、安全或商业边界的歧义。
- 最终 `USER_ACCEPTED`。

不改变 Rxx、ACxx、安全和产品边界的可逆细节由当前审批策略处理。用户若已对固定项目范围一次性授权 branch、worktree、commit、push 和 PR，应记录授权并减少重复询问；merge、生产和发布未被明确包含时仍需单独批准。

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
- Figma 节点、页面截图、交互原型链接，以及按当前审批策略记录的批准主体和证据。
- 前端真实浏览器截图与 Figma 同 viewport 差异证据。
- 真实前后端请求、成功/失败路径和集成测试。
- 自动化命令、退出码、测试 totals 与时间。
- 安全、权限和拒绝路径 Evidence。
- 未验证、延期和残余风险清单。

只有 `ACCEPTANCE_PASSED` 与 `USER_ACCEPTED` 同时成立才能关闭 Spec。生产发布不属于默认终点，除非用户另行明确授权并启用对应发布 Skill。
