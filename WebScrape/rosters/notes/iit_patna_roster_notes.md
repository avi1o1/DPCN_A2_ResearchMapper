# IIT Patna roster notes (iit_patna)

Built 2026-10-28. Scripts/caches: scratchpad `work/iit_patna_roster/code/` (wbplan, wbfetch, wbparse, nirf_old, cluster, final, emit, orcid_off) and `.../data/`; the golden-set agent's saved pages `work/iit_patna_golden/data/` were reused for the live department data.

## Size check and per-unit counts against NIRF (early)
* NIRF 2025 data submission (Feb 2025): 275 faculty-table rows; 271 "currently working". Of those, 158 are Regular with a faculty designation (Assistant 81, Associate 60, Professor 14, Associate Dean 6, Dean 1) plus 1 ad hoc Director. The rest (47 Regular + 47 Visiting + 11 Ad hoc + 7 Other with designation "Other"/blank) are research staff, postdocs, visiting scholars etc.; they were NOT added (see gaps).
* Roster current rows: **162** (live department pages 162 entries incl. two people who appear in two units, plus Director T N Singh, minus none). 151 current rows carry a NIRF 2025 source; the other 11 joined after Feb 2025 or are spelt differently. Difference to NIRF (158+1): +3; consistent (new joiners 2025-26 minus 3 leavers).
* NIRF carries no unit, so unit-level comparison is against archived department pages: ME live 25 vs Wayback Mar 2026 25; CSE 18 vs 2024 19; CEE 16 on live vs 21 on Wayback Jul 2025 (5 people missing from live = marked former, see below); EE 23 vs 23 (Aug 2024); Physics 19 vs 21 (2024); Math 15 vs 15; Chem 13 vs 15 (2024); CBE 11 vs 12; Met 13 vs 11; HSS 9 vs 10.
* Rows: 217 = current 162, former 50, visiting 4, adjunct 1. Per unit (current/former/other): CBE 11/4/2; Chemistry 13/0/0; CEE 17/7/0 (incl. Director T N Singh listed on the CEE page); CSE 18/0/1 adjunct; EE 23/2/0; HSS 9/0/1; Math 15/2/0; ME 25/0/0; Met 12/0/1; Physics 19/2/0; unit blank (NIRF-only former) 0/34/0.

## Sources and endpoints
* Live site `https://www.iitp.ac.in/departments/<dept>` (Next.js; faculty JSON embedded in the page, saved by the golden agent: name, designation, email, profile link, experience). 10 academic departments; heads listed at `/administration/leadership-and-governance/heads-of-department`. No institute-wide faculty list exists on the new site; `/research/people` is the R&D office only.
* NIRF data submissions, all through Wayback because the live links are 404: 2016 (names/designation only, no dates; the file `NIRF_Engineering_Submitted.pdf`, header date 28-11-2016), 2018 overall (`images/pdf/nirf/NIRF_Overall-05-12-2018.pdf`, joining/leaving dates), 2022 overall (`NIRF-Overall-Data-2022.pdf`), 2025 overall (`NIRF_IITP_overall_submitted.pdf`). NIRF 2017, 2019-2021, 2023, 2024 and 2026 data are not archived/linked (CDX query for any iitp.ac.in URL containing NIRF/nirf found only these). The ranking page `/student/ranking` links only the 2025 set.
* Wayback CDX over `iitp.ac.in/index.php/*` filtered to people/faculty pages -> 89 department faculty-list snapshots (last capture per URL per year), 2016-2026, across three site generations (2016-17 `departments/engineering/.../people/faculty.html`; 2018-21 `people-N/faculty` on Joomla; 2022-26 `people-N/faculty`, `peop-dept-menu`, `people-dept-menu`, `people-phy-menu`, `che-dept-menu`, `people-10/cee-faculty`, `people-2/ee-faculty`). Unit mapping: people-6 ME, people-8 Met, people-10 CEE, people-12 CBE, people-2 EE, people/faculty CSE, people-dept-menu Math, peop-dept-menu HSS, people-phy-menu Physics, che-dept-menu Chemistry. HTML comments are stripped (hidden entries are not evidence). `people-center-menu` (centres) skipped.
* Offline ORCID index `iit_patna_orcid_index.tsv`; no live ORCID API calls.
* Not used: annual reports (2016-17..2023-24 PDFs are mostly truncated/unreadable per the golden notes).

## Former faculty and tenure years
* Former = present on a dated Wayback list or NIRF table 2016-2025 and absent from the live 2026 department pages (and not on the Mar 2026 snapshot). FIRST = earliest NIRF joining date (earliest of 2018/2022/2025 tables) else first archived appearance; LAST = NIRF leaving year if given, else last year with evidence.
* **Gaps in years:** snapshots exist only for 2016-17, 2018-19 (CBE, HSS), 2020-22, 2023-26; NIRF only 2016/2018/2022/2025. So LAST for people without a NIRF leaving date can be early by up to ~2 years (e.g. 2023 snapshots then 2024+). 25 former rows (blank unit) are evidenced only by the 2016 NIRF names table ("2016-2016"): they are absent from NIRF 2018 and from later pages, so they left in 2016-17; exact year unknown. Their unit is blank (NIRF has no unit).
* Five CEE people (Pradipta Chakrabortty, Sourav Gur, Vishal Deshpande, Manoj Kumar Yadav; plus Director T N Singh kept current) were on the Jul 2025 CEE page and NIRF 2025 but are missing from the 2026 live department page. Treated as former with LAST 2025 (the live page wins); this could be an incomplete live page. Amarnath Hegde (NIRF leave 27-06-2023), Baadiga Ramu (leave 31-10-2023) as per NIRF.
* Asif Ekbal is listed on the live CSE page as "(On-Lien)" although NIRF 2025 gives leaving 27-04-2024 (moved to IIT Jodhpur): kept `current` per the live-page tie-break.
* Pramod Kumar Jain (NIRF 2022, Dean/Director, 30-06-2020 to 09-09-2021) former; Hemanta Kumar Kisan 2023 (leave 09-03-2023); Ashok Singh Sairam leave 07-08-2017; Aneek Adhya 06-07-2017; R Prabhu 25-08-2017; Ritwik Ghoshal 05-05-2018; Divyendu Mukherjee leave 29-06-2018 (all NIRF 2018).
* Stale snapshots: Ashish Kumar Upadhyay and Prashant Kumar (Physics) were still on 2022 pages after NIRF 2022 leave dates (2020, 2021); NIRF leave year used. The 2025 NIRF "Prashant Kumar, Visiting, Other" was judged a different person and ignored.

## joining_year
174 rows (all from NIRF join dates, earliest of tables; may be regularisation dates; not guessed). Blank for wb-only/2016-NIRF-only people and for the two same-name pairs below.

## Ambiguous people and decisions
* Om Prakash (Civil asst. prof. vs Mathematics professor) and Amit Kumar Verma (Civil vs Mathematics): two different people each; NIRF has no unit so joining_year left blank for all four.
* Prolay Das: archived CBE pages 2018-19 list him, live page Chemistry: one row, Chemistry, current (Chemistry page 2016+; CBE listing treated as page error).
* Dibyendu Mukherjee (CBE, visiting professor 2017) vs Divyendu Mukherjee (NIRF 2018 Professor, 2016-12 to 2018-06): possibly the same person, kept as two rows.
* Name variants merged by hand: Surbrata/Subrata Kumar, Chetan kumar/Chetankumar Patel, Kailash Chandara/Chandra Ray, Naveen Kumar Nischal/Nishchal, Md Lokman Hakim Choudhury/Chaudhury, Balendu Bhooshan/Bhushan Upadhyay, Rajiv Misra/Mishra, Raghavan K Easwaran/Kollengode Eswaran Raghavan, Sudhanshu/Sudhansu Sekhar Panda, Yogesh Mani Tripath(i). Live-page typos kept as printed (e.g. "Kailash Chandara Ray").
* Visiting/adjunct people: Prashant Jha (visiting faculty HSS 2020-2025), B B Agrawal (visiting, Met 2022-23), Dibyendu Mukherjee, Debatosh Datta (visiting CBE 2016/17), Eugenio Vocaturo (adjunct CSE 2024). Priyanka Gupta (CBE, NIRF 2025 ad hoc, 2023-2025) former faculty with unknown designation.
* Director T N Singh: current, designation Director, unit shown on CEE page.

## Identifiers
ORCID 118 rows, all via the offline index (employment/invited-position record naming IIT Patna with a faculty-type role, full-name match, and unit compatible): affiliation-record route 118; institute-page route 0; live API 0. Ambiguous (several candidate iDs, left blank): Abhinoy Kumar Singh (6), Samrat Mondal (2). ORCID lookup pending: none attempted. Email 161 rows (live pages; expanded to @iitp.ac.in only if the page printed the full address), profile_url 91 (institute profile pages), homepage 39 (personal pages). Google Scholar/DBLP/Scopus/IRINS: 0 (not printed on pages used).

## Known gaps
* 110 NIRF rows (designation "Other"/blank: research staff, scholars, visiting scholars, some foreign academics on "Visiting" association) were excluded as not faculty; some genuine visiting faculty (e.g. Adam Jatowt, Agostino Cortesi) may be among them.
* No NIRF 2017/2019-21/2023-24/2026 and no annual reports: people who joined and left between archive dates (esp. 2018-2021) may be missing.
* The 2016 NIRF table gives no unit; 34 former rows have blank department. Pages for other units (Computer Centre, Centre for Endangered Language Studies, Earthquake research) have no faculty lists.
* Live department pages (162 entries) are the only 2026 evidence; faculty of the 2026 pages absent from them would be mis-labelled former.
