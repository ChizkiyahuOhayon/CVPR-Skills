# Experiments, measured

Load this when planning an evaluation, deciding what tables a paper needs, or
reviewing whether an experiment section is complete.

## What the tables are for

Purpose of all 300 table environments, from the first 90 characters of the
caption:

| Share | Purpose |
|---|---|
| 33% | comparison against prior work |
| 22% | **ablation** |
| 13% | results on a benchmark |
| 8% | performance breakdown |
| 4% | analysis |
| ~17% | other (dataset statistics, hyper-parameters, runtime) |

**43 of 46 papers run an ablation.** Together with the comparison tables, over
half of every table in the corpus is doing one of two jobs: *are we better than
them*, and *which part of us made it better*. A paper missing the second is
missing the half reviewers argue about.

## The standard sequence

Reconstructed from table order across the corpus:

1. **Main comparison** — the headline benchmark, prior work sorted by date,
   yours last, best in bold, second-best underlined.
2. **Ablation on the contribution** — one row per component, cumulative. This
   is the table the rebuttal will be about.
3. **A design-choice study** — the hyper-parameter or variant grid.
4. **Cost** — parameters, FLOPs, latency or memory. Roughly a third of the
   corpus reports at least one; if the paper's claim is efficiency, it is
   mandatory and belongs in table 1.
5. **Qualitative figure** — not a table, but part of the evidence, and 57% of
   this literature's framework figures already carry real predictions.

## Benchmarks

Datasets named across the corpus, by number of papers:

| Papers | Dataset |
|---|---|
| 17 | nuScenes |
| 14 | ImageNet |
| 11 | Waymo Open |
| 10 | COCO |
| 8 | KITTI |
| 5 | Occ3D, ScanNet |
| 2–3 | Argoverse, SemanticKITTI, Cityscapes, OpenOcc, VOT |

Two benchmarks is the norm, not one: a primary where the method is designed to
win, and a second that shows it did not overfit to the first.

## Writing the experiment section

The corpus pattern, in order:

1. **Setup** — dataset, split, metric, and the sentence that says what
   "better" means here. Short.
2. **Implementation details** — backbone, resolution, schedule, hardware,
   batch size. Reviewers use this paragraph to decide whether the comparison
   is fair, so under-specifying it is expensive.
3. **Main results** — the table, then two or three sentences that say *what the
   number means*, not what the number is. "We reach 42.1 mIoU" is the table's
   job; "the gain is concentrated on distant voxels, which is where the sparse
   query design should help" is the paper's.
4. **Ablation** — one paragraph per component, each ending in the sentence a
   reviewer would otherwise have to write themselves.
5. **Analysis / failure cases** — where the honest papers separate from the
   rest.

## How much statistics this literature actually does

Measured across all 46 papers:

| | Papers doing it |
|---|---|
| Any significance test (p-value, t-test, ANOVA, Wilcoxon…) | **0 of 46** |
| Error bars, ±, standard deviation, confidence intervals | 5 of 46 (11%) |
| Multiple seeds mentioned at all | **0 of 46** |
| An ablation | 44 of 46 (96%) |

This is not an endorsement — a field that never reports variance is a field
where some reported gains are noise. But it is the norm you are writing into,
and it has a direct consequence for how to spend effort:

**Do not build a statistical apparatus this venue does not use.** A paper with
bootstrap confidence intervals on every cell, a Bonferroni correction and a
significance-test appendix will not be rewarded for it, and the effort would
have bought another ablation row — which *is* what 96% of the corpus does and
what reviewers argue about.

What is worth doing, in order:

1. **Run the ablation properly.** One component removed at a time, landing on
   the baseline. This is the highest-value experiment in the paper.
2. **If a gain is small (under ~1 point on the headline metric), run two or
   three seeds and say the spread in one sentence.** Not a table, not a test —
   a sentence. This costs a day and closes the "is this noise" review comment.
3. **Match the settings.** An unmatched backbone or schedule invalidates more
   comparisons than any amount of variance reporting would rescue.

Skip: p-values, hypothesis tests, power analysis, corrections for multiple
comparisons. They belong in fields with human subjects or small samples, and
importing them here signals unfamiliarity rather than rigour.

## Where the evidence sits

Which section each float lives in, across 289 figures and 300 tables:

| | Figures | Tables |
|---|---|---|
| Experiments | 32% | **69%** |
| Introduction (the teaser) | 16% | — |
| Method | 15% | 9% |
| Related Work | 7% | — |
| Appendix | 2% | 2% |

Tables are almost entirely an Experiments-section object; figures are spread
across the paper because the teaser and the method figure both carry argument.

Within the Experiments section, the **first ablation table sits about 60% of
the way through the paper's tables** — after the main comparison and the
benchmark results, before the cost and analysis tables.

## The appendix

Only **15 of 46 papers have one at all**, so it is optional, not expected. Of
those that do:

| Share | Contains |
|---|---|
| 73% | more qualitative results |
| 73% | additional comparisons |
| 53% | implementation details spilled from the main text |
| 33% | dataset details |
| 27% | limitations and failure cases |
| 27% | proofs or derivations |
| 20% | further ablations |

The pattern: an appendix holds **more of what is already in the paper**, not a
different kind of argument. A result that only exists in the appendix will not
be read. If a reviewer needs it to accept the paper, it belongs in the main
text — and something else has to go.

## What a reviewer checks that a draft usually misses

- Is the baseline the *current* one, or the one that was current when the
  project started?
- Is the comparison at matched backbone, resolution and schedule? If not, is
  the mismatch stated in the caption rather than a footnote?
- Does the ablation remove one thing at a time, and does removing everything
  land on the stated baseline number?
- Are the gains larger than the seed variance? See the section below before
  deciding how much to do about this.
- Does any table report a number that contradicts a sentence in the text?
  `scripts/audit_paper.py` does not check this; a human must.
