#!/usr/bin/env python3
"""Regression tests. No dependencies; run with `python3 tests/test_audit.py`."""

import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from cvprskills import tex, prose   # noqa: E402

FAILED = []


def check(cond, label):
    print("  %s   %s" % ("ok  " if cond else "FAIL", label))
    if not cond:
        FAILED.append(label)


def section(name):
    print("\n== %s" % name)


TMP = tempfile.mkdtemp()


def write(name, body):
    p = os.path.join(TMP, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(body)
    return p


# --------------------------------------------------------------- the reader
section("latex reader")

MAIN = r"""
\documentclass[10pt,twocolumn,letterpaper]{article}
\begin{document}
\begin{abstract}
We propose a method. It works well on two benchmarks.
\end{abstract}
\section{Introduction}
% this comment must not be read
Sparse queries beat dense voxels \cite{a,b}. We show this on nuScenes.
\input{method}
\section{Experiments}
Results are in Table~\ref{tab:main}. We reach $42.1$ mIoU.
\begin{figure}[t]
\includegraphics[width=\linewidth]{overview.pdf}
\caption{Our framework predicts occupancy from surround images, and the sparse
query design is what recovers distant structure.}
\label{fig:overview}
\end{figure}
\begin{table}[t]
\caption{Comparison on nuScenes.}
\toprule
\label{tab:main}
\end{table}
\begin{equation}
y = Wx
\end{equation}
\section{Conclusion}
We presented a method.
\end{document}
"""
write("p/main.tex", MAIN)
write("p/method.tex", r"\section{Method}" "\n" r"We use a transformer \cite{c}.")

paper = tex.load([os.path.join(TMP, "p")])
check(paper is not None, "finds the file with \\documentclass")
check(paper.cls == "article", "reads the document class")
check("this comment must not be read" not in paper.body, "strips comments")
check("Method" in paper.top_sections, "splices \\input")
check(paper.top_sections == ["Introduction", "Method", "Experiments", "Conclusion"],
      "sections come out in document order")
check("We propose a method" in paper.abstract, "extracts the abstract")
check(len(paper.figures) == 1 and len(paper.tables) == 1, "counts floats")
check(paper.figures[0]["caption_words"] > 15, "measures caption length")
check(paper.tables[0]["booktabs"], "detects booktabs")
check(paper.figures[0]["graphics"] == ["overview.pdf"], "collects graphics refs")
check(paper.equations == 1, "counts equations")
check(paper.cites == 2, "counts \\cite calls across inlined files")
check(paper.references == 3, "counts distinct reference keys, not calls")
check("MATH" in paper.body and "42.1" not in paper.body, "maths is masked, not counted as prose")
check("CITE" in paper.body, "citations are masked")
check("Comparison on nuScenes" not in paper.body, "float bodies stay out of the prose")

section("environment scanner")
nested = r"\begin{figure}\begin{figure}\end{figure}\caption{x}\end{figure}"
check(len(tex.envs(nested, "figure")) == 2, "nested environments are matched, not truncated")
check(tex.caption_of(r"\caption{a {nested} brace}") == "a {nested} brace",
      "captions survive nested braces")
check(tex.normalise_section("Our Approach") == "Approach", "section names normalise")

# ------------------------------------------------------------------ counting
section("tell counting")
c = prose.count_tells("We leverage a pivotal — approach, showing gains.")
check(c["leverage"] == 1, "counts leverage")
check(c["pivotal"] == 1, "counts pivotal")
check(c["emdash"] == 1, "counts em dashes")
check(c["by_ing"] == 1, "counts trailing -ing clauses")
check(prose.count_tells("A, B, and C")["rule_of_three"] == 1, "counts rule of three")
check(prose.count_tells("EM—DASH")["emdash"] == 1, "em dash check is case-insensitive-safe")

# ------------------------------------------------------------------- profile
section("shipped profile")
P = prose.load_profile()
check(P["provenance"]["papers"] >= 40, "profile covers the corpus")
for key in prose.TELLS:
    if key not in P["tells"]:
        check(False, "profile is missing a measured pattern: %s" % key)
        break
else:
    check(True, "every pattern the auditor counts has a measured baseline")
check(P["tells"]["pivotal"]["papers_zero"] == P["tells"]["pivotal"]["n"],
      "pivotal is absent from every corpus paper")
check(P["tells"]["by_ing"]["papers_zero"] == 0,
      "the trailing -ing clause appears in every corpus paper")
check(P["figures"]["tikz_share"] < 0.01,
      "essentially no corpus figure uses tikz (1 of 290)")
check(15 <= P["sentences"]["median_words"]["median"] <= 24, "sentence target is sane")

# -------------------------------------------------------------- the auditor
section("auditor behaviour")
rep, stats = prose.audit(paper)
check(isinstance(stats["words"], int), "returns statistics")
codes = {r.code for r in rep.rows}
check("too-short" in codes, "a stub draft is flagged as too short to judge")

AI = r"""
\documentclass{article}
\begin{document}
\begin{abstract}
In the rapidly evolving landscape of vision, we delve into a pivotal and
nuanced realm, showcasing a holistic tapestry of cutting-edge innovation.
\end{abstract}
\section{Introduction}
%s
\end{document}
""" % (("It is worth noting that this meticulous and seamless framework may "
        "potentially underscore the vital, pivotal role of innovation. "
        "Furthermore, the intricate design could arguably showcase remarkable "
        "gains — a nuanced realm indeed. ") * 40)
write("ai/main.tex", AI)
rep_ai, st_ai = prose.audit(tex.load([os.path.join(TMP, "ai")]))
check(st_ai["words"] >= prose.RATE_MIN_WORDS, "the AI fixture is long enough to rate")
check(rep_ai.counts()["error"] >= 5, "AI-flavoured prose raises errors")
check(any(r.code == "alien-phrase" and "pivotal" in r.message for r in rep_ai.rows),
      "pivotal is named specifically")
check(any(r.code == "defensive" for r in rep_ai.rows), "hedging is flagged")

# the same text, too short to rate: only absence-based errors may fire
write("ai_short/main.tex", AI.replace(") * 40", ") * 1")
      if ") * 40" in AI else AI[:AI.index("\\section{Introduction}")]
      + "\\section{Introduction}\nIt is pivotal.\n\\end{document}")
rep_s, st_s = prose.audit(tex.load([os.path.join(TMP, "ai_short")]))
check(st_s["words"] < prose.RATE_MIN_WORDS, "the short fixture is under the rate floor")
check(all("per 10k" not in r.message for r in rep_s.rows if r.code == "overused"),
      "frequency findings are suppressed below the rate floor")
check(any("pivotal" in r.message for r in rep_s.rows),
      "absence-based findings still fire on a short draft")

section("normal words are not punished")
NORMAL = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
%s
\end{document}
""" % (("We propose a robust method. We leverage temporal cues and utilize a "
        "comprehensive objective. By aggregating features, we obtain state-of-the-art "
        "results that are accurate, efficient, and general. This enables the model to "
        "capture structure. Furthermore, we evaluate on two benchmarks. ") * 40)
write("normal/main.tex", NORMAL)
rep_n, st_n = prose.audit(tex.load([os.path.join(TMP, "normal")]))
check(st_n["words"] >= prose.RATE_MIN_WORDS, "the fixture is long enough to rate")
flagged = {r.message.split()[0].strip('"') for r in rep_n.rows
           if r.code in ("alien-phrase", "rare-phrase")}
for w in ("leverage", "utilize", "robust", "state-of-the-art"):
    check(w not in flagged, "%s is not treated as a tell" % w)
check(rep_n.counts()["error"] == 0, "ordinary venue vocabulary raises no errors")

# ------------------------------------------------------------------- the CLI
section("cli")
env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "scripts"))
r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "audit_paper.py"),
                    os.path.join(TMP, "ai"), "--json"],
                   capture_output=True, text=True, env=env)
check(r.returncode == 1, "exit status is 1 when there are errors")
out = json.loads(r.stdout)
check(out["counts"]["error"] >= 5, "json report carries the findings")
check("stats" in out and "findings" in out, "json report has both halves")

r2 = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "audit_paper.py"),
                     os.path.join(TMP, "nothing-here")],
                    capture_output=True, text=True, env=env)
check(r2.returncode == 2, "missing source exits 2, not a traceback")

section("docs stay in step with the code")
skill = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
agents = open(os.path.join(ROOT, "AGENTS.md"), encoding="utf-8").read()
import re
for doc, name in ((skill, "SKILL.md"), (agents, "AGENTS.md")):
    for path in set(re.findall(r"\((references/[\w./-]+)\)", doc)):
        if not os.path.exists(os.path.join(ROOT, path)):
            check(False, "%s links to a missing file: %s" % (name, path))
            break
    else:
        check(True, "%s links only to files that exist" % name)

# Only the declared `path:` values are this repo's own; prose in the
# companion_skills block names files that live in the sibling skill.
man = open(os.path.join(ROOT, "manifest.yaml"), encoding="utf-8").read()
for path in set(re.findall(r"^\s*(?:-\s*)?(?:path|profile|rebuild):\s*(\S+)",
                           man, re.M)):
    if not os.path.exists(os.path.join(ROOT, path)):
        check(False, "manifest declares a missing path: %s" % path)
        break
else:
    check(True, "every path the manifest declares exists")

shutil.rmtree(TMP, ignore_errors=True)
print("\n%s  (%d failure%s)" % ("FAILED" if FAILED else "ALL PASSED",
                               len(FAILED), "" if len(FAILED) == 1 else "s"))
sys.exit(1 if FAILED else 0)
