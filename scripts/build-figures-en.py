#!/usr/bin/env python3
"""Apply label-translation maps (build/i18n/figures/*.json) to figures/src/*.svg.

Produces figures/en/*.svg — same geometry, English labels.
- keys are exact CJK runs found in the source SVG; every map value must be non-empty
- after substitution any remaining CJK marks the file INCOMPLETE (exit 1)
- heuristic width guard: shrink font-size when estimated text width would
  overflow the canvas (estimate: 0.52 * font-size per ASCII char)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, MAPS, OUT = ROOT / "figures/src", ROOT / "build/i18n/figures", ROOT / "figures/en"
CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]+")
TEXT = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.S)
ATTR = re.compile(r'([\w:-]+)="([^"]*)"')

def guard(tag_attrs, body, canvas_w):
    """Return (new_attrs, new_body, warnings) shrinking font if the text would overflow."""
    a = dict(ATTR.findall(tag_attrs))
    try:
        x = float(a.get("x", 0)); fs = float(a.get("font-size", 14))
    except ValueError:
        return tag_attrs, body, []
    anchor = a.get("text-anchor", "start")
    est = len(body) * 0.52 * fs
    if anchor == "middle":
        avail = 2 * min(x, canvas_w - x)
    elif anchor == "end":
        avail = x
    else:
        avail = canvas_w - x - 6
    if avail <= 0 or est <= avail:
        return tag_attrs, body, []
    new_fs = max(9.0, fs * avail / est)
    if "font-size" in a:
        na = re.sub(r'font-size="[\d.]+"', f'font-size="{new_fs:.1f}"', tag_attrs)
    else:
        na = tag_attrs + f' font-size="{new_fs:.1f}"'
    return na, body, [f"shrunk {fs:g}->{new_fs:.1f}"]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    incomplete, shrunk_n, written = [], 0, 0
    for svg in sorted(SRC.glob("*.svg")):
        out = OUT / svg.name
        # figures/en is authoritative once it exists: hand-edited fixes (e.g. the
        # cross-reference sweep) must not be reverted by a map regeneration.
        if out.exists() and out.stat().st_mtime >= max(svg.stat().st_mtime,
                (MAPS / f"{svg.stem}.json").stat().st_mtime if (MAPS / f"{svg.stem}.json").exists() else 0):
            continue
        mp = MAPS / f"{svg.stem}.json"
        if not mp.exists():
            incomplete.append((svg.name, "no translation map")); continue
        mapping = json.loads(mp.read_text(encoding="utf-8"))
        empty = [k for k, v in mapping.items() if not v.strip()]
        if empty:
            incomplete.append((svg.name, f"{len(empty)} empty values")); continue
        text = svg.read_text(encoding="utf-8")
        missing = set()
        def rep(m):
            s = m.group(0)
            t = mapping.get(s)
            if t is None:
                missing.add(s); return s
            return t
        new = CJK.sub(rep, text)
        W = float(re.search(r'viewBox="0 0 ([\d.]+)', new).group(1))
        def fix(m):
            nonlocal shrunk_n
            na, nb, w = guard(m.group(1), m.group(2), W)
            shrunk_n += len(w)
            return f"<text{na}>{nb}</text>"
        new = TEXT.sub(fix, new)
        if missing:
            incomplete.append((svg.name, f"{len(missing)} untranslated runs"))
        (OUT / svg.name).write_text(new, encoding="utf-8")
        written += 1
    for name, why in incomplete:
        print(f"INCOMPLETE {name}: {why}")
    print(f"figures/en: {written} written, {shrunk_n} labels shrunk, {len(incomplete)} incomplete")
    return 1 if incomplete else 0

if __name__ == "__main__":
    sys.exit(main())
