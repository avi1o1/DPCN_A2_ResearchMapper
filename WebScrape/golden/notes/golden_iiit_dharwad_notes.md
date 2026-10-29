# IIIT Dharwad golden set: lab notebook (October 2026, operator Arihant Tripathy)

Output: golden/golden_iiit_dharwad.csv (80 rows, below the 150 target; sources exhausted, see below). Built without Crossref/OpenAlex/S2/EuropePMC/DOAJ/ORCID/DBLP/Scholar/Scopus/IRINS/DataCite/arXiv API. All fetches through agents/polite_get.py; work dir C:\Users\Arihant\rm_work\iiit_dharwad_golden (code: build.py, crawl.py, txt.py). Annual-report text and faculty-list pages were reused from the roster agent's cache (rm_work/iiit_dharwad_roster/data, institute documents). Did not read iiit_dharwad.json.

## Sources, counts
| Source | Visited | Candidates | Rows kept |
|---|---|---|---|
| Annual reports 2015-17, 2017-18, 2018-19, 2019-20, 2020-21, 2021-22 (Wayback copies of assets.iiitdwd.ac.in PDFs, pdftotext; the live asset host does not resolve) | 6 | ~330 list entries | 38 |
| Faculty personal sites (Google Sites, github.io, wix, vercel; from roster `homepage`, home page plus publication/research subpages found by link pattern) | 31 homepages, ~75 pages | ~250 entries, most dated before the person's joining year | 25 |
| arXiv abs/PDF pages (found by web search restricted to arxiv.org; PDF first page read for affiliation) | 22 | 22 | 17 |
| iiitdwd.ac.in /academics/departments/ | 1 | descriptive only | 0 |
| iiitdwd.ac.in /academics/research/, /announcements/ | 2 | dead (ConnectionError) | 0 |
| AR 2022-23, 2023-24 (assets.iiitdwd.ac.in, iiitdwd.ac.in/docs) | 2 | dead; roster agent found no Wayback copy; AR 2024-25 archive is truncated | 0 |

Search strings (web search tool, standard mode): `"Indian Institute of Information Technology Dharwad" arxiv` (arxiv.org); `"IIIT Dharwad" arxiv paper Department of Data Science and Artificial Intelligence`; `"IIIT Dharwad" "iiitdwd.ac.in" arxiv.org abs 2022 OR ... language model OR deep learning OR network`; `"Indian Institute of Information Technology Dharwad" Deepak K T OR "Jagadish D N" OR "Sunil Saumya" OR "Kavi Mahesh" OR "Rajendra Hegadi" arxiv`; `IIIT Dharwad faculty research paper published news` (no news coverage found; only institute documents). arXiv never answered 403. Search hits that are IIT Dharwad (different institute: 2310.02590, 2504.00417, 2509.08424) were rejected. arXiv 2302.13209, 2412.03023, 2508.17083, 2607.16765 fetches did not complete or were not read (not included). 2610.* arXiv ids are dated Oct 2026 in the PDFs.

Source mix achieved: annual_report 38 (47 %), faculty_page 25 (31 %), arxiv 17 (21 %), dept_page 0, news 0. Deviations: no department/lab page or institute news lists papers; that share went to annual reports and arXiv. No external news coverage found.

## Rules applied
* Confidence: high = 17 arXiv rows (affiliation printed in PDF); everything else medium (list on report or own page + tenure rule).
* Tenure: joining year from own page (Malay Kumar Aug 2019, Prasanna May 2024), NIRF via roster, or AR 2017-18 footnote ("joined July 2018": Satija, Akki, Rangisetti, Bhattacharjee). A paper counts only if year > joining year. Faculty with no joining year but listed in AR 2015-17 (Chauhan, Mahto, Goldina Ghosh, Basavarajappa as Registrar from 2016): evidence year 2017, papers 2018+ ("tenure: on-page evidence" in notes). The AR 2015-17 evidence for these people is the report listing, an upper bound.
* Cap 8 per first-named IIIT author: max is Hegadi 7, Basavarajappa 6 (checked by eye).
* Sampling: lists are short, and most entries fail the tenure rule, so almost every eligible entry was taken rather than a spread; spreading would add nothing.
* DOIs only where printed in the report/page (27/80 = 34 %). arXiv rows have no DOI (none printed).
* Department = institute unit name; Hegadi and Kavi Mahesh given as DSAI (current), Basavarajappa/Mahto as Arts, Science, and Design (= older Humanities/Applied Sciences label). Rows with two units list both; two student-led arXiv papers have no unit printed.

## Rejected candidates
* AR 2015-17 list (mostly 2015-2016 papers, plus 2017 items by Semwal, Behera, Deepak K T): year not after evidence/joining year (Semwal, Behera, Deepak, Jagadish 2016 items); Chauhan/Goldina Ghosh 2016 items. Zero rows from AR 2015-17 except 2017 Basavarajappa (Registrar from 2016).
* Joining-year exclusions: Satija 2018 items (joined 2018), Rangisetti JNCA 2018, Akki IJACSA 2018, Neha Bharill 2018 items (evidence 2018 only), Behera 2018 IoTsm, Ram Narayan Yadav (first evidence AR 2018-19), Prabhu Prasad 2018-2020 pages (joined 2021), Yelmewad lists to 2021 (joined 2022), Siddharth, Sunil Kumar P V, Suvadip Hazra, Abdul Wahid lists (all before joining 2024; Wahid's 2024 papers are in the joining year and written at Galway), Manjusha/Khaire/Prabhu 2021 items (joining year), Prasanna 2024 items (joining year 2024).
* Akansha Singh page identifies her as at Manipal; Rahul Jetti and Jagabandhu Mishra have no joining year and no on-page evidence; Phalke page has no dated IIIT evidence; LinkedIn/Google-Doc homepages not fetched. Adjunct sites (Sathiaseelan, Cohen, Vasa, Kulkarni) 404/dead or non-IIIT lists.
* Basavarajappa papers whose authors are non-IIIT students are listed under him as the institute author only.

## Coverage (rows)
Years: 2016 0, 2017 3, 2018 6, 2019 4, 2020 16, 2021 7, 2022 10, 2023 6, 2024 4, 2025 16, 2026 8.
Departments (incl. split rows): CSE 29, DSAI 24, ECE 14, Arts Science and Design 11, none printed 2. Former faculty covered: Basavarajappa, Mahto, Goldina Ghosh, Chauhan, Satija, Akki, Rangisetti, Kavi Mahesh; non-faculty-led (student) papers: 7 arXiv rows.

## Known biases
* 2016 empty and 2017-2019 thin: AR 2015-17 predates tenure evidence for most authors; the institute started in 2015 with few faculty.
* 2020 and 2025-2026 heavy: ARs 2019-21 are the only lists and recent joiners' pages list recent work.
* No ARs after 2021-22 (not archived), so 2022-2024 rest on personal sites and arXiv only.
* Mechanical/materials (Basavarajappa) and signal-processing groups are well covered by reports; most CSE faculty without public lists (Google Sites with JS-hidden tabs, LinkedIn-only people) are under-represented.
* arXiv rows over-represent student-led AI papers from 2024-2026 (Narkedimilli group, Aswath Babu quantum/astro, Saumya NLP).
* Almost all rows medium confidence: precision depends on joining years, which for some are upper bounds from archived lists.
* Year for report rows follows the printed year, which can be the acceptance/online year (e.g. JAIHC 2022 with a 2021 DOI).
