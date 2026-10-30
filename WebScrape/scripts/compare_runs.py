"""Compare the old-code and new-code outputs of dry_run.sh (and the live file) for one institute: counts per tier, and a record-level
proof that only the intended records changed.
usage: python3 compare_runs.py <scratch_dir> <inst> [<live_WebScrape_dir>]"""
import sys, os, json, gzip, collections

scr, inst = sys.argv[1], sys.argv[2]
live = sys.argv[3] if len(sys.argv) > 3 else None
NEWF = {"author_count", "mega_collab", "mega_basis", "affiliation_substatus"}      # fields the new code adds
OUTF = {"record_id"}                                                              # renumbered after records leave the main file


def load(path):
    d = json.load(open(path))
    return d["summary"], d["records"]


def key(r):
    return (r["doi"] if r["doi"] != "TODO" else (str(r["title"]).lower(), r["year"]))


def tier(r):
    s = r["affiliation_status"]
    return "verified" if s == "verified" else "likely" if "unverified-likely" in s else "ambiguous" if "ambiguous" in s else "possible/other"


def counts(recs):
    return collections.Counter(tier(r) for r in recs)


so, ro = load(f"{scr}/old/WebScrape/v2/{inst}.json")
sn, rn = load(f"{scr}/new/WebScrape/v2/{inst}.json")
uo = json.load(open(f"{scr}/old/WebScrape/v2/candidates_unconfirmed_{inst}.json"))["records"]
un = json.load(open(f"{scr}/new/WebScrape/v2/candidates_unconfirmed_{inst}.json"))["records"]
print(f"== {inst}: main file (old code -> new code), same inputs")
co, cn = counts(ro), counts(rn)
for t in ("verified", "likely", "ambiguous", "possible/other"):
    print(f"   {t:15s} {co[t]:6d} -> {cn[t]:6d}   ({cn[t] - co[t]:+d})")
print(f"   {'all records':15s} {len(ro):6d} -> {len(rn):6d}   ({len(rn) - len(ro):+d})")
print(f"   {'unconfirmed file':15s} {len(uo):6d} -> {len(un):6d}   ({len(un) - len(uo):+d})")
print("   sub-tier of the likely records (new):", dict(collections.Counter(r["affiliation_substatus"] for r in rn if tier(r) == "likely")))
print("   mega_collab (new): True", sum(1 for r in rn if r["mega_collab"]), " False", sum(1 for r in rn if r["mega_collab"] is False),
      " unknown", sum(1 for r in rn if r["mega_collab"] is None), "| basis", dict(collections.Counter(r["mega_basis"] for r in rn)))

# --- record-level proof
ko, kn = {key(r): r for r in ro}, {key(r): r for r in rn}
removed = [ko[k] for k in ko if k not in kn]
added = [kn[k] for k in kn if k not in ko]
print(f"\n== record-level check: removed from the main file {len(removed)}, added {len(added)}")
assert not added, "new code added records to the main file"
ukn = {key(r): r for r in un}
by_rule = collections.Counter()
for r in removed:
    u = ukn.get(key(r))
    assert u is not None and u.get("demoted_by"), f"removed record not found in the unconfirmed file with a reason: {r['record_id']}"
    assert tier(r) == "likely", f"a non-likely record was removed: {r['record_id']} {r['affiliation_status'][:40]}"
    by_rule[u["demoted_by"]] += 1
print("   every removed record is a 'likely' record and sits in the unconfirmed file with a reason:", dict(by_rule))
uko = {key(r): r for r in uo}
assert set(ukn) == set(uko) | {key(r) for r in removed}, "unconfirmed file differs by more than the demoted records"
print("   unconfirmed file = old unconfirmed + demoted records, nothing else")
changed = collections.Counter()
for k, r in kn.items():
    o = ko[k]
    for f in set(r) | set(o):
        if f in NEWF or f in OUTF:
            continue
        if r.get(f) != o.get(f):
            changed[f] += 1
print("   fields changed on the records that stayed (other than the new fields and the renumbered record_id):", dict(changed) or "none")
ver = [(kn[k], ko[k]) for k in kn if tier(kn[k]) == "verified"]
print(f"   verified records: {len(ver)} in both, identical apart from the new fields: {all({f: v for f, v in a.items() if f not in NEWF | OUTF} == {f: v for f, v in b.items() if f not in OUTF} for a, b in ver)}")

print("\n== demoted records (new code), by rule")
for rule in ("F1_start_year", "F5_namesake_guard"):
    rows = [r for r in un if r.get("demoted_by") == rule]
    print(f"   {rule}: {len(rows)}")
    for r in rows[:6]:
        print(f"     {r['record_id']} {r['year']} {str(r['title'])[:48]!r}  {r['unconfirmed_reason'][:150]}")
audit = [os.path.join(scr, "new/WebScrape/v2/logs", f"{n}_{inst}.jsonl.gz") for n in ("startyear_demoted", "namesake_demoted")]
print("   audit files:", {os.path.basename(a): sum(1 for _ in gzip.open(a, "rt")) for a in audit})

if live:
    sl, rl = load(os.path.join(live, "v2", inst + ".json"))
    kl = {key(r): r for r in rl}
    print(f"\n== reproducibility: old code on the copied inputs vs the live file ({sl['generated']}): {len(ro)} vs {len(rl)} records, "
          f"same keys {set(ko) == set(kl)}, only-in-copy {len(set(ko) - set(kl))}, only-in-live {len(set(kl) - set(ko))}")
