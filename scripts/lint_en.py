#!/usr/bin/env python3
"""EN edition lint: no CJK in content/en markdown; anchors match the ZH originals."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")
bad = 0
for f in sorted((ROOT / "content/en").rglob("*.md")):
    t = f.read_text(encoding="utf-8")
    hits = CJK.findall(t)
    zh_col = 0
    if f.name == "00-glossary.md":  # 中文 column allowed
        zh_col = sum(1 for line in t.splitlines() if line.startswith("|") and re.search(r"\| [\u4e00-\u9fff]", line))
        hits = [h for h in hits]
        # crude: allow CJK only inside table lines
        line_hits = sum(len(CJK.findall(l)) for l in t.splitlines() if not l.startswith("|"))
        hits = [""] * line_hits
    if hits:
        print(f"CJK in {f.relative_to(ROOT)}: {len(hits)}"); bad += 1
zh_anchors = {}
for f in (ROOT / "content").rglob("*.md"):
    if "/en/" in str(f): continue
    for m in re.finditer(r"\{#((?:sec|fig):[\w-]+)\}", f.read_text(encoding="utf-8")):
        zh_anchors.setdefault(m.group(1), f.name)
missing = []
for f in (ROOT / "content/en").rglob("*.md"):
    for m in re.finditer(r"\{#((?:sec|fig):[\w-]+)\}", f.read_text(encoding="utf-8")):
        if m.group(1) not in zh_anchors:
            missing.append((f.name, m.group(1)))
for name, aid in missing:
    print(f"unknown anchor in EN {name}: {aid}"); bad += 1
print(f"lint-en: {'FAIL ' + str(bad) if bad else 'ok'}")
sys.exit(1 if bad else 0)
