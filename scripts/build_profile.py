#!/usr/bin/env python3
"""Rebuild references/corpus/profile.json from a directory of LaTeX sources.

Run this, not an ad-hoc script, so the profile and the auditor are produced by
the same reader.  If they diverge, a draft gets compared against numbers that
were computed a slightly different way, and the difference shows up as
findings that are really just measurement drift.

    python3 scripts/build_profile.py /path/to/sources -o references/corpus/profile.json

Each immediate subdirectory of the source directory is treated as one paper.
The sources themselves are not redistributable and are not in this repository;
the shipped profile.json is the summary they produced.
"""

import argparse
import collections
import json
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvprskills import tex, prose   # noqa: E402


def q(vals, p):
    v = sorted(vals)
    return v[int(p * (len(v) - 1))] if v else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", help="directory whose subdirectories are papers")
    ap.add_argument("-o", "--out", default="references/corpus/profile.json")
    ap.add_argument("--min-words", type=int, default=800)
    a = ap.parse_args(argv)

    papers = []
    for d in sorted(os.listdir(a.sources)):
        p = os.path.join(a.sources, d)
        if not os.path.isdir(p):
            continue
        paper = tex.load([p])
        if paper is None:
            continue
        words = len(paper.body.split())
        if words < a.min_words:
            continue
        papers.append((d, paper, words))
    if not papers:
        raise SystemExit("no papers parsed under %s" % a.sources)

    figs = [f for _, p, _ in papers for f in p.figures]
    tabs = [t for _, p, _ in papers for t in p.tables]

    def med(vals):
        return round(st.median(vals), 2) if vals else None

    sent_meds, sent_p90s, fps = [], [], []
    tell_rates = {k: [] for k in list(prose.TELLS) + ["hedge", "rule_of_three"]}
    tell_zero = {k: 0 for k in tell_rates}
    for _, p, words in papers:
        s = [len(x.split()) for x in p.sentences()]
        if s:
            sent_meds.append(st.median(s))
            sent_p90s.append(q(s, 0.9))
        fps.append(1000.0 * len(re.findall(r"\b(we|our|us)\b", p.body.lower())) / words)
        got = prose.count_tells(p.body)
        for k in tell_rates:
            tell_rates[k].append(10000.0 * got[k] / words)
            if got[k] == 0:
                tell_zero[k] += 1

    prof = {
        "provenance": {
            "papers": len(papers),
            "figure_environments": len(figs),
            "table_environments": len(tabs),
            "built_by": "scripts/build_profile.py using cvprskills.tex",
            "note": "Percentiles are over papers, not over sentences. Rates are "
                    "per 10,000 words of prose after floats, maths, citations "
                    "and macros are removed.",
        },
        "structure": {
            "sections": {"median": med([len([s for s in p.top_sections
                                             if s not in ("Acknowledgements", "Appendix")])
                                        for _, p, _ in papers])},
            "canonical": ["Introduction", "Related Work", "Method",
                          "Experiments", "Conclusion"],
            "abstract_words": {
                "median": med([len(p.abstract.split()) for _, p, _ in papers if p.abstract]),
                "p25": q([len(p.abstract.split()) for _, p, _ in papers if p.abstract], .25),
                "p75": q([len(p.abstract.split()) for _, p, _ in papers if p.abstract], .75)},
            "body_words": {"median": med([w for _, _, w in papers]),
                           "p25": q([w for _, _, w in papers], .25),
                           "p75": q([w for _, _, w in papers], .75)},
            "equations": {"median": med([p.equations for _, p, _ in papers]),
                          "p75": q([p.equations for _, p, _ in papers], .75)},
            "cite_calls": {"median": med([p.cites for _, p, _ in papers]),
                           "p25": q([p.cites for _, p, _ in papers], .25),
                           "p75": q([p.cites for _, p, _ in papers], .75)},
            "references": {"median": med([p.references for _, p, _ in papers]),
                           "p25": q([p.references for _, p, _ in papers], .25),
                           "p75": q([p.references for _, p, _ in papers], .75)},
        },
        "sentences": {"median_words": {"median": med(sent_meds),
                                       "p25": q(sent_meds, .25),
                                       "p75": q(sent_meds, .75)},
                      "p90_words": {"median": med(sent_p90s)}},
        "voice": {"first_person_per_1k": {"median": med(fps),
                                          "p25": round(q(fps, .25), 2),
                                          "p75": round(q(fps, .75), 2)}},
        "figures": {
            "per_paper": {"median": med([len(p.figures) for _, p, _ in papers])},
            "tables_per_paper": {"median": med([len(p.tables) for _, p, _ in papers])},
            "full_width_share": round(sum(f["star"] for f in figs) / max(len(figs), 1), 3),
            "caption_words": {
                "median": med([f["caption_words"] for f in figs if f["caption_words"]]),
                "p10": q([f["caption_words"] for f in figs if f["caption_words"]], .10),
                "p90": q([f["caption_words"] for f in figs if f["caption_words"]], .90)},
            "table_caption_words": {
                "median": med([t["caption_words"] for t in tabs if t["caption_words"]]),
                "p90": q([t["caption_words"] for t in tabs if t["caption_words"]], .90)},
            "single_graphic_share": round(
                sum(1 for f in figs if len(f["graphics"]) == 1) / max(len(figs), 1), 3),
            "tikz_share": round(sum(1 for f in figs if f["tikz"]) / max(len(figs), 1), 3),
            "booktabs_share": round(sum(1 for t in tabs if t["booktabs"]) / max(len(tabs), 1), 3),
        },
        "placement": _placement(papers),
        "bibliography": _bibliography(a.sources, papers),
        "rigour": _rigour(papers),
        "tells": {k: {"median": round(st.median(v), 2),
                      "p75": round(q(v, .75), 2),
                      "p90": round(q(v, .90), 2),
                      "max": round(max(v), 2),
                      "papers_zero": tell_zero[k],
                      "n": len(papers)}
                  for k, v in tell_rates.items()},
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(prof, fh, indent=1)
    print("wrote %s from %d papers, %d figures, %d tables"
          % (a.out, len(papers), len(figs), len(tabs)))
    return 0


def _placement(papers):
    """Which section each float lives in -- where the evidence actually sits."""
    figs, tabs = collections.Counter(), collections.Counter()
    appendix = 0
    for _, p, _ in papers:
        for f in p.figures:
            figs[f["section"]] += 1
        for t in p.tables:
            tabs[t["section"]] += 1
        if re.search(r"\\appendix|\\section\*?\{\s*(Appendix|Supplement)", p.doc, re.I):
            appendix += 1
    tf, tt = max(sum(figs.values()), 1), max(sum(tabs.values()), 1)
    return {
        "figures_by_section": {k: round(v / tf, 3) for k, v in figs.most_common(8)},
        "tables_by_section": {k: round(v / tt, 3) for k, v in tabs.most_common(8)},
        "papers_with_appendix": round(appendix / max(len(papers), 1), 3),
    }


def _bibliography(root, papers):
    """Reference years, absolute and relative to each paper's newest citation."""
    all_years, rel = [], []
    n = 0
    for name, _p, _w in papers:
        d = os.path.join(root, name)
        ys = []
        for base, _dirs, names in os.walk(d):
            for fn in names:
                if not fn.endswith((".bib", ".bbl")):
                    continue
                with open(os.path.join(base, fn), encoding="utf-8",
                          errors="ignore") as fh:
                    t = fh.read()
                ys += [int(y) for y in re.findall(
                    r'(?:year\s*=\s*[{"\s]*|\(|\s)((?:19|20)\d{2})[},")\s.]', t)]
        ys = [y for y in ys if 1980 <= y <= 2030]
        if len(ys) < 10:
            continue
        n += 1
        all_years += ys
        newest = max(ys)
        rel += [newest - y for y in ys]
    if not all_years:
        return {}
    all_years.sort()
    rel.sort()
    c = collections.Counter(all_years)
    tot = float(len(all_years))
    return {
        "papers": n,
        "year_median": st.median(all_years),
        "year_p10": all_years[len(all_years) // 10],
        "year_p90": all_years[9 * len(all_years) // 10],
        "share_older_than_10y": round(
            sum(v for k, v in c.items() if max(all_years) - k > 10) / tot, 3),
        "age_vs_newest_median": st.median(rel),
        "age_vs_newest_p75": rel[3 * len(rel) // 4],
        "share_within_3y_of_newest": round(
            sum(1 for r in rel if r <= 3) / float(len(rel)), 3),
    }


def _rigour(papers):
    """How much statistics this literature actually reports."""
    pats = {
        "significance_test": r"p\s*[<=]\s*0?\.0|p-value|statistically significant"
                             r"|t-test|wilcoxon|mann-whitney|anova|bonferroni",
        "error_bars": r"\\pm|\u00b1|standard deviation|std\.|error bar"
                      r"|confidence interval",
        "multiple_seeds": r"\b(three|five|3|5|10)\s+(random\s+)?seeds"
                          r"|averaged over .{0,20}runs|multiple runs",
        "ablation": r"\bablation",
    }
    out = {}
    for k, rx in pats.items():
        out[k] = round(sum(1 for _, p, _ in papers
                           if re.search(rx, p.raw, re.I)) / max(len(papers), 1), 3)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
