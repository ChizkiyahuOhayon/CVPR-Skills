"""Turn a LaTeX manuscript into prose, structure and float inventories.

The same reader that produced `references/corpus/profile.json` from 46
published papers, so a draft is measured on exactly the terms the corpus was
measured on.  Anything else would be comparing different quantities and
calling the difference a finding.
"""

import os
import re

FLOAT_ENVS = ("figure", "table", "equation", "align", "gather", "tabular",
              "algorithm", "algorithmic", "lstlisting", "verbatim",
              "thebibliography")


def strip_comments(text):
    return re.sub(r"(?<!\\)%.*", "", text)


def inline_inputs(path, text, depth=0, seen=None):
    """Splice \\input / \\include, relative to the including file."""
    if depth > 4:
        return text
    seen = seen if seen is not None else set()
    base = os.path.dirname(path)

    def rep(m):
        name = m.group(2).strip().strip('"')
        for cand in (name, name + ".tex"):
            p = os.path.normpath(os.path.join(base, cand))
            if os.path.isfile(p) and p not in seen:
                seen.add(p)
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    return inline_inputs(p, strip_comments(fh.read()), depth + 1, seen)
        return ""
    return re.sub(r"\\(input|include)\s*\{([^}]*)\}", rep, text)


def find_main(paths):
    """The file with \\documentclass and the most sections wins."""
    cands = []
    for p in paths:
        files = []
        if os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                files += [os.path.join(root, n) for n in names if n.endswith(".tex")]
        elif p.endswith(".tex"):
            files.append(p)
        for f in files:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                t = fh.read()
            if "\\documentclass" in t:
                cands.append((f, t))
    if not cands:
        return None, None
    cands.sort(key=lambda ft: ("\\begin{document}" in ft[1], ft[1].count("\\section")),
               reverse=True)
    return cands[0]


def balanced(s, i):
    """`s[i]` is '{'; return (contents, index after the matching '}')."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{" and (j == 0 or s[j - 1] != "\\"):
            depth += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    return s[i + 1:], len(s)


def envs(body, name):
    """(start, end, inner, starred, options) for each `name` environment."""
    out = []
    pat = re.compile(r"\\(begin|end)\{" + name + r"\*?\}")
    for m in re.finditer(r"\\begin\{" + name + r"(\*?)\}(\[[^\]]*\])?", body):
        depth, i = 1, m.end()
        while True:
            mm = pat.search(body, i)
            if not mm:
                break
            if mm.group(1) == "begin":
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    out.append((m.start(), mm.end(), body[m.end():mm.start()],
                                bool(m.group(1)), (m.group(2) or "").strip("[]")))
                    break
            i = mm.end()
    return out


def caption_of(inner):
    m = re.search(r"\\caption", inner)
    if not m:
        return ""
    b = inner.find("{", m.end() - 1)
    return balanced(inner, b)[0] if b >= 0 else ""


def detex(s):
    """Prose only: floats, maths, citations and macros out."""
    for env in FLOAT_ENVS:
        s = re.sub(r"\\begin\{" + env + r"\*?\}.*?\\end\{" + env + r"\*?\}", " ", s,
                   flags=re.S)
    s = re.sub(r"\$\$.*?\$\$", " MATH ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " MATH ", s)
    s = re.sub(r"\\cite[tp]?\*?(\[[^\]]*\])*\{[^}]*\}", " CITE ", s)
    s = re.sub(r"\\(ref|cref|Cref|eqref|autoref|label)\{[^}]*\}", " REF ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}\\~^_&#]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


SECTION_RE = re.compile(r"\\(section|subsection)\*?\{((?:[^{}]|\{[^{}]*\})*)\}")


def normalise_section(title):
    t = re.sub(r"\\[a-zA-Z]+|[{}]", "", title).strip().lower()
    for key, name in [("introduct", "Introduction"), ("related", "Related Work"),
                      ("background", "Background"), ("prelimin", "Preliminaries"),
                      ("method", "Method"), ("approach", "Approach"),
                      ("experim", "Experiments"), ("evaluat", "Experiments"),
                      ("result", "Results"), ("ablation", "Ablation"),
                      ("discussion", "Discussion"), ("limitation", "Limitations"),
                      ("conclusion", "Conclusion"), ("acknowledg", "Acknowledgements"),
                      ("appendix", "Appendix"), ("supplement", "Appendix")]:
        if key in t:
            return name
    return title.strip()[:32] or "(untitled)"


class Paper(object):
    """A parsed manuscript."""

    source_kind = "tex"

    def __init__(self, path, text):
        self.path = path
        self.raw = text
        b = text.find("\\begin{document}")
        self.doc = text[b:] if b >= 0 else text
        self.documentclass = (re.search(r"\\documentclass(\[[^\]]*\])?\{([^}]*)\}", text)
                              or [None, None, None])
        self.cls = self.documentclass[2] if self.documentclass[0] else None

        m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", self.doc, re.S)
        self.abstract = detex(m.group(1)) if m else ""

        self.sections = [(mm.start(), mm.group(1), normalise_section(mm.group(2)))
                         for mm in SECTION_RE.finditer(self.doc)]
        self.top_sections = [n for _, lvl, n in self.sections if lvl == "section"]

        self.figures = []
        total = max(len(self.doc), 1)
        for st, en, inner, star, opts in envs(self.doc, "figure"):
            cap = caption_of(inner)
            self.figures.append({
                "star": star, "opts": opts, "pos": st / total,
                "section": self._section_at(st),
                "caption_words": len(cap.split()),
                "graphics": re.findall(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}", inner),
                "tikz": "\\begin{tikzpicture}" in inner,
                "label": (re.search(r"\\label\{([^}]*)\}", inner) or [None, None])[1],
            })
        self.tables = []
        for st, en, inner, star, opts in envs(self.doc, "table"):
            cap = caption_of(inner)
            self.tables.append({
                "star": star, "opts": opts, "pos": st / total,
                "section": self._section_at(st),
                "caption_words": len(cap.split()),
                "booktabs": "\\toprule" in inner,
                "label": (re.search(r"\\label\{([^}]*)\}", inner) or [None, None])[1],
            })
        self.body = detex(self.doc)
        self.equations = len(envs(self.doc, "equation")) + len(envs(self.doc, "align"))
        self.algorithms = len(envs(self.doc, "algorithm"))
        # Two different quantities, and the difference matters: authors write
        # \cite{a,b,c} as one call.  `cites` counts calls, `references` counts
        # distinct keys, which is what a reader means by "how many references".
        self.cites = len(re.findall(r"\\cite", self.doc))
        keys = set()
        for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])*\{([^}]*)\}", self.doc):
            keys.update(k.strip() for k in m.group(1).split(",") if k.strip())
        self.references = len(keys)

    def _section_at(self, pos):
        cur = "(front matter)"
        for st, lvl, name in self.sections:
            if st < pos and lvl == "section":
                cur = name
            elif st >= pos:
                break
        return cur

    def section_text(self):
        """{normalised name: prose} for top-level sections, in order."""
        out = []
        tops = [(st, n) for st, lvl, n in self.sections if lvl == "section"]
        for i, (st, name) in enumerate(tops):
            end = tops[i + 1][0] if i + 1 < len(tops) else len(self.doc)
            out.append((name, detex(self.doc[st:end])))
        return out

    def sentences(self):
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(])", self.body)
                if 12 < len(s.strip()) < 800]


def load(paths):
    """Load a manuscript from .tex sources, a directory, or a compiled PDF."""
    seq = paths if isinstance(paths, (list, tuple)) else [paths]
    pdfs = [p for p in seq if p.lower().endswith(".pdf")]
    if pdfs and not any(p.lower().endswith(".tex") or os.path.isdir(p) for p in seq):
        from . import pdf as pdfmod
        return pdfmod.load(pdfs[0])
    path, text = find_main(seq)
    if path is None:
        # A directory with no .tex but a PDF in it is still readable.
        for p in seq:
            if os.path.isdir(p):
                found = sorted(f for f in os.listdir(p) if f.lower().endswith(".pdf"))
                if found:
                    from . import pdf as pdfmod
                    return pdfmod.load(os.path.join(p, found[0]))
        return None
    text = inline_inputs(path, strip_comments(text))
    return Paper(path, text)
