---
title: "Response to Reviewer A"
subtitle: "Journal of Computer Sciences Institute, submission 10503: How Dataset-Dependent Are Tabular Explainability Benchmarks?"
---

The author thanks Reviewer A for the careful reading and for the two comments, both of
which are addressed in the revised manuscript. Page numbers refer to the revised file.

## Comment 1

> It has not been explained why the value T5—rather than any other—is used in the formula (2) for stability.

**Response.** The value was fixed in the analysis plan before any classifier was trained,
for two reasons that the text now gives. Five is the number of encoded features of the
smallest dataset (phoneme), so $T_5$ is defined on every dataset of the study. It also
lies between the number of features the four methods name: Anchors and DiCE name about
three, LIME is set to ten. A smaller value would compare only the first one or two
features of LIME and SHAP; a larger one would be decided mostly by ties among the
features of a rule. Since the stability measure depends on this choice, the size of
$T_5$ is now listed among the possible sources of error. A check with another value would
need every perturbed copy explained again, which is beyond this revision.

**Change (p. 3, after Eq. (2)):** "The value 5, fixed in the plan before the run, is the
number of encoded features of the smallest dataset, so $T_5$ is defined on every dataset;
it lies between the features named by Anchors and DiCE (about 3) and the 10 of LIME."

**Change (p. 6, possible sources of error):** "… depend on how many features a method
names, on the size of $T_5$, and on the column order …"

## Comment 2

> No conclusions were presented that take into account the type of dataset. Furthermore, it was noted that two of the analyses were conducted differently. It might be worth drawing some generalizations by considering the type of data within the dataset.

**Response.** The datasets were selected in strata of feature type (Table 1), and the
revision now uses that structure. The ranks of the methods were compared between the nine
datasets with only numeric features and the six with mixed features; one dataset has only
categorical features and is too few to compare. The type of features does not change the
order of the methods, but the comparisons that vary between datasets fall where the
protocol treats the two types differently: on mixed data the faithfulness gap and
stability of LIME, SHAP and Anchors, where one-hot columns enlarge the features a method
can name and mask and the stability copies perturb numeric features only; on numeric data
the sparsity of Anchors and DiCE. The size of a dataset shows no consistent pattern. As the
comparison was made after the results were seen, on small groups, it is reported as
descriptive, without a test, and is labelled as such.

**Change (p. 5, results):** a paragraph reporting the comparison: SHAP has the largest
faithfulness gap on nine of the nine numeric datasets and on four of the six mixed ones;
LIME is more stable than Anchors on nine and three; the order on sparsity is the same on
six of the six mixed datasets, while Anchors precedes DiCE on four numeric ones; the
agreement between a numeric and a mixed dataset (0.65, 0.83, 0.84 and 0.87 for the four
measures) is close to the overall one.

**Change (p. 6, conclusions):** a fourth conclusion: "The type of features does not change
the order of the methods but moves the comparisons that vary: on mixed data the gap and
stability of LIME, SHAP and Anchors, where one-hot columns and noise on numeric features
only act; on numeric data the sparsity of Anchors and DiCE." The proposal for further
research now asks for more datasets of each type.

**On the two analyses conducted differently.** These are the two departures from the
analysis plan that the paper discloses: the shares of variance are computed by a balanced
decomposition of sums of squares rather than the mixed model named in the plan, and cost
relative to prediction time was not computed. Both were recorded in the plan's log before
the analysis was run, and neither enters the decision rule on which the conclusions rest.
The sentence now states this.

**Change (p. 6, possible sources of error):** "Two analyses differ from the plan, as its
log records before the analysis was run, and neither enters the decision rule: …"

The revised manuscript keeps the length limit of eight pages and the format corrections
requested by the editor on 13 October 2026.
