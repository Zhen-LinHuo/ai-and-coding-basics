#!/usr/bin/env python3
"""把 content/ 组装成 MkDocs 的 docs 目录（site-src/）。

- 复制各节 Markdown，保持相对路径（figures/ 一起复制，图内相对路径不变）
- 引用 [@key] 转成数字编号 [n]，并生成"参考文献"页（按首次出现排序）
- 表格/图片/标题属性原样保留（attr_list 兼容 MkDocs）
"""
import re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANG = "en" if "--lang" in sys.argv and sys.argv[sys.argv.index("--lang") + 1] == "en" else "zh"
DOCS = ROOT / ("site-src-en" if LANG == "en" else "site-src")

# (源文件, 输出名, 导航标题) —— nav 在 mkdocs.yml 中引用这些输出名
PAGES_ZH = [
    ("content/00-front/00-preface.md",           "00-front/preface.md",           "preface.md"),
    ("content/00-front/01-how-to-read.md",       "00-front/how-to-read.md",       "how-to-read.md"),
    ("content/01-ai/00-chapter.md",              "01-ai/00-chapter.md",           "p1.md"),
    ("content/01-ai/01-what-is-ai.md",           "01-ai/01-what-is-ai.md",        "1-1.md"),
    ("content/01-ai/02-three-schools.md",        "01-ai/02-three-schools.md",     "1-2.md"),
    ("content/01-ai/03-00-neural-networks.md",   "01-ai/03-00-neural-networks.md","1-3.md"),
    ("content/01-ai/03-01-neuron.md",            "01-ai/03-01-neuron.md",         "1-3-1.md"),
    ("content/01-ai/03-02-data-input.md",        "01-ai/03-02-data-input.md",     "1-3-2.md"),
    ("content/01-ai/03-03-learning.md",          "01-ai/03-03-learning.md",       "1-3-3.md"),
    ("content/01-ai/03-04-train-and-infer.md",   "01-ai/03-04-train-and-infer.md","1-3-4.md"),
    ("content/01-ai/04-00-machine-learning.md",  "01-ai/04-00-machine-learning.md","1-4.md"),
    ("content/01-ai/04-01-mlp-and-deep-learning.md","01-ai/04-01-mlp-and-deep-learning.md","1-4-1.md"),
    ("content/01-ai/04-02-paradigms.md",         "01-ai/04-02-paradigms.md",      "1-4-2.md"),
    ("content/01-ai/04-03-generalization.md",    "01-ai/04-03-generalization.md", "1-4-3.md"),
    ("content/01-ai/05-00-llms.md",              "01-ai/05-00-llms.md",           "1-5.md"),
    ("content/01-ai/05-01-scaling-laws.md",      "01-ai/05-01-scaling-laws.md",   "1-5-1.md"),
    ("content/01-ai/05-02-attention.md",         "01-ai/05-02-attention.md",      "1-5-2.md"),
    ("content/01-ai/05-03-ssm-and-linear-attention.md","01-ai/05-03-ssm-and-linear-attention.md","1-5-3.md"),
    ("content/01-ai/05-04-diffusion.md",         "01-ai/05-04-diffusion.md",      "1-5-4.md"),
    ("content/01-ai/06-alignment-hallucination-safety.md","01-ai/06-alignment-hallucination-safety.md","1-6.md"),
    ("content/01-ai/07-00-agents.md",            "01-ai/07-00-agents.md",         "1-7.md"),
    ("content/01-ai/07-01-harness.md",           "01-ai/07-01-harness.md",        "1-7-1.md"),
    ("content/01-ai/07-02-rsi-and-multi-agent.md","01-ai/07-02-rsi-and-multi-agent.md","1-7-2.md"),
    ("content/01-ai/07-03-mcp-skills-rag.md",    "01-ai/07-03-mcp-skills-rag.md", "1-7-3.md"),
    ("content/01-ai/08-compute-and-deployment.md","01-ai/08-compute-and-deployment.md","1-8.md"),
    ("content/02-dev/00-chapter.md",             "02-dev/00-chapter.md",          "p2.md"),
    ("content/02-dev/01-what-is-a-program.md",   "02-dev/01-what-is-a-program.md","2-1.md"),
    ("content/02-dev/02-git.md",                 "02-dev/02-git.md",              "2-2.md"),
    ("content/02-dev/03-ide-and-toolchain.md",   "02-dev/03-ide-and-toolchain.md","2-3.md"),
    ("content/02-dev/04-package-managers.md",    "02-dev/04-package-managers.md", "2-4.md"),
    ("content/02-dev/05-reproducibility.md",     "02-dev/05-reproducibility.md",  "2-5.md"),
    ("content/02-dev/06-declarative-os.md",      "02-dev/06-declarative-os.md",   "2-6.md"),
    ("content/02-dev/07-project-structure.md",   "02-dev/07-project-structure.md","2-7.md"),
    ("content/02-dev/08-licenses.md",            "02-dev/08-licenses.md",         "2-8.md"),
    ("content/90-back/00-glossary.md",           "90-back/glossary.md",           "glossary.md"),
]

# EN pages mirror ZH output paths under content/en (nav titles live in mkdocs-en.yml)
PAGES_EN = [("content/en/" + src.replace("content/", ""), out, title)
            for src, out, title in PAGES_ZH]

PAGES = PAGES_EN if LANG == "en" else PAGES_ZH

CITE = re.compile(r"\[@([A-Za-z0-9_]+)(?:[;,][^\]]*)?\]")

def main():
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    # 引用编号：按全书出现顺序
    order = []
    for src, _, _ in PAGES:
        text = (ROOT / src).read_text(encoding="utf-8")
        for key in CITE.findall(text):
            if key not in order:
                order.append(key)

    def renumber(text):
        return CITE.sub(lambda m: f"[{order.index(m.group(1)) + 1}]", text)

    # 锚点 → 所在页：把跨页链接 (#sec:x)/(#fig:x) 改写为 mkdocs 可解析的跨页链接
    anchor_page = {}
    for src, out, _ in PAGES:
        for m in re.finditer(r"\{#((?:sec|fig):[\w-]+)\}", (ROOT / src).read_text(encoding="utf-8")):
            anchor_page.setdefault(m.group(1), out)

    import os as _os


    def fix_links(text, out_path):
        # 纯字符串替换：](#aid) → ](相对页#aid)
        for aid, target in anchor_page.items():
            if target == out_path:
                continue  # 同页锚点保持原样
            rel = _os.path.relpath(target, _os.path.dirname(out_path))
            text = text.replace(f"](#{aid})", f"]({rel}#{aid})")
        # 图片相对路径按页面深度补 ../
        depth = out_path.count("/")
        if depth:
            text = text.replace("](figures/", "](" + "../" * depth + "figures/")
        return text

    # 复制页面
    for src, out, _ in PAGES:
        dst = DOCS / out
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(fix_links(renumber((ROOT / src).read_text(encoding="utf-8")), out), encoding="utf-8")

    # 参考文献页（按编号排序）
    bib = (ROOT / "bib" / "refs.bib").read_text(encoding="utf-8")
    entries = {}
    for m in re.finditer(r"@(\w+)\{([^,]+),\s*(.*?)\n\}", bib, re.S):
        kind, key, body = m.groups()
        title = re.search(r"title\s*=\s*[{\"](.+?)[}\"],?\s*\n", body, re.S)
        author = re.search(r"author\s*=\s*[{\"](.+?)[}\"],?\s*\n", body, re.S)
        year = re.search(r"year\s*=\s*[{\"]?(\d{4})", body)
        entries[key] = (title.group(1).replace("\n", " ").strip() if title else "(无题)",
                        (author.group(1).replace("\n", " ").strip() if author else ""),
                        year.group(1) if year else "")
    ref_title = "# References {.unnumbered}\n" if LANG == "en" else "# 参考文献 {.unnumbered}\n"
    lines = [ref_title]
    for i, key in enumerate(order, 1):
        t, a, y = entries.get(key, (("(missing entry)" if LANG == "en" else "缺失条目"), "", ""))
        lines.append(f"{i}. {a} *{t}* ({y})")
    (DOCS / "90-back" / "references.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 页脚版本号：与 release tag 一致（部署脚本核对并显示）
    try:
        ver = subprocess.run(["git", "describe", "--tags", "--abbrev=0"],
                             capture_output=True, text=True, cwd=str(ROOT)).stdout.strip()
    except Exception:
        ver = ""
    (DOCS / "version.txt").write_text(ver + "\n", encoding="utf-8")

    # 首页：README 以 <!-- en --> 分隔，中文站取前半，英文站取后半（单一语言）
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    zh_part, _, en_part = readme.partition("<!-- en -->")
    index = en_part if LANG == "en" else zh_part
    (DOCS / "index.md").write_text(renumber(index), encoding="utf-8")

    # 图：保持 figures/src/... 相对路径
    if LANG == "en":
        # EN markdown keeps the zh-style paths (figures/src/...); stage EN figures there.
        shutil.copytree(ROOT / "figures/en", DOCS / "figures/src", dirs_exist_ok=True)
    else:
        shutil.copytree(ROOT / "figures", DOCS / "figures", dirs_exist_ok=True)
    # MathJax 配置
    js = DOCS / "javascripts"
    js.mkdir(exist_ok=True)
    shutil.copy(ROOT / "build" / "javascripts" / "mathjax.js", js / "mathjax.js")

    print(f"site-src ready: {len(PAGES)} pages, {len(order)} references")

if __name__ == "__main__":
    sys.exit(main())
