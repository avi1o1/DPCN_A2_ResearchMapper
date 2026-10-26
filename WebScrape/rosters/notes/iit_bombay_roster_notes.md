# IIT Bombay faculty roster (2016–2026) — lab notebook

Built 2026-10-25/26 by a roster sub-agent. Output: `rosters/iit_bombay_faculty.csv` (1,287 rows).
Working directory (scripts, cached pages, intermediate files): `scratchpad/work/iit_bombay_roster/{code,data}`.
All fetches went through `scratchpad/tools/polite_get.py` (shared rate limit + cache).

## 1. Result summary
* 1,287 people: **804 current, 189 former, 30 emeritus, 208 visiting, 56 adjunct**; 30 units (+6 NIRF-only people whose unit could not be established, department left blank).
* joining_year filled for 786 (644 of the current) — all from NIRF data submissions (joining date column).
* ORCID: 305 rows, all via the ORCID public-API route (affiliation dump + per-record employment check); 0 ORCIDs seen on institute list pages. 179 people have unchecked candidates ("ORCID lookup pending", §10).
* Other identifiers (only as printed on institute pages/APIs): e-mail 650, profile_url 417, homepage 82, Google Scholar 69, DBLP 63 (Scholar/DBLP almost entirely from the CSE department API). Scopus/IRINS: none (not used, per brief).

## 2. Units covered and how the unit list was established
Unit list from `https://www.iitb.ac.in/units-academic` (heads table): 17 departments, 13 academic centres, 3 schools.
Included: Aerospace, BSBE, Chemical, Chemistry, Civil, CSE, Earth Sciences, Economics (split from HSS ~2023; economists before that are in HSS snapshots and were merged to their current unit), EE, Energy Sci., ESED (renamed from CESE ~2021, old domain www.cese.iitb.ac.in), HSS, IEOR, Mathematics, ME, MEMS (old domain www.met.iitb.ac.in, now www.iitb.ac.in/mems), Physics, ADCPS (cps), Climate Studies, C-MInDS, Systems & Control, CTARA, CTIKS, CSRE, KCDH, DSSE, IDC School of Design, SJM SoM, and the defunct Centre for Urban Science and Engineering (cuse.iitb.ac.in, 2016–2021; kept under its own name, it has no successor unit on the current list).
Not given own rows: CDTIS, SemiX, MedTRIC, MOCCM, Centre of Multi-Disciplinary Education, service centres — these list no faculty of their own (only a professor-in-charge from a department) or have no archived/visible faculty list (CDTIS/SemiX: Wayback has no faculty page). C-MInDS, KCDH, Climate, CTIKS "associated faculty" pages were used only for cross-reference (people are kept in their home department).
IITB-Monash staff: not included (no unit lists them as faculty).

## 3. Sources, URL patterns, endpoints
Live pages (fetched 2026-10-25): see `data/live.tsv` (34 pages). Notable endpoints the pages themselves call:
* CSE (Angular SPA): `https://www.cse.iitb.ac.in/~internal-live/api/faculty/` and `.../api/former_faculty/` (JSON; fields userid, retired flag n/v/ca/em/ja/y/fv/fa, dblp, google_scholar).
* Earth Sciences (Angular + Strapi): `https://www.geos.iitb.ac.in/api/faculties?pagination[pageSize]=500` (JSON, `ActiveDuty` flag). (GraphQL GET is rejected with 400.)
* C-MInDS: faculty list hard-coded in `static/js/main.*.js` (associated faculty only).
Other live list pages: aero `/home/people/{faculty,former-faculty}`, ieor `/index.php/people/faculty`, math `/People/{faculty,retired_fac,short_faculty}.php`, me `/{full-time-faculty,former-faculty,honorary-faculty}`, mems `/mems/en/people/{faculty-profiles,retired-faculty}.html`, ee `/people/{faculty,emeritus}/`, ese `/faculty`, economics `/faculty.html`, chem `/{people,former,retired,visiting}`, civil `/{faculty,former-faculty,professor-emeriti,visiting-adjunct-faculty-scientists}`, idc `/people/{faculty,adjunct-faculty}`, som `/{core-faculty,associate-faculty,retired-faculty,visiting-faculty}/`, ctiks `/people/`, csre `/faculty.php` (tabs present/former/retired).

**Unreachable live (recorded, not circumvented):** www.phy, www.che, www.bio, www.esed, www.cps, www.climate, www.et, www.sc, www.ctara, www.kcdh, www.dsse, www.semix, cdtis — public DNS returns NXDOMAIN for these hostnames (checked with `dig @1.1.1.1`); the machine's resolver then appends a search domain and lands on a parked/spam wildcard host (one fetch of http://www.bio… redirected to an ad domain, body discarded). www.hss resolves but serves an incomplete TLS chain (no intermediate) → fetcher SSLError. For all these units the most recent Wayback capture (2025/2026) was used as the "current" list, and NIRF 2026 decided current status (§6).

Wayback: domain-prefix CDX (`cdx?url=<host>/&matchType=prefix&from=2016&to=2026&filter=statuscode:200&collapse=urlkey&filter=mimetype:text/html`, 37 hosts) to discover historical list URLs (registry files `data/registry{1,2,3}.tsv`, 154 list URLs incl. older site generations: e.g. aero `/aero/people/{faculty,exfaculty}.html`, civil `www1.civil…/people/faculty`, che `/online/people/faculty/{core,adjunct,emeritus-professors,recently-associated,visiting}-faculty`, phy `/en/faculty`, `/physics/en/faculty`, hss `/en/faculty_details`, `/en/retired-faculty`, ee `/web/people/faculty/{core,retired,emeritus,adjunct,visiting}` and `/web/people_categories/*`, sc `coreFaculty.html` etc.). Per list URL a CDX query with `collapse=timestamp:6`; from it the **last capture of each year**, thinned to first year + last year + every even year (≈2 per 3 years; denser than that was not affordable on the shared 3-s Wayback slot) → 414 snapshots fetched as `web/<ts>id_/<url>`.

**NIRF data submissions** (institute page `https://www.iitb.ac.in/national-institutional-ranking-framework-nirf`): Overall-category PDFs for NIRF 2018, 2019, 2020, 2021, 2023, 2024, 2025, 2026 (2022 is not linked on the institute page; nirfindia.org answered 403 → not used). The "Faculty Details" table (name, age, designation, gender, joining date, leaving date, currently-working flag, association type) was parsed with `pdftotext -layout` (`code/nirf.py`): 618/603/673/682/745/759/833/909 rows, no missing serial numbers. NIRF 2018 joining dates are garbled (soft hyphens, year missing) and were ignored. Union across editions (`code/nirf_union.py`): 5,822 records → 1,274 people (NIRF truncates/misspells names, e.g. "Vinish Kumar" for Vinish Kumar Kathuria, "Bhaskaran" for Bhaskaran Muralidharan; records were merged on identical joining date + shared name token + no co-occurrence in the same edition).

## 4. Extraction
Generic heuristic extractor (`code/extract.py`) over each page: titled names ("Prof./Dr. X"), "Surname, Given" lines followed by designation/e-mail, untitled name lines followed by a designation, and name-only headings/links; section from headings / tab `div id`s (Core/Adjunct/Emeritus/Visiting/Former/Retired/Superannuated/Associated); designation and e-mail from the person's own text block; profile link from the anchor carrying the name. Noise (menu items etc.) removed with a stop-word list and a manual drop/rename list (`data/overrides.tsv`, 122 entries).
Page-level decisions: skipped phy `/people/faculty.html` (mixes staff/students), et `/en/about-iit-bombay/retired-faculty` (institute-generic template listing other units' retirees), IDC `/people/visiting-faculty.html` (historic honour roll, e.g. people who visited decades ago), CSE `faculty.php` (JS shell). Treated as "associated only" (never unit membership): Climate `/en/faculty`, C-MInDS `/people/faculty`, KCDH `/people/`, and any "Associated faculty" section.
Within a unit names were clustered by token compatibility (initials vs full names), shared e-mail, and never merged when two names occur on the same page. Across units: identical names, shared e-mail, associated-only clusters → unique compatible person elsewhere, and nested names in different units (9 merges, e.g. Vinish Kathuria SOM/ADCPS, Saptarshi P. Ghosh HSS→Economics, Malhar Kulkarni HSS/CTIKS) unless NIRF holds separate exact records (e.g. Anil Kumar (Chemistry) ≠ Anil Kumar Dikshit (ESED)). Primary unit = unit with a live current listing, else the unit with faculty-list evidence.

## 5. Status and tenure rules (as applied)
* current: on a live department list (core section); or, for units whose site is unreachable, NIRF 2026 "currently working = Yes, Regular" or presence on the 2025/26 archived list. NIRF 2026 (institute-wide) overrides department pages: dept-current but NIRF leaving date → former; dept "adjunct/visiting" but NIRF Regular → current (§8).
* emeritus / visiting / adjunct: from section/designation (professor of practice, honorary → adjunct, title kept). Live-listed ones carry no range; those no longer listed carry "(FIRST-LAST)".
* former: NIRF leaving date, or listed on faculty lists ≥2016 but not now, or a dated entry on the ME former-faculty page (retirement dates 2016–2026 parsed, `data/me_former_dates.json`).
* Window: people evidenced only before 2016 are excluded — this removes the long "retired/past faculty" honour rolls (Math, Chemistry, MEMS, ME, Aero, CSE former list without ≥2016 evidence: 16 shown in log + most of the ~300 retired-list entries).
* FIRST = NIRF joining year if known, else earliest archived-list year (2016 = start of window, not a true joining year). LAST = NIRF leaving year, else last NIRF edition with "working" (edition year − 1), else last archived snapshot year with the person (snapshots are biennial → LAST can be up to 1 year early; former LAST values cluster on even years for that reason). Stale-page rule: an archived snapshot whose name set is identical to the previous snapshot of the same page is not counted as presence evidence.
* joining_year: NIRF joining date only (may be a regularisation/re-joining date; no earlier appointment evidence was collected). ORCID employment dates not used.

## 6. Independent size check
NIRF 2026 data submission (institute's own, data as of early 2026): **749 regular faculty "currently working"** (+54 ad-hoc/contractual, +66 visiting). Earlier: NIRF 2018 582, 2020 672, 2023 707, 2025 759 regular.
Roster current = 804 = 687 linked to a NIRF record + 117 department-listed without a NIRF link. 635 of the 749 NIRF-2026 regular people are linked to a roster row; most of the remaining 114 are NIRF name fragments of people already in the roster (first name only, e.g. "Shivaram", "Prabhu", "Ganesh") that could not be linked unambiguously. The +55 difference (804 vs 749) is explained by (a) joiners after the NIRF 2026 cut-off (2025-26 new faculty on live pages), (b) department pages listing professors on lien/deputation or chair/visiting-type people inside the core list, (c) residual duplicates where one person appears under an initials-only name in one unit and a full name in another (few, see §9). Agreement within ~7%.

## 7. Per-unit counts
| unit | current | former | emeritus | visiting | adjunct | total |
|---|---|---|---|---|---|---|
| (not established) | 1 | 5 | 0 | 0 | 0 | 6 |
| Aerospace Engineering | 27 | 10 | 1 | 8 | 1 | 47 |
| Ashank Desai Centre for Policy Studies | 17 | 1 | 0 | 11 | 3 | 32 |
| Biosciences and Bioengineering | 33 | 2 | 0 | 32 | 2 | 69 |
| Centre for Climate Studies | 7 | 2 | 0 | 5 | 0 | 14 |
| Centre for Educational Technology | 4 | 12 | 0 | 1 | 0 | 17 |
| Centre for Systems and Control Engineering | 9 | 2 | 0 | 0 | 1 | 12 |
| Centre for Technology Alternatives for Rural Areas | 13 | 2 | 0 | 2 | 2 | 19 |
| Centre for Traditional Indian Knowledge and Skills | 4 | 0 | 0 | 0 | 0 | 4 |
| Centre for Urban Science and Engineering | 3 | 4 | 0 | 4 | 0 | 11 |
| Centre of Studies in Resources Engineering | 9 | 5 | 0 | 0 | 2 | 16 |
| Chemical Engineering | 45 | 8 | 0 | 1 | 5 | 59 |
| Chemistry | 39 | 14 | 0 | 57 | 0 | 110 |
| Civil Engineering | 57 | 5 | 3 | 9 | 3 | 77 |
| Computer Science and Engineering | 49 | 24 | 1 | 6 | 0 | 80 |
| Desai Sethi School of Entrepreneurship | 8 | 0 | 0 | 0 | 18 | 26 |
| Earth Sciences | 26 | 7 | 0 | 1 | 0 | 34 |
| Economics | 14 | 1 | 0 | 0 | 0 | 15 |
| Electrical Engineering | 72 | 12 | 6 | 19 | 4 | 113 |
| Energy Science and Engineering | 28 | 1 | 0 | 1 | 1 | 31 |
| Environmental Science and Engineering | 18 | 1 | 0 | 0 | 0 | 19 |
| Humanities and Social Sciences | 38 | 10 | 0 | 7 | 0 | 55 |
| IDC School of Design | 32 | 15 | 1 | 1 | 8 | 57 |
| Industrial Engineering and Operations Research | 16 | 0 | 1 | 8 | 0 | 25 |
| Koita Centre for Digital Health | 4 | 3 | 0 | 1 | 0 | 8 |
| Mathematics | 50 | 16 | 4 | 23 | 0 | 93 |
| Mechanical Engineering | 65 | 12 | 7 | 0 | 1 | 85 |
| Metallurgical Engineering and Materials Science | 41 | 3 | 0 | 0 | 0 | 44 |
| Physics | 47 | 9 | 6 | 0 | 1 | 63 |
| Shailesh J. Mehta School of Management | 28 | 3 | 0 | 11 | 4 | 46 |

## 8. Conflicts recorded (department page vs institute-wide NIRF)
* B. Krishna Mohan (csre): dept page current, NIRF leaving date 2025 -> former
* Dhimant Vyas (idc): dept lists as adjunct, NIRF 2026 'Regular' -> current
* Mayank Pareek (som): dept lists as adjunct, NIRF 2026 'Regular' -> current
* 207 people are 'current' on NIRF 2026 evidence without a live department page (mostly units whose site is unreachable: phy 45, che 37, hss 33, kcdh 13, bio 12, esed 12, cps 12, …). List:

Sridhar Iyer (cse), Mani Bhushan (che), Srikanth Srinivasan (math), Anirban Guha (me), Bhalchandra Puranik (me), Chetan Singh Solanki (ese), Anand B. Rao (ctara), Jangid R (civil), Viswanadham B V (civil), Srineash V (civil), G V Sreekumar (idc), Sumant Rao (idc), Sandesh R (idc), MALHAR A. KULKARNI (hss), P.V. Balaji (bio), P. Bhaumik (bio), S. Kaledhonkar (bio), N. Kanekar (bio), K. Kondabagil (bio), A. Kumar (bio), A. Kunwar (bio), S.K. Maji (bio), R. Mallik (bio), R. Manchanda (bio), S. Mukherji (bio), S. Nair (bio), R. Padinhateeri (bio), D. Panda (bio), S. Patankar (bio), D. Paul (bio), P.S. Phale (bio), R. Purwar (bio), R. Srivastava (bio), P. Tayalia (bio), N. Thirugnanasambandam (bio), H. Varma (bio), Rajdip Bandyopadhyaya (che), Sharad Bhartiya (che), Ravindra D Gudi (che), Devang V Khakhar (che), Sanjay M Mahajani (che), Kannan M Moudgalya (che), Hemant Nanavati (che), Rochish Madhukar Thaokar (che), K. V. Venkatesh (che), Madhu Vinjamur (che), Pramod P Wangikar (che), Jhumpa Adhikari (che), Abhijit Chatterjee (che), Ratul Dasgupta (che), Partha Sarathi Goswami (che), Abhijit Majumder (che), Ateeque Malani (che), Sarika Mehra (che), Santosh Noronha (che), Supreet Saini (che), Arindam Sarkar (che), Jyoti Seth (che), Yogendra Shastri (che), P Sunthar (che), Mukta Tripathy (che), Guruswamy Kumaraswamy (che), Swati Bhattacharya (che), Sujit S Jogwar (che), Jason R. Picardo (che), Bharatkumar Suthar (che), Ojus Mohan (che), Amol Subhedar (che), Sonali Das (che), Sayantan Dutta (che), Nagappan Ramaswamy (che), Sudarshan Vijay (che), Sanjeev Chaudhari (esed), Anil Kumar Dikshit (esed), Anurag Garg (esed), Subhankar Karmakar (esed), Suparna Mukherji (esed), Harish Phuleria (esed), Manoranjan Sahu (esed), Swatantra Pratap Singh (esed), Srinidhi Balasubramanian (esed), Indrajit Chakraborty (esed), Pradip Kalbar (esed), Renuka Verma (esed), AZIZUDDIN KHAN (hss), Kushal Deb (hss), MRINMOYI KULKARNI (hss), POOJA PURANG (hss), PRAVESH JUNG GOLAY (hss), RAJAKISHORE NATH (hss), RAMESH BAIRY T. S. (hss), RANJAN K. PANDA (hss), RATIKANTA PANDA (hss), ROWENA ROBINSON (hss), SARMISTHA PATTANAIK (hss), SIBY K GEORGE (hss), C. D. SEBASTIAN (hss), SUDHA SHASTRI (hss), VAIJAYANTHI SARMA (hss), VIKRAM SINGH SIROLA (hss), Ahonaa Roy (hss), Amrita Banerjee (hss), Anush Kapadia (hss), Sharmistha Saha (hss), Rashmi Gupta (hss), Suddhaseel Sen (hss), Saptarshi Prosonno Ghosh (hss), A. P. Rajaram (hss), Ilito H. Achumi (hss), Mrinal Kaul (hss), Naina Manjrekar (hss), Raile R. Ziipao (hss), Smriti Haricharan (hss), Deepak Naorem (hss), Neha Chatterji (hss), Rachel A. Varghese (hss), Aftab Alam (phy), M. Aslam (phy), Dibyendu Das (phy), Pragya Das (phy), Sadhana Dash (phy), Subhabrata Dhar (phy), Gopal Dixit (phy), Kantimay Das Gupta (phy), Dinesh Kabra (phy), Avinash V. Mahajan (phy), Suddhasatta Mahapatra (phy), Mithun Kumar Mitra (phy), Asmita Mukherjee (phy), Basanta Kumar Nandi (phy), Amitabha Nandi (phy), Punit Parmananda (phy), P. Ramadevi (phy), Kumar Rao (phy), Vikram Rentala (phy), Anirban Sain (phy), Pradeep Sarin (phy), M Senthil Kumar (phy), Alok Shukla (phy), K. G. Suresh (phy), Raghava Varma (phy), Parinda Vasa (phy), Sai Vinjanampathy (phy), Soumya Bera (phy), Varun Bhalerao (phy), Anshuman Kumar (phy), Archana Pai (phy), Sumiran Pujari (phy), Sunita Srivastava (phy), Pramod Kumar (phy), Nitin Kumar (phy), Hridis Kumar Pal (phy), Himadri Shekhar Dhar (phy), Maniraj Mahalingam (phy), Siddhartha Santra (phy), Sayantika Bhowal (phy), Rahul Kashyap (phy), Prashant Kumar (phy), Uditendu Mukhopadhyay (phy), Manibrata Sen (phy), Subhaskar Mandal (phy), Anupam Guha (cps), N. C. Narayanan (cps), Prabhir Vishnu Poruthiyil (cps), Bakul Rao (cps), Pennan Chinnasamy (cps), Malish C. M. (cps), Naveen Bharathi (cps), Rahul Suresh Sapkal (cps), Himanshu Burte (cps), S. Akshay (cps), Anjali Sharma (cps), S. Ravichandran (climate), Vishal Dixit (climate), Angshuman Modak (climate), Akshaya Nikumbh (climate), Jaideep Joshi (climate), Suyash Bire (climate), Sahana Murthy (et), Sanjay Chandrasekharan (et), Ritayan Mitra (et), Ramkumar Rajendran (et), Debasish Chatterjee (sc), Ravi N. Banavar (sc), Arpita Sinha (sc), Leena Vachhani (sc), Sukumar Srikant (sc), Ankur A. Kulkarni (sc), Vivek Natarajan (sc), Navin Khaneja (sc), Amit Arora (ctara), Priya Jadhav (ctara), Chaaruchandra Korde (ctara), Parmeshwar D. Udmale (ctara), Kuru Dindi (ctara), Sanjeeva Srivastava (kcdh), Santanu Kumar Ghosh (kcdh), Kshitij Jadhav (kcdh), Yogesh Rathi (kcdh), Devdip Purkayastha (dsse), Anuradha Narasimhan (dsse), Sankalp Pratap (dsse), Rajesh Gopinathan (dsse), Ramesh Kuruva (dsse), P. Vedagiri (cuse), S.D. Gupta (cuse), Indu J. (cuse)

## 9. Ambiguities / decisions
* NIRF ↔ department name matching: exact token match first, then compatible names; a link is made only when mutual-unique (75 ambiguous NIRF records logged in `data/assemble_log.json:nirf_multi`, left unlinked). Some people therefore have no joining year although NIRF lists them under a variant name.
* NIRF-only regular people with a full name and no name token shared with any roster row were added with blank department (6: Parthe Pandit, Latha Tummuru, Kamalkishor Madanlal, Maravanji Shivaramaiah, Vasudeva Raghavendra, Yogeshkumar Mangubhai — the last four are NIRF given-name+middle-name truncations whose surname is missing; they may duplicate existing rows). 71 other unmatched NIRF full names were skipped as probable variants of existing rows.
* Chemistry and BSBE "visiting faculty" pages are long lists of distinguished visitors (incl. deceased people); kept as `visiting` because the institute lists them as visiting faculty, but they are weak evidence of a faculty appointment.
* Initials-only names (BSBE page "Surname, I.") were expanded from NIRF when a compatible full name existed; otherwise kept as printed.
* CUSE (defunct): 3 people kept as current under CUSE on NIRF evidence (their present unit unknown).
* B. Krishna Mohan (CSRE): listed on live page, NIRF leaving date 2025 → former (2025).
* Residual possible duplicates across units with initials vs full names (e.g. BSBE "S. Srivastava" vs KCDH "Sanjeeva Srivastava" were merged; a few others may remain).

## 10. ORCID lookup pending
Route used: `https://pub.orcid.org/v3.0/expanded-search/?q=affiliation-org-name:"Indian Institute of Technology Bombay"` and `…:"IIT Bombay"` (10,163 records), name match (family name + first given name/initial), then `https://pub.orcid.org/v3.0/<id>/employments` must show an employment at IIT Bombay with a non-student/non-postdoc role; exactly one accepted iD per person (249 people had several qualifying iDs → left blank). 1,018 employment records were checked; the remaining candidates hit the anonymous daily quota (HTTP 429). For the people below, the batch run should fetch `https://pub.orcid.org/v3.0/<id>/employments` for the listed candidate iDs (query that produced them: the affiliation expanded-search above, matched on the person's name) and apply the same acceptance rule.

| name | department | candidate ORCID iDs whose /v3.0/{id}/employments was not fetched |
|---|---|---|
| Ajay A. Deshpande | Ashank Desai Centre for Policy Studies | 0009-0001-0573-4551, 0000-0003-2790-5726 |
| Anjali Sharma | Ashank Desai Centre for Policy Studies | 0000-0003-3633-075X, 0000-0003-1250-7901, 0000-0001-5362-0228 |
| Anupam Guha | Ashank Desai Centre for Policy Studies | 0009-0004-4768-710X, 0000-0001-8605-4736 |
| Himanshu Burte | Ashank Desai Centre for Policy Studies | 0009-0003-8259-6636, 0000-0001-8265-5083 |
| Malini Krishnankutty | Ashank Desai Centre for Policy Studies | 0000-0002-2834-7482 |
| N. C. Narayanan | Ashank Desai Centre for Policy Studies | 0000-0002-6747-4900, 0009-0003-5677-6262, 0009-0001-0877-249X, 0009-0008-3399-8061 |
| Pennan Chinnasamy | Ashank Desai Centre for Policy Studies | 0000-0002-3184-2134 |
| Rahul Suresh Sapkal | Ashank Desai Centre for Policy Studies | 0000-0002-6897-9521, 0009-0008-8173-2049, 0000-0002-4293-2303, 0000-0001-6272-3333 |
| Satish B. Agnihotri | Ashank Desai Centre for Policy Studies | 0000-0002-0703-3185 |
| Sekhar Bonu | Ashank Desai Centre for Policy Studies | 0009-0009-5028-6063 |
| Shishir K. Jha | Ashank Desai Centre for Policy Studies | 0000-0002-3646-8321 |
| Simran Agarwal | Ashank Desai Centre for Policy Studies | 0000-0002-5815-0613 |
| Subodh M. Wagle | Ashank Desai Centre for Policy Studies | 0000-0001-6895-639X |
| Varun Varghese | Ashank Desai Centre for Policy Studies | 0000-0001-6524-7192, 0000-0001-5574-8735 |
| Ambarish Kunwar | Biosciences and Bioengineering | 0000-0002-8671-7816 |
| Amit Sharma | Biosciences and Bioengineering | 0000-0001-9914-3746 |
| Anirban Banerjee | Biosciences and Bioengineering | 0000-0002-4229-5981, 0000-0003-0641-0935 |
| Ashutosh Kumar | Biosciences and Bioengineering | 0000-0002-5061-8162, 0000-0001-9449-4256 |
| D.K. Agrawal | Biosciences and Bioengineering | 0000-0001-9522-7838, 0000-0002-8215-3953, 0000-0003-0014-7347, 0000-0002-9309-5592 |
| Kiran Kondabagil | Biosciences and Bioengineering | 0000-0002-7942-023X, 0000-0003-1552-909X |
| L. Gandikota | Biosciences and Bioengineering | 0009-0008-5077-7623, 0000-0003-1738-4162, 0009-0001-9090-2774, 0000-0001-7346-6846 |
| Neeta Kanekar | Biosciences and Bioengineering | 0000-0003-2732-7110 |
| Nivethida Thirugnanasambandam | Biosciences and Bioengineering | 0000-0002-4834-3016 |
| Petety Balaji | Biosciences and Bioengineering | 0000-0002-6018-6957 |
| Prakriti Tayalia | Biosciences and Bioengineering | 0000-0002-4056-2628 |
| Prasenjit Bhaumik | Biosciences and Bioengineering | 0000-0003-1257-9809 |
| Prashant S Phale | Biosciences and Bioengineering | 0000-0002-5781-8941 |
| Ranjith Padinhateeri | Biosciences and Bioengineering | 0000-0001-5485-1474 |
| Rinti Banerjee | Biosciences and Bioengineering | 0000-0002-6400-5906 |
| Rohit Manchanda | Biosciences and Bioengineering | 0000-0001-7383-3482 |
| Rohit Srivastava | Biosciences and Bioengineering | 0000-0002-9957-8499 |
| Roop Mallik | Biosciences and Bioengineering | 0000-0001-6820-6556 |
| Samir K Maji | Biosciences and Bioengineering | 0000-0002-9110-1565 |
| Swati Patankar | Biosciences and Bioengineering | 0000-0001-7633-657X |
| Akshaya Nikumbh | Centre for Climate Studies | 0000-0001-5606-8571 |
| Angshuman Modak | Centre for Climate Studies | 0000-0002-4406-7288 |
| Jaideep Joshi | Centre for Climate Studies | 0000-0003-1315-6234 |
| Suyash Bire | Centre for Climate Studies | 0000-0001-9837-4016 |
| Vishal Dixit | Centre for Climate Studies | 0000-0002-9986-3273, 0000-0002-6675-525X, 0000-0002-1468-5253, 0000-0001-5574-8735 |
| Chandan Dasgupta | Centre for Educational Technology | 0000-0002-1380-6594 |
| Ramkumar Rajendran | Centre for Educational Technology | 0000-0002-0411-1782 |
| Sahana Murthy | Centre for Educational Technology | 0000-0002-7688-686X, 0009-0002-9410-1293 |
| Arpita Sinha | Centre for Systems and Control Engineering | 0000-0002-9116-3467, 0009-0003-9124-2143 |
| Debasish Chatterjee | Centre for Systems and Control Engineering | 0000-0002-1718-653X |
| Leena Vachhani | Centre for Systems and Control Engineering | 0000-0002-7869-6437 |
| Mayank Baranwal | Centre for Systems and Control Engineering | 0000-0001-9354-2826 |
| Vivek Natarajan | Centre for Systems and Control Engineering | 0000-0001-6757-6176, 0000-0001-5574-8735 |
| Vishal R. Sardeshpande | Centre for Technology Alternatives for Rural Areas | 0000-0002-9986-3273, 0000-0002-6675-525X, 0000-0001-5574-8735 |
| Chirag Deb | Centre for Urban Science and Engineering | 0000-0001-9634-6441 |
| Dipak Gupta | Centre for Urban Science and Engineering | 0009-0006-9109-5739 |
| Indu J. | Centre for Urban Science and Engineering | 0000-0003-4276-6138 |
| Ronita Bardhan | Centre for Urban Science and Engineering | 0000-0001-5336-4084 |
| Krishna Mohan Buddhiraju | Centre of Studies in Resources Engineering | 0000-0001-6815-8988 |
| Abhijit Majumder | Chemical Engineering | 0000-0002-0695-3967 |
| Akkihebbal K Suresh | Chemical Engineering | 0000-0003-0700-877X |
| Arindam Sarkar | Chemical Engineering | 0009-0005-1977-2910 |
| Ateeque Malani | Chemical Engineering | 0000-0003-1630-8686 |
| Bharatkumar Suthar | Chemical Engineering | 0000-0002-8612-9483 |
| Chandra Venkataraman | Chemical Engineering | 0000-0002-2280-3360 |
| Ganesh A Viswanathan | Chemical Engineering | 0000-0001-6424-0765, 0000-0002-0243-4182 |
| Guruswamy Kumaraswamy | Chemical Engineering | 0000-0001-9442-0775 |
| Jason R. Picardo | Chemical Engineering | 0000-0002-9227-5516 |
| Jayesh Bellare | Chemical Engineering | 0000-0002-6792-8327 |
| Mahesh S Tirumkudulu | Chemical Engineering | 0000-0002-7046-8069 |
| Mukta Tripathy | Chemical Engineering | 0000-0001-6954-9876 |
| Ojus Mohan | Chemical Engineering | 0000-0003-0298-2725 |
| Partha Sarathi Goswami | Chemical Engineering | 0000-0002-3835-5929 |
| Pramod P Wangikar | Chemical Engineering | 0000-0003-0108-7585 |
| Ratul Dasgupta | Chemical Engineering | 0000-0003-0621-3472 |
| Ravindra D Gudi | Chemical Engineering | 0000-0002-1655-3887 |
| Sameer Jadhav | Chemical Engineering | 0000-0002-4207-3393 |
| Sandip Roy | Chemical Engineering | 0000-0002-0303-8018, 0000-0003-2572-784X |
| Sanjay M Mahajani | Chemical Engineering | 0000-0001-9911-5120, 0000-0003-4289-0454 |
| Sarika Mehra | Chemical Engineering | 0000-0003-3844-4726 |
| Sayantan Dutta | Chemical Engineering | 0000-0002-3366-735X |
| Sharad Bhartiya | Chemical Engineering | 0000-0002-2856-695X |
| Sonali Das | Chemical Engineering | 0000-0002-4971-8780 |
| Sudarshan Vijay | Chemical Engineering | 0000-0001-8242-0161 |
| Sujit S Jogwar | Chemical Engineering | 0000-0002-7641-4635 |
| Supreet Saini | Chemical Engineering | 0000-0001-6838-4619 |
| Venkat Gundabala | Chemical Engineering | 0000-0003-0159-662X, 0000-0001-5574-8735 |
| Vinay A. Juvekar | Chemical Engineering | 0000-0002-6535-4112, 0000-0001-5574-8735 |
| Y. S. Mayya | Chemical Engineering | 0000-0003-4848-4692, 0000-0001-6161-6819, 0000-0003-0367-8661, 0009-0000-6225-2869 |
| Anil Kumar | Chemistry | 0000-0003-3658-4944, 0000-0002-6787-7259, 0000-0001-5391-754X, 0000-0003-4932-1270 |
| D M Dewaikar | Civil Engineering | 0000-0001-9522-7838, 0000-0003-0014-7347, 0000-0002-9309-5592, 0000-0001-6273-2985 |
| Jangid R | Civil Engineering | 0000-0002-5278-6223, 0009-0006-0512-6480 |
| Kamal M Bajoria | Civil Engineering | 0009-0005-3073-3699 |
| Nutan Limaye | Computer Science and Engineering | 0000-0002-0238-1674 |
| Indira Mishra | Desai Sethi School of Entrepreneurship | 0009-0000-1023-8213 |
| Radhika Sachdeva | Desai Sethi School of Entrepreneurship | 0009-0008-4696-3415, 0009-0004-5523-1452 |
| Rajiv Kumar Jain | Desai Sethi School of Entrepreneurship | 0009-0006-4824-4540, 0000-0003-4174-8587, 0000-0002-2535-1785 |
| Ramesh Kuruva | Desai Sethi School of Entrepreneurship | 0000-0002-8501-7447, 0000-0001-6885-4641 |
| Sankalp Pratap | Desai Sethi School of Entrepreneurship | 0000-0001-9699-1838 |
| Shakti Tripathy | Desai Sethi School of Entrepreneurship | 0000-0003-1559-0106 |
| Shruti Gupte | Desai Sethi School of Entrepreneurship | 0009-0003-8647-2710 |
| Mohammad Ayaz Alam | Earth Sciences | 0000-0002-3189-8744 |
| Ajit Kumar Verma | Electrical Engineering | 0000-0002-2931-3743, 0000-0002-3311-507X |
| Animesh Kumar | Electrical Engineering | 0009-0000-0940-8094 |
| Deepak Jain | Electrical Engineering | 0000-0001-5849-454X, 0000-0002-4742-7904 |
| Kunal Ghosh | Electrical Engineering | 0009-0006-3547-9615 |
| Madhav Pandurang Desai | Electrical Engineering | 0000-0002-2594-3270 |
| Prashant Navalkar | Electrical Engineering | 0009-0009-1881-5113 |
| Vinay Kulkarni | Energy Science and Engineering | 0000-0002-4531-2329, 0000-0001-5574-8735 |
| Anil Kumar Dikshit | Environmental Science and Engineering | 0000-0003-3658-4944, 0000-0002-6787-7259, 0000-0001-5391-754X, 0000-0003-4932-1270 |
| Harish C. Phuleria | Environmental Science and Engineering | 0000-0001-5801-0015 |
| Indrajit Chakraborty | Environmental Science and Engineering | 0000-0002-0812-2593 |
| Munish Chandel | Environmental Science and Engineering | 0000-0003-2233-5082 |
| Pradip Kalbar | Environmental Science and Engineering | 0000-0002-1436-3609 |
| Renuka Verma | Environmental Science and Engineering | 0000-0001-8757-5031 |
| Sanjeev Chaudhari | Environmental Science and Engineering | 0000-0002-3605-7418 |
| Shyam R. Asolekar | Environmental Science and Engineering | 0000-0002-0399-697X, 0000-0003-4172-8615 |
| Srinidhi Balasubramanian | Environmental Science and Engineering | 0000-0002-6561-5984 |
| Tabish Nawaz | Environmental Science and Engineering | 0000-0002-7851-3194 |
| AZIZUDDIN KHAN | Humanities and Social Sciences | 0000-0001-5113-4760 |
| Amrita Banerjee | Humanities and Social Sciences | 0000-0002-1977-4685 |
| Anush Kapadia | Humanities and Social Sciences | 0009-0004-7699-7633 |
| Arun Iyer | Humanities and Social Sciences | 0009-0008-0790-2089, 0009-0003-0329-4905, 0000-0001-7377-7599, 0000-0001-7014-8981 |
| C. D. SEBASTIAN | Humanities and Social Sciences | 0000-0002-8916-6028, 0000-0003-2555-0263, 0000-0002-0800-6787, 0000-0002-9129-4766 |
| Deepak Naorem | Humanities and Social Sciences | 0009-0003-2479-4933 |
| Ilito H. Achumi | Humanities and Social Sciences | 0000-0002-8977-2554 |
| Mahendra Shahare | Humanities and Social Sciences | 0000-0003-0933-9791 |
| Mrinal Kaul | Humanities and Social Sciences | 0000-0003-0256-833X |
| Naina Manjrekar | Humanities and Social Sciences | 0009-0006-6479-6011 |
| RAJAKISHORE NATH | Humanities and Social Sciences | 0000-0003-0855-9709 |
| RANJAN K. PANDA | Humanities and Social Sciences | 0000-0002-8909-4271, 0000-0002-2421-0120 |
| RATIKANTA PANDA | Humanities and Social Sciences | 0009-0006-3587-3495 |
| Rachel A. Varghese | Humanities and Social Sciences | 0009-0000-4671-5376 |
| Raile R. Ziipao | Humanities and Social Sciences | 0000-0003-3527-4362 |
| Rashmi Gupta | Humanities and Social Sciences | 0000-0002-5157-0260 |
| SARMISTHA PATTANAIK | Humanities and Social Sciences | 0009-0006-9635-9203 |
| Shweta Chawak | Humanities and Social Sciences | 0000-0001-8732-1357 |
| Smriti Haricharan | Humanities and Social Sciences | 0009-0003-6399-5703 |
| Suddhaseel Sen | Humanities and Social Sciences | 0000-0003-3495-8690 |
| Suryakant Waghmore | Humanities and Social Sciences | 0000-0001-6892-6780 |
| VAIJAYANTHI SARMA | Humanities and Social Sciences | 0000-0003-4852-9248, 0000-0001-5574-8735 |
| VIKRAM SINGH SIROLA | Humanities and Social Sciences | 0000-0002-8950-6125, 0000-0001-5574-8735 |
| Nirmal Punjabi | Koita Centre for Digital Health | 0000-0002-3953-0936 |
| Sandip Mandal | Koita Centre for Digital Health | 0000-0003-3396-639X, 0000-0001-5651-8632 |
| Santanu Kumar Ghosh | Koita Centre for Digital Health | 0000-0001-5040-4845, 0000-0003-0149-368X, 0000-0003-4566-1040 |
| Srikanth Srinivasan | Mathematics | 0000-0001-6491-124X |
| Arun Kamble | Mechanical Engineering | 0009-0008-0790-2089, 0009-0003-0329-4905, 0000-0002-9854-9872, 0000-0001-7014-8981 |
| Bhallamudi Ravi | Mechanical Engineering | 0000-0001-7558-0423 |
| Uddipta Singha | Mechanical Engineering | 0009-0005-9541-3709 |
| MJNV Prasad | Metallurgical Engineering and Materials Science | 0000-0003-4651-6419 |
| Aftab Alam | Physics | 0000-0003-1717-7438 |
| Alok Shukla | Physics | 0000-0002-0839-2956 |
| Amitabha Nandi | Physics | 0000-0002-6688-0237 |
| Anirban Sain | Physics | 0000-0002-3653-1204, 0000-0003-0641-0935 |
| Anshuman Kumar | Physics | 0000-0002-7433-8341 |
| Asmita Mukherjee | Physics | 0000-0002-0229-5565 |
| Avinash V. Mahajan | Physics | 0000-0003-3241-6660 |
| Basanta Kumar Nandi | Physics | 0009-0007-3988-5095, 0000-0003-3141-5084 |
| C.M. Srivastava | Physics | 0000-0001-6736-0105, 0009-0000-4196-2642, 0000-0003-2555-0263, 0000-0001-8444-9953 |
| Debojit Sarkar | Physics | 0000-0002-2393-0804 |
| Gopal Dixit | Physics | 0000-0003-2474-0807 |
| Himadri Shekhar Dhar | Physics | 0000-0002-5877-3415 |
| Hridis Kumar Pal | Physics | 0009-0005-6918-0104 |
| Kantimay Das Gupta | Physics | 0000-0002-3941-0520 |
| Manibrata Sen | Physics | 0000-0001-7948-4332 |
| Maniraj Mahalingam | Physics | 0000-0001-7305-1368 |
| Mohammed Aslam | Physics | 0000-0003-2782-0167 |
| Nitin Kumar | Physics | 0009-0005-8870-4807, 0000-0003-2697-4842 |
| Pradeep Sarin | Physics | 0000-0003-0754-5460, 0000-0002-6308-7348, 0000-0003-4381-5261 |
| Pramod Kumar | Physics | 0009-0001-8921-4122, 0000-0001-6988-2660, 0000-0003-0474-080X, 0000-0003-1617-3232 |
| Prashant Kumar | Physics | 0000-0002-5800-2768 |
| Punit Parmananda | Physics | 0000-0001-5410-5148 |
| Raghunath Chelakkot | Physics | 0000-0003-3704-3541 |
| Rahul Kashyap | Physics | 0000-0002-6897-9521, 0009-0008-8173-2049, 0000-0002-4293-2303, 0000-0002-5700-282X |
| Sai Vinjanampathy | Physics | 0000-0002-5919-5442 |
| Sayantika Bhowal | Physics | 0000-0002-4134-7540 |
| Shiva Prasad | Physics | 0000-0002-7871-5175, 0000-0002-9535-3989 |
| Soumya Bera | Physics | 0000-0001-6701-8107 |
| Subhabrata Dhar | Physics | 0000-0003-1530-4819 |
| Subhaskar Mandal | Physics | 0000-0002-3202-9364 |
| Sumiran Pujari | Physics | 0000-0003-2262-6752 |
| Sunita Srivastava | Physics | 0000-0003-1781-5655 |
| Varun Bhalerao | Physics | 0000-0002-6112-7609, 0000-0001-5574-8735 |
| Vikram Rentala | Physics | 0000-0002-8394-2006, 0000-0001-5574-8735 |
| Parthe Pandit |  | 0000-0002-2524-8817 |

## 11. Known gaps
* Units with unreachable sites rely on archived lists (latest 2025/2026) + NIRF; their designations are often blank.
* Wayback density was ~1 snapshot per 2 years; former faculty who joined and left between two snapshots and were never in NIRF (i.e. left before ~2017) can be missed; LAST may be early by ≤1 year for Wayback-only formers.
* NIRF 2022 edition not available (institute page lacks it; nirfindia.org blocks with 403).
* CDTIS, SemiX, MedTRIC, MOCCM have no own faculty lists; any faculty appointed only there are missing.
* Designation missing for many current faculty on pages that do not print it (CSE, EE, Chemistry, Aero) and NIRF lacked them.
* Google Scholar/DBLP only for CSE (institute API); profile pages were not crawled for identifiers.


## Post-review edit (main session, 2026-10-26)
* Removed the row `S. Akshay` (Ashank Desai Centre for Policy Studies): same person as `Akshay S` (Computer Science and Engineering), listed by the centre as associated faculty. Associated-faculty listings never create unit membership. Roster now 1,286 rows.
