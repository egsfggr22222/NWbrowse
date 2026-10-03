# -*- coding: utf-8 -*-
"""自定义协议 appfont:// 处理器。"""

import os

from PyQt6.QtCore import QBuffer, QIODevice, QUrl
from PyQt6.QtWebEngineCore import (
    QWebEngineUrlScheme,
    QWebEngineUrlSchemeHandler,
    QWebEngineUrlRequestJob,
)


FONT_SCHEME = b"appfont"

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)
FONTS_DIR = os.path.join(_PROJECT_ROOT, "assets", "fonts")


_MIME_BY_EXT = {
    ".woff2": b"font/woff2",
    ".woff":  b"font/woff",
    ".ttf":   b"font/ttf",
    ".otf":   b"font/otf",
}


class FontSchemeHandler(QWebEngineUrlSchemeHandler):
    def requestStarted(self, request: QWebEngineUrlRequestJob):
        url = request.requestUrl()
        name = url.path().lstrip("/")
        if not name or "/" in name or ".." in name:
            request.fail(QWebEngineUrlRequestJob.Error.UrlNotFound)
            return

        path = os.path.join(FONTS_DIR, name)
        if not os.path.isfile(path):
            request.fail(QWebEngineUrlRequestJob.Error.UrlNotFound)
            return

        ext = os.path.splitext(name)[1].lower()
        mime = _MIME_BY_EXT.get(ext)
        if mime is None:
            request.fail(QWebEngineUrlRequestJob.Error.RequestFailed)
            return

        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError:
            request.fail(QWebEngineUrlRequestJob.Error.RequestFailed)
            return

        buf = QBuffer(parent=request)
        buf.setData(data)
        buf.open(QIODevice.OpenModeFlag.ReadOnly)
        request.reply(mime, buf)


_REGISTERED = False


def register_font_scheme():
    global _REGISTERED
    if _REGISTERED:
        return
    _REGISTERED = True

    scheme = QWebEngineUrlScheme(FONT_SCHEME)
    scheme.setFlags(
        QWebEngineUrlScheme.Flag.SecureScheme
        | QWebEngineUrlScheme.Flag.LocalAccessAllowed
        | QWebEngineUrlScheme.Flag.CorsEnabled
    )
    scheme.setSyntax(QWebEngineUrlScheme.Syntax.Host)
    QWebEngineUrlScheme.registerScheme(scheme)