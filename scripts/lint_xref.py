#!/usr/bin/env python3
"""Cross-reference lint — 引用必须指向存在的锚点。

正文里两种写法都会被查：
  - 交叉引用：@fig:id / @sec:id（build/xref.lua 负责渲染成 \ref 或链接）
  - 锚点定义：图片的 {#fig:id} 与标题的 {#sec:id}

被引用但不存在的锚点是构建错误；定义了却没人引用只是提示。
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEF_RE = re.compile(r"\{#((?:fig|sec|eq|tab):[\w-]+)\}")
REF_RE = re.compile(r"(?<![\w])@((?:fig|sec|eq|tab):[\w-]+)")

def main():
    defined, used = {}, {}
    for p in sorted((ROOT / "content").rglob("*.md")):
        rel = p.relative_to(ROOT)
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for m in DEF_RE.findall(line):
                defined.setdefault(m, f"{rel}:{n}")
            for m in REF_RE.findall(line):
                used.setdefault(m, f"{rel}:{n}")
    ghost = sorted(set(used) - set(defined))
    orphan = sorted(set(defined) - set(used))
    for k in ghost:
        print(f"ERROR 引用了不存在的锚点 @{k}（{used[k]}）")
    for k in orphan:
        print(f"WARN  锚点 {k} 从未被引用（{defined[k]}）")
    print(f"lint_xref: {len(defined)} 个锚点，{len(used)} 个引用，"
          f"{len(ghost)} 处坏引用，{len(orphan)} 个未引用锚点")
    return 1 if ghost else 0

if __name__ == "__main__":
    sys.exit(main())
