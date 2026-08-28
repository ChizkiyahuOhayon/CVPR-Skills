"""Measure a draft against the corpus distribution.

Every threshold is a percentile of 45 published CVPR-class papers, not a
style opinion.  That matters most for the "AI tell" word lists that circulate
as blanket bans: measured against real papers, some of those words are
perfectly normal in this literature and banning them makes a draft read
*less* like the venue, not more.

  `leverage`  appears in 29 of 45 papers, median 2.3 per 10k words
  `utilize`   appears in 35 of 45, median 5.7
  rule of three ("A, B, and C")  appears in 42 of 45, median 9.8
  `, <verb>ing` clauses          appear in 45 of 45, median 36.6

  em dash     appears in 2 of 45
  `pivotal`   appears in 0 of 45
  `delve`     appears in 5 of 45, and in 4 of those exactly once

So the flags below are graded by how *absent* a pattern is from real papers,
and by how far above the 90th percentile a draft sits -- never by whether a
word appears at all.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.normpath(os.path.join(HERE, "..", "..", "references",
                                        "corpus", "profile.json"))

# The pattern set the corpus was measured on.  Keys match profile.json.
TELLS = {
    "delve": r"\bdelv(e|es|ing|ed)\b",
    "leverage": r"\bleverag(e|es|ing|ed)\b",
    "utilize": r"\butiliz(e|es|ing|ed|ation)\b",
    "showcase": r"\bshowcas(e|es|ing|ed)\b",
    "underscore": r"\bunderscor(e|es|ing|ed)\b",
    "pivotal": r"\bpivotal\b",
    "crucial": r"\bcrucial\b",
    "vital": r"\bvital\b",
    "realm": r"\brealm\b",
    "landscape_fig": r"\blandscape of\b",
    "tapestry": r"\btapestry\b",
    "furthermore": r"\bfurthermore\b",
    "moreover": r"\bmoreover\b",
    "additionally": r"\badditionally\b",
    "notably": r"\bnotably\b",
    "importantly": r"\bimportantly\b",
    "comprehensive": r"\bcomprehensiv(e|ely)\b",
    "robust": r"\brobust(ness)?\b",
    "seamless": r"\bseamless(ly)?\b",
    "cutting_edge": r"\bcutting[- ]edge\b",
    "state_of_the_art": r"\bstate[- ]of[- ]the[- ]art\b|\bSOTA\b",
    "novel": r"\bnovel\b",
    "innovative": r"\binnovative\b",
    "paradigm": r"\bparadigm\b",
    "holistic": r"\bholistic\b",
    "nuanced": r"\bnuanced\b",
    "intricate": r"\bintricate\b",
    "meticulous": r"\bmeticulous(ly)?\b",
    "significantly": r"\bsignificantly\b",
    "substantially": r"\bsubstantially\b",
    "remarkably": r"\bremarkably\b",
    "in_conclusion": r"\bin conclusion\b",
    "it_is_worth_noting": r"\bit is worth noting\b",
    "plays_a_role": r"\bplays? an? \w+ role\b",
    "aims_to": r"\baims? to\b",
    "enables": r"\benabl(e|es|ing)\b",
    "facilitate": r"\bfacilitat(e|es|ing)\b",
    "emdash": r"—",
    "not_only_but_also": r"\bnot only\b[^.]{0,80}\bbut also\b",
    "by_ing": r",\s+\w+ing\b",
    "we_propose": r"\bwe propose\b",
    "we_introduce": r"\bwe introduce\b",
    "extensive_experiments": r"\bextensive experiments\b",
    "to_the_best_of": r"\bto the best of our knowledge\b",
    "first_time": r"\bfor the first time\b",
}
CASE_SENSITIVE = {"emdash"}

HEDGE = (r"\b(may|might|could|possibly|potentially|arguably|somewhat|relatively"
         r"|to some extent|we believe|it seems|appears to)\b")
RULE_OF_THREE = r"\b\w+, \w+,? and \w+\b"

READABLE = {
    "delve": "delve", "leverage": "leverage", "utilize": "utilize",
    "showcase": "showcase", "underscore": "underscore", "pivotal": "pivotal",
    "crucial": "crucial", "vital": "vital", "realm": "realm",
    "landscape_fig": '"the landscape of"', "tapestry": "tapestry",
    "furthermore": "Furthermore", "moreover": "Moreover",
    "additionally": "Additionally", "notably": "Notably",
    "importantly": "Importantly", "comprehensive": "comprehensive",
    "robust": "robust", "seamless": "seamless", "cutting_edge": "cutting-edge",
    "state_of_the_art": "state-of-the-art", "novel": "novel",
    "innovative": "innovative", "paradigm": "paradigm", "holistic": "holistic",
    "nuanced": "nuanced", "intricate": "intricate", "meticulous": "meticulous",
    "significantly": "significantly", "substantially": "substantially",
    "remarkably": "remarkably", "in_conclusion": '"In conclusion"',
    "it_is_worth_noting": '"It is worth noting"',
    "plays_a_role": '"plays a ... role"', "aims_to": '"aims to"',
    "enables": "enable(s)", "facilitate": "facilitate",
    "emdash": "em dash (—)", "not_only_but_also": '"not only ... but also"',
    "by_ing": 'trailing ", ...ing" clause', "we_propose": '"we propose"',
    "we_introduce": '"we introduce"',
    "extensive_experiments": '"extensive experiments"',
    "to_the_best_of": '"to the best of our knowledge"',
    "first_time": '"for the first time"',
    "rule_of_three": 'rule of three ("A, B, and C")',
    "hedge": "hedge",
}

# Below this many words, a single occurrence dominates a per-10k rate and the
# frequency comparisons say more about the draft's length than its prose.
# Absolute-absence checks stay on -- "pivotal" is wrong at any length.
RATE_MIN_WORDS = 900


def load_profile(path=None):
    with open(path or PROFILE, encoding="utf-8") as fh:
        return json.load(fh)


def count_tells(text):
    low = text.lower()
    out = {}
    for key, pat in TELLS.items():
        hay = text if key in CASE_SENSITIVE else low
        out[key] = len(re.findall(pat, hay))
    out["hedge"] = len(re.findall(HEDGE, low))
    out["rule_of_three"] = len(re.findall(RULE_OF_THREE, low))
    return out


class Finding(object):
    __slots__ = ("level", "code", "message", "detail")

    def __init__(self, level, code, message, detail=None):
        self.level = level
        self.code = code
        self.message = message
        self.detail = detail

    def __repr__(self):
        return "%-5s %-22s %s" % (self.level.upper(), self.code, self.message)


class Report(object):
    def __init__(self):
        self.rows = []

    def add(self, level, code, message, detail=None):
        self.rows.append(Finding(level, code, message, detail))

    error = lambda self, c, m, d=None: self.add("error", c, m, d)
    warn = lambda self, c, m, d=None: self.add("warn", c, m, d)
    note = lambda self, c, m, d=None: self.add("note", c, m, d)

    def counts(self):
        c = {"error": 0, "warn": 0, "note": 0}
        for r in self.rows:
            c[r.level] += 1
        return c


def _band(value, lo, hi, name, unit, rep, code, advice):
    if value is None:
        return
    if value < lo:
        rep.warn(code, "%s is %s %s; the corpus runs %s-%s. %s"
                 % (name, _n(value), unit, _n(lo), _n(hi), advice))
    elif value > hi:
        rep.warn(code, "%s is %s %s; the corpus runs %s-%s. %s"
                 % (name, _n(value), unit, _n(lo), _n(hi), advice))


def _n(v):
    return "%d" % v if abs(v - round(v)) < 0.05 else "%.1f" % v


def audit(paper, profile=None):
    """Compare a parsed Paper against the corpus profile."""
    P = profile or load_profile()
    rep = Report()
    body = paper.body
    words = len(body.split())
    if words < 300:
        rep.note("too-short", "only %d words of prose; most checks need a full "
                              "draft to mean anything" % words)

    S = P["structure"]

    # ---------------------------------------------------------- structure
    _band(len(paper.abstract.split()) or None,
          S["abstract_words"]["p25"], S["abstract_words"]["p75"],
          "abstract", "words", rep, "abstract-length",
          "A short abstract usually means the result is missing; a long one "
          "usually means the setup is being re-explained.")
    if words:
        _band(words, S["body_words"]["p25"], S["body_words"]["p75"],
              "body", "words", rep, "body-length",
              "Length here is a page-budget signal, not a quality one.")

    tops = [s for s in paper.top_sections if s not in ("Acknowledgements", "Appendix")]
    canon = S["canonical"]
    missing = [c for c in canon if c not in tops and
               not (c == "Method" and "Approach" in tops)]
    if missing:
        rep.warn("structure", "no %s section; the corpus standard is %s"
                 % (", ".join(missing), " > ".join(canon)))
    if len(tops) > 8:
        rep.note("many-sections", "%d top-level sections; corpus median is %d"
                 % (len(tops), int(S["sections"]["median"])))

    R = S.get("references") or S["cite_calls"]
    if getattr(paper, "references", paper.cites) < R["p25"]:
        rep.warn("thin-citations",
                 "%d distinct references; the corpus runs %d-%d. Related work "
                 "that is thin is the fastest reject in this literature."
                 % (getattr(paper, "references", paper.cites), R["p25"], R["p75"]))

    # ---------------------------------------------------------- sentences
    sents = paper.sentences()
    if sents:
        lens = sorted(len(s.split()) for s in sents)
        med = lens[len(lens) // 2]
        p90 = lens[int(0.9 * (len(lens) - 1))]
        _band(med, 16, 23, "median sentence", "words", rep, "sentence-length",
              "Corpus median is 19 words. Long sentences here read as "
              "unedited, not as sophisticated.")
        if p90 > 45:
            worst = max(sents, key=lambda s: len(s.split()))
            rep.warn("long-sentences",
                     "the longest tenth of sentences run past %d words; corpus "
                     "p90 is 33" % p90, worst[:160] + "...")

    # -------------------------------------------------------------- voice
    fp = 1000.0 * len(re.findall(r"\b(we|our|us)\b", body.lower())) / max(words, 1)
    V = P["voice"]["first_person_per_1k"]
    if fp < V["p25"]:
        rep.warn("impersonal",
                 "first person appears %.1f times per 1000 words; the corpus "
                 "runs %.1f-%.1f. These papers say 'we propose', not 'it is "
                 "proposed'." % (fp, V["p25"], V["p75"]))

    # -------------------------------------------------------------- tells
    got = count_tells(body)
    per10k = lambda k: 10000.0 * got[k] / max(words, 1)
    T = P["tells"]
    rates_meaningful = words >= RATE_MIN_WORDS
    for key in sorted(got):
        stat = T.get(key)
        if not stat or got[key] == 0 or key == "hedge":
            continue      # hedging has its own check below
        rate = per10k(key)
        absent = stat["papers_zero"] / float(stat["n"])
        label = READABLE.get(key, key)
        seen_in = stat["n"] - stat["papers_zero"]
        if seen_in == 0:
            rep.error("alien-phrase",
                      "%s x%d. Not one of the %d corpus papers uses this word."
                      % (label, got[key], stat["n"]))
        elif absent >= 0.93 and rates_meaningful and rate > stat["max"] * 1.5:
            rep.error("alien-phrase",
                      "%s x%d = %.1f per 10k. Used by %d of %d corpus papers, "
                      "and never above %.1f. A reader notices this one."
                      % (label, got[key], rate, seen_in, stat["n"], stat["max"]))
        elif absent >= 0.88:
            rep.warn("rare-phrase",
                     "%s x%d (%.1f per 10k). Only %d of %d corpus papers use it "
                     "at all." % (label, got[key], rate, seen_in, stat["n"]))
        elif rates_meaningful and rate > max(stat["p90"], 1.0) * 1.6:
            rep.warn("overused",
                     "%s x%d = %.1f per 10k; corpus p90 is %.1f. Normal in this "
                     "literature, but not this often."
                     % (label, got[key], rate, stat["p90"]))

    hedge_rate = 10000.0 * got["hedge"] / max(words, 1)
    hs = T.get("hedge", {})
    if hs and rates_meaningful and hedge_rate > hs["p90"] * 1.3:
        rep.warn("defensive",
                 "%d hedges = %.1f per 10k words; corpus p90 is %.1f. Papers in "
                 "this corpus assert. Cut the hedges that guard a claim you can "
                 "actually support, and keep the ones that state real scope."
                 % (got["hedge"], hedge_rate, hs["p90"]))

    # ------------------------------------------------------------- floats
    F = P["figures"]
    nf, nt = len(paper.figures), len(paper.tables)
    if nf and nf < 3:
        rep.note("few-figures", "%d figures; corpus median is %d"
                 % (nf, F["per_paper"]["median"]))
    if nf > 12:
        rep.note("many-figures", "%d figures; corpus median is %d" % (nf, F["per_paper"]["median"]))
    caps = [f["caption_words"] for f in paper.figures if f["caption_words"]]
    for f in paper.figures:
        if f["caption_words"] and f["caption_words"] < 8:
            rep.warn("thin-caption",
                     "figure %s has a %d-word caption; corpus median is %d. A "
                     "caption should state the claim, not name the picture."
                     % (f["label"] or "?", f["caption_words"],
                        F["caption_words"]["median"]))
    tikz = [f for f in paper.figures if f["tikz"]]
    if tikz:
        rep.note("tikz",
                 "%d figure(s) drawn in TikZ. Zero of the 292 figures in the "
                 "corpus are; all are external artwork placed with "
                 "\\includegraphics. Not wrong, just unusual here." % len(tikz))
    nobooktabs = [t for t in paper.tables if not t["booktabs"]]
    if paper.tables and len(nobooktabs) > len(paper.tables) / 2:
        rep.note("table-rules",
                 "%d of %d tables do not use booktabs rules; 70%% of corpus "
                 "tables do" % (len(nobooktabs), len(paper.tables)))
    for t in paper.tables:
        if t["caption_words"] and t["caption_words"] > 60:
            rep.note("long-table-caption",
                     "table %s caption is %d words; corpus median is %d"
                     % (t["label"] or "?", t["caption_words"],
                        F["table_caption_words"]["median"]))
    return rep, {
        "words": words, "sentences": len(sents),
        "abstract_words": len(paper.abstract.split()),
        "sections": tops, "figures": nf, "tables": nt,
        "equations": paper.equations, "cites": paper.cites,
        "references": getattr(paper, "references", paper.cites),
        "first_person_per_1k": round(fp, 1),
        "hedges_per_10k": round(hedge_rate, 1),
        "median_sentence_words": (sorted(len(s.split()) for s in sents)[len(sents) // 2]
                                  if sents else 0),
    }
