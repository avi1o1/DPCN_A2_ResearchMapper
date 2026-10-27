"""One-off operator edit (PROCESS_OTHER.md §3.20): add the guarded neighbour exclusion to the six entries merged before the
rule-order finding. Raw strings only; asserts every anchor exists exactly once."""
fn = "C:/Users/varun/rm_v2/WebScrape/scripts/institutes_other.py"
s = open(fn, encoding="utf-8").read()

helper = r'''

def _unless_named(name, neighbours):
    """Exclusion of `neighbours` that share a place token with a lab, unless the same part also names the lab (`name`).
    `other` is consulted only after the type-mention rule, so 'CSIR ... <neighbour> ... <place token>' would otherwise count
    for the lab (PROCESS_OTHER.md §3.11-3.20)."""
    return r"^(?![\s\S]*(" + name + r"))[\s\S]*(" + neighbours + r")"
'''
anchor = "\n\ndef _others(me, *own):"
assert s.count(anchor) == 1
i = s.index(anchor)
j = s.index("\n\n", i + len(anchor))          # end of _others' body
s = s[:j] + helper + s[j:]

edits = {
    "csir_cecri": ("CECRI_NAME", r"alagappa|\bacgcet\b|chettinad|raaja\s+raajan|umayal"),
    "csir_iict": ("IICT_NAME", r"osmania|sarojini\s+naidu|pharmaceutical\s+education|\bnipe?r\b"),
    "csir_ccmb": ('CCMB_NAME + "|" + LACONES', r"zoological\s+survey|botanical\s+survey|\bzsi\b|\bbsi\b"),
    "csir_cftri": ("CFTRI_NAME", r"\bjss\b|public\s+health\s+research\s+institute|\bphrii\b|mysore\s+medical"),
    "csir_cdri": ("CDRI_NAME", r"kalam|\baktu\b|technical\s+university|centre\s+for\s+advanced\s+studies|biotech\s+park|"
                               r"remote\s+sensing|homoeopath"),
    "csir_igib": ("IGIB_NAME", r"university\s+of\s+delhi|delhi\s+university|\bdu\b|north\s+campus|ramjas|daulat\s+ram|"
                               r"hindu\s+college|miranda|kirori"),
}
for key, (name, nb) in edits.items():
    k = s.index(f'    "{key}": dict(')
    e = s.index("        exclude=r\"", k)
    assert e < s.index("    ),", k) if '    ),' in s[k:] else True
    nxt = s.find('\n    "csir_', k + 10)
    assert nxt == -1 or e < nxt, key
    s = s[:e] + f'        exclude=_unless_named({name}, r"{nb}") + "|" + ' + s[e + len("        exclude="):]
    print(key, "edited")
open(fn, "w", encoding="utf-8").write(s)
assert "\x08" not in s
