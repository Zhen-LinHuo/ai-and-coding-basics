# Vendored files

不要就地修改，改上游技能后再同步。

| 文件 | 来源 | 同步方式 |
|:--|:--|:--|
| `astra-doc-style.sty` | document-factory 技能 `templates/` | 复制 |
| `admonitions.lua` | document-factory 技能 `scripts/` | 复制 |
| `inline-code-bg.lua` | document-factory 技能 `scripts/` | 复制 |
| `ieee.csl` | citation-style-language/styles `ieee.csl` | 下载快照 |

`ieee.csl` 固定为快照：引用格式突然变化会让全书文献表重排，属于不可接受的噪声。
