# -*- coding: utf-8 -*-
"""历史记录存储。读写项目根目录下的 history.json。

记录结构：
    [
        {
            "url": "https://...",
            "title": "页面标题",
            "host": "bilibili.com",
            "time": 1790645040.5
        },
        ...
    ]

最新在前。
"""

import os
import json
import time

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "history.json")

MAX_RECORDS = 5000


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


def _host_of(url):
    try:
        from urllib.parse import urlparse
        h = (urlparse(url).hostname or "").lower()
        if h.startswith("www."):
            h = h[4:]
        return h
    except Exception:
        return ""


def add_history(url, title="", max_days=30):
    """新增一条。同 URL 同 title 跳过；同 URL 不同 title 更新。

    max_days > 0 时，写入前删掉超过 max_days 天的记录。
    """
    if not url:
        return
    data = _load()

    # 删超期
    if max_days > 0:
        cutoff = time.time() - max_days * 86400
        data = [r for r in data if r.get("time", 0) >= cutoff]

    # 同 URL 同 title → 跳过（不更新 time）
    for r in data:
        if r.get("url") == url and r.get("title") == title:
            return

    # 同 URL 不同 title → 删旧，插新
    data = [r for r in data if r.get("url") != url]

    data.insert(0, {
        "url": url,
        "title": title or "",
        "host": _host_of(url),
        "time": time.time(),
    })

    if len(data) > MAX_RECORDS:
        data = data[:MAX_RECORDS]

    _save(data)


def load_history(days=0, host="", keyword=""):
    """读记录，按条件过滤。

    days: >0 只取最近 days 天；0 = 不限
    host: 非空只取该主域
    keyword: 非空，title 或 url 任一含该关键词
    返回 list，最新在前。
    """
    data = _load()
    now = time.time()

    if days > 0:
        cutoff = now - days * 86400
        data = [r for r in data if r.get("time", 0) >= cutoff]

    if host:
        data = [r for r in data if r.get("host") == host]

    if keyword:
        kw = keyword.lower()
        data = [
            r for r in data
            if kw in (r.get("title", "") or "").lower()
            or kw in (r.get("url", "") or "").lower()
        ]

    return data


def remove_by_urls(urls):
    """按 URL 列表删除。"""
    if not urls:
        return
    s = set(urls)
    data = _load()
    data = [r for r in data if r.get("url") not in s]
    _save(data)


def clear_all():
    _save([])


def all_hosts():
    """返回出现过的所有主域（去重，排序）。"""
    data = _load()
    hosts = set()
    for r in data:
        h = r.get("host", "")
        if h:
            hosts.add(h)
    return sorted(hosts)