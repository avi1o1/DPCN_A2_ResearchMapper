"""IIIT registry (IIIT team, v2; HANDOFF_IIITs.md, PROCESS_IIIT.md). Merged into institutes.REG by institutes.py.

Same fields as institutes.py, plus the institution-type fields read by affil._C:
  family        "iiit": "another institute is named" is checked among IIITs (IITs are handled by `confusable`)
  mention       how the institution type is named (replaces the IIT pattern)
  explicit_full this institute named explicitly (decisive)
  confusable    look-alike names of other organisations: IITs and the IIITs that are not registered here
Channel queries (europepmc, doaj, orcid_q, dblp) are built by _channels() the way institutes._defaults() builds them for
the IITs: campus tokens on their own, big-city tokens only together with the institute's name, plus name phrases.
First version 2026-10-27 from the reconnaissance (PROCESS_IIIT.md §1); `other` lists grow from the string review.
"""
import re

# "International / Indian / Indraprastha Institute of Information Technology" (typos: Institue, Inst., Informaton, Technolgy)
# (review 2026-10-27: "Institute for Information Technology", "Institute of Information, Technology")
NAME = r"ins\w*\.?\s+(?:(?:of|for)\s+)?info\w*\.?[\s,]*(?:and\s+)?te(?:ch|cc|hc)\w*"   # also "Tecchnology", "Information and Technology"
# Indraprastha also as "Indaprastha", "Indraprashtha" (review 2026-10-27)
INDRAPRASTHA = r"ind\w*pra\w*"
MENTION = rf"(?:inter?national|int'?l\.?|indian|{INDRAPRASTHA})\s+{NAME}|\biiit|\bi\s*\.\s*i\s*\.\s*i\s*\.\s*t\b"
# optional ", Design and Manufacturing" / "and Management" after the name
SUFFIX = r"(?:\s*,?\s*(?:design\s*,?\s*(?:and|&|&amp;)?\s*manufacturing|and\s+management))?"
# IITs never count as an IIIT (the IIT entries likewise list IIITs among their `other` organisations)
IIT_NAMES = r"indian\s+institute\s+of\s+technology\b|\biit\b|\bi\s*\.\s*i\s*\.\s*t\b"
# Other IIITs named next to their city, or by a known abbreviation (Handoff §6). Written for the first eight, when none of
# these was registered; since 2026-10-29 the 22 further IIITs are registered too, and each of them drops only its OWN names
# from these lists (_own_lists() below), so that the first eight keep exactly their previous rules (PROCESS_IIIT.md §7.2)
CITY_LIST = ["lucknow", "kota", "vadodara", r"sri\s*city", "chittoor", "guwahati", "kalyani", "bhagalpur", "agartala", "bhubaneswar",
             "bhubaneshwar", r"naya\s*raipur", r"nava\s*raipur", r"atal\s*nagar", "dharwad", "una", "sonepat", "sonipat", "kottayam",
             "manipur", "senapati", "imphal", "nagpur", "ranchi", "bhopal", "surat", "raichur", "tiruchirappalli", "tiruchirapalli",
             "trichy", "srirangam", "kurnool", "kerala", "thiruvananthapuram", "trivandrum", "basar", "nuzvid",
             r"r\.?\s*k\.?\s*valley", "ongole", "srikakulam", "kozhikode"]
ABBR_LIST = [r"\biiitm\s*-?\s*k\b", r"\biiitnr\b", r"\biiitdmk\b", r"\biiitl\b", r"\biiitv\b", r"\biiitg\b", r"\biiitk\b",
             r"\biiitbh\b", r"\biiitn\b", r"\biiitr\b", r"\biiitu\b", r"\biiitkota\b", "digital university kerala"]


def other_named(cities=CITY_LIST):
    """an unregistered IIIT named with its city is another organisation even when one of our tokens appears in the same part
    ("IIITDM Kurnool ... Combat Vehicles R&D, Avadi, Chennai"): a strong exclusion for every IIIT (review 2026-10-27)"""
    return rf"(?:\biiit\w*|{NAME}{SUFFIX})\W{{0,6}}(?:{'|'.join(cities)})\b"


def other_iiits(cities=CITY_LIST, abbrs=ABBR_LIST):
    return other_named(cities) + "|" + "|".join(abbrs)


OTHER_CITIES = "|".join(CITY_LIST)
OTHER_NAMED = other_named()
OTHER_IIITS = other_iiits()
CONFUSABLE = IIT_NAMES + "|" + OTHER_IIITS

# Neighbours of every campus that are never an IIIT (adapted from institutes.GENERIC_OTHER, without the IIIT terms)
GENERIC_OTHER = (r"indian institute of science education|\biiser\b|indian institute of science\b(?!\s*(education|and technology))|"
                 r"dental|medical college|medical sciences|hospital|pharmacy|pharmaceutical sciences|nursing|ayurved|homoeopath|unani|"
                 r"polytechnic|\bclinic\b|\bpvt\.?\s*ltd|private limited|indian institute of management|\biim\b|"
                 r"national institute of technology|\bnit\b|college|universit|public[- ]school|"
                 r"national institute of pharmaceutical|\bniper\b|\bchina\b|jiangsu|vietnam|\bp\.?\s*r\.?\s*c\b|"
                 r"\blimited\b|\bltd\b|\bllp\b|\binc\b|consultancy|independent researcher|"
                 + IIT_NAMES)   # an IIT printed with one of our tokens is a PIN typo of an IIT address (review 2026-10-27)


def explicit(first, city, abbr=None):
    """first = name variants accepted for this institute, city = its place names. Only punctuation or a bracketed
    abbreviation may stand between the name and the place ("Indian Institute of Information Technology (IIIT), Pune"): a
    wider window matched "Indian Institute of Information Technology, Dharwad, Pune" (review 2026-10-27). Looser strings still
    count through the mention rule (mention + place in the same part, nothing else named)."""
    gap = r"[\s,\-‐–—:]*(?:\(\s*[\w&.\- ]{1,12}\s*\)[\s,\-‐–—:]*)?"
    # dotted "I.I.I.T. Hyderabad" must be caught here: otherwise the IIT rule "I.I.T. Hyderabad" (inside it) wins (review)
    x = (rf"(?:{first})\s+{NAME}{SUFFIX}{gap}(?:{city})\b|\biiit\w*\W{{0,3}}(?:{city})\b|"
         rf"\bi\s*\.\s*i\s*\.\s*i\s*\.\s*t\.?\W{{0,3}}(?:{city})\b")
    return x + (f"|{abbr}" if abbr else "")


EXT = {
    "iiit_jabalpur": dict(
        name="PDPM Indian Institute of Information Technology, Design and Manufacturing Jabalpur",
        ror="https://ror.org/00gmd7q80", grid="grid.444467.1", short="Jabalpur",
        crossref=["Jabalpur", "482005", "Dumna", "PDPM", "IIITDM", "IIITDMJ"], crossref_broad=[],
        # 482005 / Dumna: to be confirmed as campus-unique in the string review -> 'city' until then
        anchor=r"\biiitdmj\.ac\.in\b", city=r"\b482005\b|\bdumna\b", shared=r"\bjabalpur\b",
        # "Indian Institute of Design and Manufacturing Jabalpur" (Information Technology dropped): review 2026-10-27
        units=r"\bpdpm\b|\biiitdmj\b|\biiitdm\s*-?\s*j\b|indian\s+institute\s+of\s+design\s*(?:and|&|&amp;)\s*manufacturing\W{0,5}jabalpur",
        explicit_full=explicit(r"indian|inter?national", r"jabalpur", r"\bpdpm\b|\biiitdmj\b"),
        state=None,   # Madhya Pradesh also has ABV-IIITM Gwalior
        # Dumna / 482005 also host the Hitkarini colleges (HCET, dental, pharmacy): review 2026-10-27
        other=r"hitkarini|\bhcet\b|madhav institute|jabalpur engineering|\bjec\b|rani durgavati|\brdvv\b|jawaharlal nehru krishi|\bjnkvv\b|netaji subhash|\bnscb\b|"
              r"gyan ganga|global engineering|takshshila|shri ram institute|vehicle factory|gun carriage|ordnance factory|khamaria|"
              r"\bdrdo\b|tropical forest|\btfri\b|\bicmr\b|tribal health|\bnirth\b|veterinary|"
              + GENERIC_OTHER,
        orcid_city=r"jabalpur", phrases=["PDPM IIITDM Jabalpur", "IIITDM Jabalpur",
                                         "Indian Institute of Information Technology Design and Manufacturing Jabalpur",
                                         "Indian Institute of Information Technology, Design and Manufacturing, Jabalpur"]),
    "iiit_gwalior": dict(
        name="ABV-Indian Institute of Information Technology and Management Gwalior",
        ror="https://ror.org/008b3ap06", grid="grid.444426.4", short="Gwalior",
        crossref=["Gwalior", "474015", "IIITM", "ABV"], crossref_broad=[],
        anchor=r"\biiitm\.ac\.in\b", city=r"\b474015\b|morena link road", shared=r"\bgwalior\b",
        units=r"\babv\b\W{0,3}(?:iiitm|indian|inst\w*|atal)|atal\s+bihari\s+vajpayee\W{0,3}(?:indian\s+)?ins\w*\.?\s+(?:of\s+)?info|"
              r"\biiitm\W{0,3}gwalior\b|\babv\s*-?\s*i{2,3}tm\b",   # ABV-IITM typo: review 2026-10-27
        # IIITM alone: also IIITM-K (Kerala); decisive only when nothing else is named in the part
        abbr=r"\biiitm\b(?!\s*-?\s*k\b)",
        explicit_full=explicit(r"indian|inter?national|abv\W{0,3}indian|atal\s+bihari\s+vajpayee\W{0,3}indian", r"gwalior",
                               r"\babv\s*-?\s*iiitm\b"),
        state=None,
        other=r"jiwaji|madhav institute|\bmits\b|itm university|institute of technology (and|&) management|amity|scindia|gajra raja|"
              r"\bgrmc\b|vikrant|lakshmibai national|\blnipe\b|\bdrde\b|defence research|\bbsf\b|\bitm\b|prestige institute|"
              r"\bipsa?\b|rustamji|veterinary|" + GENERIC_OTHER,
        orcid_city=r"gwalior", phrases=["ABV-IIITM", "ABV-IIITM Gwalior", "IIITM Gwalior",
                                        "Atal Bihari Vajpayee Indian Institute of Information Technology and Management",
                                        "ABV-Indian Institute of Information Technology and Management",
                                        "Indian Institute of Information Technology and Management Gwalior"]),
    "iiit_kancheepuram": dict(
        name="Indian Institute of Information Technology, Design and Manufacturing Kancheepuram",
        ror="https://ror.org/023c9pb11", grid="grid.504246.1", short="Kancheepuram",
        crossref=["Kancheepuram", "Kanchipuram", "Melakottaiyur", "600127", "IIITDM", "Vandalur", "Kelambakkam", "Chennai"],
        crossref_broad=[],
        # review 2026-10-27: 600127 is also printed by VIT Chennai, Bharath Institute (Selaiyur), PSVP Engineering and LifeCell;
        # Kelambakkam by Chennai Mathematical Institute, Chettinad, SMK Fomra; Vandalur by B.S. Abdur Rahman Crescent and the
        # TN wildlife institute -> 'shared' (without an IIIT mention a string there is not about IIITDM)
        # Melakottaiyur too: Tagore Engineering / Medical College, TN Physical Education and Sports University, VIT Chennai
        anchor=r"\biiitdm\.ac\.in\b", city=None,
        shared=r"\b(?:kancheepuram|kanchipuram|chennai)\b|\b600127\b|\bvandalur\b|\bkelambakkam\b|\bmelakottaiyur\b",
        units=r"\biiit\s*-?\s*d\s*(?:&|&amp;|and)?\s*m\W{0,3}(?:kancheepuram|kanchipuram|chennai)\b|"
              r"\biiidm\W{0,5}(?:kancheepuram|kanchipuram|chennai)\b",   # IIIDM typo
        explicit_full=explicit(r"indian|inter?national", r"kancheepuram|kanchipuram|chennai"),
        state=None,   # Tamil Nadu also has IIIT Tiruchirappalli
        other=r"vellore institute|\bvit\b|sri venkateswara|\bsvce\b|pallava|\bsrm\b|sathyabama|hindustan|crescent|anna university|"
              r"tagore|\bkcg\b|madha|rajalakshmi|easwari|panimalar|saveetha|chettinad|meenakshi|"
              + GENERIC_OTHER,
        orcid_city=r"kancheepuram|kanchipuram|chennai",
        phrases=["IIITDM Kancheepuram", "IIITD&M Kancheepuram",
                 "Indian Institute of Information Technology Design and Manufacturing Kancheepuram",
                 "Indian Institute of Information Technology, Design and Manufacturing, Kancheepuram"]),
    "iiit_allahabad": dict(
        name="Indian Institute of Information Technology Allahabad",
        ror="https://ror.org/03rgjt374", grid="grid.417946.9", short="Allahabad",
        crossref=["Allahabad", "Prayagraj", "Jhalwa", "Deoghat", "Devghat", "211015", "211012", "IIITA"], crossref_broad=[],
        anchor=r"\biiita\.ac\.in\b", city=r"\bjhalwa\b|\bdeoghat\b|\bdevghat\b|\b211015\b|\b211012\b",
        shared=r"\b(?:allahabad|prayagraj)\b",
        units=r"\biiit\s*-?\s*(?:allahabad|prayagraj)\b",
        abbr=r"\biiit\s*-?\s*a\b|\biiita\b",   # also IIIT Agartala
        explicit_full=explicit(r"indian|inter?national", r"allahabad|prayagraj"),
        state=None,   # Uttar Pradesh also has IIIT Lucknow
        # Jhalwa / 211015 / 211012 also host Shambhunath Institute (SIET) and VKS Agritech: review 2026-10-27
        other=r"shambhunath|\bs\.?\s*i\.?\s*e\.?\s*t\b|agritech|motilal nehru|\bmnnit\b|university of allahabad|allahabad university|harish[- ]chandra|\bhri\b|jhunsi|"
              r"sam higginbottom|\bshuats\b|kamla nehru|\biert\b|united (college|institute|group)|ewing christian|"
              r"\bicar\b|central (soil|potato)|national academy of sciences|govind ballabh pant|\bgbpssi\b|"
              + GENERIC_OTHER,
        orcid_city=r"allahabad|prayagraj", inspire='aff:"IIIT, Allahabad"',
        phrases=["IIIT Allahabad", "IIIT-Allahabad", "Indian Institute of Information Technology Allahabad"]),
    "iiit_bangalore": dict(
        name="International Institute of Information Technology Bangalore",
        ror="https://ror.org/05h9eqy10", grid="grid.435284.c", short="Bangalore",
        crossref=["Bangalore", "Bengaluru", "Banglore", "560100", "IIITB"], crossref_broad=[],
        # Electronics City / 560100 is dominated by IBAB, C-DAC, Centre for Human Genetics, XIME, Bangalore Bioinnovation Centre
        # and companies; none of 159 uncertain strings was IIIT-B (review 2026-10-27) -> 'shared'
        anchor=r"\biiitb\.(?:ac|org)\.in\b", city=None,
        shared=r"\b(?:bangalore|bengaluru|banglore|bengalore)\b|\b560100\b|electronics?\s*city",
        units=r"\biiit\s*-?\s*(?:bangalore|bengaluru|banglore)\b",
        abbr=r"\biiit\s*-?\s*b\b|\biiitb\b",   # also IIIT Bhubaneswar / Bhagalpur
        explicit_full=explicit(r"inter?national|indian", r"bangalore|bengaluru|banglore|bengalore"),
        state=None,   # Karnataka also has IIIT Dharwad and IIIT Raichur
        other=r"\breva\b|\bpes\b|infosys|wipro|\bhcl\b|biocon|siemens|tata elxsi|\bibm\b|microsoft|\bintel\b|samsung|"
              r"\bisro\b|\bdrdo\b|\bbel\b|\bhal\b|\biisc\b|\bjncasr\b|\bncbs\b|raman research|indian statistical|"
              + GENERIC_OTHER,
        orcid_city=r"bangalore|bengaluru",
        phrases=["IIIT Bangalore", "IIIT-Bangalore", "International Institute of Information Technology Bangalore"]),
    "iiit_pune": dict(
        name="Indian Institute of Information Technology Pune",
        ror="https://ror.org/01f8qyw75", grid="grid.503420.0", short="Pune",
        # campus history (roster notes, 2026-10-27): transit Sadumbare, Talegaon-Chakan Road 412109 (2016-2018); Kondhwa Annexe,
        # Yewalewadi 411048 (by 2019-2020); Ambegaon Budruk 411041 (by 2023-2025); permanent Nanoli-Tarf Chakan, Talegaon 410507
        # (from 2025). Mentor institute COEP.
        crossref=["Pune", "IIITP", "411041", "411048", "412109", "410507", "Ambegaon", "Talegaon", "Sadumbare", "Yewalewadi"],
        crossref_broad=[],
        # every candidate PIN / locality is dominated by other organisations (review 2026-10-27): 411041 Narhe (NBNSSOE, JSPM,
        # SKNCOE), 411048 Kondhwa (VIIT, NIBM, PCCM), Ambegaon (SKNMC), Nanoli (CFSL) -> 'shared': without an IIIT mention a
        # string there is not about IIIT Pune; no campus anchor except the e-mail domain
        anchor=r"\biiitp\.ac\.in\b", city=None,
        shared=r"\bpune\b|\b41104[18]\b|\b412109\b|\b410507\b|\bambegaon\b|\bnanoli\b|\btalegaon\b|\bsadumbare\b|\byewalewadi\b|"
               r"\bkondhwa\b",
        units=r"\biiit\s*-?\s*pune\b|\biiitpune\b|\biiitp\b",
        # "International Institute of Information Technology" in Pune is the private I2IT (Hinjawadi): it is NOT a mention of
        # this institute's type, so that ORCID / DBLP person matching (city AND mention) does not accept I2IT people
        mention=rf"(?:indian)\s+{NAME}|\biiit(?:p\b|\W{{0,3}}pune\b)|\bi\s*\.\s*i\s*\.\s*i\s*\.\s*t\b",
        explicit_full=explicit(r"indian", r"pune"),
        exclude=rf"international\s+{NAME}[^|;]{{0,60}}pune|\bi2it\b|i²it|isquareit|hinjawadi|hinjewadi|hope foundation",
        state=None,   # Maharashtra also has IIIT Nagpur
        other=r"vishwakarma|\baissms\b|pune institute of computer|\bpict\b|college of engineering pune|\bcoep\b|"
              r"savitribai phule|university of pune|pune university|symbiosis|bharati vidyapeeth|\bmit\b|maeer|d\.?\s*y\.?\s*patil|"
              r"sinhgad|\bniv\b|national institute of virology|\bncl\b|national chemical|\biiser\b|\bnccs\b|\bagharkar\b|"
              r"tropical meteorology|\biitm\b|\bc-?dac\b|\bdrdo\b|\barai\b|trinity academy|kj'?s|"
              + GENERIC_OTHER,
        orcid_city=r"pune",
        phrases=["IIIT Pune", "Indian Institute of Information Technology Pune", "Indian Institute of Information Technology, Pune"]),
    "iiit_delhi": dict(
        name="Indraprastha Institute of Information Technology Delhi",
        ror="https://ror.org/03vfp4g33", grid="grid.454294.a", short="Delhi",
        crossref=["Okhla", "110020", "IIITD", "Indraprastha", "Delhi"], crossref_broad=[],
        # Okhla / 110020 is dominated by DSEU's G.B. Pant campus, AcSIR, INCLEN, IHD, Sightsavers, Fortis Escorts, companies;
        # none of 100 uncertain strings without a mention was IIIT-D (review 2026-10-27) -> 'shared'
        anchor=r"\biiitd\.(?:ac|edu)\.in\b", city=None, shared=r"\b(?:new\s+)?delhi\b|\bokhla\b|\b110020\b",
        units=rf"{INDRAPRASTHA}\s+{NAME}|\biiit\s*-?\s*delhi\b|\biiitdelhi\b",
        abbr=r"\biiit\s*-?\s*d\b(?!\s*(?:&|&amp;|and)?\s*m)|\biiitd\b(?!\s*(?:&|&amp;|and)?\s*m)",   # not IIITD&M
        explicit_full=explicit(rf"{INDRAPRASTHA}|indian|inter?national", r"delhi"),
        state=None,
        other=r"guru gobind singh|\bggsipu\b|\bipu\b|indraprastha university|indraprastha apollo|indraprastha college|"
              r"indira gandhi delhi technical|\bigdtuw?\b|netaji subhas|\bnsut\b|\bnsit\b|delhi technological|\bdtu\b|jamia|"
              r"\besic\b|escorts|\bnsic\b|\baiims\b|all india institute of medical|jawaharlal nehru university|\bjnu\b|"
              r"university of delhi|delhi university|\bicmr\b|\bcsir\b|\bdrdo\b|" + GENERIC_OTHER,
        orcid_city=r"delhi",
        phrases=["IIIT Delhi", "IIIT-Delhi", "Indraprastha Institute of Information Technology"]),
    "iiit_hyderabad": dict(
        name="International Institute of Information Technology Hyderabad",
        ror="https://ror.org/05f11g639", grid="grid.419361.8", short="Hyderabad",
        crossref=["Hyderabad", "Gachibowli", "500032", "500046", "IIITH"], crossref_broad=[],
        # Gachibowli / 500032 / 500046 are dominated by NIAB, AIG hospitals, University of Hyderabad, CR Rao AIMSCS, DRILS,
        # MANUU, TIFR-H and companies; the only IIIT-H strings among 160 uncertain ones were name typos (review 2026-10-27)
        anchor=r"\biiit\.(?:ac\.in|net)\b", city=None, shared=r"\bhyderabad\b|\bgachibowli\b|\b500032\b|\b500046\b",
        units=r"\biiit\s*-?\s*hyderabad\b|\biiithyderabad\b|kohli cent(?:re|er)|cent(?:re|er) for visual information technology",
        abbr=r"\biiit\s*-?\s*h\b|\biiith\b",
        explicit_full=explicit(r"inter?national|int'?l\.?|indian", r"hyderabad"),
        state=None,   # Telangana also has IIIT Basar (RGUKT)
        other=r"university of hyderabad|\buoh\b|indian school of business|\bisb\b|osmania|\bjntu|jawaharlal nehru technological|"
              r"\bmlr\b|vardhaman|\bgnits\b|narayanamma|chaitanya bharathi|\bcbit\b|\bvnr\b|vasavi|\bcvr\b|\bbvrit\b|"
              r"\bgriet\b|gokaraju|mahindra|\bicrisat\b|\bccmb\b|\biict\b|indian institute of chemical|\bnirdpr\b|\bdrdo\b|\bdrdl\b|"
              r"tata institute of fundamental|microsoft|google|amazon|\btcs\b|infosys|wipro|\bbits\b|birla institute|"
              + GENERIC_OTHER,
        orcid_city=r"hyderabad|gachibowli", inspire='aff:"Hyderabad, IIIT"',
        phrases=["IIIT Hyderabad", "IIIT-Hyderabad", "International Institute of Information Technology Hyderabad",
                 "International Institute of Information Technology, Hyderabad"]),
}


def _own_lists(own_cities, own_abbrs):
    """CITY_LIST / ABBR_LIST without the institute's own names (an IIIT must not exclude itself); unchanged for the first
    eight, which have none"""
    for x in tuple(own_cities) + tuple(own_abbrs):
        assert x in CITY_LIST or x in ABBR_LIST, x
    return [x for x in CITY_LIST if x not in own_cities], [x for x in ABBR_LIST if x not in own_abbrs]


# --- the 22 further IIITs (2026-10-29; PROCESS_IIIT.md §7). Facts from the campus reconnaissance (§7.1): every campus a
# paper may print, including transit campuses at mentor institutes. Anchors are e-mail domains only and every place token is
# 'shared' (without an IIIT mention a string there is about another organisation), as for the first eight (§2.3). Mentor
# cities are NOT place tokens: the IIIT's own city is part of its name ("IIIT Kota, MNIT Campus, Jaipur"), and a mentor's
# city would make every loose string of that city ambiguous for the IIIT registered there (Allahabad, Hyderabad, Chennai).
ROR_NONE = None   # no ROR record (ROR v2 searched by name, city and abbreviation, 2026-10-29): R2 of orcid_roster_ids is skipped
NEW = {
    "iiit_kurnool": dict(
        name="Indian Institute of Information Technology, Design and Manufacturing Kurnool",
        ror="https://ror.org/01kw6bd80", grid=None, short="Kurnool",
        # permanent campus Jagannathagattu, Dinnedevarapadu 518008 from 2018; 2015-2018 taught at the mentor IIITDM Kancheepuram
        crossref=["Kurnool", "518008", "Jagannathagattu", "IIITDMK"], crossref_broad=[],
        anchor=r"\biiitk\.ac\.in\b", city=None, shared=r"\bkurnool\b|\b518008\b|\bjagannathagattu\b|\bdinnedevarapadu\b",
        units=r"\biiit\s*-?\s*d\s*(?:&|&amp;|and)?\s*m\W{0,3}kurnool\b",
        explicit_full=explicit(r"indian|inter?national", r"kurnool"),
        own_cities=("kurnool",), state=None,
        other=r"kurnool medical|rayalaseema|pulla reddy|\bgprec\b|\brgm\b|santhiram|\bksrm\b|ravindra college|"
              + GENERIC_OTHER,
        orcid_city=r"kurnool", phrases=["IIITDM Kurnool", "Indian Institute of Information Technology Design and Manufacturing Kurnool",
                                        "Indian Institute of Information Technology, Design and Manufacturing, Kurnool"]),
    "iiit_bhubaneswar": dict(
        name="International Institute of Information Technology Bhubaneswar",
        ror="https://ror.org/00qryer39", grid="grid.462393.9", short="Bhubaneswar",
        crossref=["Bhubaneswar", "Bhubaneshwar", "751003", "Gothapatna"], crossref_broad=[],
        # "IIIT-BH" is also IIIT Bhagalpur (iiitbh.ac.in): not a unit name; the domain here is iiit-bh.ac.in
        anchor=r"\biiit-bh\.ac\.in\b", city=None, shared=r"\bbhubanes?h?war\b|\b751003\b|\bgothapatna\b|\bmalipada\b",
        units=r"\biiit\s*-?\s*bhubanes?h?war\b",
        explicit_full=explicit(r"inter?national|indian", r"bhubanes?h?war"),
        own_cities=("bhubaneswar", "bhubaneshwar"), state=None,   # Odisha: IIT Bhubaneswar is an IIT (confusable)
        other=r"kalinga institute|\bkiit\b|siksha\W{0,3}o\W{0,3}anusandhan|\bsoa\b|utkal|\bniser\b|institute of physics|"
              r"institute of life sciences|\bimmt\b|xavier|\bximb?\b|c\.?\s*v\.?\s*raman|\bcet\b|college of engineering (and|&) technology|"
              r"silicon institute|\bouat\b|orissa university|odisha university|\bkims\b|\bsum hospital|\bicar\b|\bcifa\b|\brmrc\b|"
              + GENERIC_OTHER,
        orcid_city=r"bhubanes?h?war", phrases=["IIIT Bhubaneswar", "International Institute of Information Technology Bhubaneswar",
                                                "International Institute of Information Technology, Bhubaneswar"]),
    "iiit_naya_raipur": dict(
        name="Dr. Shyama Prasad Mukherjee International Institute of Information Technology Naya Raipur",
        ror="https://ror.org/016kfyg29", grid=None, short="Naya Raipur",
        crossref=["Raipur", "493661", "Uparwara", "IIITNR"], crossref_broad=[],
        anchor=r"\biiitnr\.(?:ac|edu)\.in\b", city=None,
        shared=r"\b(?:naya|nava)\s*raipur\b|\batal\s*nagar\b|\braipur\b|\b493661\b|\buparwara\b",
        units=r"\biiit\s*-?\s*nr\b|\biiitnr\b|\biiit\W{0,3}(?:naya|nava)\s*raipur\b|shyama\s+prasad\s+mukherjee\s+inter?national",
        explicit_full=explicit(r"inter?national|indian", r"(?:naya|nava)\s*raipur|atal\s*nagar|raipur"),
        own_cities=(r"naya\s*raipur", r"nava\s*raipur", r"atal\s*nagar"), own_abbrs=(r"\biiitnr\b",), state=None,
        other=r"pt\.?\s*ravi\s*shankar|ravishankar shukla|\bprsu\b|hidayatullah|\bhnlu\b|kalinga university|\bigkv\b|indira gandhi krishi|"
              r"\baiims\b|chhattisgarh swami|\bcsvtu\b|\bnit\b|raipur institute|\brit\b|\bmats\b|amity|\bicar\b|\bniBSM\b|"
              + GENERIC_OTHER,
        orcid_city=r"raipur|atal nagar", phrases=["IIIT Naya Raipur", "IIIT-NR", "International Institute of Information Technology Naya Raipur",
                                                   "International Institute of Information Technology, Naya Raipur"]),
    "iiit_sri_city": dict(
        name="Indian Institute of Information Technology Sri City",
        ror="https://ror.org/026873d40", grid=None, short="Sri City",
        crossref=["Chittoor", "517646", "Satyavedu", "IIITS"], crossref_broad=[],   # "Sri City" as a query is an OR on "city"
        anchor=r"\biiits\.(?:ac\.)?in\b", city=None, shared=r"\bsri\s*city\b|\bchittoor\b|\b517646\b|\bsatyavedu\b",
        units=r"\biiit\s*-?\s*sri\s*city\b|\biiit\s*-?\s*sc\b",
        explicit_full=explicit(r"indian|inter?national", r"sri\s*city|chittoor"),
        own_cities=(r"sri\s*city", "chittoor"), state=None,
        other=r"krea university|\bkrea\b|ifmr|sri venkateswara|\bsvu\b|\bsvims\b|tirupati|mohan babu|\bsvec\b|"
              + GENERIC_OTHER,
        orcid_city=r"sri ?city|chittoor", phrases=["IIIT Sri City", "Indian Institute of Information Technology Sri City",
                                                    "Indian Institute of Information Technology, Sri City"]),
    "iiit_guwahati": dict(
        name="Indian Institute of Information Technology Guwahati",
        ror="https://ror.org/00bb9ch64", grid="grid.512560.5", short="Guwahati",
        # permanent campus Bongora 781015 from July 2018; 2013-2018 transit at the Assam Textile Institute, Ambari
        crossref=["Guwahati", "Bongora", "781015", "IIITG"], crossref_broad=[],
        anchor=r"\biiitg\.ac\.in\b", city=None, shared=r"\bguwahati\b|\bbongora\b|\b781015\b|\bambari\b",
        units=r"\biiit\s*-?\s*guwahati\b",
        abbr=r"\biiitg\b",
        explicit_full=explicit(r"indian|inter?national", r"guwahati"),
        own_cities=("guwahati",), own_abbrs=(r"\biiitg\b",), state=None,   # Assam: IIT Guwahati is an IIT (confusable)
        other=r"gauhati|cotton university|\bgmch\b|gauhati medical|assam engineering|\baec\b|\biasst\b|royal global|assam down|"
              r"\badtu\b|assam science|\bniper\b|\bicar\b|textile institute|\bkkhsou\b|\bnits\b|tezpur|" + GENERIC_OTHER,
        orcid_city=r"guwahati", phrases=["IIIT Guwahati", "Indian Institute of Information Technology Guwahati",
                                         "Indian Institute of Information Technology, Guwahati"]),
    "iiit_vadodara": dict(
        name="Indian Institute of Information Technology Vadodara",
        ror="https://ror.org/0163rt176", grid="grid.495480.4", short="Vadodara",
        # works from Gandhinagar (GEC campus, Sector 28, 382028; first years at DA-IICT) and, since 2020, the Diu campus (IIITV-ICD,
        # Kevdi 362520); the permanent Dumad (Vadodara) campus had not opened by 2026. Gandhinagar is a place token although
        # it is IIT Gandhinagar's city: IITs are another family, and no other IIIT is in Gandhinagar
        crossref=["Vadodara", "Baroda", "382028", "Kevdi", "IIITV"], crossref_broad=[],
        anchor=r"\biiitvadodara\.ac\.in\b", city=None,
        shared=r"\bvadodara\b|\bbaroda\b|\bgandhinagar\b|\b382028\b|\bdiu\b|\bkevdi\b|\b362520\b",
        units=r"\biiit\s*-?\s*v(?:adodara)?\b|\biiitv\b|\biiitv\s*-?\s*icd\b",
        explicit_full=explicit(r"indian|inter?national", r"vadodara|baroda"),
        own_cities=("vadodara",), own_abbrs=(r"\biiitv\b",), state=None,
        other=r"dhirubhai ambani|\bda-?iict\b|\bdaiict\b|government engineering college|\bgec\b|maharaja sayajirao|\bmsu\b|"
              r"gujarat university|pandit deendayal|\bpdeu\b|\bpdpu\b|national forensic|\bnfsu\b|gujarat forensic|\bgfsu\b|"
              r"\bisro\b|space applications|\bsac\b|institute for plasma|\bipr\b|\bnid\b|national institute of design|\bbisag\b|"
              r"parul university|navrachana|\bgsfc\b|\bgnlu\b|\bgift city|central university of gujarat|" + GENERIC_OTHER,
        orcid_city=r"vadodara|baroda|gandhinagar", phrases=["IIIT Vadodara", "Indian Institute of Information Technology Vadodara",
                                                             "Indian Institute of Information Technology, Vadodara"]),
    "iiit_kota": dict(
        name="Indian Institute of Information Technology Kota",
        ror="https://ror.org/05dtb1875", grid=None, short="Kota",
        # 2013-2023 at the mentor MNIT Jaipur (302017); since 2023 years 1-2 at the Ranpur (Kota) campus, the rest still at MNIT
        crossref=["Kota", "IIITK"], crossref_broad=[],
        anchor=r"\biiitkota\.ac\.in\b", city=None, shared=r"\bkota\b|\branpur\b",
        units=r"\biiit\s*-?\s*kota\b|\biiitkota\b",
        explicit_full=explicit(r"indian|inter?national", r"kota"),
        own_cities=("kota",), own_abbrs=(r"\biiitkota\b",), state=None,
        # "Kota" is also an Indonesian / Malaysian word for city (Kota Bandung, Kota Kinabalu, Kota Bharu)
        other=r"university of kota|kota university|rajasthan technical|\brtu\b|career point|\bmnit\b|malaviya|government college|"
              r"indonesia|malaysia|bandung|jakarta|surabaya|malang|kinabalu|bharu|sabah|kelantan|"
              + GENERIC_OTHER,
        orcid_city=r"kota\b", phrases=["IIIT Kota", "Indian Institute of Information Technology Kota",
                                       "Indian Institute of Information Technology, Kota"]),
    "iiit_tiruchirappalli": dict(
        name="Indian Institute of Information Technology Tiruchirappalli",
        ror=ROR_NONE, grid=None, short="Tiruchirappalli",
        # 2013-2016 BIT campus, 2016-2020 NIT Trichy, 2020-2021 Oxford Engineering College; Sethurapatti 620012 from 2021
        crossref=["Tiruchirappalli", "Trichy", "Sethurapatti", "620012", "IIITT"], crossref_broad=[],
        anchor=r"\biiitt\.ac\.in\b", city=None,
        shared=r"\btiruchirapp?alli\b|\btiruchchirappalli\b|\btrichy\b|\bsethurapatti\b|\b620012\b|\bsrirangam\b",
        units=r"\biiit\s*-?\s*t(?:richy)?\b|\biiitt\b",
        explicit_full=explicit(r"indian|inter?national", r"tiruchirapp?alli|tiruchchirappalli|trichy"),
        own_cities=("tiruchirappalli", "tiruchirapalli", "trichy", "srirangam"), state=None,
        other=r"bharathidasan|\bbit campus|st\.?\s*joseph|saranathan|ramakrishna|\bsrm\b|oxford engineering|national college|"
              r"jamal mohamed|holy cross|bishop heber|periyar maniammai|\bkapv\b|\bcapv\b|mahatma gandhi memorial|\bnrcb\b|"
              + GENERIC_OTHER,
        orcid_city=r"tiruchirapp?alli|trichy", phrases=["IIIT Trichy", "IIIT Tiruchirappalli",
                                                        "Indian Institute of Information Technology Tiruchirappalli",
                                                        "Indian Institute of Information Technology, Tiruchirappalli"]),
    "iiit_una": dict(
        name="Indian Institute of Information Technology Una",
        ror="https://ror.org/02z8z1589", grid="grid.503023.7", short="Una",
        # 2014-2019/20 at the mentor NIT Hamirpur (177005); then Chandpur / Saloh, Haroli, Una 177209
        crossref=["Una", "Saloh", "Haroli", "177209", "IIITU"], crossref_broad=[],
        anchor=r"\biiitu\.ac\.in\b", city=None, shared=r"\buna\b|\bsaloh\b|\bharoli\b|\b177209\b",
        units=r"\biiit\s*-?\s*una\b|\biiitu\b",
        explicit_full=explicit(r"indian|inter?national", r"una"),
        own_cities=("una",), own_abbrs=(r"\biiitu\b",), state=None,
        # "UNA" is also the Universidad Nacional (Costa Rica, Honduras), Universidade Nova ... : FOREIGN catches few of them
        other=r"universidad|universidade|nacional|costa rica|honduras|\bnit\b|hamirpur|himachal pradesh university|"
              + GENERIC_OTHER,
        orcid_city=r"\buna\b", phrases=["IIIT Una", "Indian Institute of Information Technology Una",
                                        "Indian Institute of Information Technology, Una"]),
    "iiit_sonepat": dict(
        name="Indian Institute of Information Technology Sonepat",
        ror="https://ror.org/03c52pz66", grid=None, short="Sonepat",
        # 2014-2018 at the mentor NIT Kurukshetra; then IIT Delhi Techno Park, Rajiv Gandhi Education City, Rai 131029; from 2022
        # also the SBIT campus (Bahalgarh)
        crossref=["Sonepat", "Sonipat", "131029"], crossref_broad=[],
        anchor=r"\biiitsonepat\.ac\.in\b", city=None, shared=r"\bsonepat\b|\bsonipat\b|\b131029\b|rajiv gandhi education city",
        units=r"\biiit\s*-?\s*son[ei]pat\b",
        explicit_full=explicit(r"indian|inter?national", r"son[ei]pat"),
        own_cities=("sonepat", "sonipat"), state=None,
        other=r"ashoka university|jindal|deenbandhu chhotu ram|\bdcrust\b|\bniftem\b|national institute of food|\bbpsmv\b|"
              r"bhagat phool singh|world college|\bsbit\b|balwant|" + GENERIC_OTHER,
        orcid_city=r"son[ei]pat", phrases=["IIIT Sonepat", "Indian Institute of Information Technology Sonepat",
                                            "Indian Institute of Information Technology, Sonepat"]),
    "iiit_kalyani": dict(
        name="Indian Institute of Information Technology Kalyani",
        ror="https://ror.org/02m9zjj28", grid=None, short="Kalyani",
        # Webel IT Park, Kalyani 741235 (2014-), permanent campus on the Kalyani Expressway; mentors IIEST Shibpur, IIT Kharagpur
        crossref=["Kalyani", "741235", "IIITK"], crossref_broad=[],
        anchor=r"\biiitkalyani\.ac\.in\b", city=None, shared=r"\bkalyani\b|\b741235\b",
        units=r"\biiit\s*-?\s*kalyani\b",
        explicit_full=explicit(r"indian|inter?national", r"kalyani"),
        own_cities=("kalyani",), state=None,
        other=r"university of kalyani|kalyani university|bidhan chandra|\bbckv\b|\baiims\b|\bnibmg\b|biomedical genomics|"
              r"kalyani government engineering|\bkgec\b|jnm hospital|college of medicine|\biiser\b|\bmakaut\b|" + GENERIC_OTHER,
        orcid_city=r"kalyani", phrases=["IIIT Kalyani", "Indian Institute of Information Technology Kalyani",
                                        "Indian Institute of Information Technology, Kalyani"]),
    "iiit_lucknow": dict(
        name="Indian Institute of Information Technology Lucknow",
        ror="https://ror.org/048m7sg95", grid=None, short="Lucknow",
        # 2015-2019 at the mentor IIIT Allahabad (Jhalwa); Chak Ganjaria, Ahmamau 226002 from 2019
        crossref=["Lucknow", "226002", "Chak Ganjaria", "IIITL"], crossref_broad=[],
        anchor=r"\biiitl\.ac\.in\b", city=None, shared=r"\blucknow\b|\b226002\b|chak\s*ganjaria|\bahmamau\b",
        units=r"\biiit\s*-?\s*l(?:ucknow)?\b|\biiitl\b",
        explicit_full=explicit(r"indian|inter?national", r"lucknow"),
        own_cities=("lucknow",), own_abbrs=(r"\biiitl\b",), state=None,
        other=r"king george|\bkgmu\b|sanjay gandhi|\bsgpgi\b|\bcdri\b|central drug|\bnbri\b|botanical research|toxicology|\biitr\b|"
              r"\bcimap\b|lucknow university|university of lucknow|\baktu\b|abdul kalam technical|babasaheb|\bbbau\b|amity|"
              r"institute of engineering (and|&) technology|\biet\b|ram manohar|\brmlims\b|integral university|\bbbd\b|"
              r"\bbsip\b|birbal sahni|era university|\bbirbal\b|" + GENERIC_OTHER,
        orcid_city=r"lucknow", phrases=["IIIT Lucknow", "Indian Institute of Information Technology Lucknow",
                                        "Indian Institute of Information Technology, Lucknow"]),
    "iiit_dharwad": dict(
        name="Indian Institute of Information Technology Dharwad",
        ror="https://ror.org/0237jt454", grid=None, short="Dharwad",
        # 2015-c.2021 rented floor at the IT Park, Hubballi (580029 / 580030); Ittigatti Road, Dharwad 580009 from 2021
        crossref=["Dharwad", "580009", "580029", "Hubballi", "Hubli"], crossref_broad=[],
        anchor=r"\biiitdwd\.ac\.in\b", city=None, shared=r"\bdharwad\b|\bhubb?all?i\b|\bhubli\b|\b5800(?:09|29|30)\b|ittigatti",
        units=r"\biiit\s*-?\s*dharwad\b|\biiitdwd\b|\biiit\s*-?\s*dwd\b",
        explicit_full=explicit(r"indian|inter?national", r"dharwad|hubb?all?i|hubli"),
        own_cities=("dharwad",), state=None,   # Karnataka: IIT Dharwad is an IIT (confusable)
        other=r"karnatak university|agricultural sciences|\buas\b|\bsdm\b|\bkle\b|b\.?\s*v\.?\s*b|\bkims\b|karnataka institute of medical|"
              r"jss|\bwalmi\b|kousali|" + GENERIC_OTHER,
        orcid_city=r"dharwad|hubb?all?i|hubli", phrases=["IIIT Dharwad", "Indian Institute of Information Technology Dharwad",
                                                         "Indian Institute of Information Technology, Dharwad"]),
    "iiit_kottayam": dict(
        name="Indian Institute of Information Technology Kottayam",
        ror="https://ror.org/04mj1ps34", grid=None, short="Kottayam",
        # 2015-2016 Amal Jyothi College (Koovappally); Dec 2016-2019 GIFT campus, Thiruvananthapuram (mentor IISER TVM);
        # Valavoor, Pala 686635 from 2019
        crossref=["Kottayam", "Valavoor", "686635", "IIITK"], crossref_broad=[],
        anchor=r"\biiitkottayam\.ac\.in\b", city=None, shared=r"\bkottayam\b|\bvalavoor\b|\b686635\b|\bpala\b|\bkaroor\b",
        units=r"\biiit\s*-?\s*kottayam\b",
        explicit_full=explicit(r"indian|inter?national", r"kottayam|pala|valavoor"),
        own_cities=("kottayam",), state=None,   # Kerala also has IIITM-K / Digital University Kerala (still confusable)
        other=r"mahatma gandhi university|\bmgu\b|cms college|amal jyothi|saintgits|rubber research|\brrii\b|st\.?\s*thomas|"
              r"alphonsa|bishop|christ|\bgift\b|gulati|\biiser\b|" + GENERIC_OTHER,
        orcid_city=r"kottayam|pala\b", phrases=["IIIT Kottayam", "Indian Institute of Information Technology Kottayam",
                                                "Indian Institute of Information Technology, Kottayam"]),
    "iiit_manipur": dict(
        name="Indian Institute of Information Technology Senapati, Manipur",
        ror="https://ror.org/052ndvg69", grid="grid.502763.5", short="Manipur",
        # City Campus, Mantripukhri, Imphal 795002 (2015-); permanent campus (Senapati / Mayangkhang) under construction
        crossref=["Manipur", "Senapati", "Imphal", "795002", "Mantripukhri"], crossref_broad=[],
        anchor=r"\biiitmanipur\.ac\.in\b", city=None, shared=r"\bmanipur\b|\bsenapati\b|\bimphal\b|\b795002\b|\bmantripukhri\b",
        units=r"\biiit\s*-?\s*(?:manipur|senapati)\b|\biiitsm\b",
        explicit_full=explicit(r"indian|inter?national", r"senapati(?:\W{0,3}manipur)?|manipur|imphal"),
        own_cities=("manipur", "senapati", "imphal"), state=None,
        other=r"manipur university|\bnit\b|\brims\b|regional institute of medical|\bjnims\b|\bibsd\b|bioresources|"
              r"central agricultural|\bcau\b|dhanamanjuri|manipur technical|\bicar\b|\bdrdo\b|manipal|" + GENERIC_OTHER,
        orcid_city=r"manipur|imphal|senapati", phrases=["IIIT Manipur", "IIIT Senapati", "Indian Institute of Information Technology Manipur",
                                                         "Indian Institute of Information Technology Senapati"]),
    "iiit_nagpur": dict(
        name="Indian Institute of Information Technology Nagpur",
        ror="https://ror.org/03e2e3s57", grid="grid.502770.7", short="Nagpur",
        # 2016-2021 BSNL RTTC, Nagpur (mentor VNIT); Waranga, Butibori 441108 from 2021
        crossref=["Nagpur", "441108", "Butibori", "IIITN"], crossref_broad=[],
        anchor=r"\biiitn\.ac\.in\b", city=None, shared=r"\bnagpur\b|\b441108\b|\bbutibori\b|\bwaranga\b",
        units=r"\biiit\s*-?\s*n(?:agpur)?\b|\biiitn\b",
        explicit_full=explicit(r"indian|inter?national", r"nagpur"),
        own_cities=("nagpur",), own_abbrs=(r"\biiitn\b",), state=None,
        other=r"visvesvaraya|\bvnit\b|rashtrasant|\brtmnu\b|nagpur university|\baiims\b|\bneeri\b|environmental engineering research|"
              r"\biim\b|government medical|\bgmc\b|yeshwantrao|\bycce\b|ramdeobaba|\brcoem\b|\brknec\b|raisoni|\bghrce\b|"
              r"\bnbss|soil survey|cotton research|\bcicr\b|citrus|\bmafsu\b|laxminarayan|priyadarshini|" + GENERIC_OTHER,
        orcid_city=r"nagpur", phrases=["IIIT Nagpur", "Indian Institute of Information Technology Nagpur",
                                       "Indian Institute of Information Technology, Nagpur"]),
    "iiit_ranchi": dict(
        name="Indian Institute of Information Technology Ranchi",
        ror="https://ror.org/03desb770", grid=None, short="Ranchi",
        # 2016-2019 at the mentor NIT Jamshedpur; 2019-2024 JUT campus, Namkum 834010; from c.2024 BSNL ARTTC, Getlatu 835217
        crossref=["Ranchi", "834010", "835217", "Namkum", "IIITR"], crossref_broad=[],
        anchor=r"\biiitranchi\.ac\.in\b", city=None, shared=r"\branchi\b|\b834010\b|\b835217\b|\bnamkum\b|\bgetlatu\b|\bkanke\b",
        units=r"\biiit\s*-?\s*ranchi\b",
        explicit_full=explicit(r"indian|inter?national", r"ranchi"),
        own_cities=("ranchi",), state=None,
        other=r"birla institute|\bbit\b|mesra|ranchi university|\brims\b|rajendra institute|central university of jharkhand|\bcuj\b|"
              r"jharkhand university of technology|\bjut\b|birsa|\biim\b|\bxiss\b|xavier|\bcmpdi\b|\bicar\b|lac|indian institute of natural|"
              r"\bnit\b|jamshedpur|sarala birla|usha martin|amity|st\.?\s*xavier|" + GENERIC_OTHER,
        orcid_city=r"ranchi", phrases=["IIIT Ranchi", "Indian Institute of Information Technology Ranchi",
                                       "Indian Institute of Information Technology, Ranchi"]),
    "iiit_surat": dict(
        name="Indian Institute of Information Technology Surat",
        ror="https://ror.org/053p6zp61", grid=None, short="Surat",
        # SVNIT campus, Ichchhanath 395007 since 2017; permanent site Kamrej
        crossref=["Surat", "395007"], crossref_broad=[],
        anchor=r"\biiitsurat\.ac\.in\b", city=None, shared=r"\bsurat\b|\b395007\b|\bkamrej\b",
        units=r"\biiit\s*-?\s*surat\b",
        explicit_full=explicit(r"indian|inter?national", r"surat"),
        own_cities=("surat",), state=None,
        other=r"sardar vallabhbhai|\bsvnit\b|veer narmad|\bvnsgu\b|\bscet\b|sarvajanik|auro university|government medical|\bgmc\b|"
              r"uka tarsadia|\bc\.?\s*k\.?\s*pithawala|bhagwan mahavir|smimer|" + GENERIC_OTHER,
        orcid_city=r"surat", phrases=["IIIT Surat", "Indian Institute of Information Technology Surat",
                                      "Indian Institute of Information Technology, Surat"]),
    "iiit_bhopal": dict(
        name="Indian Institute of Information Technology Bhopal",
        ror="https://ror.org/01zhs7w23", grid=None, short="Bhopal",
        # MANIT campus, 462003 since 2017; permanent site Fatehpur Dobra not built
        crossref=["Bhopal", "462003"], crossref_broad=[],
        anchor=r"\biiitbhopal\.ac\.in\b", city=None, shared=r"\bbhopal\b|\b462003\b",
        units=r"\biiit\s*-?\s*bhopal\b",
        explicit_full=explicit(r"indian|inter?national", r"bhopal"),
        own_cities=("bhopal",), state=None,   # Madhya Pradesh also has ABV-IIITM Gwalior and IIITDM Jabalpur
        other=r"maulana azad|\bmanit\b|\baiims\b|\biiser\b|barkatullah|rajiv gandhi proudyogiki|\brgpv\b|\biifm\b|forest management|"
              r"\blnct\b|oriental|sagar institute|\bbhel\b|\bampri\b|\bnift\b|\bspa\b|planning and architecture|\bniser\b|"
              r"gandhi medical|\bgmc\b|jagran|\bicmr\b|\bnirdpr\b|\bciae\b|agricultural engineering|truba|technocrats|"
              r"people'?s university|\bvit\b|\bsirt\b|" + GENERIC_OTHER,
        orcid_city=r"bhopal", phrases=["IIIT Bhopal", "Indian Institute of Information Technology Bhopal",
                                       "Indian Institute of Information Technology, Bhopal"]),
    "iiit_bhagalpur": dict(
        name="Indian Institute of Information Technology Bhagalpur",
        ror=ROR_NONE, grid=None, short="Bhagalpur",
        # 2017-Feb 2024 at Bhagalpur College of Engineering, Sabour; own campus Rani Talab, Sabour 813210 from 2024; mentor IIT Guwahati
        crossref=["Bhagalpur", "Sabour", "813210"], crossref_broad=[],
        anchor=r"\biiitbh\.ac\.in\b", city=None, shared=r"\bbhagalpur\b|\bsabour\b|\b813210\b",
        units=r"\biiit\s*-?\s*bhagalpur\b",
        explicit_full=explicit(r"indian|inter?national", r"bhagalpur"),
        own_cities=("bhagalpur",), state=None,
        other=r"bhagalpur college of engineering|\bbce\b|bihar agricultural|\bbau\b|tilka manjhi|\btmbu\b|jawaharlal nehru medical|"
              r"\bjlnmch?\b|marwari college|" + GENERIC_OTHER,
        orcid_city=r"bhagalpur", phrases=["IIIT Bhagalpur", "Indian Institute of Information Technology Bhagalpur",
                                          "Indian Institute of Information Technology, Bhagalpur"]),
    "iiit_agartala": dict(
        name="Indian Institute of Information Technology Agartala",
        ror=ROR_NONE, grid=None, short="Agartala",
        # NIT Agartala campus, Barjala, Jirania 799046 since 2018 (mentor: NIT Agartala); permanent site Bodhjungnagar not built
        crossref=["Agartala", "Jirania", "799046"], crossref_broad=[],
        anchor=r"\biiitagartala\.ac\.in\b", city=None, shared=r"\bagartala\b|\bjirania\b|\bbarjala\b|\b799046\b|\bbodhjungnagar\b",
        units=r"\biiit\s*-?\s*agartala\b",
        explicit_full=explicit(r"indian|inter?national", r"agartala"),
        own_cities=("agartala",), state=None,   # "IIITA" is IIIT Allahabad's abbreviation, not used here
        other=r"\bnit\b|tripura university|agartala government medical|\bagmc\b|tripura medical|\btmc\b|icfai|\bicar\b|" + GENERIC_OTHER,
        orcid_city=r"agartala", phrases=["IIIT Agartala", "Indian Institute of Information Technology Agartala",
                                         "Indian Institute of Information Technology, Agartala"]),
    "iiit_raichur": dict(
        name="Indian Institute of Information Technology Raichur",
        ror=ROR_NONE, grid=None, short="Raichur",
        # 2019-2020/21 at the mentor IIT Hyderabad (Kandi 502285); then GEC campus, Yermarus Camp 584135; permanent Wadavatti
        crossref=["Raichur", "584135", "Yermarus", "IIITR"], crossref_broad=[],
        anchor=r"\biiitr\.ac\.in\b", city=None, shared=r"\braichur\b|\b584135\b|\byermarus\b|\bwadavatti\b",
        units=r"\biiit\s*-?\s*raichur\b",
        explicit_full=explicit(r"indian|inter?national", r"raichur"),
        own_cities=("raichur",), state=None,
        other=r"agricultural sciences|\buas\b|navodaya|raichur institute of medical|\brims\b|government engineering|\bgec\b|"
              r"\bslnce?t\b|" + GENERIC_OTHER,
        orcid_city=r"raichur", phrases=["IIIT Raichur", "Indian Institute of Information Technology Raichur",
                                        "Indian Institute of Information Technology, Raichur"]),
}
EXT.update(NEW)


def _channels(k, c):
    c.setdefault("family", "iiit")
    c.setdefault("mention", MENTION)
    cities, abbrs = _own_lists(c.pop("own_cities", ()), c.pop("own_abbrs", ()))
    c.setdefault("confusable", IIT_NAMES + "|" + other_iiits(cities, abbrs))
    c["exclude"] = other_named(cities) + (f"|{c['exclude']}" if c.get("exclude") else "")
    c.setdefault("inspire", None)   # INSPIRE: only IIIT Hyderabad and IIIT Allahabad have records (PROCESS_IIIT.md §1.2)
    c.setdefault("tenure_lag", 1)
    # arXiv person channel: the co-author route is not used for papers with more authors than this (precision audit
    # 2026-10-29: 23 LIGO/Virgo papers with ~1,770 authors entered IIITDM Jabalpur through a chance co-author name match)
    c.setdefault("arxiv_coauthor_max_authors", 50)
    c.pop("short")
    ph = c.pop("phrases")
    loc = re.compile("|".join(f"(?:{p})" for p in (c["anchor"], c.get("city")) if p), re.I)
    plain = [t for t in c["crossref"] if loc.search(t)]
    with_name = [t for t in c["crossref"] if t not in plain and not t.isupper()]
    tname = "Information Technology"
    epmc = ([f'AFF:"{t}"' for t in plain] + [f'(AFF:"{tname}" AND AFF:"{t}")' for t in with_name] + [f'AFF:"{p}"' for p in ph])
    c.setdefault("europepmc", "(" + " OR ".join(epmc) + ") AND PUB_YEAR:[2016 TO 2026]")
    c.setdefault("doaj", plain + [f'bibjson.author.affiliation:"{tname}" AND bibjson.author.affiliation:"{t}"' for t in with_name]
                 + [f'bibjson.author.affiliation:"{p}"' for p in ph])
    c.setdefault("orcid_q", " OR ".join([f'affiliation-org-name:"{p}"' for p in ph]
                                        + ([f'ror-org-id:"{c["ror"]}"'] if c["ror"] else [])))
    oc = c["orcid_city"]
    c.setdefault("dblp", (oc.replace(r"\b", ""), r"\b(" + oc.replace(r"\b", "") + r")\b"))
    return c


for _k in EXT:
    EXT[_k] = _channels(_k, EXT[_k])
