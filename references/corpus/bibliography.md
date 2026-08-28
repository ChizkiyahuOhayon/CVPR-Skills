# The bibliography, measured

Load this when building a related-work section, or when a reviewer says the
citations are thin or dated.

Measured across the `.bib` and `.bbl` files of all 46 papers — 6,726 dated
reference entries.

## How many

| | p25 | median | p75 |
|---|---|---|---|
| Distinct references | 40 | **46** | 56 |
| `\cite` calls | 51 | 73 | 94 |

Roughly **46 references** and each cited about one and a half times. A draft
with 25 will read as under-read; a draft with 120 in eight pages is usually
padding a section that should have been an argument.

## How recent

This is the number most drafts get wrong.

| | |
|---|---|
| Median reference year | 2019 |
| 10th / 90th percentile | 2013 / 2023 |
| Median age relative to the paper's own newest citation | **3 years** |
| 75th percentile of that age | 5 years |
| **Share within 3 years of the newest citation** | **59%** |
| Share more than 10 years older than the newest | 16% |

So the shape of a healthy bibliography here is:

- **~60% from the last three years.** This is a fast-moving literature and the
  reviewers are the people who wrote those papers. A related-work section whose
  newest citation is two years old reads as a project that stalled.
- **~25% from three to ten years back.** The methods everyone builds on.
- **~15% older.** The foundational work — and this fraction is small. Citing
  a 1998 paper is fine; citing fifteen of them instead of the current baselines
  is what draws "the authors appear unaware of recent work".

A concrete check before submitting: sort your `.bib` by year. If fewer than
about a quarter of entries are from the current or previous calendar year, the
novelty check in `references/audit/novelty.md` was probably too narrow.

## What to cite where

- **Introduction**: the two or three papers that define the problem, and the
  one closest method. Not a survey of the field.
- **Related Work**: grouped by approach. Each group ends with what it cannot
  do — the sentence your method is measured against.
- **Method**: whatever you build on directly, cited at the point of use.
- **Experiments**: every baseline, every dataset, every metric definition that
  is not universal.

## Verification

Existence and metadata are a tool's job; whether a citation supports the claim
it is attached to is not. Both layers are in
[`../audit/citation-audit.md`](../audit/citation-audit.md).
