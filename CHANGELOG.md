# Changelog

## 1.0.0

First release.

### The corpus

46 papers with complete arXiv LaTeX sources from Tsinghua MARS, Wenzhao Zheng's
group and Megvii — 289 figure environments, 300 tables, ~200k words of prose.
Summarised in `references/corpus/profile.json`, rebuildable with
`scripts/build_profile.py`.

### The auditor

`scripts/audit_paper.py` measures a LaTeX draft against that distribution:
structure, page budget, sentence length, first-person density, hedge rate,
caption lengths, float inventories, and the frequency of 46 patterns that AI
writing checklists flag.

Calibration, which is the design constraint rather than an afterthought: **zero
errors across all 45 corpus papers**, 4.7 warnings each; **11 errors** on a
deliberately AI-written draft of comparable length. Frequency findings are
suppressed below 900 words, where a single occurrence says more about length
than about prose.

### The finding worth the whole suite

Generic "signs of AI writing" lists, measured against real papers in this
venue, are substantially wrong for it. `leverage` (29 of 45 papers), `utilize`
(35), `robust` (26), `state-of-the-art` (40), the rule of three (42) and the
trailing ", …ing" clause (**45 of 45**) are all normal here — removing them
makes a draft read less like the venue. What is genuinely absent: `pivotal`
(0 of 45), "the landscape of" (0), `tapestry` (0), and the em dash (2 of 45).

### Also in this release

- `scripts/cvprskills/tex.py` — a LaTeX reader that strips comments, splices
  `\input`, brace-matches float environments, and masks maths and citations
  before counting prose. Used by both the profile builder and the auditor, so
  the two always measure the same quantity.
- Distinct-reference counting alongside `\cite` call counting; the corpus
  medians are 46 and 73 respectively, and the first is what people mean.
- Reference material for nine stages: idea shaping, novelty, experiment design,
  writing, hedging, humanizing, citation audit, integrity, reviewer simulation,
  rebuttal and submission.
- `references/corpus/code-and-release.md` — what actually ships with a paper,
  measured across the 46 accompanying repositories. 46 of 46 have a README;
  only 33 have a licence.
- Integration with [RefChecker](https://github.com/markrussinovich/refchecker)
  as an optional external CLI, with instructions to report a bibliography as
  *unaudited* rather than skip the step silently when it is absent.

### Corrected during development

- An earlier scan reported "0 of 292 figures use TikZ". The shipped reader
  finds 290 figure environments and **1** `tikzpicture` — an ablation bar chart
  in PETR. The substance holds; the number is now the accurate one. This is why
  the profile builder and the auditor share a reader.
