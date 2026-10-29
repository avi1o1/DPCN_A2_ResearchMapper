# IIT Kanpur roster notes (iit_kanpur)

Built 2026-10-27/28 by two agents (the first was cut off by a usage limit; the second audited and repaired its output). Scripts and caches: scratchpad `work/iit_kanpur_roster/code/` (build2.py, finalize.py, orcid_off.py, lib.py) and `.../data/`.

## Sources and endpoints
* Institute-wide faculty directory `https://www.iitk.ac.in/iitk-faculty` (305 cards: name, designation, unit, profile URL). It wins over department pages for "current".
* Department / school pages (`iitk.ac.in/<dept>/faculty`, `/people`, `former_faculty` for ME, HSS, KSS; KSS adjunct and distinguished-visitor pages), parsed in `page_people*.json`.
* NIRF overall data submissions 2021-2026 (`https://www.iitk.ac.in/data/nirf/nirf-<year>/...pdf`; faculty tables with join/leave dates and "currently working" flag). NIRF 2023-2026 text/TSV parsed; 2021-2022 used for earlier leavers. Primary source for former faculty and tenure years.
* Wayback CDX (`web.archive.org/cdx/search/cdx?url=iitk.ac.in/<dept>/...&collapse=timestamp:6`, 147 department faculty-list snapshots 2016-2021 fetched) for dated former faculty pages (`former_dated.json`, 6 added rows) and wb-only people.
* Offline ORCID index `iit_kanpur_orcid_index.tsv` (no live ORCID API calls).

## Counts (858 rows)
current 607, former 127, visiting 94, adjunct 23, emeritus 7. joining_year on 798 rows (NIRF join date, or card/page; blank otherwise, never guessed). Per unit (current / former / other):
Aerospace 34/9/2; BSBE 27/0/5; Chemical 28/1/2; Chemistry 38/1/0; Civil 46/1/0; Cognitive Sci 6/0/2; CSE 37/9/3; Design 13/0/5; Earth Sci 18/1/1; Economic Sci 29/0/3; EE 53/11/7; Gangwal School 0/0/11; HSS 29/2/1; Intelligent Systems 4/0/2; Kotak School 6/0/5; Management 26/3/6; MSE 27/6/3; Materials Science Programme 1/0/0; Math & Stat 42/9/7; ME 46/7/2; Physics 49/10/5; SPASE 10/1/8; Statistics & Data Science 11/0/0; Sustainable Energy 5/0/4; Wadhwani School 0/0/3; department blank (NIRF-only, no source gives unit) 22/56/37.
Unit names are the current ones on the live site; no renames were mapped beyond Departement/Department typos. People in a second unit (e.g. Indranil Saha: CSE + Intelligent Systems joint appointment) carry only the primary unit.

## Former faculty and tenure years
* Former = present in an earlier NIRF table (2021-2026) with a leave date or "currently working = No", or on a dated Wayback list / institute former-faculty page and absent now. Range = (join year or first evidence) - (leave year, else last NIRF year - 1). NIRF join dates may be regularisation dates; the earliest NIRF join date is used. People evidenced only before 2016 are excluded. Wayback list snapshots only reach 2021, so former faculty who left 2016-2020 and are not in NIRF 2021+ may be missing (known gap); former faculty whose NIRF leave date is blank have LAST = last NIRF year minus 1 (uncertain by up to a year).
* NIRF "Adhoc / Contractual" records are mapped to `visiting` ("ad hoc / contractual per NIRF"); Professors of practice / honorary / adjunct designations -> `adjunct`; Emeritus Fellow -> `emeritus` (these three groups listed on the live pages carry no range).

## Size check
NIRF 2026 table: 636 records, 615 "currently working" (593 regular + 22 ad hoc/contractual), 21 not current. Our roster: 607 current + ad hoc as visiting/adjunct, 583 current rows carry a NIRF source; 237 are on the live directory. The live directory (305 cards) is smaller than NIRF because it lists only profiled faculty; the remaining current people come from NIRF and department pages. Consistent with NIRF within about 1-2 percent. Note IIT Kanpur's genuine faculty strength is about 600 in NIRF; the large figure is the NIRF count, not an over-scrape.

## Identifiers
ORCID 382 rows, all from the offline index (employment/qualification record naming IIT Kanpur, name and unit/years compatible); 0 from live API, 0 institute-page ORCIDs. Google Scholar/DBLP/Scopus/IRINS/homepage/email: 0 (not on the pages used). 12 name-matched cases with several qualifying iDs left blank (A. K. Gupta, A. V. Ravishankar Sarma, Rakesh Kumar, N. Gupta, B V Rathish Kumar, Rakesh Kumar Majhi, Satyadev Nandakumar, Sandeep Kumar Shukla; Vivek Verma and S. N. Singh resolved by the record's department/year, see below). ORCID lookup pending: none attempted via the API; people without index hits stay blank.

## Problems found and fixed in this pass
* Name bug: the first build matched NIRF records to page names where initials substituted for full tokens, so e.g. NIRF "Kumar Sanjay" was printed as "R. S. Ashwin Kumar" and "Virkeshwar Kumar" as "B V Rathish Kumar" (4 and 3 rows). Fixed with `compat_strict` (needs two full-token matches); 0 rows now have a name incompatible with its NIRF names.
* 18 duplicate-name warnings resolved; now 4 remain, all different people:
  Merged (same person re-listed): K. Srihari (join 1996, same date in NIRF 2021-26; typos Keshavarmurthy/Keshavamurth; dept Chemistry from ORCID index, ORCID 0000-0002-4424-6745, a "qualifications" record with Professor 1996); Sharika K. M. (visiting from 2019-12, regular from 2021-06; joining 2019); Manpreet Singh (ad hoc 2024, regular 2025-12; joining 2024); Sudhanshu Shekhar Singh (NIRF "Sudhanshu Shekhar" truncated, join 2015-12 vs 2016-08; earlier kept); J. S. Yadav (2019 visiting, 2022 re-contract; one visiting row).
  Different people, renamed/re-unit: S. N. Singh (Sri Niwas Singh, EE, 2002, ORCID 0000-0002-2451-5303) vs Namrata Singh (Chemistry, 2024, ORCID 0000-0002-8471-2245); Indranil Saha Dalal (ChE, 2014) vs Indranil Saha (CSE, profile card, 2015); Kumar Alok (adjunct, Economic Sciences, 2024) vs Alok Kumar Maloo (Mathematics, Professor, 1998, card); Shivam Tripathi 2010 (Civil) vs 2023 (MSE per ORCID index, ORCID 0000-0003-4084-9773); Vivek Verma 2009 (MSE, 0000-0003-4701-3397) vs 2025 (Sustainable Energy Engineering, 0000-0002-4890-2826); R. S. Ashwin Kumar / Rakesh Kumar vs Rakesh Kumar Majhi.
  Kept as two rows (different join dates, one still current): Abhishek (AE, Professor 2011, current; second record joined 2018-12, left 2025-08, unit not independently confirmed); Rakesh Kumar (AE, 2012 current vs 1988-2023 former; two NIRF records with different join dates); Shivam Tripathi; Vivek Verma.
* Avinash Kumar Agarwal: department was the deputation text; set to Mechanical Engineering, designation keeps "Currently on Deputation as Director, IIT Jodhpur". Dhirendra S. Katti (BSBE) is on deputation as Director IIT Goa; remains current.
* Truncated NIRF names kept as printed where no fuller name was found (e.g. "Sri Sivakuma", Materials Science Programme).

## Known gaps
* Wayback 2016-2020 coverage of former faculty is thin (NIRF starts 2021); former faculty leaving before 2021 may be missing, LAST years approximate.
* 22 current and 93 non-current rows have a blank department (NIRF-only people).
* Some NIRF-only rows may still be split/merged wrongly where NIRF records share a surname and unit. No Google Scholar/DBLP/Scopus/homepage data collected.
