"""Independent verification of agent outputs (PROCESS_OTHER.md §2.7; operator rule: no wrong or fabricated data). On top of
check_outputs.py (format), re-fetch the cited sources of a seeded random sample and confirm the content is really there:
  roster : the person's name appears on (one of) the row's source_url pages; every sampled ORCID's public employment record
           names the institution (registry `units` / explicit name) and the ORCID name matches the row name
  golden : the title appears on the row's source_url page (>= 80 % of its content words, in order not required); a printed DOI
           resolves (doi.org content negotiation) to the same title
Sources are fetched through the shared polite fetcher (cache first). Page images / image-only PDFs cannot be text-checked:
they are listed as IMAGE for a visual check by the operator.
usage: python3 verify_agent_outputs.py <inst> [--n 20] [--seed 20261027]"""
import csv, json, os, random, re, subprocess, sys, unicodedata

A = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(A)
sys.path.insert(0, os.path.join(WS, "scripts"))
from affil import C   # noqa: E402

args = sys.argv[1:]
inst = args[0]
n = int(args[args.index("--n") + 1]) if "--n" in args else 20
seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 20261027
STOP = set("a an the of and in on for with to by from at as is are via its into using based new".split())


def fetch(url, accept=None):
    """(status, text) through polite_get; PDFs converted with pdftotext; images and image-only PDFs -> ('IMAGE', '').
    A failure reported by the fetcher (DEAD:/ERR:, e.g. during a network outage) is retried once with --refresh."""
    cmd = [sys.executable, "-I", os.path.join(A, "polite_get.py"), url] + (["--accept", accept] if accept else [])
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8").stdout.strip().split("\t")
    if out and not out[0].isdigit():
        out = subprocess.run(cmd + ["--refresh"], capture_output=True, text=True, encoding="utf-8").stdout.strip().split("\t")
    if len(out) < 2 or not out[0].isdigit() or out[0] != "200":
        return out[0] if out else "ERR", ""
    path = out[1]
    if re.search(r"\.(png|jpe?g|gif|webp)(\?|$)", url, re.I):
        return "IMAGE", ""
    raw = open(path, "rb").read()
    if raw[:5] == b"%PDF-":
        t = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True).stdout.decode("utf-8", "ignore")
        pages = max(1, t.count("\f"))
        # scanned / image-only PDFs carry only a little text (covers, headers): treat as an image
        return ("200" if len(t.split()) / pages >= 80 else "IMAGE"), t
    return "200", raw.decode("utf-8", "ignore")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"<[^>]+>|&[a-z#0-9]+;", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s)


def words(s):
    return [w for w in norm(s).split() if len(w) > 2 and w not in STOP]


def title_on_page(title, text):
    w, t = words(title), set(norm(text).split())
    return bool(w) and sum(x in t for x in w) / len(w) >= 0.8


def name_on_page(name, text):
    parts = [p for p in norm(name).split() if len(p) > 1]
    t = norm(text)
    return bool(parts) and max(parts, key=len) in t and sum(p in t for p in parts) >= max(1, len(parts) - 1)


random.seed(seed)
res = {}
# ------------------------------------------------------------------ roster
fn = os.path.join(WS, "rosters", f"{inst}_faculty.csv")
if os.path.exists(fn):
    rows = list(csv.DictReader(open(fn, encoding="utf-8")))
    ok = bad = img = 0
    print(f"=== roster {inst}: {len(rows)} rows, sample {min(n, len(rows))} (seed {seed})")
    for r in random.sample(rows, min(n, len(rows))):
        urls = [u.strip() for u in r["source_url"].split(";") if u.strip()]
        verdict = "NOT FOUND"
        for u in urls[:4]:
            st, text = fetch(u)
            if st == "IMAGE":
                verdict = verdict if verdict == "FOUND" else "IMAGE"
            elif text and name_on_page(r["name"], text):
                verdict = "FOUND"; break
        ok += verdict == "FOUND"; img += verdict == "IMAGE"; bad += verdict == "NOT FOUND"
        print(f"  {verdict:9s} {r['name'][:30]:30s} {r['status']:8s} | {urls[0][:90] if urls else '(no source)'}")
    res["roster_names"] = (ok, img, bad)
    orc = [r for r in rows if r["orcid"].strip()]
    oko = bado = 0
    cx = C[inst]
    print(f"--- ORCIDs: {len(orc)} rows with an iD, sample {min(10, len(orc))}")
    for r in random.sample(orc, min(10, len(orc))):
        st, text = fetch(f"https://pub.orcid.org/v3.0/{r['orcid'].strip()}/record", accept="application/json")
        try:
            d = json.loads(text)
        except ValueError:
            print(f"  LOOKUP-FAILED {r['orcid']} ({st})"); bado += 1; continue
        nm = d.get("person", {}).get("name") or {}
        oname = " ".join(filter(None, [(nm.get("given-names") or {}).get("value"), (nm.get("family-name") or {}).get("value")]))
        orgs = [s["employment-summary"]["organization"]["name"] for g in d.get("activities-summary", {}).get("employments", {}).get("affiliation-group", [])
                for s in g.get("summaries", [])]
        emp = any(cx.units.search(o) or cx.explicit.search(o) for o in orgs)
        nm_ok = bool(set(words(oname)) & set(words(r["name"]))) or name_on_page(r["name"], oname)
        good = emp and nm_ok
        oko += good; bado += not good
        print(f"  {'OK' if good else '??':3s} {r['orcid']} roster '{r['name']}' / ORCID '{oname}' | employment: {'yes' if emp else 'NO'} {orgs[:2]}")
    res["roster_orcid"] = (oko, bado)
# ------------------------------------------------------------------ golden
fn = os.path.join(WS, "golden", f"golden_{inst}.csv")
if os.path.exists(fn):
    rows = list(csv.DictReader(open(fn, encoding="utf-8")))
    ok = bad = img = 0
    print(f"=== golden {inst}: {len(rows)} rows, sample {min(n, len(rows))} (seed {seed})")
    for r in random.sample(rows, min(n, len(rows))):
        st, text = fetch(r["source_url"].split(";")[0].strip())
        v = "IMAGE" if st == "IMAGE" else ("FOUND" if text and title_on_page(r["title"], text) else f"NOT FOUND ({st})")
        d_ok = ""
        if r["doi"].strip():
            st2, t2 = fetch("https://doi.org/" + r["doi"].strip(), accept="application/vnd.citationstyles.csl+json")
            try:
                d_ok = " doi:" + ("OK" if title_on_page(r["title"], json.loads(t2).get("title", "")) else "TITLE-DIFF")
            except ValueError:
                d_ok = f" doi:LOOKUP-FAILED({st2})"
        if v != "FOUND":
            # the cited page cannot be text-checked (image) or did not show the title: does the paper exist at all? (the
            # auditor may use Crossref; the golden-set builders may not). Title-word overlap >= 0.9 and |year| <= 1.
            st3, t3 = fetch("https://api.crossref.org/works?rows=3&query.bibliographic=" + "+".join(words(r["title"])[:20]))
            try:
                items = json.loads(t3)["message"]["items"]
            except (ValueError, KeyError):
                items = []
            ex = [it for it in items if title_on_page(r["title"], (it.get("title") or [""])[0])
                  and title_on_page((it.get("title") or [""])[0], r["title"])
                  and abs(((it.get("issued", {}).get("date-parts") or [[0]])[0][0] or 0) - int(r["year"])) <= 1]
            v += " exists:" + ("YES " + ex[0]["DOI"] if ex else ("NO" if st3 == "200" else f"LOOKUP-FAILED({st3})"))
        ok += v == "FOUND"; img += v.startswith("IMAGE") and "exists:YES" in v; bad += "exists:NO" in v or (v.startswith("NOT") and "exists:YES" not in v)
        print(f"  {v:40s}{d_ok:15s} {r['confidence']:6s} {r['year']} | {r['title'][:60]} | {r['source_url'][:60]}")
    res["golden_titles"] = (ok, img, bad)
print("\nSUMMARY", inst, {k: v for k, v in res.items()}, "(found, image, not found) / (ok, problem)")
