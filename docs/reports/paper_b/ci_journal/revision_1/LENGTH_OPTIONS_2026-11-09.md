# Paper B revision 1: options to shorten the manuscript (2026-11-09)

**Decision (author, 2026-11-09):** submit at 15 pages. The journal sets no length limit (its
articles run 7 to 17 pages), so the editor decides. Apply these options only if the editor or a
reviewer asks for a shorter paper. They supersede the 12-page budget of D-C (2026-11-06).

## Where the length is (after C-051, 15 pages)

| Part | Words | Floats |
|---|---:|---|
| §1 Introduction, §2 Background | 890 | |
| §3 Materials and Methods (six subsections) | 1,470 | Table 1 (design) |
| §4 Results | 1,850 | Tables 2, 3, 4; Figure 1. Largest: §4.3 sweep 575, §4.4 controls 399 |
| §5 Discussion | 660 | Table 5 (what holds where) |
| §6 Conclusions | 363 | |
| References | 53 entries | about 2 pages |

## Options, least to most invasive

| # | Cut | Saves | Cost to the paper |
|---|---|---|---|
| 1 | Conclusions to 150-180 words: answer the title question and its conditions, without restating §5 | 0.4 p | None; most repetitive part |
| 2 | §4.3 and §4.4: keep each ordering and its condition, move per-setting numbers to S10 and S11 | 0.8 p | Low |
| 3 | Table 4 (other datasets) and Table 3 (cost) to the supplement, 2-3 sentences each in the text | 0.8 p | Medium; cost was a reviewer theme (R1-5, R2-1), so moving Table 3 is riskier than Table 4 |
| 4 | §3: statistical detail (bootstrap, Hodges-Lehmann, rank-biserial) and the host description to the supplement; Table 1 to one sentence | 0.6 p | Low to medium |
| 5 | §1-§2 trimmed by about 250 words | 0.4 p | Low |
| 6 | References 53 to about 40, dropping older background-only entries | 0.4 p | Low; raises the share from 2024 on |
| 7 | Figure 1 shorter (panel height, legend) | 0.1 p | None |

- About 12 pages: options 1, 2, 4, 5, 6 and 7, plus option 3 for Table 4 only. Every result a
  reviewer asked about stays in the main text.
- About 13-14 pages: options 1, 2 and 7.

## When applying any option

1. The response letter cites sections, tables and figures by number: update every reference
   when a table moves (`check_revision.py` and the consistency report catch stale ones).
2. Each item moved to the supplement leaves one sentence with its conclusion and the S-section.
3. Log the change as a C-### row; rebuild the manuscript and the supplement.
