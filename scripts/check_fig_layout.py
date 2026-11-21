#!/usr/bin/env python3
"""Geometric overlap checker for book SVGs.

Estimates every <text> element's bounding box and flags:
  A) text-vs-text overlaps (same-figure pairs whose boxes intersect)
  B) text overflowing the rect/box it starts in (estimated right edge > rect right)
  C) text outside the viewBox
Width estimate: CJK char = 1.0*fs, other = 0.55*fs (monospace-ish upper bound
for Noto Sans); anchor-aware (start/middle/end).
"""
import re, sys, glob
from pathlib import Path

CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")
TEXT = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.S)
ATTR = re.compile(r'([\w:-]+)="([^"]*)"')
RECT = re.compile(r"<rect\b([^>]*)/?>")
VIEW = re.compile(r'viewBox="0 0 ([\d.]+) ([\d.]+)"')
TAG = re.compile(r"<[^>]+>")


def est_width(s, fs):
    w = 0.0
    for ch in TAG.sub("", s):
        w += fs * (1.0 if CJK.match(ch) else 0.55)
    return w


def text_box(attrs, body):
    a = dict(ATTR.findall(attrs))
    try:
        x = float(a.get("x", 0)); y = float(a.get("y", 0)); fs = float(a.get("font-size", 14))
    except ValueError:
        return None
    anc = a.get("text-anchor", "start")
    w = est_width(body, fs)
    if anc == "middle":
        x0 = x - w / 2
    elif anc == "end":
        x0 = x - w
    else:
        x0 = x
    return (x0, y - fs * 0.8, x0 + w, y + fs * 0.25)


def inter(a, b, pad=1.0):
    return not (a[2] <= b[0] + pad or b[2] <= a[0] + pad or a[3] <= b[1] + pad or b[3] <= a[1] + pad)


def main(root):
    problems = 0
    for f in sorted(glob.glob(f"{root}/*.svg")):
        t = Path(f).read_text()
        vb = VIEW.search(t)
        W, H = float(vb.group(1)), float(vb.group(2))
        texts = []
        for m in TEXT.finditer(t):
            bx = text_box(m.group(1), m.group(2))
            label = TAG.sub("", m.group(2)).strip()
            if bx and label:
                texts.append((bx, label[:40]))
        rects = []
        for m in RECT.finditer(t):
            a = dict(ATTR.findall(m.group(1)))
            try:
                rects.append((float(a["x"]), float(a["y"]),
                              float(a["x"]) + float(a["width"]), float(a["y"]) + float(a["height"])))
            except (KeyError, ValueError):
                pass
        # A) text-text
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if inter(texts[i][0], texts[j][0], pad=2):
                    print(f"OVERLAP {Path(f).stem}: [{texts[i][1]!r}] x [{texts[j][1]!r}]")
                    problems += 1
        # B) text vs the rect it starts inside (right-edge overflow)
        for bx, label in texts:
            for r in rects:
                if r[0] - 2 <= bx[0] <= r[2] and r[1] - 2 <= bx[1] <= r[3]:
                    if bx[2] > r[2] + 2:
                        print(f"OVERFLOW-BOX {Path(f).stem}: {label!r} ends {bx[2]:.0f} > box {r[2]:.0f}")
                        problems += 1
                    break
        # C) outside viewBox
        for bx, label in texts:
            if bx[0] < -2 or bx[1] < -2 or bx[2] > W + 2 or bx[3] > H + 2:
                reason = ("left" if bx[0] < -2 else "top" if bx[1] < -2 else
                          "right" if bx[2] > W + 2 else "bottom")
                print(f"OUT-CANVAS[{reason}] {Path(f).stem}: {label!r} box=({bx[0]:.0f},{bx[1]:.0f},{bx[2]:.0f},{bx[3]:.0f}) vb={W:.0f}x{H:.0f}")
                problems += 1
    print(f"-- {problems} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "figures/en"))
