# IIT Palakkad faculty roster (2016–2026): lab notebook

Built 2026-10-25. Output: `WebScrape/rosters/iit_palakkad_faculty.csv` (230 rows). Every fetch went through the shared
`polite_get.py` (rate-limited, cached). Downloaded pages and parsing scripts are in the session scratchpad
(`work/iit_palakkad_roster/data` and `.../code`), not in the repo.

## Totals

| status | rows | joining_year filled | ORCID | e-mail |
|---|---|---|---|---|
| current | 160 | 153 | 99 | 48 |
| former | 41 | 36 | 5 | 26 |
| visiting | 17 (13 IIT Madras mentor faculty from 2015-16, T. Sundararajan, Haridas V, Ravi K R, V. Muruganandam) | 3 | 0 | 3 |
| adjunct | 12 (8 adjunct faculty + 4 honorary professors) | 7 | 0 | 3 |
| **total** | **230** | **199** | **104** | **80** |

Other identifiers: Google Scholar 30 (institute profile pages, plus 3 archived profiles of former faculty), DBLP 2, Scopus 1,
homepage 70 (the "View Website" link on the profile). IRINS: none collected. The IRINS link is on the site but the brief forbids
using IRINS.

### Per-department counts (department = current official unit name)

| department | current | former | visiting | adjunct/honorary |
|---|---|---|---|---|
| Biological Sciences and Engineering | 5 | 0 | 0 | 0 |
| Chemistry | 12 | 4 | 5 | 1 |
| Civil Engineering | 23 | 5 | 0 | 1 |
| Computer Science and Engineering | 19 | 2 | 0 | 3 |
| Data Science | 11 | 1 | 0 | 0 |
| Electrical Engineering | 21 | 5 | 1 | 1 |
| Environmental Sciences and Sustainable Engineering Centre (ESSENCE) | 2 | 1 | 0 | 1 |
| Humanities and Social Sciences | 8 | 2 | 2 | 0 |
| Materials and Metallurgical Engineering | 1 | 0 | 1 | 2 |
| Mathematics | 18 | 5 | 2 | 1 |
| Mechanical Engineering | 25 | 6 | 6 | 0 |
| Physics | 15 | 8 | 0 | 2 |
| (unit not printed) | 0 | 2 | 0 | 0 |

Unit-name mapping: "Computer Science And Engineering" (profile spelling) became "Computer Science and Engineering". "Humanities" (2016-2019 pages) became
"Humanities and Social Sciences". "Civil Engg"/"Electrical Engg" (AR 2016-17) were expanded. The Nov-2016 page listed three IIT Madras
mentors under an "Applied Mechanics" heading, but IIT Palakkad has no such unit, so they are mapped to Mechanical Engineering. Sunitha K Nayar was listed under
Civil Engineering until about 2022 and later under ESSENCE, so ESSENCE is the primary unit and Civil Engineering the second.
Both campuses were covered: the Ahalia (temporary) campus addresses appear on the 2015-2022 pages and the Nila/Kanjikode campus on the current site.
There is one institute-wide faculty list, not one list per campus.

## Sources and endpoints

1. **Current lists (live site, Drupal):**
   * `https://iitpkd.ac.in/faculty-list` gives 163 entries (name, profile link, unit). The page is not paginated.
   * `https://iitpkd.ac.in/faculty-a-z-lists` gives 161 entries. The only difference is two profiles that still use `/user/NNNNN` URLs.
   * `https://iitpkd.ac.in/adjunct-faculty` gives 8 entries and `https://iitpkd.ac.in/honorary-professor` gives 4.
   * All 175 profiles `https://iitpkd.ac.in/people/<slug>` were fetched. Fields used: `field-full-name`, `field-designation-1`,
     `field-secondary-affiliation` (unit, comma-separated if more than one), `field-public-e-mail-id` (30 profiles), and `field-website`.
     Identifier links were taken from the header and biosketch only. Links inside the publication list were ignored because they point to co-authors.
   * No JSON/AJAX endpoint was found. The Drupal views render server-side.
   * `https://iitpkd.ac.in/reports-brochures` returned a JavaScript "eval(p,a,c,k,e,d)" bot-challenge page to the fetcher. It was
     **not bypassed**. The Wayback copy `web/20260618084350` was used instead to get the annual-report links. The PDFs themselves download directly.
2. **Department sites (live):**
   * Physics former faculty: `physics.iitpkd.ac.in/formerfaculty/`
   * Mathematics past faculty: `math.iitpkd.ac.in/past_faculty.html`
   * Mathematics visiting faculty: `math.iitpkd.ac.in/visitingfac.html`
   * Chemistry former faculty: `chemistry.iitpkd.ac.in/node/31`
   * Faculty and people pages: `cse.iitpkd.ac.in/faculty/`, `ee.iitpkd.ac.in/faculty`, `essence.iitpkd.ac.in/people`, `mme.iitpkd.ac.in/people`,
     `cet.iitpkd.ac.in/people`, `ce.iitpkd.ac.in/`. These were used for e-mails (name followed by an e-mail within 700 characters).
   * `ds.iitpkd.ac.in` failed with an SSL error. `physics.iitpkd.ac.in/people` returned 404.
3. **Internet Archive:** The domain CDX query `cdx?url=iitpkd.ac.in/&matchType=domain&from=2015&to=2026&filter=statuscode:200` returned 74,849
   URLs and was used to find the list pages of every site generation:
   * 2015-16 WordPress site `iitpkd.ac.in/academics/faculty/`: 4 snapshots (2015-07, 2015-09, 2016-03, 2016-11).
   * 2016-19 `turing.iitpkd.ac.in/iitpkd/index.php/faculty/` and `/web/index.php/faculty/`: 9 snapshots (2016-12 to 2019-09). This site
     was frozen from about mid-2018, so its later snapshots were not used as end-of-tenure evidence.
   * 2018+ Drupal `iitpkd.ac.in/faculty-list`: 40 monthly captures in CDX. 27 were fetched, covering 2018-01 to 2026-06 at least every 6 months and densely in 2019-2022.
   * `iitpkd.ac.in/faculty` (2021-2024, 6 snapshots): this page went stale, still listing people after they left, so it was not used for LAST.
   * `adjunt-faculty` (sic, 2019-2022, 8 snapshots), `adjunct-faculty` (2022-2026, 9), `honorary-professor` (2024-2026, 6).
   * `list-faculty` (empty view) and `50-faculty-members` (static page) gave no names.
   * 31 archived profile pages of former or visiting people were fetched via `web/2026id_/https://iitpkd.ac.in/people/<slug>`. Four
     (psmehta, tvm, mahesh, satyajitdas) are archived as HTTP 403.
   * The polite fetcher made one snapshot request per URL, using `id_` raw snapshots. The monthly sampling was thinned to one snapshot per half-year because Wayback was slow (shared with other agents).
4. **Annual reports** (live PDFs; links from the Wayback copy of reports-brochures): 2015-16, 2016-17, 2017-18, 2018-19, 2019-20, 2020-21,
   2021-22, 2022-23, 2023-24. Faculty lists were taken from the department sections in "Dr. Name, PhD (...)" format. 2016-17 uses a table with
   designation. 2015-16 lists Faculty / Full-time Visiting / Visiting from IIT Madras / Guest faculty. The 2022-23 and 2023-24 reports mark leavers
   "* relieved on <date>" or "on lien from".
5. **NIRF data submissions** (live PDFs from `https://iitpkd.ac.in/nirf`): Overall 2022, 2023, 2024, 2025 and 2026 (and Engineering for
   cross-checking). The "Faculty Details" table gives name, designation, *joining date*, *leaving date*, "currently working" and
   association type (Regular / Visiting / Adhoc-Contractual / Other). Names in it are often cut off by the PDF layout (e.g. "Bibhu Ranjan"), so
   matching used initial-aware token containment and hand checks for the 6 one-word names (e.g. "Deepak", "Lakshmi", "Mahesh", "Swapnil").
6. **ORCID public API:**
   * `pub.orcid.org/v3.0/expanded-search/?q=affiliation-org-name:"Indian Institute of Technology Palakkad"` returned 516 records.
     `affiliation-org-name:Palakkad` returned 750 and `"IIT Palakkad"` returned 8. They were merged (750 unique).
   * For roster names with no candidate in that set, the API was queried with `given-and-family-names:"<name>"`.
   * Every candidate (583 ORCID iDs) was checked through `/v3.0/<id>/employments`. A candidate was accepted only if an employment
     organisation is IIT Palakkad ("Indian Institute of Technology" or "IIT" plus Palakkad as the name or city), the name matched, and exactly one
     such iD matched the person.

## Former faculty and tenure years

* **Former** means on an institute faculty list at some time from 2016 on and not on the current lists.
* **FIRST** is the first evidence year from any source (2015 for the founding cohort, which is below 2016 as the brief allows).
* **LAST** is taken in this order of preference:
  1. NIRF leaving date or annual-report "relieved on" date.
  2. Department former-faculty page.
  3. Last faculty-list snapshot (or AR 2017-18 for FY ending Mar 2018).

  Where LAST comes only from a snapshot, the note says so. The main archive gap is 2018-01 to 2019-08 on `faculty-list`, which affects Arolla,
  T. K. Krishna Kumar, Valsakumar, Abraham and M. S. Mathews.
* **Found by:**
  * Wayback lists: 30
  * 2015-16 page / AR 2015-16 only: Deepesh, KK Balasubramanian, Kasiviswanathan, M. S. Mathews, Ramachandraiah
  * turing site only: Deepu P, Naveen Chandran, B. V. R. Tata
  * NIRF leaving dates confirmed 17 of them.

  Every name in NIRF 2022-2026 and in the AR 2017-18 to 2023-24 faculty lists was matched to someone on the roster. There were no unexplained leftovers,
  which is evidence that the former-faculty pass is complete for 2017 onwards.
* **IIT Madras mentoring:**
  * 13 serving IIT Madras faculty listed in Jan-Nov 2016 ("Visiting Faculty from IIT Madras") are `visiting` with designation
    `Mentor faculty from IIT Madras (FIRST-LAST); <IITM post>`.
  * Retired IITM professors and IGCAR retirees who were full-time or visiting faculty (KK Balasubramanian, A. Ramachandraiah, Valsakumar, Govindan Kutty)
    are `former`.
  * P. B. Sunil Kumar (IITM professor, then Director 2017-2022) and S. Kasiviswanathan (deputation from IITM, 2015-2017/18) held posts at
    IIT Palakkad and are `former`. **Kasiviswanathan is borderline mentor/regular.**
  * T. Sundararajan was a 2016 mentor and is a current Visiting Professor (one row, status visiting).
* **Excluded:**
  * Ten IITM and other people listed only for the July-Nov 2015 semester (before 2016-01-01): Thamban Nair, C. Balaji,
    P. Sriram, Mahesh Panchagnula, Prathap Haridoss, Sujatha Srinivasan, Arun Menon, Balaganesan, U. V. Varadaraju, Narayanan Namboodiri.
  * AR 2015-16 "Guest Faculty" from NCBS/CES (Ajith Kumar, Anand Osuri, Hari Shridhar).
  * Mentor Director Bhaskar Ramamurthi and Senior Project Advisor V. G. Idichandy (administration, not faculty).
  * Postdocs, staff and students.

## Joining year (199 filled; never guessed)

* **NIRF joining date: 131.** The earliest across 2022-2026 editions is used.
* **Profile biosketch (curated, quoted in the note): 16.**
* **Founding-cohort correction: 11.** NIRF gives 23-06-2017 (the date contracts were regularised) for people listed as faculty in 2015 or 2016, so the
  first listing year on the old faculty page was used (Jasine Babu 2015; Arvind Ajoy, Debarati, Deepak R., Anil Kumar, Madhu Karthik,
  Jayanarayanan, Padmesh, Swaroop, Uma 2016; Lakshmi Sankar 2016). Sudheesh was "joining soon" in 2016 and so gets 2017.
* **First appearance on a faculty-list snapshot when the previous snapshot is no more than 9 months earlier: 8** (2025-26 joiners who are not yet in NIRF).
* **Former faculty: 36**, from NIRF, AR or first listing.
* **Rule:** joining_year is the first year of *any* faculty appointment at IIT Palakkad (visiting, deputation, inter-IIT exchange, INSPIRE) except IITM
  mentoring. Examples: Anand T. N. C. 2020 (exchange) before regular 2022; Manoj Gopalakrishnan 2021 (visiting) before regular 2026;
  Mayank Tiwari 2024; Swapnil Hingmire 2021 (left 2022, rejoined 2024).
* **Blank (7 current):** Arvind Kumar, Arvind Adimoolam, Aramanda Shanmukha Kiran, C. S. Gopinath, Gokularam M, Gurdev Singh,
  Maripini Himabindu. All are new (2025-26, not in NIRF 2026) and their profiles give no date.

## Identifiers by route

* **ORCID: 104.**
  * Institute profile page: 3.
  * ORCID API affiliation search plus employment check: 99.
  * ORCID API name search plus employment check: 2 (Deepak Jaiswal, Unnikrishnan Cheramangalath; employment org recorded as
    "Indian Institute of Technology", city Palakkad).
  * 0 were rejected as ambiguous.
  * Caveat: Soumya Mukherjee's ORCID shows IIT Palakkad only as "Post Doctoral Fellow". The name matches the current Assistant Professor and was kept.
* **Google Scholar: 30.** All from profile pages (header or biosketch links). For former faculty, from archived profiles (Vinod A Prasad, K P Krishnaraj,
  H. V. R. Mittal). Links whose `user=` appears only inside citation links were normalised to `citations?user=<id>`.
* **DBLP: 2** (Nikhil Krishnan M, Srimanta Bhattacharya). Koninika Pal's profile has 8 dblp links that are all co-authors, so it was left blank.
* **Scopus: 1** (Gopikrishnan C. R.).
* **E-mail: 80.** Sources: profile e-mail field (obfuscations like "x [at] iitpkd [dot] ac [dot] in" normalised), department pages, 2015-17 faculty pages,
  and archived profiles. IIT Madras addresses printed for mentors are kept in the notes only.

## Independent size check

* **NIRF 2026 Overall** (data year 2024-25; `.../2026-03/6c4b075c-....pdf`) lists 149 faculty:
  * 144 "currently working": 128 Regular, 7 Adhoc/Contractual, 5 Other, 4 Visiting.
  * 5 left during the year: Satyajit Das, Akshay Bhatnagar, S. Sridhar, Sunitha K Nayar, Mayarani M. All are `former` here.
* **This roster as of Oct 2026:** 160 `current` plus 3 visiting on the faculty-list (163), plus 8 adjunct and 4 honorary.
* **Reconciliation:**
  * 133 of the 160 current faculty appear in NIRF 2022-2026.
  * The remaining 27 are not in any NIRF edition:
    * 19 have joining_year 2025 or 2026.
    * 7 have a blank joining_year. All appear on the faculty-list only from mid-2025, and their self-declared ORCID employment starts in 2024-2026 (C. S. Gopinath: Visiting Professor 2024; Kiran and Gurdev Singh: 2026). ORCID dates were not used as joining_year evidence.
    * Subrat Kumar Mallick: his profile says he joined in Aug 2024, yet he is not in NIRF 2025 or 2026. Unexplained.

    These late joiners account for the rise from 128 regular to 160.
  * The NIRF "Adhoc/Contractual/Other" rows are the adjunct and honorary people (Haragopal, Chittur, Langoju, Rajesh Krishnan, C. Vijayan,
    V. P. Joy, V. Kumar, R. Venkataraghavan) and INSPIRE/Ramanujan fellows (Moumita Nandi, Abdul Rasheed P, Arijit Hazra).
* The same check against NIRF 2025 (data 2023-24): 130 faculty listed, all present in the roster.
* **Conclusion:** the size is consistent and no current faculty member is missing.

## Problems and decisions

* `reports-brochures` bot challenge (see above). `ds.iitpkd.ac.in` SSL error. Four archived profiles return 403. Nothing was bypassed.
* The Wayback API was slow because several agents shared the 3 s slot. Snapshot sampling was thinned to one per half-year after the
  first 17 faculty-list snapshots, which were monthly for 2018-2020. All 2016-2017 snapshots were kept.
* `iitpkd.ac.in/faculty` and the turing site keep stale entries, so they were not used for LAST.
* **Honorary professors** have no matching status in the brief. They are `adjunct` with designation "Honorary Professor".
  The 4 honorary professors are C. Vijayan, V. Kumar, V. P. Joy and Venkatesh Raman.
* **INSPIRE / Ramanujan / Ramalingaswami fellows** are on the institute faculty list, so they are kept as `current` with the fellowship as designation.
  Moumita Nandi is still on the institute list but the physics department lists her as former (2021-2026). She is kept as current per the brief's rule.
* **V. Muruganandam** is off the institute list since Nov 2025 but is on the maths department's visiting-faculty page and NIRF 2026, so he is `visiting`.
* **R. Venkataraghavan:** NIRF 2026 says he is still working, but he is not on the current adjunct page, so he is `former` (2019-2025).
* **S. H. Kulkarni:** the maths page says 2017-2020 but NIRF and the AR say 23-07-2019 to 31-05-2023. NIRF/AR was used, and FIRST = 2016 (IITM visiting faculty).
* **Name as printed:** NIRF/AR variants (e.g. "Chandrashekar", "Mula V S", "Birenjith P A") were mapped to the website name.
  "K. P. Naveen Chandran" adds initials inferred from his e-mail kpnchn. The page printed "Prof. Naveen Chandran" (flagged).

## Known gaps

* Faculty who joined and left inside the 2018-01 to 2019-08 archive gap and are not in AR 2017-18 or 2018-19. None are expected, because NIRF 2022 lists leavers back to 2019.
* No NIRF faculty tables before the 2022 edition are available, so LAST for 2018-2019 leavers rests on snapshots.
* Department not printed for adjuncts Ravi N. Banavar and R. Venkataraghavan.
* 61 current faculty have no ORCID. The brief forbids scraping IRINS, Scopus and Scholar for IDs.
* Mentor faculty rows have only 2016 evidence. Other IITM faculty may have taught single courses without being listed.

## Per-person notes (ambiguities, second units, non-NIRF joining sources)

| name | status | note |
|---|---|---|
| Debarati Chatterjee | current | second unit: Physics ; joining_year 2016 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Padmesh A | current | joining_year 2016 from first institute listing (old faculty page); NIRF joining date 27-06-2017 |
| Sushabhan Sadhukhan | current | second unit: Biological Sciences and Engineering ; joining_year source: NIRF joining date 04-07-2019 |
| V Kumar | adjunct | second unit: Materials and Metallurgical Engineering ; joining_year source: NIRF 2025/2026: joined 02-11-2023 |
| K. K. Balasubramanian | former | AR 2015-16 "Guest Faculty"; on faculty page Jul 2015 - Nov 2016. Retired IITM faculty (not serving IITM faculty) so not classed as mentor. |
| K. L. Sebastian | former | NIRF 2022: joined 04-01-2017, left 30-11-2020. Dean R&D (AR 2016-17). Chemistry dept former-faculty page. |
| K. V. Govindan Kutty | former | NIRF 2022: joined 03-08-2015 (Visiting), left 21-06-2020. Retired IGCAR. Chemistry dept former-faculty page. |
| Priyakumari C P | former | Faculty-list from Feb 2021; relieved 28 July 2023 (AR 2023-24); chemistry former-faculty page. |
| Athira P | current | second unit: Environmental Sciences and Sustainable Engineering Centre ; joining_year source: NIRF joining date 13-07-2017 |
| M. V. Anil Kumar | current | joining_year 2016 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Madhu Karthik M. | current | joining_year 2016 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Sudheesh T. K. | current | joining_year 2016 from first institute listing (old faculty page); listed as "Joining soon" Nov-Dec 2016, on faculty list Feb 2017; NIRF regular date 23-06-2017 |
| A. Ramachandraiah | former | Listed only in the Nov 2016 snapshot of the old faculty page. |
| Balaji Narasimhan | former | Adjunct page Nov 2020 - Jan 2024 (IIT Madras faculty). |
| M. S. Mathews | former | Listed on faculty page from Jul 2015; Annual Report 2017-18 faculty list; last on turing.iitpkd.ac.in list Dec 2017. Not in NIRF 2022 (so left before 2019-20). LAST=2018 from AR 2017-18 (FY ending Mar 2018); exact leaving date unknown. |
| S.M.Shiva Nagendra | former | Adjunct page Nov 2020 - Jan 2024 (IIT Madras faculty). |
| Tom V Mathew | former | NIRF 2022: joined 01-07-2019, left 30-06-2021 (Other; IIT Bombay professor). |
| Deepak Rajendraprasad | current | joining_year 2016 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Jasine Babu | current | joining_year 2015 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Venkatesh Raman | adjunct | designation not printed on profile |
| Chandra Shekar Lakshminarayanan | former | NIRF 2022/2023 ("Chandrashekar"): joined 23-07-2018, left 31-08-2021. |
| Satyadev Nandakumar | former | NIRF 2023: joined 16-09-2021, left 19-07-2022 (Other; IIT Kanpur faculty). |
| Koninika Pal | current | second unit: Computer Science and Engineering ; joining_year source: NIRF joining date 06-09-2021 ; profile lists 8 dblp links (co-authors); none identifiable as hers without name match - left blank |
| Nikhil Krishnan M | current | second unit: Electrical Engineering ; joining_year source: profile/NIRF: DST-INSPIRE Faculty from Sep 2022, Assistant Professor from Nov 2023 |
| Sahely Bhadra | current | second unit: Computer Science and Engineering ; joining_year source: NIRF joining date 12-07-2018 |
| Swapnil Hingmire | current | joining_year source: NIRF: joined 23-12-2021, relieved 15-07-2022, rejoined 25-07-2024 |
| Satyajit Das | former | NIRF 2026: joined 31-05-2019, left 19-05-2025. Listed under CSE then Data Science (second unit CSE). |
| Arvind Ajoy | current | joining_year 2016 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Swaroop Sahoo | current | second unit: Physics ; joining_year 2016 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Lakshmi Narasimhan Theagarajan | former | NIRF ("Lakshmi"): joined 04-08-2017, left 30-11-2022; AR 2022-23 "on lien from November 30, 2022"; listed under Data Science in AR 2022-23 (second unit). |
| Mahesh R Panicker | former | NIRF: joined 14-06-2018, left 30-11-2023 (AR 2023-24 relieved 30 November 2023). |
| Selvakumar | former | NIRF 2024: joined 01-01-2023, left 31-12-2023; adjunct page Mar 2023 - Jan 2024; AR 2023-24 "Prof. C. R. Selvakumar, PhD (IIT Madras)". |
| Venkata Vanukuru | former | Adjunct list in AR 2016-17; adjunct page until May 2020; absent Nov 2020. |
| Vinod A Prasad | former | NIRF: joined 25-10-2017, left 10-06-2022 (AR 2022-23 relieved June 10, 2022); on leave at HKUST in 2021-22. |
| Deepak Jaiswal | current | second unit: Civil Engineering ; joining_year source: NIRF joining date 08-02-2021 |
| Sunitha K Nayar | former | NIRF 2026: joined 16-12-2017, left 17-12-2024 (Visiting). Listed under Civil Engineering until ~2022, later ESSENCE (renamed/moved unit; second unit Civil Engineering). |
| Santhosh Abraham | former | Faculty-list Jan 2018, turing list Jun 2018, AR 2017-18 faculty list; gave an institute talk 31 Oct 2018 (AR 2018-19) but not in AR 2018-19 faculty list; absent from Aug 2019 faculty-list. joining_year from first listing (AR 2017-18 / Jan 2018). |
| Shalina Susan Mathew | former | Visiting faculty Nov 2016; Asst. Prof. on contract (AR 2016-17); AR 2018-19 faculty list; last on faculty-list Aug 2019. |
| C. R. Jayanarayanan | current | joining_year 2016 from first institute listing (old faculty page); NIRF joining date 27-06-2017 |
| Lakshmi Sankar K | current | joining_year source: listed as Assistant Professor in Nov 2016 snapshot and AR 2016-17; NIRF regular date 03-07-2017 |
| Varadharajan Muruganandam | visiting | NIRF: Visiting Professor from 09-08-2021 (2026 edition: 01-09-2021), still working at NIRF 2026 data date; on institute faculty-list Aug 2021 - Nov 2025 but not on it in Oct 2026; currently listed on math dept Visiting Faculty page (https://math.iitpkd.ac.in/visitingfac.html), hence visiting not former. |
| Hari Vansh Rai Mittal | former | NIRF: joined 13-12-2021, left 10-06-2023 (AR: relieved 09/06/2023); math past-faculty page 2021-2023, now IIT Ropar. |
| K. P. Deepesh | former | Listed Jul 2015 - Mar 2016 (Dept. of Applied Science, GEC Calicut); AR 2015-16 "Full Time Visiting Faculty". |
| K. P. Naveen Chandran | former | Listed Nov 2016 - Jun 2017 (old site / turing.iitpkd.ac.in). Printed as "Prof. Naveen Chandran"; initials from e-mail kpnchn; name given with initials only as an inference - check. |
| R Venkatesh | former | Adjunct page Aug 2024 only. |
| S. H. Kulkarni | former | Nov 2016: visiting faculty from IIT Madras; NIRF: joined 23-07-2019, left 31-05-2023 (Other/Visiting); AR 2022-23 relieved 31/05/2023; math past-faculty page says 2017-2020 (conflict; NIRF/AR used). |
| Anand T. N. C. | current | joining_year source: NIRF 2022: Associate Professor (on Inter-IIT faculty exchange from IIT Madras) from 01-01-2020; regular from 28-07-2022 (NIRF); profile agrees |
| Mayank Tiwari | current | second unit: Materials and Metallurgical Engineering ; joining_year source: profile/NIRF: Visiting Professor from 15 Jul 2024, Professor from 18 Jun 2025 |
| Sovan Lal Das | current | joining_year source: NIRF joining date 03-12-2018 ; designation not printed on profile |
| T Sundararajan | visiting | joining_year source: NIRF 2026: Visiting Professor from 01-06-2022 ; also visiting (mentor) faculty from IIT Madras in Jan-Jun 2016 (old faculty page, AR 2015-16); NIRF: Visiting from 01-06-2022 |
| Deepu P | former | Listed Feb-Mar 2017 on turing.iitpkd.ac.in as Visiting Faculty, Mechanical Engineering; affiliation otherwise unknown. |
| Job Kurian | former | NIRF 2022: joined 01-06-2015, left 31-12-2020 (association type Other). Retired IIT Madras professor. |
| K P Krishnaraj | former | Faculty-list Dec 2021 - Jun 2022; DST INSPIRE grant listed in AR 2022-23 (start Nov 2021); absent Aug 2022 list. LAST uncertain. |
| Pramod S. Mehta | former | NIRF 2022: joined 19-10-2016, left 30-06-2021. |
| Sunil Kumar Arolla | former | AR 2016-17 (on contract) and AR 2017-18 faculty lists; last on faculty-list Jan 2018; absent Aug 2019. LAST uncertain (archive gap). |
| T. K. Krishna Kumar | former | Visiting faculty from Nov 2016 snapshot; last listed Jan 2018 (faculty-list). LAST uncertain (archive gap Jan 2018 - Aug 2019). |
| Bibhu Ranjan Sarangi | current | second unit: Biological Sciences and Engineering ; joining_year source: NIRF joining date 06-06-2019 |
| Manoj Gopalakrishnan | current | joining_year source: NIRF 2022-24: Professor (Other/Visiting) from 15-12-2021; profile: Professor IIT Palakkad from July 2026 (regular) |
| Moumita Nandi | current | joining_year source: NIRF joining date 24-12-2020 ; physics dept site lists her as former Inspire Faculty (2021-2026) while the institute faculty list still lists her |
| Uma Divakaran | current | joining_year 2016 from first institute listing (old faculty page); NIRF joining date 23-06-2017 |
| Akshay Bhatnagar | former | NIRF 2026: joined 17-04-2023, left 19-05-2025; physics former-faculty page says 2023-2024 (now IIT Roorkee). |
| Anil Kumar Dasanna | former | NIRF 2025: joined 19-05-2023, left 13-12-2023; physics former-faculty page (now IISER Mohali). |
| B. V. R. Tata | former | Listed Nov 2016 - Feb 2017. |
| M. C. Valsakumar | former | Retired IGCAR Outstanding Scientist; full-time visiting faculty 2015-16; Dean Students Affairs (AR 2016-17); last listed Jan 2018; deceased by May 2019 (memorial lecture, AR 2019-20). |
| Mayarani M | former | NIRF 2026: joined 02-01-2023, left 06-12-2024; physics former-faculty page says Inspire Faculty 2023-2025 (now Central University of Karnataka). LAST=2024 per NIRF. |
| P. B. Sunil Kumar | former | Professor-in-charge 2015 (then also IIT Madras faculty); Director from 18-01-2017 (NIRF); relieved 12-10-2022 (Annual Report 2022-23); physics dept former-faculty page: Professor 2015-2022, now IIT Madras. |
| S. Kasiviswanathan | former | IIT Madras professor; 2015-16 listed both as Professor-in-charge (Academics) and under "Visiting Faculty from IIT Madras"; AR 2016-17 lists him as Professor (Deputation from IITM); AR 2017-18 faculty list. Treated as former (held a deputation post) rather than mentor-visiting; ambiguous. |
| Seshadri Sridhar | former | NIRF: Professor (Other) joined 01-10-2022, left 30-09-2024 (2024 edition says 10-01-2022); listed on adjunct-faculty page Mar 2023 - Aug 2024. |
| R Venkataraghavan | former | Adjunct page Sep 2019 - Nov 2025; NIRF 2026: Adhoc/Contractual joined 01-01-2023, still working at data date; absent from current adjunct page (Oct 2026). joining_year = NIRF contract start; listed as adjunct since 2019. |
| Ravi N. Banavar | former | Adjunct page Nov 2020 - Aug 2024; department not printed on the list. |


## Post-review edit (main session, 2026-10-26)
* Cleared 7 e-mail values that were a department office address (office_mm@) or another person's address (vivek@ on honorary professors' rows); each address is now kept only for its owner.
