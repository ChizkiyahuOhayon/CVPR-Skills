# Writing the code

Load this when starting the implementation, or when deciding how to structure
a repository that will be released with the paper.

The measurements are from the 46 repositories that accompany the corpus papers;
the structural advice is about keeping the code and the paper in step, which is
where most of the pain in a submission cycle actually comes from.

## Pick a shape early, and pick one of the two

The corpus uses exactly two, and mixing them is what produces repositories
nobody can navigate.

**Config-driven** (OpenMMLab: mmdet, mmdet3d, mmseg). The architecture lives in
`configs/<paper>/<variant>.py` as `model = dict(type=..., ...)`; classes are
registry entries. Choose it when you will run many variants, when your
baselines are already in that ecosystem, and when the ablation is a grid.

**Class-driven.** A plain `nn.Module` tree under `models/`, hyper-parameters as
constructor arguments, one training script. Choose it when the method is a
single architecture, when you want the repository readable by someone who does
not know mmengine, and when you are not inheriting a baseline.

Config-driven costs a week of ramp-up and saves a month on the ablation.
Class-driven is the reverse. Decide before writing the training loop.

## Name things for the paper, from day one

The single cheapest thing you can do, and almost nobody does it.

`img_bev_encoder_backbone` in the code is "BEV Encoder" in the paper. Every
hour spent translating between the two — writing the method section, drawing
the figure, answering a reviewer, onboarding a collaborator — is an hour that a
naming decision in week one would have saved.

Keep a mapping in the README:

```
code                      paper
------------------------  ---------------------
occ_fuser                 Cross-Modal Fusion
pts_pillar_layer          Point Voxelisation
occ_encoder_backbone      3D Encoder
```

This also determines whether a code-derived figure is usable: CVPR-Figure's
`from_code.py` labels boxes with the attribute names, and the first edit you
make to its output is always renaming them.

## The ablation is a code-structure decision

96% of the corpus papers run an ablation, and the ablation is where the code
either helps or fights you. Build every contribution behind a flag from the
start:

```python
model = dict(
    type='OurNet',
    use_reciprocal_matching=True,   # contribution 1
    use_temporal_prior=True,        # contribution 2
    ...)
```

Turning a component off must be one flag, not a code edit, or the ablation
table becomes four half-broken branches a week before the deadline. This is the
main practical reason to prefer config-driven for a method with three or more
parts.

## Determinism, at the level this field actually needs

Fix the seed, log it, and log the config with every checkpoint. That is enough.

Do **not** build a full reproducibility harness — deterministic cuDNN kernels,
hash-pinned environments, multi-seed sweeps on every run. Measured across the
corpus, **0 of 46 papers report multiple seeds** and only 11% report any
variance at all. Spend that effort on an extra ablation row instead; see
`../corpus/experiment-design.md`.

The exception: if a headline gain is under about one point on the metric, run
two or three seeds for *that* number so you can say the spread in one sentence.

## Logging

Log enough to reconstruct a table row six weeks later: config, git SHA,
checkpoint path, the metric, and the setting it was measured at. A results
`.csv` or a Weights & Biases project is enough. The failure mode is a number in
a table that nobody can trace to a run.

## What to release

From the 46 accompanying repositories:

| Present | Share |
|---|---|
| `README.md` | **46 of 46** |
| `LICENSE` | 33 (72%) |
| `requirements.txt` | 23 (50%) |
| `assets/` or `figs/` with the paper's figures | 23 (50%) |
| `tools/` entry points | 13 (28%) |
| `configs/` | 12 (26%) |

Nine of 46 have no licence, which legally means nobody may use the code. It is
a five-minute fix and a surprising number of strong groups skip it.

A minimum release:

```
README.md          what it is, install, train, eval, checkpoints,
                   and the code-name -> paper-name mapping
LICENSE            MIT or Apache-2.0
requirements.txt   pinned, or environment.yml
configs/ | models/ the architecture, in one of the two shapes
tools/             train.py, test.py, and the data conversion you wrote
assets/            the figure artwork and the specs that generated it
```

That last line matters more than it looks: half the corpus repositories already
ship their figure files, and if the figure *specs* live there too, the figures
become as reproducible as the numbers.
