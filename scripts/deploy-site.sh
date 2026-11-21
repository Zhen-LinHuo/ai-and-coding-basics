#!/usr/bin/env bash
# Deploy the bilingual site: zh at the repo path root, en under /en/.
# (mkdocs gh-deploy alone cannot do this: the zh build cleans site/ and would
#  wipe the en/ subtree built by the en config. So we merge and push by hand.)
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/build-site.py              # refresh site-src (content + figures)
python3 scripts/build-site.py --lang en    # refresh site-src-en
mkdocs build --strict                      # -> site/cn
mkdocs build --strict -f mkdocs-en.yml     # -> site/en

WT=$(mktemp -d)
git fetch origin gh-pages -q
git worktree add --detach "$WT" origin/gh-pages >/dev/null 2>&1 || {
  echo "worktree add failed"; exit 1; }
trap 'git worktree remove --force "$WT" >/dev/null 2>&1' EXIT

# root: language landing page (redirect to the Chinese edition)
cat > "$WT/index.html" <<'HTML'
<!doctype html><meta charset="utf-8">
<title>AI and Computing, from First Principles</title>
<meta http-equiv="refresh" content="0; url=cn/">
<p><a href="cn/">中文</a> · <a href="en/">English</a></p>
HTML
rsync -a --delete --exclude .git site/cn/ "$WT/cn"/
mkdir -p "$WT/en"
rsync -a --delete site/en/ "$WT/en"/
cd "$WT"
if [[ -n $(git status --porcelain) ]]; then
  git add -A
  git commit -q -m "Deploy bilingual site: zh at root, en under /en/"
  git push origin HEAD:gh-pages -q
  echo "deployed: $(git log -1 --format=%h) gh-pages"
else
  echo "no changes to deploy"
fi
