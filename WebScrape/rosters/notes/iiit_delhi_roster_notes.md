# IIIT Delhi faculty roster (2016-2026): lab notebook

Built 2026-10-27 by Arihant Tripathy (IIIT team) with Claude. Output: `WebScrape/rosters/iiit_delhi_faculty.csv` (360 rows). All fetches went through `polite_get.py`.
Downloads and scripts: `C:/Users/Arihant/rm_work/iiit_delhi_roster/{data,code}` (not in the repo).

## Totals
| status | rows |
|---|---|
| current | 97 |
| emeritus | 1 (Pankaj Jalote) |
| former | 154 (56 with site-list evidence, 98 NIRF-only/other) |
| adjunct | 81 |
| visiting | 27 |
| total | 360 (joining_year filled about 259; homepage 87) |

Per department (current / former / adjunct+visiting; blank = no source gives a unit): CSE 28 (+1 emeritus) / 20 / 19; ECE 23 / 8 / 10; Computational Biology 11 / 2 / 14; Mathematics 13 / 2 / 4;
Social Sciences and Humanities 17 / 2 / 6; Human-Centered Design 5 / 2 / 4; blank 0 / 119 / 51 (mostly NIRF-only lecturers and ad hoc staff, and 2016-17 NIRF-only names).
Unit names: the site uses CSE, ECE, CB ("COMP-BIO" in 2016), Math ("Applied Maths" in 2016-17), SSH ("SS" in 2016-17), HCD ("DES" in 2016-18); mapped to the current names above.
Second units (row keeps the first-listed unit): Amarjeet Singh CSE/ECE; Angshul Majumdar ECE/CSE; Anubha Gupta ECE/CSE; A V Subramanyam ECE/CSE; Donghoon Chang CSE/Math; Pushpendra Singh CSE/HCD; Rajiv Raman CSE/Math;
Saket Anand CSE/ECE; Somitra Sanadhya CSE/Math; Subhasis Banerjee CSE/ECE; Sujay Deb ECE/CSE; Naqueeb Warsi ECE/Math; Saswata Shannigrahi CSE/Math; Arun Balaji Buduru CSE/HCD; Debarka Sengupta CB/CSE;
Rajiv Ratn Shah CSE/HCD; Rahul Mohanani CSE/HCD; Jainendra Shukla CSE/HCD; Arani Bhattacharya CSE/ECE; Diptapriyo Majumdar CSE/Math; Manuj Mukherjee ECE/Math.

## Sources and endpoints
1. Institute site `iiitd.ac.in`. The live host answers DEAD:SSLError in the fetcher, so everything was read from Wayback. Institute-wide list `/people/faculty` (cards with `dept`/`type` attributes: regular, visiting, pop, emeritus; name, designation with unit codes, e-mail),
   `/people/adjunct-faculty`, `/people/visiting-faculty`, `/people/pop-faculty`, `/people/emeritus-faculty`, profile pages `/<slug>`. No JSON endpoint is used by these pages (cards are server-rendered, filtering is client-side JS).
   CDX: `iiitd.ac.in/people/faculty` has monthly captures 2016-03..2026-08. I fetched the last capture of every quarter (41 captures). Three page layouts (2016 `div.cell`, 2017-2020 `facultycard` with `<strong>`, 2020+ `col-md-2 card` with `team-title`) are handled by one parser; parsed counts are 48 (2016-03), up to 110 (2023-09), 98 (2026-08).
   Adjunct, visiting, pop, emeritus pages: last capture per half-year (19 / 20 / 7 / 2 captures).
2. NIRF data submissions (the institute's own `/nirf` page lists the PDFs; read from Wayback, nirfindia.org not used): 2017 (names only, no dates), 2018-2025 with joining/leaving dates, "currently working", association type. `pdftotext -raw`, regex records;
   parsed rows equal the highest serial number in every year: 71, 71, 79, 96, 106, 111, 132, 145, 184 (2017-2025). The NIRF 2026 PDF is listed on the page but not archived (404), so NIRF coverage ends with the April 2025 submission.
3. CB department site `cb.iiitd.ac.in/cb-faculty.php` (2022 capture): used only to confirm that G. P. S. Raghava is CB faculty.
Not done: ECE/CSE/Math/SSH/HCD department pages and annual reports (the institute-wide list covers all units and wins by decision); the site has no former-faculty page.

## How status and years were established
* current/emeritus: present in the 2026-08-08 capture of `/people/faculty` (97 regular + Jalote as emeritus). People last seen 2026-06 (e.g. Debidas Kundu) are recorded as former with LAST 2026.
* adjunct / visiting (current): present in the latest (2026-06 / 2026-07) capture of the respective page. Former regular faculty now on the adjunct page are `adjunct`, range = first evidence to 2026 (about 19 people, e.g. Tanmoy Chakraborty, Ponnurangam Kumaraguru, Chetan Arora, Dhruv Kumar).
* former: not on any current list. FIRST-LAST uses only regular-faculty evidence (site list type regular, NIRF Regular/Adhoc rows with year mapping, NIRF leaving dates). A later adjunct/visiting tail is NOT counted in LAST (50 people; e.g. Alexander Fell regular 2013-2018, adjunct page 2019-2025).
  NIRF year to evidence year: 2017->2016, 2018->2017, 2019->2018, 2020->2019, 2021-2025 same year (filing dates from file names). LAST resolution on the site list is one quarter; NIRF leaving-date year is also used. The site list is maintained (it adds joiners every quarter), so snapshots are not stale.
* joining_year: earliest NIRF joining date. Where the person was already on the site list before that date it is a rejoining/regularisation date, so the field is blank (Sayan Basu Roy, Gourab Ghatak, Angshu Das). People first seen in the 2016-03 capture without a NIRF date have blank joining_year.
  FIRST in a "Former faculty (FIRST-LAST)" range is the NIRF joining year when known (may be < 2016), otherwise the first evidence year.
* Window: 2016-01-01 onward; the 2016-03 capture is the first available, so anyone who left before it is invisible.

## Decisions on ambiguous groups
* NIRF-only people (not on any site list): 91 former + 6 visiting. Mostly "Lecturer" rows (57 working in NIRF 2025, joined 2016-2024) and "Ad hoc / Other" rows 2021-2024, plus six 2016-17 names (Saket Srivastava, Shishir Nagaraja, Soshant Bali, Tanusri Bhattacharya, Hrishikesh Bhattacharya, Srikanth Sripalli).
  Following the brief they are included with blank department. Their NIRF "currently working = Yes" in 2025 means "former (..-2025)" is "last evidenced 2025", not a confirmed departure.
* Visiting cards on the main list until 2023 (Anoop Ratn, Aman Samuel, Payel Mukherjee, Vinish Kathuria) are NIRF Regular lecturers; they stay `visiting` while on the visiting page and `former`/`visiting` by their last site listing otherwise.
* Dheeraj Sanghi (visiting card 2017 with a Dean title) is kept `visiting`; whether he held the post in additional charge from another institute could not be established.
* Name variants merged (alias table in `code/aliases.py`): Samaresh Chatterjee/Chatterji, G S Visveswaran/Visweswaran, Manohar Khushlani/Khushalani, Naqueeb A Warsi, Somitra Sanadhya, Subhadip Raychudhuri, Rinku M Shah, Vijaya Raghava / V. Raghava / Raghava Mutharaju, Sanjiva Shankar / Sanjeeva Dubey, Vivek A Bohara, G.P.S. Raghava, Sambuddho / Sambuddho Chakravarty.
  Not merged (distinct NIRF entries): Hrishikesh B. Acharya vs Hrishikesh Bhattacharya; Ashish Kumar Pandey vs Satish Kumar Pandey. A card named "IIIT-Delhi" (2017-2021, visiting list) was dropped as a non-person.

## Identifiers
ORCID 0 from institute pages (none printed); the ORCID API quota of this machine is exhausted, so no API call was made. ORCID lookup pending: all 360 people. Google Scholar, DBLP, Scopus, IRINS: 0 (profile pages of the 98 current/emeritus people carry no such links; DBLP column left to the later tool).
Homepage 87 (the "Web Profile" link on 83 profile pages plus personal links printed on the lists). profile_url for current people = `https://iiitd.ac.in/<slug>`; profile pages were read from Wayback (2026), one of 98 failed. Former people: profile pages not fetched. E-mail from the cards.

## Size check
Website list (2026-08): 98 cards (97 regular + 1 emeritus). NIRF 2025 (filed 2025-04): 184 rows, 176 working = 115 non-Lecturer rows + 61 "Lecturer" rows (teaching/ad hoc staff not on the faculty page). The gap between 115 and 98 consists of
visiting/adjunct-type rows and people who left in 2025-26 (e.g. Anand Srivastava, Dhruv Kumar, Koteswar Rao Jerripothula, Garima Rani, Tammam Tillo, Ranjan Bose). Current rows with a NIRF-2025 working=Yes row: 92 of 97 (the rest joined after April 2025).
NIRF non-lecturer working counts: 64 (2018), 79, 84, 102, 103, 113, 141 (2024), 115 (2025); site list sizes: 73 (2018-03), 93 (2019-12), 102 (2021-03), 104 (2022-12), 109 (2023-12), 100 (2025), 98 (2026). Same order of magnitude; the site lists include visiting cards before 2023.

## Known gaps
* Quarterly sampling: someone who joined and left inside one quarter is missed; LAST is accurate to about 3 months.
* People who left before the 2016-03 capture are not seen. Departures between NIRF 2025 and now appear only via the site list.
* NIRF 2026 not archived. Pre-2018 NIRF has no dates. No annual reports or department pages read. Former people have no profile_url/homepage.
* The roughly 97 NIRF-only rows have no department and are low-confidence members of "faculty"; filter on blank `department` for a stricter roster.
