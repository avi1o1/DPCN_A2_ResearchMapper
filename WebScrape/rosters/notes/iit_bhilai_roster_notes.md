# IIT Bhilai roster notes (iit_bhilai)

Built 2026-10-28 by one agent. Scripts and caches are in scratchpad `work/iit_bhilai_roster/{code,data}`. Pages cached by the golden-set agent were reused (`iit_bhilai_golden/data`: ECE people page, 114 profile pages `prof_*.html`, annual-report PDFs, CDX listings). All fetches went through the shared fetcher.

## Access and sources
* **The live institute site is unreachable** (`DEAD:SSLError` for iitbhilai.ac.in). Every institute page therefore comes from Wayback copies (`web/<ts>id_/`). No bot wall was met.
* **Department people pages.** CDX prefix query `iitbhilai.ac.in/index.php?pid=dept_*` with `collapse=timestamp:6`. I fetched about 85 captures of `dept_{bsbme,chem,cse,ee,liberal,math,me,msme,phy}_people` (1-2 per year, 2019-2026). The ECE people page has a single capture, 2026-05. Earliest captures are 2019-07, so there are no department pages for 2016-2019.
* **Dated institute-wide lists:**
  * Annual Report 2017-18 faculty section (21 people).
  * `fac_faculty` 2019-08 (19 people).
  * Telephone directory 2019 (`info_directory`, 45 faculty with designation and unit).
  * Monthly-remuneration list Jan 2024 (68 regular faculty).
  * `adjunct_professors` 2023 and `distinguished_professor` 2019.
  * `dept_liberal_visiting` 2025 and `dept_liberal_adjunct` 2026.
  * 2016/2017 mentor pages `faculty.html` and `faculty2sem2016.html`.
* **NIRF data submissions.** The institute hosts them at `index.php?pid=report_{overall,engineering}_{2023,2024,2025}`. Four files were archived and parsed (`pdftotext -layout`, faculty table with joining/leaving dates): overall 2023, engineering 2023, overall 2024, engineering 2025. NIRF 2022 and 2026 are not archived.
* **Profile pages** (`index.php?pid=<id>`) give identifiers, current designation (promotions newer than the department list) and stated joining dates.
* **ORCID:** offline index only. No live ORCID API calls (no 429).

## Per-unit extraction counts against NIRF (early check)
NIRF carries no unit, so only totals can be compared. Faculty rows parsed (all rows parsed, srno matches row count):

| File | Rows | Currently working |
|---|---|---|
| NIRF 2023 | 62 | 59 |
| NIRF 2024 | 71 | 67 |
| NIRF 2025 | 77 | 72 |

Latest department-page counts (the people listed, titled Dr./Prof. only; MSME page also lists about 30 students, excluded):

| Unit | Latest page |
|---|---|
| CSE | 15 |
| EE | 10 |
| ECE | 10 |
| ME | 12 |
| Chemistry | 12 |
| Physics | 9 |
| Mathematics | 10 |
| Liberal Arts | 9 |
| BSBME | 8 |
| MSME | 9 |

## Roster totals
157 rows: current 91, former 12, visiting 48, adjunct 6, emeritus 0.
* **Visiting (48):** 42 IIT Hyderabad mentor faculty, plus Veena Bansal (IIT Kanpur), S. K. Maiti, R. K. Ghosh, R. K. Thareja, P. D. Srivastava and U. B. Desai.
* **Adjunct (6):** 5 with no department stated on the source page, plus Cecile Sandten (Liberal Arts).
* **Rows per department (current / former / other):** CSE 14/2/6 (the 6 are mentors plus Bansal and Ghosh), EE 8/2/10, ECE 8, Liberal Arts 7/4/6, Mathematics 9/1/7, Mechanical 12/0/4, Chemistry 12/0/4, Physics 9/1/3, BSBME 4, MSME 8. The remaining rows are mentor or adjunct rows from other units, one EECS (defunct) row, one blank-department NIRF-only former row, and the adjuncts without a department.
* joining_year is set on 86 rows.

## Independent size check
NIRF 2025 (engineering) lists 72 working and NIRF 2024 lists 67 working. NIRF 2026 is not archived. The roster has 91 current rows (about 82 regular, plus visiting/others already counted separately). The excess over NIRF 2025 is the 2025-26 joiners who appear only on the 2026 department pages (about 20: new EE, ECE, MSME, BSBME, Liberal Arts, Physics, Maths and Chemistry faculty) minus a few leavers. Of the current rows, 72 carry a NIRF source (appear in at least one NIRF file) (latest-file "currently working = Yes"); the rest are post-NIRF joiners. NIRF category "Other" never occurs in these files (only Regular and one Visiting), so there was nothing to map for that category.

## How status and years were established
* **current** = on the latest archived department page of its unit (2026-01..2026-07) and not contradicted by a NIRF leaving date. Latest archived page per unit is a proxy for the dead live site; the institute-wide faculty list (`fac_faculty`) is an error page after 2019.
* **Stale pages:** NIRF leaving dates override later archived pages that still list the person (Prashant Agnihotri, Sitakanta Panda, Dhriti Ghosh, Subhajit Sidhanta, Sonal Jha and P. D. Srivastava stay on pages for 1-3 years after leaving).
* **former:** FIRST = min(NIRF joining year, first archived-list/annual-report/directory year). LAST = NIRF leaving year, otherwise last archived year.
  * Kapil Jainwal: LAST 2023 from NIRF 2024 "Yes" (file year minus 1).
  * Radeef Chundakkadan and Thirthankar Chakraborty: LAST 2022 from the last page that lists them (no NIRF row). Their joining years come from their own profile pages (2019 and 2020).
  * Aniket Singha: last evidence is the 2019-08 `fac_faculty` page, which may be stale. LAST is uncertain; joining year blank.
* **joining_year** = earliest NIRF joining year; profile statements used where no NIRF row exists (Krishna Murari Dec 2024, Sreelakshmi R Dec 2024, Radeef 2019, Thirthankar 2020). Santosh Biswas = 2019: the 2019 directory lists him as visiting associate professor and Head, NIRF regular joining is 2020. Blank for people with no NIRF row and no profile statement (mostly 2025-26 joiners; first-archived appearance is only an upper bound). Profile free text was cross-checked against NIRF; the automatic profile regex picks spurious earlier years (education/other posts), so only manually read profile dates were used.
* **Promotions:** designation comes from the latest department page, overridden by a newer profile header (e.g. Anshul Faye became Associate Professor Feb 2026; Souradyuti Paul Professor).
* **Mentor faculty.** The `faculty.html` page (I-sem Jul-Dec 2016) and `faculty2sem2016.html` (captured 2017-04) list IIT Hyderabad faculty teaching at Bhilai. The second page's section heading says "II-semester (Jan-June 2016)", which cannot be right (the institute started Aug 2016). I read it as Jan-Jun 2017. People only in that section get (2017-2017), others (2016-2016) or (2016-2017). Uday B. Desai (Director IITH, mentor-director biography page) is a visiting row with no ORCID. IITH faculty on the 2017-18 academic committee (Ashok Pandey, B. B. Panigrahi etc.) are not teaching faculty and were not added.
* **Department naming.** BSBME = Biosciences and Biomedical Engineering; ECE (from 2024) split from EE; the 2019-2022 "Electrical Engineering and Computer Science" is defunct and used only for Kapil Jainwal, who was found only on the EECS-era CSE page (ORCID says Electrical). CSE 2021-22 pages list EE people too (EECS era). Mentor rows keep the IIT Hyderabad department name.

## Identifiers by route
ORCID total 64: 5 from institute profile pages, 59 from the offline index (employments with a faculty-type role, name-compatible, tie-broken by department). Zero live API lookups. No ambiguous multi-ORCID cases. Google Scholar 37, DBLP 2, Scopus 1, homepage 28 (Google Sites/Weebly/Wix/github.io only), IRINS 0. Emails come from the department pages ("[at]" replaced).

## Problems and decisions
* **Exclusions:** Kavita Devi (Physics page 2019-2022 but the 2019 directory says "Fellow", a postdoc); "Dr. Karthikeyan" and "Dr. Faculty Name" on the 2026 ECE page (template placeholders); Hao-Yu Lu (Chinese language instructor, untitled); the MSME page's student names; staff in the directory.
* **Nikhil Chander:** the 2026-07 EE page prints "Adjunct Faculty"; the 2026-05 ECE page and his profile (2026-03) print Associate Professor, ECE; NIRF 2025 says regular. Kept current, Associate Professor, ECE.
* **R. K. Ghosh:** Visiting Professor on CSE pages from 2021 and the ECE page 2026; kept current/visiting under CSE (second unit ECE).
* **Second units** (one row each, primary unit by page count): Nagesh Patil (ME; BSBME), Suchetan Pal and Mayilmurugan (Chemistry; BSBME), Rukmankesh (Chemistry; BSBME), Katchala Nanaji (Chemistry; EE page), Arzad Kherani (ECE; CSE/EE in the EECS era), Nitin Khanna (EE; CSE in the EECS era), Rajiv Prakash (MSME; also on ME pages).
* **P. D. Srivastava** = NIRF "Parmeshwary Dayal Srivastava" (visiting, 2018-2023); the institute prints "P. D. Srivastava". Name as printed is used.
* **Adjunct/distinguished** (Saraswat, Kiran Kumar, Lakhtakia, R. V. Kumar, Choubey): dated pages 2019 and 2023 only; whether they are still listed is unknown, so they carry ranges; department blank because the pages do not state one.
* **Rinkee Chopra:** NIRF-only (2022-2023), department unknown.
* **Rajat Moona:** first Director, NIRF joining 2017, left 2022; department CSE (annual report).
* **Name unification** by token-compatible matching plus manual aliases (Balkrishna Metha/Mehta, Mayil Murugan/Mayilmurugan, Eslavath Rajkumar/Rajkumar Eslavath, Vinod Kumar Reddy I / I. Vinod Kumar Reddy / Vinod Reddy, Amit Mishra / Amit Kumar Mishra).

## Known gaps
* **ORCID-only candidates not added:** the offline index shows faculty-type employment at IIT Bhilai for people absent from every dated institute source: Suchetana Banerjee (Liberal Arts 2018-2019), Rhythm Singh (EECS 2018), Dulendra Kumar Patle (ME 2019), Supriya Tripathi, Jitendra Chauhan, Shivam Gupta (2026), Sampad Laha (2026) and others. ORCID employment dates are self-declared and are not evidence, so they are listed here and not in the CSV. 2018-2019 leavers are therefore likely under-counted.
* **Archive coverage:** no department page before 2019-07; NIRF only 2023-2025 (NIRF 2018-2022 and 2026 not archived). The 2018-19 to 2023-24 annual-report PDFs were truncated or image-only.
* **Names:** several 2026 joiners lack a printed designation (listed as "Faculty (designation not stated...)"), and many have no joining year.
* **LAST for people who left before NIRF 2023** is a lower bound.
