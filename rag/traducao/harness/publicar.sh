#!/usr/bin/env bash
# Implantação do projeto independente; nunca executar dentro do job de tradução.
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
project_dir=$(cd -- "$script_dir/../../.." && pwd)
cd -- "$project_dir"
git_root=$(git rev-parse --show-toplevel)
[[ "$git_root" == "$project_dir" && "$(basename -- "$project_dir")" == Inteligencia-SOT ]] || {
  echo 'Projeto de publicação inválido' >&2; exit 1;
}
[[ -f rag/traducao/harness/policy.json && ! -f AGENTS.md ]] || exit 1
[[ "$(git branch --show-current)" == main ]] || { echo 'Branch deve ser main' >&2; exit 1; }
[[ -z "$(git status --porcelain)" ]] || { echo 'Commitar alterações antes de publicar' >&2; exit 1; }
visibility=$(gh repo view Andraus35/Inteligencia-SOT --json isPrivate --jq .isPrivate)
[[ "$visibility" == true ]] || { echo 'Destino precisa ser privado' >&2; exit 1; }
destination=https://github.com/Andraus35/Inteligencia-SOT.git
if git remote get-url origin >/dev/null 2>&1; then
  [[ "$(git remote get-url origin)" == "$destination" ]] || { echo 'Origin divergente' >&2; exit 1; }
else
  git remote add origin "$destination"
fi
git push --set-upstream origin main
gh repo view Andraus35/Inteligencia-SOT --json nameWithOwner,isPrivate,url
