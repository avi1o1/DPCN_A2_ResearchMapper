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
        exclude=r"structural\s+engineering\s+research|\bserc\b|central\s+leather\s+research|\bclri\b|"
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
        exclude=r"cellular\s+(and|&|&amp;)\s+molecular\s+biology|\bccmb\b|geophysical\s+research|\bngri\b|food\s+technological|\bcftri\b|"
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
        exclude=r"indian\s+institute\s+of\s+chemical\s+technology|\biict\b(?!\s*colony)|geophysical\s+research|\bngri\b|"
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
        exclude=r"ghana|accra|kumasi|south\s+africa|pretoria|defen[cs]e\s+food|\bdfrl\b|"
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
        exclude=r"central\s+road\s+research|\bcrri\b|shaheed\s+sukhdev",
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
        exclude=r"coalition|disaster|cambodia|phnom|cbrn|defen[cs]e|"
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
}
