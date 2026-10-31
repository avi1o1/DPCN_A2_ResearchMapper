# IIIT Ranchi (Indian Institute of Information Technology Ranchi, PPP IIIT) faculty roster: lab notes

Run: 30 Oct 2026, operator Arihant Tripathy (IIIT team). Output `rosters/iiit_ranchi_faculty.csv` (61 rows). Work files (not in repo): `C:\Users\Arihant\rm_work\iiit_ranchi_roster\data\`, scripts in `...\code\` (parse_cur.py, asp_parse.py, matrix.py, fetch_snaps.py, build2.py).

## Totals
current 32, former 25, visiting 2, adjunct 2, emeritus 0.

| unit | current | former | visiting | adjunct |
|---|---|---|---|---|
| Computer Science and Engineering | 8 | 10 | 0 | 0 |
| Electronics and Communication Engineering | 12 | 6 | 0 | 0 |
| Sciences (Physics) | 2 | 1 | 0 | 0 |
| Sciences (Mathematics) | 4 | 3 | 1 | 0 |
| Humanities and Management | 1 | 1 | 0 | 0 |
| blank | 5 | 4 | 1 | 2 |

The current website (`/faculty.aspx`, server-rendered ASP.NET) has one institute-wide list with no unit. Units come from the 2022-05 archived page (grouped CSE/ECE/Physics/Mathematics), profile PDFs (Faculty*.pdf), NIRF, emails (amit.math@, rajeshdwivedi.cse@) and the 2020-21 embedded JSON (dept field). The department pages (CSE/ECE/Sciences/HM.aspx) give only the HoD. "Sciences" is the official department; Physics/Mathematics are sections, shown in brackets. Blank unit (no source): Rajeev Srivastava, Roshan Singh, Gaurav Sundaram, Abhinav Kumar, Dhiran Kumar Mahto and some former people.
Unit conflicts: Rashmi Panda "Dept. of physics" (ad hoc, 2020-21 JSON) vs ECE from 2022: ECE used. Shahid Shadab Hassan: Mathematics on the 2022 page but specialisation Management/Communication: placed in Humanities and Management (judgement). Kumari Pritee: CSE assumed from the CSE block of the 2022-02 page.

## Campuses (verified)
* 2016-2019: mentor NIT Jamshedpur campus, Jamshedpur 831014 (site footer; 2016-19 site run by the NIT Jamshedpur webteam).
* from July 2019: interim campus at Jharkhand University of Technology (JUT), Science & Technology Campus, Khojatoli, Namkum, Ranchi 834010 (annual report 2020-21, letter of 28 Feb 2019). A second interim site, JUPMI Ranchi ("Khelgaon Campus"), is in the 2022-23 annual report and the Faculty-in-charges page.
* from c.2024: ARTTC BSNL Campus, Getlatu, Hazaribagh Road, Ranchi 835217 (current footer; "BSNL Campus" on the Faculty-in-charges page; a faculty CV gives a Getlatu address in 2024). Exact move date not documented. Permanent "Digital Valley" campus at Kanke is under construction (annual report 2022-23).

## Sources and endpoints
* Live: iiitranchi.ac.in/faculty.aspx (32 entries with qualification, designation, specialisation, email, optional profile PDF `docs/faculty/profile/FacultyNN.pdf`; 31 PDFs fetched, NN 02-39), CSE/ECE/Sciences/HM.aspx, Faculty-in-charges.aspx, director.aspx, NIRF.aspx (links annual reports 2016-17 to 2024-25 and NIRF 2025/2026 PDFs).
* NIRF PDFs `docs/Engineering_Category_{2025,2026}.pdf`, `Overall_Category_{2025,2026}.pdf` (faculty tables with joining and leaving dates). Older NIRF years are not on the site.
* Wayback CDX: `faculty.aspx` (22 captures 2022-02 to 2026-07, all fetched), old PHP site `academics/departments/faculty.php?deptid={cse,ece,maths,phy}` (2016-2018: only Goutam Mali (CSE) and Santosh Kumar Mahto (ECE); maths/phy "Department Not Found"), Laravel site `academics/faculty` and `academics/department/{cse,ece}/faculty` (2019-2021; the list is JSON embedded only in 2020-02..2021-04 snapshots: 14 people; 2019 snapshots hold only template placeholders), `legacy/.../faculty.php` (2019-07: Priye, Bhakta, Pati, Sandeep), governance pages (mentor directors), selected-candidate PDFs (2017-08, 2019-01), annual reports 2016-17..2022-23 (2016-17 to 2019-20 and 2021-22 are scanned images without text; 2020-21 and 2022-23 give committee lists and the sanctioned strength only, no faculty roster).
* ORCID public API: one expanded-search by affiliation name (43 hits), /employments for all 43, one per-person search (empty). Not used: IRINS, Scopus, OpenAlex, Scholar scraping. No bot challenge met; no JSON endpoint on the live site.

## How tenure years were established
* Current: all 32 current rows are in the NIRF 2026 table (NIRF-confirmed 32/32). NIRF dates are often regularisation dates, so earlier documented appointments win: Santosh Kumar Mahto 2017 (selected temporary-faculty list of Aug 2017, ECE; ad hoc on archived 2018 page; NIRF 2018-11); Rashmi Panda and Nishit Malviya 2019 (selection list of 30-01-2019, join by 11-02-2019; NIRF shows 2021/2023); Rajiv Kumar 2020 (temporary faculty on the 2020-02 page; NIRF 2021); Bharat Singh, Puja Ghosh, Priyank Khare, Kirti Kumari 2021 (NIRF); Dhananjoy Bhakta, Jayadeep Pati, Shashi Kant Sharma, Jitendra Kumar Mishra 2018 (NIRF Nov-Dec 2018; Bhakta and Pati also on the 2019 legacy list); Sandhir Kumar Singh and Rohit Kandulna, Rishikesh Dutta Tiwary 2022 (NIRF 2022; Sandhir's ORCID says 2020, self-declared, not used); Priyabrat Garanayak and Shashi Kant (maths) 2022 = first archived appearance as ad hoc faculty (2022-05; upper bound, NIRF 2023-03); Ravi Shanker, Noopur, Ranjan Kumar Behera 2023 (NIRF); Gaurav Sundaram, Akash Srivastava (CV: temporary from 22 Jul 2024), N Kishore Babu, Ankita Kumari 2024; Rajeev Srivastava 2024 (director page: 16 May 2024); Roshan Singh, Abhinav Kumar, Anuj Singh, Chandra Prakash Singh, Amit Kumar Singh, Dhiran Kumar Mahto, Rajesh Dwivedi 2025 (NIRF; Roshan Singh's 179 months of experience suggest the April 2025 date may be a re-appointment; first archived 2025-08, so 2025 is an upper bound).
* Former and others: FIRST/LAST are the first/last archived faculty.aspx snapshot listing the person (about 3 per year 2022-2026), earlier lists (2019 legacy, 2020-21 JSON, 2016-18 PHP pages) where applicable, cross-checked against NIRF leaving dates (2025 NIRF: Priye 02-01-2024, S K Mandal 21-04-2024, Shalini Mahato 31-01-2024, Bam Bahadur Sinha 09-07-2023, Prashanta 15-01-2024; 2026 NIRF: Nidhi Kushwaha 27-10-2024, Priyam Chakraborty 09-12-2024, Nitika Nigam 11-12-2025, Manju Mathew, Syed Sadique Anwer Askari, Shahid Shadab Hassan 30-06-2025). Where the website list lagged the NIRF date by a few months the website year is used in LAST. Archive density for 2016-2021 is low, so LAST for the 2020-21 temporary faculty (Bhattacharjee, Ritu Raj Singh, Shalu, Sandeep: last JSON snapshot 2021-04; Acharyya: 2022-02) is a lower bound; they may have stayed longer.
* Blank joining_year (first archived appearance recorded as FIRST, an upper bound): Kumari Pritee (2022-02; ORCID 2020-2022 not used), Shivang Tripathi (2024-09), Tarni Mandal (2022-12), Rambabu Kodali (2016-06), Karunesh Kumar Shukla (2017-12).
* Selection-list-only people (Saibal Majumder 2019-01 list; Abhishek Priyam, Lakshmi Kanta Patra, Nibedita Mandal, Nitin Chandra, 2017 list for walk-in temporary faculty): the list is the only evidence, joining_year is the list year, and it is unconfirmed they joined (Nitin Chandra has an ORCID employment "Temporary Faculty 2017-2019" at IIIT Ranchi, which supports him). Low confidence.
* Goutam Mali (CSE ad hoc): sole name on the 2016-08 to 2018-06 CSE page, so FIRST 2016 is an upper bound.

## Visiting / adjunct
* Adjunct: Rambabu Kodali (Mentor Director, Director NIT Jamshedpur, 2016-06 to 2017-06 pages) and Karunesh Kumar Shukla (Mentor Director, 2017-12 to 2019). Employed by NIT Jamshedpur, so adjunct.
* Vishnu Priye (first Director from 20 Jul 2018, on deputation from IIT (ISM) Dhanbad, last listed 2023-12, left 02-01-2024 per NIRF) held the Director post: regular `former` (FIRST 2018). Rajeev Srivastava (IIT BHU, on deputation) is Director since 16 May 2024: `current`.
* Visiting: Tarni Mandal and Sushil Kumar Mandal (listed "Visiting Professor" 2022-12 to 2024-03; Prof S K Mandal appears in NIRF 2025 as adhoc 22-04-2022 to 21-04-2024; Tarni Mandal is not in NIRF).
* NIT Jamshedpur faculty who only taught 2016-2018 are not named on any dated page; none added.

## Size check
Website: 32 current faculty. NIRF 2026 engineering table: 39 rows, 33 flagged "currently working" and 6 not (Shahid Shadab Hassan, Manju Mathew, Syed Sadique Anwer Askari, Nitika Nigam, Priyam Chakraborty, Nidhi Kushwaha). The one difference (33 vs 32) is Tarun Biswas, still flagged working in NIRF 2026 but dropped from the website between 2025-11 and 2026-02. The institute-wide website list wins, so he is `former` (2021-2025); status is low confidence. Annual report 2020-21: sanctioned strength 30 (4 professor, 4 associate, 22 assistant); the roster exceeds it because ad hoc/contractual staff listed as Assistant Professor (Gaurav Sundaram, Akash Srivastava, N Kishore Babu, Ankita Kumari are "Adhoc / Contractual" in NIRF 2026) are counted.

## Identifiers
ORCID 23 rows: 5 from institute profile PDFs (Priyabrat Garanayak, Akash Srivastava, Chandra Prakash Singh, Ranjan Kumar Behera (via CV-linked ORCID), Tarun Biswas), 18 from the ORCID affiliation search with /employments showing IIIT Ranchi and a name match. Rejected: students, research fellows (Ajit Kumar Singh, Rajnish Kumar), Raj Kumar Mistri (RTC Institute, not IIIT Ranchi). Google Scholar 5 and Scopus 3 (profile PDFs); dblp, irins, homepage none.
ORCID lookup pending (no ORCID in the affiliation search, per-person search not extended): Rajeev Srivastava, Dhananjoy Bhakta, Jayadeep Pati, Roshan Singh, Rajiv Kumar, Rashmi Panda, Bharat Singh, Puja Ghosh, Priyank Khare, Rohit Kandulna, Ravi Shanker, Shashi Kant, Noopur, Gaurav Sundaram, Ankita Kumari, Abhinav Kumar, Rajesh Dwivedi and former staff without ORCID.
Emails come from the site; blank for people found only on selection lists.

## Ambiguous people and decisions
* Tarun Biswas: see size check. Shashi Kant Sharma (ECE) versus Shashi Kant (maths): separated by email and date. NIRF "Prashanta" matched to Prasanta Majumdar (department blank). Sandeep and Goutam Mali: only partial names printed.
* Excluded: Registrar Satya Mandal, staff, research fellows, students.

## Known gaps
No faculty roster for 2016-2018 beyond Mali and Mahto; 2018-2019 archived pages carry no list; the temporary faculty who left before 2020 and the NIT Jamshedpur mentor-teaching faculty are largely invisible; annual reports 2016-2020 are image-only. Several unit blanks. Per-person ORCID lookups not done.
