<h1 align="center">CVPR-skills</h1>

<p align="center">
  <b>English</b>
  &nbsp;|&nbsp;
  <a href="README.zh-CN.md"><b>简体中文</b></a>
</p>

<p align="center">
  <b>Paper-production skills for CVPR-class venues, calibrated on measurements
  from 46 published papers.</b><br>
  Advice with a percentile behind it, and a working auditor that measures your
  draft against the distribution.
</p>

<p align="center">
  <a href="#the-one-command-that-matters">Quickstart</a> ·
  <a href="#install">Install</a> ·
  <a href="#what-the-corpus-says">Measurements</a> ·
  <a href="#the-correction-to-generic-humanizers">AI tells</a> ·
  <a href="#the-stages">Stages</a> ·
  <a href="#faq">FAQ</a>
</p>

<p align="center">
  <img alt="MIT licence" src="https://img.shields.io/badge/licence-MIT-blue.svg">
  <img alt="Python 3.8+" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="no dependencies" src="https://img.shields.io/badge/dependencies-none-brightgreen.svg">
  <img alt="Claude Code and Codex" src="https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex-8A2BE2.svg">
</p>

---

## Why this exists

Most writing advice for papers is taste asserted as rule. "Don't hedge." "Vary
your sentences." "Avoid AI words." None of it says *how much*, so none of it can
be checked, and some of it is wrong for this literature specifically.

This suite replaces the assertions with measurements. The LaTeX sources of **46
papers** from three groups — Tsinghua **MARS**, **Wenzhao Zheng**'s group and
**Megvii** — were parsed: 289 figure environments, 300 tables, about 200,000
words of prose. Every threshold in the suite is a percentile of that corpus.

Then the measurements were turned into a tool.

## The one command that matters

```bash
python3 scripts/audit_paper.py path/to/paper/     # or main.tex
```

```
paper/main.tex  (article)
  4211 words | 208 sentences (median 19 words) | abstract 141 words
  4 figures | 8 tables | 4 equations | 51 references (62 \cite calls)
  first person 21.8/1k words | hedges 9.5/10k words
  sections: Introduction > Related Work > BEVDepth > Experiments > Conclusion

WARN   abstract-length      abstract is 141 words; the corpus runs 149-187.
WARN   rare-phrase          delve x1 (2.4 per 10k). Only 5 of 45 corpus papers use it at all.
WARN   structure            no Method section; the corpus standard is Introduction > Related Work > Method > Experiments > Conclusion

0 error(s), 3 warning(s), 0 note(s)
```

Three levels, and they mean different things:

| | |
|---|---|
| `error` | **No paper in the corpus does this.** Fix it. |
| `warn` | Outside the corpus interquartile or 90th-percentile range. Fix it or have a reason. |
| `note` | Worth a look; often a deliberate choice. |

### How it was calibrated

Run over all 45 corpus papers, the auditor reports **zero errors** and 4.7
warnings per paper. Run over a deliberately AI-written draft of comparable
length, it reports **11 errors and 29 warnings**.

That gap is the whole design. An auditor that fires on published work is
measuring its author's taste, not the venue.

It also refuses to compute frequency findings below 900 words, because one
occurrence in a short draft tells you about the draft's length, not its prose.

---

## What the corpus says

| | p25 | median | p75 |
|---|---|---|---|
| Body prose (floats, maths, citations excluded) | 4,011 w | **4,351 w** | 4,869 w |
| Abstract | 149 w | **177 w**, 9 sentences | 187 w |
| Median sentence length | 18 w | **19 w** | 21 w |
| First person per 1,000 words | 17.5 | **20.1** | 23.4 |
| Hedges per 10,000 words | — | **9.6** | 19.4 |
| Distinct references | 40 | **46** | 56 |
| Equations | — | **8** | 11 |
| Figures / tables | — | **6 / 6** | — |
| Figure caption | 7 w (p10) | **39 w** | 84 w (p90) |
| Table caption | — | **19 w** | 45 w (p90) |

A few of these are worth stating outright.

**Hedging is rationed, not banned.** About one hedge per thousand words — four
or five in a whole paper. One paper of 45 has none, so zero is the outlier too.
Spend them on real scope limits.

**These papers say "we".** Two percent of all words are first person. A draft in
the impersonal passive is off-distribution in a way reviewers read as
translated or generated.

**Figure captions are twice as long as table captions**, and that asymmetry is
the point. A table's numbers speak for themselves. A figure caption has to
carry the claim, because a skimming reader reads the teaser caption and nothing
else on that page. The four-word "Overview of our framework." is the most
common self-inflicted wound in a draft.

**43 of 46 papers run an ablation.** Comparison tables are 33% of all tables and
ablations another 22%: over half of every table in this literature is answering
*are we better than them* or *which part of us did it*.

**Almost nobody draws figures in TikZ** — 1 of 290, and it is a bar chart. Every
architecture figure is external artwork. That is the other half of this
project: see [CVPR-Figure](https://github.com/ChizkiyahuOhayon/CVPR-Figure).

---

## The correction to generic humanizers

This is the part that changes what you actually do.

The "signs of AI writing" lists that circulate were built from encyclopaedia and
web text. Run them against 45 published CVPR-class papers and they split in two.

### Words a humanizer flags that are **normal here** — leave them alone

| | Papers using it (of 45) | Median per 10k |
|---|---|---|
| "we propose" | **44** | 10.5 |
| `state-of-the-art` / SOTA | 40 | 6.4 |
| `utilize` | 35 | 5.7 |
| `significantly` | 35 | 2.6 |
| `enable(s)` | 33 | 2.4 |
| `moreover` | 31 | 2.5 |
| `comprehensive` | 31 | 2.4 |
| `leverage` | 29 | 2.3 |
| `robust` | 26 | 2.4 |
| `novel` | 24 | 1.9 |
| rule of three — "A, B, and C" | **42** | 9.8 |
| trailing ", …ing" clause | **45 of 45** | 36.6 |

Hunting the rule of three and the "-ing" clause out of a methods section — two
of the loudest items on every generic checklist — moves the draft *away* from
how this venue writes. Every single paper in the corpus uses both.

### Patterns that are **actually absent** — these are the real tells

| | Papers using it (of 45) |
|---|---|
| `pivotal` | **0** |
| `tapestry` | **0** |
| "the landscape of" | **0** |
| **em dash (—)** | **2** |
| `nuanced`, `realm`, `cutting-edge`, `meticulous` | 1 |
| `innovative`, `seamless` | 2–3 |
| `importantly`, `intricate`, `remarkably`, `substantially` | 3–4 |
| "in conclusion", "it is worth noting" | 4 |
| `delve`, `showcase`, `holistic`, `vital`, "for the first time" | 5 |

**Start with the em dash.** Forty-three of 45 papers contain none. Cheapest fix
available, most reliable signal in the set.

And note what the auditor actually flags: not the presence of a word, but a
*rate* far past the corpus 90th percentile. `comprehensive` three times in a
300-word abstract is generated prose. `comprehensive` once in a 4,400-word
paper is a person.

> This is not an attempt to defeat AI-text detectors. Those tools have a
> false-positive rate on non-native English writing high enough that optimising
> against them is both futile and unfair to the people they misclassify. The
> goal is prose that reads like the venue — which is a writing goal, and
> happens to be the same work.

---

## Install

### As a Claude Code skill

```bash
./install.sh                       # -> ~/.claude/skills/cvpr-skills
```

Then just ask. The skill triggers on paper writing, revision, review, rebuttal
and submission requests, in English or Chinese.

> The project is **CVPR-skills**; the installed skill id is `cvpr-skills` in
> lowercase, because Claude Code skill ids are lowercase-kebab.

### With Codex, Cursor, Aider, or a plain API loop

```bash
cp -r . ~/.codex/skills/cvpr-skills
```

`AGENTS.md` is the entry point for agents that do not read `SKILL.md`
frontmatter. Same content, no Claude-specific metadata.

### By hand, without an agent

The auditor is a normal CLI:

```bash
python3 scripts/audit_paper.py paper/
python3 scripts/audit_paper.py paper/ --json | jq '.findings[] | select(.level=="error")'
```

### Requirements

Python 3.8+, standard library only. One **optional** external tool:

```bash
pip install academic-refchecker[llm]     # citation verification
```

---

## The stages

One owner per deliverable. "Make this better" and "what is wrong with this" are
different requests, and the second one does not rewrite.

| Stage | Load | Owns |
|---|---|---|
| **idea** | `references/craft/idea-shaping.md` | one defensible idea with a falsification plan |
| **novelty** | `references/audit/novelty.md` | scooped / adjacent / clear, with the nearest three |
| **experiments** | `references/corpus/experiment-design.md` | benchmarks, ablation, cost table |
| **figure** | *the CVPR-Figure skill* | framework, pipeline, teaser, module |
| **write** | `references/corpus/writing-style.md`, `references/craft/anti-defensive.md` | prose |
| **audit** | `scripts/audit_paper.py`, `references/audit/integrity.md` | measurement and self-consistency |
| **citations** | `references/audit/citation-audit.md` | RefChecker plus the layer no tool checks |
| **review** | `references/audit/reviewer-simulation.md` | assessment, never a rewrite |
| **rebuttal** | `references/craft/rebuttal.md` | response letter and revision ledger |
| **submit** | `references/audit/submission.md` | format, anonymity, fonts, page limit |

Default order:

```
idea -> novelty -> experiments -> (run the work) -> figure -> write
     -> integrity -> citations -> review -> submit
```

**Figures before prose.** A framework figure forces the method to be factored
before it is described, and writing the method section against a finished
figure is much faster than the reverse.

---

## Rebuilding the profile on your own corpus

The shipped numbers describe three groups working mostly in 3D vision. If your
subfield differs, rebuild against your own reading pile:

```bash
python3 scripts/build_profile.py /path/to/arxiv/sources -o my-profile.json
python3 scripts/audit_paper.py paper/ --profile my-profile.json
```

Each immediate subdirectory of the source directory is treated as one paper.
The profile and the auditor are produced by the **same reader**
(`scripts/cvprskills/tex.py`), so a draft is always compared against a
like-for-like measurement — a detail that matters more than it sounds, and one
that caught a real bug during development.

---

## Repository layout

```
SKILL.md                  Claude Code entry point (frontmatter routing)
AGENTS.md                 Codex / other-agent entry point
manifest.yaml             which fragment to load for which stage
install.sh                one-command install as a Claude Code skill

references/
  corpus/
    profile.json          the machine-readable distribution
    README.md             what was measured, and how to read a percentile
    venue-conventions.md  structure, page budget, floats, captions
    writing-style.md      sentence, voice and word-frequency baselines
    experiment-design.md  benchmarks, ablations, what tables are for
    code-and-release.md   what ships alongside a paper, measured on 46 repos
  craft/
    anti-defensive.md     hedging, with the number behind it
    humanizing.md         which AI tells are real in this literature
    idea-shaping.md       the five slots an idea needs
    rebuttal.md           structure, tone, the revision ledger
  audit/
    novelty.md            search the mechanism, not the topic
    citation-audit.md     RefChecker, plus what no tool checks
    integrity.md          numbers against numbers, claims against evidence
    reviewer-simulation.md  the four questions, two separate scores
    submission.md         venue geometry and the checklist
  workflow/
    routing.md            one owner per deliverable

scripts/
  audit_paper.py          the auditor
  build_profile.py        rebuild profile.json from a corpus
  cvprskills/
    tex.py                LaTeX -> prose, structure, floats
    prose.py              draft vs profile

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
the auditor's behaviour on a stub, on AI-flavoured prose, and on ordinary venue
vocabulary — including explicit checks that `leverage`, `utilize`, `robust` and
`state-of-the-art` are *not* treated as tells — the rate floor, the CLI's exit
codes and JSON, and that every path the docs and manifest declare exists.

---

## Relationship to other skills

This suite distils and corrects material from several places rather than
wrapping them:

| Source | What was taken | What was changed |
|---|---|---|
| **CCFA-skills** | the single-owner routing architecture and stage split | narrowed from CCF-A-wide to CVPR-class; every threshold replaced with a measurement |
| **anti-defensive-writing** | the posture, and the distinction between necessary and defensive limits | given a number: ~10 hedges per 10k words |
| **humanizer** | the structural tells — uniform paragraphs, symmetric lists, vague attribution | the word list was **measured and largely overturned** for this literature |
| **IdeaSpark** | one idea, with a falsification plan, not a menu | the contribution shapes were read off this corpus |
| **RefChecker** | citation verification | integrated as an optional external CLI, not vendored |
| **nature-skills / ARS** | the reference-on-demand structure | conventions here are CVPR's, which differ from Nature's |
| **CVPR-Figure** | — | kept as a separate skill; it owns figures and shares this corpus |

---

## FAQ

**Is my paper bad if the auditor warns?**
No. Published papers average 4.7 warnings each. Warnings mean *outside the usual
range*, and outside the usual range is often correct. Errors are the ones that
mean something: no paper in the corpus does that thing.

**My field isn't 3D vision.**
Then rebuild the profile. The structural findings — caption asymmetry, external
artwork, the ablation being mandatory, hedges being rationed — travel further
than the word counts do.

**Why not just use a general writing assistant?**
Because it will tell you to delete `leverage` and rewrite your rule-of-three
lists, and it has no idea that 45 out of 45 papers in your venue use the
construction it is flagging.

**Does it check whether my science is right?**
No, and it says so. It measures structure and prose. Whether the numbers support
the claims is `references/audit/integrity.md`, and that is a human pass.

**Where did the numbers come from?**
`references/corpus/README.md`, and `scripts/build_profile.py` is the script that
produced them. The sources are other people's papers and are not redistributed.

---

## Licence

MIT. See [LICENSE](LICENSE).
