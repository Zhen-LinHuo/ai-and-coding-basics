#!/usr/bin/env python3
"""Edit a <text> element located by a unique substring.

Usage: python3 fig_edit.py <file> <substring> <json-set-attrs> [delete]
Sets attributes on the matching <text> element (attribute order agnostic).
"""
import json, re, sys
from pathlib import Path


def main():
    path, sub = sys.argv[1], sys.argv[2]
    sets = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    delete = len(sys.argv) > 4 and sys.argv[4] == "delete"
    p = Path(path)
    t = p.read_text()
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", t, re.S):
        if sub in m.group(2):
            attrs = m.group(1)
            body = "" if delete else m.group(2)
            for k, v in sets.items():
                if re.search(rf'\b{k}="[^"]*"', attrs):
                    attrs = re.sub(rf'\b{k}="[^"]*"', f'{k}="{v}"', attrs, count=1)
                else:
                    attrs = attrs + f' {k}="{v}"'
            new = f"<text{attrs}>{body}</text>" if not delete else ""
            t = t[:m.start()] + new + t[m.end():]
            p.write_text(t)
            print(f"ok: {Path(path).stem} :: {sub[:30]} -> {sets or 'delete'}")
            return
    print(f"NOT FOUND: {sub[:40]} in {path}")
    sys.exit(1)


if __name__ == "__main__":
    main()
