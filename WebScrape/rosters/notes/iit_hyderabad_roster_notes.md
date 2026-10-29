# IIT Hyderabad (iit_hyderabad) faculty roster, 2016-2026: lab notebook

Output: `rosters/iit_hyderabad_faculty.csv` (558 rows). Built in two sessions (the first agent was interrupted by a usage limit after saving all fetched pages and parsers; the second reused them and finished the build, no re-fetching was needed). IIIT Hyderabad is a different institute; nobody is included as IITH faculty on the basis of IIIT-H membership (see "Ambiguous people" for the one IIIT-H person that IITH itself lists as adjunct).

## Totals

| status | rows |
|---|---|
| current | 358 |
| adjunct (adjunct / honorary / distinguished / chair / professor of practice / advisor) | 153 |
| emeritus | 2 |
| visiting | 19 |
| former | 26 |
| total | 558 |

Per-unit counts (current / adjunct / emeritus+visiting / former); department = primary unit of the institute's current card, or the last archived listing for non-current people:

| unit | cur | adj | vis/em | former |
|---|---|---|---|---|
| Mechanical & Aerospace Engineering (was "Mechanical Engineering" in 2016-17) | 40 | 5 | 1 | 2 |
| Electrical Engineering | 39 | 13 | 1 | 1 |
| Physics | 33 | 9 | 0 | 1 |
| Computer Science & Engineering | 31 | 5 | 0 | 5 |
| Civil Engineering | 31 | 10 | 2 | 3 |
| Chemistry | 30 | 5 | 0 | 1 |
| Chemical Engineering | 25 | 3 | 0 | 3 |
| Mathematics | 23 | 0 | 1 | 2 |
| Materials Science and Metallurgical Engineering | 23 | 12 | 0 | 1 |
| Liberal Arts | 21 | 24 | 2 | 1 |
| BioTechnology (spelled "Biotechnology" in 2016-17) | 17 | 3 | 0 | 2 |
| Design | 14 | 8 | 0 | 0 |
| Biomedical Engineering | 13 | 8 | 1 | 1 |
| Artificial Intelligence | 8 | 6 | 1 | 2 |
| Entrepreneurship and Management | 6 | 1 | 0 | 0 |
| Climate Change | 3 | 5 | 0 | 0 |
| Heritage Science & Technology (new unit, adjuncts only on the list) | 0 | 19 | 0 | 0 |
| Cyber Security tag (code CS) | 0 | see below | | |
| department blank | 0 | 15 | 12 | 1 |

(Rows add to 558; "Cyber Security" counts are folded into the blank-department row because code `CS` is not decoded, see problems.) Second units (Engineering Science, Climate Change, Artificial Intelligence as secondary) are recorded on the institute cards (about 30 people carry a second or third unit); the CSV keeps the first-listed unit, as the brief asks for one row per person. Engineering Science (ES) exists as a unit (it has a Head) but nobody has it as primary unit on the current cards; in the 2016-17 pages ES lists repeat people already listed under their home department, so ES was never taken as primary.

## Sources and endpoints

1. Current list: `https://iith.ac.in/people/faculty/` (one page, 462 cards in nine sections: regular, visit-faculty, adjunct, dist-faculty, em-faculty, hn-faculty, advisors, chair-professor, professor-practice; fetched 2026-10-27). 358 cards in the "regular" section, 104 in the others. Each card was followed to its profile page (`https://iith.ac.in/<dept>/<slug>/`, 392 pages saved) for position, unit list, e-mail, homepage link. Names, designations, unit, institute e-mail and homepage come only from these pages.
2. NIRF data submissions, "Overall" PDFs from `https://iith.ac.in/assets/files/NIRF-Reports/` for NIRF 2019 to 2026 (Faculty Details table: name, designation, joining date, leaving date, currently-working flag, association type). Rows parsed: 205, 222, 242, 236, 291, 306, 321, 330 (2019 to 2026); every dated line of the text extraction was captured (row count equals the count of table lines). Working=Yes rows: 190, 203, 221, 232, 288, 306, 318, 330; Working=No rows: 15, 19, 21, 4, 3, 0, 3, 0. Only 3 NIRF rows are non-Regular (Visiting).
3. Wayback snapshots of the faculty list (CDX listings saved under data/cdx_*.txt): 2016-2017 Joomla pages `iith.ac.in/community/faculty_hyd.html` (2016-03-01, 2016-07-30, 2016-12-18) and `iith.ac.in/index.php/iith-people/peple-faculty?id=63+` (2017-03-19, 2017-06-09, 2017-10-07), the honorary page `community/faculty_hon.html` (2016-12-15) and `...?id=75` (2017-03-19); 2020-2026 pages `iith.ac.in/people/faculty/` at 14 dates (2020-04-10, 2021-01-17, 2021-12-07, 2022-02-26, 2022-11-27, 2023-06-07, 2023-12-03, 2024-06-13, 2024-12-10, 2025-06-12, 2025-12-01, 2026-08-11). Roughly two per year in 2016-2017 and 2022 onwards, one per year otherwise. Snapshot sizes (unique names): 2016-03 174, 2016-07 176, 2016-12 180, 2017-03 189, 2017-06 192, 2017-10 195 (+13 visiting, +1 chair); 2020-04 221, 2021-01 251, 2021-12 272, 2022-02 288, 2022-11 344, 2023-06 366, 2023-12 373, 2024-06 388, 2024-12 412, 2025-06 420, 2025-12 419, 2026-08 446. Pages were demonstrably maintained (member counts grow in every snapshot), so they count as presence evidence, except where NIRF gives an earlier documented leaving date (below).
4. Annual reports 2015-16 to 2018-19 and 2021-22 to 2024-25 (text extracted into data/ar/): used for the faculty-strength size check and for spot checks of 2018-19 presence (publication lists). They do not carry "joined/left" lists, so they were not used to set tenure years.
5. ORCID: the offline affiliation index `work/orcid_index/iit_hyderabad_orcid_index.tsv` (3,181 records). No live ORCID API calls were made.
Not used: IRINS, Scopus, OpenAlex, Google Scholar.

## How tenure and status were established

* Entity resolution: all names (current cards, every snapshot row, every NIRF row) were normalised (titles and punctuation dropped, token sets compared, then a conservative fuzzy match) and merged into one entity per person; 600 raw entities were reduced by 36 manual merges for spelling/initial variants (for example "K Venkata Subbaiah" = "Venkatasubbaiah K.", "S Kalyanasundaram" = "Subrahmanyam Kalyanasundaram", "Sakethanath Jagarlapudi" = "J. Saketha Nath"). Pairs that a fuzzy rule wrongly merged were blocked (e.g. Ashish Misra / Ashish Mishra, Saurabh Kumar / Saurabh Kumar Singh and "Shiva Kumar" (HST adjunct) / "K Siva Kumar" (EE) are different people and stay separate).
* Status: anyone on the live list is current (regular section), adjunct (adjunct, honorary, distinguished, chair, professor of practice, advisor sections), emeritus or visiting according to the section and designation. Institute-wide list wins over department pages (there were no conflicts, the unit pages are the cards' own profile pages).
* Former: not on the live list but on an archived list or in NIRF in 2016-2026. Regular faculty (designation Assistant/Associate Professor or NIRF "Regular") who left are `former`; people listed as visiting/adjunct/honorary/emeritus keep that type and get the range as well.
* Last year: NIRF leaving date year when the NIRF row has Working=No (19 former people); otherwise the last archived list that lists them (a NIRF row in year Y counts as presence in Y-1, because NIRF Y is submitted in the autumn of Y-1). Where a later snapshot still lists a person after the NIRF leaving date, the snapshot is treated as stale and ignored: Sharada D. S. (left 21-03-2022, listed until 2024), Sandeep Kumar Singh (left 28-10-2018, listed until 2020), Samir Kumar Biswas (left 2016, listed 2017), Uday B. Desai and Naveen Sivadasan (regular tenure ended 2019 and 2015 respectively).
* First year / joining_year: earliest NIRF joining date (earliest across all submissions) for NIRF-listed regular faculty (357 rows have a joining year, all of them from NIRF); if an archived list shows the person earlier than the NIRF joining date the earlier listing year is used (one case: G. Narahari Sastry, NIRF 2024, listed 2022 as Director). For people not in NIRF (adjuncts, visiting, 2 non-NIRF former regulars) `joining_year` is blank and the FIRST year in the designation is the first year on an archived list ("first appearance on archived faculty list"). NIRF dates may be rejoining or regularisation dates for a few people; none could be checked against an earlier appointment record.
* Window: persons whose only evidence ends before 2016-01-01 were dropped (8 persons, all NIRF 2019 rows with leaving dates 2010-2015 and no later listing, e.g. Apoorva Nagar, Bhaskar Kumar, Priti Kahar). Two people with a pre-2016 NIRF leaving date but a later archived role were kept as that later role (e.g. Naveen Sivadasan, adjunct 2023-2025, regular 2010-2015, range 2010-2025; Prabhakar Akella, visiting, last listed 2016).

## Identifiers

| field | count | route |
|---|---|---|
| email | 358 | institute profile pages (current people only) |
| homepage | 207 | institute profile pages (link in the card's "Homepage" block) |
| profile_url | 397 | institute card links |
| joining_year | 357 | NIRF |
| orcid | 228 | ORCID affiliation record (offline index) = 228; ORCID name search (live API) = 0; institute page = 0 |
| google_scholar, dblp, scopus_id, irins | 0 | institute pages do not show them |

ORCID acceptance rule: index record of kind employments/invited-positions at this IIT, name equal (token set) or token-subset with two shared tokens, role not student/scholar/postdoc/fellow-type, and department compatible when both sides state one (subset-only name matches additionally needed both departments). Two people had two qualifying iDs and were left blank: Ramji M (0000-0002-8909-9224 / 0000-0002-8937-2083), Shubhadeep Bhattacharjee (0000-0002-5813-033X / 0009-0005-2517-2719). ORCID lookup pending (not attempted, live API deliberately unused to save the shared quota): all other people without an ORCID (330 rows).

## Independent size check

* NIRF 2026 (submitted autumn 2025) lists 330 working faculty (all Regular except none Visiting); NIRF 2025 318; the Annual Report 2024-25 states "As on 31 March 2025, IITH is having 325 faculty members on-roll".
* The live site (Oct 2026) has 358 cards in the regular section and the roster has 358 current rows (two different people named Neeraj Kumar, Mathematics and Liberal Arts, each have a row). This exceeds NIRF 2026 (330) by 28: 330 of 358 current rows are NIRF-2026-confirmed, and the 28 not in NIRF 2026 are people who joined after that submission (autumn 2025) or are not on NIRF's regular table (no joining year, blank in the CSV). The growth 325 (Mar 2025) to 358 (Oct 2026) is consistent with the 2022 onwards hiring pace (NIRF 2022 232 to NIRF 2026 330, about +25 per year).

## Problems and how they were resolved

* The 2018-2019 Wayback captures of the faculty page (`index.php/faculty/`, `about/people/?subpage=faculty`) contain no faculty list (list is loaded dynamically), so there is no archived list between 2017-10-07 and 2020-04-10. People who left in that gap are found only through NIRF 2019/2020 leaving dates (Prashant Saxena 2018, Sandeep Kumar Singh 2018, Arun Mascarenhas 2018, Swati Gupta 2019, Abhay Sharma 2019, Sparsh Mittal 2019). Anyone who joined and left inside the gap without a NIRF row is missed (unknown number, probably few).
* The 2016-12-15 Wayback capture of `community/faculty_adj.html` was never saved; the honorary page (3 people) and the 2017 `id=75` page were used instead.
* Joomla pages of 2016-17 list visiting and honorary people under "IIT Hyderabad Visiting Faculty" / "Honorary Faculty" h1 headings; an early parser attached them to the last department (Physics). Section headings are now parsed, so they are `visiting` / `adjunct` with unit blank.
* The 2026-08 snapshot cards carry no designation text; designation and type were inherited from the same person's earlier snapshot. Persons listed in that snapshot but gone from the live page by 27 Oct 2026 (Ravi Balasubramanian, Seeram Ramakrishna, Vasudevanpillai Biju, Raja Sengupta, Seiji Mitani) are not current; they are adjuncts with range ending 2026.
* For snapshots 2020-2025, persons with a plain "Professor" or a chair title and no NIRF row were classified `adjunct` (inferred; those pages are the adjunct section, e.g. Tarun Kant, Rao Surampalli, Nixon Patel). Persons titled Assistant/Associate Professor with no NIRF row (Mrinal Srivastava 2021, Piyush Vijay Jagtap 2022-23) were kept as `former`; whether they were regular, contractual or ad hoc is not shown by any source.
* Unit codes on cards changed between 2020 and 2021; two code maps (2020 and 2021+) were used for archived units. Code `CS` (Mahesh K. Marina, Ponnurangam Kumaraguru, both adjunct) is not decoded and left blank; codes `high`, `5g`, `operating` (parsed research keywords) are ignored (department blank for 15 adjuncts and 12 visiting people, 2 of them former).
* Rename mapping: "Department of Mechanical Engineering" (2016-17) = Mechanical & Aerospace Engineering; "Computer Science and Engineering" = Computer Science & Engineering; "Biotechnology" = BioTechnology; "Computer Science & Electrical Engineering" (honorary P R Kumar) = Electrical Engineering (unit used for the honorary page; not a real department).

## Ambiguous people and decisions

* Neeraj Kumar: two current cards with the same name (Liberal Arts, Assistant Professor, joined 2020-12-21; Mathematics, Associate Professor, joined 2019-01-21), two rows; NIRF rows were attributed by designation/date, ORCIDs by department (0000-0003-0254-7934 LA, 0000-0002-1144-2096 Math).
* Pritha Bhattacharya (NIRF 2020-2026, Associate Professor, joined 2018-12-10) merged with the current card "Pritha Chatterjee" (Associate Professor, Civil Engineering). Same designation/year; surname change assumed, not documented. If wrong, a separate NIRF-only person exists.
* Ashok K (NIRF) = Ashok Kamaraj (MSME), Sivakumar V = Sivakumar Vaidyanathan (Chemistry), Suresh P = Suresh Perumal (MSME), Gabbita Durga JanakiRam = Janaki Ram G. D, M Narasimha = Narasimha Mangadoddy, "V Ganapathi Narasimha Cheraku" = "Venkata Ganapathi Narasimha Kumar Ch": NIRF-only spellings matched to current cards by initials and joining years (single candidate each).
* Ponnurangam Kumaraguru (IIIT Hyderabad) appears on IITH's own adjunct list; kept as `adjunct` because the institute lists him, and no IIIT-H affiliation is used for any other row.
* Prof. A. G. Tsutsumi (adjunct 2025) vs Dr. Osamu Tsutsumi (current adjunct): left as two people.
* Honorary pages 2016-17: P R Kumar and V Umapathi Reddy are honorary; V. K. Saraswat (DAE Homi Bhabha Chair) is the current adjunct card "Saraswat V K".
* Aravind Reddy Talla, Ramana Vinjamuri, Kathryn Hummel, Johan Ninan, Prabhakar Akella appear as visiting assistant professors; Chandrasekharam D. as visiting professor.
* Uday B. Desai (current "Emeritus Professor"; NIRF leaving 2019) and Vinayak Eswaran (Emeritus, NIRF leaving 2024): status emeritus; joining year from NIRF.

## Known gaps

* No archived faculty list for 2018-2019 (see above); last years of former people who left in 2017-2018 rest on NIRF leaving dates only, and the two regular former people without a NIRF row (Mrinal Srivastava, Piyush Vijay Jagtap) have single-snapshot ranges.
* Visiting/adjunct people before 2020 were only available through the 2016-17 honorary and visiting pages; the adjunct list of 2017-2019 is not archived.
* Department is blank for 28 adjunct/visiting/former rows (chairs and archived visiting people with no unit code).
* Google Scholar, DBLP, Scopus and IRINS ids are empty by design. 330 people have no ORCID (live lookup not attempted).
* Joining years for adjunct and visiting people are blank (not in NIRF).
