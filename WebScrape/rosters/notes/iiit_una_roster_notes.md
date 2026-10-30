# IIIT Una (Indian Institute of Information Technology Una, Himachal Pradesh, PPP IIIT) faculty roster: lab notes

Run: October 2026, operator Arihant Tripathy (IIIT team). Output: `rosters/iiit_una_faculty.csv` (94 rows).
Working files (not in repo): `C:\Users\Arihant\rm_work\iiit_una_roster\data\`, scripts in `...\code\` (nirf_parse.py, arch.py, build.py, final.py).

## Totals
current 37, former 43, visiting 13 (NIT Hamirpur mentor faculty), emeritus 1, adjunct 0.

| unit (current name) | current | former | visiting | emeritus |
|---|---|---|---|---|
| School of Computing (SoC; includes former CSE and IT departments) | 18 | 21 | 7 | 0 |
| School of Electronics (SoE; former ECE department) | 11 | 10 | 6 | 0 |
| School of Basic Sciences (SoBS) | 8 | 9 | 0 | 1 |
| department blank (NIRF-only people) | 0 | 3 | 0 | 0 |

Unit mapping: CSE and IT (2016-2019 static site) -> School of Computing; ECE -> School of Electronics; "Basic Science" -> School of Basic Sciences. There is no separate humanities/management/design unit; the institute has only these three schools.

## Campuses (verified)
* 2014-15 to 2018-19: classes at the mentor NIT Hamirpur, Hamirpur HP 177005 (institute report, 1st convocation 29 Mar 2019; archived site "Presently IIIT Una (Saloh) has started its functioning from NIT Hamirpur", page of 12/04/2016).
* Transit campus I: NIT Hamirpur campus. Transit campus II: Chandpur, Haroli, Una (hired May 2019; first-year students from AY 2019-20), per Establishment-of-Institute-Report and 1st convocation report.
* Permanent campus: village Saloh, Haroli, Una, HP 177209 (land of about 635 kanal 8 marla; MoU with CPWD June 2018). The PIN 177209 is as given in the brief; the reports I read name the village and tehsil but not the PIN, so the PIN is not independently verified.
* Years used for faculty windows: the whole 2016-2026 window is one institute; no separate campus rows were made.

## Sources and endpoints
1. Institute website is a React single-page app (`https://iiitu.ac.in/`); the page HTML is empty. Endpoints read out of the JS bundle (`/assets/index-*.js`, `People-*.js`, `Nirfpage-*.js`):
   * `https://api.iiitu.ac.in/api/schools` (3 schools: SOC, SOE, SOBS)
   * `https://api.iiitu.ac.in/api/faculty/searchBy/school/<school _id>` (returns every faculty record including `isActive:false` ones; 24 SOC, 12 SOE, 13 SOBS incl. one test account "Admin Tester" which I dropped). Profile pages are `https://iiitu.ac.in/schools/<CODE>/faculty/<_id>`.
   * `.../api/associate-dean/all`, `.../department/allDepartments`, `.../orgStrTree`, `.../leadership` (faculty in-charges, directors; no person outside the school lists; `pastLeadership` is empty).
   * `.../api/nirf` -> NIRF PDFs on `https://cdn.iiitu.ac.in/uploads/nirf/` (2024 overall, 2025 engineering, 2025 SDG, 2026 engineering).
2. NIRF faculty tables (primary source for years): 2024 (34 rows), 2025 eng (41), 2025 SDG (41), 2026 eng (42), parsed from `pdftotext -raw` output. NIRF year N is treated as presence evidence for year N-1 (the 2026 table carries leaving dates up to Sep 2025).
3. Internet Archive, last capture per year plus a mid-year one where there were several: `faculty/default.html` (2016-17; names no faculty, says NIT Hamirpur faculty teach the students), `cse/faculty.html`, `ece/faculty.html`, `it/faculty.html` (2017-Mar 2019), `cse-faculty.html`, `ece-faculty.html`, `basicscience-faculty.html` (Apr 2019-2020), WordPress `department/school-of-computing/faculty/` and `.../school-of-electronics/faculty/` (Dec 2022-Jun 2024). CDX showed no capture of a school-of-basic-sciences faculty page and none of any faculty list between Feb 2020 and Dec 2022 (see gaps). Seven snapshot fetches returned DEAD (archive timeouts: three cse-faculty captures of Dec 2019 and May-Jul 2020, two 2017 faculty/default, two 2017 it/faculty); the same-digest or neighbouring captures were used.
4. Institute reports via archive: Establishment-of-Institute-Report (2022), 1st convocation report (Mar 2019). Used for: founding Director S. Selvakumar joined July 2018; faculty strength 13 SoC / 6 SoE / 4 SoBS in Mar 2019 and 18 / 9 / 10 in 2022; recruitment of regular faculty 27-30 Nov 2021.
5. ORCID public API (see below). IRINS, Scopus, OpenAlex, Google Scholar scraping not used.

## How current / former and years were set
* current = `isActive:true` on the institute API (the live site). Tie-break: institute list wins over NIRF. Conflicts: five people NIRF 2026 shows as working (Divyansh Thakur, Satish Kumar (SoC, joined Jun 2023), Ankur Kumar, Vandana Kushwaha, Akansha Moral) have `isActive:false` on the site: treated as former, last year 2025 (last NIRF evidence), uncertain by up to a year. Dr. Rishabh Deo Pandey: only the API record (profile created Oct 2025, now inactive, no NIRF row): range 2025-2025 from the record creation date, flagged weak.
* joining_year: NIRF joining date year (earliest across the four tables), else a dated "Experience at IIIT Una" entry in the person's profile, else blank. NIRF dates for contract staff are contract start dates. Some people shown as "Assistant Professor (Contract)" before being regular (Nishtha Hooda 2020, Ambigavathi M 2021 guest/contract then regular): the earlier date is used.
* Former range: FIRST = joining year, else first archived appearance; LAST = NIRF leaving year, else last archived/NIRF presence year. Where the only evidence is the archive, joining_year is blank and FIRST is an upper bound for the joining year (first appearance on an archived faculty list). People with only an archive appearance: Akanksha Puri, Anjum Sharma, Basudha, Ishita Vaidya, Jasleen Kaur, Kushal Sharma, Kushal Singh, Mandeep Kumar, Neha Mahajan, Priyabrat Garanayak, Ram Murti, Rama Gaur, Sarthak Chauhan, Shawli Bardhan, Sonali, Sushil Pandey, Suveer Guleria, Vanita Arora, Sarthak. Ishita Vaidya's first year 2019 is the first archive capture of the new faculty era; she and others listed in Feb-Mar 2019 may have joined 2017-18 (Richa Thakur and Himani Joshi, listed the same day, joined Apr 2017 per NIRF).
* Gap 2020-02 to 2022-12: no archived faculty list. People last seen 2019 or 2020 (e.g. Anjum Sharma, Sonali, Sushil Pandey, Priyabrat Garanayak, Rama Gaur, Kushal Singh, Ram Murti) may have stayed longer; LAST is a lower bound. Rama Gaur: ORCID employment 2019-2019 agrees.
* S. Selvakumar (founding Director, regular post at the institute): joined July 2018 (institute report); last listed Nov 2023 on the SoC page, the 24 Jun 2024 capture lists Director Manish Gaur (joined 23 Apr 2024 per NIRF). LAST=2023 is therefore a lower bound (he may have served into early 2024). Listed as `former`, department SoC. Advertisement for a new Director Dec 2022.
* Amar Nath Gill: "Professor of Emeritus" on the SoBS page 2019-2020: `emeritus` (2019-2020). Dated sources do not extend beyond Feb 2020.
* Mentor faculty from NIT Hamirpur: the 2017-2018 CSE/ECE pages list only NIT Hamirpur staff (@nith.ac.in e-mails): Narottam Chand (HoD CSE), Kamlesh Dutta, T. P. Sharma, Naveen Chauhan, Siddhartha Chauhan, Madhu, Surinder Soni (HoD ECE), Vinod Kumar Kapoor, Rajeevan Chandel, Ashok Kumar, Gargi Khanna, Ashwani Rana: `visiting`, range 2017-2018 (earliest capture in the archive is Sep 2017; the mentor arrangement itself runs 2014-2018, so FIRST is an archive upper bound). The mentor director is not named on any dated page and was not added. Ambiguous: Keshav Kaundal (Mar 2019 CSE list, @nith.ac.in e-mail, listed alongside contract staff): kept as `visiting` mentor (2019-2019).
* No one employed by the mentor institute held a post at IIIT Una on any page I saw, so no mentor-institute post-holder is `adjunct`.

## Ambiguous people and decisions
* Two Satish Kumar: SoE (NIRF join 25-07-2018, still current) and SoC (NIRF join 30-06-2023, inactive on site): two rows.
* Sumit Kumar: "Mr./Dr. Sumit Kumar" on ECE pages 2019-2020 and a new SoC "Dr. Sumit Kumar" (profile created Aug 2026). Possibly the same person; merged into one `current` row (SoC), joining_year blank, archive evidence 2019-2020 recorded here only.
* Naman Garg is Head of SoE and also listed as HoD of SoBS on the API: one row, SoE.
* Gurpreet Kaur is also the Public Information Officer: one row, SoE; the 2019-20 pages show her as "Ms." (contract), NIRF joining 16-07-2018.
* Name variants merged: Shivdutt/ShivDutt/Shiv Dutt Sharma, Vejandla Kishore/Kishore Vejandla, Shonal Chouskey/Chouksey, Madam L Verma, "Dr. Tanu" = Tanu Wadhera, G S Grewal = Gurinderbir S. Grewal, Sukriti = Sukriti Chaudhary, Ashwini Kumar = Ashwini Kumar Malviya.
* Minakshi Shastri: ORCID 0000-0003-3679-9961 not used (its IIIT Una record is a PhD-student role).
* Departments left blank (NIRF-only, no page assigned them): Ashish Maurya (2025), Sofia Singla (2022-2024), Vandita Sharma (2022-2024).
* Visiting-professor posts mentioned in the 2019 report ("Visiting Professor in Mathematics, Engineering Economics and Management, Basic Environmental Science") are not named anywhere; none added. Guest faculty (advertised 2022-2023, "Guest Faculty" SoC/SoBS) are excluded unless listed on faculty pages (Ambigavathi M appears as Guest Faculty 2021-23 before her regular post).
* Faculty on contract, adhoc and "Associate Faculty Member" persons are included as faculty with the designation kept ("Faculty on contract"), per the brief.

## Identifiers
* ORCID: 32 rows. 20 taken from the institute's own profile page (API social links), 12 via the ORCID public API.
  * API route: one expanded-search (`affiliation-org-name:"Indian Institute of Information Technology Una" OR "IIIT Una"`, 83 hits, only the first page needed), then `/employments` for 14 name-matched roster people. Accepted (employment at IIIT Una and name match): Shiv Dutt Sharma, Girdhar Gopal, Nitish Katal, Sofia Singla, Himani Joshi, Rama Gaur, S. Selvakumar ("Selvakumar Subramanian", role Director), Ashish Maurya, Sahil, Nishtha Hooda, Ina Thakur, Rishabh Deo Pandey (employment entry without dates). Rejected: Minakshi Shastri (student role), Divyansh Thakur (no IIIT Una employment entry). No 429 responses; no "ORCID lookup pending" list. No per-person name searches were made, so roster people without an ORCID in the affiliation hits stay blank.
  * Other persons in the affiliation hits are students or not on any list seen (e.g. Abhishek Gautam, Preeti Puri, Mukul Bedwa, Naresh Kumar N, Ramesh Babu Jarapala, Surender Kumar, Ajay K Sharma, Anamika Singh): not added.
* Google Scholar: 28 rows from the institute profile pages (links normalised to `?user=` form; three had login-redirect wrappers, id extracted). Homepage: 6 from the profile pages. DBLP, Scopus, IRINS: blank (not on institute pages).
* e-mail: from the profile/API; archive-only people have none (archive e-mails are personal addresses and were not copied).

## Counts and size check
* joining_year filled for 57 of 94 rows (NIRF dates 54, profile dated experience 3).
* Current-faculty size check: NIRF 2026 (engineering, data for 2024-25, parsed 42 rows) shows 35 "currently working"; the live site lists 37. The 35 minus five people now inactive on the site (above) = 30 NIRF-confirmed current rows; plus seven additions after the NIRF submission (Vishal Kaushal, Sumit Kumar, Narendra Kumar, Jayant Pal, Pramesh Kumar joined Aug-Sep 2026; Sonu and Bhamati Dash, profiles created Oct-Nov 2025, Bhamati's experience entry starts Sep 2025) = 37. All current rows with an NIRF counterpart: 30 of 37 NIRF-confirmed. The 1st-convocation report (Mar 2019) reported 13+6+4 = 23 faculty and the 2022 report 18+9+10 = 37 (all categories), consistent in magnitude. The institute's NIRF "total faculty" headline counts were not separately extracted.
* Per-unit parse check against NIRF: NIRF tables carry no unit; unit comes from the site/API (SoC 18, SoE 11, SoBS 8 current).

## Known gaps
* No archived faculty list between Feb 2020 and Dec 2022, so tenure ends for the 2019-20 cohort and starts for 2020-22 joiners (other than NIRF-dated ones) are bounds.
* No dated source for people on the 2019 pages who are absent from NIRF (leaving before 2023).
* `isActive:false` people are assumed to have left; last year taken from NIRF 2026 (2025) may be early.
* Joining years for regular faculty recruited in the Nov 2021 round come from NIRF dates (2021-2023), which may be reporting dates.
* The new Aug-Sep 2026 contract hires have no joining year from a dated source other than the profile.
* Mentor-faculty tenure (2014-2018) is bounded only by archive captures from Sep 2017.
