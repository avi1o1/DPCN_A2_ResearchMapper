# IIIT Bhagalpur (iiit_bhagalpur) faculty roster, 2016-2026: lab notes

Operator: Arihant Tripathy (IIIT team). Run date 2026-10-30. Output: `rosters/iiit_bhagalpur_faculty.csv` (68 rows).
Working data: `C:\Users\Arihant\rm_work\iiit_bhagalpur_roster\data\`, scripts in `...\code\` (fetch_snaps.py, blocks.py, build.py, orcid_emp.py).

## Institute, campuses, look-alikes
* Indian Institute of Information Technology Bhagalpur (PPP IIIT), domain `iiitbh.ac.in` (Drupal 8 site). Not IIIT Bhubaneswar (iiit-bh.ac.in), not Bhagalpur College of Engineering (BCE), not Bihar Agricultural University.
* Campuses: transit campus in buildings provided by Bhagalpur College of Engineering, Sabour, from 2017 (AR 2019-20 section 6: "Transit Campus"; 50 acres allotted from the BCE land for the permanent campus). Own campus at Rani Talab, Sabour 813210 from 2024: stated in the brief; I did not find a page on iiitbh.ac.in that I fetched confirming the address/PIN or the move date, so those two facts are UNVERIFIED here (the contact-us page was not read). No faculty list distinguishes campuses, so department values do not depend on it.
* Mentor institute: IIT Guwahati since 20 April 2017 (AR 2019-20 section 4).
* Departments (current names, from the site): Computer Science & Engineering; Electronics & Communication Engineering; Mechatronics and Automation Engineering (site calls it "facultymea"; the 2019-20 AR says "Mechatronics"); Basic Science and Humanities (2017 site listed "HSS"/"Mathematics" faculty; mapped to BSH).

## Sources and URL patterns used
* Live institute list (Oct 2026): `https://iiitbh.ac.in/faculty` (all units on one page; fetched 2026-10-30).
* Department pages (new site, archived from 2020-10): `/faccse`, `/ecefac`, `/bshfac`, `/facultymea`. Old site (2017-02/2020): `/faculty.html` (carries "Joined the Institute on Month,Year" per person), `/admin.html` (Mentor Director etc.), `/faci.html` (not used: staff).
* Wayback CDX: `cdx/search/cdx?url=iiitbh.ac.in/<page>&output=json&from=2016&to=2026&filter=statuscode:200&collapse=timestamp:6`; raw snapshots `web/<ts>id_/<url>`. 80 snapshots fetched (first+last capture of each year per page; all captures of faculty.html and admin.html). The `/faculty` page exists in the archive only from 2024-02.
* NIRF 2026 data submission (Engineering and Overall, identical faculty tables with joining/leaving dates): the institute's `sites/default/files/NIRF/` index links to the two 2026 PDFs. Earlier NIRF years (2018-2025) are NOT published on the site and the Wayback copies of the NIRF index only show the same 2026 page; no earlier NIRF faculty table was found.
* Annual reports 2019-20, 2020-21, 2021-22, 2022-23 (site `Document/` PDFs, text via pdftotext). Later reports (2023-24 is a Google Drive link) not fetched.
* ORCID public API: one expanded-search (`affiliation-org-name:"Indian Institute of Information Technology Bhagalpur"`, 31 hits, 1 page) then `/employments` for 19 candidates.
* Not used: IRINS, Scopus, OpenAlex, Scholar; no JSON endpoint exists on the site.

## Counts
Rows: 68 = 35 current, 19 former, 8 adjunct, 6 visiting.
Current by unit (status `current` only): CSE 12, ECE 10, MEA 7, BSH 6. Other rows: former CSE/ECE/MEA/BSH mixed; blank department 5 (3 IIT Guwahati mentor directors, Alok Barua (page names Electrical Engineering, which is no unit of this institute), Richard Blanchard); 2 visiting HSS 2017 faculty carry the 2017 unit name.
Per-unit extraction vs NIRF 2026 (currently-working=Yes): NIRF has 34 yes rows; the live page has 18 regular (Director + 17) + 17 guest + Prasanta Sarkar. Differences: Gaurav Kumar and Sandeep Raj are NIRF-current (Mar 2026) but absent on the live page and the 2026-06-08/09 snapshots (rows `former`, see conflicts); Vivek Kumar and Pradeep Kumar Sahu NIRF-current and on the 2026-06 snapshots but absent from the live page (rows `former` 2026-2026, guest appointments that ended); 6 live guest faculty (Subhayu Ghosh, P. V. B. Bayari, Anita Chandra, Rounak Biswas, Sumit Raj, Nehal Ahmad) joined after the NIRF submission.
Guest faculty: listed on the institute's own faculty page under "Faculty on Contract" and counted by NIRF as Assistant Professor (Adhoc/Contractual); kept as `current` with designation "Guest Faculty" (brief: contract/adhoc listed on institute pages count as faculty). Downstream can filter by designation if guests should be excluded (17 current rows).

## Size check (independent)
NIRF 2026 (submitted March 2026): 38 faculty rows, 34 currently working (20 regular, 14 adhoc/contractual incl. Prasanta Sarkar), 4 left (Anvita, Dhrubajyoti Bhattacharya, Ravishankar Mehta, Ujjwal Biswas). My roster: 35 `current` + Prasanta Sarkar (adjunct) = 36 live-list people, of which 30 are NIRF-confirmed (29 current + Prasanta). NIRF-only people not on the live page: Gaurav Kumar, Sandeep Raj, Vivek Kumar, P. K. Sahu (all four on the 2026 archived site pages, so no NIRF-only person lacks a web record). Net: 34 (NIRF) - 4 (not on live page) + 6 (joined later) = 36. Matches.
The Annual Report 2022-23 lists 15 faculty with the Director; the 2026 site list is larger because of guest faculty (17).

## How former faculty and tenure years were established
* FIRST-LAST = first and last year of presence on an archived, maintained faculty list; LAST also checked against NIRF leaving dates and the ARs.
* joining_year: "Joined the Institute on" on the 2017-2020 site pages (Dheeraj Sinha, Himadri Nayak, Hiranmoy Pal, Rupam Bhattacharyya, Pati, Biswal, Gaurav, Mandal, Sunil, Anupam, Santu, Sanjay, Sandeep, Thejaswini, Mohit, Bhowmik, Sudin, Prakash, Suraj, Verma, Choubey (Apr 2019, AR also), Tewari (Sep 2020), Chandan Jha, Dilip, Abhinav, Dhrubajyoti, Pankaj, Om Prakash, Chetan, Ravishankar, Ujjwal, P.K. Jain) and NIRF 2026 joining dates (all others in NIRF). Where the two agree no note; Sateesh Kanakannavar 2023 from NIRF only; Prasanta Sarkar 2025 (NIRF 23-09-2025; first archive listing 2025-11).
* Blank joining_year (upper bound = first archived list year): Prabhat Kumar Jha (Visiting, first listed on /bshfac 2023-10; no earlier BSH capture shows him), Raj Senani / Alok Barua / P. K. Das (first on the live page after 2026-06-09), Subhayu Ghosh, P. V. B. Bayari, Anita Chandra, Sumit Raj, Nehal Ahmad, Rounak Biswas (first seen 2026-06 or live Oct 2026), Shashank Shekhar, Meena Rani (first listed 2017-08), Richard Blanchard (single capture 2018-03), the three IIT Guwahati directors (post held ex officio; mentoring started 2017-04).
* LAST-year limits: the faculty.html page has no captures between 2018-03-13 and 2019-05-15, so people who joined and left in that gap are invisible (known gap). AR 2019-20 also lists Mohit Kumar, Bhowmik, Anupam Kumar and Santu Das whose last dated listing is mid/late 2019; their LAST could be early 2020 (taken as 2019).
* Stale pages: dept pages kept old entries for a while (e.g. the MEA page lists only 4 people in 2021-2023 although Sunil Kumar Singh was already on the institute page of 2019); only presence on a page that also lists a newer joiner was used.

## Conflicts and ambiguous people (decisions)
* Gaurav Kumar, Sandeep Raj: NIRF "currently working" (Mar 2026) vs absent on the live list (tie-break: institute list wins) -> `former`, 2018-2026. Gaurav's last page capture 2026-02-04 (dept page 2026-01), Sandeep's 2026-04-13.
* Arvind Choubey (first Director from 2019-04-26; earlier Director-in-charge of IIIT Ranchi; senior professor NIT Jamshedpur) and P. K. Jain (Director & Professor, joined 2023-07, last listed 2025-04): held the institute's Director post -> `former` regular faculty, ECE. Madhusudan Singh Director since 2025-06-17 (NIRF), `current`.
* IIT Guwahati mentor/officiating directors listed on `/admin.html`: Gautam Biswas (Mentor Director, 2017-2019, handed over April 2019 per AR 2019-20), Pinakeswar Mahanta (Officiating Director, 2018 captures), Saurabh Basu (Officiating Director, appears in 2019-05..2020-02 captures, inside a commented-out HTML block, so uncertain). All three recorded `adjunct` (post-holders employed elsewhere, per operator instruction), joining blank.
* Hiranmoy Pal, Santu Das, Anupam Kumar, Mohit Kumar, Bhowmik, Kumar Neeraj Verma: "Assistant Professor (On contract)" on the institute page -> `former` regular faculty on contract.
* Sudin Ganguly "Visiting Faculty (On contract)", Vijay Kumar (ITS; "Professor (ECE)" then "Visiting Faculty (ECE)", spelled Vijoy in his e-mail), Pallav Kumar Dutta (Visiting Assistant Professor CSE), Shashank Shekhar ("Professor (English)"/Guest Faculty), Meena Rani (Guest faculty HSS): `visiting`. Sunil Kumar Singh was labelled "Visiting Faculty (On contract)" in 2019 but is Regular since 25-07-2018 per NIRF: `current`.
* Distinguished Professors (Raj Senani, Alok Barua, P. K. Das) are new on the live page; no dated source before 2026; kept as `adjunct` with blank year (honour-roll rule: the live page of 2026-10-30 is the dated source).
* Prabhat Kumar Jha: "Visiting Faculty" on BSH page since 2023-10, still listed -> `visiting` without range. Personal Gmail printed; not stored.
* Name decisions: "Dhurbajyoti" (misspelt 2021 page) = Dhrubajyoti; NIRF "Mondal" = Mandal (site spelling kept); NIRF "Tameshwer Nath Tiwari" vs site "Tameshwer Nath" (site kept); NIRF "Bijendra Sangar" = Brijendra Sangar; site "Viwek Kumar" -> Vivek Kumar (as in NIRF); Rupam Bhattacharya/Bhattacharyya same person; ORCID "Sateesh Kumar" not used. Rounak Biswas shows no department on the page; BSH inferred from his e-mail (`rbiswas.bsh`).
* Excluded as non-faculty: technical officers on the 2017 page (Nilutpal Changkakoti, Kumar Sheelvardhan, Supriya Bhuyan), registrars, deputy registrar.
* Pankaj Kumar Tiwari/Himadri Nayak: Himadri appeared as "Assistant Professor (CSE)" on the 2017 page and "Visiting Faculty" in AR 2019-20's table, but regular BSH (Mathematics) per NIRF (2017-07-19) and all later pages: row BSH, joining 2017.
* Second units: none recorded (no person on two unit pages other than HoD notes).

## Identifier counts
* ORCID: 15, all via the affiliation expanded-search route, each accepted only after `/employments` showed IIIT Bhagalpur and the name matched: Sanjay Kumar, Arvind Choubey, Chetan Barde (org shown without dates), Gaurav Kumar, Sandeep Raj, Om Prakash Singh, Dhrubajyoti Bhattacharya, Hiranmoy Pal, Ujjwal Biswas, Chandan Kumar Jha, Santu Das, Suraj, Rupam Bhattacharyya, Subarna Roy, Subhayu Ghosh. From institute pages: 0.
* Not accepted: Sheelaj Babu, Binay Binod Kumar (JRF 2024-25), Pradeep Kundu, Ravi Prakash (no IIIT-BH employment record or students/non-faculty; none appear on faculty lists). Other hits are students.
* Scholar/DBLP/Scopus/IRINS/homepage: none seen on institute pages (CVs are PDFs; not opened). profile_url left blank: the CV links could not be aligned to people reliably.
* ORCID lookup pending (no per-person search done, per the frugal rule): the remaining 53 rows.
* joining_year filled for 52 of 68 rows.
* Emails: from pages as printed (`[AT]` replaced); director role address not stored for former directors.

## Known gaps
* No faculty-list capture 2018-03-13 to 2019-05-15 (faculty.html); departures in that window unknown. No 2018-19 or 2023-24 annual report read; no NIRF 2018-2025 tables available.
* Department page captures 2020-10 onwards; 2020-03..2020-09 gap (old site to new site).
* Guest/contract faculty churn semester by semester is only visible through the few archive captures of 2025-2026 (about 4 captures per page-year); short-lived guests may be missing.
* Rani Talab campus address/PIN and move date: unverified (see above).
* IIT Guwahati faculty who only taught (mentoring) and appear in no list: none found.

## Operator correction (2026-10-30)
The 17 current "Guest Faculty" rows are set to `adjunct`. These short-contract teaching staff would otherwise bring papers
from their previous and next employers into the likely tier (PROCESS_IIIT §7.3). They still contribute every paper that prints
IIIT Bhagalpur. The designation keeps "Guest Faculty".
