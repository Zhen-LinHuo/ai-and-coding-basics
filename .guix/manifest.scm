;; 构建环境清单。镜像只提供 guix 二进制，TeX 由这里提供。
(specifications->manifest
 (list "pandoc"              ; Markdown -> PDF/HTML
       "texlive-scheme-full" ; lualatex、ctex、booktabs、mdframed、Fandol 中文字体
       "librsvg"             ; 提供 rsvg-convert：pandoc 靠它把 SVG 塞进 PDF
       "poppler"             ; pdfinfo
       "make"
       "python"))            ; scripts/ 下的 lint
