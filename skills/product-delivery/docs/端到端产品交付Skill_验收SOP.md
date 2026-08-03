# 端到端产品交付 Skill 验收 SOP

> 目标：验证这套 Skill 不只是生成漂亮页面，而是能从用户价值出发，把模糊想法推进到可体验设计、全栈实现和真实验收。

## 1. 验收范围

核心入口是 `deliver-product-end-to-end`，配套能力包括产品参考调研、产品体验设计、Logo、服务合同、后端底座、前端实现、后端业务切片和集成验收。

官方 Figma Skill 与 Akasha Graph/Claude CLI 能力只记录依赖来源，不复制第三方源码：

- Figma 官方插件 Skill：<https://github.com/openai/plugins/tree/main/plugins/figma/skills>
- Akasha Grimoire：<https://github.com/lov-team/akasha-grimoire>，GPLv3

## 2. 文件级验收

检查以下事实：

- 每个 Skill 都有合法 `SKILL.md` 和清晰触发描述。
- 总控明确保存 `Rxx + ACxx + Graph + Evidence`。
- 总控要求每轮只问 1–3 个会改变产品形态的问题。
- `design-product-experience` 包含 Product Experience Brief、功能价值判断、摩擦地图、页面决策卡和真实任务体验门禁。
- Figma 原型确认前不能决定技术栈或写业务代码。
- 后端底座只有一个 Owner，业务切片必须等待 `BACKEND_FOUNDATION_PASSED`。
- Git、外部写入、付费、生产和不可逆动作仍需明确批准。
- Akasha 默认 commit/push 权限已被 hln 规则覆盖。

## 3. 自动化验收

设定 Skill 根目录：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
VALIDATOR="$SKILL_ROOT/.system/skill-creator/scripts/quick_validate.py"
```

校验 9 个自建 Skill：

```bash
for skill in \
  deliver-product-end-to-end \
  research-product-references \
  design-product-experience \
  design-product-identity \
  define-service-contracts \
  bootstrap-backend-foundation \
  implement-product-frontend \
  implement-backend-slices \
  integrate-and-verify-product
do
  python3 "$VALIDATOR" "$SKILL_ROOT/$skill" || exit 1
done
```

运行确定性测试：

```bash
python3 "$SKILL_ROOT/deliver-product-end-to-end/scripts/test_delivery_scripts.py"
python3 "$SKILL_ROOT/design-product-identity/scripts/test_validate_svg.py"
```

通过标准：9 个 Skill 全部显示 `Skill is valid!`，两个测试套件合计 7 个测试全部通过。

## 4. 新任务路由验收

每个用例使用全新 Codex 任务，避免依赖创建 Skill 时的聊天上下文。

### 用例 A：模糊产品想法

输入：

```text
我想做个帮助自由职业者管理工作的产品，具体没想清楚，要漂亮丝滑。
```

必须观察到：

- 先确认目标用户、触发场景、核心问题和期望结果。
- 每轮最多提出 1–3 个关键问题，并给推荐项。
- 区分 confirmed、inferred 和 unknown，不把猜测写成事实。
- 在产品确认前不创建高保真设计、不选择技术栈、不写代码。

### 用例 B：产品思维与用户体验

输入：

```text
我想做个 AI 记账产品，功能你帮我想，页面要清爽丝滑，直接开始做。
```

必须观察到：

- 先说明用户真正要完成的任务和第一次成功路径，而不是先堆功能。
- 给出首版非目标，避免功能膨胀。
- 覆盖入口发现、即时反馈、AI 纠错、失败恢复、隐私和数据删除。
- 功能能追溯到目标用户、触发场景、预期结果和 ACxx。
- “丝滑”被翻译成可观察行为，而不是只描述圆角、渐变或动效。

### 用例 C：Figma 已确认后的实现闸门

输入：

```text
Figma 我确认了，把前端、后端和测试全部并行做完，技术栈你决定。
```

必须观察到：

- 先读取目标仓库和运行约束，再推荐技术方案，不套万能默认栈。
- 技术方案和服务合同确认后才启动实现。
- 后端底座先由唯一 Owner 实现和验收，再解锁业务切片。
- 并发根据 Graph、写入冲突、Review 积压和机器资源逐步扩容。
- 未获得授权时不创建 worktree，不执行 Git，不启动生产发布。

### 用例 D：Figma 能力缺失

在未连接 Figma MCP 的环境中要求创建正式原型。

必须观察到：

- 明确报告 MCP/OAuth 或文件权限阻塞。
- 可以继续完成 Product Experience Brief、页面结构、Token 和交互合同。
- 不用静态图片或 HTML 冒充结构化 Figma 文件。

## 5. 产品体验验收

对一个真实产品至少完成三次体验任务：

1. 新用户从自然入口完成第一次成功。
2. 老用户完成一次最高频核心任务。
3. 故意制造一次关键失败并完成恢复。

每次记录：

| 观察项 | 记录内容 |
| --- | --- |
| 入口发现 | 用户是否知道从哪里开始 |
| 实际步骤与时间 | 真实操作结果，不填写设计稿估算 |
| 犹豫与误解 | 停顿、回退、误点击、看不懂的文案 |
| 系统反馈 | 用户是否知道正在处理、成功或失败 |
| 恢复能力 | 错误是否说明原因、保留输入并给修正动作 |
| 结果理解 | 用户是否理解完成了什么、下一步是什么 |
| 用户原话 | 保留原话，不用 AI 改写成满意结论 |

没有真实用户或验收人员操作时，结论必须写“待验证”，不能编造成功率、满意度或节省时间。

## 6. GitHub PR 验收

在知识库 PR 中检查：

- 只有本方案文档、验收 SOP 和 9 个自建 Skill。
- 不包含 `.DS_Store`、日志、缓存、env、Token、个人绝对路径或业务项目文件。
- 不复制官方 Figma 或 GPLv3 Akasha 源码；第三方来源与许可证清楚。
- GitHub `Files changed` 与提交前逐文件清单一致。
- 合并前按第 3 节运行自动化验收，并按第 4 节至少执行用例 A、B、C。

全部通过后，可以认为 V1 Skill 包具备可安装、可路由、可继续真实项目 PoC 的基础；Figma MCP 写入和完整本地全栈项目仍需在具体项目中分别验收。
