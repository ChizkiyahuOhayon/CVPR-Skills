# Routing

One owner per deliverable. A stage's handoff list says what may come next; it
is not permission to run several stages at once.

## Pick by what the user is asking to receive

| The user wants | Stage | Load |
|---|---|---|
| a research direction turned into one defensible idea | **idea** | `references/craft/idea-shaping.md` |
| to know whether the idea is already taken | **novelty** | `references/audit/novelty.md` |
| how to structure the implementation | **code** | `references/craft/code.md` |
| an experiment plan, benchmark and ablation design | **experiments** | `references/corpus/experiment-design.md` |
| a figure — framework, pipeline, teaser, module | **figure** | the CVPR-Figure skill, not this one |
| a plot — bars, curves, heatmaps, scatter | **plot** | matplotlib; `nature-figure` if installed |
| prose drafted, restructured, polished, compressed | **write** | `references/corpus/writing-style.md`, `references/craft/anti-defensive.md` |
| an assessment, score or reviewer report, without rewriting | **review** | `references/audit/reviewer-simulation.md` |
| how many references, how recent, what to cite where | **bibliography** | `references/corpus/bibliography.md` |
| citations verified against reality | **citations** | `references/audit/citation-audit.md` |
| numbers and claims checked against each other | **integrity** | `references/audit/integrity.md` |
| venue format, anonymity, page limit, checklist | **submission** | `references/audit/submission.md` |
| a rebuttal or response letter | **rebuttal** | `references/craft/rebuttal.md` |

## The three collisions that actually happen

**Write vs review.** If the request is "make this better", the owner is
*write*. If it is "what is wrong with this", "score this", "review this", the
owner is *review*, and it does not rewrite. When someone asks for a review and
you hand back a rewrite, you have removed their chance to disagree with the
diagnosis.

**Figure vs plot.** Boxes, arrows and architecture are the figure stage and
belong to CVPR-Figure. Anything with an axis is a plot and belongs in
matplotlib. The two look adjacent and are not: one is a deterministic layout
engine over a declarative spec, the other is a data-rendering library.

**Humanizing vs writing.** Humanizing is a pass over prose that already exists.
It never owns a deliverable, it never runs on an experiment plan or a review,
and — see `references/craft/humanizing.md` — it must be applied with the corpus
frequencies, not with a generic word list.

## Default order for a paper

```
idea -> novelty -> code -> experiments -> (run the work) -> figure -> write
     -> integrity -> citations -> review -> submission
```

Three things about this order. **Code before experiments**, because the
ablation is a code-structure decision: if each contribution is not behind a
flag from the start, the ablation table becomes four half-broken branches a
week before the deadline. **Figures before prose**, because a framework
figure forces the method to be factored before it is described, and because
writing the method section against a finished figure is much faster than the
reverse. And **review before submission**, because a format check on a draft
that is about to be restructured is wasted.

## When to stop and ask

Ask when two readings of the request produce materially different work. Do not
ask to confirm a default. Concretely: ask about venue and page limit if the
draft does not say; ask which result is the headline if there are several; do
not ask whether to use booktabs.
