#!/usr/bin/env python3
"""Emoji lint.

本仓库禁用 emoji。这不是洁癖：排版的 emoji 支持是可选的 Lua 过滤器加字体，
一旦正文出现 emoji，每个输出格式都要单独兜底，PDF 里还会退化成缺字方块。

扫描范围：正文、插图源、以及仓库根的个人文档。
"""
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 只拦真正的表情符号区段。箭头、数学符号、制表符不在此列。
RANGES = [
    (0x1F000, 0x1FAFF),   # 表情、交通、补充符号、扩展 A
    (0x2600, 0x27BF),     # 杂项符号与装饰符号
    (0x2B00, 0x2BFF),     # 杂项符号与箭头
    (0xFE00, 0xFE0F),     # 变体选择符
    (0x20E3, 0x20E3),     # 组合包围键帽
]
EXTRA_FILES = ["OUTLINE.md", "README.md", "AGENTS.md", "AGENTS.local.md"]
SCAN_DIRS = ["content", "figures"]
TEXT_EXT = {".md", ".svg", ".tex", ".css", ".py", ".lua", ".yaml", ".bib"}


def is_emoji(ch):
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in RANGES)


def files():
    for name in EXTRA_FILES:
        p = ROOT / name
        if p.is_file():
            yield p
    for d in SCAN_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in TEXT_EXT:
                yield p


def main():
    bad = 0
    for p in files():
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            hits = [c for c in line if is_emoji(c)]
            if hits:
                bad += 1
                rel = p.relative_to(ROOT)
                cps = " ".join(f"U+{ord(c):04X}" for c in hits)
                print(f"{rel}:{n}: {cps}  {line.strip()[:70]}")
    if bad:
        print(f"\n发现 {bad} 行含 emoji。本仓库禁用 emoji，请改写为文字。")
        return 1
    print("lint_emoji: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
