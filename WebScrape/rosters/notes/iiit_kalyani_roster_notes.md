# IIIT Kalyani (Indian Institute of Information Technology Kalyani, West Bengal, PPP IIIT) faculty roster: lab notes

Run: 30 Oct 2026, operator Arihant Tripathy (IIIT team). Output: `rosters/iiit_kalyani_faculty.csv` (55 rows).
Working files (not in repo): `C:\Users\Arihant\rm_work\iiit_kalyani_roster\data\`, scripts in `...\code\` (fetch_snaps.py, parse.py, build.py).

## Totals
current 15, former 5, visiting 28, adjunct 7, emeritus 0.

| unit | current | former | visiting | adjunct |
|---|---|---|---|---|
| Computer Science and Engineering (CSE) | 7 | 2 (Sandip Karmakar, Madhumita Sengupta) | 0 | 0 |
| Electronics and Communication Engineering (ECE) | 5 | 2 (Tamal Ghosh, Bapi Kar) | 1 (Bhabatosh Chanda) | 1 (Santanu Chattopadhyay) |
| Physics | 1 | 0 | 0 | 0 |
| Mathematics | 2 | 1 (Devdas Ghosh) | 0 | 0 |
| department blank | 0 | 0 | 27 | 6 |

The 27 blank-unit visiting rows are 13 "attached to teaching" people from other institutes, 13 NIRF-only visiting/adhoc people, and Rabindranath Bera (website gives no unit). The 6 blank-unit adjuncts are the mentor/executive directors other than Santanu Chattopadhyay.
Unit mapping: the current website (`/faculty`) has no department split at all (one list, "Assistant Professor" / "Professors" categories). Units (CSE, ECE, Physics, Mathematics) come from the annual reports 2014-2023 ("Unit: ..." headings, 2021-22 and 2022-23 "current incumbents" lists), archived pages (2018-2019 list pages grouped by department) and profile pages ("Dept :" on Dalia Nandi, Debasish Bera, Oishila, Pratik, Sanjoy, Soumen Pandit). Amit Ranjan Azad, Bapi Kar -> ECE (2022-23 report); Sudeshna Mondal -> Mathematics (2022-23 report); Soumen Pandit -> ECE (profile page "Dept"). No unit was renamed. Rabindranath Bera: no source gives a unit (his area, wireless, suggests ECE; not guessed).

## Campuses (verified)
* One institute, one campus in use throughout 2016-2026: temporary campus at Webel IT Park (Near Buddha Park), Kalyani 741235, Nadia, West Bengal (contact-us page of the live site; annual reports 2014-17 and 2022-23: "Phase-I, WEBEL IT Park, Buddha Park, Kalyani-741235"). Institute began in 2014 (Tenure of first registrar June 2014; first faculty Aug 2014).
* Permanent campus: 34.36 acres granted by the Government of West Bengal (about-us page), "about 50 acres earmarked at Kalyani" with Phase-I 70% (2021-22) and 80% (2022-23) complete; the live site (2026) still says the institute "is presently running from the temporary campus at Webel IT Park". The brief's "permanent campus on the Kalyani Expressway" was NOT confirmed in any source I read (no street address for the permanent campus is given). PIN 741235 is confirmed. No faculty belong to a separate campus; no campus-specific rows were made.

## Sources and endpoints
1. Live site `https://iiitkalyani.ac.in/faculty` (server-rendered; 16 faculty cards incl. mailto, personal-website links, sometimes ORCID/Scholar links). Profile pages `https://iiitkalyani.ac.in/faculty/<slug>` (17 fetched). `/administrative-body` (Director, Registrar). `/contact-us`, `/about-us`. `/staff` (technical/office staff; no faculty). Old site `https://old.iiitkalyani.ac.in/newfacultypages/faculty1.php` and `/php/administration.php` (same 16 names, still names Santanu Chattopadhyay as Director). The new-site NIRF page `/nirf` returns a 404 body; NIRF PDFs were found through the home page and CDX.
2. NIRF data submissions: only two exist online. NIRF 2025 (`.../api/serve/2026/01/06/NIRF-kalyani_1767682982_17eb0300.pdf`, file named 20250110-nirf, byte-identical to `.../2026/02/13/INDIAN_INSTITUTE_...20250110-nirf_...pdf`; 21 rows) and NIRF 2026 (`.../2026/04/16/nirf-new_1776317254_1314439f.pdf`, byte-identical to `..._1776317264_f429544f.pdf`; 26 rows). Parsed from `pdftotext -raw` (the `-layout` output scrambles wrapped rows). No NIRF 2018-2024 PDFs exist on the site or in the archive (CDX filter nirf/annual/ranking on the host returned only these).
3. Annual reports (live `api/serve/2025/09/09/` copies): 2014-2017, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22, 2022-23. Each has "Details of Faculty Members" with exact tenure dates ("Tenure: 01.07.2016 - till date" / end date), the "current incumbents" list per unit, administrative heads with tenures, committee lists, and per-semester guest-faculty tables. The 2023-24 and later reports are not online.
4. Internet Archive (CDX `url=...&output=json&filter=statuscode:200&collapse=timestamp:6`, raw `.../web/<ts>id_/<url>`), faculty-list URL patterns of each site generation (all fetched, one capture per month where CDX had one, 108 captures; membership diffed over time):
   * 2017-06 to 2018-04: `iiitkalyani.ac.in:80/faculty/` (5 captures)
   * 2018-05 to 2020-05: `/html/faculty.html` (20 captures; regular faculty by department plus "Other faculty members attached to teaching")
   * 2019-03 to 2020-02: `/php/faculty.php` (12)
   * 2019-04 to 2020-08: `/newfacultypages/faculty.php` (regular faculty only, 16)
   * 2020-12 to 2026-01: `/newfacultypages/faculty1.php` (20; the 2024-05 and 2025-09 captures were unparseable/empty and were ignored)
   * 2026: `/faculty` and `/faculty/<slug>` profile captures (parsed live instead)
   * `/php/staff.php` (4 captures 2019-2025) and `/administrative-body` (2026-02, 2026-05, 2026-08) for staff and Director checks.
5. ORCID public API (see below). IRINS, Scopus, OpenAlex, Google Scholar scraping were not used.

## Per-unit extraction counts against NIRF (current)
Website 16 cards = CSE 7 + ECE 5 (Dalia Nandi, Rinky Sha, Pratik Chakraborty, Amit Ranjan Azad, Soumen Pandit) + Physics 1 + Mathematics 2 + Rabindranath Bera (visiting, unit not stated). Current rows = 15 (Bera is `visiting`).
NIRF 2026 regular/adhoc table: 16 people (13 regular, Sudeshna Mondal and Soumen Pandit adhoc, R. Bera adhoc) = the 16 website cards, a name-for-name match. NIRF-confirmed current rows: 15 of 15.

## How current / former and years were set
* current = on the live faculty page (and NIRF 2026 "currently working: Yes", regular or adhoc). Tie-break: institute list wins; no conflicts for current people.
* joining_year (all from dated documents):
  * Annual report "Tenure" dates (2014-17 through 2022-23 reports): Uma Das 22.06.2016, Imon Mukherjee 01.07.2016, SK Hafizul Islam 01.07.2016, Sandip Karmakar 08.07.2016, Devdas Ghosh 05.07.2016, Tamal Ghosh 05.09.2017, Dalia Nandi 21.09.2017, Sanjoy Pratihar 22.09.2017, Oishila 13.10.2017, Sanjay Chatterji 02.11.2017, Anirban Lakshman 06.06.2018 (the 2019-20 report prints 21.06.2018; both 2018), Debasish Bera 22.06.2018, Bhaskar Biswas 01.08.2018, Rinky Sha 26.12.2020, Pratik Chakraborty 01.04.2021, Madhumita Sengupta 04.08.2015, Bhabatosh Chanda 04.02.2022.
  * NIRF joining dates: Amit Ranjan Azad 31-05-2022, Sudeshna Mondal 02-01-2023, Bapi Kar 02-01-2023, Soumen Pandit 04-07-2024, Rabindranath Bera 15-07-2024, and every NIRF-only person (all NIRF dates here are contract-start dates; "Currently working" flags and leaving dates from NIRF 2025). All other NIRF 2025/2026 dates agree with the annual reports to the day, which supports using them.
  * Mentor/executive directors: start of the post per the "Administrative Heads" tables (Ajoy Kumar Ray Aug 2014, P. P. Chakrabarti Feb 2017, Anupam Basu Feb 2017, S. K. Bhattacharyya Jul 2019, V. K. Tewari Jan 2020, Santanu Chattopadhyay Executive Director Feb 2020, Director 16 Dec 2020). Joining year is the post start, not a regular faculty appointment (mentoring posts of employees of other institutes).
  * Left blank (upper bound only): Suman Chakraborty (first appears on the live/archived administrative-body page in the 2026-08 capture; the 2026-05 capture still shows Santanu as Director), and the 13 "attached to teaching" visitors (first archived list 2017-06; earlier guest-faculty-table years noted below).
* Website profile pages print "Joined in <year>" for some people, but the values are unreliable (Bhaskar Biswas 2025, Debasish Bera 2025, Imon 2025, Sanjoy 2025, Sudeshna 2025, R. Bera 2025 are clearly not joining years; Dalia Nandi "2016" disagrees with the annual report 21.09.2017). Not used; the annual-report dates win.
* Former ranges (FIRST-LAST):
  * Sandip Karmakar 2016-2018: tenure 08.07.2016 - October 2018 (2018-19 report); last archive capture with him 2018-12-03 (stale by then, he is gone by 2019-01). CSE.
  * Tamal Ghosh 2017-2019: tenure 05.09.2017 - July 2019 (2019-20 report); the `faculty.php` page kept listing him until the 2020-06 capture (stale; 2020-07 capture drops him). ECE.
  * Devdas Ghosh 2016-2016: tenure 05.07.2016 - 06.10.2016 (2014-17 report). Mathematics.
  * Madhumita Sengupta 2015-2016: faculty tenure 04.08.2015 - 13.10.2016 (CSE, 2014-17 report); from October 2016 she is Assistant Registrar (administration), still so in 2026: not faculty after Oct 2016. She is the only former row with FIRST before 2016 (overlaps the window in 2016).
  * Bapi Kar 2023-2024: NIRF 2025 joining 02-01-2023, leaving 04-12-2024, Adhoc/Contractual; first archived on faculty1.php 2023-05, gone by 2025-05. ECE (2022-23 report).
  * Bhabatosh Chanda (visiting, ISI-type visiting professor, ECE): NIRF 2025 04-02-2022 to 31-01-2024; archived 2022-02 to 2023-12. Status `visiting`, range (2022-2024).
  * Mousumi Dutt (CSE, tenure 01.08.2014 - 27.07.2015) was excluded: evidenced only before 2016-01-01.
* Last-year caution: archived `faculty.php`/`html/faculty.html` pages go stale (Tamal Ghosh, and the "attached to teaching" list which has no capture after 2020-05). Annual-report tenure dates were preferred.

## Adjunct / mentor-director decisions
Post-holders employed by another institute are `adjunct` (per run instructions): Santanu Chattopadhyay (Professor, IIT Kharagpur; Executive Director Feb 2020, Director 16 Dec 2020; on the faculty list as "Professor and Director" from 2021-06; last captured Director 2026-05; the live page no longer lists him), Suman Chakraborty (Director, IIT Kharagpur; now named as Director on the administrative-body page; not on the faculty list), Anupam Basu (Executive Director Feb 2017 - Jan 2020, Director NIT Durgapur), Partha Pratim Chakrabarti (Mentor Director Feb 2017 - Jun 2019, IIT Kharagpur), Ajoy Kumar Ray (Mentor Director Aug 2014 - Feb 2017, IIEST Shibpur), Sriman Kumar Bhattacharyya (Mentor Director (Offg.) Jul - Dec 2019, IIT Kharagpur), Virendra Kumar Tewari (Mentor Director Jan - Dec 2020, IIT Kharagpur; the 2019-20 report says "since January 2020"). The Chairman of the Board of Governors (Manoj Kohli, industry) and registrars are not faculty.
Open point: Suman Chakraborty's start date is unknown (a 2026-06 PDF "Additional Charge of Chairperson" is on the home page; not read). Santanu's end is unknown, between 2026-05 and 2026-08; range printed (2020-2026).

## Visiting people and NIRF-only people
* Listed on the institute's own faculty page 2017-2020 under "Other Faculty members attached to teaching": Goutam Biswas (Retd. IIT Kharagpur), Chirantan Neogy, Shubhomoy Das, B. Chakraborty, P. Bhattacharya, Krishnendu Bhoumik, Samaresh Pal, Niladri Chatterjee (all Kalyani University), Asit Kumar Das (IIEST Shibpur), A. Faruk Mollah (Aliah University), Pranab Roy ("Assistant Professor (Contractual) at School of VLSI", IIEST Shibpur), T. K. Bandopadhyay (Retd. Principal, Bandel Survey Institute), Mallika Banerjee (Retd. Calcutta University). Treated as `visiting` because the institute lists them on its faculty page; they are mentor-institute and neighbouring-university teachers, not appointments. FIRST = first archived list (2017) or, for Neogy, Shubhomoy Das, Krishnendu Bhoumik, Pranab Roy, Samaresh Pal, the 2016 guest-faculty table of the 2014-17 report (2016 is the first in-window evidence; Neogy, Bhoumik and Samaresh Pal also appear in 2014-15 tables). LAST = 2020 is a lower bound (no list capture after 2020-05; several names recur in guest tables until 2021 or later). joining_year left blank. The guest-faculty tables of the annual reports (about 10-25 names per semester from JIS College of Engineering, Kalyani University, Kalyani Government Engineering College, IISER Kolkata and others) were NOT added: guest lecturers are excluded unless the institute lists them as faculty.
* NIRF 2026 "Visiting" (Association type) people, currently working Yes: Debasish Dutta (04-01-2021), Furquan Uddin, Poulomi Khasnobis, Jayanta Ghosh, Siddhartha Bhattacharyya, Deepsubhra Guha Ray, Rasheed K, Sunita Roy, Soumen Khatua, Shweta Basu. Furquan Uddin conflict: NIRF 2025 says Adhoc/Contractual, left 31-12-2023; NIRF 2026 says Visiting, joined 17-07-2023, still working (rejoined or listed continuously); recorded as visiting (2023-2026). Debasish Dutta and Aruna Chakraborty appear in NIRF 2025 as Adhoc/Contractual from 04-01-2021 (Dutta moves to "Visiting" in 2026; Aruna is not in the 2026 table, so her LAST=2025 is a lower bound). Maahirii Bose (03-07-2023) and Soumyadeb Hui (17-07-2023 to 31-12-2023) appear only in NIRF 2025. These people are NIRF-only (no website card); department blank; they are probably guest or ad hoc teachers listed in the NIRF faculty table.
* Rabindranath Bera: website card "Prof. Dr. Rabindranath Bera (Visiting Professor)", NIRF 2026 "Professor, Adhoc/Contractual, 15-07-2024, 12 months". Kept `visiting` ("Visiting Professor (2024-2026)") because the institute itself calls him Visiting Professor; first archived 2024-08 (`faculty1.php`), the earlier 2024-08 title was without the label (changes to "(Visiting Professor)" in 2024-11).

## Identifiers
* ORCID: 11 rows. Route 1, institute website: 1 (Anirban Lakshman, link on the faculty card/profile). Route 2, ORCID public API: 10, all name-matched with an IIIT Kalyani employment record: one expanded-search `affiliation-org-name:"Indian Institute of Information Technology Kalyani" OR "IIIT Kalyani" OR "Indian Institute of Information Technology, Kalyani"` (88 hits, mostly students) followed by `/employments` for the 10 name-matched people: Uma Das, SK Hafizul Islam, Dalia Nandi, Oishila Bandyopadhyay, Rinky Sha, Pratik Chakraborty, Amit Ranjan Azad, plus Jayanta Ghosh (Visiting Professor 2023-), Poulomi Khasnobis (Guest Lecturer 2023, matches the NIRF visiting row), Bapi Kar (Assistant Professor on contract 2023-2024, found by a leftover search). Total API calls: 1 search + 10 employment checks + 16 leftover per-person searches (Imon Mukherjee, Sanjoy Pratihar, Sanjay Chatterji, Debasish Bera, Bhaskar Biswas, Sudeshna Mondal, Soumen Pandit, Santanu Chattopadhyay, Rabindranath Bera, Bhabatosh Chanda, Bapi Kar, Sandip Karmakar, Tamal Ghosh, Siddhartha Bhattacharyya, Debasish Dutta, Madhumita Sengupta) + 1 employment check; no 429. The per-person searches found one hit besides Bapi Kar: a "Bhaskar Biswas" ORCID with Kalyani Mahavidyalaya / University of Kalyani employment (0009-0005-9901-0480), rejected (different institution). Rows with no ORCID: not found with an IIIT Kalyani employment.
* google_scholar: 2 (Oishila Bandyopadhyay, Rabindranath Bera), both links on the institute's own faculty card. homepage: 7 (Uma Das, Imon Mukherjee, Hafizul Islam, Sanjoy Pratihar, Rinky Sha, Amit Ranjan Azad, Soumen Pandit; Bera has a Scholar link only), from the faculty page's "Personal Website" link. dblp, scopus_id, irins: none seen on institute pages (0).
* email: all 16 current/visiting website cards (institute domain).
* The ORCID of Anirban Lakshman is on the institute page and also employment-confirmed (2018 start) by the API (not counted twice).
* Pending ORCID lookup: none (no 429).

## Independent size check
Current-faculty count: 15 rows `current` + 1 `visiting` website card (Bera) = 16 cards on the live page. NIRF 2026 (submitted early 2026) reports 16 Regular/Adhoc faculty plus 10 visiting (26 rows): the 16 match name for name. The institute's annual reports give "strength" of 7 CSE + 5 ECE + 1 + 1 (2021-22) and 7 CSE + 6 ECE (incl. Chanda, Santanu) + 1 + 2 (2022-23): consistent with 16 by 2026 after adding Soumen Pandit and Bera and removing the Director and the visiting professor. No unexplained difference.

## Problems and decisions
* Pages of the old (`/html/`, `/php/`) site list "Other faculty ... attached to teaching" with `-->` junk between rows; parsed by text. The `newfacultypages/faculty.php` variant lists only regular faculty, so list-differences between the two archived pages (11 vs 24 names) were not membership changes.
* The live site has no department structure; unit names came from reports (see above).
* NIRF `-layout` output misaligned wrapped rows (joining dates drifted by several rows); `-raw` gave consistent rows and was cross-checked against annual-report dates (all 12 overlapping dates agree).
* Wayback was slow (shared 3 s slot); the faculty-list captures were fetched in one queue (108 files).
* Name spelling: "Dalia Nandi (Das)" on old pages, "Dalia Nandi" on the live site (one person). "Amit Ranjan Azad" in NIRF without title, "Dr Oishila Bandyopadhyay" wrapped over two lines, "Soumen Pandit" absent from NIRF 2025 (joined 04-07-2024, probably after submission).

## Known gaps
* No NIRF 2018-2024 tables and no annual reports after 2022-23: contract/adhoc/visiting faculty of 2019-2022 and 2023-24 (other than those in NIRF 2025/2026) are probably missing (e.g. possible ad hoc assistant professors in Physics/Mathematics/Humanities before 2023; the 2021-22 report counts only regular posts). Humanities/management are taught by guest faculty and are not in the roster.
* Guest lecturers appear only in annual-report tables and were excluded; recall of "teachers of the institute" who are not on a faculty page is therefore limited.
* LAST years of the 13 "attached to teaching" visitors (2020) and Aruna Chakraborty (2025) are lower bounds.
* Santanu Chattopadhyay end year, Suman Chakraborty start year unknown.
* Unit of Rabindranath Bera and of all NIRF-only visitors unknown.
* "Kalyani Expressway" permanent-campus address unverified.
