-- Task queue ledger schema (SQLite, WAL mode).
-- Five tables. Created once; the router and worker use it as-is.
CREATE TABLE task (
    task_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    dept TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 2,  -- 0=P0, 1=P1, 2=P2
    status TEXT NOT NULL DEFAULT 'queued',  -- queued/routed/working/internal_check/awaiting_human/success/failed/timeout
    deadline TEXT,
    task_pack TEXT,  -- task brief content (JSON)
    result TEXT,     -- execution result summary
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX idx_task_status ON task(status);
CREATE INDEX idx_task_priority ON task(priority);
CREATE TABLE task_event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL REFERENCES task(task_id),
    old_status TEXT,
    new_status TEXT NOT NULL,
    actor TEXT NOT NULL,  -- router/worker/human/system
    note TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX idx_event_task ON task_event(task_id);
CREATE TABLE run_cost (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL REFERENCES task(task_id),
    model TEXT NOT NULL,
    prompt_tokens INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE INDEX idx_cost_task ON run_cost(task_id);
CREATE TABLE internal_check (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL REFERENCES task(task_id),
    check_type TEXT NOT NULL,
    passed INTEGER NOT NULL,   -- 0/1
    detail TEXT,
    created_at TEXT NOT NULL
);
CREATE TABLE attention (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT REFERENCES task(task_id),
    item_type TEXT NOT NULL,  -- decision/blocked/sync, etc.
    content TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending/acked/done
    created_at TEXT NOT NULL
);
PRAGMA journal_mode=WAL;
