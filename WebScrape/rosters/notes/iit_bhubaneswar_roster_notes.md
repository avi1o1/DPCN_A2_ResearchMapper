# IIT Bhubaneswar faculty roster - notes (iit_bhubaneswar, window 2016-2026)

Output: `WebScrape/rosters/iit_bhubaneswar_faculty.csv` (312 rows: {'current': 226, 'visiting': 26, 'former': 44, 'adjunct': 15, 'emeritus': 1}).
This run CONTINUED an interrupted run (previous agent lost to a usage limit). Inherited from it: cached Wayback captures of the
institute-wide list (`fm_*.html`, 27 snapshots 2016-03 .. 2023-12), the cached current list (`main_list.json`), the four NIRF Overall
PDFs as text (`ov23..ov26.txt`; Engineering PDFs `eng*.txt` are the same faculty table and were not used separately), and two
parsers. Added in this run: the repaired NIRF parser, entity resolution across all sources, status/tenure rules, identifier
harvest (profile pages + offline ORCID index), CSV and these notes. Parsing code is under the scratchpad
`work/iit_bhubaneswar_roster/code/` (parse_nirf2.py, parse_fm.py, entities.py, build2.py, orcid_match.py, final.py).

## Sources and endpoints
* Current list: `https://www.iitbbs.ac.in/index.php/faculty-members/` (single HTML table; columns name, designation, school, phone,
  e-mail, "View Profile" link to the school sub-site). 230 visible rows + 5 rows commented out in the HTML source.
* School profile pages (`https://<sbs|secs|sif|seocs|shssm|sms|smmme>.iitbbs.ac.in/index.php/<slug>/`): all 232 live links fetched
  through the shared fetcher (2 `old.iitbbs.ac.in` links DEAD, 1 404 `secs.../spdas`); used for Google Scholar, IRINS, DBLP, ORCID links.
* Wayback: `web.archive.org/web/<ts>id_/http://www.iitbbs.ac.in/faculty-members.php` (CDX `cdx_fac.json` for `faculty.php` was empty;
  `faculty-members.php` CDX gave the captures). 27 captures used: 2016-03, 06, 07, 08; 2017-06, 07, 08, 11, 12; 2018-01, 02, 03, 06,
  07, 08, 09, 10; 2019-03, 09, 10, 11; 2020-09; 2021-01, 05; 2022-01, 03, 11; 2023-12. Old-site layout: 2016 = name/school/phone/e-mail
  (no designation), 2017+ = name/designation/school/phone/e-mail. 2017-07/08 captures additionally list ~20 Adjunct/Visiting people.
* NIRF "Faculty Details" tables (name, designation, currently working, joining date, leaving date, association type), Overall data
  submissions: 2023 `documents/nirf/NIRF-IITBBS-Overall_01022023.pdf` (131 rows), 2024 `wp-content/uploads/2024/02/NIRF-Overall-2024-submitted-data.pdf`
  (178), 2025 `wp-content/uploads/2025/02/Overall-2025.pdf` (201), 2026 `wp-content/uploads/2026/04/Overall-Final-after-submission-2026.pdf`
  (238). Row-count check: serial numbers 1..N complete in all four.
* Not used (gaps): per-school archived faculty pages (CDX lists exist for sbs/seocs/smmme but were never fetched), annual reports
  (cached 2020-21, 2022, 2022-23; not mined), IITBBS Express newsletters.

## Problems found and resolved
* Previous parser bug (header filter dropping names starting "Sr"): the saved filter `^\s*Srno` is replaced by `^\s*Srno\s` and the
  parser no longer depends on name text at all; every NIRF table now yields a complete serial sequence (131/178/201/238, no gaps).
  The earlier wrapped-name capture (given names on the next text line, indented 5 spaces) was also fixed: wrapped lines are
  accepted only if indented at the name column (+-2) and without digits, so designation wraps ("Director / Vice Chancellor") are
  not mixed into names.
* NIRF 2023/2024 print names SURNAME-first, 2025/2026 given-name-first, often with truncated / re-wrapped tokens. Identity resolution is
  by normalised token sets with anchored clustering (each of the 230 visible current rows is its own anchor and can never be merged with
  another), then manual merges for 8 spelling/wrap cases: Abhijit Dutta/Datta Banik, Amardeep/Amar Deep Sarkar, Akshaya/Akshay Kumar Ojha,
  MALLICK SUVRADIP = Suvradip Mullick (same join date 2017-07-19), BHENDE C.N., CHANDRAPPA A.K., 'Raja Kumar Ratnam V' (NIRF Director) =
  R. V. Rajakumar (fm), PASUPUREDDI VIJAYA SANKARA RAO = Vijay Shankar Pasupureddi (same e-mail `vijay@`; found by the check script).
  "Akshay K." (ECS) and "Akshay Kumar Ojha" were NOT merged (token matcher had joined them).
* The 2026 NIRF table has no age column: designation parsing is position-independent (regex over the first columns).

## Per-unit counts (rows in CSV)
| unit | current (incl. listed visiting counted separately below) | former | visiting/adjunct/emeritus |
|---|---|---|---|
| (blank, NIRF-only) | 0 | 4 | 1 |
| School of Basic Sciences | 56 | 4 | 7 |
| School of Earth, Ocean and Climate Sciences | 17 | 4 | 13 |
| School of Electrical and Computer Sciences | 53 | 14 | 5 |
| School of Humanities, Social Sciences and Management | 19 | 3 | 7 |
| School of Infrastructure | 34 | 4 | 3 |
| School of Mechanical Sciences | 30 | 5 | 3 |
| School of Minerals, Metallurgical and Materials Engineering | 17 | 6 | 3 |

Unit names: `School of Electrical and Computer Sciences` was `Electrical Sciences` on every archived page up to 2023 (the school page
nav still says "Electrical and Computer Sciences"); `Humanities, Social Sciences & Management` (old) = `... and Management`;
`Minerals, Metallurgical & Materials Engineering` (old) = current `... and Materials Engineering`. All mapped to the current name.
No unit was dissolved in the period; no separate Toshali/Samantapuri campus listing exists on the pages used.
Counts: 'current' = listed on the institute-wide list now; status `visiting` rows with no (range) are currently listed visiting faculty
(7 of the 26 visiting rows).

## Current faculty and the size check
* Institute list: 230 visible rows. Add NIRF-2026-working people that the institute list hides/omits: Akash Ashirbad Panda (commented out in
  HTML, NIRF'26 Regular, currently working, joined 2022-11-03), Ashwini K Nanda (commented out, NIRF'25/'26 Visiting from 2023-03-17, fm 2023-12
  "Professor") and C R Subramanian (NIRF'26 Visiting from 2024-08-22, not on the list) -> 233 current rows (226 regular/current + 7 visiting).
  Conflict rule: institute-wide list wins for who is on it, but a commented-out (invisible) row with a NIRF-2026 "currently working" flag is kept.
* NIRF 2026 (as submitted, data around early 2026) reports 238 faculty rows, of which 235 "currently working": 211 Regular, 8 Visiting,
  16 Adhoc/Contractual; 2 Regular and 1 Adhoc have left. Comparable faculty strength (Regular+Visiting working) = 219.
  Roster current = 233; difference +14 = 14 people on the live list but absent from the NIRF-2026 table
  (joined after the submission: Akash Jaiswal, Arjun S, Arpan Kumar Das, Avijit Gangopadhyay, Avik Sett, Dipjyoti Das, Harish Ranot, Lipak Kumar Sahoo, Ravi Yadav, Roopayan Ghosh, Shubham Choudhary, Sudheer Kumar Kuppili, Sumit Kumar Debnath, Vimalesh Muralidharan) less people NIRF has but the list does not (adhoc/contractual, excluded below).
  216 of the 230 institute-list rows are NIRF-2026-confirmed (name+join match).
* Excluded as non-faculty (NIRF "Adhoc / Contractual", designation "Other"), 22 people: Ashish Kumar Manna; Kajari Chatterjee; Amit Kumar; Bibhuprasad Mahakud; Anu Tomy; Sumit Kumar Jha; Tahir Shamsher; Prakash Chandra Sahu; Sayan Mukherjee; Farheen Anjum; Sabana Azim; Sonam Parween; V S S Venkatesh; Ashutosh Pandey; Brighty Dutta; Pradyumna Kumar Sahoo; Ranu Singh; Archana Kumari Singh; Gopinath Sahoo; Prabhat Singh; Satyajit Sahoo; Budhadev Sahoo.
  Decision: contractual teaching staff, comparable to guest lecturers; NIRF lists them but the institute faculty page does not. Revisit if wanted.
* Excluded for no dated evidence: Kalore Shubham Arun (Asst. Prof., School of Infrastructure) and Shubham Sundeep (Asst. Prof., SECS) are
  commented out on the institute list, absent from every NIRF table and from the 2016-2023 archives -> status/years unknowable; Om Prakash
  Srivastava (listed 2017-07/08 as "Assistant Registrar") is staff.

## Former faculty and tenure years
* Former/visiting/adjunct = in an archived list or NIRF table but not on the list now. FIRST = min(first archived appearance, NIRF
  join year); LAST = NIRF leaving date year where present, else last archived snapshot year, else NIRF year-1 (NIRF'YYYY data are
  submitted early in YYYY and describe the previous year; this applies to e.g. Sujit Roy, last NIRF'25 -> 2024, and the five NIRF'24-only
  people -> 2023). Archived pages are treated as maintained (lists change snapshot to snapshot).
* Overrides: M. Sabarimalai Manikandan stays on the archive through 2022-11 ("Assistant Professor (On Lien)") but NIRF'23 gives leaving
  2021-12-30 -> LAST 2021. Rabindra Kumar Panda: NIRF leaving 2021-06-30 (retired as Professor/HoS), but archive still lists him as Visiting
  Professor to 2022-03 -> LAST 2022, status former. Godabarisha Mishra, Abhijit Sutradhar, Subhajyoti Mukherjee: NIRF leaving 2021.
* Status mapping: designation contains Visiting -> visiting; Adjunct/Honorary/Professorial Fellow -> adjunct (title kept); Emeritus -> emeritus;
  anyone with a regular-rank designation or NIRF Regular record who left -> former (so Ramanujan Fellow / DST-INSPIRE Faculty / MGM Chair Professor
  / Director are `former`). Visiting people who were once regular are `former`.
* People seen only in the 2016-03..2016-08 archives (Asmita Shukla, Kalyani Mohanta, Lalan Kumar, Padmanabhan N.P.H., Sekhar Chandra Dutta,
  Subhasish Tripathy and others) have LAST 2016; the next capture is 2017-06, so the true LAST is uncertain (could be early 2017). Their
  designation is blank on 2016 pages and is written "faculty member (designation not shown on archived page)" unless NIRF gives it.
* Adjunct / visiting people seen on 2017-07..08 captures only get range (2017-2017). Archive gaps: no capture between 2023-12 and the live page,
  and none 2022-03..2022-11 beyond one; people who joined and left within gaps (and left after 2023-12 without being in NIRF'24-'26) are missed.
* Brahma Deo (MGM Chair Professor): the list shows him as current Visiting; NIRF visiting join 2016-01-25 -> joining 2016.

## joining_year (274 of 312 rows filled)
Rule: NIRF earliest joining date (prefer earlier of the Regular/Visiting/Adhoc records; adhoc-then-regularised people keep the earlier date);
if an archived list shows the person at least one snapshot-gap (<=9 months) before the NIRF date (regularisation/rejoin) the archived year is used
(46 rows say 'first archived appearance' - these used the first archive appearance only where the prior capture was <=9 months earlier and lacked
the person, or where NIRF had no date). Persons first seen in the earliest capture (2016-03) with no NIRF date: blank (true joining may be earlier).
Akshay Kumar Ojha: listed since 2016-03 but NIRF gives 2022-10-22 (re-appointment): blank. Tapas Kumar Biswal: Adjunct Faculty 2017-07, NIRF Visiting 2023 -> 2017.
Visiting people: the year is the first listing, not necessarily a joining of a post.

## Identifiers by route
* ORCID: 142 from the offline ORCID affiliation index (employment / invited-position records naming IIT Bhubaneswar, name match
  incl. initials, school compatible) + 1 seen on an institute profile page = 143 total. Live ORCID API: not used (no per-person searches).
  Ambiguous (two qualifying iDs, left blank): Hemant Kumar ['0000-0003-4339-5711', '0009-0006-6434-9713'], Ramu Nair ['0000-0003-0504-7548', '0009-0005-1167-8727'].
  Known weak matches accepted because name + school match and the record shows IIT BBS employment: Madhusmita Dash (record is a postdoc 2021-24; same name),
  Dukhabandhu Sahoo (record dept 'School of HSS & M', start 2010 matches NIRF join 2010).
* Google Scholar 156, IRINS 117, DBLP 2 from the profile pages (only when exactly one distinct id appears on the page); Scopus 0.
  Former faculty rows carry no identifiers except ORCID-index hits.
* e-mail: the iitbbs address (obfuscations like `x[at]iitbbs[dot]ac[dot]in` decoded); personal addresses dropped. Former: from the archived list.
* profile_url for former people are old-site `www.iitbbs.ac.in/profile.php/<slug>/` URLs (dead; kept as printed). source_url lists the live list,
  the profile page, first and last archive snapshot and every NIRF year the person appears in (middle snapshots omitted).

## Ambiguous people and decisions
* Akshay Kumar Ojha: on the live list as 'Visiting Professor'; NIRF'23 Regular (join 2022-10-22), '24 leaving 2022-12-31, '25/'26 Visiting from 2023-04-24; archive lists him
  from 2016. Treated as one person, status visiting (current), joining blank.
* Ashwini K Nanda vs 'Ashwini Kumar': NIRF Visiting from 2023-03-17, designation 'Other'; fm 2023-12 Professor; treated as one person.
* Sujit Roy appears under two profile slugs (sroy, sroychem) - one person. Bankim Chandra Mandal/Mahanta, Arpan Das/Arpan Kumar Das, Satish Kumar Panda/S K Panda,
  Sandeep K K/Sandeep Kumar Samal are distinct current rows (not merged).
* R. V. Rajakumar: Director 2015-04-22..2022-04-22 (NIRF), unit set to the archived school (Electrical) - he is the Director; Professor of that school.
* Second units: none recorded in the sources used.
* Matjaz Kovse appears under two slugs (matjaz.kovse, kovse) - one person.
* Adjunct list of 2017 contains non-academic names (Gokul Chandra Pati IAS, Padmashree Kumkum Mohanty) listed by the institute as Adjunct -> kept as adjunct.

## Known gaps / ORCID lookup pending
* No per-school archive pass and no annual-report mining: people who were on a school page but never on the institute-wide list or in NIRF are missed.
  NIRF 2022 and earlier tables not fetched (not published on the institute site under the URLs found), so 2016-2021 departures rely on the archive only.
* LAST years for departures between the 2023-12 capture and NIRF 2026 depend on NIRF'24-'26 tables only.
* ORCID lookup for former faculty by live API not done (pending); Scopus IDs none.
