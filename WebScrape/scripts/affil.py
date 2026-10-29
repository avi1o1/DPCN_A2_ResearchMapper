"""Affiliation-string classifier (v2).  classify(inst, s) -> 'iit' | 'other' | 'uncertain' | None
None  = the string does not place anyone at this institute's location at all.
Institute facts (tokens, unit names, other organisations) live in institutes.py. Manual decisions for strings the rules
leave 'uncertain' live in WebScrape/affil_manual/<inst>.tsv (string<TAB>iit|other, committed; in v1 they were kept
in the git-ignored logs/ directory and were lost) and override the rules. Rules and their history: PROCESS.md §3.2, §15.4.

v2 changes (PROCESS.md §15.4): an author's affiliations are judged one at a time (units split on ' | ' and ';'), and an
IIT mention counts only together with this institute's place token in the same unit and with no other IIT named there.
In v1 "IIT + city anywhere in the author's joined affiliations" was decisive, which is safe in Kharagpur or Rupnagar
but not in Delhi, Mumbai or Chennai.
"""
import re, os, csv, html
from common import ROOT
from institutes import REG, NON_IIT, rx

WS = re.compile(r"\s+")
# fuzzy "Indian Institute of Technology" (covers Institue/Institite/Instituteof/Inst./missing 'of'); unchanged from v1
IIT = re.compile(r"indi\w*\s*ins\w*\.?\s*(of\s*)?(te[ch]\w*|ropar|rupnagar|kharagpur|roorkee)|indian\s+intitute\s+of\s+tech|\biit\b|(?<!i\.)(?<!i\.\s)\bi\s*\.\s*i\s*\.\s*t\b|iit\s*-?\s*(rpr|ropar|kgp|kharagpur)"
                 r"|iitkgp|iitrpr|indian\s+institute\s+technology|indi\s*\|\s*an\s+institute|[it]nstitute of technology,?\s*(\(iit\)\s*)?(kharagpur|ropar|rupnagar)"
                 r"|\biit\d|e\s*(&|&amp;|&#x0026;)\s*eceiit|@iitrpr\.ac\.in|@iitkgp\.ac\.in|iitkgp\.ac\.in|iitrpr\.ac\.in", re.I)
NON_IIT_RX = re.compile(NON_IIT, re.I)
# e-mail addresses show where someone was, not the affiliation on the paper: they place a string in scope (anchors) but
# are removed before unit-name / IIT-name matching (v2; v1 counted "@iitkgp.ac.in" as an IIT mention)
EMAIL = re.compile(r"\S+@\S+")
# addresses abroad: the department-only rule and the 'uncertain' fallback never apply (a 6-digit PIN can be a P.O. box or a
# foreign postcode: "Yale School of Medicine, P.O. Box 208016, New Haven")
FOREIGN = re.compile(r"\b(usa|u\.s\.a\.?|united states|united kingdom|uk|canada|australia|germany|france|italy|spain|japan|"
                     r"korea|taiwan|singapore|israel|netherlands|sweden|switzerland|p\.?\s*o\.?\s*box|new haven)\b", re.I)
EXPL_PREFIX = r"(?:indi\w*\s*ins\w*\.?\s*(?:of\s*)?te[ch]\w*|\biit|(?<!i\.)(?<!i\.\s)\bi\s*\.\s*i\s*\.\s*t\.?)\s*(?:\(\s*iit\s*\))?\s*[,\-\u2013:]?\s*\(?\s*"
# "discipline" added in v2 (IIT Indore / Gandhinagar / Jodhpur name their units "Discipline of ...")
DEPT = re.compile(r"\b(department|dept\.?|school|centre|center|coe\w*|discipline)\b", re.I)
ORGWORD = re.compile(r"universit|college|institute of science|institute of biomedical|corporate|hospital|ltd|pvt|inc\b|gmbh|abb\b", re.I)


class _C:
    """Compiled regexes of one institute."""
    def __init__(self, k, c):
        self.anchor, self.city, self.shared = rx(c["anchor"]), rx(c.get("city")), rx(c.get("shared"))
        self.units, self.state, self.other = rx(c["units"]), rx(c.get("state")), rx(c["other"])
        self.place = rx("|".join(f"(?:{p})" for p in (c["anchor"], c.get("city"), c.get("shared"), c["units"]) if p))
        self.local = rx("|".join(f"(?:{p})" for p in (c["anchor"], c.get("city"), c["units"]) if p))
        # "Indian Institute of Technology Kharagpur", "IIT (BHU)", "I.I.T., Delhi" ... : the IIT named explicitly
        # institution-type fields (optional; the defaults are the IIT behaviour). Other institution types (IIITs, NITs,
        # universities, labs) set: mention = how the type is named ("International Institute of Information Technology"),
        # explicit_full = a complete explicit-name regex, confusable = look-alike names of other organisations, family =
        # the group within which "another institute is named" is checked (institutes of one family share city tokens)
        self.family = c.get("family", "iit")
        self.mention = rx(c["mention"]) if c.get("mention") else IIT
        self.confusable = rx(c["confusable"]) if c.get("confusable") else NON_IIT_RX
        self.explicit = rx(c["explicit_full"]) if c.get("explicit_full") else \
            re.compile(r"(?:" + EXPL_PREFIX + r"|indian\s+institute\s+of\s+)(?:" + c["explicit"] + r")\b", re.I)
        self.exclude = rx(c.get("exclude"))
        self.name_parts = re.compile(r"^(?:" + c["name_parts"] + r")$", re.I) if c.get("name_parts") else None
        self.ambiguous_depts = rx(c.get("ambiguous_depts"))
        self.abbr = rx(c.get("abbr"))


C = {k: _C(k, c) for k, c in REG.items()}
_manual = {}


def manual(inst):
    if inst not in _manual:
        m = {}
        fn = os.path.join(ROOT, "affil_manual", f"{inst}.tsv")
        if os.path.exists(fn):
            for row in csv.reader(open(fn, encoding="utf-8"), delimiter="\t"):
                if len(row) >= 2 and not row[0].startswith("#"):
                    m[norm(row[0])] = row[1]
        _manual[inst] = m
    return _manual[inst]


def norm(s):
    return WS.sub(" ", s or "").strip()


def names_other_iit(inst, s):
    """True if s names the place or a unique unit of ANOTHER IIT (or an 'Indian Institute of' that is not an IIT)."""
    me = C[inst]
    if me.confusable.search(s):
        return True
    for k, c in C.items():
        if k != inst and c.family == me.family and c.place.search(s):
            # tokens shared by two institutes' configs (none at present) would need excluding here
            return True
    return False


def explicit_other(inst, s):
    return any(c.explicit.search(s) for k, c in C.items() if k != inst)


def bare_mention(inst, s):
    """The institution type is mentioned but no institute of that family is placed: ambiguous, never a contradiction."""
    me = C[inst]
    return bool(me.mention.search(s)) and not any(c.place.search(s) for c in C.values() if c.family == me.family)


def any_iit_place(s):
    return any(c.place.search(s) for c in C.values())


PRI = {"iit": 3, "uncertain": 2, "other": 1, None: 0}


def _unit(inst, s):
    c = C[inst]
    in_local = c.local.search(s)
    s_raw, s = s, EMAIL.sub(" ", s)
    in_shared = c.shared.search(s) if c.shared else None
    if not in_local and not in_shared:
        # state rule: an IIT mention + the state, no other IIT (or non-IIT 'Indian Institute of') named -> this IIT
        if c.state and c.mention.search(s) and c.state.search(s) and not names_other_iit(inst, s):
            return "iit"
        return None
    m = manual(inst).get(s)
    if m:
        return m
    if c.exclude and c.exclude.search(s):
        return "other"
    if c.explicit.search(s) or c.units.search(s):
        return "iit"
    # a four-letter abbreviation (IITD, IITK ...) is decisive only when nothing else is named in this part: "Institute of
    # International Trade and Development (IITD), University of Port Harcourt"; otherwise it is just an IIT mention
    abbr = bool(c.abbr and c.abbr.search(s))
    if abbr and not (ORGWORD.search(s) or c.other.search(s) or FOREIGN.search(s) or names_other_iit(inst, s)):
        return "iit"
    if explicit_other(inst, s):
        # another IIT is named explicitly and this one is not. Our token is then the address of another organisation
        # ('other'), or a bare PIN / e-mail typo (also 'other'); if our place NAME also appears the string is garbled
        # ("IIT Roorkee, Kharagpur, West Bengal 721302") -> 'uncertain'
        if not in_local:
            return None
        if c.other.search(s):
            return "other"
        named = any(re.search(r"[a-z]", m.group(0), re.I) and "." not in m.group(0) for m in c.local.finditer(s))
        return "uncertain" if named else "other"
    if c.mention.search(s) or abbr:
        # an IIT mention plus this institute's place in the same unit is decisive, unless another IIT is named too
        return "uncertain" if names_other_iit(inst, s) else "iit"
    if not in_local:
        return None          # only a big-city token, no IIT mention: about some other organisation of that city
    if c.other.search(s):
        return "other"
    if c.ambiguous_depts is not None and not c.ambiguous_depts.search(s):
        return "other"       # IIT (BHU): a BHU string without an IIT mention is the university unless the department exists at both
    # department/school/centre + campus anchor (PIN, campus locality), no other organisation -> this IIT
    if FOREIGN.search(s):
        return None          # an address abroad that happens to contain our PIN / token
    if c.anchor and c.anchor.search(s_raw) and DEPT.search(s) and not ORGWORD.search(s):
        return "iit"
    return "uncertain"


SEPS = (" | ", ";")   # author's separate affiliation entries (joined by the pipeline), then ';' inside one entry


def _judge(inst, s, level=0):
    """Judge each part on its own; the whole may only rescue an 'iit' verdict, because publishers often deposit ONE
    address as several parts ('Department of Chemistry | Indian Institute of Technology | Ropar | India'). The rescue is
    refused (-> 'uncertain') when any part names another IIT or another organisation. Parts are split hierarchically:
    first the separate affiliation entries (' | '), then ';' inside an entry."""
    parts = [p for p in (norm(x) for x in s.split(SEPS[level])) if p] if level < len(SEPS) else [s]
    if len(parts) <= 1:
        return _judge(inst, s, level + 1) if level + 1 < len(SEPS) else _unit(inst, s)
    kp = [_judge(inst, p, level + 1) if level + 1 < len(SEPS) else _unit(inst, p) for p in parts]
    if "iit" in kp:
        return "iit"
    best = max(kp, key=PRI.get)
    kw = _unit(inst, s)
    if kw == "iit":
        c = C[inst]
        if any(not (c.name_parts and c.name_parts.match(p)) and
               (names_other_iit(inst, p) or explicit_other(inst, p) or c.other.search(p) or ORGWORD.search(p)
                or (c.exclude and c.exclude.search(p))) for p in parts):
            return "uncertain"
        return "iit"
    if kw == "other" and best == "uncertain":
        return "other"   # e.g. 'Ahalia School of Pharmacy | Palakkad-678557': the bare location part is not evidence
    return kw if best is None else best


def classify(inst, s):
    s = norm(s)
    if not s:
        return None
    m = manual(inst).get(s)
    if m:
        return m
    return _judge(inst, norm(html.unescape(s)))
