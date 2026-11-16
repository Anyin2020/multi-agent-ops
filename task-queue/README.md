# Task Queue

The task queue turns manual dispatch into an automated loop: the
coordinator posts a task, the Router schedules it, the Worker executes
it, and every state change and cost is written to a SQLite ledger.

## Architecture

```
POST /dispatch → task table (queued)
       ↓ Router polls (5s, by priority)
     routed → calls Worker :8902/work
       ↓ Worker executes the task pack
 working → success/failed → task_event records the whole chain
```

- **Router** (`router.py`, FastAPI, loopback port 8901): `POST /dispatch`
  takes a task brief (title, department, priority, deadline, task pack),
  writes it to the `task` table as `queued`, and returns the task id.
  A scheduler thread polls every 5 seconds, takes the highest-priority
  queued task, marks it `routed`, and calls the Worker. `GET /tasks`
  and `GET /task/{task_id}` list and inspect tasks.
- **Worker** (`worker.py`, FastAPI, loopback port 8902): `POST /work`
  answers 202 immediately and executes in a background thread, so the
  scheduling loop is never blocked. It runs the task pack through
  `executor.py`, writes the result (truncated to 2000 characters) back
  to the task, records the cost, and moves the task to `success` or
  `failed`.
- **Executor** (`executor.py`): parses the task pack JSON and dispatches
  on `action`: `shell` (subprocess, 60s timeout), `python` (`python3
  -c`), or `http_get` (30s timeout). See below for the safety rules.

## Data tables

- `task`: the task itself (task_id/title/dept/priority/status/deadline/
  task_pack/result).
- `task_event`: the state-change audit trail
  (queued → routed → working → success/failed).
- `run_cost`: cost per run (model, prompt tokens, completion tokens).
- `internal_check`: internal check records (reserved).
- `attention`: pending items (reserved; a standalone message object,
  not stuffed into the task brief).

State machine — only these 8 states:
`queued / routed / working / internal_check / awaiting_human / success /
failed / timeout`

## Safety rules (executor)

- **Blacklist, by pattern** (not just exact strings): destructive
  commands (`rm -rf /`, `rm -rf /*`, `rm -rf ~`, `mkfs`, `dd of=/dev/`),
  fork bombs, `curl|wget … | sh|bash`, `/dev/tcp/`, `chmod -R /`,
  `iptables -F`, `crontab -r`, `shutdown`, `reboot`, `halt`, `poweroff`.
  A hit means `failed` — the command is never executed.
- **SSRF protection for http_get**: only `http`/`https` schemes; the
  cloud metadata address and internal addresses are blocked (loopback
  is allowed, for local dashboard tests).
- **Timeout kills the process group**: the child runs in a new session;
  on timeout the whole group is killed, so nothing hangs.
- **Runs as a low-privilege user, never root.** This matters more than
  the blacklist itself.
- **No secrets in logs.**
- **v1 does not do POST** (write-operation risk) and does not retry
  automatically.

## Status: built, in verification

The Router and Worker run as system services on the host. As of
2026-11-16 both services are active, and the ledger shows real traffic:
17 tasks succeeded, 3 failed, 1 working, with 53 state-change events
and 10 cost records. The executor started as a stub (scheduling and
bookkeeping only) and was upgraded to a real executor that runs shell,
Python, and HTTP GET actions.

## Operations

```bash
# Check status
sudo systemctl status taskqueue-router taskqueue-worker

# Restart
sudo systemctl restart taskqueue-router taskqueue-worker

# Logs
tail -f /data/taskqueue/router.log /data/taskqueue/worker.log

# Dispatch a test task
curl -X POST http://127.0.0.1:8901/dispatch \
  -H 'Content-Type: application/json' \
  -d '{"title":"test","dept":"test","priority":1}'
```

## Acceptance checks

```bash
sqlite3 /data/taskqueue/dispatch.db "SELECT COUNT(*) FROM task;"
curl -X POST http://127.0.0.1:8901/dispatch -H 'Content-Type: application/json' -d '{"title":"test","dept":"test","priority":1}'
sqlite3 /data/taskqueue/dispatch.db "SELECT SUM(prompt_tokens+completion_tokens) FROM run_cost;"
```

The executor's own acceptance checks (see `examples/executor-v1.md`):
a shell task, a Python task, an HTTP GET task, and two blacklist
rejections — all five must pass.
