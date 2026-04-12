#!/usr/bin/env bash
set -euo pipefail

# Safely sync worker result branches into main without rebasing or force pushing.
# - Runs in a temporary worktree on origin/main
# - Limits updates to result paths
# - Additive-only: skips files that already exist in main

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

TARGET_BRANCH="main"
REMOTE="origin"
MODE="apply" # apply|dry-run

WORKER_BRANCHES=(
  "results/jonaasusrog"
  "results/jon_asus"
)

SYNC_PATHS=(
  "experiments/exp2_scaled/results"
  "experiments/exp2_scaled/worker_manifests"
)

usage() {
  cat <<'EOF'
Usage: scripts/sync_worker_results_to_main.sh [--dry-run] [--worker <branch>]...

Options:
  --dry-run          Preview what would be synced without committing
  --worker <branch>  Add worker branch (example: results/workstation-a)
  --help             Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      MODE="dry-run"
      shift
      ;;
    --worker)
      [[ $# -lt 2 ]] && { echo "Missing value for --worker"; exit 1; }
      WORKER_BRANCHES+=("$2")
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

declare -A seen
deduped=()
for b in "${WORKER_BRANCHES[@]}"; do
  if [[ -z "${seen[$b]+x}" ]]; then
    deduped+=("$b")
    seen[$b]=1
  fi
done
WORKER_BRANCHES=("${deduped[@]}")

if [[ ${#WORKER_BRANCHES[@]} -eq 0 ]]; then
  echo "No worker branches configured."
  exit 1
fi

ts="$(date +%Y%m%d_%H%M%S)"
tmpdir="$REPO_ROOT/.tmp_main_sync_$ts"
sync_branch="sync/results-to-main-$ts"

cleanup() {
  git worktree remove "$tmpdir" --force >/dev/null 2>&1 || true
  git branch -D "$sync_branch" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "[SYNC] Fetching latest refs from $REMOTE"
git fetch "$REMOTE" --prune

echo "[SYNC] Creating isolated worktree at $tmpdir"
git worktree add -B "$sync_branch" "$tmpdir" "$REMOTE/$TARGET_BRANCH" >/dev/null

cd "$tmpdir"

declare -i staged_total=0

for worker in "${WORKER_BRANCHES[@]}"; do
  remote_ref="$REMOTE/$worker"
  if ! git rev-parse --verify "$remote_ref" >/dev/null 2>&1; then
    echo "[WARN] Skipping missing branch: $remote_ref"
    continue
  fi

  echo "[SYNC] Scanning $remote_ref"
  for path in "${SYNC_PATHS[@]}"; do
    while IFS= read -r file; do
      [[ -z "$file" ]] && continue
      if git cat-file -e "HEAD:$file" 2>/dev/null; then
        continue
      fi

      if [[ "$MODE" == "dry-run" ]]; then
        echo "  + $file (from $worker)"
        staged_total+=1
      else
        git checkout "$remote_ref" -- "$file"
        staged_total+=1
      fi
    done < <(git ls-tree -r --name-only "$remote_ref" -- "$path")
  done
done

if [[ "$MODE" == "dry-run" ]]; then
  echo "[DRY-RUN] Files that would be added: $staged_total"
  exit 0
fi

if git diff --cached --quiet; then
  echo "[SYNC] No new files to sync."
  exit 0
fi

commit_msg="Sync worker result files into main ($ts)"
git commit -m "$commit_msg" >/dev/null

echo "[SYNC] Created commit: $(git rev-parse --short HEAD)"
echo "[SYNC] Pushing to $REMOTE/$TARGET_BRANCH"
git push "$REMOTE" "HEAD:$TARGET_BRANCH"
echo "[SYNC] Complete."