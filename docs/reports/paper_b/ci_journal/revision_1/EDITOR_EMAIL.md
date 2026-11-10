**To:** Prof. Dr. Mehmet Tekerek, Editor in Chief, *Computers and Informatics*
**Subject:** Revised manuscript 2067810, "When Does SHAP Outperform LIME? Model- and Configuration-Dependent Results from a Paired Tabular Benchmark"

Dear Prof. Dr. Tekerek,

Thank you for the decision of 6 November 2026 and for the reviewers' detailed reports. I am submitting the revised version of manuscript 2067810.

**Files submitted**

1. Revised manuscript (Word, in the journal template; 15 pages).
2. Manuscript with changes marked, against the version first submitted.
3. Point-by-point response to the editor and the two reviewers: every comment is quoted in full, followed by the answer and the place of the change in the manuscript.
4. Supplementary file (52 pages): per-dataset tables, the configuration sweep, the validity controls, the timing data and the computing environment.

**Overview of the changes**

- **Editorial requirement.** Anchors and DiCE are now part of the main benchmark, under the same paired protocol as SHAP and LIME: same models, test instances, seeds, metrics and host.
- **New experiments.** All results come from a new experimental cohort run for this revision: five model families on Adult (confirmatory), six further datasets, a sweep over LIME's kernel width and samples and KernelSHAP's budget and background, and controls that test the validity of the stability measure.
- **Statistics.** The analysis now accounts for the dependence between configurations (mixed models with seeds nested in models, Holm correction, effect sizes with confidence intervals), and separates confirmatory from exploratory results.
- **Cost.** Time is measured on one recorded host, together with hardware-independent counts of model evaluations, and the effect of tree depth on TreeSHAP is tested with matched ensembles.
- **Literature.** The related work now covers recent comparisons and benchmarks; every new reference was checked against its DOI or registry record.
- **Claims.** The conclusions state the conditions under which each ordering holds, and descriptive results are no longer presented as tests.

Of the 51 items in the reports, 50 were addressed with changes to the manuscript and one is answered with an explanation in the response.

**Length**

The manuscript has grown from 14 to 15 pages (about 6,500 to 7,600 words). The increase comes from the material the editor and the reviewers asked for: two more explainers in the main benchmark, six further datasets, the configuration sweep with its figure, and the validity controls. To keep the paper readable, the per-dataset and per-setting detail was moved to the supplementary file, and the main text keeps the result and the condition under which it holds. The abstract remains within 150 to 200 words.

As the journal's guidelines set no length limit, I have kept these results in the main text. If you would prefer a shorter manuscript, I can move further material, such as the table for the other datasets, to the supplementary file without changing any conclusion.

Thank you for your time and for the consideration of the revised manuscript.

Yours sincerely,

Jonathan Herrera-Vásquez
