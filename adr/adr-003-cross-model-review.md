# ADR-003: Cross-Model Review

- Date: 2026-11-02
- Status: Accepted

## Context

AI-written code has the same blind spots as the model that wrote it.
A single model reviewing its own work mostly re-approves it.

## Decision

Every code or configuration change passes three gates: author
self-test, review by a different model, coordinator acceptance. The
reviewer is always a different model from the author — a model never
reviews its own work. The reviewer advises only and never edits code.

## Consequences

- Good: different models have different blind spots, so the cross-check
  catches issues a single model misses.
- Good: keeping the reviewer out of the code keeps responsibility
  clear — the author owns the fix.
- Bad: every change costs an extra review round. Two failed rounds
  escalate to the coordinator for arbitration.
- Review findings are treated as claims to verify, not conclusions.
  Every claim is checked item by item before acceptance.
