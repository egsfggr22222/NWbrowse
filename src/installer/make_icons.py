# -*- coding: utf-8 -*-
"""把单张 128x128 的 icon.ico 补成多尺寸高清 ICO。

为什么要这么做
--------------
原来的 .ico 只有**一张 128x128**。Windows 在托盘要 16、资源管理器要 32/48、
属性对话框要 32 —— 全都是现场硬缩，细线条必然出锯齿。

原则（重要）
------------
1. **原始 128x128 那一帧原样保留，一个像素都不动** —— 大尺寸显示零损失
2. 补小尺寸（16/20/24/32/40/48/64/96），每个尺寸都从超采样基准独立重采样
3. **不做任何 alpha 增益/加粗** —— 加了会让小图变粗变糊
4. 不上采样到 256（源图只有 128，放大只会更糊）

为什么必须补小尺寸（实测证据）
------------------------------
只放一张 128 的话，Windows 在资源管理器/开始菜单要 32x32、托盘要 16x16 时，
只能拿 128 **硬缩**，用的还是快速滤波 —— 细线条会碎成锯齿。
对比实验（同一台机器，都是 Windows 自己渲染的 32x32）：

    uninstall.exe（多尺寸 ICO，含 32 帧）  -> 平滑
    NWbrowser.exe（单帧 128）              -> 明显锯齿

所以：128 原样留 + 小尺寸补帧，两个目标都满足。
尺寸覆盖 Windows 各档显示：16(托盘/小图标) 20 24 32(列表/属性) 40 48(中图标)
64 96(大图标) 128(原图)。

超采样：先把 128 用**预乘 alpha**放大到 1024，再从 1024 缩到目标尺寸；
预乘可以避免缩放时边缘发灰出暗边。

输出用经典 32bpp BMP 帧（兼容性最好，和原文件格式一致）。
"""

import os
import struct
import sys
from PIL import Image

SRC_SIZES = [16, 20, 24, 32, 40, 48, 64, 96]   # 需要生成的（不含原图那一帧）
SUPER = 1024


# ----------------------------------------------------------------------
# ICO 写入（自己拼，才能精确控制每一帧的像素）
# ----------------------------------------------------------------------
def frame_to_bmp(im):
    """把 RGBA 图编码成 ICO 里的 BMP 帧（BITMAPINFOHEADER + XOR + AND）。"""
    w, h = im.size
    px = im.convert("RGBA").load()

    # XOR：32bpp BGRA，自下而上
    xor = bytearray()
    for y in range(h - 1, -1, -1):
        for x in range(w):
            r, g, b, a = px[x, y]
            xor += bytes((b, g, r, a))

    # AND 掩码：1bpp，每行补到 4 字节，自下而上；0=不透明
    row_bytes = ((w + 31) // 32) * 4
    and_mask = bytearray()
    for y in range(h - 1, -1, -1):
        row = bytearray(row_bytes)
        for x in range(w):
            if px[x, y][3] < 128:
                row[x >> 3] |= (0x80 >> (x & 7))
        and_mask += row

    header = struct.pack("<IiiHHIIiiII", 40, w, h * 2, 1, 32, 0,
                         len(xor) + len(and_mask), 0, 0, 0, 0)
    return bytes(header) + bytes(xor) + bytes(and_mask)


def write_ico(frames, out_path):
    """frames: {边长: RGBA Image}

    帧按**从大到小**排列。这一点很重要：
    `QPixmap("x.ico")` 取的是 ICO 里的**第一帧**，不是最大帧。
    如果 16x16 排在最前，任何直接 QPixmap 读它的代码都会拿到 16x16，
    再放大就发糊（输入框左侧的引擎按钮就是这么踩的坑）。
    `QIcon` 不受影响（它按请求尺寸挑帧），Windows 也不挑顺序。
    """
    sizes = sorted(frames, reverse=True)
    blobs = [frame_to_bmp(frames[s]) for s in sizes]
    offset = 6 + 16 * len(sizes)
    with open(out_path, "wb") as f:
        f.write(struct.pack("<HHH", 0, 1, len(sizes)))
        for s, blob in zip(sizes, blobs):
            f.write(struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0,
                                1, 32, len(blob), offset))
            offset += len(blob)
        for blob in blobs:
            f.write(blob)


# ----------------------------------------------------------------------
# 图像处理
# ----------------------------------------------------------------------
def largest_frame(path):
    """取 ICO 里最大的那一帧。

    注意：新版 Pillow 的 Image.size 是只读属性，不能再写
    `im.size = (256,256)` 选帧，要用 im.ico.getimage(size)。
    """
    im = Image.open(path)
    try:
        sizes = im.ico.sizes()
        return im.ico.getimage(max(sizes)).convert("RGBA")
    except Exception:
        return im.convert("RGBA")


def premultiply(im):
    from PIL import ImageChops
    r, g, b, a = im.split()
    a3 = Image.merge("RGB", (a, a, a))
    rgb = ImageChops.multiply(Image.merge("RGB", (r, g, b)), a3)
    return Image.merge("RGBA", (*rgb.split(), a))


def unpremultiply(im):
    px = im.load()
    w, h = im.size
    out = Image.new("RGBA", (w, h))
    po = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            po[x, y] = (0, 0, 0, 0) if a == 0 else (
                min(255, r * 255 // a), min(255, g * 255 // a),
                min(255, b * 255 // a), a)
    return out


def build(src_path, out_path):
    src = largest_frame(src_path)
    w0, h0 = src.size

    # 透明区域的 RGB 归零，避免缩放时带出杂色
    px = src.load()
    for y in range(h0):
        for x in range(w0):
            r, g, b, a = px[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)

    big = unpremultiply(premultiply(src).resize((SUPER, SUPER), Image.LANCZOS))

    frames = {}
    for s in SRC_SIZES:
        if s < w0:
            frames[s] = big.resize((s, s), Image.LANCZOS)
    frames[w0] = src                      # ← 原图原样，零损失

    write_ico(frames, out_path)
    return frames


def make_header(src_path, out_path, size=128, radius=26, scale=0.72):
    """安装向导深色头部用的图标：白底圆角 + 原 logo。

    logo 是黑色线条，直接放深色头部上等于看不见，所以衬一块白底板。
    原图配色一点不动。
    """
    from PIL import ImageDraw
    src = largest_frame(src_path)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).rounded_rectangle(
        [0, 0, size - 1, size - 1], radius=radius, fill=(255, 255, 255, 255))
    inner = int(size * scale)
    glyph = src.resize((inner, inner), Image.LANCZOS)
    off = (size - inner) // 2
    canvas.paste(glyph, (off, off), glyph)
    canvas.save(out_path)
    return out_path


def preview(frames, out_png, scales=(16, 24, 32, 48, 128)):
    """把各尺寸放大摆出来，直观看像素质量。"""
    from PIL import ImageDraw
    zoom = 6
    pad = 12
    cell = 128 * zoom
    W = len(scales) * (cell + pad) + pad
    H = 2 * (cell + pad) + pad
    canvas = Image.new("RGB", (W, H), (243, 243, 243))
    ImageDraw.Draw(canvas).rectangle([0, 0, W, cell + pad], fill=(28, 28, 28))
    for i, s in enumerate(scales):
        if s not in frames:
            continue
        f = frames[s].resize((s * zoom, s * zoom), Image.NEAREST)
        x = pad + i * (cell + pad)
        canvas.paste(f, (x, pad), f)
        canvas.paste(f, (x, cell + pad * 2), f)
    canvas.save(out_png)


def main():
    ws = r"C:\Users\computer\Desktop\DSH workspace"
    data = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ws,
                                                              "browser_project", "data")
    names = ["icon.ico", "settings_icon.ico", "download_icon.ico"]
    frames = None
    for n in names:
        p = os.path.join(data, n)
        if not os.path.isfile(p):
            print("  跳过（不存在）:", p)
            continue
        before = os.path.getsize(p)
        f = build(p, p)
        after = os.path.getsize(p)
        print("  %-22s %6d -> %6d 字节   尺寸=%s"
              % (n, before, after, sorted(f)))
        if frames is None:
            frames = f

    if frames:
        preview(frames, os.path.join(ws, "_icon_quality.png"))
        print("  预览: _icon_quality.png")

    inst = os.path.join(ws, "installer")
    ico = os.path.join(inst, "setup.ico")
    if os.path.isfile(ico):
        # 安装器图标直接用生成好的 icon.ico
        import shutil
        shutil.copy2(os.path.join(data, "icon.ico"), ico)
        make_header(ico, os.path.join(inst, "setup_header.png"))
        print("  向导头部图标: installer\\setup_header.png")


if __name__ == "__main__":
    main()
