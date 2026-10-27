"""Registry entries of the other-institutes team (HANDOFF_other_institutes.md; NITs, universities, IISc/TIFR/IISERs, premier
institutes, CSIR, DAE). Merged into institutes.REG by institutes.py; keys must not collide with IIT/IIIT keys.
Fields: see the institutes.py docstring, plus the institution-type fields mention / explicit_full / confusable / family
(affil._C). Unlike the IIT entries, these get no defaults: every channel query and the generic `other` list are spelled out
here. Every decision is recorded in WebScrape/PROCESS_OTHER.md and every reviewed string in test_affil_cases_other.tsv.
"""
from institutes import GENERIC_OTHER   # institutes.py defines it before it imports this module

# How CSIR labs are named as a type. AcSIR (Academy of Scientific and Innovative Research, the degree-granting academy of
# all CSIR labs) is not a mention of any one lab: "AcSIR" contains "csir" without a word boundary, so \bcsir\b skips it,
# and AcSIR alone never names a place of a lab (handoff §6). AcSIR + a lab's name counts for that lab through the lab name.
CSIR_MENTION = r"\bcsir\b|council\s+(of|for)\s+scientific\s+(and|&|&amp;)\s+industrial\s+research"

# "another CSIR lab is named": "CSIR-<lab>" with a lab other than {me}, or the name of a CSIR lab / centre (all 37 labs and
# their outstation centres seen in the review). Used as `confusable` of every CSIR entry, so a bare CSIR mention plus our
# place is not decisive when another lab is named in the same string.
CSIR_OTHER_LAB = (r"\bcsir\s*(-|–|—|‐|−|&#x2013;|\s)\s*(?!{me}|cs*es*rs*cs*i)(?!madras\s+complex|campus|road|complex|lab|labor|hrdc|hq|head)[a-z]|"
                  r"national\s+chemical\s+laboratory|indian\s+institute\s+of\s+chemical\s+(technology|biology)|central\s+leather|"
                  r"national\s+metallurgical|national\s+physical\s+laboratory|central\s+scientific\s+instruments|glass\s+(and|&)\s+ceramic|"
                  r"central\s+mechanical\s+engineering|central\s+road\s+research|mining\s+(and|&)\s+fuel|central\s+building\s+research|"
                  r"central\s+electronics\s+engineering|structural\s+engineering\s+research|advanced\s+materials\s+(and|&)\s+processes|"
                  r"central\s+drug\s+research|cellular\s+(and|&)\s+molecular\s+biology|genomics\s+(and|&)\s+integrative|"
                  r"microbial\s+technology|institute\s+of\s+oceanography|environmental\s+engineering\s+research|"
                  r"minerals\s+(and|&)\s+materials\s+technology|salt\s+(and|&)\s+marine|botanical\s+research|medicinal\s+(and|&)\s+aromatic|"
                  r"himalayan\s+bioresource|integrative\s+medicine|north\s*-?\s*east\s+institute\s+of\s+science|geophysical\s+research|"
                  r"interdisciplinary\s+science\s+(and|&)\s+technology|food\s+technological|toxicology\s+research|"
                  r"indian\s+institute\s+of\s+petroleum|aerospace\s+laborator|fourth\s+paradigm|science\s+communication|"
                  r"policy\s+research|\b(ncl|iict|iicb|clri|nml|npl|csio|cgcri|cmeri|crri|cimfr|cbri|ceeri|serc|ampri|cdri|ccmb|igib|"
                  r"imtech|nio|neeri|immt|csmcri|nbri|cimap|ihbt|iiim|neist|ngri|niist|cftri|iip|nal|4pi|niscpr|niscair|nistads)\b")

# CECRI's name. The acronym alone collides with Rome's "Centre of Excellence for Nursing Scholarship (CECRI)" (review §2.6),
# so "CECRI" counts only with a CECRI context word in the same part (CSIR, electrochemistry, its places, India).
CECRI_NAME = (r"central\s+electro\s*-?\s*chemical\s+res\w*\s+inst\w*|"
              r"\bcecri\b(?=.{0,200}(csir|electro|karaikudi|chennai|madras|tamil|india))|"
              r"(csir|electro|karaikudi|chennai|madras|tamil|india).{0,200}\bcecri\b")

# IICT's name (also "Indian Inst. Chem. Technol."). Recon 2026-10-27: about 900 of the 950 Crossref hits of "IICT" are
# DA-IICT Gandhinagar; IICT-BAS (Sofia), IICT at SUST / BUET (Bangladesh) also print it. The acronym counts only with a
# Hyderabad / CSIR context word in the same part (RMIT: the RMIT-IICT Research Centre) and never after "DA-".
IICT_CTX = r"(csir|hyderabad|tarnaka|uppal|habsiguda|50\s?0\s?[06]07|telangana|andhra|rmit)"
IICT_NAME = (r"indian\s+inst\w*\.?\s+(of\s+)?chem\w*\.?\s+tech\w*|"
             r"(?<!da-)(?<!da‐)(?<!da‑)(?<!da\s)\biict\b(?=.{0,200}" + IICT_CTX + ")|" +
             IICT_CTX + r".{0,200}(?<!da-)(?<!da‐)(?<!da‑)(?<!da\s)\biict\b")


# CCMB's name (recon 2026-10-27, PROCESS_OTHER.md §3.2). "CCMB" also belongs to the Cologne Center for Musculoskeletal
# Biomechanics, CancerCare Manitoba, Brown's Center for Computational Molecular Biology, the Culture Collection of
# Microorganisms of Bahia; "Centre for Cellular and Molecular Biology" is also printed by Deakin University and Amity. Name
# and acronym therefore count only with a CCMB context word in the same part. Not after "AIC-" / "Centre-": the Atal
# Incubation Centre-CCMB is a start-up incubator hosted by CCMB (its strings are `city` -> uncertain).
_NOT_AIC = (r"(?<!aic-)(?<!aic‐)(?<!aic‑)(?<!aic–)(?<!aic\s)(?<!aic/)"
            r"(?<!centre-)(?<!centre‐)(?<!centre‑)(?<!centre–)(?<!center-)(?<!center‐)(?<!center‑)(?<!center–)"
            r"(?<!centre\s–\s)(?<!centre\s-\s)(?<!center\s–\s)(?<!center\s-\s)(?<!aic\s–\s)(?<!aic\s-\s)")
CCMB_CTX = (r"(csir|council\s+(of|for)\s+scientific|hyderabad|telangana|uppal|habsiguda|attapur|hyderguda|annex|lacones|"
            r"500\s?0?(07|48|39)|50007)")
_CCMB_FULL = r"c[ea]nt\w*\s+(for|of)\s+cell?ular\s+(and|&|&amp;)\s+molec\w*\s+bio\w*"
CCMB_NAME = (_NOT_AIC + r"(" + _CCMB_FULL + r"|\bccmb\b)(?=.{0,200}" + CCMB_CTX + r")|" +
             CCMB_CTX + r".{0,200}" + _NOT_AIC + r"(" + _CCMB_FULL + r"|\bccmb\b)")
# LaCONES (Laboratory for the Conservation of Endangered Species, CCMB Annexe I, Attapur 500048): 11 Crossref hits, all CCMB
LACONES = r"\blacones\b"
CCMB_AIC = (r"aic\s*[-‐‑–/]?\s*(ccmb|c[ea]ntre\s+for\s+cell)|atal\s+incubation\s+c[ea]nt\w+\s*[-‐‑–]\s*(ccmb|c[ea]ntre\s+for\s+cell)|"
            r"aic\s*[-‐‑–]\s*c[ea]ntre|ccmb\s+annex\w*\s*(ii|2)\b")


# NCL's name (recon 2026-10-27, PROCESS_OTHER.md §3.3). The full name counts alone (no other "National Chemical
# Laboratory" seen in 2016-2026). "NCL" also belongs to the Naval Cyber Laboratory (France), NCL-Stiftung (Hamburg), NCL
# clinics (UK): it counts only with a CSIR / Pune context word in the same part, and never in "NCL Innovation Park" /
# "NCL Venture Center" / "NCL Colony" (tenant companies, C-DAC and IISER Pune print these addresses). NCIM = NCL's
# National Collection of Industrial Microorganisms.
NCL_CTX = r"(csir|council\s+(of|for)\s+scientific|pune|pashan|homi\s+bh\w+|411\s?0?08)"
NCL_ACR = r"\bncl\b(?!\s*[-‐‑–]?\s*(innovation|colony|venture|stiftung|stp))"
NCL_NAME = (r"national\s+chemical\s+laborator\w*|"
            + NCL_ACR + r"(?=.{0,200}" + NCL_CTX + r")|" + NCL_CTX + r".{0,200}" + NCL_ACR + "|"
            r"\bncim\b[\s‐‑–-]*resource|national\s+collection\s+of\s+industrial\s+micro-?organisms(?=.{0,200}(csir|ncl|national\s+chemical|pune))")


def _others(me, *own):
    """CSIR_OTHER_LAB for a lab whose own name is in the shared list: the lab's own fragments are replaced (asserted, so a
    change of CSIR_OTHER_LAB is noticed)."""
    s = CSIR_OTHER_LAB.format(me=me)
    for frag, rep in own:
        assert frag in s, frag
        s = s.replace(frag, rep, 1)
    return s

def _unless_named(name, neighbours):
    """Exclusion of `neighbours` that share a place token with a lab, unless the same part also names the lab (`name`).
    `other` is consulted only after the type-mention rule, so 'CSIR ... <neighbour> ... <place token>' would otherwise count
    for the lab (PROCESS_OTHER.md §3.11-3.20)."""
    return r"^(?![\s\S]*(" + name + r"))[\s\S]*(" + neighbours + r")"



# Draft registry entry (proposal) -- CSIR-Central Food Technological Research Institute (CFTRI), Mysuru, and its resource
# centres (Hyderabad, Lucknow). Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER,
# _others(). Recon 2026-10-27; evidence: csir_cftri_recon.md and csir_cftri_tests.tsv.

# CFTRI's name. Typo-tolerant: "Inst.", "CSIRCentral", "CSIR-Central, Food Technological" (comma), "CSIR - Central Technological
# Research Institute" (word 'Food' missing, with Mysuru 570020 in the string -> handled through CSIR + 570020 below). The acronym
# "CFTRI" alone: all 189 Crossref hits (2016-2026) and every sample string are CFTRI, so it counts without a place.
CFTRI_NAME = r"central\W{0,3}food\s+tech\w*\s+res\w*\s+inst\w*|\bcftri\b"


# Draft registry entry (proposal) -- CSIR-National Institute for Interdisciplinary Science and Technology (NIIST),
# Thiruvananthapuram (formerly Regional Research Laboratory, RRL-T). Names available from institutes_other.py: CSIR_MENTION,
# CSIR_OTHER_LAB, GENERIC_OTHER, _others(). Recon 2026-10-27; evidence: csir_niist_recon.md and csir_niist_tests.tsv.

# The full name counts alone. The acronym NIIST also belongs to NRI Institution of Information Science & Technology, Bhopal
# (9 of 9 non-CSIR samples): it counts only with a CSIR / Kerala context word in the same part.
NIIST_CTX = r"(csir|council\s+(of|for)\s+scientific|thiruvan\w*|trivan\w*|kerala|pappanam\w*|papanam\w*|695\s?0?19)"
NIIST_NAME = (r"national\s+inst\w*\s+(for|of)\s+interdisc\w*\s+sci\w*\s+(and|&|&amp;)\s+tech\w*|"
              r"\bniist\b(?=.{0,200}" + NIIST_CTX + r")|" + NIIST_CTX + r".{0,200}\bniist\b")


# Draft registry entry (proposal) -- CSIR-Structural Engineering Research Centre (SERC), Chennai (CSIR Madras Complex,
# Taramani). Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others(). Recon
# 2026-10-27; evidence: csir_serc_recon.md and csir_serc_tests.tsv. Mirror entry: csir_cecri (Chennai unit in the same complex).

# Collisions seen in Crossref strings (query "SERC", 40 samples + name query, 200 rows):
#  name "Structural Engineering Research Centre": International Institute of Earthquake Engineering and Seismology (Tehran);
#    "Geotechnical and Structural Engineering Research Centre" (Shandong University); "Institute of Structural Engineering,
#    Research Centre of Steel Structures" (TU Wien)  -> the full name counts only with a CSIR / Chennai / India context word
#    in the same part, and those organisations are in `exclude`;
#  acronym SERC: Temple University (Science Education and Research Center), IIIT Hyderabad (Software Engineering Research
#    Center), IISc (Supercomputer Education and Research Centre), Swedish e-Science Research Centre (SeRC, KTH), MIT, Stevens,
#    University of Houston, VIT (Solar Energy Research Cell), University of South Wales, FIU, UniMAP, AUT, LSE, Chile
#    -> the acronym counts only with CSIR together with a Chennai place word in the same part.
SERC_CTX = r"(csir|council\s+(of|for)\s+scientific|chennai|madras|taramani|tamil|600\s?0?113|india\b)"
SERC_ACR_CTX = r"(csir|council\s+(of|for)\s+scientific)"
SERC_PLACE = r"(chennai|madras|taramani|tamil|600\s?0?113)"
SERC_NAME = (r"struct\w*\s+eng\w*\.?\s+res\w*\s+c[ea]nt\w*(?=.{0,200}" + SERC_CTX + r")|" +
             SERC_CTX + r".{0,200}struct\w*\s+eng\w*\.?\s+res\w*\s+c[ea]nt\w*|"
             r"\bserc\b(?=.{0,200}" + SERC_ACR_CTX + r".{0,200}" + SERC_PLACE + r")|"
             r"\bcsir\s*[-‐‑–—−]?\s*serc\b")


# Draft registry entry (proposal) -- CSIR-National Physical Laboratory (CSIR-NPL), New Delhi. Names available from
# institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others. Recon 2026-10-27; evidence in
# csir_npl_recon.md, test strings in csir_npl_tests.tsv (every string copied from a Crossref probe run 2026-10-27).
#
# Collisions found (Crossref probe strings):
#  * "National Physical Laboratory" / "NPL" is mostly the UK's NPL, Teddington (about half of the 390 Crossref hits of "NPL",
#    1,542 hits of "Teddington"). Without a CSIR / India / Delhi / PIN context word in the same part the name is NOT counted
#    (a bare "National Physical Laboratory (NPL)" is the UK lab in nearly every string seen, 101 of ~350 strings).
#  * "NPL" is also: Nanomaterials and Polymer Nanocomposites Laboratory (UBC Kelowna), NeuroPsychoLinguistique (Toulouse),
#    Nucleo de Pesquisas em Lubrificantes (Fortaleza, Brazil), National Polio Laboratory (Baghdad), NPL Associates /
#    Nuclear Plasma Laboratories, "NPLI" = National Preparedness Leadership Initiative (Harvard) as well as NPL India.
#  * 110012 and Dr. K. S. Krishnan Marg are shared with CSIR-NIScPR (ex NISCAIR) and CSIR-NISTADS (both print "Dr. K. S.
#    Krishnan Marg, New Delhi 110012"), and 110012 is the Pusa campus of ICAR-IARI / IASRI / NBPGR / NIPB (and Jamia Hamdard
#    typos). CSIR-HRDC / AcSIR (Ghaziabad 201002) print the NPL campus as "AcSIR, CSIR-NPL Campus".
#  * "Dr. K. S. Krishnan Geomagnetic Research Laboratory" (Indian Institute of Geomagnetism, Allahabad) and Krishnan Koil /
#    Rama Krishnan College carry the word "Krishnan" -> the street rule requires "K.S. Krishnan Marg|Road".
# NPL's name is "CSIR-National Physical Laboratory"; "CSIR-NPL" counts through the "csir" context word.
def _others_npl():
    s = _others(r"npl|national\s+phys\w*",
                (r"national\s+physical\s+laboratory|", ""),
                (r"|nml|npl|csio|", r"|nml|csio|"))
    # NISTADS prints its name in full ("National Institute of Science, Technology & Development Studies") besides "nistads"
    return s + r"|science\s*,?\s+technology\s+(and|&|&amp;)\s+development\s+stud"

NPL_CTX = r"(csir|council\s+of\s+scientific|new\s*delhi|delhi|\bindia\b|110\s?012|krishnan|nplindia|ghaziabad)"
NPL_NAME = (r"national\s+phys\w*\s+lab\w*(?=.{0,200}" + NPL_CTX + r")|" + NPL_CTX + r".{0,200}national\s+phys\w*\s+lab\w*|"
            r"\bnpli\b(?=.{0,200}" + NPL_CTX + r")|" + NPL_CTX + r".{0,200}\bnpli\b|"
            r"\bnpl\b(?=.{0,200}" + NPL_CTX + r")|" + NPL_CTX + r".{0,200}\bnpl\b|"
            r"\bnpl\s*-?\s*india\b")


# Draft registry entry (proposal) -- CSIR-Central Road Research Institute (CSIR-CRRI), New Delhi (Mathura Road, Okhla).
# Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others. Recon 2026-10-27;
# evidence in csir_crri_recon.md, test strings in csir_crri_tests.tsv (copied from own Crossref scans 2026-10-27).
#
# Traps found (Crossref strings):
#  * "CRRI" = Compulsory Rotatory Residential Internship (dental / medical interns: Karpaga Vinayaga, Sathyabama, Chettinad,
#    Saveetha ... all Tamil Nadu) in about half of the 126 Crossref hits; = Central Rice Research Institute (now ICAR-NRRI,
#    Cuttack; ICAR-CRRI Regional Coastal Rice Research Station, KVK; Central Rainfed Upland Rice Research Station, Hazaribagh);
#    = Centre de Recherche en Rhumatologie et Immunologie (Laval, Quebec); = MINRESI/CRRI-West (Bafoussam, Cameroon).
#    -> the acronym counts only with a road / CSIR / Delhi / Mathura / PIN context word in the same part; `exclude` removes the
#    interns, rice institutes and the Laval / Cameroon centres.
#  * AcSIR's Delhi (coordination) office sits on CRRI's campus: "Academy of Scientific and Innovative Research, New Delhi
#    110025", "AcSIR, Delhi-Mathura Road", "AcSIR, Coordination Office, Mathura Road, CRRI, Jasola" is printed by authors of
#    NCL, IICT, CECRI, IIIM, IHBT, IIP, IGIB, CDRI ("AcSIR CSIR-CRRI New Delhi India | CSIR-IHBT Palampur"). An AcSIR part
#    that names CRRI but no CRRI division / scientist / student is therefore `other`; genuine CRRI AcSIR staff print a division
#    ("AcSIR, Pavement Evaluation Div., Central Road Research Institute") and still count.
#  * 110025 (Mathura Road, Okhla) is shared with CSIR-IGIB's South Campus (Sukhdev Vihar), AcSIR's Delhi address and Jamia
#    Millia Islamia (the bulk of the 1,972 hits). CRRI also prints 110020 and, in typos, 110016. No token is unique.
def _others_crri():
    return _others(r"crri|central\s+(road|res\w*\s+road)",
                   (r"central\s+road\s+research|", ""),
                   (r"|cmeri|crri|cimfr|", r"|cmeri|cimfr|"))

CRRI_CTX = r"(csir|council\s+(of|for)\s+scientific|road|delhi|mathura|110\s?02[05]|pavement|transport|bridge|acsir|academy\s+of\s+scientific)"
CRRI_ACR = r"\bc\.?r\.?r\.?i\b"
CRRI_NAME = (r"central\s+(road\s+res\w*|res\w*\s+road)\s+inst\w*|"          # also the typo "Central Research Road Institution"
             + CRRI_ACR + r"(?=.{0,200}" + CRRI_CTX + r")|" + CRRI_CTX + r".{0,200}" + CRRI_ACR)
# CRRI's divisions exist nowhere else
CRRI_DIV = (r"(flexible|rigid|concrete)\s+pavements?\s+div|pavement\s+evaluation\s+div|pavement\s+engineering\s+area|"
            r"bridge\s+engineering\s+(and|&|&amp;)\s+structures\s+div|traffic\s+engineering\s+(and|&|&amp;)\s+safety\s+div|"
            r"transportation\s+planning\s+(and|&|&amp;)?\s*(environment\w*\s+)?div")
_CRRI_STAFF = r"(pavement|division|\bdiv\b|\barea\b|scientist|bridge|traffic|transport|geotech|student)"
# AcSIR's Delhi office at CRRI: an AcSIR part naming CRRI without any CRRI division / staff word
ACSIR_AT_CRRI = (r"^(?![\s\S]*" + _CRRI_STAFF + r")[\s\S]*(acsir|academy\s+of\s+scientific)[\s\S]*(central\s+(road|res\w*\s+road)|crri)|"
                 r"^(?![\s\S]*" + _CRRI_STAFF + r")[\s\S]*(central\s+(road|res\w*\s+road)|crri)[\s\S]*(acsir|academy\s+of\s+scientific)")


# Draft registry entry (proposal) -- CSIR-Institute of Genomics and Integrative Biology (CSIR-IGIB), Delhi, both campuses:
# North / Mall Road campus (University of Delhi campus, 110007; former Centre for Biochemical Technology, CBT) and South
# campus (Mathura Road, Sukhdev Vihar, 110025; also printed 110020). Names available from institutes_other.py: CSIR_MENTION,
# CSIR_OTHER_LAB, GENERIC_OTHER, _others. Recon 2026-10-27; evidence in csir_igib_recon.md, strings in csir_igib_tests.tsv.
#
# Traps found (Crossref strings):
#  * 110007 is the University of Delhi's PIN (2,505 hits, almost all DU colleges / departments, Shriram Institute, Sansriti):
#    the Mall Road campus shares it -> `shared` (counts only with a CSIR mention; a DU string is None).
#  * 110025 (South campus) is shared with CSIR-CRRI, AcSIR's Delhi office, Jamia Millia Islamia; Sukhdev Vihar and Mathura Road with
#    CSIR-CRRI ("... Mathura Rd., 105, NH-19, Sukhdev Vihar, Okhla"); "Shaheed Sukhdev College" is a DU college. -> 110025 is a sweep
#    token only; "Sukhdev Vihar" is a `city` token; CRRI's name is in `exclude`.
#  * "CBT" (Centre for Biochemical Technology = IGIB's name until 2002) is otherwise Centre for Biotechnology (MDU Rohtak), cognitive
#    behavioural therapy, Chemical Biology and Therapeutics (Novartis) ...: not a token. "G. N. Ramachandran" is also IMTECH's Protein
#    Centre and CDRI's structural biology laboratory: only "Ramachandran Knowledge Center" is an IGIB unit.
#  * Typos of the name seen: "lnstitute" (lower-case L), "Genomics & Interactive Biology", "Genomics and Integrated Biology",
#    "Inst. of", "Institute Genomics and Integrative Biology" (no "of").
def _others_igib():
    return _others(r"igib|inst\w*\.?\s+((of|for)\s+)?genom",
                   (r"genomics\s+(and|&)\s+integrative|", ""),
                   (r"|ccmb|igib|", r"|ccmb|"))

IGIB_NAME = (r"[il]nst\w*\.?\s+((of|for)\s+)?genomics?\s+(and|&|&amp;)\s+(integr|interact)\w*\s+biol\w*|\bigib\b|"
             r"(csir|delhi|mall\s+road|110\s?007)\W.{0,100}cent\w+\s+for\s+biochemical\s+technology|"
             r"cent\w+\s+for\s+biochemical\s+technology.{0,100}(csir|delhi|mall\s+road|110\s?007)")
# units that exist only at IGIB (each seen only with the IGIB name; TRISUTRA 13 Crossref hits, INGEN 1 relevant)
IGIB_UNITS = r"\btrisutra\b|ingen\s*-?\s*hope|ramachandran\s+knowledge"


# Draft registry entry (proposal) -- CSIR-Central Drug Research Institute (CSIR-CDRI), Lucknow (Sector 10, Jankipuram Extension,
# Sitapur Road, 226031; the pre-2000s Chattar Manzil address is not printed 2016-2026). Names available from institutes_other.py:
# CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others. Recon 2026-10-27; evidence in csir_cdri_recon.md, csir_cdri_tests.tsv.
#
# Traps found (Crossref strings):
#  * "CDRI" = Coalition for Disaster Resilient Infrastructure, Cambodia Development Resource Institute (Phnom Penh), CBRN Defense
#    Research Institute (Korea): the acronym counts only with a Lucknow / CSIR / drug / Jankipuram / PIN / AcSIR word in the same part.
#  * 226031 and Jankipuram are shared with Dr. A.P.J. Abdul Kalam Technical University (Centre for Advanced Studies, Sector 11 Jankipuram
#    Vistar; the bulk of the 903 hits of 226031), Biotech Park (Sector G), RSAC-UP, Central Research Institute (Homoeopathy), Turtle
#    Survival Alliance, University of Lucknow institutes; CSIR-NBRI / CSIR-IITR strings print 226031 too.
#  * 226001 (1,991 hits) is Nantong (Jiangsu, China): rejected. Lucknow (21,656 hits) is shared with CSIR-NBRI, CSIR-IITR, CSIR-CIMAP,
#    KGMU, SGPGI ...: sweep only. Sitapur (573) is mostly the city of Sitapur (colleges, eye hospital).
#  * Strings contain line breaks ("CSIRCentral\nDrug Research Institute"): the patterns use \s+ and handle them.
def _others_cdri():
    return _others(r"cdri|central\s+drug",
                   (r"central\s+drug\s+research|", ""),
                   (r"|ampri|cdri|ccmb|", r"|ampri|ccmb|"))

CDRI_CTX = r"(csir|council\s+(of|for)\s+scientific|lucknow|drug|jan\w?kipur\w*|226\s?031|sitapur\s+road|acsir|academy\s+of\s+scientific)"
CDRI_NAME = (r"central\s+drugs?\s+res\w*\s+inst\w*|"
             r"\bcdri\b(?=[\s\S]{0,200}" + CDRI_CTX + r")|" + CDRI_CTX + r"[\s\S]{0,200}\bcdri\b")


# Draft registry entry (proposal) -- CSIR-Institute of Microbial Technology (IMTECH), Sector 39-A, Chandigarh 160036.
# Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others(). Recon 2026-10-27;
# evidence: csir_imtech_recon.md, csir_imtech_tests.tsv, scratch/probe_imtech.txt.
# Neighbour: csir_csio (Chandigarh too, but Sector 30-C, PIN 160030; IMTECH is Sector 39-A, 160036: not the same sector).

# Collisions seen in Crossref strings:
#  name "Institute of Microbial Technology": State Key Laboratory of Microbial Technology / "Institute of Microbial Technology",
#    Shandong University, Qingdao (about 20 of the first 40 strings of "Microbial") -> the full name counts only with a CSIR /
#    Chandigarh / PIN / India context word in the same part, and Shandong / Qingdao is in `exclude`;
#  acronym IMTECH / IMTech: Institute for Microtechnologies (IMtech), RheinMain University of Applied Sciences (Germany);
#    Institut de Matematiques (IMTech), Universitat Politecnica de Catalunya (Spain); "IMTECH FMMR", Technical University of
#    Kosice -> the acronym counts only with a CSIR / Chandigarh / 160036 / Sector 39 word in the same part (not with "India").
IMTECH_CTX = r"(csir|council\s+(of|for)\s+scientific|acsir|chandigarh|160\s?036|sector[-\s]*39|india)"
IMTECH_ACR_CTX = r"(csir|council\s+(of|for)\s+scientific|acsir|chandigarh|160\s?036|sector[-\s]*39)"
# IMTECH's own units: MTCC (Microbial Type Culture Collection & Gene Bank; the 64 Crossref hits of "MTCC" are all IMTECH),
# GNRPC (G. N. Ramachandran Protein Centre; "G.N. Ramachandran" alone is also CDRI's and IGIB's lab -> only with "Protein")
IMTECH_UNITS = (r"microbial\s+type\s+culture\s+collection|\bgnrpc\b|ramachandran\s+protein\s*cent\w*|"
                r"biochemical\s+engineering\s+research\s+(and|&|&amp;)\s+process\s+development")
IMTECH_NAME = (r"institut\w*\s+of\s+microbial\s+tech\w*(?=.{0,200}" + IMTECH_CTX + r")|" +
               IMTECH_CTX + r".{0,200}institut\w*\s+of\s+microbial\s+tech\w*|"
               r"\bimtech\b(?=.{0,200}" + IMTECH_ACR_CTX + r")|" + IMTECH_ACR_CTX + r".{0,200}\bimtech\b")


# Draft registry entry (proposal) -- CSIR-Central Scientific Instruments Organisation (CSIO), Sector 30-C, Chandigarh, and its
# centres (Chennai: CSIR Madras Complex, Taramani; Delhi: "CSIO Delhi"). Names available from institutes_other.py: CSIR_MENTION,
# CSIR_OTHER_LAB, GENERIC_OTHER, _others(). Recon 2026-10-27; evidence: csir_csio_recon.md, csir_csio_tests.tsv,
# scratch/probe_csio.txt.  Neighbour: csir_imtech (also Chandigarh, but Sector 39-A, PIN 160036: CSIO is Sector 30-C, 160030).

# The full name counts alone (the only organisation with "Central Scientific Instruments Organisation"; spellings seen:
# Instrument / Instruments / Instrumentations, Organisation / Organization, "CSIR-Central, Scientific ..." with a comma).
# "Institute of Scientific Instruments" (Brno) has no "Central" -> not matched. The acronym CSIO: all 100 sampled strings of
# the 247 Crossref hits are CSIR-CSIO, but a short acronym is kept to a context word in the same part (CSIR / Chandigarh /
# Chennai / Delhi / 160030 / India); "AcSIR-CSIO" is matched by \bcsio\b.
CSIO_CTX = r"(csir|council\s+(of|for)\s+scientific|acsir|chandigarh|chandigar|160030|sector[-\s]*30|chennai|madras|delhi|india)"
CSIO_NAME = (r"central\W{0,3}scientific\s+instrument\w*\s+organi\w*|"
             r"\bcsio\b(?=.{0,200}" + CSIO_CTX + r")|" + CSIO_CTX + r".{0,200}\bcsio\b")


# Draft registry entry (proposal) -- CSIR-Central Building Research Institute (CBRI), Roorkee 247667 (and the CBRI Ghaziabad
# centre). Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others(). Recon 2026-10-27;
# evidence: csir_cbri_recon.md, csir_cbri_tests.tsv, scratch/probe_cbri.txt, probe_cbri2.txt.
# Mirror entry: iit_roorkee (institutes.py) lists "central building research" and "\bcbri\b" in its `other`.

# CBRI's name. The full name counts alone (no other "Central Building Research Institute" in the strings; ROR's other
# "Building Research Institute" records have no "Central"). Spellings seen: "CSIR-Central, Building..." not seen; "Rookee" typo is
# in the place, not the name. The acronym CBRI also belongs to the Community-Based Research Institute of Florida International
# University (Miami): it counts only with a CSIR / Roorkee / Uttarakhand / PIN / Ghaziabad (CBRI-Ghaziabad centre) / Building
# context word in the same part.
CBRI_CTX = (r"(csir|council\s+(of|for)\s+scientific|acsir|roor?kee|roorke|rorkee|rookee|roorkie|uttarakhand|uttrakhand|"
            r"247\s?667|ghaziabad|central\s+building)")
CBRI_NAME = (r"central\W{0,3}building\s+res\w*\s+inst\w*|"
             r"\bcbri\b(?=.{0,200}" + CBRI_CTX + r")|" + CBRI_CTX + r".{0,200}\bcbri\b")


# Draft registry entry (proposal) -- CSIR-Central Electronics Engineering Research Institute (CEERI), Pilani 333031, and its
# centres (Chennai Centre at the CSIR Madras Complex, Taramani; "CEERI, Jaipur"; the Delhi centre was not seen in strings).
# Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others(). Recon 2026-10-27; evidence:
# csir_ceeri_recon.md, csir_ceeri_tests.tsv, scratch/probe_ceeri.txt, probe_ceeri2.txt.
# Shares Pilani and PIN 333031 with BITS Pilani (not yet registered; its `other`/`exclude` lists must carry "CEERI").

# CEERI's name. Typo-tolerant: "Central Electronics Engineering Institute" (word Research missing), the name split around the
# acronym ("Research Institute(CEERI),CSIR- Central Electronics Engineering"). The acronym CEERI also belongs to the Center for
# Energy Efficiency, Resilience and Innovation (NJIT, Newark), no CSIR / India / Pilani in those strings: the acronym counts
# only with a context word in the same part. The full name counts alone.
CEERI_CTX = (r"(csir|council\s+(of|for)\s+scientific|acsir|pilani|chennai|madras|taramani|jaipur|rajasthan|333\s?031|"
             r"600\s?113|india)")
CEERI_NAME = (r"central\W{0,3}electronics\s+eng\w*\s+(res\w*\s+)?inst\w*|"
              r"\bceeri\b(?=.{0,200}" + CEERI_CTX + r")|" + CEERI_CTX + r".{0,200}\bceeri\b")


# Draft registry entry (proposal) -- CSIR-Advanced Materials and Processes Research Institute (AMPRI; formerly Regional Research
# Laboratory, RRL, Bhopal), Hoshangabad Road, Habibganj Naka, Bhopal 462026 (strings also print 462064). Names available from
# institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others(). Recon 2026-10-27; evidence: csir_ampri_recon.md,
# csir_ampri_tests.tsv, scratch/probe_ampri.txt, probe_ampri2.txt.
# Shares Bhopal with IISER Bhopal, MANIT, AIIMS Bhopal, Barkatullah University (462026), VIT Bhopal; no IIT of institutes.py is in Bhopal.

# AMPRI's name. Spellings seen: "Advanced Material and Processes" (singular), "Advanced Materials Process Research Institute",
# "Advanced Materials Processes and Research Institute", "Advanced Materials & Processes" (the pipeline unescapes &amp;); name
# split over lines. The full name counts alone. The acronym AMPRI: all 183 Crossref hits (2016-2026) are CSIR-AMPRI (sampled in
# full), so it counts alone (as CFTRI). The former name "Regional Research Laboratory" / "RRL" is NOT used: "RRL" 23 hits are
# EPFL's Reconfigurable Robotics Lab, WHO Regional Reference Laboratory, Physica Status Solidi RRL, Dr. Lalpath Labs ...
AMPRI_NAME = (r"advanced\W{0,3}materials?\s+(and\s+|&\s*|&amp;\s*)?process\w*\s+(and\s+)?res\w*\s+inst\w*|\bampri\b")


# Draft registry entry (proposal) -- CSIR-Central Glass and Ceramic Research Institute (CSIR-CGCRI), Kolkata (+ Khurja and
# Naroda centres). Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others.
# Recon 2026-10-27; evidence in csir_cgcri_recon.md, test strings in csir_cgcri_tests.tsv (copied from scratch/probe_csir_cgcri.txt).
#
# Evidence (Crossref probe strings):
#  * 196 Raja S.C. Mullick Road, Jadavpur, Kolkata 700032 is shared with Jadavpur University (188), CSIR-IICB (4), IACS (2A/2B):
#    700032 (5,319 hits) and "Mullick" (1,493) are mostly Jadavpur University. CSIR-IICB prints 700032 WITH a CSIR mention ->
#    exclude. "196" is CGCRI's own door number (never printed by the others in the samples) but is not used as anchor.
#  * CGCRI itself prints "Jadavpur" ("CSIR-CGCRI,Jadavpur,West Bengal,India") and sometimes JU's door number "188" -> `other`
#    must not use the bare word "jadavpur" (use "jadavpur univ").
#  * Khurja Centre (G.T. Road, Khurja 203131): NREC College, Khurja prints Khurja / 203131 (no CSIR). Naroda Centre (Naroda
#    Industrial Estate, Ahmedabad 382330): ESIC / GCS medical colleges, Government Commerce College and Monark University
#    print Naroda / 382330 (no CSIR). CGCRI is the only CSIR lab at both -> Khurja, Naroda and their PINs are `shared`
#    (in scope only with a CSIR mention) and sweep tokens.
#  * "Kolkata" (42,039 hits) / "Calcutta" (7,050) are not unique (IICB, NEERI zonal centre, CSIR HQ units, SINP, ISI ...): sweep-only.
#  * "CGCRI" (59 hits): every sample is CGCRI; no collision found. Still counts only with a context word, as for CECRI.
CGCRI_CTX = r"(csir|council\s+(of|for)\s+scientific|glass|ceramic|kolkata|calcutta|jadavpur|west\s+bengal|khurja|naroda|ahmedabad|india|70{1,2}0?\s?0?32)"
CGCRI_NAME = (r"central\s+glass\s*(and|&|&amp;)\s*ceramic|"
              r"\bcgcri\b(?=.{0,200}" + CGCRI_CTX + r")|" + CGCRI_CTX + r".{0,200}\bcgcri\b|"
              r"khurja\s+cent\w+.{0,120}\bcsir\b|\bcsir\b.{0,120}khurja\s+cent\w+")
# CGCRI's research divisions seen in the probe strings, with a CGCRI place (no other lab of Kolkata names them)
CGCRI_DIV = (r"(fib(re|er)s?\s+optics\s+(and|&|&amp;)\s+photonics|sol\s*[-‐‑–]?\s*gel|specialty\s+glass|"
             r"functional\s+materials\s+(and|&|&amp;)\s+devices|advanced\s+mechanical\s+(and|&|&amp;)\s+material\s+characteri[sz]ation)"
             r"\s+division\b.{0,150}(kolkata|calcutta|jadavpur|\b70{1,2}0?\s?0?32\b|mullick)")


# Draft registry entry (proposal) -- CSIR-National Metallurgical Laboratory (CSIR-NML), Jamshedpur (+ Madras Centre, Chennai).
# Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others.
# Recon 2026-10-27; evidence in csir_nml_recon.md, tests in csir_nml_tests.tsv (strings copied from scratch/probe_csir_nml.txt).
#
# Evidence (Crossref probe strings):
#  * "NML" (155 hits) is also the National Measurement Laboratory: LGC Ltd (Teddington / Guildford, UK) and ITRI Taiwan ("NML/CMS").
#    The acronym counts only with a NML context word in the same part (CSIR, Jamshedpur, Burmamines, Jharkhand, India ...).
#  * "National Metallurgical Laboratory" in full is NML only (no other organisation seen). NIT strings print "Metallurgical and
#    Materials Engineering" but never "National Metallurgical Laboratory".
#  * Burmamines / Burma Mines / 831007: Tata Steel R&D prints them too ("NML Inside Rd., Burma Mines Market"); NIT Jamshedpur is
#    831014 / 831013 (not NML); Jamshedpur 3,719 hits (NIT, Tata Steel, XLRI, RVSCET, NML). NML is the only CSIR lab in Jamshedpur
#    (like CECRI in Karaikudi): CSIR + Jamshedpur counts for NML.
#  * Madras Centre = CSIR Madras Complex, Taramani 600113 (shared with CECRI, SERC, CEERI centre, CSIO centre, AcSIR old office):
#    Taramani / 600113 / Chennai are sweep tokens only; Madras Centre strings print the lab name.
NML_CTX = r"(csir|council\s+(of|for)\s+scientific|jamshedpur|burma\s?mines|jharkhand|831007|madras|chennai|taramani|india|metallurg)"
# not "NML Inside Rd." (Tata Steel R&D's address at Burma Mines: "R&D Division, Tata Steel Ltd., NML Inside Rd., Burma Mines Market")
NML_ACR = r"\bnml\b(?!\s+inside)"
NML_NAME = (r"national\s+metallurg\w*\s+lab\w*|"
            + NML_ACR + r"(?=.{0,200}" + NML_CTX + r")|" + NML_CTX + r".{0,200}" + NML_ACR)


# Draft registry entry (proposal) -- CSIR-Central Mechanical Engineering Research Institute (CSIR-CMERI), Durgapur (+ CoEFM Ludhiana).
# Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others.
# Recon 2026-10-27; evidence in csir_cmeri_recon.md, tests in csir_cmeri_tests.tsv (strings copied from scratch/probe_csir_cmeri.txt).
#
# Evidence (Crossref probe strings):
#  * CMERI sits at Mahatma Gandhi Avenue, Durgapur 713209 - the SAME address as NIT Durgapur ("National Institute of Technology
#    Durgapur, MG Avenue, Durgapur 713209"). Durgapur (4,420 hits) / 713209 (1,039) are mostly NIT Durgapur. NIT strings carry
#    no CSIR mention, CMERI strings do or name the lab. CMERI is the only CSIR lab in Durgapur, so CSIR + Durgapur / 713209 counts.
#  * "Mahatma Gandhi Avenue/Rd." / "M. G. Avenue" is printed by both -> not a token.
#  * CoEFM = CMERI's Centre of Excellence for Farm Machinery, Ludhiana 141006 (shared with Guru Nanak Dev Engineering College,
#    PAU, medical colleges, no CSIR) -> Ludhiana and 141006 are `shared` (CSIR mention needed); "CoEFM" counts as unit.
#  * "CMERI" (156 hits): every sample is CSIR-CMERI; no collision found. It still counts with a context word only.
CMERI_CTX = r"(csir|council\s+(of|for)\s+scientific|durgapur|ludhiana|west\s+bengal|713\s?209|mechanical|india|acsir)"
CMERI_NAME = (r"central\s+mechanical\s+engineering[\s,]+res\w*|"
              r"\bcmeri\b(?=.{0,200}" + CMERI_CTX + r")|" + CMERI_CTX + r".{0,200}\bcmeri\b|"
              r"\bcoefm\b|centre\s+of\s+excellence\s+for\s+farm\s+machinery")


# Draft registry entry (proposal) -- CSIR-Central Institute of Mining and Fuel Research (CSIR-CIMFR), Dhanbad (+ Nagpur and
# Bilaspur research centres). Names available from institutes_other.py: CSIR_MENTION, CSIR_OTHER_LAB, GENERIC_OTHER, _others.
# Recon 2026-10-27; evidence in csir_cimfr_recon.md, tests in csir_cimfr_tests.tsv (strings copied from scratch/probe_csir_cimfr.txt).
#
# Evidence (Crossref probe strings):
#  * Two campuses in Dhanbad: Barwa Road (826001 / 826015, the former Central Mining Research Institute) and Digwadih Campus
#    ("P.O. F.R.I.", Digwadih, 828108, the former Central Fuel Research Institute). Nagpur Research Centre (17/C Telangkhedi
#    Area, Civil Lines, 440001) and Research Centre Bilaspur print the lab name.
#  * IIT (ISM) Dhanbad prints Dhanbad and 826001 (and 826004). Complete scan of Digwadih (49 hits), 828108 (43), 826015 (26): no
#    string without CIMFR / CSIR / "Mining and Fuel" -> these three, and "Barwa Road", are verified-unique `anchor` tokens
#    (the word "Barwa" alone is also a Polish firm in Kielce: not used). 826001 is shared with IIT (ISM) -> `shared`.
#  * Old names: "Central Mining Research Institute" (CMRI) and "Central Fuel Research Institute" (CFRI) appear only in
#    "CMRI/CFRI: Central Institute of Mining and Fuel Research CSIR" form. Collisions: CMRI = China Mobile Research Institute,
#    Children's Medical Research Institute (Sydney), CMRI Kolkata (CK Birla Hospital), Channel Maintenance RI (Egypt); CFRI =
#    China Fire and Rescue Institute, Child & Family RI (UBC), Children's Foundation RI (Memphis); "Central Mining Institute"
#    is the Polish GIG (Katowice). The old acronyms / names count only with a Dhanbad-specific context word.
#  * CSIR-NEERI (Nagpur HQ) and CSIR-HRDC share Nagpur / Ghaziabad: Nagpur, 440001, Bilaspur are sweep tokens only.
#  * CIMFR is the only CSIR lab in Dhanbad: CSIR + Dhanbad counts.
CIMFR_DHN = r"(csir|council\s+(of|for)\s+scientific|dhanbad|jharkhand|digwadih|barwa|828\s?108|826\s?0(01|15))"
CIMFR_CTX = r"(csir|council\s+(of|for)\s+scientific|dhanbad|nagpur|bilaspur|jharkhand|india|mining|fuel)"
CIMFR_NAME = (r"central\s+inst\w*\s+of\s+mining\s*(and|&|&amp;)?\s*fuel|central\s+mining\s*(and|&|&amp;)\s*fuel|"
              r"\bcimfr\b(?=.{0,200}" + CIMFR_CTX + r")|" + CIMFR_CTX + r".{0,200}\bcimfr\b|"
              # former names / acronyms of the two institutes merged in 2007
              r"central\s+(mining|fuel)\s+research\s+inst\w*(?=.{0,200}" + CIMFR_DHN + r")|" +
              CIMFR_DHN + r".{0,200}central\s+(mining|fuel)\s+research\s+inst\w*|"
              r"\b(cmri|cfri)\b(?=.{0,200}" + CIMFR_DHN + r")|" + CIMFR_DHN + r".{0,200}\b(cmri|cfri)\b")


# Draft registry entry (proposal) -- Bhabha Atomic Research Centre (BARC), Trombay, Mumbai, and its outstations. Names available
# from institutes_other.py: GENERIC_OTHER. Recon 2026-10-27; evidence: dae_barc_recon.md, dae_barc_tests.tsv and the probe
# outputs scratch/probe_dae_barc.txt, scratch/probe_dae_mention.txt.
#
# This first draft file also DEFINES the shared DAE patterns (DAE_MENTION, DAE_OTHER_UNIT, HBNI_ONLY) that dae_igcar.py,
# dae_rrcat.py and dae_niser.py reuse (to be placed at the top of the DAE block of institutes_other.py when merged).

# How the Department of Atomic Energy is named as a type. "DAE" collides widely (probe_dae_mention.txt, 1000 Crossref strings):
#   * "UGC-DAE Consortium for Scientific Research" (Indore, Kolkata, Mumbai, Kalpakkam: ~600 of the strings) and "UM-DAE Centre
#     for Excellence in Basic Sciences" are separate organisations -> never a mention (lookbehind on "ugc" / "um" + one character);
#   * "Dae-jeon" / "Dae jeon" / "Dae-gu" / "Dae-dong" (Korea: Daejeon, Daegu), "DAE - IFSC" (Brazil), "DAE (Departamento de
#     Administracao e Economia)" (Lavras), "Department of Agricultural Extension (DAE), MoA, Dhaka" (Bangladesh), Bogazici
#     Kandilli "DAE" (Turkey) -> Korean name parts are excluded by lookahead; the rest have none of our place tokens, so a bare
#     "DAE" can only make a string a unit's string when one of our places is in the same part (and exclude / confusable apply).
# AcSIR-like rule: HBNI (Homi Bhabha National Institute, Anushaktinagar, Mumbai) is the degree-granting university of all DAE
# units and is NOT a mention: HBNI + a unit's name counts for the unit through the unit's name; HBNI alone counts for none.
DAE_MENTION = (r"depart?ment\s+of\s+atomic\s+energy|dept\.?\s+of\s+atomic\s+energy|"
               r"(?<!\bugc.)(?<!\bugc\s.\s)(?<!\bum.)(?<!\bum\s.\s)\bdae\b(?!\s*[-‐‑–]?\s*(jeon|jon|gu\b|dong|gyeong)|\s*[-‐‑–]\s*ifsc)")

# HBNI named (any spelling seen: "Homi Bhabha National Institute", "Homi Bhaba National Institute" (typo, 276 strings), "Bhabha
# National Institute", "Homi Bhabha Institute of Technology (HBNI)", "HBNI"). Used in `other`: a part that names HBNI and a
# place of a unit but not the unit itself is not about the unit (checked after the explicit-name rule).
HBNI_ONLY = r"homi\s+bh?a+b+h?a+\s+(national\s+)?inst\w*|bhabha\s+national\s+inst\w*|\bhbni\b"

# Look-alike DAE organisations (other DAE units, aided institutes, PSUs). Used as `confusable` of every DAE entry: a bare DAE
# mention plus our place is not decisive when another DAE organisation is named in the same part. The four units of this
# group (BARC, IGCAR, RRCAT, NISER) are not listed: they are registered, so the classifier already knows them.
DAE_OTHER_UNIT = (r"tata\s+institute\s+of\s+fundamental|\btifr\b|tata\s+memorial|\bactrec\b|\btmc\b|\btmh\b|homi\s+bhabha\s+cancer|"
                  r"homi\s+bhabha\s+cent(re|er)\s+for\s+science|\bhbcse\b|ugc\W{0,3}dae|consortium\s+for\s+scientific\s+research|"
                  r"\bcebs\b|excellence\s+in\s+basic\s+sciences|nuclear\s+power\s+corporation|\bnpcil\b|atomic\s+energy\s+regulatory|"
                  r"\baerb\b|board\s+of\s+radiation\s+(and|&)\s+isotope|\bbrit\b|heavy\s+water\s+board|variable\s+energy\s+cyclotron|"
                  r"\bvecc\b|saha\s+institute|\bsinp\b|harish.chandra\s+research|\bhri\b|institute\s+of\s+mathematical\s+sciences|"
                  r"\bimsc\b|institute\s+of\s+physics,?\s*(bhubaneswar|sachivalaya)|\biopb\b|institute\s+for\s+plasma\s+research|"
                  r"\bipr\b|atomic\s+minerals\s+directorate|indian\s+rare\s+earths|\birel\b|nuclear\s+fuel\s+complex|"
                  r"uranium\s+corporation|\bucil\b|\bbhavini\b|bharatiya\s+nabhikiya|national\s+cent(re|er)\s+for\s+radio\s+astrophysics|"
                  r"\bncra\b|indian\s+nuclear\s+society|mishra\s+dhatu|\bmidhani\b|nuclear\s+recycle\s+board\s+\(?\s*npcil")

# BARC's name. Typo-tolerant ("Bhaba", "Bhabha", "Centre"/"Center"/"Cente", "Reseach"). Acronym "BARC" collides (probe_dae_barc.txt,
# 1,109 distinct Crossref strings): USDA Beltsville Agricultural Research Center (~half of them), Basic Algorithms Research
# Copenhagen, Big Anxiety Research Centre (UNSW), Bridge Animal Referral Center, Bangladesh Agricultural Research Council (Dhaka),
# Barts Research Centre for Women's Health (QMUL), the Australian Research Council's "ARC" printed as "bARC" (Monash, Tasmania,
# Melbourne ...), Balance and Auditory Research Center (Mississippi), Biotechnology Advanced Research Centre (SHESTCO, Nigeria),
# BARC-SA (Johannesburg), PQ Barcon (Mexico). So the acronym counts only with a BARC context word in the same part, or as the
# last word of a division / section / centre ("Electron Beam Centre, BARC"), or written "B.A.R.C." (dots: no collision seen).
BARC_CTX = (r"(bh?a+b+h?a+|trombay|anushakti\w*|mumbai|bombay|india|vizag|visakhapatnam|kalpakkam|tarapur|hbni|homi|atomic|"
            r"\bdae\b|\b400\s?0?(85|94)\b|hyderabad|training\s+school|facilit|nccm|nuclear|npcil|vecc|ugc)")
BARC_ACR = r"(?<![\w-])barc\b(?!\s*[-‐‑–]\s*(sa|east|west)\b)"
BARC_NAME = (r"bh?a+b+h?a+\s+atomic\s+res\w*(\s+cent\w*)?|"
             r"\bb\.\s?a\.\s?r\.\s?c\b|"
             r"national\s+cent\w*\s+for\s+compositional\s+characteri[sz]ation\s+of\s+materials?|"
             r"(division|section|group|cent(re|er))\s*,\s*" + BARC_ACR + r"\s*($|[,|;)])|"
             + BARC_ACR + r"(?=.{0,200}" + BARC_CTX + r")|" + BARC_CTX + r".{0,200}" + BARC_ACR + r"|"
             r"\bbarc\s+facilit\w+")


# Draft registry entry (proposal) -- Indira Gandhi Centre for Atomic Research (IGCAR), Kalpakkam. Names available from
# dae_barc.py (to be merged first): DAE_MENTION, DAE_OTHER_UNIT, HBNI_ONLY; from institutes_other.py: GENERIC_OTHER.
# Recon 2026-10-27; evidence: dae_igcar_recon.md, dae_igcar_tests.tsv, scratch/probe_dae_igcar.txt.
#
# Kalpakkam is a DAE township: besides IGCAR it hosts BARC Facilities (BARCF: Water and Steam Chemistry Division, Integrated
# Nuclear Recycle Plant, Waste Immobilisation Plant), AERB's Safety Research Institute, NPCIL's Madras Atomic Power Station and
# Nuclear Power Plant Hospital, BHAVINI, the UGC-DAE CSR Kalpakkam Node (Kokilamedu 603104) and HBNI's Kalpakkam centre.
# "IGCAR" (146 Crossref hits, all IGCAR in the samples; no acronym collision found) counts alone.
# Name typo variants seen: "Indira  Gandhi", "IndiraGandhi", "Center", lower-case "atomic research".
IGCAR_NAME = r"indira\s*gandhi\s+cent\w*\s+(for|of)\s+atomic\s+res\w*|\bigcar\b"

# IGCAR's groups / divisions printed without the name next to Kalpakkam ("Metallurgy and Materials Group, Kalpakkam, India | Homi
# Bhabha National Institute, Mumbai, India"; "Corrosion Science and Technology Division, Metallurgy and Materials Group, Kalpakkam
# 603 102"; "Materials Developing and Technology Division, HBNI, Kalpakkam 603 102"). BARCF's Chemistry Group is NOT listed.
IGCAR_GROUPS = (r"(metallurgy\s+(and|&|&amp;)\s+materials|materials?\s+science|materials\s+chemistry|reprocessing|reactor\s+facilities|"
                r"fast\s+reactor\s+technology|safety\W{0,3}\s*quality|corrosion\s+science|physical\s+metallurgy|non\s+destructive\s+evaluation|"
                r"materials\s+develop\w*\s+and\s+technology)\b[^|]{0,150}(kalpakkam|\b603\s?1(02|27)\b)")


# Draft registry entry (proposal) -- Raja Ramanna Centre for Advanced Technology (RRCAT), Indore (PO CAT, 452013). Names available
# from dae_barc.py (to be merged first): DAE_MENTION, DAE_OTHER_UNIT, HBNI_ONLY; from institutes_other.py: GENERIC_OTHER.
# Recon 2026-10-27; evidence: dae_rrcat_recon.md, dae_rrcat_tests.tsv, scratch/probe_dae_rrcat.txt.
#
# Name variants seen in Crossref strings: "Raja Rammana Centre", "Raja Ramana Centre for Advance Technology", "Raja Ramanna Center",
# "Raja Ramanna Ctr." (INSPIRE style), "Raja Ramanna Research Center", and the pre-2005 name "(Centre for) Advanced Technology (CAT)",
# "P.O.: CAT, Indore". "Raja Ramanna Fellow" / "Raja Ramanna Chair" are DAE fellowships held at CSIR-NGRI, BARC, IGCAR, AMD, DRDO,
# IIT Kharagpur ...: they are NOT RRCAT, so the pattern requires Centre / Center / Ctr. / Research Centre after "Raja Ramanna".
# The acronym "RRCAT" (203 Crossref hits, every sample string is RRCAT) counts alone.
RRCAT_NAME = (r"raja\s+ram{1,2}an{1,2}a\s+(research\s+)?(cent\w*|ctr\b)|\brrcat\b|"
              r"\bcent\w*\s+for\s+advanc\w*\s+tech\w*[^|]{0,60}\bindore\b|\bp\.?\s?o\.?:?\s*cat\b")


# Draft registry entry (proposal) -- National Institute of Science Education and Research (NISER), Bhubaneswar: the Jatni campus
# (PO Bhimpur-Padanpur, Via Jatni, Khurda 752050, since 2015) and the transit campus on the Institute of Physics campus
# (Sachivalaya Marg, PO Sainik School, Bhubaneswar 751005, 2007-2015). NISER is a teaching institute (HBNI constituent; its schools
# print "An OCC of Homi Bhabha National Institute"). Names available from dae_barc.py (to be merged first): DAE_MENTION, DAE_OTHER_UNIT,
# HBNI_ONLY; from institutes_other.py: GENERIC_OTHER. Recon 2026-10-27; evidence: dae_niser_recon.md, dae_niser_tests.tsv,
# scratch/probe_dae_niser.txt.
#
# Acronym collisions (probe "NISER": 947 distinct strings, 49 without Bhubaneswar/Odisha/Jatni/HBNI/science education):
#  * Nigerian Institute of Social and Economic Research, Ibadan (the bulk: "NISER" prints ~45 of the 49), also written "National Institute
#    of Social and Economic Research (NISER)" and "Nigeria institute of Social ...";
#  * Nepal Institute for Social and Environmental Research (NISER); "Niser Eye Clinic"; "MacAuthur Project Office, NISER".
# So "NISER" counts only with a Bhubaneswar / Odisha / HBNI context word in the same part (the typo "Bubaneswar" and the abbreviation
# "BBSR" are context words), and the Nigerian / Nepalese look-alikes are in `exclude`. The full name starts with "National Institute
# of Science Education": it does not match "Indian Institute of Science Education and Research" (IISERs).
NISER_CTX = (r"(bh?u\w*nesh?war|bbsr|odisha|orissa|jat(ni|ani)|khurda|khordha|khorda|padanpur|bhimpur|\b752\s?050\b|\b751\s?005\b|"
             r"hbni|homi|\bdae\b|atomic\s+energy)")
NISER_NAME = (r"national\s+inst\w*\s+(of|for)\s+science\s+educ\w*\s*(and|&|&amp;)?\s*res\w*|"
              r"(?<![a-z])niser(?![a-z])(?=.{0,200}" + NISER_CTX + r")|" + NISER_CTX + r".{0,200}(?<![a-z])niser(?![a-z])")


EXT = {
    # ------------------------------------------------------------------ CSIR-CECRI, Karaikudi (pilot, PROCESS_OTHER.md §2)
    # Recon 2026-10-27: Karaikudi and CECRI's PINs 630003 / 630006 are shared with Alagappa University, so no token is
    # unique to the campus (anchor None: no department-only rule). The lab's name and "CECRI" count without a place
    # ("CSIR-CECRI , , , ," strings). Chennai unit = CSIR Madras Complex, Taramani 600113, shared with CSIR-SERC,
    # CSIR-CLRI, CSIR-CEERI's centre, IMSc and the University of Madras; CSIR-CSMCRI has a station at Mandapam.
    "csir_cecri": dict(
        name="CSIR-Central Electrochemical Research Institute", ror="https://ror.org/01qek3q18", grid="grid.417628.e",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CECRI_NAME,
        # another CSIR lab named ("CSIR-NCL", "CSIR-Indian Institute of Chemical Technology" ...): a bare CSIR mention in the
        # same string is then not this lab (review §2.4: NCL Pune / IICT / CDRI authors printing AcSIR's Taramani address)
        confusable=CSIR_OTHER_LAB.format(me=r"c\s*e\s*c\s*r\s*i|central\s+electro|electro"),
        crossref=["Karaikudi", "630003", "630006", "CECRI", "Karaikkudi", "Karikudi", "Taramani", "600113", "Mandapam",
                  "Tuticorin", "Thoothukudi"],
        crossref_broad=[],
        anchor=None,
        city=r"\b(karaikudi|karaikkudi|karikudi)\b|\b(630003|630006)\b|cecri\.res\.in",
        # Taramani / 600113 / Mandapam / Tuticorin / Thoothukudi are sweep tokens only: there a string counts only if it
        # names CECRI (review §2.4: the CSIR Campus Taramani is AcSIR's old head office and hosts NML, CSIO, NEERI centres)
        shared=None,
        # the name, and CECRI's electrochemistry divisions with a Karaikudi place (review §2.4: no other electrochemistry
        # division exists in Karaikudi; Alagappa University has departments of chemistry / industrial chemistry)
        units=CECRI_NAME + "|"
              r"(electro\s*-?\s*organic|electrochemical\s+(power|process|materials)|materials\s+electrochemistry|electrodics|"
              r"corrosion\s+(and|&)\s+materials?\s+protection)\b.{0,120}(karaikudi|\b630\s*00[36]\b)",
        state=None,   # Tamil Nadu has several CSIR labs (CECRI, SERC, CLRI, CEERI centre): no state rule
        # other organisations at CECRI's places: never CECRI even with a CSIR mention (checked before the mention rule)
        exclude=_unless_named(CECRI_NAME, r"alagappa(?!puram)|\bacgcet\b|chettinad|raaja\s+raajan|umayal") + "|" + r"structural\s+engineering\s+research|\bserc\b|central\s+leather\s+research|\bclri\b|"
                r"central\s+electronics\s+engineering\s+research|\bceeri\b|salt\s+(and|&|&amp;)\s+marine|\bcsmcri\b|"
                r"mathematical\s+sciences|\bimsc\b|university\s+of\s+madras|"
                # Rome's Centre of Excellence for Nursing Scholarship is also "CECRI" (review §2.6)
                r"nursing\s+scholarship|ricerca\s+infermieristica|professioni\s+infermieristiche",
        other=r"alagappa|\bacgcet\b|chettinad|raaja\s+raajan|umayal|central\s+marine\s+fisheries|\bcmfri\b|"
              r"suganthi\s+devadason|fisheries|kamaraj|chidambaram|swaminathan|voluntary\s+health|"
              # review §2.4: Quindío (Colombia) uses postcode 630003; private labs / colleges of Karaikudi and misplaced PINs
              r"quind|colombia|biome|\bkit\s+(and|&)\s+kim\b|\baccet\b|karunya|srirangam|\bsalem\b|mavmm|kumaragiri|"
              + GENERIC_OTHER,
        europepmc='(AFF:"Central Electrochemical Research Institute" OR AFF:"Central Electro Chemical Research Institute" OR '
                  'AFF:"CECRI" OR AFF:"cecri.res.in" OR (AFF:"Karaikudi" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Electrochemical Research Institute"',
              'bibjson.author.affiliation:"CECRI"',
              'bibjson.author.affiliation:"Karaikudi" AND bibjson.author.affiliation:"CSIR"'],
        inspire='(aff:"CECRI, Karaikudi" or aff:"Karaikkudi, CERI")',
        orcid_q='affiliation-org-name:"Central Electrochemical Research Institute" OR affiliation-org-name:(CECRI) OR '
                'ror-org-id:"https://ror.org/01qek3q18"',
        orcid_city=r"karaikudi|karaikkudi|cecri",
        dblp=("karaikudi|cecri|electrochemical research", r"karaikudi|cecri|central\s+electro\s*-?\s*chemical"),
        tenure_lag=1),
    # ------------------------------------------------------------------ CSIR-IICT, Hyderabad (PROCESS_OTHER.md §3)
    # Recon 2026-10-27 (logs/recon_csir_iict.tsv): no token is unique to the campus. Tarnaka = also Osmania University and
    # a pharmacy college; 500007 / Habsiguda / Uppal (Road) = also CSIR-CCMB, CSIR-NGRI, ICMR-NIN, Osmania; 500607 is a
    # misprint of IICT's PIN printed almost only by IICT.
    "csir_iict": dict(
        name="CSIR-Indian Institute of Chemical Technology", ror="https://ror.org/040dky007", grid="grid.417636.1",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=IICT_NAME,
        # another CSIR lab named (CCMB and NGRI share Uppal Road / Habsiguda / 500007): IICT's own fragments removed
        confusable=_others(r"iict|indian\s+inst\w*\.?\s+(of\s+)?(chem\w*\.?\s+tech|technology)",
                           (r"indian\s+institute\s+of\s+chemical\s+(technology|biology)|", r"indian\s+institute\s+of\s+chemical\s+biology|"),
                           (r"(ncl|iict|iicb|", r"(ncl|iicb|")),
        # Crossref hits 2016-2026: IICT 950, Tarnaka 729, 500607 50, Habsiguda 98, 500007 2,535, Uppal 907. Hyderabad
        # 62,987 (+ misspellings Hyderbad 130, Hydrabad 67, Hyderabd 11; Secunderabad 1,765): strings printing only
        # "Indian Institute of Chemical Technology, Hyderabad" contain none of the campus tokens (first pass, §3.1).
        # Sweep only: they count only when the string names IICT (shared=None).
        crossref=["IICT", "Tarnaka", "500607", "Habsiguda", "500007", "Uppal", "Hyderabad", "Hyderbad", "Hydrabad", "Hyderabd",
                  "Secunderabad"],
        crossref_broad=[],
        anchor=None,
        # Tarnaka / 500607 + a CSIR mention (no other CSIR lab named) -> IICT; without the mention -> uncertain
        city=r"\btarnaka\b|\b500\s?607\b|iict\.res\.in",
        # Habsiguda / Uppal / 500007 are sweep tokens only: there a string counts only if it names IICT (as Taramani for CECRI)
        shared=None,
        units=IICT_NAME,
        state=None,   # Telangana has CCMB, NGRI and a CFTRI resource centre too
        # same place, other organisations; look-alike acronym owners; ICT Mumbai (only with its own places, because a
        # bare "institute of chemical technology" also occurs inside IICT's name)
        exclude=_unless_named(IICT_NAME, r"osmania|sarojini\s+naidu|pharmaceutical\s+education|\bnipe?r\b") + "|" + r"cellular\s+(and|&|&amp;)\s+molecular\s+biology|\bccmb\b|geophysical\s+research|\bngri\b|food\s+technological|\bcftri\b|"
                r"national\s+institute\s+of\s+nutrition|\bicmr\b|\bcdfd\b|fingerprinting|"
                # review §3.1: CSIR-NEERI's Hyderabad Zonal Centre prints "IICT Campus, Tarnaka" as its address
                r"national\s+environmental\s+engineering\s+research|\bneeri\b|"
                r"\bda\s*[-‐‑–]?\s*iict|dhirubhai|bulgarian|\bbas\b|\bsust\b|\bbuet\b|\bkbtu\b|\bheig\b|hes-so|"
                r"institute\s+of\s+information\s+(and|&|&amp;)\s+communication|"
                r"matunga|nathalal|institute\s+of\s+chemical\s+technology\W{0,3}(mumbai|jalna|bhubaneswar|marathwada)",
        other=r"osmania|sarojini\s+naidu|\bnirmala|\bnipe?r\b|\bnrsc\b|remote\s+sensing|c-?met\b|materials\s+for\s+electronics|"
              r"tata\s+institute\s+of\s+fundamental|\btifr\b|gachibowli|neil\s+gogte|keshav\s+memorial|drugparadigm|gvk\s+bio|aragen|"
              r"anand\s+eye|jawaharlal\s+nehru\s+technological|\bjntu|" + GENERIC_OTHER,
        europepmc='(AFF:"Indian Institute of Chemical Technology" OR AFF:"CSIR-IICT" OR (AFF:"IICT" AND (AFF:"Hyderabad" OR AFF:"CSIR")) OR '
                  '(AFF:"Tarnaka" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Indian Institute of Chemical Technology"',
              'bibjson.author.affiliation:"CSIR-IICT"',
              'bibjson.author.affiliation:"Tarnaka" AND bibjson.author.affiliation:"CSIR"'],
        inspire=None,   # no INSPIRE institution record for IICT
        orcid_q='affiliation-org-name:"Indian Institute of Chemical Technology" OR ror-org-id:"https://ror.org/040dky007"',
        orcid_city=r"tarnaka|\biict\b|indian\s+institute\s+of\s+chemical\s+technology",
        dblp=("indian institute of chemical technology|iict", r"indian\s+institute\s+of\s+chemical\s+technology|csir.{0,20}iict"),
        tenure_lag=1),
    # ------------------------------------------------------------------ CSIR-CCMB, Hyderabad (PROCESS_OTHER.md §3.2)
    # Recon 2026-10-27 (agent draft, reviewed): main campus Uppal Road, Habsiguda 500007 (shared with IICT, NGRI, NIN,
    # Osmania); LaCONES at CCMB Annexe I, Attapur 500048 (shared with ZSI, BSI); AIC-CCMB incubator at IDA Uppal 500039
    # (shared with CDFD). No token is unique to the campus.
    "csir_ccmb": dict(
        name="CSIR-Centre for Cellular and Molecular Biology", ror="https://ror.org/05shq4n12", grid="grid.417634.3",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CCMB_NAME + "|" + LACONES,
        # another CSIR lab named (IICT and NGRI share Uppal Road / Habsiguda / 500007): CCMB's own fragments removed
        confusable=_others(r"ccmb|c[ea]nt\w*\s+(for|of)\s+cell?ular",
                           (r"cellular\s+(and|&)\s+molecular\s+biology|", ""),
                           (r"|ccmb|", r"|")),
        # Crossref hits 2016-2026: CCMB 226, LaCONES 11, 500048 21, Hyderguda 25, Attapur 9, Habsiguda 98, 500007 2,535,
        # Uppal 907, 500039 135; Hyderabad and misspellings as for IICT (strings with only "CCMB, Hyderabad")
        crossref=["CCMB", "LaCONES", "500048", "Hyderguda", "Attapur", "Habsiguda", "500007", "Uppal", "500039",
                  "Hyderabad", "Hyderbad", "Hydrabad", "Hyderabd", "Secunderabad"],
        crossref_broad=[],
        anchor=None,
        # 500048 (LaCONES; shared with ZSI / BSI): with a CSIR mention -> CCMB, without -> uncertain. AIC-CCMB -> uncertain.
        city=r"\b500\s?048\b|ccmb\.res\.in|" + CCMB_AIC,
        shared=None,   # Habsiguda / Uppal / 500007 / 500039 / Hyderguda / Attapur / Hyderabad: count only if CCMB is named
        units=CCMB_NAME + "|" + LACONES,
        state=None,
        # same places, other organisations; acronym / name look-alikes. "IICT Colony" is part of CCMB's own address
        # ("Uppal Road, IICT Colony, Habsiguda", §3.1 review): the IICT acronym is excluded only when not followed by "colony"
        exclude=_unless_named(CCMB_NAME + "|" + LACONES, r"zoological\s+survey|botanical\s+survey|\bzsi\b|\bbsi\b") + "|" + r"indian\s+institute\s+of\s+chemical\s+technology|\biict\b(?!\s*colony)|geophysical\s+research|\bngri\b|"
                r"food\s+technological|\bcftri\b|national\s+institute\s+of\s+nutrition|\bicmr\b|\bcdfd\b|fingerprinting|"
                r"national\s+environmental\s+engineering\s+research|\bneeri\b|"
                r"cologne|musculoskeletal|cancer\s*care\s+manitoba|manitoba|computational\s+molecular|maluku|bahia|deakin|amity",
        other=r"osmania|zoological\s+survey|botanical\s+survey|\bzsi\b|\bbsi\b|prdis|participatory\s+rural|fernandez|apollo|mythri|"
              r"icbm|keshav\s+memorial|neil\s+gogte|drugparadigm|utopia\s+therap|aditum|sarojini\s+naidu|\bnipe?r\b|\bnrsc\b|"
              r"remote\s+sensing|c-?met\b|gachibowli|medchal|cmr\s+college|malla\s+reddy|\bvnr\b|"
              r"jawaharlal\s+nehru\s+technological|\bjntu|deccan\s+college|" + GENERIC_OTHER,
        europepmc='(AFF:"Centre for Cellular and Molecular Biology" OR AFF:"Center for Cellular and Molecular Biology" OR '
                  '(AFF:"Cellular and Molecular Biology" AND AFF:"Hyderabad") OR AFF:"CSIR-CCMB" OR '
                  '(AFF:"CCMB" AND (AFF:"Hyderabad" OR AFF:"CSIR")) OR AFF:"LaCONES" OR (AFF:"Habsiguda" AND AFF:"Cellular")) '
                  'AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Centre for Cellular and Molecular Biology"',
              'bibjson.author.affiliation:"CSIR-CCMB"',
              'bibjson.author.affiliation:"LaCONES"'],
        inspire=None,   # no INSPIRE institution record
        orcid_q='affiliation-org-name:"Centre for Cellular and Molecular Biology" OR affiliation-org-name:(CCMB) OR '
                'ror-org-id:"https://ror.org/05shq4n12"',
        orcid_city=r"habsiguda|uppal|\bccmb\b|cellular\s+(and|&)\s+molecular\s+biology|lacones",
        dblp=("cellular and molecular biology|ccmb", r"cellular\s+(and|&)\s+molecular\s+biology.{0,60}hyderabad|csir.{0,20}ccmb"),
        tenure_lag=1),
    # ------------------------------------------------------------------ CSIR-NCL, Pune (PROCESS_OTHER.md §3.3)
    # Recon 2026-10-27 (agent draft, reviewed): Dr. Homi Bhabha Road, Pashan, Pune 411008, shared with IISER Pune, IITM,
    # C-MET, C-DAC, NCCS and the NCL Innovation Park / Venture Center tenants. No token is unique to the campus.
    "csir_ncl": dict(
        name="CSIR-National Chemical Laboratory", ror="https://ror.org/057mn3690", grid="grid.417643.3",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=NCL_NAME,
        confusable=_others(r"ncl|national\s+chemical",
                           (r"national\s+chemical\s+laboratory|", ""),
                           (r"(ncl|iict|", r"(iict|")),
        # Crossref hits 2016-2026: NCL 604, 411008 3,786, Pashan 1,057, NCIM 48 (411021: 187, no NCL string -> not used).
        # Pune 51,761 and Poona 542 (operator, §3.3): strings with only "National Chemical Laboratory, Pune" contain none of
        # the campus tokens. Sweep only (shared=None).
        crossref=["NCL", "411008", "Pashan", "NCIM", "Pune", "Poona"],
        crossref_broad=[],
        anchor=None,
        # NCL's address tokens: with a CSIR mention (no other CSIR lab named) -> NCL, without -> uncertain. "Pune" is not a
        # place: CSIR-URDIP, CSIR-HRDC (AcSIR) and NEERI's zonal lab are in Pune.
        city=r"\bpashan\b|\b411\s?0?08\b|homi\s+bh\w+\s+r(oa)?d|ncl\.res\.in",
        shared=None,
        units=NCL_NAME,
        state=None,   # Maharashtra has CSIR-NEERI (Nagpur) and CSIR-URDIP (Pune)
        exclude=r"science\s+education|\biiser\b|tropical\s+meteorology|\biitm\b|national\s+centre\s+for\s+cell\s+science|\bnccs\b|"
                r"national\s+institute\s+of\s+virology|\bniv\b|\bicmr\b|advanced\s+computing|c-?dac\b|materials\s+for\s+electronics|"
                r"c-?met\b|high\s+energy\s+materials|\bhemrl\b|national\s+environmental\s+engineering\s+research|\bneeri\b|"
                r"innovation\s+park|venture\s+cent|"
                r"naval|stiftung|neurodegenerative",
        other=r"shivaji|savitribai|university\s+of\s+pune|panchavati|panchawati|sutarwadi|defence|defense|\bdrdo\b|\bsus\s+road|"
              r"symbiosis|bharati\s+vidyapeeth|poona\s+college|agharkar|armed\s+forces|\bnrcg\b|national\s+research\s+centre\s+for\s+grapes|"
              + GENERIC_OTHER,
        europepmc='(AFF:"National Chemical Laboratory" OR AFF:"CSIR-NCL" OR (AFF:"NCL" AND (AFF:"Pune" OR AFF:"CSIR")) OR '
                  'AFF:"NCIM Resource" OR (AFF:"Pashan" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"National Chemical Laboratory"',
              'bibjson.author.affiliation:"CSIR-NCL"',
              'bibjson.author.affiliation:"Pashan" AND bibjson.author.affiliation:"CSIR"'],
        inspire=None,   # no INSPIRE institution record
        orcid_q='affiliation-org-name:"National Chemical Laboratory" OR affiliation-org-name:(CSIR-NCL) OR '
                'ror-org-id:"https://ror.org/057mn3690"',
        orcid_city=r"pashan|\bncl\b|national\s+chemical\s+laboratory",
        dblp=("national chemical laboratory|csir-ncl", r"national\s+chemical\s+laborator|csir.{0,20}\bncl\b"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_cftri (PROCESS_OTHER.md §3.4)
    "csir_cftri": dict(
        name="CSIR-Central Food Technological Research Institute", ror="https://ror.org/01d7fn555", grid="grid.417629.f",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CFTRI_NAME,
        # another CSIR lab named: CFTRI's own fragments removed. CSIR-IICT / CCMB / NGRI share Habsiguda / Uppal Road / 500007
        # with CFTRI's Hyderabad resource centre.
        confusable=_others(r"cftri|central\W{0,3}(food\s+)?tech",
                           (r"food\s+technological|", ""),
                           (r"|cftri|", r"|")),
        # Crossref hits 2016-2026: CFTRI 189, 570020 208, Mysuru 4,830, Mysore 4,906, Cheluvamba 18, Mysoru 0, Mysoure 1, Mysur 1
        crossref=["CFTRI", "570020", "Cheluvamba", "Mysuru", "Mysore"],
        crossref_broad=[],
        anchor=None,   # 570020 is also Yadavagiri (JSS Medical / Dental College, PHRII); Cheluvamba is also a Mysore Medical College hospital
        # 570020 / Cheluvamba / the CFTRI e-mail domain: shared with JSS and PHRII (Yadavagiri): a CSIR mention (and no other CSIR
        # lab named) -> CFTRI, without it -> uncertain.
        city=r"\b570\s?020\b|cheluvamba\s+mansion|cftri\.res\.in",
        # Mysuru / Mysore are sweep tokens only (4,800+ hits each: University of Mysore, JSS, DFRL, CIIL, AIISH, medical college;
        # a string there counts only if it names CFTRI). Mysuru + a bare CSIR mention is NOT decisive: CSIR fellows of University
        # of Mysore cannot be told apart in the probe (open question).
        shared=None,
        units=CFTRI_NAME,
        state=None,   # Karnataka has CSIR-4PI (Bengaluru) too
        # never CFTRI even with a CSIR mention: CSIR of Ghana (Council for Scientific and Industrial Research, Accra: its Food
        # Research Institute prints "Central Food Technological Research Institute, CSIR, Accra, Ghana" in one sample string) and
        # South Africa share the name "CSIR"; DRDO's Defence Food Research Laboratory (Mysuru) is the look-alike "Food Research" lab
        exclude=_unless_named(CFTRI_NAME, r"\bjss\b|public\s+health\s+research\s+institute|\bphrii\b|mysore\s+medical") + "|" + r"ghana|accra|kumasi|south\s+africa|pretoria|defen[cs]e\s+food|\bdfrl\b|"
                r"cheluvamba\s+hospital|medical\s+college",
        other=r"university\s+of\s+mysore|mysore\s+university|\buom\b|\bjss\b|public\s+health\s+research\s+institute|\bphrii\b|"
              r"ramakrishna\s+institute|yadavagiri|\bdrdo\b|defen[cs]e|siddarthanagar|central\s+institute\s+of\s+indian\s+languages|"
              r"all\s+india\s+institute\s+of\s+speech|\baiish\b|sri\s+jayachamarajendra|\bsjce\b|vidyavardhaka|maharaja|"
              r"\bsbrr\b|jss\s+academy|" + GENERIC_OTHER,
        europepmc='(AFF:"Central Food Technological Research Institute" OR AFF:"CFTRI" OR (AFF:"Cheluvamba" AND AFF:"CSIR") OR '
                  '(AFF:"Mysuru" AND AFF:"CSIR") OR (AFF:"Mysore" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Food Technological Research Institute"',
              'bibjson.author.affiliation:"CFTRI"',
              'bibjson.author.affiliation:"Mysuru" AND bibjson.author.affiliation:"CSIR"',
              'bibjson.author.affiliation:"Mysore" AND bibjson.author.affiliation:"CSIR"'],
        inspire=None,   # no INSPIRE institution record for CFTRI (queried 2026-10-27: CFTRI, "Food Technological")
        orcid_q='affiliation-org-name:"Central Food Technological Research Institute" OR affiliation-org-name:(CFTRI) OR '
                'ror-org-id:"https://ror.org/01d7fn555"',
        orcid_city=r"\bcftri\b|central\s+food\s+technological",
        dblp=("cftri|central food technological", r"cftri|central\s+food\s+technological"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_niist (PROCESS_OTHER.md §3.5)
    "csir_niist": dict(
        name="CSIR-National Institute for Interdisciplinary Science and Technology", ror="https://ror.org/05bkc5375",
        grid="grid.419023.d",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=NIIST_NAME,
        # another CSIR lab named (CSIR-NIO has a Kochi centre in Kerala): NIIST's own fragments removed
        confusable=_others(r"niist|national\s+inst\w*\s+for\s+interdisc",
                           (r"interdisciplinary\s+science\s+(and|&)\s+technology|", ""),
                           (r"|niist|", r"|")),
        # Crossref hits 2016-2026: NIIST 751, Pappanamcode 41, Papanamcode 1, 695019 616, Thiruvananthapuram 8,869, Trivandrum 4,234
        # (695581 316 = University of Kerala Kariavattom and IIITM-K, 695018 9 = SCT College: rejected)
        crossref=["NIIST", "Pappanamcode", "Papanamcode", "695019", "Thiruvananthapuram", "Trivandrum"],
        crossref_broad=[],
        anchor=None,   # 695019 is also printed by a University of Kerala research centre; Pappanamcode by SCT College of Engineering
        # Pappanamcode / 695019: a CSIR mention (and no other CSIR lab named) -> NIIST, without it -> uncertain
        city=r"\bpapp?anamcode\b|\b695\s?0?19\b|niist\.res\.in",
        # Thiruvananthapuram / Trivandrum are sweep tokens only: University of Kerala, IISER TVM, SCTIMST, IIITM-K print them and a bare
        # CSIR mention (fellows) is not decisive; a string counts only if it names NIIST
        shared=None,
        units=NIIST_NAME,
        state=None,   # Kerala also has CSIR-NIO's Kochi centre
        exclude=r"bhopal|madhya\s+pradesh|nri\s+institution|information\s+science|"
                r"sree\s+chit\w+\s+thirunal|\bsct\b|university\s+of\s+kerala|"
                r"institute\s+of\s+information\s+technology|iiitm",
        other=r"kariavattom|karyavattom|kerala\s+university|\bkerala\b.*\buniversity|medical\s+college|sctimst|chitra\s+tirunal|"
              r"science\s+education\s+and\s+research|\biiser\b|space\s+physics|vssc|vikram\s+sarabhai|technopark|apj\s+abdul|"
              r"amala\s+institute|" + GENERIC_OTHER,
        europepmc='(AFF:"National Institute for Interdisciplinary Science and Technology" OR AFF:"CSIR-NIIST" OR '
                  '(AFF:"NIIST" AND (AFF:"CSIR" OR AFF:"Thiruvananthapuram" OR AFF:"Trivandrum")) OR '
                  '(AFF:"Pappanamcode" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"National Institute for Interdisciplinary Science and Technology"',
              'bibjson.author.affiliation:"CSIR-NIIST"',
              'bibjson.author.affiliation:"Pappanamcode" AND bibjson.author.affiliation:"CSIR"'],
        inspire=None,   # no INSPIRE institution record (queried 2026-10-27: NIIST, Interdisciplinary Science and Technology, RRL Trivandrum)
        orcid_q='affiliation-org-name:"National Institute for Interdisciplinary Science and Technology" OR affiliation-org-name:(NIIST) OR '
                'ror-org-id:"https://ror.org/05bkc5375"',
        orcid_city=r"pappanamcode|\bniist\b|interdisciplinary\s+science\s+(and|&)\s+technology",
        dblp=("niist|interdisciplinary science and technology", r"interdisciplinary\s+science\s+(and|&)\s+technology|csir.{0,20}niist"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_serc (PROCESS_OTHER.md §3.6)
    "csir_serc": dict(
        name="CSIR-Structural Engineering Research Centre", ror="https://ror.org/00pyevk91", grid="grid.462888.8",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=SERC_NAME,
        # another CSIR lab named (CECRI Chennai unit, CLRI, CEERI centre, NML Madras Centre, CSIO Chennai centre share the CSIR
        # Madras Complex): SERC's own fragments removed
        confusable=_others(r"serc|struct\w*\s+eng\w*\.?\s+res",
                           (r"structural\s+engineering\s+research|", ""),
                           (r"|serc|", r"|")),
        # Crossref hits 2016-2026: SERC 362 (mostly other organisations), Taramani 599, 600113 712
        crossref=["SERC", "Taramani", "600113"],
        crossref_broad=[],
        anchor=None,   # nothing is unique to the CSIR Madras Complex
        city=r"serc\.res\.in",
        # Taramani / 600113 are sweep tokens only (as for csir_cecri, review §2.4): the Madras Complex hosts SERC, CECRI's Chennai
        # unit, CLRI, CEERI's, NML's, CSIO's Chennai centres, NEERI's zonal lab and AcSIR's old head office; a string counts only if
        # it names SERC. Chennai / Madras are not place tokens at all.
        shared=None,
        units=SERC_NAME,
        state=None,   # Tamil Nadu has several CSIR labs
        exclude=r"central\s+electrochemical|\bcecri\b|central\s+leather|\bclri\b|central\s+electronics|\bceeri\b|"
                r"national\s+metallurgical|\bnml\b|mathematical\s+sciences|\bimsc\b|university\s+of\s+madras|"
                # name look-alikes
                r"earthquake\s+engineering\s+and\s+seismology|\biiees\b|tehran|\biran\b|shandong|tu\s+wien|vienna|"
                # operator: 'steel structures' and 'geotechnical' removed (SERC has a Steel Structures Laboratory;
                # TU Wien and Shandong are excluded by name)
                # acronym look-alikes
                r"temple\s+univ|houston|\bkth\b|swedish|stockholm|\biiit\b|vellore|\bvit\b|supercomputer|software\s+engineering|"
                r"systems\s+engineering|solar\s+energy|sustainable\s+environment|south\s+wales|florida\s+international|"
                r"science\s+education\s+and\s+research|malaysia|chile|\bmit\b",
        other=r"voluntary\s+health|\bvhs\b|swaminathan|apollo|powder\s+metallurgy|\barci\b|national\s+agro|anna\s+university|"
              r"murugappa|homi\s+bhabha\s+national|\bhbni\b|chidambaram|security\s+\(?sets|" + GENERIC_OTHER,
        europepmc='(AFF:"Structural Engineering Research Centre" OR AFF:"CSIR-SERC" OR (AFF:"SERC" AND AFF:"CSIR" AND AFF:"Chennai")) '
                  'AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Structural Engineering Research Centre"',
              'bibjson.author.affiliation:"CSIR-SERC"'],
        inspire=None,   # no INSPIRE institution record (queried 2026-10-27: "Structural Engineering Research Centre", "SERC Chennai")
        orcid_q='affiliation-org-name:"Structural Engineering Research Centre" OR ror-org-id:"https://ror.org/00pyevk91"',
        orcid_city=r"structural\s+engineering\s+research\s+cent|csir.{0,10}serc",
        dblp=("structural engineering research centre", r"structural\s+engineering\s+research\s+cent"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_npl (PROCESS_OTHER.md §3.7)
    "csir_npl": dict(
        name="CSIR-National Physical Laboratory", ror="https://ror.org/0307k1x46", grid="grid.419701.a",
        # NB the ROR affiliation matcher returns the UK NPL (ror.org/015w2mp89) as `chosen` for this name; the Indian lab is
        # 0307k1x46 ("CSIR National Physical Laboratory of India", acronyms CSIR-NPL, NPL-INDIA)
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=NPL_NAME,
        # another CSIR lab named: NIScPR / NISTADS share Dr. K. S. Krishnan Marg and 110012 (NPL's own fragments removed)
        confusable=_others_npl(),
        # Crossref hits 2016-2026 (recon_probe): NPL 390, NPLI 15, 110012 1,986, Krishnan 862. "National Physical Laboratory"
        # has no rare token ("Physical" 284,986); the name is covered by NPL / Krishnan / 110012 and the other channels.
        # operator: Delhi (106,963 hits) sweep-only, for strings printing only "<name>, New Delhi"
        crossref=["NPL", "NPLI", "110012", "Krishnan", "Delhi"],
        crossref_broad=[],
        anchor=None,   # 110012 = ICAR-IARI & co, CSIR-NIScPR, CSIR-NISTADS; Krishnan Marg = NIScPR / NISTADS: nothing is unique
        # the street (NPL's street, also NIScPR's / NISTADS's) and the e-mail domain: with a CSIR mention (no other lab named)
        # -> NPL; without -> uncertain. "K. S. Krishnan Geomagnetic Research Laboratory" (IIG Allahabad) is not matched.
        city=r"k\.?\s*s\.?\s*krishnan\s+(marg|road|rd)\b|npl\.res\.in|nplindia",
        # 110012 is ICAR's Pusa campus: shared (in scope only with a CSIR mention; ICAR strings are not about NPL at all)
        shared=r"\b110\s?012\b",
        units=NPL_NAME,
        state=None,   # Delhi has several CSIR institutes (NPL, CRRI, IGIB, NIScPR, NISTADS, HQ)
        # CSIR labs of the same street / PIN: never NPL, even with a CSIR mention (checked before the mention rule)
        # operator: ICAR / IARI share 110012 and `other` is checked only after the CSIR-mention rule
        exclude=r"\bicar\b|\biari\b|niscpr|niscair|nistads|science\s+communication|policy\s+research|"
                r"science\s*,?\s+technology\s+(and|&|&amp;)\s+development\s+stud|national\s+institute\s+of\s+science",
        # organisations at 110012 / Pusa and the other Delhi institutions (handoff 5.4; IIT Delhi lists JNU, DU, AIIMS ... itself)
        other=r"icar|\biari\b|\biasri\b|nbpgr|\bnipb\b|agricultur|bioversity|\bpusa\s+institute|dseu|skill\s+and\s+entrepreneurship|"
              r"hamdard|rajendra\s+prasad|geomagnet|jawaharlal\s+nehru|\bjnu\b|university\s+of\s+delhi|delhi\s+university|"
              r"jamia\s+millia|indian\s+institute\s+of\s+technology\s+delhi|\biit\s*-?\s*delhi|all\s+india\s+institute|\baiims\b|"
              r"indraprastha|\biiit\b|indian\s+statistical|national\s+institute\s+of\s+immunology|"
              + GENERIC_OTHER,
        europepmc='(AFF:"National Physical Laboratory" AND (AFF:"CSIR" OR AFF:"New Delhi" OR AFF:"India")) OR AFF:"CSIR-NPL" OR '
                  'AFF:"NPL India" OR AFF:"National Physical Laboratory of India"',
        doaj=['bibjson.author.affiliation:"CSIR-National Physical Laboratory"',
              'bibjson.author.affiliation:"CSIR-NPL"',
              'bibjson.author.affiliation:"National Physical Laboratory" AND bibjson.author.affiliation:"New Delhi"'],
        inspire='aff:"New Delhi, Natl. Physical Lab"',   # legacy ICN, 49 INSPIRE records; ICN "CSIR Natl. Physical Lab of India"
        orcid_q='affiliation-org-name:"National Physical Laboratory of India" OR affiliation-org-name:"CSIR-National Physical Laboratory" '
                'OR ror-org-id:"https://ror.org/0307k1x46"',
        orcid_city=r"csir.{0,5}(npl|national\s+physical)|\bnpli\b|national\s+physical\s+laboratory\s+of\s+india|krishnan\s+(marg|road)",
        dblp=("national physical laboratory|csir-npl", r"csir.{0,20}(npl|national\s+physical)|national\s+physical\s+laboratory.{0,60}(india|delhi)"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_crri (PROCESS_OTHER.md §3.8)
    "csir_crri": dict(
        name="CSIR-Central Road Research Institute", ror="https://ror.org/01pdb1x94", grid="grid.499826.8",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CRRI_NAME,
        # another CSIR lab named: IGIB shares Mathura Road / 110025 / AcSIR's Delhi office (CRRI's own fragments removed)
        confusable=_others_crri(),
        # Crossref hits 2016-2026 (recon_probe / scan): CRRI 126, 110025 1,972, 110020 438, Pavement 864 (CRRI prints it in its division
        # names; rest = pavement engineering elsewhere). All are sweep tokens; none is a scope token (see `shared`).
        # operator: Delhi (106,963 hits) sweep-only
        crossref=["CRRI", "110025", "110020", "Pavement", "Delhi"],
        crossref_broad=[],
        anchor=None,   # nothing unique: 110025 = IGIB, AcSIR Delhi, Jamia Millia; 110020 = Okhla industrial estate, IIIT Delhi; "Mathura Road" too
        city=r"crridom|crri\.res\.in",    # e-mail domains only (scope; no mention -> uncertain)
        # 110025 / 110020 / Mathura Road / Okhla are sweep tokens only (shared=None, as Taramani for CECRI): a CSIR mention at
        # Mathura Road could be IGIB or AcSIR's office, so a string there counts only if it names CRRI or a CRRI division
        shared=None,
        units=CRRI_NAME + "|" + CRRI_DIV,
        state=None,   # Delhi has CRRI, NPL, IGIB, NIScPR, NISTADS, CSIR headquarters
        # never CRRI even with a CSIR mention: the acronym's other owners and AcSIR's office at CRRI (checked before the name)
        exclude=r"\brice\b|\bicar\b|rainfed|cuttack|rotat|residential\s+intern|\bintern(s|ship)?\b|dental|rheumatolog|laval|minresi|bafoussam|"
                + ACSIR_AT_CRRI,
        other=r"jamia|indraprastha|\biiit\b|fortis|apollo|george\s+institute|asia\s+pacific\s+institute|dseu|g\.?\s*b\.?\s*pant|"
              r"institute\s+for\s+human\s+development|esic|jawaharlal\s+nehru|\bjnu\b|university\s+of\s+delhi|delhi\s+university|"
              r"indian\s+institute\s+of\s+technology\s+delhi|\biit\s*-?\s*delhi|all\s+india\s+institute|\baiims\b|indian\s+statistical|"
              + GENERIC_OTHER,
        europepmc='AFF:"Central Road Research Institute" OR AFF:"CSIR-CRRI" OR (AFF:"CRRI" AND (AFF:"CSIR" OR AFF:"New Delhi" OR AFF:"Mathura Road"))',
        doaj=['bibjson.author.affiliation:"Central Road Research Institute"',
              'bibjson.author.affiliation:"CSIR-CRRI"'],
        inspire=None,   # no INSPIRE institution record for CRRI
        orcid_q='affiliation-org-name:"Central Road Research Institute" OR ror-org-id:"https://ror.org/01pdb1x94"',
        orcid_city=r"central\s+road\s+research|csir.{0,5}crri",
        dblp=("central road research institute|csir-crri", r"central\s+road\s+research|csir.{0,10}crri"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_igib (PROCESS_OTHER.md §3.9)
    "csir_igib": dict(
        name="CSIR-Institute of Genomics and Integrative Biology", ror="https://ror.org/05ef28661", grid="grid.417639.e",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=IGIB_NAME,
        # another CSIR lab named (IGIB's own fragments removed). CSIR-CRRI is also here: it shares Mathura Road / Sukhdev Vihar / 110025
        confusable=_others_igib(),
        # Crossref hits 2016-2026 (own runs): IGIB 210, 110007 2,505, 110025 1,972, Sukhdev 94, CBT 197 (not used), Ramachandran 97 (not used)
        # operator: Delhi (106,963 hits) sweep-only
        crossref=["IGIB", "110007", "110025", "Sukhdev", "Delhi"],
        crossref_broad=[],
        anchor=r"igib\.(res\.)?in\b",   # e-mail domain only; every place token is shared (DU, CRRI, AcSIR, Jamia)
        city=r"sukhdev\s+vihar",        # + CSIR mention (no other lab, CRRI is excluded) -> IGIB; no mention -> uncertain
        # 110007 = University of Delhi: in scope only with a CSIR mention. 110025 / 110020 are sweep tokens only (CRRI, AcSIR, Jamia).
        shared=r"\b110\s?007\b",
        units=IGIB_NAME + "|" + IGIB_UNITS,
        state=None,   # Delhi has CRRI, NPL, IGIB, NIScPR, NISTADS, CSIR headquarters
        exclude=_unless_named(IGIB_NAME, r"university\s+of\s+delhi|delhi\s+university|\bdu\b|north\s+campus|ramjas|daulat\s+ram|hindu\s+college|miranda|kirori") + "|" + r"central\s+road\s+research|\bcrri\b|shaheed\s+sukhdev",
        other=r"university\s+of\s+delhi|delhi\s+university|\bdu\b|ramjas|daulat\s+ram|venkateswara|hindu\s+college|miranda|kirori|"
              r"shriram\s+institute|sansriti|north\s+campus|jamia|jawaharlal\s+nehru|\bjnu\b|all\s+india\s+institute|\baiims\b|"
              r"indian\s+institute\s+of\s+technology\s+delhi|\biit\s*-?\s*delhi|indraprastha|\biiit\b|indian\s+statistical|"
              r"george\s+institute|fortis|apollo|maharshi\s+dayanand|rohtak|"
              + GENERIC_OTHER,
        europepmc='AFF:"Institute of Genomics and Integrative Biology" OR AFF:"CSIR-IGIB" OR (AFF:"IGIB" AND (AFF:"CSIR" OR AFF:"Delhi")) OR '
                  '(AFF:"Sukhdev Vihar" AND AFF:"CSIR") OR AFF:"igib.res.in"',
        doaj=['bibjson.author.affiliation:"Institute of Genomics and Integrative Biology"',
              'bibjson.author.affiliation:"CSIR-IGIB"',
              'bibjson.author.affiliation:"IGIB" AND bibjson.author.affiliation:"Delhi"'],
        inspire=None,   # no INSPIRE institution record for IGIB
        orcid_q='affiliation-org-name:"Institute of Genomics and Integrative Biology" OR affiliation-org-name:"CSIR-IGIB" OR '
                'ror-org-id:"https://ror.org/05ef28661"',
        orcid_city=r"genomics\s+(and|&)\s+integrative|\bigib\b",
        dblp=("genomics and integrative biology|igib", r"genomics\s+(and|&)\s+integrative|\bigib\b"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_cdri (PROCESS_OTHER.md §3.10)
    "csir_cdri": dict(
        name="CSIR-Central Drug Research Institute", ror="https://ror.org/04t8qjg16", grid="grid.418363.b",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CDRI_NAME,
        # another CSIR lab named: CSIR-NBRI / IITR / CIMAP (Lucknow) print 226031 and "Lucknow" (CDRI's own fragments removed)
        confusable=_others_cdri(),
        # Crossref hits 2016-2026 (own runs): CDRI 193, 226031 903, Jankipuram 317, Janakipuram 65, Sitapur 573, Nauvakhera 1, Lucknow 21,656,
        # 226001 1,991 (Nantong; sweep not useful), Chattar 6 (Pakistan / Bangladesh: rejected)
        crossref=["CDRI", "226031", "Jankipuram", "Janakipuram", "Nauvakhera", "Sitapur", "Lucknow"],
        crossref_broad=[],
        anchor=None,   # nothing unique: AKTU's Centre for Advanced Studies / Biotech Park / Homoeopathy institute share Jankipuram and 226031
        # with a CSIR mention (no other CSIR lab named) -> CDRI; without -> uncertain / other (AKTU etc. are in `other`)
        city=r"jan\w?kipur\w*|\b226\s?031\b|nauvakhera|cdri\.res\.in|cdriindia",
        shared=None,   # Lucknow / Sitapur are sweep tokens only: four CSIR labs are in Lucknow
        units=CDRI_NAME,
        state=None,    # Uttar Pradesh: CSIR-CDRI, NBRI, IITR, CIMAP (Lucknow), plus others
        # never CDRI: the acronym's other owners; CSIR labs of Lucknow (their names are explicit, so "other", not uncertain)
        exclude=_unless_named(CDRI_NAME, r"kalam|\baktu\b|technical\s+university|centre\s+for\s+advanced\s+studies|biotech\s+park|remote\s+sensing|homoeopath") + "|" + r"coalition|disaster|cambodia|phnom|cbrn|defen[cs]e|"
                r"botanical\s+research|toxicology\s+research|medicinal\s+(and|&|&amp;)\s+aromatic|\bnbri\b|\biitr\b|\bcimap\b",
        other=r"kalam|\baktu\b|technical\s+university|centre\s+for\s+advanced\s+studies|biotech\s+park|remote\s+sensing|homoeopath|"
              r"turtle|university\s+of\s+lucknow|lucknow\s+university|\bkgmu\b|king\s+george|sgpg|sanjay\s+gandhi|integral\s+university|"
              r"babasaheb|ambedkar|goel|rajkiya|ramswaroop|saxena|"
              + GENERIC_OTHER,
        europepmc='AFF:"Central Drug Research Institute" OR AFF:"CSIR-CDRI" OR (AFF:"CDRI" AND (AFF:"Lucknow" OR AFF:"CSIR")) OR AFF:"cdri.res.in" OR '
                  '(AFF:"Jankipuram" AND AFF:"CSIR")',
        doaj=['bibjson.author.affiliation:"Central Drug Research Institute"',
              'bibjson.author.affiliation:"CSIR-CDRI"',
              'bibjson.author.affiliation:"Jankipuram" AND bibjson.author.affiliation:"CSIR"'],
        inspire=None,   # no INSPIRE institution record for CDRI
        orcid_q='affiliation-org-name:"Central Drug Research Institute" OR ror-org-id:"https://ror.org/04t8qjg16"',
        orcid_city=r"central\s+drug\s+research|\bcdri\b|jan\w?kipuram",
        dblp=("central drug research institute|cdri", r"central\s+drug\s+research|csir.{0,10}cdri"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_imtech (PROCESS_OTHER.md §3.11)
    "csir_imtech": dict(
        name="CSIR-Institute of Microbial Technology", ror="https://ror.org/055rjs771", grid="grid.417641.1",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=IMTECH_NAME + "|" + IMTECH_UNITS,
        # another CSIR lab named (CSIO is in Chandigarh too): IMTECH's own fragments removed
        confusable=_others(r"imtech|microbial\s+tech",
                           (r"microbial\s+technology|", ""),
                           (r"|imtech|", r"|")),
        # Crossref hits 2016-2026: IMTECH 203, 160036 291 (shared: DRDO DGRE), 39A 213 (street numbers in Vilnius / Sassari / Iasi /
        # Tashkent / Chita; "Project 39A" of NLU Delhi), MTCC 64, Chandigarh 32,508, Mohali 14,666 (not a token: no IMTECH string
        # printed it), Panchkula 476 (no), Microbial 35,590 (name-only strings "CSIR-Institute of Microbial Technology , , ," contain
        # no other token; half of the first 40 strings are Shandong -> optional, listed last).
        # operator: "Microbial" (35,590 hits, half Shandong) dropped: the Chandigarh sweep already reaches "<name>, Chandigarh"
        crossref=["IMTECH", "160036", "MTCC", "Chandigarh", "Chandigar"],
        crossref_broad=[],
        anchor=None,   # nothing is unique to the campus (160036 is also DGRE, Sector 37/39)
        city=r"\b160\s?036\b|\bsec(tor|\.)?[-\s]*39\s*-?\s*a\b|imtech\.res\.in",
        shared=None,   # Chandigarh: count only if IMTECH is named
        units=IMTECH_NAME + "|" + IMTECH_UNITS,
        state=None,
        # name / acronym look-alikes (the name look-alike Shandong prints no CSIR; kept here so that a string with both is 'other')
        # operator: neighbours sharing the PIN moved from `other` to `exclude` (`other` is checked only after the CSIR-mention rule)
        exclude=r"government\s+medical\s+college|\bgmch\b|terminal\s+ballistics|\btbrl\b|post\s*graduate\s+institute|\bpgimer\b|\bdgre\b|geo-?informatics|shandong|qingdao|rheinmain|microtechnolog|catalunya|cataluny|kosice|tuke\.sk|matem[aà]tiques",
        other=r"defence|\bdrdo\b|\bdgre\b|geo-?informatics|government\s+medical\s+college|\bgmch\b|post\s*graduate\s+institute|"
              r"\bpgimer\b|panjab|punjab\s+engineering|\bpec\b|" + GENERIC_OTHER,
        europepmc='(AFF:"Institute of Microbial Technology" OR AFF:"CSIR-IMTECH" OR (AFF:"IMTECH" AND AFF:"Chandigarh") OR '
                  'AFF:"Microbial Type Culture Collection" OR (AFF:"160036" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Institute of Microbial Technology"',
              'bibjson.author.affiliation:"CSIR-IMTECH"',
              'bibjson.author.affiliation:"IMTECH" AND bibjson.author.affiliation:"Chandigarh"'],
        inspire=None,   # no INSPIRE institution record (queried 2026-10-27)
        orcid_q='affiliation-org-name:"Institute of Microbial Technology" OR affiliation-org-name:(IMTECH) OR '
                'ror-org-id:"https://ror.org/055rjs771"',
        orcid_city=r"institute\s+of\s+microbial\s+technology|\bimtech\b",
        dblp=("institute of microbial technology|imtech", r"institute\s+of\s+microbial\s+technology|csir.{0,20}imtech"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_csio (PROCESS_OTHER.md §3.12)
    "csir_csio": dict(
        name="CSIR-Central Scientific Instruments Organisation", ror="https://ror.org/04bfs6764", grid="grid.505973.d",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CSIO_NAME,
        # another CSIR lab named (IMTECH is in the same city, Sector 39-A; the Chennai centre shares the CSIR Madras Complex with
        # CECRI / SERC / CLRI / CEERI / NML): CSIO's own fragments removed
        confusable=_others(r"csio|central\s+scientific",
                           (r"central\s+scientific\s+instruments|", ""),
                           (r"|csio|", r"|")),
        # Crossref hits 2016-2026: CSIO 247, 160030 334 (shared: GMCH-32, DRDO TBRL), 30C 69 (mostly Sydney / Germany / Italy
        # street numbers), Chandigarh 32,508, Chandigar 7 (misspelling), Chandigrah 13 (misspelling, mostly Chandigarh University),
        # Instruments 10,728 (Texas Instruments ... not recommended). Chandigarh: sweep only (shared=None): strings printing
        # "<lab name>, Chandigarh" without "CSIO" or the PIN are harvested through it and count only because they name CSIO.
        crossref=["CSIO", "160030", "Chandigarh", "Chandigar"],
        crossref_broad=[],
        anchor=None,   # nothing is unique to the campus (160030 is also GMCH-32 and TBRL)
        # 160030 and "Sector 30-C" (TBRL prints "Sector-30 D"): with a CSIR mention -> CSIO; without -> uncertain
        city=r"\b160\s?030\b|\bsec(tor|\.)?[-\s]*30\s*-?\s*c\b|csio\.res\.in",
        shared=None,   # Chandigarh / Chennai / Delhi / Madras: count only if CSIO is named
        units=CSIO_NAME,
        state=None,    # Punjab / Chandigarh also has CSIR-IMTECH
        # only a name look-alike (Brno): the other Chandigarh organisations go to `other`
        # operator: neighbours sharing the PIN moved from `other` to `exclude` (`other` is checked only after the CSIR-mention rule)
        exclude=r"institute\s+of\s+scientific\s+instruments|government\s+medical\s+college|\bgmch\b|terminal\s+ballistics|\btbrl\b|post\s*graduate\s+institute|\bpgimer\b|\bdgre\b|geo-?informatics",
        other=r"government\s+medical\s+college|\bgmch\b|terminal\s+ballistics|\btbrl\b|post\s*graduate\s+institute|\bpgimer\b|"
              r"defence|\bdrdo\b|\bdgre\b|panjab|punjab\s+engineering|\bpec\b|texas\s+instruments|" + GENERIC_OTHER,
        europepmc='(AFF:"Central Scientific Instruments Organisation" OR AFF:"Central Scientific Instrument Organisation" OR '
                  'AFF:"Central Scientific Instruments Organization" OR AFF:"CSIR-CSIO" OR (AFF:"CSIO" AND AFF:"Chandigarh")) '
                  'AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Scientific Instruments Organisation"',
              'bibjson.author.affiliation:"CSIR-CSIO"',
              'bibjson.author.affiliation:"CSIO" AND bibjson.author.affiliation:"Chandigarh"'],
        inspire=None,   # no INSPIRE institution record (queried 2026-10-27)
        orcid_q='affiliation-org-name:"Central Scientific Instruments Organisation" OR affiliation-org-name:(CSIO) OR '
                'ror-org-id:"https://ror.org/04bfs6764"',
        orcid_city=r"central\s+scientific\s+instrument|\bcsio\b",
        dblp=("central scientific instruments|csio", r"central\s+scientific\s+instrument|csir.{0,20}csio"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_cbri (PROCESS_OTHER.md §3.13)
    "csir_cbri": dict(
        name="CSIR-Central Building Research Institute", ror="https://ror.org/03gjr0792", grid="grid.464525.4",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CBRI_NAME,
        # another CSIR lab named: CBRI's own fragments removed
        confusable=_others(r"cbri|central\s+building",
                           (r"central\s+building\s+research|", ""),
                           (r"|cbri|", r"|")),
        # Crossref hits 2016-2026: CBRI 74 (7 of 74 sampled lines are the Community-Based Research Institute, FIU), 247667 3,496
        # (IIT Roorkee, NIH, COER, Roorkee Institute of Technology, CBRI), Roorkee 11,918 (IIT Roorkee, COER, Quantum, Graphic Era,
        # Haridwar Univ., NIH, CBRI), misspellings Roorke 12 / Rorkee 9 / Rookee 3 / Roorkie 1 (all contain CBRI strings or IIT strings),
        # Rurki 3 (Kurukshetra: not Roorkee), Uttarakhand 18,269, Ghaziabad 16,237 (AcSIR head office: not a token),
        # Building 99,291 (rejected). Roorkee and 247667 are sweep only: strings "<CBRI name>, Roorkee" with no CBRI acronym are
        # harvested through them and count only because they name CBRI (a bare "CSIR" + Roorkee is not CBRI: "CSIR-SRF, IIT Roorkee").
        crossref=["CBRI", "247667", "Roorkee", "Roorke", "Rorkee", "Rookee", "Roorkie"],
        crossref_broad=[],
        anchor=None,   # nothing is unique to the campus (247667 is shared with IIT Roorkee, NIH, COER ...)
        city=r"cbri\.res\.in",
        shared=None,   # Roorkee / 247667 / Uttarakhand: count only if CBRI is named
        units=CBRI_NAME,
        state=None,    # Uttarakhand also has CSIR-IIP (Dehradun) and other CSIR / institutes
        # only the acronym look-alike (FIU)
        exclude=r"community\W{0,3}based\s+research\s+institute|florida\s+international",
        other=r"national\s+institute\s+of\s+hydrology|\bnih\b|indian\s+institute\s+of\s+technology|\biit\b|roorkee\s+institute\s+of\s+technology|"
              r"\bcoer\b|college\s+of\s+engineering\s+roorkee|quantum\s+university|graphic\s+era|haridwar\s+university|patanjali|"
              r"bengal\s+engineer|\bb\.?s\.?m\.?\b|" + GENERIC_OTHER,
        europepmc='(AFF:"Central Building Research Institute" OR AFF:"CSIR-CBRI" OR (AFF:"CBRI" AND AFF:"Roorkee")) '
                  'AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Building Research Institute"',
              'bibjson.author.affiliation:"CSIR-CBRI"',
              'bibjson.author.affiliation:"CBRI" AND bibjson.author.affiliation:"Roorkee"'],
        inspire=None,   # no INSPIRE institution record for CBRI (the only hit of "Central Building Research Institute" is TsNIImash)
        orcid_q='affiliation-org-name:"Central Building Research Institute" OR affiliation-org-name:(CBRI) OR '
                'ror-org-id:"https://ror.org/03gjr0792"',
        orcid_city=r"central\s+building\s+research|\bcbri\b",
        dblp=("central building research institute|cbri", r"central\s+building\s+research|csir.{0,20}cbri"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_ceeri (PROCESS_OTHER.md §3.14)
    "csir_ceeri": dict(
        name="CSIR-Central Electronics Engineering Research Institute", ror="https://ror.org/01hh45364", grid="grid.462181.8",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CEERI_NAME,
        # another CSIR lab named (the Chennai centre shares the CSIR Madras Complex with CECRI / SERC / CLRI / NML / CSIO's centres)
        confusable=_others(r"ceeri|central\s+electronics",
                           (r"central\s+electronics\s+engineering|", ""),
                           (r"|ceeri|", r"|")),
        # Crossref hits 2016-2026: CEERI 344 (about 315 CSIR-CEERI; NJIT's Center for Energy Efficiency... 2 sampled), 333031 1,296
        # (BITS Pilani mostly; Suresh Gyan Vihar Univ. Jaipur prints it as a misprint; CEERI), Pilani 9,070 (BITS Pilani, Jhunjhunu
        # universities...), Pilani333031 5 (no-space form; CEERI + BITS), Jhunjhunu 349 (JJT / Singhania Univ., KVK; not a token),
        # Rajasthan 24,312 (rejected), Taramani 599 / 600113 712 (CSIR Madras Complex, counts from the csir_serc recon).
        # Pilani / 333031 / Taramani / 600113 are sweep only: strings "<lab name>, Pilani" without CEERI harvested, they count only
        # because they name CEERI (a bare "CSIR" + Pilani is not CEERI: CSIR-funded BITS Pilani scholars).
        crossref=["CEERI", "333031", "Pilani", "Pilani333031", "Taramani", "600113"],
        crossref_broad=[],
        anchor=None,   # nothing is unique to the campus
        city=r"ceeri\.res\.in",
        shared=None,   # Pilani / 333031 / Taramani / 600113 / Chennai / Jaipur: count only if CEERI is named
        units=CEERI_NAME,
        state=None,    # Rajasthan has no other CSIR lab but the rule would also take BITS / MNIT / CSIR-funded authors
        # BITS Pilani shares the town and the PIN; NJIT shares the acronym
        exclude=r"birla\s+institute\s+of\s+technology|\bbits\b|new\s+jersey|\bnjit\b|energy\s+efficiency,?\s+resilience",
        other=r"suresh\s+gyan|gyan\s+vihar|singhania|tibrewala|\bjjt|krishi\s+vigyan|shekhawati|" + GENERIC_OTHER,
        europepmc='(AFF:"Central Electronics Engineering Research Institute" OR AFF:"CSIR-CEERI" OR (AFF:"CEERI" AND AFF:"Pilani")) '
                  'AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Electronics Engineering Research Institute"',
              'bibjson.author.affiliation:"CSIR-CEERI"',
              'bibjson.author.affiliation:"CEERI" AND bibjson.author.affiliation:"Pilani"'],
        inspire='aff:"Pilani, CEERI"',   # INSPIRE institution record legacy name "Pilani, CEERI" (queried 2026-10-27)
        orcid_q='affiliation-org-name:"Central Electronics Engineering Research Institute" OR affiliation-org-name:(CEERI) OR '
                'ror-org-id:"https://ror.org/01hh45364"',
        orcid_city=r"central\s+electronics\s+engineering|\bceeri\b",
        dblp=("central electronics engineering research institute|ceeri", r"central\s+electronics\s+engineering|csir.{0,20}ceeri"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_ampri (PROCESS_OTHER.md §3.15)
    "csir_ampri": dict(
        name="CSIR-Advanced Materials and Processes Research Institute", ror="https://ror.org/02x351n42", grid="grid.465028.d",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=AMPRI_NAME,
        # another CSIR lab named: AMPRI's own fragments removed
        confusable=_others(r"ampri|advanced\s+materials?\s",
                           (r"advanced\s+materials\s+(and|&)\s+processes|", ""),
                           (r"|ampri|", r"|")),
        # Crossref hits 2016-2026: AMPRI 183, 462026 264 (Barkatullah University / Habib Ganj mostly, AIIMS Bhopal, LNCT University,
        # RKDF, Sarvepalli Radhakrishnan Univ., HEG Ltd Mandideep, Bhopal School of Social Sciences, AMPRI), 462064 10 (all AMPRI),
        # Habibganj 20 (AIIMS Bhopal, Barkatullah, Bhopal School of Social Sciences, AMPRI "Habibganj Naka"), Hoshangabad 87
        # (Hoshangabad town colleges, Barkatullah / RKDF / SRK "Hoshangabad Road", AMPRI), Bhopal 15,360 (AIIMS, IISER, MANIT,
        # VIT, ...), Bhopa 15 (typo; no AMPRI string -> not added), Raisen 120 / Mandideep 17 / RRL 23 (not tokens).
        # Bhopal / 462026 are sweep only: strings "<AMPRI name>, Bhopal" without the acronym are harvested through them and count only
        # because they name AMPRI (a bare "CSIR" + Bhopal is not AMPRI: CSIR-funded Barkatullah / IISER / MANIT scholars).
        crossref=["AMPRI", "462026", "462064", "Habibganj", "Hoshangabad", "Bhopal"],
        crossref_broad=[],
        anchor=None,   # no campus token is unique (462064 is a misprint of the PIN seen only in AMPRI strings, 10 hits: too few to anchor)
        # 462064 and "Habibganj Naka" (the junction at AMPRI's gate; Barkatullah / AIIMS print plain "Habibganj"): with a CSIR
        # mention -> AMPRI; without -> uncertain
        city=r"\b462\s?064\b|habiba?\s?ganj\s+naka|ampri\.res\.in",
        shared=None,   # Bhopal / 462026 / Hoshangabad (Road) / Habibganj: count only if AMPRI is named
        units=AMPRI_NAME,
        state=None,    # Madhya Pradesh: the rule would take CSIR-funded authors of every MP university
        # nothing in Bhopal carries a CSIR mention except AMPRI; the acronym has no look-alike -> no exclude
        exclude=None,
        other=r"barkatullah|all\s+india\s+institute\s+of\s+medical|\baiims\b|\blnct|rkdf|heg\s+ltd|mandideep|\bvit\b|\bmanit\b|"
              r"maulana\s+azad|\brgpv\b|rajiv\s+gandhi\s+proudyogiki|\bbhel\b|bhopal\s+school|sarvepalli|sarvapalli|gandhi\s+medical|"
              r"sanjeev\s+agrawal|\bsam\s+global|bansal|" + GENERIC_OTHER,
        europepmc='(AFF:"Advanced Materials and Processes Research Institute" OR AFF:"Advanced Materials Process Research Institute" OR '
                  'AFF:"CSIR-AMPRI" OR AFF:"AMPRI") AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Advanced Materials and Processes Research Institute"',
              'bibjson.author.affiliation:"AMPRI"'],
        inspire=None,   # no INSPIRE institution record (queried 2026-10-27: "Advanced Materials and Processes Research Institute", "Regional Research Laboratory Bhopal")
        orcid_q='affiliation-org-name:"Advanced Materials and Processes Research Institute" OR affiliation-org-name:(AMPRI) OR '
                'ror-org-id:"https://ror.org/02x351n42"',
        orcid_city=r"advanced\s+materials?\s+(and|&)?\s*process|\bampri\b",
        dblp=("advanced materials and processes research institute|ampri", r"advanced\s+materials?\s+(and|&)\s+processes|csir.{0,20}ampri"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_cgcri (PROCESS_OTHER.md §3.16)
    "csir_cgcri": dict(
        name="CSIR-Central Glass and Ceramic Research Institute", ror="https://ror.org/039d1mp60", grid="grid.418364.c",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CGCRI_NAME,
        # another CSIR lab named ("CSIR-IICB", "CSIR-NEERI", "CSIR-CMERI" ...): a bare CSIR mention + our place is not this lab
        confusable=_others(r"c\s*g\s*c\s*r\s*i|central\s+glass|glass",
                           (r"glass\s+(and|&)\s+ceramic|", ""),
                           (r"cgcri|", "")),
        # hits 2016-2026: CGCRI 59, Mullick 1,493, 700032 5,319, Khurja 38, 203131 21, Naroda 25, 382330 13, Kolkata 42,039,
        # Calcutta 7,050 (the name has no rare token: "Glass"/"Ceramic" are huge; most CGCRI strings are found via Kolkata / Mullick)
        crossref=["CGCRI", "Mullick", "700032", "Khurja", "203131", "Naroda", "382330", "Kolkata", "Calcutta", "Mullik"],
        crossref_broad=[],
        anchor=None,   # 700032 and the street are shared with Jadavpur University, CSIR-IICB, IACS: nothing is unique
        # the campus place tokens: with a CSIR mention (no other lab named, IICB excluded) -> CGCRI, without -> uncertain/other.
        # "196 Raja S.C. Mullick Road" is CGCRI's door number; 700032 is Jadavpur (shared with JU / IACS / IICB: JU/IACS strings
        # carry no CSIR mention and hit `other`)
        city=r"\b196\s*,?\s*raja\s+s\.?\s*c\.?\s*mull?[ia]c?k|\b70{1,2}0?\s?0?32\b|cgcri\.res\.in",
        # Khurja and Naroda centres: only with a CSIR mention (NREC College Khurja, medical colleges of Naroda print them without)
        shared=r"\bkhurja\b|\b203131\b|\bnaroda\b|\b382\s?330\b",
        units=CGCRI_NAME + "|" + CGCRI_DIV,
        state=None,   # West Bengal has CSIR-IICB, CSIR-CMERI (Durgapur), NEERI zonal centre
        # CSIR lab / other bodies of CGCRI's street: never CGCRI even with a CSIR mention
        # operator: neighbour sharing a `city` token, excluded when this lab is not named (`other` is checked only after the
        # CSIR-mention rule, so 'CSIR ... <neighbour> ... <city token>' would otherwise count)
        exclude=r"^(?![\s\S]*(cgcri|glass\s+(and|&|&amp;)\s+ceramic))[\s\S]*jadavpur\s+univ|chemical\s+biology|\biicb\b|cultivation\s+of\s+science|\biacs\b|environmental\s+engineering\s+research|\bneeri\b",
        other=r"jadavpur\s+univ|\bju\b|calcutta|\bnrec\b|n\.r\.e\.c|\bnrec\s+college|bulandshahr|monark|\besic\b|\bgcs\b|commerce\s+college|"
              r"apollo\s+institute|varsha\s+goswami|\bbose\b|saha\s+institute|indian\s+statistical|\biiser\b|\bsinp\b|"
              r"presidency|\bkolkata\s+(medical|college)|tata\s+medical|\biem\b|\buem\b|c-?dac|sameer|manipal|"
              + GENERIC_OTHER,
        europepmc='(AFF:"Central Glass and Ceramic Research Institute" OR AFF:"Central Glass & Ceramic Research Institute" OR '
                  'AFF:"CGCRI" OR AFF:"cgcri.res.in" OR (AFF:"Mullick" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Glass and Ceramic Research Institute"',
              'bibjson.author.affiliation:"CGCRI"',
              'bibjson.author.affiliation:"Central Glass & Ceramic Research Institute"'],
        inspire=None,   # no INSPIRE institution record found (queries "Central Glass and Ceramic", "CGCRI": 0 hits)
        orcid_q='affiliation-org-name:"Central Glass and Ceramic Research Institute" OR affiliation-org-name:(CGCRI) OR '
                'ror-org-id:"https://ror.org/039d1mp60"',
        orcid_city=r"\bcgcri\b|central\s+glass\s*(and|&)\s*ceramic",
        dblp=("cgcri|central glass and ceramic", r"cgcri|central\s+glass\s*(and|&)\s*ceramic"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_nml (PROCESS_OTHER.md §3.17)
    "csir_nml": dict(
        name="CSIR-National Metallurgical Laboratory", ror="https://ror.org/0211zmf46", grid="grid.419695.6",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=NML_NAME,
        # another CSIR lab named (CSIR-CECRI / SERC / CEERI / CSIO at the Madras Complex, CSIR-CIMFR in Jharkhand ...)
        confusable=_others(r"nml|national\s+metallurgical",
                           (r"national\s+metallurgical|", ""),
                           (r"clri|nml|", r"clri|")),
        # hits 2016-2026: NML 155, Burmamines 8, Burma 49, 831007 186, Jamshedpur 3,719; Taramani 599 / 600113 712 (shared with CECRI)
        crossref=["NML", "Burmamines", "Burma", "831007", "Jamshedpur", "Taramani", "600113"],
        crossref_broad=[],
        anchor=None,   # 831007 / Burmamines are printed by Tata Steel R&D as well; nothing is unique to NML
        # Jamshedpur and NML's own address tokens: with a CSIR mention (no other lab named) -> NML; without -> other (NIT, Tata
        # Steel, XLRI listed) or uncertain. 831014 / 831013 (NIT Jamshedpur) are deliberately not tokens.
        city=r"\bjamshedpur\b|\b831\s?007\b|\bburma\s?mines\b|nmlindia\.org",
        # Taramani / 600113 / Chennai: sweep tokens only (AcSIR old office, CSIR Madras Complex): a string there counts only by name
        shared=None,
        units=NML_NAME,
        state=None,   # Jharkhand has CSIR-CIMFR (Dhanbad); Tamil Nadu has several CSIR labs
        # operator: neighbour sharing a `city` token, excluded when this lab is not named (`other` is checked only after the
        # CSIR-mention rule, so 'CSIR ... <neighbour> ... <city token>' would otherwise count)
        exclude=r"^(?![\s\S]*(\bnml\b|national\s+metallurgical))[\s\S]*(tata\s+steel|national\s+institute\s+of\s+technology|\bnit\b|\bxlri\b|xavier)|central\s+institute\s+of\s+mining|mining\s+(and|&)\s+fuel|\bcimfr\b",
        other=r"tata\s+(steel|metaliks|motors|consultancy|power|sons)|\bxlri\b|xavier\s+labour|\brvscet\b|"
              r"karim\s+city|\bn\.?\s?i\.?\s?t\.?\s+jamshedpur|national\s+measurement\s+lab|\blgc\b|teddington|"
              r"indian\s+institute\s+of\s+technology|\biit\b|\bism\b|indian\s+school\s+of\s+mines|"
              + GENERIC_OTHER,
        europepmc='(AFF:"National Metallurgical Laboratory" OR AFF:"CSIR-NML" OR (AFF:"NML" AND (AFF:"Jamshedpur" OR AFF:"CSIR")) OR '
                  '(AFF:"Burmamines" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"National Metallurgical Laboratory"',
              'bibjson.author.affiliation:"CSIR-NML"',
              'bibjson.author.affiliation:"Jamshedpur" AND bibjson.author.affiliation:"CSIR"'],
        inspire=None,   # no INSPIRE institution record ("Natl. Metallurg. Lab", "National Metallurgical Laboratory": 0 hits)
        orcid_q='affiliation-org-name:"National Metallurgical Laboratory" OR affiliation-org-name:(CSIR-NML) OR '
                'ror-org-id:"https://ror.org/0211zmf46"',
        orcid_city=r"national\s+metallurgical|csir.{0,6}nml|burmamines",
        dblp=("national metallurgical|csir-nml", r"national\s+metallurgical|csir.{0,20}\bnml\b"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_cmeri (PROCESS_OTHER.md §3.18)
    "csir_cmeri": dict(
        name="CSIR-Central Mechanical Engineering Research Institute", ror="https://ror.org/059h0ng81", grid="grid.501559.d",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CMERI_NAME,
        # another CSIR lab named (CSIR-NCL appears next to CMERI in AcSIR / dual-affiliation strings, CSIR-HRDC at Ghaziabad ...)
        confusable=_others(r"cmeri|central\s+mechanical|mechanical",
                           (r"central\s+mechanical\s+engineering|", ""),
                           (r"cgcri|cmeri|", r"cgcri|")),
        # hits 2016-2026: CMERI 156, Durgapur 4,420, 713209 1,039, CoEFM 10, Ludhiana 4,993, 141006 89 (Coimbatore 33,629: no CMERI string)
        crossref=["CMERI", "Durgapur", "713209", "CoEFM", "Ludhiana", "141006"],
        crossref_broad=[],
        anchor=None,   # 713209 / Durgapur / MG Avenue are NIT Durgapur's address too
        # Durgapur and CMERI's PIN: with a CSIR mention (no other lab named) -> CMERI; without -> other (NIT Durgapur, Durgapur Steel
        # Plant, colleges) or uncertain. CSIR-CMERI is the only CSIR lab in Durgapur.
        city=r"\bdurgapur\b|\b713\s?209\b|cmeri\.res\.in",
        # CoEFM, Ludhiana: only with a CSIR mention (Ludhiana = GNDEC, PAU, DMC, CMC; none prints CSIR)
        shared=r"\bludhiana\b|\b141\s?006\b",
        units=CMERI_NAME,
        state=None,   # West Bengal has CSIR-IICB, CSIR-CGCRI (Kolkata), NEERI zonal centre
        # operator: neighbour sharing a `city` token, excluded when this lab is not named (`other` is checked only after the
        # CSIR-mention rule, so 'CSIR ... <neighbour> ... <city token>' would otherwise count)
        exclude=r"^(?![\s\S]*(cmeri|mechanical\s+engineering\s+research))[\s\S]*(national\s+institute\s+of\s+technology|\bnit\b|\bn\.\s?i\.\s?t\b)",
        other=r"national\s+institute\s+of\s+technology|\bn\.\s?i\.\s?t\b|durgapur\s+(steel|government|govt|women|institute|project|chemicals|society|medical|"
              r"college)|dr\.?\s*b\.?\s*c\.?\s*roy|bidhan|\bsail\b|steel\s+authority|\bdsp\b|\bdiatm\b|guru\s+nanak\s+dev|\bgndec\b|"
              r"punjab\s+agricultural|\bpau\b|dayanand\s+medical|christian\s+medical|\bdmc\b|"
              r"indian\s+institute\s+of\s+technology|\biit\b|"
              + GENERIC_OTHER,
        europepmc='(AFF:"Central Mechanical Engineering Research Institute" OR AFF:"CSIR-CMERI" OR AFF:"CMERI" OR '
                  '(AFF:"CoEFM" AND AFF:"CSIR")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Mechanical Engineering Research Institute"',
              'bibjson.author.affiliation:"CMERI"',
              'bibjson.author.affiliation:"Durgapur" AND bibjson.author.affiliation:"CSIR"'],
        inspire=None,   # no INSPIRE institution record (queries "Central Mechanical Engineering Research", "CMERI": 0 hits)
        orcid_q='affiliation-org-name:"Central Mechanical Engineering Research Institute" OR affiliation-org-name:(CSIR-CMERI) OR '
                'ror-org-id:"https://ror.org/059h0ng81"',
        orcid_city=r"\bcmeri\b|central\s+mechanical\s+engineering",
        dblp=("cmeri|central mechanical engineering", r"\bcmeri\b|central\s+mechanical\s+engineering"),
        tenure_lag=1),
    # ------------------------------------------------------------------ csir_cimfr (PROCESS_OTHER.md §3.19)
    "csir_cimfr": dict(
        name="CSIR-Central Institute of Mining and Fuel Research", ror="https://ror.org/03vkfy293", grid="grid.505934.e",
        family="csir",
        mention=CSIR_MENTION,
        explicit_full=CIMFR_NAME,
        # another CSIR lab named (CSIR-HRDC, CSIR-NEERI at Nagpur, CSIR-ITR (ASSIST), CSIR-NML ...)
        confusable=_others(r"cimfr|central\s+institute\s+of\s+mining|mining",
                           (r"mining\s+(and|&)\s+fuel|", ""),
                           (r"crri|cimfr|", r"crri|")),
        # hits 2016-2026: CIMFR 61, Digwadih 49, 828108 43, 826015 26, 826001 35, Barwa 45, Dhanbad 5,577, CMRI 225 (collisions),
        # CFRI 20 (collisions), Telangkhedi 3, Nagpur 14,355, Bilaspur 2,524, 440001 130
        crossref=["CIMFR", "Digwadih", "828108", "826015", "826001", "Barwa", "Dhanbad", "CMRI", "CFRI", "Telangkhedi",
                  "Nagpur", "Bilaspur", "440001"],
        crossref_broad=[],
        # verified unique to CIMFR (complete scans): Digwadih, 828108, 826015, Barwa Road
        anchor=r"\bdigwadih\b|\b828\s?108\b|\b826\s?015\b|\bbarwa\s+road\b|cimfr\.nic\.in",
        # Nagpur Research Centre street; with a CSIR mention -> CIMFR (NEERI is at Nagpur but not on this street)
        city=r"\btelangkhedi\b",
        # Dhanbad and 826001 are IIT (ISM)'s too: only with a CSIR mention (no other lab named)
        shared=r"\bdhanbad\b|\b826\s?001\b",
        units=CIMFR_NAME,
        state=None,   # Jharkhand: CSIR-NML (Jamshedpur) too
        exclude=None,
        other=r"indian\s+school\s+of\s+mines|\bism\b|\biit\b|indian\s+institute\s+of\s+technology|bharat\s+coking|\bbccl\b|coal\s+india|"
              r"\bbit\s+sindri\b|sindri|binod\s+bihari|vinoba\s+bhave|koyalanchal|shaheed\s+nirmal|\bsnmmch\b|patliputra|"
              r"guru\s+nanak|p\.?\s*k\.?\s*roy|directorate\s+general\s+of\s+mines|\bdgms\b|indian\s+bureau\s+of\s+mines|"
              r"\bsail\b|tata\s+steel|"
              + GENERIC_OTHER,
        europepmc='(AFF:"Central Institute of Mining and Fuel Research" OR AFF:"Central Institute of Mining & Fuel Research" OR '
                  'AFF:"CIMFR" OR (AFF:"Digwadih") OR (AFF:"Barwa Road" AND AFF:"Dhanbad")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=['bibjson.author.affiliation:"Central Institute of Mining and Fuel Research"',
              'bibjson.author.affiliation:"CIMFR"',
              'bibjson.author.affiliation:"Dhanbad" AND bibjson.author.affiliation:"CSIR"'],
        inspire='aff:"Dhanbad, Central Fuel Res. Inst."',   # INSPIRE 903976, legacy ICN (Central Fuel Research Institute); no record for CIMFR / CMRI
        orcid_q='affiliation-org-name:"Central Institute of Mining and Fuel Research" OR affiliation-org-name:(CSIR-CIMFR) OR '
                'ror-org-id:"https://ror.org/03vkfy293"',
        orcid_city=r"\bcimfr\b|central\s+institute\s+of\s+mining|digwadih",
        dblp=("cimfr|mining and fuel research", r"\bcimfr\b|central\s+institute\s+of\s+mining"),
        tenure_lag=1),
    # ------------------------------------------------------------------ dae_barc (PROCESS_OTHER.md §4.1)
        "dae_barc": dict(
            name="Bhabha Atomic Research Centre", ror="https://ror.org/05w6wfp17", grid="grid.418304.a",
            family="dae",
            mention=DAE_MENTION,
            explicit_full=BARC_NAME,
            confusable=DAE_OTHER_UNIT,
            # Crossref hits 2016-2026 (recon_probe, logs/recon_dae_barc.tsv): BARC 1,170; Trombay 1,345; 400085 2,629; Anushaktinagar
            # 1,453; Anushakti 1,070; 400094 2,325; Bhabha 14,912 (heavy sweep: HBNI, Homi Bhabha Cancer Hospital, TIFR's Homi Bhabha Road, the
            # name-only strings "Bhabha Atomic Research Centre | Homi Bhabha National Institute"); Mumbai 53,582 and Bombay 14,497
            # NOT swept (too big: IIT Bombay, TIFR, ICT, TMC, universities; every BARC string that matters prints the name, Trombay,
            # 400085 or 400094 and is reached by those sweeps); Atomic 31,184 (rejected, generic); Kharghar 457 (colleges, ACTREC: no
            # BARC string seen), Tarapur 49 (BARC Nuclear Recycle Board / TAPS-NPCIL: reached through the name), Vizag / Visakhapatnam,
            # Kalpakkam, Mysuru: BARC outstations print the name (see recon).
            crossref=["BARC", "Trombay", "400085", "Anushaktinagar", "Anushakti", "400094", "Bhabha"],   # "Bhabha" is the heavy one (14,912)
            crossref_broad=[],
            anchor=None,   # no token unique to BARC: 400085 = also UGC-DAE CSR Mumbai Centre, Cluj-Napoca (Romania); Trombay = also
                           # UGC-DAE CSR, Tata Memorial/HBNI strings and TISS (Sion-Trombay Road, Deonar)
            # in-scope tokens shared with a few organisations: no name -> uncertain (unless a division name makes it explicit, see units)
            city=r"\btrombay\b|\b400\s?085\b|barc\.gov\.in",
            # Anushaktinagar / 400094 hold HBNI's head office, AERB, NPCIL, Heavy Water Board, Indian Nuclear Society, IITB-typo strings:
            # operator (§4.1): these are all DAE units, so a DAE mention does not place a string at BARC ("HBNI, Anushaktinagar,
            # 400094, Department of Atomic Energy" counted as BARC in the draft). Sweep-only: count only if BARC is named.
            shared=None,
            units=BARC_NAME + "|"
                  # BARC division names with Trombay / 400085 / Anushaktinagar and no name ("Technical Physics Division, Mumbai, 400085, India";
                  # "Radiochemistry Division  400085 Trombay, Mumbai India"): only BARC and UGC-DAE CSR (excluded) sit at Trombay
                  r"\b(division|section|group)\b.{0,120}(\btrombay\b|\b400\s?085\b)|"
                  r"\bnuclear\s+recycle\s+board\b(?!\s*\(?\s*npcil)|\btraining\s+school\s+complex\b.{0,60}\bbarc\b",
            state=None,   # Maharashtra has TIFR, TMC, IIT Bombay ...: no state rule
            # never BARC even with a DAE mention or a Trombay place (checked before the mention rule): the DAE neighbours at Trombay /
            # Anushaktinagar and the acronym look-alikes
            exclude=r"ugc\W{0,3}dae|consortium\s+for\s+scientific\s+research|tata\s+memorial|\bactrec\b|\btmc\b|\btmh\b|homi\s+bhabha\s+cancer|"
                    r"tata\s+institute\s+of\s+(fundamental|social)|\btifr\b|nuclear\s+power\s+corporation|\bnpcil\b|atomic\s+energy\s+regulatory|"
                    r"\baerb\b|heavy\s+water\s+board|indian\s+nuclear\s+society|board\s+of\s+radiation\s+(and|&)\s+isotope|\bbrit\b|"
                    r"babe\w*.bolyai|cluj|romania|"
                    r"beltsville|\busda\b|agricultural\s+research\s+(service|council)|\bars\b|copenhagen|big\s+anxiety|bridge\s+animal|"
                    r"barts|australia|bangladesh|dhaka|nigeria|south\s+africa|mississippi",
            # organisations at the same places that never carry a DAE mention (checked after the mention rule). HBNI alone (the
            # degree-granting university, Anushaktinagar) is never BARC: with Trombay / 400085 it would otherwise be 'uncertain'.
            other=HBNI_ONLY + r"|surface\s+modification|directorate\s+of\s+construction|v\.\s?s\.\s?bhavan|vikram\s+sarabhai\s+bhavan|"
                  + GENERIC_OTHER,
            europepmc='(AFF:"Bhabha Atomic Research Centre" OR AFF:"Bhabha Atomic Research Center" OR AFF:"B.A.R.C." OR '
                      '(AFF:"BARC" AND (AFF:"Mumbai" OR AFF:"Trombay" OR AFF:"Bombay")) OR '
                      'AFF:"National Centre for Compositional Characterisation of Materials") AND PUB_YEAR:[2016 TO 2026]',
            doaj=['bibjson.author.affiliation:"Bhabha Atomic Research Centre"',
                  'bibjson.author.affiliation:"Bhabha Atomic Research Center"',
                  'bibjson.author.affiliation:"BARC" AND bibjson.author.affiliation:"Mumbai"'],
            # INSPIRE record "Bhabha Atomic Res. Ctr." (Trombay, Van de Graaff Building)
            inspire='(aff:"Bhabha Atomic Res. Ctr." or aff:"Bhabha Atomic Research Centre")',
            orcid_q='affiliation-org-name:"Bhabha Atomic Research Centre" OR affiliation-org-name:"Bhabha Atomic Research Center" OR '
                    'ror-org-id:"https://ror.org/05w6wfp17"',
            orcid_city=r"mumbai|bombay|trombay|anushakti|visakhapatnam|vizag|tarapur|kalpakkam",
            dblp=("bhabha atomic|barc", r"bhabha\s+atomic|\bbarc\b"),
            tenure_lag=1),
    # ------------------------------------------------------------------ dae_igcar (PROCESS_OTHER.md §4.2)
        "dae_igcar": dict(
            name="Indira Gandhi Centre for Atomic Research", ror="https://ror.org/05tkzma19", grid="grid.459621.d",
            family="dae",
            mention=DAE_MENTION,
            explicit_full=IGCAR_NAME,
            # DAE_OTHER_UNIT plus the township address of all Kalpakkam DAE staff ("JRF Enclave DAE Township, Kalpakkam 603102"):
            # DAE mention + Kalpakkam + township is not decisive -> uncertain
            confusable=DAE_OTHER_UNIT + r"|dae\s+township",
            # Crossref hits 2016-2026: IGCAR 146, Kalpakkam 1,005, 603102 465, 603127 5, Kokilamedu 51 (all UGC-DAE node: rejected),
            # Kalpakam 0, Chengalpattu 1,336 / Kancheepuram 924 (districts: 3 and 1 IGCAR strings; rejected), 603104 133 (UGC-DAE node:
            # rejected), Sadras 0. Chennai 100,310 hits NOT swept (IIT Madras, hundreds of institutions; IGCAR strings print the
            # name, Kalpakkam or 603102). "Indira" 7,633 hits (IGNOU, IGIDR, Indira Gandhi colleges ... plus the IGCAR name-only strings) is swept for the
            # strings that print the name without any place.
            crossref=["IGCAR", "Kalpakkam", "603102", "603127", "Indira"],   # "Indira" 7,633 hits: the only way to reach name-only strings
            crossref_broad=[],
            anchor=None,   # Kalpakkam / 603102 are shared with BARCF, AERB-SRI, BHAVINI, NPCIL; no unique token
            city=r"\bkalpakkam\b|\b603\s?102\b|\b603127\b|igcar\.gov\.in",
            shared=None,   # Chennai (the "Chennai" printed after Kalpakkam) is a big city: sweep-less, not a place
            units=IGCAR_NAME + "|" + IGCAR_GROUPS + r"|reactor\s+research\s+cent\w*\b.{0,80}(kalpakkam|india)",
            state=None,    # Tamil Nadu: many DAE and other organisations
            # never IGCAR (checked before the name rule): the other Kalpakkam units; "BARC" counts as BARCF only when IGCAR is not
            # named in the same part (BARC Facilities strings were 116 of 1,275 Kalpakkam strings without the IGCAR name)
            exclude=r"ugc\W{0,3}dae|consortium\s+for\s+scientific\s+research|atomic\s+energy\s+regulatory|\baerb\b|safety\s+research\s+institute|"
                    r"bharatiya\s+nabhikiya|\bbhavini\b|nuclear\s+power\s+(corporation|plant)|\bnpcil\b|madras\s+atomic\s+power|"
                    r"^(?![\s\S]*(indira\s*gandhi\s+cent|\bigcar\b))[\s\S]*(\bbarcf?\b|bh?a+b+h?a+\s+atomic|nuclear\s+recycle)",
            # HBNI alone, with Kalpakkam, is not IGCAR (checked after the mention rule); organisations printing 603102 / Chengalpattu
            other=HBNI_ONLY + r"|samsung|great\s+lakes|kalpakkam\s+hospital|" + GENERIC_OTHER,
            europepmc='(AFF:"Indira Gandhi Centre for Atomic Research" OR AFF:"Indira Gandhi Center for Atomic Research" OR AFF:"IGCAR" OR '
                      '(AFF:"Kalpakkam" AND AFF:"Atomic")) AND PUB_YEAR:[2016 TO 2026]',
            doaj=['bibjson.author.affiliation:"Indira Gandhi Centre for Atomic Research"',
                  'bibjson.author.affiliation:"Indira Gandhi Center for Atomic Research"',
                  'bibjson.author.affiliation:"IGCAR"'],
            # INSPIRE record "Kalpakkam Reactor Res. Ctr." (postal address "Indira Gandhi Center for Atomic Res., DAE, Kalpakkam 603 102")
            inspire='(aff:"Kalpakkam Reactor Res. Ctr." or aff:"Indira Gandhi Centre for Atomic Research")',
            orcid_q='affiliation-org-name:"Indira Gandhi Centre for Atomic Research" OR affiliation-org-name:"Indira Gandhi Center for Atomic Research" '
                    'OR affiliation-org-name:(IGCAR) OR ror-org-id:"https://ror.org/05tkzma19"',
            orcid_city=r"kalpakkam|kancheepuram",
            dblp=("indira gandhi centre for atomic|igcar", r"indira\s+gandhi\s+cent\w*\s+for\s+atomic|\bigcar\b"),
            tenure_lag=1),
    # ------------------------------------------------------------------ dae_rrcat (PROCESS_OTHER.md §4.3)
        "dae_rrcat": dict(
            name="Raja Ramanna Centre for Advanced Technology", ror="https://ror.org/02378jc90", grid="grid.250590.b",
            family="dae",
            mention=DAE_MENTION,
            explicit_full=RRCAT_NAME,
            confusable=DAE_OTHER_UNIT,
            # Crossref hits 2016-2026: RRCAT 203; Ramanna 739 (RRCAT plus the Raja Ramanna Fellow / Chair titles: sweep for name-only
            # strings); 452013 387; 452012 67 (DAVV, IPS Academy, SAGE University: rejected); Rammana 7 (typo, all RRCAT); Indore 11,930
            # (sweep-only: DAVV, IIT Indore, IIM, medical colleges, UGC-DAE CSR ...). The name-only strings "Raja Ramanna Centre for Advanced
            # Technology | Homi Bhabha National Institute" are reached by Ramanna.
            crossref=["RRCAT", "Ramanna", "452013", "Rammana", "Indore"],
            crossref_broad=[],
            # 452013 is RRCAT's own PIN: 515 distinct strings in the first 400 Crossref rows, 508 name RRCAT; the other 7 are typos of
            # other DAE units' strings (UGC-DAE CSR Indore printing 452013, BARC's Technical Physics Division printing "Mumbai 452013") and two
            # Boston strings where RRCAT is another part. IIT Indore uses 452017 / 453552 (Khandwa Road / Simrol). Anchor (open question).
            anchor=r"\b452[\s-]?013\b",
            city=r"rrcat\.gov\.in",
            shared=None,   # Indore is sweep-only (11,930 hits): DAVV, IIT Indore, UGC-DAE CSR Indore print it
            units=RRCAT_NAME,
            state=None,    # Madhya Pradesh: UGC-DAE CSR, AMD ... no state rule
            # UGC-DAE CSR Indore (University Campus, Khandwa Road 452001/452017; one string prints 452013): never RRCAT
            exclude=r"ugc\W{0,3}dae|consortium\s+for\s+scientific\s+research",
            # HBNI alone is not RRCAT; Indore institutions; checked after the mention rule
            other=HBNI_ONLY + r"|devi\s+ahilya|\bdavv\b|ips\s+academy|sage\s+university|" + GENERIC_OTHER,
            europepmc='(AFF:"Raja Ramanna Centre for Advanced Technology" OR AFF:"Raja Ramanna Center for Advanced Technology" OR '
                      'AFF:"RRCAT" OR (AFF:"Centre for Advanced Technology" AND AFF:"Indore")) AND PUB_YEAR:[2016 TO 2026]',
            doaj=['bibjson.author.affiliation:"Raja Ramanna Centre for Advanced Technology"',
                  'bibjson.author.affiliation:"Raja Ramanna Center for Advanced Technology"',
                  'bibjson.author.affiliation:"RRCAT"'],
            # INSPIRE records "Raja Ramanna Ctr." and the legacy "Indore, Ctr. for Advanced Tech." (postal "Center for Advanced Technology, Indore")
            inspire='(aff:"Raja Ramanna Ctr." or aff:"Indore, Ctr. for Advanced Tech.")',
            orcid_q='affiliation-org-name:"Raja Ramanna Centre for Advanced Technology" OR affiliation-org-name:"Raja Ramanna Center for Advanced Technology" '
                    'OR affiliation-org-name:(RRCAT) OR ror-org-id:"https://ror.org/02378jc90"',
            orcid_city=r"indore",
            dblp=("raja ramanna centre|rrcat", r"raja\s+ramanna\s+cent|\brrcat\b"),
            tenure_lag=1),
    # ------------------------------------------------------------------ dae_niser (PROCESS_OTHER.md §4.4)
        "dae_niser": dict(
            name="National Institute of Science Education and Research", ror="https://ror.org/02r2k1c68", grid="grid.419643.d",
            family="dae",
            mention=DAE_MENTION,
            explicit_full=NISER_NAME,
            confusable=DAE_OTHER_UNIT,
            # Crossref hits 2016-2026: NISER 1,141; Jatni 941; Jatani 76 (typo, NISER and Centurion); 752050 2,038 (IIT Bhubaneswar,
            # Centurion University, XIM University, NISER); Padanpur 186 / Bhimpur 192 (Bhimpur alone also = a West Bengal college); 751005 295
            # (Institute of Physics, NISER's transit campus); Bhubaneswar 23,787 (sweep-only; the cache is shared with IIT Bhubaneswar's
            # sweep, so it costs nothing extra) and Bhubaneshwar 902: needed for strings that print the full name without the acronym or a
            # NISER place; Khurda 634 / Khordha 299 (district: includes Bhubaneswar, rejected); Bubaneswar 13 (typo, covered by NISER).
            crossref=["NISER", "Jatni", "Jatani", "Padanpur", "752050", "751005", "Bhubaneswar", "Bhubaneshwar"],
            crossref_broad=[],
            # Padanpur (as "Bhimpur-Padanpur") is NISER's postal address: 167 distinct strings in 300 rows, 0 without NISER's name in the
            # sample. Bhimpur alone is not an anchor (a West Bengal college prints it). niser.ac.in scopes e-mail addresses only.
            anchor=r"\bpadanpur\b|\bniser\.ac\.in\b",
            # in-scope tokens shared with other organisations: Jatni / 752050 with IIT Bhubaneswar (Argul), Centurion University, XIM;
            # 751005 / Sachivalaya Marg with the Institute of Physics (see exclude). No name -> uncertain.
            city=r"\bjat(ni|ani)\b|\b752\s?050\b|\b751\s?005\b|\bsachival\w*",
            shared=None,   # Bhubaneswar is sweep-only (IIT Bhubaneswar, IOP, ILS, KIIT, Utkal ...)
            units=NISER_NAME,
            state=None,    # Odisha: IIT Bhubaneswar has the state rule; NISER none
            # never NISER: the look-alike acronym owners (unconditional), and the neighbours at NISER's places when NISER is not named in
            # the same part (IIT Bhubaneswar at Jatni / 752050, Centurion University, XIM, Jatni Degree College, the Institute of Physics
            # at 751005 / Sachivalaya Marg, Utkal). A part that names NISER together with "Institute of Physics Campus" stays NISER.
            exclude=r"nigeria|ibadan|\bnepal\b|economic\s+research|environmental\s+research|eye\s+clinic|"
                    r"^(?![\s\S]*((?<![a-z])niser(?![a-z])|national\s+institute\s+of\s+science\s+educ))[\s\S]*"
                    r"((?<![a-z])iit(?![a-z])|indian\s+institute\s+of\s+technology|\bargul\b|institute\s+of\s+physics|\biopb\b|sachivalaya|sainik\s+school|"
                    r"centurion|\bxim\b|jatni\s+degree|utkal)",
            # HBNI alone is not NISER (checked after the mention rule); other organisations of Bhubaneswar that print its PINs
            other=HBNI_ONLY + r"|institute\s+of\s+life\s+sciences|\bils\b|\bkiit\b|kalinga|siksha|" + GENERIC_OTHER,
            europepmc='(AFF:"National Institute of Science Education and Research" OR AFF:"National Institute of Science Education & Research" OR '
                      '(AFF:"NISER" AND (AFF:"Bhubaneswar" OR AFF:"Odisha" OR AFF:"Jatni" OR AFF:"HBNI"))) AND PUB_YEAR:[2016 TO 2026]',
            doaj=['bibjson.author.affiliation:"National Institute of Science Education and Research"',
                  'bibjson.author.affiliation:"National Institute of Science Education & Research"',
                  'bibjson.author.affiliation:"NISER" AND bibjson.author.affiliation:"Bhubaneswar"'],
            # INSPIRE records "NISER, Jatni" and "Bhubaneswar, NISER" (the transit campus: "Institute of Physics Campus, PO: Sainik School")
            inspire='(aff:"NISER, Jatni" or aff:"Bhubaneswar, NISER")',
            orcid_q='affiliation-org-name:"National Institute of Science Education and Research" OR affiliation-org-name:(NISER) OR '
                    'ror-org-id:"https://ror.org/02r2k1c68"',
            orcid_city=r"bhubaneswar|bhubaneshwar|jatni|jatani|khurda|khordha",
            dblp=("national institute of science education|niser", r"national\s+institute\s+of\s+science\s+educ|\bniser\b"),
            tenure_lag=1),
}
