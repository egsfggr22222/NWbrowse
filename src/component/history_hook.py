# -*- coding: utf-8 -*-
"""历史记录钩子：具体逻辑在这。

由 window.History.record() 转发调用。
"""


def record(window, title, url=""):
    """记一条历史。window 是 RoundedWindow 实例。

    无痕窗口、save_history 关、非 http(s) 页面 → 不记。
    """
    # 无痕窗口不写
    if type(window).__name__ == "IncognitoWindow":
        return

    if not title:
        return

    url = url or getattr(window, "_current_url", "") or ""
    if not url.startswith(("http://", "https://")):
        return

    # save_history 关掉就不写
    try:
        from settings_backend import SettingsBackend
        if not SettingsBackend().get_save_history():
            return
    except Exception:
        pass

    # 白名单跳过
    try:
        from settings_backend import SettingsBackend
        wl = SettingsBackend().get_whitelist()
        host = _host_of(url)
        for entry in wl:
            if entry.get("host", "") == host and entry.get("no_history"):
                return
    except Exception:
        pass

    try:
        from history_store import add_history
        add_history(url, title, max_days=30)
    except Exception as e:
        print("[history_hook] 写历史失败:", e)


def _host_of(url):
    try:
        from urllib.parse import urlparse
        h = (urlparse(url).hostname or "").lower()
        if h.startswith("www."):
            h = h[4:]
        return h
    except Exception:
        return ""