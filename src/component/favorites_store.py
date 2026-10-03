# -*- coding: utf-8 -*-
"""收藏存储：读写项目根目录下的 favorites.json。

结构：
    [
        {"url": "https://...", "title": "页面标题", "time": 1234567890.0},
        ...
    ]

最新收藏在前。
"""

import os
import json
import time

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "favorites.json")


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
    except Exception as e:
        print("[favorites] 存失败:", e)


def _norm_url(url):
    """规范化 URL 用于比较：去 query + fragment。"""
    if not url:
        return ""
    try:
        from urllib.parse import urlsplit, urlunsplit
        parts = urlsplit(url)
        return urlunsplit((
            parts.scheme, parts.netloc, parts.path,
            "", "",
        ))
    except Exception:
        return url


# ======================================================================
# 对外接口
# ======================================================================
def load_all():
    """读全部收藏。返回 list[dict]，最新在前。"""
    return _load()


def is_favorited(url):
    """判断 URL 是否已收藏（精确字符串匹配）。"""
    if not url:
        return False
    for it in _load():
        if isinstance(it, dict):
            if it.get("url", "") == url:
                return True
    return False


def add(url, title=""):
    """新增收藏。已存在则更新 title。返回是否新增。"""
    if not url:
        return False

    data = _load()

    for it in data:
        if isinstance(it, dict) and it.get("url", "") == url:
            # 已存在 → 只更新 title
            if title:
                it["title"] = title
            _save(data)
            return False

    data.insert(0, {
        "url": url,
        "title": title or url,
        "time": time.time(),
    })
    _save(data)
    return True


def remove(url):
    """按 URL 删除（精确匹配）。成功返回 True。"""
    if not url:
        return False

    data = _load()
    new_list = []
    removed = False
    for it in data:
        if isinstance(it, dict) and it.get("url", "") == url:
            removed = True
            continue
        new_list.append(it)

    if not removed:
        return False
    _save(new_list)
    return True


def clear():
    _save([])