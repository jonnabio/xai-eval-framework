#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

python3 scripts/pubs/generate_fragments.py
python3 scripts/pubs/verify_sync.py

if command -v quarto >/dev/null 2>&1; then
  (cd thesis && quarto clean && quarto render --to docx --cache-refresh)
else
  echo "WARN: quarto not found; skipping thesis render"
fi

echo "DONE"

