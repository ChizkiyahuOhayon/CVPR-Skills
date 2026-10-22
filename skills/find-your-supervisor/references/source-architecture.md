# Architecture — researcher-specific study rather than generic research assistant

This Skill's product is **an evidence-backed researcher model that improves a student's independent research practice**. It is not a generic 100-skill library and does not attempt to regenerate the paper-writing guidance already available elsewhere.

## Feature synthesis — independent implementation

| Independent public project | Valuable pattern (not copied code/text) | What Find Your Supervisor implements |
| --- | --- | --- |
| [CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills) | Research storyline continuity, distinct idea-generation vs reviewer/writer tasks, claim ↔ experiments ↔ figures integrity, selective skill routing | Explicit argument/evidence graph, handoff contract between mentor/reviewer/engineering/writer, non-fabrication gates |
| [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | Research apprenticeship and a structured advisor/student decision process | Independently written weekly supervisor meeting, blind spots, paper-/person-level confidence, one falsifiable pilot, adversarial review. **No CC BY-NC-SA text or code copied.** |
| [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Specialized engineering references and orchestration by capability instead of one monolithic prompt | Conditional engineering router keyed by task, framework, environment, resource, and actual installed skills; explicit read-only/run/replication tiers |

Licenses checked October 2026: CCFA-Skills = MIT; AI-Research-SKILLs = MIT; Supervisor-Skills = CC BY-NC-SA 4.0. This codebase is *not* a fork of any of them, and redistributes none of their text, examples, or proprietary figures. Linking to a source does not install its skills or grant the agent tool access. See `ATTRIBUTION.md`.

## Three layers

1. **Reusable workflow**: identity, corpus, reading, code, experiments, argument audit, mentor feedback.
2. **Profile workspace**: researcher-specific paper cards, code maps, contribution roles, genealogy; by default PRIVATE and OUTSIDE this package.
3. **Student research plan**: independent novelty search, assumptions/compute budgets, cheap pilot, checkpoint and pivot decision.

Separation keeps the public tool reusable without publishing any specific person's private notes or the student's unpublished data.

## Gate discipline

At every stage, use actual artifact paths and source references. A generated summary is not a verified paper reading. A checked SHA does not demonstrate runtime compatibility. A logged test proves the precise test—not the complete paper. This is an integrity constraint, not a reason to refuse partial help.
