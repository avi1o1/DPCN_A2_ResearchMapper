# IIIT Bangalore faculty roster (2016-2026): lab notebook

Built 2026-10-27 by Arihant Tripathy (IIIT team) with Claude. Output: `WebScrape/rosters/iiit_bangalore_faculty.csv` (132 rows). All fetches went through `polite_get.py`.
Downloads and scripts: `C:/Users/Arihant/rm_work/iiit_bangalore_roster/{data,code}` (not in the repo).

## Totals

| status | rows |
|---|---|
| current | 49 |
| adjunct | 38 (7 still listed on the site, 31 no longer listed, with range) |
| visiting | 20 (1 still listed: S Rajagopalan... plus Harish Ramani listed as Visiting) |
| former | 25 |
| **total** | **132** |

joining_year filled: 108 (39 of 49 current). Identifiers: ORCID 19 (2 from institute profile pages: Amit Chattopadhyay, Sanghasri Mukhopadhyay; 17 from the ORCID API route), Google Scholar 11, DBLP 4, IRINS 2 (printed by the institute), homepage 11, Scopus 0, e-mail 56 (live list `data-email`).

Per unit (current / adjunct / former): CSE 15/0/0; DSAI 12/1 (Anutosh Maitra)/2; DHSS 4/0/5; ECE 11/0/2; Centre for Applied Sciences 4/0/0 (administratively under ECE, which also lists them; CAS page used as primary); EHRC 0/1 (T K Srikanth)/0;
no unit known: 3 current (Sahana M. Prabhu, Rajeevalochana Mysore Raghunath, Pankaj Chaudhary), 36 adjunct, 20 visiting, 16 former. Former faculty of 2016-2024 mostly have no unit: no archived page gave one (the 2016 area-filter pages ignore the filter and list everybody). Units for the 5 DHSS former come from the DHSS "Past" list.

## Sources and endpoints

1. **Institute site** `https://www.iiitb.ac.in/faculty` (PHP, GET form): `?faculty_type=Regular|Adjunct|Visiting|Advisory|Post+Doctorate+Fellow|All&name=first_name&faculty_name=&alphabet=`. Regular 52, Adjunct 6, Visiting 1, All 59, Advisory/Postdoc 0. 59 profile pages `/faculty/<slug>` (designation line, bio, some links). The list carries no designation or unit.
   Unit pages: `cse.iiitb.ac.in/people/`, `dhss.iiitb.ac.in/people/` (with a "Past" list), `dsai.iiitb.ac.in/faculty/` (with "Retired faculty"), `ece.iiitb.ac.in/faculty/`, `www.iiitb.ac.in/centre-for-applied-sciences`.
2. **NIRF data submissions, institute's own PDFs** (`/nirf` page links, `pdftotext -raw`, records split on the running serial number): 2018 (62 rows), 2019 (65, `images/pdf/nirf2019.pdf`), 2020 (67), 2021 (63), 2022 (63), 2023 (63), 2024 (77), 2026 (70). Serial numbers contiguous in every year, row count = last serial. No 2025 PDF exists (only a rank image). nirfindia.org not used. Year N is treated as presence in year N.
3. **Wayback** (CDX `url=iiitb.ac.in/faculty` exact, `collapse=timestamp:6`; snapshots `/web/<ts>id_/<url>`): 52 captures of `/faculty` (2016-01..09, 2020-02..2026-06) and 10 of `/faculty.php` (2016-2019). 2016 captures embed the full list (49-57 names with ranks); 2020-2023 captures show only page 1 (20 names, alphabetical A-J, all tenure types, so presence evidence only for those letters); 2021-04 pages 1-3 give the full list (54); 2024-2026 captures are unpaginated and maintained in both directions (drops of Manikandan R R 2024-07, Janaki Srinivasan 2024-09, Nanditha Rao 2024-12 match NIRF leaving dates). 2017 and 2019 `faculty.php` pages were only partly captured (pages 1, 2, 6); they were fetched but used only as presence evidence.
4. **ORCID public API**: one `expanded-search` `affiliation-org-name:"International Institute of Information Technology Bangalore"` (435 records, 3 pages of 200) plus `IIIT Bangalore` (10). 30 name-matched candidates checked with `/employments`; no 429. Accepted when the record shows IIIT-B and the name matches (19 incl. 2 from site pages). Rejected: Samar Shailendra (Melbourne Institute only), Sharvari Ravindran x2 (Radisys intern), Madurima Panja, Shruti/Vansh Sinha, S. Nagarajan's other candidate Rajagopal Nagarajan (name), students/postdocs (Riddhika Mahalanabis, Jhelum Das, Dhanya Eledath, Carolyn Tauro, Harsha, Pooja Bassin, Bindu Gowda). S Nagarajan 0000-0001-6465-7296 is accepted on a weak name-only match (record "Nagarajan S", IIIT-B, no dates): treat with care. ORCID lookup pending: none.

## How status, tenure and years were decided

* **current** = on the live institute-wide list (Oct 2026) with tenure Regular and not a Professor of Practice / consulting. **adjunct/visiting still listed**: Adjunct/Visiting tenure filter, Professors of Practice (T K Srikanth, Ajay Bakre) and Consulting Faculty (Anutosh Maitra) -> adjunct, designation kept (T K Srikanth is "Regular, Professor" in NIRF 2026; the brief rule for PoP was applied).
* **Tie-break conflicts** (institute list wins over department page): Tulika Saha (CSE/DSAI pages), Chinar Mehta (DHSS page) and Subir Kumar Roy (ECE page) are on department pages but absent from the Oct 2026 institute list -> `former` with LAST 2026 (Subir dropped from the list 2026-05, Tulika/Chinar between 2026-06 and 2026-10; their profile URLs now 404). Rituparna Choudhury (dropped 2026-01), Balaji Parthasarathy (DHSS "Past", dropped 2026-06..10), G Srinivasaraghavan (DSAI "Retired faculty", dropped 2026-05), Preeti Mudliar (dropped 2025-08; DHSS "Past"): `former`, LAST 2026 from NIRF 2026 "currently working" (Preeti may have left in 2025: uncertain). Ananda Y R: dropped from the list 2025-07, still "Yes" in NIRF 2026 -> former (2024-2026), uncertain.
* **former/adjunct/visiting, range (FIRST-LAST)**: FIRST = NIRF joining year if not later than the first archive/NIRF listing, otherwise first listing year. LAST = NIRF leaving year if given, otherwise last year with evidence (NIRF year or maintained list). 2016-only people carry (2016-2016) unless NIRF extends it.
* **joining_year** = earliest NIRF joining date over 2018-2026 (site text for Pankaj Chaudhary Aug 2026, Ajay Bakre, Amrita Mishra, Srinivas Vivek, Muralidhara agree with NIRF). Left blank where NIRF joining is later than an earlier archive listing (Vinod Vyasulu, Anand Bariya, Karthikeyan Vaidyanathan: rejoin/regularisation dates) and for 2025-26 joiners and people without NIRF rows. NIRF date caveat: rejoin dates are possible (Roland Haas 2007 and 2021, S Nagarajan 2007 and 2022: earliest used).
* Unknown tenure type: nine people appear only on archived lists without a rank (Balwant Godara, Chandramouleeswaran Sankaran, Ishu Gupta, K R V Raja Subramanian, Peter Chacko, S Ramesh, Sadanand Gulwadi, Srinivasan A) -> `adjunct`, designation "type not stated"; Srinath R Naidu has rank Assistant Professor (2016) -> `former` (2016-2016).
* Name merges: Sridhar Varadarajan = V Sridhar = Varadarajan Sridhar; Anand Baria (2016) = Anand Bariya (NIRF 2023) assumed (ambiguous); Subajit/Subhajit Sen; Roland E./Erik Haas; Linas/Linus Kendall; Mohan Ram = Mohan Ram C; Pramod Verma = Pramod Varma; Milind Gandhe, Kunal P Ghosh, Arti Yardi and spelling variants. K R V Raja Subramanian and K K Subramaniam kept separate.
* Additional-charge rule: no person fitting it was identified (Director Debabrata Das and the Deans are regular faculty).

## Excluded (not faculty or not evidenced as faculty)

NIRF 2024 "Adhoc/Contractual, Assistant Professor" cohort listed in 2024 only, not on the site, not in 2026: 23 people (Anindita Dasgupta, Anjan Kumar Veeravalli, Ashwini Baje, Asilata Karandikar, Bhoomika A P, Bindu G Gowda, Chandrima Bhattacharya, Dhanya Eledath, Harsha Rudramuniyappa, Jhelum Das, Jobin Josey P, Madhurima Panja, Nagalakshmi S R, Navitha Parthasarathy, Neeta Jha, Pooja Bassin, Rahisha Thottolil, Rashmi P S, Riddhika Mahalanabis, Sharvari N P, Sharvari Ravindran, Snigdhashree Mallick, Vasanthi D R). ORCID shows several of them as PhD/graduate students, so they are teaching contract staff. NIRF 2026 rows with designation Other/Lecturer not on the site: Apurva Prakash Kulkarni, Arun S Iyer, Carolyn Kavita Tauro (postdoc), Deepa Austin, Dibakar Das, G V K Sasirekha, K V Subramanian, Lakshmi Jagannathan, Neha Arrora, Priyanka Sharma, Sharath Srivatsa, Sunil Kumar Vuppala. Research staff, postdocs, scholars excluded. These could be added if the project wants NIRF-declared teaching staff.

## Independent size check

NIRF 2026 (Engineering) lists 70 rows: 45 Regular rows flagged currently working (two of them forced to `former` here: ex-faculty dropped from the site), 21 Adhoc/Other. The site lists 52 Regular + 7 other = 59 (Oct 2026). Our current = 49 (52 Regular minus 3 Professor of Practice/consulting reclassified as adjunct). Difference to NIRF: NIRF is ~Jan 2026 and predates 2025-26 joiners (Ahana Pradhan, Naganand Yadati, Saumya Shankar, Vaishnavi Gujjula, Sanju Ahuja, Pranesh Santikellur, Anuj Verma, Narayanan P P, Sahana Prabhu, Rajeevalochana, Pankaj Chaudhary) and still counts Balaji, Subir, Tulika, Rituparna, Preeti, Ananda, Srinivasaraghavan. NIRF-confirmed current rows: 38 of 49.

## Known gaps

* No 2025 NIRF; no usable archived list for 2017-2019 beyond partial pages and NIRF 2018/2019; page-1-only captures 2020-2023 limit presence evidence to letters A-J, so LAST for later-alphabet adjunct/visiting people rests on NIRF only (may be understated).
* Units blank for most former/adjunct people; Scopus IDs not collected; the 2016 list has no tenure type.
* Former last-year uncertainty: Preeti Mudliar, Ananda Y R, Subir Kumar Roy, Tulika Saha, Chinar Mehta (see above).

## Brief issues

* Brief mentions IIT-style sources (mentor IITs, regional pages); not applicable. The brief's "(/d{4})-(/d{4})" was read as `(\d{4})-(\d{4})`.
* Session limit interrupted the run once; resumed from saved data.
