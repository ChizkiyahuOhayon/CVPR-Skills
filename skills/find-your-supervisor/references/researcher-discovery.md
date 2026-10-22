# Researcher identity and full-corpus discovery

## Identity resolution (DO NOT skip)

- Record name variants, current/past institution, field, personal website, ORCID, DBLP URL, Scholar profile and OpenAlex ID as available. Check coauthor network, overlapping time windows and institutional affiliations to distinguish identical names.
- Prefer the personal site/CV for stated roles, DBLP/Crossref/OpenAlex/venue sites for title/venue/DOI, original publisher/arXiv for PDF metadata and papers, GitHub/project sites for code. No single source guarantees completeness.
- Resolve **publication versions**: arXiv preprint, conference proceeding, journal extension and workshop may refer to one study. Assign `canonical_work_id` and separate version IDs. Mark substantial changes and whether to count as distinct research contributions.
- Use both time windows: career overview and rolling last five years (explicit boundaries; a year-grouped view can span six calendar years). Distinguish paper publication date vs arXiv posting date.

## Completeness procedure

1. Collect author-listed publications (CV, lab page, institutional listing), then query at least two independent bibliographic registries (DBLP, Crossref, OpenAlex, proceedings/DOI, Semantic Scholar) using stable IDs when possible.
2. Deduplicate by DOI and normalized title, then inspect suspected near-matches by author list, title and abstract. Do not auto-collapse different scientific contributions with similar names.
3. Cross-check title/year, venue type (main conference, workshop, journal, preprint), authorship position and explicit contributor/project-leader markers. Equating middle authorship with ownership is prohibited.
4. Add PDFs, supplements, official code and forks; store project status (released/not released/inaccessible). Verify code-paper match and licenses, do not confuse a community reimplementation with official source.
5. Maintain `excluded_work`, `ambiguous_identity`, `unresolved`, `last_checked` and `query_snapshot` with dates and URLs.

## Source reliability ranking

- P0: Original PDF (precise version/page/figure), supplement, publisher DOI; inspected source file at pinned commit; actual run logs.
- P1: Official scholar/homepage/CV, official repo README, dataset docs.
- P2: Indexing platform metadata, public paper abstract, third-party synopsis.
- P3: Informal posts/commentary. Never let P3 displace contradictory P0 evidence.

## Output inventory columns

`canonical_id, title, year, publication_type, venue, authors, role_evidence, doi, arxiv, pdf_version, supplement, project_url, official_repo, category, corpus_stage, code_stage, reproduction_stage, provenance_urls, last_checked, open_questions`.

Coverage is a fraction of a **dated, explicitly scoped set of discovered works**, not an assertion that no more papers exist. Provide both the numerator/denominator and methodology for the denominator.
