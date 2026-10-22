# Paper reading protocol: page by page, not title by title

Read main PDF and supplementary PDF, recording page numbers in the **PDF version actually read** (printed page numbers may differ). Process every table and figure, including axes and captions. When full PDF unavailable, downgrade status and keep a retrieval task.

## Page coverage and scientific extraction

For each page, record `p. N: claim, evidence, figure/table/equation, unresolved question`. Ask:

1. **Problem and stakes:** precise inputs/outputs, operational failure motivating the work, compared to what, in which regime?
2. **Prior art boundary:** nearest 3–8 competitor papers *including independent labs*, shared assumptions, distinctions and overlaps. Verify dates.
3. **Method:** tensors and shapes; original modules, parameterizations, attention, geometry, memory, objective, losses, curriculum, inference constraints; derive equations rather than only paraphrase.
4. **Implementation:** which parts rely on pretrained teacher, data preprocessing, hand-designed priors or third-party code? Inspect links to actual code if possible.
5. **Evaluation:** exact split, metrics, downstream vs proxy, hardware, training protocol, seeds, inference, robustness, qualitative selection bias, uncertainty.
6. **Ablations:** whether one variable changes at a time and whether control parameters/data/FLOPs match. Include negative and contradictory results.
7. **Limits and speculation:** explicit author-stated limitations vs your own inference. Mark sample sizes and risk of overclaim.
8. **Paper rhetoric:** inspect what motivates Figure 1, ordering of contributions, abstract claim/data alignment, method figure completeness, where each claim is verified in the tables.

## Full-read acceptance

`full_main` only if exact main-PDF hash/page count exists, all pages have recorded notes, and the card contains specific references to the method, experiments, figure/table and limits. `full_with_supplement` additionally requires all appendix pages. A list of numbers alone is weak evidence; check quality manually. The CLI enforces necessary conditions, not sufficient academic understanding.

## Suggested writing

> Claim: ... Evidence: [Title, v3, PDF p. 8, Table 2]. Status: directly verified. Threat: difference in batch size; comparable only in FLOPs, not latency.

Do not copy full paper text or protected figures into the Skill; preserve citations and paraphrased analysis.
