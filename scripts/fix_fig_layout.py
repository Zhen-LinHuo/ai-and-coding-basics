#!/usr/bin/env python3
"""Bounded auto-fix for figure layout: wrap out-of-canvas text, shrink overflows.

Checks handled (see check_fig_layout.py):
  C-right  text past the right canvas edge  -> wrap into two lines
  C-bottom text past the bottom canvas edge -> lift y
  C-left   middle/end text past left edge   -> shift x right
  B        text wider than its box/rect     -> shrink font (tightest rect wins)
"""
import re, sys, glob
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check_fig_layout import TEXT, ATTR, VIEW, TAG, CJK, est_width, text_box  # noqa

RECT = re.compile(r"<rect\b([^>]*)/?>")


def rects(t):
    out = []
    for m in RECT.finditer(t):
        a = dict(ATTR.findall(m.group(1)))
        try:
            out.append((float(a["x"]), float(a["y"]),
                        float(a["x"]) + float(a["width"]), float(a["y"]) + float(a["height"])))
        except (KeyError, ValueError):
            pass
    return out


def set_fs(attrs, a, n):
    na = re.sub(r'font-size="[\d.]+"', f'font-size="{n:.1f}"', attrs)
    if "font-size" not in a:
        na = attrs + f' font-size="{n:.1f}"'
    return na


def drop_coord(attrs, name):
    """Remove an existing x/y attribute so a new one can be appended (no duplicates)."""
    return re.sub(rf'\s{name}="[-\d.]+"', "", attrs)


def apply_fixes(t, W, H):
    """One pass: compute fixes from current content, apply bottom-up by span."""
    fixes = []  # (start, end, replacement)
    rs = rects(t)
    for m in TEXT.finditer(t):
        attrs, body = m.group(1), m.group(2)
        plain = TAG.sub("", body).strip()
        if not plain:
            continue
        bx = text_box(attrs, body)
        if bx is None:
            continue
        a = dict(ATTR.findall(attrs))
        fs = float(a.get("font-size", 14))
        x = float(a.get("x", 0))
        y = float(a.get("y", 0))
        anc = a.get("text-anchor", "start")

        # C-right) outside canvas (right edge) -> wrap into two lines
        if bx[2] > W + 2:
            avail = W - 8 - (x if anc == "start" else min(x, W - x))
            target = max(avail, 120.0)
            # greedy char fill up to target width, prefer breaking at a space
            acc, cut = 0.0, len(plain)
            for k, ch in enumerate(plain):
                acc += fs * (1.0 if CJK.match(ch) else 0.55)
                if acc > target:
                    cut = k
                    break
            sp = plain.rfind(" ", max(0, cut - 12), cut)
            if sp > 0:
                cut = sp
            l1, l2 = plain[:cut].rstrip(), plain[cut:].lstrip()
            if l2:
                fs2 = fs
                for _ in range(8):
                    ok = True
                    for part in (l1, l2):
                        w_ = est_width(part, fs2)
                        x_ = x - (w_ / 2 if anc == "middle" else w_ if anc == "end" else 0)
                        if x_ < 4 or x_ + w_ > W - 4:
                            ok = False
                    if ok or fs2 <= 9.0:
                        break
                    fs2 *= 0.92
                na = drop_coord(set_fs(attrs, a, fs2), "y")
                dy = fs2 * 1.3
                fixes.append((m.start(), m.end(),
                              f"<text{na}>{l1}</text><text{na} y=\"{y + dy:.1f}\">{l2}</text>"))
                continue

        # C-bottom) vertical overflow (bottom legend) -> lift y so the box fits
        if bx[3] > H + 2 and bx[2] <= W + 2:
            ny = y - (bx[3] - H + 4)
            fixes.append((m.start(), m.end(),
                          f"<text{drop_coord(set_fs(attrs, a, fs), 'y')} y=\"{ny:.1f}\">{body}</text>"))
            continue

        # C-left) left overflow (middle/end anchors) -> shift x right
        if bx[0] < -2 and bx[2] <= W + 2:
            nx = x + (2 - bx[0])
            if nx + est_width(plain, fs) <= W - 4:
                fixes.append((m.start(), m.end(),
                              f"<text{drop_coord(set_fs(attrs, a, fs), 'x')} x=\"{nx:.1f}\">{body}</text>"))
            continue

        # B) text wider than its containing rect -> shrink (tightest rect wins)
        for r in sorted(rs, key=lambda r: r[2]):
            if r[0] - 2 <= bx[0] <= r[2] and r[1] - 2 <= bx[1] <= r[3]:
                if bx[2] > r[2] + 2:
                    n = fs
                    avail = r[2] - r[0] - 10
                    for _ in range(8):
                        if est_width(plain, n) <= avail or n <= 9.0:
                            break
                        n *= 0.92
                    if n < fs - 0.05:
                        fixes.append((m.start(), m.end(),
                                      f"<text{set_fs(attrs, a, n)}>{body}</text>"))
                break

    # apply bottom-up, skip overlapping spans
    fixes.sort(key=lambda f: f[0], reverse=True)
    last = len(t)
    for s, e, rep in fixes:
        if e <= last:
            t = t[:s] + rep + t[e:]
            last = s
    return t


def main(root):
    for f in sorted(glob.glob(f"{root}/*.svg")):
        p = Path(f)
        t = p.read_text()
        for _ in range(4):  # bounded passes
            vb = VIEW.search(t)
            W, H = float(vb.group(1)), float(vb.group(2))
            t2 = apply_fixes(t, W, H)
            if t2 == t:
                break
            t = t2
        p.write_text(t)
    print("done")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "figures/en")
