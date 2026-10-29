# IIIT Guwahati faculty roster: lab notes

Operator: Arihant Tripathy (IIIT team). Built 2026-10-29. Output: `rosters/iiit_guwahati_faculty.csv` (101 rows).
Working files: `C:\Users\Arihant\rm_work\iiit_guwahati_roster\data\` (pages, CDX lists, parsed JSON); parsers in `...\code\`.
All fetches went through `agents/polite_get.py`.

## Result in numbers

| status | rows |
|---|---|
| current | 50 (49 regular faculty + the Director) |
| emeritus | 1 |
| adjunct | 2 |
| visiting (guest faculty) | 11 (10 listed now, 1 former) |
| former | 37 |
| total | 101 |

Per unit (current / former / other: emeritus+adjunct+visiting):

| unit | current | former | other |
|---|---|---|---|
| Computer Science and Engineering | 19 | 19 | 3 (Barua emeritus, Dey adjunct, Banerjee guest) |
| Electronics and Communication Engineering | 19 (incl. Director S. K. Patra) | 10 | 0 |
| Science and Mathematics | 4 | 8 | 10 (guest faculty; 1 of them former) |
| Humanities and Social Sciences | 8 | 0 | 1 (Nath adjunct) |

Extraction counts per unit against NIRF 2025 (Feb 2025): the four department pages gave 62 listed people (22 CSE, 18 ECE, 13 S&M, 9 HSS),
of which 49 are regular faculty (Professor / Associate / Assistant). NIRF 2025 lists 51 regular faculty plus 8 "Other" (guests) = 59.
All 49 current regular faculty appear in NIRF; the two NIRF regulars not on the site now (Masihuddin, Srinibas Swain) left after Feb 2025.
8 of the 10 guest faculty listed on the website now are in NIRF 2025 (Debarati Mitra, a NIRF guest, was dropped from the site in 2025-26).
Current rows NIRF-confirmed: 49 of 50 (the Director is not in NIRF faculty tables).

## Independent size check

NIRF 2025 data submission (Engineering and Overall, uploaded 2025-02-14, https://www.iiitg.ac.in/uploads/2025/02/14/5293ea128861a29e27e43cbaa421d871.pdf):
59 faculty rows, all "currently working": 51 regular + 8 "Other". Website on 2026-10-29: 49 regular faculty (+ Director, + 1 emeritus,
2 adjunct, 10 guest). 51 - 2 departures (Masihuddin, Srinibas Swain) = 49, so the counts reconcile exactly. Later-joined regulars
since Feb 2025: none seen. The Director (Prof. Sarat Kumar Patra) is not in the faculty table.
NIRF 2020, 2021, 2022 PDFs (Wayback copies of nirfindia.org; the live site returns 403 to the fetcher and was not bypassed)
carry no faculty names (only PhD-student tables), so they were not used. NIRF 2023 and 2024 PDFs were not found in the Wayback CDX.

## Institute facts (campuses, mentor)

* Institute: Indian Institute of Information Technology Guwahati (PPP IIIT), site https://www.iiitg.ac.in (domain iiitg.ac.in). Look-alikes (IIT Guwahati, Gauhati University, IIM Guwahati, NIT Silchar) were not used.
* Campuses: transit campus 2013-2018 (Ambari, Guwahati): archived page footers of 2016 to mid-2018 give "IIIT Guwahati, G.N.B Road - 781001"; permanent campus Bongora, Guwahati 781015: footers from 2018-09 (first snapshot checked 20180901) and the current footer ("Bongora, Assam, Guwahati - 781015"). The footer shows no mention of "Assam Textile Institute"; that name from the brief was not seen in any fetched page, only the road address and PIN. Faculty are one pool; no separate campus unit exists.
* Mentor institute: IIT Guwahati acted as mentor (Prof. Gautam Barua listed "on secondment from IIT Guwahati" on the Jan 2016 faculty page; IIT Guwahati's Director sits on the Board). No page lists mentor faculty who only taught, so no `visiting` mentor rows were created. Barua held the Director post at IIIT Guwahati (administration page up to 2023-06), so he is regular (emeritus now).
* Unit renames: old site units "Mathematics" (faculty_math.php) and "Humanities" (faculty_hs.php; sub-areas English/Economics/HSS) became "Science and Mathematics" and "Humanities and Social Sciences" on the 2023 site. All rows use the current names. People are placed by the unit of their latest listing (old Jan 2016 page has no units: unit taken from the "(CSE)/(ECE)/(Mathematics)/(English)/(Economics)" in the designation).

## Sources and URL patterns

1. Current site: `https://www.iiitg.ac.in/faculty` (just links) -> department pages `/computer-science-and-engineering`, `/electronics-and-communication-engineering`, `/science-and-mathemetics` (sic), `/humanities-and-social-science`. Each lists name, designation, PhD, email, "Joined the Institute in YYYY" and a profile page `<unit>/<slug>`. All 62 profile pages were fetched (identifier links, mostly publication lists). No JSON endpoint is used.
2. Director: `/administration` (Prof. Sarat Kumar Patra, Professor ECE, Director) and `/from-the-directors-desk` (says he is also Director of NIT Agartala; previously IIIT Vadodara 2017-2023).
3. NIRF 2025 data PDF (above), parsed from `pdftotext -layout`; three joining dates in the table were garbled by the PDF layout and ignored.
4. Wayback CDX (`web.archive.org/cdx/search/cdx?url=...&output=json&filter=statuscode:200&collapse=timestamp:6`):
   * Old site (Material design) department pages `faculty_cse.php`, `faculty_ece.php`, `faculty_hs.php`, `faculty_math.php` (monthly captures 2016-09 to 2023-06; `.html` variants in 2016). 95 captures fetched: the last capture of each calendar quarter per page.
   * `facultyIIITG.htm` (all-in-one list): captures 20160116 and 20160907 fetched. These cover the start of the window.
   * New site department pages at 2023-10, 2024-04, 2024-10, 2025-05, 2025-12 and 2026-03/05 (nearest captures; 24 fetched) of the four URLs above.
   * `administration.php` snapshots 2016-10 to 2023-06 (5 fetched): Director/Board names only.
   * Old individual faculty homepages `iiitg.ac.in/faculty/<handle>/` (CDX listing 2017-2022): every handle maps to a person already found; none revealed an unknown faculty member.
5. ORCID public API: one expanded-search `affiliation-org-name:"Indian Institute of Information Technology Guwahati"` (257 hits, 2 pages), then `/employments` for 40 name-matched candidates. No 429. No per-person name searches.

## How former faculty and tenure years were established

* A person is "former" if listed on a faculty page between 2016-01 and now and absent from the current website. FIRST = "Joined the Institute in <month year>" printed on the page (profile or list); LAST = year of the last archived capture listing them. People first listed on 2016-01-16 and absent on 2016-09 get LAST 2016.
* Joined dates are printed on both the old and new pages, so `joining_year` mostly comes from the institute itself (90 rows from pages, 7 from NIRF). Blank for 4: Malay Ananda Dutta (no date printed), Kuntal Dey, Snehasis Banerjee, the Director.
* Quarterly sampling means a person present for less than one quarter inside the window could be missed. Cross-check: every faculty handle in the CDX of `/faculty/<handle>/` and every NIRF-2025 name was found.
* Not-first-listed rule: where the page shows an earlier documented date than the first archived listing (e.g. Sanjay Moulik, Dec 2012; Mohd Mansoor Khan 2012; Amar Nath Yadav 2012), the page date is used (FIRST < 2016 is fine for the range).
* NIRF date vs page date: lower of the two is used (stated in this file): NIRF gives the year for Debarati Mitra 2022, Nandana Bhardwaj 2020, Pragya Sharma 2022 (site says 2026: re-joined or new term), Rekha Deka 2016, Sangita Talukdar 2021, Shanta Bhar 2016 (guest rows with no page date). Anuradha Jha: NIRF row says 20-05-2015 but the table is garbled in that region, the Jan 2016 page lists a different person (J. Anuradha, PhD IIT Madras, joined 2014) and the first page listing of Anuradha Jha (PhD IIT Kanpur) is 2016-09 with "joined July 2016": 2016 used.
* Staleness check: the old pages were maintained (they list 2022 joiners such as Panthadeep Bhattacharjee on the 2023-06 capture). Quirk: people absent from the 2023-10 new-site pages but present on 2023-06 old pages (Dip Sankar Banerjee, Suchetana Chakraborty, Shyju Wilson, Soumi Chattopadhyay, Subhabrata Paul, Sanya Anees, Soumyajit Poddar, Kuntal Deka, Hemanta Kumar Mondal, Sanjeev Sharma, Subhrangsu Mandal, Panthadeep Bhattacharjee, Dipendu Maity, Shyamal Ghosh, Aparajita Dutta) got LAST 2023. Self-declared ORCID dates are not evidence, but they agree for most of these (Soumi 2018-2023, Shyamal Ghosh 2021-2023, Panthadeep 2022-2023, Sumit Mishra 2018-2024, Gautam Kalita 2014-2024) and disagree for Dip Sankar Banerjee (ORCID: ended 2020; page lists him to 2023-06). The page-based LAST (2023) is kept; treat his LAST as possibly 2020.
* Later leavers from the new-site snapshots: Aparajita Dutta (last 2023-10), Phrangboklang Lyngton Thangkhiew (2024-03), Gautam Kalita (2024-03), Sumit Mishra (2024-03), G. Aruna (2024-04), Srinibas Swain (2025-04, still in NIRF Feb 2025), Debarati Mitra (guest, 2025-11), Masihuddin (2026-05; on NIRF 2025). Exact leaving month unknown; years used are the last capture year. Masihuddin and Debarati Mitra were removed from the live site between the last capture and 2026-10-29 (the 2026 LAST is the last capture; his departure could even be in 2026-27).

## Decisions and ambiguous people

* **Director.** Prof. Sarat Kumar Patra (Professor ECE) is the current Director and is not in any faculty table: added as `current`, department ECE, joining_year blank (no evidence for the start of the directorship), source = administration page.
* **Gautam Barua** (Director until at least 2023-06, "Professor (CSE), on secondment from IIT Guwahati" 2016; "Professor Emeritus" on the current CSE page; joined 2013 per site): `emeritus`, "Professor Emeritus (formerly Director) (2013-2026)". Page text contains stray years (1995, 2016) that were ignored.
* **Guest faculty.** The institute lists "Guest Faculty" on its own faculty pages (S&M and CSE). Per the brief ("unless the institute lists them as faculty") they are included as `visiting` with designation kept. Ten are listed now (no range; Archana Kushwaha, V. S. Gayathri, Rekha Deka, Shanta Bhar, Nandana Bhardwaj, Sangita Talukdar, Pragya Sharma, Jaishree Prabha Karna, Neha Pathak, Snehasis Banerjee). Debarati Mitra (Guest Faculty in Chemistry 2022-2025) is the one that left.
* **Adjunct.** Kuntal Dey (CSE, adjunct, first seen 2021-06 capture; join year unknown) and Hiranya K. Nath (HSS; Professor, Sam Houston State University, USA; joined 2024 per page).
* **Rohit Tripathi** is listed "Assistant Professor (On lien)" on the current CSE page and as "Assistant Professor and Head of the Department" on the 2023-10 CSE page: kept `current` as the institute lists him.
* **Two Anuradhas**: J. Anuradha (Mathematics, PhD IIT Madras, joined 2014, only in the Jan 2016 list) and Anuradha Jha (Science and Mathematics, current): different people, two rows. **Two Kuntals**: Kuntal Deka (ECE, former) and Kuntal Dey (CSE adjunct): different people. Two Shounak/Shirshendu etc. are distinct. Two `Mohd Mansoor Khan` forms (Mohd. / Mohd) merged. NIRF "Mashiuddin" = site "Masihuddin" (site spelling used); NIRF "Subhabrata Nath" = "Shubha Brata Nath"; NIRF "Gayatri Subhramanium" = "V. S. Gayathri"; "Nandana Bharadwaj" = "Bhardwaj".
* Second units: none found for anyone; no person is listed in two units.
* People first/last evidenced only on the 2016-01 list: Pulak Mondal, Sam Darshi, Sandip Karmakar, J. Anuradha (all FIRST 2014-2015, LAST 2016). Suddhasil De, Gaurav Saxena, Arti Pandey, Longjam Nirman Singh were listed until later in 2016 (Sep to Dec 2016).
* Emails are filled for current rows only (former emails were not extracted from the archive).

## Identifiers by route (39 ORCIDs, 62 emails)

| item | count |
|---|---|
| ORCID printed on an institute profile page | 2 (Kaustuv Nag, Shovan Barma) |
| ORCID from the ORCID API affiliation search, accepted only if `/employments` shows IIIT Guwahati and the name matches | 37 |
| Google Scholar (links on the institute profile pages, user ID only) | 11 |
| DBLP (profile page: Sheikh Wasmir Hussain) | 1 |
| Scopus ID (profile page: Kaustuv Nag) | 1 |
| IRINS (profile page: Rakesh Biswas, `https://iiitg.irins.org/profile/141167`) | 1 |
| homepage (own Google Sites pages linked from profile) | 5 |

* Ambiguous ORCID, left blank: Sumit Mishra (CSE, former) has two IIIT Guwahati-employed ORCIDs, 0000-0001-9333-2001 (2018-2024) and 0009-0006-0764-5196 (2018-); cannot tell them apart.
* 40 `/employments` calls were made for 40 candidates; all 40 passed the IIIT Guwahati employment check (one candidate, the second Sumit Mishra, left unassigned as above). No ORCID lookups pending. ORCID names are not searched per person: people without an ORCID are simply not in the affiliation search results (typically older former faculty).
* `homepage` includes only pages linked as the person's own site from their institute profile. A link from Rajarshi Mitra's page to a project site (sites.google.com/view/fairsincoochbehar) was not treated as his homepage.

## Problems and how they were resolved

* Wayback shared slot very slow (about 7 to 20 s per page when other agents are active): sampled quarterly instead of monthly. The fetch script was restarted twice when the background shell was reaped.
* `nirfindia.org` returns 403 to the fetcher (bot protection): not bypassed; used Wayback copies of the 2020-2022 PDFs (no names).
* NIRF PDF text layout is garbled in rows 7-12 (names split from dates; the 12th numbered row has no name): used only for names, designations and unambiguous joining dates.
* Parsing issues fixed: old pages have unclosed `<a>`, "Research Interests" paragraphs sharing the name's CSS class, and the 2016-01 `facultyIIITG.htm` has a different structure than the later pages (separate parser).
* Windows/CRLF in generated URL lists produced %0D 403s once; regenerated.

## Known gaps

* Quarterly Wayback sampling: a faculty member present for only one or two months between samples would be missed (none seen in the individual-homepage CDX or NIRF).
* LAST year granularity is the last capture year; true leaving dates unknown. Dip Sankar Banerjee possibly left 2020 (see above).
* No data for 2016-01 to 2016-09 other than the two snapshots of `facultyIIITG.htm`; faculty who joined and left within 2015-2016 are covered only by the Jan 2016 list.
* No NIRF faculty tables for 2018-2024, no annual reports (the institute site's annual-report page was not fetched), no former-faculty page exists on the site.
* Directors other than Gautam Barua / Patra between 2023 and 2025 (acting or additional charge) were not established.
* Former faculty rows have no emails, ORCIDs only if the API search hit them.
* The adjunct/visiting faculty of the pre-2021 period (for example the "Adjunct Faculty" and "Guest Faculty" headings first appear on the 2021-06 and 2021-12 pages) could have been listed earlier under other headings on pages not captured.
