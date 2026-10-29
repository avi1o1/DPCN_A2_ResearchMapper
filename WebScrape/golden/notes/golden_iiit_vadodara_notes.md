# IIIT Vadodara golden set: lab notebook (October 2026, operator Arihant Tripathy)

Output: golden/golden_iiit_vadodara.csv (99 rows). Built without Crossref/OpenAlex/S2/EuropePMC/DOAJ/ORCID/DBLP/Scholar/Scopus/IRINS/DataCite/arXiv API. All fetches through agents/polite_get.py (work dir ~/rm_work/iiit_vadodara_golden).

## Sources and pages used
| Source | Pages | Found (candidate lines) | Visited | Rows kept |
|---|---|---|---|---|
| New faculty profile pages (faculty_page) | iiitvadodara.ac.in/faculty/profile.php?id=3..39 (30 pages, structured Publications tab) | ~400 entries, but most predate the person's joining | 30 | 17 |
| Old-site faculty pages (faculty_page) | oldwebsite/{jignesh_bhatt, kamal_kishor_jha, pratik_shah, barnali_chetia, ashish_phophalia, novarun_deb, dhirendra, vivek_vyas, swapnil_lokhande, bhupendra_kumar, pramit_mazumdar, sunandita_debnath, dibyendu_roy, naveen_kumar, ajay_nath, antriksh_goswami, dhrmprofeng}.php | ~270 | 17 | 35 |
| Institute Publications table (page.php?slug=publication, 210 rows, mostly 2014-2019) | 1 | ~125 in 2016+ | 1 | 14 (annual_report share) |
| Annual reports 2016-17 .. 2024-25 (Drive PDFs linked from oldwebsite/annual_reports.php, pdftotext) | 9 PDFs (2017-18 text unusable: ligature loss, skipped) | ~300 | 9 | 27 |
| arXiv abs/PDF (found by web search restricted to arxiv.org) | 2301.10929, 2312.14522, 2504.11887, 2507.05026, 2508.12307, 2509.20907 kept; 2212.09284, 2403.11480, 2511.12468 fetched and rejected (no IIIT Vadodara affiliation) | 9 | 9 | 6 |
| Research Highlights page, researchpublication.iiitvadodara.ac.in, news.php, oldwebsite news | 4 | 0 papers (research areas and events only) | 4 | 0 |

Web searches (search tool, standard mode): `arxiv "Indian Institute of Information Technology Vadodara" Gandhinagar` (allowed_domains arxiv.org); `arxiv "IIIT Vadodara" Mazumdar OR Roy OR ...` (no useful hits); `IIIT Vadodara researchers paper published news faculty study`; `"IIIT Vadodara" professor research paper published journal press release 2025`; `"Indian Institute of Information Technology Vadodara" Gandhinagar abstract paper author affiliation Mazumdar OR Phophalia OR Debnath`; `"IIIT Vadodara" faculty research highlighted news ... Times of India OR Deshgujarat` (no news coverage found).

Source mix actually achieved: faculty_page 52, annual_report 41 (institute Publications table 14 + annual reports 27), arxiv 6, dept_page 0, news 0. Deviations: no department/lab pages carry paper lists (department pages are descriptive only), so that share went to faculty pages; no external or institute news coverage of papers exists (institute news lists events), so none; the annual-report share is larger because the institute table and reports are the only lists reaching 2016-2019. arXiv found only Vyas and Wadhwa (6 papers) via search.

## Rules applied
* Confidence: high only for the 6 arXiv rows (affiliation printed in the PDF). Everything else is medium: listing on own page / institute table / annual report, tenure rule (year strictly after joining year).
* Joining years: own page where stated (Bhatt Jun 2014, Sinha Dec 2014, Nath 2015, Jha 2015, Naveen 2015, Shah 2013, Deb Feb 2020, Roy Dec 2020), else NIRF 2025/2026 via roster (Chetia 2015, Lokhande 2015, Phophalia 14-03-2016, Vyas 31-12-2020, Mazumdar 2021, Debnath 2021, Jignesh Patel 2022, Vikas Kumar 2022, Phanikrishna 2024, 2025 joiners). Patra: first archived faculty list 2017-08 (upper bound). Chattopadhyay: profile "2016 - Present".
* Cap 8 per first-named IIIT author: Naveen 8, Bhatt 8, Nath 7, Shah 7, Chetia 8 (checked by script).
* Sampling: entries spread evenly through each person's eligible list (not first N), then adjusted by hand for year/department coverage.
* DOIs only where printed on the page/report/APS link. DOI coverage is 21/99, low because most old-site and report entries print none.

## Rejected / skipped
* People with no joining year and no on-page evidence: Sneha Prasad, Abhishek Kesarwani, Sumit, Rahul Maurya etc.; Piyush Kumar Mishra (joined 2026, papers earlier); Ashish Singh, Sanjeev Mani Yadav (joined Aug 2025; no 2026 papers listed); papers dated in or before the joining year (e.g. Dwivedi, Nagendra Kumar 2022-2025 papers done at Stanford/IIIT Allahabad/etc.; Varun Kumar and Debnath 2020 items; Dibyendu Roy 2020 and earlier; Vyas 2018-2019 items; Mazumdar 2019 items; Phophalia 2016 Rupsa Saha paper; Yadav/Atta/Dutt 2019 items (joined 2019)).
* Mentor faculty from DA-IICT and visiting faculty: no tenure dates, not used.
* Institute Publications table rows with only DA-IICT/NIT Rourkela authors or pre-joining authors.
* 2017-18 annual report (ligature-broken text) and 2022-23 to 2024-25 reports only partly mined (two-column layout; used journal/conference lists by hand picking).
* Wayback not used (slot busy; live pages sufficed). arXiv was not blocked (no 403).
* arXiv 2212.09284, 2403.11480, 2511.12468: no IIIT Vadodara affiliation.
* Payal Wadhwa arXiv 2507.05026: affiliation is only a "present address" (work done at Univ. of Vienna); kept as high (affiliation visible) but flagged in notes.

## Coverage (rows)
Years: 2016 5, 2017 6, 2018 8, 2019 5, 2020 5, 2021 15, 2022 8, 2023 11, 2024 14, 2025 14, 2026 8.
Departments: CSE 32, ECE 24, Applied Physics 22, HSS 12, Mathematics and Computing 9.
Former faculty covered: Shah, Bhatt, Chetia, Phophalia, Deb, Patra, Chattopadhyay (all listed as left or possibly left in the roster). No papers from students/postdocs as lead except Ranjeet Bhadoriya (postdoc), Wadhwa.

## Known biases
* Thin early years (2016-2020): the new site lists mostly recent papers, and the 2017-18 report was unreadable; many 2016-2019 institute-table authors were mentor/DA-IICT, NIT Rourkela (Patra) or pre-joining.
* Heavy 2021-2025: faculty pages are newest-first and recent joiners dominate.
* Almost all rows are medium confidence (affiliation not printed per paper); precision depends on tenure dates, which are upper bounds for people with only list-based dates.
* Journals in physics/ECE/HSS from faculty with maintained pages are over-represented; faculty without publication tabs (CSE new hires, Math) are under-represented.
* Year for annual-report rows follows the printed year, which can be the acceptance/online year.
