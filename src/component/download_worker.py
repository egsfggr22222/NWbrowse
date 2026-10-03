# -*- coding: utf-8 -*-
"""独立下载子进程：纯命令行 HTTP 请求，不碰浏览器。

由 window.py 启动。启动后不立刻下载，先等 window 发来
MSG_DOWNLOAD_START_WORKER（带 Cookie），收到后才开始。

主线程跑 Qt 事件循环收 IPC，下载在子线程。
主线程用 QTimer 轮询 _start_event，不用 threading.Event.wait 阻塞。

退出码：
  0   成功
  1   失败
  2   被取消
"""

import sys
import os
import json
import time
import argparse
import threading
import urllib.request
import urllib.error
from urllib.parse import urlparse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ipc import (
    IpcClient, IpcServer,
    ROLE_DOWNLOADS,
    window_channel,
    MSG_DOWNLOAD_PROGRESS, MSG_DOWNLOAD_DONE,
    MSG_DOWNLOAD_START,
    MSG_DOWNLOAD_CANCEL_WORKER,
    MSG_DOWNLOAD_START_WORKER,
)
from loader import QApplication, QTimer


_cancel_flag = threading.Event()
_start_event = threading.Event()
_start_cookie = {"value": ""}


class _Cancelled(Exception):
    pass


def _make_opener(cookie, referer, user_agent):
    opener = urllib.request.build_opener()
    headers = []
    if cookie:
        headers.append(("Cookie", cookie))
    if referer:
        headers.append(("Referer", referer))
    if user_agent:
        headers.append(("User-Agent", user_agent))
    else:
        headers.append(("User-Agent", "Mozilla/5.0"))
    opener.addheaders = headers
    return opener


def _download(url, path, referer, user_agent, window_id):
    cookie = _start_cookie["value"]
    part_path = path + ".part"

    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        try:
            os.makedirs(parent, exist_ok=True)
        except Exception as e:
            return False, f"创建目录失败: {e}"

    opener = _make_opener(cookie, referer, user_agent)

    try:
        resp = opener.open(url, timeout=30)
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"URLError: {e.reason}"
    except Exception as e:
        return False, f"打开失败: {e}"

    try:
        total = int(resp.headers.get("Content-Length", -1))
    except Exception:
        total = -1

    received = 0
    last_report = 0.0

    _send_start(url, path, total, window_id)

    try:
        with open(part_path, "wb") as f:
            while True:
                if _cancel_flag.is_set():
                    raise _Cancelled()
                try:
                    chunk = resp.read(64 * 1024)
                except Exception as e:
                    return False, f"读取出错: {e}"
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                now = time.time()
                if now - last_report >= 0.5:
                    last_report = now
                    _send_progress(url, path, received, total, window_id)

    except _Cancelled:
        try:
            if os.path.isfile(part_path):
                os.remove(part_path)
        except Exception:
            pass
        _send_done(url, path, success=False, delete_partial=False,
                   window_id=window_id)
        return False, "cancelled"

    except Exception as e:
        try:
            if os.path.isfile(part_path):
                os.remove(part_path)
        except Exception:
            pass
        _send_done(url, path, success=False, delete_partial=False,
                   window_id=window_id)
        return False, f"写入出错: {e}"

    finally:
        try:
            resp.close()
        except Exception:
            pass

    try:
        if os.path.isfile(path):
            os.remove(path)
        os.rename(part_path, path)
    except Exception as e:
        return False, f"重命名失败: {e}"

    _send_progress(url, path, received, total if total > 0 else received,
                   window_id)
    _send_done(url, path, success=True, delete_partial=False,
               window_id=window_id)
    return True, "ok"


def _send_start(url, path, total, window_id):
    try:
        payload = json.dumps({
            "url": url,
            "path": path,
            "filename": os.path.basename(path),
            "total": total,
            "notify": True,
            "window_id": window_id,
        }, ensure_ascii=False)
        IpcClient.send_to_role(
            ROLE_DOWNLOADS, MSG_DOWNLOAD_START,
            payload.encode("utf-8"),
        )
    except Exception as e:
        print(f"[worker] 发开始失败: {e}")


def _send_progress(url, path, received, total, window_id):
    try:
        payload = json.dumps({
            "url": url,
            "path": path,
            "received": received,
            "total": total,
        }, ensure_ascii=False)
        IpcClient.send_to_role(
            ROLE_DOWNLOADS, MSG_DOWNLOAD_PROGRESS,
            payload.encode("utf-8"),
        )
    except Exception as e:
        print(f"[worker] 发进度失败: {e}")


def _send_done(url, path, success, delete_partial, window_id):
    try:
        payload = json.dumps({
            "url": url,
            "path": path,
            "success": bool(success),
            "delete_partial": bool(delete_partial),
        }, ensure_ascii=False)
        IpcClient.send_to_role(
            ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE,
            payload.encode("utf-8"),
        )
    except Exception as e:
        print(f"[worker] 发完成失败: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--window-id", default="")
    parser.add_argument("--referer", default="")
    parser.add_argument("--user-agent", default="")
    args = parser.parse_args()

    app = QApplication(sys.argv)

    my_channel = window_channel(args.window_id) + "_worker"

    def on_message(msg_type, payload):
        if msg_type == MSG_DOWNLOAD_START_WORKER:
            try:
                data = json.loads(payload.decode("utf-8"))
                _start_cookie["value"] = data.get("cookie", "") or ""
            except Exception:
                _start_cookie["value"] = ""
            print(f"[worker] 收到开始指令，cookie 长度="
                  f"{len(_start_cookie['value'])}")
            _start_event.set()
        elif msg_type == MSG_DOWNLOAD_CANCEL_WORKER:
            print("[worker] 收到取消")
            _cancel_flag.set()
            _start_event.set()

    server = IpcServer(my_channel, on_message, role=my_channel)
    if not server.start():
        print("[worker] 监听失败，退出")
        sys.exit(1)

    state = {
        "started": False,
        "done": False,
        "ok": False,
        "msg": "timeout",
    }

    def _do_download():
        ok, msg = _download(
            args.url, args.path,
            args.referer, args.user_agent,
            args.window_id,
        )
        state["ok"] = ok
        state["msg"] = msg
        state["done"] = True

    def check_state():
        if state["done"]:
            try:
                server.stop()
            except Exception:
                pass
            app.quit()
            return

        if _start_event.is_set() and not state["started"]:
            if _cancel_flag.is_set():
                state["done"] = True
                state["msg"] = "cancelled"
                try:
                    server.stop()
                except Exception:
                    pass
                app.quit()
                return
            state["started"] = True
            threading.Thread(target=_do_download, daemon=True).start()

        QTimer.singleShot(100, check_state)

    QTimer.singleShot(100, check_state)

    def timeout_check():
        if not state["started"] and not state["done"]:
            print("[worker] 等待开始指令超时")
            state["done"] = True
            state["msg"] = "timeout"
            try:
                server.stop()
            except Exception:
                pass
            app.quit()

    QTimer.singleShot(60000, timeout_check)

    app.exec()

    if state["ok"]:
        sys.exit(0)
    elif state["msg"] == "cancelled":
        sys.exit(2)
    else:
        print(f"[worker] 失败: {state['msg']}")
        sys.exit(1)


if __name__ == "__main__":
    main()