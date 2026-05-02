# EXP4 Multi-Judge & Human Validation Implementation Status

**Date**: 2026-04-28  
**Status**: Superseded by generated EXP4 analysis outputs  
**Timeline**: Parallel execution; judges running in background (~3-4 hours)

---

## Supersession Note

This file is retained as an execution-status note from the implementation
period. For thesis claims, use
`outputs/analysis/exp4_llm_evaluation/exp4_analysis_summary.json` and the
derived CSV files in the same directory. The generated analysis reports 4,790
parsed rows, 15 excluded dry-run rows, and 4,775 real analyzed judgments across
three judge labels.

The multi-judge LLM proxy layer is complete for thesis reporting. The human
validation layer is not complete as confirmatory evidence; the available human
annotation infrastructure and pilot responses should be described as preparation
for future human--LLM calibration.

## Phase 1: Multi-Judge LLM Analysis (historical status)

### ✅ Completed Setup

1. **Reliability Metrics Module** ([src/evaluation/exp4_reliability_metrics.py](src/evaluation/exp4_reliability_metrics.py))
   - ✅ ICC(2,1) intra-class correlation implementation
   - ✅ Krippendorff's alpha for ordinal agreement
   - ✅ Multi-judge comparison utilities
   - ✅ Case-level disagreement computation

2. **Extended Analysis Pipeline** ([src/evaluation/exp4_analysis.py](src/evaluation/exp4_analysis.py))
   - ✅ Integrated ICC and Krippendorff metrics
   - ✅ Added `_icc_per_dimension()` function
   - ✅ Added `_krippendorff_per_dimension()` function
   - ✅ Added `_judge_disagreement_matrix()` for Phase 2 case selection
   - ✅ Added `_judge_comparison_summary()` for per-judge profiling

### Historical Execution Snapshot

| Judge | Status | Expected Completion | Cases |
|-------|--------|---------------------|-------|
| **OpenAI GPT-4** | Completed in later generated analysis | Historical estimate was ~3 hours | 1,728 (192 × 3 conditions × 3 replicates) |
| **OpenRouter GPT-4-mini** | Completed in later generated analysis | Historical estimate was ~2 hours | 1,728 |

**Parallel Execution**: Both judges were launched simultaneously on independent API calls.  
**Terminal IDs**:
- OpenAI: `f3426b61-f83c-45b8-8093-d5b8fe0b753f`
- GPT-4-mini: `07955e0a-f6f4-41f1-801e-4648cfedec71`

### ⏭️ Next Steps (After Judge Completion)

1. **Re-parse all responses** (combine 3 judges → 5,184 rows)
   ```bash
   python scripts/exp4_parse_llm_responses.py \
     --input-dir experiments/exp4_llm_evaluation/raw_responses
   ```

2. **Run full multi-judge analysis** (generates ICC, Krippendorff, disagreement matrix)
   ```bash
   python scripts/exp4_analyze_llm_scores.py \
     --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml
   ```

3. **Outputs Generated**:
   - `icc_analysis.csv` — ICC(2,1) per dimension
   - `krippendorff_alpha.csv` — α per dimension
   - `judge_comparison_summary.csv` — Per-judge score profiles
   - `judge_disagreement.csv` — Case-level disagreement (seeds Phase 2)
   - `multijudge_summary_report.md` — Narrative findings

---

## Phase 2: Human Validation Study (SETUP COMPLETE)

### ✅ Infrastructure Built

1. **Case Selection Script** ([scripts/exp4_select_human_validation_cases.py](scripts/exp4_select_human_validation_cases.py))
   - ✅ Disagreement-based sampling algorithm
   - ✅ Stratification by explainer (balanced ~20 per explainer)
   - ✅ Produces case manifest with LLM scores + disagreement metadata

2. **Human Annotation Web UI** ([src/exp4_human_validation_ui/](src/exp4_human_validation_ui/))
   - ✅ React component: `HumanValidationForm.tsx`
   - ✅ Styling: `HumanValidationForm.css`
   - ✅ Features:
     - 1-case-at-a-time display
     - 5-point Likert scale ratings
     - 5 ultra-simple questions (clear language, no jargon)
     - Optional comments field
     - Real-time progress tracking
     - Responsive mobile-friendly design

3. **Annotator Guide** ([experiments/exp4_llm_evaluation/human_validation_annotator_guide.md](experiments/exp4_llm_evaluation/human_validation_annotator_guide.md))
   - ✅ 5 questions with examples (clear vs. unclear, complete vs. incomplete, etc.)
   - ✅ Step-by-step form walkthrough
   - ✅ Tips for success
   - ✅ Data privacy & ethics statement

4. **Human-LLM Correlation Script** ([scripts/exp4_human_llm_correlation.py](scripts/exp4_human_llm_correlation.py))
   - ✅ Merges human ratings with LLM scores
   - ✅ Computes Spearman ρ for each (human question, LLM dimension) pair
   - ✅ Generates inter-rater ICC on overlapping cases
   - ✅ Produces `human_llm_alignment.csv` + markdown report

### ⏭️ Phase 2 Execution Roadmap (After Phase 1 Complete)

**Step 1: Case Selection** (~15 min)
```bash
python scripts/exp4_select_human_validation_cases.py \
  --parsed-scores experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv \
  --output experiments/exp4_llm_evaluation/human_validation/case_manifest.csv \
  --n-cases 80
```

**Step 2: Recruit & Onboard Annotators** (~2-3 days)
- Target: 5-10 non-expert annotators
- Per annotator: 10 cases × 1-2 min each = 10-20 min total
- Overlap strategy: 10 cases rated by 2+ annotators (for inter-rater ICC)
- Distribution: 8-10 annotators × 10 cases ≈ 80 cases total

**Step 3: Deploy Web UI** (~2-4 hours setup if using Firestore)
- Build React app: `npm build`
- Deploy to Firebase Hosting or static server
- Share URL with annotators
- Real-time progress dashboard for manager tracking

**Step 4: Collect Human Responses** (~2-3 days)
- Annotators access form, rate assigned 10 cases each
- Auto-submit to backend (Firestore/DB)
- Progress dashboard shows % complete per annotator
- Reminders sent if incomplete by day 2

**Step 5: Correlate & Analyze** (~2-4 hours)
```bash
python scripts/exp4_human_llm_correlation.py \
  --human-responses experiments/exp4_llm_evaluation/human_validation_responses.csv \
  --parsed-scores experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv \
  --output outputs/analysis/exp4_llm_evaluation/human_llm_alignment.csv
```

**Step 6: Generate Report** (~1 hour)
- Human-LLM correlation table
- Per-judge validation (which LLM judge aligns best with humans?)
- Inter-rater reliability (human-human ICC)
- Implications for thesis

---

## The 5 Simple Questions (For Humans)

Each rated 1-5 (Strongly Disagree → Strongly Agree):

| # | Question | Rationale |
|---|----------|-----------|
| 1 | "This explanation is easy to understand." | Clarity (no jargon) |
| 2 | "This explains WHY the model made its decision." | Completeness (addresses causality) |
| 3 | "This is concise and not overly wordy." | Concision (brevity) |
| 4 | "This makes practical sense in the real world." | Plausibility (realism) |
| 5 | "I could use this to check if the model is fair." | Audit usefulness (actionability) |

**Design Philosophy**: Ultra-simplified for non-experts. Avoids technical terms (no "fidelity," "stability," "SHAP values," etc.).

---

## Expected Multi-Judge Results (Phase 1)

Based on deterministic execution (temperature=0.0), we expect:

- **ICC(2,1) > 0.90** across dimensions (excellent agreement, temp=0)
- **Krippendorff's α > 0.80** per dimension (good ordinal agreement)
- **Minimal disagreement** on most cases (unless prompt rendering differs)
- **If ICC < 0.75**: Investigate prompt hydration differences between judges

### Disagreement Analysis

Cases with **high disagreement** are candidates for human validation:
- Reveal ambiguous explanations (humans will struggle too)
- Test whether LLM judges reliable even on edge cases
- Provide qualitative data on explanation failure modes

---

## Expected Human Validation Results (Phase 2)

### Success Criteria

| Metric | Target | Interpretation |
|--------|--------|-----------------|
| **Spearman ρ (human-LLM)** | ≥ 0.40 | LLM proxy aligns with humans |
| **Inter-rater ICC (human-human)** | ≥ 0.50 | Acceptable non-expert agreement |
| **% High Correlation** | ≥ 60% | Majority of dimensions align |
| **Correlation p-value** | < 0.05 | Statistically significant |

### Interpretation Bands

- **ρ ≥ 0.50**: Strong alignment; LLM proxy highly valid
- **ρ 0.40-0.49**: Moderate alignment; LLM proxy useful but limited
- **ρ < 0.30**: Weak/no alignment; LLM proxy questionable for that dimension

---

## Files & Locations

### Phase 1 Outputs (Expected)

```
experiments/exp4_llm_evaluation/
├── raw_responses/
│   ├── openai_gpt41/                  # 1,728 new responses
│   ├── openrouter_gpt41_mini/         # 1,728 new responses
│   └── openrouter_gpt41/              # Existing 1,728 responses
├── parsed_scores/
│   └── exp4_llm_scores.csv            # 5,184 rows (3 judges × 1,728)
└── run_manifests/
    └── run_[timestamp].json           # Execution summary

outputs/analysis/exp4_llm_evaluation/
├── icc_analysis.csv                   # ICC(2,1) per dimension
├── krippendorff_alpha.csv             # α per dimension
├── judge_comparison_summary.csv       # Per-judge profiles
├── judge_disagreement.csv             # Case-level disagreement
└── multijudge_summary_report.md       # Narrative findings
```

### Phase 2 Outputs (Expected)

```
experiments/exp4_llm_evaluation/human_validation/
├── case_manifest.csv                  # 80 high-disagreement cases
├── human_validation_responses.csv     # Human ratings (5-10 annotators × 10 cases each)
└── annotator_guide.md                 # Onboarding documentation

outputs/analysis/exp4_llm_evaluation/
├── human_llm_alignment.csv            # Spearman correlations
├── human_validation_report.md         # Narrative findings
└── inter_rater_reliability.csv        # Human-human ICC
```

### Code Locations

| Module | Purpose | Status |
|--------|---------|--------|
| [src/evaluation/exp4_reliability_metrics.py](src/evaluation/exp4_reliability_metrics.py) | ICC + Krippendorff computation | ✅ New |
| [src/evaluation/exp4_analysis.py](src/evaluation/exp4_analysis.py) | Multi-judge analysis pipeline | ✅ Extended |
| [scripts/exp4_select_human_validation_cases.py](scripts/exp4_select_human_validation_cases.py) | Case selection (disagreement) | ✅ New |
| [scripts/exp4_human_llm_correlation.py](scripts/exp4_human_llm_correlation.py) | Human-LLM correlation analysis | ✅ New |
| [src/exp4_human_validation_ui/HumanValidationForm.tsx](src/exp4_human_validation_ui/HumanValidationForm.tsx) | React form component | ✅ New |
| [src/exp4_human_validation_ui/HumanValidationForm.css](src/exp4_human_validation_ui/HumanValidationForm.css) | Form styling | ✅ New |

---

## Timeline

| Phase | Task | Estimated Duration | Status |
|-------|------|-------------------|--------|
| **Phase 1** | Judge execution (parallel) | 3-4 hours | 🟢 In Progress |
| **Phase 1** | Re-parse + analysis | 30 min | ⏳ Waiting |
| **Phase 1** | QA validation | 30 min | ⏳ Waiting |
| **Phase 2** | Case selection | 15 min | ⏳ Waiting |
| **Phase 2** | Annotator recruitment | 1-2 days | ⏳ Ready (after Phase 1) |
| **Phase 2** | Web UI deployment | 2-4 hours | ✅ Ready |
| **Phase 2** | Human annotation | 2-3 days | ⏳ Ready (after Phase 1) |
| **Phase 2** | Correlation analysis | 2-4 hours | ⏳ Ready (after Phase 1) |
| **Phase 2** | Report generation | 1 hour | ⏳ Ready (after Phase 1) |
| **TOTAL** | End-to-end | ~1 week | 🟢 On Track |

---

## Next Actions

### Immediate (Judges Running)

1. ✅ **Keep both judge terminals alive** — No intervention needed; let them execute
2. ✅ **Check progress periodically** — Monitor logs in `logs/exp4_judge_*.log`
3. ✅ **Prepare for Phase 2** — Annotator guide ready; UI ready; deployment plan set

### After Judges Complete (ETA: ~4-6 hours)

1. Run: `python scripts/exp4_parse_llm_responses.py`
2. Run: `python scripts/exp4_analyze_llm_scores.py --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml`
3. Review: Multi-judge comparison outputs (ICC, Krippendorff)
4. Execute: `python scripts/exp4_select_human_validation_cases.py`
5. Launch: Annotator recruitment + onboarding

### For Thesis Integration

- **Paper C (Main Thesis)**: Use full multi-level framework (EXP1-4)
- **Paper A/B (Standalone)**: Can cite multi-judge ICCs as validation of LLM proxy reliability
- **Data Appendix**: All raw responses, parsed scores, correlations persisted for reproducibility

---

## Assumption Checks

✅ OpenAI API key configured (credentials in `secrets/`)  
✅ OpenRouter API balance available (~$2-3 for GPT-4-mini)  
✅ Temperature=0.0 ensures deterministic responses (ICC should be high)  
✅ Both judges can run in parallel (no API rate limits exceeded)  
✅ 5-10 annotators available for human study  
✅ Firebase/Firestore account ready for Phase 2 UI deployment (if using Option B)  

---

## References

- **Multi-Judge Reference**: ICC(2,1) designed for fixed set of raters evaluating same sample; appropriate for LLM judges
- **Ordinal Agreement**: Krippendorff's α handles 1-5 ordinal scale better than Cohen's κ
- **Human Validation**: Preliminary pilot (50-100 cases, 5-10 annotators) → future full-scale study
- **Thesis Scoping**: LLM proxy explicitly bounded as "reproducible proxy," not "human validation"
