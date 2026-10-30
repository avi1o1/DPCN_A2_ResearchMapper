# Golden set notebook: IIIT Una (iiit_una)

Operator: Arihant Tripathy (IIIT team). Output: golden/golden_iiit_una.csv (100 rows). Built 2026-10-30.

## Sources and yield
| source | pages visited | candidates seen | rows used |
|---|---|---|---|
| Faculty profiles (own institute site, JSON API `api.iiitu.ac.in/api/faculty/<id>`, 47 current-faculty profiles fetched, 234 listed items incl. 5 patents) | 47 | 234 | 54 |
| Institute reports (Convocation / Annual Progress Report PDFs on cdn.iiitu.ac.in: First 2019, Second 2019, Third 2020, Fourth 2021 / Institute-Report (counts only, no lists), IR 2023-24) | 6 | ~230 listed items | 43 |
| Institute news (api.iiitu.ac.in/api/news, 191 items; 7 research items) | 1 listing | 5 papers (1 DOI-only, Wiley bot wall) | 3 |
| arXiv / general web search | 4 searches, 3 arXiv abs pages | 0 verified IIIT Una papers | 0 |
| Department / lab pages | none exist as publication lists (school pages have description/mission only) | 0 | 0 |

Search strings used (WebSearch): `arxiv "Indian Institute of Information Technology Una" Himachal Pradesh` (arxiv.org only); `IIIT Una annual report publications faculty journal papers list`; `"IIIT Una" OR "Indian Institute of Information Technology Una" paper arXiv abstract authors ...`; `arxiv.org "IIIT Una" Narottam Chand OR "Mrityunjay Singh" ...`; `"Indian Institute of Information Technology Una" arxiv.org abs preprint`; `"IIIT Una" 2017 OR 2018 faculty paper ... Narottam Chand IEEE`. None surfaced an IIIT Una arXiv paper. arXiv abs pages read: 2607.09716 (authors Sharma/Dhar, no Una affiliation shown), 1911.05819 (Verma/Kumar, no affiliation; appears on a faculty list but not verifiable, not used). Wiley DOI page 10.1002/cpe.70412 (Manish Gaur, news item) returned a Cloudflare challenge: not bypassed, paper skipped (no title available).

## Deviations from the requested source mix
Requested: faculty 50 / dept 15 / annual report 15 / arXiv 10 / news 10. Actual: faculty_page 54, annual_report 43, news 3. No dept/lab publication pages exist and no arXiv paper with visible IIIT Una affiliation was found by web search, so those shares went to the institute reports (the only source covering 2018-2020) and faculty profiles. Only 1 row is `high` (explicit IIIT Una affiliation in institute news); everything else is `medium` because no per-paper affiliation was visible (publisher pages not fetched; reports and faculty lists are not affiliation evidence).

## Tenure handling
Joining years from `rosters/iiit_una_faculty.csv` (own page Experience field where present, else NIRF / first archived snapshot: upper bound). Faculty-profile items kept only if year > joining year and >= 2016 (joining-year papers dropped because affiliation is not visible). 234 profile items -> 79 strict-tenure candidates. Report items: accepted when the author has a roster joining year < paper year, otherwise `tenure: on-page evidence` (author named as faculty/"Achievements of Faculty Members" in a dated institute report) as per the no-joining-year rule. Per-person cap 8 applied (largest: Dr. Jaspreet Kaur 7, Dr. Tanu Wadhera 7, Dr. Gurpreet Kaur 6, Dr. Mrityunjay Singh 6).

## Rejected / excluded (examples)
- Profile items before joining year or in joining year (about 150, mostly pre-2022 work by faculty who joined 2022-23, e.g. Cheggoju 2014-2018 papers, Modi 2011-2021).
- Gurpreet Kaur 2018 papers (joining year 2018, no affiliation visible); Satendra Kumar PRD 2018; Divyansh Thakur 2018 papers; Hem Lata ACECE 2018 (joined 2019).
- Report items by authors not identifiable as faculty (Chandan Kumar/K. Rajawat TSP 2020, Sonam Maurya JNCA 2019, Ashna Jacob/N. Menon 2019-20, "Sharma V." Physics of Fluids 2023, student-only posters from the news item "Student Research Highlights", useR! 2026).
- Manish Gaur Concurrency and Computation (DOI 10.1002/cpe.70412): title unavailable (bot wall).
- 5 patents on faculty profiles (not publications). IRINS (iiitu.irins.org, linked as institute 'publications') not used.
- Report 2019-20 / 2020 conferences from 2018 with no further evidence beyond two Guleria and one Roopali items were kept as 2018 coverage (medium, on-page evidence only).

## Coverage (units x years)
| unit | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| School of Basic Sciences | 0 | 1 | 3 | 1 | 2 | 10 | 3 | 1 | 2 |
| School of Computing | 1 | 9 | 2 | 0 | 0 | 6 | 8 | 7 | 5 |
| School of Electronics | 2 | 2 | 4 | 1 | 0 | 11 | 3 | 10 | 5 |
| unknown (not in faculty roster) | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

Types: {'conference': 26, 'journal': 63, 'book-chapter': 9, 'book': 2}. DOI printed on source for 54 of 100 rows.

## Known biases
- Years 2016-2017 have no rows: no institute report or faculty page lists papers from the Hamirpur transit-campus period with visible tenure; 2018 (3), 2021 (2) and 2022 (2) are thin because most current faculty joined in 2022-2023 and joining-year papers were excluded, and no 2021-22 report lists papers (Fourth Convocation / Institute-Report give counts only).
- Heavy weight on 2023-2026 (current faculty profiles) and 2019-2020 (reports); former faculty are represented only via the reports (Selvakumar, Grewal, Katal, Garanayak, Guleria, Pandey, Roopali) because former-faculty profiles do not exist.
- Faculty who left before the portal was built, and non-faculty (student/postdoc) papers, are largely invisible; the report items with students as co-authors (e.g. Bhuvaneswari Amma, Elakkiya, Priya) enter only via the faculty supervisor.
- Only faculty who maintained the portal publications section appear (28 of 47 profiles had publications; 19 had none), favouring diligent self-reporters. DOIs come from the printed link on faculty entries, so DOI coverage is biased towards entries with DOI links.
- School of Computing / Electronics / Basic Sciences are the only academic units; one row (Sunil Sangwan) has unit unknown (management/humanities faculty not in roster).
- Work files: C:/Users/Arihant/rm_work/iiit_una_golden/ (data/, code/).
