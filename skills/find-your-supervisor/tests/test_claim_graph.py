import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('graph',ROOT/'scripts'/'claim_graph.py')
graph=importlib.util.module_from_spec(spec);spec.loader.exec_module(graph)

class ClaimGraphTest(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'assets'/'claim-graph.example.json').read_text())
    def test_example_valid(self):self.assertEqual([],graph.validate(self.data))
    def test_duplicate_id(self):
        self.data['claims'].append(dict(self.data['claims'][0]))
        self.assertTrue(any('duplicate' in x for x in graph.validate(self.data)))
    def test_dangling_source(self):
        self.data['claims'][0]['source_ids']=['missing']
        self.assertTrue(any('unknown source' in x for x in graph.validate(self.data)))
    def test_run_requires_log(self):
        self.data['experiments'][0]['status']='run'
        self.assertTrue(any('run without' in x for x in graph.validate(self.data)))
    def test_false_supported_without_reference(self):
        self.data['claims'][0]['status']='supported'; self.data['claims'][0]['source_ids']=[]
        self.assertTrue(any('supported without' in x for x in graph.validate(self.data)))
    def test_figure_cannot_invent_experiment(self):
        self.data['figures'][0]['experiment_ids']=['not-there']
        self.assertTrue(any('unknown experiment_ids' in x for x in graph.validate(self.data)))
    def test_report_flags_untested(self):
        self.data['experiments']=[]
        self.assertIn("['c1']",graph.report(self.data))

if __name__=='__main__':unittest.main()
