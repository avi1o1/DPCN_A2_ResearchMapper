# IIT Delhi faculty roster: lab notebook

Output: `WebScrape/rosters/iit_delhi_faculty.csv` (738 rows). Built by a continued run (an earlier agent was lost to a usage limit; its saved fetches and parsers were reused, see "Inherited").

## Sources and endpoints used
* Institute websites (live, through the shared polite fetcher): templated Laravel-style sites `<dept>.iitd.ac.in/faculty` (am, bioschool, cart, cbme, chemistry, dese, ee, mech, sense, sire, spp, textile; exfac/retired/joint subpages where they exist), bespoke pages for chemical (`/faculties/`), cse (`homecse.iitd.ac.in/faculty/`), physics, opc, scai, JSON APIs `maths.iitd.ac.in/api/faculty` (`/api/exfaculty`, `/api/visitingfaculty` returned empty), `mse.iitd.ac.in/api/faculty_api`.
* Hosts with broken TLS (civil, design, hss, dms, beb, bhartischool, abudhabi) were read from Wayback copies (2025 snapshot, `web/2025id_/...`): civil `index.php?lmenuid=faculty`, design `dod-faculty.html`, hss `/faculty`, dms `/faculty/`, beb `faculty.html`. IIT Delhi Abu Dhabi (`iitdabudhabi.ac.ae/faculty`) is also unreachable (SSL error): NOT covered.
* NIRF overall PDFs (Wayback copies of nirfindia.org, 2021, 2022, 2023, 2025; 2024 not archived): only summary tables, no faculty names; used only for the size check.
* Wayback snapshots of department faculty pages, 2016/2018/2020/2022/2024 for cse and ee, 2017 and 2021 for physics, mech, chemical, chemistry, maths, civil, hss, dms, textile, am, mse, dese, design, bioschool, cbme (home page first, then the links containing faculty/people; second-level links where the first page had no name list). URL patterns recorded in `work/iit_delhi_roster/snap*.log`. Pages whose URL looked like an ex-faculty/emeritus/staff list were not counted as evidence of presence; trailing "former faculty" sections of a snapshot were cut off before name matching.
* Former-faculty lists on the sites: dese `Former Faculty`, civil `Former Faculty Members`/`Former HoDs`, physics `ex_faculty`, cbme `exfaculty`, bioschool `Former Faculty`, chemistry `retfac` (carries service years, e.g. 1992-2022, an explicit dated source).
* The CDX prefix-wildcard queries (`url=host/*&matchType=prefix` with regex filters) returned empty or hung in the previous run and in this one; they were abandoned. Only exact-URL snapshot fetches worked.
* ORCID: offline affiliation index (`work/orcid_index/iit_delhi_orcid_index.tsv`) only; no live API calls.

## Counts per unit (current / former / other)
| unit | current | former | other (emeritus, visiting, adjunct) |
|---|---|---|---|
| Applied Mechanics | 35 | 0 | 0 |
| Biochemical Engineering and Biotechnology | 35 | 0 | 1 |
| Centre for Automotive Research and Tribology | 8 | 0 | 0 |
| Centre for Biomedical Engineering | 16 | 3 | 2 |
| Centre for Sensors, Instrumentation and Cyber-physical Systems Engineering (SeNSE) | 8 | 0 | 3 |
| Chemical Engineering | 29 | 0 | 0 |
| Chemistry | 36 | 5 | 0 |
| Civil Engineering | 46 | 14 | 8 |
| Computer Science and Engineering | 44 | 0 | 1 |
| Design | 12 | 0 | 1 |
| Electrical Engineering | 63 | 0 | 8 |
| Energy Science and Engineering | 24 | 18 | 0 |
| Humanities and Social Sciences | 42 | 0 | 3 |
| Management Studies | 23 | 0 | 2 |
| Materials Science and Engineering | 21 | 0 | 0 |
| Mathematics | 34 | 0 | 0 |
| Mechanical Engineering | 52 | 0 | 0 |
| Optics and Photonics Centre | 12 | 0 | 2 |
| Physics | 47 | 9 | 2 |
| School of Biological Sciences | 16 | 2 | 0 |
| School of Interdisciplinary Research | 1 | 0 | 0 |
| School of Public Policy | 17 | 0 | 5 |
| Textile and Fibre Engineering | 22 | 0 | 1 |
| Yardi School of Artificial Intelligence | 5 | 0 | 0 |

Totals: 738 rows, 648 current. The institute's own NIRF data submissions report "faculty members entered": 682 (2021), 880 (2022), 745 (2023), 833 (2025). Size check: 648 current rows vs 833 (2025): the roster is about 185 short. Reasons: (a) no list for CAS (JavaScript-rendered page), CRDT, ETSC, TRIPP, CARE (404), Bharti School, SIT (their faculty are mostly joint/associated from other departments, deliberately not added), and Abu Dhabi; (b) the NIRF number includes visiting/adjunct/contract/emeritus staff counted by IIT Delhi, and several department pages (cse 44, dms 23) look shorter than the real headcount; (c) NIRF faculty tables with names and joining dates could not be obtained, so no current row is NIRF-confirmed (0).

## How former faculty and tenure years were established
* Candidates: names in the former/retired/ex-faculty sections listed above (dese 36, civil 45+HoDs, physics 78, cbme 21, bioschool 4, chemistry 5 with years).
* A candidate is kept only with dated evidence: (i) chemistry `retfac` service years, or (ii) presence in archived faculty-page snapshots (year of snapshot). FIRST = earliest snapshot year with the name, LAST = latest. Because only 2 to 5 snapshots per site were read, FIRST is a lower bound on the true joining year and LAST an approximate last year; a person last seen in 2021 may have left any time to 2024-26. Most rows have range 2017-2021, i.e. they appear in the 2017 and 2021 snapshots but not on the current page. Stale snapshots were not separately tested for maintenance.
* 136 candidates (mostly long-retired DESE/physics/civil professors) had no evidence inside 2016-2026 and were excluded under the window rule (list below).
* Not done: discovery of former faculty who appear only in old snapshots and in no current/former list (name extraction from old pages of cse, ee, mech, chemical, etc.). This is the largest gap: faculty who left between 2016 and 2024 from those departments are mostly missing.

## Identifiers
* ORCID (offline affiliation-record route): 324; ORCID by live API name search: 0; by institute pages: 0.
* IRINS profile URLs from institute pages: 46; Google Scholar: 14; homepage: 300. dblp, scopus_id: none seen.
* joining_year: 5 (only the chemistry retired-faculty service years); first-appearance years were not used as joining years.
* Name-matching of the ORCID index is by surname plus first name/initial and role (professor, faculty, head ...); ORCID iDs for people with more than one candidate were left blank. Ambiguous (blank): Deepak Kumar; Sandeep Kumar Jha; Ravi Shankar; Vipin Kumar; Arun Kumar; Rahul Kumar Singh; Rahul Singh; Deepak Jain; Leena Nebhani; N. K. Garg; P. V. Madhusudhan Rao; A K Singh.

## Problems and resolutions
* The previous parse output had junk rows (designation words parsed as names, 'Publications'); removed, chair titles stripped from names, ALL-CAPS surnames title-cased, reversed 'Last, First' (civil) swapped.
* Joint/associated/INSPIRE entries (SPP associated 10, SeNSE joint 2, EE/Textile joint pages, etc.) were not made rows of the listing unit (rule: associated faculty never create membership).
* Wayback failures were cached by the fetcher (`DEAD:ConnectionError`); the same URL had to be retried with https and a different timestamp.
* Duplicates across units merged by surname plus first-name compatibility; primary unit = the parent department over centres. People in two units (second unit not stored): Aditya Mittal (Biochemical Engine / School of Biologic / Centre for Biomedi); Bishwajit Kundu (Biochemical Engine / School of Biologic); James Gomes (Biochemical Engine / School of Biologic); Tapan Kumar Chaudhuri (Biochemical Engine / School of Biologic); B. Jayaram (Chemistry / School of Biologic); Seyed E. Hasnain (Biochemical Engine / School of Biologic); Deepak Kumar (Physics / Centre for Automot); B. K. Panigrahi (Electrical Enginee / Centre for Automot); Dibyajyoti Ghosh (Chemistry / Materials Science ); Ravi P Singh (Chemistry / Civil Engineering); Ravi Shankar (Chemistry / Management Studies); Sharad Kumar Gupta (Biochemical Engine / Chemical Engineeri); Amit Kumar Jain (Electrical Enginee / Civil Engineering); Amita Das (Physics / Biochemical Engine); Sujeet Kumar Sinha (Mechanical Enginee / Civil Engineering); M. S. Sodha (Department of Ener / Physics); Sumeet Agarwal (Electrical Enginee / Yardi School of Ar); Arun Kumar (Civil Engineering / Physics); Anurag Sharma (Optics and Photoni / Physics); Bhaskar Kanseri (Physics / Optics and Photoni); Chetan Arora (Computer Science a / Yardi School of Ar); Parvendra Kumar (Optics and Photoni / Civil Engineering); Ajoy K. Ghatak (Optics and Photoni / Physics); Ramakrishna Ramaswamy (Chemistry / Physics).
* The check warns about two repeated names (Madhusudhan P Rao V, B Premachandran, different spellings of one person each in two units) and three shared e-mails; left as is, to be reviewed.
* Renames: dese listed as Energy Science and Engineering (site calls itself Department of Energy Science and Engineering); `Design` kept as the site names it.

## Known gaps
CAS, CRDT, ETSC, TRIPP, CARE, Bharti, SIT, Abu Dhabi, Sonipat/Jhajjar not covered; former-faculty discovery for most departments not done; ORCID lookup pending for everybody without an affiliation record (live API unused); joining years almost entirely blank; no NIRF-confirmed rows.

## Excluded former candidates (no evidence in 2016-2026)
Amarjeet Singh (Civil Engineer); Vikram Kumar (Physics); Saroj Mishra (Biochemical En); K. L. Chopra (Department of ); Ratna Choudhury (Department of ); K. Gadgil (Department of ); A Ganguli (Department of ); J. C. Joshi (Department of ); N. D. Kaushik (Department of ); S. S. Mathur (Physics); Subhash Chandra Mullick (Department of ); Hem Datt Panday (Department of ); B. C. Raychaudhari (Department of ); Siddavatam Ravi Prakash Reddy (Department of ); Deepak Ronanki (Department of ); S. P Sabberwal (Department of ); Y. S. Satya (Department of ); Ashok Kumar Sharma (Department of ); Durlubh Kumar Sharma (Department of ); Gopal Nath Tiwari (Department of ); S. C. Tripathi (Department of ); Ashutosh Mishra (Centre for Bio); Saranjit Singh (Civil Engineer); Arindam Banerjee (Physics); R. J. Cornish (Civil Engineer); B. M. Ahuja (Civil Engineer); K. Seetharamulu (Civil Engineer); A. K. Basu (Civil Engineer); S. K. Gulhati (Civil Engineer); Subhash Chander (Civil Engineer); T. Ramamurthy (Civil Engineer); S. Krishnamoorthy (Civil Engineer); C. S. Surana (Civil Engineer); P. Natarajan (Civil Engineer); A. Varadarajan (Civil Engineer); G. Venkatappa Rao (Civil Engineer); T. K. Datta (Civil Engineer); S. N. Sinha (Civil Engineer); Anil Sawhney (Civil Engineer); H. S. Gupta (Civil Engineer); J. M. Kate (Civil Engineer); K. K. Nayar (Civil Engineer); K. K. Gupta (Civil Engineer); Keshav Bharadwaj (Civil Engineer); M. D. Joshi (Civil Engineer); M. Raghupati (Civil Engineer); P. K. Jain (Civil Engineer); R. Kaniraj (Civil Engineer); Rajib Basu Mallick (Civil Engineer); S. Krishnamurthy (Civil Engineer); S. K. Deb (Civil Engineer); V. B. Deshpande (Civil Engineer); Kehar Singh (Physics); Ashok K. Srivastava (Biochemical En); Gopal P. Agarwal (Biochemical En); Munishwar N. Gupta (Biochemical En); Satya N. Mukhopadhyay (Biochemical En); Subhash Chand (Biochemical En); Tarun K. Ghose (Biochemical En); Virendra S. Bisaria (Biochemical En); S. C. Abbi (Physics); A. P. Kulshrestha (Physics); Manish Sharma (Physics); P. K. Aditya (Physics); L. K. Malhotra (Physics); S. D. Sharma (Physics); O. P. Agnihotri (Physics); S. C. Mathur (Physics); S. K. Sharma (Physics); A. Barman (Physics); C. L. Mehta (Physics); R. N. Singh (Physics); A. B. Bhattacharya (Physics); R. G. Mendiratta (Physics); B.(Ms) Buti (Physics); A. K. Mukhrjee (Physics); L. V. Sood (Physics); P. K. C. Pillai (Physics); Neeraj C. Srivastava (Physics); Subhash Chopra (Physics); R. K. Puri (Physics); Y. Sudhakar (Physics); D. C. Dube (Physics); S. Radhakrishna (Physics); D. P. Tewari (Physics); W. E. Duncanson (Physics); V. Ramamurthy (Physics); L. M. Tewari (Physics); A. Bhaskar. Rao (Physics); P. N. Tewari (Physics); T. C. Goel (Physics); Madan Rao (Physics); Rama Nand Tewari (Physics); I. C. Goyal (Physics); D. K. Roy (Physics); B. B. Tripathi (Physics); K. P. Jain (Physics); B. K. Sawhney (Physics); G. Umesh (Physics); Narendra Kumar Jain (Physics); H. K. Sehgal (Physics); M. P. Verma (Physics); S. C. Jain (Physics); S. B. Sharan (Physics); H. C. Gupta (Physics); P. K. Katti (Physics); G. L. Sharma (Physics); B. P. Pal (Physics); S. C. Kashyap (Physics); V. K. Tripathi (Physics); K. Thyagrajan (Physics); R. D. Tarey (Physics); R. S. Sirohi (Physics); V. D. Vankar (Physics); A. K. Tyagi (Physics); P. K. Gupta (Physics); Ravi K. Soni (Physics); M. C. Bhatnagar (Physics); Sanjay Puri (Physics); Pradeeba Sridhar (Centre for Bio); Deepak K. Agrawal (Centre for Bio); K. L. Batra (Centre for Bio); Kajzer Janusz (Centre for Bio); K. B. Sahay (Centre for Bio); N. Debnath (Centre for Bio); R. K. Saxena (Centre for Bio); Rajesh Patela (Centre for Bio); M. Seedat (Centre for Bio); Ikram Saiqa (Centre for Bio); P. K. Pradhan (Centre for Bio); S. N. Tandon (Centre for Bio); Alok Ranjan Ray (Centre for Bio); Anuradha Godavarty (Centre for Bio); Dinesh Mohan (Centre for Bio); Nivedita Gohil (Centre for Bio); Anand Sneh (Centre for Bio)
