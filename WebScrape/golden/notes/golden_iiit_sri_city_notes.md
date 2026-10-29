# Golden set IIIT Sri City: lab notebook (operator Arihant Tripathy, run 2026-10-29)

Output: `golden/golden_iiit_sri_city.csv`, 142 papers (target 150 not reached, see "Why 142"). Work files in `C:/Users/Arihant/rm_work/iiit_sri_city_golden/` (data/, code/: ar.py and build.py + rows.py, txt.py, fetchfac.sh).

## Sources and yield
| source | pages/docs visited | candidate entries seen | rows kept |
|---|---|---|---|
| faculty_page (iiits.ac.in/people/regular-faculty/<name>/, 55 profile fetches incl. 6 that returned a fallback Director page) | 55 | ~700 list lines (most undated or pre-joining) | 29 |
| dept_page: institute Publications pages (research/publications/journals/, /conferences/; years 2016-2023 only) | 2 | 179 unique entries | 28 |
| annual_report: 2020-21 (new), 2021-22, 2022-23, 2023-24, 2024-25 (4 cached from roster run, 2020-21 fetched; 2019-20 report has only 3 listed papers, unused) | 6 | ~200 entries | 79 |
| arxiv: abs page + PDF first page, 7 papers checked (PTSR 2310.13216 rejected: no Sri City affiliation) | 14 fetches | 7 | 6 |
| news: institute Press and Media page holds only event clippings; web search returned no external coverage of Sri City research | 1 | 0 | 0 |

Web searches (WebSearch, standard): `arxiv.org "IIIT Sri City" Chittoor Andhra Pradesh paper`; `arxiv "Indian Institute of Information Technology Sri City" deep learning`; `arxiv Shiv Ram Dubey "IIIT Sri City" Computer Vision Group`; `arxiv "IIIT Sri City" Ghorai OR Arun OR Chouhan OR Hazra OR Sethi OR Venkataraman`; `arxiv "IIIT Sri City" Vishwakarma OR Pulabaigari OR Thakur OR Sarkar OR Turlapaty OR Prasath`; `IIIT Sri City researchers publish paper journal news`. Search tool is a general web search (not a forbidden database).

## Deviations from the brief's source mix
Planned 50/15/15/10/10. Achieved faculty 29, dept 28, annual reports 79, arXiv 6, news 0 (about 20/20/56/4/0 percent). Reasons: (1) institute profile pages mostly link to external homepages (Google Sites) and show a publication section only for ~25 people; many of those lists are undated or pre-date joining (tenure rule), so most candidates were rejected; external homepages were not fetched. (2) no news coverage exists, news share moved to annual reports (which carry dated, per-paper lists). (3) arXiv search is forbidden and general web search surfaced only 7 candidates (mostly Dubey, former faculty).

## Tenure and confidence
* `high` (6): arXiv PDFs with IIIT Sri City affiliation printed (one 2026 paper by Chowdhury and Joshi; Dubey/Mukherjee/Gajjala/Ambati papers 2019-2021).
* `medium` (136): listed on faculty page / institute Publications page / annual report; year strictly after joining year (roster, taken from NIRF 2026 or page). Where the roster has no joining year (Tripathi, Sanodiya, Kandaswamy, Arijit Roy, Girish G N) the row is accepted only if the person appears in the faculty table of that annual report ("tenure: on-page evidence"); for the institute Publications page rows this was not used for such people. Former faculty Dubey and Mukherjee: first archived faculty list Nov 2017 is an upper bound on joining (Dubey own bio quoted on arXiv/web says June 2016), so only years after 2017 are kept.
* Annual report and Publications page lists are not affiliation evidence by themselves (they also list pre-joining work); that is why they stay medium.

## Per-person cap
Cap 8 (first-named IIIT author): Bablani, Thakur, Sreeja, R. V. Prasad, Viswanath, Venkataraman, Dubey reach or approach 8; all are <= 8.

## Coverage (department x year, rows)
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Computer Science and Engineering | 1 | 4 | 7 | 7 | 5 | 13 | 19 | 12 | 11 | 14 | 1 | 94 |
| Electronics and Communication Engineering | 1 | 3 | 6 | 7 | 2 | 4 | 4 | 5 | 4 | 3 | 0 | 39 |
| Mathematics and Data Science | 0 | 0 | 0 | 0 | 1 | 0 | 3 | 1 | 2 | 2 | 0 | 9 |

Units: Computer Science and Engineering, Electronics and Communication Engineering, Mathematics and Data Science (institute's three units; humanities lecturers sit in M&DS but no papers found). 2016 and 2026 are thin (2 and 1 rows).

## Why 142, not 150
Strict tenure rule plus the cap removed many candidates; the 2016-2017 shortfall comes from the institute having no recoverable faculty list before Nov 2017 and from papers dated in the joining year.

## Rejected candidates (examples and reasons)
* Year equals joining year with no visible affiliation: Narendra Singh Yadav ANM 2024 (joined 2024), Kartick Sutradhar TITS 2023 (joined May 2023), Abhishek Hazra 2023 papers (joined 2023), Sarkar rVAD 2020 (joined 2020), Turlapaty 2016 papers (joined 2017), Prasath 2016 papers (joined 2016), Bulla Rajesh CompTLL-UNet 2023, Manipriya 2021, Ramesh Kumar 2021, Santhosh Amilpur 2022 pairs (joined 2022).
* Pre-joining work listed on faculty pages: Sreeja 2017-2019, Joshi, Bablani, Neha Agrawal, Sethi, Santhosh, Sutradhar (all pages), Sarkar (2010-2017), Ghorai (2014-2018), Kotamraju not affected.
* Authors without joining year and not in the annual-report faculty table: R. Shathanaa 2022 (rows dropped), Girish G N 2021 (not in the 2021-22 faculty table), Prerana Mukherjee, Odelu (joined 2017; 2016-2017 papers), Mitra (2016-2018 papers, tenure unknown), Nagesh Kolagani conf 2018.
* Praseed 2021 ESWA paper (NITK-era work); Bablani lie-detection papers 2021 (done at NIT Goa).
* Dubey: only 8 rows, cap.
* Faculty pages returning the Director fallback page (Kandaswamy, Girish, Tripathi, Praseed, Sanodiya, Ray): no list; pages of Arijit Roy (id 19) hold undated lists mixed with another person's, skipped (homonym/template risk).
* Tenure of joiners from 2026 (Sharma Mar 2026, Kanakavalli, Bollipo): only 2026 rows possible, none kept without visible affiliation.

## Biases
Annual reports and the Publications page over-represent CSE faculty with stable profiles and 2018-2025; institute page ends 2023; few student-led or postdoc papers; Dubey/Mukherjee (former) are over-represented in 2018-2020 via arXiv; DOIs are filled only where printed on the source (about 25 percent), so DOI coverage is not a recall-friendliness bias but is low; no external homepages (Google Sites) were read. IIIT Hyderabad mentor-faculty and visiting faculty were not sampled.
