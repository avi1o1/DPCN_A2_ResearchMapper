# IIIT Raichur faculty roster: lab notes (run of 2026-10-30, operator Arihant Tripathy)

Output: `rosters/iiit_raichur_faculty.csv`, 85 rows: 13 current regular faculty, 3 Professors of Practice (adjunct), 11 former regular faculty, 58 visiting (mentor faculty from IIT Hyderabad). Working files: `C:\Users\Arihant\rm_work\iiit_raichur_roster\{data,code}`.

## Institute, campuses and years (verified)
* Indian Institute of Information Technology Raichur (PPP IIIT), Karnataka; mentor institute IIT Hyderabad, "IITH mentored IIIT Raichur from August 2019 to November 2022" (annual report 2022-23); mentor director B. S. Murty. First regular director Harish Kumar Sardana from 1 Dec 2022 (his profile).
* Campuses: (1) IIT Hyderabad campus, Kandi, Sangareddy 502285, Aug 2019 to Aug 2021 (annual reports 2019-20, 2023-24: "started functioning from the IIT Hyderabad campus in August 2019"; the PIN comes from the brief, not from a source I read). (2) Transit campus in Government Engineering College, Yermarus Camp, Raichur (PIN 584135 per brief, not printed in any source I read), "shifted in September 2021" (annual report 2023-24). (3) Permanent campus Wadavatti, Gadwal Road, Raichur 584102 (site contact page); the site now says the institute "runs from its permanent campus"; the move date was not found. Faculty are not split by campus anywhere, so campus does not enter the CSV.
* Faculty pages: `https://iiitr.ac.in/faculty` (one page, filter data-dept = cse / math / practice, data-doj attribute with exact joining dates for 12 of 13 regular faculty), profile pages `/faculty/<slug>`, former-faculty page `/archive/faculty` (live 404 now; Wayback only), `/nirf` (2026 only), `/reports` (annual reports 2019-20 to 2023-24), `/staff` (non-teaching, excluded). No JSON endpoint.

## Sources and URL patterns used
1. Live site (all fetched through polite_get): faculty list and the 16 profile pages, nirf, reports, contact, about, careers, staff, sitemap-style CDX list.
2. NIRF 2026 data submissions (Overall `NIRF-Full Report-20-02-2026.pdf`, Engineering `NIRF-Report-Engineering-2026.pdf`, both on the institute site; faculty table with joining/leaving dates and "currently working" flag). Only 2026 is available: the site's /nirf page has no earlier years, Wayback holds no earlier nirfindia.org PDF for IR-O-U-1089 / IR-E-U-1089 (CDX empty), and nirfindia.org answers 403 to the fetcher (not circumvented). NIRF is a 2026-only source here.
3. Wayback (CDX `iiitr.ac.in/*` 2019-2026, 942 URLs; `/faculty*`, `/faculty.html`, `/archive/faculty*`, `/staff*` captures de-duplicated by digest = 33 snapshots fetched; plus 30 profile and news pages `faculty/<slug>`, `update/2021/0x/.../New-Faculty-*`). Snapshot dates of the faculty list: 2019-06 to 2020-01 (page text only, no names), 2020-07, 2021-10, 2022-01, 2022-08, 2023-01 to 2023-09, 2024-02, 2024-07, 2024-09, 2025-02, 2026-01. `/archive/faculty` ("IIIT Raichur Previous Faculty", with date ranges) 2022-10 to 2026-05.
4. Annual reports 2019-20 to 2023-24 (pdftotext): faculty tables, joining paragraphs (Alka 1 Feb 2021, Biswas 22 Mar 2021, Jallu 8 Jan 2021, Jha 1 Feb 2021), IITH coordination committee, faculty-strength statements.
5. ORCID public API (below).

## Counts per unit
| unit | current | former | adjunct | visiting |
|---|---|---|---|---|
| Computer Science & Engineering | 9 (incl. Director) | 8 | | |
| Mathematics and Computing | 4 | 3 | | |
| Professors of Practice (no unit) | | | 3 | |
| IIT Hyderabad mentor faculty (unit blank) | | | | 58 |
Department naming: the site filter says "Mathematics"; profiles say "Department of Mathematics" (2023-25) and "Department of Mathematics and Computing" (2025 on, B.Tech Mathematics & Computing started with the 2024 batch). Mapped to the current name "Mathematics and Computing". CSE is "Computer Science & Engineering". Sardana (Director) is filed under CSE (site filter). Nobody is in two units.

## Size check against NIRF 2026
NIRF 2026 (submitted ~Feb 2026) lists 15 faculty, 10 "currently working". Site now: 13 regular (Sardana, 12 Assistant Professors). Reconciliation: 10 - Priyanka Singh (NIRF says working, but not on the live list; see below) + Arnav Ghosh (Aug 2025), Mehbub Alam (Sep 2025), Kaushiki Roy (Oct 2025) (all three are on the website, absent from the NIRF table, which is shorter than the website list; joined after the data cut-off or not reported) + Sardana (Director, not in the NIRF faculty table) = 13. NIRF-confirmed current rows: 9 of 13 (Alka, Bharat Soni, Jahnvi Tiwari, Jallu, Natesha, Neha Agarwal, Pradhan, Sain, Gyaneshwar). Annual reports: 8 faculty at 2022-23 end (5 CSE, 3 Maths), 11 by Nov 2023, 20 sanctioned (BoG); we are at 13. No NIRF faculty count from earlier years was retrievable. The 3 Professors of Practice are not in NIRF (adjunct).

## How former faculty and tenure years were established
* Former = in `/archive/faculty` (Wayback captures) and/or dated on archived faculty lists and/or in NIRF 2026 with a leaving date, and not on the live list.
* Years: NIRF 2026 joining/leaving dates where present; else profile text (Debasish Mukherjee: "joined 1 June 2022"); else the institute's own date ranges on `/archive/faculty`.
* Institute's `/archive/faculty` page contains COPY ERRORS that I did not use: Suresh Chavhan "22/03/2021 - 30/11/2021" (copied from Biswas; NIRF 03-10-2022 to 30-09-2024 and archived lists of 2023-01 to 2024-09 contradict it); Kiran Reddy, Nabin Meher, Anup Halder, Chandra Mohan "01/12/2024 - 08/05/2025" (identical for four people; NIRF gives four different spans); Avijit Das "01/07/2022 - 30/03/2023" (identical to Debasish Mukherjee; his own profile says he was a postdoc at IIT Bombay until 9 Oct 2023, so I treat 2023 as his only year; no faculty-list snapshot shows him; evidence is the profile page captured 2023-12-07). Last years are stated as NIRF leaving years (Meher 2025, Halder 2025, Chandra Mohan 2025, Kiran Reddy 2025, Chavhan 2024).
* Archived list pages stayed stale: the 2026-01 page still lists Halder and Chandra Mohan (left 09-12-2025 per NIRF). Not taken as presence beyond 2025.
* Other former: Arnab Kumar Biswas (2021: 22 Mar to 30 Nov 2021), Sadhana Jha (1 Feb 2021 to 22 Jul 2022; on lists 2021-10, 2022-01, 2022-08), Debasish Mukherjee (Jun/Jul 2022 to 30 Mar 2023; on lists 2022-08 to 2023-04, gone by 2023-09).
* Pre-2021: no regular faculty at all; "four permanent faculty recruited" (annual report 2020-21) = Alka, Biswas, Jallu, Jha; "till Nov 2022 only two regular faculty" (2022-23 report) is consistent after Biswas and Jha left.

## Joining years
joining_year filled for 23 rows (13 current regular + 10 of 11 former). Sources: data-doj attribute and profile text on the faculty page (exact dates for all 12 current Assistant Professors), NIRF 2026 (agrees on every date compared; Priodyuti Pradhan NIRF "Priyodyuti" 09-11-2022), Sardana 1 Dec 2022 (profile), annual report 2020-21 (Alka, Biswas, Jallu, Jha), profile text (Debasish 1 Jun 2022). ORCID start years were checked but never needed (no person lacked a dated source) and all agree: Jallu 2021, Gyaneshwar 2023, Priyanka 2023, Natesha 2023, Halder 2024 (to 2025), Debasish 2022-2023, Chavhan 2022-2024, Arnav 2025, Mehbub 2025.
Blank joining_year with first-appearance upper bound recorded in the designation range: Ramesh Chandra Sau (first archived 2025-10 profile page; 2025 is an upper bound; described as "INSPIRE Faculty Fellow", i.e. possibly externally funded; not in NIRF 2026; listed under "Previous Faculty" in the 2026-05 capture without dates; left after 2026-01). Professors of Practice (Anil Jain, Mitalee Agrawal, Raj Singh): no dated source; the site's list has them without dates; recruitment notification 02-2025 for PoP exists (Wayback), so they likely joined 2025-26; blank, no range because current. All 58 visiting rows: blank by design (mentoring, not appointment).

## Ambiguous people and decisions
* Priyanka Singh: NIRF 2026 "currently working: Yes", profile (Dec 2023) and 2026-01 list present, but absent from the live list (Oct 2026) and her live profile is 404. Live list wins -> former (2023-2026), not on `/archive/faculty` (2026-05 capture) either. Uncertain; verify.
* Ramesh Chandra Sau: same, on the 2026-01 list, on the 2026-05 "Previous Faculty" page without dates, absent live -> former (2025-2026).
* Mitalee Agrawal: PRO of IIT Hyderabad Nov 2019 to Mar 2024 and PR officer of IIITR (2022-23 report: "our PRO, Mitalee"); now listed as Professor of Practice -> adjunct (non-faculty PR role before 2025 not counted).
* Harish Kumar Sardana: Director, regular post since 1 Dec 2022 (current, CSE). B. S. Murty (mentor director, IITH employee) -> visiting "Mentor faculty from IIT Hyderabad".
* Mentor faculty (58 visiting): 49 IITH faculty named on the institute's own faculty page as "IIT Hyderabad Faculty" / teaching IIITR (2020-07, 2021-10, 2022-01, 2022-08, 2023-01 to 2023-09 snapshots), plus 9 IITH officers named in the annual reports' coordination committee (Murty, Prem Pal, Raja Banerjee, P. Rajalakshmi, Saptarshi Majumdar, Deepa M, K V L Subramaniam, C Krishna Mohan, Abhinav Kumar). Years: first = earliest annual-report year (2019-20 table => 2019; 2020-21 => 2020; 2021-22 => 2021) or snapshot year; last = last snapshot year (2022 or 2023; page kept listing IITH faculty until at least 2023-09 although mentoring is said to end Nov 2022). Name tokens in the annual reports were matched by distinct surnames, so mentor first years are approximate to +-1; Abhishek Subramanian, Neeraj Kumar fixed to 2023 (ambiguous tokens). Department left blank (IITH department not given consistently). Publications by these people appear under IITH, so they matter little for IIIT Raichur.
* Name forms: site prints "Priodyuti Pradhan"; NIRF "Priyodyuti". "Alka" (site), ORCID "alka chaddha", annual report "Alka Chadha": same person (ORCID record shows IIIT Raichur). Kiran Reddy M = "Mittapalle Kiran Reddy" (profile) = "M Kiran Reddy" (NIRF). Chandra Mohan D (site) = Chandra Mohan Das (NIRF).
* Lookalikes: IIIT Ranchi, UAS Raichur, IIT Hyderabad staff not named in IIITR sources: excluded.
* Lab staff, scientific/technical staff on `/staff`: excluded. No guest lecturers listed.

## Identifiers by route
* ORCID: 11 in total. Route A (affiliation expanded-search "Indian Institute of Information Technology Raichur"/"IIIT Raichur", 14 hits, then `/employments` for the 11 name-matched candidates, all show IIIT Raichur): 9 accepted (Neha Agarwal, Gyaneshwar, Priyanka Singh, Alka, Arnav Ghosh, Halder, Debasish Mukherjee, Chavhan, Jallu). Route B (printed on the institute profile page, and employment confirmed): 2 (Mehbub Alam, Natesha B V; Natesha's record is missing from the affiliation hit list, which is therefore incomplete). 3 hits discarded as students (Harsha, Agrahari, Mishra). No 429.
* Leftover name searches (13 people without ORCID, ~40 API calls): Meher, Pradhan, Sain, Sau, Sardana, Jha, Jahnvi Tiwari (3 hits), Kaushiki Roy (2), Bharat Soni (3 hits) had `/employments` read and none listed IIIT Raichur, so none accepted; Biswas, Kiran Reddy, Chandra Das and Avijit Das have too many namesakes (15 to 172 hits) and were not resolved. ORCID lookup pending: none (no 429).
* Google Scholar: 19 (institute profile pages, incl. archived), homepage: 8, email: 25 (all regular faculty and PoP). DBLP, Scopus, IRINS: none on any institute page (not searched, per brief).

## Problems and notes
* A "taskkill //IM python3.exe" I issued to stop my own stuck ORCID job also killed python3 processes of other agents sharing this machine. If another agent reports an interrupted fetch around 12:58 IST on 2026-10-30, that was me.
* First ORCID leftover search used a wrong field (`family-names`; correct is `family-name`) and produced HTTP 500; rerun fixed.
* Wayback `%0D` suffix in 30 fetch URLs (CRLF in my list file) was tolerated by the archive (200 each).
* Live NIRF PDFs on nirfindia.org 403 (not bypassed).

## Known gaps
* NIRF 2018-2025 faculty tables not retrievable: tenure dates for people who left before 2026 rest on the institute's `/archive/faculty` page (with the copy errors above), archived lists and profile text.
* Faculty-list snapshots exist only from 2020-07 (earlier captures contain only the mentor sentence); no regular faculty before Jan 2021 is known, consistent with the annual reports.
* Priyanka Singh and Sau status, Avijit Das exact tenure, exact mentor years.
* Professors of Practice have no joining dates.
