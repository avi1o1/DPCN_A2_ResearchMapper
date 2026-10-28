# IIT Madras faculty roster - notes

Output: `rosters/iit_madras_faculty.csv` (996 rows: 670 current, 60 visiting, 266 former; no emeritus/adjunct rows - see gaps).
Pipeline code and cached sources: scratchpad `work/iit_madras_roster/{code,data}` (nirf.py/union.py -> people.json; ar19*.py, livedept.py -> dept maps; assemble.py -> rows; final.py -> ORCID + CSV).
The work was done in two sessions (the first was interrupted by a usage limit); this file covers both.

## Sources used
* NIRF data submissions, faculty tables (join date, leave date, "currently working", association type), every edition available on iitm.ac.in:
  2017 (Faculty-details03Jan2017.docx), 2018 (Overall-Faculty-details.pdf), 2020 (Overall-final.pdf), 2021, 2022, 2023, 2024, 2025, 2026
  (URL patterns `https://www.iitm.ac.in/sites/default/files/NIRF/...`, listed in each row's source_url). No 2019 edition was found. Editions are mapped to data years
  (2017->2016, 2018->2017, 2020->2019, ... 2025->2024, 2026->2026). Rows per edition: 599, 607, 630, 642, 645, 684, 674, 686, 720.
  People were linked across editions by name (initial/token-tolerant) plus compatible joining date.
* Annual reports 2016-17 and 2019-20 (department-wise faculty lists) -> department for people without a live page.
* Live department/centre faculty pages (26 pages: AE, CSE, HSS, Chemistry current/former/retired/emeritus, Mathematics current/retired/visiting, Mechanical, MME, DoMS, ChemE,
  Physics, AMBE, Biotech, Engineering Design incl. adjunct, Civil (6 sub-pages), EE via Wayback copy because www.ee.iitm.ac.in has a broken TLS chain, Ocean via Wayback copy
  `web.archive.org/web/20250616132344id_/https://doe.iitm.ac.in/outerfaculty.php` because doe.iitm.ac.in is unreachable). Used for department only (matched by name).
* ORCID: offline index only (see below). No live ORCID API calls were made.
* Not reachable: dsai.iitm.ac.in, mst.iitm.ac.in, doe.iitm.ac.in, www.ee.iitm.ac.in (DNS/TLS), zanzibar.iitm.ac.in and iitm.ac.in/zanzibar/faculty (ConnectionError).

## Counts by department (current / visiting / former)
Aerospace 38/2/13; AMBE 37/2/3; Biotechnology 34/1/5; Chemical 34/0/5; Chemistry 35/0/8; Civil 61/1/12; CSE 37/0/13; EE 54/0/13; Engineering Design 12/0/0;
HSS 32/0/11; Management Studies 28/1/6; Mathematics 47/0/6; Mechanical 55/0/13; MME 29/0/4; Ocean 25/0/6; Physics 38/0/16; blank department 74/53/132.
Engineering Design (12) and Computer Science (37) look low against NIRF counts of those units; their live pages list fewer people than NIRF or the matching was partial. The
blank-department rows are NIRF-only people (NIRF has no department column) whom no department page or annual report placed.

## Status, tenure and joining years
* current = NIRF 2026 association "Regular" (670). Other NIRF 2026 rows (Visiting 24, Adhoc/Contractual 25, Other 1) -> `visiting`, with the NIRF association kept in the designation.
  Emeritus/adjunct are set only when the NIRF designation says so; there are none, so no emeritus/adjunct rows exist (honorary/emeritus pages were not found).
* former = in an earlier NIRF edition but not in 2026. LAST = year of the NIRF leaving date if one is given, else (edition data year) - 1 of the last edition where listed;
  FIRST = earliest NIRF joining date, else the first edition they appear in. People whose LAST < 2016 were dropped (4: Achintya Mukhopadhyay, B Ramamoorthy, Shireen Mirza, one garbled row).
* LAST is uncertain for people with no NIRF leaving date: it is a lower bound given by the editions (NIRF 2019 is missing, so a departure in 2019 is placed at 2018 or 2019).
* joining_year (982/996 rows) comes from NIRF joining dates (earliest across editions). NIRF dates can be regularisation dates; no other source was cross-checked per person.
* Wayback snapshots of department faculty pages for 2016-2025 were NOT harvested (only the EE CDX listing and the Ocean/EE snapshots above). Former-faculty tenure therefore rests on NIRF
  and the two annual reports; this is the main gap.

## Department rule
Live current page(s) first; if a person is on several department pages, a page also confirmed by AR 2019-20 wins, else the most frequent; conflicts are logged below. Otherwise AR 2019-20,
otherwise a former/retired page. Names in the source with `&` are normalised to "and". The per-person decisions are in `notes_pre.json` (scratchpad); typical ones: "AR2019-20 lists in several units"
(first taken) and "dept pages conflict" (e.g. one person on Aerospace, Management and Mathematics pages -> Aerospace, an associate-listing artefact). Associated faculty never create membership.

## Identifiers
* ORCID: 337 rows, all from the route "ORCID affiliation record" (offline index `iit_madras_orcid_index.tsv`): exact token-set name match (initials allowed against full tokens), an employment/invited-position
  record naming IIT Madras with a faculty-type role, not ended before 2016, and the ORCID matching exactly one roster row. 73 people matched several ORCIDs (or one ORCID matched several rows) and were left blank
  (list: scratchpad `data/orcid_amb.json`). Route 2 (institute/personal page): 0. Route 3 (live ORCID API): 0 - not used. "ORCID lookup pending": all people without a match.
* Department compatibility of the ORCID employment record was not verified; common names (e.g. Srinivasan, Kumar) carry risk although ambiguity was blanked.
* google_scholar, dblp, scopus_id, irins, homepage, email, profile_url: not collected (empty).

## Problems and resolutions
* Same person appearing as both former and current (name variants across editions): final.py merges a former row into a current row only if the sorted name tokens are identical, department is equal or blank and
  joining years are equal or blank (4 candidates; 2 wrong fuzzy merges were rejected by the stricter rule, 2 kept: Meghana Nasre, Venkatraman Srinivasan).
* Remaining same-name pairs (K Srinivasan, Raghu Prakash, V Subramanian, S Mohan) have different joining years or units and are kept as different people (K Srinivasan: a retired professor 1984-2022 and a current professor joined 2004; uncertain).
* NIRF names are sometimes truncated/misspelt/with trailing digits; cleaned by `clean()`; residual duplicates of the same person with spelling variants are possible among former rows.
* www.ee.iitm.ac.in TLS error and doe.iitm.ac.in unreachable -> Wayback copies. The fetcher reported them as DEAD, not redirected to parked domains.

## Independent size check
Annual report 2016-17: "As on 31 March 2017, 573 faculty members ... in service"; NIRF 2017 edition lists 599 rows (includes visiting/ad-hoc) - consistent. For the latest year the only
source available is NIRF 2026 itself (720 rows, 670 regular). No separate 2025-26 annual report was found,
so the current count is NIRF-confirmed by construction (all 670 current rows are in NIRF 2026) and was not independently verified.

## Known gaps
No Zanzibar campus faculty (site unreachable, not in NIRF). No emeritus/adjunct/professor-of-practice people (no pages found), except any flagged by NIRF designation. No Wayback year-by-year pass,
no dept for 259 people, no non-ORCID identifiers, centres/schools (DSAI, CFI, Sustainability, etc.) only through NIRF.
