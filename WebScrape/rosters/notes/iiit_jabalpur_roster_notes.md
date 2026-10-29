# PDPM IIITDM Jabalpur faculty roster (2016-2026): lab notebook

Built 2026-10-27 by the IIIT-team run (operator Arihant Tripathy). Output: `WebScrape/rosters/iiit_jabalpur_faculty.csv` (129 rows).
Every fetch went through `agents/polite_get.py`. Downloaded pages, PDFs and parsing scripts are in `C:/Users/Arihant/rm_work/iiit_jabalpur_roster/{data,code}`, not in the repo.
(One exception to note: before the fetcher had been used, a single direct `requests.get` of `https://www.iiitdmj.ac.in/` was made to read the response headers when the cached body looked binary. It was one request and nothing was stored from it.)

## Totals

| status | rows | joining_year filled | ORCID | e-mail |
|---|---|---|---|---|
| current | 73 (regular faculty incl. the Director, 1 INSPIRE faculty, 1 on lien) | 73 | 41 | 64 |
| former | 28 | 28 | 5 | 8 |
| visiting | 28 (8 currently listed) | 26 | 0 | 0 |
| adjunct / emeritus | 0 | 0 | 0 | 0 |
| **total** | **129** | **127** | **46** | **72** |

Other identifiers: Google Scholar 6 (institute profile pages / card links), homepage 28 (`site.iiitdmj.ac.in/<id>.php`, Google Sites, `hamlab.iiitdmj.ac.in`, a BHU profile), DBLP/Scopus/IRINS 0 (none found on institute pages; the brief forbids IRINS/Scopus scraping).

### Per-unit counts (department = current official unit name)

| unit | current | former | visiting |
|---|---|---|---|
| Computer Science and Engineering (CSE) | 16 | 8 | 0 |
| Electronics and Communication Engineering (ECE) | 16 | 8 | 0 |
| Mechanical Engineering (ME; includes the Smart Manufacturing group) | 22 | 9 | 0 |
| Natural Sciences (NS: Physics + Mathematics) | 13 | 0 | 0 |
| Design | 4 | 1 | 0 |
| Liberal Arts (LA; English / Humanities) | 2 | 0 | 2 |
| (unit not printed by any source) | 0 | 2 | 26 |

NS split: Physics 6 (Mishra, Kundu, Roy, Jaiswal, Jena, Katharria) plus Bhartendu K. Singh (Professor of Physics, Director); Mathematics 6 (Gupta, Deepmala, Balyan, Panda, Mahato, Lamba). Smart Manufacturing (`sm.iiitdmj.ac.in`, a stub site) has no separate faculty list; K. Ponappa is its Head per the ME page, so he is filed under ME.
Unit-name mapping: "Computer Science & Engineering" became "Computer Science and Engineering"; "Electronics & Communications Engineering" and "Electronics & Communication Engineering" both became "Electronics and Communication Engineering"; "Mechanical Engineering & Design" (Tandon) and "Design Discipline/Design Programme" became "Mechanical Engineering" / "Design"; "Physics", "Mathematics", "Mathematics (NS)", "Natural Sciences Discipline" became "Natural Sciences"; "English Language and Literature", "Liberal Arts - English" and the 2016 "Humanities & Social Sciences" became "Liberal Arts". The 2016 site also had "Humanities & Social Sciences" (H&S) and "Discipline" index pages; no other unit exists. Campus: single campus (Dumna Airport Road); no second campus.

## Independent size check

* NIRF 2026 faculty list (institute's own submission, file `Faculty list 2026 NIRF.pdf`, 105 rows): 84 rows flagged "currently working" = 75 Regular + 1 Adhoc/Contractual + 8 Visiting; 21 rows flagged not working (5 Regular, 16 Visiting).
* My current rows: 73 (72 NIRF-confirmed + Manish Bajpai), plus 8 currently listed visiting people = 81 people with a current status, against NIRF's 84 (75 Regular + 1 Adhoc + 8 Visiting). The gap of 3 regular is the four leavers minus Bajpai; the 8 visiting match exactly.
* NIRF-confirmed current rows: 72 of 73 current rows are "Yes" in NIRF 2026 (Regular/Adhoc). The exception is Manish Kumar Bajpai (see conflicts).
* Difference to NIRF (76 Regular+Adhoc "Yes" vs my 72 NIRF-confirmed regular rows): 4 people NIRF 2026 still shows as working but dated sources show had left (Manoj Singh Parihar, Vinod Kumar Jain, Vijaypal Singh Rathor, Vikas Chauhan; Annual Report 2024-25 gives exit dates). I moved them to former. Manish Bajpai is the one person counted current who NIRF says left.
* Other cross-check: the institute faculty page `faculty.iiitdmj.ac.in` lists 64 people (plus one spam card, see Problems); it is an opt-in list, so it is smaller than NIRF. Current rows without a profile on it (9, so NIRF-only or department-page-only): Avinash Chandra Pandey, Munesh Singh, Neelam Dayal, Rakesh Kumar Sanodiya, Atul Kumar, Pankaj Sharma, Pravin N Kondekar, Varun Bajaj, Parikshit Kundu. Annual Report 2024-25 department lists (Apr 2024-Mar 2025): CSE 19, ECE 15, ME 21, NS 13, Design 4, LA 2 = 74 names, including the four leavers above; it omits Varun Bajaj and Atul Kumar (ECE) and J.K. Tiwari (INSPIRE). My 73 current is consistent with these.
* The institute's roughly 70-80 regular faculty matches the "faculty strength" implied by the NIRF tables of 2019-2026 (59 to 75 regular "Yes" rows per year).

## Sources and endpoints

1. **Institute website** (`www.iiitdmj.ac.in`, behind Sucuri, serves `Content-Encoding: br`). `polite_get.py` stores the raw body, so bodies are brotli-compressed on disk; I installed `brotli` into a private folder (`code/lib`) and decoded in my own scripts. The fetcher itself was not changed.
   * `http://faculty.iiitdmj.ac.in/` (institute faculty list, 129 cards in 7 tabs, 65 unique profiles; tabs All/CSE/Design/ECE/ME/Natural Science/Liberal Arts; fields: name, unit, designation, research interests, profile link). Profile pages `/faculty/<id>` (64 fetched): e-mail, personal web page, "Professional Experience" text. No JSON/AJAX endpoint (server-rendered PHP).
   * Department sites: `cse.iiitdmj.ac.in/faculty.php` (also `faculty_page.php?id=<email>` links, used for e-mails), `ece.iiitdmj.ac.in/faculty.html` (stale, shows 2019-era staff such as Ravi Panwar, I.A. Ansari, Biswajeet Mukherjee), `me.iiitdmj.ac.in/faculty.html` (stale, still lists the Smart Manufacturing head as ME), `ns.iiitdmj.ac.in/faculty.php`, `design.iiitdmj.ac.in/faculty`, `la.iiitdmj.ac.in/Faculty.html`, `cse.iiitdmj.ac.in/visitingfaculty.php`. `sm.iiitdmj.ac.in` is an empty stub.
   * `administration/director.php`, `Deans.php`: 404/empty; the Director is taken from NIRF and the annual reports.
2. **NIRF data submissions** on `www.iiitdmj.ac.in/nirf.iiitdmj.ac.in/downloads/...` (the institute's own NIRF page). Each PDF has a "Faculty Details" table (name, age, designation, qualification, months of experience, currently working flag, joining date, leaving date, association type Regular/Visiting/Adhoc). Used all years available: 2018 (`Submitted_Data_NIRF_2018_DCS.pdf`), 2019 (`All Report-MHRD ... 2019.pdf`), 2020 (`NIRF 2020 Data.pdf`), 2021 (`NIRFENGG.pdf`, undated; inferred), 2022, 2023 (Engineering and Overall), 2024 (Engineering and Overall), 2025 and 2026 (Engineering; same tables as the separate `Faculty List` PDFs). 11 tables, 8 to 105 rows each, 135 name keys. Parsed with `pdftotext -raw` and a sequential-numbering parser (code/nirf2.py); no unparsed rows; counts match the last serial number of each table.
3. **Internet Archive:** CDX query `cdx/search/cdx?url=faculty.iiitdmj.ac.in/&output=json&from=2016&to=2026&filter=statuscode:200&collapse=timestamp:6` gave 64 monthly captures (2017-06 to 2026-04). 16 were fetched as raw `id_` snapshots (2017-06, 2018-01, 2019-07, 2019-12, 2020-06, 2021-01, 2021-06, 2022-01, 2022-06, 2023-02, 2023-10, 2024-04, 2024-10, 2025-02, 2025-10, 2026-04; 53 to 74 cards each). Old main-site people pages found by CDX prefix query `www.iiitdmj.ac.in/people/*` and `/People/*`: `People/faculty.html` (2016-03-04), `People/{CSE,ME,Maths,ECE,Design,H&S,Discipline}.html` (2016-04 to 2016-07), `people/faculty.php` (2017-02-05). The Discipline pages of 2016 carry e-mails; the 2017 page carries units.
4. **Annual reports** (`downloads/Annual Report/Annual Report <yr> (English).pdf`, 2015-16 to 2024-25 downloaded). Text-extractable: 2015-16, 2016-17, 2019-20, 2021-22, 2022-23, 2024-25. Image-only (no text layer, not OCR'd): 2017-18, 2018-19, 2020-21, 2023-24. Used for faculty tables, resignation lists (2015-16), visiting-faculty tables (2015-16, 2016-17) and the dated "Upto"/"On lien" notes in the 2024-25 department lists.
5. **ORCID public API** (identifiers only): one `expanded-search` with `affiliation-org-name:(IIITDM OR IIITDMJ OR "Design and Manufacturing Jabalpur" OR "PDPM Indian Institute" OR "PDPM IIITDM" OR (Jabalpur AND "Information Technology" AND Manufacturing)) OR ror-org-id:"https://ror.org/03vk3mj95"`, 3 pages of 200, 554 profiles. (I guessed the ROR id; it is unverified and may match nothing; the name tokens did the work.) Then 51 `/employments` calls for name-matched candidates. No 429 was returned. No per-person searches.

## How current, former and tenure years were established

* **Core:** every NIRF table row is a person-year observation; people were merged by normalised name (aliases: Asish K Kundu / Kumar Kundu, Ishad / Irshad Ahmad Ansari, Mohana / Mohona Ghosh). Joining year = year of the earliest NIRF joining date for the person (one documented exception below). Leaving year = year of the NIRF leaving date. NIRF leaving dates are entered retroactively and lists lag (Pavan Kankar left 03-12-2018 but is still "Yes" in 2019 and 2020), so the leaving date, not the last list, is used.
* **Current** = "Yes, no leaving date" in NIRF 2026 (submitted Oct-Nov 2025) or on the live institute faculty list. The institute list wins on conflict (brief tie-break).
* **Overrides from dated sources:** Annual Report 2024-25 shows "(Upto 26/11/2024)" for Vinod Kumar Jain, "(Upto 25/07/2024)" for Vijaypal Singh Rathor, "(Upto 03/12/2024)" for Manoj Singh Parihar, and "(16/08/2024 to 13/12/2024)" for Vikash Chouhan (NIRF name: Vikas Chauhan). All four are shown as current in NIRF 2026, so they are former with LAST=2024.
* **Former faculty:** all 28 have a NIRF leaving date, except Navjeet Bagga, Sanjeev Jain and Arundhati Arjaria (see Ambiguous). Window rule applied: Anurag Singh (left 2014), Ashutosh Srivastava (2014), Brajesh Pandey (2014), Rajesh Kumar Pandey (2014), Rajib Kumar Jha (2014), Ravibabu Mulaveesala (2012), Vinay Kumar Singh (2015) and Jayesh Pillai (18-12-2015) are in the 2018 table with leaving dates before 2016-01-01 and are excluded. Likewise K.K. Balakrishnan (resigned 04-12-2015, AR 2015-16).
* **Stale archive pages:** the March and July 2016 `People/*.html` pages still list people who had left (Ravibabu 2012, R.K. Pandey, R.K. Jha, B. Pandey, A. Srivastava, all in 2014). So none of the 2016 pages was used as presence evidence on its own. The 2017-02 page is maintained (it lists Kusum Bharti, joined 09-2016).
* **joining_year exception:** Sachin Kumar Jain: NIRF date 26-12-2007 is the start as Research Engineer; his profile says Assistant Professor from July 2013, so 2013 is used. Joining years of regular faculty agree with the profile "Professional Experience" text in every case checked (Sunil Agrawal 2006, Prabin Padhy 2007, Dinesh Kumar 2009, Prashant K. Jain 2009, Trivesh Kumar 2017, Ponappa 2019, Deepmala 2016, Pushpa Raikwal 2020).
* **Sanjeev Narayan Sharma:** NIRF 14-09-2021 (profile shows a Professor post from 2013 at an earlier employer); 2021 is used.
* FIRST in "(FIRST-LAST)" is the joining year (can be before 2016).

## Identifier counts by route

* ORCID from an institute page: 1 (Pushpa Raikwal, link on her profile page; the ORCID record also shows PDPM IIITDM Jabalpur employment).
* ORCID from the affiliation search plus employment check (employment at an IIITDM Jabalpur organisation name and a name match): 45.
* Checked and rejected (blank): Sachin Kumar Jain 0000-0002-6533-2474 (employment string is only "IIITDM", could be Kancheepuram/Kurnool/Jabalpur); Rohit Kumar 0000-0002-3039-9679 and Vinay Kumar Singh 0000-0001-6143-9242 (no Jabalpur employment). Several name-matched candidates were not checked because they obviously belong to other people (Bhartendu/Vinay Singh look-alikes, Manish Kumar Thakur/Ashish Kumar Thakur, etc.). Two candidates for Manu Srivastava existed; only 0009-0006-3711-9330 shows Jabalpur employment.
* Weak accepts, kept (name common, employment at PDPM and consistent role/years): Durgesh Singh 0000-0002-6078-1502 (employment has no dates), Anil Kumar 0000-0002-3945-4646, Atul Kumar 0000-0002-2237-0200 (his ORCID end year 2023 is self-declared, not used as evidence).
* ORCID lookup pending: none (no 429). Most people have no ORCID because no per-person searches were run.
* Self-declared ORCID employment end dates that conflict with NIRF 2026 "Yes": Varun Bajaj 2024, Atul Kumar 2023, Parikshit Kundu 2025, Vijaypal Rathor 2024, Vikas Chauhan 2024. Not evidence; only the Annual Report 2024-25 exits (Rathor, Chauhan) were used.

## Conflicts and ambiguous people (decision taken)

* **Manish Kumar Bajpai:** NIRF 2024-2026 shows left 22-11-2023, but the institute faculty page (all 2024-2026 snapshots and the live page) and the CSE department page list him, "Assistant Professor (On Lien)"; AR 2024-25 also says "(In lien)". Institute list wins: current, designation "Assistant Professor (on lien)". This is the one current row not NIRF-confirmed.
* **Varun Bajaj and Atul Kumar (ECE):** NIRF 2026 says working; they are absent from the live institute list (opt-in) and from the ECE list in AR 2024-25. No dated departure found. Kept current; may have left in 2024-25.
* **Goutam Dutta:** NIRF says left 16-12-2018 (entered in the 2023 table); AR 2019-20 lists him "on lien". LAST=2018 per NIRF.
* **Two Sachin Kumars:** one Assistant Professor ME joined 28-12-2016, left 14-05-2017 (NIRF 2018; AR 2016-17); another joined 29-02-2024 (current). Different people (the current one's profile does not list IIITDMJ in 2016-17), so two rows. Profile, e-mail and ORCID belong to the current one only.
* **Two Abhishek Vermas:** a regular CSE Assistant Professor (PhD NIT Kurukshetra, age 29-30; joined 02-08-2021, left 24-05-2023; AR 2021-22 and 2022-23 CSE lists) and a Master of Design person on Adhoc/Visiting terms (2018 to 2023, age 34-36). Two rows; the visiting one has no unit.
* **Bhartendu Kumar Singh:** NIRF dates 02/08-05-2017 (Professor, NS) and 01-05-2023 (Director). Joining year 2017; designation "Professor and Director".
* **Sanjeev Jain (Director 2019-2023, CSE, PhD Barkatullah University):** NIRF "Dean/Director, Adhoc" from 13-04-2019, listed in 2020-2023, absent after Bhartendu Singh took over on 01-05-2023. Former, 2019-2023, department set to CSE from the AR 2019-20 area ("Computer Science Engineering").
* **Pramod Kumar Jain (Director, CAD/CAM):** NIRF Adhoc, 14-12-2015 to 11-12-2017; the 2017 page and AR 2016-17 list him as Director, Professor. Filed under ME; FIRST=2015 because the appointment began in December 2015.
* **Navjeet Bagga (ECE):** NIRF 2022 and 2023 "Yes", no leaving date; on website snapshots until 2023-02; not in AR 2022-23. LAST=2022 chosen, uncertain by about a year.
* **Arundhati Arjaria:** only in NIRF 2022 (Visiting, joined 05-08-2017, working). No leaving date. LAST=2021 (the table's reference year); uncertain.
* **Shekhar Chatterjee (Design):** "Visiting Faculty" on the 2016 and 2017 archived pages and in AR 2015-16/2016-17, but NIRF 2018-2021 gives Regular Assistant Professor from 03-06-2013, left 30-11-2019 (AR 2019-20: "Upto 30-11-2019"). Treated as former faculty, 2013-2019.
* **Puneet Tandon:** listed under Mechanical Engineering and Design; one row under ME, second unit Design. **Dinesh Kumar V / Vishwakarma** is the same person (the site prints "Dinesh Kumar V"; NIRF and ARs print the full name; the full name is used). **Mohona Ghosh:** site spelling used; NIRF spells it Mohana.
* **Jitendar Kumar Tiwari** is a DST INSPIRE Faculty (NIRF "Adhoc/Contractual"); kept current with that designation.
* **Visiting people:** all 26 NIRF "Visiting" or "Adhoc" non-regular rows (2017-2025) are included as `visiting` because the institute itself lists them in its faculty table; NIRF gives no unit and most have designation "Other". Their tenure is the min joining and max leaving year over the tables. Several visiting dates change between tables (the 2026 table re-enters 2023 dates for some); the widest range is used. The Master of Design qualification of several suggests the Design unit, but this was not asserted. The Japanese visiting professors of the CSE visiting page (Akinori Ito, Hironori Washizaki, Hisa Ando, Kouichi Sakurai, Takashi Nanya, Yasushi Yamaguchi) have no dates and were excluded (honour roll).
* **Two AR-dated visiting professors added:** Akio Haga (Japanese language, AR 2015-16 faculty table; resigned 01-02-2016) and Vineeta Kaur Saluja (English, "Upto 03-06-2016", AR 2016-17). Range (2016-2016) because the evidence year is 2016; the earlier start is not documented.
* **Not included, evidence only on stale 2016 pages:** Manish Shrivastava (CSE, "Mr."), T V K Gupta and Hari Kumar Varungati (ME visiting faculty). Not in any NIRF table (the 2018 table lists leavers back to 2012, so a 2016 leaver would appear) nor annual report. Also excluded: Izumi Haga (visiting scholar), Saket Saurav (listed with research engineers), K K Balakrishnan (left Dec 2015).
* **Mentor institute:** no mentor-faculty arrangement is documented on any source read (the site and annual reports mention none); no mentor rows.
* **Honorary/adjunct/emeritus:** none found for this institute.

## Problems and how they were resolved

* **Brotli bodies:** the institute CDN returns `Content-Encoding: br` and the fetcher cached undecoded bytes. Resolved by decoding in my own scripts with a locally installed `brotli`; fetch behaviour unchanged.
* **NIRF PDF layout:** `pdftotext -layout` scrambles columns of the faculty tables (and mixes pages); `-raw` keeps each row. Page footers with dates/URLs (2018 table) break the serial-number logic and were stripped.
* **NIRF year labelling:** the file `NIRFENGG.pdf` is undated; it covers data up to AY 2020-21, so it is treated as NIRF 2021. The 2019 file is the "All Report ... 2019". NIRF year N reflects the state at about Oct-Nov of N-1.
* **Spam entry:** the live faculty list has a card "wangbantar" (`/faculty/zerobanter1337`) with no unit or designation. Not a person; excluded.
* **Name collisions** (Abhishek Verma, Sachin Kumar): handled by joining date and age.
* **Dead/blocked hosts:** none. No bot walls were met. Wayback was slow when shared; a few requests exceeded the shell timeout and ran in the background.
* **Per-person source URLs** are listed as: live faculty list and profile, the 16 Wayback faculty-list snapshots where the person appears, the NIRF PDFs of the years they appear, and the Wayback 2016/2017 pages, live department pages and annual reports where a name match was found (the match is text-based and skipped for the two name-collision pairs, which therefore have fewer URLs).

## Known gaps

* Annual reports 2017-18, 2018-19, 2020-21, 2023-24 are image-only and were not read; they could hold resignation lists or dated visiting-faculty tables.
* NIRF faculty tables cover only people in the Engineering (and Overall) submissions; staff on short contracts or people who joined and left between two consecutive NIRF snapshots may be missing. The 2016 snapshot had no NIRF table (first one is 2018, which lists leavers back to 2012).
* Visiting faculty: no unit for 26 of 28; designations are generic ("Other" in NIRF); the CSE foreign visiting list is undated and excluded.
* LAST years of Navjeet Bagga, Arundhati Arjaria and Sanjeev Jain are +/- 1 year. Varun Bajaj and Atul Kumar may have left in 2024-25.
* ORCID: 46 of 129 only; DBLP/Scopus/IRINS none; Google Scholar 6.
* E-mails: 72 (institute pages, 2016 archive pages, department pages); NIRF-only people (all visiting, most 2018-2023 leavers) have none.
