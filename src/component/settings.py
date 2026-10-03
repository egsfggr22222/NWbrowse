# -*- coding: utf-8 -*-
"""读写用户设置：按窗口类型区分配置。

配置结构：
{
    "windows": {
        "default": {
            "theme_color": "#d0d0d0",
            "background_images": [],
            "background_current": ""
        },
        "custom_1": { ... }
    }
}

窗口类型 mode：
    "default"  默认窗口，读写 windows.default
    "search"   搜索引擎窗口，只读 windows.default，不写
    "custom"   个性需求窗口，读写 windows.<id>
"""

import os
import json
from PyQt6.QtGui import QColor

import apppaths


SETTINGS_PATH = os.path.join(apppaths.APP_DIR, "settings.json")

DEFAULT_THEME = "#d0d0d0"

#: 内置资源的路径前缀。
#: 随包发布的背景图用这个占位符引用，例如
#:     "{RES}/assets/backgrounds/spaceship.jpg"
#: 运行时展开成 RES_DIR（源码模式=项目根，打包后=_internal）。
#: 这样 settings.json 里就不必写死绝对路径，换机器 / 换安装位置都不会失效。
RES_TOKEN = "{RES}"


def resolve_path(path):
    """把设置里的路径展开成可用路径。

    * ``{RES}/xxx``  ->  ``<RES_DIR>/xxx``（内置资源，随程序走）
    * 其它           ->  原样返回（用户自己选的绝对路径）
    """
    if not path:
        return ""
    p = str(path)
    if p.startswith(RES_TOKEN):
        rest = p[len(RES_TOKEN):].lstrip("/\\")
        return os.path.join(apppaths.RES_DIR, *rest.split("/"))
    return p


def to_stored_path(path):
    """写回设置时尽量用 ``{RES}`` 记内置资源，避免存绝对路径。"""
    if not path:
        return ""
    try:
        res = os.path.abspath(apppaths.RES_DIR)
        ap = os.path.abspath(str(path))
        if os.path.commonpath([res, ap]) == res:
            rel = os.path.relpath(ap, res).replace("\\", "/")
            return RES_TOKEN + "/" + rel
    except Exception:
        pass
    return str(path)


# ======================================================================
# 底层读写
# ======================================================================
def _default_window_data():
    return {
        "theme_color": DEFAULT_THEME,
        "background_images": [],
        "background_current": "",
    }


def _load_all():
    data = {"windows": {"default": _default_window_data()}}
    try:
        if os.path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                if "windows" in loaded and isinstance(loaded["windows"], dict):
                    data["windows"].update(loaded["windows"])
                else:
                    # 兼容旧版全局配置：把旧字段迁移到 windows.default
                    old = {}
                    for k in ("theme_color", "background_images",
                              "background_current"):
                        if k in loaded:
                            old[k] = loaded[k]
                    old_img = loaded.get("background_image")
                    if old_img and old_img not in old.get("background_images", []):
                        old.setdefault("background_images", []).insert(0, old_img)
                    if old:
                        data["windows"]["default"].update(old)
    except Exception:
        pass

    # 补全 default
    if "default" not in data["windows"]:
        data["windows"]["default"] = _default_window_data()
    else:
        base = _default_window_data()
        base.update(data["windows"]["default"])
        data["windows"]["default"] = base

    # 过滤失效图片路径。
    # 注意：先展开 {RES} 占位符再判断存在性 —— 否则内置背景图会被当成
    # "不存在的路径"直接过滤掉（这正是之前默认背景图丢失的原因之一）。
    for wid, w in data["windows"].items():
        imgs = [p for p in w.get("background_images", [])
                if p and os.path.isfile(resolve_path(p))]
        w["background_images"] = imgs
        cur = w.get("background_current", "")
        if cur and cur not in imgs:
            cur = imgs[0] if imgs else ""
        w["background_current"] = cur

    return data


def _save_all(data):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ======================================================================
# 按窗口读写
# ======================================================================
def _resolve_key(mode, window_id):
    """把 mode + id 映射到 windows 下的 key。"""
    if mode == "default":
        return "default"
    if mode == "search":
        return "default"      # 只读 default
    if mode == "custom":
        return window_id or "default"
    return "default"


def load_window_settings(mode="default", window_id=None):
    """读某个窗口的配置。"""
    key = _resolve_key(mode, window_id)
    data = _load_all()
    w = data["windows"].get(key)
    if w is None:
        # custom 首次启动：复制 default 作为初始
        w = dict(_default_window_data())
        w.update(data["windows"]["default"])
        data["windows"][key] = w
        if mode == "custom":
            _save_all(data)
    return dict(w)


def save_window_settings(mode, window_id, settings):
    """写某个窗口的配置。search 模式不写。"""
    if mode == "search":
        return
    key = _resolve_key(mode, window_id)
    data = _load_all()
    data["windows"][key] = dict(settings)
    _save_all(data)


# ======================================================================
# 兼容旧接口：直接操作 default 窗口
# ======================================================================
def load_theme_color():
    s = load_window_settings("default", "default")
    color = QColor(s.get("theme_color", DEFAULT_THEME))
    if not color.isValid():
        color = QColor(DEFAULT_THEME)
    return color


def save_theme_color(color):
    s = load_window_settings("default", "default")
    s["theme_color"] = QColor(color).name()
    save_window_settings("default", "default", s)


def load_background_image():
    s = load_window_settings("default", "default")
    return s.get("background_current", "")


def load_background_images():
    s = load_window_settings("default", "default")
    return list(s.get("background_images", []))


def save_background_image(path, images=None):
    s = load_window_settings("default", "default")
    if images is not None:
        s["background_images"] = list(images)
    s["background_current"] = path or ""
    save_window_settings("default", "default", s)