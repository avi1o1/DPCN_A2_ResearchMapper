"""Merge a reviewed recon draft into scripts/institutes_other.py and its test cases into scripts/test_affil_cases_other.tsv
(PROCESS_OTHER.md §3). Run only after check_draft.py passed and the operator read the rules; operator changes are made in the
draft file first and recorded in the notebook. The draft's helper definitions (everything before `DRAFT = {`) go just
above `EXT = {`, its entry at the end of EXT; test reasons get the notebook section appended.
usage: python3 merge_draft.py <key> <section>      e.g. python3 merge_draft.py csir_cftri 3.4"""
import os, sys

A = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(os.path.dirname(A), "scripts")
WORK = "C:/Users/varun/rm_v2_work/registry_drafts"
key, sec = sys.argv[1], sys.argv[2]

src = open(f"{WORK}/{key}.py", encoding="utf-8").read()
fn = os.path.join(S, "institutes_other.py")
reg = open(fn, encoding="utf-8").read()
if f'"{key}": dict(' in reg:
    sys.exit(f"{key} is already registered")
helpers = src[:src.index("DRAFT = {")].rstrip() + "\n"
body = src[src.index("DRAFT = {") + len("DRAFT = {"):src.rindex("}")].strip("\n")
body = "\n".join(("    " + l if l.strip() else l) for l in body.splitlines())   # DRAFT entries are indented one level less
body = f"    # ------------------------------------------------------------------ {key} (PROCESS_OTHER.md §{sec})\n" + body
reg = reg.replace("\nEXT = {", "\n" + helpers + "\n\nEXT = {", 1)
reg = reg[:reg.rindex("}")].rstrip("\n") + "\n" + body.rstrip() + "\n}\n"
open(fn, "w", encoding="utf-8").write(reg)

rows = [l for l in open(f"{WORK}/{key}_tests.tsv", encoding="utf-8").read().splitlines()[1:] if l.strip()]
with open(os.path.join(S, "test_affil_cases_other.tsv"), "a", encoding="utf-8") as f:
    f.write("\n".join(r + f" (§{sec} {key.split('_', 1)[1].upper()})" for r in rows) + "\n")
print(f"{key}: entry merged, {len(rows)} test cases added")
