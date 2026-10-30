# IIIT Kottayam faculty roster: lab notebook

Operator: Arihant Tripathy (IIIT team). Run date 2026-10-30. Output: `rosters/iiit_kottayam_faculty.csv` (206 rows).
Working data: `C:\Users\Arihant\rm_work\iiit_kottayam_roster\data\`, code in `...\code\` (people.py, people2.py, build_csv.py, make_notes.py).

## 1. Result in numbers

Status: current 117, adjunct 36, visiting 7, former 46, emeritus 0 (no emeritus is listed anywhere).
joining_year filled for 112 of 206 rows. ORCID filled for 67 rows (routes in section 7).

Per unit (department = Annual Report 2023-24 "Faculty Profile", which groups faculty by department; the institute's own faculty page and the NIRF tables give NO department):

| Unit | current | adjunct | visiting | former | total |
|---|---|---|---|---|---|
| (department not published) | 55 | 34 | 7 | 34 | 130 |
| Computational Science and Humanities | 11 | 0 | 0 | 0 | 11 |
| Computer Science and Engineering | 29 | 2 | 0 | 10 | 41 |
| Cyber Security | 12 | 0 | 0 | 1 | 13 |
| Electronics and Communication Engineering | 10 | 0 | 0 | 1 | 11 |
| **All** | 117 | 36 | 7 | 46 | 206 |

The "(department not published)" rows are people who joined after the 2023-24 report (2024-26 joiners), pre-2023 leavers that no source assigns to a unit, all adjunct/visiting people and the lab faculty. No department was guessed.
Departments of the institute today (from `dept_head.ctrl.js`/`admin.ctrl.js` HOD list): Electronics & Communication Engineering (HOD Ananth A), Computer Science & Engineering-1 (HOD Christina Terese Joseph) and CSE-2 (HOD Rubell Marion Lincy G), CSE-Cyber Security (HOD Arun Cyril Jose), Computational Science & Humanities (HOD Dhanyamol M V). The 2023-24 report treats CSE-1/CSE-2 as one department "Computer Science"; the roster uses "Computer Science and Engineering" for both. "Cyber Security" = CSE-Cyber Security. "Computational Science and Humanities" = "Computational Sciences and Humanities" of the report. "Electronics and Communication Engineering" = "Electronics and Communications".
One row per person; no person is placed in two units by any source (second units: none recorded). Mathew C D teaches Management Studies (AR 2021-22 adjunct, now CS&H).

## 2. Institute facts verified (campuses, mentors)

* Name/status: Indian Institute of Information Technology Kottayam (PPP IIIT; IIIT PPP Act 2017). Look-alikes NOT used: IIITM-K/Digital University Kerala, IIIT Kalyani/Kurnool/Kota, MG University (RIT Kottayam appears only as a previous employer of Renu Jose).
* 2015 to Dec 2016: temporary campus at Amal Jyothi College of Engineering, Koovappally P.O., Kanjirappally, Kottayam 686518 (AR 2015-16; Wayback contacts.jsp 2016-06). Classes began 11 Aug 2015. Mentor institute: NIT Calicut (Director NIT Calicut = Mentor Director).
* MHRD letter of 30 Nov 2016 (AR 2016-17; AR 2018-19 misprints it as 2017) moved the temporary campus to IISER Thiruvananthapuram and the mentor director to the Director of IISER TVM; classes at the transit campus (floors 4-5 of GIFT, Gulati Institute of Finance and Taxation, Thiruvananthapuram) started 9 Jan 2017. Communication address 2017-18: C/o IISER Thiruvananthapuram Transit campus, Computer Science Building, CET, Engineering College (P.O.), Trivandrum 695016 (Wayback Administration.jsp 2017-02, contact 2018-11). Registered office throughout: Building no. 340, Karoor, Valavoor P.O., Kottayam 686635.
* Permanent campus: Valavoor, Karoor Panchayath, Pala, Kottayam 686635. AR 2018-19 says the activities moved there "from first January 2019"; first convocation at Valavoor 27 Aug 2019 (AR 2019-20). Wayback pages of 2018 still show the Trivandrum address. An off-campus centre in Trivandrum runs the M.Tech for working professionals from Jan 2020 (not a faculty campus).
* Mentor/administration people: V. Ramakrishnan (Director IISER TVM, Mentor Director 2016-2019, last seen in the AR 2018-19) and M. P. Rajan (Dean Academics, from IISER TVM, 2017-2020) are post-holders employed elsewhere: status `adjunct`. Prasad Krishna (Director NIT Calicut, additional charge Director IIIT Kottayam, on the current administration page and AR 2024-25) and Ashok S (adjunct professor, former NIT Calicut professor, Professor In-charge/Dean Academic Affairs) likewise `adjunct`. Rajiv V. Dharaskar was the full Director (AR 2019-20 to AR 2024-25, "sent off" in 2025): `former`. Mentor faculty who only taught (Gopakumar G of NIT Calicut; Sivaranjana Reddy, Bikas C. Das, P. Devaraj of IISER TVM) are `visiting` with "Mentor faculty from ..." as the brief says (the institute's page calls them "Adjunct faculty from NIT Calicut / IISER,TVM"; I followed the brief's rule for pure teaching).
* Staff, not faculty, and excluded: Registrar M. Radhakrishnan (appears in NIRF as type "Other"), interim Registrar Gymmy Joseph Kattoor (2016-17), physical instructors (Rathish T, Dr. Abhilash), Junior Superintendent etc.

## 3. Sources and endpoints

1. `https://iiitkottayam.ac.in/` is an AngularJS single-page app (hash-bang routes). `#!faculty` is rendered from `https://iiitkottayam.ac.in/scripts/controllers/faculty.ctrl.js` (a JS array, 176 entries; extracted with node `eval` of the array, `code/ext.js`) and `views/faculty.html`. The entries carry designation (Assistant/Associate Professor, Adjunct Professor/Faculty, Lab Faculty, Former Faculty), contact e-mail (obfuscated "x at iiitkottayam dot ac.in"), additional charges, and a profile route. Plain `/faculty` returns 404 (SPA); the real data endpoints are the controller files found through `scripts/app.js` (route table: 120 `/faculty/<slug>` routes -> `views/faculty/<file>.html`, fetched all 120: 118 x 200, `sudhakar` and `anoop` 404).
2. Other controllers: `dept_head.ctrl.js` (HODs), `admin.ctrl.js` (Director/Registrar/Deans), `views/nirf_home.html` (NIRF PDFs 2025 and 2026 only), `views/institute.html` (annual report links).
3. NIRF: `https://iiitkottayam.ac.in/data/pdf/IIITK_nirf2025_{overall,engineering}.pdf` and `..._nirf2026_{overall,engineering}.pdf` (IR-E-U-0802 / IR-O-U-0802); the "Faculty Details" table has joining date, leaving date, currently-working flag and association type. Parsed with pdftotext -layout plus regex (`code/nirf2.py`). Earlier NIRF years (2021-2024) on nirfindia.org answer 403 to the polite fetcher (not bypassed) and have no Wayback copy (CDX returned nothing for IR-E-U-0802.pdf 2020-2024).
4. Annual reports (all linked from `views/institute.html`): 2015-16, 2016-17 (file Finalrev1.pdf), 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2023-24, 2024-25 are text PDFs; 2022-23 is a scanned image PDF (no OCR available here) and was NOT read. Faculty tables: 2016-17 (names/posts), 2017-18, 2018-19, 2019-20 (as on 31 Mar 2020), 2020-21 (31 Mar 2021), 2021-22 (31 Mar 2022); 2023-24 "Faculty Profile" grouped by department; 2024-25 profiles (29 people, no department).
5. Wayback (CDX `from=2016&to=2026&filter=statuscode:200&collapse=timestamp:6`, raw `.../web/<ts>id_/<url>`): old PHP/JSP site `www.iiitkottayam.ac.in/faculty.jsp` (6 snapshots 2016-07..2017-06), `faculty.php` (14 snapshots 2017-06..2018-10), `oldwebsite/faculty.php` (3 copies of the Oct-2018 page, 2018-11..2019-04, not used as evidence because it is a frozen copy), `administration.php`, `dean.php`, `Administration.jsp`, `contacts.jsp`, `contact.php`, `pcampus.php`; and the Angular-era `scripts/controllers/faculty.ctrl.js` (6 captures: 2022-08, 2022-11, 2023-08, 2024-02, 2025-07 twice). No Wayback copy of `views/faculty.html`/ctrl exists for 2019-2021, and none of the 120 profile pages is archived. `newlyjoined.php` (2018) is an announcement page without names. Density: every available snapshot of those pages was fetched (<= 14 per page, far below the cap).
6. ORCID public API (identifiers only): `expanded-search/?q=affiliation-org-name:"Indian Institute of Information Technology Kottayam"&rows=200` (111 hits) plus one variant query `"IIIT Kottayam"` (17 hits, 13 new): 124 candidates; 72 name-matched candidates checked with `/employments` and 10 more candidates (unmatched names that could be faculty) inspected; 84 ORCID calls in total, no 429.
7. Identifiers (ORCID, Google Scholar, dblp, Scopus, IRINS) found as hyperlinks inside the institute profile pages (30 of 120 pages carry at least one).

## 4. How the roster and the years were built

* Current list: the 176 entries of faculty.ctrl.js (175 distinct people; Anitha Ambat is listed twice, as Assistant Professor and as Lab Faculty). Entries by designation: Assistant/Associate Professor 87 (86+1), Adjunct Professor/Faculty 24, Lab Faculty 30 (29 other persons plus Anitha's second entry), Former Faculty 35.
* Lab Faculty: the site lists 30 "Lab Faculty" entries (29 persons besides Anitha Ambat; NIRF 2026 counts 31 "Lecturer" rows including her and Vidya Sagar, all M.Tech holders). The brief says staff listed as faculty by the institute count, so they are included (status `current`, designation "Lab Faculty (NIRF: Lecturer)"). They are filterable by that designation; they hold no PhD and rarely publish, so downstream users may drop them. NIRF-only lecturers not on the site: Vidya Sagar (current, 2020), Chinju John (2020-2024) and Sreelakshmi R (2023-2024; both absent from NIRF 2026).
* Extras found in Annual Reports/Wayback but absent from the current faculty page: Renu Jose, Vineeth, Hiran V. Nath, Chitra M T, Thejaswini M, C. Rajan, Athira U, Anoop Jacob Thomas, Shyju Wilson, Ranjit Thomas Abraham, Gopakumar G, V. J. Sebastian, Sivaranjana Reddy, Bikas C. Das, P. Devaraj, Guram Donadze, Viji Z. Thomas, Riyaz A., Sony C. George, Jose Dominic Joseph, Harilal Madhavan, Jobin Kanjirakkattu, Haseena, Remya Mohan, Lekshmi T.J., P. Mohanan, Prasad Krishna, Sudhakar M S.
* Matching of names across sources: token sets with spelling aliases (Bakkiyaraj/Bakkyaraj, Jayakrishna/Jayakrushna, Benefia/Benifa, Renjith/Ranjith ...) and initials tolerance; every unmatched name was printed and handled manually (`code/people.py`).
* FIRST/LAST in `designation`: earliest/latest year with dated evidence of presence: Wayback faculty pages (capture year), annual-report lists (reports "as on 31 March YYYY" count as YYYY only; reports "2016-17/2017-18/2018-19" count for both calendar years), `faculty.ctrl.js` snapshots where the person is NOT marked "Former Faculty" (the page demonstrably is maintained: it lists newer joiners), NIRF joining and leaving dates, NIRF "currently working" in the 2025 table counted as 2024 and in the 2026 table as 2025 (submission years), and AR 2015-16 (the three faculty named at the start of classes in Aug 2015). Archived listings as "Former Faculty" are not counted as presence.
* For the following former people the evidence is thin: only the year of the first archived snapshot that lists them as "Former Faculty" is available; their designation carries (Y-Y) with Y = that year and the real tenure lies at or before Y and unknown: Avinash Kumar Mittal, Kalka Dubey, Priyambada Subudhi, Resmi Ramachandran Pillai, Sunil Kumar Kashyap (all first listed as former in the 2022-08 snapshot, i.e. tenure unknown, <= 2022), T Sugirtha (first seen 2023-08), Sweeti Sah (2023-08 present as Assistant Professor, former 2024-02), Konjengbam Anand, Oswald C, Suresh Chavhan (present as AP 2022-08; the profile pages of Oswald and Chavhan say they were at VIT until Feb 2021 / Jun 2022, so they joined IIITK after that), Nilotpal Chakraborty (present 2022-11 and 2023-08), G. Narendra Kumar Reddy (present 2022-11). For Samson Anosh Babu P, Riby Abraham Boby, Sudhakar M S and Akarsh K Nair the only dates are self-declared ORCID employments (2021, 2022, 2019, 2024-2025), used for the range only and flagged below. LAST is uncertain (could be later) for everybody whose last non-former snapshot is 2022 or 2023: the next archive snapshot already marks them former.
* Table of every non-current person (first-last used, basis, first year of any dated list/report appearance = upper bound for joining):

| Person | status | range | basis | first dated list appearance (upper bound for joining) |
|---|---|---|---|---|
| Bikas C. Das | adjunct | 2016-2018 | dated evidence | 2017 |
| Gopakumar G | adjunct | 2015-2018 | dated evidence | 2015 |
| Haseena | adjunct | 2022-2022 | dated evidence | 2022 |
| Lekshmi T.J | adjunct | 2022-2022 | dated evidence | 2022 |
| M. P. Rajan | adjunct | 2016-2020 | dated evidence | 2017 |
| P. Devaraj | adjunct | 2017-2018 | dated evidence | 2017 |
| P. Mohanan | adjunct | 2022-2024 | dated evidence | 2022 |
| Remya Mohan | adjunct | 2022-2022 | dated evidence | 2022 |
| V. J. Sebastian | adjunct | 2016-2017 | dated evidence | 2016 |
| V. Ramakrishnan | adjunct | 2016-2019 | dated evidence | 2017 |
| Vennapusa Sivaranjana Reddy | adjunct | 2016-2018 | dated evidence | 2017 |
| Akarsh K Nair | former | 2024-2025 | ORCID self-declared employment dates (no dated institute source) |  |
| Anoop B N | former | 2022-2022 | dated evidence | 2022 |
| Anoop Jacob Thomas | former | 2020-2020 | dated evidence | 2020 |
| Athira U | former | 2018-2018 | dated evidence | 2018 |
| Avinash Kumar Mittal | former | 2022-2022 | first archived listing as former (20220823); tenure unknown |  |
| Bhanu Chander | former | 2022-2025 | dated evidence | 2022 |
| Bibin Francis | former | 2022-2022 | dated evidence | 2022 |
| Bini A. A. | former | 2017-2022 | dated evidence | 2017 |
| Boddepalli SanthiBhushan | former | 2021-2021 | dated evidence | 2021 |
| C. Rajan | former | 2017-2018 | dated evidence | 2017 |
| Chinju John | former | 2020-2024 | dated evidence |  |
| Chitra M T | former | 2016-2018 | dated evidence | 2017 |
| Gaanutula Damodar Reddy | former | 2020-2020 | dated evidence | 2020 |
| Gangireddy Narendra Kumar Reddy | former | 2022-2022 | dated evidence | 2022 |
| Govindan V K | former | 2015-2017 | dated evidence | 2015 |
| Hiran V. Nath | former | 2016-2017 | dated evidence | 2017 |
| Jaise Jose | former | 2017-2019 | dated evidence | 2018 |
| Jobish John | former | 2020-2020 | dated evidence | 2020 |
| Kalka Dubey | former | 2022-2022 | first archived listing as former (20220823); tenure unknown |  |
| Keshab Nath | former | 2021-2024 | dated evidence | 2021 |
| Konjengbam Anand | former | 2022-2022 | dated evidence | 2022 |
| Lekshmi B.G | former | 2022-2022 | dated evidence | 2022 |
| Maisagalla Gopal | former | 2023-2024 | dated evidence | 2024 |
| Manikandan V. M. | former | 2018-2019 | dated evidence | 2018 |
| Mirza Ghalib | former | 2022-2024 | dated evidence | 2022 |
| N. Annamalai | former | 2020-2021 | dated evidence | 2020 |
| Nilotpal Chakraborty | former | 2022-2023 | dated evidence | 2022 |
| Oswald C | former | 2022-2022 | dated evidence | 2022 |
| Priyambada Subudhi | former | 2022-2022 | first archived listing as former (20220823); tenure unknown |  |
| Rajiv V. Dharaskar | former | 2019-2025 | dated evidence | 2019 |
| Ranjit Thomas Abraham | former | 2018-2019 | dated evidence | 2018 |
| Ravi Ajmeera | former | 2023-2024 | dated evidence | 2024 |
| Renjith P. | former | 2017-2019 | dated evidence | 2017 |
| Renu Jose | former | 2015-2017 | dated evidence | 2015 |
| Resmi Ramachandran Pillai | former | 2022-2022 | first archived listing as former (20220823); tenure unknown |  |
| Riby Abraham Boby | former | 2022-2022 | dated evidence | 2022 |
| Samson Anosh Babu P | former | 2021-2021 | ORCID self-declared employment dates (no dated institute source) |  |
| Shyju Wilson | former | 2021-2021 | dated evidence | 2021 |
| Sreelakshmi R | former | 2023-2024 | dated evidence |  |
| Sudhakar M S | former | 2019-2019 | ORCID self-declared employment dates (no dated institute source) |  |
| Sunil Kumar Kashyap | former | 2022-2022 | first archived listing as former (20220823); tenure unknown |  |
| Suresh Chavhan | former | 2022-2022 | dated evidence | 2022 |
| Sweeti Sah | former | 2023-2023 | dated evidence | 2023 |
| T Sugirtha | former | 2023-2023 | first archived listing as former (20230810); tenure unknown |  |
| Thejaswini M | former | 2016-2018 | dated evidence | 2017 |
| Vineeth | former | 2016-2017 | dated evidence | 2017 |
| Guram Donadze | visiting | 2017-2018 | dated evidence | 2017 |
| Harilal Madhavan | visiting | 2018-2019 | dated evidence | 2019 |
| Jobin Kanjirakkattu | visiting | 2018-2019 | dated evidence | 2019 |
| Jose Dominic Joseph | visiting | 2016-2017 | dated evidence | 2017 |
| Riyaz A. | visiting | 2016-2017 | dated evidence | 2017 |
| Sony C. George | visiting | 2016-2017 | dated evidence | 2017 |
| Viji Z. Thomas | visiting | 2017-2018 | dated evidence | 2017 |

* joining_year: set only from (a) NIRF joining date when no earlier dated appearance exists, (b) explicit text: AR 2015-16 (Govindan V K, Renu Jose: classes began Aug 2015 with them), profile CV lines (Reetha Thomas 07/2025, Jaisooraj J April 2026, Cinu C Kiliroor Jun 2022, Manu Madhavan Jul 2022, Asha Sebastian Mar 2024, Bakkyaraj T Dec 2017; all agree with or extend NIRF). Self-declared ORCID dates were never used for joining_year. NIRF dates conflicting with an earlier dated appearance are read as regularisation/rejoining and the column is left blank: A Balu (15-11-2023 vs earlier evidence 2022), Gayathri G.R. (15-11-2023 vs earlier evidence 2022), Suriyapriya K (18-01-2024 vs earlier evidence 2023), Riyasudheen T K (18-01-2024 vs earlier evidence 2023), Keshab Nath (07-06-2022 vs earlier evidence 2021). Keshab Nath: NIRF 2022-06-07 vs AR 2020-21 "Adjunct faculty" (2021) -> blank; ORCID says 2021.
* Current people with blank joining_year and no NIRF date (joined after the NIRF 2026 data of ~Nov 2025; first appearance in an archived list is the upper bound in brackets; "only on the current page" = absent from the 2025-07 Wayback snapshot): R Tharaniya Sairaj (2025), Anu Maria Sebastian (2025), Anandhu Mohan (2025), Rosebell Paul (2025), Nayana P G (2025), Gayathri Varma (only on the current page), Jisha Mariyam John (only on the current page), Syamala S (only on the current page), Alkha Mohan (only on the current page), Kumaresan G (only on the current page), Mirothali Chand C (only on the current page), Sridhar Raj S (only on the current page), A V Prajeesh (only on the current page), Nisha J S (only on the current page).
* Adjunct people with no dated joining (first appearance year in an archived list/report): JALAJA M J (2023), Leena Mary (2023), Sujamol S (2023), Angel Thomas (2025), Raghunadhan T (2022), Mathew Joseph (n/a), Sajimon Abraham (n/a), Alexander G (2023), Sherin V. George (2022), Sasikumaran Sreedharan (2017), S. Vinaya Kumar (2017), Antony Palackal (2017), D Narayana (2017), Oommen K Mathew (2021), Augustine Joseph (2021), Shabu B Raj (2018), M.K. Mathew (2020), Lissy George (2020), N.K Narayanan (2017), Sarika Lohana (2022), Karthik A (2021), Sadanand Sadashiv Gokhale (2022), Beena Gokhale (2022), V. Ramakrishnan (2017), M. P. Rajan (2017). Many adjuncts first appear only in the 2022-08 snapshot because no earlier Angular-era capture exists; their real start may be earlier.
* Designation text for current people is the site designation (Assistant Professor/Associate Professor); Prof/Dr titles stripped. Adjunct professors Jalaja M J and Leena Mary are listed as Professor in NIRF 2026 (joined 2023): kept `adjunct` (site list wins). Angel Thomas (site: Adjunct Faculty, NIRF 2026: Assistant Professor since 2022-05) and Sujamol S (site now: Adjunct Faculty; NIRF Assistant Professor 2023-07..2024-06; AR 2023-24 lists her in CS) kept `adjunct` per the site list. Raghunadhan T (NIRF Professor, joined 2019) likewise.

## 5. Size check

* NIRF 2026 table: 105 currently-working rows were matched to roster people, plus the Registrar (type "Other", staff, excluded) = 106 "Yes" rows in total (108 rows, 2 left: Maisagalla Gopal 2024, Bhanu Chander 2025). NIRF 2025 table: 85 "Yes" of 89.
* Roster current (status `current`) = 117: of these 101 are NIRF-2026-confirmed (71 regular incl. one lecturer + 30 lab/lecturers); 16 regular faculty have no NIRF row because they joined after that submission (see list above; 6 of them already appear in the 2025-07 website snapshot). In addition NIRF counts 4 people we classify as `adjunct` (Jalaja M J, Leena Mary, Raghunadhan T, Angel Thomas). So NIRF 105 teaching rows (106 minus the Registrar) = 101 + 4 -> reconciles exactly. Institute-reported strength in the annual reports: AR 2019-20 Director's message says the faculty strength "has increased from 12 to 25" while its 31 Mar 2020 table has 18 rows (15 assistant professors + 3 adjuncts); AR 2020-21 table 25 rows (20 + 5 adjuncts); AR 2021-22 table 36 rows (31 + 5 adjuncts). No faculty-strength figure other than the NIRF tables is published for 2025/2026.
* Counts of current rows per source: faculty page (non-former, non-adjunct, non-lab) 87; NIRF-confirmed 71.

## 6. Conflicts, ambiguities and decisions

* Institute-wide list vs department page: the site has no department pages, nothing to reconcile. Annual report 2023-24 department grouping vs HOD list: no conflict.
* Anitha Ambat listed twice (Assistant Professor and Lab Faculty): one row, designation shows Lab Faculty (NIRF Lecturer).
* "Shri. Vineeth" (AR 2016-17, adhoc CSE) vs Dr. Vineeth Palliyembil (current ECE, NIRF joined 2023-12): treated as different people (not merged, identity unverified). Hiran V. Nath: AR 2016-17 layout text vs plain text disagree whether he is "on deputation"; kept as adhoc CSE.
* Ranjit Thomas Abraham (Wayback 2018, "Assistant Professor (Adhoc faculty)") and "Dr. Renjith Thomas Abhram, Computer Science" (AR 2018-19 visiting list): taken as the same person. "Renjith P" (adhoc, 2017-2019) is a different person.
* "Prof. Vijayakumar / Vinayakumar, NISH TVM" (AR 2016-17/2017-18) merged with S. Vinaya Kumar (adjunct, Wayback 2017-08 on): likely but not certain.
* Dr. Sudhakar M.S.: route `/faculty/sudhakar` in app.js (profile 404), not listed anywhere; ORCID 0000-0003-4243-9006 self-declares IIITK Assistant Professor 2019. Included as former (2019-2019), flagged weak. `anoop` route = Anoop Jacob Thomas (AR 2019-20), profile 404.
* Govindan V K: retired NIT Calicut professor appointed "Professor (on contract)" at IIITK (AR 2015-16/2016-17): regular former.
* Visiting people from the annual-report visiting lists are included only with the dated report as source (honour-roll rule). Physical-instructor trainers excluded.
* Dharaskar and Ramakrishnan dates: Dharaskar first evidence AR 2019-20 (Director message, convocation 27 Aug 2019); the exact start of his tenure is not documented in the files read.
* Bakkyaraj T: site list "Dr. Bakkyaraj T", Wayback "Bakkiyaraj Thankarasu", route title "Bakkyaraj Thangarasu" (merged). Manjith B.C. = route "Manjjith B.C".
* NIRF names truncated by line wraps (Chakradhar, Sivaiah, Kanchan Lata, Milind Thomas ...) were completed from the site list; "Mirza Galib Anwarul" = Mirza Ghalib.

## 7. Identifiers by route

* ORCID: 67 rows. Route 1, institute profile page link: 9 (4 of them are also confirmed by the API affiliation, 5 are not: Koppala Guravaiah, Chakradhar Padamutham, Jeena Thomas, Mahima Mary Mathews, Sridhar Raj S). Route 2, ORCID API (affiliation search, name match, `/employments` shows IIIT Kottayam): 58.
* Lower-confidence API acceptances (name matches and the record shows IIITK employment, but the declared role differs from the roster designation): Amrita Kumari, Helena Thomas (Research Scholar), Annette James (Senior Research Fellow 2024-27), Nayana P G (Visiting Scholar 2024; now Assistant Professor). Name-matched but ORCID shows no IIITK employment (left blank): Thomsy William, Jane George, Jeena Thomas (the institute page ORCID is used), Raghunadhan T, Bikas C. Das, Sweety Kunjachan, Elizabeth Antony, Annie Sonia, Sreelakshmi R, Remya R, Anandhu Mohan.
* ORCID candidates not matched to any roster person and not added (scholars/staff or unclear): e.g. Basil Sunny (researcher 2018-2024, co-author with faculty), Sumith A T (Junior Superintendent), Tom Kurian, Naeema Nazar, Unnikrishnan K N (research scholars), and ~25 other names (students/scholars). "John" (0000-0002-6850-9079) is ambiguous (Jobish John / John Paul Martin / Chinju John): not assigned.
* Several qualifying iDs for one person: none found.
* Google Scholar 27, dblp 2, Scopus 5, IRINS 1 (Venkatesh S: iiitkottayam.irins.org/profile/594870), homepage 3, e-mail 116; all from the institute profile/faculty pages. Google Scholar URLs are normalised to `citations?user=<id>`.
* ORCID lookup pending: none (no 429).

## 8. Problems met

* Plain `/faculty` 404: the site is a hash-bang SPA; solved by reading `scripts/app.js` and the controller JS.
* Windows: `python -I` ignores PYTHONUTF8, stdout reconfigured in scripts; CRLF in loop input caused two failed batches (re-run, bodies were already cached).
* NIRF PDF text is a mix of wrapped columns: rows parsed by regex, names re-matched manually (see section 6); parsing completeness checked against the roster (all 105 teaching rows of NIRF 2026 are matched).
* nirfindia.org returned 403 (not bypassed); Wayback has no copy; the institute's own NIRF PDFs only exist for 2025 and 2026.
* Annual report 2022-23 is image-only; Wayback has no 2019-2021 capture of the faculty page, so tenures between Mar 2019 and Mar 2022 rely on the three "as on 31 March" report tables.

## 9. Known gaps

* No department for 130 rows (see section 1). No faculty-by-year table between 2019 and 2022-08 other than the annual-report tables, and none for 2022-09..2024-02 other than three site snapshots and AR 2023-24: people who joined and left between snapshots could be missing (suspected for 2019-2021 contract faculty).
* Tenure unknown for ~12 former people (section 4). LAST year uncertain for those first marked former in 2022-08/2023-08/2024-02.
* AR 2022-23 not read (scanned). Adjunct/visiting persons from the earlier part of the window who were never listed on the faculty page or in the reports are not captured.
* 16 current rows have no NIRF confirmation (joined after the NIRF 2026 submission).

## Operator correction (2026-10-30)
The "Lab Faculty" rows, which NIRF counts as lecturers, are set from `current` to `adjunct`. They are teaching staff, and their
person channels would add namesake papers to the likely tier. As adjunct they contribute only papers that print IIIT Kottayam.
The designation keeps "Lab Faculty", so they can be restored.
