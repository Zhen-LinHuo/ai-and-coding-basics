#!/usr/bin/env python3
"""Section skeleton lint — 检查每节是否满足「六拍」的硬性构件。

不检查文风，只检查结构上最容易漏掉的东西：
  - 必须是一级标题开头，且标题带章节编号；
  - 「常见误解」callout 必须在；
  - 「小结」必须在。

带 `<!-- stub -->` 标记的文件是未撰写的占位，只检查标题。
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_PREFIX = ("00-front", "90-back")
HEADING_RE = re.compile(r"^#{1,3} \S")
MANUAL_NUM = re.compile(r"^#{1,3} [0-9]+(\.[0-9]+)*\s")
RULES = [
    ("常见误解", "缺少「常见误解」段落（这一节必须点出读者最容易搞错的地方）"),
    ("小结", "缺少「小结与自检」"),
]


def main():
    problems = 0
    checked = 0
    for p in sorted((ROOT / "content").rglob("*.md")):
        rel = p.relative_to(ROOT / "content")
        if rel.parts and rel.parts[0] in SKIP_PREFIX:
            continue
        text = p.read_text(encoding="utf-8")
        checked += 1
        lines = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("<!--")]
        first = lines[0] if lines else ""
        if not HEADING_RE.match(first):
            problems += 1
            print(f"{rel}: 必须以一至三级标题开头，实为 {first[:50]!r}")
            continue
        if MANUAL_NUM.match(first):
            problems += 1
            print(f"{rel}: 标题里不要手写编号（章节号由排版自动生成），实为 {first[:40]!r}")
            continue
        if "<!-- stub -->" in text:
            continue
        for needle, msg in RULES:
            if needle not in text:
                problems += 1
                print(f"{rel}: {msg}")
    if problems:
        print(f"\n{problems} 处结构问题（共检查 {checked} 节）。规格见 OUTLINE.md 第三节。")
        return 1
    print(f"lint_sections: ok ({checked} 节)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
