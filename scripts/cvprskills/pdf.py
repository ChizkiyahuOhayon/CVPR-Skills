"""Read a compiled PDF when the LaTeX source is not available.

A PDF is a worse source than `.tex` and this module does not pretend
otherwise.  What survives extraction reliably:

  prose            after line numbers, headers and reference lists are removed
  section headings from numbered-heading patterns
  the abstract     from the heading to the next one
  captions         "Figure 3: ..." and "Table 2: ..." are literal in the text

What does not survive, and is therefore not reported:

  float placement  `[t]` vs `[h]` is gone
  full-width vs single-column floats
  \\cite call sites   the text has "[12]" or "(Smith et al., 2024)", and
                   distinguishing a citation from a bracketed number is
                   guesswork
  equation count   display maths extracts as broken prose

`Paper.source_kind` is ``"pdf"`` so the auditor can suppress the checks that
would otherwise be measuring extraction artefacts.
"""

import re

from .tex import Paper, normalise_section

# ICLR/NeurIPS review builds print a line number in the margin of every line;
# they extract as runs of zero-padded integers and would otherwise dominate
# the word count.
LINE_NUMBERS = re.compile(r"(?:^|\s)(?:\d{3}\s+){3,}")
PAGE_FURNITURE = re.compile(
    r"^\s*(?:Under review as a conference paper at .*|Anonymous submission|"
    r"Anonymous Author.*|Paper ID \d+|\d+|Preprint\.?|Published as a conference "
    r"paper at .*)\s*$", re.M | re.I)

HEADING = re.compile(
    r"^\s*(?:(\d+(?:\.\d+)*)\s+)?"
    r"([A-Z][A-Za-z][^\n]{2,60})\s*$", re.M)

# A caption *start*.  The extent is computed separately: a single regex with a
# lookahead for the end fails outright whenever the caption runs past the
# bound without hitting a terminator, which is the common case in a
# two-column extraction where captions and body text interleave.
CAPTION_START = re.compile(r"\b(Figure|Fig\.|Table)\s*(\d+)\s*[:.]\s*")
CAPTION_MAX = 600

# Section names that mark the end of the body.
TAIL = re.compile(r"^\s*(references|bibliography|acknowledge?ments?|appendix|"
                  r"supplementary material)\b", re.I | re.M)


def extract_text(path):
    """Page text, in reading order, or None if no extractor is available."""
    try:
        import fitz
    except ImportError:
        return _pdftotext(path)
    try:
        doc = fitz.open(path)
    except Exception:
        return None
    parts = []
    for page in doc:
        parts.append(page.get_text("text"))
    doc.close()
    return "\n".join(parts)


def extract_lines(path):
    """[(text, size, bold, page)] per line, or None.

    Font size is the only reliable way to find headings in a compiled paper:
    a section title is set larger and bolder than the body, and no text
    pattern survives two-column extraction as cleanly.  Falls back to None
    when PyMuPDF is unavailable, and the caller then works from plain text.
    """
    try:
        import fitz
    except ImportError:
        return None
    try:
        doc = fitz.open(path)
    except Exception:
        return None
    out = []
    for pno, page in enumerate(doc):
        try:
            blocks = page.get_text("dict")["blocks"]
        except Exception:
            continue
        for b in blocks:
            if b.get("type") == 1:
                continue
            for line in b.get("lines", []):
                spans = [sp for sp in line.get("spans", []) if sp.get("text", "").strip()]
                if not spans:
                    continue
                text = "".join(sp["text"] for sp in spans).strip()
                big = max(spans, key=lambda sp: len(sp["text"]))
                out.append((text, round(big.get("size", 0), 1),
                            "bold" in big.get("font", "").lower(), pno))
    doc.close()
    return out


def body_size(lines):
    """The modal font size, weighted by characters -- that is the body text."""
    import collections
    c = collections.Counter()
    for text, size, _, _pno in lines:
        c[size] += len(text)
    return c.most_common(1)[0][0] if c else 10.0


def _pdftotext(path):
    import shutil
    import subprocess
    exe = shutil.which("pdftotext")
    if not exe:
        return None
    try:
        r = subprocess.run([exe, "-layout", path, "-"],
                           capture_output=True, text=True, timeout=120)
        return r.stdout or None
    except Exception:
        return None


def clean(text):
    text = LINE_NUMBERS.sub(" ", text)
    text = PAGE_FURNITURE.sub("", text)
    # de-hyphenate across line breaks
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def split_body(text):
    """Return (body, tail) split at the reference list."""
    m = TAIL.search(text, pos=len(text) // 3)
    return (text[:m.start()], text[m.start():]) if m else (text, "")


class PdfPaper(Paper):
    """A Paper reconstructed from extracted text.

    Subclasses Paper so the auditor needs no special case beyond checking
    ``source_kind``.
    """

    source_kind = "pdf"

    def __init__(self, path, text, lines=None):
        self.path = path
        self.raw = text
        self.cls = None
        self.doc = text
        body, tail = split_body(text)

        self.abstract = self._abstract(body)
        self.sections = []
        self.top_sections = self._sections_from_lines(lines or [])

        self.figures, self.tables = self._floats(text)
        self.equations = 0
        # "[12]", "[3, 7]", "(Smith et al., 2024)" -- count reference-list
        # entries instead, which is the number a reader means anyway.
        self.references = self._reference_count(tail)
        self.cites = self.references
        self.body = self._prose(body)

    # ------------------------------------------------------------------
    def _abstract(self, body):
        m = re.search(r"\bA\s?B\s?S\s?T\s?R\s?A\s?C\s?T\b|\bAbstract\b", body)
        if not m:
            return ""
        rest = body[m.end():]
        stop = re.search(r"\n\s*(?:\d+\s+)?(?:I\s?N\s?T\s?R\s?O|Introduction|"
                         r"1[.\s]+Introduction)\b", rest, re.I)
        chunk = rest[:stop.start()] if stop else rest[:2500]
        return re.sub(r"\s+", " ", chunk).strip()

    def _sections_from_lines(self, lines):
        """Headings are a *size tier*, not a text pattern.

        A compiled paper has three tiers above the body: the title (one or two
        lines), the section headings (typically 5-15 lines), and sometimes
        subsections. Picking the tier by how many lines are in it is far more
        robust than matching text, and it avoids the trap that catches every
        naive extractor -- bold run-in paragraph leads ("Metrics.") are bold at
        *body* size and are not headings.
        """
        if not lines:
            return []
        base = body_size(lines)
        cand = {}
        for text, size, bold, pno in lines:
            t = text.strip()
            if not (3 <= len(t) <= 70) or len(t.split()) > 9:
                continue
            if t.endswith((".", ",", ";", ":")) and not re.match(r"^\d", t):
                continue          # run-in lead, not a heading
            if re.match(r"^\s*(figure|fig\.|table|algorithm|equation)\b", t, re.I):
                continue
            if re.match(r"^\s*(anonymous|under review|published as|preprint|"
                        r"abstract)\b", t, re.I):
                continue
            if not t[:1].isalnum():
                continue
            key = (size, bold)
            cand.setdefault(key, []).append((t, pno))

        # Any tier whose size differs from the body, largest first.  Headings
        # are not always *larger*: ICLR sets them in small caps at 9.6 pt
        # against a 10 pt body, so a "bigger than body" rule finds nothing.
        tiers = sorted((k for k in cand if abs(k[0] - base) > 0.2),
                       key=lambda k: -k[0])
        # Bold-at-body-size is a legitimate heading style too (LNCS, ACM).
        tiers += [k for k in cand if abs(k[0] - base) <= 0.2 and k[1]]

        # A heading tier spans the document; a title block sits on page 1 and
        # can otherwise look identical -- five lines of large bold text.
        def looks_like_headings(rows):
            """Short, mostly-alphabetic lines with few digits."""
            if not rows:
                return 0.0
            good = sum(1 for t, _ in rows
                       if len(t.split()) <= 6
                       and sum(ch.isdigit() for ch in t) <= 2
                       and sum(ch.isalpha() for ch in t) >= 3)
            return good / float(len(rows))

        chosen, best = None, 0.0
        for k in tiers:
            rows = cand[k]
            pages = {pno for _, pno in rows}
            if not (4 <= len(rows) <= 30 and len(pages) >= 2):
                continue
            score = looks_like_headings(rows)
            if score > best:
                chosen, best = k, score
        if best < 0.5:
            chosen = chosen if best >= 0.35 else None
        if chosen is None:
            for k in tiers:
                if len({pno for _, pno in cand[k]}) >= 2:
                    chosen = k
                    break
        if chosen is None:
            return []

        out = []
        for t, _pno in cand[chosen]:
            t = re.sub(r"^\s*\d+(?:\.\d+)*\s*[.)]?\s*", "", t).strip()
            if len(t) < 3:
                continue
            name = normalise_section(t)
            if name not in out:
                out.append(name)
        return out

    def _floats(self, text):
        """Captions, from "Figure 3: ..." markers in the extracted text.

        The extent of a caption cannot be recovered exactly from a PDF -- it
        ends where the layout says it does, not where the text stream does --
        so the word counts here are approximate and the auditor treats them as
        indicative rather than measured.
        """
        figs, tabs = [], []
        starts = [(m.start(), m.end(), m.group(1), m.group(2))
                  for m in CAPTION_START.finditer(text)]
        for i, (st, en, kind, num) in enumerate(starts):
            stop = len(text)
            if i + 1 < len(starts):
                stop = starts[i + 1][0]
            para = text.find("\n\n", en)
            if para != -1:
                stop = min(stop, para)
            stop = min(stop, en + CAPTION_MAX)
            cap = re.sub(r"\s+", " ", text[en:stop]).strip()
            rec = {"star": None, "opts": None, "pos": st / max(len(text), 1),
                   "section": None, "caption_words": len(cap.split()),
                   "graphics": [], "tikz": False, "booktabs": None,
                   "label": "%s %s" % (kind.rstrip("."), num)}
            (tabs if kind.lower().startswith("table") else figs).append(rec)
        # A caption printed once per float; de-duplicate by number.
        def dedup(rows):
            seen, out = set(), []
            for r in rows:
                if r["label"] in seen:
                    continue
                seen.add(r["label"])
                out.append(r)
            return out
        return dedup(figs), dedup(tabs)

    def _reference_count(self, tail):
        """Entries in the reference list.

        Three bibliography styles, in order of how unambiguous they are:
        numbered ("[12] Author..."), parenthesised year ("... (2024)."), and
        bare year ("... , 2024."), which is what ICLR's natbib default emits.
        """
        if not tail:
            return 0
        n = len(re.findall(r"^\s*\[\d+\]", tail, re.M))
        if n >= 5:
            return n
        n = len(re.findall(r"\(\d{4}[a-z]?\)", tail))
        if n >= 5:
            return n
        # Bare years, deduplicated per line so a single entry citing two years
        # is not double counted.
        n = sum(1 for ln in tail.splitlines()
                if re.search(r"\b(?:19|20)\d{2}[a-z]?\b", ln)
                and re.search(r"[A-Z][a-z]+", ln))
        # Entries usually wrap over two lines; the year appears once per entry.
        return len(re.findall(r"\b(?:19|20)\d{2}[a-z]?[.,)]", tail)) or n

    def _prose(self, body):
        text = body
        # Drop caption text so it is not counted as prose, matching the
        # LaTeX reader, which drops whole float environments.
        for st, en, _k, _n in reversed([(m.start(), m.end(), m.group(1), m.group(2))
                                        for m in CAPTION_START.finditer(text)]):
            text = text[:st] + " " + text[en + CAPTION_MAX:] \
                if len(text) > en + CAPTION_MAX else text[:st]
        text = re.sub(r"\$[^$]*\$", " MATH ", text)
        text = re.sub(r"\[\d+(?:\s*,\s*\d+)*\]", " CITE ", text)
        text = re.sub(r"\([A-Z][A-Za-z-]+(?: et al\.)?,? \d{4}[a-z]?\)", " CITE ", text)
        # Numeric tables extract as long digit runs; they are not prose.
        text = re.sub(r"(?:\b\d+\.\d+\b[\s|]*){4,}", " ", text)
        return re.sub(r"\s+", " ", text).strip()


def load(path):
    text = extract_text(path)
    if text is None:
        return None
    return PdfPaper(path, clean(text), extract_lines(path))
