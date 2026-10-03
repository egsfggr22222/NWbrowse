# -*- coding: utf-8 -*-
"""搜索引擎存储：读写项目根目录下的 search_engines.json。

结构：
    {
        "engines": [
            {"abbr": "BI", "url": "https://www.bing.com/search?q=%s"},
            {"abbr": "GO", "url": "https://www.google.com/search?q=%s"},
            {"abbr": "BA", "url": "https://www.baidu.com/s?wd=%s"}
        ]
    }

* abbr：图标缩写（2 个大写字母），用户加的引擎自动从 url 主域生成
* url：含 %s 占位符的搜索 URL

首次访问时，若文件不存在，自动写入预置 3 个。
"""

import os
import re
import json
from urllib.parse import urlparse, quote_plus

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "search_engines.json")


# ======================================================================
# 预置
# ======================================================================
DEFAULT_ENGINES = [
    {"abbr": "BI", "url": "https://www.bing.com/search?q=%s"},
    {"abbr": "GO", "url": "https://www.google.com/search?q=%s"},
    {"abbr": "BA", "url": "https://www.baidu.com/s?wd=%s"},
]


# ======================================================================
# 底层读写
# ======================================================================
def _load_raw():
    """读文件。不存在返回 None；损坏返回 None。"""
    if not os.path.isfile(STORE_PATH):
        return None
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return None


def _save_raw(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[engines] 存失败:", e)


def _ensure_file():
    """确保文件存在。不存在就写预置。"""
    if os.path.isfile(STORE_PATH):
        return
    _save_raw({"engines": [dict(e) for e in DEFAULT_ENGINES]})


# ======================================================================
# 对外接口
# ======================================================================
def load_all():
    """读全部引擎。返回 list[dict]，每项 {"abbr", "url"}。"""
    _ensure_file()
    data = _load_raw()
    if not isinstance(data, dict):
        return [dict(e) for e in DEFAULT_ENGINES]

    engines = data.get("engines")
    if not isinstance(engines, list):
        return [dict(e) for e in DEFAULT_ENGINES]

    out = []
    for it in engines:
        if not isinstance(it, dict):
            continue
        url = it.get("url", "")
        abbr = it.get("abbr", "") or _abbr_from_url(url)
        if not url or "%s" not in url:
            continue
        out.append({"abbr": abbr, "url": url})
    return out


def add_engine(url):
    """新增一个引擎。url 必须含 %s 且 http(s)。成功返回 abbr，失败返回 None。"""
    url = (url or "").strip()
    if not url:
        return None
    if "%s" not in url:
        return None
    if not url.startswith(("http://", "https://")):
        return None

    _ensure_file()
    data = _load_raw()
    if not isinstance(data, dict):
        data = {"engines": []}
    engines = data.get("engines")
    if not isinstance(engines, list):
        engines = []

    # 同 url 已存在 → 直接返回
    for it in engines:
        if isinstance(it, dict) and it.get("url") == url:
            return it.get("abbr") or _abbr_from_url(url)

    abbr = _abbr_from_url(url)
    engines.append({"abbr": abbr, "url": url})
    data["engines"] = engines
    _save_raw(data)
    return abbr


def remove_engine(url):
    """按 url 删除。成功返回 True。"""
    url = (url or "").strip()
    if not url:
        return False
    _ensure_file()
    data = _load_raw()
    if not isinstance(data, dict):
        return False
    engines = data.get("engines")
    if not isinstance(engines, list):
        return False

    new_list = []
    removed = False
    for it in engines:
        if isinstance(it, dict) and it.get("url") == url:
            removed = True
            continue
        new_list.append(it)

    if not removed:
        return False
    data["engines"] = new_list
    _save_raw(data)
    return True


def build_search_url(engine, query):
    """把 query 拼成搜索 URL。engine 是 dict；query 是用户输入。"""
    if not engine or not isinstance(engine, dict):
        return ""
    tpl = engine.get("url", "")
    if not tpl or "%s" not in tpl:
        return ""
    q = quote_plus(query or "")
    try:
        return tpl % q
    except Exception:
        return ""


# ======================================================================
# 缩写生成
# ======================================================================
def _abbr_from_url(url):
    """从 URL 的主域取前两字母，大写。失败返回 '??'。"""
    try:
        host = (urlparse(url).hostname or "").lower()
        if not host:
            return "??"
        if host.startswith("www."):
            host = host[4:]
        parts = host.split(".")
        if len(parts) >= 2:
            label = parts[-2]
        else:
            label = host
        label = re.sub(r"[^a-zA-Z]", "", label)
        if not label:
            return "??"
        if len(label) == 1:
            return label.upper()
        return label[:2].upper()
    except Exception:
        return "??"