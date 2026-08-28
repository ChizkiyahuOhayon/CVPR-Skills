# Novelty check

Run before building, not after. The purpose is to find the paper that already
did this while it is still cheap to change course.

## Search the claim, not the topic

Searching "3D occupancy prediction" returns a field. Search the *mechanism*:

- the insight, in the words someone else would have used;
- the mechanism, in two or three phrasings ("sparse queries", "deformable
  sampling", "adaptive scaling");
- the failure mode you are fixing, since papers are often titled after it;
- the closest method's name plus "limitation" or "analysis" — follow-ups
  cluster there.

Cover arXiv, OpenReview (including **rejected** submissions — a rejected paper
still scoops you and reviewers will know it), Semantic Scholar and Google
Scholar. Then read the *citing* papers of your nearest neighbour: that is where
the last eighteen months live.

## The three outcomes

**Scooped.** Same insight, same mechanism, published. Change the insight or
stop. Do not proceed hoping reviewers missed it — the AC will assign the author
of that paper as a reviewer.

**Adjacent.** Same insight, different mechanism, or the same mechanism in a
different setting. This is workable and is where most real papers sit. The
requirement is a direct comparison and a paragraph saying exactly what differs.
Vagueness here is what produces "the difference from [X] is unclear" reviews.

**Clear.** Nobody has stated the insight. Then ask why — a well-populated field
with an unstated obvious insight usually means it does not work, and finding
out why in week one is worth more than finding out in month six.

## Writing it down

For each of the three nearest papers:

```
[paper]  what they do  |  what we do differently  |  the experiment that shows it
```

If the third column is empty for any of them, that comparison is missing from
the evaluation plan and a reviewer will find the gap.

## Scale

The corpus cites 40–56 distinct works, median 46. If the novelty check surfaced
fewer than about twenty relevant papers, the search was too narrow, not the
field too empty.

## Tooling

Whatever literature search is available in the session — `paper_search`,
`scoop_check`, `ccf-literature-searcher`, a web search. The method above
matters more than the tool. Record the queries you ran alongside the results,
so the check can be repeated when a reviewer names a paper you missed.
