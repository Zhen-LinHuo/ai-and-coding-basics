# Vendored files

不要就地修改：改上游，再按本表同步。

| 文件 | 说明 | 同步方式 |
|:--|:--|:--|
| `book-style.sty` | LaTeX 版式（标题、页眉页脚、callout、表格斑马纹、图题） | 覆盖复制 |
| `admonitions.lua` | 把 Markdown 引用块转成 sty 里的 callout 环境 | 覆盖复制 |
| `inline-code-bg.lua` | 行内代码底色 | 覆盖复制 |
| `gb-t-7714-2015-numeric.csl` | 参考文献样式（GB/T 7714-2015 数字制） | 下载快照 |

`gb-t-7714-2015-numeric.csl` 固定为快照：引用样式若跟着上游漂移，全书文献表会重排，
属不可接受的噪声。其余三个文件来自同一套版式，改动需与 `build/floats.tex` 一起验证。
