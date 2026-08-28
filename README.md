<h1 align="center">CVPR-Skills</h1>

<p align="center">
  <b>English</b>
  &nbsp;|&nbsp;
  <a href="README.zh-CN.md"><b>简体中文</b></a>
</p>

<p align="center">
  <b>From a research direction to a submitted paper, calibrated on 46 published CVPR-class papers.</b><br>
  Idea → novelty → code → experiments → figures → writing → review → submission.<br>
  Every number in it is a measurement, not a preference.
</p>

<p align="center">
  <a href="#the-pipeline">The pipeline</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#install">Install</a> ·
  <a href="#what-the-corpus-actually-says">Measurements</a> ·
  <a href="#the-figure-half">Figures</a> ·
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <a href="https://github.com/ChizkiyahuOhayon/CVPR-Skills/actions/workflows/test.yml"><img alt="tests" src="https://github.com/ChizkiyahuOhayon/CVPR-Skills/actions/workflows/test.yml/badge.svg"></a>
  <img alt="MIT licence" src="https://img.shields.io/badge/licence-MIT-blue.svg">
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="no dependencies" src="https://img.shields.io/badge/dependencies-none-brightgreen.svg">
  <img alt="Claude Code and Codex" src="https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex-8A2BE2.svg">
  <a href="https://github.com/ChizkiyahuOhayon/CVPR-Figure"><img alt="companion" src="https://img.shields.io/badge/figures-CVPR--Figure-8A2BE2.svg"></a>
</p>

---

## What this is

A skill suite that walks a paper from **"I have a direction"** to **"submitted"**,
and answers the questions that actually stall people:

> How many figures does a CVPR paper have, and where do they go?
> How long should the abstract be? How many references, and how recent?
> Where does the comparison table go, and where does the ablation go?
> What belongs in the appendix? How much statistics is enough?
> Is my related work thin?

Not with opinions. The LaTeX sources of **46 published papers** from three
groups — Tsinghua **MARS**, **Wenzhao Zheng**'s group, **Megvii** — were parsed:
289 figure environments, 300 tables, 6,726 dated references, ~200k words of
prose. Every threshold below is a percentile of that corpus, and
`scripts/audit_paper.py` measures your draft against it.

---

## The pipeline

```
 ┌───────┐   ┌─────────┐   ┌──────┐   ┌─────────────┐   ┌────────┐
 │ idea  │──▶│ novelty │──▶│ code │──▶│ experiments │──▶│ figures│
 └───────┘   └─────────┘   └──────┘   └─────────────┘   └────────┘
                                                             │
      ┌──────────┐   ┌────────┐   ┌───────────┐   ┌───────┐  │
      │ submit   │◀──│ review │◀──│ integrity │◀──│ write │◀─┘
      └──────────┘   └────────┘   └───────────┘   └───────┘
                          │
                          └──▶ rebuttal, if it comes back
```

| Stage | What you get | Reference |
|---|---|---|
| **idea** | one defensible idea with all five slots filled — problem, why it persists, insight, method, **falsification plan** — not a menu | [`craft/idea-shaping.md`](references/craft/idea-shaping.md) |
| **novelty** | scooped / adjacent / clear, with the nearest three papers and the experiment that distinguishes you from each | [`audit/novelty.md`](references/audit/novelty.md) |
| **code** | config-driven vs class-driven, module names that match the paper, every contribution behind a flag so the ablation is a sweep | [`craft/code.md`](references/craft/code.md) |
| **experiments** | two benchmarks, an ablation that lands on the baseline, a cost table — and an explicit ceiling on statistical machinery | [`corpus/experiment-design.md`](references/corpus/experiment-design.md) |
| **figures** | handed to [**CVPR-Figure**](https://github.com/ChizkiyahuOhayon/CVPR-Figure), which draws them from your code | — |
| **write** | structure, section-by-section word budgets, sentence and voice targets, caption lengths | [`corpus/writing-style.md`](references/corpus/writing-style.md) |
| **bibliography** | how many references, how recent, what to cite where | [`corpus/bibliography.md`](references/corpus/bibliography.md) |
| **integrity** | numbers against tables, claims against evidence, colours consistent across figures | [`audit/integrity.md`](references/audit/integrity.md) |
| **review** | a reviewer report on your own draft, with two scores that are never averaged | [`audit/reviewer-simulation.md`](references/audit/reviewer-simulation.md) |
| **submit** | page limit, anonymity, embedded fonts, vector figures | [`audit/submission.md`](references/audit/submission.md) |
| **rebuttal** | new numbers first, a revision ledger the AC can check | [`craft/rebuttal.md`](references/craft/rebuttal.md) |

**Order matters twice.** *Code before experiments*, because the ablation is a
code-structure decision — if each contribution is not behind a flag from day
one, the ablation table becomes four half-broken branches the week of the
deadline. *Figures before prose*, because a framework figure forces the method
to be factored before it is described.

---

## Quickstart

```bash
python3 scripts/audit_paper.py path/to/paper/       # a directory, main.tex, or a PDF
```

```
paper/main.tex  (article)
  4193 words | 169 sentences (median 22 words) | abstract 330 words
  2 figures | 6 tables | 0 equations | 19 references (13 \cite calls)
  first person 8.1/1k words | hedges 23.8/10k words
  sections: Introduction > Related Work > The wrong-world instrument > ... > Conclusion

WARN  abstract-length   abstract is 330 words; the corpus runs 149-187.
WARN  impersonal        first person appears 8.1 times per 1000 words; the corpus
                        runs 17.0-22.1. These papers say 'we propose'.
WARN  structure         no Method, Experiments section; the corpus standard is
                        Introduction > Related Work > Method > Experiments > Conclusion
WARN  thin-citations    19 distinct references; the corpus runs 40-56.
NOTE  few-figures       2 figures; corpus median is 6

0 error(s), 4 warning(s), 3 note(s)
```

Three levels, and they mean different things:

| | |
|---|---|
| `error` | **No paper in the corpus does this.** Fix it. |
| `warn` | Outside the corpus interquartile or p90 range. Fix it or have a reason. |
| `note` | Worth a look; often deliberate. |

It reads `.tex` sources (comments stripped, `\input` spliced, maths and floats
masked) and, when that is all you have, a **compiled PDF** — using font-size
tiers to find section headings, and telling you which checks it had to skip.

### It is calibrated, and you can check the calibration

Over all 45 corpus papers: **zero errors**, 4.7 warnings each.
Over a deliberately AI-written draft of the same length: **11 errors**.

That gap is the design constraint. An auditor that fires on published work is
measuring its author's taste, not the venue.

---

## What the corpus actually says

### Shape of a paper

| | p25 | median | p75 |
|---|---|---|---|
| Body prose (floats, maths, citations excluded) | 4,011 w | **4,351 w** | 4,869 w |
| Abstract | 149 w | **177 w**, 9 sentences | 187 w |
| Sections | — | **6** | — |
| Equations | — | **8** | 11 |
| `algorithm` environments | — | **0** | — |
| Figures / tables | — | **6 / 6** | — |
| Distinct references | 40 | **46** | 56 |

`Introduction > Related Work > Method > Experiments > Conclusion` in 16 of 46
papers, another 10 differing only by calling Method *Approach*. Eight pages is
mostly floats: the prose is about 4,400 words. And an algorithm box is the
exception, not the norm — the method goes in equations and one figure.

### Where the evidence sits

| | Figures | Tables |
|---|---|---|
| Experiments | 32% | **69%** |
| Introduction (the teaser) | 16% | — |
| Method | 15% | 9% |
| Related Work | 7% | — |
| Appendix | 2% | 2% |

Tables are almost purely an Experiments object. Figures spread out, because the
teaser and the method figure both carry argument. The teaser sits **6.9% into
the document**, is a single graphic in 41 of 46 papers, and carries a **49-word**
caption.

Within Experiments, the tables run: main comparison → **first ablation at about
60% through** → design study → cost.

What all 300 tables are for: **33% comparison, 22% ablation**, 13% benchmark
results, 8% breakdown. Over half of every table in this literature answers
*are we better than them* or *which part of us did it*.

### How much statistics — the ceiling, not the floor

| | Papers doing it |
|---|---|
| Any significance test (p-value, t-test, ANOVA) | **0 of 46** |
| Multiple seeds mentioned | **0 of 46** |
| Error bars, ±, std, confidence intervals | 5 of 46 (11%) |
| **An ablation** | **44 of 46 (96%)** |

**Do not build a statistical apparatus this venue does not use.** Bootstrap
confidence intervals on every cell and a Bonferroni correction will not be
rewarded; that effort buys another ablation row, which is what reviewers argue
about. The one exception: if a headline gain is under about a point, run two or
three seeds and say the spread **in one sentence** — not a table, not a test.

### The bibliography

| | |
|---|---|
| Distinct references | 40 / **46** / 56 (p25 / median / p75) |
| Median reference year | 2019 (p10 2013, p90 2023) |
| **Within 3 years of the newest thing cited** | **59%** |
| More than 10 years older than the newest | 16% |

The shape of a healthy bibliography here: **~60% from the last three years**,
~25% from three-to-ten years back, ~15% foundational. A related-work section
whose newest citation is two years stale reads as a project that stalled — and
the reviewers are the people who wrote those recent papers.

### The appendix

Only **15 of 46 papers have one**, so it is optional. Of those that do: more
qualitative results (73%), additional comparisons (73%), implementation detail
spilled from the main text (53%), dataset details (33%), failure cases (27%),
proofs (27%), further ablations (20%).

The pattern: an appendix holds **more of what is already in the paper**, not a
different kind of argument. A result that exists only in the appendix will not
be read. If a reviewer needs it to accept, it belongs in the main text — and
something else has to go.

### The prose

| | |
|---|---|
| Median sentence | **19 words** (p90 33) |
| First person (`we`/`our`/`us`) | **20 per 1,000 words** — 2% of all words |
| Hedges (`may`, `might`, `could`, `possibly`…) | **9.6 per 10,000 words** |
| Figure caption | **39 words** |
| Table caption | **19 words** |

Hedging is *rationed*, not banned: about four or five in a whole paper, spent
on real scope limits. These papers say **we**; a draft in the impersonal passive
is off-distribution in a way reviewers read as translated.

And figure captions are **twice as long as table captions**. A table's numbers
speak for themselves. A figure caption carries the claim, because a skimming
reader reads the teaser caption and nothing else on that page. Four-word
"Overview of our framework." is the most common self-inflicted wound in a draft.

---

## The figure half

Figures are a separate skill because they are a separate engine:
**[CVPR-Figure](https://github.com/ChizkiyahuOhayon/CVPR-Figure)**, built on the
same corpus. It draws framework, pipeline, teaser and module figures and exports
them as **natively editable Visio `.vsdx` and PowerPoint `.pptx`**, plus PDF for
LaTeX.

It can draw a first-draft architecture **straight from your model code** —
nothing imported, nothing executed, both readers parse with `ast`:

```bash
python3 ../CVPR-Figure/scripts/from_code.py models/ --model MyNet -o fig.yaml
python3 ../CVPR-Figure/scripts/from_code.py configs/model.py --mm -o fig.yaml
python3 ../CVPR-Figure/scripts/render.py fig.yaml -o build/fig -f svg,pdf,pptx
```

The relevant finding from the same scan: **1 of 290 figures in the corpus is
drawn in TikZ**, and it is a bar chart. Every architecture figure is external
artwork, and the embedded fonts say it was made in PowerPoint, Visio or
diagrams.net. So `.pptx` export is not a convenience — it is the format this
literature actually works in.

---

## Install

### As a Claude Code skill

```bash
./install.sh                       # -> ~/.claude/skills/cvpr-skills
```

Then just ask. The skill triggers on paper writing, revision, experiment
design, review, rebuttal and submission requests, in English or Chinese.

> The project is **CVPR-Skills**; the installed skill id is `cvpr-skills` in
> lowercase, because Claude Code skill ids are lowercase-kebab.

Install the figure half too:

```bash
git clone https://github.com/ChizkiyahuOhayon/CVPR-Figure.git && ./CVPR-Figure/install.sh
```

### With Codex, Cursor, Aider, or a plain API loop

```bash
cp -r . ~/.codex/skills/cvpr-skills
```

`AGENTS.md` is the entry point for agents that do not read `SKILL.md`
frontmatter.

### By hand, without an agent

```bash
python3 scripts/audit_paper.py paper/
python3 scripts/audit_paper.py paper/ --json | jq '.findings[] | select(.level=="error")'
```

### Requirements

Python 3.8+, standard library only. Two **optional** extras:

```bash
pip install academic-refchecker[llm]   # citation verification
pip install pymupdf                    # auditing a PDF when there is no .tex
```

---

## Rebuild it on your own corpus

The shipped numbers describe three groups working mostly in 3D vision. If your
subfield differs, rebuild against your own reading pile:

```bash
python3 scripts/build_profile.py /path/to/arxiv/sources -o my-profile.json
python3 scripts/audit_paper.py paper/ --profile my-profile.json
```

Each immediate subdirectory is one paper. The profile and the auditor are
produced by the **same reader** (`scripts/cvprskills/tex.py`), so a draft is
always compared like-for-like — a detail that caught a real error during
development, recorded in [CHANGELOG.md](CHANGELOG.md).

---

## One thing worth knowing about "AI-sounding" writing

A side finding, but a useful one. The "signs of AI writing" checklists that
circulate were built from web text. Measured against 45 published papers in
*this* venue, several of their headline items are simply how the field writes:

| Flagged by generic tools | Papers using it (of 45) |
|---|---|
| `leverage` | 29 |
| `utilize` | 35 |
| `robust` | 26 |
| `state-of-the-art` | 40 |
| rule of three, "A, B, and C" | 42 |
| trailing ", …ing" clause | **45 of 45** |

Removing those makes a draft read *less* like the venue. What is genuinely
absent: `pivotal` (**0 of 45**), "the landscape of" (0), `tapestry` (0), and the
em dash — **43 of 45 papers contain none**, which makes it the cheapest fix and
the most reliable signal.

Details in [`craft/humanizing.md`](references/craft/humanizing.md). This is not
about defeating AI detectors — their false-positive rate on non-native English
is high enough that optimising against them is futile and unfair. It is about
writing like the venue.

---

## Repository layout

```
SKILL.md / AGENTS.md      entry points for Claude Code / other agents
manifest.yaml             which fragment to load for which stage
install.sh

references/
  corpus/                 the measurements
    profile.json            the machine-readable distribution
    README.md               what was measured, how to read a percentile
    venue-conventions.md    structure, page budget, floats, captions
    writing-style.md        sentence, voice and word-frequency baselines
    experiment-design.md    benchmarks, ablations, the statistics ceiling,
                            where floats sit, what the appendix holds
    bibliography.md         how many references, how recent, what to cite where
    code-and-release.md     what ships with a paper, across 46 repositories
  craft/                  how to do the work
    idea-shaping.md         the five slots an idea needs
    code.md                 repo shape, naming, ablation-ready flags
    anti-defensive.md       hedging, with the number behind it
    humanizing.md           which AI tells are real in this literature
    rebuttal.md             structure, tone, the revision ledger
  audit/                  how to check it
    novelty.md              search the mechanism, not the topic
    citation-audit.md       RefChecker, plus what no tool checks
    integrity.md            numbers against numbers, claims against evidence
    reviewer-simulation.md  four questions, two scores never averaged
    submission.md           venue geometry and the checklist
  workflow/routing.md     one owner per deliverable

scripts/
  audit_paper.py          the auditor
  build_profile.py        rebuild profile.json from a corpus
  cvprskills/
    tex.py                LaTeX -> prose, structure, floats
    pdf.py                compiled PDF -> the same, minus what a PDF loses
    prose.py              draft vs profile

templates/
  paper-skeleton.tex      a skeleton with the corpus word budgets in comments
  experiment-plan.md      fill this in before running anything

tests/test_audit.py       regression checks, no dependencies
```

---

## Tests

```bash
python3 tests/test_audit.py
```

No dependencies, about a second. They cover the LaTeX reader (comment
stripping, `\input` splicing, nested environments, brace-balanced captions,
maths masking), the tell counters, the shipped profile's internal consistency,
the auditor on a stub / on AI-flavoured prose / on ordinary venue vocabulary —
including explicit checks that `leverage`, `utilize`, `robust` and
`state-of-the-art` are *not* treated as tells — the rate floor, the CLI's exit
codes and JSON, and that every path the docs and manifest declare exists.

CI runs them on Python 3.9, 3.11 and 3.13 with **nothing installed**.

---

## Where this came from

Distilled and, where the measurements disagreed, **corrected**:

| Source | Taken | Changed |
|---|---|---|
| **CCFA-skills** | single-owner routing, the stage split | narrowed from CCF-A-wide to CVPR-class; every threshold replaced with a measurement |
| **anti-defensive-writing** | the posture; necessary vs defensive limits | given a number: ~10 hedges per 10k words |
| **humanizer** | the structural tells — uniform paragraphs, symmetric lists, vague attribution | the word list was measured and largely overturned for this literature |
| **IdeaSpark** | one idea with a falsification plan, not a menu | contribution shapes read off this corpus |
| **RefChecker** | citation verification | integrated as an optional external CLI, not vendored |
| **nature-skills / ARS** | reference-on-demand structure | conventions here are CVPR's, which differ from Nature's |
| **CVPR-Figure** | — | kept separate; it owns figures and shares this corpus |

---

## FAQ

**Does it cover everything CCFA-skills does?**
The stages, yes — idea, novelty, experiments, writing, review, rebuttal,
submission, integrity, citations — plus code structure and figures, which CCFA
splits differently. What it deliberately does not carry over: the project
scaffolder, the literature *monitor* (a standing arXiv watch), the skill-forger,
and CCFA's image-model figure generator, which CVPR-Figure replaces with a
deterministic engine. If you want a standing arXiv watch, keep CCFA installed
alongside; they do not conflict.

**Is my paper bad if the auditor warns?**
No. Published papers average 4.7 warnings each. Warnings mean *outside the usual
range*, which is often correct. Errors are the ones that mean something.

**My field isn't 3D vision.**
Rebuild the profile. The structural findings — caption asymmetry, tables living
in Experiments, the ablation being mandatory, hedges being rationed, references
skewing recent — travel further than the word counts.

**Does it check whether my science is right?**
No, and it says so. It measures structure and prose. Whether the numbers support
the claims is [`audit/integrity.md`](references/audit/integrity.md), and that is
a human pass.

**Where did the numbers come from?**
[`references/corpus/README.md`](references/corpus/README.md).
`scripts/build_profile.py` is the script that produced them. The sources are
other people's papers and are not redistributed.

---

## Licence

MIT. See [LICENSE](LICENSE).
