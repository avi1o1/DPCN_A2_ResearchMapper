# Golden set IIIT Nagpur: lab notebook (operator Arihant Tripathy, 2026-10-30)

Output: `golden/golden_iiit_nagpur.csv`, 125 rows (target 150 not reached, see "Why 125").

## Sources used (all through `agents/polite_get.py`; Crossref/OpenAlex/S2/EPMC/DOAJ/ORCID/DBLP/Scholar/Scopus/IRINS/DataCite/arXiv API/arXiv search not used; `iiit_nagpur.json` not read)
| Source type | Pages | Rows kept | Notes |
|---|---|---|---|
| Faculty profile JSON of the current site (`iiitn.ac.in/api/faculty/faculty_staff/{id}`; the site is a React SPA, this is the data behind each profile) | 64 profiles fetched (all with a profile_url in the roster) | 42 | 52 listed "publications" in total, over half rejected as pre-tenure |
| Wayback copies of the institute's old faculty pages (CSE/ECE/BS, 2020-10 to 2024-07, same snapshots the roster agent cached; used because the live SPA no longer shows these lists) | about 12 snapshots | 40 | profile text states tenure ("2018 to till date") |
| Wayback copies of department "Research" pages (CSE id=316, BS id=317, ECE id=318, 2021-04) | 3 | 11 | counted as dept_page |
| Annual reports (text layer) 2020-21 (E), 2023-24 (E) | 2 of 18 PDFs usable | 20 | other reports are scanned/image-only or Hindi in a legacy font (2017-18 H: titles garbled, not usable); no OCR tool on this machine |
| arXiv abs pages and PDFs reached via web search (affiliation read in the PDF) | 25 abs+PDF fetched | 12 | arXiv never answered 403 |
| News / external coverage | web search x2 | 0 | no news items found for IIITN research (iiitn.ac.in news is SPA-only); share moved to faculty/department pages |

Web-search strings used: `"Indian Institute of Information Technology Nagpur" arxiv.org abs`; `IIIT Nagpur researchers paper published news`; `"IIIT Nagpur" OR "IIITN" Tembhurne OR Diwan OR Penurkar OR Digalwar arxiv`; `"Indian Institute of Information Technology, Nagpur" Nidhi Lal OR "Pooja Jain" ... arxiv`; `"IIIT Nagpur" Ghivela OR Parate ... arxiv`; `"iiitn.ac.in" arxiv paper author email` (productive: Goel, Tembhurne papers); `... students faculty research paper accepted conference journal 2024 2025`; `"Indian Institute of Information Technology, Nagpur" 2017 paper IEEE OR Springer ...`; `arxiv ... bt21 OR bt22 ... "@iiitn.ac.in"` (productive: Karmore, Tembhurne COVID, Patrikar/Parate); `arxiv "IIIT Nagpur" Pooja Jain OR ...` (nothing). Candidate arXiv papers checked and rejected (other institutes): 2105.02935, 2308.00943 (IIIT Sri City), 1803.09402 (IIIT Sri City), 2507.17759 (VNIT), 2511.12468 (IIIT Delhi), 2312.05589, 2406.01608 (VIIT), 2601.08319, 2510.26681, 2212.09284 (IIIT-H), 2307.03948.

## Counts
125 papers: faculty_page 82, arxiv 12, annual_report 20, dept_page 11. Confidence high 12 (arXiv, affiliation printed in the PDF), medium 113. Types: journal 77, conference 28, preprint 12, book-chapter 5, other 3. DOI on 41 (33 %), all printed on the source.
Mix against plan (50/15/15/10/10): faculty 66 %, dept 9 %, annual report 16 %, arXiv 10 %, news 0 %.

## Department x year
| Dept | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| CSE | 0 | 0 | 0 | 13 | 7 | 5 | 14 | 3 | 3 | 5 |
| ECE | 0 | 0 | 3 | 2 | 8 | 11 | 7 | 4 | 1 | 3 |
| BS (incl. humanities) | 4 | 2 | 4 | 5 | 0 | 0 | 7 | 10 | 3 | 1 |
No 2016 paper: 2016 is the opening year (campus at BSNL RTTC) and every 2016 candidate (Kolte/Daryapurkar Thin Solid Films, Ceramics Intl) is in the person's joining year without IIITN affiliation visible on the listing. 2018 has two rows for the same reason.

## Tenure rule applied
Joining years come from the roster (NIRF/first archived list, so upper bounds; Tembhurne, Pooja Jain, Ansari, Digalwar verified on their own 2020 page: "2018 / 2018 / July 2019 / 2019 to till date"). A paper counts only if year > joining year (medium), unless the affiliation is printed on the paper (arXiv, high). Dept and annual-report listings are never `high`. The `iiitn_author` field names the first-named IIITN author; per-person cap 8 counted against it (max reached: Jain, Ansari 8; Tembhurne 7; Diwan 7; Pandhare 7).
Two cap relabels: "Improvised light weight deep CNN ... U-Net" is credited to student S. Arvind, "Script independent text segmentation ..." to Parul Sahare.

## Rejected candidates and why
* Pre-tenure or joining-year items on faculty pages (the majority of profile content): Naresh Nedunuri (joined 2022; 2013-2022 list, 37 items), S. Janbandhu (2023; 20 items, only 2024-26 kept), Nishant Namdev (2022), Shankar Bhattacharjee (2022; 17 items, only 2024 kept), Mayank Thacker (2022; all 2014-2021), Anil Kushwah (2022; 2019-2022 items), Vasundhara Rathod (2024; 2022-2024), Santosh Sahu (2023; 2017-2023), Amol Bhopale (2023), Mangesh Kose (2024), Preeti (2023), Chakole, Pikle, Vrinda Yadav, Kaushlendra Sharma, Dhengre (all 2022 joiners with earlier items), Majumdar (2022; 2015-2020 items), Penurkar OPPRES/Max-Util (2015-2017, joined 2019), Pooja Jain 2016-2017, Ansari 2016-2017, Digalwar 2013-2018, Tembhurne 2016-2018 (his 2018 items are in the joining year), Nidhi Lal 2019 items (joining year), Diwan CIT 2019 (joining year), Peshwe 2019-2020 items (joined 2020), Sahare JAIHC 2020 (joined 2020), Ghivela 2019-2021 items (joined 2021), Goud 2019-2021 items (joined 2021).
* Zedacross (Hadoop fault prediction): Tapan Jain's page gives 2020 (IJICS 12(2-3)), Pooja Jain's old page gives Oct 2017, conflict, dropped.
* LARNet (annual report 2020-21): title truncated, no DOI.
* Annual report 2023-24 items whose year is not printed (only "2023-24"), e.g. Wajgi 3D localization, Khuraijam Singh book chapter, Digalwar/Ghode ACM paper, Pooja Jain LNNS paper: not included. Several Hindi annual reports (2017-18 H) list 2016-2018 papers but titles are unreadable.
* Mentor faculty from VNIT (Deep Gupta, Kurhekar, Dhabu, Ashish Tiwari etc.) and VNIT adjuncts (Bhurane, Kothari, Parlewar): their papers are VNIT work; only included where an IIITN-tenured co-author carries the entry.
* CSE faculty page `cse.iiitn.ac.in/Research`: connection error. `iiitn.ac.in/research/publications` and `/pub-dept-*.php`: SPA shell with no data.

## Why 125 and not 150
Accessible, dated, tenure-valid material ran out: the new site exposes only ~50 publication entries (most pre-tenure), the old department pages end in 2020-2021, 16 of 18 annual-report PDFs have no text layer (OCR unavailable) or garbled Hindi text, and external news does not exist. Per the brief, stopped when sources were exhausted instead of relaxing the tenure rule.

## Known biases
* Medium confidence dominates (91 %); rows rest on the tenure rule, not on a printed affiliation, so a few may have been written elsewhere (e.g. work finished before joining but published later). Joining years are upper bounds, which biases toward excluding.
* CSE-heavy in 2020 (Wayback pages with explicit lists) and 2023 (annual report), thin for 2018-2019, 2021 BS, 2025.
* Faculty with rich profile text (Tembhurne, Diwan, Jain, Ansari, Pandhare, Lal) are over-represented relative to those with empty profiles (about 40 of 64 profiles list nothing); half of the IIITN faculty are therefore absent.
* Student-led papers appear only through annual reports, arXiv and faculty lists. Former faculty present: Lal, Singh, Baghel, Kamble.
* Wayback copies of the institute's own pages were used as discovery pages (live pages are an SPA); Wayback slot was used for 15 fetches.
* arXiv sample is tiny (12) and dominated by Goel (5, mathematics) and Tembhurne (2).
