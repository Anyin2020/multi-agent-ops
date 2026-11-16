#!/usr/bin/env python3
"""任务队列 Router：FastAPI 调度器（端口 8901）"""
import os
import sqlite3
import uuid
import threading
import time
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

DB = os.environ.get("TASKQUEUE_DB", "/data/taskqueue/dispatch.db")
app = FastAPI(title="TaskQueue Router")

class DispatchReq(BaseModel):
    title: str
    dept: str = "general"
    priority: int = 2
    deadline: str = ""
    task_pack: str = ""

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def log_event(task_id, old, new, actor, note=""):
    c = db()
    c.execute(
        "INSERT INTO task_event (task_id, old_status, new_status, actor, note, created_at) VALUES (?,?,?,?,?,?)",
        (task_id, old, new, actor, note, datetime.now().isoformat())
    )
    c.execute("UPDATE task SET status=?, updated_at=? WHERE task_id=?",
              (new, datetime.now().isoformat(), task_id))
    c.commit()
    c.close()

@app.post("/dispatch")
def dispatch(req: DispatchReq):
    tid = str(uuid.uuid4())[:8]
    now = datetime.now().isoformat()
    c = db()
    c.execute(
        "INSERT INTO task (task_id, title, dept, priority, status, deadline, task_pack, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?)",
        (tid, req.title, req.dept, req.priority, "queued", req.deadline, req.task_pack, now, now)
    )
    c.execute(
        "INSERT INTO task_event (task_id, old_status, new_status, actor, note, created_at) VALUES (?,?,?,?,?,?)",
        (tid, None, "queued", "router", "任务创建", now)
    )
    c.commit()
    c.close()
    return {"task_id": tid, "status": "queued"}

@app.get("/tasks")
def list_tasks(status: str = ""):
    c = db()
    if status:
        rows = c.execute("SELECT * FROM task WHERE status=? ORDER BY priority, created_at", (status,)).fetchall()
    else:
        rows = c.execute("SELECT * FROM task ORDER BY priority, created_at").fetchall()
    c.close()
    return [dict(r) for r in rows]

@app.get("/task/{task_id}")
def get_task(task_id: str):
    c = db()
    r = c.execute("SELECT * FROM task WHERE task_id=?", (task_id,)).fetchone()
    c.close()
    return dict(r) if r else {"error": "not found"}

def scheduler_loop():
    """轮询调度器：按 priority 取 queued → routed → 调 Worker"""
    import urllib.request, json
    while True:
        try:
            c = db()
            row = c.execute(
                "SELECT task_id FROM task WHERE status='queued' ORDER BY priority ASC, created_at ASC LIMIT 1"
            ).fetchone()
            c.close()
            if row:
                tid = row["task_id"]
                log_event(tid, "queued", "routed", "router", "调度器选中")
                # 调 Worker（同步调用，MVP 简化版）
                try:
                    req = urllib.request.Request(
                        "http://127.0.0.1:8902/work",
                        data=json.dumps({"task_id": tid}).encode(),
                        headers={"Content-Type": "application/json"},
                    )
                    with urllib.request.urlopen(req, timeout=300) as resp:
                        pass
                except Exception as e:
                    log_event(tid, "routed", "failed", "router", f"Worker 调用失败: {e}")
        except Exception as e:
            print(f"scheduler error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()
    uvicorn.run(app, host="127.0.0.1", port=8901)
