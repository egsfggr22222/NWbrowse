# -*- coding: utf-8 -*-
"""下载记录存储。读写项目根目录下的 downloads.json。

记录结构：
    [
        {
            "url": "https://example.com/file.zip",
            "path": "C:/Users/xxx/Downloads/file.zip",
            "filename": "file.zip",
            "time": 1758600000.0,
            "status": "completed",
            "progress": 100,
            "total": 10485760,
            "received": 10485760,
            "window_id": "df-0"
        },
        ...
    ]

status 取值：
    "downloading"  下载中
    "completed"    已完成
    "failed"       失败
    "cancelled"    已取消
"""

import os
import json
import time

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "downloads.json")

# 最多保留多少条
MAX_RECORDS = 500


# ======================================================================
# 底层读写
# ======================================================================
def _load():
    try:
        if os.path.isfile(STORE_PATH):
            with open(STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def _save(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ======================================================================
# 对外接口
# ======================================================================
def load_downloads():
    """读全部记录。返回 list。"""
    return _load()


def add_download(url, path, filename, status="downloading", window_id=""):
    """新增或更新一条记录。

    如果同 url 同 path 已有，就更新状态和时间，不重复加。
    新记录插在最前面。

    window_id: 发起下载的窗口进程 id（如 "df-0"），
               取消时用来定向转发给对应 window。
    """
    data = _load()

    for item in data:
        if item.get("url") == url and item.get("path") == path:
            item["status"] = status
            item["time"] = time.time()
            item["filename"] = filename or item.get("filename", "")
            item["window_id"] = window_id or item.get("window_id", "")
            # 重置进度
            item["progress"] = 0
            item["total"] = 0
            item["received"] = 0
            _save(data)
            return

    data.insert(0, {
        "url": url or "",
        "path": path or "",
        "filename": filename or "",
        "time": time.time(),
        "status": status,
        "progress": 0,
        "total": 0,
        "received": 0,
        "window_id": window_id or "",
    })

    if len(data) > MAX_RECORDS:
        data = data[:MAX_RECORDS]

    _save(data)


def update_download_status(url, path, status):
    """按 url + path 定位记录，改状态。path 为空时按 url 匹配所有。"""
    data = _load()
    changed = False
    for item in data:
        if item.get("url") != url:
            continue
        if path and item.get("path") != path:
            continue
        item["status"] = status
        changed = True
    if changed:
        _save(data)


def update_download_progress(url, received, total):
    """更新下载进度。

    received: 已收字节
    total: 总字节。为 0 表示未知，progress 记 0。
    """
    data = _load()
    changed = False
    received = int(received)
    total = int(total)

    for item in data:
        if item.get("url") != url:
            continue
        item["received"] = received
        item["total"] = total
        if total > 0:
            item["progress"] = int(received * 100 / total)
        else:
            item["progress"] = 0
        changed = True
    if changed:
        _save(data)


def get_download_by_url(url):
    """按 url 找记录。返回 dict 或 None。"""
    if not url:
        return None
    data = _load()
    for item in data:
        if item.get("url") == url:
            return item
    return None


def remove_download_by_index(index):
    """按列表索引删除一条记录。"""
    data = _load()
    if 0 <= index < len(data):
        data.pop(index)
        _save(data)


def clear_downloads():
    """清空所有记录。不删文件。"""
    _save([])


def mark_stale_downloads_failed():
    """把还停留在 downloading 状态的记录标记为 failed。

    用于下载管理进程启动时清理上一轮会话的残留：上一轮没跑完就退出的
    下载（对应的窗口 / worker 都已经死了），如果一直留在"下载中"，
    进度条会永远卡着不动。
    """
    data = _load()
    changed = False
    for item in data:
        if item.get("status") == "downloading":
            item["status"] = "failed"
            changed = True
    if changed:
        _save(data)
    return changed


def file_status(path):
    """检查文件状态。

    返回:
        "ok"       父目录存在且文件存在
        "missing"  父目录不存在，或文件不存在
    """
    if not path:
        return "missing"

    try:
        parent = os.path.dirname(path)
        if not parent:
            return "ok" if os.path.isfile(path) else "missing"

        if not os.path.isdir(parent):
            return "missing"

        if not os.path.isfile(path):
            return "missing"

        return "ok"
    except Exception:
        return "missing"