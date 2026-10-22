import importlib.util
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('check_skill',ROOT/'scripts'/'check_skill.py')
check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)

class PackagingTest(unittest.TestCase):
    def test_no_broken_local_links(self):
        self.assertEqual([],check.lint(ROOT))
    def test_frontmatter(self):
        self.assertTrue((ROOT/'SKILL.md').read_text().startswith('---\nname: find-your-supervisor\n'))

if __name__=='__main__':unittest.main()
