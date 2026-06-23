# Active Context: XAI Evaluation Framework

## Session Metadata
- **Last Updated:** 2026-06-21
- **Branch:** publication/cifie-xai-fom7-book-chapter
- **Mode:** Publication workstream scaffolding

## Current Objective
Create and maintain a separate CIFIE collective book chapter workstream derived from the doctoral XAI research while preserving existing thesis and paper artifacts.

## Current State

### Working
- Core framework supports config-driven XAI experiments.
- FastAPI backend serves experiment runs, health checks, batch operations, and human evaluation endpoints.
- Thesis production is organized under `thesis/` with publication fragments under `pub/`.
- Experiment and recovery workflows are organized under `configs/`, `experiments/`, `scripts/`, and `src/experiment/`.
- CIFIE book chapter scaffolding is organized under `publications/book_chapters/2026_cifie_xai_fom7/` as an independent publication artifact.

### Local Tooling
- ACE is local AI-assisted Coding Engineering tooling and is not part of the project source.
- ACE generated files should remain ignored locally via `.git/info/exclude`, not committed to the repository.

### In Progress
- CIFIE Spanish technical book chapter workstream setup for FOM-7/XAI evaluation.
- Source inventory and evidence mapping for section-by-section chapter drafting.
- Extraction pass 1 completed for initial references, citation audit, and metrics table.
- Extraction pass 2 completed for empirical result summary and figure registry.
- Extraction pass 3 completed for FOM-7 protocol details and gate reconciliation.
- Controlled drafting pass 1 completed for XAI foundations and methods sections.
- Controlled drafting pass 2 completed for the XAI evaluation crisis section and FOM-7 transition.
- Controlled drafting pass 3 completed for empirical design and results sections.
- Controlled drafting pass 4 completed for discussion, limitations/future work, and conclusions.
- Controlled drafting pass 5 completed for abstract/keywords, introduction, chapter assembly index, and terminology/callout harmonization.
- Figure and table integration pass completed: selected thesis figures copied into the CIFIE workstream and manuscript callouts numbered.
- V2 technical draft and editorial pass completed under `drafts/v2_technical_draft/`.
- Introduction enrichment pass completed with `02_introduccion.md`: paragraphs expanded using thesis paper sources and APA-style in-text citations.
- Foundations enrichment pass completed with `03_fundamentos_xai.md`: paragraphs expanded using thesis paper sources and APA-style in-text citations.
- Methods enrichment pass completed with `04_metodos_lime_shap_anchors_dice.md`: paragraphs expanded using thesis paper sources and APA-style in-text citations.
- Second methods enrichment pass completed with `04_metodos_lime_shap_anchors_dice.md`: method profiles tied more explicitly to extracted benchmark evidence.
- XAI evaluation crisis enrichment pass completed with `05_crisis_evaluacion_xai.md`: expanded metric-fragmentation, construct-gap, reproducibility, and governance arguments with APA-style citations.
- FOM-7 protocol enrichment pass completed with `06_protocolo_fom7.md`: expanded gate-by-gate admissibility logic, operational controls, and limits with APA-style citations.
- Empirical design enrichment pass completed with `07_diseno_empirico.md`: expanded EXP1/EXP2, Adult dataset, sampling, metrics, units, FOM-7 controls, and inferential plan with APA-style citations.
- Book-chapter structural revision completed for `08_resultados.md` and `09_discusion.md`: results are now an integrated empirical application/evidence block and discussion is a concise methodological implications section.
- Preserve useful project context while excluding local assistant tooling artifacts.

### Blocked
- Full `git status` can be slow or time out on the WSL `/mnt/c` worktree; prefer targeted Git checks when possible.

## Next Steps
1. Continue section-by-section prose improvement while converting remaining citations to APA 7 in-text style.
2. Confirm final CIFIE template, word limit, and citation rendering requirements.
3. Reduce/adapt the v2 technical draft if the 7,000-8,500 word target is enforced.
4. Prepare `drafts/v3_editorial_review/` after APA/DOI validation and template adaptation.
5. Continue using narrow Git commands for status checks on this worktree.
6. Keep ACE artifacts out of project commits unless the project explicitly adopts them later.

## Active Constraints
- Do not commit secrets, generated caches, datasets, model binaries, or local assistant tooling.
- Keep experiment, thesis, API, and dashboard context project-specific.
- Preserve existing project source and generated research artifacts unless explicitly asked to remove them.
- Do not overwrite existing thesis or paper artifacts while developing the CIFIE book chapter.
- Manage the CIFIE chapter as a distinct publication output under `publications/book_chapters/2026_cifie_xai_fom7/`.
