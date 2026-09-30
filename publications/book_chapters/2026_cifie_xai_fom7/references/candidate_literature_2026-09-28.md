# Candidate Literature for the Science-First Revision

**Status:** Verified staging register; all seventeen candidates promoted to the
production bibliography on 2026-09-29 (six after citation in sections 02-03,
eleven after citation in section 04)

**Verification date:** 2026-09-28

**Scope:** Sections 02-06 of the approved scientific scaffold

## Admission rule

This is a staging and transfer inventory, not the chapter reference list. A source
moves to `references.bib` and `references_apa7.md` only when the revised manuscript
cites it. Promoted records remain here to preserve their admission rationale.
This preserves the requirement that the final reference list contain cited works
only. Metadata was checked against an official institution, publisher record, DOI
landing page, or author-hosted publication copy. Each candidate is tied to a bounded
claim and a stated limit.

## Claim-to-source matrix

| ID | Candidate | Evidence class | Admissible use | Required boundary | Primary locator | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | Phillips et al. (2021) | Official technical report | Define four evaluation principles: explanation, meaningfulness, explanation accuracy, and knowledge limits; support audience-specificity. | A principle is not proof that a deployed system satisfies it. | [NISTIR 8312](https://doi.org/10.6028/NIST.IR.8312) | Promoted; cited in sections 02-03 |
| C02 | Tabassi (2023) | Official risk framework | Place explainability within a wider trustworthy-AI risk framework. | Explainability does not substitute for validity, safety, security, privacy, fairness, transparency, or accountability. | [NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1) | Promoted; cited in sections 02-03 |
| C03 | European Parliament and Council of the European Union (2024) | Official regulation | Support the narrow claim that high-risk systems must provide sufficient transparency for deployers to interpret outputs and use them appropriately. | Do not turn the chapter into legal advice or infer a universal right to a technical explanation. | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Promoted; cited narrowly in section 02; legal-reference style retained for final audit |
| C04 | World Health Organization (2021) | Official sector guidance | Frame health-AI use around autonomy, safety, transparency, intelligibility, responsibility, and lifecycle governance. | Guidance identifies governance needs; it does not validate any specific XAI method or clinical prediction. | [WHO guidance](https://www.who.int/publications/i/item/9789240029200) | Metadata, ISBN, and official full text verified; promoted 2026-09-29, cited in section 04 |
| C05 | Ghassemi et al. (2021) | Peer-reviewed critical viewpoint | Support the caution that current post-hoc explanations can aid model interrogation without validating patient-level clinical decisions. | Present as a critical viewpoint, not a systematic review or universal empirical result. | [The Lancet Digital Health](https://doi.org/10.1016/S2589-7500(21)00208-9) | Publisher metadata and article verified; promoted 2026-09-29, cited in section 04 |
| C06 | Kim et al. (2024) | Peer-reviewed systematic review | Support the human-centered evaluation gap and the lack of consistent framework reuse. | Report review scope and do not treat counts as prevalence beyond the included corpus. | [Frontiers in Artificial Intelligence](https://doi.org/10.3389/frai.2024.1456486) | Promoted; cited in sections 02-03 |
| C07 | Alufaisan et al. (2021) | Peer-reviewed human-subject study | Provide primary counterevidence that explanations did not conclusively improve decision accuracy in the studied tasks. | Bound the statement to the experimental tasks; do not claim that explanations never help. | [AAAI proceedings](https://doi.org/10.1609/aaai.v35i8.16819) | Promoted; bounded result cited in section 02 |
| C08 | Poursabzi-Sangdeh et al. (2021) | Peer-reviewed preregistered experiments | Show that simpler, transparent models improved simulation but did not necessarily improve reliance or error correction in the studied tasks. | Bound conclusions to the experimental manipulations and outcomes; transparency is not equivalent to an explanation intervention. | [CHI 2021](https://doi.org/10.1145/3411764.3445315) | Promoted; bounded result cited in section 02 |
| C09 | Weber et al. (2024) | Peer-reviewed systematic review | Map finance uses across risk management, portfolios, markets, and anti-money laundering; identify uneven evidence coverage. | Do not infer regulatory compliance or operational effectiveness from the existence of applications. | [Management Review Quarterly](https://doi.org/10.1007/s11301-023-00320-0) | Publisher full text, volume, pages, and review corpus verified; promoted 2026-09-29, cited in section 04 |
| C10 | Rjoub et al. (2023) | Peer-reviewed survey | Organize cybersecurity uses, threat categories, and operational/adversarial challenges. | A survey supports the domain map; primary studies are still needed for concrete performance claims. | [IEEE TNSM](https://doi.org/10.1109/TNSM.2023.3282740) | DOI, venue, volume, issue, and pages verified; promoted 2026-09-29, cited in section 04 |
| C11 | Kuznietsov et al. (2024) | Peer-reviewed systematic review | Frame XAI in autonomous driving as interpretable design, surrogate explanation, monitoring, validation, and auxiliary communication. | Explanations can contribute to assurance but are not by themselves a safety case. | [IEEE T-ITS](https://doi.org/10.1109/TITS.2024.3474469) | DOI, venue, volume, issue, and pages verified; promoted 2026-09-29, cited in section 04 |
| C12 | Zhao et al. (2024) | Peer-reviewed survey | Establish that LLM explainability requires model- and paradigm-specific methods and faces distinct evaluation and faithfulness problems. | A taxonomy or generated rationale is not proof of faithful access to an LLM's internal computation. | [ACM TIST](https://doi.org/10.1145/3639372) | DOI, volume, issue, article number, and pages verified; promoted 2026-09-29, cited in section 04 |
| C13 | Lakkaraju et al. (2020) | Peer-reviewed primary methods study | Support the claim that an explanation fitted to one data distribution may cease to approximate the black box adequately after relevant distribution shifts; provide a bounded robust-explanation approach. | The tested framework covers declared perturbation sets and global linear or decision-set explanations; it does not prove universal robustness in production. | [ICML/PMLR](https://proceedings.mlr.press/v119/lakkaraju20a.html) | Full paper, authors, volume, pages, method, and experiments verified; promoted 2026-09-29, cited in section 04 |
| C14 | Roch et al. (2026) | Peer-reviewed cybersecurity user study | Show that explanations did not improve task performance or trust in the studied malicious-domain blocking task with participants who had cybersecurity knowledge. | Bound the result to the study population, task, interface, and explanation design; do not conclude that cybersecurity explanations are generally ineffective. | [USENIX Security 2026](https://www.usenix.org/conference/usenixsecurity26/presentation/roch) | Official open proceedings, authors, pages, and findings verified; promoted 2026-09-29, cited in section 04 |
| C15 | Kaufman et al. (2025) | Peer-reviewed autonomous-driving user study | Demonstrate that erroneous autonomous-vehicle explanations can reduce comfort, reliance, satisfaction, and perceived driving confidence even when driving behavior is held constant. | The outcomes are human judgments in simulated scenarios, not direct measures of vehicle safety. | [CHI 2025](https://doi.org/10.1145/3706598.3713088) | DOI, authors, article number, study design, and findings verified; promoted 2026-09-29, cited in section 04 |
| C16 | Turpin et al. (2023) | Peer-reviewed controlled LLM study | Support the bounded claim that chain-of-thought rationales can omit experimentally introduced factors that influenced model answers and can rationalize biased answers. | The result concerns specific models, prompting interventions, and tasks; it does not prove that all chain-of-thought is unfaithful. | [NeurIPS 2023](https://doi.org/10.52202/075280-3275) | Official proceedings, authors, volume, pages, and intervention verified; promoted 2026-09-29, cited in section 04 |
| C17 | Zaman and Srivastava (2026) | Peer-reviewed methodological counterpoint | Qualify hint-verbalization tests by showing that non-verbalization alone may conflate incompleteness with unfaithfulness and that conclusions vary across metrics and inference budgets. | This counterevidence does not establish that chain-of-thought is generally faithful; it establishes measurement dependence. | [ACL 2026](https://doi.org/10.18653/v1/2026.acl-long.2217) | Official ACL record, DOI, pages, methods, and conclusions verified; promoted 2026-09-29, cited in section 04 |

## APA 7 staging records

These records are formatted for controlled transfer. C01-C03 and C06-C08 entered the
production bibliography on 2026-09-29; the remaining records stay outside it until
they are cited in revised prose.

Alufaisan, Y., Marusich, L. R., Bakdash, J. Z., Zhou, Y., & Kantarcioglu, M. (2021). Does explainable artificial intelligence improve human decision-making? *Proceedings of the AAAI Conference on Artificial Intelligence, 35*(8), 6618–6626. https://doi.org/10.1609/aaai.v35i8.16819

European Parliament & Council of the European Union. (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence. *Official Journal of the European Union, L*, 2024/1689. https://eur-lex.europa.eu/eli/reg/2024/1689/oj

Ghassemi, M., Oakden-Rayner, L., & Beam, A. L. (2021). The false hope of current approaches to explainable artificial intelligence in health care. *The Lancet Digital Health, 3*(11), e745–e750. https://doi.org/10.1016/S2589-7500(21)00208-9

Kaufman, R. A., Broukhim, A., Kirsh, D., & Weibel, N. (2025). What did my car say? Impact of autonomous vehicle explanation errors and driving context on comfort, reliance, satisfaction, and driving confidence. In *Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems* (Article 89, pp. 1–17). Association for Computing Machinery. https://doi.org/10.1145/3706598.3713088

Kim, J., Maathuis, H., & Sent, D. (2024). Human-centered evaluation of explainable AI applications: A systematic review. *Frontiers in Artificial Intelligence, 7*, Article 1456486. https://doi.org/10.3389/frai.2024.1456486

Kuznietsov, A., Gyevnar, B., Wang, C., Peters, S., & Albrecht, S. V. (2024). Explainable AI for safe and trustworthy autonomous driving: A systematic review. *IEEE Transactions on Intelligent Transportation Systems, 25*(12), 19342–19364. https://doi.org/10.1109/TITS.2024.3474469

Lakkaraju, H., Arsov, N., & Bastani, O. (2020). Robust and stable black box explanations. In *Proceedings of the 37th International Conference on Machine Learning* (Vol. 119, pp. 5628–5638). PMLR. https://proceedings.mlr.press/v119/lakkaraju20a.html

Phillips, P. J., Hahn, C. A., Fontana, P. C., Yates, A. N., Greene, K. K., Broniatowski, D. A., & Przybocki, M. A. (2021). *Four principles of explainable artificial intelligence* (NISTIR 8312). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.IR.8312

Poursabzi-Sangdeh, F., Goldstein, D. G., Hofman, J. M., Vaughan, J. W., & Wallach, H. (2021). Manipulating and measuring model interpretability. In *Proceedings of the 2021 CHI Conference on Human Factors in Computing Systems* (Article 237, pp. 1–52). Association for Computing Machinery. https://doi.org/10.1145/3411764.3445315

Rjoub, G., Bentahar, J., Abdel Wahab, O., Mizouni, R., Song, A., Cohen, R., Otrok, H., & Mourad, A. (2023). A survey on explainable artificial intelligence for cybersecurity. *IEEE Transactions on Network and Service Management, 20*(4), 5115–5140. https://doi.org/10.1109/TNSM.2023.3282740

Roch, N., Sievers, H., Zufferey, N., & Zimmermann, V. (2026). You know why, but still rely: The impact of explainable AI on trust, task load, and performance in cybersecurity decision-making. In *35th USENIX Security Symposium (USENIX Security 26)* (pp. 1607–1625). USENIX Association. https://www.usenix.org/conference/usenixsecurity26/presentation/roch

Tabassi, E. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)* (NIST AI 100-1). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.AI.100-1

Turpin, M., Michael, J., Perez, E., & Bowman, S. R. (2023). Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting. *Advances in Neural Information Processing Systems, 36*, 74952–74965. https://doi.org/10.52202/075280-3275

Weber, P., Carl, K. V., & Hinz, O. (2024). Applications of explainable artificial intelligence in finance—A systematic review of finance, information systems, and computer science literature. *Management Review Quarterly, 74*(2), 867–907. https://doi.org/10.1007/s11301-023-00320-0

World Health Organization. (2021). *Ethics and governance of artificial intelligence for health: WHO guidance*. https://www.who.int/publications/i/item/9789240029200

Zaman, K., & Srivastava, S. (2026). Is chain-of-thought really not explainability? Chain-of-thought can be faithful without hint verbalization. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 48008–48030). Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.acl-long.2217

Zhao, H., Chen, H., Yang, F., Liu, N., Deng, H., Cai, H., Wang, S., Yin, D., & Du, M. (2024). Explainability for large language models: A survey. *ACM Transactions on Intelligent Systems and Technology, 15*(2), Article 20, 1–38. https://doi.org/10.1145/3639372

## Evidence gaps still open

The expanded pass is sufficient to support the chapter architecture, but not every
possible future claim. The remaining gaps are deliberately narrower:

- longitudinal evidence that explanation monitoring improves outcomes after real
  deployment, rather than merely detecting or characterizing change;
- multimodal-model faithfulness evidence if the chapter makes claims beyond the
  established LLM and autonomous-perception examples;
- explanation-specific attack evidence for a concrete operational cybersecurity
  effect beyond the current survey, user study, and general attack literature; and
- any concrete educational or public-service example if that optional domain is
  promoted to a full subsection.

## Transfer protocol

For each candidate actually used:

1. confirm the exact sentence it supports and retain the boundary in the prose;
2. add a stable citation key and checked metadata to `references.bib`;
3. add the matching APA 7 record to `references_apa7.md`;
4. record the cited location and acceptance decision in `citation_audit.md`; and
5. rerun the cited-versus-listed and DOI checks before rebuilding the Word file.
