# -*- coding: utf-8 -*-
"""固定项存储。每个主域一个文件夹，放在项目根目录 fixed/ 下。

目录结构：
    fixed/
        bing.com/
            info.json      { host, hosts, popup_urls, last_index, added_time }
            icon.png       图标（favicon 或主域前两字母生成）
        bilibili.com/
            ...

host 作为文件夹名时，Windows 非法字符会被替换成 "_"；
info.json 里存原始 host。
"""

import os
import re
import json
import time
import shutil

import apppaths

FIXED_DIR = os.path.join(apppaths.APP_DIR, "fixed")

MAX_PINNED = 24

_ILLEGAL = r'[\\/:*?"<>|]'


def _normalize(host):
    """把 host 归一为主域。所有 API 入口都过它。"""
    if not host:
        return ""
    h = host.strip().lower()
    if h.startswith("www."):
        h = h[4:]
    parts = h.split(".")
    if len(parts) <= 2:
        return h
    return ".".join(parts[-2:])


def _safe_name(host):
    if not host:
        return "_"
    s = re.sub(_ILLEGAL, "_", host)
    s = s.strip().strip(".")
    return s or "_"


def _ensure_dir():
    os.makedirs(FIXED_DIR, exist_ok=True)


def _host_dir(host):
    return os.path.join(FIXED_DIR, _safe_name(host))


def _info_path(host):
    return os.path.join(_host_dir(host), "info.json")


def _icon_path(host):
    return os.path.join(_host_dir(host), "icon.png")


# ======================================================================
# 读
# ======================================================================
def load_one(host):
    """读一个固定项。返回 dict 或 None。损坏抛 ValueError。"""
    host = _normalize(host)
    if not host:
        return None
    path = _info_path(host)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"固定项 {host} 的 info.json 损坏：{e}")
    if not isinstance(data, dict):
        raise ValueError(f"固定项 {host} 的 info.json 格式不对")
    return {
        "host": data.get("host", host),
        "hosts": list(data.get("hosts", [])),
        "popup_urls": list(data.get("popup_urls", [])),
        "last_index": int(data.get("last_index", -1)),
        "added_time": float(data.get("added_time", 0)),
        "complete_notify": bool(data.get("complete_notify", False)),
    }


def load_all():
    """读全部固定项。返回 (items, broken)。

    items 按 added_time 升序；broken 是损坏 host 列表。
    """
    _ensure_dir()
    items = []
    broken = []
    try:
        names = os.listdir(FIXED_DIR)
    except Exception:
        return [], []

    for name in names:
        full = os.path.join(FIXED_DIR, name)
        if not os.path.isdir(full):
            continue
        info = os.path.join(full, "info.json")
        if not os.path.isfile(info):
            broken.append(name)
            continue
        try:
            with open(info, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("not dict")
        except Exception:
            broken.append(name)
            continue

        items.append({
            "host": data.get("host", name),
            "hosts": list(data.get("hosts", [])),
            "popup_urls": list(data.get("popup_urls", [])),
            "last_index": int(data.get("last_index", -1)),
            "added_time": float(data.get("added_time", 0)),
            "complete_notify": bool(data.get("complete_notify", False)),
        })

    items.sort(key=lambda x: x.get("added_time", 0))
    return items, broken


def count():
    items, _ = load_all()
    return len(items)


def is_pinned(host):
    host = _normalize(host)
    if not host:
        return False
    return os.path.isfile(_info_path(host))


# ======================================================================
# 写
# ======================================================================
def add(host, hosts=None, popup_urls=None, last_index=-1, added_time=None,
        complete_notify=False):
    """新增固定项。已存在则覆盖。超 24 返回 False。"""
    host = _normalize(host)
    if not host:
        return False
    if not is_pinned(host) and count() >= MAX_PINNED:
        return False

    d = _host_dir(host)
    os.makedirs(d, exist_ok=True)

    data = {
        "host": host,
        "hosts": list(hosts or [host]),
        "popup_urls": list(popup_urls or []),
        "last_index": int(last_index),
        "added_time": float(added_time if added_time else time.time()),
        "complete_notify": bool(complete_notify),
    }
    try:
        with open(_info_path(host), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("[pinned] 写入失败:", e)
        return False


def save_one(host, hosts=None, popup_urls=None, last_index=None,
             complete_notify=None):
    """更新固定项字段（只更新传进来的）。不新建。"""
    host = _normalize(host)
    if not host:
        return False
    cur = load_one(host)
    if cur is None:
        return False
    if hosts is not None:
        cur["hosts"] = list(hosts)
    if popup_urls is not None:
        cur["popup_urls"] = list(popup_urls)
    if last_index is not None:
        cur["last_index"] = int(last_index)
    if complete_notify is not None:
        cur["complete_notify"] = bool(complete_notify)

    try:
        with open(_info_path(host), "w", encoding="utf-8") as f:
            json.dump(cur, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("[pinned] 更新失败:", e)
        return False


def remove(host):
    host = _normalize(host)
    if not host:
        return False
    d = _host_dir(host)
    if not os.path.isdir(d):
        return False
    try:
        shutil.rmtree(d, ignore_errors=True)
        return True
    except Exception as e:
        print("[pinned] 删除失败:", e)
        return False


# ======================================================================
# 图标
# ======================================================================
def save_icon(host, pixmap):
    host = _normalize(host)
    if not host or pixmap is None or pixmap.isNull():
        return False
    d = _host_dir(host)
    if not os.path.isdir(d):
        return False
    try:
        return bool(pixmap.save(_icon_path(host), "PNG"))
    except Exception as e:
        print("[pinned] 图标保存失败:", e)
        return False


def load_icon(host):
    from PyQt6.QtGui import QPixmap
    host = _normalize(host)
    if not host:
        return None
    p = _icon_path(host)
    if not os.path.isfile(p):
        return None
    pm = QPixmap(p)
    if pm.isNull():
        return None
    return pm