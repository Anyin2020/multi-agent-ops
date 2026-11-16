# ADR-001: Departments, Not Chats

- Date: 2026-11-01
- Status: Accepted

## Context

One person was using several AI tools — a planner, a local executor, a
cloud ops agent — with context copied between them by hand. There was no
shared memory, no accountability, and no reliable way to check whether
work was actually done.

## Decision

Organize the agents the way a small team is organized: fixed-scope
departments, each a dedicated channel with its own scope and rules, run
under one coordinator. Work goes to the department that owns it; nothing
floats around in a general chat.

## Consequences

- Good: responsibility is visible. A task has an owner, a priority, and
  an ETA. Missed ETAs and failed tasks can be traced to a department.
- Good: rules can be scoped per department instead of one global prompt.
- Bad: more surface to maintain — each department needs its scope kept
  current, and routing mistakes send work to the wrong place.
- The coordinator arbitrates when ownership is unclear.
