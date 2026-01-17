# Syncing Experiment Data for Production

## Problem
Experiment data (JSON results) generated on local workstations is often ignored by git to prevent repository bloat. However, for the XAI Dashboard on Render to visualize this data, the files **must be committed** to the repository.

## Solution

To sync experiment data (especially from `reproducibility` or `tuning` folders) from a workstation to production:

### 1. Update .gitignore (One-time)
Ensure `.gitignore` whitelists the deep paths. This is already done in `main`.
```gitignore
experiments/**/results/
!experiments/exp1_adult/reproducibility/**/results.json
!experiments/exp1_adult/results/tuning/**/results.json
!experiments/exp2_comparative/results/**/results.json
```

### 2. Force Add Files (On Data Workstation)
On the workstation containing the data (the "600 experiments"), run the following commands to force-track the files:

```bash
# Add reproducibility results (Deeply nested)
git add -f experiments/exp1_adult/reproducibility

# Add tuning results
git add -f experiments/exp1_adult/results/tuning

# Add comparative results
git add -f experiments/exp2_comparative/results
```
*Note: The `-f` (force) flag ensures files are added even if a broad ignore rule would otherwise exclude them.*

### 3. Verify and Push
Check that the count matches your expectations (e.g., ~600 new files):
```bash
git status --porcelain | wc -l
```

Commit and push:
```bash
git commit -m "data: Sync 600 experiment results for production"
git push origin main
```

### 4. Verify Production
Once pushed, Render will auto-deploy. Check the dashboard footer for "Experiments Loaded: 600".
