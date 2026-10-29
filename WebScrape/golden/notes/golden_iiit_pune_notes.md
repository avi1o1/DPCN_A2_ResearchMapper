# Golden set: IIIT Pune (iiit_pune), 2016-2026, lab notebook

Built by an independent agent (operator: Arihant Tripathy). No bibliographic API or aggregator was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API/search). `WebScrape/iiit_pune.json` and other pipeline output were not read. Every URL was fetched with `WebScrape/agents/polite_get.py`; downloads are in `rm_work/iiit_pune_golden/data/`, scripts in `work/iiit_pune_golden/code/` (`rows_a.py`, `rows_b.py` hold the hand-checked rows; `build.py` deduplicates, applies caps and writes the CSV).

**Result:** 94 distinct papers (target 150 not reached, see "Why 94"), 94 medium / 0 high, 10 with a DOI (10.6 %). Year range 2018-2026 (nothing for 2016-2017).

## Institute facts used
* Institute: IIIT Pune (IIITP), founded 2016, PPP IIIT. The live site iiitp.ac.in is a JavaScript single-page app (static HTML is an empty shell). Its data live in the public JS chunks served by the institute (`/assets/faculty_details-*.js` = profile data with publication lists; `/assets/PublicationsPage-*.js` = links to the publication PDFs; `/assets/ReportsAndMinutes-*.js` = annual report links; `/assets/NIRFPage-*.js` = NIRF file links). `www.iiitp.ac.in/research/` and `/page/faculty-0` failed to resolve once (ConnectionError) on the live host; the Wayback copy of `/page/faculty-0` (2024-04-21) was used for the old Drupal faculty list. Wayback copies used: faculty-0 (2024-04-21), annual-reports page (2024-08-09), NIRF page (2023-05-30), NIRF 2023 Overall PDF (2023-05-30), cse-regular-faculty (2025-01-31, only links to Google Sheets, no data), ash-adjunct/regular-faculty (2025-01-31, used to look for one name). Wayback CDX for `iiitp.ac.in/page/*` showed no snapshots before 2023.
* Campuses: transit/temporary campus in Pune (site footer: Survey No. 9/1, address only partly captured) and permanent campus at Nanoli, Talegaon Dabhade (Talegaon, Pune). I did not need the campus in any row; no paper was admitted on the basis of an address. Years/addresses were not established precisely: noted as a gap.
* Look-alike kept out: private I2IT (Hinjawadi; isquareit.ac.in), VIIT Pune (one web hit mentioned "VIIT Pune"), IITM Pune (Indian Institute of Tropical Meteorology, Bhupendra Bahadur Singh), COEP, DIAT Pune. Homonym check: Bhupendra Singh (IIIT Pune) vs Bhupendra Singh (IIT Jodhpur) and Bhupendra Bahadur Singh (IITM Pune): only the profile on iiitp.ac.in was used.
* Tenure data (rule b): NIRF "Faculty Details" tables with joining dates from institute-hosted PDFs: NIRF 2023 Overall (Wayback), `iiitp.ac.in/NIRF/2.pdf` (2026 Overall), `/NIRF/4.pdf` (2025 Overall), `/NIRF/5.pdf` (2024). Joining years used: Khiste 2016, Kushwaha 2017, Hazra/Guled/B. Singh/Nair/S. Mishra 2018, S. Sharma/Tiwari/Dixit 2019, Sushant Kumar/Lipare/Vagisha Mishra 2021, Majithia/M. P. Yadav/P. Jain/Salve 2022, Basumatary, Bepari, Chaki, Chaturvedi, Dubey, S. Gupta, K. Singh, M. Joshi, P. Joshi, S. Shukla, Semwal 2024. Dhane and Garanayak are not in any NIRF file; the 2017-18 annual report lists them as faculty with duties from 28/08/2017, so 2017 is an upper bound and only papers of 2018 or later were taken. Faculty with no joining date found (Ashish Singh, Tushar Gawande, Sohini Gayen, Manish Kumar, Yashdeep Singh, the "(T)" assistant professors, Seenivasan, Shekhar K. Yadav and others who appear only on the 2026 profile list) were excluded: none of their papers is admitted.
* Rule: a paper counts only if its year is strictly after the joining year. Affiliation was visible on no paper reached (publisher pages were not opened; no arXiv paper with an IIIT Pune affiliation was found), so there is no `high` row.

## Sources, searches, yield
| source | pages/files visited | papers listed | admitted |
|---|---|---|---|
| Faculty profile data (faculty_details chunk, 36 profiles) | 1 chunk (all profiles) + 1 profile route | about 370 items parsed (publications + book chapters) | 22 rows (profile pages) |
| Institute "Publications" PDFs (Publishing Year 2022-23 ... 2026-27, Publication before 2022) | 6 PDFs, about 740 text lines | about 100 items | 23 rows, labelled `dept_page` because they are institute research-publication web pages |
| Annual reports 2016-17 ... 2024-25 (English) | 9 PDFs | lists present in 2017-18, 2018-19, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25; none in 2016-17, 2019-20 | 49 rows |
| arXiv (web search restricted to arxiv.org, abs/PDF only) | 0 pages fetched (searches gave no IIIT Pune hit; VIIT Pune and IIIT Hyderabad hits rejected) | 0 | 0 |
| News / newsletters | not used (no research-news pages found; the site's news chunk has no paper lists) | 0 | 0 |

Search strings used (general web search): "IIIT Pune faculty publications iiitp.ac.in"; "iiitp.ac.in faculty profile publications IIIT Pune Dr. Bhupendra Singh ..."; "Anagha Khiste IIIT Pune lattice paper"; "Tanmoy Hazra Indian Institute of Information Technology Pune paper 2019 OR 2020 OR 2021"; "arxiv Indian Institute of Information Technology Pune 2020 OR 2021 OR 2019 Ritu Tiwari Rahul Dixit"; "site:arxiv.org IIIT Pune ... Sanjeev Sharma OR Hazra OR Guled ..."; "arxiv.org abs Indian Institute of Information Technology (IIIT) Pune India". Search results were not used as paper evidence.

Deviation from the requested source mix (faculty pages 50 %, department 15 %, reports 15 %, arXiv 10 %, news 10 %): actual faculty_page 23 %, dept_page 24 %, annual_report 52 %, arXiv 0 %, news 0 %. Reasons: the profile pages list few papers with years that pass the tenure rule (many lists are undated or pre-joining), and the annual reports are the only source with dated lists for 2018-2021. arXiv/news shares were moved to reports and publication PDFs. Dedup priority when one paper appeared in several sources: faculty_page > dept_page > annual_report.

## Sampling and caps
Per-person cap 8 (counted against the first-named qualifying IIIT Pune author; spread evenly across years inside the list, not top-N), plus at most 10 rows per (source, year). Rows removed by the cap: Sanjeev Sharma (14 candidates), Priyank Jain (13), Mahendra Pratap Yadav (10), Sushant Kumar (9), Divya Chaturvedi (7 kept 7). 115 rows after dedup before caps, 94 after. 26 distinct first-named IIIT Pune authors. Former faculty included: Hazra (left Oct 2023), Dixit (left Oct 2023), Nair (left Aug 2023), S. Mishra (left Oct 2023), Garanayak, Dhane. Non-faculty-led papers: none identified (student first-authored papers appear only with a faculty co-author).

## Coverage: department x year (rows)
| dept | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Applied Sciences and Humanities | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 1 | 1 | 1 | 1 | 7 |
| Computer Science and Engineering | 0 | 0 | 0 | 0 | 2 | 7 | 7 | 8 | 8 | 11 | 11 | 54 |
| Electronics and Communication Engineering | 0 | 0 | 4 | 3 | 4 | 2 | 2 | 1 | 4 | 10 | 3 | 33 |

Department names follow the institute (CSE, ECE, ASH = Applied Science and Humanities; the Applied Mathematics and Data Science unit sits inside ASH). Humanities/maths coverage is thin because Guled/Khiste/Majithia/Salve profile lists carry no years.

## Why 94 and not 150, and why 2016-2017 are empty
* IIIT Pune had one faculty member in 2016 (Khiste, Aug 2016) and one more in 2017 (Kushwaha, Jul 2017); the strict "year after joining" rule leaves nothing for those years (their dated lists are pre-2016 or undated). No annual report lists papers for 2016-17.
* Most NIRF-dated faculty joined 2018+ and most papers listed in institute documents are pre-joining works (their lists begin 2012). They were rejected, not counted.
* arXiv found nothing with IIIT Pune affiliation, so no `high` rows exist; the benchmark is therefore a medium-confidence set only and affiliation-by-date errors are possible.

## Rejected candidates (examples)
* Papers dated at or before the joining year: Hazra 2018 (IJIUS, joining 2018), B. Singh 2016/2018 (Windows forensics; joining 2018), S. Mishra 2018 (TCAS-I, matchline papers), Tiwari 2018/2019 (joined 2019), Khiste 2014-2016 lattice papers, Guled 2016/2017, M. P. Yadav 2012-2022 cloud papers (joined Dec 2022), P. Jain 2022 (joined 30-12-2022), V. Mishra 2021 (joined Sep 2021), Lipare 2021 papers, Chaki 2017-2024 (joined Aug 2024; the 2024 IEEE TAC paper is year 2024, equal to joining year), Chaturvedi 2024 antenna papers (joined July 2024), Shivangi Shukla 2019-2024, Kaptan Singh 2019-2024 (joined July 2024; no tenure-qualifying paper kept), Basumatary 2018-2024.
* Not IIIT Pune authors or unknown tenure: Narote, Sangaiah, Medhane, Mukherjee-group and Sahare/Dhok papers in the 2017-19 reports (authors not on the IIIT Pune faculty list); Sohini Gayen 2025-26 papers and others with no joining date.
* Undated or untitled items without a year: Khiste, Majithia, Salve, Guled profile items without years; Bharadwaj/Jain/Singh "Cryptocurrency forensics" (no year); Majithia "Solutions of Time-Space Fractional PDEs" (no year in the 2023-24 report).
* Quality of source text: several PDF lines were mis-encoded (dashes); titles were retyped from the text, DOIs only where printed in the same source.

## Known biases
* Heavily 2024-2026 weighted (about 40 % of rows); the early years are almost empty, so recall results for 2016-2019 are unreliable (only 7 rows).
* Reports and publication PDFs are institute-curated and list works produced elsewhere before joining: the tenure rule removes most, but papers of the joining-year-plus-one may still be pre-joining work.
* Year taken as printed in the source; online-first vs issue year can differ by one (for example Cluster Computing 27(1) listed as 2023 in the 2022-23 report and 2024 in the 2023-24 PDF; 2024 used).
* No DOIs where sources print none (reports), so DOI coverage is 10.6 % and unrepresentative.
* Accepted/forthcoming papers (GCON 2026, ET2ECN-2026) are included as conference rows with "(accepted)" in the venue.
* Faculty lists with profile owner differing from first author: row attributed to the first qualifying IIIT Pune author (cap author), noted in `notes`.
