# -*- coding: utf-8 -*-
"""设置后端接口。

读写 settings.json。
分两部分：
  * windows.*：每个窗口的主题、背景等（已存在）
  * env.*：环境级设置（WebView2 重建才生效）

env 段结构：
    {
        "language": "zh-CN",
        "user_agent": "",
        "proxy": "",
        "incognito": false,
        "user_data_folder": "",
        "download_dir": "",
        "download_notify": false,
        "scan_downloads": true,
        "js_enabled": true,
        "context_menu": false,
        "hotkeys": false,
        "devtools": false,
        "autofill": false,
        "password_autosave": false,
        "tracking_prevention": true,
        "tracking_level": 1,
        "smartscreen": true,
        "block_third_party_cookies": false,
        "insecure_content_allowed": false,
        "permission_camera": 0,
        "permission_mic": 0,
        "permission_geo": 0,
        "permission_notify": 0,
        "block_redirect": false,
        "block_popup": true,
        "block_ad": false,
        "save_cookie": true,
        "save_history": true,
        "history_days": 30,
        "whitelist": []
    }
"""

import os
import json

import apppaths


SETTINGS_PATH = os.path.join(apppaths.APP_DIR, "settings.json")


_DEFAULT_ENV = {
    "language": "zh-CN",
    "user_agent": "",
    "proxy": "",
    "incognito": False,
    "user_data_folder": "",
    "download_dir": "",
    "download_notify": False,
    "scan_downloads": True,
    "js_enabled": True,
    "context_menu": False,
    "hotkeys": False,
    "devtools": False,
    "autofill": False,
    "password_autosave": False,
    "tracking_prevention": True,
    "tracking_level": 1,
    "smartscreen": True,
    "block_third_party_cookies": False,
    "insecure_content_allowed": False,
    "permission_camera": 0,
    "permission_mic": 0,
    "permission_geo": 0,
    "permission_notify": 0,
    "block_redirect": False,
    "block_popup": True,
    "block_ad": False,
    "save_cookie": True,
    "save_history": True,
    "history_days": 30,
    "whitelist": [],
}


def _load_all():
    try:
        if os.path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _save_all(data):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _load_env():
    data = _load_all()
    env = data.get("env", {})
    if not isinstance(env, dict):
        env = {}
    out = dict(_DEFAULT_ENV)
    out.update(env)
    return out


def _save_env(env):
    data = _load_all()
    data["env"] = env
    _save_all(data)


class SettingsBackend:
    def __init__(self, web_view=None):
        self._web_view = web_view

    # ---------------- 语言 ----------------
    def get_language(self):
        return str(_load_env().get("language", "zh-CN"))

    def set_language(self, code):
        if not code:
            return
        env = _load_env()
        env["language"] = str(code)
        _save_env(env)

    # ---------------- 常规 ----------------
    def get_js_enabled(self):
        return bool(_load_env().get("js_enabled", True))

    def set_js_enabled(self, on):
        env = _load_env()
        env["js_enabled"] = bool(on)
        _save_env(env)

    def get_context_menu_enabled(self):
        return bool(_load_env().get("context_menu", False))

    def set_context_menu_enabled(self, on):
        env = _load_env()
        env["context_menu"] = bool(on)
        _save_env(env)

    def get_hotkeys_enabled(self):
        return bool(_load_env().get("hotkeys", False))

    def set_hotkeys_enabled(self, on):
        env = _load_env()
        env["hotkeys"] = bool(on)
        _save_env(env)

    def get_devtools_enabled(self):
        return bool(_load_env().get("devtools", False))

    def set_devtools_enabled(self, on):
        env = _load_env()
        env["devtools"] = bool(on)
        _save_env(env)

    def get_autofill_enabled(self):
        return bool(_load_env().get("autofill", False))

    def set_autofill_enabled(self, on):
        env = _load_env()
        env["autofill"] = bool(on)
        _save_env(env)

    def get_password_autosave_enabled(self):
        return bool(_load_env().get("password_autosave", False))

    def set_password_autosave_enabled(self, on):
        env = _load_env()
        env["password_autosave"] = bool(on)
        _save_env(env)

    # ---------------- 隐私 ----------------
    def get_tracking_prevention(self):
        return bool(_load_env().get("tracking_prevention", True))

    def set_tracking_prevention(self, on):
        env = _load_env()
        env["tracking_prevention"] = bool(on)
        _save_env(env)

    def get_tracking_level(self):
        return int(_load_env().get("tracking_level", 1))

    def set_tracking_level(self, level):
        env = _load_env()
        env["tracking_level"] = int(level)
        _save_env(env)

    def get_smartscreen(self):
        return bool(_load_env().get("smartscreen", True))

    def set_smartscreen(self, on):
        env = _load_env()
        env["smartscreen"] = bool(on)
        _save_env(env)

    def get_block_third_party_cookies(self):
        return bool(_load_env().get("block_third_party_cookies", False))

    def set_block_third_party_cookies(self, on):
        env = _load_env()
        env["block_third_party_cookies"] = bool(on)
        _save_env(env)

    def get_user_agent(self):
        return str(_load_env().get("user_agent", ""))

    def set_user_agent(self, ua):
        env = _load_env()
        env["user_agent"] = str(ua)
        _save_env(env)

    def get_block_redirect(self):
        return bool(_load_env().get("block_redirect", False))

    def set_block_redirect(self, on):
        env = _load_env()
        env["block_redirect"] = bool(on)
        _save_env(env)

    def get_block_popup(self):
        return bool(_load_env().get("block_popup", True))

    def set_block_popup(self, on):
        env = _load_env()
        env["block_popup"] = bool(on)
        _save_env(env)

    def get_block_ad(self):
        return bool(_load_env().get("block_ad", False))

    def set_block_ad(self, on):
        env = _load_env()
        env["block_ad"] = bool(on)
        _save_env(env)

    # ---------------- 安全 ----------------
    def get_scan_downloads(self):
        return bool(_load_env().get("scan_downloads", True))

    def set_scan_downloads(self, on):
        env = _load_env()
        env["scan_downloads"] = bool(on)
        _save_env(env)

    def get_permission(self, kind):
        env = _load_env()
        key = f"permission_{kind}"
        return int(env.get(key, 0))

    def set_permission(self, kind, value):
        env = _load_env()
        key = f"permission_{kind}"
        env[key] = int(value)
        _save_env(env)

    def get_insecure_content_allowed(self):
        return bool(_load_env().get("insecure_content_allowed", False))

    def set_insecure_content_allowed(self, on):
        env = _load_env()
        env["insecure_content_allowed"] = bool(on)
        _save_env(env)

    # ---------------- 历史 ----------------
    def get_save_cookie(self):
        return bool(_load_env().get("save_cookie", True))

    def set_save_cookie(self, on):
        env = _load_env()
        env["save_cookie"] = bool(on)
        _save_env(env)

    def get_save_history(self):
        return bool(_load_env().get("save_history", True))

    def set_save_history(self, on):
        env = _load_env()
        env["save_history"] = bool(on)
        _save_env(env)

    def get_history_days(self):
        return int(_load_env().get("history_days", 30))

    def set_history_days(self, days):
        env = _load_env()
        env["history_days"] = int(days)
        _save_env(env)

    def get_whitelist(self):
        wl = _load_env().get("whitelist", [])
        if not isinstance(wl, list):
            return []
        return wl

    def set_whitelist(self, wl):
        env = _load_env()
        env["whitelist"] = list(wl or [])
        _save_env(env)

    # ---------------- 下载 ----------------
    def get_download_dir(self):
        return str(_load_env().get("download_dir", ""))

    def set_download_dir(self, path):
        env = _load_env()
        env["download_dir"] = str(path)
        _save_env(env)

    def get_download_notify(self):
        return bool(_load_env().get("download_notify", False))

    def set_download_notify(self, on):
        env = _load_env()
        env["download_notify"] = bool(on)
        _save_env(env)

    # ---------------- 环境级 ----------------
    def get_incognito(self):
        return bool(_load_env().get("incognito", False))

    def set_incognito(self, on):
        env = _load_env()
        env["incognito"] = bool(on)
        _save_env(env)

    def get_proxy(self):
        return str(_load_env().get("proxy", ""))

    def set_proxy(self, proxy):
        env = _load_env()
        env["proxy"] = str(proxy)
        _save_env(env)

    def get_user_data_folder(self, window_id=None):
        """返回 WebView2 的用户数据目录。

        **所有普通窗口共用同一份 profile**（userdata/profile）。

        为什么不再按窗口 id 分目录（原实现是 userdata/df-0、df-1、df-2…）：
            profile 决定 Cookie / localStorage / 登录态。按窗口 id 分目录时，
            同一个站点在不同窗口里就是互不相干的会话 —— 固定项点开的窗口
            每次拿到新的 id（df-3、df-4…），等于每次都开一份全新的空 profile，
            表现为"关掉窗口再打开就要重新登录"（deepseek、bilibili 都会这样）。

            浏览器的正常语义是 Cookie 跟着**站点**走、不跟窗口走，所以改成共用一份。

        无痕的隔离不靠这里：incognito_window.py 根本不传 user_data_folder。

        window_id 参数保留只为兼容调用方，不再参与路径计算。
        """
        base = str(_load_env().get("user_data_folder", ""))
        if not base:
            base = os.path.join(apppaths.APP_DIR, "userdata")

        base = os.path.join(base, "profile")

        try:
            os.makedirs(base, exist_ok=True)
        except Exception:
            pass
        return base

    def set_user_data_folder(self, path):
        env = _load_env()
        env["user_data_folder"] = str(path)
        _save_env(env)

    def get_global_user_agent(self):
        return self.get_user_agent()

    def set_global_user_agent(self, ua):
        self.set_user_agent(ua)

    def restart_environment(self):
        pass

    # ---------------- 外观 ----------------
    def get_theme_color(self):
        return "#d0d0d0"

    def set_theme_color(self, color):
        pass

    def get_background_image(self):
        return ""

    def set_background_image(self, path):
        pass

    def get_radius(self):
        return 12

    def set_radius(self, r):
        pass