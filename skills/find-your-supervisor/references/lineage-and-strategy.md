# Scientific genealogy and research-DNA inference

A researcher is not a flat bag of models. Reconstruct a multi-branch directed graph from *questions* and *limitations*, with dates and confidence.

## Build lineage edges

For each transition, fill:
`prior work → unsolved failure → newly proposed representation/algorithm/optimization/data/benchmark → expected causal mechanism → empirical proof/failed tests → resource requirements → subsequent work`.

Do not invent author motivation. Use wording such as `The paper addresses X after earlier work left Y open`, not `The author privately decided ...`. An edge can be from unrelated labs or a concurrent idea rather than direct lineage.

## Research DNA (as hypotheses)

Analyze across 3+ representative first/lead-author papers and collaboration papers:

- Persistent scientific questions and objects: features, scenes, world states, actions, efficiency, uncertainty, dynamics, supervision.
- Representation grammar: coordinate systems, memory objects, structured latents, sparsity, temporal causality, geometry priors.
- Leverage strategy: frozen teachers, publicly available architectures, datasets, knowledge/data distillation, synthetic supervision.
- Proof style: task benchmark, efficiency Pareto front, OOD generalization, error decomposition, ablations, real-world validation.
- Writing/figure grammar: problem-to-solution contrast, pipeline decomposition, claim-table linkage, representative visualization vs cherry-picking risk.
- Negative evidence: failed improvements, contradictory settings, old ideas abandoned, overfitting to benchmark, unavailable code.

For each inferred pattern state `number of independent confirming works`, `counterexample`, `how general is this in the field?`, and `confidence`. Do **not** make personality judgments or claim an author's secret decision-making process.

## External counterweights

Compare exemplary method, empirical, benchmark and negative-result papers outside the target researcher's group. Ask whether the detected pattern is a universal good research habit, trend across the field or a genuinely distinctive choice. Include collaborators' principal contributions where identifiable.
