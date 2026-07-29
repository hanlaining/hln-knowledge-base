# Worked example: lightweight financial desktop Agent

Read this example to demonstrate the derivation method. Adapt the domain and task names; do not silently reuse its decisions for an unrelated product.

## 1. Requirements

| ID | Requirement |
|---|---|
| R01 | Deliver a custom C/S desktop client rather than exposing a CLI terminal. |
| R02 | Reuse Codex CLI as the Agent runtime instead of building a second runtime. |
| R03 | Open a general assistant directly from New Chat. |
| R04 | Provide a separate expert center with optional roles and recommended skills. |
| R05 | Limit the first MVP to Agent + Skill; defer PPT, OCR, billing, and model marketplace. |
| R06 | Hide upstream keys and support the user's reachable network path. |
| R07 | Make financial answers verifiable through bounded sources, citations, and explicit uncertainty. |
| R08 | Read user-authorized local files while preserving sandbox and approval boundaries. |

## 2. Acceptance cases

| ID | Observable product result | Requirements |
|---|---|---|
| AC01 | Launch a real desktop window showing the product's own Agent UI. | R01 |
| AC02 | Click New Chat and talk without choosing a role first. | R03 |
| AC03 | Stream, stop, and continue a real response. | R02, R03 |
| AC04 | Open the expert center and actively select an expert. | R04 |
| AC05 | Process the same material differently through distinct skills. | R04, R05 |
| AC06 | Answer from an authorized folder and cite the file or field source. | R07, R08 |
| AC07 | Deny or request approval for an unauthorized path. | R08 |
| AC08 | Complete a real model response without displaying an upstream key. | R06 |
| AC09 | Exit the client without leaving the embedded runtime process behind. | R01, R02 |

## 3. Derive minimum capabilities

| Acceptance group | Required capability |
|---|---|
| AC01, AC09 | Desktop shell and child-process lifecycle |
| AC02, AC03 | Chat UI, thread/turn bridge, streaming and stop |
| AC04, AC05 | Expert center, role definitions, skill loading |
| AC06, AC07 | Folder authorization, sandbox, citations |
| AC08 | Reachable model gateway and credential boundary |

## 4. Isolate uncertainty first

Create PoCs before full UI work:

- `T01 Runtime PoC`: start the embedded runtime, create a thread, stream a turn, stop, and exit.
- `T02 Gateway PoC`: obtain a real model response through the intended network path without placing the upstream key in the client.

If either PoC fails, stop downstream feature work and report the product impact.

## 5. Product-slice tasks

| Task | Outcome | Requirements | Acceptance |
|---|---|---|---|
| T10 | Real desktop shell | R01 | AC01, AC09 |
| T11 | Runtime lifecycle in the desktop main process | R01, R02 | AC03, AC09 |
| T12 | General chat to thread/turn bridge | R02, R03 | AC02, AC03 |
| T20 | General chat and expert-center entry structure | R03, R04 | AC02, AC04 |
| T21 | First bounded financial skill | R04, R05, R07 | AC05, AC06 |
| T22 | Second bounded financial skill | R04, R05, R07 | AC05, AC06 |
| T23 | Third bounded financial skill | R04, R05, R07 | AC05, AC06 |
| T30 | Authorized folders, sandbox, and citations | R07, R08 | AC06, AC07 |
| T40 | One integrated end-to-end journey | all MVP requirements | AC01-AC09 |
| T41 | Real-window design alignment | R01, R03, R04 | visual cases |
| T42 | Credential, security, dependency, and acceptance audit | all MVP requirements | AC01-AC09 |

## 6. Dependency and waves

```text
T01 runtime PoC + T10 shell -> T11 lifecycle -> T12 chat --+
T02 gateway PoC -------------------------------------------+-> T40 integration -> T41 UI -> T42 audit
T20 expert center -> T21/T22/T23 skills -------------------+
T30 folder boundary and citations -------------------------+
```

Example three-CLI waves:

| Wave | CLI 1 | CLI 2 | CLI 3 | Gate |
|---|---|---|---|---|
| 1 | Runtime PoC | Gateway PoC | read-only baseline audit | Do not expand until both critical paths are proven. |
| 2 | Shell/runtime | Expert center | folder boundary | Keep file scopes separate. |
| 3 | Chat bridge | skills | test review | Produce acceptance evidence per slice. |
| 4 | integration | single UI writer | security audit | Run every confirmed case on one candidate tree. |

## 7. Correction example

User correction:

> New Chat should use the general assistant directly. Roles belong on a separate page.

Recalculate:

- Change `R03` and `R04` if their wording differs.
- Change `AC02` to require direct general chat entry.
- Change `AC04` to require active selection in the expert center.
- Remove any mandatory role-selection route from `T20`.
- Preserve runtime, gateway, and folder-boundary tasks because the correction does not invalidate them.
