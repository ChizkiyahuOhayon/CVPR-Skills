# AI tells, and which ones are real here

Distilled from the `humanizer` skill (Wikipedia's "Signs of AI writing"), then
corrected against the corpus. The correction is the point of this file:
**a general-purpose humanizer, applied unmodified to a CVPR paper, makes it
worse.**

## Why the general lists mislead

They were built from encyclopaedia and web text. Machine-learning papers have
their own register, and several words on every "AI vocabulary" list are simply
how this literature talks. Measured across 45 published papers:

| Flagged by generic humanizers | Papers using it (of 45) | Verdict |
|---|---|---|
| "we propose" | 44 | **normal** — near-universal |
| `state-of-the-art` / SOTA | 40 | **normal** |
| `utilize` | 35 | **normal** |
| `significantly` | 35 | **normal** |
| `enable(s)` | 33 | **normal** |
| `moreover` | 31 | **normal** |
| `comprehensive` | 31 | **normal** |
| `leverage` | 29 | **normal** |
| `furthermore` | 28 | **normal** |
| `robust` | 26 | **normal** |
| `novel` | 24 | **normal** |
| rule of three ("A, B, and C") | 42 | **normal**, median 9.8 per 10k |
| trailing ", …ing" clause | **45 of 45** | **normal**, median 36.6 per 10k |

Stripping the rule of three and the "-ing" clause out of a methods section —
two of the loudest items on the generic checklists — moves the draft *away*
from how the venue writes. Every paper in the corpus uses both.

## The tells that are real

Absent or near-absent from published work:

| Pattern | Papers using it (of 45) |
|---|---|
| `pivotal` | 0 |
| `tapestry` | 0 |
| "the landscape of" | 0 |
| **em dash (—)** | **2** |
| `nuanced`, `realm`, `cutting-edge`, `meticulous` | 1 |
| `innovative`, `seamless` | 2–3 |
| `importantly`, `intricate`, `remarkably`, `substantially` | 3–4 |
| "in conclusion", "it is worth noting" | 4 |
| `delve`, `showcase`, `holistic`, `vital`, "for the first time" | 5 |

**Start with the em dash.** Forty-three of 45 papers contain none. It costs
nothing to remove and it is the most reliable single signal in the set.

## Structural tells the word lists miss

Frequency is only half of it. These show up as shape:

- **Uniform paragraph length.** Generated sections run 4–5 sentences per
  paragraph throughout. Real sections have a two-sentence paragraph where the
  argument turns and an eight-sentence one where it does not.
- **Every paragraph opening with a connective.** *Furthermore… Moreover…
  Additionally…* Each word is normal; the sequence is not.
- **Symmetric contribution lists.** Three bullets of near-identical length,
  each starting with the same part of speech.
- **Claims with no number.** "Our method significantly improves performance" in
  a paragraph that never says by how much on what.
- **The summary sentence that adds nothing.** "In this section, we have
  presented…" at the end of every section.
- **Captions that name the picture.** "Overview of our framework." The corpus
  median figure caption is 39 words and states a claim.
- **Vague attribution.** "Recent studies have shown" with a citation block
  rather than a specific paper doing a specific thing.

None of these are detectable by grep, which is why the auditor reports what it
can measure and this file lists what you have to read for.

## The order to work in

1. `python3 scripts/audit_paper.py paper/` — fix every `error`, decide on every
   `warn`.
2. Remove em dashes.
3. Read the paragraph *openings* down the page in one pass. Vary them.
4. Read the paragraph *lengths*. Break the rhythm where the argument turns.
5. Find every claim without a number and either attach one or cut the claim.
6. Read the captions alone, in order. They should tell the story of the paper.
7. Leave `leverage` alone.

## What this is not

Not an attempt to defeat AI-text detectors. Those tools are unreliable, and
their false-positive rate on non-native English writing is high enough that
optimising against them is both futile and unfair to the people they
misclassify. The goal here is prose that reads like the venue, which is a
writing goal, and it happens to be the same work.
