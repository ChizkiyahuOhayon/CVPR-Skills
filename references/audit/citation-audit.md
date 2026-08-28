# Citation audit

Fabricated and mangled references are the fastest way to lose a reviewer's
trust, and they are now common enough that some venues check for them
mechanically. This is a two-layer check: a tool for what a tool can do, and a
read for what it cannot.

## Layer 1 — RefChecker

[RefChecker](https://github.com/markrussinovich/refchecker) validates that each
reference exists and that its metadata matches. It is a separate project, not
vendored here.

```bash
pip install academic-refchecker[llm]

academic-refchecker --paper paper.pdf
academic-refchecker --paper main.tex
academic-refchecker --paper refs.bib
academic-refchecker --paper 1706.03762                    # arXiv ID or URL

# structured output to work through
academic-refchecker --paper paper.pdf --report-file report.json --report-format json
```

It catches: references that do not exist, wrong authors, wrong year, wrong
venue, arXiv preprints cited as though published (and the reverse), and
duplicate entries.

If it is not installed, say so rather than skipping the step silently — an
unaudited bibliography should be reported as unaudited.

## Layer 2 — what no tool checks

A reference can exist, have perfect metadata, and still be wrong. These need a
person, and they are where the damage is:

- **The citation does not support the claim.** The most common real error. A
  paper is cited for a result it does not contain, usually because the citation
  was chosen from an abstract or from another paper's related-work section.
- **Cited for the wrong contribution.** Right paper, wrong reason.
- **Attribution drift.** Method M is credited to the paper that popularised it
  rather than the one that introduced it. Check the earliest.
- **A survey standing in for a primary source.** Fine for "see [S] for an
  overview"; not fine for a specific technical claim.
- **The comparison number is not the number in that paper.** A baseline entry
  in your main table that does not match the source's own reported result, at
  the same setting, is a rebuttal-grade problem. Check every borrowed number
  against its origin and note the setting in the caption when it differs.
- **Self-citation density.** Count it before a reviewer does.

## Anonymity

At submission, check that self-citations are in the third person and that no
`\cite` reveals authorship through phrasing ("in our previous work [12]").
`scripts/audit_paper.py` does not check this; the submission stage does.

## Scale check

The corpus runs **40–56 distinct references**, median 46, spread over a median
of 73 `\cite` calls — so the average work is cited about one and a half times.
A draft with 25 references is not under-read, it is under-cited, and the
related-work section will read as thin. A draft with 120 in eight pages is
usually padding a section that should have been an argument.
