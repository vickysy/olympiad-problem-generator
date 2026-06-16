#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初中数学几何引擎 —— 代码绘图,不是 AI 文生图。
能画:平面直角坐标系 + 函数图象、三角形/四边形、带名字的点、连线、
     垂直/直角标记、边长标注、等长刻度。在龙象/Agent 里 `python3 geo_figure.py spec.json` 即出 PNG。

spec.json 示例(正方形 ABCD 边长4,E在BC上 BE=1,连AE,过B作BF⊥AE于F):
{
  "points": {"A":[0,4],"B":[0,0],"C":[4,0],"D":[4,4],"E":[1,0],"F":[0.47,0.88]},
  "polygon": ["A","B","C","D"],
  "segments": [["A","E"],["B","F"]],
  "right_angles": [["F","A","B"]],
  "seg_labels": [{"seg":["B","E"],"text":"1"}],
  "labels": {"A":"ul","B":"dl","C":"dr","D":"ur","E":"down","F":"up"},
  "out":"fig.png"
}
坐标系/函数图象示例:
{ "axes":{"x":[-1,5],"y":[-1,5]}, "funcs":[{"k":-1,"b":3,"label":"y=-x+3"}], "out":"fig.png" }
"""
import json, math, sys, subprocess


def _ensure(m, p):
    try: __import__(m)
    except ImportError: subprocess.run([sys.executable, "-m", "pip", "install", "-q", p], check=False)


_ensure("matplotlib", "matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge, Arc
from matplotlib import font_manager

for f in ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/STHeiti Medium.ttc",
          "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
          "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]:
    try: font_manager.fontManager.addfont(f)
    except Exception: pass
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Noto Sans CJK SC",
                                   "WenQuanYi Zen Hei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["hatch.linewidth"] = 1.2

OFF = {"left": (-1, 0), "right": (1, 0), "up": (0, 1), "down": (0, -1),
       "ul": (-1, 1), "ur": (1, 1), "dl": (-1, -1), "dr": (1, -1)}


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else json.load(sys.stdin)
    P = {k: tuple(v) for k, v in spec.get("points", {}).items()}
    out = spec.get("out", "figure.png")
    axes = spec.get("axes")
    funcs = spec.get("funcs", [])
    fig, ax = plt.subplots(figsize=(5, 5), dpi=200)
    ax.set_facecolor("#FDFBF5")
    fig.patch.set_facecolor("#FDFBF5")

    allx, ally = [p[0] for p in P.values()], [p[1] for p in P.values()]

    # ---------- 坐标系 ----------
    if axes:
        xr, yr = axes.get("x", [-5, 5]), axes.get("y", [-5, 5])
        allx += xr; ally += yr
        for gx in range(int(math.floor(xr[0])), int(math.ceil(xr[1])) + 1):
            ax.plot([gx, gx], yr, color="#E6DAC2", lw=0.6, zorder=0)
        for gy in range(int(math.floor(yr[0])), int(math.ceil(yr[1])) + 1):
            ax.plot(xr, [gy, gy], color="#E6DAC2", lw=0.6, zorder=0)
        ax.annotate("", xy=(xr[1], 0), xytext=(xr[0], 0),
                    arrowprops=dict(arrowstyle="-|>", color="#111", lw=1.6), zorder=3)
        ax.annotate("", xy=(0, yr[1]), xytext=(0, yr[0]),
                    arrowprops=dict(arrowstyle="-|>", color="#111", lw=1.6), zorder=3)
        ax.text(xr[1], -0.05 * (yr[1] - yr[0]), "x", fontsize=14, ha="right", va="top", style="italic")
        ax.text(-0.05 * (xr[1] - xr[0]), yr[1], "y", fontsize=14, ha="right", va="top", style="italic")
        ax.text(-0.04 * (xr[1] - xr[0]), -0.04 * (yr[1] - yr[0]), "O", fontsize=13, ha="right", va="top")
        for t in range(int(math.ceil(xr[0])), int(math.floor(xr[1])) + 1):
            if t: ax.text(t, -0.04 * (yr[1] - yr[0]), str(t), fontsize=9, ha="center", va="top", color="#555")
        for t in range(int(math.ceil(yr[0])), int(math.floor(yr[1])) + 1):
            if t: ax.text(-0.03 * (xr[1] - xr[0]), t, str(t), fontsize=9, ha="right", va="center", color="#555")

    # ---------- 函数图象 ----------
    for fdef in funcs:
        xr = (axes or {}).get("x", [min(allx) - 1, max(allx) + 1])
        xs = [xr[0] + (xr[1] - xr[0]) * i / 200 for i in range(201)]
        if "k" in fdef:
            ys = [fdef["k"] * x + fdef.get("b", 0) for x in xs]
        elif "a" in fdef:
            ys = [fdef["a"] * x * x + fdef.get("b", 0) * x + fdef.get("c", 0) for x in xs]
        elif "points" in fdef:
            xs = [p[0] for p in fdef["points"]]; ys = [p[1] for p in fdef["points"]]
        else:
            continue
        ax.plot(xs, ys, color=fdef.get("color", "#C0633D"), lw=2.2, zorder=4)
        if fdef.get("label"):
            ax.text(xs[int(len(xs) * 0.82)], ys[int(len(ys) * 0.82)], fdef["label"],
                    fontsize=11, color=fdef.get("color", "#C0633D"))

    # ---------- 圆 / 弧 / 扇形 / 角标记 ----------
    def rc(c):   # 解析中心:点名或坐标
        return tuple(P[c]) if isinstance(c, str) else tuple(c)
    for cir in spec.get("circles", []):
        c = rc(cir["c"]); r = cir["r"]
        ax.add_patch(Circle(c, r, fill=False, edgecolor="#111", lw=2.0, zorder=2,
                            linestyle="--" if cir.get("dash") else "-"))
        allx += [c[0] - r, c[0] + r]; ally += [c[1] - r, c[1] + r]
        if cir.get("center_dot", True):
            ax.plot([c[0]], [c[1]], "o", color="#111", ms=3.5, zorder=5)
    for arc in spec.get("arcs", []):
        c = rc(arc["c"]); r = arc["r"]
        ax.add_patch(Arc(c, 2 * r, 2 * r, theta1=arc["a0"], theta2=arc["a1"],
                         color="#111", lw=2.0, zorder=2))
        allx += [c[0] - r, c[0] + r]; ally += [c[1] - r, c[1] + r]
    for sec in spec.get("sectors", []):
        c = rc(sec["c"]); r = sec["r"]
        if sec.get("shade"):
            ax.add_patch(Wedge(c, r, sec["a0"], sec["a1"], facecolor="none",
                               hatch="///", edgecolor="#111", lw=0.0, zorder=1))
        ax.add_patch(Wedge(c, r, sec["a0"], sec["a1"], facecolor="none",
                           edgecolor="#111", lw=2.0, zorder=2))
        allx += [c[0] - r, c[0] + r]; ally += [c[1] - r, c[1] + r]
    for an in spec.get("angles", []):
        V = rc(an["v"])
        a1 = math.degrees(math.atan2(rc(an["p1"])[1] - V[1], rc(an["p1"])[0] - V[0]))
        a2 = math.degrees(math.atan2(rc(an["p2"])[1] - V[1], rc(an["p2"])[0] - V[0]))
        rr = an.get("r", 0.5)
        lo, hi = min(a1, a2), max(a1, a2)
        if hi - lo > 180: lo, hi = hi, lo + 360   # 取较小的那个夹角
        ax.add_patch(Arc(V, 2 * rr, 2 * rr, theta1=lo, theta2=hi, color="#111", lw=1.3, zorder=4))
        if an.get("text"):
            mid = math.radians((lo + hi) / 2)
            ax.text(V[0] + math.cos(mid) * rr * 1.6, V[1] + math.sin(mid) * rr * 1.6,
                    an["text"], fontsize=11, ha="center", va="center", zorder=6)

    # ---------- 多边形(浅描边/可填充) ----------
    if spec.get("polygon"):
        pts = [P[n] for n in spec["polygon"]]
        if spec.get("shade"):
            ax.add_patch(Polygon(pts, closed=True, facecolor="none", hatch="///",
                                 edgecolor="#111", lw=0.0, zorder=1))
        ax.add_patch(Polygon(pts, closed=True, facecolor="none", edgecolor="#111",
                             lw=2.2, zorder=3, joinstyle="miter"))

    # ---------- 连线 ----------
    for a, b in spec.get("segments", []):
        ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color="#111", lw=2.0, zorder=3)

    # ---------- 直角标记 ----------
    def ra_mark(v, p1, p2, s=0.28):
        V = P[v]
        def u(q):
            dx, dy = P[q][0] - V[0], P[q][1] - V[1]
            L = math.hypot(dx, dy) or 1
            return dx / L, dy / L
        u1, u2 = u(p1), u(p2)
        c1 = (V[0] + u1[0] * s, V[1] + u1[1] * s)
        c2 = (V[0] + (u1[0] + u2[0]) * s, V[1] + (u1[1] + u2[1]) * s)
        c3 = (V[0] + u2[0] * s, V[1] + u2[1] * s)
        ax.plot([c1[0], c2[0], c3[0]], [c1[1], c2[1], c3[1]], color="#111", lw=1.3, zorder=4)
    for tri in spec.get("right_angles", []):
        ra_mark(*tri)

    # ---------- 边长标注 ----------
    for sl in spec.get("seg_labels", []):
        a, b = sl["seg"]; A, B = P[a], P[b]
        mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
        dx, dy = B[0] - A[0], B[1] - A[1]
        L = math.hypot(dx, dy) or 1
        px, py = -dy / L, dx / L
        off = sl.get("off", 0.32)
        ax.text(mx + px * off, my + py * off, sl["text"], fontsize=12,
                ha="center", va="center", color="#111", zorder=5)

    # ---------- 等长刻度 ----------
    for tk in spec.get("ticks", []):
        a, b = tk["seg"]; A, B = P[a], P[b]; nseg = tk.get("n", 1)
        mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
        dx, dy = (B[0] - A[0]), (B[1] - A[1]); Ln = math.hypot(dx, dy) or 1
        ux, uy = dx / Ln, dy / Ln; px, py = -uy, ux
        for i in range(nseg):
            o = (i - (nseg - 1) / 2) * 0.08
            cx, cy = mx + ux * o, my + uy * o
            ax.plot([cx - px * .12, cx + px * .12], [cy - py * .12, cy + py * .12],
                    color="#111", lw=1.2, zorder=4)

    # ---------- 点 + 名字 ----------
    cx = sum(allx) / len(allx); cy = sum(ally) / len(ally)
    lab = spec.get("labels", {})
    for n, (x, y) in P.items():
        if spec.get("dots", True):
            ax.plot([x], [y], "o", color="#111", ms=4, zorder=5)
        d = lab.get(n)
        if d in OFF:
            ox, oy = OFF[d]
        else:
            ox, oy = (x - cx), (y - cy)
            L = math.hypot(ox, oy) or 1; ox, oy = ox / L, oy / L
        span = (max(allx) - min(allx) + max(ally) - min(ally)) / 2 or 1
        ax.text(x + ox * 0.06 * span, y + oy * 0.06 * span, n, fontsize=14,
                fontweight="bold", ha="center", va="center", zorder=6)

    pad = (max(allx) - min(allx) + max(ally) - min(ally)) * 0.06 + 0.3
    ax.set_xlim(min(allx) - pad, max(allx) + pad)
    ax.set_ylim(min(ally) - pad, max(ally) + pad)
    ax.set_aspect("equal"); ax.axis("off")
    plt.savefig(out, facecolor="#FDFBF5", bbox_inches="tight", pad_inches=0.12)
    print(out)


if __name__ == "__main__":
    main()
