# Golden set IIIT Naya Raipur: lab notebook (operator Arihant Tripathy, 2026-10-29)

Output: `golden/golden_iiit_naya_raipur.csv`, 126 rows (target 150 NOT reached, see shortfall). Sources {'annual_report': 80, 'faculty_page': 30, 'arxiv': 16}; confidence {'medium': 111, 'high': 15}; DOI printed on source for 36 rows (28%); first-named IIIT-NR authors: 33.

## Sources and yield
* Live iiitnr.ac.in fails TLS (DEAD:SSLError); all institute pages read from Wayback copies (2022-03 snapshots, three 2026 ones).
* Institute yearly "Publications 2015..2021" pages (/content/publications-2015 .. -2020, /content/research-publications = 2021): 7 pages, 267 list entries; found/visited/used: 7/7/~80 rows. Labelled `annual_report` (institute report; no per-paper affiliation) and `medium`.
* Faculty profile pages (node/NNNN, "Selected Publications"): 41 roster profile URLs tried, 22 with lists (2022-03 mostly; Agrawal 2026-08, Chaube 2026-02, Srinivasa 2026-03), 15 newer-joiner nodes (3001-3513) 404 in Wayback, 4 old leavers' pages without lists. ~510 list entries, ~30 rows kept after de-duplication against institute pages (a paper on both is credited to the institute page).
* Annual Report 2022-23 (cached by roster agent): counts only (84 publications in 2022-23, 242 journal papers in text) and a patent table, no publication list: share moved to faculty/institute pages, as per brief.
* arXiv (abs/PDF page 1; found via web search restricted to arxiv.org): searches "IIIT Naya Raipur" + DSAI / ECE / CSE / faculty names. 18 candidate IDs fetched, 16 kept; rejected 2302.14635 (no IIIT-NR affiliation on page), 2305.14389 and 1904.10354 (fetch failed, ConnectionError). arXiv never answered 403; fetches were slow because of the shared 5 s slot.
* News/web: searches for institute news / research highlights returned only other institutes; one Hitavada piece (2021) says Ruhul Amin has been at IIIT-NR since August 2017 (his roster joining year is blank), not used for rows. No news share.
* Web searches used (summary): 'arxiv "IIIT Naya Raipur" Data Science and Artificial Intelligence 2024'; 'arxiv "Naya Raipur" IIIT Department of ECE OR CSE 2022 2023 2025'; '... Mallikharjuna Rao OR Shailesh Khapre OR Avantika Singh OR Vijaya J OR Srinivasa K G'; '... Ruhul Amin OR Vinay Kumar OR Kavita Jaiswal OR Srinivas Naik OR Satyanarayana Vollala'; math/physics faculty names; 'IIIT-NR research highlights news'.

## Method
Entries parsed by script; title taken only where printed in quotes or APA style (entries without a recoverable title were skipped, a bias against plain-format lists). Author = earliest roster name matched in the entry; tenure rule: year strictly after roster joining_year (NIRF/archive upper bound), otherwise rejected. Spread-evenly sampling newest-first, cap 8 per first-named author. Patents excluded. DOIs only as printed in the list entry.

## Coverage (department x year)
| dept | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CSE | 0 | 1 | 4 | 6 | 4 | 9 | 4 | 3 | 0 | 0 | 31 |
| DSAI | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 1 | 1 | 2 | 7 |
| ECE | 1 | 1 | 9 | 12 | 22 | 14 | 0 | 0 | 1 | 0 | 60 |
| SHM (English) | 0 | 0 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 4 |
| SHM (Management) | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| SHM (Mathematics) | 0 | 0 | 6 | 3 | 5 | 0 | 0 | 1 | 0 | 0 | 15 |
| SHM (Physics) | 0 | 0 | 1 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 8 |

## Shortfall and biases
* 126 of 150: the institute stopped publishing yearly lists after 2021, newer faculty profiles (joined 2021-2024: DSAI, new SHM, Kavita Jaiswal etc.) are not archived, and no annual report lists papers. Years 2016-2017 are thin (institute lists small; many early faculty joined 2016-17 so only later years qualify under the strict tenure rule). 2026 has no row.
* ~63% of rows come from the institute yearly lists (above the 15% planned share); faculty pages ~23%; arXiv ~12%.
* Heavily ECE/VLSI/antenna weighted because those faculty keep long lists; Humanities, Management, Physics and Math few rows. Former faculty included: Debanjan Das, Vivek Tiwari, Venkanna U, Srinivas Naik N, Kuldip Singh Patel. Student/postdoc-led papers only via arXiv.
* Rows from lists are `medium` (no affiliation visible); only arXiv rows with printed affiliation are `high`. 2306.08314 is `medium` (no affiliation on page 1).
* Some list entries (pre-joining co-authored work of other institutions) cannot be excluded beyond the joining-year rule; sec/venue strings are as printed and sometimes truncated (blank venue for a few).
* Rejected: entries with joining year >= paper year (e.g. 2015-2017 items for later joiners), Ruhul Amin entries (no joining year, no on-page evidence), Pradeep Sinha entries without parsable titles, patents.
