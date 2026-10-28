# IIT Delhi golden set - lab notebook

Final: 213 papers (target 650 NOT reached), 41 with a printed DOI (19%). Built over two sessions (first agent hit a usage limit; this session assembled its saved work and added arXiv/news).

## Sources and yield
| source | pages/PDFs visited | rows | notes |
|---|---|---|---|
| faculty_page (own profile / homepage lists) | Mech, Chemistry, Textile dept profile pages (about 114 profiles parsed; only those with a usable joining year and list), 13 personal homepages (EE, DESE, AM, Maths, ChE, CARE), MSE faculty API | 171 | spread-sampled (evenly through newest-first lists), cap 8 per person |
| dept_page | physics.iitd.ac.in publications table (3 faculty, supervisor column) | 21 | affiliation not on table, medium |
| arxiv | 48 abs/PDF pages reached from institute/web links; first-page PDF text checked with pdftotext | 16 kept | kept only if IIT Delhi visible on page 1 of the PDF; year = arXiv id year (first version) |
| news | home.iitd.ac.in research-news items show.php?id=65..87 (23 pages) | 5 kept | institute states IIT Delhi researchers authored the paper; DOI from the article link. 9 further items had a DOI link but the publisher landing page returned HTTP 403 (Wiley/ACS/AGU), titles not obtainable without a lookup, so not included; ~8 items (Hindi mirrors, no paper link) skipped |
| annual_report | rti.iitd.ac.in annual report PDFs (AR-2024-25, AR-2021-22) | 0 | host fails with SSL error through the polite fetcher; Wayback copy of AR-2024-25 404, of AR-2021-22 returned an HTML wrapper, not the PDF. Not bypassed. |

Search strings used: site-restricted web search for the annual report; one web search to check a perovskite news item (not used for discovery of rows). Discovery otherwise by crawling institute pages.

## Tenure rule
Joining year taken from the person's own page (quoted in each row's notes) or, for Chemistry/Mech/Textile, from the dept profile page text (first IIT Delhi appointment year), manual overrides for a few profiles whose text states it differently. Roster has almost no joining years so it was not used. Only papers with year strictly after joining year are included (medium). arXiv and news rows are high (affiliation visible). Known upper-bound: none via archive snapshots were needed.

## Coverage (department x year)
| department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mechanical Engineering | 19 | 11 | 1 | 2 | 4 | 2 | 3 | 3 | 2 | 3 | 1 | 51 |
| Chemistry | 2 | 1 | 2 | 4 | 7 | 10 | 3 | 1 | 3 | 3 | 0 | 36 |
| Textile and Fibre Engineering | 8 | 3 | 4 | 1 | 5 | 2 | 3 | 3 | 0 | 0 | 0 | 29 |
| Physics | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 4 | 3 | 1 | 2 | 25 |
| Electrical Engineering | 1 | 1 | 2 | 2 | 2 | 1 | 5 | 1 | 3 | 4 | 0 | 22 |
| Materials Science and Engineering | 0 | 0 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| Mathematics | 1 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 2 | 8 |
| Chemical Engineering | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 8 |
| Energy Science and Engineering | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 2 | 0 | 2 | 0 | 7 |
| unspecified (IIT Delhi) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 4 | 0 | 7 |
| Centre for Applied Research in Electronics | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 4 |
| Applied Mechanics | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 3 |
| School of Artificial Intelligence | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| Computer Science and Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| Centre for Biomedical Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| Civil Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

## Rejected / skipped
* arXiv candidates without IIT Delhi on PDF page 1 (about 11 of 27 with cached PDFs) - rejected as affiliation not visible; 2 had no cached PDF.
* Faculty lists with no stated joining year (about half of the Mech/Textile/Chemistry profiles) - excluded, not guessed.
* homecse.iitd.ac.in team pages (60 CSE faculty) hold no publication lists; CSE/SAI personal pages parsed noisily (news/teaching lines) and were not included beyond arXiv.
* Departments with no papers: Civil (1 news row only), Biological Sciences, Design, Management, HSS, Public Policy, CBME (1 news), CSE (1), most of SAI: personal-page extraction not completed.

## Biases
Heavy over-representation of Mechanical, Chemistry, Textile, Physics (template-style profile pages parse cleanly); CSE/AI, Civil, Management, Design, Bio under-represented. Only papers that appear on faculty pages with a stated joining year; papers by students/former faculty almost absent. arXiv/news rows skew to 2022-2026 and to groups who post preprints / get press releases. DOI coverage low because faculty lists seldom print DOIs (no lookups done). Year 2026 is partial.
