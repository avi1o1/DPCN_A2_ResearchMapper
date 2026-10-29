# Golden set: IIITDM Kancheepuram (iiit_kancheepuram), 2016-2026, lab notebook

Built by an independent sub-agent (operator: Arihant Tripathy). No bibliographic API or aggregator was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API/search). `WebScrape/iiit_kancheepuram.json` and other pipeline output were not read. All fetching went through `WebScrape/agents/polite_get.py` (log `rm_work/iiit_kancheepuram_golden/data/fetch.log`; scripts in `.../code/`, downloads in `.../data/`). Roster and tenure inputs: the roster agent's cached institute faculty list and NIRF-derived joining/leaving dates (`rm_work/iiit_kancheepuram_roster/data/live.json`, `nirf_union.json`); these are institute/government sources, not pipeline output.

**Result:** 297 distinct papers (target 300 not quite reached; remaining source types were exhausted or unusable, see below). 275 medium, 22 high. 47 with DOI (16 %), DOI only where printed in the listing or PDF. Types: journal 160, conference 109, preprint 23, book-chapter 5. 97 distinct IIITDM-author strings; max 7 rows per first-named person (cap 8 respected). Years 2016-2026.

| evidence_source | rows | share | confidence |
|---|---|---|---|
| faculty_page (www.iiitdm.ac.in/people/faculty/EMAIL, 110 profiles fetched) | 231 | 78 % | medium |
| dept_page (ECE department site journals.html / conferences.html) | 27 | 9 % | medium |
| annual_report (2017-18, 2020-21 consolidated lists) | 17 | 6 % | medium |
| arxiv (PDF first-page affiliation checked) | 22 | 7 % | high |
| news | 0 | 0 % | |

The planned mix (faculty 50, dept 15, reports 15, arXiv 10, news 10) was not reachable: faculty pages are by far the richest source (each profile embeds journal/conference/book lists in the page data); the other shares were limited as described below. The faculty share is therefore too high (78 %).

## Source reconnaissance
* **Faculty profiles:** all 110 roster entries (CSE 25, ECE 24, ME 23, SIDI 17, Mathematics 10, Physics 8, English 3). Publication lists sit in the SvelteKit page data (`title:"Journal Publications",items:[...]`) as free-text citations, parsed heuristically (quoted title, else comma-split after the author list). About 3,700 entries parsed, about 1,530 pass the tenure rule. Some profiles have no lists (professors of practice, adjuncts, a few new joiners).
* **Selection:** per person 2 (n<10 eligible), 3 (10-39) or 4 (>=40) entries spread evenly through the eligible list, plus up to 2 older (<=2019) entries per person to cover early years. Entries with unparseable titles were skipped in favour of the next spread entry (a small bias towards cleanly formatted citations); about 25 mis-split titles were hand-corrected or dropped.
* **Annual reports** (old.iiitdm.ac.in/img/AnnualReport/): 10 English PDFs fetched. Text-extractable with a consolidated list: 2017-18 and 2020-21 (used). 2021-22, 2022-23, 2023-24 have per-department lists in a messy multi-column layout (not parsed). 2024-25, 2019-20, 2018-19, 2016-17 are image-only PDFs (no OCR attempted); 2015-16 is garbled legacy-font text and pre-dates the window. Authors were matched to roster/NIRF names (surname + initials); a row is kept only when the matched person's NIRF joining year < paper year (and year <= leaving year for former staff). Former staff without a known department were dropped (department could not be stated), which lowered the 2017-18 yield (3 rows). Report listings are medium only.
* **Department pages:** the www.iiitdm.ac.in department pages and the CSE, SIDI and TLC sites carry no publications; Mechanical's "Research Publications" page has no list text; ECE (www.ece.iiitdm.ac.in journals.html, conferences.html) has about 136 matched entries, 27 sampled. Many authors there are former ECE faculty (e.g. Asutosh Kar).
* **News / newsletters:** the Margdarshan newsletter PDFs (old.iiitdm.ac.in/img/MargDarshan/) were attempted; two downloaded but are damaged or image-based (no usable text), the rest failed during a network outage and were not pursued. No external news coverage was searched. The news share moved to faculty pages.
* **arXiv:** found by web search restricted to arxiv.org (queries: `arxiv "Indian Institute of Information Technology, Design and Manufacturing, Kancheepuram" Chennai`; `arxiv IIITDM Kancheepuram Department of Computer Science and Engineering preprint`; `arxiv IIITDM Kancheepuram Electronics and Communication Engineering Chennai 600127`; `arxiv "IIITDM Kancheepuram" Department of Mechanical Engineering OR Physics OR "School of Interdisciplinary Design"`; `arxiv "Design and Manufacturing, Kancheepuram" deep learning OR wireless OR antenna OR cryptography` (no hits); `arxiv "IIITDM Kancheepuram" Department of Mathematics OR "Sciences and Humanities" OR Physics`). 29 candidates; 23 PDFs fetched (arXiv 5 s gap plus shared-slot waits made the rest too slow, so the job was stopped). All 23 showed the affiliation; 22 rows after deduplication. arXiv never answered 403. Candidates not fetched: 2202.00596, 2607.08113, 2501.01981, 2309.04291, 2605.14748-adjacent tensor papers 2307.03977 aside, 2505.16253 (conference host only), 2108.08049; 1511.02038 is out of window (2015).

## Tenure rule applied
Joining year = NIRF earliest listed joining date or the person's own page; an upper bound for early joiners (NIRF only covers 2017 onwards). Paper counted when year > joining year (strict). Former staff: year <= leaving year. Joiners of 2024-2026 therefore contribute almost only 2025-2026 papers. People with no joining year (noor, anilthurimella, vijayakumar, manoharababu, venkatramani, manjusha, arunachalam, raguraman, office accounts) were excluded, except umarani (2014), ratnaraju (2024) and anushri (2018), whose joining years were read from their pages.

## Coverage table (rows by unit x year)
| unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CSE | 5 | 3 | 6 | 3 | 5 | 3 | 2 | 6 | 6 | 7 | 11 | 57 |
| ECE | 5 | 2 | 4 | 16 | 16 | 21 | 9 | 7 | 8 | 9 | 3 | 100 |
| Mechanical | 6 | 5 | 9 | 11 | 3 | 10 | 10 | 9 | 10 | 5 | 1 | 79 |
| S&H Mathematics | 2 | 0 | 1 | 1 | 0 | 1 | 0 | 2 | 5 | 1 | 6 | 19 |
| S&H Physics | 0 | 0 | 1 | 7 | 1 | 3 | 1 | 3 | 2 | 3 | 1 | 22 |
| S&H English | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 3 |
| S&H (stream not stated) | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 |
| SIDI | 0 | 0 | 0 | 2 | 0 | 2 | 2 | 3 | 0 | 2 | 4 | 15 |

## Rejected / excluded
* Entries with year <= the person's joining year (most of newer joiners' lists, which describe prior-employer work), entries without a year, entries outside 2016-2026.
* Mis-parsed citation fragments (e.g. "accepted for publication, 2024", venue-only lines, truncated titles such as one Pandiyarasan paper and a book chapter whose title could not be isolated).
* Professors of practice, adjuncts and visiting faculty with no page lists. No former-faculty pages exist on the current site, so former staff enter only via reports and ECE department pages.

## Known biases
* Heavy faculty-page share; 275 of 297 rows are medium (affiliation not printed in the listing).
* Year (last 20xx in the citation with DOI/URL stripped), venue and title come from heuristic parsing of free-text citations; venue strings may carry trailing words.
* ECE over-represented in 2019-2021 (ECE department lists and the 2020-21 report); 2016 and 2017 thin; NIRF-based tenure excludes recent joiners' older papers.
* Mathematics, Physics, English and SIDI are under-sampled relative to headcount (short or missing lists, recent joiners).
* "Computer Science and Engineering" is used for papers whose PDFs print "Computer Engineering" (older unit name).
* Annual-report authors matched by name-token heuristics; homonyms possible.

## Brief issues
The roster check warns that one name (s vijayakumar) occurs twice (likely two people; not resolved here). "IIT" in the brief was read as "this institute". The 300-paper target and the source mix were not fully met, as explained above.
