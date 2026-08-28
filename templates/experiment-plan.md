# Experiment plan — <method name>

Fill this in **before** running anything. The point is to commit to what would
falsify the idea while it is still cheap to be wrong.

## The claim

One sentence, with a number in it once you have one.

> Sparse queries recover distant structure that dense voxel grids miss, at
> lower memory.

## Falsification

```
If the insight is right, then <specific measurable pattern> on <benchmark>.
If it is wrong, I will see <specific other outcome>.
The experiment that distinguishes them is <experiment>, taking <time>.
```

If line two is "the numbers will be lower", sharpen it. A good falsification
names *which subset* improves and why the insight predicts that split.

## Benchmarks

Two, not one: a primary where the method is designed to win, and a second
showing it did not overfit to the first.

| | Dataset | Split | Metric | Why this one |
|---|---|---|---|---|
| Primary | | | | |
| Secondary | | | | |

## Baselines

Current, not the ones that were current when the project started.

| Method | Venue/year | Backbone | Resolution | Schedule | Number source |
|---|---|---|---|---|---|

Mark each number as **reproduced** or **quoted**. Where a setting differs from
ours, that goes in the table caption, not a footnote.

## Main comparison — Table 1

Columns, and the direction of each. Bold best, underline second.

## Ablation — Table 2

One row per component, cumulative. Removing everything must land on the stated
baseline number; if it does not, the ablation is measuring something else.

| Row | Component removed | Expected effect | Actual |
|---|---|---|---|
| 1 | (baseline) | | |
| 2 | | | |
| 3 | | | |
| 4 | (full) | | |

## Cost — Table 3

Required if any claim mentions efficiency. Parameters, FLOPs, latency, peak
memory, and the hardware they were measured on.

## Variance

How many seeds, and what the spread is. Almost no paper in the corpus reports
this, which is a weakness of the literature rather than a licence — reporting
it is cheap and disarms a whole class of review comment.

## Qualitative figure

Which inputs, which predictions, which baseline to show beside them. Real
crops from your own checkpoint. See the CVPR-Figure skill: 57% of framework
figures in this literature embed real rasters.

## Compute budget

| Experiment | GPU-hours | Blocking? |
|---|---|---|

## What would make me stop

Write it down now, while you can still be honest about it.
