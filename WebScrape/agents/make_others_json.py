"""Agent settings (others.json) of the other-institutes team for the CSIR + DAE wave (PROCESS_OTHER.md §3).
One row per lab: key, full name, campus hint, golden target, type rules (who counts as faculty, in SPECIAL).
usage: python3 make_others_json.py [--force]   -> writes others.json (keeps existing keys unless --force)"""
import json, os, sys

A = os.path.dirname(os.path.abspath(__file__))
CSIR = ("* **Who counts as faculty at a CSIR lab** (handoff §6): the scientific staff - Scientist, Senior Scientist, Principal "
        "Scientist, Senior Principal Scientist, Chief Scientist (grades Sc-B to Sc-H / Scientist B-H), Outstanding / "
        "Distinguished Scientist, and the Director. Exclude technical officers and assistants, project staff, research "
        "associates, postdocs, students and administrative staff. CSIR emeritus scientists -> `emeritus`; fellows hosted by "
        "the lab (Ramanujan, INSPIRE Faculty, CSIR Young Scientist) -> `visiting` with the fellowship in `designation`.\n"
        "* `department` = the scientist's division or group as the lab names it; scientists of an outstation centre / unit "
        "without a division get the centre's name.\n"
        "* CSIR labs are not in NIRF's university tables: wherever this brief says NIRF, use the lab's annual reports (staff "
        "lists, joinings, superannuations) and its own scientist pages instead, and say so in the notes. AcSIR faculty listings "
        "are not separate membership evidence (AcSIR faculty are the lab's own scientists).\n"
        "* This brief was written for IITs: read 'this IIT' as the lab. The mentor-IIT rules do not apply.")
DAE = ("* **Who counts as faculty at a DAE unit** (handoff §6): Scientific Officers (SO/C to SO/H+, Outstanding Scientist, "
       "Distinguished Scientist) and the Director / unit heads. Exclude technical officers, scientific assistants, project "
       "staff, research scholars and administrative staff. HBNI faculty listings are not separate membership evidence (HBNI "
       "faculty are the unit's own scientists). Raja Ramanna / DAE fellows hosted by the unit -> `visiting`.\n"
       "* `department` = the scientist's division / group / section as the unit names it.\n"
       "* DAE units are not in NIRF's university tables: wherever this brief says NIRF, use the unit's annual reports, "
       "newsletters and its own staff pages, and say so in the notes.\n"
       "* This brief was written for IITs: read 'this IIT' as the unit. The mentor-IIT rules do not apply.")
NISER = ("* NISER is a teaching institute: faculty = its schools' faculty (as for an IIT); HBNI is its degree-granting university "
         "and is not separate membership evidence.\n"
         "* This brief was written for IITs: read 'this IIT' as NISER. The mentor-IIT rules do not apply.")
LABS = [  # key, NAME, CAMPUS_HINT, TARGET, type rules
    ("csir_ncl", "CSIR-National Chemical Laboratory (CSIR-NCL), Pune", "", "400", CSIR),
    ("csir_iict", "CSIR-Indian Institute of Chemical Technology (CSIR-IICT), Hyderabad", "", "400", CSIR),
    ("csir_cftri", "CSIR-Central Food Technological Research Institute (CSIR-CFTRI), Mysuru", " and its resource centres", "300", CSIR),
    ("csir_niist", "CSIR-National Institute for Interdisciplinary Science and Technology (CSIR-NIIST), Thiruvananthapuram", "", "300", CSIR),
    ("csir_nml", "CSIR-National Metallurgical Laboratory (CSIR-NML), Jamshedpur", " and its centres (e.g. the Madras Centre, Chennai)", "300", CSIR),
    ("csir_npl", "CSIR-National Physical Laboratory (CSIR-NPL), New Delhi", "", "300", CSIR),
    ("csir_csio", "CSIR-Central Scientific Instruments Organisation (CSIR-CSIO), Chandigarh", " and its centres (e.g. the Chennai centre)", "300", CSIR),
    ("csir_cgcri", "CSIR-Central Glass and Ceramic Research Institute (CSIR-CGCRI), Kolkata", " and its outstation centres", "300", CSIR),
    ("csir_cmeri", "CSIR-Central Mechanical Engineering Research Institute (CSIR-CMERI), Durgapur", " and its centres", "300", CSIR),
    ("csir_crri", "CSIR-Central Road Research Institute (CSIR-CRRI), New Delhi", "", "250", CSIR),
    ("csir_cimfr", "CSIR-Central Institute of Mining and Fuel Research (CSIR-CIMFR), Dhanbad", " and its regional centres", "300", CSIR),
    ("csir_cbri", "CSIR-Central Building Research Institute (CSIR-CBRI), Roorkee", "", "250", CSIR),
    ("csir_ceeri", "CSIR-Central Electronics Engineering Research Institute (CSIR-CEERI), Pilani", " and its centres (e.g. Chennai, Jaipur)", "300", CSIR),
    ("csir_serc", "CSIR-Structural Engineering Research Centre (CSIR-SERC), Chennai", "", "250", CSIR),
    ("csir_ampri", "CSIR-Advanced Materials and Processes Research Institute (CSIR-AMPRI), Bhopal", "", "250", CSIR),
    ("csir_cdri", "CSIR-Central Drug Research Institute (CSIR-CDRI), Lucknow", "", "300", CSIR),
    ("csir_ccmb", "CSIR-Centre for Cellular and Molecular Biology (CSIR-CCMB), Hyderabad", " and its Laboratory for the Conservation of Endangered Species (LaCONES)", "300", CSIR),
    ("csir_igib", "CSIR-Institute of Genomics and Integrative Biology (CSIR-IGIB), New Delhi", " (both of its Delhi campuses)", "300", CSIR),
    ("csir_imtech", "CSIR-Institute of Microbial Technology (CSIR-IMTECH), Chandigarh", "", "300", CSIR),
    ("dae_barc", "Bhabha Atomic Research Centre (BARC), Mumbai", " (Trombay, and any other BARC facility the notes decide to include, with the reason)", "400", DAE),
    ("dae_igcar", "Indira Gandhi Centre for Atomic Research (IGCAR), Kalpakkam", "", "300", DAE),
    ("dae_rrcat", "Raja Ramanna Centre for Advanced Technology (RRCAT), Indore", "", "300", DAE),
    ("dae_niser", "National Institute of Science Education and Research (NISER), Bhubaneswar", " (the Jatni campus and the earlier transit campus)", "300", NISER),
]
fn = os.path.join(A, "others.json")
d = json.load(open(fn, encoding="utf-8")) if os.path.exists(fn) else {}
for k, name, hint, target, special in LABS:
    if k in d and "--force" not in sys.argv:
        continue
    d[k] = {"NAME": name, "CAMPUS_HINT": hint, "SPECIAL": special, "TARGET": target,
            "AUTHCOL": k.split("_", 1)[1] + "_author"}
json.dump(d, open(fn, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(d), "institutes in others.json")
