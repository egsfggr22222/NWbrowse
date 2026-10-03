# -*- coding: utf-8 -*-
"""完成提醒的按站点开关（独立存储，不依赖固定项）。

背景
----
「完成提醒」= DOM 监控：IDLE 态下 new 簇占多数 → 进入 W 态；
W 态下 5 秒无新增 → 自然死亡 → 响铃 + 强制窗口置顶。

原先这个开关的状态只写在**固定项**里，而且：
  * 保存：`if host and pinned_store.is_pinned(host)` —— 没固定就不写盘
  * 恢复：读固定项的那段代码嵌在 `if is_pinned(...)` 分支里面

后果：对**没有固定**的站点打开「完成提醒」，当次会话有效，
关掉窗口就忘了，下次打开又变回关 —— 看起来像"功能丢了"。

现在单独存一份 userdata/complete_notify.json：
    { "bilibili.com": true, "bing.com": false }

固定项里的 complete_notify 仍然保留（兼容旧数据），两边**取或**。
"""

import json
import os

import apppaths

STORE_PATH = os.path.join(apppaths.APP_DIR, "userdata", "complete_notify.json")


def _normalize(host):
    """归一到主域。既接受 bilibili.com，也容忍传进来的是完整 URL。"""
    if not host:
        return ""
    h = str(host).strip().lower()
    if "//" in h:                       # https://www.bilibili.com/x -> www.bilibili.com/x
        h = h.split("//", 1)[1]
    for sep in ("/", "?", "#"):         # 去掉路径、查询、片段
        h = h.split(sep, 1)[0]
    h = h.split("@")[-1].split(":")[0]  # 去掉 user@ 和端口
    h = h.strip(".")
    if h.startswith("www."):
        h = h[4:]
    parts = h.split(".")
    if len(parts) <= 2:
        return h
    return ".".join(parts[-2:])


def load():
    """读全部记录。返回 {host: bool}。文件不存在或损坏都返回空。"""
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return {str(k): bool(v) for k, v in data.items()}
    except Exception:
        return {}


def get(host):
    """查某个站点的开关。没有记录返回 False。"""
    return bool(load().get(_normalize(host), False))


def set(host, on):  # noqa: A001 - 保持与 pinned_store 风格一致的命名
    """写某个站点的开关。返回是否成功。"""
    h = _normalize(host)
    if not h:
        return False
    data = load()
    if on:
        data[h] = True
    else:
        data.pop(h, None)
    try:
        os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
        tmp = STORE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, STORE_PATH)
        print("[notify_store] %s = %s" % (h, bool(on)))
        return True
    except Exception as e:
        print("[notify_store] 写盘失败:", e)
        return False


def is_on(host):
    """带旧数据兼容：独立存储或固定项里任一为真，就认为开着。"""
    if get(host):
        return True
    try:
        import pinned_store
        item = pinned_store.load_one(_normalize(host))
        return bool(item and item.get("complete_notify"))
    except Exception:
        return False
