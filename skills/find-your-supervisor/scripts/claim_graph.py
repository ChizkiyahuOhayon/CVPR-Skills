#!/usr/bin/env python3
"""Check claim-to-evidence references. Structural checks never verify truth.

No network or dependencies. No arbitrary code execution. Synthetic examples are not
research results. This validator only checks the *shape* of a proposed argument.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

STATUS = {"hypothesis", "supported", "refuted", "uncertain"}
EXPERIMENT_STATUS = {"planned", "run", "blocked"}
KINDS = {"paper", "appendix", "code", "log", "data", "other"}


def _ids(items, label, errors):
    values=[]
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            errors.append(f"{label}: record without nonempty id")
            continue
        values.append(item["id"])
    for key,num in Counter(values).items():
        if num > 1: errors.append(f"{label}: duplicate id {key}")
    return set(values)


def validate(d):
    errs=[]
    if not isinstance(d,dict): return ["root must be an object"]
    if d.get("schema_version") != "0.2.0": errs.append("schema_version must be 0.2.0")
    for k in ("claims","sources","experiments","figures"):
        if not isinstance(d.get(k), list):errs.append(f"{k} must be a list")
    if errs: return errs
    cs=_ids(d['claims'],'claims',errs); ss=_ids(d['sources'],'sources',errs)
    es=_ids(d['experiments'],'experiments',errs); _ids(d['figures'],'figures',errs)
    for s in d['sources']:
        if not isinstance(s,dict): continue
        if s.get('kind') not in KINDS: errs.append(f"source {s.get('id')}: unknown kind")
        if not isinstance(s.get('url'),str) or not s['url'].startswith(('https://','http://','file://')):
            errs.append(f"source {s.get('id')}: requires source URL/path")
    for c in d['claims']:
        if not isinstance(c,dict):continue
        ident=c.get('id')
        if not c.get('statement'): errs.append(f"claim {ident}: missing statement")
        if c.get('status') not in STATUS: errs.append(f"claim {ident}: invalid status")
        refs=c.get('source_ids')
        if not isinstance(refs,list): errs.append(f"claim {ident}: source_ids must be a list")
        else:
            for sid in refs:
                if sid not in ss: errs.append(f"claim {ident}: unknown source {sid}")
        if c.get('status')=='supported' and not refs:
            errs.append(f"claim {ident}: supported without a source")
    for e in d['experiments']:
        if not isinstance(e,dict):continue
        ident=e.get('id')
        if not e.get('protocol'): errs.append(f"experiment {ident}: missing protocol")
        if e.get('status') not in EXPERIMENT_STATUS: errs.append(f"experiment {ident}: invalid status")
        if not isinstance(e.get('claim_ids'),list) or not e['claim_ids']:
            errs.append(f"experiment {ident}: missing claim_ids")
        else:
            for cid in e['claim_ids']:
                if cid not in cs: errs.append(f"experiment {ident}: unknown claim {cid}")
        if e.get('status')=='run' and e.get('log_source_id') not in ss:
            errs.append(f"experiment {ident}: run without a known log source")
        if e.get('log_source_id') in ss:
            src=next((s for s in d['sources'] if isinstance(s,dict) and s.get('id')==e['log_source_id']),{})
            if src.get('kind')!='log':errs.append(f"experiment {ident}: run source is not a log")
    for f in d['figures']:
        if not isinstance(f,dict):continue
        ident=f.get('id')
        if not f.get('purpose'): errs.append(f"figure {ident}: missing purpose")
        for key,known in (('claim_ids',cs),('experiment_ids',es)):
            refs=f.get(key)
            if not isinstance(refs,list):errs.append(f"figure {ident}: {key} must be list")
            else:
                for i in refs:
                    if i not in known:errs.append(f"figure {ident}: unknown {key} reference {i}")
    return errs


def report(d):
    counts=Counter(c.get('status') for c in d.get('claims',[]) if isinstance(c,dict))
    linked={cid for e in d.get('experiments',[]) if isinstance(e,dict) for cid in e.get('claim_ids',[])}
    orphaned=[c.get('id') for c in d.get('claims',[]) if isinstance(c,dict) and c.get('id') not in linked]
    return (f"Claims: {len(d.get('claims',[]))}; sources: {len(d.get('sources',[]))}; "
            f"experiments: {len(d.get('experiments',[]))}; figures: {len(d.get('figures',[]))}\n"
            f"Claim states: {dict(sorted(counts.items()))}\n"
            f"Claims missing a linked falsification experiment: {orphaned or 'none'}\n"
            "Structural validation does NOT confirm source truth, experiments or novelty.")


def main(argv=None):
    p=argparse.ArgumentParser(description="Inspect argument-to-evidence graph structure")
    p.add_argument('action',choices=['validate','report']);p.add_argument('file')
    args=p.parse_args(argv)
    d=json.loads(Path(args.file).read_text(encoding='utf-8'))
    errs=validate(d)
    if args.action=='report':print(report(d))
    if errs:
        for e in errs:print('ERROR:',e,file=sys.stderr)
        return 2
    if args.action=='validate':print('Claim graph structure OK (not evidence verification)')
    return 0

if __name__=='__main__':sys.exit(main())
