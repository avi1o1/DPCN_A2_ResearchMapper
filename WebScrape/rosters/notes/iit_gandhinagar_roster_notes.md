# IIT Gandhinagar (iit_gandhinagar) faculty roster - lab notes

Run was resumed after an interruption (usage limit, then a network error). Inherited from the first run: the parsed current faculty list
(`current.json`, from the institute's `https://iitgn.ac.in/faculty/all` page, Wayback capture 2026-03-23), the NIRF 2025 PDF, the CDX dumps and the
parser `parse_cur.py`. Everything else (archived snapshot pass, merge, CSV) was done in the second run.

## Sources and endpoints
* Current list: `https://iitgn.ac.in/faculty/all` (card layout; live host returns 403 to the fetcher, so the Wayback copy of 2026-03-23 was used). 276 cards = 248 unique names (people appear on every unit page that lists them; cross-listed people collapsed to one row, primary unit = text before "(Jointly with ...)" in the card).
* Old faculty list (2016-2019): `http://www.iitgn.ac.in/faculty.htm` (single page with one section per discipline). Snapshots (Wayback `.../web/<ts>id_/...`): 2016-06-12, 2016-11-04, 2017-06-05, 2017-12-06, 2018-05-03, 2018-11-28, 2019-05-26, 2019-12-12 (CDX `url=iitgn.ac.in/faculty.htm&collapse=timestamp:6`, 35 monthly captures 2016-2019).
* 2020-2023: `https://iitgn.ac.in/faculty` (card layout): 2020-06-12, 2020-11-28, 2021-06-09, 2021-12-05, 2022-06-15, 2022-12-03, 2023-06-01, 2023-12-03.
* From mid-2024 `/faculty` became a JavaScript department selector (no names), so the per-unit pages `https://iitgn.ac.in/faculty/<slug>` (slugs bioe, chemical, chemistry, civil, cl, cogs, cse, design, earths, ee, hss, maths, me, mse, phy, guestprof, dhp) were used: last capture of 2024 and of 2025 per slug (33 of 34 fetched at first; the 2025 phy page was refetched; 2025 guestprof/dhp/etc. as available). These form two composite snapshots (dates 2024-12-12 and 2025-11-18 = latest capture used).
* `https://iitgn.ac.in/faculty/former` (capture 2024-08-13): undated "Former Faculty Members" honour roll (visiting professors, scholars-in-residence). Used only as a cross-check: names are included only if a dated snapshot also places them at IITGN in 2016-2026.
* NIRF 2025 data submission (PDF fetched earlier, `nirf/2025.pdf`, 4 pages): reports "Number of faculty members entered: 171"; it contains the count only, no per-person names or joining/leaving dates, so it was used for the size check only. No other NIRF years were retrieved (not in cache).
* Annual reports 2018-19 .. 2021-22 (cached from the golden run) were grepped for faculty joined/left lists: they contain none, so not used.
* ORCID: offline affiliation index only (`orcid_index/iit_gandhinagar_orcid_index.tsv`). No live ORCID API calls were made.

## Method
Each snapshot was parsed into (name, designation, unit). Non-faculty (postdocs, fellows, trainees, Inspire fellows, project staff) were dropped; classes: regular (professor ranks, teaching/research professor, lecturer, chairs, director), visiting (visiting, guest, scholar-in-residence), adjunct (honorary, distinguished honorary, adjunct, professor of practice). Names were merged across snapshots by surname + first-name similarity (variants such as "Dhiraj D Bhatia"/"Dhiraj Bhatia"); manual merges: K. Chelvakumar = Kasivisvanthan Chelvakumar, S. Chandrasekaran = Srinivasan Chandrasekaran (guest + Maritime Engg), R. N. Singh = Rishi Narain Singh, K.R. Jayaprakash = Jayaprakash K R, Sriram Kanvah Gundimeda = Venkata Sriram Kanvah Gundimeda.
* current: regular faculty on the 2026-03 institute-wide list. Guests / honorary / practice professors still listed keep status visiting / adjunct.
* former / visiting / adjunct no longer listed: range (FIRST-LAST) = year of first and last snapshot in which the person appears. FIRST is the first evidence year (2016 for anybody already on the June-2016 page, so the true joining year may be earlier); LAST is the year of the last snapshot listing them, so the true leaving year can be up to ~6-12 months later or (stale pages) earlier. Pages were maintained (newer joiners appear steadily, counts grow 183 -> 304 in 2016-2019 old-format pages including guests/postdocs), so snapshot presence was accepted as evidence.
* joining_year: filled only for regular faculty whose first appearance is after the first snapshot (2016-11-04 or later) AND who were absent from the preceding snapshot: it is the year of that first archived appearance (an upper bound; the real joining can be up to ~6 months earlier, e.g. a December joiner shows up the following June). People already on the 2016-06 page: blank. Individuals who first appear in the 2026-03 list get 2026 (not evidence of a 2026 joining within the year, only first appearance). No profile/CV/NIRF dates were available.
* Second units (cross-listed, not separate rows): e.g. Bhaskar Datta (Chemistry + BSE), Pratik Mutha (CBS + BSE), Rohil Jain (BSE + ME), Sameer Patel (Civil + Chemical), Harkirat Singh (ME + Civil), Udit Bhatia (Civil + CSE + Earth Sci), Vimal Mishra (Civil + Earth Sci), Jaison Manjaly / Jooyoung Kim (HSS + CBS), Shanmuganathan Raman, Sameer Kulkarni, Joycee Mekie (EE/CSE), Gopinadhan Kalon (Physics + Materials), Alok Kanungo, C N Pandey, Sharada C.V., V.N. Prabhakar (Earth Sci + HSS/Archaeology), Sameer Sahasrabudhe (Design/HSS/ME), Kasivisvanthan Chelvakumar (ME + HSS).

## Counts (404 rows)
current 165 (regular faculty) | former 53 | visiting 163 | adjunct 23. Per unit (current/former/visiting/adjunct):
BSE 10/1/5/0; Chemical 12/2/3/0; Chemistry 15/3/0/0; Civil 12/6/17/2; CBS 6/0/0/0; CSE 14/3/5/2; Design 1/0/2/2; Earth Sci 8/4/8/2; EE 17/4/9/3; HSS 14/11/38/1; Materials 11/4/4/0; Maths 14/4/9/1; ME 15/3/17/1; Physics 14/8/5/0; Center for Creative Learning 1; Maritime Engineering 1 (current, Srinivasan Chandrasekaran); Archaeological Sciences 3 visiting; Library Science 1 visiting; no unit given (guest/honorary professors with no unit listed) 46.
Older units renamed: Biological Engineering -> Biological Sciences and Engineering; Humanities / Social Sciences -> Humanities and Social Sciences; Cognitive Science -> Cognitive and Brain Sciences; Materials Science and Engineering -> Materials Engineering; Creative Learning -> Center for Creative Learning.
Extraction counts per snapshot (rows incl. guests/visitors/postdocs before filtering): 183, 174, 192, 221, 226, 254, 280, 304 (2016-2019); 173, 176, 182, 190, 196, 212, 211, 208 (2020-2023); 249, 272 (2024, 2025 composite); 276 (2026). The step 2019 -> 2020 reflects the layout change (postdocs/scholars no longer listed).

## Size check
NIRF 2025 reports 171 faculty. This roster has 165 `current` rows (regular faculty; includes NIRF-style regular ranks incl. teaching/research professors and chairs). Difference 6: NIRF counts include people appointed after/around the submission and possibly Professors of Practice (which I put under `adjunct`: 23 adjunct rows incl. honorary professors) and the NIRF date is earlier than 2026-03. NIRF-confirmed current rows: not determinable (NIRF PDF has no names).

## Identifiers
ORCID: 136 rows, all from route "ORCID affiliation record" (offline index; employment/invited-position rows naming IIT Gandhinagar, same surname and compatible first name, excluding student/postdoc-only roles). 0 from institute pages, 0 from live API. One person with two qualifying iDs left blank: Manish Kumar (0000-0002-3351-7298, 0000-0003-3518-4391). ORCID lookup pending: live API not used for people left over. Email, Google Scholar, DBLP, Scopus, IRINS, homepage left blank (profile pages not fetched; live host blocks the fetcher). profile_url only for current rows (`https://iitgn.ac.in/faculty/<slug>/<id>`).
Index matches for visiting/adjunct people sometimes carry employment dates that differ from the snapshot range; they are accepted on name+affiliation only.

## Problems / ambiguities
* Live iitgn.ac.in returns 403; everything is from Wayback.
* Some Wayback fetches initially failed (DNS/connection errors); retried with refresh. One composite page (2025 physics) was refetched separately.
* 2024/2025 composites are made of per-unit captures taken on different days, so a person who left between those days may show LAST 2024 or 2025 inconsistently.
* People last listed in 2025 and absent from the 2026-03 list (Gaurav, Ravi Hegde, Aditya Nema, Anil Devara, Sumit Tambe, Nishaant Choksi): treated as former with LAST=2025; they may have left in 2026 or been mis-dropped from the 2026 page.
* Sudhir K. Jain (Director): LAST 2021 from snapshots; true end of directorship likely 2022 (no snapshot after 2021-12 lists him).
* Rosa Maria Perez (no designation on page) and postdocs / French trainee teachers / Inspire fellows excluded as non-faculty.
* Name-variant merges are heuristic (see Method); two people with identical surname and similar first names could be merged wrongly.
* Visiting/Guest rows without unit have blank department.

## Known gaps
* Former faculty from gaps between the semi-annual snapshots (joined and left within ~6 months) are missed. Former faculty before 2016 not included.
* joining_year mostly blank for those already present in 2016; no CVs/NIRF dates.
* NIRF years other than 2025 not used; no profile-page identifiers.
* Honour-roll visitors listed only on `/faculty/former` with no dated snapshot were excluded.
