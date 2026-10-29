# IIIT Allahabad faculty roster (2016-2026): lab notebook

Built 2026-10-27 by Arihant Tripathy (IIIT team) with Claude. Output: `WebScrape/rosters/iiit_allahabad_faculty.csv` (121 rows). All fetches went through
`polite_get.py`. Downloads and parsing scripts are in `C:/Users/Arihant/rm_work/iiit_allahabad_roster/{data,code}` (not in the repo).

## Totals

| status | rows | joining_year filled |
|---|---|---|
| current | 87 | 80 |
| former | 20 | 10 |
| visiting | 9 | 9 |
| adjunct | 5 | 5 (R. S. Verma 2022, Krishna Misra 2003, Dinesh/Subraya/Artus 2018, all NIRF) |
| **total** | **121** | **104** |

Per department (current / former / other): Applied Science 20 / 2 / 1 adjunct; Electronics and Communication Engineering 20 / 5 / 1 visiting;
Information Technology 34 / 10 / 3 adjunct; Management Studies 12 / 0 / 0; no unit recorded 1 current (Director) / 3 former / 8 visiting / 1 adjunct.
Unit names: the site says "Department of Applied Science" (older pages and annual reports: "Applied Sciences"); the roster uses "Applied Science". Single campus (Devghat, Jhalwa, Prayagraj 211015),
no centre has its own faculty (CCC, CIR, Rekhi Centre, CCEOP are headed by department faculty; heads of centres on the Key Administrative Officials page are all already in the roster).

Identifiers: ORCID 45 (4 from institute profile pages, 41 from the ORCID API route), Google Scholar 11, IRINS 6, Scopus 1, DBLP 1, homepage 40, e-mail 75.
Only identifiers printed in the institute profile header (Personal Website field and header links) were taken; the IRINS links are the ones the institute itself prints.
The DBLP value (Mohammed Javed) is a `dblp.org/pers/hd/...` page, not a `/pid/` URL, kept as printed. LinkedIn-only "personal websites" (Randheer Bagi) were left out.

## Sources and endpoints

1. **Live institute site** (Drupal, `www.iiita.ac.in`): faculty directory `/faculty?page=0..2` (75 cards, 25 per page; `page=3` empty): name, designation, unit, e-mail (some obfuscated as `[at]`, `()`, which I decoded);
   75 profile pages `/<slug>` (Personal Website, Scholar/ORCID/IRINS links; no joining dates); department pages `/department-<x>/faculty` (ECE 19, IT 25 on page 1, AS 16, MBA 12);
   `/deans`, `/heads-department`, `/key-administrative-officials`, `/directors-profile-message`, `/dean-FA`; `as.iiita.ac.in/index.php/faculty/` (AS legacy site, still live).
   `it.iiita.ac.in`, `ece.iiita.ac.in`, `mba.iiita.ac.in` no longer resolve (fetcher: DEAD); the archive was used.
2. **NIRF data submissions** (the institute's NIRF page `/nirf-rankings` itself only lists ranks; the PDFs were found with a CDX query `url=iiita.ac.in&matchType=domain&filter=original:.*nirf.*` and read from Wayback):
   2019, 2020, 2021, 2022, 2023, 2024, 2025 and 2026 (Engineering; 2026 Management also read). Faculty tables with joining/leaving date, "currently working", association type (Regular / Visiting / Other / Adhoc).
   `pdftotext -raw`, records split on the title token (Prof/Dr) because page breaks scramble the layout. Rows parsed: 69, 72, 79, 86, 79, 81, 80, 90 (2019-2026), equal to the number of table rows in each PDF.
   The 2018 NIRF PDF (`NIRF Ranking 2018`) was truncated in the archive (1 MiB, damaged xref) and could not be read. `nirfindia.org` returned 403 (bot wall), not bypassed.
3. **Annual reports** (`/annual-reports-`): 2015-16 and 2018-19 are text PDFs (faculty profile sections: name, department, designation, which gave presence in 2015 and 2018); 2023-24 is text (department faculty lists with "Date of Joining" for 79 faculty, which gave joining dates and the faculty strength);
   2016-17, 2017-18, 2019-20, 2020-21 and 2024-25 are scanned image PDFs without a text layer (no OCR available, not used); 2021-22 and 2022-23 are not posted.
4. **Wayback Machine** (CDX `web.archive.org/cdx/search/cdx?url=<page>&output=json&from=2016&to=2026&filter=statuscode:200&collapse=timestamp:6`, snapshots `/web/<ts>id_/<url>`):
   * `iiita.ac.in/academics/faculty_profile/` (6 captures Mar-Aug 2016): the only institute-wide list before 2021 (75 names by unit, with roles).
   * `www.iiita.ac.in/people/faculty/` (legacy institute-wide list, 30 captures 2021-09 to 2026-05, 73 to 81 names by unit, includes "Adjunct Professor" entries). It adds new joiners but never removes anyone and stops adding after 2024-11 (the 2025-12 and 2026-05 captures equal 2024-11), so it is not evidence of presence.
   * `it.iiita.ac.in/?pg=faculty` (38 captures 2017-03 to 2026-07; 11 read): maintained in both directions (it drops Jagpreet Singh in 2022, Kokila in 2023, Rahul Kala in 2024 and adds 2026 joiners).
   * `mba.iiita.ac.in/?pg=faculty` (2017-2023), `ece.iiita.ac.in/faculty.php` (2021) and `ece.iiita.ac.in/rfaculty.php` (retired faculty, 2020-21), `as.iiita.ac.in/index.php/faculty/` (2019-2026, 9 read).
   * `iiita.ac.in/people/former_director/` (2022-05 capture) and `institute/message_from_director/` (2022-05) for the Directors.
   * No ECE faculty list exists in the archive for 2017-2020 and no institute-wide list for 2017-2020 (bridged by NIRF 2019/2020 and the 2018-19 annual report).
5. **ORCID public API**: one expanded-search `q=affiliation-org-name:"Indian Institute of Information Technology, Allahabad"` (656 records, 4 pages of 200), then `/employments` for 50 name-matched candidates + 1 (Sutaone). No 429 received. Accepted only when the record shows employment at IIIT Allahabad and the name matches.
   Rejected: Kokila Jagadeesh (record shows IIIT Tiruchirappalli / NIT Trichy), Apurva Shukla (other employer), "Amit Kumar" (very common name, the only IIITA record has no dates and cannot be tied to the faculty member), Manish Kumar, Saurabh Mishra and Hemant Kumar (two qualifying iDs each, left blank), Sonal Agarwal (the only hit is Sonali Agarwal's iD), Shivam Dubey, Bharat Singh, Rekha Verma for R. S. Verma.
   ORCID lookup pending: none (no quota stop).

## How current / former / tenure years were decided

* **current** = on the live faculty directory, or on a live institute page in Oct 2026 (department faculty page, Deans list, Key Administrative Officials page), or listed as "currently working" in NIRF 2026 together with a maintained department page (IT page 2026-07, AS site) and AR 2023-24.
  The institute-wide directory is not complete: it lacks 12 people who are demonstrably on the faculty (see conflicts), so the tie-break "institute-wide list wins" could only be applied to people who are on it.
* **former / visiting / adjunct no longer listed**: last dated source in 2016-2026 (archived list, NIRF leaving date, annual report). `(FIRST-LAST)`: first and last year with evidence; FIRST uses the joining year when a dated source gives it (NIRF/AR) and the annual-report fiscal-year start otherwise.
  NIRF year N counts as presence in year N. Archived department pages count as evidence only where the page is demonstrably maintained (IT page, 2016 list, MBA 2017).
* **joining_year** = earliest year among NIRF 2019-2026 joining dates and AR 2023-24 "Date of Joining" (current/visiting/adjunct), explicit dated statements for the rest (NIRF leaving/joining pairs, Former Director page for Biswas and Nagabhushan).
  Disagreements between sources, earliest taken: Ranjana Vyas 2013 (NIRF 2019/2022-26) vs 2014 (NIRF 2020); Madhvendra Misra 2004 (NIRF 2019 14-07-2004) vs 2005 (NIRF 2020+/AR); Vijay Kumar Chaurasiya 2004 (NIRF 2019) vs 2005; Sitangshu Bhattacharya 2014 vs 2015 (NIRF 2019 12-11-2015); Rajat Kumar Singh 2007 (AR 01-07-2007) vs 2008 (NIRF 03-05-2008). Blank for the seven 2025-26 joiners.
  Not guessed: Sudip Sanyal, Ratna Sanyal, Amrita Chaturvedi, Rishi Ranjan Singh, Seema Awasthi, B. R. Singh, Somak Bhattacharyya, Rajesh Kumar, Satyavani Guttula, Ayon Ganguly (no dated joining source).
* NIRF-confirmed current rows: 80 of 87 (the 79 matched by name plus the Director Sutaone, printed "Mukul Sharad Sutaone" in NIRF). The 7 unconfirmed are the 2026 joiners absent from the NIRF 2026 data: Kirtan Gopal Panda, Lokendra Kumar Tiwari, Nikhilanand Arya, Priyanka Kamboj, K. R. Kaza, Amit Kumar, Jayasree Sengupta. Ranjana Vyas is among the 80 (NIRF row with designation "Other", association Adhoc/Contractual).

## Independent size check

NIRF 2026 (Engineering, submitted Jan 2026) lists 90 table rows, of which 78 are regular faculty of professor rank currently working (14 Professors, 16 Associate Professors, 48 Assistant Professors). The 2023-24 annual report prints exactly the same split
("Faculty in position": 14 / 16 / 48; the report headline says 78 faculty in position). My roster has 87 current rows = 78 (NIRF 2026) + 7 later joiners on the directory (Panda, L. K. Tiwari, Arya, Kamboj, Kaza, Amit Kumar, Sengupta)
+ Ranjana Vyas (adhoc/contractual, "Other" rank in NIRF) + the Director (Sutaone, NIRF row "Dean/Principal/Director"). The two sources agreeing on 14/16/48 despite the 2-year gap is suspicious (NIRF 2026 may have re-used the older table), so the
agreement is only a weak independent check; the 78 regular rows were matched to roster persons one by one (78 matched, 0 unmatched). The other NIRF 2026 rows are excluded or placed elsewhere:
Registrar (Karyakarte, excluded as non-faculty), Lecturers/Visiting (6, kept as `visiting`), Gaurav Sharma and Artus Krohn-Grimberghe ("Other"), Nagabhushan (former Director).

## Conflicts and ambiguous people (decision)

* **Directory vs other institute pages.** The 75-card `/faculty` directory omits 12 people present on other live pages or NIRF 2026: Anupam Agrawal and Pavan Chakraborty (live Deans page), Ranjit Singh (live MBA department page), Amit Prabhakar and B. S. Sanjeev
  (Key Administrative Officials page, AS site), Gora Chand Nandi, Om Prakash Vyas, Uma Shanker Tiwary (IT page 2026-07, NIRF 2026), Abdullah Bin Abu Baker, Seema Kushwaha, Surya Prakash (NIRF 2026, AR 2023-24, AS site), Director Sutaone (Director's message page). All treated as current.
  Risk: Nandi, Vyas, Tiwary and the three AS/ECE names rest on NIRF 2026 plus a department page that may not be maintained; a retirement or move since January 2026 would not be visible. Flagged, not downgraded.
* **Neetesh Purohit**: on the directory and ECE page "On Lien, Director SGSITS Indore". He is regular IIITA faculty (joined 2006, NIRF/AR), on lien elsewhere, so `current` (the additional-charge rule concerns people holding a post here while regular faculty elsewhere).
* **R. S. Verma**: Director (Acting) 02-04-2022 to 04-04-2023 (NIRF 2023/2024, institute page "Director (Acting)"). Recorded as `adjunct (2022-2023)` by the operator's additional-charge rule; no fetched source states his home institute, so the rule's premise is assumed (see Brief issues).
* **P. Nagabhushan**: Director May 2017-April 2022 (Former Director page). NIRF 2026 has one extra row "Professor, association Other, joined 03-04-2022, currently working" that appears in no NIRF 2023-2025, nowhere on the site and not in AR 2023-24; treated as carried over, so `former (2017-2022)`. If that row is real he would be an adjunct/emeritus current member.
* **Gaurav Sharma** (NIRF 2019-2022 and 2026 "Visiting"/"Other", absent 2023-2025) and **Artus Krohn-Grimberghe** (adjunct on legacy page 2021-2025, NIRF 2019-2022 and 2026): NIRF only, kept as current visiting / adjunct. Their departments and the institutions of Sharma are not given.
* **Ranjana Vyas**: directory lists "Assistant Professor"; NIRF 2019-2026 says adhoc/contractual since 2013. Kept `current`, designation as the site prints it.
* **Lecturers** (Sonal Agarwal, Narugopal Mondal): not faculty ranks but NIRF's faculty table lists them, so kept as `visiting` with the designation.
* **Retired-faculty honour roll**: ECE `rfaculty.php` lists B. R. Singh and M. Radhakrishna as retired professors without dates. B. R. Singh has dated evidence (2016 list, AR 2015-16) and is included (2015-2016, retirement year unknown); M. Radhakrishna has no dated source in 2016-2026 and is excluded.
* **Krishna Misra**: Honorary Professor (AR 2015-16), NIRF 2021 and 2022 association Other, absent 2023: `adjunct (2015-2022)`; the AS legacy pages still list her but they do not remove people.
* **Directors**: Somenath Biswas (May 2014-July 2016) `former (2014-2016)`; G C Nandi was Director (Offg) 2014 and 2016-17 and is a regular professor; Mukul Sutaone (Director from 5 Apr 2023) is `current`, department blank.
* **Name forms**: "Sudip Sanyal" (2016 list prints "Prof. S. Sanyal", IT 2017 page "Sanyal, Prof. Sudip"), "Kokila Jagadeesh" (NIRF "Kokila J"), "Rahul H. Meshram" (ECE page "Rahul Meshram"), "Subraya MS" and "M.S. Dinesh" as printed on the legacy page. IIITA e-mail of K. R. Kaza on the profile is "krkaza()iiita()ac()in"; AR/IT pages use "Kesav Ram Kaza".

## Known gaps

* 2017-2018 (and mid-2016 to 2018 for ECE and AS): no institute-wide list, no ECE or AS department list in the archive, annual reports 2016-17 and 2017-18 are image-only. Faculty who joined and left inside 2016-2018 (other than those in NIRF 2019, which carries Dhar and Arun Kant Singh) may be missing.
* AR 2019-20, 2020-21, 2024-25 are image-only (no OCR), so retirements in 2024-25 are not checked; NIRF 2026 and the IT page 2026-07 are the latest evidence.
* LAST year of Sudip Sanyal, Ratna Sanyal, Amrita Chaturvedi, Rishi Ranjan Singh, B. R. Singh, Seema Awasthi, Rajesh Kumar, Somak Bhattacharyya, Satyavani Guttula, Ayon Ganguly is the last archived sighting, not a leaving date. Several are single-source (2016 list only: Rajesh Kumar, Guttula, Ganguly).
* Department blank for NIRF-only people (Hemant Kumar, Sudharsan Parthasarathy, Mahapatra, Gaurav Sharma, visiting/lecturers, directors).
* 2022-23 and 2021-22 annual reports are not posted, so NIRF is the only dated source for 2021-2023 leavers.
* E-mail only from the directory and the MBA page; none for former or NIRF-only people.
