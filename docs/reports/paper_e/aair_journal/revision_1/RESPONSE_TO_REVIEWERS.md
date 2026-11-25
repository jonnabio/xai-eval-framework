# Response to the editor and reviewers: Paper E, AAIR revision 1

Status: **draft**. Every item is answered: REMEDIATED (changes C-### and location) or
EXPLAINED. Locations refer to the revised manuscript. Open: supplement and Zenodo DOI (R2-6).

---

Dear Dr. Gürfidan,

Thank you for handling the manuscript "Do Explainers Agree on Which Features Matter?
Instance-Level Agreement between SHAP and LIME" and for the opportunity to revise it. I am
grateful to the three reviewers for their careful and constructive reports. Every comment
has been addressed; the answers follow, each with the changes made and where they appear.
A file with all changes marked is included.

The main changes are: (1) the sign error reported by Reviewer 2, caused by the conversion of
the manuscript into Word, has been corrected, and every number of the Word file is now
checked automatically against the analysis output; (2) the principal agreement estimates
are reported on held-out instances only and with each seed left out; (3) LIME was run again
under the package defaults and with larger sampling budgets, and the conclusions are stated
as conditional on the evaluated configuration; (4) pre-specified and exploratory analyses
are separated explicitly; (5) the Discussion and Limitations have been condensed.

Sincerely,
Jonathan Herrera-Vásquez

---

## Reviewer 1

I thank the reviewer for the positive assessment and for the precise suggestions.

**R1-1. Held-out sensitivity for the principal agreement estimates.**
REMEDIATED. The top-5 and top-10 overlap and Kendall's τ_b were recomputed on Adult for
held-out instances only (instances that are not rows of the models' training data). The
estimates are essentially unchanged: top-5 overlap 0.394 (interval 0.372 to 0.415) on
held-out instances against 0.393 on all instances and 0.385 on training rows; the largest
difference by model is that of the random forest, whose held-out instances agree more
(0.402 against 0.389). Training-set membership therefore does not explain the level of
agreement. Section 4.1, second paragraph; Section 3.1 states the design consequence.

**R1-2. Agreement conditional on the LIME configuration.**
REMEDIATED. The Abstract, the contributions, the Discussion ("What the evidence does not
support") and the Conclusions now state that the agreement levels are those of the evaluated
configuration and not properties of the two families of explainers, and Section 4.2 reports
how they change under other LIME settings, including the package defaults: on Adult the
overlap ranged from 0.164 (package defaults) to 0.473 (default width, 5,000 samples) against
0.383 in the study's configuration. (C-005, C-006)

**R1-3. Self-agreement as a reference analysis.**
REMEDIATED. Section 4.2 is now titled "Self-Agreement and LIME Settings (Post Hoc Reference
Analysis)" and opens by stating that it gives reference levels on a subsample with one pair
of random states, not the repeatability of either method in general. The Abstract and the
Conclusions use the same wording.

**R1-4. Pre-specified sign analysis versus post hoc corrected interpretation.**
REMEDIATED. The Discussion has a dedicated paragraph, "Signs: the pre-specified measure and
the post hoc correction", which states that the pre-specified measure compared slopes with
contributions and should not be read as disagreement about direction, and that only the
post hoc conversion compares like with like. Section 4.4 is retitled accordingly.

**R1-5. SVM results qualified wherever model families are compared.**
REMEDIATED. Section 4.3 now states that the SVM is not ranked against the other models
(29.5% coverage, unbalanced between predicted classes); Sections 4.5 and 4.6 qualify the SVM
estimate where it appears, and the Discussion draws no family ranking.

## Reviewer 2

I thank the reviewer for the careful reading, in particular for detecting the sign error.

**R2-1. Numerical consistency of Tables 1, 4 and 5.**
REMEDIATED. The reviewer is right, and I am grateful for this observation. The analysis
outputs and the source tables were correct (for example, Table 4, multilayer perceptron:
difference −0.059, interval −0.069 to −0.049), but the conversion of the manuscript into
Word wrote each minus sign as a separate equation object, which some viewers do not display.
The signs of Tables 1, 4 and 5, and of the text, were therefore lost in the copy read by the
reviewer. Every sign is now ordinary text, and every build of the manuscript compares each
table row and each negative number of the Word file with the analysis output and stops on
any difference. All values were verified again against the original analysis files. (C-001)

**R2-2. Held-out sensitivity extended to the main agreement results.**
REMEDIATED. See the answer to R1-1 (Section 4.1).

**R2-3. Standard LIME settings and different sampling budgets.**
REMEDIATED. On the self-agreement subsample (760 instances), LIME was run again, twice each,
with the package defaults (default kernel width, quartile discretisation, 5,000 samples),
with the default width without discretisation (5,000 samples), and with width 3 at 5,000 and
10,000 samples. The reviewer's concern is confirmed for the level of agreement: on Adult the
SHAP–LIME top-5 overlap was 0.383 with the study's settings, rose to 0.459 with 10,000
samples and to 0.473 with the default width, and fell to 0.164 with the package defaults,
under which LIME also reproduced itself much less (self-agreement 0.336). On German Credit and
Breast Cancer the sampling budget changed the overlap little. In every setting, and for every
model and dataset, the agreement between the methods stayed below the self-agreement of both
methods. The manuscript therefore presents the levels as specific to the configuration and
the comparison with self-agreement as the result that holds across settings. Section 3.3
(settings), Section 4.2 ("LIME settings"), Abstract, Discussion and Conclusions. (C-005, C-006)

**R2-4. Permutation reference within the same predicted class.**
REMEDIATED. The reference was recomputed with the other instance drawn from the same
predicted class. It changed little (Adult 0.207 against 0.204 unrestricted; German Credit
0.288 against 0.287; Breast Cancer 0.651 against 0.650), and the instance-specific part with
it, so the instance-specific agreement is not a class-level ranking. Section 3.3 and
Section 4.1.

**R2-5. Statistical generalizability.**
REMEDIATED. _Interpretation:_ the comment does not specify which validation is expected; it
was understood as a request to show that the conclusions do not rest on a single seed or
fit, and to state the limits plainly. If a different analysis was intended, I would be glad
to provide it. (1) A leave-one-seed-out analysis was added: the Adult top-5 overlap stays
between 0.388 and 0.399, German Credit between 0.367 and 0.409, Breast Cancer between 0.675
and 0.735 (Section 4.1). (2) The Discussion and Limitations state that each Adult family is a
single fitted model, that the intervals describe the spread of seed means, and that RQ2 to
RQ4 are exploratory. (3) Refitting one model per seed is named as future work.

**R2-6. Presentation and reproducibility.**
REMEDIATED. The numerical inconsistencies are corrected and checked automatically (R2-1).
The agreement measures are defined in Section 3.3 (Eq. 1 and 2), the configuration of every
explainer is stated in Section 3.2, and a supplementary file lists every setting of every
model and explainer and the new sensitivity results. The code and outputs of the revision are
archived in a new version of the Zenodo record cited in the Data Availability section.

## Reviewer 3

I thank the reviewer for the thorough assessment and for recognising the contributions of
the reference analyses.

**R3-1. LIME configuration: sensitivity and justification.**
REMEDIATED. _Interpretation:_ the width of 3 and the absence of discretisation were inherited
from the configuration of the benchmark cohort and were not tuned; a technical justification
cannot be supplied after the fact. The manuscript now says so plainly (Section 3.2) and
replaces the missing justification with evidence: the sensitivity analysis described under
R2-3 (Section 4.2) and conclusions stated as conditional on the configuration. That analysis
shows that the level of agreement depends on the kernel width, the sampling budget and
discretisation, while the finding that the two methods agree less with each other than each
with itself holds in every setting. (C-003, C-005, C-006)

**R3-2. Three datasets; evidence versus broader implications.**
REMEDIATED. The Discussion is now organised into "What the evidence supports", "What the
evidence does not support" (including the dataset characteristics that three datasets cannot
separate: kind and number of features, domain and kernel weight) and "Implications". Future
work names datasets that vary the number and kind of features.

**R3-3. Adult design: one model trained on a single partition.**
REMEDIATED. Section 3.1 now states that training a separate model for each seed is the
cleaner design and why it was not used (the study reuses the stored runs of the cohort), and
the primary measures are reported on held-out instances (R1-1). Refitting per seed is listed
as future work.

**R3-4. Separation of pre-specified and exploratory findings.**
REMEDIATED. Section 3.6 now lists the pre-specified analyses and the exploratory ones
separately; section headings, captions, the Abstract and the Conclusions mark every
exploratory result as post hoc.

**R3-5. Condensing the Discussion and Limitations.**
REMEDIATED. The two sections were rewritten from about 1,100 to about 810 words; each caveat
is stated once, in the Limitations, and repeated caveats elsewhere were removed.
