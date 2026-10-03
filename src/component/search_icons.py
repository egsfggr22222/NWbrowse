# -*- coding: utf-8 -*-
"""搜索引擎图标存储：把 favicon 抓到 userdata/search_icons/<主域>.png。

* 读：load_icon(engine) → QPixmap 或 None
* 抓：fetch_icon(engine_url, callback) → 异步抓，抓到存盘
* 抓取源：https://<主域>/favicon.ico

抓到 ≤64 原图存；>64 缩到 64。
"""

import os
import re
from urllib.parse import urlparse

from loader import *

import apppaths

ICON_DIR = os.path.join(apppaths.APP_DIR, "userdata", "search_icons")

MAX_SIZE = 64
_ILLEGAL = r'[\\/:*?"<>|]'


def _ensure_dir():
    os.makedirs(ICON_DIR, exist_ok=True)


def _root_host(url):
    """从 URL 取主域，如 bing.com。"""
    try:
        host = (urlparse(url).hostname or "").lower()
        if not host:
            return ""
        if host.startswith("www."):
            host = host[4:]
        parts = host.split(".")
        if len(parts) <= 2:
            return host
        return ".".join(parts[-2:])
    except Exception:
        return ""


def _host_of_engine(engine):
    if not isinstance(engine, dict):
        return ""
    return _root_host(engine.get("url", ""))


def _safe_name(host):
    if not host:
        return "_"
    s = re.sub(_ILLEGAL, "_", host)
    return s.strip().strip(".") or "_"


def _icon_path(host):
    return os.path.join(ICON_DIR, _safe_name(host) + ".png")


# ======================================================================
# 读
# ======================================================================
def load_icon(engine):
    """读本地图标。返回 QPixmap 或 None。"""
    host = _host_of_engine(engine)
    if not host:
        return None
    path = _icon_path(host)
    if not os.path.isfile(path):
        return None
    pm = QPixmap(path)
    if pm.isNull():
        return None
    return pm


# ======================================================================
# 写
# ======================================================================
def save_icon(engine, pixmap):
    """把 pixmap 存盘。超过 64 缩到 64。返回是否成功。"""
    host = _host_of_engine(engine)
    if not host or pixmap is None or pixmap.isNull():
        return False

    _ensure_dir()

    w = pixmap.width()
    h = pixmap.height()
    if max(w, h) > MAX_SIZE:
        pixmap = pixmap.scaled(
            MAX_SIZE, MAX_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    try:
        return bool(pixmap.save(_icon_path(host), "PNG"))
    except Exception as e:
        print("[engine_icon] 存盘失败:", e)
        return False


# ======================================================================
# 抓
# ======================================================================
_nam = None


def _get_nam(parent=None):
    global _nam
    if _nam is None:
        from PyQt6.QtNetwork import QNetworkAccessManager
        _nam = QNetworkAccessManager(parent)
    return _nam


def fetch_icon(engine, callback=None, parent=None):
    """异步抓 favicon。

    * engine：dict {"abbr", "url"}
    * callback：抓到后回调 callback(engine, pixmap_or_None)
                pixmap 为 None 表示失败
    * parent：QNetworkAccessManager 的 parent（一般是窗口）
    """
    host = _host_of_engine(engine)
    if not host:
        if callback:
            try:
                callback(engine, None)
            except Exception:
                pass
        return

    # 本地已有 → 直接回调
    pm = load_icon(engine)
    if pm is not None and not pm.isNull():
        if callback:
            try:
                callback(engine, pm)
            except Exception:
                pass
        return

    scheme = "https"
    try:
        p = urlparse(engine.get("url", ""))
        if p.scheme:
            scheme = p.scheme
    except Exception:
        pass

    fav_url = f"{scheme}://{host}/favicon.ico"

    from PyQt6.QtNetwork import QNetworkRequest
    nam = _get_nam(parent)
    reply = nam.get(QNetworkRequest(QUrl(fav_url)))

    def _done():
        try:
            data = bytes(reply.readAll())
            pm = QPixmap()
            pm.loadFromData(data)
            if pm.isNull():
                if callback:
                    try:
                        callback(engine, None)
                    except Exception:
                        pass
                return

            # 存盘
            save_icon(engine, pm)

            # 重新读盘，确保拿到的是缩放后的版本
            pm2 = load_icon(engine) or pm
            if callback:
                try:
                    callback(engine, pm2)
                except Exception:
                    pass
        except Exception as e:
            print("[engine_icon] 抓取回调异常:", e)
            if callback:
                try:
                    callback(engine, None)
                except Exception:
                    pass
        finally:
            reply.deleteLater()

    reply.finished.connect(_done)


def fetch_all(engines, on_one=None, parent=None):
    """批量抓。每个抓完调 on_one(engine, pixmap_or_None)。

    串行（前一个抓完再抓下一个），避免同时开太多连接。
    """
    items = list(engines or [])

    def _next(idx):
        if idx >= len(items):
            return
        eng = items[idx]

        def _cb(e, pm):
            if on_one:
                try:
                    on_one(e, pm)
                except Exception:
                    pass
            # 延迟 50ms 再抓下一个
            QTimer.singleShot(50, lambda: _next(idx + 1))

        fetch_icon(eng, _cb, parent)

    _next(0)