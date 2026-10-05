import re, csv, statistics as st, datetime as dt
from pathlib import Path

HERE = Path(__file__).parent
PUB = {40: "2026-09-30", 39: "2026-06-30", 38: "2026-03-30", 37: "2025-12-30", 36: "2025-09-30"}
MONTHS = {m: i for i, m in enumerate(
    "January February March April May June July August September October November December".split(), 1)}
PL = dict(zip("stycznia lutego marca kwietnia maja czerwca lipca sierpnia września października listopada grudnia".split(),
              range(1, 13)))


def parse(s):
    m = re.search(r"(\d{1,2})\s+([A-Za-zśźń]+)\s+(\d{4})", s)
    if not m:
        return None
    mon = MONTHS.get(m.group(2).capitalize()) or PL.get(m.group(2).lower())
    return dt.date(int(m.group(3)), mon, int(m.group(1))) if mon else None


rows = []
for txt in sorted(HERE.glob("v*.txt")):
    vol = int(txt.stem[1:3])
    t = txt.read_text(encoding="utf-8", errors="replace")
    head = t[:6000]
    rec = re.search(r"(?:Received|Wpłynęło|Przyjęto do redakcji)\s*:\s*(.+)", head)
    acc = re.search(r"(?:Accepted|Zaakceptowano|Przyjęto)\s*:\s*(.+)", head)
    r, a = (parse(rec.group(1)) if rec else None), (parse(acc.group(1)) if acc else None)
    p = dt.date.fromisoformat(PUB[vol])
    pg = re.search(r"JCSI\s+\d+\s*\(\d{4}\)\s*(\d+)\s*[-–]\s*(\d+)", head)
    pages = int(pg.group(2)) - int(pg.group(1)) + 1 if pg else None
    lines = [l.strip() for l in head.splitlines() if l.strip()]
    title = ""
    for i, l in enumerate(lines):
        if l.startswith("Accepted") or l.startswith("Zaakceptowano"):
            title = " ".join(lines[i + 1:i + 3])[:110]
            break
    refs = len(set(re.findall(r"^\s*\[(\d+)\]\s", t[int(len(t) * 0.6):], flags=re.M)))
    figs = len(set(re.findall(r"(?:Figure|Rysunek)\s+(\d+)[:.]", t)))
    tabs = len(set(re.findall(r"(?:Table|Tabela)\s+(\d+)[:.]", t)))
    words = len(t.split())
    lublin = "Lublin University of Technology" in head or "Politechnika Lubelska" in head
    polish = bool(re.search(r"Streszczenie|Słowa kluczowe", head))
    stats = bool(re.search(r"p\s*[<=]\s*0[.,]\d|Wilcoxon|ANOVA|t-test|Friedman|Mann|confidence interval|Kruskal", t))
    hyp = bool(re.search(r"hypothes[ie]s|hipotez", t, flags=re.I))
    comp = bool(re.search(r"compar|porówn", title, flags=re.I))
    rows.append(dict(vol=vol, art=txt.stem.split("_")[1], received=r, accepted=a,
                     d_accept=(a - r).days if r and a else None,
                     d_publish=(p - r).days if r else None,
                     d_acc_pub=(p - a).days if a else None,
                     pages=pages, refs=refs, figs=figs, tabs=tabs, words=words,
                     lublin=lublin, polish=polish, stats=stats, hyp=hyp, comp=comp, title=title))

with (HERE / "jcsi.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

ok = [r for r in rows if r["d_publish"] is not None and r["d_accept"] is not None]
print("articles", len(rows), "with dates", len(ok))
for key in ("d_accept", "d_publish", "d_acc_pub"):
    v = sorted(r[key] for r in ok)
    print(key, "min", v[0], "q1", v[len(v)//4], "median", st.median(v), "q3", v[3*len(v)//4], "max", v[-1])
print("by volume: median received->accepted, received->published")
for vol in sorted(PUB):
    s = [r for r in ok if r["vol"] == vol]
    if s:
        print(vol, len(s), st.median(r["d_accept"] for r in s), st.median(r["d_publish"] for r in s),
              "received range", min(r["received"] for r in s), max(r["received"] for r in s))

ok.sort(key=lambda r: r["d_publish"])
third = len(ok) // 3
fast, slow = ok[:third], ok[-third:]
def prof(g, name):
    print(f"\n{name} n={len(g)} d_publish {g[0]['d_publish']}..{g[-1]['d_publish']}")
    for k in ("d_accept", "pages", "refs", "figs", "tabs", "words"):
        v = [r[k] for r in g if r[k] is not None]
        print(f"  {k}: median {st.median(v)} mean {st.mean(v):.1f}")
    for k in ("lublin", "polish", "stats", "hyp", "comp"):
        print(f"  {k}: {sum(r[k] for r in g)}/{len(g)}")
prof(fast, "FAST third"); prof(slow, "SLOW third")
eng26 = [r for r in ok if r["vol"] >= 38]
eng26.sort(key=lambda r: r["d_accept"])
print("\n2026 only, sorted by received->accepted")
for r in eng26:
    print(r["vol"], r["art"], r["received"], r["accepted"], r["d_accept"], r["d_publish"], r["pages"], r["refs"], r["figs"], r["tabs"],
          "L" if r["lublin"] else "-", "S" if r["stats"] else "-", r["title"][:70])
print("missing dates:", [(r["vol"], r["art"]) for r in rows if r not in ok])
