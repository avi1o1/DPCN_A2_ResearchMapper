# IIT Kanpur golden set: lab notebook

Final: 433 papers (target 600 NOT reached), 204 faculty/author groups, 22 units, 2016-2026, DOI on 90 (20%).
Work was resumed after an interruption (a usage limit and a network error); the earlier agent's cached pages and parsers under the scratchpad work dir were reused.

## Sources used and counts
| Source | rows | confidence | what was done |
|---|---|---|---|
| faculty_page | 287 | medium | 665 faculty profile pages under iitk.ac.in (fetched via polite fetcher) parsed for publication lists (1,747 candidate entries, 613 after tenure rule and spread-sampling, 503 after title clean-up); 383 personal homepages linked from profiles (hp/) also parsed. Final: cap 3 per person spread evenly through newest-first lists (1,134 entries rejected: year <= joining year, no joining year, or over cap). |
| dept_page | 103 | medium | Department publication pages: EE (8 sub-pages: control, microelectronics, optec, power, simulation, RF, signal processing, general), Civil (recent-publications), Physics (recent-publications, book-publications). Authors matched to the faculty list by surname + initial (ambiguous pairs dropped); year > joining year required; max 2 per person, total cap 8. Aerospace and Mathematics pages were fetched but yielded no matchable entries. |
| arxiv | 34 | high | 42 arXiv abs/html/PDF pages reached via web search (arxiv.org-restricted) and links on institute pages; 34 kept where an IIT Kanpur affiliation is printed on the page/PDF (8 dropped: no IITK author, one 404). Preprint year = first-version year (arXiv id). |
| annual_report | 6 | medium | Annual reports 2016-17, 2018-19 (no text), 2020-21, 2024-25 contain NO publication lists; only project-output sections list papers (Sahay 2024-25, Goel 2020-21). Sahay rows beyond the 8-per-person cap were dropped. |
| news | 3 | high | 108 press-release / media-coverage pages from iitk.ac.in fetched (filtered by research keywords); only a handful name the exact paper title; 4 with title + journal + IITK author kept (3 survived dedup). External news (TOI etc.) not used. |

Pages visited: faculty pages 665, homepages 383, dept pages 22, annual reports 5, arXiv 42, news 108 + listing pages (press-releases 69, media-coverage 35).
Search strings: arxiv.org-restricted web queries "IIT Kanpur" + topic/department (list in earlier session was lost; not reproducible verbatim).

## Source mix vs brief
Brief: faculty 50 / dept 15 / annual 15 / arXiv 10 / news 10 %. Achieved: faculty 66 %, dept 24 %, arXiv 8 %, annual report 1.4 %, news 0.7 %. Annual reports have no publication lists and few news items give exact titles, so those shares went to faculty/dept pages.

## Tenure rule
Joining year: own profile page, else roster (WebScrape/rosters/iit_kanpur_faculty.csv, NIRF-derived), else NIRF; some manual overrides from profiles (upper bounds). Paper counts if year strictly > joining year (confidence medium) or affiliation visible on the page/PDF (high; arXiv, news). Rows with no joining year available were rejected. No former-faculty tenure end dates were applied to faculty-page rows (only current pages exist).

## Coverage: department x year (rows)
| Department | n | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aerospace Engineering | 29 | 1 | 1 | 1 | 6 | 2 | 6 | 2 | 4 | 2 | 2 | 2 |
| Biological Sciences & Bioengineering | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| Chemical Engineering | 6 | 0 | 0 | 0 | 1 | 4 | 0 | 1 | 0 | 0 | 0 | 0 |
| Chemistry | 28 | 1 | 1 | 3 | 2 | 2 | 0 | 1 | 2 | 7 | 6 | 3 |
| Civil Engineering | 63 | 4 | 9 | 9 | 5 | 12 | 7 | 2 | 2 | 4 | 8 | 1 |
| Computer Science & Engineering | 16 | 0 | 1 | 3 | 0 | 1 | 0 | 2 | 1 | 3 | 3 | 2 |
| Design | 6 | 1 | 1 | 0 | 0 | 1 | 2 | 1 | 0 | 0 | 0 | 0 |
| Earth Sciences | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Economic Sciences | 25 | 7 | 0 | 3 | 3 | 2 | 3 | 6 | 0 | 0 | 1 | 0 |
| Electrical Engineering | 80 | 2 | 4 | 6 | 3 | 4 | 1 | 5 | 4 | 26 | 22 | 3 |
| Humanities and Social Sciences | 26 | 1 | 3 | 1 | 0 | 4 | 4 | 5 | 4 | 1 | 2 | 1 |
| Intelligent Systems | 11 | 2 | 2 | 2 | 1 | 2 | 0 | 1 | 0 | 0 | 1 | 0 |
| Kotak School of Sustainability | 6 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| Management Sciences | 27 | 0 | 1 | 1 | 6 | 3 | 3 | 7 | 2 | 1 | 2 | 1 |
| Materials Science & Engineering | 13 | 2 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 3 | 4 | 0 |
| Materials Science Programme | 6 | 0 | 1 | 2 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| Mathematics | 20 | 1 | 2 | 2 | 2 | 2 | 6 | 2 | 2 | 0 | 0 | 1 |
| Mechanical Engineering | 14 | 1 | 1 | 0 | 1 | 2 | 2 | 1 | 4 | 1 | 1 | 0 |
| Photonics Science and Engineering Programme | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| Physics | 46 | 5 | 8 | 3 | 4 | 1 | 2 | 1 | 5 | 9 | 5 | 3 |
| Space, Planetary and Astronomical Sciences and Engineering | 5 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| Sustainable Energy Engineering | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

## Rejected / issues
* Entries with year <= joining year: ~1134 rejected overall (rej1.json), including joining-year papers without visible affiliation.
* Entries whose title could not be parsed reliably (author/venue fragments, talks, awards, "et al." titles) dropped.
* Biology, Chemical, Earth Sciences, Photonics, Sustainable Energy etc. are thin because their profiles carry few parseable lists.

## Known biases
* Over-represents faculty with parseable web lists; EE/Civil/Physics over-represented via department pages; 2024-25 over-represented (EE pages).
* Almost all rows are medium (tenure rule only); only arXiv/news are affiliation-verified.
* Titles parsed from free-text citation lists; venue strings may be messy ("venue not parsed" when absent); some type labels are heuristic.
* DOI only where printed on the source; DOIs are sparse by design.

<!-- SUPPLEMENT 2026-10-28: extension pass (432 -> 573 rows) -->
## Supplement (extension pass)
Result: +141 rows (all faculty_page, medium), 573 total, target 600 still not reached. Years 2016-2021: 286 rows (was ~215).
Added units: Chemical Eng +18, Mgmt +12, Materials Science Programme +11, Chemistry +11, Mech +10, Econ +9, Civil +8, BSBE +7 (2 -> 9), Math/Physics +7 each, Intelligent Systems +6, Photonics +5 (2 -> 7), Sustainable Energy +4 (1 -> 5), Earth Sciences +3 (1 -> 4), CSE +4, Statistics & Data Science +3, Cognitive Science +2. Thin units remain thin.

### Sources and yields
| Source | fetched | rows added | note |
|---|---|---|---|
| Institute-hosted faculty CV PDFs (iitk.ac.in/data/cv/*, home.iitk.ac.in/~x/*CV.pdf) found by re-scanning links in the 665 cached profile pages that the first pass ignored | 34 PDFs | ~25 | publication sections parsed with a numbered-entry splitter |
| Faculty/lab pages not reached before (home.iitk.ac.in/~bushra/PI.html, bsbe/index.php/<name> x30, Misra lab Google Sites publications page, che/old/*.htm) | ~45 | ~25 (Misra lab page, BSBE pages have no lists) | |
| Re-parse of cached profile/homepage text with two new parsers (PubMed-style "Authors. Title. Journal" and "Authors, Title. Journal" lists) | cached | ~90 | earlier pass failed on these formats, which is why BSBE/Earth/Photonics were thin; the earlier cap of 3 per person was raised to max 3-5 (thin units) within the 8-per-person total |
| Annual reports | re-checked 2016-17, 2020-21, 2024-25 with `pdftotext -raw` (no column crop needed: text is one stream) | 0 | grep for journal/vol./pp./Transactions finds 0-13 hits, all project-output notes (Sahay, Goel, already used). No per-faculty research-output list exists in these reports. 2018-19 is image-only (no OCR tool available). 2019-20, 2021-22, 2022-23, 2023-24 PDFs (iitk.ac.in/data/...) were requested but the shared fetch had not returned them at the end of the run, not checked. |
| R&D newsletters (39 monthly PDFs listed at dord/publication/publication-r-d-newsletter), research-highlights list | 2 PDFs sampled, list page | 0 | newsletters carry project/event news, no paper titles; research highlights are funded projects, not papers |
| arXiv via web search restricted to arxiv.org (4 queries: BSBE, Earth Sciences, Photonics, Sustainable Energy) | search only | 0 | no hit with a printed IIT Kanpur affiliation in these units; no new arXiv rows, no /search use |
| News | 0 new | 0 | no new titled-paper pages found beyond the earlier 108 |

### Rejected / dropped
Auto-parsed candidates 2,319 -> 414 sampled -> 192 after format filters -> 141 after manual removal (author-list fragments as titles, news lines such as "paper accepted at ...", talks, workshops, patents, titles with venue fused in, truncated titles, "Copyright" footers). One Sahay row removed to keep 8 papers per person. No joining year: 63 candidate entries dropped.

### Biases and caveats
* Source mix drifted further to faculty_page (about 75 %); annual reports and news did not contribute.
* Titles from CVs and lab pages are free-text parses; venue is "(venue not parsed from listing)" where authors leaked into the venue field. Some venue strings still carry volume/page text.
* Tenure rule only (medium); join years from profile/roster/NIRF as before. 2024-26 still about 33 % of rows because most lists are newest-first.
* BSBE, Earth Sciences, Photonics and Sustainable Energy faculty mostly publish through external lab sites or Google Scholar/IRINS, which are excluded; fewer than half of those faculty have any parseable list.
<!-- /SUPPLEMENT -->
