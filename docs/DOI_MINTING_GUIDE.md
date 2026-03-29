# DOI Minting Guide

This guide explains how to mint a real archival DOI for the repository snapshot used in Paper A.

## Recommended Path: Zenodo + GitHub Release

1. Ensure the repository metadata is ready.
   - `CITATION.cff`
   - `.zenodo.json`
   - `LICENSE`
   - manuscript and reproducibility files updated to the exact submission snapshot

2. Create a clean archival tag in Git.
   - Example: `paper-a-submission-2026-03-28`

3. Push the tag to GitHub.

4. Log in to Zenodo with the GitHub account that has access to the repository.

5. Enable the repository in Zenodo's GitHub integration.
   - Authorize Zenodo to access GitHub if prompted.
   - In Zenodo, toggle the repository on for archiving.

6. Create a GitHub release from the archival tag.
   - GitHub release title example: `Paper A submission snapshot`
   - Include the exact commit hash and a short description of what is frozen in the release.

7. Wait for Zenodo to ingest the GitHub release.
   - Zenodo will create a deposition tied to that release.
   - Review the metadata generated from `.zenodo.json` and `CITATION.cff`.

8. Edit and publish the Zenodo record.
   - Confirm title, author, description, version, keywords, and license.
   - Publish the record to mint the version-specific DOI.

9. Copy both DOI forms.
   - Version DOI: cite this exact submission snapshot.
   - Concept DOI: use this for the project as a whole across versions.

## What To Update After DOI Minting

After Zenodo publishes the archive, update these files:

- `docs/reports/paper_a/paper_a_prototype.md`
- `docs/reports/paper_a/paper_a_prototype_jmlr.tex`
- `docs/reports/paper_a/paper_a_validity_and_reporting_caveats.md`
- `experiments/exp1_adult/reproducibility_package/REPRODUCIBILITY_GUIDE.md`
- `CITATION.cff` if you want the DOI recorded there as well

## Suggested DOI Wording For Paper A

Use wording like:

`Code, experiment configurations, qualified result artifacts, inferential exports, and figure-generation scripts are archived at DOI: <version-doi> and mirrored at https://github.com/jonnabio/xai-eval-framework.`

## What To Cite

- Cite the version DOI in the paper and supplementary materials.
- Keep the GitHub URL as a secondary access path.
- Prefer the version DOI over the concept DOI for exact reproducibility claims.
