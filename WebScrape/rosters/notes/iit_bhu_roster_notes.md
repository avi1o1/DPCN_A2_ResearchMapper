# IIT (BHU) Varanasi roster notes (iit_bhu)

Built 2026-10-28. Work dir (scratchpad) `work/iit_bhu_roster/{code,data}`; all fetches through the shared `polite_get.py`. Only IIT (BHU) pages used (iitbhu.ac.in/dept/*/people/*); no BHU Institute of Science / IMS / IAS people.

## Size check against NIRF (early, as required)
* Live site: 408 department-list entries (19 units) -> 404 distinct people (4 people listed under both School of Decision Sciences and Engineering and Mechanical Engineering, e.g. P. Bhardwaj, C. Samuel, S. Pratap, Lakshay; primary unit = Mechanical, second unit DSE). School of Physical AI (/dept/spa) lists no people.
* NIRF 2026 faculty table (data year 2024-25/2025-26): 409 rows parsed (408 "currently working", 396 Regular + 13 Adhoc/Contractual); NIRF has no department column, so the unit comparison is by total. Parsed rows per edition: 2019 356, 2021 343, 2022 351, 2023 365, 2024 381, 2025 390, 2026 409. Annual-report faculty strength: 309 (31.3.2021), 324 (2021-22), 349 (2022-23, 2023-24), 359 (31.3.2025; text says 377 regular + 3 visiting + 3 adjunct + 1 contract).
* Our current rows: 412 (404 live-site + 8 NIRF-2026-only regular), of which 374 are NIRF-2026-confirmed (366 live people linked to a NIRF 2026 row). 38 live people are not in NIRF 2026 (mostly 2025-26 joiners). Consistent with NIRF 408/409.
* Per-unit live extraction (current rows): APD 10, Ceramic 11, Chem Eng 28, Chemistry 18, Civil 40, CSE 25, Electrical 26, Electronics 25, HSS 15, Maths 31, Mechanical 44, Metallurgy 28, Mining 18, Pharma 20, Physics 30, Biochemical 12, Biomedical 13, SMST 13 (+5 current with blank unit = NIRF-only). Unit headcounts from NIRF are not published, so misparses were checked by total and by NIRF-name linking (every live person without a NIRF link was inspected; they are recent joiners listed in annual report 2024-25 or unlinked new names).
* Mathematical Sciences, Chemistry, Physics count the IIT (BHU) departments only.

## Sources
1. Live profile pages `https://www.iitbhu.ac.in/dept/<unit>/people/<slug>` (fetched by the golden-set agent, reused; name, designation, unit, email, social links). ORCID taken only from the person's own social-link anchor (210 rows); Google Scholar links parsed from the page body excluding the institute-wide template ID (105 rows); DBLP/Scopus/IRINS none.
2. NIRF data submissions `https://iitbhu.ac.in/contents/iitbhu/docs/nirf_<Y>_overall_report.pdf` (index https://iitbhu.ac.in/nirf). 2019, 2021-2026 parsed (pdftotext -layout; names wrap, 2019 dates wrap, designations wrap). 2018 is an image PDF (not parsed); 2020 body is a 9 KB stub (not usable). Columns: joining/leaving date, currently working, association.
3. Annual reports `.../contents/institute/dean/doaa/doc/annual_report_english_<YYYY-YY>.pdf` 2016-17 to 2024-25: lists of faculty appointed (with joining date and unit), resigned/relieved, retired, expired. Used for unit assignment of former faculty and for leaving dates (override NIRF when earlier). The 2024-25 "internal faculty who joined" lists are promotions/transfers, not appointments, and were not used for joining years.
4. Wayback: CDX `iitbhu.ac.in/dept/<unit>/people/faculty` prefix, last capture per year, 2018-2022; 72 snapshots from 15 units parsed (1020 name/unit rows). CDX for civ and cse failed (timeout), chy, phy and dse returned no captures with that URL form; the crawl was stopped when the coordinator paused parallel work, so no further Wayback was fetched. Wayback was used only for unit assignment (11 former rows), not for tenure ends (old pages go stale).
5. ORCID: offline index `work/orcid_index/iit_bhu_orcid_index.tsv` only; no live ORCID API calls.

## Method
* Persons from NIRF editions were clustered by (joining date + fuzzy name); clusters with disjoint editions and name score >= 0.85 were merged (566 -> 558 clusters). Names are printed surname-first in several editions; matching is token-set based with initials. Live people linked to NIRF clusters one-to-one (score >= 0.6, manual aliases for 10 spelling variants, listed in code/link.py).
* current = on the institute's live list (tie-break: institute list wins) plus NIRF-2026 "Yes" rows not on the live list (NIRF-only, 9 regular rows; 5 of them have no unit).
* former = NIRF cluster absent from live list and from NIRF 2026 (or NIRF "No", or retired per annual report). LAST = leaving year from annual report retire/resign date, else NIRF leaving date, else (last NIRF edition year - 1) (36 people: no leave date, so LAST is a lower bound). FIRST = joining year (NIRF earliest joining date) else first NIRF edition year - 1. NIRF edition Y describes faculty of year Y-1.
* NIRF designation "Other" (age 60-75 re-employed or contractual senior people, plus management/architecture adhoc faculty): status `visiting`, designation "Re-employed / contractual faculty (NIRF 'Other')" or "Adhoc/contractual faculty", with range when no longer listed (83 with range, 31 still listed in NIRF 2026). Their NIRF joining dates are re-employment/contract start dates, so joining_year is left blank for re-employed Regular "Other" rows (70). This is a judgement call: some may be emeritus/honorary; no source distinguishes.
* Retired professors Kamdeo Mandal (retired 31.1.2025 per AR 2024-25) and R. K. Mandal (31.3.2025) are still "currently working" in NIRF 2026 (probably re-employed) but absent from the live list: set `former` (2025).
* joining_year (487 rows): earliest NIRF joining date; evidence = NIRF (dates may be regularisation dates; AR appointment dates agree for 2018-2025 appointees checked).
* People in two units: 4 (Mechanical/DSE) - primary Mechanical.

## Identifiers by route
ORCID 320 rows: institute page link 210; ORCID affiliation record (offline index, role contains professor/faculty etc. or empty role with unit overlap, name score >= 0.9, unique) 110; ORCID API search 0. Ambiguous (several qualifying iDs, left blank): Atul Kumar (two people on the roster), Sanjay Singh, Rajendra Prasad, Vakil Singh (see data/final_stats.json). Google Scholar 105, DBLP 0, Scopus 0, IRINS 0. Email 404 (live profiles only). No "ORCID lookup pending" list (API unused).

## Problems and decisions
* NIRF 2026 text: 'Ropesh Goel' (NIRF) = 'Ropesh Goyal' (AR 2024-25), kept as NIRF spelling; 'Kul Deep Verma' = live 'Kuldeep Verma'; 'Harsha A P' = Arakere Puttaswamy Harsha; others in link.py ALIAS.
* Names in former rows are printed as NIRF prints them (often surname first, e.g. "Mohan Anand Chandra"); not reordered. Nine names occur twice (check_outputs warn): different people with common names (Atul Kumar, Abhishek Kumar, Deepak Kumar, ...).
* Former rows with blank unit: 9 `former`, 103 `visiting` (NIRF has no unit; not on any parsed annual-report list or Wayback list).
* Rajeev Sangal (Director until ~2017; NIRF 2019 only) kept with LAST 2018 from NIRF edition; true end may be earlier.
* Departments: ECE listed as Department of Electronics Engineering, "Chemical Engineering & Technology" as ...and Technology, Biochemical/Biomedical/Materials are "School of ...".

## Known gaps
* Regular faculty who joined and left between 2016 and mid-2018 (before NIRF 2019 data) appear only if in NIRF 2019/AR; NIRF 2018 (image PDF) and 2020 (stub) not parsed; no OCR attempted. Annual reports 2016-17/2017-18 resign lists parsed but short.
* Wayback missing for civ, cse, chy, phy, dse; unit of 82 former/visiting rows blank.
* NIRF-only current people (9) may have left after data submission; no emeritus/adjunct status could be established (no honorary/emeritus page found).
* The live site 2025-26 joiners have no joining year (38 rows, 2024-25 appointees have it via NIRF only when in NIRF 2026).
