#!/usr/bin/env bash
# 发版：本地构建双语 PDF + HTML，打签名 tag，上传 Release，再把资产读回来校验。
#
# 用法（必须经 Guix 环境，否则 pandoc/lualatex 不在 PATH）：
#   guix time-machine -C .guix/channels.scm -- shell -m .guix/manifest.scm -- \
#     scripts/release.sh v0.2.0
#
# 为什么不用 CI 造 PDF：公网冷拉取的空 store 会触发 Guix 全源码 bootstrap
# （gcc-mesboot0 2.95.3 起，以天计），实测不可行。本地 25 秒。CI 只做 lint。
# 校验纪律不因此放松——第 7 步照做。
set -euo pipefail

VERSION="${1:-}"
REPO="Zhen-LinHuo/ai-and-coding-basics"
OUT="build/out"
# 只发 PDF：网页版由 GitHub Pages 承载，单文件 HTML 不构成有意义的交付
ASSETS=(
  "$OUT/ai-and-coding-basics.pdf"
  "$OUT/ai-and-coding-basics-en.pdf"
)

fail() { echo "release: $*" >&2; exit 1; }

[[ -n "$VERSION" ]] || fail "用法: scripts/release.sh vX.Y.Z"
[[ "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail "版本号须形如 vX.Y.Z，实为 $VERSION"

# 1. 工作区必须干净：发出去的东西要能被这个 commit 完整解释
[[ -z "$(git status --porcelain)" ]] || fail "工作区有未提交改动，先提交或 stash"

# 2. 构建并自检
echo "== 构建 =="
make check

# 3. 资产齐全
for a in "${ASSETS[@]}"; do
  [[ -s "$a" ]] || fail "缺产物 $a，先 make pdf pdf-en html html-en"
done

# 4. tag：已存在就核对，不存在就现场签
if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null; then
  echo "== tag $VERSION 已存在，核对签名 =="
  git tag -v "$VERSION" 2>&1 | grep -q 'Good signature' || fail "tag $VERSION 没有有效签名"
else
  echo "== 创建签名 tag $VERSION =="
  git tag -s "$VERSION" -m "release $VERSION"
  git push origin "$VERSION"
fi

# 5. 发布说明：从 CHANGELOG.md 取对应版本小节
NOTES="$(mktemp)"
awk -v ver="$VERSION" '
  $0 ~ "^## \\[" ver "\\]" { flag = 1; next }
  /^## \[/ && flag { exit }
  flag { print }
' CHANGELOG.md > "$NOTES"
[[ -s "$NOTES" ]] || fail "CHANGELOG.md 里没有 $VERSION 小节"
# GitHub 把单个换行和行尾双空格都渲染成硬换行——段内折行合并回一行，
# 并剥掉行首空白（条目行与空行保留）
sed -E 's/[[:space:]]+$//' "$NOTES" | awk '
  { sub(/^[[:space:]]+/, "") }
  /^- |^#|^$/ { if (buf != "") print buf; buf = ""; print; next }
  { buf = buf (buf == "" ? "" : " ") $0 }
  END { if (buf != "") print buf }
' ＞ "$NOTES.joined"
mv "$NOTES.joined" "$NOTES"

# 6. 上传
echo "== 上传 Release =="
if gh release view "$VERSION" --repo "$REPO" >/dev/null 2>&1; then
  gh release upload "$VERSION" "${ASSETS[@]}" --clobber --repo "$REPO"
  gh release edit "$VERSION" --notes-file "$NOTES" --repo "$REPO"
else
  gh release create "$VERSION" "${ASSETS[@]}" --notes-file "$NOTES" \
    --repo "$REPO" --verify-tag --title "$VERSION"
fi

# 7. 回读校验——不核对回读，等于不知道发出去的是什么
echo "== 回读校验 =="
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP" "$NOTES"' EXIT
gh release download "$VERSION" --repo "$REPO" --pattern '*' --dir "$TMP"
ok=1
for a in "${ASSETS[@]}"; do
  name="$(basename "$a")"
  local_sum="$(sha256sum "$a" | awk '{print $1}')"
  remote_sum="$(sha256sum "$TMP/$name" | awk '{print $1}')"
  echo "$name"
  echo "  local : $local_sum"
  echo "  remote: $remote_sum"
  [[ "$local_sum" == "$remote_sum" ]] || { echo "  资产与本地构建不一致!"; ok=0; }
done
[[ "$ok" == 1 ]] || fail "回读校验失败"
pdfinfo "$TMP/$(basename "${ASSETS[0]}")" | awk '/^Pages:/{print "pages (zh):", $2}'
pdfinfo "$TMP/$(basename "${ASSETS[1]}")" | awk '/^Pages:/{print "pages (en):", $2}'
echo "== release $VERSION 完成 =="
