# -*- coding: utf-8 -*-
"""DOM 节点监控：new / lazy 簇状态机。

规则（全部在 JS 里判定）：
  - 有用户操作（滚动、点击、键盘、URL 变化、加载）后 1000ms 内的插入 → lazy
  - 没有用户操作时的插入 → new
  - 每 300ms flush 一次，算一条记录
  - 窗口 10 条
  - IDLE 态：new >= 7 → 进入 W 态
  - W 态：lazy >= 7 → 非自然死亡（不提醒）
  - 5s 无新增：
        W 态   → 自然死亡（提醒）
        IDLE 态 → 自然死亡（不提醒）
  - 超时后清空窗口，回 IDLE

JS 通过 ipc.postMessage 上报以下事件：
  cluster_start
  enter_w
  natural_death          ← W 态自然死亡 → 触发 on_over（提醒 + 置顶）
  natural_death_idle
  lazy_death
  dom_added              ← 每次 flush 一条，附带统计数据

Python 侧只做事件接收与分派：
  - natural_death → 调用 on_over()
  - 其他事件     → 打日志
"""

from loader import *


# ======================================================================
# 注入的 JS
# ======================================================================
DOM_ACTIVITY_JS = r"""
(function() {
    if (window.__dom_new_lazy_test) return;
    window.__dom_new_lazy_test = true;

    var USER_ACTION_WINDOW_MS = 1000;
    var WINDOW_SIZE = 10;
    var A_RATIO_NORMAL = 7;
    var LAZY_CANCEL = 7;
    var CLUSTER_GAP_MS = 5000;

    var pending_new = 0;
    var pending_lazy = 0;
    var flush_scheduled = false;

    var window_records = [];
    var in_cluster = false;
    var in_w_state = false;
    var last_record_time = 0;

    var last_action_time = 0;

    function mark_action() {
        last_action_time = performance.now();
    }

    window.addEventListener('scroll', mark_action, true);
    document.addEventListener('click', mark_action, true);
    document.addEventListener('keydown', mark_action, true);
    document.addEventListener('mousedown', mark_action, true);

    var last_url = location.href;
    setInterval(function() {
        if (location.href !== last_url) {
            last_url = location.href;
            mark_action();
        }
    }, 200);

    window.addEventListener('load', mark_action);
    if (document.readyState === 'complete') {
        mark_action();
    }

    function report(msg) {
        try {
            if (window.ipc && window.ipc.postMessage) {
                window.ipc.postMessage(JSON.stringify(msg));
            }
        } catch (e) {}
    }

    function start_cluster() {
        in_cluster = true;
        in_w_state = false;
        window_records = [];
        report({ type: "cluster_start" });
    }

    function finish_cluster(reason) {
        if (!in_cluster) return;
        if (reason === "natural") {
            if (in_w_state) {
                report({ type: "natural_death" });
            } else {
                report({ type: "natural_death_idle" });
            }
        } else if (reason === "lazy") {
            report({ type: "lazy_death" });
        }
        in_cluster = false;
        in_w_state = false;
        window_records = [];
        last_record_time = 0;
    }

    // 5s 超时检查
    setInterval(function() {
        if (!in_cluster) return;
        if (last_record_time === 0) return;
        var gap = performance.now() - last_record_time;
        if (gap >= CLUSTER_GAP_MS) {
            finish_cluster("natural");
        }
    }, 500);

    function schedule_flush() {
        if (flush_scheduled) return;
        flush_scheduled = true;
        setTimeout(function() {
            flush_scheduled = false;
            if (pending_new > 0 || pending_lazy > 0) {
                var source = (pending_new >= pending_lazy) ? "new" : "lazy";
                var count = pending_new + pending_lazy;

                // 开簇
                if (!in_cluster) {
                    start_cluster();
                }

                window_records.push(source);
                if (window_records.length > WINDOW_SIZE) {
                    window_records.shift();
                }
                last_record_time = performance.now();

                var new_count = 0;
                var lazy_count = 0;
                for (var i = 0; i < window_records.length; i++) {
                    if (window_records[i] === "new") new_count++;
                    else if (window_records[i] === "lazy") lazy_count++;
                }

                report({
                    type: "dom_added",
                    source: source,
                    count: count,
                    win: window_records.length,
                    new_count: new_count,
                    lazy_count: lazy_count,
                    in_w: in_w_state,
                });

                if (window_records.length >= WINDOW_SIZE) {
                    if (!in_w_state && new_count >= A_RATIO_NORMAL) {
                        in_w_state = true;
                        report({ type: "enter_w" });
                    } else if (in_w_state && lazy_count >= LAZY_CANCEL) {
                        finish_cluster("lazy");
                    }
                }

                pending_new = 0;
                pending_lazy = 0;
            }
        }, 300);
    }

    function install_dom_observer() {
        var target = document.body;
        if (!target) {
            setTimeout(install_dom_observer, 200);
            return;
        }
        var mo = new MutationObserver(function(mutations) {
            var now = performance.now();
            var is_lazy = (now - last_action_time < USER_ACTION_WINDOW_MS);

            for (var i = 0; i < mutations.length; i++) {
                var m = mutations[i];
                if (m.type !== "childList") continue;
                if (m.addedNodes.length === 0) continue;

                var n = m.addedNodes.length;
                if (is_lazy) {
                    pending_lazy += n;
                } else {
                    pending_new += n;
                }
            }
            if (pending_new > 0 || pending_lazy > 0) {
                schedule_flush();
            }
        });
        mo.observe(target, { childList: true, subtree: true });
        report({ type: "dom_observer_installed" });
    }

    install_dom_observer();
})();
"""


# ======================================================================
# Python 侧监控器
# ======================================================================
class DomActivityMonitor(QObject):
    """接收 JS 状态机上报的事件，分派回调。

    window 必须提供：
      * _on_js_message 里把 type 属于本监控器的事件转发给 feed()
      * 一个回调 on_over（W 态自然死亡时调用，用于提醒 + 置顶）

    用法：
        self._dom_monitor = DomActivityMonitor(self, self._on_dom_over)
        self._dom_monitor.start()
        ...
        self._dom_monitor.feed(data)   # data 是 dict
        self._dom_monitor.stop()
    """

    EVT_CLUSTER_START      = "cluster_start"
    EVT_ENTER_W            = "enter_w"
    EVT_NATURAL_DEATH      = "natural_death"
    EVT_NATURAL_DEATH_IDLE = "natural_death_idle"
    EVT_LAZY_DEATH         = "lazy_death"
    EVT_DOM_ADDED          = "dom_added"

    # 需要转发给 feed 的所有 type
    TYPES = (
        EVT_CLUSTER_START,
        EVT_ENTER_W,
        EVT_NATURAL_DEATH,
        EVT_NATURAL_DEATH_IDLE,
        EVT_LAZY_DEATH,
        EVT_DOM_ADDED,
    )

    def __init__(self, parent, on_over):
        super().__init__(parent)
        self._parent = parent
        self._on_over = on_over
        self._active = False

    def start(self):
        self._active = True
        print("[dom] monitor started")

    def stop(self):
        self._active = False
        print("[dom] monitor stopped")

    def is_active(self):
        return self._active

    def feed(self, data):
        """收到 JS 上报的事件（dict）。"""
        if not self._active:
            return
        if not isinstance(data, dict):
            return

        t = data.get("type")

        if t == self.EVT_CLUSTER_START:
            print("[dom] cluster_start")
            return

        if t == self.EVT_ENTER_W:
            print("[dom] enter_w")
            return

        if t == self.EVT_NATURAL_DEATH:
            print("[dom] natural_death → 提醒 + 置顶")
            try:
                self._on_over()
            except Exception as e:
                import traceback
                print("[dom] on_over 回调异常:")
                traceback.print_exc()
            return

        if t == self.EVT_NATURAL_DEATH_IDLE:
            print("[dom] natural_death_idle（不提醒）")
            return

        if t == self.EVT_LAZY_DEATH:
            print("[dom] lazy_death（不提醒）")
            return

        if t == self.EVT_DOM_ADDED:
            source = data.get("source", "?")
            count = data.get("count", 0)
            win = data.get("win", 0)
            new_c = data.get("new_count", 0)
            lazy_c = data.get("lazy_count", 0)
            in_w = data.get("in_w", False)
            print(f"[dom] [{source}] +{count} win={win} "
                  f"new={new_c} lazy={lazy_c} W={in_w}")
            return