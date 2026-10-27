"""Operator check of a recon agent's registry draft (PROCESS_OTHER.md §3) before it is merged into institutes_other.py:
  1. ROR: the draft's ror id resolves; its names, GRID id and city are printed next to the draft's name / grid
  2. test strings: every string of <key>_tests.tsv is found (whitespace-normalised) in the agent's probe output
     (rm_v2_work/scratch/probe_<lab>.txt, rm_v2_work/registry_drafts/_probe/*) or in the existing test files — strings that
     are found nowhere are listed as MISSING (made up or retyped: not accepted)
  3. rules: the draft is compiled together with the registered entries (a temporary copy of the registry, the repository is
     not changed) and its own test cases are classified; the IIT and other-team test files are re-run as a regression
usage: python3 check_draft.py <key>        (run from WebScrape/agents; RM_OUT=v2)"""
import glob, json, os, re, subprocess, sys, tempfile, urllib.request

A = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(A)
WORK = "C:/Users/varun/rm_v2_work"
key = sys.argv[1]
lab = key.split("_", 1)[1]
W = lambda x: re.sub(r"\s+", " ", x or "").strip()

src = open(f"{WORK}/registry_drafts/{key}.py", encoding="utf-8").read()
tests = [l.split("\t") for l in open(f"{WORK}/registry_drafts/{key}_tests.tsv", encoding="utf-8").read().splitlines()[1:] if l.strip()]

# 1. ROR
ror = re.search(r'ror="https://ror.org/(\w+)"', src).group(1)
grid = re.search(r'grid="([^"]+)"', src).group(1)
d = json.load(urllib.request.urlopen(f"https://api.ror.org/v2/organizations/{ror}", timeout=60))
names = [n["value"] for n in d["names"] if n.get("lang") in (None, "en")]
grids = [g for e in d["external_ids"] if e["type"] == "grid" for g in e["all"]]
print(f"ROR {ror}: {names[:3]} | grid {grids} (draft {grid}{' OK' if grid in grids else ' DIFFERENT'}) | "
      f"{d['locations'][0]['geonames_details']['name']} | status {d.get('status')}")

# 2. test strings
pool = ""
for fn in glob.glob(f"{WORK}/scratch/probe_{lab}*.txt") + glob.glob(f"{WORK}/registry_drafts/_probe/*") + \
          glob.glob(f"{WORK}/scratch/*{lab}*") + glob.glob(f"{WORK}/review/*.txt") + glob.glob(f"{WORK}/review/*.tsv") + \
          [os.path.join(WS, "scripts", "test_affil_cases_other.tsv"), os.path.join(WS, "scripts", "test_affil_cases.tsv")]:
    if os.path.isfile(fn):
        pool += W(open(fn, encoding="utf-8", errors="ignore").read()) + "\n"
missing = [t[2] for t in tests if W(t[2]) not in pool]
print(f"test strings: {len(tests)}, missing from every probe / test file: {len(missing)}")
for s in missing:
    print("  MISSING", s[:150])

# 3. rules, on a temporary copy of the registry
tmp = tempfile.mkdtemp()
for fn in glob.glob(os.path.join(WS, "scripts", "*.py")) + glob.glob(os.path.join(WS, "scripts", "*.tsv")):
    open(os.path.join(tmp, os.path.basename(fn)), "w", encoding="utf-8").write(open(fn, encoding="utf-8").read())
reg = open(os.path.join(tmp, "institutes_other.py"), encoding="utf-8").read()
body = src[src.index("DRAFT = {") + len("DRAFT = {"):src.rindex("}")]
helpers = src[:src.index("DRAFT = {")]
reg = reg.replace("\nEXT = {", "\n" + helpers + "\nEXT = {", 1)
reg = reg[:reg.rindex("}")] + body.rstrip() + "\n}\n"
open(os.path.join(tmp, "institutes_other.py"), "w", encoding="utf-8").write(reg)
with open(os.path.join(tmp, "test_affil_cases_other.tsv"), "a", encoding="utf-8") as f:
    f.write("\n".join("\t".join(t) for t in tests) + "\n")
r = subprocess.run([sys.executable, "test_affil.py"], cwd=tmp, capture_output=True, text=True, encoding="utf-8")
print("test_affil with the draft merged:", (r.stdout.strip().splitlines() or ["?"])[-1])
fails = [l for l in r.stdout.splitlines() if "FAIL" in l or "expected" in l.lower()]
for l in fails[:30]:
    print("  ", l[:220])
if r.returncode and r.stderr:
    print(r.stderr[-1500:])
# a non-zero exit stops a chained merge_draft.py
sys.exit(1 if (missing or fails or r.returncode or grid not in grids) else 0)
