"""Second-pass precision audit (PROCESS_OTHER.md §2.9) for rows the agent audit left `unknown` (no affiliation visible:
Crossref / Europe PMC empty, publisher bot-blocked, no OA copy). OpenAlex keeps the raw affiliation strings it extracted
from the publisher's landing page / PDF (`authorships[].raw_affiliation_strings`); OpenAlex is not one of the pipeline's
harvest channels, so this stays independent of what is being audited. Verdict per row:
  yes     - a raw string is classified as this institution (affil.classify == 'iit')
  no      - raw strings present for every author, none classified as this institution
  unknown - no raw strings (or some authors without strings and none ours)
The API key is read from OPENALEX_KEY_FILE (outside the repository) and never printed.
usage: OPENALEX_KEY_FILE=... python3 audit_openalex.py <inst>  -> golden/precision_audit_<inst>_openalex.csv"""
import csv, json, os, sys, time, urllib.parse, urllib.request
from affil import classify

inst = sys.argv[1]
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key = open(os.environ["OPENALEX_KEY_FILE"], encoding="utf-8").read().strip()
src = os.path.join(WS, "golden", f"precision_audit_{inst}.csv")
rows = list(csv.DictReader(open(src, encoding="utf-8")))
out = []
for r in rows:
    if r["verdict"] != "unknown":
        continue
    doi = r["doi"].replace("https://doi.org/", "").strip()
    url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi) + "?" + urllib.parse.urlencode(
        {"api_key": key, "mailto": os.environ.get("RM_MAILTO", ""), "select": "id,doi,title,authorships"})
    try:
        w = json.load(urllib.request.urlopen(url, timeout=60))
    except Exception as e:
        out.append({**r, "oa_verdict": "unknown", "oa_evidence": "", "oa_notes": f"OpenAlex lookup failed ({type(e).__name__})"})
        continue
    finally:
        time.sleep(0.2)
    au = w.get("authorships") or []
    strings = [(a.get("author", {}).get("display_name", ""), s) for a in au for s in (a.get("raw_affiliation_strings") or [])]
    ours = [(n, s) for n, s in strings if classify(inst, s) == "iit"]
    with_str = sum(1 for a in au if a.get("raw_affiliation_strings"))
    if ours:
        v, ev = "yes", f"{ours[0][0]}: {ours[0][1]}"
    elif au and with_str == len(au):
        v, ev = "no", "; ".join(sorted({s for _, s in strings}))[:300]
    else:
        v, ev = "unknown", f"{with_str} of {len(au)} authors have raw affiliation strings, none ours"
    out.append({**r, "oa_verdict": v, "oa_evidence": ev[:300], "oa_notes": f"OpenAlex {w.get('id', '')}"})
fn = os.path.join(WS, "golden", f"precision_audit_{inst}_openalex.csv")
with open(fn, "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    wr.writeheader()
    wr.writerows(out)
from collections import Counter
print(inst, "second pass on", len(out), "unknown rows:", Counter((o["tier"], o["oa_verdict"]) for o in out))
for o in out:
    if o["oa_verdict"] == "no":
        print("  NO ", o["doi"], "|", o["title"][:60], "|", o["oa_evidence"][:160])
