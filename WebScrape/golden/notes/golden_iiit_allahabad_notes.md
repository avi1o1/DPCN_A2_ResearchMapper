# Golden set notebook: IIIT Allahabad (iiit_allahabad), 2016-2026

Operator: Arihant Tripathy (IIIT team). Built 2026-10-27. All fetching through `WebScrape/agents/polite_get.py`. No Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite or arXiv API/search was used; the pipeline output for this institute was not read.

**Result:** 265 distinct papers (target 350 was not reached; see "Why 265"). 245 medium, 20 high. Only 2 rows carry a DOI (DOIs are printed on few of the sources; none was looked up). Types: journal 171, conference 64, preprint 20, book-chapter 9, book 1. 63 distinct IIITA-author strings, at most 8 rows per first-named author. Years 2016-2026, but thin at both ends (see table).

## Sources, counts, yield

| evidence_source | rows | share | what it is |
|---|---|---|---|
| annual_report | 140 | 53 % | IIITA Annual Report 2023-24 (publications table, 540 rows parsed, institute authors printed in bold; 251 usable rows after matching a bold author to a current faculty member and the tenure rule) and Annual Report 2018-19 (per-faculty profile lists, 144 quoted-title entries, 103 after tenure/dedupe) |
| faculty_page | 94 | 35 % | own pages: profile.iiita.ac.in/{manish, venkat, manishgoswami, sonali/publications.html, sitangshu/publications_new.html, ratank.saha/publication.html, asahoo, srdubey/publications.php, vijayk} (all Wayback copies), and publications sections on www.iiita.ac.in profile pages (Soumyadev Maity, Prasanna Kumar Misra, Vineet Tiwari, Rekha Verma, Ashutosh Kumar Singh, Utkarsh Goel) |
| arxiv | 20 | 8 % | 62 arXiv PDFs fetched (ids taken from Dubey's, the CVBL lab's, Sonali Agarwal's and Ratan Saha's pages plus four ids from general web search), 36 + 2 show "Allahabad" in the first-page affiliations; 20 kept after the per-author cap |
| dept_page | 8 | 3 % | Computer Vision and Biometrics Lab (CVBL) publications page, Wayback copy; attributed to Satish Kumar Singh |
| news | 4 | 2 % | Network Security & Cryptography Lab "latest" news page, Wayback copy |

Planned mix was faculty 50 / dept 15 / annual report 15 / arXiv 10 / news 10. Actual mix deviates strongly (annual report 53 %, news 2 %). Reasons: (1) only about 17 faculty members have a parseable publication list that is reachable (see below); (2) the 2023-24 report has a clean, structured table, so it was the largest usable source; (3) the institute's news page (www.iiita.ac.in/news) has no paper items, and the one external news item found (MarkTechPost on T2CI-GAN, 2022) answered 403 and was not bypassed (the paper itself is in the set via its arXiv PDF); (4) department sites (it/ece/as.iiita.ac.in) hold no publication lists.

## Why 265 and not 350

* profile.iiita.ac.in and the lab subdomains (iris., cvbl., security.) do not resolve from this machine (fetcher: DEAD:ConnectionError). Wayback copies were used instead where they exist (recorded in each row's URL); several pages (tlahiri/CompleteList2019.htm, rkbhukya/publications.php, kavindra/publications, pragyabhardwaj publication page, sunnys, iris publications) had no Wayback copy (404) and were skipped.
* Three English annual reports (2016-17, 2017-18, 2020-21) are image-only PDFs (pdftotext returns about 200 bytes) and no OCR tool is installed; skipped. This is the main reason 2016, 2017 and 2020 are thin. The 2019-20 and 2022-23 and 2024-25 reports were not fetched (the first and last are 180 MB scans per the listing; 2022-23 was not linked on the current page).
* Many faculty pages carry no publication list (new Drupal profiles for most of the 75 current faculty list only teaching and projects), several personal pages are Google Sites (JavaScript, no list in the HTML), and IRINS/Google Scholar, the usual places, are forbidden.
* Faculty-page candidates dropped by the tenure rule (year not strictly after the joining bound): large for recent joiners (for example Anjali Gautam, Naveen Saini, Boddepalli SanthiBhushan, K. R. Kaza, whose pages list mostly earlier work; none of their listed papers qualified or the pages had no list), and every 2016 paper of faculty whose only evidence is the March 2016 Wayback snapshot (rule: strictly after the bound).

## Method notes (search strings and page types)

* Faculty list: roster agent's cached `www.iiita.ac.in/faculty` pages (75 current faculty); each profile page fetched (75 pages, 1 s per host) to find personal-website links and publication sections.
* Web searches used (general web search only): "IIIT Allahabad annual report publications list ...", "iiita.ac.in annual report 2021-22 ...", "profile.iiita.ac.in publications.php journal papers", "IIIT Allahabad lab publications page ...", "iiita.ac.in news research highlights ...", "IIIT Allahabad researchers develop paper published journal professor team news", "iiita.ac.in achievements OR research highlights ...", "arxiv.org Indian Institute of Information Technology, Allahabad 2017 ...", "arxiv.org abs IIIT Allahabad 2016 OR 2018 ...". Yield from the last three was four arXiv ids (two verified as IIITA-affiliated and added, two not).
* Annual report PDFs: https://www.iiita.ac.in/annual-reports- lists them under /sites/default/files/. The 2023-24 table was parsed from `pdftohtml -xml` coordinates (columns by x-position; bold font marks the institute's own authors).
* Title/venue/year extraction from the pages is by quoted-title regex plus manual rules; a handful of ambiguous entries (title/venue swapped by quote parity, page-number suffixes) were dropped or corrected by hand. Residual errors in venue strings are possible for faculty-page rows.

## Tenure rule used

* Own page: Manish Kumar (Assistant Professor since June 2010), Manish Goswami (joined June 2008), Prasanna Kumar Misra (faculty since 2014), Boddepalli SanthiBhushan (May 2021, no rows kept), Vijay Kumar Chaurasiya (page lists IIITA courses 2016-2018; on-page evidence).
* All others: first archived faculty-list snapshot in the roster agent's Wayback cache (iiita.ac.in faculty profile 2016-03 is the earliest; IT, MBA, applied-science and ECE department pages from 2017-2021; www.iiita.ac.in 2021-2026). This is an upper bound on the joining year, so a paper counts only if its year is strictly greater. Consequence: for faculty already present in March 2016, 2016 papers are excluded (only 2 rows dated 2016, both Manish Kumar with own-page tenure).
* Annual Report 2018-19 profiles: dated on-page evidence that the person is at IIITA in FY 2018-19. Rows for people not on the current list (former faculty such as G. C. Nandi) use year 2019 only.
* Annual Report 2023-24 rows: the bold author must match exactly one current faculty member (surname plus given-name tokens); first bold author is the cap owner. Student-only rows were not taken from this report because tenure cannot be shown.
* arXiv rows are `high`: the PDF prints "Indian Institute of Information Technology, Allahabad" with the named author. Preprint year = first version (year of the arXiv id). Shiv Ram Dubey's 2020-21 arXiv papers print an IIITA affiliation ("now associated with IIITA", arXiv:2001.05489), which is earlier than the 2021 snapshot bound used for his faculty-page rows. Student-led arXiv papers (first IIITA author a student, faculty co-author) are marked in `notes`.

## Selection design and its effect

* Per-author cap 8 across all sources combined, counted on the first-named IIITA author. Priority order when filling the cap: arXiv, own-page extras, news, faculty/dept pages, Annual Report 2018-19 (at most 4 per person), Annual Report 2023-24 (at most 6 per person).
* Within a person's eligible list the pick is year-balanced (round-robin over distinct years, oldest first, middle entry of each year) instead of strictly every-n-th; this was done to raise coverage of 2016-2019, since the lists are newest-first and dominated by recent years. It is a deliberate deviation from "evenly through the list".
* Duplicates by normalised title removed (Dubey and CVBL pages list the same papers; the same title in two annual reports counted once).

## Departments x years (rows)

| unit | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Information Technology | 2 | 5 | 2 | 5 | 13 | 7 | 10 | 40 | 18 | 2 | 1 |
| Electronics and Communication Engineering | 0 | 1 | 5 | 6 | 4 | 8 | 6 | 26 | 10 | 4 | 0 |
| Applied Science | 0 | 0 | 2 | 1 | 0 | 5 | 3 | 35 | 15 | 4 | 0 |
| Management Studies | 0 | 0 | 1 | 5 | 1 | 2 | 2 | 9 | 2 | 2 | 1 |

(Counts taken from the CSV at the time of writing; the department strings are the institute's own unit names. Centers (CCC, CIR, RCSoH) have no separate rows; their members appear under their home department.)

## Rejected or unusable candidates (examples)

* Dubey papers up to 2021 on his page (IIIT Sri City period, no affiliation shown): not used as faculty-page rows; his arXiv PDFs that print an IIITA affiliation are used instead.
* Anjali Gautam, Naveen Saini, K. R. Kaza, Amit Kumar, SanthiBhushan, Kavindra Kandpal: pages list mostly pre-joining work or talks; no rows from their own pages (Anjali Gautam, Navjot Singh, Anshu Anand etc. do appear through the 2023-24 report).
* Talks, workshops, FDPs and teaching entries that appear inside publication sections of some pages (Vineet Tiwari, Soumyadev Maity, Utkarsh Goel, Kavindra Kandpal, Akhilesh Tiwari, Anupam, G. C. Nandi): filtered by keyword rules and by hand.
* arXiv PDFs without an IIITA affiliation (26 of 62; mostly Dubey's IIIT Sri City period): excluded. arXiv:2301.03325 (EMAHA-DB1) shows an IIITA mention but the IIITA author could not be identified from the first page; excluded.
* IRINS profile pages (iiita.irins.org) appeared in search results and on faculty pages; not used (forbidden).
* MarkTechPost (403 bot response): not bypassed.

## Known biases

* Year skew: 2023 holds 110 rows (Annual Report 2023-24 table). 2016-2018 and 2025-2026 are thin. Use year-stratified weights when estimating recall.
* Department skew by source: Applied Science is represented mostly through the 2023-24 report; Management Studies is small (few pages with lists).
* 92 % of rows are `medium` (tenure rule or report listing, no per-paper affiliation); only arXiv rows are `high`. arXiv rows are IT/CVBL-heavy (Dubey, Satish Kumar Singh, Sonali Agarwal groups).
* People-selection bias: faculty with a public, parseable page or a mention in the annual report are over-represented; faculty without either are absent. Former faculty are present only through the 2018-19 report (G. C. Nandi, Anupam, Shirshu Varma and similar).
* The Annual Report 2023-24 table is institute-curated and is probably biased toward Scopus/WoS-indexed output, which is also what the pipeline's sources index. That makes this part of the set less independent than arXiv or personal-page rows.
* DOI coverage is about 1 % because none was looked up.
