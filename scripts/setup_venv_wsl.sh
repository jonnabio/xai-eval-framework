#!/bin/bash
# setup_venv_wsl.sh - Create a WSL/Linux venv and install project requirements.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

VENV_DIR="${VENV_DIR:-.venv-wsl}"
PYTHON="${PYTHON:-python3}"
REQUIREMENTS="${REQUIREMENTS:-requirements.txt}"

RECREATE=0
SKIP_INSTALL=0

usage() {
  cat <<'EOF'
Usage: bash scripts/setup_venv_wsl.sh [--recreate] [--no-install]

Environment variables:
  VENV_DIR       venv directory (default: .venv-wsl)
  PYTHON         python executable (default: python3)
  REQUIREMENTS   requirements file (default: requirements.txt)
EOF
}

while [ "${1:-}" != "" ]; do
  case "$1" in
    --recreate)
      RECREATE=1
      shift
      ;;
    --no-install)
      SKIP_INSTALL=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "[ERROR] Python not found: $PYTHON" >&2
  exit 1
fi

if [ ! -f "$REQUIREMENTS" ] && [ "$SKIP_INSTALL" -eq 0 ]; then
  echo "[ERROR] Requirements file not found: $REQUIREMENTS" >&2
  exit 1
fi

echo "=========================================================="
echo "WSL venv setup"
echo "Repo: $PROJECT_ROOT"
echo "Python: $PYTHON ($("$PYTHON" --version 2>/dev/null || true))"
echo "Venv: $VENV_DIR"
echo "Requirements: $REQUIREMENTS"
echo "=========================================================="

if [ "$RECREATE" -eq 1 ] && [ -d "$VENV_DIR" ]; then
  echo "[INFO] Removing existing venv: $VENV_DIR"
  rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO] Creating venv..."
  "$PYTHON" -m venv "$VENV_DIR"
else
  echo "[INFO] Venv already exists; skipping create."
fi

VENV_PY="$VENV_DIR/bin/python3"
if [ ! -x "$VENV_PY" ]; then
  VENV_PY="$VENV_DIR/bin/python"
fi

if [ ! -x "$VENV_PY" ]; then
  echo "[ERROR] Could not resolve venv python under $VENV_DIR/bin" >&2
  exit 1
fi

echo "[INFO] Upgrading pip..."
"$VENV_PY" -m pip install --upgrade pip >/dev/null

if [ "$SKIP_INSTALL" -eq 0 ]; then
  echo "[INFO] Installing requirements (this may take a while)..."
  "$VENV_PY" -m pip install -r "$REQUIREMENTS"
else
  echo "[INFO] Skipping requirements install (--no-install)."
fi

echo "[INFO] Verifying core imports..."
"$VENV_PY" - <<'PY'
import importlib
import sys

modules = [
    "numpy",
    "pandas",
    "sklearn",
    "xgboost",
    "shap",
    "lime",
    "alibi",
    "dice_ml",
    "yaml",
]

failed = []
for name in modules:
    try:
        importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001 - user-facing diagnostic
        failed.append((name, str(exc)))

if failed:
    print("FAILED IMPORTS:")
    for name, msg in failed:
        print(f"- {name}: {msg}")
    sys.exit(1)

print("OK: core imports succeeded")
PY

cat <<EOF
==========================================================
Ready.

Next commands:

  # Train EXP3 model artifacts
  $VENV_PY scripts/train_exp3_models.py

  # Run EXP3 managed runner (recommended)
  VENV_PYTHON=$VENV_PY bash scripts/managed_runner_exp3.sh
==========================================================
EOF
