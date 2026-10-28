# Golden set: IIT (BHU) Varanasi (iit_bhu), 2016-2026, lab notebook

Built 2026-10-27 (work interrupted once by the usage limit and continued from the saved state). Only IIT (BHU) faculty pages were used (iitbhu.ac.in/dept/*/people/*; 408 profiles from the 20 department / school faculty lists); no BHU Institute of Science, IMS or IAS people. No bibliographic API or forbidden source was used for discovery and the pipeline output for this institute was not read. All fetches went through the shared polite fetcher. Data: `/tmp/claude-1000/-home-avilol-Downloads-GitHub-ANLP-A2-ResearchMapper/995e1c99-7243-44f2-a3b6-c40300a778f4/scratchpad/work/iit_bhu_golden/data/` (profiles.json, cand_rows.json), code: `/tmp/claude-1000/-home-avilol-Downloads-GitHub-ANLP-A2-ResearchMapper/995e1c99-7243-44f2-a3b6-c40300a778f4/scratchpad/work/iit_bhu_golden/code/` (join.py, build.py).

**Result: 365 papers (target 550; shortfall explained below)**, all evidence_source = faculty_page, all confidence = medium, 97 with DOI (26 %), 79 faculty, at most 8 per person, titles deduplicated across people.

## Method
1. Faculty profile pages fetched live (308 of 408 carry long text). Their publication lists are free text without a fixed format.
2. A rule-based parser takes entries of the form `Authors (YEAR). Title. Venue ...` (APA style, 181 profiles). An entry is kept only if the person's surname appears in the 260 characters before the year (homonym / template guard).
3. Tenure rule (b): joining year = earliest year in an IIT (BHU) / IT-BHU / BHU context on the same page matching "since / joined / YYYY - till date" (271 of 408 profiles). An entry counts only if its year is strictly after that year. Profiles without a joining year are excluded (138 candidate entries), as decided in the brief. Using the earliest year makes this an upper bound on joining and may drop real papers.
4. Rejected: fused fields (second year inside the title, patents, invited talks, author lists in the venue slot, venue under 9 characters). Counts: about 590 fused/noisy, 270 venue/title junk, 370 year not after joining, 205 author not in entry, 138 no joining info.
5. Per-person cap 8, entries spread evenly through the newest-first list. `iitbhu_author` is the profile owner's name (co-author lists are not split). DOI only where printed within 200 characters of the entry.

## Deviations and biases (read before using for recall)
* Source mix: 100 % faculty pages instead of the 50/15/15/10/10 mix. No annual reports, arXiv PDFs, news or lab pages were used; confidence is therefore medium throughout (affiliation is not printed on the entry).
* Only profiles with APA-style lists are covered (about 80 faculty). Other formats were skipped, so coverage is uneven: Computer Science, Electrical, Electronics, Metallurgy and Physical AI are under-represented or empty; Civil, Mechanical, Mining, Biochemical Engineering and Humanities are over-represented. A recall estimate from this set describes the pipeline on these units only.
* Titles come from regex splitting at the first sentence end; a few may be truncated or carry venue fragments. Venue strings are as printed, sometimes cut at a period.
* Wayback copies of 11 profiles and 80+ personal websites were fetched (data/w, data/site) but not mined.
* department uses the institute's unit name (APD = Architecture, Planning and Design; DSE = School of Decision Sciences and Engineering; SPA = School of Physical AI).

## Departments x years
| Unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Department of Architecture, Planning and Design | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 4 | 3 | 10 | 0 | 18 |
| Department of Ceramic Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 2 |
| Department of Chemical Engineering | 2 | 1 | 2 | 2 | 2 | 2 | 3 | 0 | 1 | 2 | 0 | 17 |
| Department of Chemistry | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| Department of Civil Engineering | 2 | 4 | 3 | 6 | 8 | 11 | 5 | 9 | 7 | 7 | 0 | 62 |
| Department of Computer Science and Engineering | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 2 | 0 | 0 | 6 |
| Department of Electrical Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| Department of Humanistic Studies | 1 | 0 | 0 | 0 | 2 | 3 | 1 | 7 | 11 | 11 | 0 | 36 |
| Department of Mathematical Sciences | 0 | 0 | 0 | 2 | 0 | 1 | 1 | 0 | 2 | 2 | 0 | 8 |
| Department of Mechanical Engineering | 3 | 6 | 1 | 11 | 2 | 1 | 3 | 8 | 6 | 3 | 0 | 44 |
| Department of Mining Engineering | 0 | 1 | 2 | 0 | 11 | 6 | 5 | 5 | 3 | 7 | 0 | 40 |
| Department of Pharmaceutical Engineering & Technology | 3 | 2 | 1 | 1 | 2 | 2 | 1 | 5 | 3 | 4 | 0 | 24 |
| Department of Physics | 1 | 0 | 1 | 2 | 1 | 1 | 1 | 3 | 4 | 2 | 0 | 16 |
| School of Biochemical Engineering | 0 | 1 | 2 | 2 | 3 | 3 | 5 | 4 | 11 | 9 | 0 | 40 |
| School of Biomedical Engineering | 0 | 1 | 3 | 6 | 1 | 0 | 1 | 2 | 1 | 1 | 0 | 16 |
| School of Decision Sciences & Engineering | 0 | 0 | 0 | 0 | 0 | 2 | 4 | 1 | 6 | 3 | 0 | 16 |
| School of Materials Science and Technology | 2 | 1 | 2 | 3 | 2 | 4 | 0 | 1 | 0 | 0 | 0 | 15 |

<!-- SUPPLEMENT-1 BEGIN (extension pass, 2026-10-28) -->
## Supplement 1: extension pass (365 -> 543 rows)
Work dir: `/tmp/bhuwork/` (scripts cand.py, ar.py, selar.py, sites_build.py, prevb.py, merge.py; texts of reports and sites). All pages fetched through the shared polite fetcher; no IRINS / Scopus / Scholar / OpenAlex / Crossref, no arXiv /search, no bot-wall bypass. First-pass rows untouched (backup of the first pass: `/tmp/bhuwork/firstpass.csv`).

### Sources, yields, rejections
| Source | Rows added | Confidence | How |
|---|---|---|---|
| Annual reports 2016-17 .. 2023-24 (`iitbhu.ac.in/contents/institute/dean/doaa/doc/annual_report_english_<FY>.pdf`; only the 2024-25 URL was linked on the site, the other years were obtained by changing the year in that URL pattern and all returned PDFs) | 76 | medium | "Refereed International Journals" lists per department; 3,304 parsed entries 2016+ (about 55 % of entries parse; the rest skipped), author matched to roster by name tokens (unique roster hit, same department as the section's vote, year > roster joining year), max 3 per person |
| Lab / personal sites (the unmined `data/site` set, then their own "publications" sub-pages, 40 fetched) | 37 offered, 36 kept as `dept_page` | medium | CSE (Chanak, Dutta, Patra, Chaturvedi, Mastan, Obbattu), EEE (S. Paul), Metallurgy (Basu, Nandam), Physics (Bhoi); titles of unquoted lists typed by hand |
| Department publication pages, archived copy of `prev.iitbhu.ac.in/dept/{cse,ece}/research/publications` (live host unreachable: ConnectionError; Wayback snapshots 2025-01/02 used) | 42 | medium | 150 candidates (CSE 2016-2019, ECE 2019-2020), name-matched, 3 per person |
| arXiv PDFs found with web search restricted to arxiv.org (6 queries, 33 PDFs fetched at 15 s each) | 24 | high | affiliation printed on page 1 of the PDF; year = first version (arXiv id) |
| Institute news / research news | 0 | n/a | iitbhu.ac.in/news is administrative notices only; press articles (Statesman, NewsBytes) returned 403 (not bypassed); Lokmat page carried no paper titles |
| Wayback copies of 11 profiles | 0 | | not mined (faculty-page rows already cover them) |

Rejected: 9 arXiv PDFs without the institute in the first page (2008.01997, 2206.13186, 2211.12729, 2409.16835 math preprints of M. K. Vemuri / M. Mishra; 2312.02082, 2403.15977, 2404.02724 (a thesis), 2404.09215; 2407.20133 only an internal report number); Anubrata Das lab list (all pre-2025 = before his 2025 joining); Chanak/Dutta/Basu/Nandam/Paul entries on or before the roster joining year; harsh Kasyap site (joined 2025, list is pre-joining); Jyotirmoy Ghosh (no joining year in the roster; list is Purdue-era); 2024-25 annual report (publication section is a single undifferentiated APA list, not parsed); annual-report entries with junk venue ("ISSN", "accepted"); Metallurgy section of the reports did not match any roster name unambiguously.

### Biases and caveats (read before use)
* Annual-report and archived-department rows are `medium`: the listing is not affiliation evidence; the authors are mapped to the roster heuristically (initials + surname, unique hit, department vote), so some rows may belong to a same-initial outsider co-author; the person named in `iitbhu_author` is the roster name, not necessarily the exact one printed. NIRF joining years are an upper bound (rule b).
* Annual-report rows come from 2016-17..2023-24 only; fiscal-year lists contain 2016-2024 papers, so 2025-2026 stays thin in that source. Report lists are by IIT (BHU) staff but may include papers from BHU colleagues with the same initials.
* Year balance: 2016 and 2017 remain the thinnest years (26 and 25 rows). The source mix is now 67 % faculty pages, 14 % department/lab pages, 14 % annual reports, 4 % arXiv, 0 % news (target 50/15/15/10/10).
* Roster department names were used for new rows (Chemical Engineering and Pharmaceutical normalised to the first pass spelling). Metallurgy and Electrical stay thin because their annual-report sections could not be matched and personal sites list mostly pre-joining work.
* arXiv rows include student-led papers (first-page `rs.*@itbhu.ac.in` emails); `iitbhu_author` lists the BHU-affiliated authors as printed; some of these (Himanshu Sahu, Savita Chaturvedi, ...) are not on the faculty roster, so the 8-per-person cap is only applied to roster people.
* DOI only where printed in the entry (23 % of all rows).
<!-- SUPPLEMENT-1 END -->
