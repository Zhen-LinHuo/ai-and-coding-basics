# ai-and-coding-basics — book build
#
# Everything runs inside the pinned Guix environment:
#   guix time-machine -C .guix/channels.scm -- shell -m .guix/manifest.scm -- make
SHELL := /bin/bash

BOOK  := ai-and-coding-basics
BUILD := build
OUT   := $(BUILD)/out
SRC   := $(sort $(shell find content -name '*.md' -not -path 'content/en/*'))

PDF   := $(OUT)/$(BOOK).pdf
MDS_EN := $(shell find content/en -name '*.md' 2>/dev/null)
HTML  := $(OUT)/index.html

PANDOC := pandoc
PFLAGS := \
  --from markdown+smart+pipe_tables+implicit_figures \
  --pdf-engine=latexmk --pdf-engine-opt=-lualatex \
  --listings \
  --toc --toc-depth=3 \
  --citeproc \
  --bibliography=bib/refs.bib \
  --lua-filter=$(BUILD)/xref.lua \
  --lua-filter=$(BUILD)/admonitions.lua \
  --lua-filter=$(BUILD)/inline-code-bg.lua \
  -H $(BUILD)/book-style.sty \
  --include-in-header=$(BUILD)/floats.tex \
  --metadata-file=$(BUILD)/metadata.yaml \
  -V colorlinks=true \
  -V papersize=a4

.PHONY: all pdf html lint check doctor clean figures-en pdf-en html-en site-en lint-en

all: pdf

pdf: $(PDF)

FIGS := $(wildcard figures/src/*.svg)

$(PDF): $(SRC) $(FIGS) bib/refs.bib $(BUILD)/metadata.yaml $(BUILD)/book-style.sty $(BUILD)/xref.lua $(BUILD)/floats.tex
	@mkdir -p $(OUT)
	$(PANDOC) $(SRC) $(PFLAGS) --csl=$(BUILD)/gb-t-7714-2015-numeric.csl -V toc-title="目录" -o $@
	@printf '%s: %s pages\n' "$@" "$$(pdfinfo $@ 2>/dev/null | awk '/^Pages:/{print $$2}')"

html: $(HTML)

# ---- English edition (en-GB) ----
# Staged build: content/en + figures/en presented as content/ + figures/src,
# so the EN markdown keeps the same image paths as the ZH edition.
EN_STAGE := $(BUILD)/en-stage
PDF_EN   := $(OUT)/$(BOOK)-en.pdf
HTML_EN  := $(OUT)/$(BOOK)-en.html
PFLAGS_EN := $(PFLAGS) --metadata-file=$(BUILD)/metadata-en.yaml \
  --include-in-header=$(BUILD)/floats-en.tex -V toc-title="Contents" \
  --csl=$(BUILD)/harvard-cite-them-right.csl

.PHONY: figures-en pdf-en html-en site-en lint-en

figures-en:
	python3 scripts/build-figures-en.py

en-stage:
	@mkdir -p $(EN_STAGE)/figures
	@ln -sfn $(CURDIR)/content/en $(EN_STAGE)/content
	@ln -sfn $(CURDIR)/figures/en $(EN_STAGE)/figures/src
	@ln -sfn $(CURDIR)/bib $(EN_STAGE)/bib
	@ln -sfn $(CURDIR)/build $(EN_STAGE)/build

pdf-en: $(PDF_EN)

$(PDF_EN): en-stage $(MDS_EN) $(FIGS_EN) bib/refs.bib $(BUILD)/metadata-en.yaml $(BUILD)/floats-en.tex $(BUILD)/xref.lua
	@mkdir -p $(OUT)
	cd $(EN_STAGE) && $(PANDOC) $$(find -L content -name '*.md' | sort) $(PFLAGS_EN) -o $(CURDIR)/$@
	@printf '%s: %s pages\n' "$@" "$$(pdfinfo $@ 2>/dev/null | awk '/^Pages:/{print $$2}')"

html-en: $(HTML_EN)

$(HTML_EN): en-stage $(MDS_EN) $(FIGS_EN) bib/refs.bib
	@mkdir -p $(OUT)
	cd $(EN_STAGE) && $(PANDOC) $$(find -L content -name '*.md' | sort) --standalone --toc --toc-depth=3 \
	  --number-sections --mathml --citeproc --bibliography=bib/refs.bib \
	  --csl=build/gb-t-7714-2015-numeric.csl --metadata-file=build/metadata-en.yaml \
	  --lua-filter=build/xref.lua --lua-filter=build/admonitions.lua \
	  -V toc-title="Contents" --css=site.css -o $(CURDIR)/$@
	@cp $(BUILD)/site.css $(OUT)/site.css

site-en:
	python3 scripts/build-site.py --lang en
	mkdocs build --strict -f mkdocs-en.yml

lint-en:
	@python3 scripts/lint_en.py

site:
	python3 scripts/build-site.py
	mkdocs build --strict

site-deploy: site
	./scripts/deploy-site.sh

$(HTML): $(SRC) bib/refs.bib $(BUILD)/metadata.yaml
	@mkdir -p $(OUT)
	$(PANDOC) $(SRC) --standalone --toc --toc-depth=3 --number-sections --mathml \
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
