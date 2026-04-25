# WSL Python Environment (Experiment Execution)

This guide defines the **WSL/Linux** Python environment baseline used for running
experiments (including EXP3).

## Why this matters

- A Python virtual environment created on **Windows** (e.g., `.venv` created from
  PowerShell) cannot be used reliably from **WSL** because the interpreter and
  compiled wheels differ.
- EXP3 uses `xgboost`, `shap`, `scikit-learn`, `pyyaml`, and `alibi` (Anchors);
  missing any of these typically fails late (during training or runner startup).

## Create a WSL venv

From the repository root in WSL:

```bash
bash scripts/setup_venv_wsl.sh
```

Defaults:

- venv path: `.venv-wsl`
- requirements: `requirements.txt`

Overrides:

```bash
VENV_DIR=.venv-wsl PYTHON=python3 REQUIREMENTS=requirements.txt bash scripts/setup_venv_wsl.sh
```

## Use the venv for EXP3

The EXP3 runner scripts accept `VENV_PYTHON`:

```bash
VENV_PYTHON=.venv-wsl/bin/python3 bash scripts/managed_runner_exp3.sh
```

## German Credit dataset download (OpenML)

The first time you train or run German Credit, OpenML downloads are required:

- dataset: `credit-g` (OpenML)
- cache location (default): `data/openml/`

If you want to prewarm the cache:

```bash
.venv-wsl/bin/python3 -c "from sklearn.datasets import fetch_openml; fetch_openml(name='credit-g', version=1, data_home='data/openml', as_frame=True)"
```

## Git push authentication in WSL (recommended)

If `git push` fails in WSL with:

```text
fatal: could not read Username for 'https://github.com': No such device or address
```

configure Windows Git Credential Manager (GCM) as the credential helper:

```bash
git config --global credential.helper /mnt/c/PROGRA~1/Git/mingw64/bin/git-credential-manager.exe
git push --dry-run
```

The first push will open an auth flow (browser/device login) and then WSL pushes
become non-interactive.
