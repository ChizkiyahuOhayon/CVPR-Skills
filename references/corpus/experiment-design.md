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

## What a reviewer checks that a draft usually misses

- Is the baseline the *current* one, or the one that was current when the
  project started?
- Is the comparison at matched backbone, resolution and schedule? If not, is
  the mismatch stated in the caption rather than a footnote?
- Does the ablation remove one thing at a time, and does removing everything
  land on the stated baseline number?
- Are the gains larger than the seed variance? Almost no paper in this corpus
  reports error bars — which is a weakness of the literature, not a licence.
  Reporting them is cheap and disarms a whole class of review comment.
- Does any table report a number that contradicts a sentence in the text?
  `scripts/audit_paper.py` does not check this; a human must.
