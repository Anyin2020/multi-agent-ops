# ADR-002: Task Packs as the Handoff Contract

- Date: 2026-11-01
- Status: Accepted

## Context

Verbal instructions between the coordinator and the executor kept
drifting: the executor improvised, steps were skipped, and "done"
meant different things to each side. Verification was impossible
because there was nothing to verify against.

## Decision

Planning and execution are separated by a written contract — the task
pack. It lists the exact commands (verified beforehand, written in
full), the constraints, the forbidden shortcuts, and hidden checks used
for verification. The executor follows it literally. The coordinator
verifies the result against it.

## Consequences

- Good: verification is independent of execution, because the checks
  are written before the work starts and the executor cannot see them.
- Good: a task pack is reviewable, versioned, and reusable as an
  example for the next similar task.
- Bad: writing a good pack takes time up front. A vague pack produces
  vague execution — the quality of the pack is the quality of the work.
- A step the executor cannot do is reported as uncompleted with the
  reason. The pack is never marked complete with silent gaps.
