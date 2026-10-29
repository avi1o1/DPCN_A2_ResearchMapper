# ABV-IIITM Gwalior faculty roster (2016-2026): lab notebook

Built 2026-10-27 by Arihant Tripathy (IIIT team). Output: `WebScrape/rosters/iiit_gwalior_faculty.csv` (137 rows). All fetches went through
`polite_get.py`. Downloads and parsing scripts are in `C:/Users/Arihant/rm_work/iiit_gwalior_roster/{data,code}` (not in the repo).

## Totals

| status | rows | joining_year filled |
|---|---|---|
| current | 78 | 70 |
| former | 12 (G K Sharma retired, 11 regular faculty who left) | 4 |
| visiting | 3 (Nirmal Roberts, Om Vikas, S G Deshmukh) | 2 |
| adjunct | 44 (24 adjunct + 1 honorary listed now, 19 no longer listed) | 25 |
| **total** | **137** | **101** |

Identifiers: ORCID 44 (17 from institute profile pages, 27 from the ORCID API route: affiliation search + `/employments` confirmation), Google Scholar 14,
Scopus 6, DBLP 1, homepage 16, e-mail 98, IRINS 0 (not used). Homepage values come only from the profile header, with institute/social/news links removed.

Per department (current / former / adjunct), department = unit printed on the staff page: Computer Science and Engineering 16/0/2,
Electrical and Electronics Engineering 19/2/2, Engineering Sciences 14/0/0, Information Technology 18/2/1, Management Studies 11/2/2.
No unit recorded: 0 current, 6 former, 3 visiting, 37 adjunct (the new site prints no unit for adjuncts; blank where no source gives it).
Unit renames: "Applied Sciences/Applied Science" (2016-2023 pages) = Engineering Sciences; "Business Administration" (Wayback department filter) = Management Studies;
"Electrical / Electronics" = Electrical and Electronics Engineering. Single campus (Morena Link Road, Gwalior 474015); one institute-wide list.

## Sources and endpoints

1. Live site (2026): `https://www.iiitm.ac.in/staff` (79 cards, institute-wide: name, designation, unit), `.../staff/adjunct-and-honorary` (24 adjunct + 1 honorary),
   profiles `/staff/faculty/<slug>` and `/staff/adjunct/<slug>` (104 fetched; e-mail, ORCID/Scholar/Scopus/DBLP links, homepage, sometimes "Date of Joining").
   `/whos-who` and `/departments/*` (HoD only) were read but add no members.
2. NIRF data submissions (`.../national-institute-ranking-framework`): 2025 and 2026, Engineering and Management PDFs (no earlier years posted). Parsed with `pdftotext -raw`.
   Tables carry joining/leaving date, "currently working" and association type. They list almost only current staff (2025 Engg 60 regular + 18 visiting; 2026 Engg 72 regular + 25 visiting).
3. Annual reports (`/annual-reports`): 2015-16 and 2017-18 to 2023-24 downloaded (no 2016-17 report is posted). They give the faculty list, adjunct lists, and dated lien/resignation/retirement notes.
4. Wayback Machine (CDX `web.archive.org/cdx/search/cdx?url=...&output=json&collapse=timestamp:6`, snapshots `/web/<ts>id_/<url>`):
   * 2016: `iiitm.ac.in/faculties/faculty` and `/index.php/faculties/faculty` (26 faculty; captures 2016-02..2016-08).
   * 2018-2026: `.../index.php/en/component/splms/?view=teachers` (about 40 captures, 39 usable, last 2026-05-11 with 79 entries); 2022-2024 department-filtered versions
     `...?view=teachers&department_name=<Applied Science|Business Administration|Computer Science|Electrical / Electronics|Engineering Science|Information Technology>` give each person's unit;
     profile pages `.../splms/teacher/<slug>` (2018-2025).
   * No faculty-list capture exists for 2017 (bridged by the 2017-18 annual report).
   Some 2024-2026 department-filtered captures failed during a DNS outage; the plain list captures cover the same years.
5. ORCID public API: one expanded-search `q=ror-org-id:"https://ror.org/008b3ap06"` (369 records, 2 pages of 200), then `/employments` for 30 name-matched candidates.

## How current / former / tenure years were decided

* current = on the 2026 staff page (the institute-wide list wins). Former = on a dated source in 2016-2026 and not on that page.
* `(FIRST-LAST)`: first and last year with evidence. Annual-report years are fiscal years and I used their start year (AR 2017-18 gives 2017), so AR-based starts may be one year early. Wayback captures use the capture year.
* Stale snapshots were not taken as presence: the 2018-2022 lists kept Chanak (on lien from Aug 2020) and Neetesh Kumar (left 29 Jun 2020) for some months; LAST uses annual-report dates (2021 and 2020).
* joining_year: NIRF joining date (about 61 current), profile statements (Ajay Kumar, Anuwedita Singh Jan 2024, Ritu Tiwari "since 2008", Pradip Swarnakar 2009), AR 2021-22 (S N Singh joined as Director 8 Apr 2022).
  Blank when no evidence (G K Sharma, Chanak, Neetesh Kumar, Daultani, Rajagopal, Bansal, most adjuncts). For adjuncts and visitors it is the NIRF appointment date.

## Independent size check

NIRF 2026 (Engineering) lists 72 regular faculty, all "currently working"; the live staff page gives 78 current rows. Reconciliation: 72 minus 3 who have since left
(Biswabandhu Jana, Nalin Kumar Sharma, Rashmi Ranjan Behera) = 69 present, plus 9 current people absent from NIRF (Neeraj K. Jaiswal, Narendra Kumar Dewangan, Ankur Jaiswal, Vijay Rao Kumbhare,
Jatoth Deepak Naik, Tsering Thargay, Neelesh Yadav, V Ramanjaneyulu Yannam, Anuwedita Singh) = 78. NIRF-confirmed current rows: 69 of 78. Eight of the nine are 2025-26 joiners;
Anuwedita Singh joined January 2024 and is missing from NIRF for an unknown reason. The Management NIRF sheet (28 regular) is a subset of the Engineering sheet.

## Conflicts and ambiguous people (decision)

* **Nalin Kumar Sharma, Biswabandhu Jana, Rashmi Ranjan Behera**: NIRF 2025/2026 flags all three "currently working" and none is on the live page. Sharma resigned 15 Dec 2023 (AR 2023-24) -> former (2023-2023).
  Jana last on the Wayback list 2026-05 -> former (2023-2026). Behera last list 2026-01 -> former (2024-2026). NIRF is stale for them.
* **Dheeraj Kodati**: only on Wayback lists 2026-03 and 2026-05, not on the live page -> former (2026-2026); unit unknown.
* **Gopal Krishan Sharma**: still printed as "(Retired)" on the staff page; superannuated 31 Aug 2023 (AR 2023-24) -> former (2015-2023).
* **Anupam Shukla**: "(On Deputation)" on the staff page (earlier lien as Director IIIT Pune, now Director SVNIT Surat) -> current, joined 2006.
* **Ritu Tiwari**: lien at IIIT Pune from 25/07/2019, resigned 29/12/2022 (AR 2022-23), back on the 2026 page; NIRF 20-06-2025 is a rejoining date -> current, joining_year 2008 (profile). The gap is not shown in the CSV.
* **Pradip Swarnakar**: unit not printed in any fetched source -> blank (not inferred). Left 31 Dec 2018 (AR 2018-19).
* **J C Bansal** (listed "On Leave" on 2016 pages, absent from AR 2015-16): former (2016-2016), unit blank. **Nirmal Roberts** (Visiting Faculty 2015-16): visiting.
* **K V Arya** (lien at AKTU 11 Sep 2017 to 27 Feb 2019) and **Manoj Kumar Dash** (lien from 8 Jun 2018): same persons, kept current.
* **Adjuncts**: AR 2017-18..2021-22 list V S R Krishnaiah, Prem Pyara, G S Singh, H M Gupta, N K Sharma, A K Singh, Manish Gupta (2017-2021; H M Gupta to 2025 via his 2025 profile).
  Wayback 2025 profile pages list Kripa Shanker, Guillermo Paya Vaya, H C Karnick, Sankar Kumar Pal, Navin Bishnoi, Peeyush Chandra, Vishnu Dutt Sharma, Sameep Mehta, Prawal Sinha, Y N Srikant, Ashok Chandra,
  P D Srivastava (2024/2025-2025; not on the live adjunct page). NIRF "Visiting" Om Vikas and S G Deshmukh (appointed 2014 / 2019, left 22 Jan 2024) -> visiting.
  NIRF calls all of these "Visiting" while the site says "Adjunct Faculty"; I used the site's term, and NIRF's term only for people not on the site.
  Prof. D P Agrawal (honorary, Ex-Director) is current; his joining_year 2014 is the NIRF visiting appointment, earlier Director years are not documented here.
* **Excluded**: N M Agrawal (2017 visitor, not faculty); Ravi P Agarwal (a 2025 Wayback profile URL seen in CDX, content not archived, so no designation evidence).
* Spelling variants merged: Purnedu/Purnendu Mishra, Godfrey/Godfery, Devangan/Dewangan, Srivastav/Srivastava, Kamal Chandra Das (NIRF "Chnadra").

## ORCID

Routes: 17 from institute profile pages; 27 from the API (ROR affiliation search, then `/employments` showing ABV-IIITM/Gwalior employment and a name match).
Rejected after the check: Manish Gupta 0000-0003-0848-6132 and Arun Kumar R 0000-0001-5605-2190 (no ABV-IIITM employment). Avadh Kishor has two qualifying iDs
(profile 0000-0002-4375-8773 kept; API 0000-0001-8358-1194 not used). No 429 responses, so no "ORCID lookup pending" list; people without an ORCID were not searched by name (quota).

## Known gaps

* No faculty-list capture for 2017 and no 2016-17 annual report: anyone who joined and left between Apr 2016 and Mar 2017 may be missing.
* Unit blank for 6 former, 3 visiting and 37 adjunct rows; joining year blank for most former and some adjunct rows.
* LAST for AR-only adjuncts (2021) is the start year of the last fiscal year listed.
* Some 2024-2026 department-filtered captures and the Wayback copy of the 2016-17 annual-report page failed to download (DNS outage); no effect on membership found.
* IRINS not collected (forbidden); Google Scholar/Scopus/DBLP only from institute profile pages.
