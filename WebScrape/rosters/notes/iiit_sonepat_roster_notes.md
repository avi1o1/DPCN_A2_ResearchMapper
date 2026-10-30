# IIIT Sonepat roster notes (2026-10-30, operator Arihant Tripathy)

## Result
22 rows: 18 current (17 faculty + Director), 4 former (Ashish Ranjan, Diwakar Tripathi, M. N. Doja, K. K. Pant). No emeritus/visiting/adjunct found.
Per unit (current): CSE 12, Mathematics 2, ECE 2, Humanities (English) 1, Director (no unit) 1. Former: CSE 2, directors 2.
The brief's pre-filled campus text was verified only partly: site header/footer (2023 snapshot) gives "IIT Delhi Techno Park, Rajiv Gandhi Education City, Rai, Sonipat, Haryana-131001"; the brief's PIN 131029 and the SBIT campus from 2022 were NOT verified from any source I read. Mentor NIT Kurukshetra (2014-18) confirmed by /api/about.

## Sources and endpoints
* Site is a React SPA (https://iiitsonepat.ac.in/); bundle assets/index-C_8IOucD.js names JSON endpoints. Used: /api/faculty (17 current), /api/past-faculty (empty list `[]`), /api/past-director (2 entries), /api/director, /api/academic-departments (3 programmes CSE, Data Science & Analytics, IT; only an HoD each), /api/annual-reports, /api/people-administration (staff, excluded), /api/senate.
* Annual reports (PDF, via /uploads/...): 2023-24 (faculty list + counts), 2024-25 (counts), 2025-26 (faculty photo list, 18 names). 2021-22 (Hindi, Devanagari lost in pdftotext) and 2022-23 (image-only PDF) unreadable without OCR (no tesseract on machine): GAP.
* Wayback: CDX for iiitsonepat.ac.in/*. Old WordPress site (2019-2022, /home/*, /academic/*) has no archived faculty page. New site /faculty snapshots 2023-10-01, 2024-02-29, 2024-06-20, 2024-07-18 (8 names), 2024-11-04, 2025-02-10, 2025-05-17 (17 names), 2025-09-10 (empty SPA shell). Also /directory, /computer-science-and-engineering, /information-technology (no names), /home/directors 2019 (Doja).
* NIRF: web search found no IIIT Sonepat NIRF faculty submission; none used. GAP.
* ORCID: expanded-search affiliation-org-name (32 hits, one page) + /employments for 12 name-matched candidates.

## Former faculty / tenure years
* Faculty page 2023-10..2024-07 lists 8: Mann, Jain, Swamy, Hashmi, Bhati, Ahmad, Tripathi, Pathak. AR 2023-24: 8 faculty at start of 2023-24 (CSE 6, Maths 1, English 1), 11 appointed during 2023-24 (CSE 8, ECE 2, Maths 1), total 19 at end. The 11 first appear on the 2024-11 snapshot (Verma, Ansari, Kumar, Ranjan, Kaushik, Saha, Bansal, Samriya, Khan, Arquam, G. Jain) plus Tripathi had left.
* Diwakar Tripathi: on 2023-10 to 2024-07 lists, absent 2024-11 and later; ORCID (self-declared) 2023-2024. Range 2023-2024.
* Ashish Ranjan: AR 2023-24 lists him; on 2024-11 and 2025-05 snapshots and in AR 2025-26 photo list; absent from live /api/faculty (17). Conflict: the live institute list wins, so former, last year 2026 (AR 2025-26; AR may reflect staff during 2025-26). Gap: exact leaving date unknown; could also be an API omission.
* M. N. Doja: Founding Director 31-07-2018 to 08-10-2024 (/api/past-director). Kept as regular post-holder, joining 2018. Department blank.
* K. K. Pant: Director In-charge 09-10-2024 to 02-03-2025; he is from IIT Roorkee (not the mentor). Kept as former post-holder; arguably deputation/adjunct. Ambiguous.
* Manisha Sharma: Director, current (/api/director created 2025-04). Joining year left blank (ORCID self-declared 2025; Pant's in-charge term ended 2025-03-02 so 2025 is an upper-bound-ish estimate).
* Pre-2023 faculty (2016-2022) NOT identified: no archived faculty lists, AR 2021-22/2022-23 unreadable. Likely some early faculty and 2016-2018 mentor-run period (NIT Kurukshetra director/faculty) missing. Biggest gap.

## joining_year (blank for all faculty except directors)
Upper bounds (first archived appearance): Mann, Jain, Swamy, Hashmi, Bhati, Ahmad, Pathak, Tripathi: 2023 (2023-10-01 snapshot; AR says already 8 at start of 2023-24, so actual join may be earlier; ORCID self-declared Mann/Swamy/Verma 2019 not used as evidence). Verma, Ansari, Kumar, Ranjan, Kaushik, Saha, Bansal, Samriya, Khan, Arquam, G. Jain: appointed in academic year 2023-24 (AR 2023-24), first listed 2024-11-04 snapshot (upper bound 2024).
Note: Verma, Ansari etc. unit mapping per /api/faculty. Second unit: Samriya listed "CSE/IT" in his bio; Mann HoD of IT; Chanchal Kumar HoD CSE; Arquam HoD Data Science & Analytics (programmes are not separate faculty lists, so CSE used).

## Identifiers by route
ORCID 9: all by ORCID API affiliation search with /employments showing IIIT Sonepat (Mann, Swamy, Verma, Bansal, Saha, Samriya, Ranjan, Tripathi, Sharma). 0 from institute pages. Rejected: Hashmi 0000-0001-7196-5780 (IIIT Sonepat only as education, not employment); Vishu Tyagi (PhD scholar); Shivam Gupta (no Sonepat employment entry; not on any faculty list). Other hits are students/staff. Remaining faculty (Jain, Bhati, Ahmad, Pathak, Ansari, Kumar, Kaushik, Khan, Arquam, G. Jain, Hashmi) not found in affiliation search: ORCID lookup pending (per-person search not done, quota). Other identifiers: none on institute pages (only LinkedIn, not collected). joining_year filled: 2 (directors).

## Size check
Current faculty rows (excl. Director) = 17; AR 2024-25 reports 18 (CSE 13, ECE 2, Maths 2, English 1); AR 2025-26 photo list 18. Difference = Ashish Ranjan (missing from live list). NIRF-confirmed current rows: 0 (no NIRF source found).

## Problems
Direct polite_get of Wayback slot was slow (shared). Faculty page 2025-09-10 snapshot is an empty SPA shell, not evidence. Designations on /faculty snapshots all say "Professor" (template), live API and ARs say Assistant Professor; used Assistant Professor. Rajiv Verma printed as "Rajeev/Rajiv". Zamir Ahmad Ansari printed "Zameer Ahmed" in AR.

## Operator correction (2026-10-30)
**K. K. Pant** (Director in charge 2024-2025) is set to `adjunct`. He held the post while employed by IIT Roorkee, so his
papers print IIT Roorkee. As adjunct he contributes only papers that print IIIT Sonepat. This is the same rule as for IIIT Kota's
MNIT post-holders (PROCESS_IIIT §7.3).
