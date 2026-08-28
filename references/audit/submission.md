# Submission check

Last stage. Format and compliance only; no content changes here.

## Venue geometry

| Venue | Pages (excl. refs) | Column | Style |
|---|---|---|---|
| CVPR / ICCV / WACV | 8 | 237.13 pt | two-column, `cvpr.sty` |
| ECCV | 14 | 347.12 pt | single-column LNCS |
| NeurIPS | 9 | 397.48 pt | single-column |
| ICLR | 9 | 397.48 pt | single-column |
| ICML | 8 | 234.88 pt | two-column |
| AAAI | 7 | 238.49 pt | two-column |
| ACL / EMNLP | 8 | 219.08 pt | two-column |

Confirm against the current call for papers. These change.

## Checklist

- [ ] Page limit met **without** shrinking margins, line spacing, or float
      separation. Reviewers and desk checks both look for this.
- [ ] Anonymised: no author names, no acknowledgements, no institutional
      identifiers in paths, no `\thanks`.
- [ ] Self-citations in the third person.
- [ ] Supplementary is a separate file if the venue requires it, and the main
      paper is self-contained without it.
- [ ] Every figure is vector (PDF) unless it is genuinely a photograph.
      Rasterised diagrams are the most common camera-ready regression.
- [ ] Fonts embedded. `pdffonts paper.pdf` — every row should say `emb`.
- [ ] PDF has no comments, no `\todo`, no visible change bars, no
      `\usepackage{lineno}` left in.
- [ ] Bibliography style matches the venue; no `\cite{?}`.
- [ ] File size under the portal's limit; a 600 dpi raster nobody needed is
      usually the cause.
- [ ] Checklist / reproducibility statement / ethics statement filled in where
      the venue asks, honestly.
- [ ] Code and data availability statement matches what will actually be
      released, on a date you will actually meet.

## Quick commands

```bash
pdffonts paper.pdf | head -20        # every font should show emb
pdfinfo paper.pdf                    # page count and page size
grep -rn "todo\|TODO\|XXX\|FIXME" *.tex
grep -rn "\\\\thanks\|acknowledg" *.tex   # anonymity
python3 scripts/audit_paper.py .     # structure and prose, one more time
```

## Figures at camera-ready

The most common late failure is a figure that was fine on screen and is
unreadable in print. If the figures came from CVPR-Figure, re-run its auditor
after any resize:

```bash
python3 ../cvpr-figure/scripts/validate.py figures/src/overview.yaml \
        --svg figures/overview.svg
```

Under 5.0 pt rendered type is an error there, and that threshold is the 29th
percentile of what published figures actually do — so it is a floor, not a
target.
