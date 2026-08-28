# Integrity audit

Run before review, and again before camera-ready. It checks the paper against
itself; nothing here needs external sources.

## Numbers

- Every number in the prose appears in a table or figure, with the same value.
  Rounding differences between text and table are a real finding.
- Every bolded "best" in a table is actually the best in its column, including
  where lower is better.
- Improvements quoted in the abstract match the main table.
- Percentages: absolute or relative? Pick one, say which, and be consistent.
  "Improves mIoU by 5%" is ambiguous and reviewers read it uncharitably.
- Totals add up. Ablation rows that remove one component each should land on
  the stated baseline when all are removed.

## Claims

For each claim in the abstract and introduction, name the table, figure or
section that supports it. A claim with no referent is either unsupported or
belongs in the conclusion as a direction.

Three specific patterns:

- **Generalisation claimed from one benchmark.** Either add the second
  benchmark or scope the claim to the first.
- **Efficiency claimed without a cost table.** Parameters, FLOPs, latency or
  memory — at least one, measured on stated hardware.
- **"First to" claims.** These get checked. Make them precise enough to be
  true, or drop them. Only five of 45 corpus papers use "for the first time"
  at all.

## Figures and tables

- Every float is referenced from the text, in order.
- Every axis has units. Every table column has a metric and a direction (↑/↓).
- The caption states what is being compared, not what the object is.
- Colours mean the same thing in every figure in the paper. This is the single
  most visible sign of a figure set assembled rather than designed, and
  CVPR-Figure's auditor checks it within one figure — across figures, you have
  to check it.
- No figure contains a crop from another paper presented as your own result.

## Reproducibility

- Backbone, input resolution, schedule, batch size, hardware, and seed policy
  are all stated somewhere findable.
- Baseline numbers are labelled as reproduced or quoted, and quoted ones cite
  the source.
- If the setting differs from the baseline's original, that is in the caption,
  not a footnote.

## Automated part

```bash
python3 scripts/audit_paper.py paper/
```

That covers structure, prose distribution, caption lengths and float
inventories. It does not read the numbers. Everything above is a human pass.
