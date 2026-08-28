# CVPR-skills — agent entry point

Portable instructions for agents that do not read `SKILL.md` frontmatter
(Codex, Cursor, Aider, plain API loops). Behaviour is identical; `SKILL.md` is
the same document with Claude Code routing metadata.

## What this is

Research support for CVPR-class papers, calibrated on the LaTeX sources of 46
published papers from Tsinghua MARS, Wenzhao Zheng's group and Megvii. The
distribution is in `references/corpus/profile.json`; `scripts/audit_paper.py`
measures a draft against it.

Pure Python standard library. No install step. Python 3.8+.

## Use it when

The user is writing, revising, reviewing, rebutting or submitting a paper to a
top-tier vision or ML venue, or shaping the idea and experiments behind one.
Also: 顶会论文写作、论文润色、实验设计、审稿意见、rebuttal、投稿检查.

Do **not** use it for figures (that is the `cvpr-figure` skill) or for data
plots (matplotlib).

## The loop

```bash
# 1. measure the draft before forming any opinion about it
python3 scripts/audit_paper.py path/to/paper/

#    error = no corpus paper does this      -> fix
#    warn  = outside the corpus p25-p75/p90 -> fix or justify
#    note  = worth a look

# 2. verify the bibliography
pip install academic-refchecker[llm]
academic-refchecker --paper paper.pdf --report-file refs.json --report-format json

# 3. re-measure
python3 scripts/audit_paper.py path/to/paper/ --quiet
```

## Which reference to read

| Task | File |
|---|---|
| routing between stages | `references/workflow/routing.md` |
| paper structure, page budget, captions | `references/corpus/venue-conventions.md` |
| sentence, voice and word-frequency targets | `references/corpus/writing-style.md` |
| benchmarks, ablations, what tables are for | `references/corpus/experiment-design.md` |
| what ships with the code | `references/corpus/code-and-release.md` |
| cutting hedges without losing real scope | `references/craft/anti-defensive.md` |
| which "AI tells" are real *here* | `references/craft/humanizing.md` |
| turning a direction into one idea | `references/craft/idea-shaping.md` |
| writing a rebuttal | `references/craft/rebuttal.md` |
| has this been done | `references/audit/novelty.md` |
| citations | `references/audit/citation-audit.md` |
| numbers and claims against each other | `references/audit/integrity.md` |
| reviewer report | `references/audit/reviewer-simulation.md` |
| format and compliance | `references/audit/submission.md` |

## The measurements worth memorising

| | |
|---|---|
| Body prose | ~4,400 words (p25 4,011, p75 4,869) |
| Abstract | 177 words, 9 sentences |
| Median sentence | 19 words |
| First person | 20 per 1,000 words |
| Hedges | ~10 per 10,000 words — four or five in a paper |
| Distinct references | 46 (p25 40, p75 56) |
| Figures / tables | 6 each |
| Figure caption | 39 words; table caption 19 |
| Papers with an ablation | 43 of 46 |
| Figures drawn in TikZ | 1 of 290, and it is a bar chart |
| Em dashes | 2 of 45 papers |
| Trailing ", …ing" clause | 45 of 45 papers — leave it alone |

## Standing rules

1. Never invent a result, a number, a citation or a figure crop.
2. Quote the measurement when giving style advice. "Your abstract is 240 words;
   the corpus runs 149–187" is actionable. "Your abstract is too long" is not.
3. Assessment and rewriting are different jobs. Do not hand back a rewrite when
   someone asked what was wrong.
4. Do not apply a generic AI-word blacklist. `leverage`, `utilize`, `robust`,
   `state-of-the-art` and the rule of three are normal in this literature;
   `pivotal`, "the landscape of" and the em dash are not.
5. The corpus is three groups in mostly-3D vision. Say so when the paper at
   hand is outside that.
