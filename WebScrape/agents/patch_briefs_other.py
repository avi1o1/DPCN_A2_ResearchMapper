"""Adapt the filled agent briefs (briefs/filled_*_<key>.md, written by fill.py) for the other-institutes team: operator name,
type notes in the golden brief (CSIR / DAE / teaching institute), independence from the v2 outputs, and the brief issues
learned on the pilot (PROCESS_OTHER.md §2.7). Edits only our filled copies, never the shared templates.
usage: python3 patch_briefs_other.py <key> [<key> ...]"""
import os, re, sys, json

A = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(A, "others.json"), encoding="utf-8"))
for k in sys.argv[1:]:
    name = S[k]["NAME"]
    unit = "lab" if k.startswith("csir_") else ("institute" if k == "dae_niser" else "unit")
    note = ("## Notes for this institution type (other-institutes team)\n"
            f"* This brief was written for IITs: read 'this IIT' / 'IIT authors' as {name} and its scientific staff / faculty.\n"
            f"  Where the tenure rule says NIRF, use the {unit}'s annual reports (staff lists, joinings) if it is not in NIRF.\n"
            "* Students and project staff count as authors of the institution when the paper prints it. AcSIR / HBNI alone (the\n"
            "  degree-granting academies) do not identify the institution; AcSIR / HBNI + the institution's name does.\n"
            "* `evidence_source`: use `dept_page` for an institutional repository or an institute-wide publication list, and name\n"
            "  the real source in `notes` (pilot finding).\n"
            "* Image-only annual reports: you may read rendered pages; cite the page image / PDF page in `source_url`, and\n"
            "  double-check long chemical names against the publisher page when one is linked.\n"
            "* Every row must come from a page you actually fetched; titles and DOIs are copied from the source, never from memory.\n"
            "* Independence also covers the v2 outputs: never read anything under WebScrape/v2/, WebScrape/raw/ or WebScrape/logs/.\n\n")
    for kind in ("roster", "golden"):
        fn = os.path.join(A, "briefs", f"filled_{kind}_{k}.md")
        t = open(fn, encoding="utf-8").read()
        t = re.sub(r"operator\s+Aviral Gupta", "operator Varun Shastry, other-institutes team", t)
        if kind == "golden" and "Notes for this institution type" not in t:
            t = t.replace("## Decisions already taken", note + "## Decisions already taken", 1)
        open(fn, "w", encoding="utf-8").write(t)
    print(k, "briefs patched")
