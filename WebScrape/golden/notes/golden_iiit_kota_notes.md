# Golden set notebook: IIIT Kota (iiit_kota), 2016-2026

Result: 74 papers (target 100 not reached; see "Why short"). Output: golden/golden_iiit_kota.csv. Operator: Arihant Tripathy.

## Sources and searches
* Institute JSON API behind the React site (webapi.iiitkota.ac.in/api/out/faculty/<id>): 27 faculty profile JSONs fetched (journals / conferences / bookchapters lists, tenure lines). Visited 27, 19 with a tenure basis, 9 yielded rows (plus 3 guest-faculty rows via Springer-verified DOIs). Roster faculty list reused from the roster agent (iiit_kota_roster/data/faculty.json, rosters csv).
* Annual Report 2022-23 (cdn.iiitkota.ac.in/pdf files/Annual Report 2022-23.pdf): has a publication list (10 journals, conferences, chapters). 10 rows. Guessed URLs for other years (2018-19 .. 2024-25) returned only the SPA shell (4.6 KB), so no other annual reports; the roster agent's 2016-17 PDF was corrupt.
* Springer landing pages reached through DOIs printed on faculty pages (24 DOIs fetched via doi.org; Springer meta tags give author affiliation): 14 confirmed IIIT Kota affiliation, giving the `high` rows. Springer pages for Lalji Kumar, Pooja Sharma, Veena Khandelwal papers did NOT show IIIT Kota (pre-joining work), and one Ajay Kumar 2024 paper did not either: all excluded. Three DOIs had no fetched page (blocked/no file).
* Web search (general engine) strings: "Indian Institute of Information Technology Kota" arxiv paper (arxiv.org only); "IIIT Kota" department of computer science paper 2017-2019; Basant Agarwal "Indian Institute of Information Technology Kota" arxiv sentiment; arxiv "IIIT Kota" Rajasthan "iiitkota.ac.in"; arxiv.org "Indian Institute of Information Technology, Kota" + Basant Agarwal/Harjule/Anupam Kumar/Gyan Singh Yadav/Isha Pathak; IIIT Kota faculty research paper news; Smita Naval / Solanki / Tapan Jain / Pooja Jain IIIT Kota 2016-17. Yield: 3 arXiv preprints (abs/PDF read, affiliation printed), 3 Springer pages.
* Institute news/achievements/announcements/events API endpoints: student/competition news only, no publications. No external news coverage found, so the news share is 0 (moved to faculty pages).
* Department pages (computer-science-eng, electronics-communication-eng) only carry faculty cards; the publication lists are the same profile JSON, so counted under faculty_page.
* Not used (forbidden): Scholar, Scopus, IRINS, Crossref etc. arXiv: fetches only of three PDFs (no 403).

## Counts
faculty_page 58, annual_report 10, websearch 3 (Springer pages), arxiv 3. Confidence: high 19, medium 55. DOI present for 25 (34%), only where printed on the source or Springer page. Years: 2017:1, 2019:1, 2020:9, 2021:4, 2022:21, 2023:9, 2024:4, 2025:19, 2026:6.
Departments: ECE 40, CSE 27, HMAS 5, Mathematics (HMAS) 2. (AIDE department: no eligible paper.)

## Why short (74 of 100) and gaps
* Tenure rule: most regular faculty joined May-June 2019 (the institute moved to its own staff then); papers of 2019 and earlier are excluded unless affiliation visible. 2016-2018 and 2019 are nearly empty: faculty before 2019 (Pooja Jain, Tapan Jain, Smita Naval, R. K. Solanki, B. Agarwal 2019-20 etc.) have no page publication lists and no allowed external source was found. Years 2016 and 2018 have zero rows.
* Guest faculty (joined 2023-2025, 15+ people) list mostly pre-joining work; they contribute only when a publisher page shows IIIT Kota.
* Faculty with no joining year (Rajendra Kachhava, Shekhar P. Singh, Aditi Gaur, Chitra Pachouri, Adarsh Kumar, Anil Sharma): excluded, no on-page IIIT Kota evidence. Pintu Kumar, Abhay Upadhyay, Ritam Sharma, Veena Khandelwal, Ankita Birla, Prashant Goyal, Lalji Kumar, Pooja Sharma: no paper after their joining year.
* Per-person cap of 8 reached for Amit Kumar, Garg, Chetna, Isha, Parikshit; others had fewer eligible.
## Rejected candidates
Ritu Raj papers in the annual report (Fuzzy Information and Engineering 2023, TS fuzzy controller 2022): no tenure information. Priyanka Mishra patent (not a paper). Vinita Tiwari "Impact of laser beam welding ... P22 steel" (probable homonym) and "9 Combining News" (incomplete title). Kapil Choudhary 2023-24 BITS workshop entry (not a paper). Vinita's 2017 start is the roster value; her own page says BITS Pilani until Dec 2017, so rows are 2019+ only. Duplicate listings (Nehra/Yadav CVMI 2024) merged.
## Biases
Heavily faculty-page based and recent (2022 and 2025 dominate); medium rows depend on profile pages possibly listing co-authored work not done at IIIT Kota; titles come from free-text lists, a few venue strings are as printed (some abbreviated). Years of accepted-only items follow the page. ECE over-represented. Mentor-institute (MNIT Jaipur) faculty not included. Springer-verified rows over-represent Springer venues.
