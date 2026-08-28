# Venue conventions, measured

Load this when planning a paper's shape, budgeting pages, or deciding how many
figures and tables it needs.

## The default skeleton

`Introduction > Related Work > Method > Experiments > Conclusion`

Sixteen of 46 papers use exactly those five, and another ten differ only by
calling Method *Approach*. The median paper has **6** top-level sections; the
sixth is usually Acknowledgements or a named method section standing in for
"Method" (BEVDepth's is literally called `BEVDepth`).

Naming the method section after the method is a small, real signal of
confidence, and it costs nothing.

## Page and word budget

| | p25 | median | p75 |
|---|---|---|---|
| Body words (floats, maths and citations excluded) | 4,011 | 4,351 | 4,869 |
| Abstract words | 149 | 177 | 187 |
| Abstract sentences | — | 9 | — |
| Distinct references | 40 | 46 | 56 |
| `\cite` calls (a key cited twice counts twice) | 51 | 73 | 94 |
| `equation` / `align` environments | — | 8 | 11 |
| `algorithm` environments | — | 0 | — |

Two things to take from this. A CVPR-class paper is **about 4,400 words** of
actual prose — the eight pages are mostly floats. And an algorithm box is the
exception, not the norm: most of these papers put the method in equations and
a figure instead.

## Floats

| | |
|---|---|
| Figures per paper | median 6 |
| Tables per paper | median 6 |
| `figure*` (full page width) | 44% |
| `table*` | 25% |
| Placement `t` / `t!` / `!t` | 75% of all floats |
| Figures that are a single `\includegraphics` | 86% |
| Figures drawn in TikZ | **1 of 290** — an ablation bar chart |
| Tables using booktabs rules | 70% |

Essentially every figure is external artwork — the one TikZ figure in the
corpus is a bar chart. Composition — panels, insets, callouts — happens in the
drawing tool and arrives as one PDF, not as a LaTeX `subfigure` grid. See CVPR-Figure's `references/corpus-report.md` for what
that artwork is made of.

## Captions

| | median | p10 | p90 |
|---|---|---|---|
| Figure caption | 39 words | 7 | 84 |
| Table caption | 19 words | — | 45 |
| Teaser (first figure) caption | 49 words | | |

Figure captions are **twice as long as table captions**, and that asymmetry is
the point: a table's numbers speak for themselves and the caption says what is
being compared; a figure's caption has to carry the claim, because a reader
skimming the paper reads the teaser caption and nothing else on that page.

A four-word caption ("Overview of our framework.") is the most common
self-inflicted wound in a draft. It is also the easiest thing to fix.

## The teaser

The first figure sits **6.9% into the document** — top of page 1 or 2, before
Related Work. In 41 of 46 papers it is a single graphic. Only 10 of 46 make it
full width, so the default is a **single-column** teaser that sits beside the
introduction.

## What this does not tell you

These are conventions of three strong groups working mostly in 3D perception
and detection. A theory paper, a dataset paper or an HCI paper will differ,
and the numbers here should not be pushed onto them. The structural findings
(caption asymmetry, external artwork, top-anchored floats) travel further than
the word counts.
