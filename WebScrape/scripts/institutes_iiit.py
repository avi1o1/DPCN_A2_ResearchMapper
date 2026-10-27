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
# IIITs that are not registered here (Handoff §6): named next to their city, or by a known abbreviation
OTHER_CITIES = (r"lucknow|kota|vadodara|sri\s*city|chittoor|guwahati|kalyani|bhagalpur|agartala|bhubaneswar|bhubaneshwar|"
                r"naya\s*raipur|nava\s*raipur|atal\s*nagar|dharwad|una|sonepat|sonipat|kottayam|manipur|senapati|imphal|nagpur|"
                r"ranchi|bhopal|surat|raichur|tiruchirappalli|tiruchirapalli|trichy|srirangam|kurnool|kerala|thiruvananthapuram|"
                r"trivandrum|basar|nuzvid|r\.?\s*k\.?\s*valley|ongole|srikakulam|kozhikode")
# an unregistered IIIT named with its city is another organisation even when one of our tokens appears in the same part
# ("IIITDM Kurnool ... Combat Vehicles R&D, Avadi, Chennai"): a strong exclusion for every IIIT (review 2026-10-27)
OTHER_NAMED = rf"(?:\biiit\w*|{NAME}{SUFFIX})\W{{0,6}}(?:{OTHER_CITIES})\b"
OTHER_IIITS = (OTHER_NAMED + r"|\biiitm\s*-?\s*k\b|\biiitnr\b|\biiitdmk\b|\biiitl\b|"
               r"\biiitv\b|\biiitg\b|\biiitk\b|\biiitbh\b|\biiitn\b|\biiitr\b|\biiitu\b|\biiitkota\b|digital university kerala")
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
        crossref=["Pune", "IIITP", "411041", "411048", "412109", "Ambegaon"], crossref_broad=[],
        # every candidate PIN / locality is dominated by other organisations (review 2026-10-27): 411041 Narhe (NBNSSOE, JSPM,
        # SKNCOE), 411048 Kondhwa (VIIT, NIBM, PCCM), Ambegaon (SKNMC), Nanoli (CFSL) -> 'shared': without an IIIT mention a
        # string there is not about IIIT Pune; no campus anchor except the e-mail domain
        anchor=r"\biiitp\.ac\.in\b", city=None,
        shared=r"\bpune\b|\b411041\b|\b411048\b|\b412109\b|\bambegaon\b|\bnanoli\b",
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


def _channels(k, c):
    c.setdefault("family", "iiit")
    c.setdefault("mention", MENTION)
    c.setdefault("confusable", CONFUSABLE)
    c["exclude"] = OTHER_NAMED + (f"|{c['exclude']}" if c.get("exclude") else "")
    c.setdefault("inspire", None)   # INSPIRE: only IIIT Hyderabad and IIIT Allahabad have records (PROCESS_IIIT.md §1.2)
    c.setdefault("tenure_lag", 1)
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
    c.setdefault("orcid_q", " OR ".join([f'affiliation-org-name:"{p}"' for p in ph] + [f'ror-org-id:"{c["ror"]}"']))
    oc = c["orcid_city"]
    c.setdefault("dblp", (oc.replace(r"\b", ""), r"\b(" + oc.replace(r"\b", "") + r")\b"))
    return c


for _k in EXT:
    EXT[_k] = _channels(_k, EXT[_k])
