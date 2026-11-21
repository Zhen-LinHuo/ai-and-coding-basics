-- Cross-references without pandoc-crossref.
-- Syntax in prose: a normal Markdown link whose target anchors a label,
--   [Figure 1-2](#fig:perceptron-sum)   [Section 1.2](#sec:three-schools)
-- LaTeX: the whole link becomes 图\ref{...} / 第\ref{...}节 -- the printed
-- number always follows the caption, never the text. Other formats keep the
-- link as-is (it already points at the anchor), so HTML degrades gracefully.
-- Labels follow the document language (meta.lang): zh-* -> 图/第…节, else Figure/Section.
local function labels()
  local lang = ""
  if PANDOC_DOCUMENT and PANDOC_DOCUMENT.meta and PANDOC_DOCUMENT.meta.lang then
    lang = pandoc.utils.stringify(PANDOC_DOCUMENT.meta.lang)
  end
  if lang:sub(1, 2) == "zh" then
    return { fig = "图", sec = "第", tab = "表", eq = "式" }, { sec = "节" }
  end
  return { fig = "Figure", sec = "Section", tab = "Table", eq = "Eq." }, { sec = "" }
end

function Link(el)
  local id, kind = el.target:match("^#((%a+):([%w%-_]+))$")
  if not id then return el end
  local prefix, suffix = labels()
  if not prefix[kind] then return el end
  if FORMAT ~= "latex" then return el end
  local out = prefix[kind] .. "\\ref{" .. id .. "}" .. (suffix[kind] or "")
  return pandoc.RawInline("latex", out)
end
