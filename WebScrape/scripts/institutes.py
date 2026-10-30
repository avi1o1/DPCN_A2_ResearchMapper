"""Institute registry: every institute-specific fact used by the pipeline, in one place (v2, 2026-10-25).

Until v1 these facts were spread over affil.py, build_candidates.py, europepmc_aff.py, doaj_aff.py, inspire_aff.py,
orcid_people.py, dblp_people.py and roster_channels.py. The three v1 institutes are ported verbatim (regression test:
scripts/test_affil.py); the 20 IITs added in v2 were configured from the Crossref token probes and the review of
real affiliation strings recorded in PROCESS.md §15.

Fields (regexes are case-insensitive)
  name, ror, grid      official name, ROR id (api.ror.org, 2026-10-25), GRID id
  crossref             Crossref `query.affiliation` sweep tokens (single rare tokens; see PROCESS.md §3.1)
  crossref_broad       state-level sweep tokens (used only with the state rule)
  anchor               tokens that place a string AT the IIT campus (campus PIN, campus locality, e-mail domain): with a
                       department/school/centre named and no other organisation, the string counts as this IIT
  city                 further in-scope tokens shared with other organisations; without an IIT mention -> 'uncertain'
  shared               big-city tokens (Delhi, Mumbai, Chennai ...): in scope only together with an IIT mention; a string
                       with only these tokens and no IIT mention is not about this IIT at all (None), never 'uncertain'
  units                names that only exist at this IIT (count without any city token)
  state                state/UT name for the state rule (IIT mention + state, no other IIT named -> this IIT); None when
                       the state has more than one IIT (Uttar Pradesh: Kanpur, BHU)
  other                other organisations in the same city/district (never this IIT)
  europepmc, doaj, inspire, orcid_q, orcid_city, dblp   channel queries
  tenure_lag           years added to a former faculty member's last listed year (publication lag)
"""
import re

I = re.I


def rx(s):
    return re.compile(s, I) if s else None


# --- organisations that contain "Indian Institute of ..." but are not IITs, and generic organisation words
# v1 also listed "drishti" here: that is IIT Jodhpur's own iHub Drishti (now one of its units), and the bare word matched
# IIT Roorkee's Divyadrishti lab
NON_IIT = r"engineering science and technology|information technology|science education"

REG = {
    # ------------------------------------------------------------------ v1 institutes (ported verbatim)
    "iit_ropar": dict(
        name="Indian Institute of Technology Ropar", ror="https://ror.org/02qkhhn56", grid="grid.462391.b",
        crossref=["Ropar", "Rupnagar", "Roopnagar", "140001"], crossref_broad=["Punjab"],
        anchor=r"\b(ropar|rupnagar|roopnagar)\b|\b140001\b|iitrpr", city=None, shared=None,
        units=r"school of mechanical,?\s*(\||,)?\s*materials\s*(&|and)\s*energy\s*engg?\w*.*(ropar|rupnagar|punjab)|indian institute of ropar|iit\s*ropar|ihub.?awadh",
        state=r"\bpunjab\b",
        other=r"pharmacy|shivalik|lamrin|global college|saraswati nursing|aimil|bangladesh|nano science and technology\b.*mohali|"
              r"govt\.?|government|college|nursing|polytechnic|hospital|school of education|university(?!.*indian institute)|"
              r"agroparistech|ropar wetland|forest|kendriya|army|bhaddal|infrared vision|nielit|electronics and information technology|"
              r"beijing|hanoi|vietnam|china|assam|guwahati|gcet|rayat|path lab|dental|polyclinic|medical officer|"
              r"institute of engineering and technology|ch nangal",
        europepmc='(AFF:"Ropar" OR AFF:"Rupnagar" OR AFF:"Roopnagar" OR AFF:"140001") AND PUB_YEAR:[2016 TO 2026]',
        doaj=["Ropar", "Rupnagar", "Roopnagar", "140001"],
        inspire='aff:"Indian Inst. Tech., Ropar"',
        orcid_q='affiliation-org-name:(Ropar) OR affiliation-org-name:(Rupnagar) OR ror-org-id:"https://ror.org/02qkhhn56"',
        orcid_city=r"ropar|rupnagar|roopnagar",
        dblp=("ropar|rupnagar", r"\b(ropar|rupnagar|roopnagar)\b"),
        explicit=r"ropar|rupnagar|roopnagar", tenure_lag=1),
    "iit_kharagpur": dict(
        name="Indian Institute of Technology Kharagpur", ror="https://ror.org/03w5sq511", grid="grid.429017.9",
        crossref=["Kharagpur", "721302", "Khargpur", "Kgp", "Kharagapur", "Kharagur", "Kharapur", "Khragpur", "Karagpur",
                  "Kharagpu", "IITKGP"], crossref_broad=["West Bengal"],
        anchor=r"\b(kharagpur|kharagapur|kharagur|kharapur|khragpur|karagpur|khargpur|kharagpu|kgp|iitkgp)\b|\b721302\b",
        city=None, shared=None,
        units=r"vinod gupta school|rajiv gandhi school of intellectual|rajendra mishra school|g\.?\s*s\.?\s*sanyal school|ranbir (and|&) chitra gupta|"
              r"b\.?\s*c\.?\s*roy (multi|technology)|p\.?\s*k\.?\s*sinha cent|kalpana chawla space|subir chowdhury school|deysarkar cent",
        state=r"west\s*bengal|\bw\.?\s*b\.?\b",
        other=r"kharagpur college|hijli college|railway|south eastern|midnapore|medinipur|vidyasagar|prabhat kumar|"
              r"silda|ramakrishna|kgp\s*hospital|sub-?divisional|nursing|polytechnic|government|govt|"
              r"west bengal state|kendriya|airforce|air force station|\bgdc\b|bremerhaven|kazakh|phthisio|almaty|bern\b|poland|forensic|"
              r"tata steel|tata metaliks|dental|institute of chemical technology|bhubaneswar|bhatter|jadavpur|"
              r"institute of management|national institute of technology|engineering science and technology|"
              r"munger|koneru|berhmpur|berhampur|massey|kangsabati|hijli co|homoeopathic|bhawanipur|edutainment|"
              r"independent researcher|institute for clarity|college",
        europepmc='(AFF:"Kharagpur" OR AFF:"721302" OR AFF:"IIT KGP" OR AFF:"IITKGP" OR AFF:"Khargpur" '
                  'OR AFF:"Kharagapur" OR AFF:"Kharagur" OR AFF:"Kharapur" OR AFF:"Khragpur" OR AFF:"Karagpur") '
                  'AND PUB_YEAR:[2016 TO 2026]',
        doaj=["Kharagpur", "721302", "IITKGP", "Khargpur", "Kharagapur", "Kharagur", "Kharapur", "Khragpur", "Karagpur"],
        inspire='aff:"Indian Inst. Tech., Kharagpur"',
        orcid_q='affiliation-org-name:(Kharagpur) OR ror-org-id:"https://ror.org/03w5sq511"',
        orcid_city=r"kharagpur|kharagapur|khragpur|\bkgp\b",
        dblp=("kharagpur|kgp|kharagapur|khragpur", r"\b(kharagpur|kharagapur|khragpur|kgp)\b"),
        explicit=r"kharagpur|kgp|kharagapur|khargpur",
        # ICT Mumbai's IOC Odisha campus sits in the "IIT Kharagpur Extension Centre", Bhubaneswar: not IIT Kharagpur.
        # v1 documented this as 'other' (§3.2) but its IIT-first rule counted it; v2 enforces it.
        exclude=r"institute of chemical technology.{0,80}(extension|odisha|bhubaneswar)|(extension|odisha|bhubaneswar).{0,80}institute of chemical technology",
        tenure_lag=1),
    "iit_roorkee": dict(
        name="Indian Institute of Technology Roorkee", ror="https://ror.org/00582g326", grid="grid.19003.3b",
        crossref=["Roorkee", "247667", "Roorke", "Rorkee", "Saharanpur", "247001"], crossref_broad=["Uttarakhand"],
        # Saharanpur (247001) = IIT Roorkee's Saharanpur campus, but many unrelated institutions there -> 'city', not 'anchor'
        anchor=r"\b(roorkee|roorke|rorkee)\b|\b247667\b", city=r"\b(roorkie|iitr\.ac\.in|saharanpur)\b|\b247001\b", shared=None,
        # v1 also listed "mehta family school": the Mehta Family School of Data Science and AI exists at IIT Roorkee, IIT
        # Guwahati and IIT Palakkad (removed in v2, §15.4)
        units=r"iit\s*roorkee|saharanpur campus.*(iit|indian institute)|"
              r"\biitr\b.*\broorkee\b|\broorkee\b.*\biitr\b|"   # "IITR" only with Roorkee (CSIR-IITR is in Lucknow)
              r"polymer (and|&) process engineering.*(saharanpur|247001)|(saharanpur|247001).*polymer (and|&) process engineering",
        state=r"uttarakhand|uttaranchal",
        other=r"national institute of hydrology|\bnih\b|central building research|\bcbri\b|college of engineering roorkee|\bcoer\b|"
              r"roorkee institute of technology|roorkee college|quantum university|\bb\.?s\.?m\.?\b|bengal engineer|"
              r"toxicology research|csir-iitr|cdri|government|govt|medical college|hospital|polytechnic|nursing|pharmacy|"
              r"maa shakumbhari|glocal university|j\.?\s*v\.?\s*jain|munna lal|tula|college|uttar pradesh technical|"
              r"irrigation research institute|\bciet\b|army|cantonment|motherhood|motherwood|haridwar university|patanjali|arogyam|"
              r"shobhit|adarsh vijendra|pulp (and|&|&amp;) paper research|cppri|tarawati|pritam|suraksha|parenterals|green grahi|"
              r"private practice|east china|forest research institute|galgotias|\brims\b|pvt|ltd|universit|research institute|"
              r"national institutt?e of technology|paramedical|foundation",
        europepmc='(AFF:"Roorkee" OR AFF:"247667" OR AFF:"Roorke" OR AFF:"Rorkee" OR AFF:"IIT Roorkee" OR AFF:"iitr.ac.in" OR '
                  '(AFF:"Saharanpur" AND AFF:"Indian Institute of Technology")) AND PUB_YEAR:[2016 TO 2026]',
        doaj=["Roorkee", "247667", "Roorke", "Rorkee", "Saharanpur", "247001"],
        inspire='aff:"IIT, Roorkee"',
        orcid_q='affiliation-org-name:(Roorkee) OR ror-org-id:"https://ror.org/00582g326"',
        orcid_city=r"roorkee|roorke|rorkee|saharanpur",
        dblp=("roorkee|roorke|rorkee", r"\b(roorkee|roorke|rorkee)\b"),
        explicit=r"roorkee|roorke|rorkee",
        # former-faculty end years are lower bounds (archive gaps, rosters/notes) -> +4
        tenure_lag=4),
}

# ---------------------------------------------------------------------------------------------- v2 institutes
# Configured 2026-10-25 from the Crossref probes (PROCESS.md §15.2); `other` lists grow from the string review (§15.4).
_NEW = {
    "iit_bombay": dict(explicit=r"bombay|mumbai|powai", ror="https://ror.org/02qyf5152", grid="grid.417971.d", short="Bombay",
        crossref=["Powai", "400076", "Bombay", "Mumbai", "IITB"], crossref_broad=["Maharashtra"],
        anchor=r"\bpowai\b|\b400076\b|\biitb\.ac\.in\b", city=None, shared=r"\b(bombay|mumbai)\b",
        units=r"\biit\s*-?\s*bombay\b|\biitbombay\b|idc school of design|industrial design cent(re|er).*(bombay|powai)|"
              r"shailesh j\.?\s*mehta school|kanwal rekhi school|centre for technology alternatives for rural areas|\bctara\b|"
              r"cent(re|er) of studies in resources engineering|koita cent(re|er) for digital health|desai sethi school|"
              r"iitb\s*-?\s*monash|monash research academy",
        abbr=r"\biitb\b(?!\s*(&|&amp;)\s*m)",
        # SAMEER (MeitY) sits on the IIT Bombay campus but is a separate organisation; IITB-Monash Research Academy students are
        # IIT Bombay PhD students and count (review §15.4)
        exclude=r"\bsameer\b|society for applied microwave",
        state=r"\bmaharashtra\b", other=r"\bnitie\b|national institute of industrial engineering|hiranandani|larsen|\bl\s*&\s*t\b|"
              r"tata consultancy|aranca|good food institute|monad nanotech|shoulder and knee|larson",
        orcid_city=r"bombay|mumbai|powai"),
    "iit_madras": dict(explicit=r"madras|chennai|zanzibar", ror="https://ror.org/03v0r5n49", grid="grid.417969.4", short="Madras",
        crossref=["Madras", "600036", "Chennai", "IITM", "Guindy", "Zanzibar"], crossref_broad=["Tamil"],
        # 600036 is also printed by the Cancer Institute (WIA), IMSc, ARCI, VIT Chennai, CSIR-CEERI ... and Zanzibar hosts many
        # Tanzanian bodies -> no department-rule anchor except the e-mail domain (review §15.4). "Institute of Technology Madras"
        # (word order; Anna University's college is "Madras Institute of Technology") and "IITM ... Chennai" (IITM alone is
        # the Indian Institute of Tropical Meteorology, Pune) are IIT Madras
        exclude=r"research park",   # tenants of the IITM Research Park (ARCI centres, Pfizer, TCS, ERNET, DRDO RIC) are not IIT Madras
        anchor=r"\biitm\.ac\.in\b", city=r"\b600036\b", shared=r"\b(madras|chennai|guindy|zanzibar)\b",
        units=r"\biit\s*-?\s*madras\b|\biitmadras\b|robert bosch cent(re|er) for data science|wadhwani school of data science|"
              r"(?<!madras )\binstitute of technology,?\s*\(?\s*madras\b|\biitm\b.{0,40}(chennai|madras|600036)|(chennai|madras|600036).{0,40}\biitm\b",
        state=r"tamil\s*nadu", other=r"university of madras|madras medical|madras christian|madras veterinary|madras institute of technology|"
              r"madras diabetes|madras school of economics|anna university|college of engineering,?\s*guindy|\bstate university of zanzibar\b|\bsuza\b|"
              r"cancer institute|\bwia\b|mathematical sciences|\bimsc\b|\barci\b|powder metallurgy|vellore institute|\bvit\b|"
              r"indian statistical|\bceeri\b|\bcsir\b|carnatic|central leather|tanzania|malaria|ministry of health",
        orcid_city=r"madras|chennai|zanzibar"),
    "iit_delhi": dict(explicit=r"delhi|new delhi|abu dhabi", ror="https://ror.org/049tgcd06", grid="grid.417967.a", short="Delhi",
        crossref=["Delhi", "Hauz", "110016", "IITD", "Abu Dhabi", "Sonipat", "Jhajjar"], crossref_broad=[],
        # Hauz Khas / 110016 is an institutional area (PHFI-CCDC, FORE, DST Technology Bhavan, IIFT, WRI, The Union, NIFT,
        # NCERT, ISI ...) and 110016 is also Shenyang's postcode -> no department-rule anchor except the e-mail domain (§15.4)
        anchor=r"\biitd\.(ac|ernet)\.in\b", city=r"hauz\s*khas|\b110016\b", shared=r"\bdelhi\b|abu\s*dhabi|\bsonipat\b|\bjhajjar\b",
        units=r"\biit\s*-?\s*delhi\b|\biitdelhi\b|iit\s*delhi\s*-?\s*abu\s*dhabi|uq\s*-?\s*iitd",
        abbr=r"\biitd\b(?!\s*(&|&amp;)\s*m)",
        state=None, other=r"national institute of fashion technology|\bnift\b|ncert|indian statistical institute|\bisi\b|"
              r"jawaharlal nehru university|\bjnu\b|all india institute of medical|\baiims\b|indraprastha|\biiit\b|university of delhi|delhi university|"
              r"chronic disease control|public health foundation|\bphfi\b|fore school|department of science and technology|technology bhavan|"
              r"foreign trade|\biift\b|world resources institute|tuberculosis|the union|nutrition|society for applied studies|\bnlr\b|"
              r"sitaram bhartia|mediworld|quazar|journal of visualized|\bcarpl\b|shenyang|chinese academy|qutab institutional|qutub institutional|"
              r"safdarjung development|sarvapriya|\bfoundation\b",
        orcid_city=r"delhi|abu dhabi"),
    "iit_kanpur": dict(explicit=r"kanpur", ror="https://ror.org/05pjsgx75", grid="grid.417965.8", short="Kanpur",
        crossref=["Kanpur", "208016", "IITK", "Kalyanpur"], crossref_broad=[],
        # Kalyanpur is also an IIT (ISM) address in Dhanbad and a Lucknow locality -> 'shared'
        anchor=r"\b208016\b|\biitk\.ac\.in\b", city=None, shared=r"\bkanpur\b|\bkalyanpur\b",
        units=r"\biit\s*-?\s*kanpur\b|\biitkanpur\b|gangwal school of medical",
        abbr=r"\biitk\b(?!\s*(&|&amp;)\s*m)",
        state=None, other=r"harcourt butler|\bhbtu\b|chhatrapati shahu|\bcsjm|gsvm|ganesh shankar vidyarthi|national sugar institute|"
              r"pulses research|\biipr\b|chandra shekhar azad university|rama university|pranveer singh|\bpsit\b|kanpur university|"
              r"\bdmsrde\b|defence materials|\bdrdo\b",
        orcid_city=r"kanpur"),
    "iit_guwahati": dict(explicit=r"guwahati|gauhati", ror="https://ror.org/0022nd079", grid="grid.417972.e", short="Guwahati",
        crossref=["Guwahati", "781039", "Amingaon", "IITG", "Gauhati", "Guwahat", "Guwahti"], crossref_broad=["Assam"],
        # North Guwahati / Amingaon also host GNRC hospital, the Guwahati Biotech Park and an industrial park (review §15.4)
        anchor=r"\b781039\b|\biitg\.(ac|ernet)\.in\b", city=r"north\s+guwahati|\bamingaon\b", shared=r"\b(guwahati|gauhati|guwahat|guwahti)\b",
        units=r"\biit\s*-?\s*guwahati\b|\biitguwahati\b",
        abbr=r"\biitg\b(?!\s*(&|&amp;)\s*m)",
        state=r"\bassam\b", other=r"gauhati university|guwahati university|gauhati medical|\bgmch\b|cotton (college|university)|"
              r"institute of advanced study in science and technology|\biasst\b|niper|national institute of pharmaceutical|"
              r"aiims|all india institute of medical|assam don bosco|royal global|assam down town|\bnit\b|national institute of technology|"
              r"\bgnrc\b|guwahati neurological|biotech park|eris lifesciences|industrial park|malaria|biosciences \(opc\)",
        orcid_city=r"guwahati|gauhati"),
    "iit_hyderabad": dict(explicit=r"hyderabad", ror="https://ror.org/01j4v3x97", grid="grid.459612.d", short="Hyderabad",
        crossref=["Hyderabad", "Kandi", "Sangareddy", "Sangareddi", "502285", "502284", "502205", "Medak", "Yeddumailaram", "IITH"],
        crossref_broad=["Telangana"],
        # Kandi mandal also hosts Aurobindo Pharma's research centre and an agricultural engineering college; Sangareddy and
        # Medak are districts (B V Raju Institute of Technology, pharma plants); the ODF estate at Yeddumailaram (502205,
        # the IIT's campus until 2015) is also the Ordnance Factory -> only the campus PINs are anchors (review §15.4)
        anchor=r"\b50228[45]\b|\biith\.ac\.in\b", city=r"\bkandi\b|\b502205\b|\byeddumailaram\b|ordnance factory estate",
        shared=r"\bhyderabad\b|\b(sangareddy|sangareddi|sanga\s*reddy|medak)\b",
        units=r"\biit\s*-?\s*hyderabad\b|\biithyderabad\b",
        abbr=r"\biith\b(?!\s*(&|&amp;)\s*m)",
        state=r"\btelangana\b", other=r"university of hyderabad|\buoh\b|international institute of information|\biiit\b|osmania|jntu|"
              r"jawaharlal nehru technological|icrisat|ccmb|cellular and molecular biology|\biict\b|indian institute of chemical technology|"
              r"national institute of nutrition|\bdrdo\b|\bdrdl\b|\bnirdpr\b|bits pilani|birla institute|\bisb\b|indian school of business|"
              r"\bkandi\b.*(west bengal|murshidabad)|kandi,?\s*(raj|college)|aurobindo|\bpharma\b|laborator(y|ies)\s*\(?p?\)?\.?\s*(ltd|limited)|"
              r"\bgitam\b|\barci\b|powder metallurgy|tata institute of fundamental|wisig",
        orcid_city=r"hyderabad|kandi|sangareddy|medak"),
    "iit_bhubaneswar": dict(explicit=r"bhubaneswar|bhubaneshwar|bhubhaneswar|bbs", ror="https://ror.org/04gx72j20", grid="grid.459611.e", short="Bhubaneswar",
        crossref=["Bhubaneswar", "Bhubaneshwar", "Bhubneswar", "Bhubhaneswar", "Argul", "Jatni", "752050", "751013", "IITBBS"],
        crossref_broad=["Odisha", "Orissa"],
        # Jatni 752050 = IIT (Argul) and NISER; 751013 (Samantapuri, the IIT's campus until 2015) = CSIR-IMMT, ICT-IOC
        anchor=r"\bargul\b|\biitbbs\.ac\.in\b", city=r"\bjatni\b|\bkhordha\b|\b752050\b|\b751013\b|\bsamantap?uri\b|toshali bhawan",
        shared=r"\b(bhubaneswar|bhubaneshwar|bhubneswar|bhubhaneswar)\b",
        units=r"\biit\s*-?\s*(bbs|bhubaneswar|bhubaneshwar)\b|\biitbbs\b",
        state=r"\b(odisha|orissa)\b", other=r"niser|national institute of science education|\bniser\b|\bimmt\b|minerals\s*(and|&)\s*materials|"
              r"institute of chemical technology|\bict\s*-?\s*ioc\b|indian\s*oil odisha|national institute of science,?\s*education|"
              r"institute of minerals|national aluminium|\bnalco\b|indian institute of public health|public health foundation|"
              r"institute of physics|\biop\b|institute of life sciences|\bils\b|utkal|\bkiit\b|kalinga institute|siksha|\bsoa\b|"
              r"xavier|aiims|all india institute of medical|\bcipt\b|\bnit\b|national institute of technology|iiit bhubaneswar|"
              r"international institute of information|\bicar\b|central institute of freshwater|\bcifa\b|\bcutm\b|centurion university",
        orcid_city=r"bhubaneswar|bhubaneshwar|argul"),
    "iit_gandhinagar": dict(explicit=r"gandhinagar", ror="https://ror.org/0036p5w23", grid="grid.462384.f", short="Gandhinagar",
        crossref=["Gandhinagar", "Palaj", "382355", "Chandkheda", "382424", "IITGN", "Gandhinager"], crossref_broad=["Gujarat"],
        # Palaj 382355 also hosts NIPER Ahmedabad and Gujarat Biotechnology University; Chandkheda 382424 (VGEC, the IIT's
        # campus until 2015) hosts GTU, VGEC and a medical college -> no campus anchor except the e-mail domain (review §15.4)
        anchor=r"\biitgn\.ac\.in\b", city=r"\bpalaj\b|\b382355\b", shared=r"\bgandhinag[ae]r\b|\bchandkheda\b|\b382424\b",
        units=r"\biit\s*-?\s*(gn|gandhinagar)\b|\biitgn\b|\biitgandhinagar\b",
        state=r"\bgujarat\b", other=r"dhirubhai ambani|\bdaiict\b|\bdau\b|pandit deendayal|\bpdeu\b|\bpdpu\b|gujarat forensic|"
              r"national forensic|\bnfsu\b|central university of gujarat|gujarat university|institute of seismological|\bisr\b|"
              r"indian institute of public health|\biiph\b|gujarat biotechnology|\bgbu\b|\bgift\b|vishwakarma government|"
              r"\bvgec\b|ahmedabad university|nirma|\bisro\b|space applications|institute for plasma research|\biter-?india\b|"
              r"gujarat technological|\bgtu\b|biotechnology university|air force station(?!.*indian institute of technology)|pharmaceutical education",
        orcid_city=r"gandhinagar|palaj"),
    "iit_jodhpur": dict(explicit=r"jodhpur|rajasthan", ror="https://ror.org/03yacj906", grid="grid.462385.e", short="Jodhpur",
        crossref=["Jodhpur", "Karwar", "342037", "342030", "342011", "IITJ", "Jodhapur"], crossref_broad=["Rajasthan"],
        anchor=r"\b342037\b|\biitj\.ac\.in\b|\bn\.?\s*h\.?\s*-?\s*6[25]\b|nagaur road|surpura bypass|karwar\W{1,5}(jodhpur|rajasthan)",
        city=r"\bkarwar\b|\b342030\b|\b342011\b",
        shared=r"\b(jodhpur|jodhapur)\b",
        units=r"\biit\s*-?\s*jodhpur\b|\biitjodhpur\b|ihub\s*-?\s*drishti",
        abbr=r"\biitj\b(?!\s*(&|&amp;)\s*m)",
        state=r"\brajasthan\b", other=r"aiims|all india institute of medical|mbm|jai narain vyas|\bjnvu\b|central arid zone|\bcazri\b|"
              r"defence laboratory|\bdlj\b|national law university|\bnlu\b|dr\.?\s*s\.?\s*n\.?\s*medical|\bnift\b|"
              r"\bkarwar\b.*(karnataka|uttara kannada)|agriculture university|arid forest|\bafri\b|\bicar\b|"
              r"national institute of fashion|lachoo|\bmgh\b|jodhpur national university|defen[cs]e lab|\bdrdo\b|defen[cs]e research|"
              r"central marine fisheries|\bcmfri\b|karwar (research|regional)|karnataka|collage",
        orcid_city=r"jodhpur"),
    "iit_patna": dict(explicit=r"patna", ror="https://ror.org/01ft5vz71", grid="grid.459592.6", short="Patna",
        crossref=["Patna", "Bihta", "801106", "801103", "800013", "Amhara", "IITP"], crossref_broad=["Bihar"],
        # Bihta also hosts NSMCH, ESIC Medical College, NSIT, NIELIT and CIPET; "Amhara" is mostly the Ethiopian region and
        # Patliputra 800013 hosts NGOs and state boards (review §15.4)
        anchor=r"\b80110[36]\b|\biitp\.ac\.in\b", city=r"\bbihta\b",
        shared=r"\bpatna\b|\b800013\b|\bamhara\b|navin government polytechnic|patliputra",
        units=r"\biit\s*-?\s*patna\b|\biitpatna\b",
        abbr=r"\biitp\b(?!\s*(&|&amp;)\s*m)",
        state=r"\bbihar\b", other=r"aiims|all india institute of medical|patna university|patna medical|\bpmch\b|\bnit\b|"
              r"national institute of technology|indira gandhi institute of medical|\bigims\b|rajendra memorial|\brmrims\b|"
              r"chanakya national law|aryabhatta knowledge|\bicar\b|research complex for eastern|niper|national institute of pharmaceutical|"
              r"\bamhara\b.*(ethiopia|bahir dar|gondar|regional)|ethiopia|bahir dar|gondar|debre|woldia|wollo|"
              r"netaji subhash?|\bnsmch\b|\bnsit\b|\besic\b|\bnielit\b|national institute of electronics|central institute of petrochemicals|\bcipet\b|\bipt\b|esicmch|nscmch",
        orcid_city=r"patna|bihta"),
    "iit_indore": dict(explicit=r"indore", ror="https://ror.org/01hhf7w52", grid="grid.450280.b", short="Indore",
        crossref=["Indore", "Simrol", "453552", "452017", "Khandwa", "IITI"], crossref_broad=["Madhya"],
        # Khandwa Road / 452017 (the IIT's campus until 2015, at IET-DAVV) also hosts DAVV's Takshashila campus and UGC-DAE CSR
        anchor=r"\bsimrol\b|\b453552\b|\biiti\.ac\.in\b", city=None, shared=r"\bindore\b|\b452017\b|khandwa road",
        units=r"\biit\s*-?\s*indore\b|\biitindore\b",
        abbr=r"\biiti\b(?!\s*(&|&amp;)\s*m)",
        state=r"madhya\s*pradesh|\bm\.?\s*p\.?\b(?=.*india)", other=r"devi ahilya|\bdavv\b|raja ramanna|\brrcat\b|shri govindram seksaria|"
              r"\bsgsits\b|mahatma gandhi memorial|\bmgm\b|indian institute of management|\biim\b|medicaps|acropolis|"
              r"prestige institute|symbiosis|\bips academy\b|sri aurobindo|choithram|index medical|\bicar\b|soybean research|"
              r"khandwa (?!road)|institute of engineering and technology|ugc\s*-?\s*dae|consortium for scientific research|takshashila",
        orcid_city=r"indore|simrol"),
    "iit_mandi": dict(explicit=r"mandi", ror="https://ror.org/05r9r2f34", grid="grid.462387.c", short="Mandi",
        crossref=["Mandi", "Kamand", "175005", "175075", "175001", "Kataula"], crossref_broad=["Himachal"],
        anchor=r"\bkamand\b|\b1750(05|75)\b|\biitmandi\.ac\.in\b|\bkataula\b", city=r"\b175001\b", shared=r"\bmandi\b",
        units=r"\biit\s*-?\s*mandi\b|\biitmandi\b|indian institute of mandi",
        state=r"himachal", other=r"mandi gobindgarh|gobindgarh|mandi dabwali|mandi adampur|sardar patel university|"
              r"lal bahadur shastri|medical college|nerchowk|ner chowk|vallabh|\bmandi house\b|mandi bahauddin|pakistan|"
              r"sabzi mandi|krishi upaj mandi|grain mandi|\bmandi\b.*(punjab|haryana|rajasthan|uttar pradesh)",
        orcid_city=r"mandi|kamand"),
    "iit_bhu": dict(explicit=r"bhu|banaras hindu university|varanasi", ror="https://ror.org/01kh5gc44", grid="grid.467228.d", short="BHU",
        crossref=["Varanasi", "221005", "BHU", "Banaras", "Benaras", "Benares", "Kashi"], crossref_broad=[],
        # 221005 is the whole BHU campus (university + IIT): not an anchor. The IIT is identified by an IIT mention,
        # the old name "Institute of Technology, BHU" (IT-BHU), or an engineering department with BHU (§15.4)
        anchor=r"\biitbhu\.ac\.in\b", city=r"\b(bhu|banaras|benaras|benares)\b|\b221005\b", shared=r"\b(varanasi|kashi)\b",
        units=r"\biit\s*-?\s*\(?\s*bhu\b|\biitbhu\b|indian institute of technology\s*,?\s*\(?\s*(banaras|bhu)|"
              r"(?<!indian )\binstitute of technology\s*,?\s*\(?\s*(banaras hindu university|bhu)\b|\bit\s*-?\s*bhu\b|"
              r"indian institute of technology\s*\[\s*iit\s*;\s*banaras|"
              r"(ceramic|metallurgical|mining|chemical|civil|electrical|mechanical|biochemical|biomedical|pharmaceutical)\s+engineering.{0,60}\b(bhu|banaras hindu)|"
              r"computer science (and|&) engineering.{0,60}\b(bhu|banaras hindu)|school of materials science (and|&) technology|"
              r"school of biochemical engineering|school of biomedical engineering|engineering physics.{0,60}\b(bhu|banaras hindu)",
        state=None, other=r"institute of science|institute of medical sciences|\bims\b|institute of agricultural sciences|"
              r"institute of environment|faculty of|mahila maha|sir sunderlal|\bssl hospital|dst centre for interdisciplinary|"
              r"institute of management studies|centre for genetic disorders|\bmmv\b|\bi\.?\s*a\.?\s*s\b|\bi\.?\s*ag\.?\s*scs?\b|\bi\.?\s*m\.?\s*s\b|"
              r"\bfods\b|\brgsc\b|cims|interdisciplinary and mathematical sciences|agricultural|veterinary|"
              r"mahamana|indian institute of vegetable|\biivr\b|kashi vidyapith|sampurnanand|\bupc\b|udai pratap|"
              r"homi bhabha cancer|international rice research|\birri\b|college|hospital|vasanta|karachi|pakistan",
        # parts of the IIT's official name that must not block the whole-string rescue (affil._judge)
        name_parts=r"\(?\s*(banaras hindu university|b\.?\s*h\.?\s*u\.?)\s*\)?",
        # without an IIT mention, a BHU string is the university unless it names a department both have (§15.4)
        ambiguous_depts=r"\b(chemistry|physics|mathematic\w*|humanistic|architecture)\b",
        orcid_city=r"varanasi|banaras|bhu"),
    "iit_palakkad": dict(explicit=r"palakkad|palghat", ror="https://ror.org/0264cg909", grid="grid.494639.5", short="Palakkad",
        crossref=["Palakkad", "Palghat", "Kanjikode", "678623", "678557", "Kozhippara", "Pudussery", "Ahalia", "IITPKD"],
        crossref_broad=["Kerala"],
        # 678557 / Kozhippara / Pudussery = the Ahalia Integrated Campus, which hosted the IIT 2015-2023 but also Ahalia's own
        # schools; Kanjikode is an industrial area (BHEL, Instrumentation Ltd) -> 'city', not 'anchor' (review §15.4)
        anchor=r"\b678623\b|\biitpkd\.ac\.in\b", city=r"\bkanjikode\b|\b678557\b|\bkozhippara\b|\bpudussery\b|ahalia",
        shared=r"\b(palakkad|palghat)\b",
        units=r"\biit\s*-?\s*(pkd|palakkad)\b|\biitpkd\b",
        state=r"\bkerala\b", other=r"ahalia(?! integrated campus)|nss college|government (victoria|engineering|medical)|"
              r"mercy college|jawaharlal college|\bnehru college\b|\bbhel\b|kerala agricultural|instrumentation limited|pharmacy",
        orcid_city=r"palakkad|palghat"),
    "iit_tirupati": dict(explicit=r"tirupati|tirupathi", ror="https://ror.org/01xtkxh20", grid="grid.494642.9", short="Tirupati",
        crossref=["Tirupati", "Tirupathi", "Yerpedu", "517619", "517506", "Renigunta", "Chindepalle", "IITTP"],
        crossref_broad=["Andhra"],
        # IISER Tirupati shares PIN 517619 and Yerpedu mandal with the IIT's permanent campus -> 'city' (review §15.4)
        anchor=r"\bchindepalle\b|\biittp\.ac\.in\b", city=r"\byerpedu\b|\b517619\b|\b517506\b|\brenigunta\b",
        shared=r"\b(tirupati|tirupathi)\b",
        units=r"\biit\s*-?\s*(tp|tirupati)\b|\biittp\b|\biittirupati\b",
        state=r"andhra\s*pradesh", other=r"sri venkateswara|\bsvu\b|\bsvims\b|padmavati|padmavathi|indian institute of science education|"
              r"\biiser\b|national atmospheric research|\bnarl\b|\bsv\b|national sanskrit|sree vidyanikethan|chadalawada|"
              r"tirumala|\bttd\b|siddharth|annamacharya|mohan babu|sri padmavathi|ayurved|buddolla|fergusson|krishna teja|theja|sri balaji",
        orcid_city=r"tirupati|yerpedu"),
    "iit_ism": dict(explicit=r"ism|indian school of mines|dhanbad", ror="https://ror.org/013v3cc28", grid="grid.417984.7", short="ISM",
        crossref=["Dhanbad", "826004", "ISM", "Mines", "Sindri", "IITISM"], crossref_broad=["Jharkhand"],
        anchor=r"\b826004\b|\biitism\.ac\.in\b|\bismdhanbad\.ac\.in\b", city=None, shared=r"\bdhanbad\b",
        units=r"indian school of mines|\biit\s*\(?\s*-?\s*ism\b|\biitism\b|\bism\s*,?\s*dhanbad\b",
        name_parts=r"\(?\s*(indian school of mines|ism)\s*\)?",
        state=r"\bjharkhand\b", other=r"central institute of mining|\bcimfr\b|\bcmri\b|central fuel research|birsa institute|\bbit\s*sindri\b|"
              r"sindri|bharat coking|\bbccl\b|coal india|binod bihari|koyalanchal|shaheed nirmal mahto|\bsnmmch\b|patliputra medical|"
              r"\bpmch\b|guru nanak college|p\.?\s*k\.?\s*roy|directorate general of mines|\bdgms\b|indian bureau of mines",
        orcid_city=r"dhanbad|indian school of mines"),
    "iit_bhilai": dict(explicit=r"bhilai", ror="https://ror.org/02sscsx71", grid="grid.494637.b", short="Bhilai",
        # 2016-2022 the institute ran from the Government Engineering College campus, Sejbahar, Raipur (492015)
        crossref=["Bhilai", "Durg", "491001", "491002", "492015", "Raipur", "Sejbahar", "Kutelabhata"], crossref_broad=["Chhattisgarh"],
        # Durg is a district with dozens of institutions; Sejbahar also hosts IIIT Bhilai and IIM Raipur -> 'shared' (review §15.4)
        anchor=r"\bkutelabhata\b|\biitbhilai\.ac\.in\b", city=None,
        shared=r"\b(bhilai|raipur|durg|sejbahar)\b|\b49100[12]\b|\b492015\b",
        units=r"\biit\s*-?\s*bhilai\b|\biitbhilai\b",
        exclude=r"naya\s*raipur|nava\s*raipur|atal\s*nagar",  # IIIT Naya Raipur, sometimes written "IIT"
        state=r"chhattisgarh|chattisgarh", other=r"bhilai steel|\bsail\b|steel authority|bhilai institute of technology|\bbit\b|"
              r"chhattisgarh swami vivekanand|\bcsvtu\b|pt\.? ravishankar|ravishankar shukla|\bnit\b|national institute of technology|"
              r"aiims|all india institute of medical|government engineering college|\bgec\b|indira gandhi krishi|hemchand|"
              r"shri shankaracharya|rungta|kalinga university|iiit naya raipur|international institute of information|\biim\b|"
              r"hidayatullah|medical college|college",
        orcid_city=r"bhilai|raipur|durg"),
    "iit_goa": dict(explicit=r"goa", ror="https://ror.org/02v7trd43", grid="grid.503024.0", short="Goa",
        crossref=["Goa", "Ponda", "Farmagudi", "403401", "403703", "Cuncolim"], crossref_broad=[],
        # Farmagudi/Ponda 403401 is shared with NIT Goa (until 2023), GEC Goa, PES and GVM colleges and NFSU's Goa campus;
        # Cuncolim 403703 is NIT Goa's permanent campus -> no campus anchor except the e-mail domain (review §15.4)
        anchor=r"\biitgoa\.ac\.in\b", city=r"\bponda\b|\bfarmagudi\b|\b403401\b|\b403703\b|\bcuncolim\b", shared=r"\bgoa\b",
        units=r"\biit\s*-?\s*goa\b|\biitgoa\b|school of (chemical and materials|mechanical|electrical|mathematics and computer|physical|interdisciplinary life) sciences?.{0,80}\binstitute of technology,?\s*goa\b",
        state=None,  # "Goa" is both the state and the shared token
        other=r"goa university|national institute of oceanography|\bnio\b|national centre for polar|\bncpor\b|\bncaor\b|bits pilani|"
              r"birla institute|goa medical college|\bgmc\b|\bnit\b|national institute of technology|goa college of engineering|"
              r"\bgec\b|central coastal agricultural|\bicar\b|goa institute of management|\bdbcs\b|\bgoa\b.*(portugal|lisbon|india goa trade)|"
              r"national forensic|\bnfsu\b|ravi s\.?\s*naik|\bp\.?\s*e\.?\s*s\b|ponda education|\bgvm|vidyaprasarak|dada vaidya|kala academy|"
              r"college|national institute of technolo?gy|engineering college|private practice|consultant|\bn\.\s*i\.\s*t\b|\bg\.\s*e\.\s*c\b|\bbits\b",
        orcid_city=r"\bgoa\b|ponda|farmagudi"),
    "iit_jammu": dict(explicit=r"jammu", ror="https://ror.org/02f0vsw63", grid="grid.499272.3", short="Jammu",
        crossref=["Jammu", "Jagti", "Jagati", "Nagrota", "181221", "Paloura"], crossref_broad=["Kashmir"],
        anchor=r"\bjagti\b|\bjagati\b|\b181221\b|\bpaloura\b|\biitjammu\.ac\.in\b", city=r"\bnagrota\b", shared=r"\bjammu\b",
        units=r"\biit\s*-?\s*jammu\b|\biitjammu\b",
        state=r"jammu\s*(and|&)\s*kashmir|\bj\s*&\s*k\b|\bkashmir\b", other=r"university of jammu|jammu university|central university of jammu|"
              r"shri mata vaishno devi|\bsmvdu\b|government medical|\bgmc\b|sher-?e-?kashmir|\bskuast\b|indian institute of integrative|"
              r"\biiim\b|aiims|all india institute of medical|\biim\b|model institute|\bmiet\b|nagrota bagwan|kangra|himachal",
        orcid_city=r"jammu"),
    "iit_dharwad": dict(explicit=r"dharwad", ror="https://ror.org/0509djg30", grid="grid.495560.b", short="Dharwad",
        crossref=["Dharwad", "580011", "580007", "WALMI", "Chikkamalligawad", "Hubli", "Hubballi"], crossref_broad=["Karnataka"],
        # the WALMI campus (580011) also hosts NFSU's Dharwad campus; 580007 is a general Dharwad PIN -> 'city' (review §15.4)
        anchor=r"\bchikkamalligawad\b|\biitdh\.ac\.in\b", city=r"\b580011\b|\b580007\b|\bwalmi\b", shared=r"\b(dharwad|hubli|hubballi)\b",
        units=r"\biit\s*-?\s*(dh|dharwad)\b|\biitdh\b|\biitdharwad\b",
        state=r"\bkarnataka\b", other=r"karnatak university|university of agricultural sciences|\buas\b|\bsdm\b|kle|b\.?\s*v\.?\s*b|"
              r"kims|karnataka institute of medical|iiit dharwad|indian institute of information|tie-?up|"
              r"water and land management institute(?!.*iit)|national forensic|\bnfsu\b|\bjss\b|powergrid|biochem research|walmi karnataka",
        orcid_city=r"dharwad"),
}


# Name phrases used in Europe PMC / DOAJ / ORCID queries (besides the campus tokens)
PHRASES = {
    "iit_bombay": ["IIT Bombay", "Indian Institute of Technology Bombay", "IIT-Bombay"],
    "iit_madras": ["IIT Madras", "Indian Institute of Technology Madras", "IIT-Madras"],
    "iit_delhi": ["IIT Delhi", "Indian Institute of Technology Delhi", "IIT-Delhi"],
    "iit_kanpur": ["IIT Kanpur", "Indian Institute of Technology Kanpur", "IIT-Kanpur"],
    "iit_guwahati": ["IIT Guwahati", "Indian Institute of Technology Guwahati", "IIT-Guwahati"],
    "iit_hyderabad": ["IIT Hyderabad", "Indian Institute of Technology Hyderabad", "IIT-Hyderabad"],
    "iit_bhubaneswar": ["IIT Bhubaneswar", "Indian Institute of Technology Bhubaneswar", "IIT-Bhubaneswar"],
    "iit_gandhinagar": ["IIT Gandhinagar", "Indian Institute of Technology Gandhinagar"],
    "iit_jodhpur": ["IIT Jodhpur", "Indian Institute of Technology Jodhpur", "Indian Institute of Technology Rajasthan"],
    "iit_patna": ["IIT Patna", "Indian Institute of Technology Patna"],
    "iit_indore": ["IIT Indore", "Indian Institute of Technology Indore"],
    "iit_mandi": ["IIT Mandi", "Indian Institute of Technology Mandi"],
    "iit_bhu": ["IIT BHU", "IIT (BHU)", "IIT-BHU", "Indian Institute of Technology (BHU)",
                "Indian Institute of Technology (Banaras Hindu University)", "Indian Institute of Technology BHU"],
    "iit_palakkad": ["IIT Palakkad", "Indian Institute of Technology Palakkad"],
    "iit_tirupati": ["IIT Tirupati", "Indian Institute of Technology Tirupati"],
    "iit_ism": ["Indian School of Mines", "IIT (ISM)", "IIT ISM", "IIT-ISM", "Indian Institute of Technology (ISM)",
                "Indian Institute of Technology (Indian School of Mines)", "Indian Institute of Technology Dhanbad"],
    "iit_bhilai": ["IIT Bhilai", "Indian Institute of Technology Bhilai"],
    "iit_goa": ["IIT Goa", "Indian Institute of Technology Goa"],
    "iit_jammu": ["IIT Jammu", "Indian Institute of Technology Jammu"],
    "iit_dharwad": ["IIT Dharwad", "Indian Institute of Technology Dharwad"],
}


# Organisations that are never an IIT, found next to many campuses in the string review (§15.4): IISERs, IISc, medical /
# dental / pharmacy / nursing colleges, hospitals, polytechnics. Appended to every v2 institute's `other`.
GENERIC_OTHER = (r"indian institute of science education|\biiser\b|indian institute of science\b(?!\s*(education|and technology))|"
                 r"dental|medical college|medical sciences|hospital|pharmacy|pharmaceutical sciences|nursing|ayurved|homoeopath|unani|"
                 r"polytechnic|\bclinic\b|\bpvt\.?\s*ltd|private limited|indian institute of management|\biim\b|"
                 r"indian institute of information technology|\biiit|national institute of technology|\bnit\b|"
                 r"college|universit|public[- ]school|national institute of pharmaceutical|\bniper\b|"
                 r"\bchina\b|jiangsu|vietnam|\bp\.?\s*r\.?\s*c\b|\blimited\b|\bltd\b|\bllp\b|\binc\b|consultancy|independent researcher")  # 6-digit PINs collide with Chinese postcodes (221005 Xuzhou)


def _defaults(k, c):
    """Channel queries of a v2 institute. Campus tokens (anchor/city) are searched on their own; shared big-city and
    noisy tokens (Delhi, Mumbai, Mines, ISM ...) only together with "Indian Institute of Technology"; name phrases always."""
    short = c.pop("short")
    c["other"] = c["other"] + "|" + GENERIC_OTHER
    nm = {"iit_bhu": "Indian Institute of Technology (BHU) Varanasi", "iit_ism": "Indian Institute of Technology (ISM) Dhanbad"}
    c.setdefault("name", nm.get(k, f"Indian Institute of Technology {short}"))
    loc = re.compile("|".join(f"(?:{p})" for p in (c["anchor"], c.get("city")) if p), re.I)
    plain = [t for t in c["crossref"] if loc.fullmatch(t) or loc.search(t)]
    with_iit = [t for t in c["crossref"] if t not in plain and not t.isupper()]
    ph = PHRASES[k]
    epmc = [f'AFF:"{t}"' for t in plain] + [f'(AFF:"Indian Institute of Technology" AND AFF:"{t}")' for t in with_iit] + [f'AFF:"{p}"' for p in ph]
    c.setdefault("europepmc", "(" + " OR ".join(epmc) + ") AND PUB_YEAR:[2016 TO 2026]")
    # DOAJ: list of query fragments (a bare token means bibjson.author.affiliation:"<token>", as in v1)
    c.setdefault("doaj", plain + [f'bibjson.author.affiliation:"Indian Institute of Technology" AND bibjson.author.affiliation:"{t}"'
                                  for t in with_iit] + [f'bibjson.author.affiliation:"{p}"' for p in ph])
    c.setdefault("inspire", None)  # INSPIRE normalised names: INSPIRE below
    anc = re.compile(c["anchor"], re.I)
    c.setdefault("orcid_q", " OR ".join([f'affiliation-org-name:"{p}"' for p in ph] + [f"affiliation-org-name:({t})" for t in plain
                                                                                    if not t.isdigit() and anc.search(t)]
                                       + [f'ror-org-id:"{c["ror"]}"']))
    oc = c["orcid_city"]
    c.setdefault("dblp", (oc.replace(r"\b", ""), r"\b(" + oc.replace(r"\b", "") + r")\b"))
    c.setdefault("tenure_lag", 1)
    return c


for _k, _c in _NEW.items():
    REG[_k] = _defaults(_k, _c)

# INSPIRE-HEP normalised affiliation names (looked up with the INSPIRE institutions API, PROCESS.md §15.3)
INSPIRE = {
    "iit_bombay": 'aff:"Indian Inst. Tech., Mumbai"', "iit_madras": 'aff:"Indian Inst. Tech., Madras"',
    "iit_delhi": 'aff:"Indian Inst. Tech., New Delhi"', "iit_kanpur": 'aff:"Indian Inst. Tech., Kanpur"',
    "iit_guwahati": 'aff:"Indian Inst. Tech., Guwahati"',
    # two INSPIRE records for IIT Hyderabad (legacy + new), and for IIT (ISM) Dhanbad (before/after the 2016 conversion)
    "iit_hyderabad": '(aff:"Indian Inst. Tech., Hyderabad" or aff:"Indian Institute of Technology Hyderabad")',
    "iit_bhubaneswar": 'aff:"Indian Inst. Tech., Bhubaneswar"', "iit_gandhinagar": 'aff:"Indian Inst. Tech., Gandhinagar"',
    "iit_jodhpur": 'aff:"IIT, Jodhpur"', "iit_patna": 'aff:"Indian Inst. Tech., Patna"', "iit_indore": 'aff:"Indian Inst. Tech., Indore"',
    "iit_mandi": 'aff:"Indian Institute of Technology, Mandi"', "iit_bhu": 'aff:"Indian Inst. Tech. (BHU), Varanasi"',
    "iit_palakkad": 'aff:"Indian Inst. Tech., Palakkad"', "iit_tirupati": 'aff:"Indian Inst. Tech., Tirupati"',
    "iit_ism": '(aff:"Indian Inst. Tech., Dhanbad" or aff:"Indian Sch. Mines, Dhanbad")',
    "iit_bhilai": 'aff:"Indian Inst. Tech., Bhilai"', "iit_goa": 'aff:"Indian Inst. Tech. Goa"', "iit_dharwad": 'aff:"IITDH, Dharwad"',
    # IIT Jammu: no INSPIRE institution record (searched 2026-10-25)
}
for _k, _v in INSPIRE.items():
    REG[_k]["inspire"] = _v

# Other institution types are registered by their teams in separate files (no edits to this file needed, no merge conflicts):
# institutes_iiit.py and institutes_other.py each define EXT = {key: dict(...)} with the same fields as above, plus the
# institution-type fields (mention, explicit_full, confusable, family; see affil._C). Keys must be new.
import importlib
for _mod in ("institutes_iiit", "institutes_other"):
    try:
        _ext = importlib.import_module(_mod).EXT
    except ModuleNotFoundError:
        continue
    for _k, _c in _ext.items():
        assert _k not in REG, f"{_mod}: institute key {_k} already registered"
        _c.setdefault("tenure_lag", 1)
        REG[_k] = _c

# ---------------------------------------------------------------------------------------------- founding dates (F6)
# (founded, became_iit, former names).  Used by startyear.py: a person-channel ("likely") record must not be older than the
# institution it is credited to, and `founded` - NOT `became_iit` - is the bound, because the predecessor institution is the
# same institution (an "Indian School of Mines" paper of 2016 belongs to IIT (ISM) Dhanbad; the classifier already counts it,
# PHRASES above).  `became_iit` is kept as information and for the dashboard's age labels; no rule drops a record before it.
# Verified 2026-10-30 against Wikipedia, fetched through WebScrape/agents/polite_get.py ("Indian Institutes of Technology" table
# of established / IIT year, plus the infobox and history of IIT Roorkee, Delhi, (ISM) Dhanbad and (BHU) Varanasi):
#   Roorkee 1847 (Thomason College 1854, University of Roorkee 1947, declared an IIT by ordinance of 21 Sep 2001; the list table
#   prints 2002, the year of the Act); Delhi 1961, "decreed an Institute of National Importance" by the Institutes of Technology
#   (Amendment) Act 1963; BHU 1919 as Banaras Engineering College, IT-BHU 1968, IIT 2012; ISM founded 9 Dec 1926, IIT 25 May 2016;
#   Guwahati 1994 (first intake 1995); Kharagpur 1951 in the list table (the IIT system page says first IIT 15 May 1950; both lie
#   before the 2016-2026 window, which is all that matters here); Palakkad / Tirupati 2015; Bhilai, Dharwad, Jammu, Goa 2016.
DATES = {
    "iit_kharagpur": (1951, 1951, ()), "iit_bombay": (1958, 1958, ()), "iit_kanpur": (1959, 1959, ()),
    "iit_madras": (1959, 1959, ()),
    "iit_delhi": (1961, 1963, ("College of Engineering and Technology, Delhi",)),
    "iit_guwahati": (1994, 1994, ()),
    "iit_roorkee": (1847, 2001, ("University of Roorkee", "Thomason College of Civil Engineering")),
    "iit_ropar": (2008, 2008, ()), "iit_bhubaneswar": (2008, 2008, ()), "iit_gandhinagar": (2008, 2008, ()),
    "iit_hyderabad": (2008, 2008, ()), "iit_patna": (2008, 2008, ()),
    "iit_jodhpur": (2008, 2008, ("Indian Institute of Technology Rajasthan",)),
    "iit_indore": (2009, 2009, ()), "iit_mandi": (2009, 2009, ()),
    "iit_bhu": (1919, 2012, ("Institute of Technology, Banaras Hindu University", "IT-BHU", "Banaras Engineering College",
                             "College of Mining and Metallurgy")),
    "iit_palakkad": (2015, 2015, ()), "iit_tirupati": (2015, 2015, ()),
    "iit_ism": (1926, 2016, ("Indian School of Mines", "ISM Dhanbad")),
    "iit_bhilai": (2016, 2016, ()), "iit_dharwad": (2016, 2016, ()), "iit_jammu": (2016, 2016, ()), "iit_goa": (2016, 2016, ()),
}
for _k, (_f, _b, _fn) in DATES.items():
    REG[_k]["founded"], REG[_k]["became_iit"], REG[_k]["former_names"] = _f, _b, tuple(_fn)
for _k in REG:                     # other institution types (IIITs ...): dates not registered here; rules that need them skip
    REG[_k].setdefault("founded", None)
    REG[_k].setdefault("became_iit", None)
    REG[_k].setdefault("former_names", ())

V1 = ("iit_ropar", "iit_kharagpur", "iit_roorkee")
IITS = tuple(k for k in REG if REG[k].get("family", "iit") == "iit")
ALL = tuple(REG)


def cfg(inst):
    return REG[inst]
