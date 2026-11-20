;; 构建环境清单。镜像只提供 guix 二进制，TeX 由这里提供。
;;
;; TeX 用的是逐包最小集（替代 texlive-scheme-full 的数 GB）。
;; 新增依赖时：book-style.sty 里每出现一个 \usepackage，
;; 就要在下面补对应包；缺了会在构建时报 "File not found"，按名字补即可。
(specifications->manifest
 (list "pandoc"                 ; Markdown -> PDF/HTML
       "librsvg"                ; rsvg-convert：pandoc 靠它把 SVG 塞进 PDF
       "poppler"                ; pdfinfo
       "make" "python"
       "tar" "gzip" "zstd"      ; actions/cache 在容器里解包要用

       ;; LaTeX 最小集
       "texlive-luatex"         ; 引擎本体
       "texlive-collection-langchinese"   ; 中文：ctex、zhnumber、fandol 等
       "texlive-luatexja"       ; sty 里的 luatexja-fontspec
       "texlive-collection-latexrecommended" ; booktabs/longtable/graphics 等常用
       "texlive-xcolor" "texlive-titlesec" "texlive-titling" "texlive-fancyhdr"
       "texlive-listings" "texlive-caption" "texlive-float" "texlive-enumitem"
       "texlive-setspace" "texlive-mdframed" "texlive-environ" "texlive-geometry"
       "texlive-tocloft" "texlive-hyperref" "texlive-luacolor" "texlive-lua-ul"))
