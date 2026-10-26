"""Write the filled agent briefs for this machine.
usage: python3 fill.py <work_dir> [inst ...]      (default: every institute in the settings files)
Briefs go to WebScrape/agents/briefs/filled_<roster|golden>_<inst>.md (git-ignored); downloads and agent scripts go under
<work_dir>/<inst>_<roster|golden>/ (keep it outside the repository)."""
import os, sys, json
A = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(A))
WORK = os.path.abspath(sys.argv[1])
C = {}
for f in ("iits.json", "iiits.json", "others.json"):    # one settings file per team (iits.json = IIT team)
    if os.path.exists(os.path.join(A, f)):
        for k, v in json.load(open(os.path.join(A, f), encoding="utf-8")).items():
            assert k not in C, f"{f}: {k} already defined"
            C[k] = v
insts = sys.argv[2:] or list(C)
os.makedirs(os.path.join(A, "briefs"), exist_ok=True)
for inst in insts:
    for kind in ("roster", "golden"):
        t = open(os.path.join(A, f"{kind}_brief.md")).read()
        for k, v in C[inst].items():
            t = t.replace("{" + k + "}", v)
        t = t.replace("{INST}", inst).replace("{REPO}", REPO).replace("{WORK}", WORK).replace("{AGENTS}", A)
        open(os.path.join(A, "briefs", f"filled_{kind}_{inst}.md"), "w").write(t)
print("wrote briefs for", len(insts), "institutes to", os.path.join(A, "briefs"))
