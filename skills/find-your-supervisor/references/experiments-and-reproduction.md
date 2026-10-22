# Low-compute experiment discipline

## Resource accounting

Make assumptions explicit: GPU model and available VRAM, memory, GPU hours, wall-clock, disk for datasets/checkpoints, preprocessing, teacher outputs, hyperparameter search, evaluation rollouts and reproduction costs. Compute once for baseline and again for ablations. Do not equate one GPU 24GB with multi-node full-paper training.

## Pre-register hypotheses

For each H: causal factor, predicted effect, dataset/split, metric, nearest alternative explanation, primary baseline, exact change, seeds, resource cap and reject threshold. Distinguish scientific significance from publication SOTA.

## Experiment matrix

- **Sanity**: evaluate published checkpoint; deterministic data loader; test tiny overfit; metric parity.
- **Simple controls**: frozen backbone/no new module, FIFO, random, saliency, learned query, same params.
- **Mechanism**: drop novelty component, perturb representation, replace geometry with matched 2D features, temporal shuffle and blind/unblind ablations.
- **Robustness**: corruptions, sensor or modality dropout, calibration drift, camera change, occlusion, changed domain, long horizon.
- **Efficiency**: same device and batch size, warmup, peak CUDA mem, real latency distributions incl preprocessing; FLOPs and train GPUh separately.
- **Confidence**: multiple seeds, intervals, paired scenario comparison; avoid selecting best test result.

## Reproduction ledger

Reference experiment includes paper URL/version, official commit SHA, commands, datasets and licenses, container/driver/CUDA/torch, checkpoint hashes, seeds, run logs, full metric definitions, paper versus observed results and exceptions. Record non-reproduced/censored results faithfully. A smoke test confirms wiring, not original numbers.

## Decision gates

Week 1–2 minimal benchmark > mechanism probing > only then costly model changes. If matched simple baseline wins, pivot to failure analysis or a sharper scientific question. End with reproducible plots and a failure taxonomy, even for negative findings.
