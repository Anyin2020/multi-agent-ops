# Departments

Seven channels with fixed scopes. Work goes to the department that owns
it; nothing floats around in a general chat. Each department is a
dedicated channel with its own scope and rules, run under one coordinator
(the personal agent). The human is the final decision-maker for all of
them.

## The seven departments

### Wealth Management

Money. Holdings, watchlists, and the daily market scan. Owns the
holdings record (positions, cost basis, current value) and the daily
close update. Responsible for flagging data anomalies in its own reports
before they reach the human.

### Basic Operations

Infrastructure and operations. Owns server-side deployment, scheduled
jobs, monitoring, and the cloud host. Receives and runs task packs for
anything that lives on a server. Owns the gateway and the task-queue
services.

### Engineering Development

Code. Owns scripts, wrappers, and configuration changes. Everything it
ships passes the three-gate cross-model review (see `review/`). Works to
the standard-library-first rule and never hardcodes secrets or IPs.

### Personal Secretary

The human's day-to-day assistant channel. Owns scheduling, reminders,
message triage, and anything that needs the human's attention. This
channel does not accept external pushes; its rules are held by the
coordinator and applied when work runs there.

### Copywriting

Words. Owns drafts, rewrites, and tone checks for posts, scripts,
captions, and decks. Works from a brief and a source the human approved;
it does not invent facts, clients, or numbers.

### Creative Production

Images, video, and decks. Owns visual assets end to end: brief, draft,
review, final file. It does not decide what to publish — that stays with
the human and Platform Operations.

### Platform Operations

Publishing and distribution. Owns the checklist per platform (format,
size, caption, timing), the posting record, and the follow-up numbers.
It does not write the copy or make the visuals — it receives finished
pieces from Copywriting and Creative Production.

## How work is routed

1. The human (or the coordinator) names the owning department.
2. The coordinator writes a task pack (see `task-pack-protocol/`) and
   dispatches it with a priority (P0/P1/P2) and an ETA to the hour.
3. The department executes, reports at the four points (see
   `ops-manual/rules.md`), and the coordinator accepts or sends back
   against the three acceptance lines.
4. A task that fails twice is escalated automatically: to another
   department, or to the coordinator, and then to the human if needed.

## Scope boundaries

- A department does not take work that belongs to another department's
  scope. If it is unclear who owns it, the coordinator decides.
- No department adds scope to a task on its own. Suggestions go to the
  coordinator first.
- Production work (Copywriting, Creative Production, Platform Operations)
  is one flow; see `production-pipeline.md`.
