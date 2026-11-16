# Dispatch

Dispatch is how work leaves the coordinator and reaches a department:
a priority, an ETA to the hour, and a written task pack. This document
is the dispatch side of the 20 operating rules (`ops-manual/rules.md`).

## Priority tiers

| Tier | Meaning | Handling |
|------|---------|----------|
| P0 | Fault | Jumps the queue. Worked on immediately. |
| P1 | Main line | Worked on in order. |
| P2 | Improvement | Done when idle. |

Every dispatched task carries its tier. A task without a tier is not
accepted for dispatch.

## ETA rules

- The ETA is exact to the hour, e.g. "Nov 3, 15:00". Vague ETAs
  ("afternoon", "tonight") are not accepted.
- The coordinator may correct an unreasonable ETA based on the size of
  the work.
- If there is no substantial progress 2 hours after accepting a task,
  the department reports the reason and a new ETA on its own initiative.
  It does not wait to be asked.
- Three missed ETAs on serious work is written up as a failure record (see below).

## Progress receipts

Four reporting points, from the task-progress sync rule:

1. **Start** — within 10 minutes of receiving the task: "received,
   starting".
2. **Milestone** — when a key step is done. Sent twice: once in the
   department channel, once to the coordinator. A milestone with a
   missing copy counts as incomplete.
3. **Blocked** — immediately when stuck, with where it is stuck, what
   was tried, and what is needed.
4. **Done** — immediately on completion, with the acceptance points.

Format: the message starts with `[progress]`, `[done]`, or `[blocked]`
followed by one sentence on the state; details are attached separately.
No receipt means no work, and problems are traced to the receipt first.

## Escalation path

```
Agent fails → retry once with the same agent
Still fails → escalate to another department or the coordinator
Coordinator cannot fix it → mark it for a human decision
```

- A task that fails twice is escalated automatically. No approval from
  the human is needed for the escalation itself.
- Escalation is not a failure to hide: the escalation message carries
  what was tried, where it got stuck, and what alternatives remain.

## Failure record

- **Failure record.** A serious failure (for example, 11 hours with
  zero output, or three missed ETAs) is written up once: what was tried,
  where it got stuck, and what changes. The write-up is kept as a
  reference so the next attempt does not repeat it.
- **Acceptance.** Nothing ships until it passes the three lines: it
  runs, the data is real, the experience is smooth. The coordinator
  issues an acceptance checklist per task; the human spot-checks it.
