# Argument graph — every scientific claim needs a corresponding test

Maintain edges from proposed hypotheses to literature, code paths, experiments, tables/figures and counterevidence. A good paper tells **one testable argument**, not just a list of network components.

## Graph contract

- `claims` — each has `id`, `statement`, `status` (`hypothesis`, `supported`, `refuted`, `uncertain`) and `source_ids`.
- `sources` — each has stable `id`, `url`, `kind` (paper, appendix, code, log, data, other) and optional `version`/`location`.
- `experiments` — each has `id`, `claim_ids`, `protocol`, `negative_control`, `status` (`planned`, `run`, `blocked`), and, when `run`, `log_source_id`.
- `figures` — each has `id`, `claim_ids`, `purpose`, `experiment_ids`; every result figure must be anchored to actual experiments before presentation as empirical evidence.

Run `scripts/claim_graph.py validate ...` to check dangling references and missing evidence (not the semantic truth of the research). `report` shows hypothesis/evidence/test gaps and identifies claims that lack a planned falsification test.

## Figures as argument, not decoration

1. **Teaser**: one concise counterexample / bottleneck / contrast grounded in a real case, not fabricated results.
2. **Method diagram**: entities are tensors/representations/modules actually found in code, with clear directions, shapes, losses and training-only branches.
3. **Main comparison**: fair protocols; hardware/environment differences explicitly noted.
4. **Ablation table**: remove a single mechanism, leave the rest matched; include the baseline.
5. **Failure grid**: reveal systematic limits, not cherry-picked cases.
6. **Efficiency curve**: actual latency, VRAM, task result at matched budget with hardware reported.

Do not generate a performance bar with invented numerical data. When a figure is mockup-only, label its synthetic numbers prominently.
