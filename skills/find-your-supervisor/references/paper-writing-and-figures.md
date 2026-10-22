# Paper argument architecture, rhetorical analysis and visual evidence

Do not imitate a researcher's distinctive wording or duplicate copyrighted figures. Analyze **structural choices** and elevate them with outside examples.

## Claim-driven paper structure

- Title: the *problem/idea*, not only a branded acronym.
- Abstract: failure → limitation of strongest existing work → concrete principle → what actually changed → quantified *verified* result and scope.
- Introduction: central tension and why solving it matters, then specific scientific hypothesis, not an unsourced promotional list.
- Related work: group by failure/assumption and explain closest conflicts and why this is not redundant.
- Method: overview with typed inputs/outputs, derivation with dimensionally coherent equations, a diagram matching Forward, implementation without hidden extra supervision.
- Experiments: study mechanics, strong baselines, fair matched budgets, ablations, OOD, resource cost, failure analysis, uncertainty.
- Limitations: boundary of task, data, bias, cost, reproducibility and mistakes discovered by auditing.

## Figure and table storyboard

1. **Teaser (Fig 1):** concrete failing situation, baseline failure, what your mechanism changes; avoid visually misleading montage or noncomparable views.
2. **Method (Fig 2):** precise dataflow and variables; input dimensions and train-only versus inference-only branches clearly marked. Diagram should map to actual code paths.
3. **Mechanism evidence:** targeted variable or controlled perturbation; show cases where it fails.
4. **Main table:** metrics and dataset protocols matched; bold only fair comparable values; include resource columns.
5. **Ablation table:** hypothesis per row, same seeds/config, avoid multi-change comparisons.
6. **Efficiency plot:** Pareto front mAP/success versus latency or memory, measuring hardware accurately.
7. **Qualitative figure:** positive, negative, ordinary, and adversarial cases selected with stated protocol.

For each figure, make a `claim → visual encoding → source dataset → axis labels → statistical unit → failure condition` map. Never manufacture quantitative data. Use vector/editable assets where possible, and consistent color semantics and font accessibility.

## Style comparisons

Use the target scholar and at least 2 other excellent papers as *structural comparators*: paragraph progression, claims density, headings, appendix organization, figure placement. Don't assert a universal unique voice from coauthored prose.
