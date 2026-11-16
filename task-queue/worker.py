#!/usr/bin/env python3
"""任务队列 Worker v2：真执行器（端口 8902）"""
import sqlite3
import json
import threading
import time
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import sys
sys.path.insert(0, "/data/taskqueue")
from executor import execute

DB = "/data/taskqueue/dispatch.db"
app = FastAPI(title="TaskQueue Worker v2")

class WorkReq(BaseModel):
    task_id: str

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

def do_work(task_id):
    """后台执行任务（线程）"""
    c = db()
    task = c.execute("SELECT * FROM task WHERE task_id=?", (task_id,)).fetchone()
    c.close()
    if not task:
        return
    
    log_event(task_id, "routed", "working", "worker", "开始执行")
    start = time.time()
    try:
        ok, result = execute(task["task_pack"] or "{}")
        elapsed = time.time() - start
        c = db()
        # 成本记执行时长
        c.execute(
            "INSERT INTO run_cost (task_id, model, prompt_tokens, completion_tokens, created_at) VALUES (?,?,?,?,?)",
            (task_id, "executor", int(elapsed), 0, datetime.now().isoformat())
        )
        c.execute("UPDATE task SET result=?, updated_at=? WHERE task_id=?",
                  (result[:2000], datetime.now().isoformat(), task_id))
        c.commit()
        c.close()
        if ok:
            log_event(task_id, "working", "success", "worker", f"执行完成 ({elapsed:.1f}s)")
        else:
            log_event(task_id, "working", "failed", "worker", result[:200])
    except Exception as e:
        log_event(task_id, "working", "failed", "worker", f"执行异常: {e}")

@app.post("/work", status_code=202)
def work(req: WorkReq):
    """接单即返回 202，后台线程执行，不阻塞调度循环"""
    tid = req.task_id
    c = db()
    task = c.execute("SELECT task_id FROM task WHERE task_id=?", (tid,)).fetchone()
    c.close()
    if not task:
        return {"error": "task not found"}
    t = threading.Thread(target=do_work, args=(tid,), daemon=True)
    t.start()
    return {"task_id": tid, "status": "accepted"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8902)
