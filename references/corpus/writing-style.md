# Writing style, measured

Load this when drafting or revising prose, and whenever a general-purpose
"humanizer" or "AI-detector" wants to change a word.

## The shape of a sentence

| | p25 | median | p75 |
|---|---|---|---|
| Median sentence length in a paper | 18 w | 19 w | 21 w |
| 90th-percentile sentence in a paper | — | 33 w | — |
| First person (`we`/`our`/`us`) per 1,000 words | 17.5 | 20.1 | 23.4 |

Nineteen words. Not fifteen, not thirty. And **2% of all words are first
person** — these papers say *we propose*, *we observe*, *our method*. A draft
written in the impersonal passive ("it is proposed that") is off-distribution
in a way reviewers read as translated or generated.

## Hedging: the number that matters most

Hedges (`may`, `might`, `could`, `possibly`, `potentially`, `arguably`,
`somewhat`, `to some extent`, `we believe`, `it seems`, `appears to`):

| | |
|---|---|
| Median | **9.6 per 10,000 words** — about one per thousand |
| 90th percentile | 24 per 10,000 |
| Papers with none at all | 1 of 45 |

So: hedging is not forbidden, it is *rationed*. A 4,400-word paper has room for
roughly four or five hedges. Spend them on real scope limits — the setting the
method was not tested in, the assumption the derivation needs — and nowhere
else.

Everything a defensive draft hedges instead: an unsupported claim (fix the
claim, not the sentence), a result the reviewer might dislike (state it and
say what it means), or a comparison you did not run (run it, or say you did
not).

## Word frequencies, and why blanket bans are wrong

The lists of "AI words" that circulate were built from general web text. Run
against 45 published CVPR-class papers, they split into three groups.

### Absent — treat as a real tell

Never used, or used by at most a handful of papers and never more than once:

| Word / pattern | Papers using it (of 45) |
|---|---|
| `pivotal` | **0** |
| `tapestry` | **0** |
| "the landscape of" | **0** |
| em dash (—) | **2** |
| `nuanced`, `realm`, `cutting-edge`, `meticulous` | 1 each |
| `innovative`, `seamless` | 2–3 |
| `importantly`, `intricate`, `remarkably`, `substantially` | 3–4 |
| "in conclusion", "it is worth noting" | 4 each |
| `delve`, `showcase`, `holistic`, `vital`, "for the first time" | 5 each |

The em dash deserves its own line: **43 of 45 papers contain none**. It is the
single cheapest signal to remove and the single most reliable one to notice.

### Normal — do not remove these

Words a general humanizer will flag that are ordinary in this literature:

| Word / pattern | Papers using it | Median per 10k |
|---|---|---|
| "we propose" | 44 of 45 | 10.5 |
| `state-of-the-art` / SOTA | 40 of 45 | 6.4 |
| `utilize` | 35 of 45 | 5.7 |
| `enable(s)` | 33 of 45 | 2.4 |
| `moreover` | 31 of 45 | 2.5 |
| `leverage` | 29 of 45 | 2.3 |
| `furthermore` | 28 of 45 | 2.1 |
| `comprehensive` | 31 of 45 | 2.4 |
| `robust` | 26 of 45 | 2.4 |
| `novel` | 24 of 45 | 1.9 |
| `significantly` | 35 of 45 | 2.6 |
| rule of three ("A, B, and C") | 42 of 45 | 9.8 |
| trailing ", …ing" clause | **45 of 45** | 36.6 |

Rewriting `utilize` to `use` is fine. Rewriting it because a checklist says
"AI word" is not, and hunting the rule of three out of a draft actively moves
it away from how this venue writes. Every paper in the corpus uses the
"by X-ing, we Y" construction; it is how methods sections are written here.

### Overused — the real failure mode

The tell is almost never a word. It is a *rate*. `comprehensive` three times in
a 300-word abstract is generated prose; `comprehensive` once in a 4,400-word
paper is a person. `scripts/audit_paper.py` flags a word only when the draft
sits well past the corpus 90th percentile, and it refuses to compute rates at
all below 900 words, because a single occurrence in a short draft says nothing.

## Applying this

```bash
python3 scripts/audit_paper.py path/to/paper/
```

Errors mean *no paper in the corpus does this*. Warnings mean *outside the
usual range, so have a reason*. The tool reports zero errors on all 45 corpus
papers and 11 on a deliberately AI-written draft of comparable length, so the
gap between those two states is what it is measuring.
