# IIIT Hyderabad faculty roster (2016-2026): lab notebook

Built 2026-10-27/28 by Arihant Tripathy (IIIT team). Output: `WebScrape/rosters/iiit_hyderabad_faculty.csv` (211 rows). Every fetch went through `polite_get.py`. Downloads: `C:/Users/Arihant/rm_work/iiit_hyderabad_roster/data`, scripts: `C:/Users/Arihant/work/iiit_hyderabad_roster/code` (not in the repo). Institute = International Institute of Information Technology Hyderabad (iiit.ac.in), not IIT Hyderabad / University of Hyderabad.

## Totals

| status | rows |
|---|---|
| current | 131 (123 also in NIRF 2026; 8 only on the website: new joiners, lecturers listed on /lecturers/) |
| adjunct | 31 (20 on the Adjunct Faculty page, 7 Distinguished, 1 Affiliate, 3 professors of practice) |
| emeritus | 9 (4 listed now: Dipti Misra Sharma, Rajeev Sangal, Harjinder Singh, Jayanthi Sivaswamy; 5 with ranges) |
| visiting | 15 (2 listed now) |
| former | 25 |

Rows by centre: LTRC 22, CCNSB 15, CSTAR 13, HSRC 17, SPCRC 14, CVEST 9, CVIT 10, SERC 9, EERC 8, RRC 6, LSI 5, CogSci 5, CSG 5, DSAC 5, CQST 4, MLL 3, iHub-Data 3, RCTS 2, CMC 2, BMRC 1, KCIS 1, CBS 1, CIE 1, CETLS 1; no centre recorded 49 (NIRF-only people, adjunct/visiting without a lab, people whose archived page printed no lab). Primary centre only; second centres are not recorded (profile pages show one centre; old snapshots list several, the first is used).
Identifiers (row counts): e-mail 122, homepage 83 (as printed on the institute profile), Google Scholar 11, DBLP 7, ORCID 5, Scopus 4, IRINS 0. joining_year 179 rows.
ORCID by route: institute profile 1 (P Pravin Kumar Venkat Rao); personal homepage printed 4 (Abhishek Kr Singh, Hrishikesh Rajesh Terdalkar, Indranil Chakrabarty, Vishal Garg); ORCID API 0 (no calls, daily quota exhausted).
DBLP: 2 from the institute profile (Nelakanti, Das), 5 from personal homepages (Varma, Kurri, Terdalkar, Vaidhyanathan, Gandhi: pid URLs). Abhishek Kr Singh's homepage prints a `pers/hd` DBLP URL, not a pid, so it was not entered.
ORCID lookup pending: everyone without an ORCID (206 rows).

## Sources and endpoints

1. Live site `https://www.iiit.ac.in/` (WordPress). robots.txt read first: disallows /wp-admin/, /wp-content/, /wp-includes/. `/faculty/` and `/faculty/page/N` are the same 12 names (JS paging), so profiles came from `faculty-sitemap.xml` (148 profile URLs, last modified 2026-10-06), each fetched once: name, designation, e-mail, centre, Scholar/ORCID/DBLP and homepage links. The same post type also holds staff profiles (many removed after 2024), only the 148 current ones were used. Lists: `/adjunct-faculty/` (21), `/distinguished-faculty/` (7), `/affiliate-faculty/` (1), `/lecturers/` (6 names). The WordPress REST API was not touched.
2. NIRF data submissions (Engineering DCS) 2019-2026 from `/nirf-report/`. The PDFs sit under /wp-content/ (disallowed), so they were read from Wayback copies of `cdn.iiit.ac.in/cdn/www.iiit.ac.in/wp-content/uploads/...` (snapshots 2025-10-01 to 2026-06-03; `web.archive.org/web/2id_/`). Faculty tables (joining/leaving date, currently working, association type) parsed with `pdftotext -raw` (`code/nirf.py`). Rows: 2026 157 (156 working), 2025 141, 2024 130, 2023 121, 2022 111, 2021 103, 2020 89, 2019 94. The 2019-2020 layout has an extra "associated last year" column; the "currently working" value is the second Yes/No.
3. Wayback snapshots of the old faculty list `https://www.iiit.ac.in/people/faculty/` (CDX `from=2016&to=2026&collapse=timestamp:6`; layout name / designation / degree / research areas / lab). Read (16): 2016-01-23 (different layout, not parsed), 2016-08-06, 2017-02-14, 2017-07-08, 2019-05-31, 2019-12-09, 2020-06-09, 2020-11-26, 2021-06-22, 2021-12-02, 2022-06-15, 2022-12-02, 2023-06-05, 2023-11-29, 2024-04-23, 2024-07-05 (72-111 names each). After mid 2024 the new `/faculty/` page is JS paged (12 names), so the last complete list is July 2024. CDX of `/faculty/*` (2024-2026) was used only to see which profile slugs existed in 2024-2025 and are gone now.
4. Personal homepages printed on profiles (53 fetched, 200 OK; 17 TLS failures, 6 404, 3 DNS, 2 timeouts, 1 403, 1 skipped, see incident) for DBLP/ORCID/Scopus links.
5. ORCID API: not used.

## How status, tenure and "former" were established

* current: has a profile in the faculty sitemap (tie-break: institute-wide list wins). Adjunct/distinguished/affiliate-page people with a profile -> `adjunct` (designation "Adjunct Faculty; <affiliation>"). Emeritus, Visiting, Professor of Practice designations follow the profile text (PoP -> adjunct, designation kept: Ramesh Loganathan, Praveen Garimella, Yalla Veera Prakash).
* NIRF-only current: people with "currently working = Yes" in NIRF 2026 and no profile but also no evidence of profile removal (Azeemuddin, Ubaidulla P, Bhaswar Ghosh, Arun Kumar Pati, Venkata Suresh Reddy P, Jayachandran, and 8 people who first appear in NIRF 2025/2026: Deepika M, Meghna Lowalekar, Santanu Mandal, Sarath Babu A, Subha Chakraburtty, Ramesh Dheeravath, Usha Gogineni, Vindhya Undurti). These are the weakest current rows: they may have left since the NIRF 2026 submission (data for AY 2024-25), or sit in a unit with no web profiles. Department blank.
* former: in a snapshot or NIRF row, not current. FIRST = NIRF joining year if known, else first snapshot year; LAST = max(last snapshot year, NIRF leaving date year, NIRF year minus 1 for a "Yes" row). Profiles that existed in Sept 2024 and are gone from the sitemap (Rahul Mishra, Nagamanikandan Govindan, Sarma K R, Venkateshwarlu M, Yegnanarayana B) got LAST at least 2024; where NIRF 2026 says Yes the LAST is 2025 (Nagamanikandan, Rahul Mishra, Venkateshwarlu M, Yegnanarayana). Emeritus/visiting people no longer listed keep that status with a range.
* joining_year: earliest NIRF joining date (regularisation or rejoining dates are possible; Bapi Raju S: NIRF 2014, listed as Visiting Professor in 2016). Left blank where the person was on the faculty list in 2016 and NIRF gives a later date, and for people not in NIRF. NIRF year given for people who left or became adjunct (e.g. Avinash Sharma 2015, Vishal Garg 2000).
* Archive gaps: no list snapshot between 2017-07 and 2019-05 (nobody who joined and left in that gap is visible), no parsable snapshot for Jan-Jul 2016, no complete list after July 2024. LAST years for 2017-2019 leavers rest on NIRF dates where present, otherwise on the last snapshot (Rahul Shrestha, Bhaskararao Peri: only the Aug 2016 list, so 2016-2016; Subramanian Ramanathan, Sanjay Rawat, Supriya Mohanty 2016-2017).

## Size check

NIRF 2026 (Engineering DCS, AY 2024-25) lists 157 faculty rows, 156 "currently working": 145 Regular, 11 Adhoc. After removing 13 Other/Adhoc/Visiting rows that are not on the faculty lists (see exclusions) 143 remain. The website now has 108 profiles of regular, emeritus, visiting and research faculty and 6 lecturers, plus 29 adjunct/distinguished/affiliate. My current + emeritus rows (listed or NIRF-confirmed) total 140; 123 of the 131 current rows are in NIRF 2026. Difference to the 143: people in NIRF 2026 who have left or turned adjunct since (e.g. Avinash Sharma, Vishal Garg, Ramesh Loganathan, Yalla Veera Prakash, Praveen Garimella are adjunct now), NIRF Lecturer/Other rows, and joiners after the submission (Aakansha, Khaliq Parkar, Angarika Rakshit and 2025-26 hires with no NIRF row).

## Exclusions

* Research scientists/staff: Chandrasekher Mukku (UGC Research Scientist), Venkata Suresh Kumar N, Abhishek Sarkar (Senior Research Scientist 2016-2020; a Dec 2022 snapshot prints "Abhisek Sarkar, Assistant Professor", after his NIRF leaving date, judged a different or mistyped entry), Ajoy Mondal, Shipra Dixit (NIRF "Other").
* Bagga R K ("Advisor Outreach", 2016-2017 list): staff-like.
* NIRF Other/Adhoc rows not on any faculty list: Andleeb Zahra, Aniket Pal, Geetika Arora, Gurpreet Singh Lehal, Harsha Satya, Himanshu Badani, Pawan Harish, Rakesh Srivastava, Sai Anirudh Karre, Shivakrishna Dasi, Som Kanjilal, Swajit Singh Goud, Yusuf Indorewala, Ziaul Haque Choudhury. Add them if the team wants ad hoc teaching staff.
* NIRF "Visiting"-type rows with designation Other are kept as `visiting` with a generic designation: Himanshu Warudkar, Mayank Mathur, Lakshmi Burra, Jayasree Saha, Ravi Warrier, Ritesh Kumar Dubey.
* Soma Paul (2016 list: Research Assistant Professor; later Senior Research Scientist [Part-time]; NIRF Regular 2005-2020) kept as former because the list gave a professor-type title.

## Ambiguous people and decisions

* "Santosh Ravikiran" (NIRF 2019-2026, Associate Professor, joined 2018-07-09) mapped to Ravi Kiran Sarvadevabhatla (CVIT) by title and joining year; no other source ties the names. joining_year 2018 rests on this mapping.
* Centre names: CDE (old) mapped to DSAC, CEH (old) mapped to HSRC, CSL to CogSci. These renames were assumed from lab acronyms, not checked against a page. Cyber Manthan Center is listed as its own centre (Sandeep Shukla, Goswami); it is part of CSTAR.
* Lecturers (Puja Chauhan, Shajil K G, Priya Prithiviraj, Tapasinath, Vamsi Madhavi, Satish Kathirisetti [part-time]) are on the Faculty menu's /lecturers/ page, so they are included as current, designation Lecturer. Vamsi Madhavi (Arts, dance) and Satish have no NIRF row. Drop these 6 if lecturers should not count.
* Research Professors (Nimmi Rangaswamy, Viswanath K) and the "Systems Associate Professors" (Semparithi Aravindan, Shatrunjay Rawat) are on the faculty list and kept as current.
* Duplicate profile slugs for one person (e.g. `vamshi-ambati` is the page of Vishal Garg) use the name printed on the page.
* Vishal Garg: Professor in NIRF 2026 (joined 2000), but the site lists him as adjunct (Plaksha University); status adjunct. Same for Avinash Sharma (IIT Jodhpur).

## Problems and resolutions

* polite_get cached a transient DNS failure as `DEAD:ConnectionError` for Wayback URLs; `--refresh` fetched them.
* `python3 -I` ignores PYTHONUTF8: used `-X utf8`.
* NIRF "currently working" parse bug (took the "associated last year" column) fixed and rerun.
* Security incident: the coordinator reported that Windows Defender quarantined the cached 404 body of `https://devalab.in/robots.txt` (Deva Priyakumar's personal site) as a Trojan. devalab.in was not fetched again, no cached body from it was opened or parsed, no links were followed, and the homepage scan skips it. That person's identifiers come from the institute profile only (the homepage URL string is kept as printed on the profile). The robots/404 request to devalab.in had been made by my own homepage scan before the notice.
* check_outputs.py also reports the golden-set notes as missing: not part of this task.

## Known gaps

* ORCID: 5 of 211. No API calls (quota). DBLP 7: run the DBLP-id tool for the rest; Google Scholar 11.
* No annual-report check of leavers (not searched); tenure for 2017-2019 leavers rests on two snapshots plus NIRF.
* No list for 2018 and early 2016; the current list for the 8 NIRF-only 2025/2026 joiners is unverified.
* 49 rows have no centre.
