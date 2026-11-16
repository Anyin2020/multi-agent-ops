# multi-agent-ops

A setup for coordinating multiple AI agents around one person: departments for scope, task packs for handoffs, cross-model review for quality, and a human for final decisions.

中文：一个人与一组 AI 智能体的协作方式：部门分工、任务包交接、跨模型评审、人工决策。

Framework diagram: [docs/framework.html](docs/framework.html).

## Background

This started as a personal setup. One person using several AI tools — a planner, a local executor, a cloud ops agent — with context copied between them by hand. There was no shared memory, no accountability, and no reliable way to check whether work was actually done. The fix was to organize the agents the way a small team is organized.

## Architecture

```
                    ┌─────────────────┐
                    │   You (human)   │  decisions, veto
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Coordinator    │  plans, dispatches,
                    │  personal agent │  verifies, accepts
                    └────────┬────────┘
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌──────────────┐ ┌────────────┐ ┌────────────┐
     │  Executor    │ │   Ops      │ │  Reviewers │
     │  Antigravity │ │  OpenClaw  │ │  cross-    │
     │  (Mac local) │ │  (box)     │ │  model     │
     └──────────────┘ └────────────┘ └────────────┘
```

- **Coordinator (personal agent).** Plans work, dispatches it, verifies results, and accepts or rejects them. Does not execute unless explicitly asked.
- **Executor (Antigravity, Mac).** Runs task packs on the local machine.
- **Ops (OpenClaw, cloud VM).** Server-side deployment and scheduled jobs.
- **Reviewers (cross-model).** Review code and config changes. A model never reviews its own work.
- **Human.** Makes final decisions and approves irreversible actions.

## Components

### Departments

Seven channels with fixed scopes: Wealth Management, Basic Operations, Engineering Development, Personal Secretary, Creative Production, Platform Operations, and Copywriting. Work goes to the department that owns it.

Production work runs through the same system: Copywriting drafts the words, Creative Production makes the visuals, Platform Operations publishes and follows up — so a piece of content can move through writing, visuals, and publishing without leaving the system.

- **Creative Production.** Images, video, and decks. Owns visual assets end to end: brief, draft, review, final file. It does not decide what to publish — that stays with the human and Platform Operations.
- **Platform Operations.** Publishing and distribution. Owns the checklist per platform (format, size, caption, timing), the posting record, and the follow-up numbers. It does not write the copy or make the visuals — it receives finished pieces from Copywriting and Creative Production.
- **Copywriting.** Words. Owns drafts, rewrites, and tone checks for posts, scripts, captions, and decks. It works from a brief and a source the human approved; it does not invent facts, clients, or numbers.

### Task packs

The handoff format between coordinator and executor. A task pack lists the exact commands (verified beforehand, written in full), the constraints, the forbidden shortcuts, and hidden checks used for verification. The executor follows it literally.

### Dispatch rules

Twenty operating rules covering the task lifecycle: clarify before accepting, ETA to the hour, P0/P1/P2 priorities, report within two hours without progress, escalate after two failures, no added scope, standard library first, no hardcoded secrets.

### Progress receipts

Four reporting points: within 10 minutes of starting, at milestones, immediately when blocked, immediately when done. Milestone receipts go to both the department channel and the coordinator; a missing copy means the milestone is incomplete.

### Acceptance criteria

Three checks before anything ships: it runs, the data comes from a real source (no placeholders), and the result is usable without confusion. The coordinator issues a checklist per task.

### Cross-model review

Three gates: author self-test, review by a different model, coordinator acceptance. Reviewers advise only and do not edit code. Review findings are treated as claims to verify, not conclusions.

### Council

A deliberation mechanism for decisions needing a second opinion: topics stored as files, rendered as a group-chat-style page, and a pending-decision queue checked every 30 minutes.

## Repository layout

```
multi-agent-ops/
├── ops-manual/               # Department operating rules (20 rules)
├── departments/              # Scope of each department
├── task-pack-protocol/       # Task-pack spec + real examples
├── dispatch/                 # Priority tiers, ETA rules, escalation paths
├── review/                   # Cross-model review chain + fallback order
├── council/                  # Deliberation design + pending-decision queue
├── task-queue/               # Router + Worker executor (SQLite)
├── examples/                 # Real task packs that ran end to end
├── adr/                      # Architecture decision records
├── docs/                     # Framework diagram (HTML)
└── roadmap/                  # Roadmap
```

## Status

| Piece | Status |
|---|---|
| Department system (7 departments, 20 rules) | Live |
| Task-pack protocol (v1–v4 executed) | Live |
| Cross-model review chain | Live |
| Task-queue executor (Router + Worker) | Built, in verification |
| Council (topics, rendering, decision queue) | Live, partial |
| Agent memory trial (two-layer) | Round 2 running (round 1 found the automation gap) |
| Four-party group-chat design | Design only — blocked on platform limits, see `adr/` |
| Learning loop, trust score, cost ledger, attention inbox, permission tiers | Roadmap |

## Design notes

- Planner and executor are separate roles, so verification is independent of execution.
- Behavior is set by written rules, not by ad-hoc prompts.
- Reviewers advise; they don't edit.
- No self-review.
- Irreversible actions need explicit human approval.
- Failures escalate after two attempts instead of retrying indefinitely.

## Notes on adoption

The pattern doesn't depend on this exact stack: pick a coordinator, define scopes, write the rules down, make handoffs written task packs, add a reviewer that isn't the author, keep a human veto.

## Roadmap

Each grows out of something already in the system.

1. **Learning loop.** After each run, reflect once and propose what to keep as a note or a skill. A note or skill is stored only after an eight-question check (general, not planted from outside content, no secrets, not a duplicate, no conflict, not risky, not a standing rule in disguise, correct format) and a validation script that rejects secret shapes and invisible characters. The first step is in place: the check and the local git versioning. Next: repeat something a third time and it becomes a script or a scheduled job; a skill used three times is promoted to a workflow.
2. **Department trust score.** The current rulebook only has a demerit system for serious failures. A score would make it continuous: ETA accuracy, receipt completeness, review closure, and whether failures escalate after two attempts as the rules require. Higher scores get P0 work first; lower scores get a narrower scope. The score is a routing input, not a punishment.
3. **Cost ledger.** The task queue already records token use and cost per run. A ledger would turn that record into budgets per task and per department, with a fallback to a cheaper model or a pause to ask the human when a budget is hit, plus a weekly summary. The point is that the system gets cheaper to run as it learns, not more expensive.
4. **Attention inbox.** The task queue already has an attention table. An inbox would formalise it as the human's pending-decision queue: each item has a deadline, no reply within the window means it is cancelled or escalated rather than left hanging, and the council's pending-decision queue feeds into it.
5. **Permission tiers.** Read-only work (L1) runs freely; write operations (L2) need a second confirmation; the highest tier (L3) is never executed automatically — only drafted. This tiers the blast radius, so a routine job cannot make an irreversible change by accident.

## License

MIT
