# Reference audit (WP8): Paper B revision 1

Date: 2026-11-06. Answers R1-9 (literature) together with P-02 (CHANGELOG C-002, C-027).

## Method

Every new entry was checked against the registry that issued its DOI, never from memory:
Crossref for articles (title similarity ≥ 0.9 and the first author's surname must both match;
volume, issue, pages and DOI copied from the record), DataCite for the UCI datasets (creators
as the DOI record lists them), PubMed Central for Smith et al. 1988 (no DOI). Candidates were
rejected when the only record was a preprint (Krishna et al., disagreement problem) or the
paper predates 2024 (Saeed 2023, Zhou 2021, Guidotti 2022, Bodria 2023). The scripts and
their raw output are not part of the paper; the commands are in this file's history.

The new related-work paragraph (§2) cites each recent paper only for what its title and venue
establish (topic and setting), not for findings, because the papers were not read in full.
**The author should read the abstracts of the 15 papers before submission** and adjust any
characterization.

## Added (19 entries, all verified)

| Key | Year | Venue | Used for |
|---|---|---|---|
| hooshyar2024problems | 2024 | IEEE Access | SHAP–LIME comparison (education) |
| schulte2024studying | 2024 | Empirical Software Engineering | SHAP–LIME comparison (software engineering) |
| lazar2026beyond | 2026 | Int. J. on AI Tools | SHAP–LIME on mixed-type tabular models |
| ababneh2026faithfulness | 2026 | Big Data and Cognitive Computing | faithfulness and stability, tabular and image |
| salih2025perspective | 2025 | Advanced Intelligent Systems | review of SHAP and LIME |
| mersha2024survey | 2024 | Neurocomputing | XAI survey |
| velmurugan2025guidelines | 2025 | Eng. Appl. of AI | functionally grounded evaluation, tabular |
| moiseev2025benchmark | 2025 | Algorithms | open XAI benchmark |
| olsen2024comparative | 2024 | Data Min. Knowl. Discov. | Shapley estimators, accuracy and cost |
| saadatfar2024uslime | 2024 | Neurocomputing | LIME neighborhood sampling |
| brughmans2024disagreement | 2024 | TOP | counterfactual disagreement |
| baniecki2024adversarial | 2024 | Information Fusion | manipulation of explanations |
| huang2024failings | 2024 | Int. J. Approx. Reasoning | limits of Shapley values |
| bilodeau2024impossibility | 2024 | PNAS | limits of feature attribution |
| clark2024xaitris | 2024 | Machine Learning | false-positive attributions |
| smith1988adap | 1988 | Proc. SCAMC | Diabetes (Pima) dataset |
| hopkins1999spambase | 1999 | UCI (DataCite DOI) | Spambase dataset |
| mohammad2012phishing | 2012 | UCI (DataCite DOI) | Phishing dataset |
| tromp1995connect4 | 1995 | UCI (DataCite DOI) | Connect-4 dataset |

The four statistics references added in P-11 were verified as well: Bates 2015 (JSS),
Field & Welsh 2007 (JRSS-B), Hodges & Lehmann 1963 (Ann. Math. Stat.), Kerby 2014
(Comprehensive Psychology). Dataset row counts match the cited sources (Phishing 11,055;
Spambase 4,601; Connect-4 67,557; Pima 768).

## The 80%-from-2024 rule (D-6): status and the decision it needs

Now: **61 references, 22 from 2024 on (36%).**

| Category | Entries | Can be recent? |
|---|---:|---|
| Method definitions (LIME, SHAP, Anchors, DiCE, random forest, XGBoost) | 6 | no |
| Dataset sources (Adult ×2, UCI, Breast Cancer, German Credit, 4 new) | 9 | no |
| Statistical methods (Demšar, Wilcoxon, Lakens, Holm, Bates, Field, Hodges–Lehmann, Kerby) | 8 | no |
| Metric definitions (Bhatt, Samek, Alvarez-Melis) | 3 | no |
| Literature (positioning, limits, evaluation) | 35 | yes: 22 recent, 13 older |

Applied literally, the rule needs ≈ 4 recent entries per old one: with 26 entries that cannot
be recent, about 130 references (≈ 4 pages), which breaks the 12-page budget (D-C).

**Decision (author, 2026-11-06): option A**, applied in CHANGELOG C-028. Nine entries removed
(Slack 2020, Kumar 2020, Rong 2022, Ali 2023, Hooker 2019, Doshi-Velez 2017, Jacovi 2020,
Wilming 2022 and 2023, the last two replaced by Clark 2024 in §5). Result: **52 references,
22 from 2024 on (42%); literature 26 entries, 22 recent (85%)**; older literature kept:
Adebayo 2018, Agarwal 2022, Hedström 2023, Nauta 2023 (each cited for a point no recent
verified entry covers). Exempt (26): definitions 9 (6 methods, 3 metrics), datasets 9,
statistical methods 8.

**Options for the author (as proposed):**

- **A (recommended).** Apply the rule to the *literature* category and exempt definitions,
  datasets and statistical methods (stated in the response to R1-9). To reach 80% there,
  replace or drop about 8 of the 13 older literature entries, where a verified recent entry
  already covers the point: `slack2020fooling` → baniecki2024; `kumar2020problems` →
  huang2024; `wilming2022/2023` → clark2024; `rong2022consistent` → zheng2025;
  `ali2023trustworthy`, `doshivelez2017rigorous`, `jacovi2020faithfulness`,
  `hooker2019benchmark` dropped. Result ≈ 27 literature entries, 22 recent (81%); list ≈ 53.
  Saves ≈ 0.2 page.
- **B.** Keep the list as it is (36% overall, 63% of literature) and explain in the response
  that foundational definitions and data sources are cited where they are used.
- **C.** Literal 80% overall (≈ 130 references). Not compatible with 12 pages.

## Length

With the new paragraph and 19 entries the manuscript is **11 pages** (budget 12), before the
results text and Figure 1. Option A recovers a little; the supplement (D-B) takes the detail
tables. A 13-page outcome is possible; the build will warn.
