# Code release, measured

Load this when planning what ships with a paper, or when writing the
reproducibility statement a submission checklist asks for.

Measured across the 46 released repositories that accompany the corpus papers.

## What is actually in the box

| Present | Share |
|---|---|
| `README.md` | **46 of 46** |
| `LICENSE` | 33 (72%) |
| `requirements.txt` | 23 (50%) |
| An `assets/` or `figs/` directory of paper figures | 23 (50%) |
| `setup.py` | 14 (30%) |
| `tools/` (train / test / conversion entry points) | 13 (28%) |
| `configs/` | 12 (26%) |
| `docs/` | 11 (24%) |
| OpenMMLab layout (`mmdet3d/`, `projects/`, …) | 7 (15%) |

Two observations worth acting on.

**A README is universal and a LICENSE is not.** Nine repositories out of 46 are
"open source" with no licence at all, which legally means nobody may use them.
This is a five-minute fix that a surprising number of strong groups skip.

**Half of them ship the paper's figures in the repo.** `assets/`, `figs/` or
`images/` holding the very PDFs that `\includegraphics` pulls in. If you keep
your figure specs alongside the artwork — which CVPR-Figure is built to let you
do — that directory becomes the reproducible half of your figures too.

## Two ways these groups define a model

**Config-driven (OpenMMLab).** The architecture lives in
`configs/<paper>/<variant>.py` as `model = dict(type=..., img_backbone=dict(...),
...)`, and the classes in `mmdet3d/models/` are registry entries. Dominant in
the driving and detection work.

**Class-driven.** A plain `nn.Module` tree under `models/` or `model/`, with
hyper-parameters as constructor arguments. Dominant in the restoration,
homography and tracking work.

Which one a repository uses determines how to read it, and it determines which
front-end of CVPR-Figure's `from_code.py` to point at:

```bash
python3 ../cvpr-figure/scripts/from_code.py configs/model.py --mm   # config-driven
python3 ../cvpr-figure/scripts/from_code.py models/ --list          # class-driven
```

Prefer the config when there is one: it names every stage in pipeline order
with its channel widths, which is exactly what a framework figure needs.

## Naming, and why it matters for the paper

The gap between what a module is called in the code and what it is called in
the paper is where reviewers get confused and where a code-derived figure goes
wrong. `img_bev_encoder_backbone` in the config is "BEV Encoder" in the text.

Decide the paper's names first, then keep a one-line mapping in the README so a
reader moving between the two does not have to guess. Half the value of
releasing code is lost when the reader cannot find the contribution in it.

## A minimum release

Nothing exotic; this is what the corpus does, plus the two things half of it
forgets:

```
README.md          what it is, install, train, eval, checkpoint links,
                   and the code-name -> paper-name mapping
LICENSE            pick one. MIT or Apache-2.0.
requirements.txt   pinned, or an environment.yml
configs/ or models/  the architecture, in whichever of the two styles
tools/             train.py, test.py, and the data conversion you had to write
assets/            the figure artwork and the specs that generated it
```
