# IIT Delhi golden set - lab notebook

Final: 213 papers (target 650 NOT reached), 41 with a printed DOI (19%). Built over two sessions (first agent hit a usage limit; this session assembled its saved work and added arXiv/news).

## Sources and yield
| source | pages/PDFs visited | rows | notes |
|---|---|---|---|
| faculty_page (own profile / homepage lists) | Mech, Chemistry, Textile dept profile pages (about 114 profiles parsed; only those with a usable joining year and list), 13 personal homepages (EE, DESE, AM, Maths, ChE, CARE), MSE faculty API | 171 | spread-sampled (evenly through newest-first lists), cap 8 per person |
| dept_page | physics.iitd.ac.in publications table (3 faculty, supervisor column) | 21 | affiliation not on table, medium |
| arxiv | 48 abs/PDF pages reached from institute/web links; first-page PDF text checked with pdftotext | 16 kept | kept only if IIT Delhi visible on page 1 of the PDF; year = arXiv id year (first version) |
| news | home.iitd.ac.in research-news items show.php?id=65..87 (23 pages) | 5 kept | institute states IIT Delhi researchers authored the paper; DOI from the article link. 9 further items had a DOI link but the publisher landing page returned HTTP 403 (Wiley/ACS/AGU), titles not obtainable without a lookup, so not included; ~8 items (Hindi mirrors, no paper link) skipped |
| annual_report | rti.iitd.ac.in annual report PDFs (AR-2024-25, AR-2021-22) | 0 | host fails with SSL error through the polite fetcher; Wayback copy of AR-2024-25 404, of AR-2021-22 returned an HTML wrapper, not the PDF. Not bypassed. |

Search strings used: site-restricted web search for the annual report; one web search to check a perovskite news item (not used for discovery of rows). Discovery otherwise by crawling institute pages.

## Tenure rule
Joining year taken from the person's own page (quoted in each row's notes) or, for Chemistry/Mech/Textile, from the dept profile page text (first IIT Delhi appointment year), manual overrides for a few profiles whose text states it differently. Roster has almost no joining years so it was not used. Only papers with year strictly after joining year are included (medium). arXiv and news rows are high (affiliation visible). Known upper-bound: none via archive snapshots were needed.

## Coverage (department x year)
| department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mechanical Engineering | 19 | 11 | 1 | 2 | 4 | 2 | 3 | 3 | 2 | 3 | 1 | 51 |
| Chemistry | 2 | 1 | 2 | 4 | 7 | 10 | 3 | 1 | 3 | 3 | 0 | 36 |
| Textile and Fibre Engineering | 8 | 3 | 4 | 1 | 5 | 2 | 3 | 3 | 0 | 0 | 0 | 29 |
| Physics | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 4 | 3 | 1 | 2 | 25 |
| Electrical Engineering | 1 | 1 | 2 | 2 | 2 | 1 | 5 | 1 | 3 | 4 | 0 | 22 |
| Materials Science and Engineering | 0 | 0 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 0 | 9 |
| Mathematics | 1 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 2 | 8 |
| Chemical Engineering | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 8 |
| Energy Science and Engineering | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 2 | 0 | 2 | 0 | 7 |
| unspecified (IIT Delhi) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 4 | 0 | 7 |
| Centre for Applied Research in Electronics | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 4 |
| Applied Mechanics | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 3 |
| School of Artificial Intelligence | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| Computer Science and Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| Centre for Biomedical Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| Civil Engineering | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

## Rejected / skipped
* arXiv candidates without IIT Delhi on PDF page 1 (about 11 of 27 with cached PDFs) - rejected as affiliation not visible; 2 had no cached PDF.
* Faculty lists with no stated joining year (about half of the Mech/Textile/Chemistry profiles) - excluded, not guessed.
* homecse.iitd.ac.in team pages (60 CSE faculty) hold no publication lists; CSE/SAI personal pages parsed noisily (news/teaching lines) and were not included beyond arXiv.
* Departments with no papers: Civil (1 news row only), Biological Sciences, Design, Management, HSS, Public Policy, CBME (1 news), CSE (1), most of SAI: personal-page extraction not completed.

## Biases
Heavy over-representation of Mechanical, Chemistry, Textile, Physics (template-style profile pages parse cleanly); CSE/AI, Civil, Management, Design, Bio under-represented. Only papers that appear on faculty pages with a stated joining year; papers by students/former faculty almost absent. arXiv/news rows skew to 2022-2026 and to groups who post preprints / get press releases. DOI coverage low because faculty lists seldom print DOIs (no lookups done). Year 2026 is partial.

## Supplement (second pass, interrupted by a session restart; target 650 NOT reached)
Final 278 rows (213 before, +65 after dropping 3 rows outside 2016-2026). Added 9 people from personal publication lists, all `faculty_page`, `medium`, cap 8 per person with even spread through the list:
CSE: Amit Kumar, Amitabha Bagchi, Srikanta Bedathur, Sorav Bansal, Preeti Ranjan Panda (news-style "Research paper X by ... published in" items), Chetan Arora (publications.html); Civil: C. T. Dhanya, Sumedha Chakma; Design: Srinivasan Venkataraman. Parsers per page format are in the work dir code2/parsers.py.
Tenure: Bansal, Dhanya, Chakma, Venkataraman from their own page (2009, Nov 2011, 2014, Oct 2017). Amit Kumar, Bagchi, Panda (2015), Bedathur, Arora (2018): first Wayback snapshot of the personal page (upper bound on joining; papers must be strictly later, which suppresses their 2016-2018 rows).
Sources visited: about 213 roster profile/homepage URLs (45 CSE team pages: navigation only, no publications), 25 guessed cse.iitd.ac.in/~user pages (about 10 with lists), cbme.iitd.ac.in/journal (88 entries, no years: unusable) and /conference, spp/bioschool research pages (no lists), Wayback front pages of civil/dms/hss/design (not mined for lists; time), AR-2018-19/2021-22/2023-24 annual-report PDFs via Wayback id_ copies: all truncated at exactly 1 MiB by the archive, pdftotext fails (no annual_report rows). scai.iitd.ac.in/publications returned HTTP 500.
Rejected: Sanjiva Prasad, Rahul Garg, Rohan Paul, Sayan Ranu pages (irregular formats, not parsed); Jyoti Kumar (Design, 91 entries but no tenure evidence, Wayback 404); Saikat Sarkar (titles not on page, only venues); Patrick Gurian/Haldar/Kodur/N.K. Garg pages (external or vidwan, not IIT Delhi lists); papers at or before joining/first-seen year.
Not covered: Management, HSS, Public Policy, Biological Sciences, Biomedical (CBME profile pages hold bios only), most of School of AI. Biases: still faculty-page heavy (about 85%), CSE theory/data/architecture over-represented among added rows, no 2018/2026 correction, no news or annual-report additions, DOIs mostly absent.


## Supplement 2 (third pass; extends the 278-row set to 504 rows; target 650 NOT reached)
Rows added: 226 (faculty_page 215, arxiv 11 net of dedupe/cap; annual_report 0; news 0). Source mix is therefore about 89 % faculty pages, 4 % dept pages, 5 % arXiv, 1 % news; the planned 15 % annual reports and 10 % news could not be filled (see below).

**Sources and yields (all fetched through polite_get.py)**
* HSS: faculty pages hss.iitd.ac.in/faculty/<slug> (host TLS broken, so Wayback 2024 copies `web.archive.org/web/2024id_/...`, 43 pages fetched, about 25 with a publication section, 13 used) -> 59 rows. Tenure from the page's own employment/CV lines (Agrawal 2013, Jayan Thomas 2010, Jogdand 2017, Anand Jul 2022, Sanyal 2012, R. Kumar 2011, Khanna 2009, V. Singh 2013, Nair >=2006, Leonard Oct 2021; Khera only 2021+ because she was at IIM Ahmedabad 2018-20, yielded 0). HSS entries of types talk/newspaper/submitted/invited were dropped by regex; some conference-presentation rows remain.
* Management (DMS): dms.iitd.ac.in profile pages (TLS broken, Wayback) hold bios only; /faculty-publications lists only books and papers up to 2015; Ravi Shankar's lists stop in 2015-2017. Only P. Vigneswara Ilavarasan's own page (at IIT Delhi since 2005) gave usable lists: 8 rows (his 2019 entries; "forthcoming" items skipped).
* CSE/SAI: personal pages of Sayan Ranu (HTML articles), Smruti Sarangi (J/C-numbered list), Rohan Paul, Mausam (publications.html from the "Refereed Journal Articles" heading on, talks/tutorials/videos excluded). Tenure: first Wayback snapshot of the page (Ranu 2017, Sarangi 2014, Paul 2021, Mausam 2014), an upper bound on joining, so earlier papers are suppressed (Paul's rows are 2022+). Written parsers: code2/p3.py (scratchpad work dir). scai.iitd.ac.in/publications: HTTP 500 live and no Wayback copy; no SAI-wide list exists, SAI rows come from member pages and arXiv.
* EE/Energy/Civil/Maths/MSE/Biology/Biomedical personal pages, discovered by following the "Publications" link from the roster homepages (about 95 pages checked) and by 8 web searches restricted to iitd domains: Swades De (2007), Brejesh Lall (2019), A. Chattopadhyay (2019), R. Palani (2020), G. Ghatak (2021), A. Singhal (2018), Tanmoy Chakraborty (own CV: Associate Professor IIT Delhi from 8 Sep 2022; 2023+ only), R. Mohanty (own page: IIT Delhi 2023-present), Subrat Kar (since 1994), D. Rakshit (2017), Vipin Kumar (2022), D. R. Sahoo (2011), G. Habib (2013), N. Chatterjee (2008), J. Jain (2013), Neetu Singh (CBME, April 2014 from own page), A. Kalra (CBME, joined Sep 2023 per own page; "before joining" list excluded), T. K. Chaudhuri (2016), V. Perumal (2015); years in brackets are the joining/first-snapshot year used (first-snapshot years are upper bounds).
* Biomedical (CBME): the 88-paper cbme.iitd.ac.in/journal list prints no years and was not used; instead 5 lab/personal sites (above) -> 13 rows in total. Public Policy: no publication lists found on spp pages or via search; 0 rows. Biological Sciences: 8 rows (Perumal), Chaudhuri filed under the roster label Biochemical Engineering and Biotechnology (8 rows).
* arXiv (web search restricted to arxiv.org, then abs/PDF via the fetcher, 15 s spacing): 22 PDFs read, 15 show IIT Delhi on page 1 (high; 1 via an e-mail footnote @ee.iitd.ac.in), of which 14 were new (Civil 5, CSE 3, Applied Mechanics 2, SAI 1, EE 1, other 1); rejected: 2202.01585 (IIT Roorkee), 2205.05360 (no IIT Delhi on page 1), 2203.04159, 2102.12362, 2212.04645, 2101.08996, 2001.09182 (no affiliation on page 1). Year = first-version year from the arXiv id.
* Annual reports: the 1 MiB truncation came from the specific Wayback timestamps. A CDX listing (`web.archive.org/cdx/search/cdx?url=...&fl=timestamp,statuscode,length`) shows another capture of AR-2018-19E.pdf (20220320115834) that is complete (152 pages, 4.9 MB, pdftotext works). It contains only aggregate counts ("51 journal papers..." / Scopus counts), per-department activity text and award lists, and NO per-paper publication lists, so annual reports yield 0 rows. The other years' reports were not re-fetched after this finding.
* News: home.iitd.ac.in/news-all.php (876 items) and research-all.php (23 research stories, already mined in pass 1): headings are mostly programmes/MoUs/events; no additional titled papers; 0 rows added.

**Rejected / skipped**: Pradipta Mukherjee (BioPhotonica lab, no joining year), Aayush Kant, B. Mukherjee, S. Jha, K. K. Deepak, N. K. Singh, J. Bhattacharyya, M. Menon, Tapan Nayak (no tenure statement or only 1-2 entries); EE/Energy/AM people with long lists but no joining year or Wayback snapshot (Sreyam Sinha, Yashasvi Bansal, Krishan Kant, Kaushalya Jhuria, S. Sundeep, R. Goyal, B. Sahu, S. Panigrahy, T. Singh, N. K. Jha, A. Mishra's lab, R. Nayek) and Arihant Bhandari (first snapshot 2025); Kodamana, S. Basu, A. Ganguli, S. P. Singh pages (formats not parsed); Reetika Khera (format not parsed). Dropped rows: obvious non-papers in HSS lists (grants, talks, conference presentations), duplicates of earlier titles, rows beyond the 8-per-person cap.

**Known problems**: titles/venues parsed by regex from free-text lists; a few venue fields still contain author names (Brejesh Lall) or truncated text. First-snapshot tenure is an upper bound, so some valid early papers are excluded, while 'faculty_page' rows remain `medium` (affiliation not printed). Brejesh Lall, Chattopadhyay, Rohan Paul rows are therefore 2020+. The DOIs are only those printed on the list line (about 13 % of rows).

**Coverage after this pass (department x year)**
| department | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Electrical Engineering | 2 | 1 | 2 | 5 | 8 | 5 | 12 | 9 | 11 | 11 | 9 | 75 |
| Computer Science and Engineering | 1 | 3 | 1 | 5 | 5 | 3 | 13 | 8 | 11 | 8 | 14 | 72 |
| Humanities and Social Sciences | 9 | 8 | 6 | 4 | 5 | 2 | 5 | 9 | 6 | 0 | 0 | 54 |
| Mechanical Engineering | 19 | 11 | 1 | 2 | 4 | 2 | 3 | 3 | 2 | 3 | 1 | 51 |
| Chemistry | 2 | 1 | 2 | 4 | 7 | 10 | 3 | 1 | 3 | 3 | 0 | 36 |
| Civil Engineering | 1 | 3 | 5 | 1 | 0 | 2 | 2 | 3 | 6 | 7 | 5 | 35 |
| Textile and Fibre Engineering | 8 | 3 | 4 | 1 | 5 | 2 | 3 | 3 | 0 | 0 | 0 | 29 |
| Energy Science and Engineering | 0 | 1 | 1 | 1 | 2 | 3 | 2 | 5 | 3 | 4 | 3 | 25 |
| Physics | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 4 | 3 | 1 | 2 | 25 |
| Mathematics | 2 | 1 | 3 | 2 | 1 | 2 | 1 | 1 | 0 | 1 | 2 | 16 |
| Materials Science and Engineering | 1 | 3 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 0 | 14 |
| Centre for Biomedical Engineering | 0 | 0 | 0 | 0 | 2 | 3 | 3 | 0 | 2 | 1 | 2 | 13 |
| Chemical Engineering | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 8 |
| unspecified (IIT Delhi) | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 2 | 1 | 4 | 0 | 8 |
| Design | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 2 | 1 | 2 | 8 |
| Management Studies | 1 | 2 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| Biochemical Engineering and Biotechnology | 0 | 0 | 2 | 2 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 8 |
| School of Biological Sciences | 0 | 0 | 0 | 2 | 0 | 0 | 2 | 1 | 1 | 2 | 0 | 8 |
| Applied Mechanics | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 2 | 5 |
| Centre for Applied Research in Electronics | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 4 |
| School of Artificial Intelligence | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| Yardi School of Artificial Intelligence | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |

**Biases (updated)**: faculty-page share rose to about 89 %; EE/CSE/HSS/Civil now fuller, but Management (8), Public Policy (0), SAI (2), Applied Mechanics (5), Chemical Engineering (8), Design (8) remain thin; 2016-2018 still under-represented (50/41/37 vs ~55 for 2022-2024) because tenure lower bounds exclude them. High-confidence rows are only the 32 arXiv/news ones.
