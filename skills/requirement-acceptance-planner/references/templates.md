# Reusable templates

Use only the sections needed for the current mode. Keep user-confirmed facts separate from assumptions.

## 1. Requirement brief

```markdown
# [Product] MVP requirement brief

## Product outcome

## Target users

## Shortest user journey

## Final user-visible result

## Product sketch

## Requirements

| ID | Status | User requirement | Source or correction |
|---|---|---|---|
| R01 | confirmed |  |  |

## MVP in scope

## Out of scope

## Direct reuse, selective extraction, and concept references

## Unknowns and conflicts
```

## 2. Acceptance case

```markdown
### AC01: [Observable outcome]

- Related requirements: R01
- Status: draft
- Precondition:
- User action:
- Expected observable result:
- Negative or boundary behavior:
- Required evidence:
```

## 3. Traceability matrix

```markdown
| Requirement | Requirement summary | Acceptance cases | Tasks | Final evidence | Status |
|---|---|---|---|---|---|
| R01 |  | AC01 | T01 |  | pending |
```

## 4. Task MD

```markdown
# Txx: [Task outcome]

## Worker role

## Related requirements Rxx

## Related acceptance cases ACxx

## Prerequisites

## Goal

## Allowed files

## Forbidden files

## Implementation boundary

## Required tests

## User-visible evidence

## Completion condition

## Risks and rollback point

## Delivery format
```

## 5. Execution board

```markdown
| Task | Rxx | ACxx | Status | Worker | Worktree | File scope | Evidence | Blocker |
|---|---|---|---|---|---|---|---|---|
| T01 | R01 | AC01 | pending |  |  |  |  |  |
```

Use only these task states unless repository rules specify otherwise:

```text
pending -> running -> review -> fix -> done
                    -> blocked
                    -> deferred
```

## 6. Correction delta

```markdown
## User correction

> [Preserve the user's key wording]

## Requirement delta

- Added:
- Changed:
- Removed:
- Unchanged:

## Acceptance delta

- Added:
- Changed:
- Removed:

## Task and dependency impact

- Add:
- Change:
- Remove:
- Defer:
- Still valid:

## Remaining material decision
```

## 7. Final acceptance report

```markdown
## What the user requested

## Final product shape

## Requirement coverage

## Acceptance results

| ACxx | Result | Real evidence | Remaining gap |
|---|---|---|---|

## Automated verification

## Real-product verification

## Explicitly untested or deferred

## User reproduction steps
```
