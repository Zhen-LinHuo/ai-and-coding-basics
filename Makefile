# ai-and-coding-basics — book build
#
# Everything runs inside the pinned Guix environment:
#   guix time-machine -C .guix/channels.scm -- shell -m .guix/manifest.scm -- make
SHELL := /bin/bash

BOOK  := ai-and-coding-basics
BUILD := build
OUT   := $(BUILD)/out
SRC   := $(sort $(shell find content -name '*.md'))

PDF   := $(OUT)/$(BOOK).pdf
HTML  := $(OUT)/index.html

PANDOC := pandoc
PFLAGS := \
  --from markdown+smart+pipe_tables+implicit_figures \
  --pdf-engine=latexmk --pdf-engine-opt=-lualatex \
  --listings \
  --toc --toc-depth=3 \
  --citeproc \
  --bibliography=bib/refs.bib \
  --csl=$(BUILD)/gb-t-7714-2015-numeric.csl \
  --lua-filter=$(BUILD)/xref.lua \
  --lua-filter=$(BUILD)/admonitions.lua \
  --lua-filter=$(BUILD)/inline-code-bg.lua \
  -H $(BUILD)/astra-doc-style.sty \
  --include-in-header=$(BUILD)/floats.tex \
  --metadata-file=$(BUILD)/metadata.yaml \
  -V colorlinks=true \
  -V papersize=a4 \
  -V toc-title="目录"

.PHONY: all pdf html lint check doctor clean

all: pdf

pdf: $(PDF)

FIGS := $(wildcard figures/src/*.svg)

$(PDF): $(SRC) $(FIGS) bib/refs.bib $(BUILD)/metadata.yaml $(BUILD)/astra-doc-style.sty
	@mkdir -p $(OUT)
	$(PANDOC) $(SRC) $(PFLAGS) -o $@
	@printf '%s: %s pages\n' "$@" "$$(pdfinfo $@ 2>/dev/null | awk '/^Pages:/{print $$2}')"

html: $(HTML)

$(HTML): $(SRC) bib/refs.bib $(BUILD)/metadata.yaml
	@mkdir -p $(OUT)
	$(PANDOC) $(SRC) --standalone --toc --toc-depth=3 --number-sections \
	  --citeproc --bibliography=bib/refs.bib --csl=$(BUILD)/gb-t-7714-2015-numeric.csl \
	  --metadata-file=$(BUILD)/metadata.yaml \
	  --lua-filter=$(BUILD)/xref.lua \
  --lua-filter=$(BUILD)/admonitions.lua \
	  --css=site.css -o $@
	@cp $(BUILD)/site.css $(OUT)/site.css

lint:
	@python3 scripts/lint_emoji.py
	@python3 scripts/lint_sections.py
	@python3 scripts/lint_bib.py
	@python3 scripts/lint_xref.py

check: lint pdf

doctor:
	@for c in pandoc lualatex rsvg-convert pdfinfo; do \
	  printf '%-14s ' "$$c"; command -v $$c >/dev/null && echo ok || echo MISSING; \
	done

clean:
	rm -rf $(OUT)
