# AGENTS.md

本仓库是一本书的源文件，不是软件项目。以下约定对所有者与所有智能体同等生效。

## 真源

| 事项 | 真源 |
|:--|:--|
| 章节结构、每节三问、页数预算、图清单 | `OUTLINE.md` |
| 构建环境 | `.guix/channels.scm` + `.guix/manifest.scm` |
| 参考文献 | `bib/refs.bib` |
| 版式与过滤器 | `build/`（vendored 快照，见 `build/VENDOR.md`） |

## 构建

不依赖宿主环境，一律经 Guix：

```sh
guix time-machine -C .guix/channels.scm -- shell -m .guix/manifest.scm -- make check
```

目标：`doctor`（查工具）、`lint`、`pdf`、`html`、`check`（lint + pdf）、`clean`。

## 发版

PDF 默认本地构建；CI 只在打 tag 时构建一次发版 PDF（`release.yml`）。冷拉取约 5 GB，
大头是 pandoc 的 Haskell 闭包（TeX 已瘦身为逐包最小集），一次十几分钟，发版频率低，可接受：

1. 本地跑通 `check`；
2. 打签名 tag：`git tag -s vX.Y.Z`（SemVer，必须高于已有最大 tag）；
3. `gh release create vX.Y.Z build/out/ai-and-coding-basics.pdf --verify-tag`；
4. **回读校验**：从 Release 下载资产，SHA256 与本地比对一致才算发完。
   第 4 步不能省——不核对回读，等于不知道发出去的是什么。

查环境能不能拉起来而不真去下载，用

```sh
guix time-machine -C .guix/channels.scm -- build -m .guix/manifest.scm --dry-run
```

它会把结果分成 "would be downloaded"（有替代品，快）和 "would be built"（要从源码编，
先怀疑频道钉错或缓存未同步）。texlive-scheme-full 体积数 GB，首次拉取慢属正常。

**构建只发生在 `guix shell` 里，宿主环境不参与。** 宿主的工具链即使碰巧能用，也是
不可复现的：它依赖本机 profile 的内容和 `GUIX_LOCPATH` 这类只在 profile 里才有的变量
（缺了它 lualatex 会报 `Unable to read locale data` 直接退出，看起来像工具链坏了）。

## 硬规则

1. **禁用 emoji。** `scripts/lint_emoji.py` 会拦截。理由是排版的 emoji 支持是可选插件：
   一旦引入，每个输出格式都要单独兜底，PDF 里还容易出现缺字方块。
2. **配色只用 Okabe–Ito 八色**，且任何靠颜色承载的信息必须同时用形状或标签冗余编码。
3. **每节按「六拍」写**：一句话直觉、生活类比、示意图、它解决什么问题、**它的天然短板**、
   小结与自检。第五拍不是可选段落，且必须从原理推出，不许写"目前还不够成熟"。
4. **公式只出现在节末「数学注解」**。正文不依赖公式也能读懂；做不到就是没讲清楚。
5. **事实必须有引用**。模型名、榜单、价格这类时效内容只进带日期的注记框，不进正文叙述。
6. **单节上限 11 页**。超了就往「数学注解」里挪，或者另立一节。
7. 术语首次出现给中英并列，例如「梯度下降（gradient descent）」。
8. 「常见误解」写成两段，标题与正文之间留一个空引用行，否则标题会和正文挤在一行：

   ```
   > **常见误解**
   >
   > 正文。
   ```

## 变更

- 增删章节、改动编号：先改 `OUTLINE.md`，再动 `content/`。两者不一致时以 `OUTLINE.md` 为准。
- `OUTLINE.md`、`.guix/`、`build/astra-doc-style.sty` 属于受保护文件，修改前须所有者批准。
- 提交信息用中文，标题写"做了什么"，不写"改了哪几个文件"。

## Git

身份与签名键见 `AGENTS.local.md`，使用 repo-local 配置，不依赖全局 gitconfig。
推送前须所有者过目；标签只在发版时打，且必须签名。

## 已知缺口

- `pandoc-crossref` 不在 Guix 里（`guix search` 无结果），交叉引用的实现方案待定。
  在方案确定前，正文引用图表一律写明"见第 X 节图 Y"的绝对文字，不依赖自动编号。
