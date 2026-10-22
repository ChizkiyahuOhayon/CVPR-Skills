import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "audit.py"
spec = importlib.util.spec_from_file_location("supervisor_audit", MODULE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def pages(n=3):
    return {"page_count":n, "pages_read":list(range(1,n+1)), "sha256":"0"*64,
            "page_notes":{str(i):f"Page {i} method / experimental detail" for i in range(1,n+1)}}


class AuditTest(unittest.TestCase):
    def test_empty_unverified(self):
        d=audit.fresh('Example Researcher','example-researcher')
        self.assertFalse(d['researcher']['identity_confirmed'])
        self.assertEqual([],audit.validate(d))
        self.assertIn("Discovered works: 0",audit.report(d))

    def test_slug_safety(self):
        with self.assertRaises(ValueError):audit.fresh('X','../bad')

    def test_paper_full_requires_notes(self):
        paper={"canonical_id":"p1","title":"a","year":2025,"url":"https://example.org/paper","claimed_stage":"full_main","main_pdf":{"page_count":2,"pages_read":[1,2],"sha256":"0"*64}}
        self.assertEqual('selected_pages', audit.derived_paper_stage(paper))
        d=audit.fresh('A','a');d['papers'].append(paper)
        self.assertTrue(audit.validate(d))

    def test_main_read(self):
        p={"main_pdf":pages(),"method_anchor":"p2 Eq 1", "experiment_anchor":"p3 Table 1", "limitation_anchor":"p3"}
        self.assertEqual('full_main',audit.derived_paper_stage(p))

    def test_supplement_requires_full_coverage(self):
        p={"main_pdf":pages(),"method_anchor":"p2", "experiment_anchor":"p3", "limitation_anchor":"p3", "supplement_pdf":pages(2)}
        self.assertEqual('full_with_supplement',audit.derived_paper_stage(p))
        p['supplement_pdf']['pages_read']=[1]
        self.assertEqual('full_main',audit.derived_paper_stage(p))

    def test_readme_is_not_core_code(self):
        r={"readme_checked":True}
        self.assertEqual('readme_checked',audit.derived_code_stage(r))

    def test_code_full_requires_eligible_files(self):
        r={"repo_id":"r", "commit_sha":"a"*40,"eligible_source_files":["a.py","b.py"],"reviewed_files":["a.py"],"claim_to_code":["claim->a.py:forward"]}
        self.assertEqual('core_partial',audit.derived_code_stage(r))
        r['reviewed_files'].append('b.py')
        self.assertEqual('source_audited',audit.derived_code_stage(r))

    def test_repro_requires_real_log(self):
        run={"run_id":"r","claimed_stage":"metric_replication"}
        self.assertEqual('not_run',audit.derived_run_stage(run))
        d=audit.fresh('A','a');d['runs'].append(run)
        self.assertTrue(audit.validate(d))

    def test_repro_full_evidence(self):
        run={"execution_log":"/tmp/run.log","exit_code":0,"dataset_version":"v1","environment":"torch x","hardware":"GPU x","seed":1,"commit_sha":"a"*40,"command":"python eval.py", "measured_metrics":{"iou":.5},"reference_metrics":{"iou":.5},"comparison_note":"same within margin","evaluation_type":"paper_metric"}
        self.assertEqual('metric_replication',audit.derived_run_stage(run))

    def test_duplicate_paper(self):
        d=audit.fresh('A','a')
        d['papers']=[{"canonical_id":"x","title":"a","year":2024,"url":"u"},{"canonical_id":"x","title":"b","year":2025,"url":"u"}]
        self.assertTrue(any('duplicate' in e for e in audit.validate(d)))


if __name__ == '__main__': unittest.main()
