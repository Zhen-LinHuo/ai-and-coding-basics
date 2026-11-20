-- Cross-references without pandoc-crossref.
-- Syntax in prose: a normal Markdown link whose target anchors a label,
--   [图 1-2](#fig:perceptron-sum)   [第 1.2 节](#sec:three-schools)
-- LaTeX: the whole link becomes 图\ref{...} / 第\ref{...}节 -- the printed
-- number always follows the caption, never the text. Other formats keep the
-- link as-is (it already points at the anchor), so HTML degrades gracefully.
local PREFIX = { fig = "图", sec = "第", tab = "表", eq = "式" }
local SUFFIX = { sec = "节" }

function Link(el)
  local id, kind = el.target:match("^#((%a+):([%w%-_]+))$")
  if not id or not PREFIX[kind] then return el end
  if FORMAT ~= "latex" then return el end
  local out = PREFIX[kind] .. "\\ref{" .. id .. "}" .. (SUFFIX[kind] or "")
  return pandoc.RawInline("latex", out)
end
