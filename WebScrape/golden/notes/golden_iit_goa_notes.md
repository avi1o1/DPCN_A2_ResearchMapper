# Golden set: IIT Goa (iit_goa), 2016-2026, lab notebook

Built on 2026-10-26/27 by an independent sub-agent. No bibliographic API was used for discovery: no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite or the arXiv API. `WebScrape/iit_goa.json` and the other pipeline outputs were not read. Every URL went through the shared fetcher `scratchpad/tools/polite_get.py` (371 fetch calls, logged in `work/iit_goa_golden/data/fetch.log`); downloads are in `work/iit_goa_golden/data/`, scripts in `work/iit_goa_golden/code/` (`merge.py` builds the CSV; row transcriptions are in `fac_rows1.py`, `fac_rows2.py`, `ar_rows.py`, `other_rows.py`; `people.py` holds the tenure table). arXiv was never blocked (no ARXIV_BLOCKED).

**Result:** 287 distinct papers in `golden/golden_iit_goa.csv` (target 300; see "Shortfall" below).

| evidence_source | rows | confidence | rows with DOI |
|---|---|---|---|
| faculty_page (institute profiles + 3 personal homepages) | 190 (66 %) | all medium | 25 |
| annual_report (R&D Brochure 2021 + Annual Reports 2018-19, 2019-20) | 42 (15 %) | all medium | 0 |
| dept_page (Chemistry and Physics publication pages, 2 lab sites) | 16 (6 %) | all medium | 0 |
| arxiv (PDF affiliation checked) | 28 (10 %) | all high | 12 (journal DOI shown on the arXiv abs page) |
| news (institute Awards & Recognition page, homepage "Latest Research Publications") | 11 (4 %) | 10 high, 1 medium | 0 |
| **total** | **287** | 249 medium / 38 high | 37 (13 %) |

Types: journal 207, conference 44, preprint 30, book-chapter 5, book 1 (an edited LNCS proceedings volume). 65 distinct IIT Goa people (incl. 5 students/postdocs); at most 8 rows per person (cap reached by 11 people).

## Departments x years coverage
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Chemical and Materials Engineering |  |  |  |  |  |  | 3 |  | 3 | 1 | 1 | 8 |
| Chemistry |  |  |  |  | 4 | 1 | 3 | 3 | 4 | 8 | 8 | 31 |
| Computer Science and Engineering |  |  |  | 9 | 4 | 6 | 5 | 2 | 5 | 4 | 3 | 38 |
| Mathematics |  |  |  | 1 | 1 | 3 | 7 | 5 | 3 | 6 | 9 | 35 |
| School of Electrical Sciences |  |  |  | 6 | 12 | 10 | 6 | 7 | 7 | 7 | 2 | 57 |
| School of Humanities and Social Sciences |  |  |  | 1 | 2 | 1 |  |  | 3 | 3 |  | 10 |
| School of Mechanical Sciences |  |  | 2 | 6 | 10 | 5 | 4 | 5 | 10 | 11 | 11 | 64 |
| School of Physical Sciences |  |  |  | 6 | 3 | 2 | 4 | 5 | 7 | 4 | 13 | 44 |
| **all** |  |  | 2 | 29 | 36 | 28 | 32 | 27 | 42 | 44 | 47 | 287 |

Units: IIT Goa's "School of Mathematics and Computer Science" is split into its two programmes (Mathematics; Computer Science and Engineering) and the "School of Chemical and Materials Sciences" into Chemistry and Chemical and Materials Engineering, as on the institute faculty list. The School of Interdisciplinary Life Sciences has no own faculty (members are listed under other schools); its R&D-brochure entries are attributed to the author's home school. Materials Engineering (B. K. Mishra, Satyaprakash Ahirwar) is folded into School of Mechanical Sciences / Chemical and Materials Engineering as on the profile URLs (SMS-faculty-profile ... exp=MS).

**2016-2018 are (almost) empty.** IIT Goa started on 30 July 2016; almost all faculty joined in 2017-2018 (own pages; Wayback captures of the old `faculty_page.php?id=N` pages start Feb 2018). The tenure rule (year strictly greater than the joining year, joining year rejected unless affiliation visible) therefore removes nearly all 2016-2018 papers; the 2018-19 annual report's 2018 entries were all rejected for this reason (they demonstrably include pre-joining work, e.g. Bidhan Pramanick's 2018 IIT Kharagpur microneedle paper, Sujit Sahoo's 2018 NTU Applied Optics paper). The two 2018 rows are B. K. Mishra (joined 2017). No arXiv preprint with an IIT Goa address from 2016-2018 was found by web search.

## 1. Faculty pages, source "faculty_page"
* Roster: `https://iitgoa.ac.in/facultyprofile/` lists 84 profile pages (`<X>-faculty-profile/?uid=<id>`), incl. adjunct, visiting, former-faculty stubs (Sharad Bhartiya, Shobha Madan) and the Director. All 84 were fetched (200). The pages are static WordPress HTML with sections "Professional Appointments" and "Recent Publications" (free text, hand-entered, usually a "selected" list, often stale).
* Parsing: `code/sections.py` splits each profile into sections; `code/select.py` takes the "Recent Publications" entries, finds the entry year (largest 1990-2027 year in the entry), drops entries with year <= J or marked submitted / under review, and takes up to 5 entries spread evenly over the remaining list (list order, not the first 5). Titles/venues were then transcribed by hand from the selected entries. Continuation lines and title-less entries (e.g. Kanungo, PRB 102 174401) were replaced by the next eligible entry; patents (Priyabrata Sahoo) and poster abstracts (Arindam Das, ComFlu 2022 poster) were skipped.
* Faculty personal homepages linked from the profile ("Personal Page") were used where the profile list was empty or stale: Harpreet Singh (`iitgoa.ac.in/~harpreet/publications.html`, 5 rows), Sharad Sinha (`sharadsinha.wordpress.com/publications/`, 4 rows), Bidyadhar Subudhi (`iitgoa.ac.in/~bidyadhar/?var=Publication`, 4 rows, only 2021 entries taken because the date he went on lien to NIT Warangal is not stated). Fetched but unusable: ~sreejithav (empty), ~sudakshina (only 2012-2017 papers, before tenure), ~ravi, ~clint, prasad-research.github.io (no list), nehakaranjkar.github.io (no years), nrjcs.github.io (Niraj Kumar joined Jul 2024; no list).
* Tenure rule (b): J from the person's own page ("Professional Appointments") where stated; otherwise from Wayback: the first capture of the person's old institute profile `faculty_page.php?id=N` (CDX listing + earliest snapshot of each of 49 ids) or the first `facultyprofile/` snapshot that lists the uid (snapshots 2021-11, 2022-12, 2023-12, 2024-12). Wayback dates are upper bounds on joining. A paper is accepted only if year > J. Sharad Sinha left IIT Goa Aug 2021 and returned Sep 2023 (own page), so his 2022-2023 papers were excluded. The tenure source is quoted in every row's `notes`.
* Yield: 84 profiles visited; 677 dated entries on profiles of faculty with a known J: 318 rejected as outside tenure (year <= J), 42 had no year. 15 people had no in-tenure profile entry (amal, arpita, bidhan, bidyadhar, haridas, harpreet, jhuma, krishna, mantu, niraj, satyanath, sdutt, seenivasan, shitala, sudakshina); most of them are covered by other sources. People with no row at all: Arpita Korwar, Satyanath Bhat, Sunil Dutt, Krishna Kumar, Niraj Kumar, Keval Ramani, Selvaraj Seenivasan, Ponnulakshmi V K, Anirudha Ambekar (only as co-author), Vijay Victor (IIT Roorkee until Jun 2026), Abhijeet Giri (joined Sep 2025; 1 pre-joining entry), Jhuma Sannigrahi appears via arXiv only.

## 2. Annual reports / institute reports, source "annual_report"
* `https://iitgoa.ac.in/annual-report/` links English reports 2016-17 to 2019-20 as turn.js flipbooks (`activity/annual-report/english-YY-YY/index.html`, pages are JPEG images, no text layer) and bilingual 2020-21 to 2024-25 flipbooks. No OCR tool is installed; pages were read visually (image files fetched through the fetcher, cropped with PIL).
* R&D Brochure 2021 (`iitgoa.ac.in/wp-content/uploads/RD_Brochure_2021.pdf`, linked from the Research menu): "Research Publications" pp. 45-54, 156 entries grouped by school (2019-2021). The text layer uses a broken font encoding (pdftotext gives garbage), so the 10 pages were read visually. Sampling: about 3 entries spread through each school's list, skipping duplicates and people at the cap; 34 rows kept. R&D Brochure 2022 (`RDBrochure2022.pdf`) has only publication counts per school (no list): not usable.
* Annual Report 2018-19 (flipbook, 100 pages): publication pages located with a contact sheet of pages 25-58 (offset +4 to the printed page numbers): flipbook pp. 29 (SES), 34 (SHSS), 40 (SMCS), 47-48 (SMS), 52 (SPS). Most entries are 2018 and were rejected under the tenure rule (joining year); 7 in-tenure 2019 entries kept (incl. one edited LNCS volume, ICLA 2019).
* Annual Report 2019-20 (flipbook, 118 pages, pages 20-60 fetched): publication pages 29 (SCBS), 33-37 (SES), 41 (Maths), 46 (CSE), 52-53 (SMS). Nearly all entries duplicate rows already taken or belong to people at the cap; 1 new row (Saumya Bajpai, AMC 2020). Reports 2016-17, 2017-18 and 2020-21 to 2024-25 were not read (image-only, and the in-tenure share of their lists is small for 2016-18).
* Confidence: medium (report listing alone is not affiliation evidence, per the pilot decision); every row also satisfies the tenure rule. Rejected: Pydi Ganga Bahubalindruni (former faculty, first seen 2019-03; all her listed papers 2019), Harpreet Singh's 2020 MMS paper (first seen 2020-11), Kuntal Deka (former, first seen 2019-02; 2018-19 entries), T. S. Rathore (visiting professor, no joining date), R. S. Prabhu Gaonkar (on deputation, first seen 2021-04; entries 2019-2021), Dhanya Rajendran (former, 2018 papers), Anirudha Ambekar and Thaseem Thajudeen 2019 entries (joining year), all 2018 entries.

## 3. Department and lab pages, source "dept_page"
* `iitgoa.ac.in/chemistry-journal-publications-book-chapter/` (Chemistry, ~100 entries 2019-2026, by year): 13 rows, entries spread over the years, preferring people under the cap.
* `iitgoa.ac.in/physical-sciences-journal-publications-book-chapters/` (Physics, lists up to 2023 for Das, Kanungo, Kumar, Wasnik): 1 new row; the rest are duplicates or people at the cap (Santosh K. Das, Sudipta Kanungo).
* `iitgoa.ac.in/journal-publications-book-chapter/` (older chemistry list, 3 entries, all duplicates), `iitgoa.ac.in/computerscience-research/` (research areas only), `compurterscience-news-events/` (news items without paper titles): no rows.
* Lab sites linked from profiles: MitraLab (`rajamitra28.wixsite.com/mitralab/publications`, 1 row), E. S. S. Iyer group (`sites.google.com/site/essiyer/publications-1`, 1 row); fetched but no new in-tenure rows: SAIL (Kedar Joshi), Narayan lab, HK research group (Haridas Kar), ACRL (Krishna Kumar, joined 2024), Nandi lab.
* `iitgoa.ac.in/Research_Publications/` is an institute publication database behind a POST search form (needs a login for some views); the fetcher only does GET, so it was not used. `iitgoa.irins.org` (linked as "Faculty Research Profiles") is IRINS: forbidden, not opened.

## 4. arXiv PDFs, source "arxiv"
* arXiv listing search on the website was not used (robots.txt disallows /search). Discovery by web search restricted to arxiv.org, strings:
  * `"Indian Institute of Technology Goa" arxiv`
  * `"IIT Goa" arxiv.org School of Mathematics and Computer Science preprint`
  * `"Indian Institute of Technology Goa" Ponda 403401 arxiv`
  * `"Indian Institute of Technology Goa" Farmagudi arxiv physics`
  * `"IIT Goa" "School of Electrical Sciences" arxiv`
  * `"Indian Institute of Technology Goa" computer science arxiv 2019 2020 2021`
  * `"Indian Institute of Technology Goa" arxiv 2017 2018 preprint`
  * `"IIT Goa" OR "Indian Institute of Technology Goa" arxiv graph algorithms theory`
  * `"Indian Institute of Technology Goa" arxiv chemistry OR materials OR chemical engineering`
  * `"Indian Institute of Technology Goa" arxiv mathematics operator theory OR number theory OR PDE`
  * `"IIT Goa" "School of Mechanical Sciences" arxiv`
  * `"Indian Institute of Technology Goa" arxiv machine learning OR networks OR security 2022 2023`
  * `"Indian Institute of Technology Goa" arxiv economics OR humanities OR social`
  * `"IIT Goa" arxiv "School of Physical Sciences" 2020 OR 2021 OR 2019 heavy quark`
  * `"Indian Institute of Technology Goa" arxiv hep-ph cosmology neutrino`
  * `"IIT Goa" arxiv formal languages automata logic`
  * `"Indian Institute of Technology Goa" arxiv control systems power electronics robotics`
  * `"Indian Institute of Technology Goa" arxiv statistics probability optimization`
  * `"IIT Goa" arxiv computer vision deep learning image`
  * `"IIT Goa" arxiv "School of Physical Sciences" spectroscopy OR optics OR photonics`
  * `"Indian Institute of Technology Goa" arxiv 2023 cs`
  * `"IIT Goa" arxiv "School of Chemical and Materials Sciences" OR "School of Interdisciplinary Life Sciences"`
  * `"Indian Institute of Technology Goa" arxiv mechanical fluid flow simulation 2020 2021 2022`
  * `"Indian Institute of Technology Goa" arxiv quantum OR condensed matter 2019 2020 2021`
  * `arxiv "IIT Goa" Mathematics operator theory OR Hardy OR Dirichlet "School of Mathematics and Computer Science"`
  * `"Indian Institute of Technology Goa" arxiv cs.LO OR cs.DS OR cs.CC automata complexity`
  * `"IIT Goa" arxiv electrical "School of Electrical Sciences" wireless OR power OR VLSI 2023 2024 2025`
  * `"Indian Institute of Technology Goa" arxiv economics OR finance OR "Humanities and Social Sciences" 2024 2025`
* 38 candidate ids; abs page + PDF of each fetched (76 arXiv requests, all 200; fetcher gap 5 s plus 10 s sleep between requests, so >= 15 s as robots.txt asks). Affiliation searched in the first 3 PDF pages (`pdftotext -l 3`), else the full text.
* Rejected: 2004.00256 (Goa University, not IIT Goa), 2404.09215 (IIT Madras), 2404.13890 (no IIT Goa author); per-person cap (Santosh K. Das already had 7 rows): 2203.06712 (duplicate of profile row anyway), 2208.13440, 2306.07966, 2507.22620, 2606.18854, 2607.22403; 2503.02871 (Arindam Das at cap; preprint version of his Langmuir 2025 profile row).
* Accepted 28 (6 of them also appear as faculty-page/report entries, so the arXiv row carries the faculty-page/AR listing in `notes`). Non-faculty-led: 2111.12746 (Svara Mehta, ME student), 2304.04003 (Jai Prakash, M. Y. Jamal, postdocs), 2501.07240 (Ankit Kumar Panda), 2607.04420 (Soumyadip Dey), 2506.19792 (Kartik Anand, student; iitgoa.ac.in e-mail), plus Jhuma Sannigrahi (Ramanujan fellow) x3. 2610.05914 (Karthick Babu): affiliation is in the arXiv HTML version (seen in web search) and the PDF acknowledges an "IIT Goa Start-up Grant". Year = arXiv v1 year. DOI recorded only where the arXiv abs page prints the journal DOI (12 rows).

## 5. News and web, source "news"
* `iitgoa.ac.in/awards-recognition/` (2018-2026 items): every item mentioning a paper was read; 10 rows from items that name the paper title and state the IIT Goa authors (best-paper awards, travel grants). These are institute statements that the authors were at IIT Goa: confidence high.
* Institute homepage "Latest Research Publications" box (8 papers, 2024-2026): 7 duplicate other rows; 1 new row (medium, listing only, tenure checked).
* Research highlights page (`/research-highlights/`, 5 items: COVID e-book, airborne virus transmission, VoterDost chatbot, bamboo equipment, oxygen concentrator): only the airborne-virus item is a paper (Santosh K. Das, at the cap). `/news/` ("IIT Goa in the news"), `/newsletter/` (issue list fetched, flipbooks not read), physical-sciences and CSE news pages: no paper titles usable.
* Rejected news items: TinyML INDICON 2022 best paper (Sharad Sinha, outside his tenure gap 2022-23), Nature Microsystems & Nanoengineering Dec 2018 (Pramanick, joining year, IIT Kharagpur co-authors), Applied Optics "Single-shot large field of view imaging..." (Sahoo, 2018), IETE 2017 best paper (Rathore, no title), MARSS 2023 best student paper (no title), KM3-230213A JCAP 2025 (Mahapatra, joining year 2025).
* External web search for press coverage: `IIT Goa researchers study published journal`; `"IIT Goa" professor research paper published heraldgoa OR navhindtimes OR thegoan`; `IIT Goa annual report pdf publications list journal` (site iitgoa.ac.in); `iitgoa.ac.in publications department journal publications conference`; `iitgoa.ac.in/~ publications lab group`; `iitgoa.ac.in news paper published journal cover article research group`; `IIT Goa annual report pdf wp-content uploads "Annual Report"`. They returned institute pages (used above), Nature Index, unrelated institutions (Goa University, BITS Goa, Goa Institute of Management) and no press article naming a paper: no "websearch" rows. Web-search-found arXiv papers are labelled "arxiv".

## Shortfall and source mix
* 287 rows, not 300: the in-tenure pool is small (young institute, ~85 faculty, most lists stale or pre-joining; 11 people hit the cap of 8). Faculty pages are 66 % (target 50 %) because the annual reports are image-only flipbooks, the R&D brochures cover only 2019-2021, department publication pages exist only for Chemistry and Physics, and external news coverage of papers does not exist.

## Known biases
* **Recency:** 85 % of rows are from 2020-2026; 2016-2018 has 2 rows (see above). Faculty "Recent Publications" lists favour recent work.
* **Survivorship:** profiles exist only for current faculty; former faculty appear only through reports (Pydi Ganga Bahubalindruni, Kuntal Deka, Dhanya Rajendran were all rejected by the tenure rule), so the set has essentially no former-faculty papers.
* **Affiliation:** 87 % of rows are medium (tenure-based). Faculty lists, reports and department pages include pre-joining and collaborator-institution work (e.g. Sujit Sahoo's NTU optics papers 2019-2021, Sharad Sinha's HKUST work); the strict year > J rule removes the joining year but papers written elsewhere and published in the first year(s) at IIT Goa may remain. Wayback dates are upper bounds on joining.
* **DOI:** only 13 % carry a DOI (printed on the source); DOI coverage is not representative.
* **Department mix:** SMS and SES are over-represented (64, 57); HSS (10) and Chemical and Materials Engineering (8) are thin; Materials Engineering faculty are folded into neighbouring units.
* **Version duplicates:** some arXiv rows may be preprint versions of faculty-page journal rows with different titles (e.g. 2412.00453 vs the APL 2026 bandgap paper of Santosh Kumar); matching should allow title variants.
* **Students/postdocs:** 5 non-faculty-led arXiv rows and 4 student-led news rows; otherwise students appear only as co-authors.
