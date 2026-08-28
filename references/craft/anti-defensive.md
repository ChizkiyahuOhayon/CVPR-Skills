# Defensive writing

Distilled from the `anti-defensive-writing` skill, then calibrated against the
corpus so the advice has a number behind it.

## The measurement

Hedges per 10,000 words across 45 published CVPR-class papers:

| | |
|---|---|
| Median | **9.6** — roughly one per thousand words |
| 75th percentile | 19.4 |
| 90th percentile | 24.0 |
| Papers with zero | 1 of 45 |

A 4,400-word paper therefore has room for about **four or five hedges**. Not
zero — the one paper with none is the outlier, not the model — but few enough
that each one has to be earned.

## The rule

Advance the claim. Say what is true, what the evidence shows, what the method
does. Do not spend sentences on what the paper does not claim, does not prove,
does not cover, or does not attempt.

Write as an author explaining a result, not as an author negotiating with an
imagined reviewer.

## Hedges worth keeping

Keep a limitation when it changes how the reader should act on the paper:

- **Scope.** "We evaluate on driving scenes; indoor performance is untested."
  A reader deciding whether to use the method needs this.
- **Assumption.** "The derivation assumes calibrated intrinsics." The maths
  fails without it.
- **Causality.** "The gain correlates with query density; we do not isolate
  which factor drives it." Honest about what the ablation shows.
- **Ethics, safety, licensing, human subjects.** Never trimmed.

Each of these attaches to a specific claim and could be checked. That is the
test.

## Hedges to cut, and what to do instead

| Pattern | What it is really doing | Do this instead |
|---|---|---|
| "may potentially improve" | guarding a claim you can measure | measure it and state the number |
| "we believe this is because" | speculation dressed as analysis | run the ablation, or write "one explanation is X; we did not test it" |
| "to some extent" | softening a real result | delete |
| "arguably the first" | claiming a first while pre-conceding it | drop the claim or make it precisely ("the first to do X under Y") |
| "results appear to show" | distancing from your own experiment | "results show" |
| "somewhat outperforms" | you won by a little | give the margin |
| "It is worth noting that X" | X is a normal sentence | write X |
| "While not exhaustive, our evaluation…" | apologising pre-emptively | state what you evaluated |
| "Due to space constraints, we omit…" | filler | omit it silently, or put it in the appendix and say where |

Note the double hedge, which is the most common form: *may potentially*,
*could possibly*, *might somewhat*. One of the two is always redundant and
usually both are.

## The related-work trap

The most defensive paragraph in most drafts is the one distinguishing the paper
from the closest prior work. Symptoms: three sentences of what the paper is not,
before one sentence of what it is.

Invert it. State the difference as a positive property of your method, once, in
a sentence a reader could verify from your tables. "Unlike X, we do not require
Y" is fine as *one* clause. It is not a paragraph.

## The limitations section

If the venue asks for one — NeurIPS and ICLR checklists do — write it as
engineering, not as apology. Three or four specific, checkable statements beat
a paragraph of general humility, and reviewers reward the former. A limitations
section that could have been written without reading the paper is worth
negative points.

## Checking

```bash
python3 scripts/audit_paper.py paper/ | grep defensive
```

The `defensive` finding fires when hedge density exceeds 1.3× the corpus 90th
percentile. It is deliberately loose: it catches drafts that hedge as a habit,
not papers that hedge four times on purpose.
