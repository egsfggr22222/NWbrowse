# -*- coding: utf-8 -*-
"""网页注入用的字体与滚动条 CSS / JS。

字体通过自定义协议 appfont:// 提供，由 font_scheme_handler 直接读磁盘返回。

跨导航 / SPA 动态 DOM / 内联样式覆盖 的处理：
  * 去重看 document.getElementById('__sb_style')，不用 window 标志；
  * 定时巡检：style 丢了重建；内联 font-family 出现就删掉；
  * CSS 规则不用 inherit，而是直接写完整字体栈 + 覆盖常见元素。

额外：
  * content-visibility 视窗外渲染跳过；
  * 视窗外 <img> 卸载 src，释放解码位图内存，滚回再恢复。
"""

import os

import apppaths

# ----------------------------------------------------------------------
# 路径 / 探测
# ----------------------------------------------------------------------
FONTS_DIR = os.path.join(apppaths.RES_DIR, "assets", "fonts")

FORCE_FILES = {
    400: None,
    500: None,
    700: None,
}

_EXTS = [".woff2", ".ttf", ".otf"]

_WEIGHT_KEYWORDS = {
    400: ["regular", "normal", "book", "400"],
    500: ["medium", "500"],
    700: ["bold", "700"],
}

_FMT_BY_EXT = {
    ".woff2": "woff2",
    ".ttf":   "truetype",
    ".otf":   "opentype",
}

SINGLE_WEIGHT_ONLY = False


def _list_font_files():
    if not os.path.isdir(FONTS_DIR):
        return []
    out = []
    for root, _dirs, files in os.walk(FONTS_DIR):
        for f in files:
            if f.startswith("."):
                continue
            if os.path.splitext(f)[1].lower() in _EXTS:
                out.append(os.path.join(root, f))
    return out


def _pick_file(weight):
    forced = FORCE_FILES.get(weight)
    if forced:
        path = os.path.join(FONTS_DIR, forced)
        if os.path.isfile(path):
            return path

    keywords = _WEIGHT_KEYWORDS[weight]
    candidates = []
    for path in _list_font_files():
        name = os.path.basename(path).lower()
        if "italic" in name or "oblique" in name:
            continue
        for idx, kw in enumerate(keywords):
            if kw in name:
                candidates.append((idx, path))
                break

    if not candidates:
        return None

    def sort_key(item):
        kw_idx, path = item
        ext = os.path.splitext(path)[1].lower()
        ext_rank = _EXTS.index(ext) if ext in _EXTS else 99
        return (kw_idx, ext_rank)

    candidates.sort(key=sort_key)
    return candidates[0][1]


def _font_face(family, weight):
    path = _pick_file(weight)
    if not path:
        print(f"[styles] weight={weight} 未找到字体文件")
        return ""

    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()
    fmt = _FMT_BY_EXT.get(ext, "truetype")
    url = "appfont:///" + name
    return (
        f"@font-face {{ font-family: '{family}'; "
        f"src: url('{url}') format('{fmt}'); "
        f"font-weight: {weight}; font-display: swap; }}"
    )


# ----------------------------------------------------------------------
# 字体 CSS
# ----------------------------------------------------------------------
def _build_font_css():
    family = "MiSans"

    if SINGLE_WEIGHT_ONLY:
        faces = _font_face(family, 400)
    else:
        faces = (
            _font_face(family, 400)
            + _font_face(family, 500)
            + _font_face(family, 700)
        )

    stack = (
        f"'{family}', -apple-system, 'Segoe UI', "
        f"'Microsoft YaHei', 'PingFang SC', sans-serif"
    )

    return f"""
{faces}
html, body {{
    font-family: {stack} !important;
}}

body, body *,
h1, h2, h3, h4, h5, h6,
p, span, a, li, ul, ol, dl, dt, dd,
div, section, article, aside, header, footer, nav, main,
td, th, table, tr, tbody, thead,
blockquote, pre, figure, figcaption,
label, input, textarea, select, button, optgroup, option,
[contenteditable], [contenteditable="true"] {{
    font-family: {stack} !important;
}}

i, em, svg, canvas,
[class*="icon"], [class*="Icon"],
[class*="fa-"], [class*="fa_"],
[class*="material"], [class*="Material"] {{
    font-family: revert !important;
}}
"""


FONT_CSS = _build_font_css()


# ----------------------------------------------------------------------
# 滚动条样式
# ----------------------------------------------------------------------
SCROLLBAR_CSS = """
::-webkit-scrollbar,
*::-webkit-scrollbar {
    width: 8px !important;
    height: 8px !important;
    background: transparent !important;
}
::-webkit-scrollbar-track,
*::-webkit-scrollbar-track {
    background: transparent !important;
    margin: 12px !important;
}
::-webkit-scrollbar-track-piece,
*::-webkit-scrollbar-track-piece {
    background: transparent !important;
    margin: 12px !important;
}
::-webkit-scrollbar-thumb,
*::-webkit-scrollbar-thumb {
    background: rgba(120, 120, 120, 0.04) !important;
    border-radius: 4px !important;
    border: none !important;
}
::-webkit-scrollbar-corner,
*::-webkit-scrollbar-corner {
    background: transparent !important;
}
::-webkit-scrollbar-button,
*::-webkit-scrollbar-button {
    display: none !important;
    background: transparent !important;
}
html.sb-hover::-webkit-scrollbar-thumb,
html.sb-hover *::-webkit-scrollbar-thumb {
    background: rgba(120, 120, 120, 0.75) !important;
}
"""


# ----------------------------------------------------------------------
# 渲染优化：视窗外元素跳过渲染
# ----------------------------------------------------------------------
RENDER_CSS = """
img, video, iframe, picture {
    content-visibility: auto;
    contain-intrinsic-size: 0 200px;
}
"""


# ----------------------------------------------------------------------
# 巡检 + 内联样式清理 + 滚动条 hover + 视窗外图片卸载
# ----------------------------------------------------------------------
MAINTENANCE_JS = """
(function() {
    // ================================================================
    // 样式巡检
    // ================================================================
    function ensureStyle() {
        var el = document.getElementById('__sb_style');
        if (el) return;
        var style = document.createElement('style');
        style.id = '__sb_style';
        style.type = 'text/css';
        style.appendChild(document.createTextNode(window.__sb_css || ''));
        (document.head || document.documentElement).appendChild(style);
    }

    function stripInlineFontFamily() {
        var nodes = document.querySelectorAll('[style*="font-family"]');
        for (var i = 0; i < nodes.length; i++) {
            var el = nodes[i];
            if (el.style && el.style.fontFamily) {
                el.style.removeProperty('font-family');
            }
        }
    }

    // ================================================================
    // 视窗外图片卸载 / 恢复
    // ================================================================
    var SB_PLACEHOLDER = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
    var SB_BUFFER = 800;      // 视窗上下各 800px 内不卸载
    var SB_MIN_SIZE = 4096;   // 小于 4KB 的图（图标等）不卸载

    // 记录每个 img 的原始属性，恢复时用
    function sbUnload(img) {
        if (img.dataset.sbOrig) return;           // 已卸载
        if (!img.src || img.src === SB_PLACEHOLDER) return;
        if (img.src.indexOf('data:') === 0) return;  // 本身是 data URI

        // 小图不卸载（图标、头像等）
        var w = img.naturalWidth || img.width || 0;
        var h = img.naturalHeight || img.height || 0;
        if (w > 0 && h > 0 && w * h < SB_MIN_SIZE) return;

        img.dataset.sbOrig = img.src;

        // 摘掉 B 站的 onload / onerror，避免占位图触发它的逻辑
        var ol = img.getAttribute('onload');
        var oe = img.getAttribute('onerror');
        if (ol !== null) img.dataset.sbOnload = ol;
        if (oe !== null) img.dataset.sbOnerror = oe;
        img.removeAttribute('onload');
        img.removeAttribute('onerror');

        img.src = SB_PLACEHOLDER;
    }

    function sbRestore(img) {
        if (!img.dataset.sbOrig) return;
        img.src = img.dataset.sbOrig;
        delete img.dataset.sbOrig;

        // 挂回 onload / onerror
        if (img.dataset.sbOnload !== undefined) {
            img.setAttribute('onload', img.dataset.sbOnload);
            delete img.dataset.sbOnload;
        }
        if (img.dataset.sbOnerror !== undefined) {
            img.setAttribute('onerror', img.dataset.sbOnerror);
            delete img.dataset.sbOnerror;
        }
    }

    function sbProcessImages() {
        var imgs = document.getElementsByTagName('img');
        var vh = window.innerHeight || document.documentElement.clientHeight;
        for (var i = 0; i < imgs.length; i++) {
            var img = imgs[i];

            // 跳过视频封面之外的特殊 img（如弹幕、图标）
            // 这里只按尺寸判断，尺寸太小就不动

            var rect = img.getBoundingClientRect();
            var top = rect.top;
            var bottom = rect.bottom;

            var inWindow = (bottom > -SB_BUFFER) && (top < vh + SB_BUFFER);

            if (inWindow) {
                sbRestore(img);
            } else {
                sbUnload(img);
            }
        }
    }

    var sbPending = false;
    function sbOnScroll() {
        if (sbPending) return;
        sbPending = true;
        requestAnimationFrame(function() {
            sbProcessImages();
            sbPending = false;
        });
    }

    // ================================================================
    // 安装
    // ================================================================
    if (!window.__sbMonitorInstalled) {
        window.__sbMonitorInstalled = true;

        var SB_W = 14, hovering = false, pending = false;

        function setHover(on) {
            if (on === hovering) return;
            hovering = on;
            if (on) document.documentElement.classList.add('sb-hover');
            else    document.documentElement.classList.remove('sb-hover');
        }

        document.addEventListener('mousemove', function(e) {
            if (pending) return;
            pending = true;
            requestAnimationFrame(function() {
                var nearRight = (window.innerWidth - e.clientX) <= SB_W;
                var nearBottom = (window.innerHeight - e.clientY) <= SB_W;
                setHover(nearRight || nearBottom);
                pending = false;
            });
        }, { passive: true });

        document.addEventListener('mouseleave', function() { setHover(false); });
        window.addEventListener('blur', function() { setHover(false); });

        // 样式巡检
        setInterval(function() {
            var el = document.getElementById('__sb_style');
            if (!el) {
                ensureStyle();
                return;
            }
            var head = document.head || document.documentElement;
            if (head.lastElementChild !== el) head.appendChild(el);
        }, 3000);

        setInterval(stripInlineFontFamily, 3000);

        // 图片卸载：滚动 + 定时
        window.addEventListener('scroll', sbOnScroll, { passive: true });
        setInterval(sbProcessImages, 1000);

        try {
            var mo = new MutationObserver(function() {
                if (!document.getElementById('__sb_style')) ensureStyle();
            });
            mo.observe(document.documentElement, { childList: true, subtree: true });
        } catch (e) {}
    }

    ensureStyle();
    stripInlineFontFamily();
    sbProcessImages();
})();
"""


# ----------------------------------------------------------------------
# 注入源（缓存）
# ----------------------------------------------------------------------
_INJECTED_SOURCE = None


def build_injected_source():
    global _INJECTED_SOURCE
    if _INJECTED_SOURCE is not None:
        return _INJECTED_SOURCE

    css = SCROLLBAR_CSS + RENDER_CSS + FONT_CSS
    _INJECTED_SOURCE = (
        "(function(){\n"
        "window.__sb_css = " + repr(css) + ";\n"
        + MAINTENANCE_JS +
        "})();\n"
    )
    print(f"[styles] injected source: {len(_INJECTED_SOURCE)//1024} KB")
    return _INJECTED_SOURCE