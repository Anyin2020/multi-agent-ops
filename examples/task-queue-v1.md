# Example Task Pack v1: Task Queue Minimum Viable Version (Scheduler + Ledger)

> Ran end to end. Target: deploy a SQLite ledger + a Router scheduling
> prototype + a minimal Worker on the host, and verify that "automatic
> task scheduling + state written to the database" works.

## Background

Dispatching still runs on manual work: the coordinator checks the
department channels every hour, a dispatch tracker file keeps the books,
and the "report progress" discipline chases updates. Once tasks pile up,
that does not scale. This task implements the minimum viable automated
task queue.

## Goal

On the host, under the task-queue directory: a SQLite ledger + a Router
scheduling prototype + a minimal Worker. Verify that automatic
scheduling and state persistence work.

## Acceptance criteria

1. `sqlite3 <db> "SELECT COUNT(*) FROM task;"` returns a number that
   matches the number of tasks imported from the dispatch tracker.
2. `curl -X POST http://127.0.0.1:8901/dispatch -H 'Content-Type:
   application/json' -d '{"title":"test","dept":"test","priority":1}'`
   returns a task id, and a database query shows that task's status as
   `queued`.
3. The Router schedules 3 test tasks by priority (high → low), and the
   `task_event` table has the matching state-change records
   (queued → routed → working → success).
4. `sqlite3 <db> "SELECT SUM(prompt_tokens+completion_tokens) FROM
   run_cost;"` returns non-zero (the Worker called a model, so there is
   a cost record).

## Steps

1. Create the database: `sqlite3 <db> < schema.sql` (5 tables: task /
   task_event / run_cost / internal_check / attention — see
   `task-queue/schema.sql`).
2. Write a migration script: parse the existing dispatch tracker file
   and import its tasks into the `task` and `task_event` tables.
3. Write the Router: a web service with `POST /dispatch` (takes a task
   brief, parses department / priority / deadline, generates a UUID,
   writes the task table with status `queued`); a polling scheduler
   takes the highest-priority queued task → marks it `routed` → calls
   the Worker.
4. Write the Worker (minimal version): reads a task id, calls a model
   once to complete a short exchange, writes the result back with
   status `success`, and records the cost.
5. Run 3 test tasks through and attach the command outputs for
   acceptance.

## Table structure (5 tables)

```sql
CREATE TABLE task(task_id TEXT PRIMARY KEY,title TEXT,dept TEXT,priority INTEGER,status TEXT,created_at TEXT,deadline TEXT,worktree_id TEXT,parent_task_id TEXT);
CREATE TABLE task_event(event_id INTEGER PRIMARY KEY AUTOINCREMENT,task_id TEXT,ts TEXT,type TEXT,payload TEXT);
CREATE TABLE run_cost(run_id INTEGER PRIMARY KEY AUTOINCREMENT,task_id TEXT,ts TEXT,model TEXT,prompt_tokens INTEGER,completion_tokens INTEGER,cost_usd REAL);
CREATE TABLE internal_check(check_id INTEGER PRIMARY KEY AUTOINCREMENT,task_id TEXT,ts TEXT,check_type TEXT,result TEXT,detail TEXT);
CREATE TABLE attention(attention_id INTEGER PRIMARY KEY AUTOINCREMENT,task_id TEXT,ts TEXT,question TEXT,why TEXT,suggested_option TEXT,choices TEXT,resolved INTEGER DEFAULT 0);
PRAGMA journal_mode=WAL;
```

## Red lines

- Do not modify the existing dispatch tracker file (read-only migration).
- Do not stuff attention items into the task brief (they are standalone
  message objects, for a later iteration).
- Do not write to the database on every token call (flush in batches
  every 5–10 seconds).
- The state machine uses only these 7 states:
  queued / routed / working / internal_check / awaiting_human /
  success / failed / timeout.

## Notes

- Router port suggestion: 8901 (to avoid clashing with the dashboard
  on 8900).
- Failure retries, spot checks, and worktree isolation are not in this
  version — later iterations.

## Receipt

Attach the actual outputs of the 4 acceptance commands, plus one
sentence: "minimum version works". No performance review.
