# Golden set IIT Bombay (iit_bombay) — lab notebook

Built 2026-10-25/26 by a golden-set sub-agent (pilot institute for the brief template). Output: `WebScrape/golden/golden_iit_bombay.csv`
(**582 distinct papers**, 2016–2026). All fetches went through the shared `polite_get.py` (625 fetches logged in
`scratchpad/work/iit_bombay_golden/data/fetchlog.tsv`; 569×200, 28×403, 22 timeouts/killed, 3×404, 1 SSL error).
No pipeline output for IIT Bombay was read. No bibliographic API (Crossref, OpenAlex, S2, ORCID, DBLP, Scholar, Scopus, IRINS, arXiv API) was used.

## Result summary
* By source: faculty_page 374, news 80, arxiv 71, dept_page 57, annual_report 0, websearch 0.
* By confidence: high 151 (affiliation visible: IITB research-highlight pages naming IITB authors, or arXiv PDF p.1–2), medium 431 (tenure rule only).
* DOI printed on source / reached landing page: 138 (23.7 %). arXiv rows carry no DOI (journal refs not resolved; no lookups).
* Types: journal 400, conference 97, preprint 66, book-chapter 10, book 6, other 3.
* Target was 650; reached 582 (see deviations).

## Departments × years
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Electrical Engineering | 5 | 8 | 8 | 14 | 11 | 4 | 7 | 5 | 7 | 4 | 8 | 81 |
| Chemistry | 10 | 14 | 5 | 7 | 15 | 4 | 4 | 3 | 5 | 8 | 2 | 77 |
| Mechanical Engineering | 11 | 20 | 12 | 4 | 3 | 4 | 3 | 3 | 5 | 6 | 2 | 73 |
| Physics | 0 | 0 | 1 | 0 | 3 | 2 | 1 | 4 | 5 | 11 | 14 | 41 |
| Computer Science and Engineering | 0 | 2 | 1 | 0 | 6 | 5 | 3 | 5 | 3 | 3 | 9 | 37 |
| Biosciences and Bioengineering | 1 | 0 | 6 | 4 | 4 | 4 | 8 | 0 | 2 | 4 | 2 | 35 |
| Energy Science and Engineering | 2 | 0 | 3 | 3 | 3 | 6 | 2 | 4 | 2 | 4 | 2 | 31 |
| Civil Engineering | 0 | 1 | 1 | 0 | 2 | 2 | 3 | 3 | 5 | 6 | 3 | 26 |
| SJM School of Management | 3 | 1 | 0 | 3 | 5 | 2 | 3 | 0 | 3 | 4 | 0 | 24 |
| Chemical Engineering | 1 | 3 | 0 | 1 | 2 | 2 | 0 | 0 | 5 | 8 | 1 | 23 |
| Mathematics | 1 | 2 | 2 | 1 | 0 | 5 | 3 | 3 | 1 | 1 | 3 | 22 |
| Industrial Engineering and Operations Research | 0 | 0 | 0 | 0 | 4 | 4 | 4 | 3 | 3 | 2 | 1 | 21 |
| Economics | 2 | 1 | 1 | 4 | 1 | 4 | 3 | 0 | 3 | 0 | 1 | 20 |
| Aerospace Engineering | 2 | 1 | 1 | 1 | 2 | 7 | 1 | 1 | 2 | 0 | 1 | 19 |
| Metallurgical Engineering and Materials Science | 0 | 0 | 0 | 1 | 1 | 1 | 3 | 6 | 0 | 3 | 1 | 16 |
| Humanities and Social Sciences | 0 | 1 | 0 | 0 | 2 | 1 | 3 | 1 | 1 | 2 | 0 | 11 |
| Centre for Urban Science and Engineering | 0 | 1 | 0 | 2 | 0 | 2 | 0 | 0 | 2 | 1 | 1 | 9 |
| Systems and Control Engineering | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 2 | 1 | 2 | 6 |
| Environmental Science and Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 4 |
| Centre of Studies in Resources Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 3 |
| Interdisciplinary Programme in Climate Studies | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| IITB-Monash Research Academy | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| Earth Sciences | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| **All** | 38 | 55 | 41 | 45 | 65 | 59 | 51 | 41 | 60 | 73 | 54 | 582 |

Units with ≥5 faculty sampled: ME (≈14 incl. dept-page attributions), EE (≈12), Chemistry (≈13 incl. arXiv/news), CSE (≈10 mostly arXiv),
Physics (≈9 mostly arXiv/news), BSBE (5 + news), ESE (6), SJMSOM (5), Mathematics (8 incl. arXiv), Economics (4), Aero (5), Civil (4 + news), IEOR (dept page, 11 people).
Thin: Earth Sciences (SPA site, news only), ESED (live site unreachable; news only), CSRE/Climate/CTARA/KCDH/C-MInDS/CPS/IDC/DSSE (sites unreachable,
403, or no lists; covered only through news where at all). Physics and CSE early years (2016–2019) are thin because their pages link only Google Scholar
(forbidden) and arXiv sampling was newest-first spread.

## Sources, page types, search strings
1. **Institute annual reports** (`https://www.iitb.ac.in/annual-reports`): AR 2018-19 and 2022-23 PDFs fetched and `pdftotext`-ed. They contain only
   publication **counts** (e.g. 2375 journal papers 2022-23), no lists. The only list PDF (`Publication201314.pdf`) is 2013-14 → out of range.
   Maths dept annual reports (AR-15-16, AR-16-17) are 1-page empty PDFs. Aero "Reports" page = event report. ⇒ **annual_report share = 0 % (unavailable)**.
2. **Faculty pages** (374 rows): ME profile + `/faculty/<x>/publications` pages (systematic every-12th faculty; 13 profiles), Chemistry
   `facultyuserview` + `/faculty-publications/<id>` (13 faculty), EE profile → EE wiki / `~user` homepages (12), ESE profiles (6), Aero profiles/homepages (5),
   Civil `~user` homepages and `/faculty/details/` (4), BSBE/ChemE/HSS profiles via **Wayback copies** (live sites unreachable: timeouts/SSL),
   SJMSOM `?p=` pages (5), Economics pages (4), Maths homepages linked from the faculty list (2), CSE homepages via the CSE faculty JSON
   (`~internal-live/api/faculty/?format=json`, the institute's own page backend) (2), Physics personal homepage (`homepages.iitb.ac.in/~shukla`), MEMS profiles (1).
   Faculty chosen by systematic index (every k-th in list order); within a list, entries spread evenly (systematic sample, ≤8, list order kept).
3. **Department/lab pages** (57): IEOR department publications page (pages 0,2,4,6,8; every 4th item, talks excluded), ME department "All Publications"
   page (items attributed to ME faculty whose IITB start year is printed on their profile; ≤4 per person, evenly spread), MEMS CMEG lab Google Site,
   Physics Nonlinear Dynamics Lab Google Site.
4. **News / research highlights** (80): all 92 `/research-highlight/` pages linked from the IITB home page fetched; 80 had an identifiable paper link +
   IITB author named in the text. Full titles taken from the publisher landing page when it was reachable (Springer, Nature, IOP); Elsevier/ACS/Wiley/RSC/APS/
   T&F/PNAS/Portland returned 403/Cloudflare or JS redirects → **not bypassed**; title kept as printed (truncated with "…" on the IITB page) and noted.
5. **arXiv** (71): arXiv **website** author search (`/search/?searchtype=author`) for 33 named faculty, systematic sample of results 2016–2026, PDF fetched,
   affiliation string "Indian Institute of Technology Bombay/IIT Bombay/Powai" required on PDF p.1–2 (12+1 candidates rejected for missing affiliation).
   Done **before** the operator decision that `/search` is disallowed by robots.txt; not used afterwards. Two homonym cases corrected (S. Krishna → CSE;
   a physics "Arpita Mondal").
6. **Web search** (tool, not fetched pages): queries used —
   "IIT Bombay department annual report publications list pdf journal papers 2019"; "site:iitb.ac.in faculty publications list journal 2020 2021 \"IIT Bombay\" department homepage";
   "IIT Bombay Department of Chemistry annual report publications"; "\"IIT Bombay\" professor homepage \"selected publications\" 2018 2022";
   "iitb.ac.in \"annual report\" department publications pdf physics OR chemistry OR \"computer science\" OR aerospace 2018-19";
   "\"IIT Bombay\" centre \"annual report\" 2022-23 publications list Koita OR CTARA OR \"Climate Studies\" OR CSRE OR \"Policy Studies\"";
   "iitb.ac.in department \"annual report\" pdf \"list of publications\" journal papers faculty". Yield: 0 usable pages (results dominated by IIT Palakkad/IRINS-type
   portals of other IITs, Nature Index, Scribd). Hence websearch share 0.

Per-source yield (visited → rows): faculty/homepage pages ≈120 visited → 374 rows; dept/lab pages 9 → 57; research highlights 92 → 80; arXiv searches 33 + 84 PDFs → 71;
annual-report PDFs 5 → 0; landing pages 67 tried → 22 usable titles.

## Tenure handling
Rule (b) with the *strict* operator rule (paper year must be **after** the joining year) applied to every row with a stated joining year; the one
pre-decision violation (Sandeep Kumar 2017 = joining year) was removed. For ~25 long-standing faculty whose pages give **no** joining year
(e.g. A. Chowdhury, P.S. Gandhi, B. Ravi, S.K. Saha, M. Ravikanth, Prabhu Ramachandran, V. Menezes, P.V. Balaji, S. Mukherji, Swati Bhattacharya, P. Dutta,
S. Gaurav, S. Narayan Rao, P. Pant/M.P. Gururajan lab, P. Parmananda lab, IEOR dept-page authors) the row is `medium` and the note says "start not stated"
with the on-page evidence used (IITB awards dated ≤2015, IITB roles, students since year, co-authors who are IITB faculty). Snapshot verification
(NIRF / first archived faculty list) was attempted for ME, Chem, ChemE, BSBE, SJMSOM 2016 Wayback lists: only BSBE's 2016 list is server-rendered
(confirms Balaji and Mukherji in 2016); the others are JS shells. **These ~150 rows are the weakest part of the set** and should be treated as
"probably in tenure" — a precision audit should start here.

## Rejected candidates (why)
| Unit | Person / source | Items | Reason |
|---|---|---|---|
| Mechanical Engineering | Soham Mujumdar | all 5 listed 2016-2018 papers | outside tenure: page states postdoc UIUC 2016-2018 (UIUC/Kapoor co-authors) |
| Mechanical Engineering | Harkirat Singh | no papers listed | joined IITB after IIT Gandhinagar (Nov 2025 - July 2026); none in tenure |
| Mechanical Engineering | Shailesh Ganpule | 2025-2026 papers on dept list | outside tenure: page states IIT Roorkee Aug 2016-Mar 2026, IITB from Apr 2026 (affiliation of 2025/early 2026 items = IIT Roorkee) |
| Mechanical Engineering | Vibhor Pandhare | none listed | IITB from 2025 (IIT Indore 2023-25); faculty page empty |
| Mechanical Engineering | Janani Srree Murallidharan | none listed | faculty page publication list empty |
| Mechanical Engineering | S. V. Prabhu | none in 2016-2026 | faculty page list only pre-2016 |
| Chemistry | Satyadeep Waiba | 13 listed 2019-2025 papers | outside tenure: page states Jadavpur Univ 2019-2025 / Bayreuth postdoc 2023-2025, IITB from Nov 2025; no listed item after Nov 2025 |
| Aerospace Engineering | Deepak Prakash Kumar | none | joined IITB June 2026 (UC Irvine postdoc till June 2026); profile points to Google Scholar only |
| Aerospace Engineering | Kowsik Bodi | listed papers 2001-2010 only | no 2016-2026 items on profile |
| Aerospace Engineering | C. S. Yerramalli | none | profile links to Google Scholar only (forbidden source) |
| Aerospace Engineering | V. Menezes | 2016 US patent | patent, not a publication |
| Aerospace Engineering | Rohit V. Nanavati | 2022-2024 items (incl. 2 papers with IITB co-authors) | outside stated IITB periods (TA Jan 2018-Oct 2021; Loughborough Dec 2021-Dec 2024; IITB faculty from Dec 2024) |
| Aerospace Engineering | Abhijit Gogulapati, Ganesh Patil | none in scope | profile lists none in 2016-2026 |
| Energy Science and Engineering | Anish Modi, J. K. Nayak, P. C. Ghosh | none in scope | faculty pages list no 2016-2026 publications (Ghosh list pre-2016) |
| Civil Engineering | Anshul Yadav | 5 papers 2022-2024 | IITB start not stated; listed papers from PhD period elsewhere (co-author S. Sen; PhD awards 2022-2023) -> not attributable |
| Civil Engineering | K. Gupta (~kgupta) | Key publications pre-2016 | no 2016-2026 items |
| Civil Engineering | M. Salman | homepage is Google Sites behind sign-in redirect | inaccessible |
| Civil Engineering | R. S. Jangid, V. Prakash | no parsable publication list on homepage | skipped |
| News | research highlights | 2012 Proteomics paper; Twist in light / Thermal battery / Theta-gamma / Langmuir blood droplet / HDPE composites | out of range (2012) or paper title/IITB author not identifiable from page |
| News | publisher landing pages | sciencedirect, pubs.acs.org, wiley, rsc, aps, tandfonline, portlandpress, pnas return 403/Cloudflare challenge | not bypassed; titles kept truncated as printed on IITB page |
| Metallurgical Engineering and Materials Science | Anirban Patra | 2016-2017 items | outside tenure (LANL postdoc Apr 2015-Jun 2017; IITB from Oct 2017) |
| Metallurgical Engineering and Materials Science | Deepoo Kumar | 2019 item | profile shows CMU/Praxair until 2019; IITB start later |
| Metallurgical Engineering and Materials Science | Mithun Chowdhury, S. Shukla | no list on profile | profile has no publication list |
| SJM School of Management | Vinish Kathuria (?p=989) | sampled | Professor of Practice page; 2016-2018 papers likely from prior affiliation (no IITB tenure stated) - rejected |
| SJM School of Management | ?p=455 (practice faculty) | none | no publications; IITB from Dec 2018 |
| Biosciences and Bioengineering | Neeta Kanekar | 2016 papers (co-authors UIC) | IITB start not stated; papers likely from prior position |
| Biosciences and Bioengineering | whole site | live www.bio.iitb.ac.in unreachable (timeout) | Wayback copies used |
| Humanities and Social Sciences | Anush Kapadia | 2016 EPW article | joining year 2016 (strict rule: only with visible affiliation) |
| Humanities and Social Sciences | Malhar Kulkarni, P. Rajaram | no 2016-2026 publication list | - |
| Energy Science and Engineering | Sandeep Kumar | 2017 ATE paper (Dasappa, IISc) | joining year 2017 -> excluded under strict tenure rule (decision taken after pilot start) |
| Civil Engineering | Jayadipta Ghosh, Sangram Nirmale, T. I. Eldho, N. S. Mohammad (faculty/details pages) | all | civil faculty/details pages render another faculty member's (P. Nanthagopalan) content - attribution unreliable, skipped |
| Civil Engineering | ~agoyal | - | 403 (not bypassed) |
| Chemistry | Venkateswarlu Yarlagadda | 10 listed 2016-2022 papers | outside tenure (McMaster/Dalriada until Apr 2022; IITB from June 2022) |
| Chemistry | Sajal Sen | 25 listed papers | outside tenure (MIT/OHSU/NISER; IITB from May 2026) |
| Chemistry | Ishita Sengupta | pre-2021 items | IIT Kanpur 2018-2019 / NCBS; IITB from 2020 -> only >2020 |
| Mechanical Engineering | dept publications page | sampled items of D.S. Shah 2019 (Imperial), Yelve 2025 (joined 2026), Ganpule 2025, Guha 2016 (UCLA), Fan et al. Nature 2017 | outside tenure or tenure unknown - dept list includes pre-joining work |
| Computer Science and Engineering | Biswabandan Panda, Vinay Ribeiro | lists available | IITB joining year not stated on homepage (lists contain Inria/IIT Delhi era papers) - skipped |
| Computer Science and Engineering | Sujoy, Harshad, Manas | no parsable list | - |
| Mathematics | Dipendra Prasad | items <=2020 | TIFR 2002-2020 per homepage |
| Economics | Souvik Banerjee | 2017-2019 papers (Boston/US co-authors) | before IITB start 2020 |
| Economics | dept publications.html | books without years | not usable |
| Electrical Engineering | A. Seshia, S. R. B. Pillai, M. Gopalkrishnan, R. Parasnis | - | profile links only Google Scholar / no list / not sampled further |

Also rejected implicitly: talks, keynotes, courses, patents, theses, project lists and "submitted" manuscripts without arXiv id found in faculty lists (skipped,
next listed publication taken).

## Known biases
* Source mix deviates from the brief (faculty 64 %, dept/lab 10 %, annual reports 0 %, arXiv 12 %, news 14 %): annual reports with lists do not exist for 2016+.
* High-confidence rows come only from news (2023–2026 heavy, big-journal heavy) and arXiv (CS/physics/maths heavy) — high/medium split is not field-neutral.
* Many department profile lists are stale (ME and Chemistry lists stop around 2018–2020) → 2016–2018 over-represented for ME/Chem, 2024–2026 for news/physics.
* Live sites of Physics, BSBE, ChemE, HSS, ESED, CTARA, Climate, CPS, KCDH, SysCon did not answer (timeouts/SSL) → Wayback copies or nothing;
  IDC returned 403 and its Wayback fetches were killed → IDC absent. Earth Sciences site is an Angular SPA (no server-rendered list).
* Research-highlight titles from bot-walled publishers are truncated (≈45 rows); evaluation should match those by DOI.
* Year for highlight papers without a reachable landing page is approximated from DOI/PII/highlight date (noted per row).
* Former faculty: only N.S. Punekar (retired 2021). Student-led rows: R.V. Nanavati (PhD period), IITB-Monash student papers, PhD-scholar-led highlights.
