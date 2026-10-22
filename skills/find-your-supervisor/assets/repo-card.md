# Repository audit card · {repository@sha}

- Repo/project URL; paper IDs; official/community? license; commit SHA/tag; date read
- Sources included/excluded; vendored code separately named; inspected paths and line anchors
- Runtime prerequisites, CUDA custom ops, model weights, data access and licensing
- Computation DAG: input -> dataset -> preprocess -> model -> original block -> loss -> eval
- Tensor shapes, coordinate frames, memory cache, detach/freezing, teacher-only privilege
- Claim-to-code: paper/page/claim -> path:class.function@sha -> observation -> discrepancy
- Training command, inference command, evaluator, possible test leakage / reproducibility failures
- Compute inventory: GPUs, VRAM, GPUh, disk, checkpoints, precomputation, rollouts
- Real runs: actual command, logs/checkpoint hashes, seeds, measured/reference metrics
- Scope: readme_checked / core_partial / source_audited / blocked (with evidence)
