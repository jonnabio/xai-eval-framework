#!/usr/bin/env python3
"""Insert each reviewer comment, cut verbatim from DECISION_LETTER.md, before its answer in
RESPONSE_TO_REVIEWERS.md (author request 2026-11-24: the letter carries the full text).
Idempotent: earlier quote blocks are replaced. Fails if any cut point is not found."""
import re
import sys
from pathlib import Path

REV = Path(__file__).resolve().parents[1]
letter = (REV / "DECISION_LETTER.md").read_text(encoding="utf-8")


def section(start: str, end: str) -> str:
    a = letter.index(start)
    b = letter.index(end, a)
    return letter[a:b]


r1 = section("## Reviewer-1", "## Reviewer-2")
r2 = section("## Reviewer-2", "## Reviewer-3")
r3 = letter[letter.index("## Reviewer-3"):]


def between(text: str, a: str, b: str | None) -> str:
    i = text.index(a)
    j = text.index(b, i + len(a)) if b else len(text)
    return " ".join(text[i:j].split()).strip()


def editor(text: str) -> str:
    return between(text, "**1. Comments to Editor:**", "**2. Comments to Author:**").replace(
        "**1. Comments to Editor:**", "Comments to the editor:").strip()


def numbered(text: str, n: int, last: str) -> str:
    body = text[text.index("**2. Comments to Author:**"):]
    nxt = f" {n + 1}. " if n < last else None
    return between(body, f" {n}. ", nxt)


Q = {}
Q["ED-1"] = "Decision: Major Revision (Editor, Remzi Gürfidan, November 24, 2026)."
# Reviewer 1
a1 = r1[r1.index("**2. Comments to Author:**"):]
Q["R1-0"] = " ".join([editor(r1),
                      "Comments to the author (general): " + between(a1, "The manuscript presents", " 1. "),
                      "Closing: " + between(a1, "These points do not require", "**Comments and Suggestions"),
                      "Comments and suggestions: " + between(r1, "**Comments and Suggestions for Author:**",
                                                             "**Recommendation:**").replace(
                          "**Comments and Suggestions for Author:** ", ""),
                      "Recommendation: Minor Revision."])
for n in range(1, 6):
    q = numbered(r1, n, 5)
    Q[f"R1-{n}"] = q.split(" These points do not require")[0].strip()
# Reviewer 2
a2 = r2[r2.index("**2. Comments to Author:**"):]
Q["R2-0"] = " ".join([editor(r2),
                      "Comments to the author (general): " + between(a2, "The manuscript investigates", " 1. "),
                      "Comments and suggestions: " + between(r2, "**Comments and Suggestions for Author:**",
                                                             "**Recommendation:**").replace(
                          "**Comments and Suggestions for Author:** ", ""),
                      "Recommendation: Major Revision."])
for n in range(1, 7):
    q = numbered(r2, n, 6)
    Q[f"R2-{n}"] = q.split("**Comments and Suggestions")[0].strip()
# Reviewer 3: one paragraph, cut at its sentences
a3 = r3[r3.index("**2. Comments to Author:**") + len("**2. Comments to Author:**"):]
cuts = [("R3-0", "This manuscript investigates", "The primary concern"),
        ("R3-1", "The primary concern", "A second concern"),
        ("R3-2", "A second concern", "The experimental design on the Adult"),
        ("R3-3", "The experimental design on the Adult", "Another aspect"),
        ("R3-4", "Another aspect", "The quality of the writing"),
        ("R3-5", "The quality of the writing", "Overall, I find"),
        ("R3-6", "Overall, I find", "**Comments and Suggestions")]
for key, a, b in cuts:
    Q[key] = between(a3, a, b)
Q["R3-0"] = editor(r3) + " " + Q["R3-0"]
Q["R3-6"] += (" Comments and suggestions: I'd like to thank to author(s) for their valuable study."
              " Recommendation: Major Revision.")

path = REV / "RESPONSE_TO_REVIEWERS.md"
text = path.read_text(encoding="utf-8")
text = re.sub(r"(?m)^> \*\*Reviewer comment[^\n]*\n(?:>[^\n]*\n)*\n?", "", text)
text = re.sub(r"(?m)^> \*\*Editor's decision[^\n]*\n(?:>[^\n]*\n)*\n?", "", text)
for key, quote in Q.items():
    label = "Editor's decision" if key == "ED-1" else "Reviewer comment"
    block = f"> **{label} ({key}).** {quote}\n\n"
    marker = f"**{key}."
    if text.count(marker) != 1:
        sys.exit(f"answer heading for {key} not found once")
    i = text.index(marker)
    text = text[:i] + block + text[i:]
path.write_text(text, encoding="utf-8")
print(f"quoted {len(Q)} comments")
