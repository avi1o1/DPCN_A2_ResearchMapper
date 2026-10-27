# Lab notebook: golden set CSIR-National Chemical Laboratory (CSIR-NCL), Pune, 2016-2026

Output: `WebScrape/golden/golden_csir_ncl.csv` (393 rows). Scripts: `rm_v2_work/csir_ncl_golden/code/` (parse_lib.py, parse_allotrope.py, split_tv.py, parse_arxiv.py, build_csv.py, make_notes.py, scan_ar.sh, txt.py). Raw pages: `rm_v2_work/csir_ncl_golden/data/`. All fetches went through `polite_get.py` (only HEAD/range-style size checks used curl, see below). No pipeline output, v2/, raw/, logs/ or csir_ncl.json was read.

## What the NCL web offers (and why the mix differs from the brief)
* ncl.res.in (new site, Hindi default, ASP.NET) renders scientist profiles (`/Research/SearchScientistProfile`), the staff list (only 11 rows server-side) and the annual-report list through JavaScript / reCAPTCHA forms. No static per-scientist publication lists were reachable. So there are no faculty-page rows (the brief asks ~50%); this is the main deviation.
* library.ncl.res.in (live), dspace.ncl.res.in (IR@NCL) and `www.ncl.res.in/Resources/Reports` did not answer (connection errors, hangs or 404). The library's "Publications by Year" pages were taken from Wayback copies (allowed, because the live site was unreachable).
* Group websites: web search found no NCL group sites with publication lists (PI-name queries, sites.google.com / github.io style queries). None used.
* Institute news / research highlights (`/Research/RndFeature`, home-page cards) load by JavaScript; not usable.
* HEAD returns 405 on the ncl.res.in file API; size was read from Content-Length of a GET response (curl, headers only, body discarded) before using polite_get for the download.

## Sources used
1. **NCL Library "Publications by Year"** (Wayback copies of library.ncl.res.in/publications-by-year/<year>, headed "As updated from WoS-SCI on 7th-December 2023"), 2016-2023, one page per year. 264 rows (`evidence_source=dept_page`, real source named in `notes`). Each archived page holds only 157-275 entries although the year header counts 294-672; the archive has page 1 only (`?page=1` is 404 there), and page 1 is a title-sorted slice (e.g. 2016 runs from digits/"A" to about "G"). The library rows are therefore NOT a uniform sample of NCL output. DOIs are printed as links on the page; the page gives a division category (used for `department`). Sampling: evenly spaced entries through each year page (33 per year, with a small oversample for de-duplication). The 2022 snapshot is dated Dec 2022 (157 entries, partial year).
2. **Allotrope (CSIR-NCL quarterly newsletter) PDFs**, found via ncl.res.in `/Resources/AnnualReportDetails/<id>` pages -> `/api/File/open-file/...pdf`; "Publications" sections of Jul-Sep 2025 (9.3 MB, 98 entries), Oct-Dec 2025 (16 MB, 87), Jan-Mar 2026 (19 MB, 83), Apr-Jun 2026 (11.7 MB, 100). 112 rows (28 per issue, evenly spaced; `evidence_source=annual_report`, newsletter named in notes). The lists give authors, year, title, journal, volume/pages but no DOI and no division. Titles come from pdftotext; entries with damaged glyphs (lost Greek letters, subscripts, spaced formulas) were excluded, which biases against such titles. Some kept titles may still have lost subscripts; no DOI exists to cross-check.
3. **arXiv** abs pages + PDFs (candidates found by general web search restricted to arxiv.org; never /search or the API). 18 abs pages and 18 PDFs fetched; 17 rows kept with `confidence=high` because the PDF's first pages print "CSIR-National Chemical Laboratory"; 1603.00937 rejected (no NCL in the first two pages). Year = first submitted version. A DOI is recorded only when printed on the abs page.
4. Not used: Annual Report 2024-25 (83 MB, Content-Length checked) and Annual Report 2023-24 (69.7 MB per repository listing), above the ~50 MB limit. AR 2021-22 (36 MB) is in dspace.ncl.res.in, which was unreachable.

## Searches (web search tool)
"CSIR-NCL Pune scientist publications list Google site faculty ... group website"; "arxiv CSIR-National Chemical Laboratory Pune 2024"; "research group CSIR-National Chemical Laboratory Pune lab website publications ... sites.google.com OR github.io"; "ncl.res.in scientist profile publications selected publications ncl-india.org"; arXiv-restricted queries for Physical and Materials / Polymer Science and Engineering / Electronic Structure Theory / Biochemical / Organic / Catalysis with "CSIR-National Chemical Laboratory", "Academy of Scientific and Innovative Research", Sarika Maitra Bhattacharyya; "Kumar Vanka ... group homepage"; "Vivek Ranade / Ashish Orpe ... group website"; "CSIR-NCL Allotrope newsletter ..."; "dspace.ncl.res.in annual report 2023-24 OR 2022-23". Search results were used only to find URLs.

## Counts (found / visited / yield)
| source | candidate entries parsed | rows in set |
|---|---|---|
| Library year pages 2016-2023 (8 Wayback pages) | 2,024 | 264 |
| Allotrope, 4 issues | 368 | 112 |
| arXiv candidates (abs + PDF fetched) | 18 | 17 |

Newsletter hunt: AnnualReportDetails ids 1380-1391 and 1424-1535 were fetched (only 1442, 1459, 1475, 1511, 1530 carry PDFs; 1459 is the 83 MB AR). Other ids were not scanned because the server became very slow. Newsletters for 2024, Jan-Jun 2025 and earlier were not found.

## Coverage (unit x year), 393 rows
`(not stated on source)` = Allotrope rows (no division printed) and one arXiv row. For arXiv rows the division was taken from the PDF when printed.

| unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (not stated on source) |  |  |  |  | 1 |  |  |  |  | 56 | 56 | 113 |
| Biochemical Sciences | 5 | 7 | 5 | 3 | 6 | 7 | 2 | 5 |  |  |  | 40 |
| Catalysis and Inorganic Chemistry | 4 | 3 | 6 | 3 | 6 | 5 | 7 | 6 |  |  |  | 40 |
| Center for Material Characterization (CMC) | 3 |  | 3 | 1 | 2 |  | 1 | 2 |  |  |  | 12 |
| Central NMR Facility | 1 |  |  | 1 | 1 |  | 1 |  |  |  |  | 4 |
| Chemical Engineering & Process Development | 5 | 5 | 6 | 4 | 8 | 7 | 9 | 3 |  |  |  | 47 |
| Chemical Engineering and Process Development Division (arXiv) |  |  |  |  |  |  | 1 |  |  |  |  | 1 |
| National Collection of Industrial Micr-organisms (NCIM) |  | 2 | 1 | 3 |  |  |  |  |  |  |  | 6 |
| Organic Chemistry | 6 | 5 | 4 | 6 | 3 | 5 | 4 | 3 |  |  |  | 36 |
| Physical and Materials Chemistry (incl. Physical Chemistry Division, arXiv) | 8 | 5 | 6 | 5 | 4 | 9 | 7 | 12 |  |  |  | 56 |
| Polymer Science & Engineering | 3 | 8 | 4 | 7 | 5 |  | 3 | 3 | 2 | 3 |  | 38 |
| all | 35 | 35 | 35 | 33 | 36 | 33 | 35 | 34 | 2 | 59 | 56 | 393 |

Counts: evidence_source dept_page 264, annual_report 112, arxiv 17; confidence medium 376, high 17; type journal 368, preprint 17, book-chapter 5, conference 3; DOI on 267 rows (67.9%).

## Confidence and tenure
* 376 rows `medium`: institute-wide lists (library list, newsletter) are the institute's own output lists, not per-paper affiliation evidence; no affiliation is printed on the paper/abstract page in these rows. The tenure rule is not applicable to an institute list.
* 17 rows `high`: arXiv PDF prints the affiliation.
* `ncl_author` = first-listed author as printed (the lists do not mark which co-author is at NCL).
* No faculty-tenure tests, no former-faculty rows (no faculty pages reachable). Students/postdocs appear as first authors where the lists show them.

## Rejected / skipped
* Wayback `?page=1` of year lists: 404 in the archive (pages 2+ missing).
* Library 2024 page (1 entry only) and 2005-2015 pages: not used.
* arXiv 1603.00937 (no NCL affiliation). Search hits that were bibliometric studies of Indian research (2412.06652, 2002.03093) or other-institute papers were not taken.
* Newsletter entries with glyph damage or no recoverable title/journal split.
* AR 2024-25 and AR 2023-24: size above 50 MB.

## Known biases
* Year spread: 2016-2023 evenly covered (33-36 per year); 2025 (Jul-Dec newsletters + arXiv) and 2026 (Jan-Jun newsletters) have ~56-59 each; 2024 has only 2 rows (arXiv). Gap: 2024 and Jan-Jun 2025.
* Source concentration: 67% library lists (title-sliced), 29% newsletter lists, 4% arXiv. No faculty / group / news rows.
* Library list is WoS-SCI based: omits non-WoS output; 2022/2023 snapshots are partial; type mix is almost all journal articles.
* Library slices are alphabetical by title, so titles starting with later letters are under-represented in the library share.
* arXiv rows are physics/theory-heavy (glass, electronic structure, granular) and not representative of NCL chemistry.
* The cap of 8 per person could only be checked on first-listed authors (max 5 per person); co-author PIs may appear more often.
