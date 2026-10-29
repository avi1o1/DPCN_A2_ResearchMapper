# Golden set notebook: IIIT Bangalore (iiit_bangalore), 2016-2026

Operator: Arihant Tripathy (IIIT team). All fetching via `WebScrape/agents/polite_get.py`. No Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API/search used; pipeline output for this institute not read. No Wayback copies were needed (all hosts resolved).

**Result:** 261 distinct papers (target 300 not reached: see "Why 261"). 228 medium, 33 high. 137 rows (52 %) carry a DOI, all printed on the source (no lookups). Types: conference 168, journal 70, preprint 16, book-chapter 7. 81 distinct first-named IIITB author strings; at most 7 rows per first-named IIITB faculty member (cap 8). Years 2016-2026 with 23-24 rows each (year-balanced on purpose).

## Sources, counts, yield
| evidence_source | rows | what |
|---|---|---|
| annual_report | 105 | IIITB annual reports (www.iiitb.ac.in/includefiles/annual_reports/*.pdf): 2016-17 (71 entries parsed) and 2017-18 (91) have a "Faculty Publications" section; 2019-20 to 2025-26 have conference/journal lists (1186 entries parsed). Capped at ~10 per year for 2016-18 and ~6 for 2019+. 2015-16 report is image-only (no text), 2018-19 has only per-lab lists (not used). |
| faculty_page | 67 | own profile pages www.iiitb.ac.in/faculty/<slug> (59 current-faculty pages cached by the roster agent, reused; 25 had parseable lists). Quoted-title entries plus a few title-extracted entries (period/comma styles); noisy lines (awards, grants, talks, theses, trade press) dropped. |
| dept_page | 52 | the institute's own year-wise page www.iiitb.ac.in/publications (static HTML, 2019-2026, about 1200 entries; not an IRINS/Scopus widget). Capped ~5 per year. Counted as dept_page. |
| news | 21 | Naviiina (naviiina.iiitb.ac.in, institute newsletter) "Publications"/"Publication Lounge"/other-stories pages for Dec 2020, Feb 2021, Apr-May 2021, Jan 2022, Mar 2023, Aug 2023, Apr 2025, Sep 2025, Nov 2025, Oct 2026 (10 pages). DHSS site pages (publications-conferences, research-roundup, faculty-spotlight, news) held no usable paper entries. |
| arxiv | 16 | 18 abs pages + PDFs fetched (ids from profile pages of Jaya Sreevalsan-Nair, Amit Chattopadhyay, Ahana Pradhan and from web-search result snippets); IIITB affiliation read on page 1 of each PDF; 1 dropped (2602.12028, no affiliation visible). Year = first version. |

Searches (web search tool): `arxiv.org "IIIT Bangalore" Bengaluru 560100 abstract`; `arxiv 2017 OR 2018 OR 2019 "International Institute of Information Technology Bangalore"`; `arxiv "IIIT-Bangalore" Electronics City Hosur Road 2020 2021`; `arxiv "IIIT Bangalore" 2016 ... faculty names`; `arxiv "IIIT Bangalore" 2023 2024 2025 ...`; `... 2018 paper Srinath Srinivasa OR Jaya Sreevalsan ...`; `IIIT Bangalore researchers paper published journal professor team study news`; `iiitb.ac.in news research paper accepted conference best paper award`. Only the first and last two found useful results; no arXiv papers for 2017-2019 were found, so those years rest on annual reports and faculty pages.

Planned mix was faculty 50 / dept 15 / annual report 15 / arXiv 10 / news 10. Actual: faculty 26 %, dept 20 %, annual report 40 %, news 8 %, arXiv 6 %. Reasons: most profile pages carry no publication list (34 of 59), several others are bios/awards only; annual reports are structured and give 2016-2018 coverage; arXiv search by affiliation is not possible without the forbidden `/search`.

## Tenure handling
Joining year from the NIRF files cached by the roster agent (earliest dated row per name; e.g. Thangaraju 2017, Debabrata Das 2002 per own page, Ramasubramanian Feb 2017, Srinivas Vivek Jan 2018, Amrita Mishra Dec 2020, Prem Singh 2021, Raghuram 2022, Kurian 2022, Tulika Saha 2024) or own page. Rule: year strictly after joining year (affiliation not printed in annual-report / institute-list / profile entries, hence `medium`). Where no joining year exists (Srinath Srinivasa, Chandrashekar Ramanathan, Jyotsna Bapat, Ashish Choudhury) rows are accepted only with on-page evidence (named as IIITB faculty/lab member in the same dated annual report) and the note says so. NIRF dates are upper bounds on joining and some names are ambiguous (e.g. Madhav Rao 2012 vs 2017, ambiguous first-name-only rows); papers are 2016+ so the effect is small. Former faculty (Neelam Sinha, Nanditha Rao, Subhajit Sen, Chetan Parikh, Janaki Srinivasan, Bidisha Chaudhuri, Balaji Parthasarathy, Preeti Mudliar, Tricha Anjali, S. Sadagopan) are used only from annual-report listings (dated documents); their leaving year was not established. Retired G. Srinivasaraghavan excluded.

## Coverage (departments x years 2016..2026)
DSAI: 8 5 6 6 3 9 4 10 13 12 6 (82); ECE: 8 5 8 7 6 6 13 6 8 6 8 (81); CSE: 7 9 6 9 7 7 2 5 1 2 6 (61); DHSS: 1 5 2 2 7 2 5 2 1 2 2 (31); E-Health Research Centre: 6 rows. Department = unit of the first-named IIITB author as on the institute's department people pages (d_cse/d_dsai/d_dhss/d_ece, roster cache); students and multi-affiliated faculty (e.g. Amit Chattopadhyay CSE/DSAI) assigned to the supervising faculty's primary unit. Centre for Applied Sciences has no rows (no author mapped).

## Rejected / skipped
Papers of faculty without a joining year or on-page evidence (Naganand Yadati, Amit Chattopadhyay as first IIITB author, Aswin Kannan, Sanghasri) from lists; Voice and Data / Open Source For You / newspaper op-eds; grant, award and talk lines on profile pages; theses; entries with garbled titles; duplicates across sources (title-normalised). 352 institute-list entries with no matched current/former faculty author were not used (affiliation of unmatched authors unknown).

## Why 261
The per-person cap (8) over about 45 faculty with known tenure bounds the total; pools for 2023-2026 shrank after caps and tenure filtering, and sources outside lists (arXiv, news) were thin.

## Known biases
Heavy reliance on annual reports (2016-18), over-representation of ECE/DSAI faculty with parseable pages, under-representation of CSE/DHSS in 2022-2026, current-faculty skew (former faculty only through reports), conference-heavy (64 %), title-extraction favoured entries with quoted titles on profile pages, selection within year by seeded random choice with least-picked-person-first (not DOI-driven), student-led arXiv/news rows identified only by institute newsletters/PDF front matter. Venue strings are heuristically cleaned from the printed citation.
