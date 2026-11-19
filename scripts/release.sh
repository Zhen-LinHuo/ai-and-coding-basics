#!/usr/bin/env bash
# 发版：本地构建 PDF，打签名 tag，上传 Release，再把资产读回来校验。
#
# 用法（必须经 Guix 环境，否则 pandoc/lualatex 不在 PATH）：
#   guix time-machine -C .guix/channels.scm -- shell -m .guix/manifest.scm -- \
#     scripts/release.sh v0.1.0
#
# 为什么不用 CI 造 PDF：公网冷拉取 Guix 工具链实测 40 分钟以上，
# 本地 25 秒。CI 只做 lint。校验纪律不因此放松——第 5 步照做。
set -euo pipefail

VERSION="${1:-}"
PDF="build/out/ai-and-coding-basics.pdf"
REPO="Zhen-LinHuo/ai-and-coding-basics"

fail() { echo "release: $*" >&2; exit 1; }

[[ -n "$VERSION" ]] || fail "用法: scripts/release.sh vX.Y.Z"
[[ "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail "版本号须形如 vX.Y.Z，实为 $VERSION"

# 1. 工作区必须干净：发出去的东西要能被这个 commit 完整解释
[[ -z "$(git status --porcelain)" ]] || fail "工作区有未提交改动，先提交或 stash"

# 2. 构建并自检
echo "== 构建 =="
make check

# 3. tag：已存在就核对，不存在就现场签
if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null; then
  echo "== tag $VERSION 已存在，核对签名 =="
  git tag -v "$VERSION" 2>&1 | grep -q 'Good signature' || fail "tag $VERSION 没有有效签名"
else
  echo "== 创建签名 tag $VERSION =="
  git tag -s "$VERSION" -m "release $VERSION"
  git push origin "$VERSION"
fi

# 4. 上传
echo "== 上传 Release =="
if gh release view "$VERSION" --repo "$REPO" >/dev/null 2>&1; then
  gh release upload "$VERSION" "$PDF" --clobber --repo "$REPO"
else
  gh release create "$VERSION" "$PDF" --repo "$REPO" --verify-tag --generate-notes
fi

# 5. 回读校验——不核对回读，等于不知道发出去的是什么
echo "== 回读校验 =="
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
gh release download "$VERSION" --repo "$REPO" --pattern '*.pdf' --dir "$TMP"
local_sum="$(sha256sum "$PDF" | awk '{print $1}')"
remote_sum="$(sha256sum "$TMP"/*.pdf | awk '{print $1}')"
echo "local : $local_sum"
echo "remote: $remote_sum"
[[ "$local_sum" == "$remote_sum" ]] || fail "资产与本地构建不一致"
pdfinfo "$TMP"/*.pdf | awk '/^Pages:/{print "pages:", $2}'
echo "release: $VERSION 完成"
