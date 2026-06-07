#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""课本风格几何图引擎 —— 代码绘图，不是 AI 文生图。

用法:
    python3 draw_figure.py spec.json
    或  cat spec.json | python3 draw_figure.py

spec.json 结构:
    {
      "polygon": [[0,0],[10,0],[10,3],[6,3],[6,6],[0,6]],   # 顶点(cm)，按顺序连成图形
      "shade": true,                                         # 是否画 45° 斜线阴影
      "dims": [                                              # 尺寸标注
        {"from":[0,0],"to":[10,0],"label":"10cm"},           #   from/to = 被测线段两端(在图形上)
        {"from":[6,3],"to":[10,3],"label":"4cm","gap":1.4}   #   gap=标注线离图形多远(cm,默认1.0)
      ],                                                     #   dir=[dx,dy] 可手动指定标注甩向
      "out": "fig.png"
    }

设计铁律(老师最头疼的"字压线"就靠这三条根治):
  ① 标注一律甩到图形外的留白(延长线 + 双箭头)，不压在阴影上。
  ② 自动按所有内容算边距，绝不裁切。
  ③ 图里的数字来自 spec —— 与题干、与答案校验脚本同源。

纯 Python(matplotlib) 出 PNG，不依赖浏览器，OpenClaw 的 host / 容器环境都能跑。
"""
import json, sys, math, subprocess


def _ensure(mod, pip):
    try:
        __import__(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pip], check=False)


_ensure("matplotlib", "matplotlib")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib import font_manager

# 中文字体(标题/区域名可能用到；cm 标注是 ASCII)
for f in [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]:
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Noto Sans CJK SC",
                                    "WenQuanYi Zen Hei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["hatch.linewidth"] = 1.4


def load_spec():
    if len(sys.argv) > 1:
        return json.load(open(sys.argv[1], encoding="utf-8"))
    return json.load(sys.stdin)


def main():
    spec = load_spec()
    poly = [tuple(p) for p in spec["polygon"]]
    dims = spec.get("dims", [])
    shade = spec.get("shade", True)
    out = spec.get("out", "figure.png")

    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)

    def perp_away(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        px, py = -dy / L, dx / L
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if px * (mx - cx) + py * (my - cy) < 0:  # 指向远离图形中心的一侧
            px, py = -px, -py
        return px, py

    rendered, allpts = [], list(poly)
    for d in dims:
        a, b = tuple(d["from"]), tuple(d["to"])
        gap = d.get("gap", 1.0)
        if "dir" in d:
            px, py = d["dir"]
            L = math.hypot(px, py) or 1.0
            px, py = px / L, py / L
        else:
            px, py = perp_away(a, b)
        a2 = (a[0] + px * gap, a[1] + py * gap)
        b2 = (b[0] + px * gap, b[1] + py * gap)
        lab = ((a2[0] + b2[0]) / 2 + px * 0.55, (a2[1] + b2[1]) / 2 + py * 0.55)
        rendered.append((a, b, a2, b2, lab, d["label"]))
        allpts += [a, b, a2, b2, lab]

    xs = [p[0] for p in allpts]
    ys = [p[1] for p in allpts]
    pad = 0.8
    xmin, xmax = math.floor(min(xs) - pad), math.ceil(max(xs) + pad)
    ymin, ymax = math.floor(min(ys) - pad), math.ceil(max(ys) + pad)

    fig, ax = plt.subplots(figsize=((xmax - xmin) * 0.55, (ymax - ymin) * 0.55), dpi=200)
    ax.set_facecolor("#F4ECD8")
    fig.patch.set_facecolor("#F4ECD8")

    for x in range(xmin, xmax + 1):
        ax.plot([x, x], [ymin, ymax], color="#DACBA6", lw=0.8, zorder=0)
    for y in range(ymin, ymax + 1):
        ax.plot([xmin, xmax], [y, y], color="#DACBA6", lw=0.8, zorder=0)

    if shade:
        ax.add_patch(Polygon(poly, closed=True, facecolor="none", hatch="///",
                             edgecolor="#111", lw=0.0, zorder=2))
    ax.add_patch(Polygon(poly, closed=True, facecolor="none", edgecolor="#111",
                         lw=3, zorder=3, joinstyle="miter"))

    for a, b, a2, b2, lab, txt in rendered:
        ax.plot([a[0], a2[0]], [a[1], a2[1]], color="#999", lw=1, zorder=2)   # 延长线
        ax.plot([b[0], b2[0]], [b[1], b2[1]], color="#999", lw=1, zorder=2)
        ax.annotate("", xy=b2, xytext=a2,
                    arrowprops=dict(arrowstyle="<->", color="#111", lw=1.6), zorder=4)
        ax.text(lab[0], lab[1], txt, ha="center", va="center",
                fontsize=15, color="#111", zorder=5)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.savefig(out, facecolor="#F4ECD8", bbox_inches="tight", pad_inches=0.12)
    print(out)


if __name__ == "__main__":
    main()
