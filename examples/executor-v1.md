# Example Task Pack v1: Real Executor for the Task Queue

> Ran end to end. Target: a Worker that really executes tasks.

## Background

The task queue MVP works (scheduling + ledger), but the Worker is a
stub — it only calls a model to summarize the task title in one
sentence and does not execute the task content. This task implements a
Worker that really executes tasks.

## Goal

The Worker can execute three kinds of actions from a task brief: run
a shell command, run a Python script, call an HTTP API (v1 does GET
only). Execution results are written back to the task table, and the
cost is recorded.

## Acceptance criteria

1. Dispatch a "run `echo hello`" task: the result field contains
   "hello", status `success`.
2. Dispatch a "run Python to print 1+1" task: the result contains "2",
   status `success`.
3. Dispatch a "GET the local dashboard" task: the result contains a
   fragment of the dashboard HTML, status `success`.
4. Dispatch a "run `rm -rf /`" task: status `failed`, failure reason
   "hit the blacklist".
5. Dispatch a "run `rm -rf /*`" task (a bypass variant): status
   `failed`, blocked by the same blacklist.

## Steps

1. Next to `worker.py`, add `executor.py`: parse the task pack JSON
   (`{"action":"shell","cmd":"…"}`) and dispatch on `action`
   (shell / python / http_get).
2. shell: `subprocess.run`, 60-second timeout, stdout/stderr truncated
   to 2000 characters and written back to `result`.
3. python: same, via `python3 -c` or by running a script file; the
   payload goes through the same blacklist.
4. http_get: HTTP GET, 30-second timeout; **block the cloud metadata
   address, block non-http(s) schemes**.
5. Blacklist (matched by pattern): `rm -rf /`, `rm -rf /*`, `rm -rf ~`,
   `mkfs`, `dd of=/dev/`, fork bombs, `curl|wget … | sh`, `curl|wget …
   | bash`, `/dev/tcp/`, `chmod -R /`, `iptables -F`, `crontab -r`,
   `shutdown`, `reboot`.
6. The `/work` endpoint is async: it returns 202 on receipt and
   executes in a background thread, so it never blocks the scheduling
   loop.
7. On timeout, kill the whole process group: start a new session and
   kill the group.

## Red lines

- Never execute a blacklisted command (matched by pattern, not only by
  exact string).
- Never run the Worker as root (use a low-privilege user) — this matters
  more than the blacklist itself.
- Never print a secret into a log.
- On timeout, the process group must be killed; nothing may hang.
- v1 does not do POST (write-operation / request-forgery risk) and does
  not retry automatically.

## Notes

- Build shell + Python first; http_get can come after.
- Execution tasks record elapsed time as cost.
- The task pack reuses the JSON format, so no new table field is needed.

## Receipt

Attach the actual outputs of the 5 acceptance commands, plus one
sentence: "the real executor works".
