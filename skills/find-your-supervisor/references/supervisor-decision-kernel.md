# Supervisor decision kernel: construct → challenge → decide

**Aim:** turn paper-level evidence into a research student's next concrete decision. This is a protocol, not a claim to possess a particular scientist's mind.

## Stage A: constructive mentor

Answer in plain, testable language: (1) which observed failure motivates the question? (2) why does a reasonable baseline fail? (3) which representation/architecture/data modification is minimal? (4) what public evidence suggests it could work? (5) what prior papers already overlap? (6) how does the proposed experiment isolate the central mechanism?

## Stage B: independent skeptical reviewer

Review without access to Stage A's justifications if an independent agent is available; otherwise adopt an explicitly separate adversarial pass. Check closest work, inadequate baselines, confounders, class distribution, hardware mismatch, test-set leakage, synthetic-to-real generalization, unmeasured cost and irreproducible pipeline. State the most plausible rejection reason and the **cheapest decisive counterexperiment**. Do not pretend a second model was invoked if it was not.

## Stage C: decision

Return one of `GO` / `REVISE` / `PIVOT` / `BLOCKED` with explanation and evidence. `GO` means pilot justified, not publication guaranteed. Always record disconfirming observations and compute ceiling. Prefer 1 short baseline and 1 controlled perturbation to five trained variants at the outset.

## Meeting notes (for weekly check-ins)

- Prior hypothesis, test planned, execution evidence, confidence and negative results
- Current claim → required result → observed result; sources must be pinned
- Unexpected failures, new overlapping papers, assumptions invalidated
- Decision and next 3 tasks; explicit budget and stop criterion
- Next question in researcher lineage, without adopting someone else's identity

## Supervisor-comparison scorecard

Do not reduce scholarly quality to h-index or total paper count. Distinguish mentoring fit from fame: coherence of publicly observable research programme, evidence of accessible artifacts, training-resource needs, researcher-topic match, breadth-vs-depth tradeoff, ethical boundaries, and opportunities for independent contributions. If student background is unknown, show assumptions, not precise personalized rankings.
