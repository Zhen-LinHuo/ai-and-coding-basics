-- inline-code-bg.lua — Pandoc Lua filter for inline code background
-- Converts `Code` inline elements (backtick code) to \icode{...}
-- for GitHub-style gray background with monospace font.
-- Requires: \icode command defined in .sty (colorbox + texttt)
-- Usage: pandoc input.md -o output.pdf --lua-filter=inline-code-bg.lua ...
--
-- REVISION HISTORY
--   v2 (2026-06-06): SOH placeholder pattern for brace escaping;
--     \~{} instead of \textasciitilde{} (CJK font-safe);
--     \textunderscore{} instead of \_ (no math-mode leak);
--     \allowbreak{} after / for long-path wrapping;
--     %$#& escaping after \ substitution to keep \& intact.
--   v1 (2026-06-04): Initial version — basic escaping with \textasciitilde,
--     \{/\} via set pattern, \textbackslash, \textasciicircum.
--
-- Inline-code background filter (vendored snapshot; see build/VENDOR.md).

function Code(elem)
  local text = elem.text

  -- Step 1: protect original braces with SOH placeholders (before any LaTeX commands)
  local LB, RB = "\1LB\1", "\1RB\1"  -- SOH-delimited, cannot appear in normal text
  text = text:gsub("{", LB)
  text = text:gsub("}", RB)

  -- Step 2: escape LaTeX special characters
  text = text:gsub("\\", "\\textbackslash{}")
  text = text:gsub("_", "\\textunderscore{}")
  text = text:gsub("%^", "\\textasciicircum{}")
  text = text:gsub("~", "\\~{}")
  text = text:gsub("([%%$#&])", "\\%1")    -- %/$/#/& — AFTER backslash to keep \& intact

  -- Step 3: line-break opportunities after path separators
  text = text:gsub("/", "/\\allowbreak{}")

  -- Step 4: restore original braces as escaped LaTeX
  text = text:gsub(LB, "\\{")
  text = text:gsub(RB, "\\}")

  return pandoc.RawInline("latex", "\\icode{" .. text .. "}")
end
