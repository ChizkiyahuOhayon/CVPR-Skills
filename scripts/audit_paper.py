#!/usr/bin/env python3
"""Measure a LaTeX manuscript against the CVPR-class corpus.

    python3 scripts/audit_paper.py paper/            # a source directory
    python3 scripts/audit_paper.py main.tex --json

Every threshold is a percentile of 45 published papers from three groups whose
work this suite is calibrated on, not a style opinion. The point of the
percentiles is as much to say what is *fine* as what is not: `leverage`,
`utilize`, `robust`, `state-of-the-art` and the rule of three are all normal in
this literature, and blanket bans on them make a draft read less like the
venue, not more.

Levels:
  error  no paper in the corpus does this
  warn   outside the corpus's interquartile or 90th-percentile range
  note   worth a look; often a deliberate choice
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvprskills import tex, prose   # noqa: E402

COLOR = {"error": "\033[31m", "warn": "\033[33m", "note": "\033[2m"}
RESET = "\033[0m"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="+", help=".tex file or source directory")
    ap.add_argument("--profile", help="path to an alternative corpus profile")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true", help="errors and warnings only")
    a = ap.parse_args(argv)

    paper = tex.load(a.source)
    if paper is None:
        print("no file with \\documentclass found under %s" % ", ".join(a.source),
              file=sys.stderr)
        return 2

    prof = prose.load_profile(a.profile) if a.profile else None
    rep, stats = prose.audit(paper, prof)

    if a.json:
        print(json.dumps({
            "paper": paper.path, "stats": stats,
            "findings": [{"level": r.level, "code": r.code,
                          "message": r.message, "detail": r.detail}
                         for r in rep.rows],
            "counts": rep.counts()}, indent=1))
        return 1 if rep.counts()["error"] else 0

    tty = sys.stdout.isatty()
    kind = "compiled PDF" if stats.get("source_kind") == "pdf" else (paper.cls or "unknown class")
    print("%s  (%s)" % (paper.path, kind))
    print("  %d words | %d sentences (median %d words) | abstract %d words"
          % (stats["words"], stats["sentences"],
             stats["median_sentence_words"], stats["abstract_words"]))
    if stats.get("source_kind") == "pdf":
        print("  %d figures | %d tables | %d references"
              % (stats["figures"], stats["tables"], stats["references"]))
    else:
        print("  %d figures | %d tables | %d equations | %d references (%d \\cite calls)"
              % (stats["figures"], stats["tables"], stats["equations"],
                 stats["references"], stats["cites"]))
    print("  first person %.1f/1k words | hedges %.1f/10k words"
          % (stats["first_person_per_1k"], stats["hedges_per_10k"]))
    print("  sections: %s" % " > ".join(stats["sections"]))
    print()

    order = {"error": 0, "warn": 1, "note": 2}
    for r in sorted(rep.rows, key=lambda r: (order[r.level], r.code)):
        if a.quiet and r.level == "note":
            continue
        tag = r.level.upper()
        if tty:
            tag = COLOR[r.level] + tag + RESET
        print("%-14s %-20s %s" % (tag, r.code, r.message))
        if r.detail:
            print("%-14s %-20s   %s" % ("", "", r.detail))

    c = rep.counts()
    print("\n%d error(s), %d warning(s), %d note(s)"
          % (c["error"], c["warn"], c["note"]))
    stub = any(r.code == "too-short" for r in rep.rows)
    if stub:
        print("Too little prose to judge; most findings above are about length.")
    elif c["error"] == 0 and c["warn"] <= 2:
        print("Within the corpus distribution on every measured axis that matters.")
    return 1 if c["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
