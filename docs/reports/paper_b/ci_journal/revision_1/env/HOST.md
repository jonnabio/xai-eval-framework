# Single recorded host for the Paper B revision runs (D-7)

Captured 2026-11-06 on the machine itself (`Win32_Processor`, `Win32_ComputerSystem`,
`Win32_OperatingSystem`, `powercfg`).

| Item | Value |
|---|---|
| Machine | ASUSTeK COMPUTER INC. ASUS TUF Gaming A15 FA506IH |
| CPU | AMD Ryzen 5 4600H with Radeon Graphics; 6 cores, 12 threads; base clock 3,000 MHz |
| RAM | 31.4 GB |
| OS | Microsoft Windows 11 Home 10.0.26300 |
| Power plan at capture | "ASUS Recommended" (GUID 956322ba-a6e8-46e7-be17-4fa9faa967c4). Plan for timing runs: fixed to one scheme, mains power, recorded in each run manifest |
| Python | CPython 3.11.11 (uv-managed), venv `.venv` (git-ignored) |
| Environment | `requirements-rev1-frozen.txt` (this folder) |

## Environment versus the paper's pinned environment

Core packages are **identical** to `requirements-frozen.txt` and to the versions stated in the
manuscript: scikit-learn 1.7.1, XGBoost 3.1.2, SHAP 0.50.0, LIME 0.2.0.1, NumPy 2.2.6, pandas
2.3.3, SciPy 1.16.3.

Added for Anchors and DiCE (`requirements.txt` lists them unpinned; the EXP2 runs recorded
no version):

- `alibi==0.9.6`, installed **without its dependency resolution** because it declares
  `numpy<2`, which would downgrade the pinned NumPy 2.2.6. Its remaining dependencies (spaCy
  3.8.18, transformers, dill, blis) were installed with NumPy, scikit-image, scikit-learn,
  pandas, SciPy, SHAP and XGBoost held at their pins. `AnchorTabular` passed a smoke test on
  NumPy 2.2.6 (fit + explain on a random forest).
- `dice-ml==0.12`.

**Disclosure for the paper:** the EXP2 Anchors and DiCE runs used unrecorded library
versions. Their re-timing (WP2-T) uses the versions above, so a timing difference may partly
reflect a library version.
