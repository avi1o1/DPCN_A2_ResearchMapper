# Golden set: IIT Hyderabad (iit_hyderabad), 2016-2026, lab notebook

Built 2026-10-27 by sub-agents; the work was interrupted once by a usage limit and continued from the saved state. No bibliographic API was used for discovery (no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite, arXiv API); pipeline outputs were not read. All fetches went through the shared polite fetcher; the full fetch log is in the scratchpad work folder `iit_hyderabad_golden/data/fetch.log`.

Result: 398 rows (target ~650 not reached; see Bias). Sources: annual_report: 58, arxiv: 20, dept_page: 88, faculty_page: 232. All rows `medium` except arXiv rows (`high`, affiliation visible in the PDF).

## Sources and yield
* Faculty/lab homepages (about 330 pages fetched, 45 usable publication lists): entries spaced evenly through each list, cap 8 per person. Only entries with a year strictly after the person's joining year were taken.
* Department pages: CSE publications tables, Mathematics publications page (IITH authors highlighted), Liberal Arts research-publications page. Matching of authors by full name (CSE/Math) or surname plus initial (LA); tenure rule applied.
* Annual reports 2016-17 to 2018-19 (publication lists per faculty): hand-reviewed sample; report listings alone are `medium`.
* arXiv: abs pages and PDFs reached through general web search restricted to arxiv.org (never /search); 55 papers fetched, 20 kept where the PDF first pages show an IIT Hyderabad address and an IITH faculty author. Year = v1.
* News/highlights: iith.ac.in news, highlights and press-release pages were fetched; they list awards and events, almost no papers with titles, so the news share is 0 (no rows). Annual reports 2021-22 to 2024-25 are text-extracted but their publication lists are scrambled two-column text, so they were not used.

## Tenure rule
Joining year: NIRF joining date in the roster, else the first annual report that lists the person (an upper bound), else own page (Sanghi Oct 2025, Dandapat Sep 2025). Paper year must be strictly greater. People with no joining year anywhere were excluded (except where the own page gave one).

## Coverage
Years: 2016: 32, 2017: 48, 2018: 23, 2019: 32, 2020: 21, 2021: 29, 2022: 32, 2023: 33, 2024: 70, 2025: 40, 2026: 38
Departments: Artificial Intelligence: 3, BioTechnology: 1, Biomedical Engineering: 10, Chemical Engineering: 10, Chemistry: 38, Civil Engineering: 36, Computer Science & Engineering: 86, Design: 5, Electrical Engineering: 76, Liberal Arts: 30, Materials Science and Metallurgical Engineering: 7, Mathematics: 33, Mechanical & Aerospace Engineering: 52, Physics: 11

## Rejected / dropped
* ~17 parsed rows dropped for broken title/venue parsing; patents, awards, talks, grants and theses lines filtered out.
* Papers by "IIIT Hyderabad" (International Institute of Information Technology) were rejected; one arXiv candidate (2410.08285) is IIIT and was not used.
* arXiv candidates whose first pages did not show IIT Hyderabad (large collaborations such as DES, DUNE, Belle II, ProtoDUNE) were not used.
* Kundu (Physics) skipped: no joining year found.

## Bias
Physics, Chemical Engineering, MSME, Design, Biotech, BME and AI are under-represented because few faculty there have scrapable publication lists (many use Google Scholar/IRINS links). CSE, EE and MAE are over-represented. 2016-2020 and 2018/2020 are thinner than 2024. DOI coverage is low for list-based sources.

<!-- SUPPLEMENT-1 BEGIN (2026-10-28): extension of the first pass, 398 -> 565 rows -->
## Supplement 1 (extension pass, 2026-10-28)

Goal: raise thin units (Physics, Chemical Engineering, MSME, Design, BME, AI, Biotech) and years 2021-25. Same rules as the first pass (no bibliographic API or IRINS/Scopus/OpenAlex discovery, no arXiv /search, shared fetcher only, no bot-wall bypass, cap 8 papers per person across all rows, tenure rule b = year strictly after joining year). Rows added: 167 (annual_report 146, faculty_page 17, arxiv 4). Total 565 (before: 398). DOI present on 259 of 565 rows.

### Sources and yield
* Annual reports 2021-22, 2022-23, 2023-24, 2024-25 (previously unused). The text was scrambled because the per-department "Publications" lists are two-column. Fix: `pdftotext` of each page cropped into left/right column (x 0-298, x 297-595), entries split at the numbering, a second `-raw` pass of the same page used only to restore hyphens that the default mode drops (titles, DOIs); department taken from the last "Department of ..." heading on or before the page. 7,741 numbered items extracted, 4,607 parsed as a dated citation, 3,083 matched to a roster person of the same department with joining year < paper year (surname plus initial or full name; common surnames such as Kumar/Singh/Das needed the full first name). Only thin units were sampled: up to 2 papers per person, spread evenly through that person's list across the four reports. 150 selected, 146 kept after deduplication and the cap. These are `medium` (report listing only; the report lists papers of the report year by current faculty, and a DOI is printed in the report for most).
* Faculty pages never fetched in the first pass: 108 roster homepages of non-CSE/EE units were fetched (first pass had fetched only the pages it found by crawling). Only Rathinavelan (Biotech, `people.iith.ac.in/tr/`) and Deshpande (MSME group page) had parseable lists with titles; 11 rows. Further sub-pages found by web search (`people.iith.ac.in/ksahu/Publications.html`, `jgiri/publications.html`, `suhash/publications.html`; also tried `asthanas/7Publications.html` (no years on the page), `subhradeep/publist.html` (multi-line entries, not parsed), `kdmakwana/cv_kirit.pdf` (not parsed)): 6 more rows (Sahu, Giri, Dey).
* arXiv: web search restricted to arxiv.org with the printed address string ("Indian Institute of Technology Hyderabad", department names); 33 candidate PDFs, 25 fetched (the arXiv host hung for the remaining ones after repeated stalls; those were dropped, not retried), 16 had already been judged in the first pass. 6 candidates built (Sahu x2, Kundu, Pahari, Onkar (Design), Sen/Mohan (AI)); 4 rows survived the 8-per-person cap and deduplication (affiliation read on the PDF first page, so `high`). Candidates with an IITH address but one author among very large collaborations (DES 2202.10480) were not used.
* News / press: `pr.iith.ac.in` press release on the InPTA/EPTA pulsar papers (2023) names two A&A DOIs but no titles; the publisher landing pages answered 403 (bot challenge, not bypassed), so no row. Newsletter issue 22 (PDF) contained no titled papers of IITH authors beyond reference lists. News share therefore remains 0.

### Rejected / not used
* `cc.iith.ac.in/publications.html` (Climate Change): the list uses Scopus-export fields ("Source Title", "Publication Date"), so it was treated as a Scopus-backed widget and not used.
* One Giri item (2016, work done at NIST, authors not IITH) dropped; one parse with title = venue dropped; 5 titles already in the set; 3 rows dropped by the 8-per-person cap.
* Non-thin units (CSE, EE, MAE, Chemistry, Civil, Math, Liberal Arts) deliberately not extended from the reports, although 1,900+ parsed matches exist there.
* Department pages: no new dated department publication list was found for the thin units (Physics, MSME, BME, Design, Biotech, Chemical Engineering department sites list research areas/news only; the Climate Change list above was refused), so dept_page stays at 88.

### Biases added by this pass
* Years: 2021-24 now carry most added rows (reports cover only those years: 2021 +40, 2022 +25, 2023 +66, 2024 +26). 2018 (+2) and 2020 (+1) stay thin: there are no annual reports for 2019-20 and 2020-21 on the website and few dated faculty lists. 2016-17 is unchanged.
* Annual-report rows are `medium` and inherit the report's coverage: faculty who report more appear more often; large collaboration papers (Belle II, DUNE, EPTA) appear through one IITH co-author.
* Rows added from faculty pages come from the few people who keep text lists with titles; extension remains at low-effort sampling (<= 2 per person from the reports).
* Roster joining years come from NIRF or the first report listing (an upper bound, as in the first pass); 32 roster people without any joining year were excluded from the report-derived rows.
* Source mix now: faculty_page 44 %, annual_report 36 %, dept_page 16 %, arxiv 4 %, news 0 % (target 50/15/15/10/10).
<!-- SUPPLEMENT-1 END -->
