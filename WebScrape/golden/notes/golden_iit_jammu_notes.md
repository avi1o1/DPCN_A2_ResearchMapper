# Golden set: IIT Jammu (iit_jammu), 2016-2026, lab notebook

Built on 2026-10-26 by an independent sub-agent. No bibliographic API was used for discovery: no Crossref, OpenAlex, Semantic Scholar, Europe PMC, DOAJ, ORCID, DBLP, Google Scholar, Scopus, IRINS, DataCite or the arXiv API.
`WebScrape/iit_jammu.json` and the other pipeline outputs were not read. Every URL went through the shared fetcher `scratchpad/tools/polite_get.py` (133 fetch calls, logged in `work/iit_jammu_golden/data/fetch.log`). Downloads are in `work/iit_jammu_golden/data/` and scripts are in `work/iit_jammu_golden/code/`. arXiv was never blocked (no ARXIV_BLOCKED file); an extra 10 s sleep was added between arXiv requests.

**Result:** 348 distinct papers in `golden/golden_iit_jammu.csv` (target 350).

| evidence_source | rows | confidence | rows with DOI |
|---|---|---|---|
| faculty_page | 187 (54 %) | all medium | 56 |
| annual_report | 69 (20 %) | all medium | 8 |
| dept_page (11 lab / personal sites linked from institute profiles + 1 institute-hosted lab page) | 44 (13 %) | all medium | 5 |
| arxiv (PDF affiliation checked) | 31 (9 %) | all high | 0 (no arXiv DOIs recorded) |
| news (institute news posts) | 17 (5 %) | all high | 2 |
| **total** | **348** | 300 medium / 48 high | 71 (20 %) |

Types: journal 227, conference 74, preprint 31, book-chapter 14, book 2.

## Departments x years coverage
| Department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bioscience and Bioengineering |  |  |  |  |  | 1 | 3 | 5 | 2 | 5 | 1 | 17 |
| Chemical Engineering |  |  |  |  |  | 1 | 3 | 6 | 4 |  |  | 14 |
| Chemistry |  |  | 2 | 1 | 1 | 1 | 7 | 5 | 10 | 5 |  | 32 |
| Civil Engineering |  |  |  |  | 2 | 3 | 4 | 7 | 12 | 16 | 8 | 52 |
| Computer Science & Engineering |  |  |  | 1 | 1 | 4 | 1 | 5 | 13 | 9 | 5 | 39 |
| Electrical Engineering |  |  | 1 | 4 | 3 | 11 | 6 | 4 | 28 | 12 | 10 | 79 |
| Humanities & Social Sciences |  |  |  |  | 5 | 1 | 1 |  | 1 | 6 | 3 | 17 |
| Inter Disciplinary Program |  |  |  |  |  |  |  |  |  |  | 1 | 1 |
| Materials Engineering |  |  |  |  |  | 2 |  | 6 | 4 | 8 | 3 | 23 |
| Mathematics |  |  |  | 1 | 1 | 3 | 2 | 2 | 5 | 4 | 4 | 22 |
| Mechanical Engineering |  |  |  |  |  | 2 | 3 | 6 | 6 | 7 |  | 24 |
| Physics |  | 1 | 3 |  | 1 | 3 | 3 | 6 | 4 | 4 | 3 | 28 |

2016 has 0 rows and 2017 has 1 row (arXiv 1712.02137, affiliation visible). See "Known biases".
`department` is the institute's own unit name from the faculty JSON; for joint appointments the first unit other than "Inter Disciplinary Program" is used.

## 0. Website structure
* www.iitjammu.ac.in is an Angular single-page app. The faculty data comes from the public JSON endpoint `https://userlogin.iitjammu.ac.in/api/faculty/public`, which the app itself calls. It returned 161 profiles; 160 are active: 150 regular, 3 former, 2 INSPIRE, 1 visiting, 1 advisor and others. These are the same fields shown on `https://www.iitjammu.ac.in/faculty/~<id>`, which is recorded as `source_url`. The `archive.iitjammu.ac.in/api/...` endpoints referenced in the bundle return 404.
* News posts ("Awards and Achievements", "News and Update", 639 English posts) and the annual-report links are embedded in the app bundle `main-ZBU3Q22Y.js` (10 MB). These were parsed from the bundle, and each news row cites `https://www.iitjammu.ac.in/update/<slug>`.

## 1. Faculty pages, source "faculty_page"
* Publication entries were split from the profile's `publications` and `bookchapter` HTML fields. Eligibility: at least one entry inside tenure.
* **Tenure (J) sources, in order:**
  1. The person's own profile: research_experience, professional background or bio. Examples: "Assistant Professor ... IIT Jammu, Dec 2019 - till date", or the end date of the previous job.
  2. No NIRF faculty list was found.
  3. The first institute listing. Two listings were used:
     * The Wayback snapshot of `iitjammu.ac.in/faculty` from 2018-08-30, the only early faculty-list capture. It lists 25 regular faculty.
     * The first IIT Jammu annual report that names the person. The FY 2016-17, 18-19, 20-21, 21-22, 22-23, 23-24 and 24-25 reports were name-matched. J is set to the end year of the first FY that names the person.

  Both are upper bounds, so they are conservative. The rule is strict: a paper is accepted only if its year is greater than J. The J source is quoted in each row's `notes`.
* **Sampling:**
  * Per unit, eligible faculty were ordered alphabetically and roughly evenly spaced: 4-6 for large units and all eligible faculty for small units.
  * Per person, up to 5 in-tenure entries were taken, evenly spread through the list in list order. Units thin in eligible faculty (Physics, Mathematics, BSE, Chemical Eng.) allowed up to 8 per person.
  * After a first pass, six more faculty were added to reach the target: Arun Kumar Verma, Karan Nathwani, Chembolu Vinay, Pratik Kumar, Nitin Joshi and Dhanendra Kumar.
  * Final: 46 faculty, 187 rows.
* **Dropped entries (3):**
  * Prasun Halder's 2024 GeoMandu conference version, a duplicate of the 2026 LNCE version.
  * A Salunkhe entry with no title on the page.
  * A Ravikant Saini entry whose title is split across two list items.
* **Rejected for tenure:** 1,071 of 1,680 listed 2016+ entries of faculty with a determined J were at or before J. Most "Selected publications" lists on this site are pre-joining work. Faculty who joined in 2024-2026 contributed 0 entries. Examples of eligible-looking lists with no in-tenure entry:
  * Abhishek Kumar: joined Mar 2025.
  * Ajay Gautam: joined 2025.
  * Sarita: joined 2026.
  * Jigmi Basumatary: joined Feb 2026.
  * Priyatosh Jena: not in any report up to 2024-25.
* **Profiles with no list:** about 30 profiles have empty or "see website" publication fields. Their lab sites were used where available (section 3).

## 2. Annual reports, source "annual_report"
* Links come from the app's /annual-report page, which points to Google Drive files. The English PDFs were downloaded through `drive.google.com/uc?export=download&id=...`, using the plain public download with no confirmation bypass needed.
* Report contents:
  * FY 2016-17 has no publication list.
  * FY 2017-18 and FY 2019-20 are image-only PDFs and no OCR is installed. For 2017-18, pages 39-44 ("List of publications by faculty") were rendered with `pdftoppm` and read visually, giving 3 rows. FY 2019-20 was not used.
  * FY 2018-19: one text page of publications.
  * FY 2020-21: department "key publications" lists only.
  * FY 2021-22 to 2024-25: department lists, often in two-column tables that `pdftotext` interleaves.
* **Sampling:**
  * Citation-like blocks were extracted with `code/ar_blocks.py`: they need a year, venue cues, and a roster name match. Counts: 2021: 11, 2122: 36, 2223: 35, 2324: 68, 2425: 84.
  * Two systematic passes picked evenly spaced blocks: positions j*n/k, then the midpoints (j+0.5)*n/k.
  * Each picked block was read by hand. Entries were skipped when they were talks, grants or patents, had illegible or truncated titles, were duplicates, or fell outside tenure. Titles reassembled from interleaved columns are flagged in `notes`.
* **Confidence:** medium for every row, because a report listing is not affiliation evidence. Each row also passes the tenure rule.
* **Rejected examples:**
  * Outside tenure:
    * All 2018 entries of people whose J is 2018 (Nathwani, Hasan, Ajay Singh, Bijral, Gaur in the 2017-18 and 2018-19 reports).
    * Tyagi's 2021 CRC chapter (J=2021).
    * Madge 2021 (J=2021).
    * Verma's 2023 TVT/EV-charger paper (J=2023).
    * Meenakshi Rajeev's 2024 J. Int. Dev. paper (J=2024).
    * Garima Singh's 2024 MEG paper (J=2024).
    * Gochhayat's 2024 BSCIAM paper (J=2024).
    * Chakraborty's 2019 WS2 LED paper (J=2020).
  * Unknown tenure: Anand Kumar S, Varsha Singh and Swagata Bhaumik (former faculty), Dinesh K Pandya (mentor faculty), Debolina Ghatak (visiting).
  * Unclear authorship: "Bera A." on a Monarda citriodora fumigant paper.
* Yield: 69 rows (FY 2024-25: 31, 2023-24: 17, 2022-23: 8, 2020-21: 5, 2021-22: 4, 2017-18: 3, 2018-19: 1).

## 3. Lab / personal pages, source "dept_page"
* **Department pages:** the app's `department/:id/...` routes have no publication lists.
* **Lab and personal sites linked from the institute profiles (personalwebsite / bio fields):**
  * Used:
    * IC-ResQ (A P Shah), journals page
    * AADHRIT lab (Anup Shukla): "under review" items skipped
    * Badri Subudhi (Google Site)
    * Sartaj Ul Hasan (Google Site)
    * Vinit Jakhetiya (Google Site)
    * Srishilan C publications
    * Shirsha Bose Bio3RG
    * iMASS (Ankit Kathuria)
    * Prakram Labs (Sidharth Maheshwari)
    * Guru research group (R. Gurubrahamam)
    * The institute-hosted Materials Research Laboratory page (Rahul Salunkhe), found via web search
  * Not usable:
    * Ajay Singh: list stops in 2018 (J=2018).
    * Satya Sekhar: list stops in 2019, before J.
    * Sanat Tiwari (WordPress): profile only, no list.
    * Shivnath Mazumder (Wix): no publication list.
    * High Pressure Fluid Lab: JavaScript-rendered and empty.
    * Rahul Kitture (Google Site): requires sign-in.
    * medsenselab.com: SSL error.
* **Sampling:** about 5 in-tenure entries spread over each list, fewer where the per-person cap of 8 applied or entries duplicated other rows. 44 rows.

## 4. arXiv, source "arxiv"
* robots.txt disallows `/search`, so no listing search was used. Ids came from:
  * web search restricted to arxiv.org;
  * the id `arXiv:2303.16329` printed on Parveen Kumar's institute profile;
  * the id `arXiv:1712.02137` printed in the FY 2017-18 report.
* Web search strings:
  * `"Indian Institute of Technology Jammu" arxiv`
  * `"IIT Jammu" arxiv.org`
  * `Jammu 181221 arxiv preprint Indian Institute of Technology`
  * `"IIT Jammu" OR "Indian Institute of Technology Jammu" arxiv 2018 2019 mathematics physics` (0 IIT Jammu hits)
  * `"Indian Institute of Technology Jammu" "Department of Electrical Engineering" arxiv`
  * `"Indian Institute of Technology Jammu" Chemistry OR "Civil Engineering" OR "Materials Engineering" arxiv preprint`
  * `"IIT Jammu" arxiv speech OR image OR graph OR network 2020 2021 2022 2023` (0)
  * `"Indian Institute of Technology Jammu" arxiv plasma OR quantum OR condensed matter OR battery` (0)
  * `"Indian Institute of Technology Jammu" "Department of Mathematics" arxiv`
  * `"IIT Jammu" arxiv 2017 OR 2018 OR 2019 preprint "Jammu, India"` (0)
  * `"Indian Institute of Technology Jammu" arxiv "Computer Science and Engineering" deep learning`
  * `arxiv Tanmay Sarkar "IIT Jammu" ...` (0)
  * `arxiv Sanat Tiwari Jammu dusty plasma 2018 OR 2019 OR 2020`
  * `arxiv "Sartaj Ul Hasan" Jammu permutation polynomials`
* For each id, the abs page and PDF were fetched (33 ids, 66 fetches, all 200). The affiliation was checked in `pdftotext` of the first 2 pages; for mathematics papers the address block at the end of the PDF was checked.
* Results: 31 accepted, all high. Rejected:
  * 2107.11412: no Jammu in the PDF text.
  * 2609.12730: no Jammu in the PDF text.
  * 1906.04907: University of Jammu, not IIT Jammu (seen in search results only, not fetched).
* Year = v1 submission year. Venue = "arXiv preprint <id>" (plus journal-ref when present).

## 5. News, source "news"
* **Institute news:**
  * 168 "Awards and Achievements" posts in the bundle were filtered by `publish|journal|paper|article|cover|featured|breakthrough|study|interspeech|icassp|conference|research`, and about 45 were read.
  * Posts that give a paper title produced 17 rows. They are high confidence, because the institute post attributes the work to IIT Jammu researchers. Many are student-led (PhD, MTech, BTech first authors).
* **Rejected:**
  * Poster awards: Vanisha Sodhi, Manisha Sharma, Deepak Sharma, Masoom Mairaj (GLS-2025), Akashdeep Sharma.
  * Award posts with no paper title: FMFP 2022 (Vivek Sahu), Rohit Anand, ICONE31, INCAM 2022.
  * Image-only posts whose images now return 404: Neha Rani (Organometallics), Piyush Olivkar (RSER), Murtiza Ali (DSP), Pradosh & Sapna, Insha Amin, Sapna Thapar, Jayaramulu (Chem Rev), Rahat Gupta review. A Wayback attempt also returned 404.
  * Two posts give only a DOI: the Salunkhe JMCA zinc paper (10.1039/D3TA05805K) and the Chauhan Angewandte paper (10.1002/ange.202309184). The publisher pages reached from these links returned Cloudflare "Just a moment" (403) challenges and were **not** bypassed, so these rows were not created.
  * Bhaduri's CHEMCON 2023 paper was skipped because he had already reached the cap of 8.
  * The GLOF / Times Now item is a duplicate of a faculty-page row.
  * The Rahat Gupta J. Mol. Struct. item is a duplicate of an annual-report row.
* **External press (web search):**
  * Strings: `IIT Jammu researchers study published journal`, `"IIT Jammu" researchers paper published in journal study finds`, `IIT Jammu professor research study published glacial OR battery OR speech OR Himalaya news`, `"IIT Jammu" study published "Science of the Total Environment" OR "Scientific Reports" OR "Nature" researchers news`.
  * These returned mostly University of Jammu pages, IRINS (forbidden, not opened) and Nature Index pages, which have no titles.
  * One press item (watertoday.org on Navneet Kumar's evaporation device, linked from his profile) gives no paper title or IIT Jammu affiliation, so it was rejected.
  * There are no `websearch` rows. The external-news share was replaced by institute news, as the brief allows.

## Per-person cap
The cap of 8 is counted per sampled person across all sources, by the person whose list or primary authorship produced the row. Two annual-report rows were removed to respect it: Subudhi's INDICON 2024 paper and Suman Sarkar's Cu-hBN paper. People at the cap: Shah, Nathwani, Dubey, Chauhan, Salunkhe, Saurav, Bhaduri, Sartaj Ul Hasan, Suman Sarkar and Subudhi. Rows where a faculty member is only a co-author on someone else's list are not counted against them.

## Known biases
* **Recency:** 2016 has 0 rows, 2017 has 1 and 2018 has 6. The institute started in Aug 2016 with about 25 faculty in 2018. The strict tenure rule (year > J, with J often an upper bound from the 2018 Wayback list or the first annual report) rejects almost all 2016-2018 papers that lack visible affiliation. FY 2017-18 and 2019-20 reports are image-only. arXiv web search returned almost only 2020+ preprints.
* **Survivorship:**
  * Faculty pages exist only for current faculty (plus 3 "former").
  * Former faculty appear through news only (Sayantan Mandal, Dikshant Malhotra).
  * Many former faculty in the 2017-18 and 2018-19 reports (Anand Kumar S, Swagata Bhaumik, Varsha Singh, Arnab Banerjee, Anubha Jindal) were rejected because their tenure was unknown.
* **Selected-publication lists:** about half of the profiles show only 5 "selected" papers, chosen by the faculty member, often their highest-impact work. This favours journal papers in high-IF venues.
* **Department mix:**
  * Electrical Engineering (79) and Civil Engineering (52) are large. Electrical Engineering is the largest unit, with rich lists and lab sites.
  * Chemical Engineering (14), BSE (17) and HSS (17) are thin, because most of their faculty joined in 2024-26 or list only pre-joining work.
  * Inter Disciplinary Program has 1 row, an arXiv preprint.
* **Affiliation:** 86 % of rows are medium confidence (tenure-based). Annual reports and lab pages demonstrably include pre-joining or collaborator-led papers; these were rejected where visible.
* **Medium-confidence rows with foreign co-authors:** papers of recently joined faculty may still have been done at the previous employer, for example Abhay Sharma (KU Leuven co-authors), Shirsha Bose (Trinity) and Sidharth Maheshwari (Newcastle).
* **Annual-report text quality:** titles reassembled from interleaved columns are flagged. Three annual-report rows have an empty venue and three have a truncated one.
* **DOI coverage:** 20 % overall, but uneven: faculty pages 30 %, reports 12 %, arXiv 0 %.
