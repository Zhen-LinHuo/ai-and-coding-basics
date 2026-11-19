#!/usr/bin/env python3
"""Bibliography lint — 两个方向都查。

1. 正文引用了 bib 里不存在的键：构建错误（pandoc 会静默给出 [?]，读者看到的是破引用）。
2. bib 里有从未被引用的条目：警告（多半是删章时忘了清）。

带日期的注记框里的引用同样计入，不做例外。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIB = ROOT / "bib" / "refs.bib"
ENTRY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")
# pandoc 引用语法：[@key]、[see @key, p.3]、[-@key]；排除邮箱
CITE_RE = re.compile(r"(?<![A-Za-z0-9._%+-])@([A-Za-z][A-Za-z0-9_:.\-]*)")


def main():
    if not BIB.is_file():
        print("lint_bib: bib/refs.bib 不存在")
        return 1
    keys = set(ENTRY_RE.findall(BIB.read_text(encoding="utf-8")))
    cited = {}
    for p in sorted((ROOT / "content").rglob("*.md")):
        rel = p.relative_to(ROOT)
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for k in CITE_RE.findall(line):
                cited.setdefault(k, f"{rel}:{n}")

    ghost = sorted(set(cited) - keys)
    unused = sorted(keys - set(cited))

    for k in ghost:
        print(f"ERROR 引用了 bib 里不存在的键 @{k}（{cited[k]}）")
    for k in unused:
        print(f"WARN  bib 条目 @{k} 从未被引用")

    print(f"lint_bib: {len(keys)} 条记录，{len(cited)} 个被引用的键，"
          f"{len(ghost)} 处坏引用，{len(unused)} 条未使用")
    return 1 if ghost else 0


if __name__ == "__main__":
    sys.exit(main())
