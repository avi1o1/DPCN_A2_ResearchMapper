# Golden set IIIT Bhubaneswar: lab notebook

Result: 107 papers (target 150 not reached; sources exhausted, see below). Built 2026-10-29, operator Arihant Tripathy. All fetches via polite_get.py; no forbidden source and no pipeline output used.

## Sources used (found / visited / yield)
| source | visited | rows |
|---|---|---|
| iiit-bh.ac.in home, 5 department pages, research page, rd-cell, nirfs, print-digital-media-coverage | 10 | 0 (navigation, tenure only; research page lists "Publication page" links to the faculty pages) |
| faculty profile pages (50 links found in the faculty list and department pages; 49 fetched, 1 was /feed) | 49 | 92 (faculty_page); 21 pages have a "Publication" section, ~28 say "Coming Soon" or have none |
| 13 laboratory pages | 13 | 9 (only Information Security Lab has a publication list, ~19 entries) |
| NIRF 2026 Faculty PDF (DOJ for ~40 faculty) and NIRF 2025 Faculty PDF | 2 | tenure evidence only |
| Google Sites newsletter/achievements pages | 2 | 0 (JavaScript shells, no text without a browser) |
| arXiv abs pages + PDFs reached through web search | 14 abs / 12 PDFs | 6 (arxiv) |
| publisher landing pages reached from printed DOIs (Springer, PIER, doi.org) | ~28 | used to upgrade 11 rows to high (affiliation quoted in notes); MDPI, Hindawi, IEEE, Inderscience, T&F, Elsevier gave 403/202/no affiliation text |

Web-search strings (WebSearch tool): "IIIT Bhubaneswar annual report list of publications journal papers faculty"; "IIIT Bhubaneswar" arXiv Department of Computer Science International Institute of Information Technology Bhubaneswar; arxiv.org "International Institute of Information Technology Bhubaneswar" Odisha India abstract; arxiv "IIIT Bhubaneswar" Balabantaray OR Jena OR Vipsita OR Patra OR Sahu paper pdf; arxiv "IIIT-Bhubaneswar" iiit-bh.ac.in antenna OR blockchain OR "deep learning" OR "NLP"; IIIT Bhubaneswar researchers publish paper news faculty research highlights; "International Institute of Information Technology Bhubaneswar" department of mathematics OR "basic science" article ...; "IIIT Bhubaneswar" professor research paper published journal Odisha news 2024 OR 2025. Search returned mostly IIT Bhubaneswar / IIIT Bangalore material.

## Source-mix deviations (planned 50/15/15/10/10)
Actual: faculty pages 86 % (92), department/lab pages 8 % (9), arXiv 6 % (6), annual reports 0, news 0.
* Annual reports: IIIT Bhubaneswar publishes no annual report with publication lists that I could find (search only returned IIT Bhubaneswar reports); NIRF PDFs contain counts only. Share moved to faculty pages.
* News: no IIIT-BH research news items found (press-coverage page holds event clippings as JPEGs only). Share moved to faculty pages.
* Department pages carry no publication lists; the lab page share is the Information Security Lab only.

## Tenure rule
Joining dates come from the NIRF 2026 Faculty-NIRF PDF (DOJ column), which is the actual date of joining recorded for NIRF, not an archived-snapshot upper bound. Used DOJ: Balabantaray 2008, Giri/Bharati Mishra/Pradyut Biswal/Patra/Subrata Mohanty/Tushar Sahoo/Sunanda 2011, Jena/Padhi/Subudhi 2009-2011, Vipsita 2012, Surya Singh and Venkata Sridhar 2016-07-01, Sanjeev Mishra 2016-08-08, Deepak Rout 2022 (visiting). Papers need year > DOJ year, so 2016 papers of the 2016 joiners were excluded. Surya Singh's 2017-2019 papers are co-written with IIT Kanpur authors (M J Akhtar group) and may have been done partly there; kept as medium per rule.

## Confidence
high 17 (publisher page or arXiv PDF shows the affiliation); medium rest (faculty-page listing plus tenure). Affiliation seen quoted in `notes`.

## Rejected / skipped
* Arun Kumar Sahoo (DOJ 2022, listed papers all <= 2022, PhD at IIIT-BH but affiliation not visible): excluded.
* Bibekananda Panda (joined Jul 2025), Saswati Sinha (Apr 2024), Arpit Mohapatra (2023), Dasari Arun Kumar, Sourav Kundu, Satyajit Panigrahy etc.: no in-tenure publication list on page.
* Rows before the joining year, or dated 2015 and earlier (e.g. Balabantaray arXiv 1502.07938, 2015) excluded.
* Papers whose full title is split or truncated on the page (e.g. Pradyut Biswal 2022 BSPC epileptic seizure paper) were skipped. Sunanda rows reconstructed from two-line titles.
* arXiv candidates rejected on affiliation check: 2406.15794 (NISER), 2502.11736 (KIIT/IIIT Delhi), 2307.12072, 1808.03299, 2501.00029, 1803.09402, 2206.01524 (no IIIT-BH affiliation on the PDF or not IIIT-BH); 2311.11250 and 2512.07822 (IIT Bhubaneswar).
* Duplicates: the Springer "Complex Prediction ..." paper appears on three faculty pages (kept once, under Vipsita); IJDMB 2021/2022 dense sub-graph paper skipped because the two pages disagree on its year.

## Coverage (rows)
Departments: Computer Science 45, Electronics Engineering 35, Mechanical 16, Electrical 6, Basic Science and Humanities 5 (Mathematics: Sunanda, Nayak). Years: 2016 6, 2017 8, 2018 15, 2019 18, 2020 15, 2021 17, 2022 14, 2023 8, 2024 3, 2025 2, 2026 1.

## Known biases
* Heavily faculty-page based: only lists that faculty maintain; most pages stop at 2022-2023, so 2024-2026 are thin (6 rows).
* Per-person cap 8 reached for Mishra, Vipsita, Sahoo (Bamadev), Padhi, Biswal, Singh; prolific small-group authors dominate Electronics and Mechanical.
* Basic Science and Humanities and Electrical are under-covered (most pages "Coming Soon"). No former faculty found; student-led papers appear only through co-authored lists (Information Security Lab, arXiv).
* DOI rate is low (44 %, 47 of 107) because many pages print no DOI and none was looked up.
* Year of a few rows is taken from the page's heuristic year (printed in the citation); the Springer Interdiscip Sci paper is 2023 by volume (online 2022).
* Titles are as printed on the page (some contain page-typed spellings).
