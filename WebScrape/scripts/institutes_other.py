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


def _others(me, *own):
    """CSIR_OTHER_LAB for a lab whose own name is in the shared list: the lab's own fragments are replaced (asserted, so a
    change of CSIR_OTHER_LAB is noticed)."""
    s = CSIR_OTHER_LAB.format(me=me)
    for frag, rep in own:
        assert frag in s, frag
        s = s.replace(frag, rep, 1)
    return s


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
        # Crossref hits 2016-2026: IICT 950, Tarnaka 729, 500607 50, Habsiguda 98, 500007 2,535, Uppal 907
        crossref=["IICT", "Tarnaka", "500607", "Habsiguda", "500007", "Uppal"],
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
}
