# Cross-Model Review

Every code or configuration change passes three quality gates before it
ships. The point is simple: different models have different blind spots,
and a cross-check catches what a single model misses.

## The three gates

| Gate | Who | What |
|------|-----|------|
| 1. Author self-test | The department that wrote the code | Runs it, plus edge-case tests (timeout, empty data, insufficient permissions) |
| 2. Review by a different model | The same department, with another model | Reviews only: gives opinions, does not change code. After fixes, one more review round. |
| 3. Coordinator acceptance | The personal agent (coordinator) | Read-only verification against the task pack's acceptance standard. |

**The rule that matters most:** a model never reviews its own work.
The reviewer is always a different model from the author. If the author
model and the reviewer model are the same, the review does not count.

## Review checklist (checked every time)

1. **Logic correct**: does the code do what the requirement says?
2. **Edge cases**: empty input, null, timeout, oversized input — how are
   they handled?
3. **Secret safety**: any hardcoded token, key, or password?
4. **Error handling**: does a failure report an error, or go silent?
   Silent failures are sent back.
5. **Resource release**: files, connections, locks — released after use?

## Review format

The reviewer outputs:

```
<filename>
- Passing items: ...
- Issues:
  1. <description> (<file>:<line>)
  2. ...
- Suggestions: ...
```

The author fixes the issues one by one, marks each "fixed", and sends
it back to the reviewer for one confirmation round. If it fails two
rounds, it is escalated to the coordinator for arbitration.

## Scope

- Applies to: all scripts, wrappers, and configuration changes from
  Engineering Development; all deployment scripts, configuration
  changes, and scheduled-job changes from Basic Operations.
- Does not apply to: pure documentation, pure configuration with no
  logic.

## Red lines

- The reviewer never edits code directly — only gives opinions. This
  keeps responsibility clear.
- A secret problem is a veto: it must be fixed before anything passes.
- At acceptance, the coordinator spot-checks whether the reviewer's
  issues were actually closed. Unclosed issues mean the change is sent
  back.
- Review findings are treated as claims to verify, not conclusions.
  Every claim is checked item by item before acceptance.
