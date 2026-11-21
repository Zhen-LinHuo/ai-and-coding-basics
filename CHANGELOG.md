# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com).
The book text itself is versioned by release tags (SemVer).

## [Unreleased]

## [v0.2.0] — 2026-11-21

### Added
- British-English (en-GB) edition: full translation of all 35 sections,
  back matter and all 84 figures; separate PDF, single-page HTML and
  MkDocs build targets (`make pdf-en`, `make html-en`, `make site-en`)
- Bilingual website: Chinese edition at `/cn/`, English at `/en/`,
  language landing page at the root, header language switcher,
  footer previous/next section navigation on both editions
- Deterministic figure-layout checker (`scripts/check_fig_layout.py`) and
  auto-fixer (`scripts/fix_fig_layout.py`): text-text overlap, box overflow
  and out-of-canvas detection for all SVG figures, wired into the toolchain
- `CHANGELOG.md` (this file)

### Fixed
- Figure typography in both languages: removed all detected text overlaps,
  box overflows and out-of-canvas labels (Chinese 10 → 0, English 212 → 0
  findings); root causes included duplicate y-attributes on wrapped text
  elements and a stale site-source refresh in the deploy script
- SVG figures no longer contain cross-reference text ("Figure 1-3" style):
  numbers are edition-specific and links do not work inside images
- Heading level jumps that produced `x.y.0.z` section numbers in the PDF
- Missing-glyph issue: U+2075 rendered via maths notation instead
- English typographic names (Contents/Figure/Part) were being reset by
  ctex at `\begin{document}`; overrides now win the hook order

### Changed
- README is now bilingual (Chinese / English separated by a marker)
- References restyled with a single CSL (GB/T 7714-2015 numeric) for both
  languages; `REUSE.toml` replaces the deprecated `.reuse/dep5`
- Release workflow: CI lint-only on push; bilingual PDF/HTML built at
  release time; site deployed with `scripts/deploy-site.sh`
  (zh → `/cn/`, en → `/en/`, root redirect)

## [v0.1.0] — 2026-11-21

### Added
- First complete draft: Part 1 (foundations of AI, 1.1–1.8) and Part 2
  (computing and development basics, 2.1–2.8), 83 pages, ~40 figures,
  48 references
- Consistent six-beat section structure (intuition → analogy → diagram →
  problem it solves → built-in limitations → summary and self-check)
- Build pipeline: pandoc + LuaLaTeX PDF, single-page HTML, MkDocs Material
  site; four lint gates (emoji, section skeleton, bibliography,
  cross-references)
- Licensing: CC BY-SA 4.0 for text and figures, Apache-2.0 for code and
  build scripts (REUSE-compliant)
