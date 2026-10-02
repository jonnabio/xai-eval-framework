# Zenodo release for the PeerJ CS submission

PeerJ requires a DOI archive holding an **exact copy** of the code and data the study used. A
GitHub link is not enough. The current snapshot `10.5281/zenodo.21538180` (commit `553f65d71`)
predates EXP4 cohort 2 and EXP6, so it does not qualify. Make a new **version** of the same
Zenodo record, so the concept DOI keeps every version together.

Only the author can do this: it publishes under your Zenodo account and cannot be undone.

## Before you start

1. The retarget branch `paper/bc-peerj-cs` is merged and green: `verify_claims.py`,
   `verify_sync.py`, `verify_exp4_reconstruction.py`, `scan_shared_literals.py --strict`.
2. Run `python scripts/pubs/verify_claims.py` **from a fresh clone** (RCA-001: cited artifacts
   must be tracked, not just present on disk).
3. `.zenodo.json` and `CITATION.cff` are updated (version `0.3.0`, affiliation spelling). Done
   on this branch.

## Option A — GitHub release (recommended if the Zenodo–GitHub integration is on)

1. Check the integration: zenodo.org → your name → **GitHub** → the switch for
   `jonnabio/xai-eval-framework` is **On**. If it is off, use Option B (switching it on now
   only archives future releases, which is fine, but check the version link in step 4).
2. Tag the exact commit that the submitted PDF is built from:
   ```
   git tag -a v0.3.0 -m "Paper B+C PeerJ CS submission snapshot" <commit>
   git push origin v0.3.0
   ```
3. GitHub → Releases → **Draft a new release** → tag `v0.3.0` → title
   "Paper B+C PeerJ CS submission snapshot (v0.3.0)" → **Publish**. Zenodo archives the source
   zip within a few minutes, using `.zenodo.json` for the metadata.
4. On Zenodo, open the new record. Check that it appears as a **new version** of record 21538180
   (sidebar "Versions"). If it was created as a separate record, it still works, but tell me and
   I will cite it directly.

## Option B — manual new version (how 21538180 appears to have been made)

1. zenodo.org → record `21538180` → **New version**.
2. Delete the old file. Upload `git archive --format=zip -o xai-eval-framework-v0.3.0.zip v0.3.0`
   (this contains tracked files only, which is exactly what the paper cites).
3. Also upload `docs/reports/paper_bc/paper_bc_artifacts.zip`, built with
   `python scripts/pubs/build_artifact_bundle.py` (needs `data/adult.csv`).
4. Version `0.3.0`. Publication date: today. Leave the metadata as `.zenodo.json`. **Publish.**

## After publishing — send me

- the **version DOI** (e.g. `10.5281/zenodo.2xxxxxxx`) and the **concept DOI** (the "Cite all
  versions" DOI).

I will then:
- cite the version DOI in the Data Availability section and the PeerJ form;
- set `CITATION.cff` `identifiers` to the concept DOI;
- tag the commit `peerjcs-submission-<id>` once filed.

## Do not

- Do not delete or edit record 21538180. The thesis and RIMI materials cite it.
- Do not upload `data/adult.csv` separately. It is third-party UCI data; the paper cites its
  source DOI instead.
