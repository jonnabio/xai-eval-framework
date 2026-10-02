# Zenodo release: the code and data archive of Paper B+C

> **DONE 2026-10-02.** Version 0.4.0 is published as **`10.5281/zenodo.23111684`**
> (https://doi.org/10.5281/zenodo.23111684), through Route A. Tag
> `paper-bc-peerj-submission-2026-10-02` = `main` at `ba6e835f2`; archive 907 MB; open
> access, MIT licence; name and affiliation correct. The manuscript cites it. The rest of
> this file is the procedure, kept for the next release.
>
> **Venue changed (ADR-0020):** the paper now goes to *Inteligencia Artificial*, which reviews
> double-blind. The review PDF withholds this DOI; the camera-ready build prints it. Before the
> camera-ready version, publish a new version (Route A below, with a new tag name) so the
> archive matches the published paper, and update `\zenodoversiondoi`.

PeerJ requires a DOI archive holding an **exact copy** of the code and data the study used. A
GitHub link is not enough. The current Zenodo version predates EXP4 cohort 2 and EXP6, so a
new **version** of the same record is needed.

Only the author can publish it: it goes out under your Zenodo account and cannot be undone.

## The record today (checked against the Zenodo API, 2026-10-02)

| | DOI | Version | Date | How it was made |
|---|---|---|---|---|
| Concept (all versions) | `10.5281/zenodo.19297723` | – | – | – |
| Version 1 | `10.5281/zenodo.19297724` | 0.2.0 | 2026-03-28 | GitHub release `paper-a-submission-2026-03-28` (61 MB) |
| Version 2 (current) | `10.5281/zenodo.21538180` | 0.3.0 | 2026-07-24 | Manual upload of one zip (888 MB), commit `553f65d71` |
| **Version 3 (current)** | `10.5281/zenodo.23111684` | **0.4.0** | 2026-10-02 | GitHub release `paper-bc-peerj-submission-2026-10-02` (907 MB) |

- The new version is **0.4.0**. Version 0.3.0 is already taken by the current record.
- `CITATION.cff` cites the concept DOI. The paper cites the **version** DOI of version 3.
- A zip of today's `main` is about 905 MB. Zenodo's limit is 50 GB.

## What gets archived

Tag `paper-bc-peerj-submission-2026-10-02` on `main`. It holds every tracked file: code,
configurations, raw run outputs, statistical exports, the review corpus sheet, the EXP4 cohorts
and the PeerJ manuscript source.

The manuscript inside the archive prints "[ZENODO VERSION DOI PENDING]", because the DOI exists
only after publishing. That is expected. The DOI is added to the manuscript in the next commit,
and the archived code and data, which are what PeerJ requires, are exact.

## Route A — GitHub release (try this first)

Claude can do steps 1–2 when you say so. Step 3 happens on Zenodo by itself if the integration
is on.

1. Tag and push:
   ```
   git tag -a paper-bc-peerj-submission-2026-10-02 -m "Paper B+C PeerJ CS submission snapshot (v0.4.0)" origin/main
   git push origin paper-bc-peerj-submission-2026-10-02
   ```
2. Publish a GitHub release on that tag, titled
   "Paper B+C PeerJ CS submission snapshot (v0.4.0)".
3. Zenodo archives it within about 10 minutes, with the metadata in `.zenodo.json`. Check at
   zenodo.org → your uploads. It should appear as a new version of record 21538180.

**Check first that the integration is on:** zenodo.org → your name (top right) → **GitHub** →
the switch beside `jonnabio/xai-eval-framework` is **On**. Version 1 came through this
integration; version 2 did not, so it may have been switched off since. If it is off, switch
it on *before* the release is published, or use Route B.

## Route B — manual new version (how version 2 was made)

1. Claude builds the zip from the tag:
   ```
   git archive --format=zip --prefix=xai-eval-framework-0.4.0/ -o xai-eval-framework-0.4.0.zip paper-bc-peerj-submission-2026-10-02
   ```
2. zenodo.org → record `21538180` → **New version**.
3. Remove the old 888 MB file and upload the new zip.
4. Set **Version** `0.4.0` and **Publication date** today. While editing, correct two fields
   copied from the old version: the creator name to `Herrera-Vásquez, Jonathan` and the
   affiliation to `Universidad Americana de Europa` (the old records say "Herrera-Vasquez" and
   "Americada").
5. Related identifiers: "is supplement to"
   `https://github.com/jonnabio/xai-eval-framework/tree/paper-bc-peerj-submission-2026-10-02`.
6. **Publish.**

## After publishing — send Claude

- the **version DOI** of version 3 (for example `10.5281/zenodo.2xxxxxxx`).

Claude then:
- sets `\zenodoversiondoi` in `paper_bc_iberamia.tex` and rebuilds the PDF;
- records the DOI in `IBERAMIA_SUBMISSION.md` §8;
- runs the four verifiers and commits.

## Optional, any time: fix the old records' metadata

Versions 1 and 2 show "Herrera-Vasquez" and "Universidad Americada de Europa". Zenodo lets you
edit a published record's metadata without changing its DOI: open the record → **Edit** → fix
the creator name and affiliation → **Publish**.

## Do not

- Do not delete record 21538180 or its file. The thesis and the RIMI materials cite it.
- Do not upload `data/adult.csv` as a separate item. It is third-party UCI data, already inside
  the archive as a tracked file, and the paper cites its source DOI.
