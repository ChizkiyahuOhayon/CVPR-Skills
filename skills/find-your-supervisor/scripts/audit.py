#!/usr/bin/env python3
"""Evidence integrity validator; no dependencies, no network, no scientific claims.

Paper coverage is a *necessary* test, never proof of actual scholarly comprehension.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCHEMA_VERSION = "0.1.0"
PAPER_STAGES = ("metadata_only", "abstract_checked", "selected_pages", "full_main", "full_with_supplement", "blocked")
CODE_STAGES = ("unlinked", "readme_checked", "core_partial", "source_audited", "blocked")
RUN_STAGES = ("not_run", "smoke_test_only", "partial_replication", "metric_replication", "failed", "blocked")


def clean_slug(slug):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("slug must contain lowercase letters, numbers and hyphens only")
    return slug


def fresh(name, slug):
    return {"schema_version": SCHEMA_VERSION,
            "researcher": {"name": name, "slug": clean_slug(slug), "affiliation": "",
                           "identifiers": {}, "homepage": "", "identity_confirmed": False,
                           "scope": "all-public-research", "discovery_checked_at": "",
                           "sources_checked": [], "identity_notes": "Unverified, empty profile."},
            "papers": [], "repositories": [], "runs": [], "exclusions": [], "open_questions": []}


def complete_pages(fragment):
    if not isinstance(fragment, dict):
        return False
    try:
        n = fragment.get("page_count")
        pages = fragment.get("pages_read")
        notes = fragment.get("page_notes")
        hash_value = fragment.get("sha256")
        if not isinstance(n, int) or isinstance(n, bool) or not (0 < n <= 2000):
            return False
        if not isinstance(pages, list) or len(pages) != n or sorted(pages) != list(range(1, n+1)):
            return False
        if not isinstance(hash_value, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", hash_value):
            return False
        # Each page needs a non-empty observation. The script cannot establish truth.
        if not isinstance(notes, dict):
            return False
        return all(isinstance(notes.get(str(i)), str) and len(notes[str(i)].strip()) >= 10 for i in range(1, n+1))
    except (ValueError, TypeError):
        return False


def derived_paper_stage(p):
    if p.get("blocked_reason"):
        return "blocked"
    main = complete_pages(p.get("main_pdf"))
    if main and complete_pages(p.get("supplement_pdf")) and p.get("method_anchor") and p.get("experiment_anchor") and p.get("limitation_anchor"):
        return "full_with_supplement"
    if main and p.get("method_anchor") and p.get("experiment_anchor") and p.get("limitation_anchor"):
        return "full_main"
    if p.get("main_pdf", {}).get("pages_read"):
        return "selected_pages"
    if p.get("abstract_checked"):
        return "abstract_checked"
    return "metadata_only"


def derived_code_stage(r):
    if r.get("blocked_reason"):
        return "blocked"
    sha = r.get("commit_sha", "")
    reviewed = r.get("reviewed_files", [])
    eligible = r.get("eligible_source_files", [])
    claim_map = r.get("claim_to_code", [])
    valid_sha = isinstance(sha, str) and bool(re.fullmatch(r"[0-9a-fA-F]{40}", sha))
    if valid_sha and eligible and isinstance(eligible, list) and set(eligible) == set(reviewed) and len(reviewed)==len(set(reviewed)) and claim_map:
        return "source_audited"
    if valid_sha and reviewed and claim_map:
        return "core_partial"
    if r.get("readme_checked"):
        return "readme_checked"
    return "unlinked"


def derived_run_stage(run):
    if run.get("blocked_reason"):
        return "blocked"
    if run.get("execution_log") and run.get("exit_code") is not None:
        if run.get("failed") or run["exit_code"] != 0:
            return "failed"
        required = ("dataset_version", "environment", "hardware", "seed", "commit_sha", "command", "measured_metrics", "reference_metrics", "comparison_note")
        if all(run.get(k) or run.get(k) == 0 for k in required) and run.get("evaluation_type") == "paper_metric":
            return "metric_replication"
        if run.get("evaluation_type") in ("partial_paper", "paper_metric"):
            return "partial_replication"
        return "smoke_test_only"
    return "not_run"


def validate(data):
    errors=[]
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("Unsupported schema_version")
    if not isinstance(data.get("researcher"), dict):
        errors.append("Missing researcher object")
    for key in ("papers", "repositories", "runs", "exclusions", "open_questions"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key} must be a list")
    if errors:
        return errors
    for category, field in (("papers", "canonical_id"), ("repositories", "repo_id"), ("runs", "run_id")):
        ids=[]
        for item in data[category]:
            if not isinstance(item, dict) or not item.get(field):
                errors.append(f"{category}: record missing {field}")
                continue
            ids.append(item[field])
        duplicates=[k for k,v in Counter(ids).items() if v>1]
        if duplicates:
            errors.append(f"{category}: duplicate identifiers {duplicates}")
    for p in data["papers"]:
        if not isinstance(p, dict) or not p.get("canonical_id"):
            continue
        pid=p["canonical_id"]
        for k in ("title", "year", "url"):
            if not p.get(k): errors.append(f"paper {pid}: missing {k}")
        d=derived_paper_stage(p)
        if p.get("claimed_stage") and p["claimed_stage"] not in PAPER_STAGES:
            errors.append(f"paper {pid}: invalid claimed_stage")
        if p.get("claimed_stage") in ("full_main", "full_with_supplement") and d not in ("full_main", "full_with_supplement"):
            errors.append(f"paper {pid}: claimed {p['claimed_stage']} but verified as {d}")
        if p.get("claimed_stage") == "full_with_supplement" and d != "full_with_supplement":
            errors.append(f"paper {pid}: supplement coverage is insufficient")
    for r in data["repositories"]:
        if not isinstance(r, dict) or not r.get("repo_id"): continue
        d=derived_code_stage(r)
        if r.get("claimed_stage") == "source_audited" and d != "source_audited":
            errors.append(f"repo {r['repo_id']}: claimed source_audited but verified as {d}")
    for run in data["runs"]:
        if not isinstance(run,dict) or not run.get("run_id"):continue
        d=derived_run_stage(run)
        if run.get("claimed_stage") == "metric_replication" and d != "metric_replication":
            errors.append(f"run {run['run_id']}: claimed metric_replication but verified as {d}")
    return errors


def report(data):
    lines=[f"Researcher: {data['researcher'].get('name','unknown')}",
           f"Identity confirmed: {data['researcher'].get('identity_confirmed',False)}",
           f"Corpus checked at: {data['researcher'].get('discovery_checked_at') or 'not checked'}",
           f"Discovered works: {len(data['papers'])}; repositories: {len(data['repositories'])}; run records: {len(data['runs'])}"]
    for label, things, func in (("Paper stages", data["papers"], derived_paper_stage), ("Code stages", data["repositories"], derived_code_stage),("Run stages", data["runs"], derived_run_stage)):
        counts=Counter(func(x) for x in things if isinstance(x,dict))
        lines.append(f"{label}: " + (", ".join(f"{k}={v}" for k,v in sorted(counts.items())) if counts else "none"))
    if not data['researcher'].get('identity_confirmed'):
        lines.append("WARNING: Scholar identity has not been verified.")
    lines.append("NOTE: Syntactic evidence validation cannot certify genuine reading, code comprehension or run outcomes.")
    return "\n".join(lines)


def main(argv=None):
    ap=argparse.ArgumentParser(description="Honest research evidence ledger helper")
    subs=ap.add_subparsers(dest="cmd",required=True)
    i=subs.add_parser("init");i.add_argument("--name",required=True);i.add_argument("--slug",required=True);i.add_argument("--output",required=True)
    for cmd in ("validate","report"):
        s=subs.add_parser(cmd);s.add_argument("workspace")
    args=ap.parse_args(argv)
    if args.cmd=="init":
        path=Path(args.output)
        if path.exists():
            ap.error(f"Will not overwrite existing file: {path}")
        try:d=fresh(args.name,args.slug)
        except ValueError as e: ap.error(str(e))
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"Created empty, unverified evidence workspace: {path}")
        return 0
    data=json.loads(Path(args.workspace).read_text(encoding="utf-8"))
    errors=validate(data)
    if args.cmd=="report":
        print(report(data));return 2 if errors else 0
    if errors:
        for err in errors:print("ERROR:",err,file=sys.stderr)
        return 2
    print("Evidence ledger consistency checks passed (NOT scientific verification).")
    return 0

if __name__=="__main__":
    sys.exit(main())
