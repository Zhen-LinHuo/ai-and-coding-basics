#!/usr/bin/env bash
# Deploy the bilingual site: zh at the repo path root, en under /en/.
# (mkdocs gh-deploy alone cannot do this: the zh build cleans site/ and would
#  wipe the en/ subtree built by the en config. So we merge and push by hand.)
set -euo pipefail
cd "$(dirname "$0")/.."

mkdocs build --strict                      # -> site/
mkdocs build --strict -f mkdocs-en.yml     # -> site/en

WT=$(mktemp -d)
git worktree add --detach "$WT" gh-pages >/dev/null 2>&1 || {
  echo "worktree add failed"; exit 1; }
trap 'git worktree remove --force "$WT" >/dev/null 2>&1' EXIT

rsync -a --delete --exclude .git site/ "$WT"/
cd "$WT"
if [[ -n $(git status --porcelain) ]]; then
  git add -A
  git commit -q -m "Deploy bilingual site: zh at root, en under /en/"
  git push origin HEAD:gh-pages -q
  echo "deployed: $(git log -1 --format=%h) gh-pages"
else
  echo "no changes to deploy"
fi
