"""Shared loading, definitions and chart style for the Group 3 statistics.
Which institutes, where the data is and where results go are set by environment variables. The defaults are the original
Kharagpur / Roorkee analysis (same paths, same numbers as before):
  ANALYSIS_INSTS       comma list of registry keys (iit_kharagpur,iit_roorkee,...) or a preset: 'v2' = the 14 newer IITs
                       (default: iit_kharagpur,iit_roorkee)
  ANALYSIS_PROFILE     'v2' sets the defaults of every variable below for the 14-institute run (Enrichment/out_v2 ->
                       Analysis/results_v2, figures_v2, cache_v2, offline). Any variable can still be set on its own.
  ANALYSIS_IN_DIR      folder with <inst>_enriched.json, group3_data.csv, citation_network.csv, authorship_network.csv,
                       indian_connections.csv   (default: Enrichment/out; read-only, never modified)
  ANALYSIS_OUT_DIR     tables (default: results)       ANALYSIS_FIG_DIR  charts (default: figures)
  ANALYSIS_CACHE_DIR   OpenAlex extras written by fetch_openalex_extra.py (default: cache)
  ANALYSIS_ENRICH_CACHE_DIR  Enrichment stage-A works cache read by fetch_openalex_extra.py (default: Enrichment/cache)
  ANALYSIS_OFFLINE     1 = never call OpenAlex: steps that need live data (or an OpenAlex cache that is missing) are
                       skipped and listed in <ANALYSIS_OUT_DIR>/skipped_panels.csv (default 0; 1 under profile v2)
  ANALYSIS_FIGS        0 = write tables only (default 1)
  ANALYSIS_REC_CACHE   folder for the pickled analysis-set records, a speed-up keyed by file size and mtime ('' = off;
                       default Analysis/.rec_cache, not tracked by git)
Relative paths are taken relative to Analysis/.
Inputs (read-only): the enriched datasets + network files built by Enrichment/scripts.
Analysis set = the submission set: affiliation 'verified' AND in field scope (Enrichment/scripts/scope.py; since
2026-10-12 Physical and Life Sciences only) - the same papers as group3_data.csv.
Citations = the dataset's citation count at collection date (Crossref; OpenAlex where Crossref had none);
papers whose count is unknown are left out of citation statistics (never counted as 0)."""
import os, sys, csv, json, pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                   # Analysis/
A2 = os.path.dirname(ROOT)
ENRICH = os.path.join(A2, "Enrichment")

# ---------------------------------------------------------------- institute registry
# key -> (display name as in group3_data.csv 'institution' and the network files, OpenAlex name as in the partner tables,
#         OpenAlex institution id, short label for column names, colour: fixed per institute, never by rank)
REGISTRY = {
    "iit_kharagpur": ("IIT Kharagpur", "Indian Institute of Technology Kharagpur", "I145894827", "kharagpur", "#2a78d6"),
    "iit_roorkee": ("IIT Roorkee", "Indian Institute of Technology Roorkee", "I154851008", "roorkee", "#eb6834"),
    "iit_bombay": ("IIT Bombay", "Indian Institute of Technology Bombay", "I162827531", "bombay", "#1baf7a"),
    "iit_madras": ("IIT Madras", "Indian Institute of Technology Madras", "I24676775", "madras", "#e34948"),
    "iit_kanpur": ("IIT Kanpur", "Indian Institute of Technology Kanpur", "I94234084", "kanpur", "#6250d6"),
    "iit_goa": ("IIT Goa", "Indian Institute of Technology Goa", "I4210112052", "goa", "#eda100"),
    "iit_tirupati": ("IIT Tirupati", "Indian Institute of Technology Tirupati", "I4210109292", "tirupati", "#e87ba4"),
    "iit_patna": ("IIT Patna", "Indian Institute of Technology Patna", "I132153292", "patna", "#008300"),
    "iit_palakkad": ("IIT Palakkad", "Indian Institute of Technology Palakkad", "I4210113248", "palakkad", "#0b8a9c"),
    "iit_guwahati": ("IIT Guwahati", "Indian Institute of Technology Guwahati", "I1317621060", "guwahati", "#8a5a2b"),
    "iit_hyderabad": ("IIT Hyderabad", "Indian Institute of Technology Hyderabad", "I65181880", "hyderabad", "#b44fd1"),
    "iit_bhubaneswar": ("IIT Bhubaneswar", "Indian Institute of Technology Bhubaneswar", "I99729588", "bhubaneswar", "#3b4a6b"),
    "iit_bhu": ("IIT (BHU) Varanasi", "Indian Institute of Technology BHU", "I56404289", "bhu", "#9bbf2f"),
    "iit_gandhinagar": ("IIT Gandhinagar", "Indian Institute of Technology Gandhinagar", "I27674431", "gandhinagar", "#7a7a7a"),
    "iit_indore": ("IIT Indore", "Indian Institute of Technology Indore", "I64295750", "indore", "#d4572b"),
    "iit_mandi": ("IIT Mandi", "Indian Institute of Technology Mandi", "I9579091", "mandi", "#4ea3c9"),
}
PRESETS = {
    "default": ["iit_kharagpur", "iit_roorkee"],
    "v2": ["iit_bombay", "iit_madras", "iit_kanpur", "iit_goa", "iit_tirupati", "iit_patna", "iit_palakkad", "iit_guwahati",
           "iit_hyderabad", "iit_bhubaneswar", "iit_bhu", "iit_gandhinagar", "iit_indore", "iit_mandi"],
}
PROFILE = os.environ.get("ANALYSIS_PROFILE", "").strip()
_sel = os.environ.get("ANALYSIS_INSTS", "").strip() or (PROFILE if PROFILE in PRESETS else "default")
INST_KEYS = PRESETS[_sel] if _sel in PRESETS else [k.strip() for k in _sel.split(",") if k.strip()]
for _k in INST_KEYS:
    if _k not in REGISTRY:
        raise SystemExit(f"ANALYSIS_INSTS: unknown institute '{_k}' (registry: {', '.join(REGISTRY)}; presets: {', '.join(PRESETS)})")
INSTS = {k: REGISTRY[k][0] for k in INST_KEYS}                  # key -> display name, in the order of the run
OA_NAME = {v[0]: v[1] for v in REGISTRY.values()}               # display name -> OpenAlex name (every registered institute)
OA_ID = {v[0]: v[2] for v in REGISTRY.values()}                 # display name -> OpenAlex institution id
SHORT_KEY = {v[0]: v[3] for v in REGISTRY.values()}             # display name -> lower-case label
COLOR = {v[0]: v[4] for v in REGISTRY.values()}                 # entity colours: fixed, never by rank
OWN = set(OA_NAME) | set(OA_NAME.values())                      # every registered institute under either of its names
N_INST = len(INSTS)
CLUSTER = ("Cluster (both IITs)" if N_INST == 2 else f"Cluster (all {N_INST} IITs)" if N_INST > 2
           else "Cluster (" + "".join(INSTS.values()) + ")")
ALL_LABEL = "Both" if N_INST == 2 else "All"
PAIR_LABEL = "Kharagpur-Roorkee" if N_INST == 2 else "cross-institute"   # label of ties between two institutes of the run
INST_PHRASE = "both IITs" if N_INST == 2 else f"all {N_INST} IITs"


def _path(var, default):
    v = os.environ.get(var, "").strip()
    return os.path.abspath(v if os.path.isabs(v) else os.path.join(ROOT, v)) if v else default


_v2 = PROFILE == "v2"
DATA = _path("ANALYSIS_IN_DIR", os.path.join(ENRICH, "out_v2" if _v2 else "out"))
RES = _path("ANALYSIS_OUT_DIR", os.path.join(ROOT, "results_v2" if _v2 else "results"))
FIG = _path("ANALYSIS_FIG_DIR", os.path.join(ROOT, "figures_v2" if _v2 else "figures"))
CACHE = _path("ANALYSIS_CACHE_DIR", os.path.join(ROOT, "cache_v2" if _v2 else "cache"))
ENRICH_CACHE = _path("ANALYSIS_ENRICH_CACHE_DIR", os.path.join(ENRICH, "cache_v2" if _v2 else "cache"))
REC_CACHE = _path("ANALYSIS_REC_CACHE", os.path.join(ROOT, ".rec_cache")) if os.environ.get("ANALYSIS_REC_CACHE", "x") != "" else ""
OFFLINE = os.environ.get("ANALYSIS_OFFLINE", "1" if _v2 else "0").strip() not in ("", "0")
FIGS = os.environ.get("ANALYSIS_FIGS", "1").strip() not in ("", "0")
for d in (RES, CACHE) + ((FIG,) if FIGS else ()):
    os.makedirs(d, exist_ok=True)
sys.path.insert(0, os.path.join(ENRICH, "scripts"))           # reuse oa.py (OpenAlex client) where needed
csv.field_size_limit(10 ** 8)

YEARS = list(range(2016, 2027))
PARTIAL_YEAR = 2026                                            # collected in October 2026

# ---------------------------------------------------------------- panels that could not be computed
SKIP_FILE = os.path.join(RES, "skipped_panels.csv")


def _clear_skips(script):
    """Drop the rows of `script` from the skipped-panels file (it is about to re-decide what it can compute)."""
    if not os.path.exists(SKIP_FILE):
        return
    with open(SKIP_FILE, encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["script"] != script]
    if rows:
        with open(SKIP_FILE, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=["script", "panel", "reason", "needs"])
            w.writeheader()
            w.writerows(rows)
    else:
        os.remove(SKIP_FILE)


_clear_skips(os.path.basename(sys.argv[0]))


def note_skip(script, panel, reason, needs=""):
    """Record (and print) a panel that was skipped because an input is missing; idempotent per (script, panel)."""
    rows = {}
    if os.path.exists(SKIP_FILE):
        with open(SKIP_FILE, encoding="utf-8-sig", newline="") as fh:
            rows = {(r["script"], r["panel"]): r for r in csv.DictReader(fh)}
    rows[(script, panel)] = {"script": script, "panel": panel, "reason": reason, "needs": needs}
    with open(SKIP_FILE, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["script", "panel", "reason", "needs"])
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda r: (r["script"], r["panel"])))
    print(f"SKIPPED [{script}] {panel}: {reason}", flush=True)


# ---------------------------------------------------------------- data
# fields of an enriched record that no statistic reads (reference lists and provenance); dropped to save memory
_DROP = ("references", "references_openalex", "evidence", "citations_by_source", "references_meta", "found_via_person",
         "todo_fields", "preprint_versions", "duplicate_dois", "filled", "cites_indian_institutions",
         "cited_by_indian_institutions", "cited_by_indian_works", "institute_affiliations_matched", "type_raw", "isbn",
         "pmid", "arxiv", "citations_source", "affiliation_openalex", "publisher")


def _parse_records(fn, analysis_set):
    out = []
    with open(fn, encoding="utf8") as fh:
        for line in fh:
            s = line.strip().rstrip(",")
            if not s.startswith('{"title"'):
                continue
            r = json.loads(s)
            if analysis_set and (r["affiliation_status"] != "verified" or r["sci_eng_scope"]["in_scope"] is not True):
                continue
            for k in _DROP:
                r.pop(k, None)
            al = r.get("authors_openalex")                      # only the name and the OpenAlex id of an author are ever read
            if isinstance(al, list):
                r["authors_openalex"] = [{"name": a.get("name"), "openalex_author": a.get("openalex_author")} for a in al]
            au = r.get("authors")                               # the scraped author list is only ever counted (n_authors)
            if isinstance(au, list):
                r["authors"] = [None] * len(au)
            out.append(r)
    return out


def load_records(inst, analysis_set=True):
    """Records of one institute (dicts as in enriched JSON); by default only the analysis (submission) set.
    Reference lists and provenance fields are dropped (no statistic reads them). The parsed list is pickled in
    REC_CACHE when that is set, keyed by the size and mtime of the JSON (a refreshed file is re-read)."""
    fn = os.path.join(DATA, inst + "_enriched.json")
    if not REC_CACHE:
        return _parse_records(fn, analysis_set)
    st = os.stat(fn)
    tag = f"{inst}_{'a' if analysis_set else 'all'}_s1_"            # s1 = the record format above
    pk = os.path.join(REC_CACHE, f"{tag}{st.st_size}_{st.st_mtime_ns}.pkl")
    if os.path.exists(pk):
        with open(pk, "rb") as fh:
            return pickle.load(fh)
    out = _parse_records(fn, analysis_set)
    os.makedirs(REC_CACHE, exist_ok=True)
    for old in os.listdir(REC_CACHE):                         # drop stale versions of this file
        if old.startswith(tag):
            os.remove(os.path.join(REC_CACHE, old))
    with open(pk + ".tmp", "wb") as fh:
        pickle.dump(out, fh, protocol=pickle.HIGHEST_PROTOCOL)
    os.replace(pk + ".tmp", pk)
    return out


def paper_key(r):
    d = r["doi"]
    if isinstance(d, str) and not d.startswith("TODO"):
        return d.lower()
    return r.get("openalex_id") or r["record_id"]


def cites(r):
    return r["citations"] if isinstance(r["citations"], int) else None


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def iter_csv(path):
    """Rows of a (large) CSV one at a time: the citation network has over a million rows."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        yield from csv.DictReader(fh)


def write_csv(name, rows, cols=None):
    path = os.path.join(RES, name)
    cols = cols or (list(rows[0].keys()) if rows else [])
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return path


def h_index(citation_counts):
    c = sorted((x for x in citation_counts if x is not None), reverse=True)
    return sum(1 for i, x in enumerate(c, 1) if x >= i)


def i10_index(citation_counts):
    """Papers with at least 10 citations (Google Scholar's i10-index), over the counts given."""
    return sum(1 for x in citation_counts if x is not None and x >= 10)


# ---------------------------------------------------------------- OpenAlex extras (fetch_openalex_extra.py)
_oa = {}
OA_KEYS = ("counts_by_year", "sources", "paper_source", "authors")


def oa_extra():
    """Caches written by fetch_openalex_extra.py: counts_by_year, sources, paper -> source, faculty authors.
    A cache file that does not exist reads as empty (see oa_have)."""
    if not _oa:
        for k in OA_KEYS:
            fn = os.path.join(CACHE, f"oa_{k}.json")
            _oa[k] = {}
            if os.path.exists(fn):
                with open(fn, encoding="utf-8") as fh:
                    _oa[k] = json.load(fh)
    return _oa


def oa_have(*keys):
    """True when every named OpenAlex cache (oa_<key>.json in CACHE) exists and has content."""
    o = oa_extra()
    return all(o[k] for k in keys)


def source_of(r):
    """OpenAlex source record of a paper's venue (name, publisher, if_2yr, ...) or None."""
    o = oa_extra()
    s = o["paper_source"].get(r.get("openalex_id") or "")
    return o["sources"].get(s) if s else None


def impact_factor(r):
    """'IF (OpenAlex)': the venue's 2-year mean citedness, for journal papers only; None if unknown."""
    if r["type"] != "journal":
        return None
    s = source_of(r)
    return s.get("if_2yr") if s else None


def n_authors(r):
    """Number of authors listed by OpenAlex (it lists at most 100, so 100 means 100 or more); else the scraped list."""
    a = r.get("authors_openalex") or r.get("authors")
    return len(a) if isinstance(a, list) and a else None


def safe_div(a, b, nd=4):
    """a / b rounded, or '' when b is 0 (an institute with no ranked papers, no faculty, ...)."""
    return round(a / b, nd) if b else ""


# ---------------------------------------------------------------- chart style (validated palette, light surface)
SURFACE = "#fcfcfb"
TEXT, TEXT2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
ORDINAL = ["#0d366b", "#1c5cab", "#3987e5", "#86b6ef"]          # dark -> light (Q1 darkest, Q4 lightest)


def style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID, "axes.labelcolor": TEXT2, "axes.titlecolor": TEXT, "axes.titlesize": 12,
        "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlepad": 10,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.8, "axes.axisbelow": True, "xtick.color": TEXT2, "ytick.color": TEXT2,
        "xtick.labelsize": 9, "ytick.labelsize": 9, "axes.labelsize": 10, "legend.frameon": False,
        "legend.fontsize": 9, "font.family": "DejaVu Sans", "lines.linewidth": 2, "figure.dpi": 110,
    })


def save(fig, name):
    path = os.path.join(FIG, name)
    if FIGS:
        fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def bar_layout(n, ratio=0.9474, total=0.76):
    """(offsets, bar width) for n grouped bars per category. n = 2 gives the original +-0.19 offsets and 0.36 width."""
    slot = total / max(n, 1)
    return [(k - (n - 1) / 2) * slot for k in range(n)], slot * ratio


def panels(n, figsize, sharey=False, ncols=4):
    """(fig, [axes]) with one panel per institute. Two institutes: the original 1 x 2 layout at `figsize`; otherwise a
    grid of ncols columns, each panel the size of one of the two originals."""
    if n <= 2:
        fig, axes = plt.subplots(1, max(n, 1), figsize=figsize, sharey=sharey, squeeze=False)
        return fig, list(axes[0])
    cols = min(ncols, n)
    rows = -(-n // cols)
    fig, axes = plt.subplots(rows, cols, figsize=(figsize[0] / 2 * cols, figsize[1] * rows), sharey=sharey, squeeze=False)
    flat = list(axes.ravel())
    for ax in flat[n:]:
        ax.set_visible(False)
    return fig, flat[:n]


SHORT = {"Academy of Scientific and Innovative Research": "AcSIR (CSIR academy)",
         "Vellore Institute of Technology University": "VIT University",
         "University of Petroleum and Energy Studies": "UPES Dehradun",
         "SRM Institute of Science and Technology": "SRM IST",
         "Council of Scientific and Industrial Research": "CSIR",
         "Birla Institute of Technology, Mesra": "BIT Mesra",
         "Indian Institute of Engineering Science and Technology, Shibpur": "IIEST Shibpur",
         "Central Building Research Institute": "CSIR-CBRI Roorkee",
         "S.N. Bose National Centre for Basic Sciences": "S.N. Bose Centre",
         "Homi Bhabha National Institute": "HBNI"}


def short_name(name, width=34):
    """Readable label for an institution: known abbreviations, then common prefixes, then an ellipsis."""
    n = SHORT.get(name, name)
    for a, b in (("Indian Institute of Technology", "IIT"), ("National Institute of Technology", "NIT"),
                 ("Indian Institute of Science Education and Research", "IISER"), ("Indian Institute of Science", "IISc"),
                 ("Indian Institute of Information Technology", "IIIT")):
        n = n.replace(a, b)
    return n if len(n) <= width else n[:width - 1].rstrip() + "…"
