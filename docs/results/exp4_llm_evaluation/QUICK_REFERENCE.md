# EXP4 Multi-Judge & Human Validation: Quick Reference Guide

**Created**: 2026-04-28 | **Status**: Superseded by generated analysis outputs

> This quick reference is retained as an implementation-period note. For thesis
> claims, use `outputs/analysis/exp4_llm_evaluation/exp4_analysis_summary.json`,
> which reports 4,790 parsed rows, 15 excluded dry-run rows, and 4,775 real
> analyzed judgments across three judge labels. Human validation remains a
> separate, non-completed confirmatory calibration layer.

---

## Current Status

| Component | Status | Execution | Terminal ID |
|-----------|--------|-----------|-----------|
| OpenAI GPT-4 Judge | Completed in later analysis snapshot | 1,728 planned judgments | f3426b61-f83c-45b8-8093-d5b8fe0b753f |
| OpenRouter GPT-4-mini | Completed in later analysis snapshot | 1,728 planned judgments | 07955e0a-f6f4-41f1-801e-4648cfedec71 |
| Thesis source | Generated analysis controls | 4,775 real analyzed judgments | `exp4_analysis_summary.json` |

---

## 📋 What We Built

### Phase 1: Multi-Judge Analysis Infrastructure ✅

**New Modules**:
- [src/evaluation/exp4_reliability_metrics.py](src/evaluation/exp4_reliability_metrics.py) — ICC(2,1) + Krippendorff α
- [src/evaluation/exp4_analysis.py](src/evaluation/exp4_analysis.py) — Extended with multi-judge support

**New Scripts**:
- [scripts/exp4_orchestrate_multijudge_human.py](scripts/exp4_orchestrate_multijudge_human.py) — Automate post-execution workflow

**What It Does**:
- Computes inter-judge reliability (ICC, Krippendorff)
- Identifies high-disagreement cases
- Generates comparison tables

### Phase 2: Human Validation Study Infrastructure ✅

**New Components**:
- [src/exp4_human_validation_ui/HumanValidationForm.tsx](src/exp4_human_validation_ui/HumanValidationForm.tsx) — React form
- [src/exp4_human_validation_ui/HumanValidationForm.css](src/exp4_human_validation_ui/HumanValidationForm.css) — Styling
- [experiments/exp4_llm_evaluation/human_validation_annotator_guide.md](experiments/exp4_llm_evaluation/human_validation_annotator_guide.md) — Onboarding

**New Scripts**:
- [scripts/exp4_select_human_validation_cases.py](scripts/exp4_select_human_validation_cases.py) — Case selection (disagreement)
- [scripts/exp4_human_llm_correlation.py](scripts/exp4_human_llm_correlation.py) — Correlation analysis

**What It Does**:
- Selects 80 cases with highest LLM judge disagreement
- Displays explanations one-at-a-time to humans
- Collects 5 ultra-simple ratings (1-5 scale)
- Correlates human & LLM scores

---

## Historical Timeline

```
04-28-2026, ~14:00:
├─ GPT-4 OpenAI: launched (historical estimate ~3 hours)
├─ GPT-4-mini: launched (historical estimate ~2 hours)
│
~17:00 (Judge Completion):
├─ Parse + Analyze: 30 min
├─ Multi-judge report: Auto-generated
│
~17:30 (Phase 1 Complete):
├─ Case selection: 15 min
├─ Output: 80 high-disagreement cases
│
~17:45 (Phase 2 Ready):
├─ Annotator recruitment: 1-2 days
├─ Human annotation: 2-3 days
├─ Correlation analysis: 2-4 hours
│
~30-04-2026 (Complete):
└─ Full multi-judge + human validation pipeline finished
```

---

## 🎯 The 5 Human Questions

Ultra-simple, 1-5 Likert scale (no jargon):

1. **"This explanation is easy to understand."**
2. **"This explains WHY the model made its decision."**
3. **"This is concise and not overly wordy."**
4. **"This makes practical sense in the real world."**
5. **"I could use this to check if the model is fair."**

**Per Human**: ~10 cases × 1-2 min each = 10-15 min total

---

## 📍 Key File Locations

### Execution & Configuration
- Manifest: `configs/experiments/exp4_llm_evaluation/manifest.yaml`
- Judge logs: `logs/exp4_judge_*.log`

### Phase 1 Outputs (After Judge Completion)
- Parsed scores: `experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv`
- ICC analysis: `outputs/analysis/exp4_llm_evaluation/icc_analysis.csv`
- Disagreement: `outputs/analysis/exp4_llm_evaluation/judge_disagreement.csv`
- Report: `outputs/analysis/exp4_llm_evaluation/multijudge_summary_report.md`

### Phase 2 Setup (Ready Now)
- Case manifest: `experiments/exp4_llm_evaluation/human_validation/case_manifest.csv`
- Annotator guide: `experiments/exp4_llm_evaluation/human_validation_annotator_guide.md`
- Web UI: `src/exp4_human_validation_ui/`

### Phase 2 Outputs (After Human Annotation)
- Human responses: `experiments/exp4_llm_evaluation/human_validation_responses.csv`
- Correlations: `outputs/analysis/exp4_llm_evaluation/human_llm_alignment.csv`
- Report: `outputs/analysis/exp4_llm_evaluation/human_validation_report.md`

---

## 🔧 How To Execute (After Judges Complete)

### Option A: Use Orchestration Script (Recommended)

```bash
# Run everything automatically
python scripts/exp4_orchestrate_multijudge_human.py --phase all --n-cases 80
```

Output:
- Re-parses all 3 judges
- Computes ICC, Krippendorff, disagreement
- Selects 80 human validation cases
- Generates summary reports

### Option B: Manual Execution

```bash
# Step 1: Re-parse all judge responses
python scripts/exp4_parse_llm_responses.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml

# Step 2: Run multi-judge analysis
python scripts/exp4_analyze_llm_scores.py \
  --manifest configs/experiments/exp4_llm_evaluation/manifest.yaml

# Step 3: Select human validation cases
python scripts/exp4_select_human_validation_cases.py \
  --parsed-scores experiments/exp4_llm_evaluation/parsed_scores/exp4_llm_scores.csv \
  --output experiments/exp4_llm_evaluation/human_validation/case_manifest.csv \
  --n-cases 80
```

---

## 📊 Expected Results

### Multi-Judge Reliability (Phase 1)

- **ICC(2,1)**: Expected ≥ 0.90 (excellent; temp=0.0 → deterministic)
- **Krippendorff's α**: Expected ≥ 0.80 (good ordinal agreement)
- **Disagreement**: Highest on ambiguous cases (seeds Phase 2)

### Human-LLM Correlation (Phase 2)

- **Spearman ρ ≥ 0.40**: LLM proxy aligns with humans ✅
- **Inter-rater ICC ≥ 0.50**: Acceptable human agreement
- **% High Correlation ≥ 60%**: Majority of dimensions align

---

## ✅ Implementation Checklist

- ✅ Multi-judge reliability metrics (ICC, Krippendorff)
- ✅ Extended analysis pipeline
- ✅ Case selection script (disagreement-based)
- ✅ Web UI for human annotation (React)
- ✅ Annotator guide (5 ultra-simple questions)
- ✅ Human-LLM correlation analysis
- ✅ Orchestration script (automates workflow)
- ✅ Documentation (implementation guide, quick ref)
- 🟢 Parallel judge execution (running now)
- ⏳ Phase 1 completion (after judges finish)
- ⏳ Phase 2 human annotation (after Phase 1)

---

## 🎓 For Your Thesis

### Multi-Judge Results Use Cases

- **Paper A/B**: "3 LLM judges with ICC = 0.92 show reproducible semantic proxy"
- **Paper C (Thesis)**: Full multi-level framework narrative
- **Data Appendix**: All raw responses, scores, correlations

### Human Validation Use Cases

- **Thesis Chapter 5**: "Preliminary human validation pilot (n=80, 5-10 annotators)"
- **Limitations**: Acknowledge single-judge LLM + non-expert human sample
- **Future Work**: "Extended multi-site human validation study"

---

## 📞 Troubleshooting

### Judge Execution Stuck?
- Check terminal logs: `cat logs/exp4_judge_openai_gpt41.log`
- Verify API keys in `secrets/`
- Check internet connection

### Analysis Fails?
- Ensure judges produced JSON files in `raw_responses/[judge_id]/`
- Verify column names match schema (`exp4_schema.py`)
- Check `exp4_parse_failures.csv` for parse errors

### Web UI Won't Deploy?
- Verify Node.js installed: `node --version`
- Install dependencies: `npm install` (in UI folder)
- Check Firebase config (if using Option B)

---

## 📚 Reference

- **ICC Reference**: [src/evaluation/exp4_reliability_metrics.py](src/evaluation/exp4_reliability_metrics.py#L1-L100)
- **Krippendorff Reference**: [src/evaluation/exp4_reliability_metrics.py](src/evaluation/exp4_reliability_metrics.py#L100-L200)
- **Human Validation Design**: [experiments/exp4_llm_evaluation/human_validation_annotator_guide.md](experiments/exp4_llm_evaluation/human_validation_annotator_guide.md)

---

## 🎯 Next Immediate Action

**DO NOT**: Restart judges or modify running terminals  
**DO**: Wait for judge completion (~3-4 hours)  
**THEN**: Run orchestration script or manual steps above

---

**Created by**: GitHub Copilot (Data Scientist Mode)  
**Last Updated**: 2026-04-28  
**Status**: ✅ Ready for Phase 1 Completion & Phase 2 Execution
