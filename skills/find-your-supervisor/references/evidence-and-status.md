# Status calculus, auditability and truth-in-advertising

Status should be **derived from evidence**, never incremented just because a narrative was generated.

## Paper stages

`metadata_only`: title/author/year known. `abstract_checked`: abstract read. `selected_pages`: confirmed subset of a PDF. `full_main`: every page of exact main PDF accounted for, page-level notes+method/experiment/limitation anchors. `full_with_supplement`: main + supplemental as above. `blocked`: source not accessible. No stage implies comprehension or reproduction.

## Code stages

`unlinked`: no repo. `readme_checked`: metadata and instructions only. `core_partial`: one or more relevant source files inspected at pinned SHA; actual functions/paths noted. `source_audited`: scoped first-party source inventory reviewed and scientific claim-to-code map checked; exclusions explicit. `blocked`: inaccessible or broken repository. A repo may support multiple studies; do not count it as separate entire audit automatically.

## Reproduction stages

`not_run`, `smoke_test_only`, `partial_replication`, `metric_replication`, `failed`, `blocked`. `metric_replication` requires observed run with environment, dataset version, checkpoint, seed, logs, measured metrics, reference metrics, uncertainties and a comparison statement. Differences must be preserved, not masked.

## Evidence record

For each claim, record `source_uri`, `content_hash_or_commit`, `paper_version`, `page`, `figure/table/equation`, `repo_path`, `function`, `date_checked`, `extracted_fact`, `analyst_inference`, `confidence`, `counterevidence`.

## Metrics

- Paper scope: `n metadata / n abstract / n selected / n fully main / n main+supp`.
- Code scope: `n repos official / n readme / n core partial / n audited / n unavailable`.
- Reproduction scope: `n real runs / n matched results / n failed / n blocked`; tool unit tests are separate.
- Disclose that bibliography denominators are discovery-date limited, not exhaustive truth.

The local audit script checks **necessary consistency** (e.g., page coverage) but cannot verify that a claimed page note is truthful; human/editorial inspection and source comparison remain essential.
