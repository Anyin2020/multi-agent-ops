#!/usr/bin/env python3
"""任务队列真执行器：解析 task_pack JSON，按 action 执行"""
import json
import re
import signal
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime

# 黑名单模式（正则）
BLACKLIST_PATTERNS = [
    r"rm\s+-rf\s+/\s*$",           # rm -rf /
    r"rm\s+-rf\s+/\*\s*",          # rm -rf /*
    r"rm\s+-rf\s+~\s*",            # rm -rf ~
    r"rm\s+-rf\s+/",               # rm -rf / 开头（宽松）
    r"\bmkfs\b",
    r"\bdd\s+.*of=/dev/",
    r":\(\)\s*\{",                 # fork bomb
    r"curl.*\|\s*sh\b",
    r"wget.*\|\s*sh\b",
    r"curl.*\|\s*bash\b",
    r"wget.*\|\s*bash\b",
    r"/dev/tcp/",
    r"chmod\s+-R\s+/",
    r"iptables\s+-F",
    r"crontab\s+-r",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bhalt\b",
    r"\bpoweroff\b",
]

# http_get 禁止的目标
BLOCKED_HOSTS = ["169.254.169.254", "metadata.google.internal"]
BLOCKED_SCHEMES = ["file", "ftp", "gopher", "dict"]

def check_blacklist(cmd):
    """检查命令是否命中黑名单，返回 (命中, 原因)"""
    for pattern in BLACKLIST_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return True, f"命中黑名单模式: {pattern}"
    return False, ""

def run_shell(cmd, timeout=60):
    """跑 shell 命令，超时杀进程组"""
    hit, reason = check_blacklist(cmd)
    if hit:
        return {"ok": False, "error": f"命中黑名单: {reason}", "output": ""}
    try:
        proc = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            start_new_session=True,  # 新进程组，超时可 killpg
            text=True,
        )
        try:
            out, _ = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # 杀整个进程组
            import os
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            out, _ = proc.communicate()
            return {"ok": False, "error": f"超时 ({timeout}s)，已杀进程组", "output": out[:2000]}
        return {"ok": proc.returncode == 0, "output": out[:2000], "returncode": proc.returncode}
    except Exception as e:
        return {"ok": False, "error": str(e), "output": ""}

def run_python(code, timeout=60):
    """跑 Python 代码（同样过黑名单）"""
    hit, reason = check_blacklist(code)
    if hit:
        return {"ok": False, "error": f"命中黑名单: {reason}", "output": ""}
    return run_shell(f"python3 -c {json.dumps(code)}", timeout=timeout)

def http_get(url, timeout=30):
    """HTTP GET，禁 SSRF"""
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return {"ok": False, "error": f"禁止的 scheme: {parsed.scheme}", "output": ""}
        host = parsed.hostname or ""
        if host in BLOCKED_HOSTS:
            return {"ok": False, "error": f"禁止的主机: {host}（实例元数据）", "output": ""}
        # 禁内网 IP（简单版）
        if host.startswith(("10.", "192.168.", "172.16.", "172.17.", "172.18.", "172.19.",
                            "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.",
                            "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.")):
            # 允许 127.0.0.1（本地面板测试用）
            if host != "127.0.0.1" and not host.startswith("127."):
                return {"ok": False, "error": f"禁止的内网地址: {host}", "output": ""}
        req = urllib.request.Request(url, headers={"User-Agent": "TaskQueue/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(10000).decode("utf-8", errors="replace")
        return {"ok": True, "output": body[:2000]}
    except Exception as e:
        return {"ok": False, "error": str(e), "output": ""}

def execute(task_pack_json):
    """主入口：解析 task_pack 并执行，返回 (ok, result_text)"""
    try:
        pack = json.loads(task_pack_json) if isinstance(task_pack_json, str) else task_pack_json
    except Exception as e:
        return False, f"task_pack JSON 解析失败: {e}"
    
    action = pack.get("action", "")
    if action == "shell":
        r = run_shell(pack.get("cmd", ""))
    elif action == "python":
        r = run_python(pack.get("code", ""))
    elif action == "http_get":
        r = http_get(pack.get("url", ""))
    else:
        return False, f"未知 action: {action}（支持: shell/python/http_get）"
    
    if r["ok"]:
        return True, r.get("output", "")
    else:
        return False, r.get("error", "执行失败")
