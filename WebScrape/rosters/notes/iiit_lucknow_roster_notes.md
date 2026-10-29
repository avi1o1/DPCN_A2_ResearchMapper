# IIIT Lucknow faculty roster (2016-2026): lab notebook

Built 2026-10-29 by Arihant Tripathy (IIIT team) with Claude. Output: `WebScrape/rosters/iiit_lucknow_faculty.csv` (71 rows). All fetches went through `polite_get.py`.
Downloads and scripts: `C:/Users/Arihant/rm_work/iiit_lucknow_roster/{data,code}` (not in the repo).

## Totals
| status | rows | joining_year filled |
|---|---|---|
| current | 23 | 8 (profile text: Rahul Verma 2021, Padma Tripathi 2024, Niraj Vishvakarma 2021, Shubhra Jain 2023, Rashi Srivastava 2026, Neelu 2020, Soumendu Chakraborty 2018, Niharika Anand 2018) |
| former | 11 | 3 (Arun Mohan Sherry 2019, annual report "w.e.f. 28/02/2019"; Vinod Kumar 2020 and Chandranath Adak 2021, profile pages) |
| visiting | 34 | 0 |
| adjunct | 3 | 0 |
| total | 71 | 11 |

Per department (current / former / visiting+adjunct): Information Technology 7 / 1 / 17+3; Computer Science 2 / 3 / 1; Mathematics 5 / 2 / 0; Management and Humanities 8 / 1 / 10;
no unit printed: 1 current (Dean D. K. Singh) / 4 former / 6 visiting. The institute has four departments; the name appears as "Management & Humanities", "Management and Humanities" and
"Humanities and Management" on different profiles, the roster uses "Management and Humanities". No centre has its own faculty (CDSAI, WCARL, CREATE are headed by department faculty).
Campuses: 2015-2019 mentor campus at IIIT Allahabad (Jhalwa, Prayagraj); permanent campus Chak Ganjaria, C. G. City, Lucknow 226002 (address printed on every profile page, footer "2019 IIIT Lucknow").
The 2022-23 annual report dates Director Sherry w.e.f. 28/02/2019. The first archived faculty page is Dec 2019. The PIN and years of the campus move were not verified from a dated source beyond this.

## Sources and endpoints
1. Live site (WordPress, `iiitl.ac.in/index.php/faculty/`): 52 cards (name, qualification, e-mail Cloudflare-obfuscated and decoded from `data-cfemail`, designation and roles). 52 profile pages `/index.php/personnel/<slug>/`
   (the Contact block gives the department; joining dates only in some CVs).
2. Wayback: CDX for `iiitl.ac.in/index.php/faculty/` (31 monthly captures 2019-12 to 2026-05, fetched with `id_`); CDX prefix for `/index.php/personnel/*` (143 pages; those not on the live list fetched,
   most are research scholars or staff and were dropped); `personnel_category` pages. Before Dec 2019 the site was Drupal (2019) and a static page (2017): no faculty lists archived for 2016-2018.
3. Annual reports 2015-16 to 2022-23 (English) from `wp-content/uploads`. Only 2022-23 has a text layer (faculty list, visiting list); the others are scans, no OCR tool available (gap).
4. ORCID public API: one expanded-search `affiliation-org-name:"Indian Institute of Information Technology Lucknow"` (65 hits, one page), then `/employments` for 22 name-matched candidates.
5. Not reachable: NIRF (see below).

## Former-faculty method
Presence per snapshot was tabulated (`data/presence.json`). FIRST = year of first appearance (or earlier dated evidence), LAST = year of the last snapshot listing the person. The page is clearly maintained
(later joiners appear in each snapshot). On the 2026-05 snapshot but not on the live list now: Arun Mohan Sherry (Director), Dhananjoy Dey, Kumud Tripathi, Anshima Chaudhari (consultant, excluded);
their LAST is 2026 and could be a few months earlier. The 2019-12 snapshot lists only 9 people (partial page): Abhishek Pandey and Shikha Gautam appear only there (2019-2019).
People who left between Dec 2019 and Sep 2021 (no snapshots) and anyone employed 2016-2019 are missed. Visiting faculty known only from a profile-page capture get that capture year for both ends.

## Identifiers (12 ORCIDs: 2 from institute pages, 10 from the ORCID API route)
Institute page: Ankita Srivastava (0000-0003-0802-8748, Scopus/ORCID link on her profile), Mainak Adhikari (0000-0003-0647-4656, also confirmed by the API: IIIT Lucknow 2021-2024; counted under the page route).
API route (employment at IIIT Lucknow and name match): Deepshikha Agarwal, Deepak Kumar Singh, Saurabh Shukla, Padma Tripathi, Rahul Kumar Verma, Varun Sharma, Manoj Joshi (visiting), Naveen Saini,
Vishal Krishna Singh, Chandranath Adak. Not accepted: Gaurav Tripathi, Amit Kumar Kushwaha, Vibhav Singh, Manpreet Rajpal, Akansha Singh, Prashant Singh, Sangeetha K P (no faculty employment at IIIT Lucknow; several are scholars),
Dipanjan Roy (Guest Faculty 2019 only, no row), 0000-0003-2455-1301 (no name).
Google Scholar 4 (Deepshikha Agarwal, Vinaya Sathyanarayana, Diptesh Kanojia, Mainak Adhikari; user ids from links on their profile pages), homepage 4, e-mail 64. No DBLP, Scopus or IRINS values.
ORCID lookup pending: no per-person ORCID searches were run for the remaining people (frugality rule).

## Decisions and ambiguous people
* Excluded as non-faculty although on the Faculty page: Aditya Narayan Singh (Sports & Gym Consultant), Deepak Kumar Maurya (Yoga Consultant), Aditi Thapliyal (Trainer, Dance & Music); from archived pages Anshima Chaudhari (Dance Consultant),
  Anuj Kumar Sharma (Sports and Yoga consultant), Manish Joshi (Yoga Instructor). Registrars, technicians and research scholars excluded.
* Abhinesh Kaushik and Arvind Chaturvedi: card blank, profile says "Visiting Faculty": kept as visiting. Abhinesh Kaushik was "Assistant Professor" in the 2022-23 annual report and a second person page `dr-abhinesh-kaushik-2` calls him Deputy Registrar: roles unclear, status taken from the live profile.
* Department on visiting profiles is often "Information Technology" even for non-IT people (e.g. Dheeraj Misra, finance): probably a template default, kept as printed, unreliable.
* Vishal Krishna Singh: 2022 profile says IT, 2022-23 annual report says Computer Science; CS used. Deepak Kumar Singh was "Visiting Faculty" in 2021 and is now Associate Professor and Dean (current, department blank).
* Sushil Kumar Tiwari: "Visiting" in 2021, now Assistant Professor; two slugs = one person. Neelu: `dr-neelu` / `dr-neelu-singh` = one person. Brijesh Kumar Chaurasia: two slugs and a "Kr." variant = one person.
* Naveen Saini: ORCID says IIIT Lucknow 2022-2024, last snapshot 2023-11; LAST taken from the snapshot (ORCID dates self-declared). Chandranath Adak: LAST 2022 from snapshots (ORCID 2021-2022 agrees).
* No mentor-faculty (IIIT Allahabad) visiting rows could be established. TCS Faculty (Suhas Rautmare, Satish Kulkarni) are 2022 industry teachers: visiting. Prosenjit Gupta ("Algorithms Faculty") and Shuchi Aggarwal ("Design & Thinking") are on the visiting list: visiting.

## Size check and NIRF
The NIRF submission could not be obtained: `nirfindia.org` answers 403 to the fetcher (not bypassed), Wayback copies of the ranking pages do not list IIIT Lucknow, its NIRF code is unknown and the institute site has no NIRF page.
Zero current rows are NIRF-confirmed. Substitute check: the live Faculty page has 52 cards = 23 regular + 26 visiting/adjunct + 3 non-faculty consultants; the 2022-23 annual report lists 16 regular faculty and about 30 visiting names;
the 2026-05 snapshot shows 49 cards. Growth from 16 to 23 regular faculty fits the 2023-2026 recruitment drives (advertisements and interviews Jul 2023 for Mathematics, Management and Humanities, CS) and the August 2026 joiner.
The target 150 in `iiits.json` is planned strength, not a count.

## Known gaps
No faculty lists for 2016-2018 (mentor era at Allahabad), so early and mentor faculty are missing; no snapshot between Dec 2019 and Sep 2021; scanned annual reports not OCRed (joining years missing);
NIRF inaccessible; joining_year blank for 60 of 71 rows; department blank for 11 rows; ORCIDs only from the affiliation search.
