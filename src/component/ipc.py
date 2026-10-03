# -*- coding: utf-8 -*-
"""本地 IPC：QLocalServer / QLocalSocket + 进程注册表 + 计时。

通道名约定：
    窗口：  browser_window_<id>       role = window:<id>
    窗口 worker：browser_window_<id>_worker  （下载子进程监听）
    bar：   browser_bar_channel       role = bar
    托盘：  browser_tray_channel      role = tray
    设置：  browser_settings_channel  role = settings
    下载：  browser_downloads_channel role = downloads
    广播：  browser_broadcast_channel（预留，未使用）

消息格式：
    [4 字节大端长度][1 字节类型][N 字节负载]
    长度 = 1(类型) + len(负载)
    完整消息字节数 = 4 + 长度

注册表结构（每个 role 一条）：
    {
        "window:cn.bing.com": {
            "pid": 12345,
            "channel": "browser_window_cn.bing.com",
            "time": 1758600000.0,
            "type": "default",
            "window_id": "cn.bing.com",
            "hosts": ["bing.com", "cn.bing.com"],
            "host": "cn.bing.com"
        },
        ...
    }
"""

import struct
import json
import os
import tempfile
import time

from loader import *
from PyQt6.QtNetwork import QLocalServer, QLocalSocket


IPC_TIMING = True


def _t():
    return time.perf_counter()


def _log(tag, t0, extra=""):
    if not IPC_TIMING:
        return
    dt = (time.perf_counter() - t0) * 1000
    print(f"[ipc-t] {tag} {dt:.1f}ms {extra}")


CHANNEL_BAR = "browser_bar_channel"
CHANNEL_TRAY = "browser_tray_channel"
CHANNEL_SETTINGS = "browser_settings_channel"
CHANNEL_DOWNLOADS = "browser_downloads_channel"
CHANNEL_BROADCAST = "browser_broadcast_channel"

CHANNEL_WINDOW_PREFIX = "browser_window_"

ROLE_BAR = "bar"
ROLE_TRAY = "tray"
ROLE_SETTINGS = "settings"
ROLE_DOWNLOADS = "downloads"
ROLE_WINDOW_PREFIX = "window:"


def window_channel(window_id):
    return CHANNEL_WINDOW_PREFIX + str(window_id)


def window_role(window_id):
    return ROLE_WINDOW_PREFIX + str(window_id)


MSG_SHOW = 1
MSG_HIDE = 2
MSG_PING = 3
MSG_PONG = 4
MSG_QUIT = 5
MSG_NAVIGATE = 6
MSG_CONFIG_CHANGED = 8
MSG_OPEN_SETTINGS = 9
MSG_SETTINGS_SHOW = 10
MSG_LANGUAGE_CHANGED = 11
MSG_OPEN_DOWNLOADS = 12
MSG_DOWNLOADS_SHOW = 13
MSG_DOWNLOADS_REFRESH = 14
MSG_DOWNLOAD_DONE = 16
MSG_DOWNLOAD_START = 17
MSG_DOWNLOAD_PROGRESS = 18
MSG_DOWNLOAD_CANCEL_FOR_WINDOW = 21
MSG_DOWNLOAD_CANCEL_WORKER = 22
MSG_DOWNLOAD_START_WORKER = 23
MSG_REVERT_TO_LAST_URL = 24
MSG_PIN_RELOAD = 25           # window → bar：刷新固定图标（建/删/改）
MSG_PIN_STATE = 26            # window → bar：上报固定开关状态
MSG_PIN_TOGGLE_FROM_BAR = 27  # bar → window：bar 处取消固定，让 window 关开关
MSG_PIN_DATA = 28             # window → bar：上报固定内容（host/popup/索引）
MSG_PIN_REQUEST = 29          # bar → window：向 window 请求固定内容
MSG_FAVORITE_CHANGED = 30     # 收藏变化：广播给所有窗口


HEADER = struct.Struct(">IB")
HEADER_SIZE = HEADER.size


REGISTRY_PATH = os.path.join(tempfile.gettempdir(), "browser_ipc_registry.json")


def _read_registry():
    t0 = _t()
    result = {}
    try:
        if os.path.isfile(REGISTRY_PATH):
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                result = data
    except Exception:
        pass
    _log("registry.read", t0, f"keys={len(result)}")
    return result


def _write_registry(data):
    t0 = _t()
    try:
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    _log("registry.write", t0, f"keys={len(data)}")


def register_process(role, channel, pid=None, extra=None):
    if pid is None:
        pid = os.getpid()
    data = _read_registry()
    entry = {"pid": pid, "channel": channel, "time": time.time()}
    if extra:
        entry.update(extra)
    data[role] = entry
    _write_registry(data)


def unregister_process(role):
    data = _read_registry()
    if role in data:
        del data[role]
        _write_registry(data)


def find_process(role):
    data = _read_registry()
    return data.get(role)


def find_windows(predicate=None):
    data = _read_registry()
    out = {}
    for role, entry in data.items():
        if not role.startswith(ROLE_WINDOW_PREFIX):
            continue
        if predicate is None or predicate(entry):
            out[role] = entry
    return out


def find_window_by_host(host):
    if not host:
        return None, None
    data = _read_registry()
    for role, entry in data.items():
        if not role.startswith(ROLE_WINDOW_PREFIX):
            continue
        # 跳过死进程
        if not _pid_alive(entry.get("pid")):
            continue
        hosts = entry.get("hosts")
        if isinstance(hosts, list) and host in hosts:
            return role, entry
        if entry.get("host") == host:
            return role, entry
    return None, None


def alloc_window_id(prefix, active_ids):
    used = set()
    p = prefix + "-"
    for wid in active_ids:
        if wid.startswith(p):
            try:
                used.add(int(wid[len(p):]))
            except ValueError:
                pass
    n = 0
    while n in used:
        n += 1
    return f"{prefix}-{n}"


def cleanup_registry():
    data = _read_registry()
    changed = False
    for role, entry in list(data.items()):
        pid = entry.get("pid")
        if not _pid_alive(pid):
            del data[role]
            changed = True
    if changed:
        _write_registry(data)


def _pid_alive(pid):
    if pid is None:
        return False
    try:
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h = ctypes.windll.kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid)
        )
        if not h:
            return False
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    except Exception:
        return True


def encode(msg_type, payload=b""):
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    length = 1 + len(payload)
    return HEADER.pack(length, msg_type) + payload


class MessageReader:
    def __init__(self, on_message):
        self._buf = bytearray()
        self._on_message = on_message

    def feed(self, data: bytes):
        if data:
            self._buf.extend(data)
        while True:
            if len(self._buf) < HEADER_SIZE:
                return
            length, msg_type = HEADER.unpack(bytes(self._buf[:HEADER_SIZE]))
            if length < 1:
                self._buf.clear()
                return
            total = 4 + length
            if len(self._buf) < total:
                return
            payload = bytes(self._buf[HEADER_SIZE:total])
            del self._buf[:total]
            try:
                self._on_message(msg_type, payload)
            except Exception as e:
                print("[ipc] 回调异常:", e)


class IpcServer:
    def __init__(self, channel, on_message, role=None, extra=None):
        self.channel = channel
        self._on_message = on_message
        self._role = role
        self._extra = extra
        self._server = QLocalServer()
        self._readers = {}

    def start(self):
        t0 = _t()
        QLocalServer.removeServer(self.channel)
        t1 = _t()
        if not self._server.listen(self.channel):
            QLocalServer.removeServer(self.channel)
            if not self._server.listen(self.channel):
                print(f"[ipc] 监听失败 {self.channel}:",
                      self._server.errorString())
                return False
        t2 = _t()
        self._server.newConnection.connect(self._on_new_conn)
        if self._role:
            register_process(self._role, self.channel, extra=self._extra)
        t3 = _t()
        _log("server.start", t0,
             f"channel={self.channel} "
             f"remove={1000*(t1-t0):.1f} listen={1000*(t2-t1):.1f} "
             f"reg={1000*(t3-t2):.1f}")
        return True

    def _on_new_conn(self):
        t0 = _t()
        conn = self._server.nextPendingConnection()
        reader = MessageReader(lambda t, p: self._on_message(t, p))
        self._readers[conn] = reader

        def _on_ready():
            t1 = _t()
            data = bytes(conn.readAll())
            reader.feed(data)
            _log("server.on_ready", t1,
                 f"channel={self.channel} bytes={len(data)}")

        def _on_disconn():
            self._readers.pop(conn, None)
            conn.deleteLater()

        conn.readyRead.connect(_on_ready)
        conn.disconnected.connect(_on_disconn)
        _log("server.new_conn", t0, f"channel={self.channel}")

    def stop(self):
        try:
            self._server.close()
        except Exception:
            pass
        if self._role:
            unregister_process(self._role)


class IpcClient:
    def __init__(self, channel):
        self.channel = channel

    def send(self, msg_type, payload=b"", timeout_ms=600):
        if not IPC_TIMING:
            sock = QLocalSocket()
            sock.connectToServer(self.channel)
            if not sock.waitForConnected(timeout_ms):
                return False
            sock.write(encode(msg_type, payload))
            sock.flush()
            sock.waitForBytesWritten(300)
            sock.disconnectFromServer()
            return True

        t0 = _t()
        sock = QLocalSocket()
        sock.connectToServer(self.channel)
        t1 = _t()
        if not sock.waitForConnected(timeout_ms):
            _log("client.connect 超时", t0,
                 f"channel={self.channel}")
            return False
        t2 = _t()
        sock.write(encode(msg_type, payload))
        sock.flush()
        sock.waitForBytesWritten(300)
        t3 = _t()
        sock.disconnectFromServer()
        _log("client.send", t0,
             f"channel={self.channel} type={msg_type} "
             f"connect={1000*(t1-t0):.1f} wait={1000*(t2-t1):.1f} "
             f"write={1000*(t3-t2):.1f}")
        return True

    @staticmethod
    def send_to_role(role, msg_type, payload=b"", timeout_ms=600):
        entry = find_process(role)
        if not entry:
            return False
        return IpcClient(entry["channel"]).send(
            msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_host_window(host, msg_type, payload=b"", timeout_ms=600):
        role, entry = find_window_by_host(host)
        if not role:
            return False
        return IpcClient(entry["channel"]).send(
            msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_tray(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_TRAY, msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_bar(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_BAR, msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_settings(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_SETTINGS, msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_downloads(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_DOWNLOADS, msg_type, payload, timeout_ms
        )


# ======================================================================
# 广播：遍历注册表，给每个进程逐个发
# ======================================================================
def broadcast(msg_type, payload=b"", exclude_role=None, timeout_ms=400):
    data = _read_registry()
    count = 0
    for role, entry in data.items():
        if exclude_role and role == exclude_role:
            continue
        ch = entry.get("channel")
        if not ch:
            continue
        try:
            if IpcClient(ch).send(msg_type, payload, timeout_ms):
                count += 1
        except Exception:
            pass
    return count


class RegistryWatchdog:
    def __init__(self, interval_ms=3000, parent=None):
        self._timer = QTimer(parent)
        self._timer.setInterval(interval_ms)
        self._timer.timeout.connect(cleanup_registry)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()