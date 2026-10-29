# IIIT Bhubaneswar (iiit_bhubaneswar) faculty roster 2016-2026: lab notes

Operator: Arihant Tripathy (IIIT team). Built 2026-10-29. Output: `rosters/iiit_bhubaneswar_faculty.csv` (87 rows).
Work files: `C:/Users/Arihant/rm_work/iiit_bhubaneswar_roster/{data,code}`. All fetches went through `agents/polite_get.py`.

## Institute, campus
International Institute of Information Technology Bhubaneswar (IIIT-Bh, state university of Odisha, est. 2006). Domain **iiit-bh.ac.in** (not iiitbh.ac.in).
One campus throughout: Gothapatna, PO Malipada, Bhubaneswar 751003 (address printed on every profile page and in the 2016 brochure and the Wayback footers 2016-2026).
No transit or second campus found; no mentor institute (state institute). Look-alikes (IIT Bhubaneswar, IIIT Bhagalpur, KIIT, SOA, CET) were not used; the IIIT-Bhagalpur-style domain was never touched.
Departments today: Computer Science and Engineering (CSE), Electronics and Telecommunication Engineering (ETC), Electrical and Electronics Engineering (EEE), Mechanical Engineering (ME), Basic Science and Humanities (BSH). No "Management" department page exists even though the faculty-category filter lists the word.
Renames/mappings: "Basic Sciences" + "Humanities" (separate pages 2019-2023, 2016 brochure grouped Mechanical under "Basic Sciences and Humanities") = BSH today; "Electronics and Telecom Engineering"/"Electronics Engineering"/"ETC" = ETC; "Electrical Engineering" = EEE; the 2016-2024 combined "CSE and IT" = CSE. The department column always carries the current name.

## Sources and URL patterns
1. Current site (WordPress, redesigned 2024): `https://www.iiit-bh.ac.in/category/faculty/` (49 people, one page, no pagination) and the WP REST endpoint the site itself exposes `https://www.iiit-bh.ac.in/wp-json/wp/v2/faculty?per_page=100` (49 records; category ids 6=faculty, 7=CSE, 8=ETC, 9=EEE, 10=BSH, 11=ME; used for departments). Each person has `/faculty/<slug>/` (fetched all 49: designation, email, profile links). Dept pages `/department/department-of-*/` give the same 49 (17+13+7+2+10). Director page `/administration/director/` (Ashish Ghosh), deans page, registrar page (Sabyasachi Hota OAS(S), administrative, excluded).
2. NIRF faculty tables (primary dated source). Institute NIRF page `https://www.iiit-bh.ac.in/nirfs/`: PDFs `.../2026/NIRF/Faculty-NIRF-2026.pdf` (44 rows with DOJ, currently-working flag, DOL; header "Faculty-MoE", data AY 2024-25), `.../2025/NIRF/Faculty-NIRF-2025.pdf` (52 rows, header "India Rankings 2024", AY 2023-24, no DOJ), and Google-Drive copies for the 2024 file (47 rows, AY 2022-23, drive id 1uzWNDw-qtEedE4qixS7dVxRbXj_PP_MY) and 2023 file (38 rows, AY 2021-22, drive id 172C_mOlrndrv4KmN1ivAoc6sD0fP-Kbl), downloaded via `drive.google.com/uc?export=download&id=...` (redirects to drive.usercontent.google.com, plain file, no challenge). The institute's labels of the files (2023/2024/2025/2026) do not match the headers (2025 file is headed India Rankings 2024); I follow the printed headers and academic years. NIRF 2020-2022 sections of the page are empty ("No posts found"), so AY 2019-20 and 2020-21 have no faculty table.
3. Wayback (CDX `url=iiit-bh.ac.in/...` prefix queries for `/faculty*`, `/home/faculty*`, `/university/*`, `/departments*`, `/department/*`, plus a domain-wide key list). Snapshots used (raw `id_`): `/home/faculty/all` 2019-08-23, 2019-12-15, 2020-07-29, 2020-10-23, 2021-04-20, 2021-08-03; `/university/faculty` 2021-09-18, 2022-07-01, 2023-03-29, 2024-01-06, 2024-06-12, 2024-12-22; `/departments/faculty-{cse,ee,etc,mechanical,humanities,basic-science}` 2023-02-07 and `faculty-*` 2024-11-04; `/home/faculty/by-department` 2019-08-23. Old Google-Sites site (2016-2018, `/faculty`, `/faculty/faculty-list`) archives only an empty gadget ("The gadget spec URL could not be found"), so it carries no names.
4. 2016 faculty brochure `http://placement.iiit-bh.ac.in/info/fp.pdf` ("Profile Faculty 2016", PDF created 28 Mar 2016; Wayback 20170329132509): 40 named faculty with departments. 2014 brochure (`IIIT_BH_Faculty_Profile_2015_Batch.pdf`, "Faculty Profile 2014") used only for tenure text (Ajit Das "associated since its inception in 2006"; Debasish Jena "joined 2010") and to confirm nobody extra existed in 2016. Placement page `placement.iiit-bh.ac.in/faculties.html` (Jan 2016) lists Harish Kumar Sahoo, Muktikanta Sahoo (= Muktikanta Sahu), Suvendu Rup, Tapas Kumar Panigrahi, Umamani Subudhi, "Prasant Ray" (taken as Prakash Kumar Ray, the only Ray in the 2016 brochure; no separate row).
5. ORCID public API (identifiers only, see below).
Tried and unusable: Hibiscus time-table PDFs of 2017 (OCR-garbled scans), NIRF national portal (counts only), Dropbox `fac.pdf` (404 in archive).

## How former faculty and years were established
* Presence evidence = (a) 2016 brochure (year 2016), (b) Wayback snapshots 2019-2024, (c) NIRF tables (AY end year: AY 2021-22 -> 2022 etc.; NIRF 2026 uses DOL year when present, else 2025), (d) the live site (2026). FIRST = joining_year if documented, else first evidence year; LAST = last evidence year.
* **Stale pages:** the 2019-08 to 2021-08 lists are identical in length (44) yet drop Ajit Das, G.K. Nayak, Ajith K.K. by 2021-09, so they were maintained up to 2021-09. The 2022-07, 2023-02 and 2023-03 snapshots still list Suraj Sharma, Suvendu Rup, Bijayananda Patnaik, Srinivasarao Chintagunta, Tanutrushna Panigrahi but omit every 2022 joiner (Arun K. Sahoo Feb 2022, Deepak Rout and Shikha Vats Nov 2022) and these people are absent from NIRF AY 2021-22 onward, so those snapshots count only for people also in a NIRF table; LAST for the five is therefore **2021** (could be 2022: their ORCID employment lists end 2022 for Suraj Sharma and Srinivasarao, self-declared so not used). Janendra Routray, Sanjaya K. Parhi, Ajith K.K., Ajit Das, G.K. Nayak: last listed 2021.
* **2016-2019 archive gap:** no names exist for 2017-2018 and early 2019. People first listed in 2019-08 may have joined 2016-2019 (FIRST = 2019 is first evidence, not joining), and anyone who joined after Mar 2016 and left before Aug 2019 is **missing**. Five people seen only in 2016 (Prakash Kumar Ray, Sivkumar Mishra, Tapas Kumar Panigrahi, Harish Kumar Sahoo, Sachidananda Sahoo) have LAST = 2016 by evidence; their real last year is unknown (ORCID self-declared employment ends: Panigrahi 2018, S. Mishra 2018).
* Joining years: NIRF 2026 DOJ column (49 rows incl. visiting/contract), documented earlier dates where the 2025 file prints a start date (Bibhuti B. Mishra 2022, Sarthak Padhi 2022, Lopamudra Prusty 2022, Nilambar Tripathy 2022, Satakshi Ghosh 2023, Arpit S. Mohapatra 2022 over NIRF-2026 2024), Ajit Das 2006 and Rupaj K. Nayak 2009 (own profile text "2009-2012 and 2013-till date"). NIRF DOJ can be a regularisation or re-joining date (e.g. contract staff re-dated 08-04-2024), so for some regular faculty the true joining year may be earlier. Blank where no dated source exists (all former people seen only in snapshots, 12 new 2025-26 joiners without NIRF rows).
* People in the 2014 brochure but not in the 2016 brochure (Soumen Bag, Asutosh Kar, Mukesh Tiwari and similar) are pre-window and excluded.

## Counts (rows = 87)
| Department | current | visiting | adjunct | former |
|---|---|---|---|---|
| Computer Science and Engineering | 16 | 0 | 0 | 12 |
| Electronics and Telecommunication Eng. | 9 | 4 | 0 | 6 |
| Electrical and Electronics Eng. | 7 | 0 | 0 | 4 |
| Mechanical Engineering | 2 | 0 | 0 | 0 |
| Basic Science and Humanities | 8 | 2 | 0 | 9 |
| department blank | 1 (Director Ashish Ghosh) | 0 | 1 (Sankar Pal) | 6 (NIRF-only) |
| total | 43 | 6 | 1 | 37 |

Per-source check of extraction counts: category page 49 = dept pages 17+13+7+2+10; NIRF parse 38/47/52/44 rows = rows printed by the PDFs; snapshot parser 44-46 names per `/home/faculty/all` page.

## Independent size check
NIRF 2026 faculty table (AY 2024-25): 44 rows, 39 flagged "currently working" (36 regular/contract + 3 visiting; incl. the Director). Live site Oct 2026: 49 faculty pages (42 regular/contract, 6 visiting, 1 distinguished visitor) + Director = 50 rows. Of the 50 non-former rows, 38 are NIRF-2026-confirmed currently-working. The 12 not in NIRF 2026 are 2025-26 joiners or adjunct (Abhinav Chakraborty, Meenu Rani Dey, Paramita Koley, Sangita Dhara, Utkalika Satapathy, Satyajit Panigrahy, Basabadatta Mohanty, Bibekananda Panda, Sourav Kundu, Dasari Arun Kumar, Gobinda Prasad Samanta, Sankar Pal); their profile pages are dated 2025-09 to 2026-08. The one NIRF-YES person missing from the site is Rupaj Kumar Nayak (see below). The difference 50 vs 39 is explained by 11 new people minus 5 who left (DOL set in NIRF 2026: Satakshi Ghosh, Hemanta Pati, Sanjay Saxena, Santisudha Panigrahi, Sumanta Nanda) and rounding of the NIRF snapshot date (mid-2025).

## Decisions on ambiguous people
* Rupaj Kumar Nayak: NIRF 2026 "currently working", listed in 2024-12 snapshot, but absent from the 2026 institute-wide faculty list; tie-break rule (institute list wins) -> `former`, LAST 2025. Could be a site omission; re-check.
* Ashish Ghosh (Director since 2023-10-16 per NIRF 2026 DOJ, director page): not in the faculty category; included as `current` Director, department blank (no unit printed).
* Sankar Pal: "ANRF Prime Minister Professor (Distinguished Scientist and Former Director, ISI)" -> `adjunct`, department blank, no joining year (page date 2026-02 is not evidence).
* Visiting (page says Visiting): Sambit Mohapatra, Dasari Arun Kumar, Gobinda Prasad Samanta, Sourav Kundu, Smaranika Swain, Deepak Kumar Rout -> `visiting` (still listed, no range).
* Name variants merged: Hemant/Hemanta Pati; Sobhnayak/Sobhanayak/Shobhanayak; Usharani Rout/Raut; Sanjaya/Sanjay Saxena; Debasish/Debashish Jena (site prints Debashish); Bamdev/Bamadev; Siksha Vat/Shikha Vats; Jayanta Kumar Sahu (NIRF) = Jayanta Kumar Sahoo (site 2024) assumed; Biswaranjan Pattanayak/Pattnaik; Tapan Kumar sahoo; Biranchi Narayan(a) Padhi; Muktikanta Sahoo = Sahu; Prasant Ray = Prakash Kumar Ray (assumed).
* Second units: Lipika Das (Humanities until 2024, now BSH); Biranchi Padhi and Bamadev Sahoo sat under BSH in the 2016 brochure but are ME; Jolly Dey (Humanities, BSH). No person appears in two current units.
* NIRF-only people (department blank, no profile): Gayatri Pattnaik, Nilambar Tripathy, Soubhagya Ranjan Mallick, Pranita Jena, Santisudha Panigrahi; Laxmidhar Biswal (2024-01 snapshot, no department printed).
* Contract/adhoc staff listed in NIRF or on the institute list are kept as faculty with designation "Assistant Professor" (the site does not mark contract status except via NIRF type).
* Excluded: Registrar (Sabyasachi Hota), staff, project fellows, research scholars.

## Identifiers
* ORCID: one affiliation search (`expanded-search`, `affiliation-org-name:"International Institute of Information Technology Bhubaneswar"` = 74 profiles) plus one variant-spelling query (IIIT Bhubaneswar / IIIT-Bhubaneswar / IIIT Bh / comma form = 113 profiles, union 113). Name-matched candidates were checked with `/employments` (21 calls): accepted only if employment at IIIT Bhubaneswar shown (2 rejected for empty employment records: Sarthak Padhi 0000-0001-6615-3817, Utkalika Satapathy 0000-0002-7477-1479). No 429 received; no per-person name searches; "ORCID lookup pending": none.
* Counts of 39 ORCIDs in CSV: 30 from institute profile pages (10 of them also confirmed by the API route, no conflicts), 9 from the ORCID API route only (employment at IIIT Bhubaneswar verified): Alok Ranjan Nayak, Rupaj Kumar Nayak, Sivkumar Mishra, Srinivasarao Chintagunta, Sumanta Kumar Nanda, Suraj Sharma, Tapan Kumar Sahoo, Tapas Kumar Panigrahi, Ajith K.K. One page link (Sanjeev K. Mishra) had a %20 inside the iD and was normalised; `orcid.org/my-orcid?orcid=` links normalised to the bare iD.
* Google Scholar 42 (profile pages, normalised to `citations?user=ID`); homepage 38 (own sites, not "#" placeholders); Scopus id 1 (Dasari Arun Kumar, from his profile); email 71 (profile pages, or the 2019-2021 faculty list for former people); dblp/irins empty by design. Link placeholders "#" on profile pages ignored.
* joining_year filled for 49 of 87 rows.

## Known gaps
1. 2016-03 to 2019-08 roster is unobservable (Google-Sites gadget not archived): short-tenure faculty of 2016-2019 are missing; FIRST years for people first seen 2019 are first-seen years.
2. No NIRF/faculty table for AY 2019-20 and 2020-21; LAST for the 2021 leavers may be off by one.
3. Former people have no joining year in most cases.
4. NIRF DOJ dates may be regularisation dates.
5. Contract staff (about 12) are known only through NIRF tables and may have a different department or exact tenure.
6. Only one department page per unit 2023-02/2024-11 and four `/university/faculty` snapshots between 2022 and 2024 were fetched; a short-lived contract person between them could be missed.
