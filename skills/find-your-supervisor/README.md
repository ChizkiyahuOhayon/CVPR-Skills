# Find Your Supervisor · v0.2.0

**A general-purpose Agent Skill for studying a scientist's entire publicly discoverable research career, including papers, supplementary material, code and results—then mentoring your own original research with honest evidence gates.** Unaffiliated with and not endorsed by any researcher.

> **Input:** researcher name, ORCID / homepage / DBLP / GitHub plus your research topic and compute limitations.  
> **Output:** validated paper inventory, annotated PDF reading, source-pinned code maps, research genealogy, inferred research principles, a low-compute falsification pilot, and an independent reviewer challenge.

## Why this is different

Most research skills help you **write a paper** or **train a model**. Find Your Supervisor first asks **why a researcher's scientific questions evolved**, what a given paper actually proves, where the method lives in code, which ideas are really author-specific, and what a student could independently contribute under limited resources.

It uses six audit gates: identity → bibliography → paper pages → code archaeology → replication evidence → original research guidance. The reading/reproduction ledger cannot be promoted to 'complete' just because a Markdown card or README exists. The agent must show source and experiment evidence and uncertainty.

The v0.2 improvement adds a **mentor → skeptical reviewer → decide** protocol, a **claim ↔ source ↔ experiment ↔ figure** graph validator, and a capability-aware router for engineering/figure/writing specialists. All three features are independent implementations; they do not download or bundle external projects. See [architecture](references/source-architecture.md) and [attribution](ATTRIBUTION.md).

## Install

Copy this entire directory to your agent's skills directory (e.g. `.agents/skills/find-your-supervisor/` or `.claude/skills/find-your-supervisor/`, depending on the host) so it can read [SKILL.md](SKILL.md).

Example user message:

> Use `find-your-supervisor` to study researcher `<homepage or ORCID>`. Reconcile the complete public paper list, verify the closest 5 papers and corresponding code, map their research lineage, and use their evidenced habits to propose a distinctive but feasible experiment for my problem with a single 24GB GPU. Distinguish unreviewed work from complete reading, and give the most likely reviewer objection.

## Offline checkers (Python 3.8+, zero dependencies)

```bash
python scripts/audit.py init --name 'Example Scientist' --slug example-scientist --output researcher.json
python scripts/audit.py validate researcher.json
python scripts/audit.py report researcher.json
python scripts/claim_graph.py validate assets/claim-graph.example.json
python scripts/claim_graph.py report assets/claim-graph.example.json
python scripts/check_skill.py
python -m unittest discover -s tests -v
```

These scripts validate structural claims and link integrity; they do not search scholarly indexes, download source, execute training or prove scientific understanding. The graph example is **hypothetical**, not a research result. Reading public papers and running code require the host's actual tools and the user's compute/data permissions.

## File map

`SKILL.md`: routing and six-gate protocol; `references/`: detailed discovery, reading, code, mentorship, idea, experiments, figures, argument, engineering router; `assets/`: generic blank/hypothetical templates; `scripts/`: research-state and argument-graph validators; `tests/`: offline tests; [`ATTRIBUTION.md`](ATTRIBUTION.md): inspiration and licenses.

## Public vs private

This **public** repository contains *only* general procedures and fictional/synthetic examples, not individual researcher dossiers or student projects. Store named researcher corpora, source notes and unpublished ideas in an independent private workspace. See [public design rationale](references/source-architecture.md).

## Related projects and licenses

Conceptually informed by [CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills) (MIT), [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) (CC BY-NC-SA 4.0) and [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) (MIT). **No text, code, figures or templates from these projects are copied or redistributed**, especially nothing governed by the non-commercial/share-alike license. This Skill uses independently authored methods and links to the original resources. Details: [`ATTRIBUTION.md`](ATTRIBUTION.md).
