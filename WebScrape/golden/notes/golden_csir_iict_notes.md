# Golden set: CSIR-IICT Hyderabad (csir_iict), 2016-2026, lab notebook

Built 2026-10-27 by an independent sub-agent. No Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP,
Google Scholar, Scopus, IRINS/Vidwan, DataCite or arXiv API was used. `WebScrape/csir_iict.json`, `v2/`, `raw/`, `logs/` not read.
All fetches went through `agents/polite_get.py` (wrapper `rm_v2_work/csir_iict_golden/code/get.sh`, log in `data/fetch.log`).
Scripts in `.../code/` (extract/parse: `parse_ar.py`, `split_entry.py`, `build_ar_rows.py`, `build_manual_rows.py`, `build_csv.py`);
the manual-row builder asserts that every title appears verbatim in the fetched page text.

**Result: 400 rows = 392 annual_report + 8 faculty_page; 0 DOIs; years 2018 and 2019 = 393 rows, 2016/2017/2020/2021/2023/2024/2026 = 1 row each.
This is far from the requested design (every unit, every year, source mix). The reasons are below; the set is usable only as a
2018-2019 institute-wide recall benchmark plus a token sample.**

## What was reachable
* **iict.res.in live site is unreachable from this machine** (www and bare host: ConnectionError / ConnectTimeout, all retries). Wayback copies are allowed by the brief, used instead.
* **Faculty profile pages (`/People/view?id=`, `/URL_PROFILE?StaffNo=`)** load the publication tab by a POST AJAX call
  (`getPeopleData`); the Wayback copies contain only the "About" text. No publication lists obtainable (tested id=335 B.V. Subba Reddy, StaffNo=1867 Patra).
* **Department pages / roster:** not obtained (same site). Hence no department field for annual-report rows and no department x year table beyond the one below.
* **Digital repository dri.iictindia.org (DSpace):** Wayback copy says "Updated upto 2015": out of range, not used. iictindia.org answers 403 (not bypassed).
* **Annual reports:** the site lists four biennial reports: 2016-18 (35.9 MB), 2018-20 (15.8 MB), 2022 (53.7 MB), 2024 (46.6 MB).
  Only 2018-20 came through Wayback complete (`web.archive.org/web/20260915004558id_/https://iict.res.in/annualreport/1001_1685367041.pdf`, 16.6 MB, text layer).
  The other three were returned truncated by Wayback (exactly 5 MiB or 1 MiB, several snapshots tried: 2023, 2024, 2025, 2026), PDF unreadable (no xref).
  2022 is also above the ~50 MB limit. So 2016-17 and 2020-2026 report lists are missing.
* **arXiv:** two web searches for IICT-authored arXiv papers returned only scientometric papers about India; none with IICT authors found. No arXiv fetch made.
* **News / web search:** the search tool returned almost no IICT paper pages (6 searches, see below); csirnews.niscpr.res.in timed out; X/Twitter not fetchable. No news rows.
* **Personal/group pages found:** only one (Chittaranjan Patra, Google Sites). S. Prabhakar biodata PDF (nacsindia.in) lists journal/year/volume only, no titles: not used. Wikipedia pages of S. Venkata Mohan, D. Srinivasa Reddy, S. Chandrasekhar, L. Kantam: no publication lists.

## Sources used
| source | pages visited | rows |
|---|---|---|
| Biennial Report 2018-20 PDF (343 pp; PUBLICATIONS-2018 pp.276-303 printed, PUBLICATIONS-2019 pp.304-330 printed; PDF pages 288-341) | 1 | 392 |
| sites.google.com/view/crpatragroup/publications (+ home page for tenure) | 2 | 8 |

Annual-report extraction: 1105 entries parsed (568 for 2018, 537 for 2019); 1099 usable (title, venue and year parsed, no encoding damage).
Rows are spaced evenly through each year's list (196 per year, index = (i+0.5)*len/196), in the printed order; every title was re-checked against the raw PDF text.
Types: "Proceedings Paper:" prefix -> conference, "Editorial Material:" prefix -> other, rest journal. The list is institute-wide: **no per-paper IICT author, no DOI, no department**
(17 entries of 2019 print a full author list, put in `iict_author` as printed). Confidence is `medium` because a report listing alone is not affiliation evidence under the brief;
the tenure rule cannot be applied to unnamed authors, but the list is the institute's own output list for 2018-19, so a paper being listed there
is itself strong (not paper-level) evidence of an IICT author. Treat these as "institute-reported".
Patra rows: medium (page header shows CSIR-IICT, Dept. of Applied Biology; at IICT since 2010 per own page); selected 8 of the page's ~65 journal entries spread 2016-2026 (cap 8); page prints no DOIs.

## Search strings used (web search tool)
1. CSIR-IICT Hyderabad annual report 2022-23 publications list pdf
2. iict.res.in scientist profile publications CSIR-IICT Hyderabad chief scientist
3. CSIR-IICT Hyderabad Biennial Report 2018-20 publications pdf
4. "CSIR-Indian Institute of Chemical Technology" Hyderabad arxiv.org abs
5. Subba Reddy B. V. CSIR-IICT personal website publications list 2022 2023
6. CSIR-IICT Hyderabad research group website "list of publications" principal scientist
7. sites.google.com CSIR-Indian Institute of Chemical Technology Hyderabad group publications
8. IICT Hyderabad scientists develop new study published in journal 2025 CSIR-IICT researchers
9. "CSIR-Indian Institute of Chemical Technology, Hyderabad" Scientific Reports 2021 article
10. "CSIR-Indian Institute of Chemical Technology" Hyderabad MDPI 2022 open access
11. IICT Hyderabad researchers develop news Telangana Today CSIR-IICT study journal
12. "IICT" Hyderabad group leader personal homepage ... AcSIR Principal Scientist
13. CSIR-IICT Hyderabad scientist github.io OR sites.google.com OR wordpress "publications"

## Departments x years
Department is known only for Patra rows (Applied Biology: 2016, 2017, 2018, 2020, 2021, 2023, 2024, 2026 = 1 each). Annual-report rows: department unknown (institute list) , 2018: 196, 2019: 196 (+1 faculty_page row for 2018 counted separately).
All other departments and years: no coverage.

## Rejected / not used
* Truncated Wayback annual reports 2016-18, 2022, 2024 (unreadable).
* IICT DSpace repository (only to 2015).
* S. Prabhakar biodata (no titles).
* 6 annual-report entries with encoding damage or unparsable tails, excluded rather than repaired.
* Patra page entries lacking a parseable year/venue and entries in the "Selected Editorials/Reviews/Book chapters" blocks were not sampled.

## Biases
* 98 % of rows from one report and two years (2018-19); no 2016-17, 2020-26 coverage; no department balance; no DOIs (DOI recall cannot be assessed from this set).
* Report lists are WoS-style records ("Article Number: ...", Web of Science journal names, "Editorial Material") so the list favours WoS-indexed journal articles; books, chapters, conference papers and non-indexed work are under-represented.
* Titles are as printed in the report (hyphenation and a few typographic characters may differ from the publisher version).
* Because authors are not printed, a pipeline miss on these rows is a miss against an institute-reported paper, not a verified IICT-author paper.
