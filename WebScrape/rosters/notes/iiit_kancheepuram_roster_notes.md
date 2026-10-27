# IIITDM Kancheepuram faculty roster (2016-2026): lab notebook

Built 2026-10-27 by the IIIT-team run (operator Arihant Tripathy). Output: `WebScrape/rosters/iiit_kancheepuram_faculty.csv` (157 rows).
Every fetch went through `agents/polite_get.py`. Downloaded pages, PDFs and scripts are in `C:/Users/Arihant/rm_work/iiit_kancheepuram_roster/{data,code}`, not in the repo. No direct HTTP request was made outside the fetcher. The first run was interrupted twice (DNS outage, usage limit) and resumed from the fetcher cache.

## Totals

| status | rows | joining_year filled | ORCID | e-mail |
|---|---|---|---|---|
| current | 104 (103 on the live faculty list + Director in additional charge) | 102 | 49 | 103 |
| adjunct | 12 (5 on the live list, 7 not listed now, with range) | 10 | 0 | 10 |
| visiting | 17 (2 on the live list: Distinguished Visiting Professors) | 15 | 0 | 10 |
| emeritus | 2 (S Narayanan, S P Venkateshan, with range) | 2 | 0 | 2 |
| former | 22 | 20 | 2 | 14 |
| **total** | **157** | **149** | **51** | **139** |

E-mail comes from the live list and from archived pages. Google Scholar, DBLP, Scopus, IRINS and homepage are blank for everyone (see Identifiers).

### Per-unit counts (department = current official unit name)

| unit | current | former | adjunct/visiting/emeritus |
|---|---|---|---|
| Computer Science and Engineering (CSE) | 24 | 6 | 1 adjunct, 3 visiting |
| Electronics and Communication Engineering (ECE) | 22 | 8 | 2 visiting (live DVPs) |
| Mechanical Engineering (ME) | 22 | 2 | 3 adjunct, 2 visiting, 2 emeritus |
| Sciences and Humanities (S&H) | 21 | 1 | 3 visiting |
| School of Interdisciplinary Design and Innovation (SIDI) | 14 | 1 | 5 adjunct |
| unit not printed by any source | 1 (Director, additional charge) | 4 | 3 adjunct, 7 visiting |

S&H is the live site's grouping of Mathematics (10 on the live list), Physics (8) and English (3); the discipline is not a CSV column. Live list totals: CSE 25, ECE 24, ME 23, SIDI 17, Mathematics 10, Physics 8, English 3 = 110.
Unit-name mapping: "Electrical and Electronics Engineering" (2016-17 page) became ECE; "Mechanical Engineering" unchanged; the 2016-17 pages had Mathematics, Physics, Humanities as separate headings, later "Department of Sciences and Humanities" (Mathematics / Physics / English); "Department of Design" (2023 snapshots) became "School of Interdisciplinary Design and Innovation (SIDI)" by mid-2024. Single campus (Melakottaiyur, Chennai); no second campus.

## Independent size check

* NIRF 2026 (Engineering) faculty table, the institute's own submission: 108 rows, 107 "currently working" (102 Regular, rest Adhoc/Contractual). My list: 110 people on the live faculty page (103 regular, 5 adjunct, 2 distinguished visiting), plus the Director (additional charge).
* NIRF-confirmed current rows: 100 of my 104 `current` rows have a NIRF 2026 row; the four without are Ratna Raju Mekala (joined 2025-26), Manjusha Battabyal (profile and ORCID show 2024), Vijayakumar S (the Mathematics colleague of the same name; the NIRF key collides with the CSE namesake, see below) and Anupam Shukla (Director from 03-09-2026). 103 of the 110 live people have a NIRF 2026 row.
* Difference: 107 NIRF "working" against 110 live: the 7 live people with no NIRF row are the two DVPs, two Professors of Practice, Thurimella, Mekala, Battabyal (mixed: some are visiting/adjunct and not in NIRF Engineering). The other direction: M V Kartikeyan (NIRF 2026 "Yes", Director in the April 2026 Wayback snapshot) is not on the live list and the Director page shows Anupam Shukla in additional charge since 03-09-2026, so Kartikeyan is former (LAST 2026). Suresh Varadarajan, Hariharan S, E P Mohammed Basheer and a few other NIRF-working adjuncts are not on the live list and are filed as adjunct/visiting with a range.
* The roster counts therefore agree with NIRF to within a handful of people. The institute reported "regular faculty strength 40" after the Feb-2018 recruitment (Annual Report 2017-18); NIRF regular rows rise 36 (2017) -> 46 (2018) -> 102 (2026).

## Sources and endpoints

1. **Institute website** `https://www.iiitdm.ac.in/` (SvelteKit). `/people/faculty` embeds the full faculty list as a JS object in the page (`faculties:{cse:{members:[...]},...}`: name, e-mail, `/people/faculty/<email>` profile link, designation, PhD institute, research areas, stream). No JSON endpoint is called; the page source is the data. 110 members. `/administration/director` gives the current Director (additional charge) and `/nirf` the NIRF links. Profile pages were not fetched (not needed for years; see gaps).
2. **NIRF data submissions** on `http://old.iiitdm.ac.in/img/NIRF/<year>/NIRF<year>_Engineering.pdf` for 2017-2026 (links on `/nirf`; also `NIRF2026_Overall.pdf`, not parsed). Each has a "Faculty Details" table (name, age, designation, qualification, experience, working flag, joining and leaving date, association type). Parsed with `pdftotext -raw` and a sequential-serial parser (`code/nirf.py`, `nirf17.py`): rows per year 2017 36 (older layout, joining date only), 2018 46, 2019 56, 2020 66, 2021 55, 2022 73, 2023 83, 2024 82, 2025 81, 2026 108; no unparsed rows. Table-year N includes people joined up to about Jan-Mar of N (the 2022 table has 09-01-2022 joiners), so NIRF year N is used as year-N evidence.
3. **Internet Archive.** CDX queries: `iiitdm.ac.in/People/faculty.php` (53 monthly captures 2017-03 to 2023-06), `www.iiitdm.ac.in/people/faculty` (30 captures 2023-10 to 2026-06; the new SvelteKit site), `iiitdm.ac.in/Faculty.php` (10 captures in 2016 for the first site), `iiitdm.ac.in/old/Faculty.php` (28 captures, not fetched; redundant). Fetched as `https://web.archive.org/web/<ts>id_/<url>`: 2016-03, 2016-12, 2017-03, 2017-08, 2018-03, 2019-07, 2019-12, 2020-06, 2021-01, 2021-10, 2022-06, 2022-12, 2023-06 (old PHP page, one card per person with title, designation, e-mail) and 2023-10, 2023-12, 2024-04, 2024-12, 2025-06, 2025-12, 2026-04 (embedded JS object). 2018-10 snapshot is not archived. About two per year; no change in membership was left unexamined between consecutive snapshots except 2018-03 to 2019-07 (the page lists only 38 then 48 names, and NIRF 2018/2019 cover that gap).
4. **Annual reports** (`old.iiitdm.ac.in/img/AnnualReport/...`): 2015-16 and 2017-18 text-extractable and read (they give "six new faculty joined 2015-16", "sixteen faculty recruited Feb 2018, regular strength 40", and the Dean/HoD lists of 2017-18); 2016_17.pdf is image-only. 2018-19, 2019-20, 2020-21 were downloaded but not mined (no resignation lists were found in the two readable reports, so low expected yield).
5. **ORCID public API**: one `expanded-search` with `affiliation-org-name:(IIITDM OR "IIITDM Kancheepuram" OR ... Kancheepuram AND "Information Technology" AND Manufacturing ...)`, 3 pages of 200, 437 profiles; then 51 `/employments` calls for name-matched candidates. No 429. No per-person searches.

## How current, former and tenure years were established

* **Current** = on the live institute faculty list (Oct 2026). The institute-wide list wins over NIRF (tie-break). Adjunct Faculty and Professor of Practice rows are `adjunct`; the two Distinguished Visiting Professors are `visiting`.
* **joining_year** = earliest NIRF joining date of the person (year), from any table; for the 2017 table the printed year. 8 rows are blank: six live people not in NIRF (Thurimella, Mekala, Rao, Joshi, Rama Manohara Babu, Battabyal) and two archive-only people (Muneeswaran P, Priyabrata Sahoo).
* **Former**: each is absent from the live list and either has a NIRF leaving date or disappears from successive archived lists. LAST = the NIRF leaving year when one exists (NIRF lists lag: e.g. Pandian shows "Yes" in the 2021 and 2022 tables after a 31-12-2020 leaving date, Karthikeyan in 2019-20 after 17-05-2018), otherwise the latest of the last archived snapshot and the last NIRF "working" table year.
* FIRST = joining year.
* **Stale pages**: the 2016 pages list only 30-35 names and no leavers from before 2016; none was used alone as presence evidence for someone absent from NIRF. Presence in a snapshot was only taken as evidence where it agrees with NIRF dates.
* Aliases used for merging: Shak Noor Mahammad / Noor Mahammad SK, Umarani J / Umarani Jayaraman, Vijayakumar K / Vijayakumar Krishnasamy (ECE), Anushree Purushottam Khandale / Anushree P Khandale, Gouthaman / Gowthaman Swaminathan, Dr Venkatramani / J Venkatramani, Sudhir Varadharajan / Varadarajan, Chitra Chandrashekar / Chitra C (same unit and start, 2021-08), Hari Narayanan (2017 page, e-mail tknarayanan) / T S Narayanan (Hari) (NIRF joining 17-07-2017; e-mail differs, merged with moderate confidence), Suresh Varadharajan / Varadarajan (age consistent across 2018 and 2026 tables), N Vijayarangan / Vijayarangan Natarajan, S Rajasekara Pandian / Shunmugham R. Pandian.

## Identifier counts by route

* ORCID: 51 from the affiliation search plus an `/employments` check showing Kancheepuram employment and a name match; 0 from institute pages (profile pages were not fetched; the faculty list does not carry ORCID).
* Checked and not accepted: 0009-0001-0167-7051 ("Karthick V J", could be neither Karthick S nor Karthick G), 0000-0002-7808-7180 (Vivek Kumar Chouhan, other institutions), 0009-0008-8238-0997 (Naveen Kumar Kasukurthi, IIITDM Kurnool). Weak accepts (very common names, Kancheepuram employment with plausible start): Naveen Kumar 0000-0003-0865-7421, Vivek Kumar 0000-0003-3386-0755, Raja B 0000-0003-0445-888X, Avinash Kumar 0000-0002-8071-5748, Om Prakash 0000-0003-0482-072X, Jayavel S 0000-0002-2334-2842; Priyanka Kokil's and some others' ORCID start years are self-declared and were not used as evidence.
* Google Scholar, DBLP, Scopus ID, IRINS, homepage: 0 (not on the faculty list; profile pages not fetched; IRINS/Scopus scraping not allowed).
* ORCID lookup pending: none (no 429); most current people have no ORCID simply because no per-person searches were run.

## Conflicts and ambiguous people (decision taken)

* **Two Vijayakumar S** (same printed name): CSE (`vijaycse@`, NIRF 2026 joining 28-11-2024) and Mathematics (`vijay@`, NIRF joining 24-07-2009, HoD Mathematics 2017-18). Two rows; the NIRF key for both collides, so the Mathematics row's NIRF-2026 confirmation is not asserted. Joining years 2024 and 2009.
* **Vijayakumar K / Vijayakumar Krishnasamy** (ECE, NIRF joining 25-04-2018) is a third, different person.
* **M V Kartikeyan**: Director from 2022 (NIRF 12-10-2022, "Professor and Director" on every snapshot to 2026-04), absent from the live list; the Director page shows an additional-charge Director from 03-09-2026. Former, 2022-2026 (LAST uncertain by a few months; Department ECE from the department heading).
* **Anupam Shukla** (Professor at ABV-IIITM Gwalior): Director (additional charge) since 03-09-2026. Included as `current` per the brief's rule that a Director holds a post at the institute; he is not on the faculty list and has no unit. The ABV-IIITM roster presumably also lists him. Flag for downstream: not a Kancheepuram appointment in the usual sense.
* **Gnanamoorthy R** (Director to 26-07-2017, NIRF joining 20-07-2007) and **Banshidhar Majhi** (Director 26-07-2017 to 04-08-2021): former, units set to ME and CSE from their fields.
* **S Rajasekara Pandian** (Dean Planning): NIRF 25-05-2015, leaving 31-12-2020, on archived pages to 2019-12; unit ECE from the 2016 "Electrical and Electronics Engineering" heading.
* **Sudhir Varadarajan**: "Visiting Faculty, Dean (DII)" in Annual Report 2017-18 but NIRF "Regular" from 22-07-2015 and Associate Professor in SIDI now. Kept as current, joining 2015.
* **Karthikeyan S S**: NIRF 2017 says 2016, NIRF 2018 says 17-08-2011 (left 17-05-2018); on the March 2016 page, so 2011 used.
* **Visiting/adjunct people** (NIRF "Visiting" or "Adhoc/Contractual", also on the faculty pages as "Visiting Faculty", "Adjunct Faculty", "Faculty on Contract"): A Divya, Anumula Sunilkumar, C Chandrasekaran, Charles Suresh David, Jegannathan Srinivasan, P Ganesan, P Sekar, R Karthic Narayanan, Shankar Raman M J, Subramanian Swaminathan, Suresh Varadarajan, Swathi Tanjore Gurumani, T S Narayanan, Vasumathi K Narayanan, N Vijayarangan, Nargis Pervin, plus 2022-25 adjuncts (Sundara Mohan, Velan, Basheer, Jinan Kodapully, Hariharan S, Hariesh K). Ranges use the NIRF joining/leaving years and snapshot years. S Narayanan and S P Venkateshan are shown as "Emeritus"/"Emeritus (Adjunct)" in the 2019 department page and are `emeritus` (their NIRF type is Visiting; they appear as IIT Madras emeriti, but no source calls them mentor faculty, so no "Mentor faculty" label was used).
* **Mentor IIT Madras**: no dated source (annual reports 2015-16 and 2017-18, snapshots from 2016, NIRF) describes IIT Madras mentor faculty in 2016-2026; no rows labelled mentor.
* **Satish Gunturi, Priyabrata Sahoo, Muneeswaran P** (Temporary Faculty on the 2023-12 snapshot): unit and designation partly unknown; Sahoo appears on one snapshot only (2023-06) and is retained as "Faculty (listed 2023)" with LAST 2023.
* **Ram Prasad Padhy**: NIRF 2025 still "Yes", last snapshot 2024-04, not on the live list. LAST 2025 (uncertain by about a year). **E P Mohammed Basheer, M Velan, Jinan Kodapully**: NIRF 2025 or last snapshot 2024-12; LAST 2025 or 2024 uncertain.
* **Chetan** (ME, Assistant Professor): NIRF 2020 and the 2019-12 snapshot only; LAST 2020 (maybe 2019).
* **Hariharan S** (adjunct): NIRF 2026 working, not on the live list: kept as adjunct with range to 2026.

## Problems and how they were resolved

* Network outage and usage-limit pauses mid-run; resumed from cache.
* Python `-I` ignores PYTHONUTF8: scripts reconfigure stdout to UTF-8.
* The shared JS-object parse overwrote a prior output once (live list), regenerated.
* NIRF layout varies by year (2017 has one old layout with year-only joining dates and a page-break duplicate row; 2018-2021 have an extra "associated last year" column and dates split over lines; a "31-05 2018" typo); parser handles all.
* No bot walls and no dead hosts (the institute site returned 200; its `old.iiitdm.ac.in` host serves the PDFs).

## Known gaps

* Profile pages (`/people/faculty/<email>`) not fetched: no per-person homepage/Scholar/ORCID links and no CV evidence of joining years; joining years are NIRF dates (may be regularisation dates).
* Archived page density: two to three per year; leavers who joined and left between snapshots and were never in a NIRF Engineering table could be missing (especially 2016-17 and 2018-19, when NIRF tables are small). Annual reports 2016-17 (image only), 2018-19, 2019-20, 2020-21 not mined.
* NIRF year labels: table N used as year-N evidence; leaving dates in NIRF are entered retroactively.
* ORCID employment start/end years are self-declared and were not used as tenure evidence.
* Faculty in the NIRF Overall/Innovation submissions only (not Engineering) would be absent from the NIRF parse; the live list covers current ones.


## Operator decision (2026-10-27)
Anupam Shukla (Professor at ABV-IIITM Gwalior, Director of IIITDM Kancheepuram in additional charge since 03-09-2026) changed from `current` to `adjunct` with range (2026-2026). He is regular faculty of another institute; as adjunct he contributes only papers that print IIITDM Kancheepuram's affiliation (PROCESS.md §15.6), so his Gwalior papers cannot enter through the person channels.
