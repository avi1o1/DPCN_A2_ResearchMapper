# IIIT Kottayam golden set: lab notebook

Operator: Arihant Tripathy (IIIT team). Run date 2026-10-30. Output golden/golden_iiit_kottayam.csv (145 rows). Work data: C:/Users/Arihant/rm_work/iiit_kottayam_golden/data/, code in .../code/.

## Sources and yield (found / used)
* Faculty profile pages (iiitkottayam.ac.in/#!faculty/KEY, views/faculty/KEY.html), reused from the roster agent's cache: 119 pages, 112 matched to roster rows with a Publications section, 2412 list items parsed; 94 rows used (includes 6 from Shajulin Benedict's homepage www.sbenedictglobal.com).
* Institute page views/studentPublication.html (B.Tech students' papers): 25 entries, 16 used. Lab pages: netsci publications.php (7 used), cedm publications.php (7 used), i2cs /publications (101 entries, 6 used). dsrg says "will be updated soon"; iotcloud 404; dabd SSL error; cyberlabs, bigml, biomirg, iiotrg, create, factsh, qudaislab, swing have no usable list. dept_page rows: 36.
* Annual reports (cached PDFs): only AR 2016-17, 2017-18, 2018-19 keep author names in extractable text; ARs 2019-20 to 2024-25 lost author names (non-ASCII font), so papers cannot be attributed to people. 8 rows used. The AR share (target 15%) was moved to faculty/department pages as the brief allows.
* arXiv (abs/PDF only, found via web search and institute pages): 10 PDFs read, 6 kept (affiliation read in the PDF, confidence high). Rejected: 2107.11844 and 2108.12610 (Susheel K. Joshi, 2021, no IIIT Kottayam in PDF, before 2022 joining), 2204.10195 (IIITDWD), 1607.05817 (Renjith, 2016, no Kottayam affiliation). arXiv never answered 403.
* News: institute news.ctrl.js has 210 items, one paper-level (Bini A. A., IET IPR; DOI from its link; IET page is Cloudflare-blocked, not bypassed); media.ctrl.js 96 clips are not paper-level. News share (target 10%) therefore 1 row; moved to faculty/lab pages.
* Publisher pages opened for affiliation checks (Springer): s00607-016-0534-5, s40815-016-0245-2, s11760-016-1047-6 (no Kottayam, so these 2016-17 papers were rejected), s10586-017-1657-y (Kottayam visible, kept as high). Inderscience, Elsevier and IET were bot-walled or redirected; skipped.
* Web search strings: "Indian Institute of Information Technology Kottayam" 2016 paper Trivandrum affiliation arxiv; arxiv.org "IIIT Kottayam" 2017 abstract; arxiv "Indian Institute of Information Technology Kottayam" 2022 OR 2023 federated learning...; arxiv.org "IIIT Kottayam" blockchain OR cryptography OR quantum OR graph; arxiv.org "Department of" "IIIT Kottayam, Kerala, India" 2021 OR 2020 OR 2019 preprint; arxiv Manu Madhavan Selvi C IIIT-Kottayam Kathakali...; arxiv Shajulin Benedict IIIT Kottayam IoT cloud; arxiv Jayakrushna Sahoo OR "Ebin Deni Raj" OR "Divya Sindhu Lekha" IIIT Kottayam; two exact-title searches for 2017 Springer papers.

## Result
145 papers, 65 first-named IIIT Kottayam authors (cap of 8 never binding after dedupe). Confidence: high 7, medium 138. DOI printed on source for about 30%.

Departments x years (department = Annual Report 2023-24 grouping from the roster; "Not published" = people the roster could not place, e.g. post-2023 joiners, former faculty, students; no unit guessed):

| Unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Computational Science and Humanities | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 1 | 1 | 1 |
| Computer Science and Engineering | 0 | 0 | 2 | 2 | 6 | 5 | 11 | 13 | 12 | 13 | 3 |
| Cyber Security | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 4 | 3 | 6 | 1 |
| Electronics and Communication Engineering | 0 | 0 | 0 | 1 | 0 | 2 | 1 | 1 | 6 | 6 | 1 |
| Not published | 0 | 0 | 4 | 7 | 4 | 6 | 5 | 1 | 3 | 4 | 3 |

## Rejected / not used
* All 2016 and 2017 papers: tenure rule needs year strictly after joining and earliest faculty have first dated presence 2016-2017; publisher pages checked did not show IIIT Kottayam. 2016 and 2017 are NOT covered (a real gap; the institute started in Aug 2015).
* People without a joining year (e.g. Balu, Alkha Mohan, Gayathri G R, Nayana P G, most former faculty) excluded for lack of on-page evidence; Kumaresan G (Dec 2024) and Bini A. A. (Aug 2017) entered with on-page dates.
* Papers dated at or before joining year (e.g. Bibal Benifa 2018, Sivaiah 2018, Lekha 2019-2020 Physica A, Manikandan and Jaise Jose 2017).
* Non-paper items on profile pages (workshops, roles, talks, reviewing) filtered by regex and by hand; one talk, one "under review" item and one in-press chapter dropped; duplicate titles removed.
* No homonym/template bug seen on netsci/cedm/i2cs pages.

## Biases
* Faculty-page sampling skews to 2023-2026 because most faculty joined 2022 or later; 2018-2022 comes mainly from the student page, ARs and labs.
* Mostly medium (tenure rule); affiliation verified on the paper for 7 rows only. Entries chosen evenly within each list, but profile lists are self-reported.
* Venue strings for APA-style profile entries were auto-extracted and may carry trailing remarks; titles checked by eye.
* DOI only as printed on the source.
