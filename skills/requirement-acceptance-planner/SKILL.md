---
name: requirement-acceptance-planner
description: "Turn vague, conversational, or repeatedly corrected product ideas into a user-confirmed MVP, observable acceptance cases, traceable task breakdown, and optional multi-CLI execution plan using two anchors: the user's requirement descriptions and the user's acceptance tests. Use when Codex must clarify what a product should become, show its final user-facing shape, define MVP scope, convert requirements into Given/When/Then acceptance cases, explain how tasks were derived, update plans after user corrections, write task MD files, or coordinate at most three coding CLIs without losing product intent."
---

# Requirement Acceptance Planner

## Core rule

Treat only two artifacts as product truth:

1. The user's requirement descriptions, indexed as `Rxx`.
2. The user-confirmed acceptance cases, indexed as `ACxx`.

Treat architecture, plans, task MDs, code, commits, and PRs as intermediate artifacts. Do not call the product complete until the real product passes the confirmed `ACxx` cases.

Keep this loop active:

```text
user requirement
-> restated product shape
-> acceptance cases
-> task derivation
-> implementation and integration
-> run acceptance cases
-> user finds deviation
-> update Rxx and ACxx
-> recalculate affected tasks
```

Reject or defer work that cannot point to at least one `Rxx` and one `ACxx`.

## Choose the operating mode

Infer the narrowest mode from the user's request:

- **Discuss**: compare product choices and preserve unresolved decisions; do not edit files.
- **Plan**: produce the product brief, acceptance cases, traceability, and task map; do not implement.
- **Package**: write the approved plan and task MD files.
- **Execute**: implement only when explicitly requested, while preserving repository and approval rules.
- **Correct**: process the user's latest correction as a delta and update every affected artifact.

Do not treat a request for a plan, SOP, or prompt as authorization to change business code, Git state, external systems, or deployments.

## Step 1: Preserve the user's requirements

Record the user's meaning before translating it into technology.

Classify every statement as:

- `confirmed`: explicitly stated or confirmed by the user.
- `inferred`: useful working assumption not yet confirmed.
- `unknown`: information that is genuinely missing.
- `conflict`: two statements that imply different product shapes.

Assign IDs only to product-relevant requirements:

```text
R01 [confirmed] The user sees a desktop client, not a CLI terminal.
R02 [confirmed] A new chat opens the general assistant without forcing a role choice.
R03 [inferred] The first release targets macOS only.
```

Quote important corrections in the user's own words. Never silently rewrite a correction into a nearby but different technical choice.

Ask a question only when the answer materially changes the product shape, acceptance result, security boundary, or authorized action. Otherwise, produce a first-pass interpretation and mark the assumption.

## Step 2: Show the “1” and the “100”

Lead with the outcome, not the internal black box.

Always describe:

1. What is being built.
2. What the user sees.
3. The shortest user journey.
4. What the user receives at the end.
5. What is explicitly outside the MVP.

For UI or multi-step products, include the smallest useful ASCII sketch or flow. Keep services, adapters, protocols, and class names out of this product-facing section unless they materially affect the product choice.

Separate reuse decisions into:

- `direct reuse`: use an existing runtime or component as-is.
- `selective extraction`: copy or adapt bounded code or behavior.
- `concept reference`: borrow product structure or interaction ideas only.

For each external reference, state what is borrowed, why it helps, which reuse class applies, and what must be removed or adjusted.

## Step 3: Convert product shape into acceptance cases

Write acceptance cases before large-scale task decomposition.

Do not reduce “testing” to unit tests. Include observable product-shape checks such as:

- real application launch and shutdown;
- shortest user journey;
- page layout and visible states;
- role or skill selection behavior;
- real input and output shape;
- source citations and uncertainty behavior;
- permission prompts and negative-path denial;
- key and credential visibility;
- network boundary;
- real-window screenshot or recording evidence.

Write every case with:

```text
ACxx Title
Related requirements: Rxx
Precondition:
Action:
Expected observable result:
Required evidence:
Status: draft | confirmed | changed | passed | failed | deferred
```

Prefer user-observable language. Replace “API returns successfully” with the screen, behavior, output, or audit evidence the user can verify.

Ask the user to correct the cases when they do not match the intended product shape. Treat confirmed cases as the definition of done.

## Step 4: Build bidirectional traceability

Create a matrix linking requirements, acceptance cases, tasks, and evidence:

| Requirement | Requirement summary | Acceptance cases | Tasks | Final evidence |
|---|---|---|---|---|
| R01 |  | AC01 | T01 |  |

Check both directions:

- Every confirmed `Rxx` must map to at least one `ACxx` or be explicitly deferred.
- Every `ACxx` must map to a confirmed `Rxx`.
- Every implementation `Txx` must map to both `Rxx` and `ACxx`.
- Every passed `ACxx` must name real evidence.

Do not hide unmapped requirements or untested tasks.

## Step 5: Derive tasks instead of inventing them

Use this derivation chain:

```text
Rxx
-> ACxx
-> minimum capabilities needed to pass ACxx
-> uncertainty-removing PoC
-> independently verifiable product slice Txx
-> dependencies and file boundaries
-> execution wave
-> final integrated ACxx run
```

Apply these rules:

1. Group acceptance cases by observable product outcome.
2. List only the minimum capabilities necessary to pass each group.
3. Isolate the largest technical uncertainties into early PoCs.
4. Split one task around one independently verifiable outcome.
5. Avoid tasks named only after vague technical layers.
6. Give each task explicit allowed and forbidden file scopes when a repository exists.
7. Prevent two workers from editing the same entry point, global style, contract, or config concurrently.
8. Put end-to-end integration and final acceptance in dedicated tasks.

Read [templates.md](references/templates.md) when producing a requirement brief, acceptance suite, task MD, status board, correction report, or final report.

Read [worked-example.md](references/worked-example.md) when the user asks how the decomposition works, requests an example, or presents an Agent/client/role/skill product similar to the Finance Agent case.

## Step 6: Plan dependencies and multi-CLI execution

Draw the dependency graph before assigning workers.

When the user requests multiple coding CLIs:

- Default to at most three concurrent CLIs unless the user sets a lower limit.
- Assign work in waves, not all at once.
- Start with read-only discovery or PoCs when the baseline is uncertain.
- Keep at most one UI-writing worker for a shared page or design system.
- Use other slots for isolated runtime, skill, test, or read-only review work.
- Do not start a task whose dependencies or acceptance cases are not ready.
- Make the supervising chat review diffs, run tests, and collect evidence; never accept a worker's verbal completion alone.

For every task, include:

- task ID and outcome;
- related `Rxx` and `ACxx`;
- prerequisites;
- allowed and forbidden files;
- implementation boundary;
- required tests and user-visible evidence;
- completion condition;
- risks and rollback point;
- worker and wave assignment when applicable.

## Step 7: Process user corrections as controlled deltas

When the user says “not this,” “I mean,” “only MVP,” or otherwise redirects the product:

1. Restate the correction plainly.
2. List changed, added, removed, and unchanged `Rxx` items.
3. Update affected `ACxx` cases.
4. Identify tasks to add, change, remove, or defer.
5. Recalculate dependencies and execution waves.
6. State what prior implementation or plan remains valid.
7. Ask for confirmation only if a remaining ambiguity changes the product or authorization boundary.

Never patch only the current screen or task while leaving the requirement, acceptance, and downstream plans inconsistent.

## Step 8: Gate completion with real evidence

Distinguish these states:

1. Code exists on a branch.
2. A PR exists.
3. Changes are integrated into one candidate tree.
4. Automated checks pass.
5. The real product passes confirmed acceptance cases.
6. The user accepts the product shape.

Only states 5 and 6 justify product completion language.

Require evidence appropriate to the case:

- exact command and result for automated checks;
- real API/model response for integration behavior;
- real application window screenshots for UI;
- permission denial and audit output for security boundaries;
- redacted presence/absence checks for credentials;
- explicit deferred list for anything not tested.

Do not use AI-generated mockups, worker claims, PR counts, or isolated branch tests as substitutes for final integrated acceptance.

## Default response structure

For a new product request, respond in this order:

1. `我理解你要做什么` — concise product outcome.
2. `用户最终看到什么` — journey and sketch.
3. `需求清单 Rxx` — confirmed, inferred, unknown, conflicts.
4. `验收用例 ACxx` — observable product-shape tests.
5. `MVP 做与不做`.
6. `复用与借鉴`.
7. `从用例倒推的任务 Txx`.
8. `依赖与最多三 CLI 波次` when requested.
9. `需要用户纠偏的点` — only material decisions.

For a correction, lead with the requirement, acceptance, and task deltas instead of repeating the entire plan.

## Quality gate

Before delivery, verify:

- The user's words remain distinguishable from agent assumptions.
- The product's final shape is understandable without reading the technical middle.
- Acceptance cases test the real product shape, not only internal APIs.
- Requirement and acceptance mappings are bidirectional.
- Every task is traceable and independently verifiable.
- PoCs precede expensive implementation when uncertainty is high.
- Multi-CLI work respects dependencies and file ownership.
- Corrections update all affected artifacts.
- “Done” is backed by integrated real-product evidence.
