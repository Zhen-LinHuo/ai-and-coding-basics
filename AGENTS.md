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

PDF 一律本地构建，CI 只做 lint。理由不是懒：公网冷拉取 Guix 工具链实测 40 分钟以上，
本地 25 秒。

```sh
guix time-machine -C .guix/channels.scm -- shell -m .guix/manifest.scm -- \
  scripts/release.sh vX.Y.Z
```

`scripts/release.sh` 依次做五件事，其中第 5 步不可省：

1. 检查工作区干净；2. `make check`；3. 签名 tag（已存在则核对签名）；4. 上传 Release；
5. **把资产下载回来比对 SHA256**——不核对回读，等于不知道发出去的是什么。

## 硬规则

1. **禁用 emoji。** `scripts/lint_emoji.py` 会拦截。理由是排版的 emoji 支持是可选插件：
   一旦引入，每个输出格式都要单独兜底，PDF 里还容易出现缺字方块。
2. **配色只用 Okabe–Ito 八色**，且任何靠颜色承载的信息必须同时用形状或标签冗余编码。
3. **每节按「六拍」写**：一句话直觉、生活类比、示意图、它解决什么问题、**它的天然短板**、
   小结与自检。第五拍不是可选段落，且必须从原理推出，不许写"目前还不够成熟"。
   「常见误解」callout 是第五拍的默认呈现方式，若误解已在正文辟清可省略
   （`lint_sections` 只提示不拦截）。
4. **公式只出现在节末「数学注解」**。正文不依赖公式也能读懂；做不到就是没讲清楚。
5. **事实必须有引用**。模型名、榜单、价格这类时效内容只进带日期的注记框，不进正文叙述。
6. **单节上限 11 页**。超了就往「数学注解」里挪，或者另立一节。
7. 术语首次出现给中英并列，例如「梯度下降（gradient descent）」。
8. **图题与编号交给 LaTeX。** 图题写在图片替代文字里，是**标题式的短语**，不是一句话——
   解释放进正文。编号由 LaTeX 自动生成（"图 1-2"式），不要手写编号；
   `build/floats.tex` 已设 `[H]` 让图停在写它的地方。写法：

   ```
   ![标题短语](figures/src/xx.svg){#fig:简短名}
   ```
9. **交叉引用必须用引用，不写死编号。** 写成指向锚点的普通链接，由
   `build/xref.lua` 在 LaTeX 输出里升级为 `\ref`（编号永远跟随图题/节号）：

   ```
   见[图 1-2](#fig:简短名)；详见[第 1.3.3 节](#sec:目标节)。
   ```

   不要用裸 `@fig:x`——那是 pandoc 的行内引用语法，会被 citeproc 抢走。
   新增锚点后跑 `make lint`，`scripts/lint_xref.py` 会核对每个引用都有归宿。
10. **数学/正文里的负号用 ASCII 连字符 `-`，不用 U+2212**：Fandol 字体没有这个字形，会静默掉字。
11. **移除即无痕。** 这是面向交付、面向他人阅读的产物，不是台帐：删掉一个示例、
    一个术语或一个部件时，所有相关行——引用它的句子、给它的伏笔、"下文会讲"的
    承诺——都要一并清掉，让那里读起来像一开始就没有它。`git grep` 是最低限度的自检。

## 变更

- 增删章节、改动编号：先改 `OUTLINE.md`，再动 `content/`。两者不一致时以 `OUTLINE.md` 为准。
- `OUTLINE.md`、`.guix/`、`build/book-style.sty` 属于受保护文件，修改前须所有者批准。
- 提交信息用中文，标题写"做了什么"，不写"改了哪几个文件"。

## Git

身份与签名键见 `AGENTS.local.md`，使用 repo-local 配置，不依赖全局 gitconfig。
推送前须所有者过目；标签只在发版时打，且必须签名。

## 已知缺口

- `pandoc-crossref` 不在 Guix 里（`guix search` 无结果），交叉引用的实现方案待定。
  在方案确定前，正文引用图表一律写明"见第 X 节图 Y"的绝对文字，不依赖自动编号。
