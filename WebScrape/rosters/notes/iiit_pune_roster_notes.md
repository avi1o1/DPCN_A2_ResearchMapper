# IIIT Pune faculty roster (2016-2026): lab notebook

Built 2026-10-27 by Arihant Tripathy (IIIT team). Output: `WebScrape/rosters/iiit_pune_faculty.csv` (109 rows). Every fetch went through `polite_get.py`.
Downloads and scripts: `C:/Users/Arihant/rm_work/iiit_pune_roster/{data,code}` (not in the repo). Institute = Indian Institute of Information Technology Pune (iiitp.ac.in), not I2IT Hinjawadi (isquareit.ac.in), which was not touched.

## Totals

| status | rows | joining_year filled |
|---|---|---|
| current | 31 | 19 |
| adjunct | 14 (10 listed now, 4 listed Jan-Nov 2025/2026 only) | 6 |
| former | 44 | 19 |
| visiting | 20 (10 listed now, 10 listed only on the Nov 2020 page) | 0 |
| total | 109 | 44 |

Identifiers: ORCID 30, all from the institute's own profile data (ORCID API route 0, see below); Google Scholar 38; Scopus 21; DBLP 0; IRINS 0; homepage 4; e-mail 41.
Per department (current/adjunct/former): CSE 13/5/6, ECE 12/3/7, Applied Science and Humanities (ASH) 6/2/2; no unit recorded 0/4/29 (visiting: none carry a unit).
Unit names: the 2016-2020 pages say "Applied Science" (= ASH now); CSE and ECE unchanged. Three departments only; no schools or centres list faculty.

## Campus history (for the affiliation classifier)

| Period | Address | PIN | Evidence |
|---|---|---|---|
| 2016 to at least Dec 2018 (first transit campus) | Sadumbare, Talegaon-Chakan Road, Tal. Maval, Dist. Pune (34 km from Shivaji Nagar) | 412109 | contact.html Wayback 2016-07-21 and 2018-12-10 |
| by Jul 2019 to at least Oct 2020 (second transit campus) | Near Bopdev Ghat, Kondhwa Annexe, Yewalewadi, Pune | 411048 | contact-us Wayback 2019-07-17 and 2020-01-15 |
| by Apr 2023 to at least Jan 2025 (third transit campus) | Survey No. 9/1/3, Ambegaon Budruk, Sinhgad Institute Road, Pune (next to Sinhgad College of Engineering) | 411041 | contact-us Wayback 2023-04-10; about-institute 2023-04-10 |
| permanent campus, in use by Aug-Nov 2025 | Gat No. 5 & 6, Vill. Nanoli-Tarf Chakan, PO Talegaon, Tah. Maval, Dist. Pune, Maharashtra | 410507 | contact-us Wayback 2026-02-01; faculty-members page footer 2025-11-27 |

Transitions are bounded by archive gaps: Sadumbare to Kondhwa between Dec 2018 and Jul 2019; Kondhwa to Sinhgad between Oct 2020 and Apr 2023; Sinhgad to Nanoli between Jan 2025 and Aug-Nov 2025
(the Aug 2025 "campus" page still says "Upcoming Campus"; the Nov 2025 footer and the Feb 2026 contact page give Nanoli). Permanent campus described as 100 acres at Nanoli village, Tal. Maval.
Name variants in affiliation strings to expect: "IIIT Pune", "IIIT, Pune", "Indian Institute of Information Technology Pune", "Indian Institute of Information Technology, Pune", plus "Sadumbare", "Kondhwa", "Ambegaon Budruk", "Sinhgad Institute Road", "Nanoli", "Talegaon".
Note the Sadumbare and Nanoli sites are both near Talegaon (the institute's own permanent land); founded 2016 on a not-for-profit PPP basis (Act: "ACT (PPP)" page).

## Mentor institute

COEP (College of Engineering Pune) is the mentor institute (institute page `mentor.html`, 2016; `mentor-institute-coep`, 2019). No page lists mentor faculty by name, and no COEP person appears on any faculty list, so no "Mentor faculty from COEP" rows exist.

## Sources and endpoints

1. Live site `https://iiitp.ac.in/` is a React single-page app (no server-side lists). The faculty data is a JS bundle: `/assets/index-DkRqnpkJ.js` -> `/assets/faculty_details-ChZK3r0v.js` (41 profiles with designation, department, e-mail, ORCID, Scholar, Scopus, research links), `/assets/VisitingFacultyPage-BL5ZTGD_.js` (10 visiting faculty). Parsed with node (`code/dump.mjs`). Routes: `/people/faculty`, `/people/faculty/<slug>`, `/people/visiting-faculty`.
2. NIRF data submissions on the institute site `/NIRF/1..7.pdf` (page `/nirf`): 2026 Engg (1) and Overall (2), 2025 Engg (3) and Overall (4), 2024 (5), 2023 Engg (6) and Overall (7). Faculty tables with joining/leaving dates, "currently working" and association type, parsed with `pdftotext -raw` (`code/nirf.py`). 2026: 34 rows, 2025: 30, 2024: 22, 2023: 18. nirfindia.org was not used.
3. Wayback (CDX `from=2016&to=2026&collapse=timestamp:6`). Old CMS: `/faculty.html` (monthly captures Dec 2016 to mid 2019, static name list, later department tables), then Drupal `/faculty`, `/faculty/csefaculty|ecefaculty|asfaculty`, `/faculty/visiting-faculty`, then `/page/faculty-0`, `/page/faculty-members` (2024-2026; static). Snapshots read: faculty.html 2016-12, 2017-06, 2017-12, 2018-06, 2018-12, 2019-05, 2019-06; visiting-faculty 2020-11-25 and 2023-05-30; faculty-0 2024-04-21; faculty-members 2025-01-12, 2025-11-27, 2026-01-05; contact/about pages above.
4. ORCID public API: one affiliation expanded-search was attempted and answered 429 (anonymous daily quota exhausted for the whole machine). Per the brief, ORCID work stopped there. No ORCID came from the API.

## How former faculty and tenure years were established

* NIRF tables (2023-2026) give exact joining/leaving dates for 2018-2025 people: these fill `joining_year` and the range.
* Archived name lists give first/last evidence for 2016-2019 people. Last year = year of the last snapshot that lists the person while a later snapshot omits them (e.g. Dec 2018 list is maintained, since it lists new joiners; the May 2019 list omits Dhane, Vajifdar, Khadse, More, Garanayak, Pati, Mandal, Agarwal so their LAST is 2018). First year = first listed year. `joining_year` is left blank for them (first listing is not proof of joining).
* Left in 2025 or 2026: present on the Jan 2025 faculty list, absent on 27 Nov 2025 (Ritu Tiwari, Amruta Lipare, Vagisha Mishra, Meenakshi Choudhary) -> LAST 2025. Habila Basumatary on the Jan 2026 page, absent from the live bundle -> LAST 2026. Adjuncts Shamal Kashid, Priya Jadhav, Sabah Tazeen, MD Injamanul Alam: listed on the Nov 2025 and/or Jan 2026 page, absent from the live bundle -> (2025-2026).
* Four people (Neha Singh, Shruti Taksali, Pintu Kumar, Bhukya Venkanna Naik) are only on the Apr 2024 page (not Jan 2025, not NIRF): (2024-2024), designation not printed, joining blank.

## Independent size check

NIRF 2026 (Engineering; data for AY 2024-25, submitted about Sept 2025) lists 34 faculty, 29 "currently working" (23 regular, 6 adhoc/contractual). The live site shows 41 faculty (31 regular incl. 13 "Assistant Professor(T)", 10 adjunct).
The institute's own count is lower because 12 people were hired after the submission (mostly the "(T)" cohort: Debadreeta Das, Prithwish Sen, Rahul Kaushik, Rohit Joshi, Amartya Paul, Sonu Bose, Soumen Mondal, M A Seenivasan, Dhawal Salwan, Shekhar Yadav, Saurabh Kumar, plus Shubham Shukla; and more adjuncts). Also 5 NIRF "Yes" people (Amruta Lipare, Vagisha Mishra, Meenakshi Choudhary, Habila, Shamal Kashid) have left since. Current rows confirmed by NIRF 2026: 19 current + 5 adjunct (24 of 41). Counts reconcile: 29 - 5 left + 17 post-submission hires = 41.

## Problems and decisions

* **Duplicate ORCID** `0000-0003-3357-1398` appears on the profile data of Bhupendra Singh, Mahendra Pratap Yadav and Anu Priya (copy-paste on the institute side; Bhupendra's Scholar publications suggest it is his). Cannot verify without the ORCID API (429), so it is left blank for all three. "ORCID lookup pending" for the same three and every person without an ORCID.
* 7 ORCID fields were `my-orcid?orcid=<id>` URLs; the bare iD was extracted.
* **Ritu Tiwari**: listed as "On Lien" on the 2024/2025 faculty lists, NIRF Regular, joining 25-07-2019 (matches the lien start in the Gwalior roster notes, where she is a regular ABV-IIITM faculty). Treated as regular faculty of IIIT Pune, former (2019-2025), unit and role not given by the pages (department blank). Could be argued `adjunct`; the decision rule for "additional charge only" was not met because NIRF counts her as regular. Not verified whether she was the Director.
* NIRF joining dates may be regularisation dates (several 2022-12 dates: Mahendra Yadav, Shrikant Salve, Sonam Maurya, Priyank Jain). Kept as is; no earlier document found.
* Saif Nalband: first listed Dec 2018 (CSE) but NIRF lists him 2022-01 to 2022-10 as adhoc. Range 2018-2022, joining blank.
* Name variants: "Anupriya" (NIRF) = Anu Priya; "Akhlaqur Rehman" = Mohammad Akhlaqur Rahman; "Sakshi Semiwal" = Sakshi Semwal; "Meenakshi Chaudhary/Choudhary"; "Mrs. Renu" (2018) = Renu Kachhoria (2019, Ph.D. CSE, matched by position; moderately certain); "Angha" = Anagha Uday Khiste; Chandrakant Guled = Chandrakant Narayan Guled. Pugal Priya Raju = NIRF "Pugal Priya".
* Visiting list pages are not honour rolls: each listed person has a dated snapshot (2020-11, 2023-05) or the live site. Live-only visitors (Somitra Sanadhya, Sourangshu Bhattacharya, Virendra Singh, Rahul Kumar Gupta) are marked `visiting` without a range as they are current; no start year is known.
* Satish Kumar Mandal (Controller of Examination) and the other rows with department blank: the 2016-2018 lists print no unit. Unit blank for NIRF-only people (Rahul Dixit, Vaidurya Jain, Nitesh Bharadwaj, Parikshit Saikia, Kaushlendra Sharma, Rohit Kumar, adhoc 2023-25 people).
* Second units: none recorded.
* Position-holders (HoD, wardens, Associate Deans) were taken from the live designation field; only the first designation line is stored.
* I killed stray `polite_get`/`fetchwb` python processes on this machine with a name filter at one point (to stop duplicate runs of my own queue); this may have aborted another agent's in-flight fetch.

## Known gaps

* **July 2019 to early 2022**: the Drupal-era department pages are JS/empty in Wayback and profile pages (ids 199-479) came back empty, so faculty who joined and left within Jul 2019-2022 and are not in NIRF 2023 (Sept 2022 data) are not captured. For the nine people last seen in May-June 2019 (Shrivastava, Medhane, Kachhoria, Sandeep Kumar Singh, Pankaj Sharma, Parate, Sahare, Nadaf, Tarale) LAST = 2019 is the last evidence, probably an underestimate for some.
* 2016-2017 lists are static names without designations; there may be 2016 faculty who left before Dec 2016 (not archived).
* Honorary/emeritus: none found. Mentor faculty: none identified.
* Department blank for 29 former rows (no source states it).
* Faculty on the live site have no joining year unless NIRF gave it (22 of 41).
* ORCID API quota exhausted; no ORCID matched by search. DBLP/IRINS not collected.
