# IIT Goa roster notes (iit_goa)

Built 2026-10-27 (resumed after a usage-limit interruption). Scripts: scratchpad `work/iit_goa_roster/code/` (build_roster.py, match.py, extract_snaps.py, parse_*.py); data in `work/iit_goa_roster/data/`. All fetches via the shared `polite_get.py`.

## Sources
* Current: live faculty directory `https://iitgoa.ac.in/facultyprofile/` (84 entries, `live_fp.json`) plus each `*-faculty-profile/?uid=` page (`live_profiles.json`; identifiers only where linked on the page).
* NIRF 2025 and 2026 faculty tables (joining/leaving dates, "currently working"): `nirf2025.pdf`, `nirf2026.pdf`. NIRF 2019-2024 PDFs could not be fetched (118-byte error bodies), so no use.
* Wayback snapshots (CDX of Faculty.php, Faculty16.php, people.php?type=faculty&year=2016/2017/2018, people.php?...&dept=XX, faculty_page.php?id=N): 2017-2021 pages parsed (about 114 of 122 attempted fetches returned 200; the rest of the 216 prioritised snapshots, mostly 2021-2026 WordPress pages, were not needed because the live directory covers them). The 2017 Faculty.php pages load faculty via JS and contain no names.
* Annual report 2016-17 (ar1617.pdf): only IIT Bombay mentors and Prof. Nandakumar Nambath's appointment; 2018-19/2019-20 PDFs download truncated (1 MB), unused.

## Counts
113 rows: 69 current, 13 former, 25 visiting (14 mentor faculty from IIT Bombay), 6 adjunct. Dedup by token-matching names (match.py).
Identifiers: ORCID 1, Google Scholar 10, DBLP 0, Scopus 0 (all from institute profile pages; no ORCID API search done).
Joining year (67 rows) only from NIRF 2025/2026 joining dates; blank otherwise (never guessed).

## Decisions
* Former with NIRF leave dates: B. K. Mishra (founding Director, 2017-2024), Rajesh S. Prabhu Gaonkar (2018-2024), Sreejith A V (2017-2025; still on live site but NIRF 2026 gives leave date 31-12-2025), Ashok Kumar Ummireddi (2023-2024), Biplab Paul (2024). NIRF also lists Neeraja Raghavan (ad hoc staff) and Sundeep Kumar Nayak: Nayak kept as adjunct (Professor of Practice), Raghavan excluded as non-faculty.
* Other former faculty (Kini, Sajid, Bahubalindruni, Rajendran, Majumder, Deka, Kobaku, Sangle): range = labelled year of the archived list (year=2016/17/18) or the snapshot year for unlabelled lists. LAST is the last archived appearance, so true departure may be later; FIRST is first evidence, not necessarily joining. Several snapshot years are crawl dates of "year=2016" pages, so (2016-2016) style ranges mean "listed in the 2016-17 list".
* IIT Bombay mentors listed on the 2016-17/2017-18 faculty pages -> `visiting`, "Mentor faculty from IIT Bombay". Appaji B B (sports officer) and J. Sannigrahi (postdoc) excluded. Prof. Rodney Fernandes was also Dean (Academic Programme & Faculty Affairs) of IIT Goa per the page; kept as mentor/visiting, ambiguous.
* Visiting Madan and Bhartiya (live site says "Former Faculty") -> visiting with archived range. Fellows (Ramanujan, DST-INSPIRE) kept as current with designation.
* People in two units: primary unit only (e.g. Rishikesh Narayan: Chemistry + Biology).
* Departments use the live site names; blank for 7 adjunct/fellow rows without a unit.

## Independent size check
NIRF 2026 lists 65 currently working (incl. contractual/visiting); live site has 84 entries including 14 adjunct/visiting/fellows/former-labelled and one postdoc. Our 69 current + 6 adjunct is consistent after excluding those categories.

## Known gaps
Wayback coverage 2019-2021 only for dept lists; no 2022-2024 snapshots parsed, so regular faculty who left between 2021 and 2024 and are not in NIRF 2025/26 (people leaving before NIRF 2025 date window) may be missing. Tenure ends are lower bounds.
* E-mails of Majumder and Sangle blanked (first-name aliases now used by current faculty); a stray 'contact' e-mail blanked.
