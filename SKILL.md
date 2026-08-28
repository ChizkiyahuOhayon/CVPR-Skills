---
name: cvpr-skills
description: >-
  End-to-end research support for CVPR, ICCV, ECCV, NeurIPS, ICLR, ICML and AAAI
  papers, calibrated on measurements taken from 46 published papers by three
  strong vision groups. Covers shaping a research idea, checking novelty,
  designing experiments and ablations, drafting and revising prose, auditing a
  manuscript against the corpus distribution, verifying citations, simulating
  peer review, writing rebuttals, and submission compliance. Use for 顶会论文写作、
  论文润色、实验设计、审稿意见、rebuttal、投稿检查、论文查重引用核对、科研写作.
  Ships a working auditor: scripts/audit_paper.py measures a LaTeX draft against
  the corpus on structure, sentence length, voice, hedging and word frequency,
  where every threshold is a percentile of real published papers rather than a
  style opinion. Figures are owned by the separate cvpr-figure skill; data plots
  belong in matplotlib.
---

# CVPR-Skills — router

A paper-production suite whose advice has numbers behind it. The numbers come
from the LaTeX sources of 46 papers by Tsinghua MARS, Wenzhao Zheng's group and
Megvii — 289 figure environments, 300 tables, ~200k words of prose — summarised
in [`references/corpus/profile.json`](references/corpus/profile.json).

Read fragments from disk as directed. Do not work from memory of this file.

## 0. Route

Load [`references/workflow/routing.md`](references/workflow/routing.md) if the
request spans stages. Otherwise go straight to the row:

| The user wants | Go to |
|---|---|
| a direction turned into one defensible idea | §1 idea |
| to know whether it is already done | §2 novelty |
| how to structure the implementation | §2b code |
| an evaluation plan | §3 experiments |
| a framework / pipeline / teaser figure | **the `cvpr-figure` skill** |
| a bar chart, curve, heatmap, scatter | **matplotlib** — not this skill |
| prose drafted, restructured or polished | §4 write |
| a manuscript measured and diagnosed | §5 audit |
| how many references, how recent | §3b bibliography |
| citations verified | §6 citations |
| a reviewer report | §7 review |
| a rebuttal | §8 rebuttal |
| a submission check | §9 submit |

One owner per deliverable. "Make this better" is §4; "what is wrong with this"
is §7, and §7 does not rewrite.

## 1. Idea

Load [`references/craft/idea-shaping.md`](references/craft/idea-shaping.md).

Produce **one** idea with all five slots filled — problem, why it persists,
insight, method, falsification — not a menu. Name which of the corpus's
contribution shapes it is. If the falsification plan cannot be written, the
idea is not ready and saying so is the useful answer.

## 2. Novelty

Load [`references/audit/novelty.md`](references/audit/novelty.md). Search the
mechanism, not the topic; include rejected OpenReview submissions; read the
papers citing your nearest neighbour. Report as scooped / adjacent / clear,
with the three-column table for the nearest three papers.

## 2b. Code

Load [`references/craft/code.md`](references/craft/code.md).

Two shapes only — config-driven (mmengine) or class-driven — decided before the
training loop. Name modules for the **paper**, not the codebase, from day one.
Put every contribution behind a flag so the ablation is a config sweep rather
than four branches.

## 3. Experiments

Load [`references/corpus/experiment-design.md`](references/corpus/experiment-design.md).

Two benchmarks, an ablation that removes one component at a time and lands on
the baseline, and a cost table if any claim mentions efficiency. 44 of 46
corpus papers run an ablation; it is not optional.

**Do not over-build the statistics.** Measured across the corpus: **0 of 46
papers report a significance test**, 0 mention multiple seeds, and 11% report
any variance at all. A bootstrap-CI appendix will not be rewarded; another
ablation row will. The one exception is a headline gain under about a point,
where two or three seeds and a single sentence about the spread closes the
"is this noise" comment.

Tables live in Experiments (69% of them). Figures spread out: 32% Experiments,
16% Introduction, 15% Method. The first ablation table sits about 60% through
the paper's tables.

An appendix is optional — only 15 of 46 papers have one — and it holds *more of
what is already there*: qualitative results (73%), extra comparisons (73%),
implementation detail (53%). A result that exists only in the appendix will not
be read.

Never invent results. Design the table and leave the cells empty.

## 3b. Bibliography

Load [`references/corpus/bibliography.md`](references/corpus/bibliography.md).

**46 distinct references** (p25 40, p75 56), and **59% of them within three
years** of the newest thing cited. Only 16% are more than a decade old. A
related-work section whose newest citation is two years stale reads as a
project that stalled.

## 4. Write

Load [`references/corpus/writing-style.md`](references/corpus/writing-style.md)
and [`references/craft/anti-defensive.md`](references/craft/anti-defensive.md).
Load [`references/corpus/venue-conventions.md`](references/corpus/venue-conventions.md)
for structure and page budget.

The targets, all measured:

- ~4,400 words of prose; abstract 149–187 words, 9 sentences
- median sentence 19 words
- first person 20 per 1,000 words — *we propose*, not *it is proposed*
- hedges about 10 per 10,000 words: four or five in a whole paper
- figure captions ~39 words and stating a claim; table captions ~19

Before changing a word because it "sounds like AI", read
[`references/craft/humanizing.md`](references/craft/humanizing.md). `leverage`,
`utilize`, `robust`, `state-of-the-art`, the rule of three and the trailing
"-ing" clause are all normal in this literature — the last appears in **45 of
45** corpus papers. The real tells are `pivotal` (0 of 45), "the landscape of"
(0), and the em dash (2 of 45).

## 5. Audit — run this before any writing verdict

```bash
python3 scripts/audit_paper.py path/to/paper/        # or main.tex
python3 scripts/audit_paper.py paper/ --json         # machine-readable
```

- `error` — no paper in the corpus does this. Fix it.
- `warn` — outside the corpus interquartile or p90 range. Fix or justify.
- `note` — worth a look; often deliberate.

Calibration: the tool reports **zero errors across all 45 corpus papers** and
11 on a deliberately AI-written draft of comparable length. If it reports many
errors on human writing, the profile is wrong — say so rather than making the
author chase it.

Then the human pass in
[`references/audit/integrity.md`](references/audit/integrity.md): numbers in
the prose against numbers in the tables, claims against evidence, colours
consistent across figures. The tool does not read numbers.

## 6. Citations

Load [`references/audit/citation-audit.md`](references/audit/citation-audit.md).

```bash
pip install academic-refchecker[llm]
academic-refchecker --paper paper.pdf --report-file report.json --report-format json
```

If it is not installed, report the bibliography as **unaudited** rather than
skipping quietly. Then the layer no tool checks: does each citation support the
claim it is attached to, and does every borrowed baseline number match its
source at the same setting.

## 7. Review

Load [`references/audit/reviewer-simulation.md`](references/audit/reviewer-simulation.md).
Run §5 first so the review is not spent on mechanical findings.

Assess; do not rewrite. Keep relative progress and absolute readiness as two
separate scores and never average them. Every weakness names the table or line;
every score comes with the sentence that would change it.

## 8. Rebuttal

Load [`references/craft/rebuttal.md`](references/craft/rebuttal.md). New
numbers first, before any prose. Answer what was asked. Keep the ledger of
promised edits — the AC checks it.

## 9. Submit

Load [`references/audit/submission.md`](references/audit/submission.md). Page
limit without margin tricks, anonymity, embedded fonts, vector figures, no
`\todo`. Re-audit any figure that was resized.

## Working with cvpr-figure

Figures are a separate skill because they are a separate engine. If it is
installed, hand off at the figure stage; the two share the same corpus and the
same measurements, and the figure skill's
`references/corpus-report.md` is the visual half of this suite's evidence.

Draw figures **before** writing the method section. A framework figure forces
the method to be factored before it is described.

## Standing rules

1. **Never invent a result, a number, a citation or a figure crop.** Design the
   table and leave it empty; mark the placeholder.
2. **Cite the measurement.** When you tell an author their abstract is too
   long, say what the corpus range is. Advice with a number attached can be
   argued with; advice without one cannot.
3. **The corpus is three groups in mostly-3D vision.** Say so when the paper at
   hand is a theory, dataset or HCI paper — the structural findings travel, the
   word counts may not.
4. **Do not chase AI detectors.** Their false-positive rate on non-native
   English is high enough that optimising against them is both futile and
   unfair. Write like the venue; that is the same work and a better goal.
