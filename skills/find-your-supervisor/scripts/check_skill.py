#!/usr/bin/env python3
"""Offline packaging lint for this skill; does not validate scientific claims."""
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]

def lint(root=ROOT):
    errors=[]
    skill=root/'SKILL.md'
    if not skill.exists():return ['SKILL.md missing']
    text=skill.read_text(encoding='utf-8')
    if not text.startswith('---\n'):errors.append('SKILL.md missing frontmatter')
    elif not re.search(r'^name: find-your-supervisor$',text,re.M):errors.append('frontmatter name must be find-your-supervisor')
    if not re.search(r'^description:\s*\S',text,re.M):errors.append('frontmatter description missing')
    for doc in root.rglob('*.md'):
        payload=doc.read_text(encoding='utf-8')
        for href in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',payload):
            target=href.split('#')[0].strip()
            if not target or target.startswith(('http://','https://','mailto:','#')):continue
            if not (doc.parent/target).exists():errors.append(f'{doc.relative_to(root)}: broken link {href}')
    # Python creates __pycache__ on import; packaging excludes these via .gitignore.
    return errors
if __name__=='__main__':
    problems=lint()
    for e in problems:print('ERROR',e)
    print(f'{len(problems)} packaging lint issue(s)')
    sys.exit(1 if problems else 0)
