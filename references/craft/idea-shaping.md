# Shaping an idea

Distilled from `idea-spark` and `ccf-idea-optimizer`, narrowed to what this
corpus rewards. The goal is **one** defensible idea with a falsification plan,
not a list of directions.

## The shape an idea has to have

Five slots. An idea missing any of them is not yet an idea.

1. **Problem** — a failure that exists in the world, statable without naming
   your method. "Occupancy predictors degrade beyond 30 m" is a problem;
   "existing methods lack global context" is a slogan.
2. **Why it persists** — the reason prior work has not fixed it. If there is no
   answer, either it is fixed already or it is not a problem.
3. **Insight** — the one thing you know that they did not. Usually a property
   of the data, the task, or the failure mode. This is the paper.
4. **Method** — the smallest construction that exploits the insight. If the
   method has three novel components, you have three papers or one confused
   one.
5. **Falsification** — the experiment whose result would tell you the insight
   is wrong. Design this *before* running anything.

## How this corpus makes contributions

Read across the 46 papers, the shapes recur:

- **A representation swap.** Dense voxels → sparse Gaussians, BEV grid →
  queries. The claim is efficiency at equal accuracy, or accuracy at equal
  cost, and it lives or dies on the cost table.
- **A missing signal added.** Explicit depth supervision, temporal stereo,
  trajectory conditioning. The ablation removing the signal is the paper.
- **A constraint relaxed.** Works without HD maps; without LiDAR at test time;
  without per-scene optimisation. The comparison must be at matched
  information, and reviewers check this first.
- **A unification.** Two tasks that shared a backbone now share a head. The
  burden is showing the joint model beats both specialists, not just one.
- **A benchmark or protocol.** Rare, high-value, and judged on whether anyone
  else can use it. Ships with data, code and a leaderboard or it does not count.

If your idea does not fit one of these, that is interesting — but be able to
say what shape it *is*, because a reviewer will be looking for one.

## The falsification plan

Write these three lines before you write code:

```
If <insight> is right, then <specific measurable thing> on <benchmark>.
If it is wrong, I will see <specific other outcome>.
The experiment that distinguishes them is <experiment>, which takes <time>.
```

If the second line is "the numbers will be lower", the plan is not sharp
enough. A good falsification names a *pattern*: which subset improves, which
does not, and why the insight predicts that split.

## Killing an idea early

Cheaper than killing it in review. Reasons to stop:

- The insight is already in a paper you had not read. Check before building —
  see `references/audit/novelty.md`.
- The gain only exists at a setting nobody uses.
- The method needs information the baselines do not have, and there is no fair
  way to give it to them.
- You cannot state the falsification. This usually means the idea is a method
  looking for a problem.

Sunk effort is not evidence. The corpus groups publish a fraction of what they
start.

## Output

One page:

```
Problem        one sentence, no method words
Why it persists one sentence
Insight        one sentence
Method         a paragraph and a figure sketch
Falsification  the three lines above
Evidence plan  primary benchmark, second benchmark, ablation, cost table
Nearest work   three papers and the specific difference from each
Risk           what most likely goes wrong, and what you would do then
```
