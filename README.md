# hln Knowledge Base

hln 的个人公开 AI 协作知识库，用于沉淀可复用的 Skills、SOP、任务拆分方法和验收标准。

> 本仓库包含维护者的原创整理，也可能包含对公开资料、开源项目及 AI 工具输出的借鉴、改写或引用。详细边界、引用要求与 Codex 辅助说明见[《原创、借鉴、引用与 AI 辅助说明》](./原创借鉴与引用说明.md)。

## 核心打法

1. 始终盯住两个事实锚点：用户的需求描述 `Rxx` 和用户确认的验收用例 `ACxx`。
2. Prompt 只负责表达本次任务，Skill 负责沉淀稳定的可复用方法。
3. AI 根据 Skill 名称、描述、正向触发和负面边界自动路由，用户不需要记住所有 Skill 名称。
4. 计划、代码和 PR 都是中间产物；真实产品通过验收用例才算完成。

## 知识库目录

### Skills

- [`requirement-acceptance-planner`](skills/requirement-acceptance-planner/SKILL.md)：将模糊、口语化或反复纠偏的产品想法，转换为 MVP 产品形态、Rxx 需求、ACxx 验收用例、Txx 任务和多 CLI 执行计划。

### SOP

- [从模糊需求到多 CLI 执行：Agent 产品规划与交付 SOP](sop/从模糊需求到多CLI执行_Agent产品规划SOP.md)
  - 需求与验收双锚点。
  - 从 Prompt 驱动转向 Skill 驱动。
  - Skill Tree、正负触发边界、召回与重排。
  - 总体计划、任务 MD、最多三个 CLI 和真实产品验收。

## 安装 Skill

将完整 Skill 目录复制到 Codex Skills 目录：

```text
~/.codex/skills/requirement-acceptance-planner/
```

在新任务中调用：

```text
使用 $requirement-acceptance-planner 把我的产品想法整理成需求 Rxx、
验收用例 ACxx 和可执行的任务计划。
```

## 内容原则

- 只提交可公开、可复用的知识。
- 不提交 Key、Token、Cookie、密码、个人绝对路径或内部生产配置。
- 方法论必须附带适用边界、验收方式和可复现模板。
- 用户的需求和验收用例始终高于 AI 自动选择的执行方法。

## 致谢

关于 Skill 描述区分度、分层路由、负面边界以及召回/重排的思路，结合了 yangyida 的《Skill过多怎么怎么提高命中率》中的观点。

如发现遗漏署名、引用不当或权利冲突，请通过本仓库 GitHub Issues 联系维护者；核实后将及时补充出处、修订或移除相关内容。
