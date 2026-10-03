# -*- coding: utf-8 -*-
"""UI 文字国际化。

只管自己画的 UI。WebView2 内核自带的文字（右键菜单、错误页）
跟随系统语言，不在这个范围内。

语言文件放 component/i18n/<code>.json，结构：
    {
        "_meta": {"code": "zh-CN", "name": "简体中文"},
        "key1": "文字1",
        "key2": "文字2"
    }

切换语言：
    load("en-US")  # 加载并触发所有 on_change 回调
"""

import os
import json
import shutil

import apppaths


I18N_DIR = os.path.join(apppaths.COMPONENT_DIR, "i18n")

DEFAULT_CODE = "zh-CN"

_current_code = DEFAULT_CODE
_current_data = {}

# 语言变化时的回调列表
_listeners = []


# ======================================================================
# 校验
# ======================================================================
def validate_language(data):
    """校验语言 JSON 结构。不合法抛 ValueError。"""
    if not isinstance(data, dict):
        raise ValueError("语言文件必须是一个 JSON 对象")

    meta = data.get("_meta")
    if not isinstance(meta, dict):
        raise ValueError("缺少 _meta 字段")

    code = meta.get("code")
    if not isinstance(code, str) or not code.strip():
        raise ValueError("_meta.code 必须是非空字符串")

    name = meta.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("_meta.name 必须是非空字符串")

    keys = [k for k in data.keys() if k != "_meta"]
    if not keys:
        raise ValueError("语言文件里没有任何翻译条目")

    for k in keys:
        if not isinstance(data[k], str):
            raise ValueError(f"键 {k!r} 的值必须是字符串")

    return code.strip()


# ======================================================================
# 加载 / 切换
# ======================================================================
def _path(code):
    return os.path.join(I18N_DIR, code + ".json")


def _notify():
    """通知所有监听者。"""
    print(f"[i18n] _notify 触发，listeners={len(_listeners)}")
    for fn in list(_listeners):
        try:
            fn()
        except Exception as e:
            print("[i18n] on_change 回调异常:", e)


def load(code, notify=True):
    """加载指定语言。

    code 加载失败就回退到默认。
    加载成功后，如果 notify=True，触发所有 on_change 回调。
    """
    global _current_code, _current_data

    data = None
    try:
        with open(_path(code), "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[i18n] 加载 {code} 失败: {e}")
        data = None

    if not isinstance(data, dict):
        if code != DEFAULT_CODE:
            try:
                with open(_path(DEFAULT_CODE), "r", encoding="utf-8") as f:
                    data = json.load(f)
                code = DEFAULT_CODE
            except Exception:
                data = {}
        else:
            data = {}

    _current_data = data if isinstance(data, dict) else {}
    _current_code = code

    print(f"[i18n] load 完成 code={code} keys={len(_current_data)}")

    if notify:
        _notify()


def current_code():
    return _current_code


def t(key, default=""):
    """取文字。找不到就返回 default 或 key 本身。"""
    if not _current_data:
        load(_current_code, notify=False)
    v = _current_data.get(key)
    if v is None:
        print(f"[i18n] 缺失 key: {key}")
        return default or key
    return v


def on_change(fn):
    """注册语言变化回调。"""
    if fn not in _listeners:
        _listeners.append(fn)
        print(f"[i18n] on_change 注册: {fn}, 当前 listeners={len(_listeners)}")


def off_change(fn):
    """取消注册。"""
    if fn in _listeners:
        _listeners.remove(fn)
        print(f"[i18n] on_change 注销: {fn}, 当前 listeners={len(_listeners)}")


# ======================================================================
# 列出 / 导入 / 导出
# ======================================================================
def list_languages():
    """列出 i18n 目录下所有语言文件，返回 [(code, name), ...]。"""
    out = []
    if not os.path.isdir(I18N_DIR):
        return out

    for name in os.listdir(I18N_DIR):
        if not name.endswith(".json"):
            continue
        path = os.path.join(I18N_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        meta = data.get("_meta", {}) if isinstance(data, dict) else {}
        code = meta.get("code", "") or os.path.splitext(name)[0]
        label = meta.get("name", "") or code
        out.append((code, label))

    out.sort()
    return out


def import_language(src_path):
    """导入用户拖进来的语言文件。

    校验格式，通过后拷到 i18n/<code>.json。
    返回 (code, name)。不合法抛 ValueError。
    """
    if not os.path.isfile(src_path):
        raise ValueError("不是有效的文件")

    try:
        with open(src_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"不是合法的 JSON 文件：{e}")

    code = validate_language(data)
    name = data["_meta"]["name"]

    if code == DEFAULT_CODE:
        raise ValueError(f"不能覆盖默认语言 {DEFAULT_CODE}")

    os.makedirs(I18N_DIR, exist_ok=True)
    dst = _path(code)

    try:
        shutil.copyfile(src_path, dst)
    except Exception as e:
        raise ValueError(f"写入语言文件失败：{e}")

    return code, name


def export_language(code, dst_path):
    """把指定语言文件导出到 dst_path。返回是否成功。"""
    src = _path(code)
    if not os.path.isfile(src):
        return False
    try:
        shutil.copyfile(src, dst_path)
        return True
    except Exception:
        return False